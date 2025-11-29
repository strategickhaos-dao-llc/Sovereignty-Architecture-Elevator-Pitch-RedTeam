#!/usr/bin/env bash
# ============================================================================
# Pelican Pi Build & Provisioning Script
# Automated setup for Pelican (mobile/field) nodes
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

# Node identification (pelican1, pelican2, pelican3, etc.)
PELICAN_ID="${PELICAN_ID:-pelican1}"
SWARM_NAME="${SWARM_NAME:-sovereign-swarm}"

# Command-0 details (must be provided)
COMMAND0_PUBKEY="${COMMAND0_PUBKEY:-}"
COMMAND0_ENDPOINT="${COMMAND0_ENDPOINT:-}"

# Directory paths
SWARM_BASE="/opt/sovereign-swarm"
KEYS_DIR="${SWARM_BASE}/keys"
CONFIG_DIR="${SWARM_BASE}/config"
LOG_DIR="/var/log/sovereign-swarm"

# WireGuard configuration
WG_INTERFACE="${WG_INTERFACE:-wg0}"
WG_PORT="${WG_PORT:-51820}"

# Pelican-specific settings
PELICAN_MODE="${PELICAN_MODE:-mobile}"  # mobile, fixed, hybrid
POWER_MODE="${POWER_MODE:-battery}"      # battery, solar, grid
SYNC_INTERVAL="${SYNC_INTERVAL:-300}"    # seconds between syncs

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

check_raspberry_pi() {
    log_section "Checking Hardware"
    
    if [[ -f /proc/device-tree/model ]]; then
        local model=$(cat /proc/device-tree/model)
        log_info "Hardware: $model"
        
        if [[ "$model" == *"Raspberry Pi"* ]]; then
            log_success "Raspberry Pi detected"
            return 0
        fi
    fi
    
    log_warn "Not running on Raspberry Pi - some features may not work"
    return 0
}

install_dependencies() {
    log_section "Installing Dependencies"
    
    apt-get update -qq
    
    local packages=(
        "wireguard"
        "wireguard-tools"
        "openssl"
        "jq"
        "curl"
        "ufw"
        "syncthing"
        "htop"
        "iotop"
        "tmux"
    )
    
    apt-get install -y -qq "${packages[@]}"
    
    log_success "Dependencies installed"
}

create_directories() {
    log_section "Creating Directory Structure"
    
    local dirs=(
        "$SWARM_BASE"
        "$KEYS_DIR"
        "$KEYS_DIR/wireguard"
        "$CONFIG_DIR"
        "$LOG_DIR"
        "${SWARM_BASE}/sync"
        "${SWARM_BASE}/vault"
    )
    
    for dir in "${dirs[@]}"; do
        mkdir -p "$dir"
        chmod 700 "$dir"
    done
    
    log_success "Directories created"
}

# ============================================================================
# Network Configuration
# ============================================================================

