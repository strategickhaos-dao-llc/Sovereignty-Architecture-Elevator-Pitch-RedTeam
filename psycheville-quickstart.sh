#!/bin/bash
# PsycheVille Quick Start Script
# Self-Observing Infrastructure Architecture

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
LOG_DIR="/var/log/psycheville"
OBSIDIAN_DIR="${HOME}/Obsidian/PsycheVille"
CONFIG_FILE="psycheville.yaml"
WORKER_SCRIPT="psycheville_reflection_worker.py"

echo -e "${CYAN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║                                                            ║${NC}"
echo -e "${CYAN}║              PsycheVille Quick Start                       ║${NC}"
echo -e "${CYAN}║        Self-Observing Infrastructure Architecture          ║${NC}"
echo -e "${CYAN}║                                                            ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Function to print status
print_status() {
    echo -e "${GREEN}✅${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠️${NC}  $1"
}

print_error() {
    echo -e "${RED}❌${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ️${NC}  $1"
}

# Check if running as root for log directory creation
check_permissions() {
    if [ ! -d "$LOG_DIR" ]; then
        print_info "Log directory doesn't exist. Attempting to create..."
        if sudo mkdir -p "$LOG_DIR" 2>/dev/null; then
            sudo chown $USER:$USER "$LOG_DIR"
            print_status "Created log directory: $LOG_DIR"
        else
            print_warning "Could not create log directory with sudo. Using ~/.psycheville/logs instead"
            LOG_DIR="${HOME}/.psycheville/logs"
            mkdir -p "$LOG_DIR"
        fi
    else
        print_status "Log directory exists: $LOG_DIR"
    fi
}

# Check dependencies
check_dependencies() {
    echo -e "\n${CYAN}═══ Checking Dependencies ═══${NC}\n"
    
    # Check Python
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        print_status "Python 3 installed: v$PYTHON_VERSION"
    else
        print_error "Python 3 not found. Please install Python 3.8+"
        exit 1
    fi
    
    # Check pip
    if command -v pip3 &> /dev/null || command -v pip &> /dev/null; then
        print_status "pip installed"
    else
        print_error "pip not found. Please install pip"
        exit 1
    fi
    
    # Check PyYAML
    if python3 -c "import yaml" 2>/dev/null; then
        print_status "PyYAML installed"
    else
        print_warning "PyYAML not installed. Installing..."
        pip3 install pyyaml
        print_status "PyYAML installed"
    fi
    
    # Check Ollama (optional)
    if command -v ollama &> /dev/null; then
        print_status "Ollama installed"
        OLLAMA_MODELS=$(ollama list 2>/dev/null | grep -c llama || echo "0")
        if [ "$OLLAMA_MODELS" -gt 0 ]; then
            print_status "Ollama models available"
        else
            print_warning "No Ollama models found. Run: ollama pull llama3:latest"
        fi
    else
        print_warning "Ollama not installed. AI analysis will be unavailable."
        print_info "Install from: https://ollama.ai/"
    fi
    
    # Check Docker (optional)
    if command -v docker &> /dev/null; then
        print_status "Docker installed"
        if command -v docker-compose &> /dev/null || docker compose version &> /dev/null 2>&1; then
            print_status "Docker Compose available"
        else
            print_warning "Docker Compose not found"
        fi
    else
        print_warning "Docker not installed (optional)"
    fi
}

# Setup directories
setup_directories() {
    echo -e "\n${CYAN}═══ Setting Up Directories ═══${NC}\n"
    
    # Create log directory
    check_permissions
    
    # Create department log directories
    for dept in tools_refinery sovereign_ai_lab rf_sensor_lab quantum_emulation cloud_os valoryield_engine; do
        mkdir -p "${LOG_DIR}/${dept}"
        touch "${LOG_DIR}/${dept}.jsonl"
    done
    print_status "Created department log files"
    
    # Create Obsidian directory
    mkdir -p "$OBSIDIAN_DIR"/{Daily\ Reports,Weekly\ Synthesis}
    print_status "Created Obsidian vault structure: $OBSIDIAN_DIR"
}

