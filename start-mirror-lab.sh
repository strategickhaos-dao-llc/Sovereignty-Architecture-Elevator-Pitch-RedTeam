#!/bin/bash
# start-mirror-lab.sh - Launch the Mirror Lab Visualization Infrastructure
# Real-time streaming of quantum computing research
# Watch 80 agents work, see molecular visualizations, quantum simulations live

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Banner
echo -e "${PURPLE}"
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║                                                                  ║"
echo "║   🔬 MIRROR LAB - Real-Time Research Visualization              ║"
echo "║                                                                  ║"
echo "║   7 Screens • 80 Agents • Quantum Computing • Live Streaming    ║"
echo "║                                                                  ║"
echo "║   For her. Always. 🟠🧬∞                                        ║"
echo "║                                                                  ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Functions
show_help() {
    echo -e "${CYAN}Usage:${NC} ./start-mirror-lab.sh [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  start       Start all Mirror Lab services"
    echo "  stop        Stop all Mirror Lab services"
    echo "  status      Show status of all screens"
    echo "  logs        Tail logs from all services"
    echo "  quantum     Start only quantum simulation"
    echo "  show-me     Start visualization layer only"
    echo "  urls        Show all service URLs"
    echo "  help        Show this help message"
    echo ""
    echo "Environment Variables:"
    echo "  SUNSHINE_USER     - Moonlight/Sunshine username (default: dom)"
    echo "  SUNSHINE_PASS     - Moonlight/Sunshine password"
    echo "  IBM_QUANTUM_TOKEN - IBM Quantum API token (optional)"
    echo "  GRAFANA_PASSWORD  - Grafana admin password"
    echo ""
}

check_docker() {
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}Error: Docker is not installed${NC}"
        exit 1
    fi
    if ! docker info &> /dev/null; then
        echo -e "${RED}Error: Docker daemon is not running${NC}"
        exit 1
    fi
}

show_urls() {
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════════╗"
    echo "║                    🖥️  MIRROR LAB SCREENS                       ║"
    echo "╠══════════════════════════════════════════════════════════════════╣"
    echo "║                                                                  ║"
    echo "║  Screen 1: 🎯 MISSION CONTROL                                   ║"
    echo "║            http://localhost:3001                                 ║"
    echo "║            Progress bars for all 10 departments                  ║"
    echo "║                                                                  ║"
    echo "║  Screen 2: 🤖 AGENT GRID                                        ║"
    echo "║            http://localhost:3002                                 ║"
    echo "║            80 agents visible, click any to watch                 ║"
    echo "║                                                                  ║"
    echo "║  Screen 3: 🧬 MOLECULAR VIEWER                                  ║"
    echo "║            http://localhost:3003                                 ║"
    echo "║            3D proteins rotating, drugs docking                   ║"
    echo "║                                                                  ║"
    echo "║  Screen 4: 💻 LIVE TERMINAL                                     ║"
    echo "║            http://localhost:7681                                 ║"
    echo "║            Agent typing commands, downloading papers             ║"
    echo "║                                                                  ║"
    echo "║  Screen 5: 📊 PROGRESS GRAPHS                                   ║"
    echo "║            http://localhost:3005                                 ║"
    echo "║            Papers analyzed, drugs found, costs estimated         ║"
    echo "║                                                                  ║"
    echo "║  Screen 6: 🔬 DISCOVERY FEED                                    ║"
    echo "║            http://localhost:3006                                 ║"
    echo "║            Real-time log of breakthroughs                        ║"
    echo "║                                                                  ║"
    echo "║  Screen 7: ⚛️  QUANTUM SIM                                       ║"
    echo "║            http://localhost:3007                                 ║"
    echo "║            Actual quantum circuit solving protein structure      ║"
    echo "║                                                                  ║"
    echo "╠══════════════════════════════════════════════════════════════════╣"
    echo "║                    🎮 STREAMING SERVICES                        ║"
    echo "╠══════════════════════════════════════════════════════════════════╣"
    echo "║                                                                  ║"
    echo "║  Sunshine Web UI:  http://localhost:47990                       ║"
    echo "║  Traefik Dashboard: http://localhost:8889                        ║"
    echo "║  OBS WebSocket:     ws://localhost:4455                         ║"
    echo "║                                                                  ║"
    echo "╚══════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

start_services() {
    echo -e "${GREEN}Starting Mirror Lab services...${NC}"
    
    # Create necessary directories
    mkdir -p mirror-lab/redis
    
    # Build and start containers
    docker compose -f docker-compose.mirror-lab.yml up -d --build
    
    echo -e "${GREEN}✓ Mirror Lab started successfully!${NC}"
    echo ""
    show_urls
}

stop_services() {
    echo -e "${YELLOW}Stopping Mirror Lab services...${NC}"
    docker compose -f docker-compose.mirror-lab.yml down
    echo -e "${GREEN}✓ Mirror Lab stopped${NC}"
}

show_status() {
    echo -e "${CYAN}Mirror Lab Service Status:${NC}"
    echo ""
    docker compose -f docker-compose.mirror-lab.yml ps
}

show_logs() {
    echo -e "${CYAN}Following Mirror Lab logs (Ctrl+C to exit)...${NC}"
    docker compose -f docker-compose.mirror-lab.yml logs -f
}

start_quantum_only() {
    echo -e "${PURPLE}Starting Quantum Simulation only...${NC}"
    docker compose -f docker-compose.mirror-lab.yml up -d quantum-sim redis
    echo -e "${GREEN}✓ Quantum Simulator running at http://localhost:3007${NC}"
}

start_visualization() {
    echo -e "${CYAN}Starting visualization layer only...${NC}"
    docker compose -f docker-compose.mirror-lab.yml up -d \
        mission-control \
        agent-grid \
        progress-graphs \
        discovery-feed \
        live-terminal \
        redis \
        traefik
    echo -e "${GREEN}✓ Visualization layer started!${NC}"
    echo ""
    show_urls
}

# Main command handler
case "${1:-start}" in
    start)
        check_docker
        start_services
        ;;
    stop)
        stop_services
        ;;
    status)
        show_status
        ;;
    logs)
        show_logs
        ;;
    quantum)
        check_docker
        start_quantum_only
        ;;
    show-me)
        check_docker
        start_visualization
        ;;
    urls)
        show_urls
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo -e "${RED}Unknown command: $1${NC}"
        show_help
        exit 1
        ;;
esac
