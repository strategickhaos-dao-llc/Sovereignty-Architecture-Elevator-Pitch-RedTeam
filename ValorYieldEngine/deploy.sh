#!/bin/bash
# ============================================================================
# ValorYield Engine - Master Deployment Script
# Sovereign Wealth Platform - $0 Fees, 100% Yours
# ============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=============================================="
echo "🔥 ValorYield Engine - Deployment Starting"
echo "   Sovereignty Unlocked"
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Check prerequisites
check_prereqs() {
    echo -e "\n${CYAN}📋 Checking prerequisites...${NC}"
    
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ Python 3 not found${NC}"
        exit 1
    fi
    echo "  ✓ Python 3 found"
    
    if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
        echo -e "${RED}❌ pip not found${NC}"
        exit 1
    fi
    echo "  ✓ pip found"
    
    if command -v node &> /dev/null; then
        echo "  ✓ Node.js found ($(node --version))"
    else
        echo "  ⚠ Node.js not found - web/mobile won't start"
    fi
}

# Install dependencies
install_deps() {
    echo -e "\n${CYAN}📦 Installing dependencies...${NC}"
    
    # API dependencies
    echo "  Installing API dependencies..."
    cd "$SCRIPT_DIR/api"
    pip3 install -q -r requirements.txt 2>/dev/null || pip install -q -r requirements.txt
    
    # SwarmGate dependencies
    echo "  Installing SwarmGate dependencies..."
    cd "$SCRIPT_DIR/swarmgate"
    pip3 install -q -r requirements.txt 2>/dev/null || pip install -q -r requirements.txt
    
    cd "$SCRIPT_DIR"
    echo -e "  ${GREEN}✓ Dependencies installed${NC}"
}

# Start API server
start_api() {
    echo -e "\n${CYAN}🔌 Starting API server on port 8080...${NC}"
    cd "$SCRIPT_DIR/api"
    nohup python3 -m uvicorn main:app --host 0.0.0.0 --port 8080 > ../logs/api.log 2>&1 &
    echo $! > ../pids/api.pid
    sleep 2
    if curl -s http://localhost:8080/health > /dev/null; then
        echo -e "  ${GREEN}✓ API running at http://localhost:8080${NC}"
    else
        echo -e "  ${RED}⚠ API may still be starting...${NC}"
    fi
}

# Start SwarmGate
start_swarmgate() {
    echo -e "\n${CYAN}🤖 Starting SwarmGate integration...${NC}"
    cd "$SCRIPT_DIR/swarmgate"
    nohup python3 integration.py > ../logs/swarmgate.log 2>&1 &
    echo $! > ../pids/swarmgate.pid
    echo -e "  ${GREEN}✓ SwarmGate started (NATS events on port 4222)${NC}"
}

# Start Web UI (if Node available)
start_web() {
    if ! command -v node &> /dev/null; then
        echo -e "\n⚠ Skipping Web UI (Node.js not installed)"
        return
    fi
    
    echo -e "\n${CYAN}🌐 Starting Web UI on port 8009...${NC}"
    cd "$SCRIPT_DIR/web"
    
    if [ ! -d "node_modules" ]; then
        echo "  Installing web dependencies..."
        npm install --silent
    fi
    
    nohup npm run dev > ../logs/web.log 2>&1 &
    echo $! > ../pids/web.pid
    echo -e "  ${GREEN}✓ Web UI starting at http://localhost:8009${NC}"
}

# Create logs and pids directories
setup_dirs() {
    mkdir -p "$SCRIPT_DIR/logs" "$SCRIPT_DIR/pids"
}

# Stop all services
stop_all() {
    echo -e "\n${CYAN}🛑 Stopping all services...${NC}"
    
    for pidfile in "$SCRIPT_DIR/pids"/*.pid; do
        if [ -f "$pidfile" ]; then
            pid=$(cat "$pidfile")
            if kill -0 "$pid" 2>/dev/null; then
                kill "$pid" 2>/dev/null || true
                echo "  Stopped process $pid"
            fi
            rm -f "$pidfile"
        fi
    done
    
    echo -e "  ${GREEN}✓ All services stopped${NC}"
}

# Print status
print_status() {
    echo -e "\n=============================================="
    echo -e "${GREEN}✅ ValorYield Engine Deployed!${NC}"
    echo "=============================================="
    echo ""
    echo "🌐 Services:"
    echo "   API:       http://localhost:8080"
    echo "   Web UI:    http://localhost:8009"
    echo "   SwarmGate: NATS @ localhost:4222"
    echo ""
    echo "📁 Logs:"
    echo "   API:       $SCRIPT_DIR/logs/api.log"
    echo "   Web:       $SCRIPT_DIR/logs/web.log"
    echo "   SwarmGate: $SCRIPT_DIR/logs/swarmgate.log"
    echo ""
    echo "🛑 To stop: ./deploy.sh stop"
    echo ""
    echo "🚀 Next steps:"
    echo "   1. Set environment variables for broker APIs"
    echo "   2. Configure NATS server for production"
    echo "   3. Deploy to GCP GKE for 24/7 sovereignty"
    echo ""
    echo "💜 Sovereignty Achieved!"
}

# Main
case "${1:-start}" in
    start)
        setup_dirs
        check_prereqs
        install_deps
        start_api
        start_swarmgate
        start_web
        print_status
        ;;
    stop)
        stop_all
        ;;
    restart)
        stop_all
        sleep 2
        setup_dirs
        check_prereqs
        install_deps
        start_api
        start_swarmgate
        start_web
        print_status
        ;;
    status)
        echo "Checking service status..."
        for pidfile in "$SCRIPT_DIR/pids"/*.pid; do
            if [ -f "$pidfile" ]; then
                service=$(basename "$pidfile" .pid)
                pid=$(cat "$pidfile")
                if kill -0 "$pid" 2>/dev/null; then
                    echo "  ✓ $service is running (PID: $pid)"
                else
                    echo "  ✗ $service is not running"
                fi
            fi
        done
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac
