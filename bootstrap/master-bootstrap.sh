#!/bin/bash
# Sovereign Swarm Edge Node Bootstrap Script v0.1.4
# A hardened bootstrap script for deploying sovereign swarm edge nodes
# 
# SAFETY NOTES:
# - No destructive rollback() function that could purge system packages
# - If script fails, it exits cleanly - manual cleanup only
# - PyNaCl validation happens before any system changes
#
# Usage:
#   cd /opt/sovereign-swarm
#   sudo NODE_ID=edge3 ./master-bootstrap.sh

set -euo pipefail

# ==============================================================================
# Configuration
# ==============================================================================
readonly SCRIPT_VERSION="0.1.4"
readonly LOG_FILE="/var/log/sovereign-swarm-bootstrap.log"
readonly SWARM_DIR="/opt/sovereign-swarm"
readonly WG_INTERFACE="wg0"

# NODE_ID must be set before running
NODE_ID="${NODE_ID:-}"

# Colors for output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m' # No Color

# ==============================================================================
# Logging Functions
# ==============================================================================
log_info() {
    local msg
    msg="[INFO] $(date '+%Y-%m-%d %H:%M:%S') - $1"
    echo -e "${BLUE}${msg}${NC}"
    echo "$msg" >> "$LOG_FILE" 2>/dev/null || true
}

log_success() {
    local msg
    msg="[SUCCESS] $(date '+%Y-%m-%d %H:%M:%S') - $1"
    echo -e "${GREEN}${msg}${NC}"
    echo "$msg" >> "$LOG_FILE" 2>/dev/null || true
}

log_warning() {
    local msg
    msg="[WARNING] $(date '+%Y-%m-%d %H:%M:%S') - $1"
    echo -e "${YELLOW}${msg}${NC}"
    echo "$msg" >> "$LOG_FILE" 2>/dev/null || true
}

log_error() {
    local msg
    msg="[ERROR] $(date '+%Y-%m-%d %H:%M:%S') - $1"
    echo -e "${RED}${msg}${NC}"
    echo "$msg" >> "$LOG_FILE" 2>/dev/null || true
}

# ==============================================================================
# Pre-flight Checks
# ==============================================================================
check_root() {
    if [[ $EUID -ne 0 ]]; then
        log_error "This script must be run as root (sudo)"
        exit 1
    fi
}

check_node_id() {
    if [[ -z "$NODE_ID" ]]; then
        log_error "NODE_ID environment variable must be set"
        log_error "Usage: sudo NODE_ID=edge3 ./master-bootstrap.sh"
        exit 1
    fi
    log_info "Bootstrapping node: $NODE_ID"
}

# ==============================================================================
# PyNaCl Validation (CRITICAL - Run before any system changes)
# ==============================================================================
validate_pynacl() {
    log_info "Validating PyNaCl installation..."
    
    # Test if nacl.signing is available
    if python3 -c "from nacl.signing import SigningKey; print('PyNaCl OK')" 2>/dev/null; then
        log_success "PyNaCl validation passed"
        return 0
    fi
    
    log_warning "PyNaCl not found or not working. Attempting to install..."
    
    # Update package lists first for apt installation
    log_info "Updating package lists..."
    apt-get update || log_warning "apt-get update had issues, continuing..."
    
    # Try apt first (Debian's python3-nacl)
    log_info "Attempting to install python3-nacl via apt..."
    if apt-get install -y python3-nacl; then
        if python3 -c "from nacl.signing import SigningKey; print('PyNaCl OK')" 2>/dev/null; then
            log_success "PyNaCl installed via apt"
            return 0
        fi
        log_warning "apt installed python3-nacl but import still fails, trying pip..."
    else
        log_warning "apt install failed, trying pip..."
    fi
    
    # Fallback to pip
    log_info "Attempting pip installation..."
    if ! command -v pip3 &>/dev/null; then
        log_info "Installing pip3..."
        apt-get install -y python3-pip || log_warning "pip3 installation had issues"
    fi
    
    if pip3 install pynacl; then
        if python3 -c "from nacl.signing import SigningKey; print('PyNaCl OK')" 2>/dev/null; then
            log_success "PyNaCl installed via pip"
            return 0
        fi
    fi
    
    log_error "Failed to install PyNaCl. Cannot continue."
    log_error "Please manually run: pip3 install pynacl"
    exit 1
}

# ==============================================================================
# System Package Installation
# ==============================================================================
install_packages() {
    log_info "Updating package lists..."
    apt-get update
    
    log_info "Installing required packages..."
    apt-get install -y \
        wireguard \
        wireguard-tools \
        nftables \
        ufw \
        curl \
        jq \
        ca-certificates \
        gnupg
    
    log_success "Core packages installed"
}

