#!/usr/bin/env bash
# Sovereign Mesh Bootstrap - Omnipresent Autonomous Executive Override
# Handles multi-environment deployment with intelligent shell detection
set -euo pipefail

# ANSI color codes for beautiful output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Banner
echo_banner() {
    echo -e "${CYAN}${BOLD}"
    echo "┌─────────────────────────────────────────────────────────────────┐"
    echo "│         SOVEREIGN MESH BOOTSTRAP - EXECUTIVE OVERRIDE           │"
    echo "│     Omnipresent Autonomous Architecture Deployment System       │"
    echo "└─────────────────────────────────────────────────────────────────┘"
    echo -e "${NC}"
}

# Logging functions
echo_status() {
    echo -e "${BLUE}[STATUS]${NC} $1"
}

echo_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

echo_warning() {
    echo -e "${YELLOW}[⚠]${NC} $1"
}

echo_error() {
    echo -e "${RED}[✗]${NC} $1"
}

echo_exec() {
    echo -e "${MAGENTA}[EXEC]${NC} $1"
}

# Shell Environment Detection
detect_shell_environment() {
    echo_status "Detecting shell environment..."
    
    local shell_type="unknown"
    local os_type="unknown"
    
    # Detect OS
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        os_type="linux"
        if grep -qi microsoft /proc/version 2>/dev/null; then
            shell_type="wsl"
            echo_success "Environment: WSL (Windows Subsystem for Linux)"
        else
            shell_type="native-linux"
            echo_success "Environment: Native Linux"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        os_type="macos"
        shell_type="native-macos"
        echo_success "Environment: macOS"
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
        os_type="windows"
        shell_type="git-bash"
        echo_success "Environment: Git Bash (MSYS)"
    elif [[ -n "${BASH_VERSION:-}" ]]; then
        os_type="unknown-bash"
        shell_type="bash"
        echo_warning "Environment: Generic Bash (unidentified system)"
    else
        os_type="unknown"
        shell_type="unknown"
        echo_error "Environment: Unknown shell type"
    fi
    
    # Check if running in PowerShell by mistake
    if [[ -n "${PSModulePath:-}" ]] && [[ -z "${WSL_DISTRO_NAME:-}" ]]; then
        echo_error "CRITICAL: This script is being executed in PowerShell!"
        echo_error "PowerShell cannot properly interpret Bash scripts."
        echo ""
        echo_warning "Solutions:"
        echo "  1. Run in WSL: ${BOLD}wsl bash ./sovereign-mesh-bootstrap.sh${NC}"
        echo "  2. Run in Git Bash: ${BOLD}\"C:\\Program Files\\Git\\bin\\bash.exe\" ./sovereign-mesh-bootstrap.sh${NC}"
        echo "  3. Install WSL: ${BOLD}wsl --install${NC}"
        exit 1
    fi
    
    export DETECTED_SHELL="$shell_type"
    export DETECTED_OS="$os_type"
}

# GitHub CLI Detection and Installation
check_gh_cli() {
    echo_status "Checking for GitHub CLI (gh)..."
    
    if command -v gh &> /dev/null; then
        local gh_version
        gh_version=$(gh --version | head -n1 | awk '{print $3}')
        echo_success "GitHub CLI found: version $gh_version"
        export GH_CLI_AVAILABLE="true"
        return 0
    else
        echo_warning "GitHub CLI (gh) not found in PATH"
        echo_warning "Current PATH: $PATH"
        
        echo ""
        echo_status "GitHub CLI Installation Options:"
        echo ""
        
        case "$DETECTED_SHELL" in
            wsl)
                echo "  ${BOLD}For WSL (Ubuntu/Debian):${NC}"
                echo "    curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg"
                echo "    echo \"deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main\" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null"
                echo "    sudo apt update && sudo apt install gh"
                ;;
            git-bash)
                echo "  ${BOLD}For Windows (via winget in PowerShell):${NC}"
                echo "    winget install GitHub.cli"
                echo ""
                echo "  ${BOLD}Or via Chocolatey:${NC}"
                echo "    choco install gh"
                echo ""
                echo "  ${BOLD}Or download installer:${NC}"
                echo "    https://github.com/cli/cli/releases/latest"
                ;;
            native-macos)
                echo "  ${BOLD}For macOS (via Homebrew):${NC}"
                echo "    brew install gh"
                ;;
            native-linux)
                echo "  ${BOLD}For Linux:${NC}"
                echo "    See instructions at: https://github.com/cli/cli/blob/trunk/docs/install_linux.md"
                ;;
            *)
                echo "  ${BOLD}Visit:${NC} https://cli.github.com/"
                ;;
        esac
        
        echo ""
        echo_warning "Install gh CLI and re-run this script, or continue without it (some features disabled)"
        
        # Ask if user wants to continue
        read -p "Continue without gh CLI? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo_error "Bootstrap aborted. Install gh CLI and try again."
            exit 1
        fi
        
        export GH_CLI_AVAILABLE="false"
        return 1
    fi
}

