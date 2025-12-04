#!/usr/bin/env bash
#===============================================================================
# Sovereignty Architecture - WireGuard Peer Setup Script
# Configures WireGuard peer connection to Command-0 or other mesh nodes.
#
# Usage: sudo ./wg-peer-setup.sh
# Or with parameters: sudo ./wg-peer-setup.sh <public_key> <endpoint>
#
# Version: 1.0.0
#===============================================================================
set -euo pipefail

readonly WG_INTERFACE="wg0"
readonly WG_CONF="/etc/wireguard/${WG_INTERFACE}.conf"

# Colors
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly RED='\033[0;31m'
readonly NC='\033[0m'

log_ok() { echo -e "${GREEN}[+]${NC} $*"; }
log_warn() { echo -e "${YELLOW}[!]${NC} $*"; }
log_error() { echo -e "${RED}[-]${NC} $*"; }

#===============================================================================
# Main Functions
#===============================================================================

validate_public_key() {
    local key="$1"
    # WireGuard public keys are 44 characters base64
    if [[ ${#key} -ne 44 ]] || [[ ! "$key" =~ ^[A-Za-z0-9+/]+={0,2}$ ]]; then
        return 1
    fi
    return 0
}

validate_endpoint() {
    local endpoint="$1"
    # Basic IP:PORT or hostname:PORT validation
    if [[ "$endpoint" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+:[0-9]+$ ]] || \
       [[ "$endpoint" =~ ^[a-zA-Z0-9.-]+:[0-9]+$ ]]; then
        return 0
    fi
    return 1
}

get_peer_info() {
    local c0_pubkey=""
    local c0_endpoint=""

    if [[ $# -ge 2 ]]; then
        c0_pubkey="$1"
        c0_endpoint="$2"
    else
        echo "=============================================="
        echo " Sovereignty Swarm - Peer Connection Setup"
        echo "=============================================="
        echo
        echo "Enter Command-0 (or peer node) connection details:"
        echo

        read -rp "Command-0 PublicKey: " c0_pubkey
        read -rp "Command-0 Endpoint (IP:PORT): " c0_endpoint
    fi

    # Add port if not specified
    if [[ ! "$c0_endpoint" =~ :[0-9]+$ ]]; then
        c0_endpoint="${c0_endpoint}:51820"
    fi

    # Validate inputs
    if ! validate_public_key "$c0_pubkey"; then
        log_error "Invalid public key format"
        exit 1
    fi

    if ! validate_endpoint "$c0_endpoint"; then
        log_error "Invalid endpoint format. Use: IP:PORT or hostname:PORT"
        exit 1
    fi

    echo "$c0_pubkey"
    echo "$c0_endpoint"
}

configure_peer() {
    local pubkey="$1"
    local endpoint="$2"

    log_warn "Configuring WireGuard peer..."

    # Backup current config
    if [[ -f "$WG_CONF" ]]; then
        cp "$WG_CONF" "${WG_CONF}.bak.$(date +%Y%m%d%H%M%S)"
    fi

    # Update the configuration
    if grep -q "COMMAND_0_PUBLIC_KEY_PLACEHOLDER" "$WG_CONF" 2>/dev/null; then
        # Replace placeholder
        sed -i "s|PublicKey = COMMAND_0_PUBLIC_KEY_PLACEHOLDER|PublicKey = ${pubkey}|g" "$WG_CONF"
        sed -i "s|Endpoint = COMMAND_0_ENDPOINT_PLACEHOLDER:51820|Endpoint = ${endpoint}|g" "$WG_CONF"
    elif grep -q "PublicKey = ${pubkey}" "$WG_CONF" 2>/dev/null; then
        log_warn "Peer already configured, updating endpoint..."
        sed -i "/PublicKey = ${pubkey}/,/^\[/ s|Endpoint = .*|Endpoint = ${endpoint}|" "$WG_CONF"
    else
        # Add new peer section
        cat >> "$WG_CONF" << EOF

[Peer]
# Added peer: $(date)
PublicKey = ${pubkey}
Endpoint = ${endpoint}
AllowedIPs = 10.44.0.0/16
PersistentKeepalive = 25
EOF
    fi

    log_ok "WireGuard configuration updated"
}

restart_wireguard() {
    log_warn "Restarting WireGuard interface..."

    systemctl restart "wg-quick@${WG_INTERFACE}"

    # Wait for interface to come up
    sleep 2

    # Check status
    if wg show "${WG_INTERFACE}" &>/dev/null; then
        log_ok "WireGuard interface is up"
        echo
        echo "Current WireGuard status:"
        wg show "${WG_INTERFACE}"
    else
        log_error "WireGuard interface failed to start"
        echo "Check logs: journalctl -u wg-quick@${WG_INTERFACE}"
        exit 1
    fi
}

wait_for_handshake() {
    echo
    log_warn "Waiting for peer handshake..."

    local attempts=0
    local max_attempts=30

    while [[ $attempts -lt $max_attempts ]]; do
        local latest_handshake
        latest_handshake=$(wg show "${WG_INTERFACE}" latest-handshakes 2>/dev/null | awk '{print $2}' | head -1)

        if [[ -n "$latest_handshake" ]] && [[ "$latest_handshake" != "0" ]]; then
            log_ok "Handshake successful!"
            echo
            echo "Swarm connection established 🜂"
            return 0
        fi

        ((attempts++))
        echo -ne "\r[*] Waiting for handshake... ${attempts}/${max_attempts}"
        sleep 2
    done

    echo
    log_warn "No handshake yet - peer may not be reachable or configured"
    echo "The connection will establish automatically when the peer comes online."
    return 0
}

#===============================================================================
# Main Execution
#===============================================================================
main() {
    # Check root
    if [[ $EUID -ne 0 ]]; then
        log_error "This script must be run as root"
        exit 1
    fi

    # Check WireGuard config exists
    if [[ ! -f "$WG_CONF" ]]; then
        log_error "WireGuard configuration not found at $WG_CONF"
        log_error "Run master-bootstrap.sh first"
        exit 1
    fi

    # Get peer info (from args or interactive)
    local peer_info
    peer_info=$(get_peer_info "$@")

    local c0_pubkey
    local c0_endpoint
    c0_pubkey=$(echo "$peer_info" | head -1)
    c0_endpoint=$(echo "$peer_info" | tail -1)

    echo
    log_ok "Configuring peer:"
    echo "  PublicKey: ${c0_pubkey}"
    echo "  Endpoint:  ${c0_endpoint}"
    echo

    configure_peer "$c0_pubkey" "$c0_endpoint"
    restart_wireguard
    wait_for_handshake

    echo
    log_ok "Peer setup complete!"
}

main "$@"
