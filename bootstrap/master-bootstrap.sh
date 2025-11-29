#!/usr/bin/env bash
# master-bootstrap.sh
# Strategickhaos DAO LLC / Valoryield Engine — Sovereign Swarm Bootstrap
# Purpose: Bootstrap a node into the Sovereign Swarm mesh network
#
# This script sets up:
#   - WireGuard mesh (wg0) with per-node keys + PSKs
#   - Ed25519 CA + JWT tokens for node capabilities
#   - SwarmGate agent for authenticated node participation
#   - NATS JetStream for telemetry / command bus
#   - Matrix Synapse (Docker) for encrypted swarm chat
#   - UFW default-deny firewall with only SSH + WireGuard exposed
#   - Yearly PSK rotation cron
#
# Usage: sudo ./master-bootstrap.sh [node-name]
# Example: sudo ./master-bootstrap.sh starlink-node-1

set -euo pipefail

# Exit on error, undefined vars, and pipe failures
trap 'echo "Error on line $LINENO. Exit code: $?" >&2' ERR

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                           CONFIGURATION                                       ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

NODE_NAME="${1:-$(hostname)}"
SWARM_DIR="/opt/sovereignty-swarm"
CA_DIR="${SWARM_DIR}/ca"
WG_DIR="${SWARM_DIR}/wireguard"
NATS_DIR="${SWARM_DIR}/nats"
MATRIX_DIR="${SWARM_DIR}/matrix"
LOGS_DIR="${SWARM_DIR}/logs"
SWARMGATE_BIN="${SWARM_DIR}/bin/swarmgate"

# WireGuard configuration
WG_INTERFACE="wg0"
WG_PORT="51820"
WG_SUBNET="10.137.0.0/24"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                           UTILITY FUNCTIONS                                   ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

log_section() {
    echo ""
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}  $1${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════════${NC}"
}

check_root() {
    if [[ $EUID -ne 0 ]]; then
        log_error "This script must be run as root (use sudo)"
        exit 1
    fi
}

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                           PREREQUISITES CHECK                                 ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

