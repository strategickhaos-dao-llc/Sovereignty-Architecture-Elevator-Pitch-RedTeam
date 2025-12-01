#!/bin/bash
# Chess Council Agent Entrypoint Script
# Initializes the agent environment and starts services

set -e

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[AGENT]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Read environment configuration
BOARD_LAYER="${BOARD_LAYER:-0}"
AGENT_ID="${AGENT_ID:-agent-0}"
AGENT_POSITION=$(echo "$AGENT_ID" | grep -oE '[0-9]+$' || echo "0")

log "═══════════════════════════════════════════════════════════"
log "10-DIMENSIONAL CHESS COUNCIL AGENT"
log "═══════════════════════════════════════════════════════════"
log "Board Layer: $BOARD_LAYER"
log "Agent ID: $AGENT_ID"
log "Position: $AGENT_POSITION"
log "═══════════════════════════════════════════════════════════"

# Calculate frequency
calculate_frequency() {
    python3 << EOF
import math
board = int("$BOARD_LAYER")
position = int("$AGENT_POSITION")
row = position // 8
col = position % 8

board_offset = board * 64
global_position = board_offset + (row * 8) + col
piano_key = global_position % 88
frequency = 440.0 * math.pow(2, (piano_key - 49) / 12.0)

notes = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
octave = (piano_key + 8) // 12
note = notes[(piano_key) % 12]

print(f"FREQUENCY_HZ={frequency:.2f}")
print(f"PIANO_KEY={piano_key + 1}")
print(f"NOTE_NAME={note}{octave}")
EOF
}

# Export frequency variables
eval "$(calculate_frequency)"
export FREQUENCY_HZ PIANO_KEY NOTE_NAME

log "Frequency: ${FREQUENCY_HZ} Hz"
log "Note: ${NOTE_NAME} (Piano Key ${PIANO_KEY})"

# Initialize workspace
init_workspace() {
    log "Initializing workspace..."
    
    # Create agent-specific directories
    mkdir -p /workspace/papers/${BOARD_LAYER}/${AGENT_POSITION}
    mkdir -p /workspace/games/${AGENT_ID}
    mkdir -p /workspace/syntheses/${AGENT_ID}
    
    # Write agent config
    cat > /config/agent.yaml << EOF
agent:
  id: "${AGENT_ID}"
  board_layer: ${BOARD_LAYER}
  position: ${AGENT_POSITION}
  frequency:
    hz: ${FREQUENCY_HZ}
    piano_key: ${PIANO_KEY}
    note: "${NOTE_NAME}"
  
  llm:
    primary: "${PRIMARY_MODEL:-qwen2.5:72b}"
    ollama_host: "${OLLAMA_HOST:-http://localhost:11434}"
    grok_api: "${GROK_API_KEY:+enabled}"
  
  tools:
    stockfish: "${STOCKFISH_PATH:-/usr/games/stockfish}"
    latex: "pdflatex"
    pandoc: "pandoc"
  
  endpoints:
    api: "http://0.0.0.0:8080"
    metrics: "http://0.0.0.0:9090"
    qdrant: "${QDRANT_URL:-http://qdrant:6333}"
    postgres: "\${POSTGRES_DSN}"
EOF
    
    log "Workspace initialized"
}

# Start SSH server
start_ssh() {
    log "Starting SSH server..."
    sudo /usr/sbin/sshd -D &
}

# Start X11 virtual framebuffer
start_xvfb() {
    log "Starting X11 virtual framebuffer..."
    Xvfb :0 -screen 0 1920x1080x24 &
    export DISPLAY=:0
    sleep 2
    fluxbox &
}

# Start VNC server
start_vnc() {
    log "Starting VNC server..."
    x11vnc -display :0 -forever -shared -rfbport 5900 &
}

# Start agent API server
start_api() {
    log "Starting Agent API server..."
    python3 /usr/local/bin/agent-api.py &
}

# Main entrypoint
main() {
    case "${1:-agent}" in
        agent)
            init_workspace
            start_ssh
            start_xvfb
            start_vnc
            start_api
            
            log "Agent ${AGENT_ID} is ready!"
            log "API: http://0.0.0.0:8080"
            log "VNC: :5900"
            log "SSH: :22"
            
            # Keep container running
            tail -f /dev/null
            ;;
        
        shell)
            exec /bin/bash
            ;;
        
        *)
            exec "$@"
            ;;
    esac
}

main "$@"
