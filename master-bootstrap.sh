#!/usr/bin/env bash
# master-bootstrap.sh v0.1.3 — Hardened Sovereign Swarm Bootstrap
# Sovereign Swarm — Zero-Trust AI Orchestration Mesh
# Apache-2.0 License
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/strategickhaos/sovereign-swarm/main/master-bootstrap.sh -o /tmp/ss.sh
#   sudo bash /tmp/ss.sh                     # runs as command0
#   sudo NODE_ID=edge3 /opt/sovereign-swarm/master-bootstrap.sh

set -euo pipefail

# === CONFIGURATION ===
SWARM_VERSION="0.1.3"
SWARM_HOME="${SWARM_HOME:-/opt/sovereign-swarm}"
NODE_ID="${NODE_ID:-command0}"
SWARM_DOMAIN="${SWARM_DOMAIN:-localhost}"
LOG_FILE="${SWARM_HOME}/logs/bootstrap-$(date +%Y%m%d-%H%M%S).log"

# Service ports
WG_PORT="${WG_PORT:-51820}"
NATS_PORT="${NATS_PORT:-4222}"
MATRIX_PORT="${MATRIX_PORT:-8008}"

# Network configuration
WG_NETWORK="${WG_NETWORK:-10.100.0.0/24}"
WG_ADDRESS="${WG_ADDRESS:-10.100.0.1/24}"

# === LOGGING ===
log() { 
    local msg
    msg="[$(date -u +%FT%TZ)] [INFO] $*"
    printf '%s\n' "${msg}"
    printf '%s\n' "${msg}" >> "${LOG_FILE}" 2>/dev/null || true
}

warn() {
    local msg
    msg="[$(date -u +%FT%TZ)] [WARN] $*"
    printf '%s\n' "${msg}" >&2
    printf '%s\n' "${msg}" >> "${LOG_FILE}" 2>/dev/null || true
}

die() {
    local msg
    msg="[$(date -u +%FT%TZ)] [ERROR] $*"
    printf '%s\n' "${msg}" >&2
    printf '%s\n' "${msg}" >> "${LOG_FILE}" 2>/dev/null || true
    exit 1
}

# === VALIDATION ===
check_root() {
    [[ $EUID -eq 0 ]] || die "This script must be run as root (use sudo)"
}

check_os() {
    if [[ -f /etc/os-release ]]; then
        # shellcheck source=/dev/null
        source /etc/os-release
        case "${ID:-}" in
            ubuntu)
                case "${VERSION_ID:-}" in
                    22.04|24.04)
                        log "Detected supported OS: Ubuntu ${VERSION_ID}"
                        ;;
                    *)
                        warn "Ubuntu ${VERSION_ID} not officially supported, proceeding anyway"
                        ;;
                esac
                ;;
            debian)
                log "Detected Debian, proceeding with Ubuntu-compatible setup"
                ;;
            *)
                warn "OS '${ID}' not officially supported, proceeding anyway"
                ;;
        esac
    else
        warn "Could not detect OS, proceeding anyway"
    fi
}

