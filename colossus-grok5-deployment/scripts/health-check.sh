#!/bin/bash
# health-check.sh - Health check for Colossus Grok-5 deployment
# Artifact #3558

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

NAMESPACE="${NAMESPACE:-colossus-grok5}"
VERBOSE=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --namespace=*)
            NAMESPACE="${1#*=}"
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -h|--help)
            echo "Usage: health-check.sh [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --namespace=NS     Kubernetes namespace (default: colossus-grok5)"
            echo "  -v, --verbose      Show detailed output"
            echo "  -h, --help         Show this help message"
            exit 0
            ;;
        *)
            shift
            ;;
    esac
done

# Functions
check_pass() {
    echo -e "${GREEN}[PASS]${NC} $1"
}

check_fail() {
    echo -e "${RED}[FAIL]${NC} $1"
}

check_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

# Header
echo "========================================="
echo "Colossus Grok-5 Health Check"
echo "Namespace: ${NAMESPACE}"
echo "========================================="
echo ""

FAILURES=0

# Check 1: Namespace exists
echo "Checking namespace..."
if kubectl get namespace "${NAMESPACE}" &>/dev/null; then
    check_pass "Namespace ${NAMESPACE} exists"
else
    check_fail "Namespace ${NAMESPACE} not found"
    ((FAILURES++))
fi

# Check 2: Deployment exists and healthy
echo ""
echo "Checking deployment..."
DESIRED=$(kubectl get deployment grok5-trainer -n "${NAMESPACE}" -o jsonpath='{.spec.replicas}' 2>/dev/null || echo "0")
READY=$(kubectl get deployment grok5-trainer -n "${NAMESPACE}" -o jsonpath='{.status.readyReplicas}' 2>/dev/null || echo "0")

if [ "$DESIRED" -gt 0 ] && [ "$READY" -eq "$DESIRED" ]; then
    check_pass "Deployment healthy (${READY}/${DESIRED} replicas ready)"
elif [ "$DESIRED" -gt 0 ]; then
    check_warn "Deployment partially ready (${READY}/${DESIRED} replicas)"
else
    check_fail "Deployment not found or has 0 replicas"
    ((FAILURES++))
fi

# Check 3: HPA configured
echo ""
echo "Checking HPA..."
if kubectl get hpa grok5-trainer-hpa -n "${NAMESPACE}" &>/dev/null; then
    MIN=$(kubectl get hpa grok5-trainer-hpa -n "${NAMESPACE}" -o jsonpath='{.spec.minReplicas}')
    MAX=$(kubectl get hpa grok5-trainer-hpa -n "${NAMESPACE}" -o jsonpath='{.spec.maxReplicas}')
    check_pass "HPA configured (min: ${MIN}, max: ${MAX})"
else
    check_warn "HPA not found"
fi

# Check 4: Services running
echo ""
echo "Checking services..."
if kubectl get service grok5-trainer -n "${NAMESPACE}" &>/dev/null; then
    check_pass "Service grok5-trainer exists"
else
    check_fail "Service grok5-trainer not found"
    ((FAILURES++))
fi

# Check 5: ConfigMap exists
echo ""
echo "Checking configuration..."
if kubectl get configmap grok5-config -n "${NAMESPACE}" &>/dev/null; then
    check_pass "ConfigMap grok5-config exists"
else
    check_warn "ConfigMap grok5-config not found"
fi

# Check 6: Secrets (if any)
echo ""
echo "Checking secrets..."
SECRET_COUNT=$(kubectl get secrets -n "${NAMESPACE}" --no-headers 2>/dev/null | wc -l)
if [ "$SECRET_COUNT" -gt 0 ]; then
    check_pass "${SECRET_COUNT} secrets configured"
else
    check_warn "No secrets found in namespace"
fi

# Check 7: PVCs
echo ""
echo "Checking storage..."
PVC_COUNT=$(kubectl get pvc -n "${NAMESPACE}" --no-headers 2>/dev/null | wc -l)
if [ "$PVC_COUNT" -gt 0 ]; then
    BOUND=$(kubectl get pvc -n "${NAMESPACE}" --no-headers 2>/dev/null | grep -c "Bound" || echo "0")
    if [ "$BOUND" -eq "$PVC_COUNT" ]; then
        check_pass "${PVC_COUNT} PVCs bound"
    else
        check_warn "${BOUND}/${PVC_COUNT} PVCs bound"
    fi
else
    check_warn "No PVCs found"
fi

# Check 8: Pod health
echo ""
echo "Checking pod health..."
RUNNING=$(kubectl get pods -n "${NAMESPACE}" --no-headers 2>/dev/null | grep -c "Running" || echo "0")
TOTAL=$(kubectl get pods -n "${NAMESPACE}" --no-headers 2>/dev/null | wc -l)
if [ "$TOTAL" -gt 0 ]; then
    if [ "$RUNNING" -eq "$TOTAL" ]; then
        check_pass "${RUNNING}/${TOTAL} pods running"
    else
        check_warn "${RUNNING}/${TOTAL} pods running"
        if [ "$VERBOSE" = true ]; then
            echo "  Non-running pods:"
            kubectl get pods -n "${NAMESPACE}" --no-headers | grep -v "Running" | awk '{print "    - " $1 ": " $3}'
        fi
    fi
else
    check_fail "No pods found"
    ((FAILURES++))
fi

# Check 9: Recent events
echo ""
echo "Checking recent events..."
WARNINGS=$(kubectl get events -n "${NAMESPACE}" --field-selector type=Warning --no-headers 2>/dev/null | head -5 | wc -l)
if [ "$WARNINGS" -eq 0 ]; then
    check_pass "No warning events"
else
    check_warn "${WARNINGS} warning events in last hour"
    if [ "$VERBOSE" = true ]; then
        echo "  Recent warnings:"
        kubectl get events -n "${NAMESPACE}" --field-selector type=Warning --no-headers 2>/dev/null | head -5 | awk '{print "    - " $4 ": " $5}'
    fi
fi

# Summary
echo ""
echo "========================================="
if [ "$FAILURES" -eq 0 ]; then
    echo -e "${GREEN}Health check passed!${NC}"
    exit 0
else
    echo -e "${RED}Health check failed with ${FAILURES} critical issue(s)${NC}"
    exit 1
fi
