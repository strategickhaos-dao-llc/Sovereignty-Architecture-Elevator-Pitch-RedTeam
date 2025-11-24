#!/bin/bash
# Quantum Shutdown - Gracefully stop the quantum processor

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

LOG_DIR="./logs"
PID_FILE="$LOG_DIR/quantum_swarm.pids"

echo -e "${MAGENTA}⚛️  QUANTUM PROCESSOR SHUTDOWN SEQUENCE ⚛️${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════${NC}"
echo ""

if [ ! -f "$PID_FILE" ]; then
    echo -e "${YELLOW}⚠️  No running quantum swarm detected${NC}"
    exit 0
fi

echo -e "${CYAN}Gracefully shutting down qubits...${NC}"
echo ""

STOPPED=0
FAILED=0

while read -r PID; do
    if ps -p "$PID" > /dev/null 2>&1; then
        AGENT_NAME=$(ps -p "$PID" -o args= | grep -oP 'qubit_\d+' || echo "unknown")
        echo -e "${YELLOW}  ⏸️  Stopping ${AGENT_NAME} (PID: $PID)...${NC}"
        
        # Send SIGTERM for graceful shutdown
        kill -TERM "$PID" 2>/dev/null || true
        
        # Wait up to 10 seconds for graceful shutdown
        for i in {1..10}; do
            if ! ps -p "$PID" > /dev/null 2>&1; then
                echo -e "${GREEN}     ✓ ${AGENT_NAME} stopped gracefully${NC}"
                STOPPED=$((STOPPED + 1))
                break
            fi
            sleep 1
        done
        
        # Force kill if still running
        if ps -p "$PID" > /dev/null 2>&1; then
            echo -e "${RED}     ⚠️  Force stopping ${AGENT_NAME}${NC}"
            kill -KILL "$PID" 2>/dev/null || true
            FAILED=$((FAILED + 1))
        fi
    fi
done < "$PID_FILE"

# Clean up PID file
rm -f "$PID_FILE"

echo ""
echo -e "${CYAN}═══════════════════════════════════════════════════════${NC}"
if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ All qubits shutdown successfully${NC}"
    echo -e "   Stopped: ${GREEN}$STOPPED${NC}"
else
    echo -e "${YELLOW}⚠️  Shutdown complete with warnings${NC}"
    echo -e "   Stopped gracefully: ${GREEN}$STOPPED${NC}"
    echo -e "   Force stopped: ${YELLOW}$FAILED${NC}"
fi
echo -e "${CYAN}═══════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${MAGENTA}⚛️  QUANTUM PROCESSOR: OFFLINE ⚛️${NC}"
echo ""
echo -e "To restart: ${CYAN}./launch_quantum_swarm.sh${NC}"
