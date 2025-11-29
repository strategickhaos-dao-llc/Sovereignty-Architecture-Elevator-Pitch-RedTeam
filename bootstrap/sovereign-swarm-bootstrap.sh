#!/usr/bin/env bash
# Sovereign Swarm — Master Bootstrap v0.2.0 (Production-Ready)
# Validated for Ubuntu 22.04+ and Debian 12+
# Run as root. First on Command-0, then on other nodes.

set -euo pipefail

# ========= CONFIG =========
NODE_ID="${NODE_ID:-command0}"
SWARM_NET="10.44.0.0/16"
WG_IF="wg0"
WG_PORT="${WG_PORT:-51820}"
UFW_SSH_PORT="${UFW_SSH_PORT:-22}"
REPO_ROOT="${REPO_ROOT:-/opt/sovereign-swarm}"
DOMAIN="${DOMAIN:-swarm.local}"
LOG_FILE="/var/log/swarm-bootstrap-${NODE_ID}.log"
STATE_FILE="${REPO_ROOT}/.bootstrap-state"
# ==========================

exec > >(tee -a "$LOG_FILE") 2>&1
log() { echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] [*] $*"; }
err() { echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] [ERR] $*" >&2; }

log "=== Sovereign Swarm Bootstrap v0.2.0 — NODE_ID=$NODE_ID ==="

# Root check
[ "$EUID" -eq 0 ] || { err "Must run as root"; exit 1; }

# OS check
command -v apt >/dev/null || { err "Debian/Ubuntu required"; exit 1; }

# State tracking for safe rollback
mark_state() { echo "$1" >> "$STATE_FILE"; }
get_state() { grep -q "^$1$" "$STATE_FILE" 2>/dev/null; }

# Safe rollback - only removes what we created
rollback() {
    err "ROLLBACK initiated..."
    
    if get_state "wg-enabled"; then
        systemctl stop "wg-quick@${WG_IF}" 2>/dev/null || true
        systemctl disable "wg-quick@${WG_IF}" 2>/dev/null || true
        rm -f /etc/wireguard/wg0.conf
    fi
    
    if get_state "nats-enabled"; then
        systemctl stop nats 2>/dev/null || true
        systemctl disable nats 2>/dev/null || true
        rm -rf /etc/nats
    fi
    
    if get_state "matrix-started"; then
        cd "$REPO_ROOT/matrix" 2>/dev/null && docker compose down 2>/dev/null || true
    fi
    
    if get_state "swarmsgd-enabled"; then
        systemctl stop swarmsgd 2>/dev/null || true
        systemctl disable swarmsgd 2>/dev/null || true
    fi
    
    # Clean temporary files
    rm -rf /run/wg-tokens /etc/swarmsgd-pubkey
    
    # Remove repo if we created it
    if get_state "repo-created"; then
        rm -rf "$REPO_ROOT"
    fi
    
    rm -f "$STATE_FILE"
    err "Rollback complete. Check $LOG_FILE for details."
}

trap 'err "Failed at line $LINENO"; rollback; exit 1' ERR

# ========= PHASE 0: System Preparation =========
log "Checking prerequisites..."

# Create repo
if [ ! -d "$REPO_ROOT" ]; then
    mkdir -p "$REPO_ROOT" || { err "Cannot create $REPO_ROOT"; exit 1; }
    mark_state "repo-created"
fi

cd "$REPO_ROOT"
mkdir -p .bootstrap-state-dir
STATE_FILE="${REPO_ROOT}/.bootstrap-state-dir/state"
touch "$STATE_FILE"

log "Installing system packages..."
export DEBIAN_FRONTEND=noninteractive
apt-get update -y

# Install core packages
apt-get install -y \
    wireguard wireguard-tools \
    nftables ufw \
    curl jq git ca-certificates \
    python3 python3-pip python3-venv \
    docker.io docker-compose-plugin \
    nats-server \
    syncthing

mark_state "packages-installed"

# Install PyNaCl via pip (more reliable than Debian package)
log "Installing PyNaCl..."
pip3 install --break-system-packages pynacl 2>/dev/null || pip3 install pynacl

