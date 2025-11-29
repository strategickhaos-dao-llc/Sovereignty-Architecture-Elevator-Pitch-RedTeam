#!/bin/bash
# =============================================================================
# Pelican-Case Edge Node Build Script
# Creates deployable Raspberry Pi 5 image for sovereign swarm edge nodes
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
PELICAN_DIR="$SWARM_HOME/pelican-build"
NODE_NAME="${NODE_NAME:-edge3}"

# Install edge node dependencies
install_deps() {
    echo_info "Installing edge node dependencies..."
    
    sudo apt update
    sudo apt install -y wireguard qrencode curl wget
    
    echo_success "Dependencies installed"
}

# Create join script for sovereign swarm
create_join_script() {
    echo_info "Creating sovereign swarm join script..."
    
    mkdir -p "$PELICAN_DIR"
    
    cat > "$PELICAN_DIR/join-sovereign-swarm.sh" << 'JOINEOF'
#!/bin/bash
# =============================================================================
# Sovereign Swarm Auto-Join Script for Edge Nodes
# Runs on boot to automatically connect to the mesh network
# =============================================================================
set -euo pipefail

echo "[INFO] Starting Sovereign Swarm join process..."

# Read credentials from boot partition (provisioned during setup)
WG_KEY_FILE="/boot/firmware/swarmgate.key"
WG_TOKEN_FILE="/boot/firmware/swarmgate.token"
WG_CONFIG_FILE="/boot/firmware/wg0.conf"

# Check if configuration exists
if [ -f "$WG_CONFIG_FILE" ]; then
    echo "[INFO] Using pre-configured WireGuard config"
    sudo cp "$WG_CONFIG_FILE" /etc/wireguard/wg0.conf
    sudo chmod 600 /etc/wireguard/wg0.conf
elif [ -f "$WG_KEY_FILE" ] && [ -f "$WG_TOKEN_FILE" ]; then
    echo "[INFO] Generating WireGuard config from credentials"
    
    WG_KEY=$(cat "$WG_KEY_FILE")
    WG_TOKEN=$(cat "$WG_TOKEN_FILE")
    
    # Extract node info from token
    NODE_IP=$(echo "$WG_TOKEN" | grep -oP 'ip=\K[0-9.]+' || echo "10.13.33.9")
    
    # Create WireGuard configuration
    sudo tee /etc/wireguard/wg0.conf > /dev/null << EOF
[Interface]
Address = ${NODE_IP}/24
PrivateKey = ${WG_KEY}
DNS = 10.13.33.1

[Peer]
# Command-0 Hub
# NOTE: Replace REPLACE_WITH_COMMAND0_PUBKEY with actual Command-0 public key from phase1
PublicKey = REPLACE_WITH_COMMAND0_PUBKEY
Endpoint = command0.sovereign.local:51820
AllowedIPs = 10.13.33.0/24
PersistentKeepalive = 25
EOF

    sudo chmod 600 /etc/wireguard/wg0.conf
else
    echo "[ERROR] No WireGuard credentials found. Cannot join swarm."
    exit 1
fi

# Enable and start WireGuard
sudo systemctl enable wg-quick@wg0
sudo systemctl start wg-quick@wg0

# Verify connection
sleep 5
if ping -c 1 10.13.33.1 &> /dev/null; then
    echo "[SUCCESS] Connected to sovereign swarm!"
else
    echo "[WARNING] Could not reach hub. Check network connectivity."
fi

echo "[INFO] Sovereign swarm join process complete"
JOINEOF

    chmod +x "$PELICAN_DIR/join-sovereign-swarm.sh"
    echo_success "Join script created: $PELICAN_DIR/join-sovereign-swarm.sh"
}

# Create systemd service for auto-join on boot
create_systemd_service() {
    echo_info "Creating systemd service for auto-join..."
    
    cat > "$PELICAN_DIR/sovereign-swarm-join.service" << 'EOF'
[Unit]
Description=Sovereign Swarm Auto-Join Service
After=network-online.target
Wants=network-online.target
Before=multi-user.target

[Service]
Type=oneshot
ExecStart=/opt/sovereign-swarm/join-sovereign-swarm.sh
RemainAfterExit=yes
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

    echo_success "Systemd service created: $PELICAN_DIR/sovereign-swarm-join.service"
}

