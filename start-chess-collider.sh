#!/bin/bash
# start-chess-collider.sh
# Launch the Chess Collider - 10-Dimensional AI Research Super-Collider
# Usage: ./start-chess-collider.sh [command] [options]
#
# Commands:
#   start     - Start the chess collider (default: 1 layer MVP)
#   stop      - Stop all chess collider services
#   status    - Show status of all services
#   logs      - Show logs from services
#   scale     - Scale to specified number of layers
#   full      - Start all 10 layers (640 agents)
#   mvp       - Start minimal viable product (1 layer, 64 agents)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE_FILE="$SCRIPT_DIR/docker-compose.chess-collider.yml"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Banner
print_banner() {
    echo -e "${CYAN}"
    cat << 'EOF'
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║     ♟️  CHESS COLLIDER - 10-DIMENSIONAL AI RESEARCH SUPER-COLLIDER  ♟️       ║
║                                                                              ║
║                    Sovereign AI Research Collective                          ║
║                    Strategickhaos DAO LLC                                    ║
║                                                                              ║
║    10 Boards × 64 Squares = 640 LLM Agents                                  ║
║    Frequency-Tuned Communication (Circle of 5ths)                           ║
║    Adversarial Knowledge Synthesis via Chess Games                          ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

# Show usage
usage() {
    echo -e "${YELLOW}Usage:${NC} $0 [command] [options]"
    echo ""
    echo -e "${GREEN}Commands:${NC}"
    echo "  start [layers]  Start chess collider with specified layers (default: 1)"
    echo "  stop            Stop all chess collider services"
    echo "  restart         Restart all services"
    echo "  status          Show status of all services"
    echo "  logs [service]  Show logs (optionally for specific service)"
    echo "  scale [layers]  Scale to specified number of layers (1-10)"
    echo "  full            Start all 10 layers (640 agents) - FULL POWER"
    echo "  mvp             Start minimal viable product (1 layer, 64 agents)"
    echo "  shell           Open shell in orchestrator container"
    echo "  research [topic] Start a new research task"
    echo "  game            Start an adversarial chess game between layers"
    echo ""
    echo -e "${GREEN}Options:${NC}"
    echo "  --local         Use local Ollama (\$3.5K/month)"
    echo "  --cloud         Use Grok API (\$22K-27K/month)"
    echo "  --dry-run       Show what would be done without executing"
    echo ""
    echo -e "${GREEN}Examples:${NC}"
    echo "  $0 start                    # Start MVP (1 layer)"
    echo "  $0 start 3                  # Start with 3 layers"
    echo "  $0 full                     # Start all 10 layers"
    echo "  $0 research 'AI alignment'  # Start research on AI alignment"
    echo "  $0 game                     # Start adversarial game"
    echo ""
    echo -e "${GREEN}Cost Estimates:${NC}"
    echo "  MVP (1 layer, 64 agents):    ~\$350/month"
    echo "  Full (10 layers, 640 agents): ~\$3,500/month (local)"
    echo "                               ~\$22,000-27,000/month (cloud)"
}

# Check prerequisites
check_prerequisites() {
    echo -e "${BLUE}Checking prerequisites...${NC}"
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}Error: Docker is not installed${NC}"
        exit 1
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        echo -e "${RED}Error: Docker Compose is not installed${NC}"
        exit 1
    fi
    
    # Check if compose file exists
    if [ ! -f "$COMPOSE_FILE" ]; then
        echo -e "${RED}Error: docker-compose.chess-collider.yml not found${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✓ Prerequisites check passed${NC}"
}

# Get docker compose command
get_compose_cmd() {
    if docker compose version &> /dev/null 2>&1; then
        echo "docker compose"
    else
        echo "docker-compose"
    fi
}

