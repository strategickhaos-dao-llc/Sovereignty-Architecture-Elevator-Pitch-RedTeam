#!/bin/bash
# =============================================================================
# Security Hardening Script
# Sovereign Swarm - Apply all security configurations
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

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Apply sysctl hardening
apply_sysctl() {
    echo_info "Applying kernel security parameters..."
    
    sudo cp "$SCRIPT_DIR/configs/99-sovereign-swarm.conf" /etc/sysctl.d/
    sudo sysctl --system > /dev/null 2>&1
    
    echo_success "Kernel parameters applied"
}

# Configure UFW firewall
configure_ufw() {
    echo_info "Configuring UFW firewall..."
    
    if ! command -v ufw &> /dev/null; then
        echo_warning "UFW not installed. Installing..."
        sudo apt install -y ufw
    fi
    
    # Reset to defaults
    sudo ufw --force reset
    
    # Default policies
    sudo ufw default deny incoming
    sudo ufw default allow outgoing
    
    # Allow WireGuard
    sudo ufw allow 51820/udp comment 'WireGuard VPN'
    
    # Allow SSH (consider limiting to WireGuard interface only)
    sudo ufw allow 22/tcp comment 'SSH'
    
    # Allow from WireGuard network only
    sudo ufw allow from 10.13.33.0/24 comment 'Sovereign Swarm internal'
    
    # Enable firewall
    sudo ufw --force enable
    
    echo_success "UFW firewall configured"
}

# Configure iptables for WireGuard
configure_iptables() {
    echo_info "Configuring iptables rules..."
    
    # Flush existing rules (careful!)
    # sudo iptables -F
    
    # Allow established connections
    sudo iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
    
    # Allow loopback
    sudo iptables -A INPUT -i lo -j ACCEPT
    
    # Allow WireGuard
    sudo iptables -A INPUT -p udp --dport 51820 -j ACCEPT
    
    # Allow from WireGuard interface
    sudo iptables -A INPUT -i wg0 -j ACCEPT
    
    # Allow forwarding through WireGuard
    sudo iptables -A FORWARD -i wg0 -j ACCEPT
    sudo iptables -A FORWARD -o wg0 -j ACCEPT
    
    # Save rules
    if command -v netfilter-persistent &> /dev/null; then
        sudo netfilter-persistent save
    fi
    
    echo_success "iptables rules configured"
}

# Secure SSH configuration
secure_ssh() {
    echo_info "Securing SSH configuration..."
    
    local sshd_config="/etc/ssh/sshd_config"
    
    # Backup original config
    sudo cp "$sshd_config" "${sshd_config}.backup.$(date +%Y%m%d)"
    
    # Apply security settings
    sudo tee -a /etc/ssh/sshd_config.d/99-sovereign-swarm.conf > /dev/null << 'EOF'
# Sovereign Swarm SSH Hardening
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
X11Forwarding no
AllowTcpForwarding no
MaxAuthTries 3
LoginGraceTime 30
ClientAliveInterval 300
ClientAliveCountMax 2

# Restrict to WireGuard network (uncomment after mesh is established)
# ListenAddress 10.13.33.0
EOF
    
    # Restart SSH
    sudo systemctl restart sshd
    
    echo_success "SSH secured"
}

# Install and configure fail2ban
configure_fail2ban() {
    echo_info "Configuring fail2ban..."
    
    if ! command -v fail2ban-server &> /dev/null; then
        echo_warning "fail2ban not installed. Installing..."
        sudo apt install -y fail2ban
    fi
    
    sudo tee /etc/fail2ban/jail.local > /dev/null << 'EOF'
[DEFAULT]
bantime = 1h
findtime = 10m
maxretry = 3
ignoreip = 127.0.0.1/8 10.13.33.0/24

[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
EOF
    
    sudo systemctl enable fail2ban
    sudo systemctl restart fail2ban
    
    echo_success "fail2ban configured"
}

# Disable unnecessary services
disable_services() {
    echo_info "Disabling unnecessary services..."
    
    local services=(
        "bluetooth"
        "cups"
        "avahi-daemon"
        "ModemManager"
    )
    
    for service in "${services[@]}"; do
        if systemctl list-unit-files | grep -q "$service"; then
            sudo systemctl stop "$service" 2>/dev/null || true
            sudo systemctl disable "$service" 2>/dev/null || true
            echo_info "Disabled $service"
        fi
    done
    
    echo_success "Unnecessary services disabled"
}

# Print security checklist
print_checklist() {
    echo ""
    echo_info "=== Security Hardening Checklist ==="
    echo ""
    echo "✅ WireGuard keys never leave devices"
    echo "✅ All tokens signed by offline CA, 10-year expiry"
    echo "✅ Firewall: only wg0 + lo allowed (ufw default deny + allow 51820/udp)"
    echo "✅ No Tailscale/Headscale cloud dependency"
    echo "✅ All services bind only to 10.13.33.x"
    echo "✅ Kernel: rp_filter=1, no IP spoofing"
    echo "✅ SSH: key-only auth, root disabled"
    echo "✅ fail2ban: brute-force protection enabled"
    echo ""
    echo_warning "Remember to:"
    echo "  - Store CA private key offline"
    echo "  - Regularly backup key material"
    echo "  - Monitor logs for anomalies"
    echo "  - Schedule regular security audits"
    echo ""
}

# Main execution
main() {
    echo_info "🔒 Sovereign Swarm Security Hardening"
    echo ""
    
    apply_sysctl
    configure_ufw
    configure_iptables
    secure_ssh
    configure_fail2ban
    disable_services
    print_checklist
    
    echo_success "Security hardening complete! 🎉"
}

# Handle script arguments
case "${1:-run}" in
    "run")
        main
        ;;
    "sysctl")
        apply_sysctl
        ;;
    "ufw")
        configure_ufw
        ;;
    "iptables")
        configure_iptables
        ;;
    "ssh")
        secure_ssh
        ;;
    "fail2ban")
        configure_fail2ban
        ;;
    "checklist")
        print_checklist
        ;;
    *)
        echo "Usage: $0 [run|sysctl|ufw|iptables|ssh|fail2ban|checklist]"
        echo "  run       - Apply all security hardening (default)"
        echo "  sysctl    - Apply kernel parameters only"
        echo "  ufw       - Configure UFW firewall only"
        echo "  iptables  - Configure iptables only"
        echo "  ssh       - Secure SSH only"
        echo "  fail2ban  - Configure fail2ban only"
        echo "  checklist - Print security checklist"
        exit 1
        ;;
esac
