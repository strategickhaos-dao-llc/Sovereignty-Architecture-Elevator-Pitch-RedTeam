#!/bin/bash
# deploy-quantum-chess.sh
# Quantum Chess Wargame Simulator Deployment Script
# Part of Strategickhaos Sovereignty Architecture

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NAMESPACE_QUANTUM="quantum-chess"
NAMESPACE_RED="red-team"
NAMESPACE_BLUE="blue-team"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_banner() {
    echo -e "${PURPLE}"
    echo "♟️  ═══════════════════════════════════════════════════════════════════"
    echo "    QUANTUM CHESS WARGAME SIMULATOR"
    echo "    Moonlight Sunshine Matrix Prototype Sovereign"
    echo "    10-Dimensional Attack/Defense Game"
    echo "═══════════════════════════════════════════════════════════════════════${NC}"
    echo ""
}

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_red() {
    echo -e "${RED}[RED TEAM]${NC} $1"
}

log_blue() {
    echo -e "${BLUE}[BLUE TEAM]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    if ! command -v kubectl &> /dev/null; then
        log_error "kubectl is required but not installed."
        exit 1
    fi
    
    if ! command -v helm &> /dev/null; then
        log_warn "helm not found. NATS deployment will use kubectl apply."
    fi
    
    log_info "Prerequisites check passed ✓"
}

# Create namespaces
create_namespaces() {
    log_info "Creating namespaces..."
    
    kubectl apply -f "${SCRIPT_DIR}/k8s/nats/namespace.yaml" 2>/dev/null || true
    kubectl apply -f "${SCRIPT_DIR}/k8s/red-team/namespace.yaml" 2>/dev/null || true
    kubectl apply -f "${SCRIPT_DIR}/k8s/blue-team/namespace.yaml" 2>/dev/null || true
    
    log_info "Namespaces created ✓"
}

# Deploy NATS for quantum entanglement
deploy_nats() {
    log_info "⚡ Deploying NATS quantum entanglement layer..."
    
    if command -v helm &> /dev/null; then
        # Add NATS Helm repo if not exists
        helm repo add nats https://nats-io.github.io/k8s/helm/charts/ 2>/dev/null || true
        helm repo update
        
        # Install NATS with JetStream enabled
        helm upgrade --install nats nats/nats \
            --namespace "${NAMESPACE_QUANTUM}" \
            --set cluster.enabled=true \
            --set cluster.replicas=3 \
            --set jetstream.enabled=true \
            --set jetstream.fileStore.enabled=true \
            --wait --timeout 300s || {
            log_warn "Helm install failed, falling back to kubectl"
            kubectl apply -f "${SCRIPT_DIR}/k8s/nats/"
        }
    else
        kubectl apply -f "${SCRIPT_DIR}/k8s/nats/"
    fi
    
    log_info "NATS quantum entanglement layer deployed ✓"
}

# Deploy Red Team cluster
deploy_red_team() {
    log_red "🔴 Deploying Red Team (Kali Linux) cluster..."
    
    kubectl apply -f "${SCRIPT_DIR}/k8s/red-team/"
    kubectl apply -f "${SCRIPT_DIR}/agents/red-team/"
    
    log_red "Red Team cluster deployed ✓"
}

# Deploy Blue Team cluster
deploy_blue_team() {
    log_blue "🔵 Deploying Blue Team (Parrot OS) cluster..."
    
    kubectl apply -f "${SCRIPT_DIR}/k8s/blue-team/"
    kubectl apply -f "${SCRIPT_DIR}/agents/blue-team/"
    
    log_blue "Blue Team cluster deployed ✓"
}

# Deploy visualization layer
deploy_visualization() {
    log_info "👁️  Deploying visualization layer..."
    
    kubectl apply -f "${SCRIPT_DIR}/k8s/visualization/"
    
    log_info "Visualization layer deployed ✓"
}

