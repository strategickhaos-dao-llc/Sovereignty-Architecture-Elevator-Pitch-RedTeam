#!/usr/bin/env bash
#===============================================================================
# Sovereignty Architecture - Master Bootstrap Script
# Deploys a sovereign edge node with WireGuard VPN, NATS messaging, and
# Matrix/Synapse for secure, decentralized infrastructure.
#
# Usage: sudo NODE_ID=edge3 ./master-bootstrap.sh
#
# Tested on: Ubuntu 24.04 LTS
# Version: 1.0.0
#===============================================================================
set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPT_DIR
readonly LOG_FILE="${SCRIPT_DIR}/bootstrap.log"
readonly ARTIFACTS_DIR="${SCRIPT_DIR}/artifacts"

# Network configuration
readonly WG_PORT=51820
readonly WG_INTERFACE="wg0"
readonly WG_SUBNET="10.44.0.0/16"
readonly NATS_CLIENT_PORT=4222
readonly NATS_MONITOR_PORT=8222
readonly SYNAPSE_PORT=8008

# Colors for output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m' # No Color

#===============================================================================
# Logging Functions
#===============================================================================
log() {
    local level="$1"
    shift
    local message="$*"
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "${timestamp} [${level}] ${message}" >> "${LOG_FILE}"
    case "${level}" in
        OK)     echo -e "${GREEN}[+]${NC} ${message}" ;;
        WARN)   echo -e "${YELLOW}[!]${NC} ${message}" ;;
        ERROR)  echo -e "${RED}[-]${NC} ${message}" ;;
        INFO)   echo -e "${BLUE}[*]${NC} ${message}" ;;
    esac
}

die() {
    log ERROR "$*"
    exit 1
}

#===============================================================================
# Prerequisites Check
#===============================================================================
check_prerequisites() {
    log INFO "Checking prerequisites..."

    # Check root privileges
    if [[ $EUID -ne 0 ]]; then
        die "This script must be run as root (use sudo)"
    fi

    # Check NODE_ID
    if [[ -z "${NODE_ID:-}" ]]; then
        die "NODE_ID environment variable is required. Usage: sudo NODE_ID=edge3 ./master-bootstrap.sh"
    fi

    # Check Ubuntu version
    if [[ -f /etc/os-release ]]; then
        # shellcheck source=/dev/null
        source /etc/os-release
        log INFO "Detected OS: ${PRETTY_NAME:-Unknown}"
    fi

    # Check internet connectivity
    if ! ping -c 1 -W 5 8.8.8.8 &>/dev/null; then
        log WARN "Internet connectivity check failed - some packages may not install"
    fi

    log OK "Prerequisites check passed"
}

#===============================================================================
# System Setup
#===============================================================================
setup_system() {
    log INFO "Updating system packages..."

    export DEBIAN_FRONTEND=noninteractive
    apt-get update -qq
    apt-get upgrade -y -qq

    log INFO "Installing required packages..."
    apt-get install -y -qq \
        wireguard \
        wireguard-tools \
        docker.io \
        docker-compose-plugin \
        ufw \
        curl \
        jq \
        gnupg2 \
        lsb-release \
        ca-certificates \
        apt-transport-https \
        software-properties-common

    # Enable and start Docker
    systemctl enable docker
    systemctl start docker

    log OK "System packages installed"
}

#===============================================================================
# WireGuard Setup
#===============================================================================
setup_wireguard() {
    log INFO "Setting up WireGuard VPN..."

    # Create WireGuard directory
    mkdir -p /etc/wireguard
    chmod 700 /etc/wireguard

    # Generate keys if not exist
    if [[ ! -f /etc/wireguard/private.key ]]; then
        wg genkey | tee /etc/wireguard/private.key | wg pubkey > /etc/wireguard/public.key
        chmod 600 /etc/wireguard/private.key
        log INFO "Generated new WireGuard keypair"
    fi

    local private_key
    private_key=$(cat /etc/wireguard/private.key)
    local public_key
    public_key=$(cat /etc/wireguard/public.key)

    # Determine node IP based on NODE_ID
    local node_number
    node_number=$(echo "${NODE_ID}" | grep -oE '[0-9]+$' || echo "1")
    local node_ip="10.44.0.${node_number}"

    # Create WireGuard configuration
    cat > "/etc/wireguard/${WG_INTERFACE}.conf" << EOF
[Interface]
Address = ${node_ip}/16
PrivateKey = ${private_key}
ListenPort = ${WG_PORT}
SaveConfig = false

# Peer configuration (Command-0)
# These placeholders will be replaced when connecting to the mesh
[Peer]
# Command-0 Public Key (replace with actual key)
PublicKey = COMMAND_0_PUBLIC_KEY_PLACEHOLDER
# Command-0 Endpoint (replace with actual endpoint)
Endpoint = COMMAND_0_ENDPOINT_PLACEHOLDER:${WG_PORT}
AllowedIPs = ${WG_SUBNET}
PersistentKeepalive = 25
EOF

    chmod 600 "/etc/wireguard/${WG_INTERFACE}.conf"

    # Enable and start WireGuard
    systemctl enable "wg-quick@${WG_INTERFACE}"
    systemctl restart "wg-quick@${WG_INTERFACE}" || {
        log WARN "WireGuard service restart - may need peer configuration"
    }

    # Store public key for sharing
    echo "${public_key}" > "${ARTIFACTS_DIR}/${NODE_ID}-pubkey.txt"

    log OK "WireGuard configured with public key: ${public_key}"
}

#===============================================================================
# NATS Setup
#===============================================================================
setup_nats() {
    log INFO "Setting up NATS messaging server..."

    # Create NATS configuration directory
    mkdir -p /etc/nats

    # Download NATS server if not installed
    if ! command -v nats-server &>/dev/null; then
        log INFO "Installing NATS server..."
        curl -sfL https://get.nats.io -o /tmp/install-nats.sh
        chmod +x /tmp/install-nats.sh
        /tmp/install-nats.sh -s nats-server
        rm -f /tmp/install-nats.sh
    fi

    # Create NATS configuration
    cat > /etc/nats/nats.conf << EOF
# NATS Server Configuration for ${NODE_ID}
# Sovereign Swarm Node

# Server identification
server_name: ${NODE_ID}

# Network binding - localhost only for security
# WireGuard provides external connectivity
host: 127.0.0.1
port: ${NATS_CLIENT_PORT}

# HTTP monitoring
http_port: ${NATS_MONITOR_PORT}

# JetStream configuration for persistence
jetstream {
    store_dir: /var/lib/nats/jetstream
    max_mem: 256MB
    max_file: 1GB
}

# Leafnode configuration for mesh connectivity
leafnodes {
    host: 127.0.0.1
    port: 7422
}

# Logging
debug: false
trace: false
logfile: /var/log/nats/nats.log
logfile_size_limit: 100MB

# Security
max_connections: 1024
max_payload: 8MB
max_pending: 64MB
EOF

    # Create NATS directories
    mkdir -p /var/lib/nats/jetstream
    mkdir -p /var/log/nats

    # Create systemd service
    cat > /etc/systemd/system/nats.service << EOF
[Unit]
Description=NATS Server
After=network.target

[Service]
Type=simple
ExecStart=/usr/local/bin/nats-server -c /etc/nats/nats.conf
ExecReload=/bin/kill -HUP $MAINPID
Restart=on-failure
RestartSec=5
LimitNOFILE=65536
User=root
Group=root

[Install]
WantedBy=multi-user.target
EOF

    # Enable and start NATS
    systemctl daemon-reload
    systemctl enable nats
    systemctl restart nats

    log OK "NATS server configured and running"
}

