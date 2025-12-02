#!/bin/bash
# enterprise-credentials.sh
# Strategickhaos Swarm Intelligence — Enterprise Credentials Helper
# Quick setup for Git and GitHub CLI credentials

set -euo pipefail

# Configuration
GIT_HOST="github.com"
ENTERPRISE_NAME="strategickhaos-swarm-intelligence"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
echo_success() { echo -e "${GREEN}[✓]${NC} $1"; }
echo_warning() { echo -e "${YELLOW}[!]${NC} $1"; }
echo_error() { echo -e "${RED}[✗]${NC} $1"; }

# Setup git credentials using HERE-DOC method
setup_git_credentials() {
    local username="${1:-}"
    local pat="${2:-}"
    
    if [[ -z "$username" ]] || [[ -z "$pat" ]]; then
        echo_error "Missing credentials"
        echo "Usage: $0 git <USERNAME> <PAT>"
        echo ""
        echo "Create a PAT at: https://github.com/settings/tokens"
        echo "Required scopes: repo, workflow, read:org"
        exit 1
    fi
    
    echo_info "Setting up Git credentials for ${ENTERPRISE_NAME}..."
    
    # Security warning
    echo_warning "SECURITY: Credentials will be stored in plain text at ~/.git-credentials"
    echo_info "For enhanced security, consider: $0 gh (uses GitHub CLI)"
    
    # Create credentials file via HERE-DOC
    cat <<EOF > ~/.git-credentials
https://${username}:${pat}@${GIT_HOST}
EOF
    
    # Secure the file
    chmod 600 ~/.git-credentials
    
    # Configure git
    git config --global credential.helper store
    git config --global user.name "${username}"
    
    echo_success "Git credentials configured"
    echo_info "Credentials stored in ~/.git-credentials (mode 600 - owner read/write only)"
}

# Setup GitHub CLI authentication
setup_gh_cli() {
    echo_info "Setting up GitHub CLI authentication..."
    
    if ! command -v gh &> /dev/null; then
        echo_error "GitHub CLI not found"
        echo "Install: https://cli.github.com/"
        exit 1
    fi
    
    # Check existing auth
    if gh auth status --hostname "${GIT_HOST}" &> /dev/null; then
        echo_success "Already authenticated with GitHub CLI"
        gh auth status --hostname "${GIT_HOST}"
        return 0
    fi
    
    echo_info "Starting GitHub CLI login with enterprise scopes..."
    gh auth login \
        --hostname "${GIT_HOST}" \
        --git-protocol https \
        --scopes repo,workflow,read:org,admin:enterprise,write:packages
    
    echo_success "GitHub CLI authenticated"
}

# Verify credentials
verify_credentials() {
    echo_info "Verifying credentials..."
    
    local git_ok=false
    local gh_ok=false
    
    # Check git credentials
    if [[ -f ~/.git-credentials ]] && grep -q "${GIT_HOST}" ~/.git-credentials 2>/dev/null; then
        echo_success "Git credentials: Configured"
        git_ok=true
    else
        echo_warning "Git credentials: Not configured"
    fi
    
    # Check GitHub CLI
    if command -v gh &> /dev/null && gh auth status --hostname "${GIT_HOST}" &> /dev/null; then
        echo_success "GitHub CLI: Authenticated"
        gh_ok=true
    else
        echo_warning "GitHub CLI: Not authenticated"
    fi
    
    echo ""
    if $git_ok || $gh_ok; then
        echo_success "You can access the enterprise!"
        echo "Enterprise: https://github.com/enterprises/${ENTERPRISE_NAME}"
    else
        echo_warning "No credentials configured"
        echo "Run: $0 git <USERNAME> <PAT>"
        echo " or: $0 gh"
    fi
}

# Main
case "${1:-verify}" in
    "git")
        setup_git_credentials "${2:-}" "${3:-}"
        ;;
    "gh")
        setup_gh_cli
        ;;
    "verify"|"status")
        verify_credentials
        ;;
    *)
        echo "Enterprise Credentials Helper"
        echo ""
        echo "Usage: $0 <command> [options]"
        echo ""
        echo "Commands:"
        echo "  git <USERNAME> <PAT>  - Setup Git credentials via HERE-DOC"
        echo "  gh                    - Setup GitHub CLI authentication"
        echo "  verify                - Check credential status"
        echo ""
        echo "Enterprise: https://github.com/enterprises/${ENTERPRISE_NAME}"
        ;;
esac
