#!/bin/bash
# Strategickhaos Legion Kernel Initialization Script
# Run this in ANY codespace to connect to the Legion
#
# Usage: chmod +x init.sh && ./init.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

echo "🏛️ Strategickhaos Legion Kernel Initializer"
echo "============================================"
echo ""

# 1. Check Python version
echo "📋 Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi
PYTHON_VERSION=$(python3 --version 2>&1)
echo "   Found: $PYTHON_VERSION"

# 2. Install dependencies
echo ""
echo "📦 Installing dependencies..."
REQUIREMENTS_FILE="${SCRIPT_DIR}/../requirements.txt"
if [ -f "$REQUIREMENTS_FILE" ]; then
    pip install -q -r "$REQUIREMENTS_FILE" 2>/dev/null || {
        echo "   ⚠️  Some dependencies could not be installed"
        echo "   Install manually: pip install gitpython pyyaml requests discord.py"
    }
else
    # Install core dependencies directly
    pip install -q gitpython pyyaml requests 2>/dev/null || {
        echo "   ⚠️  Could not install dependencies automatically"
    }
fi
echo "   ✅ Dependencies ready"

# 3. Configure Git (if not already configured)
echo ""
echo "🔧 Configuring Git..."
if [ -z "$(git config --global user.name)" ]; then
    git config --global user.name "Strategickhaos Legion"
fi
if [ -z "$(git config --global user.email)" ]; then
    git config --global user.email "legion@strategickhaos.io"
fi
echo "   User: $(git config --global user.name)"
echo "   Email: $(git config --global user.email)"

# Optional: Enable GPG signing if key is available
if [ -n "$GPG_KEY_PATH" ] && [ -f "$GPG_KEY_PATH" ]; then
    git config --global commit.gpgsign true
    echo "   ✅ GPG signing enabled"
else
    echo "   ℹ️  GPG signing not configured (set GPG_KEY_PATH to enable)"
fi

# 4. Connect to collective
echo ""
echo "🔗 Connecting to Strategickhaos collective..."
cd "$REPO_ROOT"
python3 "${SCRIPT_DIR}/connect.py"

# 5. Start daemon (optional, in background)
echo ""
echo "🔄 Starting proposal daemon..."
if [ "$1" = "--daemon" ] || [ "$1" = "-d" ]; then
    nohup python3 "${SCRIPT_DIR}/daemon.py" > /tmp/legion_daemon.log 2>&1 &
    DAEMON_PID=$!
    echo "   Daemon started (PID: $DAEMON_PID)"
    echo "   Logs: /tmp/legion_daemon.log"
else
    echo "   ℹ️  Daemon not started (use --daemon flag to enable)"
fi

# 6. Print status
echo ""
echo "============================================"
echo "✅ Connected to Strategickhaos Legions OS"
echo ""
echo "Workspace ID: ${CODESPACE_NAME:-$(hostname)}"
echo ""

# Try to get branch count from GitHub API (non-blocking)
if command -v curl &> /dev/null && command -v jq &> /dev/null; then
    GITHUB_REPO=$(git config --get remote.origin.url 2>/dev/null | sed 's/.*github.com[:/]\(.*\)\.git/\1/' || echo "")
    if [ -n "$GITHUB_REPO" ]; then
        BRANCHES=$(curl -s "https://api.github.com/repos/${GITHUB_REPO}/branches" 2>/dev/null | jq length 2>/dev/null || echo "?")
        echo "Active branches: $BRANCHES"
    fi
fi

echo ""
echo "📚 Quick Commands:"
echo "   Submit proposal: python3 ${SCRIPT_DIR}/connect.py"
echo "   Run daemon:      python3 ${SCRIPT_DIR}/daemon.py"
echo "   Discord bot:     python3 ${SCRIPT_DIR}/discord_bot.py"
echo ""
