#!/bin/bash
# Strategickhaos Discord DevOps Control Plane Bootstrap Script
set -euo pipefail

NAMESPACE="${NAMESPACE:-ops}"
KUBECTL="${KUBECTL:-kubectl}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

echo_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

echo_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

echo_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    echo_info "Checking prerequisites..."
    
    if ! command -v kubectl &> /dev/null; then
        echo_error "kubectl is required but not installed"
        exit 1
    fi
    
    if ! command -v jq &> /dev/null; then
        echo_warning "jq not found - some features may not work properly"
    fi
    
    # Check cluster connectivity
    if ! $KUBECTL cluster-info &> /dev/null; then
        echo_error "Cannot connect to Kubernetes cluster"
        exit 1
    fi
    
    echo_success "Prerequisites check passed"
}

# Create namespace
create_namespace() {
    echo_info "Creating namespace: $NAMESPACE"
    
    if $KUBECTL get namespace "$NAMESPACE" &> /dev/null; then
        echo_warning "Namespace $NAMESPACE already exists"
    else
        $KUBECTL create namespace "$NAMESPACE"
        $KUBECTL label namespace "$NAMESPACE" name="$NAMESPACE"
        echo_success "Namespace $NAMESPACE created"
    fi
}

# Apply Kubernetes manifests
apply_manifests() {
    echo_info "Applying Kubernetes manifests..."
    
    local manifests=(
        "rbac.yaml"
        "secrets.yaml"
        "configmap.yaml"
        "bot-deployment.yaml"
        "gateway-deployment.yaml"
        "email-intelligence-deployment.yaml"
        "ingress.yaml"
    )
    
    for manifest in "${manifests[@]}"; do
        if [[ -f "k8s/$manifest" ]]; then
            echo_info "Applying $manifest..."
            $KUBECTL apply -f "k8s/$manifest" -n "$NAMESPACE"
            echo_success "$manifest applied"
        else
            echo_warning "Manifest $manifest not found, skipping"
        fi
    done
}

# Wait for deployments
wait_for_deployments() {
    echo_info "Waiting for deployments to be ready..."
    
    local deployments=("discord-ops-bot" "event-gateway" "email-intelligence")
    
    for deployment in "${deployments[@]}"; do
        echo_info "Waiting for $deployment..."
        if $KUBECTL get deployment "$deployment" -n "$NAMESPACE" &> /dev/null; then
            $KUBECTL wait --for=condition=available --timeout=300s deployment/"$deployment" -n "$NAMESPACE"
            echo_success "$deployment is ready"
        else
            echo_warning "Deployment $deployment not found"
        fi
    done
}

# Verify installation
verify_installation() {
    echo_info "Verifying installation..."
    
    echo_info "Checking pod status..."
    $KUBECTL get pods -n "$NAMESPACE" -l app=strategickhaos-discord-ops
    
    echo_info "Checking services..."
    $KUBECTL get services -n "$NAMESPACE" -l app=strategickhaos-discord-ops
    
    echo_info "Checking ingress..."
    $KUBECTL get ingress -n "$NAMESPACE" strategickhaos-events || echo_warning "Ingress not found"
    
    # Check if pods are running
    local running_pods
    running_pods=$($KUBECTL get pods -n "$NAMESPACE" -l app=strategickhaos-discord-ops --field-selector=status.phase=Running --no-headers | wc -l)
    
    if [[ $running_pods -gt 0 ]]; then
        echo_success "Installation verification passed - $running_pods pods running"
    else
        echo_error "No running pods found - check logs for issues"
        return 1
    fi
}