get_pelican_ip() {
    # Generate consistent IP based on Pelican ID
    case "$PELICAN_ID" in
        pelican1) echo "10.44.0.11" ;;
        pelican2) echo "10.44.0.12" ;;
        pelican3) echo "10.44.0.13" ;;
        pelican4) echo "10.44.0.14" ;;
        pelican5) echo "10.44.0.15" ;;
        *)
            # Generate from hash for unknown IDs
            local hash=$(echo -n "$PELICAN_ID" | md5sum | cut -c1-2)
            local octet=$((16#$hash % 40 + 11))
            echo "10.44.0.${octet}"
            ;;
    esac
}

generate_wireguard_keys() {
    log_section "Generating WireGuard Keys"
    
    local wg_private="${KEYS_DIR}/wireguard/${PELICAN_ID}.key"
    local wg_public="${KEYS_DIR}/wireguard/${PELICAN_ID}.pub"
    local wg_psk="${KEYS_DIR}/wireguard/${PELICAN_ID}.psk"
    
    if [[ -f "$wg_private" ]]; then
        log_warn "WireGuard keys already exist"
    else
        wg genkey > "$wg_private"
        chmod 600 "$wg_private"
    fi
    
    wg pubkey < "$wg_private" > "$wg_public"
    
    if [[ ! -f "$wg_psk" ]]; then
        wg genpsk > "$wg_psk"
        chmod 600 "$wg_psk"
    fi
    
    log_success "WireGuard keys generated"
    log_info "Public Key: $(cat "$wg_public")"
}

configure_wireguard() {
    log_section "Configuring WireGuard"
    
    local wg_private="${KEYS_DIR}/wireguard/${PELICAN_ID}.key"
    local wg_psk="${KEYS_DIR}/wireguard/${PELICAN_ID}.psk"
    local wg_config="/etc/wireguard/${WG_INTERFACE}.conf"
    local pelican_ip=$(get_pelican_ip)
    
    # Validate Command-0 details
    if [[ -z "$COMMAND0_PUBKEY" ]]; then
        log_error "COMMAND0_PUBKEY is required"
        log_info "Get this from Command-0 after running master-bootstrap.sh"
        exit 1
    fi
    
    if [[ -z "$COMMAND0_ENDPOINT" ]]; then
        log_error "COMMAND0_ENDPOINT is required"
        log_info "Format: <public-ip>:${WG_PORT}"
        exit 1
    fi
    
    cat > "$wg_config" << EOF
# Sovereign Swarm WireGuard Configuration
# Pelican Node: ${PELICAN_ID}
# Mode: ${PELICAN_MODE}
# Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)

[Interface]
Address = ${pelican_ip}/24
ListenPort = ${WG_PORT}
PrivateKey = $(cat "$wg_private")
# Save battery by reducing handshake frequency
# FwMark = 0x200

[Peer]
# Command-0 (Primary Hub)
PublicKey = ${COMMAND0_PUBKEY}
PresharedKey = $(cat "$wg_psk")
AllowedIPs = 10.44.0.0/24
Endpoint = ${COMMAND0_ENDPOINT}
PersistentKeepalive = 25
EOF

    chmod 600 "$wg_config"
    
    log_success "WireGuard configuration created"
    log_info "Pelican IP: ${pelican_ip}"
}

start_wireguard() {
    log_section "Starting WireGuard"
    
    # Enable IP forwarding
    echo 1 > /proc/sys/net/ipv4/ip_forward
    echo "net.ipv4.ip_forward = 1" >> /etc/sysctl.conf
    
    systemctl enable "wg-quick@${WG_INTERFACE}"
    systemctl start "wg-quick@${WG_INTERFACE}"
    
    log_success "WireGuard started"
    wg show "$WG_INTERFACE"
}

# ============================================================================
# Firewall Configuration
# ============================================================================

configure_firewall() {
    log_section "Configuring Firewall"
    
    ufw --force reset
    ufw default deny incoming
    ufw default allow outgoing
    
    # Allow SSH
    ufw allow 22/tcp comment 'SSH'
    
    # Allow WireGuard
    ufw allow "${WG_PORT}/udp" comment 'WireGuard'
    
    # Allow mesh traffic
    ufw allow from 10.44.0.0/24 comment 'Swarm Mesh'
    
    ufw --force enable
    
    log_success "Firewall configured"
}

# ============================================================================
# Power Management (Raspberry Pi specific)
# ============================================================================

configure_power_management() {
    log_section "Configuring Power Management"
    
    local power_script="${SWARM_BASE}/power-manager.sh"
    
    cat > "$power_script" << 'POWER'
#!/usr/bin/env bash
# Pelican Power Manager
# Optimizes power consumption based on mode

POWER_MODE="${POWER_MODE:-battery}"
LOG_FILE="/var/log/sovereign-swarm/power.log"

log() {
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) - $*" >> "$LOG_FILE"
}

# Get battery level (if available)
get_battery_level() {
    # Check for UPS HAT or similar
    if command -v upower &> /dev/null; then
        upower -i /org/freedesktop/UPower/devices/battery_BAT0 2>/dev/null | \
            grep percentage | awk '{print $2}' | tr -d '%'
    else
        echo "100"  # Assume full if no battery monitoring
    fi
}

# Adjust sync frequency based on battery
adjust_sync_frequency() {
    local battery=$(get_battery_level)
    local sync_interval
    
    if [[ $battery -lt 20 ]]; then
        sync_interval=1800  # 30 min
        log "Critical battery ($battery%) - reducing sync to 30min"
    elif [[ $battery -lt 50 ]]; then
        sync_interval=900   # 15 min
        log "Low battery ($battery%) - reducing sync to 15min"
    else
        sync_interval=300   # 5 min
        log "Normal battery ($battery%) - standard sync"
    fi
    
    echo "$sync_interval"
}

# Disable unused hardware
optimize_hardware() {
    # Disable HDMI output (saves ~25mA)
    if command -v tvservice &> /dev/null; then
        tvservice --off 2>/dev/null || true
    fi
    
    # Reduce WiFi power (if using ethernet/LTE)
    if [[ -d /sys/class/net/wlan0 ]]; then
        iwconfig wlan0 power on 2>/dev/null || true
    fi
    
    # Disable Bluetooth (if not needed)
    if command -v bluetoothctl &> /dev/null; then
        bluetoothctl power off 2>/dev/null || true
    fi
    
    log "Hardware optimized for power saving"
}

case "${1:-status}" in
    optimize)
        optimize_hardware
        ;;
    battery)
        get_battery_level
        ;;
    sync-interval)
        adjust_sync_frequency
        ;;
    status)
        echo "Battery: $(get_battery_level)%"
        echo "Mode: ${POWER_MODE}"
        ;;
