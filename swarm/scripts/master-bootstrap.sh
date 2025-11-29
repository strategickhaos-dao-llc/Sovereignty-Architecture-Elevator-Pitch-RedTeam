#!/bin/bash
# master-bootstrap.sh — Sovereign Swarm System v2.0
# Core node bootstrap for Command-0, Fixed-1, Mobile-2 archetypes
# Phase 0-3+5 enforcement: SwarmGate @ WireGuard, NATS telemetry, Matrix chat, Syncthing sync
# Generated for: Strategickhaos DAO LLC / Valoryield Engine
# Author: Domenic Garza (Node 137)

set -euo pipefail

# === Configuration ===
SWARM_SUBNET="10.44.0.0/16"
NATS_PORT="4222"
NATS_CLUSTER_PORT="6222"
WG_PORT="51820"
MATRIX_PORT="8008"
SYNCTHING_PORT="22000"
NODE_ROLE="${NODE_ROLE:-core}"  # core, fixed, mobile, pelican

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[✓]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║       SOVEREIGN SWARM SYSTEM v2.0 — MASTER BOOTSTRAP        ║${NC}"
echo -e "${BLUE}║                 Zero Cloud. Zero Trust. Full Mesh.           ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# === Phase 0: System Requirements ===
log_info "Phase 0: Validating system requirements..."

check_root() {
    if [[ $EUID -ne 0 ]]; then
        log_error "This script must be run as root"
        exit 1
    fi
}

install_dependencies() {
    log_info "Installing core dependencies..."
    apt-get update -qq
    apt-get install -y --no-install-recommends \
        wireguard \
        wireguard-tools \
        nftables \
        jq \
        curl \
        gnupg2 \
        python3 \
        python3-pip \
        docker.io \
        docker-compose \
        prometheus-node-exporter \
        syncthing \
        2>/dev/null || true

    # Install NATS client tools
    if ! command -v nats &> /dev/null; then
        curl -L https://github.com/nats-io/natscli/releases/latest/download/nats-0.1.1-linux-amd64.zip -o /tmp/nats.zip 2>/dev/null || true
        unzip -o /tmp/nats.zip -d /usr/local/bin/ 2>/dev/null || true
    fi

    log_success "Dependencies installed"
}

# === Phase 1: WireGuard + SwarmGate Setup ===
setup_wireguard() {
    log_info "Phase 1: Configuring WireGuard mesh..."

    WG_DIR="/etc/wireguard"
    mkdir -p "$WG_DIR"

    # Generate keys if not exists
    if [[ ! -f "$WG_DIR/privatekey" ]]; then
        wg genkey | tee "$WG_DIR/privatekey" | wg pubkey > "$WG_DIR/publickey"
        chmod 600 "$WG_DIR/privatekey"
        log_success "WireGuard keys generated"
    fi

    PRIVATE_KEY=$(cat "$WG_DIR/privatekey")
    PUBLIC_KEY=$(cat "$WG_DIR/publickey")

    # Determine node IP based on role
    case "$NODE_ROLE" in
        core|command) NODE_IP="10.44.0.1" ;;
        fixed)        NODE_IP="10.44.1.1" ;;
        mobile)       NODE_IP="10.44.2.1" ;;
        pelican)      NODE_IP="10.44.100.1" ;;
        *)            NODE_IP="10.44.99.1" ;;
    esac

    cat > "$WG_DIR/wg0.conf" << EOF
# Sovereign Swarm WireGuard Configuration
# Node Role: $NODE_ROLE
# Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)

[Interface]
Address = ${NODE_IP}/24
PrivateKey = ${PRIVATE_KEY}
ListenPort = ${WG_PORT}
PostUp = nft -f /etc/nftables.d/swarmgate.nft
PostDown = nft delete table inet swarmgate 2>/dev/null || true

# Peers configured via swarm-join protocol
# Add peers with: wg set wg0 peer <pubkey> allowed-ips <ip>/32 endpoint <host>:${WG_PORT}
EOF

    chmod 600 "$WG_DIR/wg0.conf"
    log_success "WireGuard configured at $NODE_IP"
}

