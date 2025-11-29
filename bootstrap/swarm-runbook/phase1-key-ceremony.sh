#!/bin/bash
# =============================================================================
# PHASE 1: SwarmGate v1.0 Key Ceremony
# Generates WireGuard keys and capability tokens for mesh network
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
TOKEN_EXPIRY="${TOKEN_EXPIRY:-2035-12-31}"

# Default node list - can be overridden
NODES="${NODES:-command0 fixed1 mobile2 edge3 edge4}"

# Ensure WireGuard tools are available
check_wireguard() {
    if ! command -v wg &> /dev/null; then
        echo_error "WireGuard tools not installed. Run phase0-bootstrap.sh first."
        exit 1
    fi
}

# Create keys directory with secure permissions
setup_keys_directory() {
    echo_info "Setting up secure keys directory..."
    
    mkdir -p "$KEYS_DIR"
    chmod 700 "$SWARM_HOME/keys"
    chmod 700 "$KEYS_DIR"
    
    echo_success "Keys directory created with secure permissions"
}

# Generate master CA key pair
generate_ca_keys() {
    echo_info "Generating Master CA key pair..."
    
    if [ -f "$KEYS_DIR/ca.private" ]; then
        echo_warning "CA keys already exist. Skipping to prevent overwrite."
        echo_warning "To regenerate, remove $KEYS_DIR/ca.* files first."
        return
    fi
    
    # Generate CA private key
    wg genkey > "$KEYS_DIR/ca.private"
    chmod 600 "$KEYS_DIR/ca.private"
    
    # Derive CA public key
    cat "$KEYS_DIR/ca.private" | wg pubkey > "$KEYS_DIR/ca.public"
    chmod 644 "$KEYS_DIR/ca.public"
    
    echo_success "Master CA keys generated"
    echo_info "CA Public Key: $(cat "$KEYS_DIR/ca.public")"
}

# Generate node key pair and capability token
generate_node_keys() {
    local node="$1"
    local role="${2:-full}"
    local capabilities="${3:-all}"
    
    echo_info "Generating keys for node: $node"
    
    if [ -f "$KEYS_DIR/${node}.private" ]; then
        echo_warning "Keys for $node already exist. Skipping."
        return
    fi
    
    # Generate node private key
    wg genkey > "$KEYS_DIR/${node}.private"
    chmod 600 "$KEYS_DIR/${node}.private"
    
    # Derive node public key
    cat "$KEYS_DIR/${node}.private" | wg pubkey > "$KEYS_DIR/${node}.public"
    chmod 644 "$KEYS_DIR/${node}.public"
    
    # Generate capability token (signed metadata)
    local token_data="node=${node} role=${role} capabilities=${capabilities} expiry=${TOKEN_EXPIRY} generated=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo "$token_data" > "$KEYS_DIR/${node}.token"
    chmod 600 "$KEYS_DIR/${node}.token"
    
    echo_success "Keys generated for $node"
}

# Generate pre-shared keys for additional security
generate_psk() {
    local node1="$1"
    local node2="$2"
    local psk_file="$KEYS_DIR/psk-${node1}-${node2}.key"
    
    if [ -f "$psk_file" ]; then
        echo_warning "PSK for $node1-$node2 already exists. Skipping."
        return
    fi
    
    wg genpsk > "$psk_file"
    chmod 600 "$psk_file"
    
    echo_success "Pre-shared key generated for $node1 <-> $node2"
}

# Generate all node keys
generate_all_keys() {
    echo_info "Generating keys for all nodes: $NODES"
    
    for node in $NODES; do
        generate_node_keys "$node"
    done
    
    # Generate PSKs between command0 and all other nodes
    for node in $NODES; do
        if [ "$node" != "command0" ]; then
            generate_psk "command0" "$node"
        fi
    done
}