# Generate sample logs
generate_sample_logs() {
    echo -e "\n${CYAN}═══ Generating Sample Logs ═══${NC}\n"
    
    read -p "Generate sample log data for testing? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "Generating sample logs..."
        
        # Use the Python sample logger for robust log generation
        if command -v python3 &> /dev/null && [ -f "$WORKER_SCRIPT" ]; then
            python3 psycheville_sample_logger.py --log-dir "$LOG_DIR" --events 50
        else
            print_warning "Python sample logger not available, creating minimal logs..."
            TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
            echo "{\"timestamp\": \"$TIMESTAMP\", \"department\": \"tools_refinery\", \"event_type\": \"endpoint_called\", \"metadata\": {\"endpoint\": \"/api/v1/tools/list\", \"response_time_ms\": 45}}" >> "${LOG_DIR}/tools_refinery.jsonl"
            print_status "Generated minimal sample logs"
        fi
    fi
}

# Run reflection worker
run_worker() {
    echo -e "\n${CYAN}═══ Running Reflection Worker ═══${NC}\n"
    
    if [ ! -f "$WORKER_SCRIPT" ]; then
        print_error "Worker script not found: $WORKER_SCRIPT"
        exit 1
    fi
    
    if [ ! -f "$CONFIG_FILE" ]; then
        print_error "Configuration file not found: $CONFIG_FILE"
        exit 1
    fi
    
    # Update config with actual paths
    if command -v sed &> /dev/null; then
        sed -i.bak "s|/var/log/psycheville|${LOG_DIR}|g" "$CONFIG_FILE" 2>/dev/null || true
        sed -i.bak "s|/home/user/Obsidian/PsycheVille|${OBSIDIAN_DIR}|g" "$CONFIG_FILE" 2>/dev/null || true
    fi
    
    print_info "Starting reflection worker..."
    python3 "$WORKER_SCRIPT" --config "$CONFIG_FILE"
}

# Docker deployment option
docker_deploy() {
    echo -e "\n${CYAN}═══ Docker Deployment ═══${NC}\n"
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker not installed"
        return 1
    fi
    
    print_info "Deploying PsycheVille with Docker Compose..."
    
    # Set environment variable for Obsidian vault path
    export OBSIDIAN_VAULT="$OBSIDIAN_DIR"
    
    if command -v docker-compose &> /dev/null; then
        docker-compose -f docker-compose.psycheville.yml up -d
    elif docker compose version &> /dev/null 2>&1; then
        docker compose -f docker-compose.psycheville.yml up -d
    else
        print_error "Docker Compose not available"
        return 1
    fi
    
    print_status "PsycheVille deployed with Docker"
    print_info "View logs: docker-compose -f docker-compose.psycheville.yml logs -f"
    print_info "Stop services: docker-compose -f docker-compose.psycheville.yml down"
}

# Main menu
main_menu() {
    echo -e "\n${CYAN}═══ Deployment Options ═══${NC}\n"
    echo "1. Run once (manual execution)"
    echo "2. Deploy with Docker Compose (scheduled)"
    echo "3. Setup only (no execution)"
    echo "4. Exit"
    echo ""
    read -p "Select option (1-4): " -n 1 -r
    echo
    
    case $REPLY in
        1)
            run_worker
            ;;
        2)
            docker_deploy
            ;;
        3)
            print_info "Setup complete. Run manually with: python3 $WORKER_SCRIPT"
            ;;
        4)
            echo "Exiting..."
            exit 0
            ;;
        *)
            print_error "Invalid option"
            exit 1
            ;;
    esac
}

# Main execution
main() {
    check_dependencies
    setup_directories
    generate_sample_logs
    main_menu
    
    echo -e "\n${GREEN}═══════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}✅ PsycheVille Quick Start Complete!${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}\n"
    
    print_info "Next steps:"
    echo "  1. Check your Obsidian vault: $OBSIDIAN_DIR"
    echo "  2. View department logs: $LOG_DIR"
    echo "  3. Configure departments in: $CONFIG_FILE"
    echo "  4. Review documentation: PSYCHEVILLE_COMPARATIVE_ANALYSIS.md"
    echo ""
}

# Run main function
main