# Start port forwarding for local access
start_port_forward() {
    log_info "Starting port forwarding for local access..."
    
    # Kill existing port forwards
    pkill -f "kubectl port-forward.*quantum-chess" 2>/dev/null || true
    
    # Start new port forwards in background
    kubectl port-forward -n "${NAMESPACE_QUANTUM}" svc/visualization 8080:8080 &
    kubectl port-forward -n "${NAMESPACE_QUANTUM}" svc/nats 4222:4222 &
    
    log_info "Port forwarding started ✓"
}

# Print status
print_status() {
    echo ""
    echo -e "${PURPLE}═══════════════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}✅ QUANTUM CHESS WARGAME SIMULATOR DEPLOYED!${NC}"
    echo -e "${PURPLE}═══════════════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "🎮 Visualization:     ${BLUE}http://localhost:8080${NC}"
    echo -e "🔴 Red Team:          ${RED}kubectl -n ${NAMESPACE_RED} get pods${NC}"
    echo -e "🔵 Blue Team:         ${BLUE}kubectl -n ${NAMESPACE_BLUE} get pods${NC}"
    echo -e "⚡ Entanglement:      ${PURPLE}nats://localhost:4222${NC}"
    echo ""
    echo -e "${YELLOW}Watch the wargame unfold in real-time 🔥${NC}"
    echo ""
}

# Help message
show_help() {
    echo "Quantum Chess Wargame Simulator Deployment"
    echo ""
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --all              Deploy all components (default)"
    echo "  --component NAME   Deploy specific component (red-team|blue-team|nats|viz)"
    echo "  --status           Show deployment status"
    echo "  --port-forward     Start port forwarding only"
    echo "  --clean            Remove all quantum chess deployments"
    echo "  -h, --help         Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                           # Deploy everything"
    echo "  $0 --component red-team      # Deploy red team only"
    echo "  $0 --status                  # Show current status"
}

# Show deployment status
show_status() {
    print_banner
    
    echo -e "${PURPLE}NATS Cluster:${NC}"
    kubectl get pods -n "${NAMESPACE_QUANTUM}" 2>/dev/null || echo "  Not deployed"
    echo ""
    
    echo -e "${RED}Red Team Pods:${NC}"
    kubectl get pods -n "${NAMESPACE_RED}" 2>/dev/null || echo "  Not deployed"
    echo ""
    
    echo -e "${BLUE}Blue Team Pods:${NC}"
    kubectl get pods -n "${NAMESPACE_BLUE}" 2>/dev/null || echo "  Not deployed"
    echo ""
}

# Clean up deployments
clean_up() {
    log_warn "Removing Quantum Chess deployments..."
    
    kubectl delete namespace "${NAMESPACE_QUANTUM}" 2>/dev/null || true
    kubectl delete namespace "${NAMESPACE_RED}" 2>/dev/null || true
    kubectl delete namespace "${NAMESPACE_BLUE}" 2>/dev/null || true
    
    log_info "Cleanup complete ✓"
}

# Main deployment function
deploy_all() {
    print_banner
    check_prerequisites
    create_namespaces
    deploy_nats
    deploy_red_team
    deploy_blue_team
    deploy_visualization
    print_status
}

# Parse command line arguments
COMPONENT=""
ACTION="all"

while [[ $# -gt 0 ]]; do
    case $1 in
        --all)
            ACTION="all"
            shift
            ;;
        --component)
            ACTION="component"
            COMPONENT="$2"
            shift 2
            ;;
        --status)
            ACTION="status"
            shift
            ;;
        --port-forward)
            ACTION="port-forward"
            shift
            ;;
        --clean)
            ACTION="clean"
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            log_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Execute based on action
case $ACTION in
    all)
        deploy_all
        ;;
    component)
        print_banner
        check_prerequisites
        case $COMPONENT in
            red-team)
                create_namespaces
                deploy_red_team
                ;;
            blue-team)
                create_namespaces
                deploy_blue_team
                ;;
            nats)
                create_namespaces
                deploy_nats
                ;;
            viz|visualization)
                create_namespaces
                deploy_visualization
                ;;
            *)
                log_error "Unknown component: $COMPONENT"
                exit 1
                ;;
        esac
        ;;
    status)
        show_status
        ;;
    port-forward)
        start_port_forward
        ;;
    clean)
        clean_up
        ;;
esac
