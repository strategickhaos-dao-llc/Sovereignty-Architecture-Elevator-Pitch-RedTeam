#!/bin/bash
# SovereignPRManager Installation Script
# Autonomous PR Orchestration System

set -e

echo "=============================================="
echo "🤖 SovereignPRManager Installation"
echo "=============================================="
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Python version: $PYTHON_VERSION"

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is required but not installed."
    exit 1
fi
echo "✅ pip3 is available"

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo ""
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Check for required environment variables
echo ""
echo "🔍 Checking environment variables..."

MISSING_VARS=""

if [ -z "$GITHUB_TOKEN" ]; then
    MISSING_VARS="$MISSING_VARS GITHUB_TOKEN"
fi

if [ -z "$GITHUB_REPO" ]; then
    MISSING_VARS="$MISSING_VARS GITHUB_REPO"
fi

if [ -n "$MISSING_VARS" ]; then
    echo ""
    echo "⚠️  Warning: The following environment variables are not set:"
    echo "   $MISSING_VARS"
    echo ""
    echo "   Set them before running SovereignPRManager:"
    echo "   export GITHUB_TOKEN='your_token'"
    echo "   export GITHUB_REPO='owner/repo'"
    echo ""
fi

echo ""
echo "=============================================="
echo "✅ Installation Complete!"
echo "=============================================="
echo ""
echo "Usage:"
echo "  # Process all open PRs:"
echo "  python -m sovereign_pr_manager.process_existing_prs"
echo ""
echo "  # Process a specific PR:"
echo "  python -m sovereign_pr_manager.manager --pr 123"
echo ""
echo "  # Start monitoring mode:"
echo "  python -m sovereign_pr_manager.manager --monitor"
echo ""
echo "  # Build Docker image:"
echo "  docker build -t sovereignprmanager -f Dockerfile .."
echo ""
echo "  # Deploy to Kubernetes:"
echo "  kubectl apply -f k8s/"
echo ""
