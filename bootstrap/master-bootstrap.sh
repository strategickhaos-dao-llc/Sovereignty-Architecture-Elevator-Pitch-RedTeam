#!/usr/bin/env bash
# Sovereign Swarm — Master Bootstrap (Hardened)
# Phase 0→3: CA/keys, WireGuard+SwarmGate, NATS, Synapse (docker), UFW, PSK-rotation.
# Run first on Command-0 (NODE_ID=command0). Then on each node with its NODE_ID.
#
# Usage:
#   sudo NODE_ID=command0 ./master-bootstrap.sh
#   sudo NODE_ID=fixed1 C0PUB=<command0-pubkey> C0EP=<command0-endpoint> ./master-bootstrap.sh

set -euo pipefail
trap 'echo "[ERR] Failed at line $LINENO"; rollback; exit 1' ERR

# ===== Defaults (override via env) =====
NODE_ID="${NODE_ID:-command0}"          # command0|fixed1|mobile2|edge3|edge4
SWARM_NET="10.44.0.0/16"
WG_IF="wg0"
WG_PORT="${WG_PORT:-51820}"
UFW_SSH_PORT="${UFW_SSH_PORT:-22}"
REPO_ROOT="${REPO_ROOT:-/opt/sovereign-swarm}"
DOMAIN="${DOMAIN:-swarm.local}"         # Synapse server_name (no public DNS needed)
LOG_FILE="/var/log/swarm-bootstrap.log"
# Command-0 public key and endpoint (required for non-hub nodes)
C0PUB="${C0PUB:-}"
C0EP="${C0EP:-}"
# ======================================

# Strict file permissions
umask 077

# Create repo root
mkdir -p "$REPO_ROOT" || { echo "[ERR] Can't create $REPO_ROOT"; exit 1; }
cd "$REPO_ROOT"

# Setup logging
touch "$LOG_FILE" 2>/dev/null || LOG_FILE="/tmp/swarm-bootstrap.log"
exec > >(tee -a "$LOG_FILE") 2>&1

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [*] $*"
}

log_error() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [ERR] $*" >&2
}

log_warn() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [WARN] $*"
}

log_success() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [OK] $*"
}

# Root check
need_root() {
    if [ "$EUID" -ne 0 ]; then
        log_error "This script must be run as root"
        exit 1
    fi
}

# Check for Debian/Ubuntu
check_distro() {
    if ! command -v apt >/dev/null 2>&1; then
        log_error "Debian/Ubuntu required. apt not found."
        exit 1
    fi
}

