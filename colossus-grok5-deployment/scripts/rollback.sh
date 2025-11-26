#!/bin/bash
# rollback.sh - Rollback Colossus Grok-5 deployment
# Artifact #3558

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Default values
CLUSTER=""
TO_TAG=""
NAMESPACE="colossus-grok5"
CONFIRM=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --cluster=*)
            CLUSTER="${1#*=}"
            shift
            ;;
        --to-tag=*)
            TO_TAG="${1#*=}"
            shift
            ;;
        --namespace=*)
            NAMESPACE="${1#*=}"
            shift
            ;;
        --yes|-y)
            CONFIRM=true
            shift
            ;;
        -h|--help)
            echo "Usage: rollback.sh [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --cluster=NAME     Kubernetes cluster name (required)"
            echo "  --to-tag=TAG       Tag to rollback to (required)"
            echo "  --namespace=NS     Kubernetes namespace (default: colossus-grok5)"
            echo "  --yes, -y          Skip confirmation prompt"
            echo "  -h, --help         Show this help message"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

# Validate required arguments
if [ -z "$CLUSTER" ] || [ -z "$TO_TAG" ]; then
    echo -e "${RED}Error: --cluster and --to-tag are required${NC}"
    echo "Usage: rollback.sh --cluster=<name> --to-tag=<tag>"
    exit 1
fi

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

# Main rollback process
echo "========================================="
echo "Colossus Grok-5 Rollback"
echo "========================================="
echo "Cluster: ${CLUSTER}"
echo "Namespace: ${NAMESPACE}"
echo "Target Tag: ${TO_TAG}"
echo ""

# Get current deployment info
CURRENT_IMAGE=$(kubectl get deployment grok5-trainer -n "${NAMESPACE}" \
    -o jsonpath='{.spec.template.spec.containers[0].image}' 2>/dev/null || echo "unknown")

log_info "Current image: ${CURRENT_IMAGE}"
log_info "Target tag: ${TO_TAG}"
echo ""

# Confirmation
if [ "$CONFIRM" = false ]; then
    echo -e "${YELLOW}WARNING: This will rollback the deployment to ${TO_TAG}${NC}"
    read -p "Are you sure you want to proceed? [y/N] " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_info "Rollback cancelled"
        exit 0
    fi
fi

# Step 1: Create backup of current state
log_info "Step 1: Creating backup of current state..."
BACKUP_DIR="/tmp/grok5-rollback-$(date +%Y%m%d-%H%M%S)"
mkdir -p "${BACKUP_DIR}"

kubectl get deployment grok5-trainer -n "${NAMESPACE}" -o yaml > "${BACKUP_DIR}/deployment-backup.yaml"
kubectl get configmap grok5-config -n "${NAMESPACE}" -o yaml > "${BACKUP_DIR}/configmap-backup.yaml" 2>/dev/null || true

log_info "Backup saved to: ${BACKUP_DIR}"

# Step 2: Scale down to safe level
log_info "Step 2: Scaling down deployment..."
kubectl scale deployment grok5-trainer -n "${NAMESPACE}" --replicas=1000

# Wait for scale down
kubectl rollout status deployment/grok5-trainer -n "${NAMESPACE}" --timeout=120s

# Step 3: Update image tag
log_info "Step 3: Updating image to ${TO_TAG}..."
NEW_IMAGE="ghcr.io/xai/grok5-trainer:${TO_TAG}"
kubectl set image deployment/grok5-trainer trainer="${NEW_IMAGE}" -n "${NAMESPACE}"

# Step 4: Wait for rollout
log_info "Step 4: Waiting for rollout to complete..."
if kubectl rollout status deployment/grok5-trainer -n "${NAMESPACE}" --timeout=300s; then
    log_info "Rollout completed successfully"
else
    log_error "Rollout failed, attempting to restore from backup"
    kubectl apply -f "${BACKUP_DIR}/deployment-backup.yaml"
    exit 1
fi

# Step 5: Run health check
log_info "Step 5: Running health check..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if "${SCRIPT_DIR}/health-check.sh" --namespace="${NAMESPACE}"; then
    log_info "Health check passed"
else
    log_warn "Health check reported issues, please investigate"
fi

# Summary
echo ""
echo "========================================="
log_info "Rollback completed!"
echo "========================================="
echo "Previous image: ${CURRENT_IMAGE}"
echo "New image: ${NEW_IMAGE}"
echo "Backup location: ${BACKUP_DIR}"
echo ""
log_info "To restore if needed:"
echo "  kubectl apply -f ${BACKUP_DIR}/deployment-backup.yaml"