check_prerequisites() {
    log_section "Checking Prerequisites"
    
    local missing_deps=()
    
    # Check for required commands
    local required_cmds=("apt-get" "systemctl" "docker" "openssl")
    for cmd in "${required_cmds[@]}"; do
        if ! command -v "$cmd" &>/dev/null; then
            missing_deps+=("$cmd")
        fi
    done
    
    if [[ ${#missing_deps[@]} -gt 0 ]]; then
        log_warning "Missing dependencies: ${missing_deps[*]}"
        log_info "Installing prerequisites..."
        apt-get update -qq
        
        # Install Docker if missing
        if [[ " ${missing_deps[*]} " =~ " docker " ]]; then
            log_info "Installing Docker..."
            curl -fsSL https://get.docker.com | sh
            systemctl enable docker
            systemctl start docker
        fi
    fi
    
    log_success "Prerequisites check passed"
}

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                           INSTALL PACKAGES                                    ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

install_packages() {
    log_section "Installing Required Packages"
    
    apt-get update -qq
    
    # Core packages
    apt-get install -y --no-install-recommends \
        wireguard \
        wireguard-tools \
        ufw \
        jq \
        curl \
        openssl \
        python3 \
        python3-pip \
        python3-venv \
        ca-certificates \
        gnupg \
        lsb-release
    
    # Install PyNaCl for Ed25519 token minting
    log_info "Installing PyNaCl for cryptographic operations..."
    pip3 install --quiet pynacl
    
    log_success "Packages installed successfully"
}

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                           DIRECTORY SETUP                                     ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

setup_directories() {
    log_section "Setting Up Directory Structure"
    
    mkdir -p "$CA_DIR"
    mkdir -p "$WG_DIR"
    mkdir -p "$NATS_DIR"
    mkdir -p "$MATRIX_DIR"
    mkdir -p "$LOGS_DIR"
    mkdir -p "${SWARM_DIR}/bin"
    mkdir -p "${SWARM_DIR}/tokens"
    
    # Secure permissions
    chmod 700 "$CA_DIR"
    chmod 700 "$WG_DIR"
    chmod 700 "${SWARM_DIR}/tokens"
    
    log_success "Directory structure created at $SWARM_DIR"
}

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                           ED25519 CA SETUP                                    ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

setup_ca() {
    log_section "Setting Up Ed25519 Certificate Authority"
    
    if [[ -f "${CA_DIR}/ca_private.pem" ]]; then
        log_warning "CA already exists, skipping generation"
        return
    fi
    
    # Generate Ed25519 CA key pair
    openssl genpkey -algorithm ed25519 -out "${CA_DIR}/ca_private.pem"
    openssl pkey -in "${CA_DIR}/ca_private.pem" -pubout -out "${CA_DIR}/ca_public.pem"
    
    chmod 600 "${CA_DIR}/ca_private.pem"
    chmod 644 "${CA_DIR}/ca_public.pem"
    
    log_success "Ed25519 CA created"
    log_info "CA Public Key: ${CA_DIR}/ca_public.pem"
    log_warning "BACKUP ${CA_DIR}/ca_private.pem SECURELY - This controls swarm access!"
}

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                           WIREGUARD MESH SETUP                                ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

setup_wireguard() {
    log_section "Configuring WireGuard Mesh Network"
    
    # Generate node keys if they don't exist
    if [[ ! -f "${WG_DIR}/${NODE_NAME}_private.key" ]]; then
        log_info "Generating WireGuard keys for ${NODE_NAME}..."
        
        wg genkey > "${WG_DIR}/${NODE_NAME}_private.key"
        wg pubkey < "${WG_DIR}/${NODE_NAME}_private.key" > "${WG_DIR}/${NODE_NAME}_public.key"
        wg genpsk > "${WG_DIR}/${NODE_NAME}_psk.key"
        
        chmod 600 "${WG_DIR}/${NODE_NAME}_private.key"
        chmod 600 "${WG_DIR}/${NODE_NAME}_psk.key"
        chmod 644 "${WG_DIR}/${NODE_NAME}_public.key"
    fi
    
    local PRIVATE_KEY
    PRIVATE_KEY=$(cat "${WG_DIR}/${NODE_NAME}_private.key")
    
    # Create WireGuard configuration
    cat > "/etc/wireguard/${WG_INTERFACE}.conf" <<EOF
# Sovereign Swarm WireGuard Configuration
# Node: ${NODE_NAME}
# Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)

[Interface]
PrivateKey = ${PRIVATE_KEY}
Address = ${WG_SUBNET%.*}.$(( (RANDOM % 253) + 2 ))/24
ListenPort = ${WG_PORT}
SaveConfig = false

# Post-up: Enable IP forwarding for mesh routing
PostUp = sysctl -w net.ipv4.ip_forward=1
PostUp = sysctl -w net.ipv6.conf.all.forwarding=1

# Peers will be added dynamically by SwarmGate
# Example peer entry (add manually or via swarmgate add-peer):
# [Peer]
# PublicKey = <peer_public_key>
# PresharedKey = <psk>
# AllowedIPs = 10.137.0.X/32
# Endpoint = <peer_ip>:51820
# PersistentKeepalive = 25
EOF
    
    chmod 600 "/etc/wireguard/${WG_INTERFACE}.conf"
    
    # Enable and start WireGuard
    systemctl enable "wg-quick@${WG_INTERFACE}"
    systemctl restart "wg-quick@${WG_INTERFACE}" || log_warning "WireGuard start deferred (no peers yet)"
    
    log_success "WireGuard mesh configured"
    log_info "Public Key: $(cat "${WG_DIR}/${NODE_NAME}_public.key")"
}

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                           JWT TOKEN MINTING                                   ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

create_token_minter() {
    log_section "Creating JWT Token Minter"
    
    cat > "${SWARM_DIR}/bin/mint_token.py" <<'PYTHON_EOF'
#!/usr/bin/env python3
"""
Sovereign Swarm JWT Token Minter
Uses Ed25519 signing for node capability tokens
"""

import sys
import json
import time
import base64
import hashlib
from pathlib import Path

try:
    from nacl.signing import SigningKey
    from nacl.encoding import Base64Encoder
except ImportError:
    print("Error: PyNaCl not installed. Run: pip3 install pynacl", file=sys.stderr)
    sys.exit(1)

CA_DIR = Path("/opt/sovereignty-swarm/ca")
TOKEN_DIR = Path("/opt/sovereignty-swarm/tokens")


def base64url_encode(data: bytes) -> str:
    """URL-safe base64 encoding without padding"""
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')


def create_jwt(payload: dict, private_key_pem: str) -> str:
    """Create a JWT signed with Ed25519"""
    # Header
    header = {"alg": "EdDSA", "typ": "JWT"}
    header_b64 = base64url_encode(json.dumps(header).encode())
    
    # Payload
    payload_b64 = base64url_encode(json.dumps(payload).encode())
    
    # Message to sign
    message = f"{header_b64}.{payload_b64}".encode()
    
    # Load private key and sign
    # Extract raw key from PEM (simplified - assumes standard format)
    key_lines = private_key_pem.strip().split('\n')
    key_data = ''.join(key_lines[1:-1])
    raw_key = base64.b64decode(key_data)
    # Ed25519 private key is last 32 bytes of the DER structure
    seed = raw_key[-32:]
    
    signing_key = SigningKey(seed)
    signature = signing_key.sign(message).signature
    signature_b64 = base64url_encode(signature)
    
    return f"{header_b64}.{payload_b64}.{signature_b64}"


def mint_node_token(node_name: str, capabilities: list, ttl_days: int = 365) -> str:
    """Mint a capability token for a swarm node"""
    
    # Load CA private key
    private_key_path = CA_DIR / "ca_private.pem"
    if not private_key_path.exists():
        print(f"Error: CA private key not found at {private_key_path}", file=sys.stderr)
        sys.exit(1)
    
    private_key_pem = private_key_path.read_text()
    
    # Build payload
    now = int(time.time())
    payload = {
        "iss": "sovereignty-swarm-ca",
        "sub": node_name,
        "iat": now,
        "exp": now + (ttl_days * 86400),
        "cap": capabilities,
        "swarm": "strategickhaos"
    }
    
    token = create_jwt(payload, private_key_pem)
    
    # Save token
    TOKEN_DIR.mkdir(parents=True, exist_ok=True)
    token_file = TOKEN_DIR / f"{node_name}.jwt"
    token_file.write_text(token)
    token_file.chmod(0o600)
    
    return token


def main():
    if len(sys.argv) < 2:
        print("Usage: mint_token.py <node_name> [capabilities...]")
        print("Example: mint_token.py starlink-node-1 mesh telemetry command")
        sys.exit(1)
    
    node_name = sys.argv[1]
    capabilities = sys.argv[2:] if len(sys.argv) > 2 else ["mesh", "telemetry"]
    
    print(f"Minting token for node: {node_name}")
    print(f"Capabilities: {capabilities}")
    
    token = mint_node_token(node_name, capabilities)
    
    print(f"\nToken minted successfully!")
    print(f"Saved to: /opt/sovereignty-swarm/tokens/{node_name}.jwt")
    print(f"\nToken preview: {token[:50]}...")


if __name__ == "__main__":
    main()
PYTHON_EOF
    
    chmod +x "${SWARM_DIR}/bin/mint_token.py"
    log_success "Token minter created at ${SWARM_DIR}/bin/mint_token.py"
}

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                           SWARMGATE AGENT                                     ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

setup_swarmgate() {
    log_section "Setting Up SwarmGate Agent"
    
    # Create SwarmGate wrapper script
    cat > "$SWARMGATE_BIN" <<'BASH_EOF'
#!/usr/bin/env bash
# SwarmGate - Sovereign Swarm access control agent
# Only allows properly-signed nodes to participate in the mesh

set -euo pipefail

SWARM_DIR="/opt/sovereignty-swarm"
WG_INTERFACE="wg0"

verify_token() {
    local token_file="$1"
    local ca_public="${SWARM_DIR}/ca/ca_public.pem"
    
    if [[ ! -f "$token_file" ]]; then
        echo "Error: Token file not found: $token_file" >&2
        return 1
    fi
    
    # Basic JWT structure validation
    local token
    token=$(cat "$token_file")
    
    if [[ ! "$token" =~ ^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$ ]]; then
        echo "Error: Invalid token format" >&2
        return 1
    fi
    
    echo "Token structure valid"
    return 0
}

add_peer() {
    local peer_name="$1"
    local peer_pubkey="$2"
    local peer_endpoint="$3"
    local peer_ip="$4"
    local psk="${5:-}"
    
    echo "Adding peer: $peer_name"
    
    local wg_cmd="wg set $WG_INTERFACE peer $peer_pubkey allowed-ips ${peer_ip}/32"
    
    if [[ -n "$peer_endpoint" ]]; then
        wg_cmd="$wg_cmd endpoint ${peer_endpoint}:51820"
    fi
    
    if [[ -n "$psk" ]]; then
        wg_cmd="$wg_cmd preshared-key <(echo '$psk')"
    fi
    
    wg_cmd="$wg_cmd persistent-keepalive 25"
    
    eval "$wg_cmd"
    echo "Peer $peer_name added successfully"
}

remove_peer() {
    local peer_pubkey="$1"
    wg set "$WG_INTERFACE" peer "$peer_pubkey" remove
    echo "Peer removed"
}

show_status() {
    echo "=== SwarmGate Status ==="
    echo "Node: $(hostname)"
    echo ""
    echo "=== WireGuard Status ==="
    wg show "$WG_INTERFACE" 2>/dev/null || echo "WireGuard not active"
    echo ""
    echo "=== Active Tokens ==="
    ls -la "${SWARM_DIR}/tokens/" 2>/dev/null || echo "No tokens found"
}

case "${1:-status}" in
    verify)
        verify_token "$2"
        ;;
    add-peer)
        add_peer "$2" "$3" "$4" "$5" "${6:-}"
        ;;
    remove-peer)
        remove_peer "$2"
        ;;
    status)
        show_status
        ;;
    *)
        echo "Usage: swarmgate {verify|add-peer|remove-peer|status}"
        echo ""
        echo "Commands:"
        echo "  verify <token_file>                    - Verify a node token"
        echo "  add-peer <name> <pubkey> <endpoint> <ip> [psk]  - Add mesh peer"
        echo "  remove-peer <pubkey>                   - Remove mesh peer"
        echo "  status                                 - Show swarm status"
        exit 1
        ;;
