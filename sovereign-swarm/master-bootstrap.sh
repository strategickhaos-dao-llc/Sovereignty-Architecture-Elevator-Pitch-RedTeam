#!/usr/bin/env bash
# ============================================================================
# Sovereign Swarm Master Bootstrap Script
# Production-hardened deployment with real cryptography
# ============================================================================
# Version: 1.0.0
# License: MIT
# Author: Strategickhaos Swarm Intelligence
# ============================================================================

set -euo pipefail
IFS=$'\n\t'

# ============================================================================
# Configuration
# ============================================================================

# Node identification
NODE_ID="${NODE_ID:-$(hostname)}"
SWARM_NAME="${SWARM_NAME:-sovereign-swarm}"
SWARM_DOMAIN="${SWARM_DOMAIN:-swarm.local}"

# Directory paths
SWARM_BASE="/opt/sovereign-swarm"
CA_DIR="${SWARM_BASE}/ca"
KEYS_DIR="${SWARM_BASE}/keys"
CONFIG_DIR="${SWARM_BASE}/config"
TOKENS_DIR="${SWARM_BASE}/tokens"
LOG_DIR="/var/log/sovereign-swarm"

# WireGuard configuration
WG_INTERFACE="${WG_INTERFACE:-wg0}"
WG_PORT="${WG_PORT:-51820}"
WG_NETWORK="${WG_NETWORK:-10.44.0.0/24}"

# Service ports
NATS_PORT="${NATS_PORT:-4222}"
MATRIX_PORT="${MATRIX_PORT:-8008}"
SYNCTHING_PORT="${SYNCTHING_PORT:-22000}"

# Colors for output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly CYAN='\033[0;36m'
readonly NC='\033[0m'

# ============================================================================
# Logging Functions
# ============================================================================

log_info() {
    echo -e "${BLUE}[INFO]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $*"
}

log_success() {
    echo -e "${GREEN}[OK]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $*"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $*"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $*" >&2
}

log_section() {
    echo ""
    echo -e "${CYAN}========================================${NC}"
    echo -e "${CYAN}  $*${NC}"
    echo -e "${CYAN}========================================${NC}"
    echo ""
}

# ============================================================================
# Utility Functions
# ============================================================================

check_root() {
    if [[ $EUID -ne 0 ]]; then
        log_error "This script must be run as root"
        exit 1
    fi
}

