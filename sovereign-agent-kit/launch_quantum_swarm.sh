#!/bin/bash
# Launch Quantum Swarm - Sovereign Quantum Processor
# Spin up multiple agent qubits in parallel

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Default values
QUBITS=16
MODEL="claude-3-opus"
LOCAL=false
CONFIG_FILE="./config/quantum_swarm_config.yaml"
VAULT_PATH="./obsidian_vault"
LOG_DIR="./logs"

# Print banner
print_banner() {
    echo -e "${MAGENTA}"
    cat << "EOF"
    ╔═══════════════════════════════════════════════════════╗
    ║  ⚛️  SOVEREIGN QUANTUM PROCESSOR - LAUNCH SEQUENCE   ║
    ║                                                       ║
    ║  Transform your Obsidian vault into a living         ║
    ║  quantum computer made of LLMs and markdown          ║
    ╚═══════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --qubits)
            QUBITS="$2"
            shift 2
            ;;
        --model)
            MODEL="$2"
            shift 2
            ;;
        --local)
            LOCAL=true
            shift
            ;;
        --config)
            CONFIG_FILE="$2"
            shift 2
            ;;
        --vault)
            VAULT_PATH="$2"
            shift 2
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --qubits N       Number of agent qubits to launch (default: 16)"
            echo "  --model MODEL    LLM model to use (default: claude-3-opus)"
            echo "  --local          Use local models (Ollama)"
            echo "  --config FILE    Path to config file"
            echo "  --vault PATH     Path to Obsidian vault"
            echo "  --help           Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0 --qubits 16 --model claude-3-opus"
            echo "  $0 --qubits 32 --model llama3.1:70b --local"
            echo "  $0 --qubits 8 --model grok-4-fast-reasoning"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

print_banner

echo -e "${CYAN}Configuration:${NC}"
echo -e "  Qubits:     ${GREEN}$QUBITS${NC}"
echo -e "  Model:      ${GREEN}$MODEL${NC}"
echo -e "  Local:      ${GREEN}$LOCAL${NC}"
echo -e "  Vault:      ${GREEN}$VAULT_PATH${NC}"
echo -e "  Config:     ${GREEN}$CONFIG_FILE${NC}"
echo ""

# Create necessary directories
mkdir -p "$VAULT_PATH"
mkdir -p "$LOG_DIR"

# Check if vault is a git repository
if [ ! -d "$VAULT_PATH/.git" ]; then
    echo -e "${YELLOW}⚠️  Vault is not a git repository. Initializing...${NC}"
    (cd "$VAULT_PATH" && git init && git add . && git commit -m "Initial quantum state" || true)
fi

# Check for required dependencies
check_dependencies() {
    echo -e "${CYAN}Checking dependencies...${NC}"
    
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ Python 3 not found. Please install Python 3.8+${NC}"
        exit 1
    fi
    
    if [ "$LOCAL" = true ] && ! command -v ollama &> /dev/null; then
        echo -e "${RED}❌ Ollama not found. Please install Ollama for local models${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Dependencies OK${NC}"
}

check_dependencies

# Create Python virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${CYAN}Creating Python virtual environment...${NC}"
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install pyyaml structlog
else
    source venv/bin/activate
fi

# Launch agent qubits
echo -e "${CYAN}🚀 Launching $QUBITS quantum agent qubits...${NC}"
echo ""

PIDS=()

for i in $(seq 0 $((QUBITS - 1))); do
    AGENT_ID="qubit_$i"
    LOG_FILE="$LOG_DIR/${AGENT_ID}.log"
    
    echo -e "${BLUE}  ⚛️  Launching ${AGENT_ID}...${NC}"
    
    # Launch agent in background
    python3 -m swarm.quantum_loop \
        --agent-id "$AGENT_ID" \
        --model "$MODEL" \
        --vault "$VAULT_PATH" \
        --config "$CONFIG_FILE" \
        > "$LOG_FILE" 2>&1 &
    
    PID=$!
    PIDS+=($PID)
    
    echo -e "${GREEN}     ✓ ${AGENT_ID} started (PID: $PID)${NC}"
    
    # Small delay to avoid thundering herd
    sleep 0.5
done

echo ""
echo -e "${GREEN}✅ All $QUBITS qubits launched successfully!${NC}"
echo ""

# Save PIDs for later management
PID_FILE="$LOG_DIR/quantum_swarm.pids"
printf "%s\n" "${PIDS[@]}" > "$PID_FILE"

# Print status
echo -e "${CYAN}═══════════════════════════════════════════════════════${NC}"
echo -e "${MAGENTA}🎯 QUANTUM PROCESSOR ONLINE${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════${NC}"
echo ""
echo -e "  Active Qubits:    ${GREEN}$QUBITS${NC}"
echo -e "  Model:            ${GREEN}$MODEL${NC}"
echo -e "  Vault Path:       ${GREEN}$VAULT_PATH${NC}"
echo -e "  Logs:             ${GREEN}$LOG_DIR${NC}"
echo -e "  PIDs File:        ${GREEN}$PID_FILE${NC}"
echo ""
echo -e "${YELLOW}Management Commands:${NC}"
echo -e "  Monitor logs:     ${CYAN}tail -f $LOG_DIR/qubit_*.log${NC}"
echo -e "  Check status:     ${CYAN}./quantum_status.sh${NC}"
echo -e "  Stop swarm:       ${CYAN}./quantum_shutdown.sh${NC}"
echo -e "  Re-center swarm:  ${CYAN}./quantum_recenter.sh${NC}"
echo ""
echo -e "${BLUE}💡 Tip: Watch the entanglement graph grow in real-time:${NC}"
echo -e "   ${CYAN}watch -n 5 'find $VAULT_PATH -name \"*.md\" | wc -l'${NC}"
echo ""
echo -e "${MAGENTA}⚛️  The quantum processor is now running autonomously ⚛️${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════${NC}"
