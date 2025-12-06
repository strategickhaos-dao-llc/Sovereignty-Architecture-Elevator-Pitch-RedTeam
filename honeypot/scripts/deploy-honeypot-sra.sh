#!/bin/bash
# deploy-honeypot-sra.sh
# Deploy vulnerable Signal Routing Authority as honeypot for offensive security testing
#
# SECURITY NOTICE: This script deploys an INTENTIONALLY VULNERABLE system
# for red team training and attack pattern learning. Deploy only in isolated
# environments with proper monitoring.
#
# Author: Strategickhaos Swarm Intelligence
# Purpose: Offensive Sovereignty - Learn by being attacked

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

echo -e "${PURPLE}🎣 DEPLOYING HONEYPOT: Signal Routing Authority${NC}"
echo "================================================"
echo ""
echo -e "${YELLOW}⚠️  WARNING: This deploys an INTENTIONALLY VULNERABLE system${NC}"
echo -e "${YELLOW}⚠️  Only deploy in isolated red team environments${NC}"
echo ""

# Check prerequisites
check_prerequisites() {
    echo -e "${GREEN}[1/6] Checking prerequisites...${NC}"
    
    if ! command -v kubectl &> /dev/null; then
        echo -e "${RED}ERROR: kubectl not found. Please install kubectl first.${NC}"
        exit 1
    fi
    
    if ! kubectl cluster-info &> /dev/null; then
        echo -e "${RED}ERROR: Cannot connect to Kubernetes cluster.${NC}"
        exit 1
    fi
    
    echo "  ✅ kubectl found and cluster accessible"
}

# Create isolated namespace
create_namespace() {
    echo -e "${GREEN}[2/6] Creating isolated red team namespace...${NC}"
    
    if kubectl get namespace red-team-honeypot &> /dev/null; then
        echo "  ⚠️  Namespace red-team-honeypot already exists"
    else
        kubectl create namespace red-team-honeypot
        echo "  ✅ Created namespace red-team-honeypot"
    fi
    
    # Label it clearly for identification
    kubectl label namespace red-team-honeypot \
        security=honeypot \
        team=red \
        purpose=offensive-testing \
        --overwrite
    
    echo "  ✅ Namespace labeled as honeypot"
}

# Apply network isolation (allow only specific ingress)
apply_network_policies() {
    echo -e "${GREEN}[3/6] Applying network isolation policies...${NC}"
    
    cat << 'EOF' | kubectl apply -f -
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: honeypot-isolation
  namespace: red-team-honeypot
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress
  ingress:
    # Allow all external ingress (this is a honeypot - we want attacks)
    - {}
  egress:
    # Allow only internal honeytrap logging
    - to:
        - namespaceSelector:
            matchLabels:
              name: red-team-honeypot
    # Allow DNS
    - to:
        - namespaceSelector: {}
      ports:
        - protocol: UDP
          port: 53
EOF
    
    echo "  ✅ Network policies applied (isolated from production)"
}

# Deploy the vulnerable SRA
deploy_honeypot_sra() {
    echo -e "${GREEN}[4/6] Deploying vulnerable SRA...${NC}"
    
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    kubectl apply -f "$SCRIPT_DIR/../k8s/honeypot-sra-deployment.yaml"
    
    echo "  ✅ Honeypot SRA deployment applied"
}

# Deploy honeytrap logging service
deploy_honeytrap() {
    echo -e "${GREEN}[5/6] Deploying Honeytrap logging service...${NC}"
    
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    kubectl apply -f "$SCRIPT_DIR/../k8s/honeytrap-deployment.yaml"
    
    echo "  ✅ Honeytrap logging service deployed"
}

# Show status and URLs
show_status() {
    echo -e "${GREEN}[6/6] Checking deployment status...${NC}"
    
    echo ""
    echo -e "${PURPLE}📊 DEPLOYMENT STATUS${NC}"
    kubectl get pods -n red-team-honeypot
    
    echo ""
    echo -e "${PURPLE}🌐 SERVICES${NC}"
    kubectl get svc -n red-team-honeypot
    
    echo ""
    echo -e "${PURPLE}🔗 INGRESS${NC}"
    kubectl get ingress -n red-team-honeypot 2>/dev/null || echo "  No ingress configured yet"
    
    echo ""
    echo -e "${PURPLE}═══════════════════════════════════════════════════${NC}"
    echo -e "${RED}🎣 HONEYPOT DEPLOYED - INTENTIONALLY VULNERABLE:${NC}"
    echo -e "${YELLOW}   - No HMAC verification${NC}"
    echo -e "${YELLOW}   - No rate limiting${NC}"
    echo -e "${YELLOW}   - No authentication${NC}"
    echo -e "${YELLOW}   - Exposed to internet${NC}"
    echo ""
    echo -e "${PURPLE}🔥 LET THE RED TEAM PLAY${NC}"
    echo -e "${PURPLE}═══════════════════════════════════════════════════${NC}"
}

# Main execution
main() {
    echo -e "${PURPLE}Starting Honeypot Deployment...${NC}"
    echo ""
    
    check_prerequisites
    create_namespace
    apply_network_policies
    deploy_honeypot_sra
    deploy_honeytrap
    show_status
    
    echo ""
    echo -e "${GREEN}✅ Honeypot deployment complete!${NC}"
    echo ""
    echo -e "${PURPLE}Next steps:${NC}"
    echo "  1. Run red team attacks: ./red-team-attacks.sh"
    echo "  2. Watch attack logs: kubectl logs -f deployment/honeytrap -n red-team-honeypot"
    echo "  3. Analyze with Legion: kubectl logs -f deployment/legion-analyzer -n red-team-honeypot"
}

# Cleanup function
cleanup() {
    echo -e "${YELLOW}Cleaning up honeypot deployment...${NC}"
    kubectl delete namespace red-team-honeypot --ignore-not-found
    echo -e "${GREEN}✅ Honeypot namespace deleted${NC}"
}

# Handle arguments
case "${1:-deploy}" in
    deploy)
        main
        ;;
    cleanup|delete|remove)
        cleanup
        ;;
    status)
        show_status
        ;;
    *)
        echo "Usage: $0 [deploy|cleanup|status]"
        echo "  deploy  - Deploy the honeypot (default)"
        echo "  cleanup - Remove the honeypot deployment"
        echo "  status  - Show current deployment status"
        exit 1
        ;;
esac