# Start services
start_services() {
    local layers=${1:-1}
    local mode=${2:-"local"}
    
    echo -e "${BLUE}Starting Chess Collider with ${layers} layer(s)...${NC}"
    
    # Set environment variables
    export ACTIVE_LAYERS=$layers
    export AGENTS_PER_LAYER=64
    
    # Calculate totals
    local total_agents=$((layers * 64))
    local monthly_cost=$((layers * 350))
    
    echo -e "${YELLOW}Configuration:${NC}"
    echo "  • Active Layers: $layers"
    echo "  • Total Agents: $total_agents"
    echo "  • Estimated Monthly Cost: \$${monthly_cost}"
    echo ""
    
    # Start core services
    $(get_compose_cmd) -f "$COMPOSE_FILE" up -d ollama qdrant-chess stockfish
    
    echo -e "${BLUE}Waiting for core services to be healthy...${NC}"
    sleep 10
    
    # Start orchestrator
    $(get_compose_cmd) -f "$COMPOSE_FILE" up -d orchestrator bibliography-service
    
    echo -e "${BLUE}Waiting for orchestrator...${NC}"
    sleep 5
    
    # Start layer coordinators based on active layers
    $(get_compose_cmd) -f "$COMPOSE_FILE" up -d layer-1-coordinator layer-1-workers
    
    if [ "$layers" -ge 2 ]; then
        $(get_compose_cmd) -f "$COMPOSE_FILE" --profile layer-2 up -d
    fi
    
    if [ "$layers" -ge 7 ]; then
        $(get_compose_cmd) -f "$COMPOSE_FILE" --profile layer-7 up -d
    fi
    
    if [ "$layers" -eq 10 ]; then
        $(get_compose_cmd) -f "$COMPOSE_FILE" --profile layer-10 up -d
    fi
    
    # Start monitoring
    $(get_compose_cmd) -f "$COMPOSE_FILE" up -d chess-prometheus chess-grafana
    
    echo ""
    echo -e "${GREEN}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║               CHESS COLLIDER ONLINE                           ║${NC}"
    echo -e "${GREEN}╠═══════════════════════════════════════════════════════════════╣${NC}"
    echo -e "${GREEN}║  Orchestrator API:  http://localhost:8090                     ║${NC}"
    echo -e "${GREEN}║  Grafana Dashboard: http://localhost:3001                     ║${NC}"
    echo -e "${GREEN}║  Prometheus:        http://localhost:9091                     ║${NC}"
    echo -e "${GREEN}║  Ollama LLM:        http://localhost:11434                    ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${CYAN}Quick commands:${NC}"
    echo "  • Check status:    curl http://localhost:8090/status"
    echo "  • Create research: curl -X POST http://localhost:8090/research/create -H 'Content-Type: application/json' -d '{\"topic\":\"AI safety\"}'"
    echo "  • Start game:      curl -X POST http://localhost:8090/games/start -H 'Content-Type: application/json' -d '{\"type\":\"research_battle\",\"layer1\":1,\"layer2\":2}'"
}

# Stop services
stop_services() {
    echo -e "${BLUE}Stopping Chess Collider...${NC}"
    $(get_compose_cmd) -f "$COMPOSE_FILE" down
    echo -e "${GREEN}Chess Collider stopped${NC}"
}

# Show status
show_status() {
    echo -e "${BLUE}Chess Collider Status:${NC}"
    $(get_compose_cmd) -f "$COMPOSE_FILE" ps
    
    echo ""
    echo -e "${BLUE}Orchestrator Health:${NC}"
    curl -s http://localhost:8090/health 2>/dev/null | jq . || echo "Orchestrator not responding"
    
    echo ""
    echo -e "${BLUE}Collider Status:${NC}"
    curl -s http://localhost:8090/status 2>/dev/null | jq . || echo "Orchestrator not responding"
}

# Show logs
show_logs() {
    local service=${1:-""}
    
    if [ -z "$service" ]; then
        $(get_compose_cmd) -f "$COMPOSE_FILE" logs -f
    else
        $(get_compose_cmd) -f "$COMPOSE_FILE" logs -f "$service"
    fi
}

# Scale layers
scale_layers() {
    local layers=${1:-1}
    
    if [ "$layers" -lt 1 ] || [ "$layers" -gt 10 ]; then
        echo -e "${RED}Error: Layers must be between 1 and 10${NC}"
        exit 1
    fi
    
    echo -e "${BLUE}Scaling Chess Collider to ${layers} layers...${NC}"
    
    # Update environment and restart
    export ACTIVE_LAYERS=$layers
    start_services "$layers"
}

# Open shell
open_shell() {
    echo -e "${BLUE}Opening shell in orchestrator...${NC}"
    docker exec -it chess-collider-orchestrator /bin/sh
}

# Start research task
start_research() {
    local topic=${1:-"AI research"}
    
    echo -e "${BLUE}Starting research task: ${topic}${NC}"
    
    curl -X POST http://localhost:8090/research/create \
        -H "Content-Type: application/json" \
        -d "{\"topic\":\"${topic}\"}" | jq .
}

# Start game
start_game() {
    local layer1=${1:-1}
    local layer2=${2:-2}
    local type=${3:-"research_battle"}
    
    echo -e "${BLUE}Starting ${type} between Layer ${layer1} and Layer ${layer2}...${NC}"
    
    curl -X POST http://localhost:8090/games/start \
        -H "Content-Type: application/json" \
        -d "{\"type\":\"${type}\",\"layer1\":${layer1},\"layer2\":${layer2}}" | jq .
}

# Main
main() {
    print_banner
    check_prerequisites
    
    local command=${1:-"help"}
    
    case "$command" in
        start)
            start_services "${2:-1}"
            ;;
        stop)
            stop_services
            ;;
        restart)
            stop_services
            sleep 2
            start_services "${2:-1}"
            ;;
        status)
            show_status
            ;;
        logs)
            show_logs "$2"
            ;;
        scale)
            scale_layers "${2:-1}"
            ;;
        full)
            start_services 10
            ;;
        mvp)
            start_services 1
            ;;
        shell)
            open_shell
            ;;
        research)
            start_research "$2"
            ;;
        game)
            start_game "$2" "$3" "$4"
            ;;
        help|--help|-h)
            usage
            ;;
        *)
            echo -e "${RED}Unknown command: $command${NC}"
            usage
            exit 1
            ;;
    esac
}

main "$@"
