#!/bin/bash
# Setup script for Sovereignty Architecture Data Pipeline

set -e

echo "============================================================"
echo "🤖 Sovereignty Architecture - Data Pipeline Setup"
echo "============================================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running on Linux/Mac
if [[ "$OSTYPE" == "linux-gnu"* ]] || [[ "$OSTYPE" == "darwin"* ]]; then
    echo "✅ Platform: $OSTYPE"
else
    echo "⚠️  Warning: This script is designed for Linux/Mac. Windows users should use WSL or adapt the script."
fi

# Check Python version
echo ""
echo "📋 Checking prerequisites..."
echo ""

if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo "✅ Python 3 installed: $PYTHON_VERSION"
else
    echo -e "${RED}❌ Python 3 not found. Please install Python 3.7 or higher.${NC}"
    exit 1
fi

# Check for git
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version | cut -d' ' -f3)
    echo "✅ Git installed: $GIT_VERSION"
else
    echo -e "${YELLOW}⚠️  Git not found. Git integration will be disabled.${NC}"
fi

# Install Python dependencies
echo ""
echo "📦 Checking Python dependencies..."
if python3 -c "import yaml" 2>/dev/null; then
    echo "✅ PyYAML already installed"
else
    echo "   Installing PyYAML..."
    pip3 install pyyaml -q
    echo "✅ PyYAML installed"
fi

# Create directory structure
echo ""
echo "📁 Creating directory structure..."
mkdir -p ingest
mkdir -p logs
echo "✅ Directories created"

# Create vault structure (optional)
read -p "📂 Do you want to create a local vault structure? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    mkdir -p vault/labs/{cyber-recon,architecture,ai-ml,devops,legal,business}
    mkdir -p vault/canvas
    mkdir -p vault/daily
    mkdir -p vault/templates
    mkdir -p vault/assets
    echo "✅ Vault structure created"
else
    echo "ℹ️  Vault structure skipped. You can create it later."
fi

# Make scripts executable
echo ""
echo "🔧 Setting executable permissions..."
chmod +x ingest_daemon.py
if [ -f "gl2discord.sh" ]; then
    chmod +x gl2discord.sh
    echo "✅ Scripts are executable"
fi

# Create sample .env if it doesn't exist
if [ ! -f ".env.pipeline" ]; then
    echo ""
    echo "⚙️  Creating sample environment configuration..."
    cat > .env.pipeline << 'EOF'
# Sovereignty Architecture Data Pipeline Configuration

# Obsidian Vault Path (customize to your setup)
VAULT_PATH="$HOME/ObsidianVault"

# Discord Integration (optional)
DISCORD_TOKEN=""
KNOWLEDGE_FEED_CHANNEL=""

# Ingest Daemon Settings
INGEST_INTERVAL=5
INGEST_CONFIG="lab.yaml"

# Git Settings
GIT_AUTO_COMMIT=true
GIT_COMMIT_SIGNING=false

# MCP Server (if running)
MCP_SERVER_URL="http://localhost:3100"
EOF
    echo "✅ Created .env.pipeline (customize as needed)"
    echo "   Edit .env.pipeline to configure your setup"
fi

# Test the daemon
echo ""
echo "🧪 Testing ingest daemon..."
python3 ingest_daemon.py --help > /dev/null
if [ $? -eq 0 ]; then
    echo "✅ Ingest daemon is working"
else
    echo -e "${RED}❌ Ingest daemon test failed${NC}"
    exit 1
fi

# Print next steps
echo ""
echo "============================================================"
echo "✅ Setup Complete!"
echo "============================================================"
echo ""
echo "📖 Next Steps:"
echo ""
echo "1. Review and customize configuration:"
echo "   - Edit lab.yaml to define your labs and keywords"
echo "   - Edit tools.yaml to configure MCP tools"
echo "   - Edit .env.pipeline for environment settings"
echo ""
echo "2. Start the ingest daemon:"
echo "   python3 ingest_daemon.py"
echo ""
echo "3. Test with a file:"
echo "   echo 'Test content' > ingest/test.txt"
echo ""
echo "4. Monitor logs:"
echo "   tail -f logs/ingest_events.jsonl | jq ."
echo ""
echo "5. Read the documentation:"
echo "   - ARCHITECTURE_DATA_PIPELINE.md - Complete architecture guide"
echo "   - GITLENS_100_WAYS.md - GitLens integration"
echo "   - lab.yaml - Lab definitions"
echo "   - tools.yaml - Tool definitions"
echo ""
echo "📚 For more information:"
echo "   https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-"
echo ""
echo "🔥 Built by the Strategickhaos Swarm Intelligence collective"
echo ""
