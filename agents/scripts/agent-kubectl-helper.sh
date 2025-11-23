#!/bin/bash
# Agent kubectl Helper Script
# Provides convenient commands for agent interaction with Kubernetes

set -euo pipefail

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Display usage
usage() {
    cat << EOF
Usage: $(basename "$0") <command> [options]

Commands:
  pods [namespace]          List pods in namespace (default: ops)
  logs <pod> [namespace]    Get logs from a pod
  exec <pod> <command>      Execute command in pod
  services [namespace]      List services in namespace
  status                    Show cluster status
  metrics                   Display cluster metrics
  api-test                  Test API endpoint connectivity
  port-forward <pod> <port> Forward port from pod to localhost

Examples:
  $(basename "$0") pods ops
  $(basename "$0") logs discord-ops-bot-12345 ops
  $(basename "$0") exec discord-ops-bot-12345 "ps aux"
  $(basename "$0") api-test

EOF
}

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_cmd() { echo -e "${BLUE}[CMD]${NC} $1"; }

# List pods
cmd_pods() {
    local namespace="${1:-ops}"
    log_info "Listing pods in namespace: $namespace"
    log_cmd "kubectl get pods -n $namespace"
    kubectl get pods -n "$namespace" -o wide
}

# Get logs
cmd_logs() {
    local pod="$1"
    local namespace="${2:-ops}"
    local lines="${3:-100}"
    
    log_info "Getting logs from pod: $pod (namespace: $namespace)"
    log_cmd "kubectl logs $pod -n $namespace --tail=$lines"
    kubectl logs "$pod" -n "$namespace" --tail="$lines"
}

# Execute command
cmd_exec() {
    local pod="$1"
    local command="${2:-/bin/sh}"
    local namespace="${3:-ops}"
    
    log_info "Executing command in pod: $pod"
    log_cmd "kubectl exec -it $pod -n $namespace -- $command"
    kubectl exec -it "$pod" -n "$namespace" -- $command
}

# List services
cmd_services() {
    local namespace="${1:-ops}"
    log_info "Listing services in namespace: $namespace"
    log_cmd "kubectl get services -n $namespace"
    kubectl get services -n "$namespace" -o wide
}

# Cluster status
cmd_status() {
    log_info "Cluster Status"
    echo ""
    
    log_info "Cluster Info:"
    kubectl cluster-info
    
    echo ""
    log_info "Node Status:"
    kubectl get nodes
    
    echo ""
    log_info "Namespace Summary:"
    kubectl get namespaces
    
    echo ""
    log_info "Top Resource Consumers:"
    kubectl top nodes 2>/dev/null || log_info "Metrics server not available"
}

# Display metrics
cmd_metrics() {
    log_info "Cluster Metrics"
    echo ""
    
    if kubectl top nodes &> /dev/null; then
        log_info "Node Resource Usage:"
        kubectl top nodes
        
        echo ""
        log_info "Pod Resource Usage (ops namespace):"
        kubectl top pods -n ops
    else
        log_info "Metrics server not available. Install with:"
        echo "  kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml"
    fi
}

# Test API endpoint
cmd_api_test() {
    local vpn_ip="${VPN_IP:-localhost}"
    local api_port="${API_PORT:-30000}"
    
    log_info "Testing API endpoint at http://${vpn_ip}:${api_port}"
    
    echo ""
    log_info "Health check:"
    curl -v "http://${vpn_ip}:${api_port}/health" 2>&1 | grep -E "(HTTP|Connected)"
    
    echo ""
    log_info "API version:"
    curl -s "http://${vpn_ip}:${api_port}/api/version" | jq . || echo "No JSON response"
}

# Port forwarding
cmd_port_forward() {
    local pod="$1"
    local port="$2"
    local local_port="${3:-$port}"
    local namespace="${4:-ops}"
    
    log_info "Forwarding port $port from $pod to localhost:$local_port"
    log_cmd "kubectl port-forward $pod -n $namespace $local_port:$port"
    kubectl port-forward "$pod" -n "$namespace" "$local_port:$port"
}

# Main command router
main() {
    if [[ $# -eq 0 ]]; then
        usage
        exit 1
    fi
    
    local command="$1"
    shift
    
    case "$command" in
        pods)
            cmd_pods "$@"
            ;;
        logs)
            cmd_logs "$@"
            ;;
        exec)
            cmd_exec "$@"
            ;;
        services)
            cmd_services "$@"
            ;;
        status)
            cmd_status
            ;;
        metrics)
            cmd_metrics
            ;;
        api-test)
            cmd_api_test
            ;;
        port-forward)
            cmd_port_forward "$@"
            ;;
        help|--help|-h)
            usage
            ;;
        *)
            echo "Unknown command: $command"
            usage
            exit 1
            ;;
    esac
}

main "$@"
