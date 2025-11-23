#!/bin/bash
# Test Agent Connection to Kubernetes Cluster
# Validates connectivity and access to agent API endpoints

set -euo pipefail

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Configuration
VPN_IP="${VPN_IP:-localhost}"
API_PORT="${API_PORT:-30000}"
METRICS_PORT="${METRICS_PORT:-30090}"

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }

# Test VPN connectivity
test_vpn() {
    log_info "Testing VPN connectivity..."
    if ping -c 1 -W 2 "$VPN_IP" &> /dev/null; then
        log_info "✓ VPN connection successful to $VPN_IP"
        return 0
    else
        log_error "✗ Cannot reach $VPN_IP - check VPN connection"
        return 1
    fi
}

# Test kubectl access
test_kubectl() {
    log_info "Testing kubectl access..."
    if kubectl cluster-info &> /dev/null; then
        log_info "✓ kubectl connected to cluster"
        kubectl cluster-info | head -n 3
        return 0
    else
        log_error "✗ kubectl cannot connect to cluster"
        return 1
    fi
}

# Test API endpoint
test_api_endpoint() {
    log_info "Testing API endpoint at http://${VPN_IP}:${API_PORT}..."
    
    # Test health endpoint
    if curl -f -s --connect-timeout 5 "http://${VPN_IP}:${API_PORT}/health" > /dev/null; then
        log_info "✓ API health endpoint responding"
        return 0
    else
        log_warn "✗ API endpoint not responding at http://${VPN_IP}:${API_PORT}/health"
        return 1
    fi
}

# Test metrics endpoint
test_metrics() {
    log_info "Testing metrics endpoint at http://${VPN_IP}:${METRICS_PORT}..."
    
    if curl -f -s --connect-timeout 5 "http://${VPN_IP}:${METRICS_PORT}/metrics" > /dev/null; then
        log_info "✓ Metrics endpoint responding"
        return 0
    else
        log_warn "✗ Metrics endpoint not responding"
        return 1
    fi
}

# Test pod access
test_pod_access() {
    log_info "Testing pod access..."
    
    if kubectl get pods -n ops &> /dev/null; then
        local pod_count=$(kubectl get pods -n ops --no-headers 2>/dev/null | wc -l)
        log_info "✓ Can access pods in ops namespace (found $pod_count pods)"
        return 0
    else
        log_error "✗ Cannot access pods in ops namespace"
        return 1
    fi
}

# Test service discovery
test_service_discovery() {
    log_info "Testing service discovery..."
    
    if kubectl get services -n ops &> /dev/null; then
        local svc_count=$(kubectl get services -n ops --no-headers 2>/dev/null | wc -l)
        log_info "✓ Can discover services (found $svc_count services)"
        return 0
    else
        log_error "✗ Cannot discover services"
        return 1
    fi
}

# Test Docker access
test_docker() {
    log_info "Testing Docker access..."
    
    if docker ps &> /dev/null; then
        local container_count=$(docker ps -q | wc -l)
        log_info "✓ Docker is accessible (running $container_count containers)"
        return 0
    else
        log_warn "✗ Docker is not accessible or not running"
        return 1
    fi
}

# Generate test report
generate_report() {
    local passed=$1
    local total=$2
    local failed=$((total - passed))
    
    echo ""
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║              Connection Test Report                       ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo ""
    echo "Total Tests: $total"
    echo "Passed: $passed"
    echo "Failed: $failed"
    echo ""
    
    if [[ $passed -eq $total ]]; then
        log_info "All tests passed! Agent collaboration environment is ready."
        return 0
    else
        log_error "Some tests failed. Review the output above for details."
        return 1
    fi
}

# Main test execution
main() {
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║        Agent Collaboration Connection Test                ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo ""
    
    local passed=0
    local total=7
    
    test_vpn && ((passed++)) || true
    test_kubectl && ((passed++)) || true
    test_pod_access && ((passed++)) || true
    test_service_discovery && ((passed++)) || true
    test_docker && ((passed++)) || true
    test_api_endpoint && ((passed++)) || true
    test_metrics && ((passed++)) || true
    
    generate_report $passed $total
}

# Run tests
main "$@"
