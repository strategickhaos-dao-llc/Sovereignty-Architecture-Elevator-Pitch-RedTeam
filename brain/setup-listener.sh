#!/bin/bash
# Strategickhaos Listener Setup Script (Unix/Linux/macOS)
# This script creates a virtual environment and installs dependencies

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/jarvis_venv"

echo "🔧 Strategickhaos Listener Setup"
echo "================================="
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "✅ Found: $PYTHON_VERSION"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment at: $VENV_DIR"
if [ -d "$VENV_DIR" ]; then
    echo "⚠️  Virtual environment already exists. Removing..."
    rm -rf "$VENV_DIR"
fi

python3 -m venv "$VENV_DIR"
echo "✅ Virtual environment created"
echo ""

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Upgrade pip
echo "📥 Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies from requirements.txt..."
pip install -r "$SCRIPT_DIR/requirements.txt"

echo ""
echo "✅ Setup complete!"
echo ""
echo "To use the listener:"
echo "  1. Activate the virtual environment:"
echo "     source $VENV_DIR/bin/activate"
echo ""
echo "  2. Run the listener:"
echo "     python3 $SCRIPT_DIR/plugins/listener_bind_58563.py"
echo ""
echo "  Or run with logging:"
echo "     python3 $SCRIPT_DIR/plugins/listener_bind_58563.py | tee $SCRIPT_DIR/logs/listener_output.log"
echo ""
