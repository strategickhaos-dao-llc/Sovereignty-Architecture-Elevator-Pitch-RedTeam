#!/bin/bash

# Infrastructure Verification Script
# Validates that all 7 pillars are properly configured

echo "=============================================="
echo "   SOVEREIGNTY INFRASTRUCTURE VERIFICATION"
echo "=============================================="
echo ""

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

ERRORS=0

# Function to check if file exists
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $1"
    else
        echo -e "${RED}✗${NC} $1 - MISSING"
        ((ERRORS++))
    fi
}

# Function to check if directory exists
check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✓${NC} $1"
    else
        echo -e "${RED}✗${NC} $1 - MISSING"
        ((ERRORS++))
    fi
}

echo -e "${YELLOW}[1/7] Checking Kubernetes Cluster Federation...${NC}"
check_dir "kubernetes/base"
check_dir "kubernetes/overlays/production"
check_dir "kubernetes/overlays/chaos-god-origin"
check_file "kubernetes/base/kustomization.yaml"
echo ""

echo -e "${YELLOW}[2/7] Checking Terraform Enterprise IaC...${NC}"
check_file "terraform/main.tf"
check_dir "terraform/modules/k3s-cluster"
check_dir "terraform/modules/eks-cluster"
check_dir "terraform/modules/vault"
check_dir "terraform/modules/tailscale"
check_dir "terraform/environments/prod"
check_dir "terraform/environments/staging"
check_dir "terraform/environments/chaos-god-local"
echo ""

echo -e "${YELLOW}[3/7] Checking GitOps (ArgoCD + Flux)...${NC}"
check_file "kubernetes/argocd/application.yaml"
check_file "kubernetes/flux/kustomization.yaml"
check_file "kubernetes/flux/gitrepository.yaml"
check_file "gitops/bootstrap/install.yaml"
check_file "gitops/applications/sovereignty-core.yaml"
echo ""

echo -e "${YELLOW}[4/7] Checking Zero-Trust Networking...${NC}"
check_file "terraform/modules/tailscale/main.tf"
echo ""

echo -e "${YELLOW}[5/7] Checking Observability Stack...${NC}"
check_file "observability/prometheus/prometheus.yaml"
check_file "observability/grafana/dashboards.yaml"
check_file "observability/loki/loki-config.yaml"
echo ""

echo -e "${YELLOW}[6/7] Checking Secrets Management...${NC}"
check_file "secrets/vault/vault-config.yaml"
check_file "terraform/modules/vault/main.tf"
echo ""

echo -e "${YELLOW}[7/7] Checking CI/CD Fortress...${NC}"
check_file "ci-cd/tekton/pipeline.yaml"
check_file "ci-cd/github-actions/deploy.yaml"
check_file "ci-cd/github-actions/security-scan.yaml"
echo ""

# Check deployment scripts
echo -e "${YELLOW}Checking deployment scripts...${NC}"
check_file "deploy-production.sh"
check_file "PRODUCTION_README.md"
check_file "NEXT_100_ASCENSION.md"
echo ""

# Summary
echo "=============================================="
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}   ALL CHECKS PASSED ✓${NC}"
    echo "   Infrastructure is ready for deployment"
else
    echo -e "${RED}   FOUND $ERRORS ERROR(S) ✗${NC}"
    echo "   Please fix the missing components"
fi
echo "=============================================="
echo ""

exit $ERRORS
