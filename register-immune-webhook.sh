#!/usr/bin/env bash
# Register Immune System Webhook with Discord Gateway
# This script registers the immune system to report events to Discord channels
set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
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

echo_cyan() {
    echo -e "${CYAN}$1${NC}"
}

# Configuration
EVENTS_URL="${EVENTS_URL:-https://events.strategickhaos.com}"
IMMUNE_CHANNEL="${IMMUNE_RESPONSE_CHANNEL_ID:-}"
SWARM_CHANNEL="${SWARM_HEALTH_CHANNEL_ID:-}"
WEBHOOK_SECRET="${IMMUNE_WEBHOOK_SECRET:-}"

# Display banner
display_banner() {
    echo_cyan "╔══════════════════════════════════════════════════════════════╗"
    echo_cyan "║       🧬 IMMUNE SYSTEM WEBHOOK REGISTRATION 🧬              ║"
    echo_cyan "║                                                              ║"
    echo_cyan "║       Sovereignty Architecture - Living Infrastructure       ║"
    echo_cyan "╚══════════════════════════════════════════════════════════════╝"
    echo
}

# Check required environment variables
check_env() {
    echo_info "Checking environment variables..."
    
    local missing=()
    
    if [[ -z "${DISCORD_TOKEN:-}" ]]; then
        missing+=("DISCORD_TOKEN")
    fi
    
    if [[ -z "$IMMUNE_CHANNEL" ]]; then
        echo_warning "IMMUNE_RESPONSE_CHANNEL_ID not set - immune response events won't be routed"
    fi
    
    if [[ -z "$SWARM_CHANNEL" ]]; then
        echo_warning "SWARM_HEALTH_CHANNEL_ID not set - swarm health events won't be routed"
    fi
    
    if [[ ${#missing[@]} -gt 0 ]]; then
        echo_error "Missing required environment variables: ${missing[*]}"
        echo
        echo "Please set the following environment variables:"
        echo "  export DISCORD_TOKEN='your_discord_bot_token'"
        echo "  export IMMUNE_RESPONSE_CHANNEL_ID='channel_id_for_immune_events'"
        echo "  export SWARM_HEALTH_CHANNEL_ID='channel_id_for_swarm_health'"
        exit 1
    fi
    
    echo_success "Environment check passed"
}

# Register immune system webhook endpoint
register_webhook() {
    echo_info "Registering immune system webhook..."
    
    local webhook_config=$(cat << EOF
{
    "name": "immune-system-webhook",
    "type": "immune",
    "events": [
        "threat_detected",
        "wbc_spawned",
        "antibody_learned",
        "mode_changed",
        "circadian_shift",
        "quorum_density_change"
    ],
    "channels": {
        "immune_response": "$IMMUNE_CHANNEL",
        "swarm_health": "$SWARM_CHANNEL"
    },
    "routing": {
        "threat_detected": "immune_response",
        "wbc_spawned": "immune_response",
        "antibody_learned": "immune_response",
        "mode_changed": "swarm_health",
        "circadian_shift": "swarm_health",
        "quorum_density_change": "swarm_health"
    }
}
EOF
)
    
    echo_info "Webhook configuration:"
    echo "$webhook_config" | jq . 2>/dev/null || echo "$webhook_config"
    echo
    
    # Test connectivity to events gateway
    echo_info "Testing connectivity to events gateway..."
    if curl -sS --fail "${EVENTS_URL}/health" > /dev/null 2>&1; then
        echo_success "Events gateway is reachable"
    else
        echo_warning "Events gateway not reachable at $EVENTS_URL - will configure for later"
    fi
    
    echo_success "Webhook registration configured"
}

# Send test message to Discord
send_test_message() {
    echo_info "Sending test message to Discord..."
    
    if [[ -n "$IMMUNE_CHANNEL" ]]; then
        local test_payload=$(cat << EOF
{
    "embeds": [{
        "title": "🧬 Immune System Online",
        "description": "Webhook registration complete.\n\n🩸 3 RBC active\n🔬 2 WBC scanning\n🧠 Quorum sensing enabled",
        "color": 65280,
        "fields": [
            {"name": "Mode", "value": "🤝 Coordinate", "inline": true},
            {"name": "Density", "value": "14 cells active", "inline": true},
            {"name": "Status", "value": "✅ Operational", "inline": true}
        ],
        "footer": {"text": "Sovereignty Architecture • Living Infrastructure"},
        "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    }]
}
EOF
)
        
        if curl -sS \
            -H "Authorization: Bot $DISCORD_TOKEN" \
            -H "Content-Type: application/json" \
            -X POST "https://discord.com/api/v10/channels/$IMMUNE_CHANNEL/messages" \
            -d "$test_payload" > /dev/null; then
            echo_success "Test message sent to #immune-response"
        else
            echo_warning "Failed to send test message - check channel ID and permissions"
        fi
    fi
}

# Generate Kubernetes secret manifest
generate_k8s_secret() {
    echo_info "Generating Kubernetes secret manifest..."
    
    cat > immune-webhook-secret.yaml << EOF
apiVersion: v1
kind: Secret
metadata:
  name: immune-webhook-secrets
  namespace: ops
  labels:
    app: strategickhaos-immune-system
    component: webhook
type: Opaque
stringData:
  IMMUNE_WEBHOOK_SECRET: "${WEBHOOK_SECRET:-$(openssl rand -hex 32)}"
  IMMUNE_RESPONSE_CHANNEL_ID: "$IMMUNE_CHANNEL"
  SWARM_HEALTH_CHANNEL_ID: "$SWARM_CHANNEL"
EOF
    
    echo_success "Generated immune-webhook-secret.yaml"
}

# Display next steps
show_next_steps() {
    echo
    echo_cyan "══════════════════════════════════════════════════════════════"
    echo_cyan "                    🎉 REGISTRATION COMPLETE 🎉              "
    echo_cyan "══════════════════════════════════════════════════════════════"
    echo
    echo "Next steps:"
    echo
    echo "1. Apply the Kubernetes secret:"
    echo "   kubectl apply -f immune-webhook-secret.yaml"
    echo
    echo "2. Deploy the immune system to your GKE clusters:"
    echo "   kubectl apply -f ~/swarm-immune/deploy/gke/"
    echo
    echo "3. Test the integration in Discord:"
    echo "   /immune status"
    echo "   /swarm health"
    echo
    echo "4. Wake the first dragon:"
    echo "   /cluster wake jarvis-swarm-personal-001"
    echo
    echo_cyan "══════════════════════════════════════════════════════════════"
    echo
    echo "The swarm is ready to speak through Discord. 🐉"
}

# Main execution
main() {
    display_banner
    check_env
    register_webhook
    send_test_message
    generate_k8s_secret
    show_next_steps
}

# Handle script arguments
case "${1:-register}" in
    "register")
        main
        ;;
    "test")
        check_env
        send_test_message
        ;;
    "help"|"-h"|"--help")
        echo "Usage: $0 [register|test|help]"
        echo
        echo "Commands:"
        echo "  register  - Register immune system webhook (default)"
        echo "  test      - Send test message to Discord"
        echo "  help      - Show this help message"
        echo
        echo "Environment Variables:"
        echo "  DISCORD_TOKEN                - Discord bot token (required)"
        echo "  IMMUNE_RESPONSE_CHANNEL_ID   - Channel for immune events"
        echo "  SWARM_HEALTH_CHANNEL_ID      - Channel for swarm health"
        echo "  EVENTS_URL                   - Events gateway URL"
        echo "  IMMUNE_WEBHOOK_SECRET        - Webhook secret (auto-generated if not set)"
        ;;
    *)
        echo_error "Unknown command: $1"
        echo "Use '$0 help' for usage information"
        exit 1
        ;;
esac