check_network() {
    log "Checking network connectivity..."
    
    # In air-gapped mode, skip external connectivity checks
    if [[ "${AIRGAPPED:-false}" == "true" ]]; then
        log "Air-gapped mode enabled, skipping external connectivity check"
        PUBLIC_IP="airgapped"
        return 0
    fi
    
    # Check if we have a public IP or at least network access
    if command -v curl &>/dev/null; then
        if curl -s --max-time 5 https://api.ipify.org &>/dev/null; then
            PUBLIC_IP=$(curl -s --max-time 5 https://api.ipify.org)
            log "Detected public IP: ${PUBLIC_IP}"
        else
            warn "Could not detect public IP (air-gapped mode?)"
            PUBLIC_IP="unknown"
        fi
    else
        warn "curl not available, skipping public IP detection"
        PUBLIC_IP="unknown"
    fi
}

# === DIRECTORY SETUP ===
setup_directories() {
    log "Setting up directory structure..."
    
    mkdir -p "${SWARM_HOME}"/{ca/state,nats,matrix,wireguard,nodes,logs,artifacts}
    chmod 700 "${SWARM_HOME}/ca/state"
    
    # Create log file
    touch "${LOG_FILE}"
    chmod 600 "${LOG_FILE}"
    
    log "Directories created at ${SWARM_HOME}"
}

# === PACKAGE INSTALLATION ===
install_dependencies() {
    log "Installing dependencies..."
    
    # Update package lists
    apt-get update -qq
    
    # Core packages
    DEBIAN_FRONTEND=noninteractive apt-get install -y -qq \
        curl \
        wget \
        gnupg \
        ca-certificates \
        openssl \
        jq \
        git \
        wireguard \
        wireguard-tools \
        iptables \
        ufw \
        || die "Failed to install core packages"
    
    log "Core packages installed"
}

install_nats() {
    log "Installing NATS server..."
    
    local nats_version="${NATS_VERSION:-2.10.7}"
    local nats_url="https://github.com/nats-io/nats-server/releases/download/v${nats_version}/nats-server-v${nats_version}-linux-amd64.tar.gz"
    local nats_dir="/opt/nats"
    local offline_archive="${SWARM_HOME}/artifacts/nats-server-v${nats_version}-linux-amd64.tar.gz"
    
    if [[ -x "${nats_dir}/nats-server" ]]; then
        log "NATS server already installed"
        return 0
    fi
    
    mkdir -p "${nats_dir}"
    
    # Check for pre-staged offline archive first (air-gapped mode)
    if [[ -f "${offline_archive}" ]]; then
        log "Using pre-staged NATS archive for air-gapped installation"
        tar -xzf "${offline_archive}" -C /tmp
        mv /tmp/nats-server-v${nats_version}-linux-amd64/nats-server "${nats_dir}/"
        chmod +x "${nats_dir}/nats-server"
        rm -rf /tmp/nats-server-*
        log "NATS server installed from offline archive"
        return 0
    fi
    
    # Fall back to downloading if not air-gapped
    if [[ "${AIRGAPPED:-false}" == "true" ]]; then
        warn "Air-gapped mode enabled but no pre-staged NATS archive found at ${offline_archive}"
        warn "Please pre-stage the NATS binary for air-gapped installation"
        return 1
    fi
    
    if curl -fsSL "${nats_url}" -o /tmp/nats.tar.gz; then
        tar -xzf /tmp/nats.tar.gz -C /tmp
        mv /tmp/nats-server-v${nats_version}-linux-amd64/nats-server "${nats_dir}/"
        chmod +x "${nats_dir}/nats-server"
        rm -rf /tmp/nats.tar.gz /tmp/nats-server-*
        log "NATS server installed to ${nats_dir}"
    else
        warn "Failed to download NATS server (offline mode?)"
    fi
}

# === WIREGUARD SETUP ===
setup_wireguard() {
    log "Configuring WireGuard..."
    
    local wg_dir="/etc/wireguard"
    local node_wg_dir="${SWARM_HOME}/nodes/${NODE_ID}/wireguard"
    
    mkdir -p "${node_wg_dir}"
    chmod 700 "${node_wg_dir}"
    
    # Generate keys if not exist
    if [[ ! -f "${node_wg_dir}/privatekey" ]]; then
        log "Generating WireGuard keys for ${NODE_ID}..."
        wg genkey > "${node_wg_dir}/privatekey"
        chmod 600 "${node_wg_dir}/privatekey"
        wg pubkey < "${node_wg_dir}/privatekey" > "${node_wg_dir}/publickey"
        wg genpsk > "${node_wg_dir}/presharedkey"
        chmod 600 "${node_wg_dir}/presharedkey"
    fi
    
    local private_key
    private_key=$(cat "${node_wg_dir}/privatekey")
    
    # Generate WireGuard config
    cat > "${wg_dir}/wg0.conf" <<EOF
# Sovereign Swarm WireGuard Configuration
# Node: ${NODE_ID}
# Generated: $(date -u +%FT%TZ)

[Interface]
Address = ${WG_ADDRESS}
ListenPort = ${WG_PORT}
PrivateKey = ${private_key}

PostUp = iptables -A FORWARD -i %i -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE || true
PostDown = iptables -D FORWARD -i %i -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE || true

# Add peers here
# [Peer]
# PublicKey = <peer_public_key>
# AllowedIPs = <peer_ip>/32
# Endpoint = <peer_endpoint>:${WG_PORT}
# PersistentKeepalive = 25
EOF
    
    chmod 600 "${wg_dir}/wg0.conf"
    
    # Enable and start WireGuard
    systemctl enable wg-quick@wg0 || true
    systemctl start wg-quick@wg0 || warn "Failed to start WireGuard (may need reboot)"
    
    log "WireGuard configured for ${NODE_ID}"
}

# === CERTIFICATE AUTHORITY ===
setup_ca() {
    log "Setting up Certificate Authority..."
    
    export CA_DIR="${SWARM_HOME}/ca"
    
    if [[ -f "${SWARM_HOME}/ca/init_ca.sh" ]]; then
        bash "${SWARM_HOME}/ca/init_ca.sh"
    else
        warn "CA initialization script not found, creating inline..."
        
        local ca_state="${CA_DIR}/state"
        mkdir -p "${ca_state}"/{certs,newcerts,private}
        chmod 700 "${ca_state}/private"
        
        if [[ ! -f "${ca_state}/private/ca.key" ]]; then
            openssl genrsa -out "${ca_state}/private/ca.key" 4096
            chmod 600 "${ca_state}/private/ca.key"
        fi
        
        if [[ ! -f "${ca_state}/certs/ca.crt" ]]; then
            openssl req -new -x509 \
                -key "${ca_state}/private/ca.key" \
                -out "${ca_state}/certs/ca.crt" \
                -days 3650 \
                -subj "/CN=Sovereign Swarm CA/O=Legion of Minds/OU=Infrastructure"
        fi
    fi
    
    log "CA setup complete"
}

# === FIREWALL CONFIGURATION ===
setup_firewall() {
    log "Configuring firewall..."
    
    # Allow SSH
    ufw allow 22/tcp comment 'SSH'
    
    # Allow WireGuard
    ufw allow "${WG_PORT}/udp" comment 'WireGuard'
    
    # Allow NATS
    ufw allow "${NATS_PORT}/tcp" comment 'NATS'
    
    # Allow Matrix
    ufw allow "${MATRIX_PORT}/tcp" comment 'Matrix Synapse'
    
    # Enable firewall
    ufw --force enable
    
    log "Firewall configured"
}

# === SYSTEMD SERVICES ===
create_services() {
    log "Creating systemd services..."
    
    # NATS service
    cat > /etc/systemd/system/sovereign-nats.service <<EOF
[Unit]
Description=Sovereign Swarm NATS Server
After=network.target

[Service]
Type=simple
ExecStart=/opt/nats/nats-server -c ${SWARM_HOME}/nats/nats-server.conf
Restart=always
RestartSec=5
User=root

[Install]
WantedBy=multi-user.target
EOF
    
    systemctl daemon-reload
    
    log "Systemd services created"
}

# === NATS CONFIGURATION ===
configure_nats() {
    log "Configuring NATS..."
    
    local nats_conf="${SWARM_HOME}/nats/nats-server.conf"
    
    cat > "${nats_conf}" <<EOF
# Sovereign Swarm NATS Configuration
# Node: ${NODE_ID}
# Generated: $(date -u +%FT%TZ)

server_name: ${NODE_ID}-nats

listen: 0.0.0.0:${NATS_PORT}
http_port: 8222

jetstream {
    store_dir: ${SWARM_HOME}/nats/jetstream
    max_mem: 256MB
    max_file: 1GB
}

debug: false
trace: false
logtime: true
log_file: ${SWARM_HOME}/logs/nats-server.log
EOF
    
    mkdir -p "${SWARM_HOME}/nats/jetstream"
    
    log "NATS configured"
}

# === HEALTH CHECK ===
health_check() {
    log "Running health checks..."
    
    local status=0
    
    # Check WireGuard
    if wg show wg0 &>/dev/null; then
        log "✓ WireGuard: OK"
    else
        warn "✗ WireGuard: NOT RUNNING"
        status=1
    fi
    
    # Check NATS (if installed)
    if [[ -x /opt/nats/nats-server ]]; then
        if curl -s http://localhost:8222/healthz &>/dev/null; then
            log "✓ NATS: OK"
        else
            warn "✗ NATS: NOT RESPONDING"
            status=1
        fi
    fi
    
    return ${status}
}

# === MAIN ===
main() {
    log "=========================================="
    log "Sovereign Swarm Bootstrap v${SWARM_VERSION}"
    log "Node ID: ${NODE_ID}"
    log "Domain: ${SWARM_DOMAIN}"
    log "=========================================="
    
    check_root
    check_os
    setup_directories
    check_network
    
    install_dependencies
    install_nats
    
    setup_ca
    setup_wireguard
    setup_firewall
    
    configure_nats
    create_services
    
    # Start services
    log "Starting services..."
    systemctl start sovereign-nats || warn "NATS failed to start (may need config)"
    
    # Final health check
    log "Running final health check..."
    health_check || true
    
    log "=========================================="
    log "Bootstrap complete!"
    log "=========================================="
    log ""
    log "Troubleshooting commands:"
    log "  wg show                              # WireGuard status"
    log "  nats bench test --msgs 1000 --size 128  # NATS benchmark"
    log "  curl http://localhost:8008/health   # Matrix health"
    log ""
    log "Node public key: $(cat "${SWARM_HOME}/nodes/${NODE_ID}/wireguard/publickey" 2>/dev/null || echo 'N/A')"
    log ""
    log "Next steps:"
    log "  1. Add peer nodes by editing /etc/wireguard/wg0.conf"
    log "  2. Exchange public keys with other nodes"
    log "  3. Run: sudo wg-quick down wg0 && sudo wg-quick up wg0"
    log ""
}

# Run main
main "$@"
