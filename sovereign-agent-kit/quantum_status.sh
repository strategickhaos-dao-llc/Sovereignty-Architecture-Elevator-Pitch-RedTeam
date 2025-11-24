#!/bin/bash
# Quantum Status - Check the health of your quantum processor

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

LOG_DIR="./logs"
PID_FILE="$LOG_DIR/quantum_swarm.pids"
VAULT_PATH="./obsidian_vault"

echo -e "${MAGENTA}⚛️  QUANTUM PROCESSOR STATUS REPORT ⚛️${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════${NC}"
echo ""

# Check if swarm is running
if [ ! -f "$PID_FILE" ]; then
    echo -e "${RED}❌ No quantum swarm detected${NC}"
    echo -e "   Run ${CYAN}./launch_quantum_swarm.sh${NC} to start"
    exit 1
fi

# Count active qubits
ACTIVE_COUNT=0
TOTAL_COUNT=0

while read -r PID; do
    TOTAL_COUNT=$((TOTAL_COUNT + 1))
    if ps -p "$PID" > /dev/null 2>&1; then
        ACTIVE_COUNT=$((ACTIVE_COUNT + 1))
    fi
done < "$PID_FILE"

# Quantum register stats
if [ -d "$VAULT_PATH" ]; then
    NOTE_COUNT=$(find "$VAULT_PATH" -name "*.md" | wc -l)
    LINK_COUNT=$(grep -r "\[\[" "$VAULT_PATH" --include="*.md" 2>/dev/null | wc -l || echo "0")
else
    NOTE_COUNT=0
    LINK_COUNT=0
fi

# Gate fidelity (approximate from logs)
if [ -d "$LOG_DIR" ]; then
    CONSENSUS_PASS=$(grep -r "PASS" "$LOG_DIR" --include="*.log" 2>/dev/null | wc -l || echo "0")
    CONSENSUS_FAIL=$(grep -r "FAIL" "$LOG_DIR" --include="*.log" 2>/dev/null | wc -l || echo "0")
    TOTAL_CHECKS=$((CONSENSUS_PASS + CONSENSUS_FAIL))
    
    if [ $TOTAL_CHECKS -gt 0 ]; then
        FIDELITY=$(echo "scale=1; $CONSENSUS_PASS * 100 / $TOTAL_CHECKS" | bc)
    else
        FIDELITY="N/A"
    fi
else
    FIDELITY="N/A"
fi

# Print status
echo -e "${CYAN}Qubit Status:${NC}"
if [ $ACTIVE_COUNT -eq $TOTAL_COUNT ]; then
    echo -e "  Active Qubits:    ${GREEN}$ACTIVE_COUNT / $TOTAL_COUNT${NC} ✅"
else
    echo -e "  Active Qubits:    ${YELLOW}$ACTIVE_COUNT / $TOTAL_COUNT${NC} ⚠️"
fi
echo ""

echo -e "${CYAN}Quantum Register:${NC}"
echo -e "  Total Notes:      ${GREEN}$NOTE_COUNT${NC}"
echo -e "  Total Links:      ${GREEN}$LINK_COUNT${NC}"
echo ""

echo -e "${CYAN}Performance Metrics:${NC}"
if [ "$FIDELITY" != "N/A" ]; then
    if (( $(echo "$FIDELITY > 95" | bc -l) )); then
        echo -e "  Gate Fidelity:    ${GREEN}${FIDELITY}%${NC} ✅"
    elif (( $(echo "$FIDELITY > 80" | bc -l) )); then
        echo -e "  Gate Fidelity:    ${YELLOW}${FIDELITY}%${NC} ⚠️"
    else
        echo -e "  Gate Fidelity:    ${RED}${FIDELITY}%${NC} ❌"
    fi
else
    echo -e "  Gate Fidelity:    ${YELLOW}N/A${NC}"
fi
echo ""

# Recent activity
echo -e "${CYAN}Recent Activity:${NC}"
if [ -d "$LOG_DIR" ]; then
    echo -e "  Last 5 quantum operations:"
    tail -n 5 "$LOG_DIR"/qubit_*.log 2>/dev/null | grep -E "(created note|iteration complete)" | tail -5 | while read -r line; do
        echo -e "    ${GREEN}•${NC} $line"
    done
else
    echo -e "    ${YELLOW}No recent activity${NC}"
fi
echo ""

echo -e "${CYAN}═══════════════════════════════════════════════════════${NC}"

# Health assessment
if [ $ACTIVE_COUNT -eq $TOTAL_COUNT ]; then
    echo -e "${GREEN}✅ QUANTUM PROCESSOR: HEALTHY${NC}"
elif [ $ACTIVE_COUNT -gt 0 ]; then
    echo -e "${YELLOW}⚠️  QUANTUM PROCESSOR: DEGRADED${NC}"
    echo -e "   Some qubits are offline. Consider restarting."
else
    echo -e "${RED}❌ QUANTUM PROCESSOR: OFFLINE${NC}"
    echo -e "   Run ${CYAN}./launch_quantum_swarm.sh${NC} to restart"
fi

echo -e "${CYAN}═══════════════════════════════════════════════════════${NC}"
