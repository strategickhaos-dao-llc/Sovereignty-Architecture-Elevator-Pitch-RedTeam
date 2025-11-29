#!/bin/bash
# =============================================================================
# PHASE 2: WireGuard Mesh Network Configuration
# SwarmGate enforced secure mesh with iptables NAT
# =============================================================================
set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
echo_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
echo_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
echo_error() { echo -e "${RED}[ERROR]${NC} $1"; }

SWARM_HOME="${SWARM_HOME:-$HOME/sovereign-swarm}"
KEYS_DIR="$SWARM_HOME/keys/swarmgate"
CONFIGS_DIR="$SWARM_HOME/configs"
WG_INTERFACE="${WG_INTERFACE:-wg0}"
WG_PORT="${WG_PORT:-51820}"
WG_NETWORK="${WG_NETWORK:-10.13.33.0/24}"

# Node IP assignments
declare -A NODE_IPS=(
    ["command0"]="10.13.33.1"
    ["fixed1"]="10.13.33.2"
    ["mobile2"]="10.13.33.3"
    ["edge3"]="10.13.33.4"
    ["edge4"]="10.13.33.5"
)

# Verify keys exist
check_keys() {
    echo_info "Verifying keys exist..."
    
    if [ ! -f "$KEYS_DIR/command0.private" ]; then
        echo_error "Keys not found. Run phase1-key-ceremony.sh first."
        exit 1
    fi
    
    echo_success "Keys verified"
}

# Detect external interface
detect_interface() {
    # Find the default route interface
    local default_iface
    default_iface=$(ip route | grep default | awk '{print $5}' | head -1)
    
    if [ -z "$default_iface" ]; then
        echo_warning "Could not detect external interface. Using eth0 as default."
        echo "eth0"
    else
        echo "$default_iface"
    fi
}

# Get external IP address
get_external_ip() {
    local external_ip
    external_ip=$(curl -s --max-time 5 ifconfig.me 2>/dev/null || \
                  curl -s --max-time 5 icanhazip.com 2>/dev/null || \
                  curl -s --max-time 5 ipinfo.io/ip 2>/dev/null || \
                  echo "EXTERNAL_IP_PLACEHOLDER")
    echo "$external_ip"
}

# Generate Command-0 (hub) configuration
generate_command0_config() {
    echo_info "Generating Command-0 WireGuard configuration..."
    
    local private_key
    local external_iface
    local external_ip
    
    private_key=$(cat "$KEYS_DIR/command0.private")
    external_iface=$(detect_interface)
    external_ip=$(get_external_ip)
    
    mkdir -p "$CONFIGS_DIR"
    
    cat > "$CONFIGS_DIR/${WG_INTERFACE}.conf" << EOF
# =============================================================================
# Sovereign Swarm - Command-0 Hub Configuration
# Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)
# =============================================================================

[Interface]
Address = ${NODE_IPS["command0"]}/24
PrivateKey = ${private_key}
ListenPort = ${WG_PORT}

# NAT and forwarding rules
PostUp = iptables -A FORWARD -i %i -j ACCEPT; iptables -A FORWARD -o %i -j ACCEPT; iptables -t nat -A POSTROUTING -o ${external_iface} -j MASQUERADE
PostDown = iptables -D FORWARD -i %i -j ACCEPT; iptables -D FORWARD -o %i -j ACCEPT; iptables -t nat -D POSTROUTING -o ${external_iface} -j MASQUERADE

# -----------------------------------------------------------------------------
# Peer: Fixed-1 (Primary Anchor Node)
# -----------------------------------------------------------------------------
EOF

    # Add peer configurations for each node (except command0)
    for node in fixed1 mobile2 edge3 edge4; do
        if [ -f "$KEYS_DIR/${node}.public" ]; then
            local peer_pubkey
            peer_pubkey=$(cat "$KEYS_DIR/${node}.public")
            local peer_ip="${NODE_IPS[$node]}"
            local psk_file="$KEYS_DIR/psk-command0-${node}.key"
            
            cat >> "$CONFIGS_DIR/${WG_INTERFACE}.conf" << EOF

[Peer]
# Node: ${node}
PublicKey = ${peer_pubkey}
AllowedIPs = ${peer_ip}/32
PersistentKeepalive = 25
EOF
            
            # Add PSK if available
            if [ -f "$psk_file" ]; then
                echo "PresharedKey = $(cat "$psk_file")" >> "$CONFIGS_DIR/${WG_INTERFACE}.conf"
            fi
        fi
    done
    
    chmod 600 "$CONFIGS_DIR/${WG_INTERFACE}.conf"
    echo_success "Command-0 configuration generated: $CONFIGS_DIR/${WG_INTERFACE}.conf"
    echo_info "External IP detected: $external_ip"
}

# Generate peer configuration for a specific node
generate_peer_config() {
    local node="$1"
    local hub_endpoint="${2:-COMMAND0_ENDPOINT:51820}"
    
    echo_info "Generating configuration for peer: $node"
    
    if [ ! -f "$KEYS_DIR/${node}.private" ]; then
        echo_error "Private key for $node not found"
        return 1
    fi
    
    local private_key
    local command0_pubkey
    local node_ip
    local psk_file
    
    private_key=$(cat "$KEYS_DIR/${node}.private")
    command0_pubkey=$(cat "$KEYS_DIR/command0.public")
    node_ip="${NODE_IPS[$node]}"
    psk_file="$KEYS_DIR/psk-command0-${node}.key"
    
    cat > "$CONFIGS_DIR/${WG_INTERFACE}-${node}.conf" << EOF
# =============================================================================
# Sovereign Swarm - ${node} Peer Configuration
# Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)
# =============================================================================

[Interface]
Address = ${node_ip}/24
PrivateKey = ${private_key}
DNS = ${NODE_IPS["command0"]}

[Peer]
# Command-0 Hub
PublicKey = ${command0_pubkey}
Endpoint = ${hub_endpoint}
AllowedIPs = ${WG_NETWORK}
PersistentKeepalive = 25
EOF
    
    # Add PSK if available
    if [ -f "$psk_file" ]; then
        echo "PresharedKey = $(cat "$psk_file")" >> "$CONFIGS_DIR/${WG_INTERFACE}-${node}.conf"
    fi
    
    chmod 600 "$CONFIGS_DIR/${WG_INTERFACE}-${node}.conf"
    echo_success "Peer configuration generated: $CONFIGS_DIR/${WG_INTERFACE}-${node}.conf"
}