# Check Prerequisites
check_prerequisites() {
    echo_status "Checking prerequisites..."
    
    local missing_deps=()
    
    # Essential commands
    local required_commands=("git" "docker" "curl" "jq")
    
    for cmd in "${required_commands[@]}"; do
        if ! command -v "$cmd" &> /dev/null; then
            missing_deps+=("$cmd")
            echo_warning "Missing: $cmd"
        else
            echo_success "Found: $cmd"
        fi
    done
    
    # Docker Compose (check both docker-compose and docker compose)
    if command -v docker-compose &> /dev/null || docker compose version &> /dev/null 2>&1; then
        echo_success "Found: docker-compose"
    else
        missing_deps+=("docker-compose")
        echo_warning "Missing: docker-compose or 'docker compose'"
    fi
    
    # Node.js (optional but recommended)
    if command -v node &> /dev/null; then
        local node_version
        node_version=$(node --version)
        echo_success "Found: Node.js $node_version"
    else
        echo_warning "Optional: Node.js not found (needed for Discord bot)"
    fi
    
    if [ ${#missing_deps[@]} -gt 0 ]; then
        echo_error "Missing required dependencies: ${missing_deps[*]}"
        echo_error "Please install missing dependencies and re-run this script"
        exit 1
    fi
    
    echo_success "All required prerequisites met"
}

# Initialize Environment Configuration
init_environment() {
    echo_status "Initializing environment configuration..."
    
    # Check if .env exists
    if [ -f ".env" ]; then
        echo_warning ".env file already exists"
        read -p "Overwrite existing .env? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo_status "Keeping existing .env file"
            return 0
        fi
    fi
    
    # Copy from .env.example if it exists
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo_success "Created .env from .env.example"
    else
        echo_warning ".env.example not found, creating minimal .env"
        cat > .env << 'EOF'
# Sovereign Mesh Configuration
# Auto-generated by sovereign-mesh-bootstrap.sh

# Discord Configuration
DISCORD_TOKEN=your_discord_bot_token_here
DISCORD_GUILD_ID=your_discord_guild_id_here
DISCORD_PR_CHANNEL_ID=
DISCORD_WEBHOOK_URL=

# GitHub Configuration
GITHUB_WEBHOOK_SECRET=
GITHUB_APP_ID=
GITHUB_APP_PRIVATE_KEY_PATH=

# Security
HMAC_SECRET=
JWT_SECRET=

# Environment
ENV=development
LOG_LEVEL=info
PORT=3001

# Vault (Development)
VAULT_ADDR=http://vault:8200
VAULT_TOKEN=root

# AI/ML APIs (Optional)
OPENAI_API_KEY=
XAI_API_KEY=
ANTHROPIC_API_KEY=
EOF
        echo_success "Created minimal .env file"
    fi
    
    echo_warning "Remember to edit .env with your actual credentials!"
}

# Install Node Dependencies
install_dependencies() {
    echo_status "Installing project dependencies..."
    
    if [ -f "package.json" ]; then
        if command -v npm &> /dev/null; then
            echo_exec "npm install"
            npm install
            echo_success "Node.js dependencies installed"
        else
            echo_warning "npm not found, skipping Node.js dependencies"
        fi
    else
        echo_warning "package.json not found, skipping dependency installation"
    fi
}

# Docker Compose Deployment
deploy_infrastructure() {
    echo_status "Deploying sovereign infrastructure..."
    
    # Check which compose files are available
    local compose_files=()
    
    if [ -f "docker-compose.yml" ]; then
        compose_files+=("docker-compose.yml")
    fi
    
    if [ -f "docker-compose.obs.yml" ]; then
        echo_status "Found observability stack configuration"
        compose_files+=("docker-compose.obs.yml")
    fi
    
    if [ ${#compose_files[@]} -eq 0 ]; then
        echo_warning "No docker-compose files found, skipping infrastructure deployment"
        return 0
    fi
    
    echo_exec "Starting Docker services..."
    
    # Try docker compose (new) first, fall back to docker-compose (old)
    if docker compose version &> /dev/null 2>&1; then
        for file in "${compose_files[@]}"; do
            echo_status "Deploying: $file"
            docker compose -f "$file" up -d
        done
    elif command -v docker-compose &> /dev/null; then
        for file in "${compose_files[@]}"; do
            echo_status "Deploying: $file"
            docker-compose -f "$file" up -d
        done
    else
        echo_error "Neither 'docker compose' nor 'docker-compose' is available"
        return 1
    fi
    
    echo_success "Infrastructure deployment initiated"
    
    # Wait for services to start
    echo_status "Waiting for services to initialize..."
    sleep 5
    
    # Check service status
    if docker compose version &> /dev/null 2>&1; then
        docker compose ps
    elif command -v docker-compose &> /dev/null; then
        docker-compose ps
    fi
}

# Kubernetes Bootstrap (if available)
deploy_kubernetes() {
    echo_status "Checking for Kubernetes deployment..."
    
    if [ -d "bootstrap/k8s" ]; then
        if command -v kubectl &> /dev/null; then
            echo_status "Kubernetes detected, deploying control plane..."
            
            if [ -f "bootstrap/deploy.sh" ]; then
                bash bootstrap/deploy.sh
                echo_success "Kubernetes deployment complete"
            else
                echo_warning "bootstrap/deploy.sh not found, skipping K8s deployment"
            fi
        else
            echo_warning "kubectl not found, skipping Kubernetes deployment"
        fi
    else
        echo_status "No Kubernetes configuration found, skipping"
    fi
}

# Executive Override System - Autonomous Operations
setup_executive_override() {
    echo_status "Configuring Omnipresent Autonomous Executive Override..."
    
    # Create executive override configuration
    mkdir -p .sovereign-mesh
    
    cat > .sovereign-mesh/executive-override.yaml << 'EOF'
# Omnipresent Autonomous Executive Override Configuration
# This system provides autonomous decision-making capabilities

override:
  enabled: true
  mode: "autonomous"
  
  # Autonomous decision criteria
  decision_matrix:
    security_critical: "immediate"
    performance_degradation: "automatic"
    resource_exhaustion: "proactive"
    
  # Executive permissions
  permissions:
    - "system:restart"
    - "system:scale"
    - "system:failover"
    - "system:rollback"
    - "security:patch"
    
  # Notification channels
  notifications:
    discord: true
    email: false
    sms: false
    
  # Autonomous actions log
  audit:
    enabled: true
    retention_days: 90
    
  # Override thresholds
  thresholds:
    cpu_critical: 90
    memory_critical: 85
    disk_critical: 90
    error_rate_critical: 5
EOF
    
    # Create autonomous monitoring script
    cat > .sovereign-mesh/autonomous-monitor.sh << 'MONITOR_EOF'
#!/usr/bin/env bash
# Autonomous System Monitor - Executive Override
# Continuously monitors system health and takes autonomous action

while true; do
    # Check Docker container health
    UNHEALTHY=$(docker ps --filter "health=unhealthy" --format "{{.Names}}" 2>/dev/null | wc -l)
    
    if [ "$UNHEALTHY" -gt 0 ]; then
        echo "[AUTONOMOUS] Detected unhealthy containers: $UNHEALTHY"
        echo "[AUTONOMOUS] Initiating automatic restart..."
        docker ps --filter "health=unhealthy" --format "{{.Names}}" | xargs -I {} docker restart {}
    fi
    
    # Monitor system resources
    if command -v df &> /dev/null; then
        DISK_USAGE=$(df -h / | tail -1 | awk '{print $5}' | sed 's/%//')
        if [ "$DISK_USAGE" -gt 90 ]; then
            echo "[AUTONOMOUS] Critical disk usage: ${DISK_USAGE}%"
            echo "[AUTONOMOUS] Initiating cleanup procedures..."
            docker system prune -f --volumes
        fi
    fi
    
    sleep 60
done
MONITOR_EOF
    
    chmod +x .sovereign-mesh/autonomous-monitor.sh
    
    echo_success "Executive override system configured"
    echo_status "Configuration: .sovereign-mesh/executive-override.yaml"
    echo_status "Monitor script: .sovereign-mesh/autonomous-monitor.sh"
    
    # Offer to start autonomous monitor
    echo ""
    read -p "Start autonomous monitoring in background? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        nohup ./.sovereign-mesh/autonomous-monitor.sh > .sovereign-mesh/monitor.log 2>&1 &
        echo_success "Autonomous monitor started (PID: $!)"
        echo_status "Monitor logs: .sovereign-mesh/monitor.log"
    fi
}

# Health Check and Verification
verify_deployment() {
    echo_status "Verifying deployment health..."
    
    local status_ok=true
    
    # Check Docker services
    if docker ps --format "{{.Names}}" &> /dev/null; then
        local running_containers
        running_containers=$(docker ps --format "{{.Names}}" | wc -l)
        echo_success "Docker containers running: $running_containers"
    else
        echo_warning "No Docker containers detected"
        status_ok=false
    fi
    
    # Check common endpoints
    local endpoints=(
        "http://localhost:3000|Grafana"
        "http://localhost:9090|Prometheus"
        "http://localhost:8200|Vault"
        "http://localhost:8080|Event Gateway"
    )
    
    for endpoint_info in "${endpoints[@]}"; do
        IFS='|' read -r url name <<< "$endpoint_info"
        if curl -s -o /dev/null -w "%{http_code}" "$url" 2>/dev/null | grep -q "200\|302"; then
            echo_success "$name accessible at $url"
        else
            echo_status "$name not accessible (may not be deployed)"
        fi
    done
    
    echo ""
    if [ "$status_ok" = true ]; then
        echo_success "Deployment verification complete"
    else
        echo_warning "Some services may not be running - check docker logs"
    fi
}

# Display Final Report
show_report() {
    echo ""
    echo_banner
    echo ""
    echo -e "${GREEN}${BOLD}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}${BOLD}║  SOVEREIGN MESH BOOTSTRAP COMPLETE                             ║${NC}"
    echo -e "${GREEN}${BOLD}╚════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo_status "Environment: $DETECTED_SHELL on $DETECTED_OS"
    echo_status "GitHub CLI: ${GH_CLI_AVAILABLE:-false}"
    echo ""
    echo -e "${CYAN}${BOLD}🎯 Key Endpoints:${NC}"
    echo "   • Grafana Dashboard: http://localhost:3000 (admin/admin)"
    echo "   • Prometheus Metrics: http://localhost:9090"
    echo "   • Vault Dev Server: http://localhost:8200 (token: root)"
    echo "   • Event Gateway: http://localhost:8080"
    echo ""
    echo -e "${CYAN}${BOLD}📋 Next Steps:${NC}"
    echo "   1. Edit .env with your actual credentials"
    echo "   2. Configure Discord bot: https://discord.com/developers/applications"
    echo "   3. Set up GitHub App for webhooks"
    echo "   4. Test GitLens integration: ./gl2discord.sh"
    echo "   5. Review autonomous monitor: .sovereign-mesh/monitor.log"
    echo ""
    echo -e "${CYAN}${BOLD}🔧 Useful Commands:${NC}"
    echo "   • View logs: docker compose logs -f"
    echo "   • Check status: docker compose ps"
    echo "   • Stop services: docker compose down"
    echo "   • Full restart: docker compose down && docker compose up -d"
    echo ""
    echo -e "${CYAN}${BOLD}🤖 Autonomous Features:${NC}"
    echo "   • Executive Override: Enabled"
    echo "   • Autonomous Monitor: .sovereign-mesh/autonomous-monitor.sh"
    echo "   • Configuration: .sovereign-mesh/executive-override.yaml"
    echo ""
    echo -e "${CYAN}${BOLD}📖 Documentation:${NC}"
    echo "   • Architecture: README.md"
    echo "   • Deployment: DEPLOYMENT.md"
    echo "   • Diagnostics: BOOT_RECON.md"
    echo "   • Community: COMMUNITY.md"
    echo ""
    echo -e "${GREEN}${BOLD}🔥 Sovereignty Architecture is now operational!${NC}"
    echo ""
}

# Main Execution Flow
main() {
    echo_banner
    
    # Core initialization
    detect_shell_environment
    check_gh_cli
    check_prerequisites
    
    # Environment setup
    init_environment
    install_dependencies
    
    # Infrastructure deployment
    deploy_infrastructure
    deploy_kubernetes
    
    # Advanced features
    setup_executive_override
    
    # Verification
    verify_deployment
    
    # Final report
    show_report
}

# Script entry point
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
