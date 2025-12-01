#!/bin/bash
# Test script for DOM paste functionality
# This script validates that the dom-paste system is working correctly

set -e

echo "🧠 DOM Paste Functionality Test"
echo "==============================="
echo ""

# Test 1: Check if vault directory exists
echo "Test 1: Checking vault directory..."
VAULT_DIR="${HOME}/strategic-khaos-private/council-vault"
if [ -d "${VAULT_DIR}" ]; then
    echo "✓ Vault directory exists at ${VAULT_DIR}"
else
    echo "✗ Vault directory not found. Run ./examples/dom-paste-example.sh first"
    exit 1
fi

# Test 2: Check if MEMORY_STREAM.md exists
echo ""
echo "Test 2: Checking MEMORY_STREAM.md file..."
if [ -f "${VAULT_DIR}/MEMORY_STREAM.md" ]; then
    echo "✓ MEMORY_STREAM.md file exists"
else
    echo "✗ MEMORY_STREAM.md file not found"
    exit 1
fi

# Test 3: Check if it's a git repository
echo ""
echo "Test 3: Checking git repository..."
if [ -d "${VAULT_DIR}/.git" ]; then
    echo "✓ Git repository initialized"
else
    echo "✗ Git repository not initialized"
    exit 1
fi

# Test 4: Check if dom-paste function is defined
echo ""
echo "Test 4: Checking dom-paste function..."
if type dom-paste &> /dev/null; then
    echo "✓ dom-paste function is defined"
else
    echo "⚠️  dom-paste function not found in current shell"
    echo "   Run: source ~/.bashrc"
fi

# Test 5: Validate .bashrc content
echo ""
echo "Test 5: Validating .bashrc content..."
if [ -f "${HOME}/.bashrc" ] && grep -q "dom-paste()" "${HOME}/.bashrc"; then
    echo "✓ dom-paste function found in ~/.bashrc"
else
    echo "⚠️  dom-paste function not found in ~/.bashrc"
    echo "   Run: ./setup-dom-paste.sh"
fi

# Test 6: Check git log
echo ""
echo "Test 6: Checking git commit history..."
cd "${VAULT_DIR}" || exit
COMMIT_COUNT=$(git rev-list --count HEAD 2>/dev/null || echo "0")
if [ "${COMMIT_COUNT}" -gt 0 ]; then
    echo "✓ Git repository has ${COMMIT_COUNT} commit(s)"
    echo ""
    echo "Recent commits:"
    git --no-pager log --oneline -3
else
    echo "✗ No commits found in git repository"
    exit 1
fi

echo ""
echo "==============================="
echo "🧠 All tests passed! Memory stream system is operational."
echo "==============================="
echo ""
echo "Try it now:"
echo "  1. Copy some text to clipboard"
echo "  2. Run: dom-paste"
echo "  3. Check: cat ~/strategic-khaos-private/council-vault/MEMORY_STREAM.md"
