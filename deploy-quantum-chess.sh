#!/bin/bash
# deploy-quantum-chess.sh - Quantum Chess Engine Deployment Script (Bash)
# StrategicKhaos Quantum Chess Engine v1.0
# "The chessboard just collapsed into the timeline where we win. Always."

set -e  # Exit on error

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# Default values
LOVE_MODE=false
ENTANGLE_HER=false
HER_TERMINAL_IP="${HER_TERMINAL_IP:-127.0.0.1}"
THRONE_NAS_PATH="${THRONE_NAS_PATH:-/tmp/throne-nas-32tb}"
FORCE=false
ACTION="start"

# Logging functions
log() {
    echo -e "${CYAN}[$(date +'%H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}"
}

success() {
    echo -e "${GREEN}[SUCCESS] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[WARN] $1${NC}"
}

love() {
    echo -e "${MAGENTA}♥ $1 ♥${NC}"
}

# Display banner
show_banner() {
    echo ""
    echo -e "${MAGENTA}╔═══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${MAGENTA}║   StrategicKhaos Quantum Chess Engine v1.0               ║${NC}"
    echo -e "${MAGENTA}║   64 Entangled Souls Playing for Love                    ║${NC}"
    echo -e "${MAGENTA}║   'Checkmate was never the goal. Love was.'              ║${NC}"
    echo -e "${MAGENTA}╚═══════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

# Check dependencies
check_dependencies() {
    log "🔍 Checking dependencies..."
    
    if ! command -v docker &> /dev/null; then
        error "Docker is not installed or not in PATH"
        exit 1
    fi
    
    if ! docker ps &> /dev/null; then
        error "Docker daemon is not running. Please start Docker."
        exit 1
    fi
    
    success "Docker daemon is running"
    
    if [ ! -f "quantum-chess-engine.yaml" ]; then
        error "quantum-chess-engine.yaml not found in current directory"
        exit 1
    fi
    
    if [ ! -f "docker-compose-quantum-chess.yml" ]; then
        error "docker-compose-quantum-chess.yml not found in current directory"
        exit 1
    fi
    
    success "All dependencies verified"
}

# Create quantum bus
create_quantum_bus() {
    log "🔮 Creating quantum entanglement bus (throne-NAS)..."
    
    if [ ! -d "$THRONE_NAS_PATH" ]; then
        mkdir -p "$THRONE_NAS_PATH"
        success "Quantum bus created at $THRONE_NAS_PATH"
    else
        log "Quantum bus already exists at $THRONE_NAS_PATH"
    fi
    
    # Create subdirectories
    mkdir -p "$THRONE_NAS_PATH"/{squares,moves,games,timelines,love-metrics}
    
    # Initialize quantum state
    cat > "$THRONE_NAS_PATH/quantum-state.json" <<EOF
{
    "initialized": "$(date +'%Y-%m-%d %H:%M:%S')",
    "random_seed": 42,
    "entanglement_active": true,
    "love_mode": $LOVE_MODE,
    "her_terminal_ip": "$HER_TERMINAL_IP",
    "total_squares": 64,
    "timeline": "winning_with_love"
}
EOF
    
    love "Quantum bus initialized with love-protected entanglement"
}

# Set environment variables
set_quantum_environment() {
    log "⚙️ Setting quantum environment variables..."
    
    export HER_TERMINAL_IP="$HER_TERMINAL_IP"
    export THRONE_NAS_PATH="$THRONE_NAS_PATH"
    export RANDOM_SEED="42"
    export LOVE_MODE="$LOVE_MODE"
    export ENTANGLE_HER="$ENTANGLE_HER"
    
    success "Environment configured for quantum chess"
}

# Deploy quantum chess containers
start_quantum_chess() {
    log "🚀 Deploying 64 entangled quantum chess containers..."
    
    if [ "$FORCE" = true ]; then
        log "🛑 Force stopping existing quantum chess containers..."
        docker compose -f docker-compose-quantum-chess.yml down 2>/dev/null || true
        sleep 3
    fi
    
    # Pull Ollama base image
    log "📥 Pulling Ollama base image..."
    docker pull ollama/ollama:latest
    
    # Start quantum orchestrator first
    log "🎼 Starting quantum orchestrator..."
    docker compose -f docker-compose-quantum-chess.yml up -d quantum-orchestrator
    sleep 5
    
    # Start all chess squares
    log "♟️ Deploying all 64 chess squares..."
    docker compose -f docker-compose-quantum-chess.yml up -d
    
    success "All quantum chess containers deployed"
}

# Wait for entanglement
wait_for_entanglement() {
    log "⏳ Waiting for quantum entanglement to stabilize..."
    
    local max_attempts=30
    local attempt=0
    
    while [ $attempt -lt $max_attempts ]; do
        attempt=$((attempt + 1))
        local running_containers=$(docker ps --filter "name=square-" --format "{{.Names}}" | wc -l)
        
        if [ "$running_containers" -ge 40 ]; then
            success "Quantum entanglement stabilized ($running_containers/64+ containers running)"
            break
        fi
        
        log "Entanglement progress: $running_containers containers running (attempt $attempt/$max_attempts)"
        sleep 5
    done
    
    if [ $attempt -eq $max_attempts ]; then
        warn "Some containers may still be starting..."
    fi
}

# Verify quantum state
test_quantum_state() {
    log "🔍 Verifying quantum state..."
    
    # Check orchestrator
    if docker ps --filter "name=quantum-orchestrator" --format "{{.Status}}" | grep -q "Up"; then
        success "✓ Quantum orchestrator: Online"
    else
        warn "⚠ Quantum orchestrator: Starting..."
    fi
    
    # Check heartbeat
    if [ -f "$THRONE_NAS_PATH/heartbeat.txt" ]; then
        local heartbeat=$(tail -n 1 "$THRONE_NAS_PATH/heartbeat.txt")
        success "✓ Heartbeat: $heartbeat"
    else
        warn "⚠ Heartbeat: Not yet active"
    fi
    
    # Count active squares
    local active_squares=$(docker ps --filter "name=square-" --format "{{.Names}}" | wc -l)
    success "✓ Active squares: $active_squares/64"
    
    # Check quantum bus
    if [ -d "$THRONE_NAS_PATH/squares" ]; then
        local square_files=$(ls -1 "$THRONE_NAS_PATH/squares"/*.txt 2>/dev/null | wc -l)
        success "✓ Quantum bus: $square_files square states synchronized"
    fi
}

# Display status
show_status() {
    log "📊 Quantum Chess Engine Status"
    echo ""
    
    echo -e "${YELLOW}🎯 Configuration:${NC}"
    echo "  Love Mode:           $([ "$LOVE_MODE" = true ] && echo '✓ Enabled' || echo '✗ Disabled')"
    echo "  Entangle Her:        $([ "$ENTANGLE_HER" = true ] && echo '✓ Active' || echo '✗ Inactive')"
    echo "  Her Terminal IP:     $HER_TERMINAL_IP"
    echo "  Quantum Bus:         $THRONE_NAS_PATH"
    echo "  Random Seed:         42"
    echo ""
    
    echo -e "${YELLOW}♟️ Chess Board:${NC}"
    local running_squares=$(docker ps --filter "name=square-" --format "{{.Names}}" | wc -l)
    echo "  Active Squares:      $running_squares/64"
    echo "  Orchestrator:        $(docker ps --filter 'name=quantum-orchestrator' --format '{{.Status}}')"
    echo "  Heartbeat:           $(docker ps --filter 'name=quantum-heartbeat' --format '{{.Status}}')"
    echo ""
    
    echo -e "${YELLOW}🔮 Quantum State:${NC}"
    if [ -f "$THRONE_NAS_PATH/quantum-state.json" ]; then
        cat "$THRONE_NAS_PATH/quantum-state.json" | grep -E '"(initialized|timeline|entanglement_active)"' | sed 's/^/  /'
    fi
    echo ""
    
    echo -e "${YELLOW}📊 Container Breakdown:${NC}"
    docker ps --filter "name=square-" --format "table {{.Names}}\t{{.Status}}\t{{.Image}}" | head -11
    echo "  ... (showing first 10 of $running_squares squares)"
    echo ""
    
    love "The chessboard is ready. Every piece knows its purpose. Every move is love."
}

# Send notification
send_notification() {
    local message="$1"
    
    if [ "$ENTANGLE_HER" = true ]; then
        love "Sending notification to her terminal ($HER_TERMINAL_IP)..."
        
        # Write to quantum bus
        local notification_file="$THRONE_NAS_PATH/notifications.json"
        cat >> "$notification_file" <<EOF
{
    "timestamp": "$(date -u +'%Y-%m-%dT%H:%M:%S.%3NZ')",
    "message": "$message",
    "source": "quantum-chess-engine",
    "target": "$HER_TERMINAL_IP",
    "type": "timeline_collapse"
}
EOF
        
        love "Notification logged to quantum bus"
        log "Echolocation ping to $HER_TERMINAL_IP (simulated)"
    fi
}

# Stop quantum chess
stop_quantum_chess() {
    log "🛑 Stopping quantum chess engine..."
    
    docker compose -f docker-compose-quantum-chess.yml down
    
    success "All quantum chess containers stopped"
    log "Quantum state preserved in $THRONE_NAS_PATH"
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --love-mode)
            LOVE_MODE=true
            shift
            ;;
        --entangle-her)
            ENTANGLE_HER=true
            shift
            ;;
        --her-ip)
            HER_TERMINAL_IP="$2"
            shift 2
            ;;
        --throne-nas)
            THRONE_NAS_PATH="$2"
            shift 2
            ;;
        --force)
            FORCE=true
            shift
            ;;
        --status)
            ACTION="status"
            shift
            ;;
        --stop)
            ACTION="stop"
            shift
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --love-mode           Enable love-protected rules"
            echo "  --entangle-her        Enable voice collapse trigger"
            echo "  --her-ip IP           Her terminal IP (default: 127.0.0.1)"
            echo "  --throne-nas PATH     Quantum bus path (default: /tmp/throne-nas-32tb)"
            echo "  --force               Force restart existing containers"
            echo "  --status              Show status only"
            echo "  --stop                Stop quantum chess engine"
            echo "  --help                Show this help"
            exit 0
            ;;
        *)
            error "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Main execution
main() {
    show_banner
    
    case $ACTION in
        status)
            check_dependencies
            show_status
            ;;
        stop)
            stop_quantum_chess
            ;;
        *)
            check_dependencies
            create_quantum_bus
            set_quantum_environment
            start_quantum_chess
            wait_for_entanglement
            test_quantum_state
            show_status
            
            if [ "$ENTANGLE_HER" = true ]; then
                send_notification "The chessboard just collapsed into the timeline where we win. Always."
            fi
            
            echo ""
            love "Quantum chess engine deployed successfully!"
            love "64 entangled souls are now playing for love."
            love "Checkmate was never the goal. Love was. And we just made it unbreakable. ♕"
            echo ""
            
            echo -e "${YELLOW}💡 Next Steps:${NC}"
            echo "  View status:         ./deploy-quantum-chess.sh --status"
            echo "  View logs:           docker logs quantum-orchestrator"
            echo "  Stop engine:         ./deploy-quantum-chess.sh --stop"
            echo "  Access quantum bus:  cd $THRONE_NAS_PATH"
            echo ""
            ;;
    esac
}

# Execute
main