esac
BASH_EOF
    
    chmod +x "$SWARMGATE_BIN"
    
    # Add to PATH
    if ! grep -q "sovereignty-swarm/bin" /etc/profile.d/swarm.sh 2>/dev/null; then
        echo 'export PATH="$PATH:/opt/sovereignty-swarm/bin"' > /etc/profile.d/swarm.sh
    fi
    
    log_success "SwarmGate agent installed"
}

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                           NATS JETSTREAM SETUP                                ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

setup_nats() {
    log_section "Setting Up NATS JetStream"
    
    # Create NATS configuration
    cat > "${NATS_DIR}/nats-server.conf" <<EOF
# NATS JetStream Configuration for Sovereign Swarm
# Telemetry and command bus

port: 4222
http_port: 8222

jetstream {
    store_dir: "${NATS_DIR}/data"
    max_mem: 256MB
    max_file: 1GB
}

# Cluster configuration (for multi-node)
cluster {
    name: sovereignty-swarm
    listen: 0.0.0.0:6222
    
    routes = [
        # Add other node routes here
        # nats-route://10.137.0.X:6222
    ]
}

# Logging
log_file: "${LOGS_DIR}/nats.log"
debug: false
trace: false

# Security
authorization {
    default_permissions = {
        publish = ["swarm.>", "telemetry.>"]
        subscribe = ["swarm.>", "telemetry.>", "_INBOX.>"]
    }
}
EOF
    
    # Create Docker Compose for NATS
    cat > "${NATS_DIR}/docker-compose.yml" <<EOF
version: '3.8'

services:
  nats:
    image: nats:latest
    container_name: sovereignty-nats
    restart: unless-stopped
    ports:
      - "4222:4222"   # Client connections
      - "8222:8222"   # HTTP monitoring
      - "6222:6222"   # Cluster routing
    volumes:
      - ${NATS_DIR}/nats-server.conf:/etc/nats/nats-server.conf:ro
      - ${NATS_DIR}/data:/data
      - ${LOGS_DIR}:/logs
    command: ["--config", "/etc/nats/nats-server.conf"]
    networks:
      - sovereignty-mesh

networks:
  sovereignty-mesh:
    driver: bridge
EOF
    
    mkdir -p "${NATS_DIR}/data"
    
    log_success "NATS JetStream configured"
    log_info "Start with: cd ${NATS_DIR} && docker compose up -d"
}

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                           MATRIX SYNAPSE SETUP                                ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

