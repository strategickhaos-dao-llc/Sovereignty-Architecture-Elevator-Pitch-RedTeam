#!/bin/bash
#
# configure-webhooks.sh
# 
# Points all repository webhooks to the Queen.js Federation Hub.
# This script uses the GitHub CLI (gh) to configure webhooks.
#
# Prerequisites:
# - GitHub CLI (gh) installed and authenticated
# - GITHUB_TOKEN or gh auth login completed
# - QUEEN_URL environment variable set
#
# Usage:
#   ./configure-webhooks.sh
#
# Or with custom Queen URL:
#   QUEEN_URL="https://queen.yourdomain.com" ./configure-webhooks.sh
#

set -euo pipefail

# Configuration
QUEEN_URL="${QUEEN_URL:-https://queen.strategickhaos.com/webhook/github}"
WEBHOOK_SECRET="${WEBHOOK_SECRET:-}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warn() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check prerequisites
check_prerequisites() {
    echo "🔍 Checking prerequisites..."
    
    if ! command -v gh &> /dev/null; then
        log_error "GitHub CLI (gh) is not installed. Please install it first."
        echo "  → https://cli.github.com/manual/installation"
        exit 1
    fi
    
    if ! gh auth status &> /dev/null; then
        log_error "GitHub CLI is not authenticated. Please run: gh auth login"
        exit 1
    fi
    
    if [ -z "$WEBHOOK_SECRET" ]; then
        log_warn "WEBHOOK_SECRET is not set. Webhooks will be created without signature verification."
        echo "  → For production, set WEBHOOK_SECRET environment variable"
    fi
    
    log_info "All prerequisites met"
}

# Add webhook to a repository
add_webhook() {
    local org=$1
    local repo=$2
    
    echo "📡 Adding webhook for $org/$repo..."
    
    # Build webhook config
    local config_url="$QUEEN_URL"
    local events='["push","pull_request","issues","check_suite","deployment"]'
    
    # Check if webhook already exists
    existing=$(gh api "/repos/$org/$repo/hooks" --jq '.[] | select(.config.url == "'"$config_url"'") | .id' 2>/dev/null || echo "")
    
    if [ -n "$existing" ]; then
        log_warn "Webhook already exists for $org/$repo (ID: $existing)"
        echo "  → Updating existing webhook..."
        
        # Update existing webhook
        if [ -n "$WEBHOOK_SECRET" ]; then
            gh api --method PATCH "/repos/$org/$repo/hooks/$existing" \
                -f "config[url]=$config_url" \
                -f "config[content_type]=json" \
                -f "config[secret]=$WEBHOOK_SECRET" \
                -F "config[insecure_ssl]=0" \
                --silent
        else
            gh api --method PATCH "/repos/$org/$repo/hooks/$existing" \
                -f "config[url]=$config_url" \
                -f "config[content_type]=json" \
                -F "config[insecure_ssl]=0" \
                --silent
        fi
        
        log_info "Updated webhook for $org/$repo"
        return 0
    fi
    
    # Create new webhook
    if [ -n "$WEBHOOK_SECRET" ]; then
        gh api --method POST "/repos/$org/$repo/hooks" \
            -f "name=web" \
            -F "active=true" \
            -f "config[url]=$config_url" \
            -f "config[content_type]=json" \
            -f "config[secret]=$WEBHOOK_SECRET" \
            -F "config[insecure_ssl]=0" \
            -f "events[]=push" \
            -f "events[]=pull_request" \
            -f "events[]=issues" \
            -f "events[]=check_suite" \
            -f "events[]=deployment" \
            --silent
    else
        gh api --method POST "/repos/$org/$repo/hooks" \
            -f "name=web" \
            -F "active=true" \
            -f "config[url]=$config_url" \
            -f "config[content_type]=json" \
            -F "config[insecure_ssl]=0" \
            -f "events[]=push" \
            -f "events[]=pull_request" \
            -f "events[]=issues" \
            -f "events[]=check_suite" \
            -f "events[]=deployment" \
            --silent
    fi
    
    log_info "Created webhook for $org/$repo"
}

# Main function
main() {
    echo "👑 Queen.js Federation Hub - Webhook Configuration"
    echo "================================================="
    echo ""
    echo "🌐 Queen URL: $QUEEN_URL"
    echo ""
    
    check_prerequisites
    
    echo ""
    echo "📋 Configuring webhooks for all organizations..."
    echo ""
    
    # Organization 1: Strategickhaos (personal/main)
    echo "🏛️ Organization: Strategickhaos"
    add_webhook "Strategickhaos" "Sovereignty-Architecture-Elevator-Pitch-" || true
    # Add more repos as needed:
    # add_webhook "Strategickhaos" "treasury-os" || true
    
    echo ""
    
    # Organization 2: Strategickhaos-Swarm-Intelligence (team/projects)
    echo "🏛️ Organization: Strategickhaos-Swarm-Intelligence"
    # add_webhook "Strategickhaos-Swarm-Intelligence" "quantum-symbolic-emulator" || true
    # add_webhook "Strategickhaos-Swarm-Intelligence" "valoryield-engine" || true
    echo "  → Add repos as they are created"
    
    echo ""
    
    # Organization 3: SNHU Enterprise (school - if applicable)
    echo "🏛️ Organization: SNHU (if applicable)"
    echo "  → Add repos if you have SNHU GitHub access"
    # add_webhook "SNHU-YourUsername" "class-project-repo" || true
    
    echo ""
    echo "================================================="
    echo "👑 Webhook configuration complete!"
    echo ""
    echo "🔧 To test webhooks:"
    echo "   curl -X POST $QUEEN_URL/health"
    echo ""
    echo "📚 Documentation:"
    echo "   See FEDERATION_ARCHITECTURE.md for architecture details"
}

# Run main function
main "$@"