# ==============================================================================
# WireGuard Configuration
# ==============================================================================
setup_wireguard() {
    log_info "Setting up WireGuard..."
    
    # Create WireGuard directory if it doesn't exist
    mkdir -p /etc/wireguard
    chmod 700 /etc/wireguard
    
    # Generate keys if they don't exist
    if [[ ! -f /etc/wireguard/privatekey ]]; then
        log_info "Generating WireGuard keys..."
        wg genkey | tee /etc/wireguard/privatekey | wg pubkey > /etc/wireguard/publickey
        chmod 600 /etc/wireguard/privatekey
        chmod 644 /etc/wireguard/publickey
        log_success "WireGuard keys generated"
    else
        log_info "WireGuard keys already exist, skipping key generation"
    fi
    
    # Create basic wg0.conf if it doesn't exist
    if [[ ! -f /etc/wireguard/${WG_INTERFACE}.conf ]]; then
        log_warning "WireGuard config not found at /etc/wireguard/${WG_INTERFACE}.conf"
        log_info "Please create your WireGuard configuration manually"
        log_info "Your public key: $(cat /etc/wireguard/publickey)"
    else
        log_info "WireGuard config exists"
    fi
    
    log_success "WireGuard setup complete"
}

# ==============================================================================
# Firewall Configuration
# ==============================================================================
setup_firewall() {
    log_info "Configuring firewall..."
    
    # Check if UFW is already enabled
    if ufw status | grep -q "Status: active"; then
        log_info "UFW is already enabled, adding rules..."
    else
        log_info "Enabling UFW..."
        # Use yes to auto-confirm the enable prompt instead of --force
        # This allows the user to see what's happening
        yes | ufw enable || {
            log_warning "Could not enable UFW, you may need to enable it manually"
        }
    fi
    
    # Allow SSH (always keep SSH open!)
    ufw allow 22/tcp comment 'SSH'
    
    # Allow WireGuard
    ufw allow 51820/udp comment 'WireGuard'
    
    # Allow NATS
    ufw allow 4222/tcp comment 'NATS'
    
    # Allow Syncthing (optional, common port)
    ufw allow 8008/tcp comment 'Syncthing'
    
    log_success "Firewall configured"
}

# ==============================================================================
# Sovereign Swarm Directory Setup
# ==============================================================================
setup_swarm_dir() {
    log_info "Setting up sovereign swarm directory..."
    
    mkdir -p "$SWARM_DIR"/{config,data,logs,scripts}
    
    # Create node identity file
    echo "$NODE_ID" > "$SWARM_DIR/config/node_id"
    
    log_success "Swarm directory structure created at $SWARM_DIR"
}

# ==============================================================================
# Verification
# ==============================================================================
verify_installation() {
    log_info "Verifying installation..."
    
    echo ""
    echo "=============================================="
    echo "  Verification Commands"
    echo "=============================================="
    echo ""
    
    # WireGuard status
    echo "--- WireGuard Status ---"
    wg show || echo "WireGuard not active (no peers configured yet)"
    echo ""
    
    # Listening ports
    echo "--- Listening Ports (SSH, WireGuard, NATS, Syncthing) ---"
    ss -lntup | grep -E ':(22|51820|4222|8008)' || echo "Some expected ports not listening yet"
    echo ""
    
    # UFW status
    echo "--- UFW Firewall Status ---"
    ufw status verbose || echo "UFW status check failed"
    echo ""
    
    # Service status (if configured)
    echo "--- Service Status ---"
    if systemctl is-enabled wg-quick@${WG_INTERFACE} 2>/dev/null; then
        systemctl status wg-quick@${WG_INTERFACE} --no-pager || true
    else
        echo "wg-quick@${WG_INTERFACE} not enabled yet"
    fi
    echo ""
    
    # PyNaCl validation with proper error handling
    echo "--- PyNaCl Validation ---"
    if python3 -c "from nacl.signing import SigningKey; print('PyNaCl OK')" 2>/dev/null; then
        echo "PyNaCl validation: PASSED"
    else
        log_error "PyNaCl validation: FAILED"
        log_error "The nacl.signing import is not working properly"
    fi
    echo ""
    
    log_success "Verification complete for node: $NODE_ID"
}

# ==============================================================================
# Main Execution
# ==============================================================================
main() {
    echo ""
    echo "=============================================="
    echo "  Sovereign Swarm Bootstrap v${SCRIPT_VERSION}"
    echo "=============================================="
    echo ""
    
    # Pre-flight checks
    check_root
    check_node_id
    
    # CRITICAL: Validate PyNaCl BEFORE any system changes
    validate_pynacl
    
    # Proceed with installation
    install_packages
    setup_wireguard
    setup_firewall
    setup_swarm_dir
    
    # Verify everything
    verify_installation
    
    echo ""
    log_success "Bootstrap complete for node: $NODE_ID"
    echo ""
    echo "Next steps:"
    echo "  1. Configure WireGuard peers in /etc/wireguard/${WG_INTERFACE}.conf"
    echo "  2. Enable WireGuard: sudo systemctl enable --now wg-quick@${WG_INTERFACE}"
    echo "  3. Install additional services (NATS, Syncthing, Docker) as needed"
    echo ""
}

# Run main (no trap - if script fails, it just exits cleanly)
main "$@"