# Generate configuration templates
generate_config_templates() {
    echo_info "Generating configuration templates..."
    
    cat > discord-bot-env.template << 'EOF'
# Discord Bot Configuration Template
# Copy to .env and fill in real values

# Discord Bot Token (from Discord Developer Portal)
DISCORD_BOT_TOKEN=your_bot_token_here

# Discord Guild (Server) ID
DISCORD_GUILD_ID=your_discord_server_id

# Channel IDs (right-click channel in Discord, copy ID)
PRS_CHANNEL=channel_id_for_prs
DEV_FEED_CHANNEL=channel_id_for_dev_feed

# GitHub App Configuration
GITHUB_APP_ID=your_github_app_id
GITHUB_APP_WEBHOOK_SECRET=your_webhook_secret
GITHUB_APP_PRIVATE_KEY_PATH=/path/to/private-key.pem

# OpenAI API Key
OPENAI_API_KEY=sk-your-openai-api-key

# PostgreSQL Vector Database
PGVECTOR_CONN=postgresql://user:pass@host:5432/db

# HMAC Key for webhook verification (generate with: openssl rand -hex 32)
EVENTS_HMAC_KEY=your_64_character_hmac_key_here
EOF

    cat > github-app-manifest.json << 'EOF'
{
  "name": "Strategickhaos Discord DevOps",
  "url": "https://github.com/Strategickhaos-Swarm-Intelligence",
  "hook_attributes": {
    "url": "https://events.strategickhaos.com/git"
  },
  "redirect_url": "https://events.strategickhaos.com/auth/callback",
  "description": "Discord-based DevOps automation for Strategickhaos infrastructure",
  "public": false,
  "default_events": [
    "pull_request",
    "push",
    "check_suite",
    "issue_comment",
    "release"
  ],
  "default_permissions": {
    "contents": "read",
    "metadata": "read",
    "pull_requests": "write",
    "checks": "write"
  }
}
EOF

    echo_success "Configuration templates generated:"
    echo "  - discord-bot-env.template"
    echo "  - github-app-manifest.json"
}

# Show next steps
show_next_steps() {
    echo_info "🚀 Strategickhaos Discord DevOps Control Plane Bootstrap Complete!"
    echo
    echo "Next steps:"
    echo "1. Configure secrets in k8s/secrets.yaml with real values"
    echo "2. Create Discord bot at https://discord.com/developers/applications"
    echo "3. Create GitHub App using github-app-manifest.json"
    echo "4. Set up DNS for events.strategickhaos.com -> your ingress"
    echo "5. Configure Discord channels and permissions"
    echo "6. Test integration with: ./gl2discord.sh \"\$PRS_CHANNEL\" \"Test\" \"Bootstrap complete!\""
    echo
    echo "Useful commands:"
    echo "  - View logs: kubectl logs -f deployment/discord-ops-bot -n $NAMESPACE"
    echo "  - Check status: kubectl get all -n $NAMESPACE"
    echo "  - Update config: kubectl patch configmap discord-ops-discovery -n $NAMESPACE --patch-file new-config.yaml"
    echo
    echo "Documentation: https://github.com/Strategickhaos-Swarm-Intelligence/sovereignty-architecture"
}

# Main execution
main() {
    echo_info "🔥 Strategickhaos Discord DevOps Control Plane Bootstrap"
    echo_info "Deploying sovereign architecture to Kubernetes..."
    echo
    
    check_prerequisites
    create_namespace
    apply_manifests
    wait_for_deployments
    verify_installation
    generate_config_templates
    show_next_steps
    
    echo_success "Bootstrap complete! 🎉"
}

# Handle script arguments
case "${1:-deploy}" in
    "deploy")
        main
        ;;
    "verify")
        verify_installation
        ;;
    "clean")
        echo_warning "Cleaning up Strategickhaos Discord DevOps deployment..."
        $KUBECTL delete namespace "$NAMESPACE" --ignore-not-found=true
        echo_success "Cleanup complete"
        ;;
    *)
        echo "Usage: $0 [deploy|verify|clean]"
        echo "  deploy  - Deploy the complete control plane (default)"
        echo "  verify  - Verify existing deployment"
        echo "  clean   - Remove all deployed resources"
        exit 1
        ;;
esac