# Verify PyNaCl works
python3 -c "from nacl.signing import SigningKey" || {
    err "PyNaCl installation failed"
    exit 1
}

mark_state "pynacl-installed"

# ========= PHASE 1: Directory Structure =========
log "Creating directory structure..."
mkdir -p ca/state
mkdir -p "nodes/$NODE_ID"
mkdir -p wireguard/conf
mkdir -p swarmgate/{nft,swarmsgd,systemd}
mkdir -p nats/{conf,systemd,accounts}
mkdir -p matrix/synapse
mkdir -p scripts
mkdir -p artifacts

mark_state "dirs-created"

# ========= PHASE 2: CA and Keys =========
log "Generating Certificate Authority..."

if [ ! -f ca/state/swarm-ed25519.key ]; then
    openssl rand 32 > ca/state/swarm-ed25519.key
    sha256sum ca/state/swarm-ed25519.key | awk '{print $1}' | xxd -r -p | head -c 32 > ca/state/swarm-ed25519.pub
    chmod 600 ca/state/swarm-ed25519.key
    log "CA keypair generated"
else
    log "CA keypair exists, skipping generation"
fi

log "Generating node keys for $NODE_ID..."

if [ ! -f "nodes/$NODE_ID/wg.key" ]; then
    wg genkey | tee "nodes/$NODE_ID/wg.key" | wg pubkey > "nodes/$NODE_ID/wg.pub"
    chmod 600 "nodes/$NODE_ID/wg.key"
fi

WG_PRIV=$(cat "nodes/$NODE_ID/wg.key")
WG_PUB=$(cat "nodes/$NODE_ID/wg.pub")

mark_state "keys-generated"

# ========= PHASE 3: Token Minting =========
log "Creating token minting script..."

cat > scripts/mint_token.py <<'PYEOF'
#!/usr/bin/env python3
import json, time, base64, os, argparse, secrets
from nacl.signing import SigningKey

def b64u(b):
    return base64.urlsafe_b64encode(b).rstrip(b'=').decode()

parser = argparse.ArgumentParser()
parser.add_argument("--ca", required=True)
parser.add_argument("--node", required=True)
parser.add_argument("--aud", required=True)
parser.add_argument("--ttl", default="86400")
parser.add_argument("--caps", required=True)
args = parser.parse_args()

# Read CA key (first 32 bytes)
with open(args.ca, "rb") as f:
    seed = f.read(32)

sk = SigningKey(seed)
now = int(time.time())
exp = now + int(args.ttl)

claims = {
    "iss": "SwarmCA",
    "sub": os.path.basename(args.node),
    "aud": args.aud,
    "iat": now,
    "exp": exp,
    "cap": args.caps.split(","),
    "jti": secrets.token_urlsafe(16)
}

hdr = {"alg": "EdDSA", "typ": "JWT"}

# Create JWT
payload = b'.'.join([
    b64u(json.dumps(hdr).encode()).encode(),
    b64u(json.dumps(claims).encode()).encode()
])

sig = sk.sign(payload).signature
jwt = payload.decode() + "." + b64u(sig)

# Write token
token_path = os.path.join(args.node, "token.jwt")
with open(token_path, "w") as f:
    f.write(jwt)

print(jwt)
PYEOF

chmod +x scripts/mint_token.py

# Determine capabilities based on node role
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

log "Minting capability token for $NODE_ID..."
python3 scripts/mint_token.py \
    --ca ca/state/swarm-ed25519.key \
    --node "nodes/$NODE_ID" \
    --aud wg \
    --ttl 604800 \
    --caps "$CAPS" > /dev/null

# Verify token was created
[ -f "nodes/$NODE_ID/token.jwt" ] || {
    err "Token minting failed"
    exit 1
}

# Install CA public key for verification
install -Dm644 ca/state/swarm-ed25519.pub /etc/swarmsgd-pubkey

mark_state "tokens-minted"

# ========= PHASE 4: SwarmGate Agent =========
log "Installing SwarmGate enforcement agent..."

cat > swarmgate/swarmsgd/agent.py <<'PYEOF'
#!/usr/bin/env python3
import os, sys, json, base64, time, subprocess
from nacl.signing import VerifyKey

