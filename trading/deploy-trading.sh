#!/bin/bash
# Trading Arsenal Deployment Script
# StrategicKhaos DAO LLC - Production Ready Trading System

set -e
set -u

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
TRADING_DIR="$PROJECT_ROOT/trading"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    local missing=()
    
    command -v docker >/dev/null 2>&1 || missing+=("docker")
    command -v docker-compose >/dev/null 2>&1 || missing+=("docker-compose")
    
    if [ ${#missing[@]} -ne 0 ]; then
        log_error "Missing dependencies: ${missing[*]}"
        exit 1
    fi
    
    if ! docker info >/dev/null 2>&1; then
        log_error "Docker daemon is not running"
        exit 1
    fi
    
    log_success "Prerequisites satisfied"
}

# Load environment
load_environment() {
    log_info "Loading environment..."
    
    if [ -f "$PROJECT_ROOT/.env" ]; then
        source "$PROJECT_ROOT/.env"
        log_info "Loaded .env configuration"
    fi
    
    # Set defaults
    export TRADING_ENV="${TRADING_ENV:-development}"
    export PAPER_TRADING="${PAPER_TRADING:-true}"
    export EXECUTION_ENABLED="${EXECUTION_ENABLED:-false}"
    export AUTO_START_AUTONOMOUS="${AUTO_START_AUTONOMOUS:-false}"
    
    log_success "Environment loaded (TRADING_ENV=$TRADING_ENV, PAPER_TRADING=$PAPER_TRADING)"
}

# Build images
build_images() {
    log_info "Building Trading Arsenal Docker images..."
    
    cd "$PROJECT_ROOT"
    
    docker build -f Dockerfile.trading -t trading-arsenal:latest .
    
    if [ $? -eq 0 ]; then
        log_success "Trading Arsenal image built successfully"
    else
        log_error "Failed to build Trading Arsenal image"
        exit 1
    fi
}

# Deploy with Docker Compose
deploy_docker() {
    log_info "Deploying Trading Arsenal with Docker Compose..."
    
    cd "$TRADING_DIR"
    
    # Stop existing services
    docker-compose -f docker-compose.trading.yml down || true
    
    # Start services
    docker-compose -f docker-compose.trading.yml up -d
    
    if [ $? -eq 0 ]; then
        log_success "Trading Arsenal deployed successfully"
    else
        log_error "Failed to deploy Trading Arsenal"
        exit 1
    fi
    
    # Wait for health
    log_info "Waiting for services to be healthy..."
    sleep 15
    
    check_health
}

# Check service health
check_health() {
    log_info "Checking service health..."
    
    local max_attempts=30
    local attempt=0
    
    while [ $attempt -lt $max_attempts ]; do
        if curl -sf http://localhost:8086/health >/dev/null 2>&1; then
            log_success "Trading API is healthy"
            return 0
        fi
        
        attempt=$((attempt + 1))
        sleep 2
    done
    
    log_warning "Health check timed out"
}

# Deploy to Kubernetes
deploy_k8s() {
    log_info "Deploying Trading Arsenal to Kubernetes..."
    
    if ! command -v kubectl >/dev/null 2>&1; then
        log_error "kubectl not found"
        exit 1
    fi
    
    if ! kubectl cluster-info >/dev/null 2>&1; then
        log_error "Cannot connect to Kubernetes cluster"
        exit 1
    fi
    
    cd "$TRADING_DIR/k8s"
    
    kubectl apply -f configmap.yaml
    kubectl apply -f deployment.yaml
    kubectl apply -f ingress.yaml
    kubectl apply -f autoscaling.yaml
    
    # Wait for deployment
    log_info "Waiting for deployment to be ready..."
    kubectl wait --for=condition=available --timeout=300s deployment/trading-api -n trading
    
    log_success "Kubernetes deployment completed"
}

# Show status
show_status() {
    echo
    log_success "🚀 Trading Arsenal Deployed!"
    echo
    echo "📋 Service Endpoints:"
    echo "  • Trading API:      http://localhost:8086"
    echo "  • API Docs:         http://localhost:8086/docs"
    echo "  • Metrics:          http://localhost:8086/metrics"
    echo "  • Prometheus:       http://localhost:9091"
    echo "  • Grafana:          http://localhost:3003"
    echo
    echo "🤖 API Endpoints:"
    echo "  • GET  /health           - Health check"
    echo "  • GET  /status           - System status"
    echo "  • GET  /algorithms       - Algorithm status"
    echo "  • POST /cycle            - Run signal cycle"
    echo "  • POST /autonomous/start - Start autonomous mode"
    echo "  • POST /autonomous/stop  - Stop autonomous mode"
    echo "  • GET  /alerts           - Active alerts"
    echo "  • GET  /performance      - Performance metrics"
    echo
    echo "📊 Trading Arsenal Configuration:"
    echo "  • Tier 0 Algos:     5 (80%+ readiness)"
    echo "  • Tier 1 Algos:     4 (70-80% readiness)"
    echo "  • Target Yield:     7% annualized"
    echo "  • Max Drawdown:     20%"
    echo "  • Paper Trading:    $PAPER_TRADING"
    echo "  • Execution:        $EXECUTION_ENABLED"
    echo
    echo "🔧 Management Commands:"
    echo "  • View logs:   docker-compose -f $TRADING_DIR/docker-compose.trading.yml logs -f"
    echo "  • Stop:        docker-compose -f $TRADING_DIR/docker-compose.trading.yml down"
    echo "  • Restart:     docker-compose -f $TRADING_DIR/docker-compose.trading.yml restart"
    echo
}

# Cleanup
cleanup() {
    log_info "Cleaning up Trading Arsenal deployment..."
    
    cd "$TRADING_DIR"
    docker-compose -f docker-compose.trading.yml down --volumes --remove-orphans
    
    log_success "Cleanup completed"
}

# Main
main() {
    echo
    echo "🚀 Trading Arsenal Deployment"
    echo "=============================="
    echo "StrategicKhaos DAO LLC"
    echo
    
    local command="${1:-docker}"
    
    case "$command" in
        "docker"|"compose")
            check_prerequisites
            load_environment
            build_images
            deploy_docker
            show_status
            ;;
        "k8s"|"kubernetes")
            check_prerequisites
            load_environment
            deploy_k8s
            ;;
        "build")
            check_prerequisites
            build_images
            ;;
        "status")
            check_health
            ;;
        "cleanup"|"clean")
            cleanup
            ;;
        "help"|"-h"|"--help")
            echo "Usage: $0 [command]"
            echo
            echo "Commands:"
            echo "  docker      Deploy with Docker Compose (default)"
            echo "  kubernetes  Deploy to Kubernetes"
            echo "  build       Build Docker images only"
            echo "  status      Check service health"
            echo "  cleanup     Remove deployment"
            echo
            ;;
        *)
            log_error "Unknown command: $command"
            echo "Use '$0 help' for usage"
            exit 1
            ;;
    esac
}

main "$@"
