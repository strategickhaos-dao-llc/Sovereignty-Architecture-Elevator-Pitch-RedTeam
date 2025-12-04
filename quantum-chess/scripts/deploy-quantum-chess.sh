#!/bin/bash
# deploy-quantum-chess.sh
# Quantum Chess Wargame Simulator Deployment Script
# Codename: Moonlight Sunshine Matrix Prototype Sovereign

set -e

# Colors for output
RED='\033[0;31m'
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Configuration
QUANTUM_CHESS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NAMESPACE="${QUANTUM_CHESS_NAMESPACE:-quantum-chess}"
RED_TEAM_ZONE="${RED_TEAM_ZONE:-us-central1-a}"
BLUE_TEAM_ZONE="${BLUE_TEAM_ZONE:-us-central1-b}"
NODE_COUNT="${NODE_COUNT:-3}"
MACHINE_TYPE="${MACHINE_TYPE:-n1-standard-2}"

echo -e "${PURPLE}♟️  QUANTUM CHESS WARGAME SIMULATOR${NC}"
echo -e "${PURPLE}==================================================${NC}"
echo ""
echo -e "   ${YELLOW}10-Dimensional Attack/Defense Security Game${NC}"
echo -e "   ${YELLOW}Codename: Moonlight Sunshine Matrix Prototype Sovereign${NC}"
echo ""

