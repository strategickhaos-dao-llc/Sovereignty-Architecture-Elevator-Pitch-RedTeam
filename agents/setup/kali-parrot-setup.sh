#!/bin/bash
# Agent Environment Setup for Kali Linux / Parrot OS
# This script installs necessary tools for agent collaboration with Kubernetes cluster

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running on Kali or Parrot
check_os() {
    log_info "Checking operating system..."
    if [[ -f /etc/os-release ]]; then
        . /etc/os-release
        if [[ "$ID" == "kali" ]] || [[ "$ID" == "parrot" ]]; then
            log_info "Detected $NAME - proceeding with setup"
            return 0
        fi
    fi
    log_warn "This script is optimized for Kali Linux or Parrot OS, but will attempt to continue"
}

# Update system packages
update_system() {
    log_info "Updating system packages..."
    sudo apt-get update -qq
    sudo apt-get upgrade -y -qq
}

# Install Docker CLI tools
install_docker() {
    log_info "Installing Docker CLI..."
    if command -v docker &> /dev/null; then
        log_info "Docker already installed: $(docker --version)"
        return 0
    fi
    
    # Install Docker
    curl -fsSL https://get.docker.com -o /tmp/get-docker.sh
    sudo sh /tmp/get-docker.sh
    sudo usermod -aG docker "$USER"
    rm /tmp/get-docker.sh
    
    log_info "Docker installed successfully"
}

# Install kubectl
install_kubectl() {
    log_info "Installing kubectl..."
    if command -v kubectl &> /dev/null; then
        log_info "kubectl already installed: $(kubectl version --client -o yaml 2>/dev/null | grep gitVersion || echo 'version check failed')"
        return 0
    fi
    
    # Download latest kubectl
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
    sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
    rm kubectl
    
    log_info "kubectl installed successfully"
}

# Install helm
install_helm() {
    log_info "Installing Helm..."
    if command -v helm &> /dev/null; then
        log_info "Helm already installed: $(helm version --short)"
        return 0
    fi
    
    curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
    
    log_info "Helm installed successfully"
}

# Install essential networking tools
install_network_tools() {
    log_info "Installing networking tools..."
    sudo apt-get install -y -qq \
        curl \
        wget \
        netcat \
        nmap \
        net-tools \
        dnsutils \
        iputils-ping \
        traceroute \
        tcpdump \
        wireshark-common \
        jq \
        yq
    
    log_info "Networking tools installed successfully"
}

# Install VPN tools
install_vpn_tools() {
    log_info "Installing VPN tools..."
    sudo apt-get install -y -qq \
        wireguard \
        wireguard-tools \
        openvpn \
        network-manager-openvpn
    
    log_info "VPN tools installed successfully"
}

# Install monitoring and debugging tools
install_monitoring_tools() {
    log_info "Installing monitoring tools..."
    sudo apt-get install -y -qq \
        htop \
        iotop \
        iftop \
        sysstat
    
    log_info "Monitoring tools installed successfully"
}

# Create kubectl configuration directory
setup_kubectl_config() {
    log_info "Setting up kubectl configuration..."
    mkdir -p "$HOME/.kube"
    chmod 700 "$HOME/.kube"
    
    if [[ ! -f "$HOME/.kube/config" ]]; then
        log_warn "kubectl config file not found. You'll need to copy your kubeconfig to ~/.kube/config"
        log_warn "Example: export KUBECONFIG=~/.kube/config"
    fi
}

# Setup bash completion
setup_completion() {
    log_info "Setting up bash completion..."
    
    # kubectl completion
    kubectl completion bash | sudo tee /etc/bash_completion.d/kubectl > /dev/null
    
    # helm completion
    helm completion bash | sudo tee /etc/bash_completion.d/helm > /dev/null
    
    # docker completion
    if [[ -f /usr/share/bash-completion/completions/docker ]]; then
        log_info "Docker completion already available"
    fi
    
    log_info "Bash completion setup complete"
}

# Create agent workspace
create_workspace() {
    log_info "Creating agent workspace..."
    mkdir -p "$HOME/agent-workspace"
    mkdir -p "$HOME/agent-workspace/scripts"
    mkdir -p "$HOME/agent-workspace/configs"
    mkdir -p "$HOME/agent-workspace/logs"
    
    log_info "Agent workspace created at $HOME/agent-workspace"
}

# Verification
verify_installation() {
    log_info "Verifying installation..."
    
    local failed=0
    
    # Check Docker
    if command -v docker &> /dev/null; then
        log_info "✓ Docker: $(docker --version)"
    else
        log_error "✗ Docker not found"
        ((failed++))
    fi
    
    # Check kubectl
    if command -v kubectl &> /dev/null; then
        log_info "✓ kubectl: $(kubectl version --client -o yaml 2>/dev/null | grep gitVersion | head -n1 || echo 'installed')"
    else
        log_error "✗ kubectl not found"
        ((failed++))
    fi
    
    # Check helm
    if command -v helm &> /dev/null; then
        log_info "✓ Helm: $(helm version --short)"
    else
        log_error "✗ Helm not found"
        ((failed++))
    fi
    
    # Check curl
    if command -v curl &> /dev/null; then
        log_info "✓ curl: $(curl --version | head -n1)"
    else
        log_error "✗ curl not found"
        ((failed++))
    fi
    
    # Check jq
    if command -v jq &> /dev/null; then
        log_info "✓ jq: $(jq --version)"
    else
        log_error "✗ jq not found"
        ((failed++))
    fi
    
    if [[ $failed -eq 0 ]]; then
        log_info "All tools installed successfully!"
        return 0
    else
        log_error "$failed tool(s) failed to install"
        return 1
    fi
}

# Display post-install instructions
post_install_instructions() {
    cat << 'EOF'

╔════════════════════════════════════════════════════════════════╗
║           Agent Environment Setup Complete!                    ║
╚════════════════════════════════════════════════════════════════╝

Next Steps:
-----------
1. Configure kubectl access:
   - Copy your kubeconfig to ~/.kube/config
   - Test with: kubectl get nodes

2. Setup VPN connection:
   - Configure WireGuard: sudo wg-quick up wg0
   - Or OpenVPN: sudo openvpn --config /path/to/config.ovpn

3. Verify cluster access:
   - kubectl get pods --all-namespaces
   - kubectl get services -n ops

4. Test API endpoint:
   - curl http://<vpn-ip>:30000/api/v1/health

5. Review documentation:
   - See docs/agents/AGENT_COLLABORATION.md for details

For issues, check the troubleshooting guide in the documentation.

EOF
}

# Main execution
main() {
    log_info "Starting agent environment setup..."
    
    check_os
    update_system
    install_docker
    install_kubectl
    install_helm
    install_network_tools
    install_vpn_tools
    install_monitoring_tools
    setup_kubectl_config
    setup_completion
    create_workspace
    verify_installation
    post_install_instructions
    
    log_info "Setup complete! Please restart your terminal or run: source ~/.bashrc"
}

# Run main function
main "$@"