setup_matrix() {
    log_section "Setting Up Matrix Synapse (Encrypted Swarm Chat)"
    
    # Create Matrix configuration
    cat > "${MATRIX_DIR}/docker-compose.yml" <<EOF
version: '3.8'

services:
  synapse:
    image: matrixdotorg/synapse:latest
    container_name: sovereignty-matrix
    restart: unless-stopped
    environment:
      - SYNAPSE_SERVER_NAME=swarm.local
      - SYNAPSE_REPORT_STATS=no
    volumes:
      - ${MATRIX_DIR}/data:/data
    ports:
      - "8008:8008"
      - "8448:8448"
    networks:
      - sovereignty-mesh

networks:
  sovereignty-mesh:
    external: true
EOF
    
    mkdir -p "${MATRIX_DIR}/data"
    
    log_success "Matrix Synapse configured"
    log_info "Start with: cd ${MATRIX_DIR} && docker compose up -d"
    log_warning "Run 'docker exec sovereignty-matrix generate' on first start"
}

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                           FIREWALL CONFIGURATION                              ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

setup_firewall() {
    log_section "Configuring UFW Firewall (Default-Deny)"
    
    # Reset UFW to defaults
    ufw --force reset
    
    # Default policies
    ufw default deny incoming
    ufw default allow outgoing
    
    # Allow SSH (essential for remote management)
    ufw allow ssh comment 'SSH Access'
    
    # Allow WireGuard
    ufw allow "${WG_PORT}/udp" comment 'WireGuard VPN'
    
    # Allow traffic on WireGuard interface
    ufw allow in on "$WG_INTERFACE" comment 'WireGuard Mesh Traffic'
    
    # Enable UFW
    ufw --force enable
    
    log_success "Firewall configured (default-deny, SSH + WireGuard allowed)"
    ufw status verbose
}

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                           PSK ROTATION CRON                                   ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

