#!/bin/bash
# ═══════════════════════════════════════════════════════════
# 10D Chess Council - Deployment Script
# Deploy 640 LLM agents to Kubernetes cluster
# ═══════════════════════════════════════════════════════════

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NAMESPACE="chess-council"
K8S_DIR="${SCRIPT_DIR}/bootstrap/k8s/chess-council"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

print_banner() {
    echo ""
    echo "═══════════════════════════════════════════════════════════"
    echo " 10-DIMENSIONAL CHESS COUNCIL"
    echo " AI Research Super-Collider Architecture"
    echo " 640 Containerized LLM Agents"
    echo "═══════════════════════════════════════════════════════════"
    echo ""
}

usage() {
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  deploy      Deploy all chess council components"
    echo "  status      Check deployment status"
    echo "  logs        View logs from agents"
    echo "  scale       Scale number of agents"
    echo "  delete      Remove chess council deployment"
    echo "  generate    Generate StatefulSet manifests for all boards"
    echo "  local       Start local development environment"
    echo ""
    echo "Examples:"
    echo "  $0 deploy"
    echo "  $0 status"
    echo "  $0 logs chess-board-4-27"
    echo "  $0 scale 128"
    echo ""
}

check_prerequisites() {
    log_info "Checking prerequisites..."
    
    if ! command -v kubectl &> /dev/null; then
        log_error "kubectl is not installed"
        exit 1
    fi
    
    if ! kubectl cluster-info &> /dev/null; then
        log_error "Cannot connect to Kubernetes cluster"
        exit 1
    fi
    
    log_success "Prerequisites satisfied"
}

generate_boards() {
    log_info "Generating StatefulSet manifests for all 10 boards..."
    
    if [ -f "${SCRIPT_DIR}/generate-chess-boards.sh" ]; then
        bash "${SCRIPT_DIR}/generate-chess-boards.sh"
        log_success "Generated manifests for 640 agents"
    else
        log_error "generate-chess-boards.sh not found"
        exit 1
    fi
}

deploy_namespace() {
    log_info "Creating namespace and core resources..."
    kubectl apply -f "${K8S_DIR}/namespace-and-config.yaml"
    log_success "Namespace ${NAMESPACE} created"
}

deploy_supporting_services() {
    log_info "Deploying supporting services (Ollama, Qdrant, PostgreSQL, Stockfish)..."
    kubectl apply -f "${K8S_DIR}/supporting-services.yaml"
    
    log_info "Waiting for supporting services to be ready..."
    kubectl wait --namespace "${NAMESPACE}" \
        --for=condition=ready pod \
        --selector=app=ollama-service \
        --timeout=300s || log_warn "Ollama not ready yet"
    
    kubectl wait --namespace "${NAMESPACE}" \
        --for=condition=ready pod \
        --selector=app=qdrant \
        --timeout=300s || log_warn "Qdrant not ready yet"
    
    kubectl wait --namespace "${NAMESPACE}" \
        --for=condition=ready pod \
        --selector=app=postgres \
        --timeout=300s || log_warn "PostgreSQL not ready yet"
    
    log_success "Supporting services deployed"
}

deploy_agents() {
    log_info "Deploying 640 chess agents (10 boards × 64 agents)..."
    
    # Deploy each board
    for board in {0..9}; do
        manifest="${K8S_DIR}/board-${board}-statefulset.yaml"
        if [ -f "$manifest" ]; then
            log_info "Deploying board ${board}..."
            kubectl apply -f "$manifest"
        else
            log_warn "Manifest for board ${board} not found, generating..."
            generate_boards
            kubectl apply -f "$manifest"
        fi
    done
    
    log_success "All agent boards deployed"
}

deploy_hpa_policies() {
    log_info "Deploying HPA and network policies..."
    kubectl apply -f "${K8S_DIR}/hpa-and-policies.yaml"
    log_success "HPA and policies configured"
}

full_deploy() {
    print_banner
    check_prerequisites
    generate_boards
    deploy_namespace
    deploy_supporting_services
    deploy_agents
    deploy_hpa_policies
    
    echo ""
    log_success "═══════════════════════════════════════════════════════════"
    log_success " 10D Chess Council Deployment Complete!"
    log_success "═══════════════════════════════════════════════════════════"
    echo ""
    echo "Next steps:"
    echo "  1. Check status:     $0 status"
    echo "  2. View agent logs:  $0 logs chess-board-4-27"
    echo "  3. Pull Ollama model: kubectl exec -n ${NAMESPACE} deploy/ollama-service -- ollama pull qwen2.5:72b"
    echo ""
}