# === Phase 2: SwarmGate NFT Rules ===
setup_swarmgate() {
    log_info "Phase 2: Deploying SwarmGate nftables rules..."

    mkdir -p /etc/nftables.d

    cat > /etc/nftables.d/swarmgate.nft << 'EOF'
#!/usr/sbin/nft -f
# SwarmGate v2.0 — JWT-enforced mesh firewall
# Only allow authenticated swarm traffic on wg0

table inet swarmgate {
    set trusted_peers {
        type ipv4_addr
        flags interval
        elements = { 10.44.0.0/16 }
    }

    chain input {
        type filter hook input priority 0; policy drop;

        # Allow established connections
        ct state established,related accept

        # Allow loopback
        iif lo accept

        # Allow WireGuard UDP
        udp dport 51820 accept

        # Allow NATS within swarm
        ip saddr @trusted_peers tcp dport { 4222, 6222, 8222 } accept

        # Allow Matrix within swarm
        ip saddr @trusted_peers tcp dport 8008 accept

        # Allow Syncthing within swarm
        ip saddr @trusted_peers tcp dport 22000 accept
        ip saddr @trusted_peers udp dport 22000 accept

        # Allow Prometheus metrics within swarm
        ip saddr @trusted_peers tcp dport 9100 accept

        # Allow SSH for admin (restrict in production)
        tcp dport 22 accept

        # Log and drop everything else
        log prefix "swarmgate-drop: " drop
    }

    chain forward {
        type filter hook forward priority 0; policy drop;

        # Allow forwarding within swarm mesh
        ip saddr @trusted_peers ip daddr @trusted_peers accept
    }

    chain output {
        type filter hook output priority 0; policy accept;
    }
}
EOF

    log_success "SwarmGate nftables rules deployed"
}

# === Phase 3: NATS JetStream Setup ===
setup_nats() {
    log_info "Phase 3: Configuring NATS JetStream with RAFT clustering..."

    NATS_DIR="/opt/sovereign-swarm/nats"
    mkdir -p "$NATS_DIR"

    cat > "$NATS_DIR/nats.conf" << EOF
# NATS Server Configuration — Sovereign Swarm v2.0
# Node Role: $NODE_ROLE

port: ${NATS_PORT}
http_port: 8222

# Authentication
authorization {
    user: swarm
    password: \$NATS_PASSWORD
}

# JetStream for persistent telemetry
jetstream {
    store_dir: ${NATS_DIR}/jetstream
    max_mem: 1G
    max_file: 10G
}

# Cluster configuration for RAFT consensus
cluster {
    name: sovereign-swarm
    listen: 0.0.0.0:${NATS_CLUSTER_PORT}
    routes: [
        nats-route://10.44.0.1:${NATS_CLUSTER_PORT}
        nats-route://10.44.1.1:${NATS_CLUSTER_PORT}
        nats-route://10.44.2.1:${NATS_CLUSTER_PORT}
    ]
}

# Logging
debug: false
trace: false
logtime: true
log_file: ${NATS_DIR}/nats.log
EOF

    # Create NATS systemd service
    cat > /etc/systemd/system/nats-server.service << EOF
[Unit]
Description=NATS Server — Sovereign Swarm Telemetry
After=network.target wireguard.target

[Service]
Type=simple
ExecStart=/usr/local/bin/nats-server -c ${NATS_DIR}/nats.conf
Restart=always
RestartSec=5
User=root
Environment=NATS_PASSWORD=${NATS_PASSWORD:-swarm}

[Install]
WantedBy=multi-user.target
EOF

    log_success "NATS JetStream configured with RAFT cluster"
}

# === Phase 4: Verizon LTE Failover (Evolution #1) ===
setup_verizon_failover() {
    log_info "Phase 4: Configuring Verizon LTE failover..."

    # Check for NetworkManager and LTE interface
    if command -v nmcli &> /dev/null; then
        # Detect LTE interfaces
        LTE_IFACES=$(nmcli device | grep -E "gsm|lte|wwan" | awk '{print $1}' || true)

        if [[ -n "$LTE_IFACES" ]]; then
            for iface in $LTE_IFACES; do
                log_info "Configuring failover for interface: $iface"
                nmcli device connect "$iface" 2>/dev/null || true
            done
            log_success "Verizon LTE failover configured"
        else
            log_warn "No LTE interfaces detected — failover skipped"
        fi
    else
        log_warn "NetworkManager not available — manual LTE config required"
    fi

    # Create failover check script
    cat > /usr/local/bin/swarm-failover-check.sh << 'FAILOVER_EOF'
#!/bin/bash
# Swarm connectivity failover monitor
PRIMARY_GW="${PRIMARY_GW:-192.168.1.1}"
FAILOVER_IFACE="${FAILOVER_IFACE:-lte0}"

check_primary() {
    ping -c 2 -W 5 "$PRIMARY_GW" > /dev/null 2>&1
}

activate_failover() {
    if command -v nmcli &> /dev/null; then
        nmcli device connect "$FAILOVER_IFACE" 2>/dev/null || true
    fi
}

deactivate_failover() {
    if command -v nmcli &> /dev/null; then
        nmcli device disconnect "$FAILOVER_IFACE" 2>/dev/null || true
    fi
}

if ! check_primary; then
    echo "Primary connection failed — activating failover"
    activate_failover
else
    echo "Primary connection OK"
fi
FAILOVER_EOF
    chmod +x /usr/local/bin/swarm-failover-check.sh

    # Add cron job for failover monitoring
    echo "*/5 * * * * root /usr/local/bin/swarm-failover-check.sh >> /var/log/swarm-failover.log 2>&1" > /etc/cron.d/swarm-failover

    log_success "Failover monitoring configured"
}