# Create node provisioning script (runs on Command-0)
create_provisioning_script() {
    echo_info "Creating node provisioning script..."
    
    cat > "$PELICAN_DIR/provision-edge-node.sh" << 'PROVEOF'
#!/bin/bash
# =============================================================================
# Provision Edge Node - Run from Command-0
# Usage: ./provision-edge-node.sh <node_name> <pi_ip_or_hostname>
# =============================================================================
set -euo pipefail

NODE_NAME="${1:-edge3}"
PI_HOST="${2:-pelican-local.local}"
SWARM_HOME="${SWARM_HOME:-$HOME/sovereign-swarm}"
KEYS_DIR="$SWARM_HOME/keys/swarmgate"
CONFIGS_DIR="$SWARM_HOME/configs"

echo "[INFO] Provisioning edge node: $NODE_NAME at $PI_HOST"

# Check if keys exist
if [ ! -f "$KEYS_DIR/${NODE_NAME}.private" ]; then
    echo "[ERROR] Keys for $NODE_NAME not found. Run phase1-key-ceremony.sh first."
    exit 1
fi

# Check if config exists
WG_CONFIG="$CONFIGS_DIR/wg0-${NODE_NAME}.conf"
if [ ! -f "$WG_CONFIG" ]; then
    echo "[ERROR] WireGuard config for $NODE_NAME not found. Run phase2-wireguard-mesh.sh first."
    exit 1
fi

# Create temporary directory for transfer
TEMP_DIR=$(mktemp -d)

# Copy files to temp directory
cp "$KEYS_DIR/${NODE_NAME}.private" "$TEMP_DIR/swarmgate.key"
cp "$KEYS_DIR/${NODE_NAME}.token" "$TEMP_DIR/swarmgate.token"
cp "$WG_CONFIG" "$TEMP_DIR/wg0.conf"

echo "[INFO] Transferring credentials to $PI_HOST..."

# Transfer to Pi's boot partition
scp -r "$TEMP_DIR/"* "pi@${PI_HOST}:/tmp/"
ssh "pi@${PI_HOST}" "sudo cp /tmp/swarmgate.* /tmp/wg0.conf /boot/firmware/"

# Transfer and install join script
scp "$SWARM_HOME/pelican-build/join-sovereign-swarm.sh" "pi@${PI_HOST}:/tmp/"
ssh "pi@${PI_HOST}" "sudo mkdir -p /opt/sovereign-swarm && sudo cp /tmp/join-sovereign-swarm.sh /opt/sovereign-swarm/ && sudo chmod +x /opt/sovereign-swarm/join-sovereign-swarm.sh"

# Install systemd service
scp "$SWARM_HOME/pelican-build/sovereign-swarm-join.service" "pi@${PI_HOST}:/tmp/"
ssh "pi@${PI_HOST}" "sudo cp /tmp/sovereign-swarm-join.service /etc/systemd/system/ && sudo systemctl daemon-reload && sudo systemctl enable sovereign-swarm-join.service"

# Run join script
echo "[INFO] Joining sovereign swarm..."
ssh "pi@${PI_HOST}" "sudo /opt/sovereign-swarm/join-sovereign-swarm.sh"

# Cleanup
rm -rf "$TEMP_DIR"

echo "[SUCCESS] Edge node $NODE_NAME provisioned successfully!"
echo "[INFO] Rebooting to verify auto-join..."
ssh "pi@${PI_HOST}" "sudo reboot" || true
PROVEOF

    chmod +x "$PELICAN_DIR/provision-edge-node.sh"
    echo_success "Provisioning script created: $PELICAN_DIR/provision-edge-node.sh"
}

