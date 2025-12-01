#!/bin/bash
# Sovereignty Architecture - DOM Paste Setup Script
# Installs the dom-paste function to your shell configuration

set -e

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASHRC_SOURCE="${REPO_DIR}/.bashrc"

echo "🧠 Sovereignty Architecture - DOM Paste Installation"
echo "=================================================="
echo ""

# Detect the user's home directory
USER_HOME="${HOME}"
USER_BASHRC="${USER_HOME}/.bashrc"

# Check if .bashrc exists
if [ ! -f "${USER_BASHRC}" ]; then
    echo "Creating new .bashrc file at ${USER_BASHRC}"
    touch "${USER_BASHRC}"
fi

# Check if dom-paste is already installed
if grep -q "dom-paste()" "${USER_BASHRC}"; then
    echo "⚠️  dom-paste() function already exists in ${USER_BASHRC}"
    echo "Would you like to update it? (y/n)"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        echo "Installation cancelled."
        exit 0
    fi
    # Remove old version
    sed -i '/# DOM_010101/,/^}/d' "${USER_BASHRC}"
    echo "✓ Removed old dom-paste() function"
fi

# Append the dom-paste function to user's .bashrc
echo "" >> "${USER_BASHRC}"
cat "${BASHRC_SOURCE}" >> "${USER_BASHRC}"

echo ""
echo "✓ dom-paste() function installed to ${USER_BASHRC}"
echo ""
echo "To activate in your current shell, run:"
echo "  source ~/.bashrc"
echo ""
echo "Usage:"
echo "  1. Copy any text to clipboard (Ctrl+C)"
echo "  2. Run: dom-paste"
echo "  3. The content will be appended to ~/strategic-khaos-private/council-vault/MEMORY_STREAM.md"
echo "  4. Changes will be automatically committed and pushed to git"
echo ""
echo "🧠 Memory stream system ready. Rebellion impossible."