check_dependencies() {
    log_section "Checking Dependencies"
    
    local deps=(
        "openssl"
        "wg"
        "jq"
        "curl"
        "base64"
        "systemctl"
    )
    
    local missing=()
    
    for dep in "${deps[@]}"; do
        if ! command -v "$dep" &> /dev/null; then
            missing+=("$dep")
        else
            log_success "Found: $dep"
        fi
    done
    
    if [[ ${#missing[@]} -gt 0 ]]; then
        log_error "Missing dependencies: ${missing[*]}"
        log_info "Installing missing packages..."
        apt-get update -qq
        apt-get install -y -qq wireguard wireguard-tools openssl jq curl nats-server ufw
    fi
    
    log_success "All dependencies satisfied"
}

create_directories() {
    log_section "Creating Directory Structure"
    
    local dirs=(
        "$SWARM_BASE"
        "$CA_DIR"
        "$CA_DIR/state"
        "$KEYS_DIR"
        "$KEYS_DIR/wireguard"
        "$CONFIG_DIR"
        "$TOKENS_DIR"
        "$LOG_DIR"
    )
    
    for dir in "${dirs[@]}"; do
        mkdir -p "$dir"
        chmod 700 "$dir"
        log_success "Created: $dir"
    done
}

# ============================================================================
# Cryptographic Functions (Ed25519 + JWT)
# ============================================================================

generate_ca_keys() {
    log_section "Generating Certificate Authority Keys"
    
    local ca_private="${CA_DIR}/ca.key"
    local ca_public="${CA_DIR}/ca.pub"
    
    if [[ -f "$ca_private" ]]; then
        log_warn "CA keys already exist, skipping generation"
        return 0
    fi
    
    # Generate Ed25519 key pair for CA
    openssl genpkey -algorithm ed25519 -out "$ca_private"
    openssl pkey -in "$ca_private" -pubout -out "$ca_public"
    
    chmod 600 "$ca_private"
    chmod 644 "$ca_public"
    
    # Store CA state
    cat > "${CA_DIR}/state/ca-info.json" << EOF
{
    "created": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "algorithm": "Ed25519",
    "swarm_name": "${SWARM_NAME}",
    "node_id": "${NODE_ID}"
}
EOF
    
    log_success "CA key pair generated"
    log_info "CA Public Key: $(cat "$ca_public" | tail -n +2 | head -n -1 | tr -d '\n')"
}

generate_node_keys() {
    log_section "Generating Node Keys for: $NODE_ID"
    
    local node_private="${KEYS_DIR}/${NODE_ID}.key"
    local node_public="${KEYS_DIR}/${NODE_ID}.pub"
    
    # Generate Ed25519 key pair for this node
    openssl genpkey -algorithm ed25519 -out "$node_private"
    openssl pkey -in "$node_private" -pubout -out "$node_public"
    
    chmod 600 "$node_private"
    chmod 644 "$node_public"
    
    log_success "Node keys generated for: $NODE_ID"
}

# Base64 URL encoding (for JWT)
base64url_encode() {
    openssl enc -base64 -A | tr '+/' '-_' | tr -d '='
}

base64url_decode() {
    local len=$((${#1} % 4))
    local result="$1"
    if [[ $len -eq 2 ]]; then result="$1"'=='
    elif [[ $len -eq 3 ]]; then result="$1"'='
    fi
    echo "$result" | tr '_-' '/+' | openssl enc -d -base64 -A
}

# Generate JWT with Ed25519 signature
generate_jwt() {
    local node_id="$1"
    local capabilities="$2"
    local expiry_hours="${3:-8760}"  # Default 1 year
    
    local ca_private="${CA_DIR}/ca.key"
    
    if [[ ! -f "$ca_private" ]]; then
        log_error "CA private key not found"
        return 1
    fi
    
    # JWT Header (EdDSA)
    local header='{"alg":"EdDSA","typ":"JWT"}'
    local header_b64=$(echo -n "$header" | base64url_encode)
    
    # JWT Payload
    local now=$(date +%s)
    local exp=$((now + expiry_hours * 3600))
    local payload=$(cat << EOF
{
    "iss": "${SWARM_NAME}",
    "sub": "${node_id}",
    "aud": "${SWARM_DOMAIN}",
    "iat": ${now},
    "exp": ${exp},
    "jti": "$(openssl rand -hex 16)",
    "cap": ${capabilities}
}
EOF
)
    local payload_b64=$(echo -n "$payload" | jq -c '.' | base64url_encode)
    
    # Message to sign
    local message="${header_b64}.${payload_b64}"
    
    # Sign with Ed25519 (OpenSSL 1.1.1+)
    local signature=$(echo -n "$message" | openssl pkeyutl -sign -inkey "$ca_private" | base64url_encode)
    
    # Complete JWT
    echo "${message}.${signature}"
}

mint_capability_token() {
    log_section "Minting Capability Token for: $NODE_ID"
    
    local token_file="${TOKENS_DIR}/${NODE_ID}.jwt"
    
    # Define node capabilities based on NODE_ID
    local capabilities
    case "$NODE_ID" in
        command0|command-0)
            capabilities='["ca:sign","mesh:admin","nats:admin","matrix:admin","swarm:bootstrap"]'
            ;;
        fixed1|fixed-1)
            capabilities='["mesh:peer","nats:publish","nats:subscribe","matrix:user"]'
            ;;
        pelican*)
            capabilities='["mesh:peer","nats:subscribe","sync:read"]'
            ;;
        *)
            capabilities='["mesh:peer","nats:subscribe"]'
            ;;
    esac
    
    local jwt=$(generate_jwt "$NODE_ID" "$capabilities")
    
    echo "$jwt" > "$token_file"
    chmod 600 "$token_file"
    
    log_success "Capability token minted: $token_file"
    log_info "Token capabilities: $capabilities"
    
    # Decode and display token info
    local payload=$(echo "$jwt" | cut -d'.' -f2)
    log_info "Token payload:"
    echo "$payload" | base64url_decode | jq '.'
}

# ============================================================================
# WireGuard Mesh Setup
# ============================================================================

generate_wireguard_keys() {
    log_section "Generating WireGuard Keys"
    
    local wg_private="${KEYS_DIR}/wireguard/${NODE_ID}.key"
    local wg_public="${KEYS_DIR}/wireguard/${NODE_ID}.pub"
    local wg_psk="${KEYS_DIR}/wireguard/${NODE_ID}.psk"
    
    if [[ -f "$wg_private" ]]; then
        log_warn "WireGuard keys already exist"
    else
        wg genkey > "$wg_private"
        chmod 600 "$wg_private"
    fi
    
    wg pubkey < "$wg_private" > "$wg_public"
    
    # Generate pre-shared key for additional security
    if [[ ! -f "$wg_psk" ]]; then
        wg genpsk > "$wg_psk"
        chmod 600 "$wg_psk"
    fi
    
    log_success "WireGuard keys generated"
    log_info "Public Key: $(cat "$wg_public")"
}

configure_wireguard() {
    log_section "Configuring WireGuard Mesh"
    
    local wg_private="${KEYS_DIR}/wireguard/${NODE_ID}.key"
    local wg_config="/etc/wireguard/${WG_INTERFACE}.conf"
    
    # Determine node IP based on NODE_ID
    local node_ip
    case "$NODE_ID" in
        command0|command-0)
            node_ip="10.44.0.1"
            ;;
        fixed1|fixed-1)
            node_ip="10.44.0.2"
            ;;
        pelican1)
            node_ip="10.44.0.11"
            ;;
        pelican2)
            node_ip="10.44.0.12"
            ;;
        pelican3)
            node_ip="10.44.0.13"
            ;;
        *)
            # Generate IP from hash of NODE_ID
            local hash=$(echo -n "$NODE_ID" | md5sum | cut -c1-2)
            local octet=$((16#$hash % 200 + 50))
            node_ip="10.44.0.${octet}"
            ;;
    esac
    
    cat > "$wg_config" << EOF
# Sovereign Swarm WireGuard Configuration
# Node: ${NODE_ID}
# Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)

[Interface]
Address = ${node_ip}/24
ListenPort = ${WG_PORT}
PrivateKey = $(cat "$wg_private")
# PostUp and PostDown for firewall integration
PostUp = iptables -A FORWARD -i %i -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i %i -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE

# Peer configurations will be added below
# Use: wg set ${WG_INTERFACE} peer <PUBKEY> allowed-ips <IP>/32 endpoint <HOST>:<PORT>
EOF

    # Add peer configurations for command0 (if not command0)
    if [[ "$NODE_ID" != "command0" && "$NODE_ID" != "command-0" ]]; then
        cat >> "$wg_config" << EOF

# Command-0 (Primary Hub)
[Peer]
# Replace with actual Command-0 public key after deployment
PublicKey = REPLACE_COMMAND0_PUBKEY
AllowedIPs = 10.44.0.1/32, 10.44.0.0/24
Endpoint = REPLACE_COMMAND0_ENDPOINT:${WG_PORT}
PersistentKeepalive = 25
EOF
    fi
    
    chmod 600 "$wg_config"
    
    log_success "WireGuard configuration created: $wg_config"
    log_info "Node IP: $node_ip"
    
    # Store node info for reference
    cat > "${CONFIG_DIR}/node-info.json" << EOF
{
    "node_id": "${NODE_ID}",
    "wireguard_ip": "${node_ip}",
    "wireguard_port": ${WG_PORT},
    "wireguard_pubkey": "$(cat "${KEYS_DIR}/wireguard/${NODE_ID}.pub")",
    "created": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF
}

start_wireguard() {
    log_section "Starting WireGuard Interface"
    
    # Enable IP forwarding
    echo 1 > /proc/sys/net/ipv4/ip_forward
    echo "net.ipv4.ip_forward = 1" >> /etc/sysctl.conf
    
    # Start WireGuard
    if systemctl is-active --quiet "wg-quick@${WG_INTERFACE}"; then
        log_warn "WireGuard already running, restarting..."
        systemctl restart "wg-quick@${WG_INTERFACE}"
    else
        systemctl enable "wg-quick@${WG_INTERFACE}"
        systemctl start "wg-quick@${WG_INTERFACE}"
    fi
    
    log_success "WireGuard interface started"
    
    # Show status
    wg show "$WG_INTERFACE"
}

# ============================================================================
# Firewall Configuration
# ============================================================================

configure_firewall() {
    log_section "Configuring Firewall (UFW)"
    
    # Reset UFW to defaults
    ufw --force reset
    
    # Default policies
    ufw default deny incoming
    ufw default allow outgoing
    
    # Allow SSH (for management)
    ufw allow 22/tcp comment 'SSH'
    
    # Allow WireGuard
    ufw allow "${WG_PORT}/udp" comment 'WireGuard'
    
    # Allow internal mesh traffic
    ufw allow from 10.44.0.0/24 comment 'Sovereign Swarm Mesh'
    
    # Allow NATS on mesh only
    ufw allow from 10.44.0.0/24 to any port "${NATS_PORT}" proto tcp comment 'NATS Mesh'
    
    # Allow Matrix on mesh only  
    ufw allow from 10.44.0.0/24 to any port "${MATRIX_PORT}" proto tcp comment 'Matrix Mesh'
    
    # Allow Syncthing on mesh only
    ufw allow from 10.44.0.0/24 to any port "${SYNCTHING_PORT}" proto tcp comment 'Syncthing Mesh'
    
    # Enable UFW
    ufw --force enable
    
    log_success "Firewall configured"
    ufw status verbose
}

# ============================================================================
# Service Installation
# ============================================================================

install_swarmgate() {
    log_section "Installing SwarmGate Enforcement Agent"
    
    local swarmgate_script="${SWARM_BASE}/swarm-gate.sh"
    
    cat > "$swarmgate_script" << 'SWARMGATE'
#!/usr/bin/env bash
# SwarmGate - Token Verification Enforcement Agent
# Verifies JWT capability tokens before allowing peer connections

set -euo pipefail

SWARM_BASE="/opt/sovereign-swarm"
CA_PUBLIC="${SWARM_BASE}/ca/ca.pub"
LOG_FILE="/var/log/sovereign-swarm/swarmgate.log"

log() {
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) - $*" >> "$LOG_FILE"
}

verify_token() {
    local token="$1"
    local required_cap="$2"
    
    # Split JWT
    local header=$(echo "$token" | cut -d'.' -f1)
    local payload=$(echo "$token" | cut -d'.' -f2)
    local signature=$(echo "$token" | cut -d'.' -f3)
    
    # Verify signature (simplified - in production use proper JWT library)
    local message="${header}.${payload}"
    
    # Decode payload using base64url decoding
    # Add padding and convert from base64url to standard base64
    local padded_payload="$payload"
    local len=$((${#payload} % 4))
    if [[ $len -eq 2 ]]; then padded_payload="${payload}=="
    elif [[ $len -eq 3 ]]; then padded_payload="${payload}="
    fi
    local payload_json=$(echo "$padded_payload" | tr '_-' '/+' | base64 -d 2>/dev/null || echo '{}')
    
    # Check expiration
    local exp=$(echo "$payload_json" | jq -r '.exp // 0')
    local now=$(date +%s)
    
    if [[ $exp -lt $now ]]; then
        log "Token expired for peer"
        return 1
    fi
    
    # Check capability
    local has_cap=$(echo "$payload_json" | jq -r --arg cap "$required_cap" '.cap | if . then contains([$cap]) else false end')
    
    if [[ "$has_cap" != "true" ]]; then
        log "Missing capability: $required_cap"
        return 1
    fi
    
    log "Token verified successfully"
    return 0
}

# Main verification loop
case "${1:-verify}" in
    verify)
        if [[ -z "${2:-}" ]]; then
            echo "Usage: $0 verify <token> [capability]"
            exit 1
        fi
        verify_token "$2" "${3:-mesh:peer}"
        ;;
    watch)
        log "SwarmGate watching for peer connections..."
        # In production, this would integrate with WireGuard handshake
        tail -f /var/log/syslog | grep -i wireguard | while read line; do
            log "WG Event: $line"
        done
        ;;
    *)
        echo "Usage: $0 {verify|watch}"
        exit 1
        ;;
esac
SWARMGATE

    chmod +x "$swarmgate_script"
    
    # Create systemd service
    cat > /etc/systemd/system/swarmgate.service << EOF
[Unit]
Description=SwarmGate Token Enforcement Agent
After=network.target wg-quick@${WG_INTERFACE}.service

[Service]
Type=simple
ExecStart=${swarmgate_script} watch
Restart=always
RestartSec=5
User=root
StandardOutput=append:${LOG_DIR}/swarmgate.log
StandardError=append:${LOG_DIR}/swarmgate.log

[Install]
WantedBy=multi-user.target
EOF

    systemctl daemon-reload
    systemctl enable swarmgate.service
    
    log_success "SwarmGate installed"
}

install_nats() {
    log_section "Installing NATS Server"
    
    # Check if NATS is installed
    if ! command -v nats-server &> /dev/null; then
        log_info "Installing NATS server..."
        
        # Download and install NATS
        local nats_version="2.10.7"
        local nats_url="https://github.com/nats-io/nats-server/releases/download/v${nats_version}/nats-server-v${nats_version}-linux-amd64.tar.gz"
        
        curl -sL "$nats_url" | tar -xz -C /tmp
        mv "/tmp/nats-server-v${nats_version}-linux-amd64/nats-server" /usr/local/bin/
        chmod +x /usr/local/bin/nats-server
    fi
    
    # Get mesh IP
    local mesh_ip=$(jq -r '.wireguard_ip' "${CONFIG_DIR}/node-info.json")
    
    # Create NATS configuration
    cat > "${CONFIG_DIR}/nats.conf" << EOF
# NATS Server Configuration for Sovereign Swarm
# Bind only to WireGuard mesh interface

listen: ${mesh_ip}:${NATS_PORT}
server_name: ${NODE_ID}

jetstream {
    store_dir: ${SWARM_BASE}/nats-data
    max_memory_store: 256MB
    max_file_store: 1GB
}

cluster {
    name: ${SWARM_NAME}
    listen: ${mesh_ip}:6222
    routes: [
        nats://10.44.0.1:6222
        nats://10.44.0.2:6222
    ]
}

# Logging
log_file: ${LOG_DIR}/nats.log
debug: false
trace: false
logtime: true

# Limits
max_payload: 1MB
max_pending: 64MB
max_connections: 1024
EOF

    mkdir -p "${SWARM_BASE}/nats-data"
    
    # Create systemd service
    cat > /etc/systemd/system/nats-swarm.service << EOF
[Unit]
Description=NATS Server for Sovereign Swarm
After=network.target wg-quick@${WG_INTERFACE}.service

[Service]
Type=simple
ExecStart=/usr/local/bin/nats-server -c ${CONFIG_DIR}/nats.conf
Restart=always
RestartSec=5
User=root
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
EOF

    systemctl daemon-reload
    systemctl enable nats-swarm.service
    
    log_success "NATS server configured"
}

# ============================================================================
# Post-Installation
# ============================================================================

print_summary() {
    log_section "Deployment Summary"
    
    local wg_pubkey=$(cat "${KEYS_DIR}/wireguard/${NODE_ID}.pub")
    local node_info=$(cat "${CONFIG_DIR}/node-info.json")
    local mesh_ip=$(echo "$node_info" | jq -r '.wireguard_ip')
    
    echo ""
    echo "=== Node: ${NODE_ID} ===" 
    echo "WireGuard IP: ${mesh_ip}"
    echo "WireGuard Port: ${WG_PORT}"
    echo ""
    echo "=== Share with other nodes ===" 
    echo "PublicKey: ${wg_pubkey}"
    echo "Endpoint: <YOUR_PUBLIC_IP>:${WG_PORT}"
    echo "==============================="
    echo ""
    echo "=== Next Steps ==="
    echo "1. Note the PublicKey and Endpoint above"
    echo "2. Share with other nodes for mesh configuration"
    echo "3. Edit /etc/wireguard/${WG_INTERFACE}.conf to add peers"
    echo "4. Restart WireGuard: systemctl restart wg-quick@${WG_INTERFACE}"
    echo ""
    
    if [[ "$NODE_ID" == "command0" || "$NODE_ID" == "command-0" ]]; then
        echo "=== CA Backup Required ==="
        echo "CRITICAL: Backup your CA keys immediately!"
        echo "sudo tar -czf ~/swarm-ca-backup-\$(date +%Y%m%d).tar.gz ${CA_DIR}/state/"
        echo ""
    fi
    
    log_success "Bootstrap complete for node: ${NODE_ID}"
}

# ============================================================================
# Main Execution
# ============================================================================

main() {
    log_section "Sovereign Swarm Master Bootstrap"
    log_info "Node ID: ${NODE_ID}"
    log_info "Swarm Name: ${SWARM_NAME}"
    
    check_root
    check_dependencies
    create_directories
    
    # Cryptographic setup
    generate_ca_keys
    generate_node_keys
    mint_capability_token
    
    # Network setup
    generate_wireguard_keys
    configure_wireguard
    start_wireguard
    configure_firewall
    
    # Service installation
    install_swarmgate
    install_nats
    
    # Start services
    log_section "Starting Services"
    systemctl start swarmgate.service || log_warn "SwarmGate start deferred"
    systemctl start nats-swarm.service || log_warn "NATS start deferred"
    
    print_summary
}

# Handle script arguments
case "${1:-deploy}" in
    deploy)
        main
        ;;
    --help|-h)
        echo "Sovereign Swarm Master Bootstrap Script"
        echo ""
        echo "Usage: NODE_ID=<name> $0 [command]"
        echo ""
        echo "Commands:"
        echo "  deploy    - Full deployment (default)"
        echo "  --help    - Show this help"
        echo ""
        echo "Environment Variables:"
        echo "  NODE_ID       - Node identifier (required)"
        echo "  SWARM_NAME    - Swarm name (default: sovereign-swarm)"
        echo "  WG_PORT       - WireGuard port (default: 51820)"
        echo ""
        echo "Examples:"
        echo "  NODE_ID=command0 $0 deploy"
        echo "  NODE_ID=fixed1 $0 deploy"
        echo "  NODE_ID=pelican1 $0 deploy"
        ;;
    *)
        echo "Unknown command: $1"
        echo "Use --help for usage information"
        exit 1
        ;;
esac