# Install WireGuard configuration
install_config() {
    echo_info "Installing WireGuard configuration..."
    
    # Check if WireGuard interface already exists
    if ip link show "$WG_INTERFACE" &> /dev/null; then
        echo_warning "WireGuard interface $WG_INTERFACE already exists"
        read -p "Do you want to restart it? (y/N) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            sudo wg-quick down "$WG_INTERFACE" 2>/dev/null || true
        else
            return
        fi
    fi
    
    # Copy configuration to system directory
    sudo cp "$CONFIGS_DIR/${WG_INTERFACE}.conf" "/etc/wireguard/${WG_INTERFACE}.conf"
    sudo chmod 600 "/etc/wireguard/${WG_INTERFACE}.conf"
    
    echo_success "Configuration installed to /etc/wireguard/${WG_INTERFACE}.conf"
}

# Start WireGuard interface
start_wireguard() {
    echo_info "Starting WireGuard interface..."
    
    sudo wg-quick up "$WG_INTERFACE"
    
    # Enable on boot
    sudo systemctl enable "wg-quick@${WG_INTERFACE}" 2>/dev/null || true
    
    echo_success "WireGuard interface $WG_INTERFACE is up"
}

# Show WireGuard status
show_status() {
    echo_info "WireGuard Status:"
    echo ""
    sudo wg show "$WG_INTERFACE"
    echo ""
    echo_info "Interface details:"
    ip addr show "$WG_INTERFACE"
}

# Generate all peer configurations
generate_all_peers() {
    local hub_endpoint="${1:-COMMAND0_ENDPOINT:51820}"
    
    for node in fixed1 mobile2 edge3 edge4; do
        generate_peer_config "$node" "$hub_endpoint"
    done
}

# Print deployment instructions
print_instructions() {
    local external_ip
    external_ip=$(get_external_ip)
    
    echo ""
    echo_info "=== WireGuard Mesh Configuration Complete ==="
    echo ""
    echo "Hub configuration: $CONFIGS_DIR/${WG_INTERFACE}.conf"
    echo "Peer configurations generated for all nodes."
    echo ""
    echo "To deploy peer configurations to remote nodes:"
    echo ""
    echo "  # Copy configuration to Fixed-1"
    echo "  scp $CONFIGS_DIR/${WG_INTERFACE}-fixed1.conf user@fixed1:/etc/wireguard/${WG_INTERFACE}.conf"
    echo "  ssh user@fixed1 'sudo wg-quick up ${WG_INTERFACE}'"
    echo ""
    echo "  # Copy configuration to Mobile-2"
    echo "  scp $CONFIGS_DIR/${WG_INTERFACE}-mobile2.conf user@mobile2:/etc/wireguard/${WG_INTERFACE}.conf"
    echo ""
    echo "External IP for endpoints: $external_ip"
    echo ""
    echo_warning "Update peer configurations with the actual endpoint address if needed."
}

# Main execution
main() {
    echo_info "🔗 Sovereign Swarm Phase 2: WireGuard Mesh"
    echo_info "Configuring secure mesh network..."
    echo ""
    
    check_keys
    generate_command0_config
    generate_all_peers "$(get_external_ip):${WG_PORT}"
    
    echo ""
    read -p "Do you want to install and start WireGuard now? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        install_config
        start_wireguard
        show_status
    fi
    
    print_instructions
    
    echo_success "Phase 2 complete! 🎉"
    echo ""
    echo "Next step: Deploy edge nodes with ./pelican-build.sh"
}

# Handle script arguments
case "${1:-run}" in
    "run")
        main
        ;;
    "hub")
        check_keys
        generate_command0_config
        ;;
    "peer")
        if [ -z "${2:-}" ]; then
            echo "Usage: $0 peer <node_name> [hub_endpoint]"
            exit 1
        fi
        check_keys
        generate_peer_config "$2" "${3:-COMMAND0_ENDPOINT:51820}"
        ;;
    "all-peers")
        check_keys
        generate_all_peers "${2:-COMMAND0_ENDPOINT:51820}"
        ;;
    "install")
        install_config
        ;;
    "start")
        start_wireguard
        ;;
    "status")
        show_status
        ;;
    "stop")
        sudo wg-quick down "$WG_INTERFACE"
        echo_success "WireGuard interface stopped"
        ;;
    *)
        echo "Usage: $0 [run|hub|peer|all-peers|install|start|status|stop]"
        echo "  run       - Run complete Phase 2 setup (default)"
        echo "  hub       - Generate hub (Command-0) configuration"
        echo "  peer      - Generate peer configuration for specific node"
        echo "  all-peers - Generate all peer configurations"
        echo "  install   - Install configuration to /etc/wireguard"
        echo "  start     - Start WireGuard interface"
        echo "  status    - Show WireGuard status"
        echo "  stop      - Stop WireGuard interface"
        exit 1
        ;;
esac
