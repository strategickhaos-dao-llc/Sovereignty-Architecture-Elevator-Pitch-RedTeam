#!/usr/bin/env bash
# Deploy GitLens Aggregator and Mind OS Orchestrator with LLM Generals
set -euo pipefail

echo "🚀 Deploying GitLens to Mind OS Distribution System"
echo "=================================================="

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl not found. Please install kubectl first."
    exit 1
fi

# Function to check deployment status
check_deployment() {
    local namespace=$1
    local deployment=$2
    echo "⏳ Waiting for $deployment to be ready..."
    kubectl rollout status deployment/$deployment -n $namespace --timeout=300s
}

# Create namespaces
echo "📦 Creating namespaces..."
kubectl apply -f - <<EOF
apiVersion: v1
kind: Namespace
metadata:
  name: ops
  labels:
    name: ops
---
apiVersion: v1
kind: Namespace
metadata:
  name: agents
  labels:
    name: agents
EOF

# Deploy LLM Generals
echo "🤖 Deploying LLM Generals..."
kubectl apply -f bootstrap/k8s/llm-generals-deployment.yaml

# Deploy GitLens Aggregator and Mind OS
echo "🧠 Deploying GitLens Aggregator and Mind OS Orchestrator..."
kubectl apply -f bootstrap/k8s/gitlens-mindos-deployment.yaml

# Wait for deployments
echo ""
echo "⏳ Checking deployment status..."
check_deployment ops gitlens-aggregator
check_deployment ops mindos-orchestrator

# Check LLM Generals in agents namespace
echo ""
echo "🤖 Checking LLM Generals status..."
kubectl get deployments -n agents

# Display service endpoints
echo ""
echo "📊 Service Endpoints:"
echo "===================="
kubectl get services -n ops | grep -E "gitlens|mindos"
kubectl get services -n agents | grep general

# Display pod status
echo ""
echo "🔍 Pod Status:"
echo "=============="
kubectl get pods -n ops | grep -E "gitlens|mindos"
kubectl get pods -n agents | grep general

echo ""
echo "✅ Deployment Complete!"
echo ""
echo "🎯 Next Steps:"
echo "  1. Configure GitLens webhook to point to: https://gitlens.strategickhaos.com/webhook/gitlens"
echo "  2. Test event flow: curl -X POST http://localhost:8086/events -d '{\"type\":\"pr_created\",\"repository\":\"test-repo\",\"user\":\"testuser\",\"metadata\":{}}'"
echo "  3. Check Mind OS status: curl http://localhost:8090/status"
echo "  4. View LLM Generals: kubectl get pods -n agents"
echo ""
echo "📖 Documentation: See README.md for full integration guide"