# Create first-boot setup script for fresh Raspberry Pi OS
create_firstboot_script() {
    echo_info "Creating first-boot setup script..."
    
    cat > "$PELICAN_DIR/pelican-firstboot.sh" << 'EOF'
#!/bin/bash
# =============================================================================
# Pelican Edge Node First-Boot Setup
# Run this on a fresh Raspberry Pi OS 64-bit installation
# =============================================================================
set -euo pipefail

echo "=== Pelican Edge Node First-Boot Setup ==="

# Update system
echo "[INFO] Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install required packages
echo "[INFO] Installing required packages..."
sudo apt install -y \
    wireguard \
    wireguard-tools \
    qrencode \
    curl \
    wget \
    htop \
    iptables-persistent

# Create directory structure
sudo mkdir -p /opt/sovereign-swarm
sudo mkdir -p /var/log/sovereign-swarm

# Configure kernel parameters
echo "[INFO] Configuring kernel parameters..."
sudo tee /etc/sysctl.d/99-sovereign-swarm.conf > /dev/null << SYSCTL
net.ipv4.ip_forward=1
net.ipv4.conf.all.rp_filter=1
net.ipv4.conf.default.rp_filter=1
SYSCTL
sudo sysctl --system

# Set hostname
echo "[INFO] Setting hostname..."
HOSTNAME="pelican-$(cat /proc/cpuinfo | grep Serial | awk '{print $3}' | tail -c 9)"
sudo hostnamectl set-hostname "$HOSTNAME"

# Enable SSH
sudo systemctl enable ssh
sudo systemctl start ssh

# Disable unnecessary services
sudo systemctl disable bluetooth 2>/dev/null || true
sudo systemctl disable avahi-daemon 2>/dev/null || true

echo "[SUCCESS] First-boot setup complete!"
echo "[INFO] Hostname set to: $HOSTNAME"
echo "[INFO] Ready for provisioning from Command-0"
echo ""
echo "Next steps:"
echo "1. Ensure this Pi is accessible from Command-0"
echo "2. Run provision-edge-node.sh from Command-0"
EOF

    chmod +x "$PELICAN_DIR/pelican-firstboot.sh"
    echo_success "First-boot script created: $PELICAN_DIR/pelican-firstboot.sh"
}

# Print deployment instructions
print_instructions() {
    echo ""
    echo_info "=== Pelican Edge Node Build Complete ==="
    echo ""
    echo "Build artifacts in: $PELICAN_DIR"
    echo ""
    echo "Files created:"
    echo "  - join-sovereign-swarm.sh         : Auto-join script for edge nodes"
    echo "  - sovereign-swarm-join.service    : Systemd service for auto-join"
    echo "  - provision-edge-node.sh          : Provisioning script (run from Command-0)"
    echo "  - pelican-firstboot.sh            : First-boot setup for fresh Pi OS"
    echo ""
    echo "Deployment workflow:"
    echo "  1. Flash Raspberry Pi OS 64-bit to SD card"
    echo "  2. Boot Pi and run: ./pelican-firstboot.sh"
    echo "  3. From Command-0, run: ./provision-edge-node.sh <node_name> <pi_hostname>"
    echo "  4. Pi will auto-join the sovereign swarm on boot"
    echo ""
}

# Main execution
main() {
    echo_info "📦 Pelican-Case Edge Node Build"
    echo_info "Creating Raspberry Pi 5 deployment package..."
    echo ""
    
    create_join_script
    create_systemd_service
    create_provisioning_script
    create_firstboot_script
    print_instructions
    
    echo_success "Pelican build complete! 🎉"
}

# Handle script arguments  
case "${1:-run}" in
    "run")
        main
        ;;
    "deps")
        install_deps
        ;;
    "provision")
        if [ -z "${2:-}" ] || [ -z "${3:-}" ]; then
            echo "Usage: $0 provision <node_name> <pi_hostname>"
            exit 1
        fi
        NODE_NAME="$2"
        PI_HOST="$3"
        bash "$PELICAN_DIR/provision-edge-node.sh" "$NODE_NAME" "$PI_HOST"
        ;;
    *)
        echo "Usage: $0 [run|deps|provision]"
        echo "  run       - Create all pelican build artifacts (default)"
        echo "  deps      - Install dependencies on current system"
        echo "  provision - Provision a specific edge node"
        exit 1
        ;;
esac