esac
POWER

    chmod +x "$power_script"
    
    # Create systemd timer for power management
    cat > /etc/systemd/system/pelican-power.service << EOF
[Unit]
Description=Pelican Power Manager
After=network.target

[Service]
Type=oneshot
ExecStart=${power_script} optimize
Environment=POWER_MODE=${POWER_MODE}
EOF

    cat > /etc/systemd/system/pelican-power.timer << EOF
[Unit]
Description=Run Pelican Power Manager periodically

[Timer]
OnBootSec=1min
OnUnitActiveSec=5min

[Install]
WantedBy=timers.target
EOF

    systemctl daemon-reload
    systemctl enable pelican-power.timer
    
    log_success "Power management configured"
}

# ============================================================================
# Syncthing Configuration
# ============================================================================

configure_syncthing() {
    log_section "Configuring Syncthing"
    
    local pelican_ip=$(get_pelican_ip)
    local sync_dir="${SWARM_BASE}/sync"
    
    # Stop syncthing if running
    systemctl stop syncthing@root 2>/dev/null || true
    
    # Create syncthing configuration
    mkdir -p ~/.config/syncthing
    
    cat > ~/.config/syncthing/config.xml << EOF
<configuration version="37">
    <folder id="swarm-vault" label="Swarm Vault" path="${SWARM_BASE}/vault" type="receiveonly">
        <filesystemType>basic</filesystemType>
        <device id="COMMAND0-DEVICE-ID" introducedBy="">
            <encryptionPassword></encryptionPassword>
        </device>
    </folder>
    <device id="${PELICAN_ID}" name="${PELICAN_ID}">
        <address>dynamic</address>
    </device>
    <gui enabled="true" tls="true" debugging="false">
        <address>${pelican_ip}:8384</address>
    </gui>
    <options>
        <listenAddress>tcp://${pelican_ip}:22000</listenAddress>
        <globalAnnounceEnabled>false</globalAnnounceEnabled>
        <localAnnounceEnabled>false</localAnnounceEnabled>
        <relaysEnabled>false</relaysEnabled>
        <natEnabled>false</natEnabled>
    </options>
</configuration>
EOF

    # Enable syncthing
    systemctl enable syncthing@root
    
    log_success "Syncthing configured"
    log_warn "Syncthing device IDs must be exchanged with Command-0"
}

# ============================================================================
# Connectivity Watchdog
# ============================================================================

install_watchdog() {
    log_section "Installing Connectivity Watchdog"
    
    local watchdog_script="${SWARM_BASE}/watchdog.sh"
    
    cat > "$watchdog_script" << 'WATCHDOG'
#!/usr/bin/env bash
# Pelican Connectivity Watchdog
# Monitors mesh connectivity and attempts recovery

COMMAND0_IP="10.44.0.1"
LOG_FILE="/var/log/sovereign-swarm/watchdog.log"
MAX_FAILURES=3
FAILURE_COUNT=0

log() {
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) - $*" >> "$LOG_FILE"
}

check_connectivity() {
    if ping -c 1 -W 5 "$COMMAND0_IP" &> /dev/null; then
        return 0
    else
        return 1
    fi
}

restart_wireguard() {
    log "Restarting WireGuard interface..."
    systemctl restart wg-quick@wg0
    sleep 10
}

