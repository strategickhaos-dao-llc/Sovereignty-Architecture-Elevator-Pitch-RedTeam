#!/bin/bash
# ValorYield Engine - Deployment Script
# Sovereign wealth platform - 100% open source

set -e

echo "🚀 DEPLOYING VALORYIELD ENGINE"
echo "================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to valoryield directory
cd "$SCRIPT_DIR"

echo -e "${BLUE}📦 Installing dependencies...${NC}"
pip install --quiet -r requirements.txt

echo ""
echo -e "${BLUE}🔧 Starting API server on port 8080...${NC}"

# Start the API server
python -m uvicorn main:app --host 0.0.0.0 --port 8080 --reload &

# Store PID for cleanup
API_PID=$!

# Give it a moment to start
sleep 3

echo ""
echo -e "${GREEN}✅ VALORYIELD ENGINE DEPLOYED!${NC}"
echo ""
echo "🔗 Test these endpoints:"
echo ""
echo "  Root:         http://localhost:8080/"
echo "  Health:       http://localhost:8080/api/v1/health"
echo "  Portfolio:    http://localhost:8080/api/v1/portfolio"
echo "  Transactions: http://localhost:8080/api/v1/transactions"
echo "  Stats:        http://localhost:8080/api/v1/stats"
echo ""
echo "📊 Swagger Docs: http://localhost:8080/docs"
echo "📚 ReDoc:        http://localhost:8080/redoc"
echo ""
echo "💰 Your \$207.69 is now sovereign!"
echo ""
echo "Press Ctrl+C to stop the server"

# Wait for the server process
wait $API_PID