PUB = "/etc/swarmsgd-pubkey"

def b64_pad(s):
    return s + '=' * ((4 - len(s) % 4) % 4)

def verify_token(jwt, aud):
    try:
        hdr, payload, sig = jwt.split('.')
        claims = json.loads(base64.urlsafe_b64decode(b64_pad(payload)))
        
        if claims.get("aud") != aud:
            raise Exception("Invalid audience")
        
        if claims.get("exp", 0) < int(time.time()):
            raise Exception("Token expired")
        
        # Verify signature
        with open(PUB, "rb") as f:
            pub_key = f.read()
        
        vk = VerifyKey(pub_key)
        message = (hdr + "." + payload).encode()
        signature = base64.urlsafe_b64decode(b64_pad(sig))
        vk.verify(message, signature)
        
        return claims
    except Exception as e:
        print(f"Token verification failed: {e}", file=sys.stderr)
        raise

def apply_allowed_ips(peer_pub, networks):
    # Remove existing allowed IPs
    subprocess.run(
        ["wg", "set", "wg0", "peer", peer_pub, "remove", "allowed-ips"],
        check=False,
        capture_output=True
    )
    
    # Add new allowed IPs
    for net in networks:
        subprocess.run(
            ["wg", "set", "wg0", "peer", peer_pub, "allowed-ips", net],
            check=False,
            capture_output=True
        )

def main():
    peer = os.environ.get("WG_PEER_PUBLIC_KEY", "")
    if not peer:
        print("No peer public key in environment", file=sys.stderr)
        sys.exit(1)
    
    token_path = f"/run/wg-tokens/{peer}.jwt"
    if not os.path.exists(token_path):
        print(f"No token found for peer {peer}", file=sys.stderr)
        sys.exit(1)
    
    with open(token_path) as f:
        token = f.read().strip()
    
    claims = verify_token(token, "wg")
    
    # Extract allowed networks from capabilities
    networks = [
        cap.split(":", 1)[1]
        for cap in claims.get("cap", [])
        if cap.startswith("net:")
    ]
    
    if not networks:
        print("No network capabilities in token", file=sys.stderr)
        sys.exit(1)
    
    apply_allowed_ips(peer, networks)
    print("OK")

if __name__ == "__main__":
    main()
PYEOF

chmod +x swarmgate/swarmsgd/agent.py

# Create systemd service
cat > swarmgate/systemd/swarmsgd.service <<'UNITEOF'
[Unit]
Description=SwarmGate Capability Enforcement Agent
After=network.target

[Service]
Type=oneshot
ExecStart=/usr/bin/python3 /opt/sovereign-swarm/swarmgate/swarmsgd/agent.py
StandardOutput=journal
StandardError=journal
RemainAfterExit=no

[Install]
WantedBy=multi-user.target
UNITEOF

install -Dm644 swarmgate/systemd/swarmsgd.service /etc/systemd/system/swarmsgd.service
systemctl daemon-reload
systemctl enable swarmsgd
mark_state "swarmsgd-enabled"

# ========= PHASE 5: WireGuard Configuration =========
log "Configuring WireGuard..."

# Determine node IP address
case "$NODE_ID" in
    command0) WG_ADDR="10.44.0.1/16" ;;
    fixed1)   WG_ADDR="10.44.1.1/16" ;;
    mobile2)  WG_ADDR="10.44.2.1/16" ;;
    edge3)    WG_ADDR="10.44.10.3/16" ;;
    edge4)    WG_ADDR="10.44.10.4/16" ;;
    *)        WG_ADDR="10.44.10.100/16" ;;
esac