#===============================================================================
# Synapse (Matrix) Setup
#===============================================================================
setup_synapse() {
    log INFO "Setting up Matrix Synapse via Docker..."

    # Create Synapse data directory
    mkdir -p /opt/synapse/data

    # Generate Synapse configuration if not exists
    if [[ ! -f /opt/synapse/data/homeserver.yaml ]]; then
        docker run --rm \
            -v /opt/synapse/data:/data \
            -e SYNAPSE_SERVER_NAME="${NODE_ID}.sovereign.local" \
            -e SYNAPSE_REPORT_STATS=no \
            matrixdotorg/synapse:latest generate
    fi

    # Create docker-compose for Synapse
    cat > /opt/synapse/docker-compose.yml << EOF
version: '3.8'
services:
  synapse:
    image: matrixdotorg/synapse:latest
    container_name: synapse
    restart: unless-stopped
    environment:
      - SYNAPSE_SERVER_NAME=${NODE_ID}.sovereign.local
      - SYNAPSE_REPORT_STATS=no
    volumes:
      - /opt/synapse/data:/data
    ports:
      - "127.0.0.1:${SYNAPSE_PORT}:8008"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8008/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
EOF

    # Start Synapse
    cd /opt/synapse
    docker compose up -d

    log OK "Matrix Synapse configured and running"
}

#===============================================================================
# Firewall Configuration
#===============================================================================
configure_firewall() {
    log INFO "Configuring firewall rules..."

    # Enable UFW
    ufw --force enable

    # Default policies
    ufw default deny incoming
    ufw default allow outgoing

    # Allow SSH
    ufw allow 22/tcp comment 'SSH'

    # Allow WireGuard
    ufw allow "${WG_PORT}/udp" comment 'WireGuard'

    # Allow Synapse HTTP (for federation)
    ufw allow "${SYNAPSE_PORT}/tcp" comment 'Synapse'

    # Allow NATS client from swarm only
    ufw allow from "${WG_SUBNET}" to any port "${NATS_CLIENT_PORT}" proto tcp comment 'NATS client'

    # Reload firewall
    ufw reload

    log OK "Firewall configured"
}

#===============================================================================
# Generate Artifacts
#===============================================================================
generate_artifacts() {
    log INFO "Generating node artifacts..."

    mkdir -p "${ARTIFACTS_DIR}"

    local public_key
    public_key=$(cat /etc/wireguard/public.key 2>/dev/null || echo "NOT_GENERATED")

    local public_ip
    public_ip=$(curl -sf4 https://ifconfig.me 2>/dev/null || hostname -I | awk '{print $1}')

    # Create node info file
    cat > "${ARTIFACTS_DIR}/${NODE_ID}-info.txt" << EOF
=== ${NODE_ID} ===
PublicKey: ${public_key}
Endpoint : ${public_ip}:${WG_PORT}
=============
EOF

    # Create artifact bundle
    tar -czf "${ARTIFACTS_DIR}/${NODE_ID}-artifacts.tgz" \
        -C "${ARTIFACTS_DIR}" \
        "${NODE_ID}-info.txt" \
        "${NODE_ID}-pubkey.txt" 2>/dev/null || true

    log OK "Artifact bundle created: artifacts/${NODE_ID}-artifacts.tgz"
}

#===============================================================================
# Display Status
#===============================================================================
display_status() {
    echo
    echo -e "${GREEN}[+] Bootstrap complete for ${NODE_ID}.${NC}"
    cat "${ARTIFACTS_DIR}/${NODE_ID}-info.txt"
    echo
    log OK "Bootstrap complete for ${NODE_ID}."
}

#===============================================================================
# Main Execution
#===============================================================================
main() {
    echo "=============================================="
    echo " Sovereignty Architecture - Edge Bootstrap"
    echo " Node ID: ${NODE_ID:-NOT_SET}"
    echo "=============================================="
    echo

    # Initialize log
    mkdir -p "$(dirname "${LOG_FILE}")"
    mkdir -p "${ARTIFACTS_DIR}"
    echo "=== Bootstrap started at $(date) ===" >> "${LOG_FILE}"

    check_prerequisites
    setup_system
    setup_wireguard
    setup_nats
    setup_synapse
    configure_firewall
    generate_artifacts
    display_status

    echo "=== Bootstrap completed at $(date) ===" >> "${LOG_FILE}"
}

# Execute main function
main "$@"