# Main watchdog loop
while true; do
    if check_connectivity; then
        if [[ $FAILURE_COUNT -gt 0 ]]; then
            log "Connectivity restored after $FAILURE_COUNT failures"
        fi
        FAILURE_COUNT=0
    else
        ((FAILURE_COUNT++))
        log "Connectivity check failed (count: $FAILURE_COUNT)"
        
        if [[ $FAILURE_COUNT -ge $MAX_FAILURES ]]; then
            restart_wireguard
            FAILURE_COUNT=0
        fi
    fi
    
    sleep 60
done
WATCHDOG

    chmod +x "$watchdog_script"
    
    cat > /etc/systemd/system/pelican-watchdog.service << EOF
[Unit]
Description=Pelican Connectivity Watchdog
After=wg-quick@wg0.service

[Service]
Type=simple
ExecStart=${watchdog_script}
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

    systemctl daemon-reload
    systemctl enable pelican-watchdog.service
    
    log_success "Watchdog installed"
}

# ============================================================================
# Summary
# ============================================================================

print_summary() {
    log_section "Pelican Build Summary"
    
    local wg_pubkey=$(cat "${KEYS_DIR}/wireguard/${PELICAN_ID}.pub")
    local pelican_ip=$(get_pelican_ip)
    
    echo ""
    echo "=== Pelican: ${PELICAN_ID} ==="
    echo "Mode: ${PELICAN_MODE}"
    echo "Power: ${POWER_MODE}"
    echo "Mesh IP: ${pelican_ip}"
    echo ""
    echo "=== WireGuard ==="
    echo "PublicKey: ${wg_pubkey}"
    echo ""
    echo "=== Add to Command-0 ==="
    echo "Run on Command-0:"
    echo "  wg set wg0 peer ${wg_pubkey} allowed-ips ${pelican_ip}/32"
    echo ""
    echo "=== Test Connectivity ==="
    echo "  ping 10.44.0.1  # Command-0"
    echo ""
    echo "=== Services ==="
    echo "  systemctl status wg-quick@wg0"
    echo "  systemctl status pelican-watchdog"
    echo "  systemctl status syncthing@root"
    echo ""
    
    log_success "Pelican ${PELICAN_ID} provisioning complete!"
}

# ============================================================================
# Main Execution
# ============================================================================

main() {
    log_section "Pelican Pi Build Script"
    log_info "Pelican ID: ${PELICAN_ID}"
    log_info "Mode: ${PELICAN_MODE}"
    log_info "Power: ${POWER_MODE}"
    
    check_root
    check_raspberry_pi
    install_dependencies
    create_directories
    
    # Network setup
    generate_wireguard_keys
    configure_wireguard
    start_wireguard
    configure_firewall
    
    # Pelican-specific features
    configure_power_management
    configure_syncthing
    install_watchdog
    
    # Start services
    log_section "Starting Services"
    systemctl start pelican-watchdog.service || log_warn "Watchdog deferred"
    systemctl start syncthing@root || log_warn "Syncthing deferred"
    
    print_summary
}

# Handle script arguments
case "${1:-build}" in
    build)
        main
        ;;
    --help|-h)
        echo "Pelican Pi Build & Provisioning Script"
        echo ""
        echo "Usage: $0 [command]"
        echo ""
        echo "Required Environment Variables:"
        echo "  PELICAN_ID         - Pelican identifier (pelican1, pelican2, etc.)"
        echo "  COMMAND0_PUBKEY    - Command-0 WireGuard public key"
        echo "  COMMAND0_ENDPOINT  - Command-0 endpoint (ip:port)"
        echo ""
        echo "Optional Environment Variables:"
        echo "  PELICAN_MODE       - mobile, fixed, hybrid (default: mobile)"
        echo "  POWER_MODE         - battery, solar, grid (default: battery)"
        echo "  SYNC_INTERVAL      - Sync interval in seconds (default: 300)"
        echo ""
        echo "Examples:"
        echo "  PELICAN_ID=pelican1 COMMAND0_PUBKEY=xyz COMMAND0_ENDPOINT=1.2.3.4:51820 $0"
        ;;
    status)
        echo "=== Pelican Status ==="
        systemctl status wg-quick@wg0 --no-pager || true
        echo ""
        wg show wg0 || true
        ;;
    *)
        echo "Unknown command: $1"
        echo "Use --help for usage information"
        exit 1
        ;;
esac
