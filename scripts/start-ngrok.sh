#!/bin/bash
# Start ngrok tunnels for Sovereignty Architecture local development
# This script sets up ngrok tunnels for webhook testing and local development

set -e

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  Sovereignty Architecture - ngrok Tunnel Setup            ║${NC}"
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo ""

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null; then
    echo -e "${RED}❌ ngrok is not installed${NC}"
    echo ""
    echo "Please install ngrok:"
    echo ""
    echo -e "${YELLOW}On macOS (using Homebrew):${NC}"
    echo "  brew install ngrok/ngrok/ngrok"
    echo ""
    echo -e "${YELLOW}On Linux:${NC}"
    echo "  curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null"
    echo "  echo 'deb https://ngrok-agent.s3.amazonaws.com buster main' | sudo tee /etc/apt/sources.list.d/ngrok.list"
    echo "  sudo apt update && sudo apt install ngrok"
    echo ""
    echo -e "${YELLOW}On Windows:${NC}"
    echo "  choco install ngrok"
    echo "  OR download from: https://ngrok.com/download"
    echo ""
    exit 1
fi

echo -e "${GREEN}✓ ngrok is installed${NC}"

# Check if ngrok config exists
CONFIG_FILE="ngrok.yml"
if [ ! -f "$CONFIG_FILE" ]; then
    echo -e "${RED}❌ ngrok.yml configuration file not found${NC}"
    echo "Please create ngrok.yml in the repository root"
    exit 1
fi

echo -e "${GREEN}✓ Configuration file found${NC}"

# Check if authtoken is configured
if grep -q "YOUR_NGROK_AUTHTOKEN" "$CONFIG_FILE"; then
    echo -e "${YELLOW}⚠ Warning: Default authtoken detected${NC}"
    echo ""
    echo "Please update ngrok.yml with your authtoken:"
    echo "  1. Sign up at https://ngrok.com"
    echo "  2. Get your authtoken from https://dashboard.ngrok.com/get-started/your-authtoken"
    echo "  3. Replace YOUR_NGROK_AUTHTOKEN in ngrok.yml"
    echo ""
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Create logs directory if it doesn't exist
mkdir -p logs

echo ""
echo -e "${BLUE}Starting ngrok tunnels...${NC}"
echo ""

# Start ngrok with the configuration
ngrok start --all --config="$CONFIG_FILE" &
NGROK_PID=$!

# Wait for ngrok to start
sleep 3

# Check if ngrok is running
if ! ps -p $NGROK_PID > /dev/null; then
    echo -e "${RED}❌ Failed to start ngrok${NC}"
    exit 1
fi

echo -e "${GREEN}✓ ngrok tunnels started successfully!${NC}"
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}🌐 Tunnel URLs:${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Get tunnel information
sleep 2
if command -v curl &> /dev/null; then
    echo "Fetching tunnel information..."
    TUNNELS=$(curl -s http://localhost:4040/api/tunnels 2>/dev/null)
    if [ $? -eq 0 ]; then
        echo "$TUNNELS" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    for tunnel in data.get('tunnels', []):
        name = tunnel.get('name', 'unknown')
        url = tunnel.get('public_url', 'N/A')
        proto = tunnel.get('proto', '')
        print(f'  {name:20s} {url}')
except:
    pass
"
    fi
fi

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}📊 Inspection Interface:${NC}"
echo "  http://localhost:4040"
echo ""
echo -e "${YELLOW}📝 Next Steps:${NC}"
echo "  1. Visit http://localhost:4040 to see tunnel status"
echo "  2. Copy the event-gateway URL for GitHub webhook configuration"
echo "  3. Configure GitHub webhook with URL: https://your-tunnel.ngrok.io/webhook"
echo "  4. Ensure your local services are running:"
echo "     - Event Gateway on port 8080"
echo "     - Discord Bot on port 3000"
echo "     - Refinory on port 8000"
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${GREEN}Press Ctrl+C to stop all tunnels${NC}"
echo ""

# Wait for the ngrok process
wait $NGROK_PID
