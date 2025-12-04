#!/bin/bash
# deploy-treasury-os.sh
# Integrates Treasury OS with existing Sovereignty Architecture
# 
# Prerequisites:
#   - kubectl configured with cluster access
#   - Docker registry access (ghcr.io or local)
#   - Treasury API secrets set as environment variables

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NAMESPACE="${NAMESPACE:-ops}"

echo "💰 DEPLOYING TREASURY OS TO SOVEREIGNTY ARCHITECTURE"
echo "===================================================="
echo ""
echo "Namespace: $NAMESPACE"
echo ""

# Function to check if required env vars are set
check_env_vars() {
    local missing=0
    for var in "$@"; do
        if [[ -z "${!var}" ]]; then
            echo "⚠️  Warning: $var not set (will use default/placeholder)"
        fi
    done
    return $missing
}

# Check optional environment variables
echo "📋 Checking environment variables..."
check_env_vars MONEYLION_API_KEY KRAKEN_API_KEY KRAKEN_API_SECRET NINJATRADER_API_TOKEN THREAD_BANK_API_KEY

# 1. Create namespace if needed
echo ""
echo "📦 Creating namespace $NAMESPACE..."
kubectl create namespace "$NAMESPACE" --dry-run=client -o yaml | kubectl apply -f -

# 2. Create treasury secrets (if env vars are provided)
echo ""
echo "🔐 Creating/updating treasury secrets..."
kubectl create secret generic treasury-secrets \
    --from-literal=moneylion-api-key="${MONEYLION_API_KEY:-placeholder}" \
    --from-literal=kraken-api-key="${KRAKEN_API_KEY:-placeholder}" \
    --from-literal=kraken-api-secret="${KRAKEN_API_SECRET:-placeholder}" \
    --from-literal=ninjatrader-api-token="${NINJATRADER_API_TOKEN:-placeholder}" \
    --from-literal=thread-bank-api-key="${THREAD_BANK_API_KEY:-placeholder}" \
    -n "$NAMESPACE" \
    --dry-run=client -o yaml | kubectl apply -f -

# 3. Deploy Treasury OS components
echo ""
echo "🚀 Deploying ValorYield API..."
kubectl apply -f "$SCRIPT_DIR/bootstrap/k8s/valoryield-api.yaml"

# 4. Wait for deployment
echo ""
echo "⏳ Waiting for ValorYield API deployment..."
kubectl wait --for=condition=available deployment/valoryield-api -n "$NAMESPACE" --timeout=120s || {
    echo "⚠️  Deployment not ready yet (may need image to be built first)"
    echo "   Run: docker build -t ghcr.io/strategickhaos-swarm-intelligence/valoryield-api:latest ./valoryield-engine"
    echo "   Then: docker push ghcr.io/strategickhaos-swarm-intelligence/valoryield-api:latest"
}

# 5. Restart Discord bot to pick up new commands (if deployed)
echo ""
echo "🔄 Restarting Discord bot (if deployed)..."
kubectl rollout restart deployment/discord-ops-bot -n "$NAMESPACE" 2>/dev/null || {
    echo "   Discord bot not deployed yet, skipping restart"
}

# 6. Display deployment status
echo ""
echo "📊 Deployment Status:"
echo "===================="
kubectl get pods -n "$NAMESPACE" -l app=valoryield-api
kubectl get svc -n "$NAMESPACE" -l app=valoryield-api

echo ""
echo "✅ TREASURY OS DEPLOYMENT COMPLETE!"
echo ""
echo "🎯 Next steps:"
echo "   1. Ensure ValorYield API image is built and pushed"
echo "   2. Set real API keys in treasury-secrets"
echo "   3. Test /portfolio command in Discord"
echo "   4. Test /deposit <amount> to verify SwarmGate integration"
echo "   5. Test /rebalance to verify Legion integration"
echo ""
echo "💜 Your empire is now Discord-native"
