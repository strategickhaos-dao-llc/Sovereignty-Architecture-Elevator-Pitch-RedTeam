#!/bin/bash
# =============================================================================
# PHASE 0: Bootstrap Command-0 (Primary Control Node with Starlink Mini)
# Sovereign Swarm Infrastructure - Zero Cloud Dependency
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

# Check if running as root for system installations
check_root() {
    if [ "$EUID" -ne 0 ]; then
        echo_warning "Some operations require root privileges. You may be prompted for sudo password."
    fi
}

# Install required dependencies
install_dependencies() {
    echo_info "Installing Phase 0 dependencies..."
    
    sudo apt update
    sudo apt install -y \
        wireguard-tools \
        qrencode \
        git \
        curl \
        wget \
        unzip \
        build-essential \
        python3-pip \
        sqlite3 \
        iptables \
        net-tools
    
    # Optional: YubiHSM support (uncomment if hardware HSM available)
    # sudo apt install -y yubihsm-shell libykhsmauth1-dev
    
    echo_success "Dependencies installed successfully"
}

# Create sovereign swarm directory structure
create_swarm_structure() {
    echo_info "Creating sovereign swarm directory structure at $SWARM_HOME..."
    
    mkdir -p "$SWARM_HOME"/{keys/swarmgate,configs,logs,backups}
    cd "$SWARM_HOME"
    
    # Initialize git repository if not already initialized
    if [ ! -d ".git" ]; then
        git init .
        echo_success "Git repository initialized"
    else
        echo_warning "Git repository already exists"
    fi
    
    # Create .gitignore for sensitive files
    cat > .gitignore << 'EOF'
# Private keys - NEVER commit these
keys/swarmgate/*.private
keys/swarmgate/*.token
*.pem
*.key

# Logs and temporary files
logs/
*.log
*.tmp

# Backup files
backups/
EOF
    
    echo_success "Directory structure created"
}

# Configure kernel parameters for WireGuard
configure_kernel() {
    echo_info "Configuring kernel parameters for WireGuard..."
    
    # Enable IP forwarding
    sudo sysctl -w net.ipv4.ip_forward=1
    sudo sysctl -w net.ipv4.conf.all.src_valid_mark=1
    
    # Anti-spoofing protection
    sudo sysctl -w net.ipv4.conf.all.rp_filter=1
    sudo sysctl -w net.ipv4.conf.default.rp_filter=1
    
    # Make persistent across reboots
    sudo tee /etc/sysctl.d/99-sovereign-swarm.conf > /dev/null << 'EOF'
# Sovereign Swarm WireGuard Configuration
net.ipv4.ip_forward=1
net.ipv4.conf.all.src_valid_mark=1
net.ipv4.conf.all.rp_filter=1
net.ipv4.conf.default.rp_filter=1
EOF
    
    sudo sysctl --system > /dev/null 2>&1
    
    echo_success "Kernel parameters configured"
}

# Configure basic firewall rules
configure_firewall() {
    echo_info "Configuring firewall rules..."
    
    # Check if ufw is installed
    if command -v ufw &> /dev/null; then
        sudo ufw default deny incoming
        sudo ufw default allow outgoing
        sudo ufw allow 51820/udp comment 'WireGuard VPN'
        sudo ufw allow 22/tcp comment 'SSH'
        sudo ufw --force enable
        echo_success "UFW firewall configured"
    else
        echo_warning "UFW not installed. Using iptables directly."
        # Basic iptables rules
        sudo iptables -A INPUT -p udp --dport 51820 -j ACCEPT
        sudo iptables -A INPUT -i lo -j ACCEPT
        sudo iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
    fi
}

# Print next steps
print_next_steps() {
    echo ""
    echo_info "=== Phase 0 Bootstrap Complete ==="
    echo ""
    echo "Next steps:"
    echo "  1. Run Phase 1 Key Ceremony: ./phase1-key-ceremony.sh"
    echo "  2. Configure WireGuard mesh: ./phase2-wireguard-mesh.sh"
    echo "  3. Deploy edge nodes with: ./pelican-build.sh"
    echo ""
    echo "Working directory: $SWARM_HOME"
    echo ""
    echo_success "Command-0 is ready for sovereign swarm operations"
}

# Main execution
main() {
    echo_info "🔥 Sovereign Swarm Phase 0: Bootstrap"
    echo_info "Initializing Command-0 node..."
    echo ""
    
    check_root
    install_dependencies
    create_swarm_structure
    configure_kernel
    configure_firewall
    print_next_steps
    
    echo_success "Phase 0 complete! 🎉"
}

# Handle script arguments
case "${1:-run}" in
    "run")
        main
        ;;
    "deps")
        install_dependencies
        ;;
    "structure")
        create_swarm_structure
        ;;
    "kernel")
        configure_kernel
        ;;
    "firewall")
        configure_firewall
        ;;
    *)
        echo "Usage: $0 [run|deps|structure|kernel|firewall]"
        echo "  run       - Run complete Phase 0 bootstrap (default)"
        echo "  deps      - Install dependencies only"
        echo "  structure - Create directory structure only"
        echo "  kernel    - Configure kernel parameters only"
        echo "  firewall  - Configure firewall only"
        exit 1
        ;;
esac
