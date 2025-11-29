#!/bin/bash
# Strategickhaos Webhook Inbox - Quick Start Script
# Usage: ./start.sh [secret]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Strategickhaos Webhook Inbox Startup${NC}"
echo "=================================================="

# Check if docker is available
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed or not in PATH${NC}"
    exit 1
fi

# Check for webhook secret
if [ -z "$GITHUB_WEBHOOK_SECRET" ]; then
    if [ -n "$1" ]; then
        export GITHUB_WEBHOOK_SECRET="$1"
        echo -e "${GREEN}✓${NC} Using provided webhook secret"
    else
        echo -e "${YELLOW}⚠️  No webhook secret provided${NC}"
        echo "Generate one with: python -c \"import secrets; print(secrets.token_hex(32))\""
        echo ""
        read -p "Enter webhook secret (or press Enter to use default): " secret
        if [ -z "$secret" ]; then
            export GITHUB_WEBHOOK_SECRET="your-secret-here"
            echo -e "${YELLOW}⚠️  Using default secret (not secure for production!)${NC}"
        else
            export GITHUB_WEBHOOK_SECRET="$secret"
            echo -e "${GREEN}✓${NC} Using provided secret"
        fi
    fi
fi

echo ""
echo "Starting webhook inbox service..."
echo ""

# Check if using docker compose or docker-compose
if docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
elif docker-compose version &> /dev/null; then
    COMPOSE_CMD="docker-compose"
else
    echo -e "${RED}❌ Neither 'docker compose' nor 'docker-compose' is available${NC}"
    exit 1
fi

# Start the service
$COMPOSE_CMD up -d

echo ""
echo -e "${GREEN}✓ Webhook inbox service started!${NC}"
echo ""
echo "📊 Service Status:"
$COMPOSE_CMD ps
echo ""
echo "🔗 Endpoints:"
echo "  - Health: http://localhost:5000/health"
echo "  - Webhook: http://localhost:5000/github-webhook"
echo ""
echo "📋 Useful Commands:"
echo "  - View logs: $COMPOSE_CMD logs -f"
echo "  - View events: docker exec strategickhaos-webhook-inbox cat /inbox/events.log"
echo "  - Stop service: $COMPOSE_CMD down"
echo ""
echo "💡 For GitHub webhook setup, expose with ngrok:"
echo "  ngrok http 5000"
echo ""