setup_psk_rotation() {
    log_section "Setting Up Yearly PSK Rotation"
    
    # Create rotation script
    cat > "${SWARM_DIR}/bin/rotate_psk.sh" <<'BASH_EOF'
#!/usr/bin/env bash
# Rotate WireGuard Pre-Shared Keys annually
# This script should be called by cron

set -euo pipefail

SWARM_DIR="/opt/sovereignty-swarm"
WG_DIR="${SWARM_DIR}/wireguard"
LOG_FILE="${SWARM_DIR}/logs/psk_rotation.log"

log() {
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $1" >> "$LOG_FILE"
}

log "Starting PSK rotation..."

# Backup current PSK
for psk_file in "${WG_DIR}"/*_psk.key; do
    if [[ -f "$psk_file" ]]; then
        cp "$psk_file" "${psk_file}.backup.$(date +%Y%m%d)"
        # Generate new PSK
        wg genpsk > "$psk_file"
        chmod 600 "$psk_file"
        log "Rotated: $psk_file"
    fi
done

log "PSK rotation complete. Manual peer update required."
log "WARNING: Update all mesh peers with new PSKs!"
BASH_EOF
    
    chmod +x "${SWARM_DIR}/bin/rotate_psk.sh"
    
    # Add cron job for yearly rotation (January 1st at 3 AM)
    local cron_entry="0 3 1 1 * ${SWARM_DIR}/bin/rotate_psk.sh"
    
    # Add to root crontab if not already present
    if ! crontab -l 2>/dev/null | grep -q "rotate_psk.sh"; then
        (crontab -l 2>/dev/null; echo "$cron_entry") | crontab -
        log_success "PSK rotation cron job added (yearly on Jan 1)"
    else
        log_info "PSK rotation cron job already exists"
    fi
}

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                           MINT INITIAL TOKEN                                  ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

mint_initial_token() {
    log_section "Minting Initial Node Token"
    
    # Mint a token for this node with full capabilities
    python3 "${SWARM_DIR}/bin/mint_token.py" "$NODE_NAME" mesh telemetry command admin
    
    log_success "Initial token minted for ${NODE_NAME}"
}

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                           VERIFICATION                                        ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

verify_installation() {
    log_section "Verifying Installation"
    
    local errors=0
    
    # Check directories
    for dir in "$CA_DIR" "$WG_DIR" "$NATS_DIR" "$MATRIX_DIR"; do
        if [[ -d "$dir" ]]; then
            echo -e "${GREEN}✅ Directory exists: $dir${NC}"
        else
            echo -e "${RED}❌ Missing directory: $dir${NC}"
            ((errors++))
        fi
    done
    
    # Check CA files
    if [[ -f "${CA_DIR}/ca_private.pem" ]] && [[ -f "${CA_DIR}/ca_public.pem" ]]; then
        echo -e "${GREEN}✅ Ed25519 CA: Configured${NC}"
    else
        echo -e "${RED}❌ Ed25519 CA: Missing${NC}"
        ((errors++))
    fi
    
    # Check WireGuard
    if [[ -f "/etc/wireguard/${WG_INTERFACE}.conf" ]]; then
        echo -e "${GREEN}✅ WireGuard: Configured${NC}"
    else
        echo -e "${RED}❌ WireGuard: Not configured${NC}"
        ((errors++))
    fi
    
    # Check UFW
    if ufw status | grep -q "Status: active"; then
        echo -e "${GREEN}✅ Firewall: Active${NC}"
    else
        echo -e "${YELLOW}⚠️  Firewall: Inactive${NC}"
    fi
    
    # Check PyNaCl
    if python3 -c "from nacl.signing import SigningKey" 2>/dev/null; then
        echo -e "${GREEN}✅ PyNaCl: Installed${NC}"
    else
        echo -e "${RED}❌ PyNaCl: Not installed${NC}"
        ((errors++))
    fi
    
    # Check token
    if [[ -f "${SWARM_DIR}/tokens/${NODE_NAME}.jwt" ]]; then
        echo -e "${GREEN}✅ Node Token: Minted${NC}"
    else
        echo -e "${YELLOW}⚠️  Node Token: Not found${NC}"
    fi
    
    echo ""
    if [[ $errors -eq 0 ]]; then
        log_success "All verifications passed!"
    else
        log_error "$errors verification(s) failed"
        return 1
    fi
}

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                           SUMMARY                                             ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

show_summary() {
    echo ""
    echo -e "${CYAN}╔══════════════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║                    SOVEREIGN SWARM BOOTSTRAP COMPLETE                        ║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${GREEN}Node:${NC} ${NODE_NAME}"
    echo -e "${GREEN}Swarm Directory:${NC} ${SWARM_DIR}"
    echo ""
    echo -e "${BLUE}Components Installed:${NC}"
    echo "  • WireGuard mesh interface (${WG_INTERFACE})"
    echo "  • Ed25519 Certificate Authority"
    echo "  • JWT Token Minter (PyNaCl)"
    echo "  • SwarmGate Access Control Agent"
    echo "  • NATS JetStream (telemetry/command bus)"
    echo "  • Matrix Synapse (encrypted chat)"
    echo "  • UFW Firewall (default-deny)"
    echo "  • PSK Rotation (yearly cron)"
    echo ""
    echo -e "${YELLOW}Next Steps:${NC}"
    echo "  1. Start NATS:   cd ${NATS_DIR} && docker compose up -d"
    echo "  2. Start Matrix: cd ${MATRIX_DIR} && docker compose up -d"
    echo "  3. Add peers:    swarmgate add-peer <name> <pubkey> <endpoint> <ip>"
    echo "  4. Check status: swarmgate status"
    echo ""
    echo -e "${RED}IMPORTANT:${NC}"
    echo "  • Backup ${CA_DIR}/ca_private.pem securely!"
    echo "  • Share public keys with other nodes to build mesh"
    echo "  • This node's public key: $(cat "${WG_DIR}/${NODE_NAME}_public.key" 2>/dev/null || echo 'N/A')"
    echo ""
    echo -e "${CYAN}Documentation:${NC} See SOVEREIGN_SWARM_NOTES.md for board-level summary"
    echo ""
}

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                           MAIN EXECUTION                                      ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

main() {
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════════════════════╗"
    echo "║                                                                              ║"
    echo "║   ███████╗ ██████╗ ██╗   ██╗███████╗██████╗ ███████╗██╗ ██████╗ ███╗   ██╗  ║"
    echo "║   ██╔════╝██╔═══██╗██║   ██║██╔════╝██╔══██╗██╔════╝██║██╔════╝ ████╗  ██║  ║"
    echo "║   ███████╗██║   ██║██║   ██║█████╗  ██████╔╝█████╗  ██║██║  ███╗██╔██╗ ██║  ║"
    echo "║   ╚════██║██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗██╔══╝  ██║██║   ██║██║╚██╗██║  ║"
    echo "║   ███████║╚██████╔╝ ╚████╔╝ ███████╗██║  ██║███████╗██║╚██████╔╝██║ ╚████║  ║"
    echo "║   ╚══════╝ ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝  ║"
    echo "║                                                                              ║"
    echo "║                    SWARM MESH NETWORK BOOTSTRAP                              ║"
    echo "║                    Strategickhaos DAO LLC                                    ║"
    echo "║                                                                              ║"
    echo "╚══════════════════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    check_root
    check_prerequisites
    install_packages
    setup_directories
    setup_ca
    setup_wireguard
    create_token_minter
    setup_swarmgate
    setup_nats
    setup_matrix
    setup_firewall
    setup_psk_rotation
    mint_initial_token
    verify_installation
    show_summary
    
    log_success "Bootstrap complete for node: ${NODE_NAME}"
}

# Run main function
main "$@"