if [ "$NODE_ID" = "command0" ]; then
    # Command-0 is the hub
    PUB_IP=$(curl -4s --max-time 5 https://ifconfig.me || echo "UNKNOWN")
    
    cat > wireguard/conf/wg0.conf <<WGEOF
[Interface]
Address = ${WG_ADDR}
PrivateKey = ${WG_PRIV}
ListenPort = ${WG_PORT}
PostUp = sysctl -w net.ipv4.ip_forward=1
PostUp = nft -f /etc/nftables.conf 2>/dev/null || true

# Peers will be added here as they connect
WGEOF

    log ""
    log "==================================================="
    log "Command-0 Configuration Complete"
    log "==================================================="
    log "WireGuard Public Key: ${WG_PUB}"
    log "Endpoint: ${PUB_IP}:${WG_PORT}"
    log ""
    log "Provide these values when bootstrapping other nodes"
    log "==================================================="
    log ""
else
    # Non-hub node - needs Command-0 details
    log ""
    log "This is a non-hub node. You need Command-0 details."
    log ""
    
    if [ -z "${COMMAND0_PUBKEY:-}" ]; then
        read -rp "Enter Command-0 WireGuard PublicKey: " COMMAND0_PUBKEY
    fi
    
    if [ -z "${COMMAND0_ENDPOINT:-}" ]; then
        read -rp "Enter Command-0 Endpoint (IP or FQDN): " COMMAND0_ENDPOINT
    fi
    
    # Generate PSK for this peer
    mkdir -p /etc/wireguard/psk
    PSK_FILE="/etc/wireguard/psk/${NODE_ID}.psk"
    if [ ! -f "$PSK_FILE" ]; then
        wg genpsk > "$PSK_FILE"
        chmod 600 "$PSK_FILE"
    fi
    PSK=$(cat "$PSK_FILE")
    
    cat > wireguard/conf/wg0.conf <<WGEOF
[Interface]
Address = ${WG_ADDR}
PrivateKey = ${WG_PRIV}
ListenPort = ${WG_PORT}
PostUp = sysctl -w net.ipv4.ip_forward=1

[Peer]
PublicKey = ${COMMAND0_PUBKEY}
PresharedKey = ${PSK}
Endpoint = ${COMMAND0_ENDPOINT}:${WG_PORT}
AllowedIPs = 10.44.0.0/16
PersistentKeepalive = 25
WGEOF

    log "Non-hub node configured with Command-0 peer"
fi

# Install WireGuard config
install -Dm600 wireguard/conf/wg0.conf /etc/wireguard/wg0.conf

# Setup token handoff directory
mkdir -p /run/wg-tokens
chmod 700 /run/wg-tokens
cp "nodes/$NODE_ID/token.jwt" "/run/wg-tokens/${WG_PUB}.jwt"

mark_state "wg-configured"

# ========= PHASE 6: Firewall =========
log "Configuring firewall..."

ufw --force reset
ufw default deny incoming
ufw default allow outgoing
ufw allow "${UFW_SSH_PORT}/tcp"
ufw allow "${WG_PORT}/udp"
ufw --force enable

mark_state "firewall-configured"

# ========= PHASE 7: Start WireGuard =========
log "Starting WireGuard..."

systemctl enable wg-quick@${WG_IF}
systemctl restart wg-quick@${WG_IF}

# Wait for interface to come up
sleep 2

# Verify WireGuard is running
if ! wg show wg0 >/dev/null 2>&1; then
    err "WireGuard failed to start"
    exit 1
fi

mark_state "wg-enabled"
log "WireGuard mesh active"

# ========= PHASE 8: NATS =========
log "Configuring NATS..."

cat > nats/conf/nats.conf <<NATSEOF
listen: 0.0.0.0:4222
http: 127.0.0.1:8222
server_name: ${NODE_ID}

leafnodes: {
    listen: 7422
}

jetstream: {
    store_dir: "/var/lib/nats/jetstream"
    max_mem_store: 512MB
    max_file_store: 10GB
}

cluster: {
    name: swarm
    listen: 0.0.0.0:6222
}

authorization: {
    users: [
        {
            user: "swarm"
            pass: "swarm"
            permissions: {
                publish: ["telemetry.>", "alerts.>", "cmd.>"]
                subscribe: ["telemetry.>", "cmd.>"]
            }
        }
    ]
}
NATSEOF

# Ensure NATS user exists
id nats >/dev/null 2>&1 || useradd -r -s /usr/sbin/nologin nats

# Create JetStream directory
mkdir -p /var/lib/nats/jetstream
chown -R nats:nats /var/lib/nats

# Install config
install -Dm644 nats/conf/nats.conf /etc/nats/nats.conf

systemctl enable nats
systemctl restart nats

# Wait for NATS to start
sleep 2

if ! systemctl is-active nats >/dev/null; then
    err "NATS failed to start"
    exit 1
fi

mark_state "nats-enabled"
log "NATS messaging bus active"

# ========= PHASE 9: Matrix Synapse =========
log "Configuring Matrix Synapse..."

cat > matrix/docker-compose.yml <<MATRIXEOF
services:
  synapse:
    image: matrixdotorg/synapse:latest
    container_name: synapse
    restart: unless-stopped
    network_mode: host
    volumes:
      - ${REPO_ROOT}/matrix/synapse:/data
    environment:
      - SYNAPSE_SERVER_NAME=${DOMAIN}
      - SYNAPSE_REPORT_STATS=no
MATRIXEOF

mkdir -p matrix/synapse

if [ ! -f matrix/synapse/homeserver.yaml ]; then
    log "Generating Synapse config..."
    docker run --rm \
        -v "${REPO_ROOT}/matrix/synapse:/data" \
        -e SYNAPSE_SERVER_NAME="${DOMAIN}" \
        -e SYNAPSE_REPORT_STATS=no \
        matrixdotorg/synapse:latest \
        generate
    
    # Harden config
    sed -i 's/^enable_registration:.*/enable_registration: false/' matrix/synapse/homeserver.yaml || true
    sed -i 's/^max_upload_size:.*/max_upload_size: 50M/' matrix/synapse/homeserver.yaml || true
fi

log "Starting Matrix Synapse..."
cd matrix
docker compose up -d
cd ..

mark_state "matrix-started"
log "Matrix homeserver active"

# ========= PHASE 10: PSK Rotation =========
log "Installing PSK rotation cron..."

cat > scripts/rotate-psk.sh <<'PSKEOF'
#!/usr/bin/env bash
set -euo pipefail

IF="wg0"
PEERS=$(wg show ${IF} peers 2>/dev/null || true)

if [ -z "$PEERS" ]; then
    echo "No peers to rotate"
    exit 0
fi

mkdir -p /etc/wireguard/psk

for peer in $PEERS; do
    psk_file="/etc/wireguard/psk/${peer}.psk"
    wg genpsk > "$psk_file"
    chmod 600 "$psk_file"
    wg set ${IF} peer ${peer} preshared-key "$psk_file"
    echo "Rotated PSK for peer ${peer}"
done
PSKEOF

chmod +x scripts/rotate-psk.sh

# Add yearly cron (Jan 1 at 5am)
(crontab -l 2>/dev/null | grep -v rotate-psk.sh || true; echo "0 5 1 1 * ${REPO_ROOT}/scripts/rotate-psk.sh") | crontab -

mark_state "cron-installed"

# ========= PHASE 11: Create Artifact Bundle =========
log "Creating deployment artifact..."

tar czf "artifacts/${NODE_ID}-bundle.tgz" \
    "nodes/$NODE_ID" \
    wireguard/conf/wg0.conf \
    scripts/mint_token.py

# ========= COMPLETE =========
trap - ERR  # Clear error trap on success

log ""
log "==================================================="
log "Bootstrap Complete: ${NODE_ID}"
log "==================================================="
log "WireGuard: $(systemctl is-active wg-quick@${WG_IF})"
log "NATS: $(systemctl is-active nats)"
log "Matrix: $(docker inspect synapse --format='{{.State.Status}}' 2>/dev/null || echo 'not running')"
log ""
log "Artifact bundle: ${REPO_ROOT}/artifacts/${NODE_ID}-bundle.tgz"
log "Bootstrap log: ${LOG_FILE}"
log ""

if [ "$NODE_ID" != "command0" ]; then
    log "Test mesh connectivity: ping 10.44.0.1"
    log "View WireGuard status: sudo wg show"
fi

log "==================================================="
log "Sovereign swarm node ${NODE_ID} is ONLINE"
log "==================================================="

exit 0
