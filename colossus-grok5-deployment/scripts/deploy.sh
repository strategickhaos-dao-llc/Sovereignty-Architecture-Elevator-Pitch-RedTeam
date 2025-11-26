#!/bin/bash
# deploy.sh - Deploy Colossus Grok-5 to Kubernetes
# Artifact #3558

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default values
CLUSTER="colossus2"
REGION="nv-giga-01"
NAMESPACE="colossus-grok5"
SKIP_TESTS=false
DRY_RUN=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --cluster=*)
            CLUSTER="${1#*=}"
            shift
            ;;
        --region=*)
            REGION="${1#*=}"
            shift
            ;;
        --namespace=*)
            NAMESPACE="${1#*=}"
            shift
            ;;
        --skip-tests)
            SKIP_TESTS=true
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        -h|--help)
            echo "Usage: deploy.sh [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --cluster=NAME     Kubernetes cluster name (default: colossus2)"
            echo "  --region=REGION    Region for deployment (default: nv-giga-01)"
            echo "  --namespace=NS     Kubernetes namespace (default: colossus-grok5)"
            echo "  --skip-tests       Skip integration tests"
            echo "  --dry-run          Print commands without executing"
            echo "  -h, --help         Show this help message"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
K8S_DIR="${SCRIPT_DIR}/../k8s"
MONITORING_DIR="${SCRIPT_DIR}/../monitoring"

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

run_cmd() {
    if [ "$DRY_RUN" = true ]; then
        echo "[DRY-RUN] $*"
    else
        "$@"
    fi
}

# Main deployment steps
log_info "Starting Colossus Grok-5 deployment"
log_info "Cluster: ${CLUSTER}"
log_info "Region: ${REGION}"
log_info "Namespace: ${NAMESPACE}"

# Step 1: Verify cluster connection
log_info "Step 1: Verifying cluster connection..."
if ! kubectl cluster-info &>/dev/null; then
    log_error "Cannot connect to Kubernetes cluster"
    exit 1
fi

# Step 2: Create namespace
log_info "Step 2: Creating namespace..."
run_cmd kubectl apply -f "${K8S_DIR}/namespace.yaml"

# Step 3: Apply storage configuration
log_info "Step 3: Configuring storage..."
run_cmd kubectl apply -f "${K8S_DIR}/storage.yaml"

# Step 4: Apply network policies
log_info "Step 4: Configuring network policies..."
run_cmd kubectl apply -f "${K8S_DIR}/network-policy.yaml"

# Step 5: Apply service mesh configuration
log_info "Step 5: Configuring service mesh..."
if kubectl get crd virtualservices.networking.istio.io &>/dev/null; then
    run_cmd kubectl apply -f "${K8S_DIR}/service-mesh.yaml"
else
    log_warn "Istio not installed, skipping service mesh configuration"
fi

# Step 6: Deploy main application
log_info "Step 6: Deploying Grok-5 trainer..."
run_cmd kubectl apply -f "${K8S_DIR}/deployment-550k-gpu.yaml"

# Step 7: Configure HPA
log_info "Step 7: Configuring energy-aware HPA..."
run_cmd kubectl apply -f "${K8S_DIR}/hpa-energy-aware.yaml"

# Step 8: Run database migrations
log_info "Step 8: Running database migrations..."
run_cmd "${SCRIPT_DIR}/migrate-db.sh"

# Step 9: Configure monitoring
log_info "Step 9: Configuring monitoring..."
if kubectl get crd prometheusrules.monitoring.coreos.com &>/dev/null; then
    run_cmd kubectl apply -f "${MONITORING_DIR}/prometheus-rules.yaml"
else
    log_warn "Prometheus Operator not installed, skipping Prometheus rules"
fi

# Step 10: Configure alerting
log_info "Step 10: Configuring alerting..."
run_cmd kubectl apply -f "${MONITORING_DIR}/alertmanager-config.yaml" 2>/dev/null || \
    log_warn "Alertmanager config skipped (may require manual configuration)"

# Step 11: Run integration tests
if [ "$SKIP_TESTS" = false ]; then
    log_info "Step 11: Running integration tests..."
    run_cmd "${SCRIPT_DIR}/../tests/integration_test.sh"
else
    log_warn "Step 11: Skipping integration tests (--skip-tests)"
fi

# Step 12: Verify deployment
log_info "Step 12: Verifying deployment..."
run_cmd kubectl rollout status deployment/grok5-trainer -n "${NAMESPACE}" --timeout=300s

# Summary
log_info "========================================="
log_info "Deployment complete!"
log_info "========================================="
log_info "Namespace: ${NAMESPACE}"
log_info "Cluster: ${CLUSTER}"
log_info "Region: ${REGION}"
log_info ""
log_info "Next steps:"
log_info "  1. Check pod status: kubectl get pods -n ${NAMESPACE}"
log_info "  2. View logs: kubectl logs -f deployment/grok5-trainer -n ${NAMESPACE}"
log_info "  3. Check HPA: kubectl get hpa -n ${NAMESPACE}"
log_info ""
log_info "To rollback: ./rollback.sh --cluster=${CLUSTER} --to-tag=vLAST_GOOD"