check_status() {
    print_banner
    
    echo "Namespace: ${NAMESPACE}"
    echo ""
    
    echo "═══════════════════════════════════════════════════════════"
    echo " Pods Status"
    echo "═══════════════════════════════════════════════════════════"
    kubectl get pods -n "${NAMESPACE}" -o wide
    
    echo ""
    echo "═══════════════════════════════════════════════════════════"
    echo " StatefulSets Status"
    echo "═══════════════════════════════════════════════════════════"
    kubectl get statefulsets -n "${NAMESPACE}"
    
    echo ""
    echo "═══════════════════════════════════════════════════════════"
    echo " Services"
    echo "═══════════════════════════════════════════════════════════"
    kubectl get services -n "${NAMESPACE}"
    
    echo ""
    echo "═══════════════════════════════════════════════════════════"
    echo " Resource Usage"
    echo "═══════════════════════════════════════════════════════════"
    kubectl top pods -n "${NAMESPACE}" 2>/dev/null || echo "Metrics server not available"
    
    # Count total agents
    total=$(kubectl get pods -n "${NAMESPACE}" -l app=chess-agent --no-headers 2>/dev/null | wc -l)
    ready=$(kubectl get pods -n "${NAMESPACE}" -l app=chess-agent --no-headers 2>/dev/null | grep -c "Running" || echo "0")
    
    echo ""
    echo "═══════════════════════════════════════════════════════════"
    echo " Summary: ${ready}/${total} agents running"
    echo "═══════════════════════════════════════════════════════════"
}

view_logs() {
    local agent_name="${1:-}"
    
    if [ -z "$agent_name" ]; then
        log_info "Showing logs from game orchestrator..."
        kubectl logs -n "${NAMESPACE}" -f deploy/game-orchestrator --tail=100
    else
        log_info "Showing logs from ${agent_name}..."
        kubectl logs -n "${NAMESPACE}" -f "pod/${agent_name}" --tail=100
    fi
}

scale_agents() {
    local replicas="${1:-64}"
    
    log_info "Scaling all boards to ${replicas} agents each..."
    
    for board in {0..9}; do
        kubectl scale statefulset "chess-board-${board}" \
            -n "${NAMESPACE}" \
            --replicas="${replicas}"
    done
    
    total=$((replicas * 10))
    log_success "Scaled to ${total} total agents (${replicas} per board)"
}

delete_deployment() {
    log_warn "This will delete all chess council resources!"
    read -p "Are you sure? (yes/no): " confirm
    
    if [ "$confirm" = "yes" ]; then
        log_info "Deleting chess council namespace..."
        kubectl delete namespace "${NAMESPACE}" --timeout=300s
        log_success "Chess council deleted"
    else
        log_info "Deletion cancelled"
    fi
}

start_local() {
    log_info "Starting local development environment..."
    
    if ! command -v docker-compose &> /dev/null && ! command -v docker &> /dev/null; then
        log_error "Docker is not installed"
        exit 1
    fi
    
    # Use docker compose (v2) or docker-compose (v1)
    if command -v docker &> /dev/null && docker compose version &> /dev/null; then
        docker compose -f docker-compose.chess-council.yml up -d
    else
        docker-compose -f docker-compose.chess-council.yml up -d
    fi
    
    log_success "Local environment started"
    echo ""
    echo "Services:"
    echo "  - Ollama:       http://localhost:11434"
    echo "  - Qdrant:       http://localhost:6333"
    echo "  - PostgreSQL:   localhost:5432"
    echo "  - Orchestrator: http://localhost:8081"
    echo "  - Agent (dev):  http://localhost:8082"
    echo "  - Prometheus:   http://localhost:9090"
    echo "  - Grafana:      http://localhost:3001"
    echo ""
}

# Main entry point
case "${1:-}" in
    deploy)
        full_deploy
        ;;
    status)
        check_status
        ;;
    logs)
        view_logs "${2:-}"
        ;;
    scale)
        scale_agents "${2:-64}"
        ;;
    delete)
        delete_deployment
        ;;
    generate)
        generate_boards
        ;;
    local)
        start_local
        ;;
    *)
        usage
        exit 1
        ;;
esac
