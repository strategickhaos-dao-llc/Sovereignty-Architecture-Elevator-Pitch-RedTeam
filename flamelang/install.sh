#!/bin/bash
# FlameLang One-Command Installer

set -e

echo "============================================================"
echo "🔥 FlameLang Installer"
echo "============================================================"
echo ""

# Check Python version
echo "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Error: Python 3.8+ required (found $PYTHON_VERSION)"
    exit 1
fi

echo "✓ Python $PYTHON_VERSION detected"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip3 install --user numpy sympy scipy psutil

echo ""
echo "✓ Dependencies installed"
echo ""

# Make executable
chmod +x flamelang
echo "✓ Made flamelang executable"
echo ""

# Run tests
echo "Running tests..."
python3 tests/test_all.py

if [ $? -eq 0 ]; then
    echo ""
    echo "============================================================"
    echo "🔥 Installation Complete!"
    echo "============================================================"
    echo ""
    echo "Quick start:"
    echo "  ./flamelang repl              # Start REPL"
    echo "  python3 demo.py               # Run demo"
    echo "  ./flamelang run examples/demo.fl  # Execute example"
    echo ""
    echo "🔥 Stay sovereign."
    echo ""
else
    echo ""
    echo "❌ Tests failed. Please check the output above."
    exit 1
fi
