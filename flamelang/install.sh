#!/bin/bash
# FlameLang Installation Script

set -e

echo "🔥 Installing FlameLang..."

# Check Python version
python3 --version >/dev/null 2>&1 || {
    echo "Error: Python 3 is required"
    exit 1
}

# Install dependencies
echo "Installing dependencies..."
pip3 install numpy scipy sympy psutil || {
    echo "Error: Failed to install dependencies"
    exit 1
}

# Create symlink to flamelang command
INSTALL_DIR="/usr/local/bin"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -w "$INSTALL_DIR" ]; then
    ln -sf "$SCRIPT_DIR/flamelang" "$INSTALL_DIR/flamelang"
    echo "✓ Installed flamelang command to $INSTALL_DIR"
else
    echo "⚠️  Cannot write to $INSTALL_DIR"
    echo "   Run with sudo or add $SCRIPT_DIR to your PATH:"
    echo "   export PATH=\"$SCRIPT_DIR:\$PATH\""
fi

echo ""
echo "🔥 FlameLang installation complete!"
echo ""
echo "Try these commands:"
echo "  flamelang repl              # Start REPL"
echo "  flamelang info              # System info"
echo "  flamelang export-glyphs     # Export glyph table"
