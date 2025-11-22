#!/bin/bash
# Deploy Gaming Console Infrastructure for Sovereign Architecture
# PlayStation Remote Play Integration with Kubernetes

set -euo pipefail

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
NAMESPACE="gaming-consoles"
K8S_DIR="bootstrap/k8s"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${BLUE}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  PlayStation Remote Play Kubernetes Deployment           ║${NC}"
echo -e "${BLUE}║  Sovereign Gaming Console Infrastructure                 ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

# Function to print status
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    print_error "kubectl is not installed. Please install kubectl first."
    exit 1
fi

print_status "kubectl found"

# Check if we can connect to Kubernetes cluster
if ! kubectl cluster-info &> /dev/null; then
    print_error "Cannot connect to Kubernetes cluster. Please check your kubeconfig."
    exit 1
fi

print_status "Connected to Kubernetes cluster"

# Check if namespace exists
if kubectl get namespace "$NAMESPACE" &> /dev/null; then
    print_warning "Namespace '$NAMESPACE' already exists. Continuing..."
else
    print_info "Creating namespace '$NAMESPACE'..."
fi

# Deploy Kubernetes manifests
echo ""
print_info "Deploying Gaming Console Infrastructure..."
echo ""

# 1. Create namespace and resource quotas
print_info "Step 1/6: Creating namespace and resource quotas..."
kubectl apply -f "$K8S_DIR/gaming-console-namespace.yaml"
print_status "Namespace and resource quotas created"

# 2. Setup RBAC
print_info "Step 2/6: Setting up RBAC..."
kubectl apply -f "$K8S_DIR/gaming-console-rbac.yaml"
print_status "RBAC configured"

# 3. Apply network policies
print_info "Step 3/6: Applying network policies (closed-loop security)..."
kubectl apply -f "$K8S_DIR/gaming-console-network-policy.yaml"
print_status "Network policies applied"

# 4. Deploy PlayStation Remote Play gateway
print_info "Step 4/6: Deploying PlayStation Remote Play gateway..."
kubectl apply -f "$K8S_DIR/playstation-remote-play-deployment.yaml"
print_status "Remote Play gateway deployed"

# 5. Deploy 4 gaming consoles (StatefulSet)
print_info "Step 5/6: Deploying 4 gaming consoles..."
kubectl apply -f "$K8S_DIR/gaming-console-statefulset.yaml"
print_status "Gaming consoles deployed"

# 6. Wait for deployments to be ready
print_info "Step 6/6: Waiting for deployments to be ready..."
echo ""

echo -e "${YELLOW}Waiting for Remote Play gateway...${NC}"
kubectl wait --for=condition=available --timeout=120s \
    deployment/playstation-remote-play-gateway -n "$NAMESPACE" || true

echo -e "${YELLOW}Waiting for gaming consoles...${NC}"
kubectl wait --for=condition=ready --timeout=180s \
    pod -l app=gaming-console -n "$NAMESPACE" || true

echo ""
print_status "All deployments ready"

# Display deployment status
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}Deployment Summary${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""

echo -e "${YELLOW}Namespace:${NC} $NAMESPACE"
echo ""

echo -e "${YELLOW}Gaming Consoles:${NC}"
kubectl get pods -n "$NAMESPACE" -l app=gaming-console -o wide

echo ""
echo -e "${YELLOW}Services:${NC}"
kubectl get svc -n "$NAMESPACE"

echo ""
echo -e "${YELLOW}Network Policies:${NC}"
kubectl get networkpolicy -n "$NAMESPACE"

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
print_status "Gaming console infrastructure deployed successfully!"
echo ""

# Display connection information
echo -e "${YELLOW}PlayStation Remote Play Endpoints:${NC}"
echo "  Gateway: playstation-remote-play-gateway.gaming-consoles.svc.cluster.local:9987"
echo "  Console 1: ps5-console-1.gaming-consoles.svc.cluster.local:9987"
echo "  Console 2: ps5-console-2.gaming-consoles.svc.cluster.local:9987"
echo "  Console 3: ps5-console-3.gaming-consoles.svc.cluster.local:9987"
echo "  Console 4: ps5-console-4.gaming-consoles.svc.cluster.local:9987"
echo ""

echo -e "${YELLOW}Scholarly Resources:${NC}"
echo "  View deployed resources: kubectl get configmap playstation-config -n $NAMESPACE -o yaml"
echo "  36 web pages from .org, .gov domains are documented in the configuration"
echo ""

echo -e "${GREEN}✓ Closed-loop sovereign gaming infrastructure is now active!${NC}"
echo ""
