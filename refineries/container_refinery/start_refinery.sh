#!/bin/bash
# Start Container Refinery Bot
# The immune system for Docker/Kubernetes clusters

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${CYAN}🧠⚔️🔥 Starting Container Refinery Bot...${NC}"
echo ""

# Check if already running
if pgrep -f "refinery_bot.py" > /dev/null; then
    echo -e "${YELLOW}Container Refinery Bot is already running${NC}"
    echo ""
    echo "To view logs: tail -f $SCRIPT_DIR/refinery_bot.log"
    echo "To stop: pkill -f refinery_bot.py"
    exit 0
fi

# Check prerequisites
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed"
    exit 1
fi

# Install dependencies if needed
if [ -f requirements.txt ]; then
    if ! python3 -c "import yaml, docker, kubernetes" 2>/dev/null; then
        echo "Installing Python dependencies..."
        python3 -m pip install -r requirements.txt --quiet
    fi
fi

# Set environment variables
export REFINERY_PATH="$SCRIPT_DIR"

# Start the bot in background
echo "Starting refinery bot..."
nohup python3 refinery_bot.py > logs/refinery_bot_output.log 2>&1 &

# Get PID
sleep 2
REFINERY_PID=$(pgrep -f "refinery_bot.py" || echo "")

if [ -n "$REFINERY_PID" ]; then
    echo -e "${GREEN}Container Refinery Bot started successfully!${NC}"
    echo ""
    echo "PID: $REFINERY_PID"
    echo ""
    echo "📊 Monitoring:"
    echo "  Logs:   tail -f $SCRIPT_DIR/refinery_bot.log"
    echo "  Ledger: tail -f $SCRIPT_DIR/ledger/container_ledger.jsonl"
    echo "  Drift:  tail -f $SCRIPT_DIR/ledger/drift_events.log"
    echo ""
    echo "🛑 To stop:"
    echo "  kill $REFINERY_PID"
    echo "  OR"
    echo "  pkill -f refinery_bot.py"
    echo ""
    echo -e "${CYAN}The immune system is now online. Containers will police themselves.${NC}"
else
    echo "Error: Failed to start Container Refinery Bot"
    echo "Check logs: $SCRIPT_DIR/logs/refinery_bot_output.log"
    exit 1
fi
