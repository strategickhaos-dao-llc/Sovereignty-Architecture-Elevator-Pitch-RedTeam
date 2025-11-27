#!/bin/bash
# Post-create script for Sovereignty Architecture Dev Container

set -e

echo "🏛️ Setting up Sovereignty Architecture environment..."

# Initialize IPFS if not already initialized
if [ ! -d ~/.ipfs ]; then
    echo "📦 Initializing IPFS..."
    ipfs init --profile=server
fi

# Install Python dependencies if requirements exist
if [ -f requirements.txt ]; then
    echo "🐍 Installing Python dependencies..."
    pip install -r requirements.txt
fi

if [ -f requirements.alignment.txt ]; then
    pip install -r requirements.alignment.txt
fi

# Install Node.js dependencies
if [ -f package.json ]; then
    echo "📦 Installing Node.js dependencies..."
    npm install
fi

# Set up GPG if keys exist
if [ -d ~/.gnupg ]; then
    echo "🔐 GPG keys detected"
    chmod 700 ~/.gnupg
    chmod 600 ~/.gnupg/* 2>/dev/null || true
fi

# Create provenance directory
mkdir -p provenance audit

# Verify tools are installed
echo ""
echo "🔧 Verifying installed tools..."
echo "  b3sum: $(b3sum --version 2>/dev/null || echo 'not found')"
echo "  ipfs: $(ipfs version 2>/dev/null | head -1 || echo 'not found')"
echo "  cosign: $(cosign version 2>/dev/null | head -1 || echo 'not found')"
echo "  syft: $(syft version 2>/dev/null || echo 'not found')"
echo "  grype: $(grype version 2>/dev/null | head -1 || echo 'not found')"

echo ""
echo "✅ Sovereignty Architecture Dev Container ready!"
echo ""
echo "Available CLI commands:"
echo "  pin      - Pin bundle to IPFS"
echo "  sign     - GPG sign bundle"
echo "  commit   - Commit with provenance"
echo "  verify   - Verify bundle integrity"
echo "  receipts - Generate provenance receipts"
