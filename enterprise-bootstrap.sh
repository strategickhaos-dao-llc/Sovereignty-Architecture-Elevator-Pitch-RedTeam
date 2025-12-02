#!/bin/bash
# enterprise-bootstrap.sh
# Strategickhaos Swarm Intelligence — GitHub Enterprise Bootstrap
# Purpose: Automated setup of GitHub Enterprise Cloud infrastructure
# URL: https://github.com/enterprises/strategickhaos-swarm-intelligence

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Enterprise Configuration
ENTERPRISE_NAME="strategickhaos-swarm-intelligence"
ENTERPRISE_URL="https://github.com/enterprises/${ENTERPRISE_NAME}"
DEFAULT_ORG="Strategickhaos-Swarm-Intelligence"
GIT_HOST="github.com"

echo_banner() {
    echo -e "${PURPLE}"
    cat << 'EOF'
╔══════════════════════════════════════════════════════════════════════════════╗
║            🔥 STRATEGICKHAOS SWARM INTELLIGENCE 🔥                           ║
║                GitHub Enterprise Cloud Bootstrap                              ║
║          Enterprise Control Plane — Sovereignty Architecture                  ║
╚══════════════════════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

echo_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
echo_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
echo_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
echo_error() { echo -e "${RED}[ERROR]${NC} $1"; }
echo_step() { echo -e "${CYAN}[STEP]${NC} $1"; }

# Check for required tools
check_prerequisites() {
    echo_step "Checking prerequisites..."
    
    local missing_tools=()
    
    if ! command -v git &> /dev/null; then
        missing_tools+=("git")
    fi
    
    if ! command -v gh &> /dev/null; then
        echo_warning "GitHub CLI (gh) not found - some features will use curl fallback"
    fi
    
    if ! command -v curl &> /dev/null; then
        missing_tools+=("curl")
    fi
    
    if [ ${#missing_tools[@]} -gt 0 ]; then
        echo_error "Missing required tools: ${missing_tools[*]}"
        echo_info "Install with: apt-get install ${missing_tools[*]} (or equivalent)"
        exit 1
    fi
    
    echo_success "Prerequisites check passed"
}

# Setup git credentials via HERE-DOC
setup_git_credentials() {
    local username="${1:-}"
    local pat="${2:-}"
    
    echo_step "Setting up Git credentials..."
    
    if [[ -z "$username" ]] || [[ -z "$pat" ]]; then
        echo_warning "Username or PAT not provided"
        echo_info "Usage: $0 credentials <USERNAME> <PAT>"
        echo_info ""
        echo_info "To create a PAT, go to: https://github.com/settings/tokens"
        echo_info "Required scopes: repo, workflow, read:org, admin:enterprise (optional)"
        return 1
    fi
    
    # Create credentials file via HERE-DOC
    cat <<EOF > ~/.git-credentials
https://${username}:${pat}@${GIT_HOST}
EOF
    
    chmod 600 ~/.git-credentials
    
    # Configure git credential helper
    git config --global credential.helper store
    git config --global user.name "${username}"
    
    echo_success "Git credentials configured"
    echo_info "Credentials stored in ~/.git-credentials"
}

# Authenticate with GitHub CLI (Enterprise mode)
gh_enterprise_login() {
    echo_step "Authenticating with GitHub CLI (Enterprise mode)..."
    
    if ! command -v gh &> /dev/null; then
        echo_error "GitHub CLI (gh) is required for this operation"
        echo_info "Install: https://cli.github.com/"
        return 1
    fi
    
    # Check if already authenticated
    if gh auth status --hostname "${GIT_HOST}" &> /dev/null; then
        echo_success "Already authenticated with GitHub CLI"
        gh auth status --hostname "${GIT_HOST}"
        return 0
    fi
    
    echo_info "Starting GitHub CLI authentication..."
    echo_info "This will authenticate with enterprise scopes"
    
    # GitHub CLI login with enterprise scopes
    gh auth login \
        --hostname "${GIT_HOST}" \
        --git-protocol https \
        --scopes repo,workflow,read:org,admin:enterprise,write:packages
    
    echo_success "GitHub CLI authentication complete"
}

# Mirror a repository to the enterprise
mirror_repo_to_enterprise() {
    local source_repo="${1:-}"
    local target_org="${2:-$DEFAULT_ORG}"
    local target_name="${3:-}"
    
    echo_step "Mirroring repository to enterprise..."
    
    if [[ -z "$source_repo" ]]; then
        echo_error "Source repository required"
        echo_info "Usage: $0 mirror <source_repo_url> [target_org] [target_name]"
        return 1
    fi
    
    # Extract repo name if not provided
    if [[ -z "$target_name" ]]; then
        target_name=$(basename "$source_repo" .git)
    fi
    
    local target_url="https://${GIT_HOST}/${target_org}/${target_name}.git"
    
    echo_info "Source: $source_repo"
    echo_info "Target: $target_url"
    
    # Create temporary directory for mirroring
    local temp_dir
    temp_dir=$(mktemp -d)
    
    echo_info "Cloning source repository..."
    git clone --mirror "$source_repo" "$temp_dir"
    
    cd "$temp_dir"
    
    echo_info "Pushing to enterprise..."
    git remote add enterprise "$target_url"
    git push enterprise --mirror
    
    cd - > /dev/null
    rm -rf "$temp_dir"
    
    echo_success "Repository mirrored successfully!"
    echo_info "View at: https://${GIT_HOST}/${target_org}/${target_name}"
}

# Generate enterprise configuration
generate_enterprise_config() {
    echo_step "Generating enterprise configuration..."
    
    # Generate enterprise discovery configuration via HERE-DOC
    cat <<EOF > enterprise-discovery.yml
# Strategickhaos Swarm Intelligence — Enterprise Discovery Configuration
# Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)

enterprise:
  name: "Strategickhaos Swarm Intelligence"
  url: "${ENTERPRISE_URL}"
  slug: "${ENTERPRISE_NAME}"
  tier: "GitHub Enterprise Cloud"
  
  capabilities:
    - unlimited_organizations
    - enterprise_sso
    - advanced_audit_logs
    - enterprise_runners
    - centralized_billing
    - enterprise_api
    - policy_enforcement
    - cloud_automation
    - advanced_security

organizations:
  primary:
    name: "${DEFAULT_ORG}"
    url: "https://${GIT_HOST}/${DEFAULT_ORG}"
    purpose: "Main sovereignty architecture deployment"
    
  planned:
    - name: "Strategickhaos-Infrastructure"
      purpose: "Infrastructure-as-Code repositories"
    - name: "Strategickhaos-AI-Agents"
      purpose: "AI agent and LLM safety repositories"
    - name: "Strategickhaos-Security"
      purpose: "Security tools and compliance"

settings:
  default_org: "${DEFAULT_ORG}"
  git_host: "${GIT_HOST}"
  git_protocol: "https"
  
tokens:
  required_scopes:
    - repo
    - workflow
    - read:org
    - admin:enterprise  # Optional, for enterprise management
    - write:packages    # Optional, for GitHub Packages
  
  token_url: "https://${GIT_HOST}/settings/tokens"

integrations:
  gitlens:
    host_domain: "${GIT_HOST}"
    protocol: "https"
    
  vscode:
    github_extension: true
    gitlens_extension: true
    
  gitkraken:
    host_domain: "${GIT_HOST}"
    authentication: "PAT"
    
  cloud_shell:
    gh_cli: true
    git_credentials: true

automation:
  runners:
    - type: "enterprise"
      labels: ["sovereignty", "self-hosted"]
    - type: "github-hosted"
      labels: ["ubuntu-latest"]
      
  secrets:
    level: "enterprise"
    sync: true
    
  actions:
    allowed_actions: "selected"
    patterns: ["github/*", "actions/*"]
EOF
    
    echo_success "Enterprise configuration generated: enterprise-discovery.yml"
}

# Generate PAT creation guide
generate_pat_guide() {
    echo_step "Generating PAT creation guide..."
    
    cat <<'PATEOF' > PAT_SETUP_GUIDE.md
# GitHub Personal Access Token Setup Guide

## Enterprise: Strategickhaos Swarm Intelligence

This guide helps you create a Personal Access Token (PAT) for the 
Strategickhaos Swarm Intelligence GitHub Enterprise.

## Quick Setup

### 1. Create a Fine-Grained Token (Recommended)

1. Go to: https://github.com/settings/tokens?type=beta
2. Click "Generate new token"
3. Set:
   - Token name: \`strategickhaos-enterprise\`
   - Expiration: 90 days (recommended)
   - Resource owner: Select your enterprise or organization

4. Permissions:
   - Repository access: All repositories (or select specific ones)
   - Repository permissions:
     - Contents: Read and write
     - Metadata: Read
     - Pull requests: Read and write
     - Workflows: Read and write
   - Organization permissions:
     - Members: Read
     - Administration: Read (optional)

### 2. Create a Classic Token (Alternative)

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes:
   - \`repo\` - Full control of private repositories
   - \`workflow\` - Update GitHub Action workflows
   - \`read:org\` - Read org and team membership
   - \`admin:enterprise\` - (Optional) Enterprise administration
   - \`write:packages\` - (Optional) Upload packages

4. Click "Generate token"
5. **IMPORTANT**: Copy the token immediately - you won't see it again!

## Using Your Token

### With Git Credentials (HERE-DOC method)

\`\`\`bash
cat <<EOF > ~/.git-credentials
https://YOUR_USERNAME:YOUR_TOKEN@github.com
EOF

git config --global credential.helper store
\`\`\`

### With GitHub CLI

\`\`\`bash
gh auth login \\
  --hostname github.com \\
  --git-protocol https \\
  --scopes repo,workflow,read:org
\`\`\`

### With GitKraken

1. Open GitKraken Preferences
2. Go to Integrations > GitHub
3. Enter:
   - Host Domain: \`github.com\`
   - Personal Access Token: Your token

### With VS Code

1. Open Command Palette (Ctrl+Shift+P)
2. Search "GitHub: Sign in"
3. Follow the authentication flow

## Security Best Practices

1. **Rotate tokens regularly** - Set expiration dates
2. **Use fine-grained tokens** - Limit permissions to what's needed
3. **Never commit tokens** - Use environment variables or secret managers
4. **Enable SSO** - If your enterprise uses SAML SSO, authorize the token

## Enterprise URL

- Enterprise Dashboard: https://github.com/enterprises/strategickhaos-swarm-intelligence
- Token Settings: https://github.com/settings/tokens

---
Generated for Strategickhaos Swarm Intelligence Enterprise
PATEOF
    
    echo_success "PAT guide generated: PAT_SETUP_GUIDE.md"
}

# Show enterprise status
show_enterprise_status() {
    echo_banner
    
    echo -e "${CYAN}Enterprise Information:${NC}"
    echo -e "  Name:    ${GREEN}Strategickhaos Swarm Intelligence${NC}"
    echo -e "  URL:     ${BLUE}${ENTERPRISE_URL}${NC}"
    echo -e "  Tier:    ${PURPLE}GitHub Enterprise Cloud${NC}"
    echo ""
    
    echo -e "${CYAN}Enterprise Capabilities:${NC}"
    local capabilities=(
        "✅ Unlimited organizations"
        "✅ Enterprise SSO"
        "✅ Advanced audit logs"
        "✅ Enterprise runners"
        "✅ Centralized billing"
        "✅ Enterprise API"
        "✅ Policy enforcement"
        "✅ Cloud automation"
        "✅ Advanced Security (if enabled)"
    )
    
    for cap in "${capabilities[@]}"; do
        echo -e "  ${GREEN}${cap}${NC}"
    done
    echo ""
    
    echo -e "${CYAN}Quick Commands:${NC}"
    echo -e "  ${YELLOW}Setup credentials:${NC}     $0 credentials <USERNAME> <PAT>"
    echo -e "  ${YELLOW}GitHub CLI login:${NC}      $0 gh-login"
    echo -e "  ${YELLOW}Mirror repository:${NC}     $0 mirror <source_url> [org] [name]"
    echo -e "  ${YELLOW}Generate config:${NC}       $0 config"
    echo -e "  ${YELLOW}Generate PAT guide:${NC}    $0 pat-guide"
    echo ""
}

# Display help
show_help() {
    echo_banner
    echo "Usage: $0 <command> [options]"
    echo ""
    echo "Commands:"
    echo "  status              Show enterprise status and capabilities"
    echo "  credentials         Setup git credentials via HERE-DOC"
    echo "                      Usage: $0 credentials <USERNAME> <PAT>"
    echo "  gh-login            Authenticate with GitHub CLI (enterprise mode)"
    echo "  mirror              Mirror a repository to the enterprise"
    echo "                      Usage: $0 mirror <source_url> [target_org] [target_name]"
    echo "  config              Generate enterprise configuration files"
    echo "  pat-guide           Generate PAT creation guide"
    echo "  bootstrap           Run full bootstrap (config + guides)"
    echo "  help                Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 status"
    echo "  $0 credentials myuser ghp_xxxxxxxxxxxx"
    echo "  $0 mirror https://github.com/user/repo.git"
    echo "  $0 bootstrap"
    echo ""
    echo "Enterprise URL: ${ENTERPRISE_URL}"
}

# Full bootstrap
full_bootstrap() {
    echo_banner
    echo_info "Starting full enterprise bootstrap..."
    echo ""
    
    check_prerequisites
    generate_enterprise_config
    generate_pat_guide
    
    echo ""
    echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║           ENTERPRISE BOOTSTRAP COMPLETE ✅                   ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo_info "Generated files:"
    echo "  - enterprise-discovery.yml (Enterprise configuration)"
    echo "  - PAT_SETUP_GUIDE.md (Token creation guide)"
    echo ""
    echo_info "Next steps:"
    echo "  1. Create a PAT: https://github.com/settings/tokens"
    echo "  2. Run: $0 credentials <USERNAME> <PAT>"
    echo "  3. Run: $0 gh-login"
    echo "  4. Mirror repos: $0 mirror <source_url>"
    echo ""
}

# Main execution
main() {
    local command="${1:-status}"
    
    case "$command" in
        "status")
            show_enterprise_status
            ;;
        "credentials")
            setup_git_credentials "${2:-}" "${3:-}"
            ;;
        "gh-login")
            gh_enterprise_login
            ;;
        "mirror")
            mirror_repo_to_enterprise "${2:-}" "${3:-}" "${4:-}"
            ;;
        "config")
            check_prerequisites
            generate_enterprise_config
            ;;
        "pat-guide")
            generate_pat_guide
            ;;
        "bootstrap")
            full_bootstrap
            ;;
        "help"|"--help"|"-h")
            show_help
            ;;
        *)
            echo_error "Unknown command: $command"
            show_help
            exit 1
            ;;
    esac
}

main "$@"
