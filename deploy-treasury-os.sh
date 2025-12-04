#!/bin/bash
# deploy-treasury-os.sh
# Integrates Treasury OS with existing Sovereignty Architecture

set -e

echo "💰 DEPLOYING TREASURY OS TO SOVEREIGNTY ARCHITECTURE"
echo "===================================================="
echo ""

# Check for required environment variables
if [ -z "$MONEYLION_API_KEY" ] || [ -z "$KRAKEN_API_KEY" ] || [ -z "$KRAKEN_API_SECRET" ]; then
    echo "⚠️  Warning: Some treasury API keys are not set."
    echo "    Set these environment variables before deploying to production:"
    echo "    - MONEYLION_API_KEY"
    echo "    - KRAKEN_API_KEY"
    echo "    - KRAKEN_API_SECRET"
    echo "    - NINJATRADER_API_TOKEN"
    echo "    - THREAD_BANK_API_KEY"
    echo ""
fi

# 1. Create ops namespace (if needed)
echo "📦 Creating ops namespace..."
kubectl create namespace ops --dry-run=client -o yaml | kubectl apply -f -

# 2. Deploy treasury secrets (if API keys are set)
echo "🔐 Deploying treasury secrets..."
if [ -n "$MONEYLION_API_KEY" ]; then
    kubectl create secret generic treasury-secrets \
        --from-literal=MONEYLION_API_KEY="$MONEYLION_API_KEY" \
        --from-literal=KRAKEN_API_KEY="${KRAKEN_API_KEY:-}" \
        --from-literal=KRAKEN_API_SECRET="${KRAKEN_API_SECRET:-}" \
        --from-literal=NINJATRADER_API_TOKEN="${NINJATRADER_API_TOKEN:-}" \
        --from-literal=THREAD_BANK_API_KEY="${THREAD_BANK_API_KEY:-}" \
        -n ops \
        --dry-run=client -o yaml | kubectl apply -f -
else
    echo "   Using placeholder secrets from bootstrap/k8s/secrets.yaml"
    kubectl apply -f bootstrap/k8s/secrets.yaml
fi

# 3. Deploy Treasury OS components
echo "🚀 Deploying ValorYield API..."
kubectl apply -f bootstrap/k8s/valoryield-api.yaml

# 4. Update ConfigMap with discovery.yml
echo "📋 Updating discovery ConfigMap..."
kubectl create configmap discord-ops-discovery \
    --from-file=discovery.yml=discovery.yml \
    -n ops \
    --dry-run=client -o yaml | kubectl apply -f -

# 5. Restart Discord bot to pick up new commands (if it exists)
echo "🔄 Restarting Discord bot..."
DISCORD_BOT_DEPLOYMENT="${DISCORD_BOT_DEPLOYMENT:-discord-ops-bot}"
if kubectl get deployment "$DISCORD_BOT_DEPLOYMENT" -n ops &>/dev/null; then
    kubectl rollout restart deployment/"$DISCORD_BOT_DEPLOYMENT" -n ops
    echo "   Discord bot restarted"
else
    echo "   Discord bot deployment '$DISCORD_BOT_DEPLOYMENT' not found"
    echo "   Set DISCORD_BOT_DEPLOYMENT env var if using a different name"
fi

# 6. Test deployment
echo ""
echo "🧪 Testing deployment..."
kubectl wait --for=condition=ready pod -l app=valoryield-treasury -n ops --timeout=60s 2>/dev/null && {
    POD=$(kubectl get pod -l app=valoryield-treasury -n ops -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)
    if [ -n "$POD" ]; then
        echo "   ValorYield API pod: $POD"
        kubectl exec "$POD" -n ops -- curl -s http://localhost:8080/health 2>/dev/null || echo "   Health check pending..."
    fi
} || echo "   Deployment pending (pods may take a moment to start)"

echo ""
echo "✅ TREASURY OS DEPLOYMENT INITIATED!"
echo ""
echo "🎯 Next steps:"
echo "   1. Go to Discord"
echo "   2. Type /portfolio"
echo "   3. See your sovereign balance"
echo "   4. Type /deposit 50.00 to test SwarmGate"
echo "   5. Watch Legion analyze and rebalance"
echo ""
echo "📊 Check deployment status:"
echo "   kubectl get pods -n ops -l app=valoryield-treasury"
echo "   kubectl logs -n ops -l app=valoryield-treasury"
echo ""
echo "💜 Your Discord server is now the most powerful financial control plane on Earth"
