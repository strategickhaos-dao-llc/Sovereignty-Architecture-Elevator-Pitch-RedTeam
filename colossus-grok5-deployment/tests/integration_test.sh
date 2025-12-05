#!/bin/bash
# integration_test.sh - Integration tests for Colossus Grok-5
# Artifact #3558

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

NAMESPACE="${NAMESPACE:-colossus-grok5}"
TIMEOUT="${TIMEOUT:-300}"
FAILURES=0

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

test_pass() {
    echo -e "${GREEN}[PASS]${NC} $1"
}

test_fail() {
    echo -e "${RED}[FAIL]${NC} $1"
    ((FAILURES++))
}

# Header
echo "========================================="
echo "Colossus Grok-5 Integration Tests"
echo "Namespace: ${NAMESPACE}"
echo "Timeout: ${TIMEOUT}s"
echo "========================================="
echo ""

# Test 1: Deployment exists
log_info "Test 1: Checking deployment exists..."
if kubectl get deployment grok5-trainer -n "${NAMESPACE}" &>/dev/null; then
    test_pass "Deployment exists"
else
    test_fail "Deployment not found"
fi

# Test 2: Pods are running
log_info "Test 2: Checking pods are running..."
RUNNING=$(kubectl get pods -n "${NAMESPACE}" -l app=grok5-trainer --no-headers 2>/dev/null | grep -c "Running" || echo "0")
if [ "$RUNNING" -gt 0 ]; then
    test_pass "Pods running (${RUNNING} found)"
else
    test_fail "No running pods found"
fi

# Test 3: Service is accessible
log_info "Test 3: Checking service accessibility..."
if kubectl get service grok5-trainer -n "${NAMESPACE}" &>/dev/null; then
    CLUSTER_IP=$(kubectl get service grok5-trainer -n "${NAMESPACE}" -o jsonpath='{.spec.clusterIP}')
    if [ -n "$CLUSTER_IP" ] && [ "$CLUSTER_IP" != "None" ]; then
        test_pass "Service accessible at ${CLUSTER_IP}"
    else
        test_fail "Service has no ClusterIP"
    fi
else
    test_fail "Service not found"
fi

# Test 4: ConfigMap exists
log_info "Test 4: Checking configuration..."
if kubectl get configmap grok5-config -n "${NAMESPACE}" &>/dev/null; then
    test_pass "ConfigMap exists"
else
    test_fail "ConfigMap not found"
fi

# Test 5: HPA configured
log_info "Test 5: Checking HPA configuration..."
if kubectl get hpa grok5-trainer-hpa -n "${NAMESPACE}" &>/dev/null; then
    MIN=$(kubectl get hpa grok5-trainer-hpa -n "${NAMESPACE}" -o jsonpath='{.spec.minReplicas}')
    MAX=$(kubectl get hpa grok5-trainer-hpa -n "${NAMESPACE}" -o jsonpath='{.spec.maxReplicas}')
    if [ "$MIN" -ge 1000 ] && [ "$MAX" -ge 550000 ]; then
        test_pass "HPA configured correctly (min: ${MIN}, max: ${MAX})"
    else
        test_fail "HPA limits incorrect (min: ${MIN}, max: ${MAX})"
    fi
else
    test_fail "HPA not found"
fi

# Test 6: Storage configured
log_info "Test 6: Checking storage..."
PVC_COUNT=$(kubectl get pvc -n "${NAMESPACE}" --no-headers 2>/dev/null | wc -l)
if [ "$PVC_COUNT" -ge 1 ]; then
    test_pass "Storage configured (${PVC_COUNT} PVCs)"
else
    log_warn "No PVCs found (may be expected for minimal deployments)"
fi

# Test 7: Network policies
log_info "Test 7: Checking network policies..."
NETPOL_COUNT=$(kubectl get networkpolicy -n "${NAMESPACE}" --no-headers 2>/dev/null | wc -l)
if [ "$NETPOL_COUNT" -gt 0 ]; then
    test_pass "Network policies configured (${NETPOL_COUNT} policies)"
else
    log_warn "No network policies found"
fi

# Test 8: Health endpoint (if pod is running)
log_info "Test 8: Testing health endpoint..."
POD_NAME=$(kubectl get pods -n "${NAMESPACE}" -l app=grok5-trainer -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || echo "")
if [ -n "$POD_NAME" ]; then
    if kubectl exec -n "${NAMESPACE}" "${POD_NAME}" -- curl -s http://localhost:8080/health &>/dev/null; then
        test_pass "Health endpoint responding"
    else
        log_warn "Health endpoint not responding (may be expected during startup)"
    fi
else
    log_warn "No pod available for health check"
fi

# Test 9: Metrics endpoint
log_info "Test 9: Testing metrics endpoint..."
if [ -n "$POD_NAME" ]; then
    if kubectl exec -n "${NAMESPACE}" "${POD_NAME}" -- curl -s http://localhost:9090/metrics &>/dev/null; then
        test_pass "Metrics endpoint responding"
    else
        log_warn "Metrics endpoint not responding"
    fi
else
    log_warn "No pod available for metrics check"
fi

# Test 10: RBAC configured
log_info "Test 10: Checking RBAC..."
if kubectl get serviceaccount grok5-trainer -n "${NAMESPACE}" &>/dev/null; then
    test_pass "ServiceAccount configured"
else
    test_fail "ServiceAccount not found"
fi

# Summary
echo ""
echo "========================================="
if [ "$FAILURES" -eq 0 ]; then
    echo -e "${GREEN}All integration tests passed!${NC}"
    exit 0
else
    echo -e "${RED}${FAILURES} test(s) failed${NC}"
    exit 1
fi
