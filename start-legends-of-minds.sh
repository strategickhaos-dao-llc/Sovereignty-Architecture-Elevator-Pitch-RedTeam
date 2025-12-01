#!/bin/bash
# Quick Start - Legends of Minds Unified Agent Orchestration Platform

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LEGENDS_DIR="$REPO_ROOT/legends_of_minds"

echo "🧠 Legends of Minds - Unified Agent Orchestration Platform"
echo "=========================================================="
echo ""
echo "Total Sovereignty | Full Automation | End-to-End Audit"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed."
    echo "Please install Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not installed."
    echo "Please install Docker Compose: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"
echo ""

# Navigate to legends_of_minds directory
cd "$LEGENDS_DIR"

echo "📦 Starting Legends of Minds services..."
echo ""

# Start services
docker-compose up -d

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check health
echo ""
echo "🏥 Checking service health..."

if curl -sf http://localhost:8080/health > /dev/null 2>&1; then
    echo "✅ Orchestrator is healthy"
else
    echo "⚠️  Orchestrator is starting up... (this may take a moment)"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ Legends of Minds is now running!"
echo ""
echo "📊 Access Points:"
echo "   • Command Center:  http://localhost:8080"
echo "   • API Docs:        http://localhost:8080/docs"
echo "   • Health Check:    http://localhost:8080/health"
echo ""
echo "🏛️  Available Departments (10 total):"
echo "   1. Proof Ledger        - Immutable audit trail"
echo "   2. Legal Compliance    - 30+ laws (DAO, IP, Privacy, etc.)"
echo "   3. GitLens             - Repository analysis"
echo "   4. Refinery MCP        - Model Context Protocol"
echo "   5. Compose Generator   - Docker Compose generation"
echo "   6. YAML Generator      - Config file generation"
echo "   7. Repo Builder        - Automated scaffolding"
echo "   8. Code Search         - Fast code search"
echo "   9. Picture Search      - Image classification"
echo "   10. Glossary           - Knowledge base"
echo ""
echo "🔍 Service Status:"
docker-compose ps
echo ""
echo "📋 View Logs:"
echo "   docker-compose -f $LEGENDS_DIR/docker-compose.yml logs -f"
echo ""
echo "⏹️  Stop Services:"
echo "   docker-compose -f $LEGENDS_DIR/docker-compose.yml down"
echo ""
echo "📖 Full Documentation:"
echo "   • $REPO_ROOT/LEGENDS_OF_MINDS_DEPLOYMENT.md"
echo "   • $LEGENDS_DIR/README.md"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🛡️  You now have total sovereignty over your AI infrastructure!"
echo ""