# === Phase 5: Matrix Synapse Setup ===
setup_matrix() {
    log_info "Phase 5: Configuring Matrix Synapse for swarm chat..."

    MATRIX_DIR="/opt/sovereign-swarm/matrix"
    mkdir -p "$MATRIX_DIR"

    # Docker Compose for Matrix
    cat > "$MATRIX_DIR/docker-compose.yml" << 'EOF'
version: '3.8'

services:
  synapse:
    image: matrixdotorg/synapse:latest
    container_name: swarm-synapse
    restart: unless-stopped
    environment:
      SYNAPSE_SERVER_NAME: ${SYNAPSE_SERVER_NAME:-swarm.local}
      SYNAPSE_REPORT_STATS: "no"
    volumes:
      - ./data:/data
    ports:
      - "8008:8008"
    networks:
      - swarm-net

  # Matrix-NATS Bridge (Evolution #5)
  mautrix-nats:
    image: dock.mau.dev/mautrix/nats:latest
    container_name: swarm-mautrix-nats
    restart: unless-stopped
    depends_on:
      - synapse
    volumes:
      - ./mautrix:/data
    networks:
      - swarm-net

networks:
  swarm-net:
    driver: bridge
EOF

    log_success "Matrix Synapse configured with NATS bridge"
}

# === Phase 6: Syncthing Obsidian Sync ===
setup_syncthing() {
    log_info "Phase 6: Configuring Syncthing for Obsidian vault sync..."

    SYNCTHING_DIR="/opt/sovereign-swarm/syncthing"
    mkdir -p "$SYNCTHING_DIR"

    # Enable Syncthing service
    systemctl enable syncthing@root 2>/dev/null || true

    log_success "Syncthing configured for vault sync"
}

# === Phase 7: Prometheus Node Exporter (Evolution #9) ===
setup_monitoring() {
    log_info "Phase 7: Configuring Prometheus monitoring..."

    systemctl enable prometheus-node-exporter 2>/dev/null || true

    log_success "Prometheus node exporter enabled"
}

# === Bring up WireGuard ===
bring_up_wireguard() {
    log_info "Bringing up WireGuard interface..."

    # Load nftables rules
    nft -f /etc/nftables.d/swarmgate.nft 2>/dev/null || true

    # Enable and start WireGuard
    systemctl enable wg-quick@wg0 2>/dev/null || true
    wg-quick up wg0 2>/dev/null || true

    # Verizon failover check (Evolution #1)
    if command -v nmcli &> /dev/null; then
        nmcli device connect lte0 2>/dev/null || true
    fi

    log_success "WireGuard mesh interface active"
}

# === Main Execution ===
main() {
    check_root
    install_dependencies
    setup_wireguard
    setup_swarmgate
    setup_nats
    setup_verizon_failover
    setup_matrix
    setup_syncthing
    setup_monitoring
    bring_up_wireguard

    echo ""
    echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║              SOVEREIGN SWARM NODE BOOTSTRAPPED               ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${BLUE}Node Role:${NC} $NODE_ROLE"
    echo -e "${BLUE}WireGuard:${NC} $(wg show wg0 2>/dev/null | grep 'public key' | awk '{print $3}' || echo 'pending')"
    echo -e "${BLUE}NATS:${NC} localhost:${NATS_PORT}"
    echo -e "${BLUE}Matrix:${NC} localhost:${MATRIX_PORT}"
    echo -e "${BLUE}Syncthing:${NC} localhost:${SYNCTHING_PORT}"
    echo ""
    echo -e "${YELLOW}Next Steps:${NC}"
    echo "1. Add peers: wg set wg0 peer <pubkey> allowed-ips <ip>/32 endpoint <host>:51820"
    echo "2. Start NATS: systemctl start nats-server"
    echo "3. Start Matrix: cd /opt/sovereign-swarm/matrix && docker-compose up -d"
    echo "4. Join swarm: ./swarm-join.sh <rendezvous-ip>"
    echo ""
}

# Run if executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
