#!/bin/bash
# Sovereign Banking Integration - Quick Setup Script
# StrategicKhaos DAO LLC & ValorYield Engine
# Authorization: Board Resolution 2025-12-004

set -e

echo "=================================================="
echo "Sovereign Banking Integration Setup"
echo "StrategicKhaos DAO LLC & ValorYield Engine"
echo "=================================================="
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check prerequisites
echo "Checking prerequisites..."

# Check kubectl
if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}✗ kubectl not found${NC}"
    echo "Please install kubectl: https://kubernetes.io/docs/tasks/tools/"
    exit 1
fi
echo -e "${GREEN}✓ kubectl found${NC}"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ python3 not found${NC}"
    echo "Please install Python 3.11+: https://www.python.org/downloads/"
    exit 1
fi
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo -e "${GREEN}✓ Python ${PYTHON_VERSION} found${NC}"

# Check if connected to cluster
if ! kubectl cluster-info &> /dev/null; then
    echo -e "${YELLOW}⚠ Not connected to Kubernetes cluster${NC}"
    echo "Please configure kubectl to connect to your cluster"
    exit 1
fi
echo -e "${GREEN}✓ Connected to Kubernetes cluster${NC}"

echo ""
echo "=================================================="
echo "Configuration"
echo "=================================================="
echo ""

# Get configuration from user
read -p "Enter Sequence.io API Key: " -s SEQUENCE_API_KEY
echo ""
read -p "Enter Discord Webhook URL: " DISCORD_WEBHOOK_URL
echo ""
read -p "Enter NATS URL (default: nats://nats-service:4222): " NATS_URL
NATS_URL=${NATS_URL:-nats://nats-service:4222}
echo ""

if [ -z "$SEQUENCE_API_KEY" ] || [ -z "$DISCORD_WEBHOOK_URL" ]; then
    echo -e "${RED}Error: API Key and Webhook URL are required${NC}"
    exit 1
fi

echo ""
echo "=================================================="
echo "Deployment"
echo "=================================================="
echo ""

# Create namespace
echo "Creating namespace..."
kubectl create namespace sovereign-banking --dry-run=client -o yaml | kubectl apply -f -
echo -e "${GREEN}✓ Namespace created${NC}"

# Create secrets
echo "Creating secrets..."
kubectl create secret generic banking-secrets \
    --namespace=sovereign-banking \
    --from-literal=sequence_api_key="$SEQUENCE_API_KEY" \
    --from-literal=discord_webhook_url="$DISCORD_WEBHOOK_URL" \
    --dry-run=client -o yaml | kubectl apply -f -
echo -e "${GREEN}✓ Secrets created${NC}"

# Update ConfigMap with NATS URL
echo "Creating ConfigMap..."
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: ConfigMap
metadata:
  name: banking-config
  namespace: sovereign-banking
data:
  nats_url: "$NATS_URL"
  sequence_api_url: "https://api.getsequence.io/v1"
  audit_log_path: "/var/log/sovereign-banking/audit.jsonl"
  strategickhaos_ein: "39-2900295"
  valoryield_ein: "39-2923503"
  log_level: "INFO"
EOF
echo -e "${GREEN}✓ ConfigMap created${NC}"

# Create ConfigMap with application code
echo "Creating application ConfigMap..."
kubectl create configmap banking-app-code \
    --namespace=sovereign-banking \
    --from-file=sovereign_banking.py=./sovereign_banking.py \
    --dry-run=client -o yaml | kubectl apply -f -
echo -e "${GREEN}✓ Application code ConfigMap created${NC}"

# Apply Kubernetes manifests
echo "Deploying banking integration..."
kubectl apply -f ../kubernetes/deployment.yaml
echo -e "${GREEN}✓ Deployment manifests applied${NC}"

echo ""
echo "=================================================="
echo "Verification"
echo "=================================================="
echo ""

# Wait for pods to be ready
echo "Waiting for pods to be ready (this may take a minute)..."
kubectl wait --for=condition=ready pod \
    -l app=sovereign-banking \
    -n sovereign-banking \
    --timeout=180s

# Get pod status
echo ""
echo "Pod Status:"
kubectl get pods -n sovereign-banking

echo ""
echo "=================================================="
echo "Setup Complete!"
echo "=================================================="
echo ""
echo -e "${GREEN}✓ Sovereign Banking Integration deployed successfully${NC}"
echo ""
echo "Next steps:"
echo "1. View logs: kubectl logs -f deployment/sovereign-banking -n sovereign-banking"
echo "2. Send test transaction: See README.md for NATS message format"
echo "3. Monitor Discord channel for notifications"
echo ""
echo "Documentation: banking-integration/README.md"
echo ""
echo "Board Authorization: Resolution 2025-12-004"
echo "StrategicKhaos DAO LLC (EIN: 39-2900295) - 93%"
echo "ValorYield Engine (EIN: 39-2923503) - 7%"
echo ""
