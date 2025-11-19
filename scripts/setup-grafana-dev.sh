#!/bin/bash
# Setup Grafana Development Environment
# This script clones the Grafana repository and sets up a development environment
# for custom dashboard development and Grafana plugin creation

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
GRAFANA_DEV_DIR="${PROJECT_ROOT}/dev/grafana"

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

# Check for required tools
check_dependencies() {
    log_info "Checking dependencies..."
    
    local missing_deps=()
    
    if ! command -v git &> /dev/null; then
        missing_deps+=("git")
    fi
    
    if ! command -v gh &> /dev/null; then
        log_warn "GitHub CLI (gh) not found. Will use git clone instead."
    fi
    
    if ! command -v node &> /dev/null; then
        log_warn "Node.js not found. Required for Grafana development."
        missing_deps+=("node")
    fi
    
    if ! command -v go &> /dev/null; then
        log_warn "Go not found. Required for Grafana backend development."
        missing_deps+=("go")
    fi
    
    if [ ${#missing_deps[@]} -gt 0 ]; then
        log_error "Missing required dependencies: ${missing_deps[*]}"
        log_error "Please install them and try again."
        exit 1
    fi
}

# Clone Grafana repository
clone_grafana() {
    log_info "Setting up Grafana development repository..."
    
    # Create dev directory if it doesn't exist
    mkdir -p "$(dirname "$GRAFANA_DEV_DIR")"
    
    # Check if directory already exists
    if [ -d "$GRAFANA_DEV_DIR" ]; then
        log_warn "Grafana repository already exists at $GRAFANA_DEV_DIR"
        read -p "Do you want to update it? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            log_info "Updating existing Grafana repository..."
            cd "$GRAFANA_DEV_DIR"
            git fetch origin
            git pull origin main
        else
            log_info "Skipping clone/update"
            return 0
        fi
    else
        # Try using gh CLI first, fall back to git
        if command -v gh &> /dev/null; then
            log_info "Cloning Grafana repository using GitHub CLI..."
            gh repo clone grafana/grafana "$GRAFANA_DEV_DIR"
        else
            log_info "Cloning Grafana repository using git..."
            git clone https://github.com/grafana/grafana.git "$GRAFANA_DEV_DIR"
        fi
    fi
    
    log_info "Grafana repository ready at: $GRAFANA_DEV_DIR"
}

# Setup Grafana development environment
setup_grafana_dev() {
    log_info "Setting up Grafana development environment..."
    
    cd "$GRAFANA_DEV_DIR"
    
    # Install dependencies
    if [ -f "package.json" ]; then
        log_info "Installing Node.js dependencies..."
        npm install || yarn install || log_warn "Failed to install Node.js dependencies"
    fi
    
    # Build backend
    if [ -f "Makefile" ]; then
        log_info "Building Grafana backend..."
        make build-go || log_warn "Failed to build Go backend"
    fi
}

# Create symbolic link to custom dashboards
link_custom_dashboards() {
    log_info "Linking custom dashboards..."
    
    local custom_dashboards="${PROJECT_ROOT}/monitoring/grafana/dashboards"
    local grafana_dashboards="${GRAFANA_DEV_DIR}/public/dashboards"
    
    if [ -d "$custom_dashboards" ] && [ -d "$GRAFANA_DEV_DIR" ]; then
        mkdir -p "$grafana_dashboards"
        ln -sf "$custom_dashboards" "${grafana_dashboards}/strategickhaos" 2>/dev/null || \
            log_warn "Could not create symbolic link to custom dashboards"
        log_info "Custom dashboards linked at: ${grafana_dashboards}/strategickhaos"
    fi
}

# Print usage instructions
print_usage() {
    cat << EOF

${GREEN}Grafana Development Environment Setup Complete!${NC}

${YELLOW}Location:${NC} $GRAFANA_DEV_DIR

${YELLOW}Next Steps:${NC}

1. Start Grafana development server:
   cd $GRAFANA_DEV_DIR
   make run

2. Access Grafana at: http://localhost:3000
   Default credentials: admin/admin

3. Develop custom dashboards:
   - Create dashboards in the Grafana UI
   - Export JSON to: ${PROJECT_ROOT}/monitoring/grafana/dashboards/

4. Build custom plugins:
   cd $GRAFANA_DEV_DIR
   npx @grafana/toolkit plugin:create my-plugin

5. Connect to existing Strategickhaos stack:
   - Use datasources configured in: ${PROJECT_ROOT}/monitoring/grafana/provisioning/datasources/

${YELLOW}Documentation:${NC}
   - Grafana Plugin Development: https://grafana.com/docs/grafana/latest/developers/plugins/
   - Grafana API: https://grafana.com/docs/grafana/latest/http_api/

${YELLOW}Contributing to Grafana:${NC}
   - Follow guidelines at: https://github.com/grafana/grafana/blob/main/CONTRIBUTING.md

EOF
}

# Main execution
main() {
    log_info "Starting Grafana development environment setup..."
    
    check_dependencies
    clone_grafana
    
    # Ask if user wants to setup development environment
    read -p "Do you want to setup the development environment now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        setup_grafana_dev
        link_custom_dashboards
    fi
    
    print_usage
    
    log_info "Setup complete!"
}

main "$@"