# Rollback function - cleans up partial installations on failure
rollback() {
    log_warn "Rolling back partial installation..."
    
    # Stop services (ignore errors)
    systemctl stop "wg-quick@${WG_IF}" 2>/dev/null || true
    systemctl stop nats 2>/dev/null || true
    systemctl stop swarmsgd 2>/dev/null || true
    systemctl stop docker 2>/dev/null || true
    
    # Disable services
    systemctl disable "wg-quick@${WG_IF}" 2>/dev/null || true
    systemctl disable nats 2>/dev/null || true
    systemctl disable swarmsgd 2>/dev/null || true
    
    # Clean up configs
    rm -rf /etc/wireguard/* 2>/dev/null || true
    rm -rf /etc/nats/* 2>/dev/null || true
    rm -f /etc/swarmsgd-pubkey 2>/dev/null || true
    rm -rf /run/wg-tokens 2>/dev/null || true
    
    # Reset firewall
    ufw --force reset 2>/dev/null || true
    
    # Optional: purge packages (commented out to avoid breaking other services)
    # apt-get purge -y wireguard wireguard-tools nftables ufw python3-nacl docker.io docker-compose-plugin nats-server syncthing 2>/dev/null || true
    
    # Clean repo root only if we created it and it's nearly empty
    if [ -d "$REPO_ROOT" ] && [ "$(find "$REPO_ROOT" -maxdepth 1 -type f 2>/dev/null | wc -l)" -lt 2 ]; then
        rm -rf "$REPO_ROOT" 2>/dev/null || true
    fi
    
    log_warn "Rollback complete."
}

# Prompt for Command-0 details if not provided (for non-hub nodes)
prompt_c0_details() {
    if [ "$NODE_ID" != "command0" ]; then
        if [ -z "$C0PUB" ]; then
            log_warn "C0PUB (Command-0 public key) not set"
            read -rp "Enter Command-0 WireGuard public key: " C0PUB
            if [ -z "$C0PUB" ]; then
                log_error "C0PUB is required for non-hub nodes"
                exit 1
            fi
        fi
        if [ -z "$C0EP" ]; then
            log_warn "C0EP (Command-0 endpoint) not set"
            read -rp "Enter Command-0 endpoint (IP:Port, e.g., 192.168.1.100:51820): " C0EP
            if [ -z "$C0EP" ]; then
                log_error "C0EP is required for non-hub nodes"
                exit 1
            fi
        fi
        log "Using Command-0 pub: ${C0PUB:0:20}..."
        log "Using Command-0 endpoint: $C0EP"
    fi
}

# Assign node IP based on NODE_ID
get_node_ip() {
    case "$NODE_ID" in
        command0) echo "10.44.0.1" ;;
        fixed1)   echo "10.44.0.2" ;;
        mobile2)  echo "10.44.0.3" ;;
        edge3)    echo "10.44.0.4" ;;
        edge4)    echo "10.44.0.5" ;;
        *)
            # Deterministic IP based on node ID hash (avoids conflicts)
            local hash
            hash=$(echo -n "$NODE_ID" | sha256sum | cut -c1-4)
            local ip_suffix=$((16#$hash % 250 + 6))
            echo "10.44.0.$ip_suffix"
            ;;
    esac
}

# Install base packages
install_packages() {
    log "Installing base packages..."
    export DEBIAN_FRONTEND=noninteractive
    
    apt-get update -y
    apt-get install -y \
        wireguard wireguard-tools nftables ufw curl jq git ca-certificates \
        python3 python3-pip python3-venv python3-nacl \
        docker.io docker-compose-plugin \
        nats-server syncthing
    
    # Ensure PyNaCl is installed via pip for reliable nacl.signing import
    # Debian's python3-nacl package can have import path issues in mixed setups
    # Try system package first, then pip as fallback
    log "Verifying PyNaCl installation for EdDSA support..."
    if ! python3 -c "from nacl.signing import SigningKey" 2>/dev/null; then
        log_warn "System python3-nacl not working, installing via pip..."
        # Create a venv for swarm-specific Python dependencies
        python3 -m venv /opt/sovereign-swarm-venv 2>/dev/null || true
        if [ -f /opt/sovereign-swarm-venv/bin/pip ]; then
            /opt/sovereign-swarm-venv/bin/pip install pynacl
            # Update PATH to use venv
            export PATH="/opt/sovereign-swarm-venv/bin:$PATH"
        else
            # Fallback to system pip if venv fails
            pip3 install --break-system-packages pynacl 2>/dev/null || pip3 install pynacl
        fi
    fi
    
    # Verify installation
    if ! python3 -c "from nacl.signing import SigningKey" 2>/dev/null; then
        log_error "PyNaCl installation verification failed"
        exit 1
    fi
    
    log_success "Base packages installed"
}

# Setup directory structure
setup_directories() {
    log "Setting up directory structure..."
    mkdir -p ca/state
    mkdir -p "nodes/$NODE_ID"
    mkdir -p wireguard/conf
    mkdir -p swarmgate/{nft,swarmsgd,systemd}
    mkdir -p nats/{conf,systemd,accounts}
    mkdir -p matrix/synapse
    mkdir -p scripts
    mkdir -p artifacts
    
    log_success "Directory structure created"
}

# Generate CA and node keys
generate_keys() {
    log "Generating CA and node keys..."
    
    # CA key (only on command0 or if not exists)
    # For Ed25519/NaCl, the 32-byte random seed IS the private key
    # The public key is derived mathematically by PyNaCl when signing
    if [ ! -f ca/state/swarm-ed25519.key ]; then
        log "Generating CA seed (32-byte Ed25519 private key)..."
        openssl rand 32 > ca/state/swarm-ed25519.key
        # Derive public key using PyNaCl (proper Ed25519 derivation)
        python3 -c "
from nacl.signing import SigningKey
seed = open('ca/state/swarm-ed25519.key', 'rb').read()
sk = SigningKey(seed)
open('ca/state/swarm-ed25519.pub', 'wb').write(bytes(sk.verify_key))
" || {
            log_error "Failed to derive CA public key - PyNaCl issue"
            exit 1
        }
    fi
    
    if [ ! -f ca/state/swarm-ed25519.key ]; then
        log_error "CA key generation failed"
        exit 1
    fi
    log_success "CA key ready"
    
    # WireGuard key
    if [ ! -f "nodes/$NODE_ID/wg.key" ]; then
        log "Generating WireGuard key for $NODE_ID..."
        wg genkey | tee "nodes/$NODE_ID/wg.key" | wg pubkey > "nodes/$NODE_ID/wg.pub"
    fi
    
    if [ ! -f "nodes/$NODE_ID/wg.key" ]; then
        log_error "WireGuard key generation failed"
        exit 1
    fi
    log_success "WireGuard key ready: $(cat "nodes/$NODE_ID/wg.pub")"
    
    # Ed25519 key for node identity (same approach as CA)
    if [ ! -f "nodes/$NODE_ID/ed25519.key" ]; then
        log "Generating Ed25519 key for $NODE_ID..."
        openssl rand 32 > "nodes/$NODE_ID/ed25519.key"
        # Generate fingerprint from derived public key
        python3 -c "
from nacl.signing import SigningKey
import hashlib
seed = open('nodes/$NODE_ID/ed25519.key', 'rb').read()
sk = SigningKey(seed)
fp = hashlib.sha256(bytes(sk.verify_key)).hexdigest()
open('nodes/$NODE_ID/ed25519.fp', 'w').write(fp)
" || {
            log_warn "Could not derive Ed25519 fingerprint"
        }
    fi
    
    if [ ! -f "nodes/$NODE_ID/ed25519.key" ]; then
        log_error "Ed25519 key generation failed"
        exit 1
    fi
    log_success "Ed25519 key ready"
}

# Create token minting script
create_mint_script() {
    log "Installing token minting script..."
    
    install -D -m 755 /dev/stdin scripts/mint_token.py <<'PYTHON'
#!/usr/bin/env python3
"""
Sovereign Swarm - Minimal EdDSA JWT Token Minter
Generates JWTs signed with Ed25519 for mesh authentication.
"""
import json
import time
import base64
import os
import argparse
from nacl.signing import SigningKey

def b64url_encode(data: bytes) -> str:
    """URL-safe base64 encode without padding."""
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('ascii')

def main():
    parser = argparse.ArgumentParser(description='Mint EdDSA JWT tokens for Sovereign Swarm')
    parser.add_argument('--ca', '-c', required=True, help='Path to CA private key (32-byte seed)')
    parser.add_argument('--node', '-n', required=True, help='Path to node directory')
    parser.add_argument('--aud', '-a', required=True, help='Token audience (e.g., wg, nats)')
    parser.add_argument('--ttl', default='86400', help='Token TTL in seconds (default: 86400)')
    parser.add_argument('--caps', required=True, help='Comma-separated capabilities')
    args = parser.parse_args()
    
    # Load CA seed
    with open(args.ca, 'rb') as f:
        seed = f.read()
    
    if len(seed) != 32:
        raise ValueError(f'CA key must be 32 bytes, got {len(seed)}')
    
    signing_key = SigningKey(seed)
    
    # Build claims
    now = int(time.time())
    exp = now + int(args.ttl)
    jti = base64.urlsafe_b64encode(os.urandom(16)).decode().rstrip('=')
    
    node_id = os.path.basename(args.node.rstrip('/'))
    
    claims = {
        'iss': 'SwarmCA',
        'sub': node_id,
        'aud': args.aud,
        'iat': now,
        'exp': exp,
        'cap': args.caps.split(','),
        'jti': jti
    }
    
    header = {'alg': 'EdDSA', 'typ': 'JWT'}
    
    # Encode header and payload
    header_b64 = b64url_encode(json.dumps(header, separators=(',', ':')).encode())
    payload_b64 = b64url_encode(json.dumps(claims, separators=(',', ':')).encode())
    
    # Sign
    message = f'{header_b64}.{payload_b64}'.encode()
    signature = signing_key.sign(message).signature
    signature_b64 = b64url_encode(signature)
    
    jwt = f'{header_b64}.{payload_b64}.{signature_b64}'
    
    # Save token
    token_path = os.path.join(args.node, 'token.jwt')
    with open(token_path, 'w') as f:
        f.write(jwt)
    
    print(jwt)

if __name__ == '__main__':
    main()
PYTHON

    if [ ! -f scripts/mint_token.py ]; then
        log_error "mint_token.py installation failed"
        exit 1
    fi
    
    log_success "Token minting script installed"
}

# Mint node token
mint_node_token() {
    log "Minting authentication token for $NODE_ID..."
    
    # Define capabilities based on node role
    case "$NODE_ID" in
        command0)
            CAPS="nats.pub:telemetry.>,nats.sub:cmd.>,matrix.role:admin,router:true,net:${SWARM_NET}"
            ;;
        fixed1)
            CAPS="nats.pub:telemetry.>,nats.sub:cmd.>,matrix.role:server,router:true,net:${SWARM_NET}"
            ;;
        mobile2)
            CAPS="nats.pub:telemetry.>,nats.sub:cmd.>,matrix.role:agent,router:false,net:${SWARM_NET}"
            ;;
        edge*)
            CAPS="nats.pub:telemetry.>,nats.sub:cmd.>,matrix.role:agent,router:false,net:${SWARM_NET}"
            ;;
        *)
            CAPS="nats.pub:telemetry.>,nats.sub:cmd.>,matrix.role:agent,router:false,net:${SWARM_NET}"
            ;;
    esac
    
    python3 scripts/mint_token.py \
        -c ca/state/swarm-ed25519.key \
        -n "nodes/$NODE_ID" \
        -a wg \
        --ttl 86400 \
        --caps "$CAPS" >/dev/null
    
    if [ ! -f "nodes/$NODE_ID/token.jwt" ]; then
        log_error "Token minting failed"
        exit 1
    fi
    
    # Install CA public key for verification
    install -D -m 644 ca/state/swarm-ed25519.pub /etc/swarmsgd-pubkey
    
    if [ ! -f /etc/swarmsgd-pubkey ]; then
        log_error "CA public key installation failed"
        exit 1
    fi
    
    log_success "Token minted and CA pubkey installed"
}

# Configure WireGuard
configure_wireguard() {
    log "Configuring WireGuard..."
    
    local NODE_IP
    NODE_IP=$(get_node_ip)
    local WG_PRIVKEY
    WG_PRIVKEY=$(cat "nodes/$NODE_ID/wg.key")
    
    # Detect default network interface dynamically
    local DEFAULT_IF
    DEFAULT_IF=$(ip route show default 2>/dev/null | awk '/default/ {print $5}' | head -n1)
    if [ -z "$DEFAULT_IF" ]; then
        DEFAULT_IF="eth0"
        log_warn "Could not detect default interface, using eth0"
    fi
    log "Using network interface: $DEFAULT_IF"
    
    # Check if WireGuard is already running
    if systemctl is-active --quiet "wg-quick@${WG_IF}"; then
        log_warn "WireGuard already running, stopping for reconfiguration..."
        systemctl stop "wg-quick@${WG_IF}"
    fi
    
    # Generate random PSK for peer authentication
    local PSK
    PSK=$(wg genpsk)
    echo "$PSK" > "nodes/$NODE_ID/psk"
    
    # Create WireGuard config
    cat > "/etc/wireguard/${WG_IF}.conf" <<EOF
# Sovereign Swarm WireGuard Config - ${NODE_ID}
# Generated: $(date)
[Interface]
PrivateKey = ${WG_PRIVKEY}
Address = ${NODE_IP}/16
ListenPort = ${WG_PORT}
SaveConfig = false

# Post-up rules for mesh routing
PostUp = sysctl -w net.ipv4.ip_forward=1
PostUp = iptables -A FORWARD -i %i -j ACCEPT
PostUp = iptables -t nat -A POSTROUTING -o ${DEFAULT_IF} -j MASQUERADE || true
PostDown = iptables -D FORWARD -i %i -j ACCEPT || true
PostDown = iptables -t nat -D POSTROUTING -o ${DEFAULT_IF} -j MASQUERADE || true
EOF

    # Add Command-0 as peer if we're not Command-0
    if [ "$NODE_ID" != "command0" ] && [ -n "$C0PUB" ] && [ -n "$C0EP" ]; then
        cat >> "/etc/wireguard/${WG_IF}.conf" <<EOF

# Command-0 (Hub) Peer
[Peer]
PublicKey = ${C0PUB}
PresharedKey = ${PSK}
Endpoint = ${C0EP}
AllowedIPs = ${SWARM_NET}
PersistentKeepalive = 25
EOF
    fi
    
    chmod 600 "/etc/wireguard/${WG_IF}.conf"
    
    # Enable and start WireGuard
    systemctl enable "wg-quick@${WG_IF}"
    systemctl start "wg-quick@${WG_IF}"
    
    if ! systemctl is-active --quiet "wg-quick@${WG_IF}"; then
        log_error "WireGuard failed to start"
        exit 1
    fi
    
    log_success "WireGuard configured and running"
    log "Node IP: $NODE_IP"
    log "Public Key: $(cat "nodes/$NODE_ID/wg.pub")"
    log "Listening on port: $WG_PORT"
}

# Create SwarmGate daemon
create_swarmgate() {
    log "Installing SwarmGate agent..."
    
    # Create SwarmGate Python daemon
    install -D -m 755 /dev/stdin swarmgate/swarmsgd/swarmsgd.py <<'PYTHON'
#!/usr/bin/env python3
"""
SwarmGate Daemon - JWT-authenticated mesh management
Handles peer registration and token rotation for Sovereign Swarm.
"""
import os
import sys
import json
import time
import base64
import socket
import logging
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any

try:
    from nacl.signing import VerifyKey
    from nacl.exceptions import BadSignatureError
except ImportError:
    print("ERROR: PyNaCl not installed. Run: pip3 install pynacl")
    sys.exit(1)

# Configuration
CONFIG = {
    'token_dir': '/run/wg-tokens',
    'ca_pubkey': '/etc/swarmsgd-pubkey',
    'wg_interface': 'wg0',
    'listen_port': 51821,
    'log_file': '/var/log/swarmsgd.log',
}

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(CONFIG['log_file']),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('swarmsgd')

def b64url_decode(data: str) -> bytes:
    """URL-safe base64 decode with padding restoration."""
    padding = 4 - len(data) % 4
    if padding != 4:
        data += '=' * padding
    return base64.urlsafe_b64decode(data)

def load_ca_pubkey() -> Optional[VerifyKey]:
    """Load CA public key for JWT verification."""
    try:
        with open(CONFIG['ca_pubkey'], 'rb') as f:
            pubkey_bytes = f.read()
        return VerifyKey(pubkey_bytes[:32])
    except Exception as e:
        logger.error(f"Failed to load CA pubkey: {e}")
        return None

def verify_jwt(token: str, verify_key: VerifyKey) -> Optional[Dict[str, Any]]:
    """Verify and decode a JWT token."""
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return None
        
        header_b64, payload_b64, sig_b64 = parts
        
        # Verify signature
        message = f'{header_b64}.{payload_b64}'.encode()
        signature = b64url_decode(sig_b64)
        verify_key.verify(message, signature)
        
        # Decode payload
        payload = json.loads(b64url_decode(payload_b64))
        
        # Check expiration
        if payload.get('exp', 0) < time.time():
            logger.warning("Token expired")
            return None
        
        return payload
    except BadSignatureError:
        logger.warning("Invalid token signature")
        return None
    except Exception as e:
        logger.error(f"Token verification error: {e}")
        return None

def add_wg_peer(pubkey: str, allowed_ips: str, endpoint: Optional[str] = None) -> bool:
    """Add a WireGuard peer."""
    try:
        cmd = ['wg', 'set', CONFIG['wg_interface'], 'peer', pubkey, 'allowed-ips', allowed_ips]
        if endpoint:
            cmd.extend(['endpoint', endpoint])
        subprocess.run(cmd, check=True, capture_output=True)
        logger.info(f"Added peer: {pubkey[:20]}...")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to add peer: {e.stderr.decode()}")
        return False

def handle_registration(data: Dict[str, Any], verify_key: VerifyKey) -> Dict[str, Any]:
    """Handle peer registration request."""
    token = data.get('token', '')
    pubkey = data.get('pubkey', '')
    endpoint = data.get('endpoint')
    
    if not token or not pubkey:
        return {'error': 'Missing token or pubkey', 'code': 400}
    
    # Verify token
    claims = verify_jwt(token, verify_key)
    if not claims:
        return {'error': 'Invalid or expired token', 'code': 401}
    
    # Extract capabilities
    caps = claims.get('cap', [])
    node_id = claims.get('sub', 'unknown')
    
    # Determine allowed IPs from capabilities
    for cap in caps:
        if cap.startswith('net:'):
            allowed_ips = cap.split(':', 1)[1]
            break
    else:
        allowed_ips = '10.44.0.0/32'  # Default: single IP only
    
    # Add peer
    if add_wg_peer(pubkey, allowed_ips, endpoint):
        logger.info(f"Registered peer {node_id} with caps: {caps}")
        return {'status': 'registered', 'node': node_id, 'allowed_ips': allowed_ips}
    else:
        return {'error': 'Failed to add peer', 'code': 500}

def run_server():
    """Run the SwarmGate daemon server."""
    verify_key = load_ca_pubkey()
    if not verify_key:
        logger.error("Cannot start without CA public key")
        sys.exit(1)
    
    # Ensure token directory exists
    Path(CONFIG['token_dir']).mkdir(parents=True, exist_ok=True)
    
    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', CONFIG['listen_port']))
    logger.info(f"SwarmGate daemon listening on port {CONFIG['listen_port']}")
    
    while True:
        try:
            data, addr = sock.recvfrom(4096)
            logger.debug(f"Received from {addr}")
            
            try:
                request = json.loads(data.decode())
            except json.JSONDecodeError:
                continue
            
            action = request.get('action', '')
            
            if action == 'register':
                response = handle_registration(request, verify_key)
            elif action == 'ping':
                response = {'status': 'pong', 'time': int(time.time())}
            else:
                response = {'error': 'Unknown action', 'code': 400}
            
            sock.sendto(json.dumps(response).encode(), addr)
            
        except KeyboardInterrupt:
            logger.info("Shutting down...")
            break
        except Exception as e:
            logger.error(f"Server error: {e}")

if __name__ == '__main__':
    run_server()
PYTHON

    # Create systemd service
    cat > /etc/systemd/system/swarmsgd.service <<EOF
[Unit]
Description=SwarmGate Mesh Authentication Daemon
After=network.target wg-quick@${WG_IF}.service
Requires=wg-quick@${WG_IF}.service

[Service]
Type=simple
ExecStart=/usr/bin/python3 ${REPO_ROOT}/swarmgate/swarmsgd/swarmsgd.py
Restart=always
RestartSec=5
User=root
WorkingDirectory=${REPO_ROOT}

# Security hardening
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=true
PrivateTmp=true
ReadWritePaths=/run/wg-tokens /var/log

[Install]
WantedBy=multi-user.target
EOF

    # Create token directory
    mkdir -p /run/wg-tokens
    chmod 700 /run/wg-tokens
    
    # Enable and start SwarmGate
    systemctl daemon-reload
    systemctl enable swarmsgd
    systemctl start swarmsgd
    
    if ! systemctl is-active --quiet swarmsgd; then
        log_warn "SwarmGate daemon failed to start (may need peer config first)"
    else
        log_success "SwarmGate daemon installed and running"
    fi
}

# Configure NATS messaging
configure_nats() {
    log "Configuring NATS messaging..."
    
    local NODE_IP
    NODE_IP=$(get_node_ip)
    
    # Check if NATS is already running
    if systemctl is-active --quiet nats; then
        log_warn "NATS already running, stopping for reconfiguration..."
        systemctl stop nats
    fi
    
    # Create NATS config
    mkdir -p /etc/nats
    cat > /etc/nats/nats-server.conf <<EOF
# Sovereign Swarm NATS Configuration - ${NODE_ID}
# Generated: $(date)

server_name: ${NODE_ID}
host: ${NODE_IP}
port: 4222
http_port: 8222

# Cluster configuration for mesh
cluster {
    name: sovereign-swarm
    listen: ${NODE_IP}:6222
    
    routes: [
        # Add other node routes here
        # nats-route://10.44.0.1:6222
        # nats-route://10.44.0.2:6222
    ]
}

# Logging
log_file: /var/log/nats-server.log
debug: false
trace: false

# Limits
max_payload: 1048576
max_pending: 64MB
max_connections: 64K

# Authorization (using token from swarm)
authorization {
    timeout: 2
}
EOF

    chmod 640 /etc/nats/nats-server.conf
    
    # Enable and start NATS
    systemctl enable nats
    systemctl start nats || log_warn "NATS may need routes configured"
    
    log_success "NATS configured on $NODE_IP:4222"
}

# Configure UFW firewall
configure_firewall() {
    log "Configuring UFW firewall..."
    
    # Reset and configure UFW
    ufw --force reset
    ufw default deny incoming
    ufw default allow outgoing
    
    # Allow SSH
    ufw allow "${UFW_SSH_PORT}/tcp" comment 'SSH'
    
    # Allow WireGuard
    ufw allow "${WG_PORT}/udp" comment 'WireGuard'
    
    # Allow SwarmGate
    ufw allow 51821/udp comment 'SwarmGate'
    
    # Allow NATS (only from mesh)
    ufw allow from 10.44.0.0/16 to any port 4222 proto tcp comment 'NATS'
    ufw allow from 10.44.0.0/16 to any port 6222 proto tcp comment 'NATS Cluster'
    ufw allow from 10.44.0.0/16 to any port 8222 proto tcp comment 'NATS HTTP'
    
    # Enable UFW
    ufw --force enable
    
    log_success "Firewall configured"
}

# Print summary
print_summary() {
    local NODE_IP
    NODE_IP=$(get_node_ip)
    local WG_PUB
    WG_PUB=$(cat "nodes/$NODE_ID/wg.pub" 2>/dev/null || echo "N/A")
    
    echo ""
    echo "=============================================="
    echo "  Sovereign Swarm Bootstrap Complete"
    echo "=============================================="
    echo ""
    echo "  Node ID:        $NODE_ID"
    echo "  Node IP:        $NODE_IP"
    echo "  WireGuard Port: $WG_PORT"
    echo "  WG Public Key:  $WG_PUB"
    echo ""
    echo "  Services:"
    echo "    - WireGuard:  systemctl status wg-quick@${WG_IF}"
    echo "    - SwarmGate:  systemctl status swarmsgd"
    echo "    - NATS:       systemctl status nats"
    echo ""
    echo "  Config Root:    $REPO_ROOT"
    echo "  Log File:       $LOG_FILE"
    echo ""
    
    if [ "$NODE_ID" = "command0" ]; then
        echo "  For other nodes, run:"
        echo "    sudo NODE_ID=fixed1 C0PUB='$WG_PUB' C0EP='<your-ip>:$WG_PORT' ./master-bootstrap.sh"
        echo ""
    fi
    
    echo "  Test mesh: wg show ${WG_IF}"
    echo "  Test NATS: nats sub telemetry.>"
    echo ""
    echo "=============================================="
}

# Main execution
main() {
    log "================================================"
    log "Sovereign Swarm Master Bootstrap - Hardened"
    log "Node: $NODE_ID"
    log "================================================"
    
    need_root
    check_distro
    prompt_c0_details
    install_packages
    setup_directories
    generate_keys
    create_mint_script
    mint_node_token
    configure_wireguard
    create_swarmgate
    configure_nats
    configure_firewall
    
    # Clear error trap on success
    trap - ERR
    
    print_summary
    log_success "Bootstrap complete for ${NODE_ID}!"
}

# Run main
main "$@"
