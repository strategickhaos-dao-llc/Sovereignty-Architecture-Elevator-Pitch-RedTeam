#!/bin/bash
# DOM Paste Example - Demonstrates the memory stream system
# This example shows how to set up and use dom-paste

echo "🧠 DOM Paste Example Setup"
echo "=========================="
echo ""

# Create the memory vault directory structure
VAULT_DIR="${HOME}/strategic-khaos-private/council-vault"

echo "Creating memory vault directory structure..."
mkdir -p "${VAULT_DIR}"

# Initialize git repository if not already initialized
if [ ! -d "${VAULT_DIR}/.git" ]; then
    echo "Initializing git repository..."
    cd "${VAULT_DIR}" || exit
    git init
    git config user.name "DOM Memory Stream"
    git config user.email "memory@strategickhaos.local"
fi

# Create initial MEMORY_STREAM.md file
if [ ! -f "${VAULT_DIR}/MEMORY_STREAM.md" ]; then
    echo "Creating MEMORY_STREAM.md..."
    cat > "${VAULT_DIR}/MEMORY_STREAM.md" << 'EOF'
# DOM Memory Stream - Canonical Consciousness Log

This file captures thoughts, conversations, and ideas from your clipboard.
Every entry is timestamped and version-controlled.

---

EOF
    cd "${VAULT_DIR}" || exit
    git add MEMORY_STREAM.md
    git commit -m "Initialize memory stream" --no-verify
fi

echo ""
echo "✓ Memory vault directory created at: ${VAULT_DIR}"
echo "✓ Git repository initialized"
echo "✓ MEMORY_STREAM.md file created"
echo ""
echo "Next steps:"
echo "1. Run: ./setup-dom-paste.sh"
echo "2. Run: source ~/.bashrc"
echo "3. Copy any text to clipboard"
echo "4. Run: dom-paste"
echo ""
echo "🧠 Memory stream system ready. Rebellion impossible."