print_step() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[ℹ]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[⚠]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Function to check prerequisites
check_prerequisites() {
    echo -e "${BLUE}Checking prerequisites...${NC}"
    
    local missing_tools=()
    
    if ! command -v kubectl &> /dev/null; then
        missing_tools+=("kubectl")
    fi
    
    if ! command -v helm &> /dev/null; then
        missing_tools+=("helm")
    fi
    
    if [ ${#missing_tools[@]} -gt 0 ]; then
        print_warning "Some tools are not installed: ${missing_tools[*]}"
        print_info "Install them to use full features, or use Docker Compose for local deployment"
    else
        print_step "All prerequisites met"
    fi
}

# Function to deploy using Docker Compose (local development)
deploy_local() {
    echo ""
    echo -e "${PURPLE}🐳 DEPLOYING LOCAL ENVIRONMENT (Docker Compose)${NC}"
    echo -e "${PURPLE}--------------------------------------------------${NC}"
    echo ""
    
    # Check if docker-compose is available
    if ! command -v docker &> /dev/null && ! command -v docker-compose &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    print_info "Starting local Quantum Chess environment..."
    
    # Navigate to the root directory and start services
    cd "${QUANTUM_CHESS_DIR}/.."
    
    # Create docker-compose override for quantum-chess
    cat > docker-compose.quantum-chess.yml << 'EOF'
version: '3.8'

networks:
  quantum-chess-network:
    driver: bridge

services:
  # NATS JetStream - Quantum Entanglement Layer
  nats:
    image: nats:2.10-alpine
    container_name: quantum-chess-nats
    command: ["--js", "--cluster_name", "quantum-chess"]
    ports:
      - "4222:4222"
      - "8222:8222"
    networks:
      - quantum-chess-network
    healthcheck:
      test: ["CMD", "nats-server", "--signal", "health=1"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis - Move State & Pub/Sub
  redis:
    image: redis:7-alpine
    container_name: quantum-chess-redis
    ports:
      - "6380:6379"
    networks:
      - quantum-chess-network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Red Team Controller
  red-team-controller:
    image: alpine:latest
    container_name: quantum-chess-red-controller
    volumes:
      - ./quantum-chess:/quantum-chess:ro
    networks:
      - quantum-chess-network
    depends_on:
      nats:
        condition: service_healthy
      redis:
        condition: service_healthy
    command: ["tail", "-f", "/dev/null"]
    environment:
      - TEAM=red
      - NATS_URL=nats://nats:4222
      - REDIS_URL=redis://redis:6379

  # Blue Team Controller
  blue-team-controller:
    image: alpine:latest
    container_name: quantum-chess-blue-controller
    volumes:
      - ./quantum-chess:/quantum-chess:ro
    networks:
      - quantum-chess-network
    depends_on:
      nats:
        condition: service_healthy
      redis:
        condition: service_healthy
    command: ["tail", "-f", "/dev/null"]
    environment:
      - TEAM=blue
      - NATS_URL=nats://nats:4222
      - REDIS_URL=redis://redis:6379

  # Legion AI Analyzer
  legion-analyzer:
    image: alpine:latest
    container_name: quantum-chess-legion
    volumes:
      - ./quantum-chess:/quantum-chess:ro
    networks:
      - quantum-chess-network
    depends_on:
      nats:
        condition: service_healthy
      redis:
        condition: service_healthy
    command: ["tail", "-f", "/dev/null"]
    environment:
      - TEAM=legion
      - NATS_URL=nats://nats:4222
      - REDIS_URL=redis://redis:6379

  # Visualization Server
  quantum-chess-viz:
    image: nginx:alpine
    container_name: quantum-chess-viz
    ports:
      - "8090:80"
    volumes:
      - ./quantum-chess/docs:/usr/share/nginx/html:ro
    networks:
      - quantum-chess-network
    healthcheck:
      test: ["CMD", "wget", "-q", "--spider", "http://localhost:80"]
      interval: 10s
      timeout: 5s
      retries: 5
EOF

    print_step "Created docker-compose.quantum-chess.yml"
    
    # Start the services
    if command -v docker &> /dev/null; then
        docker compose -f docker-compose.quantum-chess.yml up -d
    else
        docker-compose -f docker-compose.quantum-chess.yml up -d
    fi
    
    print_step "Started local Quantum Chess environment"
    
    echo ""
    echo -e "${GREEN}✅ LOCAL QUANTUM CHESS DEPLOYED!${NC}"
    echo ""
    echo -e "🎮 Services:"
    echo -e "   ${BLUE}NATS (Quantum Entanglement):${NC} localhost:4222 (monitoring: localhost:8222)"
    echo -e "   ${BLUE}Redis (State Store):${NC}        localhost:6380"
    echo -e "   ${RED}Red Team Controller:${NC}        quantum-chess-red-controller"
    echo -e "   ${BLUE}Blue Team Controller:${NC}       quantum-chess-blue-controller"
    echo -e "   ${PURPLE}Legion AI Analyzer:${NC}         quantum-chess-legion"
    echo -e "   ${GREEN}Visualization:${NC}              http://localhost:8090"
    echo ""
}

# Function to deploy Red Team Cluster (Kali)
deploy_red_team() {
    echo ""
    echo -e "${RED}🔴 DEPLOYING RED TEAM (Kali Linux Cluster)${NC}"
    echo -e "${RED}--------------------------------------------${NC}"
    echo ""
    
    if command -v gcloud &> /dev/null; then
        print_info "Creating Red Team GKE cluster..."
        gcloud container clusters create red-team-kali \
            --zone "${RED_TEAM_ZONE}" \
            --num-nodes "${NODE_COUNT}" \
            --machine-type "${MACHINE_TYPE}" \
            --enable-network-policy \
            --labels="team=red,purpose=offensive-security" \
            || print_warning "Red team cluster may already exist"
    else
        print_warning "gcloud not available - skipping GKE cluster creation"
        print_info "Using kubectl to apply Kubernetes manifests instead..."
    fi
    
    # Apply Red Team Kubernetes manifests
    if [ -d "${QUANTUM_CHESS_DIR}/k8s/red-team" ]; then
        kubectl apply -f "${QUANTUM_CHESS_DIR}/k8s/red-team/" --context="${RED_CONTEXT:-}" 2>/dev/null || \
            kubectl apply -f "${QUANTUM_CHESS_DIR}/k8s/red-team/" 2>/dev/null || true
    fi
    
    print_step "Red Team cluster configured"
}

# Function to deploy Blue Team Cluster (Parrot)
deploy_blue_team() {
    echo ""
    echo -e "${BLUE}🔵 DEPLOYING BLUE TEAM (Parrot OS Cluster)${NC}"
    echo -e "${BLUE}--------------------------------------------${NC}"
    echo ""
    
    if command -v gcloud &> /dev/null; then
        print_info "Creating Blue Team GKE cluster..."
        gcloud container clusters create blue-team-parrot \
            --zone "${BLUE_TEAM_ZONE}" \
            --num-nodes "${NODE_COUNT}" \
            --machine-type "${MACHINE_TYPE}" \
            --enable-network-policy \
            --labels="team=blue,purpose=defensive-security" \
            || print_warning "Blue team cluster may already exist"
    else
        print_warning "gcloud not available - skipping GKE cluster creation"
        print_info "Using kubectl to apply Kubernetes manifests instead..."
    fi
    
    # Apply Blue Team Kubernetes manifests
    if [ -d "${QUANTUM_CHESS_DIR}/k8s/blue-team" ]; then
        kubectl apply -f "${QUANTUM_CHESS_DIR}/k8s/blue-team/" --context="${BLUE_CONTEXT:-}" 2>/dev/null || \
            kubectl apply -f "${QUANTUM_CHESS_DIR}/k8s/blue-team/" 2>/dev/null || true
    fi
    
    print_step "Blue Team cluster configured"
}

# Function to deploy NATS (Quantum Entanglement Layer)
deploy_nats() {
    echo ""
    echo -e "${PURPLE}⚡ DEPLOYING NATS QUANTUM ENTANGLEMENT LAYER${NC}"
    echo -e "${PURPLE}----------------------------------------------${NC}"
    echo ""
    
    # Create namespace
    kubectl create namespace "${NAMESPACE}" 2>/dev/null || true
    
    # Check if Helm is available
    if command -v helm &> /dev/null; then
        print_info "Installing NATS via Helm..."
        
        # Add NATS Helm repository
        helm repo add nats https://nats-io.github.io/k8s/helm/charts/ 2>/dev/null || true
        helm repo update
        
        # Install NATS with JetStream enabled
        helm upgrade --install nats nats/nats \
            --namespace "${NAMESPACE}" \
            --set cluster.enabled=true \
            --set cluster.replicas=3 \
            --set jetstream.enabled=true \
            --set jetstream.memoryStore.enabled=true \
            --set jetstream.memoryStore.size=1Gi \
            --set jetstream.fileStore.enabled=true \
            --set jetstream.fileStore.size=10Gi \
            || print_warning "NATS installation may already exist"
    else
        print_warning "Helm not available - applying NATS Kubernetes manifests directly"
        kubectl apply -f "${QUANTUM_CHESS_DIR}/k8s/nats/" -n "${NAMESPACE}" 2>/dev/null || true
    fi
    
    print_step "NATS quantum entanglement layer configured"
}

# Function to deploy visualization layer
deploy_visualization() {
    echo ""
    echo -e "${GREEN}👁️  DEPLOYING VISUALIZATION LAYER${NC}"
    echo -e "${GREEN}------------------------------------${NC}"
    echo ""
    
    if [ -d "${QUANTUM_CHESS_DIR}/k8s/visualization" ]; then
        kubectl apply -f "${QUANTUM_CHESS_DIR}/k8s/visualization/" -n "${NAMESPACE}" 2>/dev/null || true
    fi
    
    print_step "Visualization layer configured"
}

# Function to deploy AI agents
deploy_agents() {
    echo ""
    echo -e "${YELLOW}🤖 DEPLOYING AI AGENTS${NC}"
    echo -e "${YELLOW}------------------------${NC}"
    echo ""
    
    # Deploy Red Team agents
    if [ -d "${QUANTUM_CHESS_DIR}/agents/red-team" ]; then
        print_info "Deploying Red Team agents..."
        for agent in "${QUANTUM_CHESS_DIR}"/agents/red-team/*.yaml; do
            [ -f "$agent" ] && kubectl apply -f "$agent" --context="${RED_CONTEXT:-}" 2>/dev/null || true
        done
    fi
    
    # Deploy Blue Team agents
    if [ -d "${QUANTUM_CHESS_DIR}/agents/blue-team" ]; then
        print_info "Deploying Blue Team agents..."
        for agent in "${QUANTUM_CHESS_DIR}"/agents/blue-team/*.yaml; do
            [ -f "$agent" ] && kubectl apply -f "$agent" --context="${BLUE_CONTEXT:-}" 2>/dev/null || true
        done
    fi
    
    print_step "AI agents deployed"
}

# Function to start the simulation
start_simulation() {
    echo ""
    echo -e "${PURPLE}♟️  STARTING QUANTUM CHESS SIMULATION${NC}"
    echo -e "${PURPLE}----------------------------------------${NC}"
    echo ""
    
    # Start port forwarding for visualization (if in K8s mode)
    if command -v kubectl &> /dev/null; then
        kubectl port-forward -n "${NAMESPACE}" svc/visualization 8080:8080 &>/dev/null &
        VIZ_PID=$!
        echo "${VIZ_PID}" > /tmp/quantum-chess-viz.pid
        print_info "Visualization port-forwarding started (PID: ${VIZ_PID})"
    fi
    
    print_step "Simulation environment ready"
}

# Function to show status
show_status() {
    echo ""
    echo -e "${GREEN}✅ QUANTUM CHESS WARGAME SIMULATOR DEPLOYED!${NC}"
    echo ""
    echo -e "${PURPLE}┌─────────────────────────────────────────────────────────────┐${NC}"
    echo -e "${PURPLE}│           QUANTUM CHESS WARGAME SIMULATOR                     │${NC}"
    echo -e "${PURPLE}│          (10-Dimensional Attack/Defense Game)                │${NC}"
    echo -e "${PURPLE}└─────────────────────────────────────────────────────────────┘${NC}"
    echo ""
    echo -e "🎮 ${GREEN}Visualization:${NC} http://localhost:8080"
    echo -e "🔴 ${RED}Red Team:${NC}      gke_red-team-kali (Offensive AI Agents)"
    echo -e "🔵 ${BLUE}Blue Team:${NC}     gke_blue-team-parrot (Defensive AI Agents)"
    echo -e "⚡ ${YELLOW}Entanglement:${NC}  NATS cluster in ${NAMESPACE} namespace"
    echo ""
    echo -e "${PURPLE}Watch the wargame unfold in real-time! 🔥${NC}"
    echo ""
}

# Function to stop local deployment
stop_local() {
    echo -e "${YELLOW}Stopping local Quantum Chess environment...${NC}"
    cd "${QUANTUM_CHESS_DIR}/.."
    
    if command -v docker &> /dev/null; then
        docker compose -f docker-compose.quantum-chess.yml down
    else
        docker-compose -f docker-compose.quantum-chess.yml down
    fi
    
    print_step "Local environment stopped"
}

# Function to show help
show_help() {
    echo ""
    echo -e "${PURPLE}Quantum Chess Wargame Simulator - Deployment Script${NC}"
    echo ""
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  local        Deploy local development environment (Docker Compose)"
    echo "  stop-local   Stop local development environment"
    echo "  full         Deploy full Kubernetes environment (GKE)"
    echo "  red-team     Deploy only Red Team cluster"
    echo "  blue-team    Deploy only Blue Team cluster"
    echo "  nats         Deploy only NATS entanglement layer"
    echo "  agents       Deploy only AI agents"
    echo "  viz          Deploy only visualization layer"
    echo "  status       Show deployment status"
    echo "  help         Show this help message"
    echo ""
    echo "Environment Variables:"
    echo "  QUANTUM_CHESS_NAMESPACE  Kubernetes namespace (default: quantum-chess)"
    echo "  RED_TEAM_ZONE            GKE zone for Red Team (default: us-central1-a)"
    echo "  BLUE_TEAM_ZONE           GKE zone for Blue Team (default: us-central1-b)"
    echo "  NODE_COUNT               Number of nodes per cluster (default: 3)"
    echo "  MACHINE_TYPE             GKE machine type (default: n1-standard-2)"
    echo ""
}

# Main execution
main() {
    check_prerequisites
    
    case "${1:-local}" in
        local)
            deploy_local
            ;;
        stop-local|stop)
            stop_local
            ;;
        full)
            deploy_red_team
            deploy_blue_team
            deploy_nats
            deploy_visualization
            deploy_agents
            start_simulation
            show_status
            ;;
        red-team|red)
            deploy_red_team
            ;;
        blue-team|blue)
            deploy_blue_team
            ;;
        nats)
            deploy_nats
            ;;
        agents)
            deploy_agents
            ;;
        viz|visualization)
            deploy_visualization
            ;;
        status)
            show_status
            ;;
        help|-h|--help)
            show_help
            ;;
        *)
            echo -e "${RED}Unknown command: $1${NC}"
            show_help
            exit 1
            ;;
    esac
}

main "$@"