# Generate QR codes for mobile provisioning
generate_qr_codes() {
    echo_info "Generating QR codes for mobile provisioning..."
    
    if ! command -v qrencode &> /dev/null; then
        echo_warning "qrencode not installed. Skipping QR code generation."
        return
    fi
    
    local qr_dir="$SWARM_HOME/keys/qrcodes"
    mkdir -p "$qr_dir"
    
    for node in $NODES; do
        if [ -f "$KEYS_DIR/${node}.private" ]; then
            # Create minimal config for QR
            local private_key=$(cat "$KEYS_DIR/${node}.private")
            local public_key=$(cat "$KEYS_DIR/${node}.public")
            
            # Generate QR code PNG
            echo "$private_key" | qrencode -o "$qr_dir/${node}-private.png"
            chmod 600 "$qr_dir/${node}-private.png"
            
            echo_success "QR code generated for $node"
        fi
    done
    
    echo ""
    echo_warning "⚠️  SECURITY WARNING ⚠️"
    echo_warning "QR codes contain PRIVATE KEYS - handle with EXTREME care!"
    echo_warning "- Store QR images in encrypted storage only"
    echo_warning "- Delete QR images immediately after use"
    echo_warning "- Never share or transmit QR images over insecure channels"
    echo_warning "QR codes saved to: $qr_dir"
}

# Print key summary
print_key_summary() {
    echo ""
    echo_info "=== Key Ceremony Summary ==="
    echo ""
    echo "Keys generated in: $KEYS_DIR"
    echo ""
    echo "Public keys (safe to share):"
    for node in $NODES; do
        if [ -f "$KEYS_DIR/${node}.public" ]; then
            echo "  $node: $(cat "$KEYS_DIR/${node}.public")"
        fi
    done
    echo ""
    echo_warning "Private keys and tokens are stored securely."
    echo_warning "NEVER share private keys or commit them to git."
    echo ""
}

# Backup keys securely
backup_keys() {
    echo_info "Creating encrypted backup of keys..."
    
    local backup_dir="$SWARM_HOME/backups"
    local backup_file="$backup_dir/keys-backup-$(date +%Y%m%d-%H%M%S).tar.gz"
    
    mkdir -p "$backup_dir"
    
    tar -czf "$backup_file" -C "$SWARM_HOME/keys" swarmgate
    chmod 600 "$backup_file"
    
    echo_success "Keys backed up to: $backup_file"
    echo_warning "Store this backup in a secure offline location!"
}

# Main execution
main() {
    echo_info "🔐 Sovereign Swarm Phase 1: Key Ceremony"
    echo_info "SwarmGate v1.0 Key Generation"
    echo ""
    
    check_wireguard
    setup_keys_directory
    generate_ca_keys
    generate_all_keys
    generate_qr_codes
    print_key_summary
    
    echo_success "Phase 1 Key Ceremony complete! 🎉"
    echo ""
    echo "Next step: Run ./phase2-wireguard-mesh.sh to configure the mesh network"
}

# Handle script arguments
case "${1:-run}" in
    "run")
        main
        ;;
    "ca")
        check_wireguard
        setup_keys_directory
        generate_ca_keys
        ;;
    "node")
        if [ -z "${2:-}" ]; then
            echo "Usage: $0 node <node_name> [role] [capabilities]"
            exit 1
        fi
        check_wireguard
        setup_keys_directory
        generate_node_keys "$2" "${3:-full}" "${4:-all}"
        ;;
    "qr")
        generate_qr_codes
        ;;
    "backup")
        backup_keys
        ;;
    "summary")
        print_key_summary
        ;;
    *)
        echo "Usage: $0 [run|ca|node|qr|backup|summary]"
        echo "  run     - Run complete key ceremony (default)"
        echo "  ca      - Generate CA keys only"
        echo "  node    - Generate keys for a specific node"
        echo "  qr      - Generate QR codes for all nodes"
        echo "  backup  - Create encrypted backup of keys"
        echo "  summary - Print key summary"
        exit 1
        ;;
esac
