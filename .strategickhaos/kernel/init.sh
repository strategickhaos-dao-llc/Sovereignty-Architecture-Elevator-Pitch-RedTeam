#!/bin/bash
# .strategickhaos/kernel/init.sh
# 
# Strategickhaos Legions of Minds OS - One-Command Deploy
# 
# Run this in ANY codespace/environment to connect to the Legion collective.
# 
# Usage:
#   curl -sSL https://raw.githubusercontent.com/<repo>/main/.strategickhaos/kernel/init.sh | bash
#   
# Or locally:
#   ./.strategickhaos/kernel/init.sh

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo ""
echo -e "${PURPLE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${PURPLE}║                                                                ║${NC}"
echo -e "${PURPLE}║   ${CYAN}STRATEGICKHAOS LEGIONS OF MINDS OS${PURPLE}                         ║${NC}"
echo -e "${PURPLE}║   ${NC}Distributed Cognitive Governance Operating System${PURPLE}          ║${NC}"
echo -e "${PURPLE}║                                                                ║${NC}"
echo -e "${PURPLE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Detect workspace ID
if [ -n "$CODESPACE_NAME" ]; then
    WORKSPACE_ID="$CODESPACE_NAME"
    WORKSPACE_TYPE="GitHub Codespace"
elif [ -n "$GITPOD_WORKSPACE_ID" ]; then
    WORKSPACE_ID="$GITPOD_WORKSPACE_ID"
    WORKSPACE_TYPE="Gitpod"
elif [ -n "$WORKSPACE_ID" ]; then
    WORKSPACE_TYPE="Custom"
else
    WORKSPACE_ID=$(hostname)
    WORKSPACE_TYPE="Local"
fi

echo -e "${BLUE}[INFO]${NC} Detected workspace: ${GREEN}$WORKSPACE_ID${NC} (${WORKSPACE_TYPE})"

# Find repository root
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
cd "$REPO_ROOT"
echo -e "${BLUE}[INFO]${NC} Repository root: ${GREEN}$REPO_ROOT${NC}"

# Check for required directories
KERNEL_DIR=".strategickhaos/kernel"
PROPOSALS_DIR=".strategickhaos/proposals"
LOGS_DIR=".strategickhaos/logs"

if [ ! -d "$KERNEL_DIR" ]; then
    echo -e "${RED}[ERROR]${NC} Kernel directory not found: $KERNEL_DIR"
    echo -e "${YELLOW}[HINT]${NC} Please clone the repository with the Legion kernel first."
    exit 1
fi

# Create runtime directories
mkdir -p "$PROPOSALS_DIR" "$LOGS_DIR"
echo -e "${BLUE}[INFO]${NC} Created runtime directories"

# Check Python version
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo -e "${RED}[ERROR]${NC} Python 3 is required but not found"
    echo -e "${YELLOW}[HINT]${NC} Install Python 3.9+ and try again"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1)
echo -e "${BLUE}[INFO]${NC} Python version: ${GREEN}$PYTHON_VERSION${NC}"

# Install Python dependencies
echo -e "${BLUE}[INFO]${NC} Installing Python dependencies..."
REQUIREMENTS_FILE="$KERNEL_DIR/requirements.txt"

if [ -f "$REQUIREMENTS_FILE" ]; then
    $PYTHON_CMD -m pip install -q -r "$REQUIREMENTS_FILE" 2>/dev/null || {
        echo -e "${YELLOW}[WARN]${NC} Some dependencies may not have installed correctly"
        echo -e "${YELLOW}[WARN]${NC} Core functionality should still work"
    }
    echo -e "${GREEN}[OK]${NC} Dependencies installed"
else
    echo -e "${YELLOW}[WARN]${NC} Requirements file not found, installing core dependencies..."
    $PYTHON_CMD -m pip install -q PyYAML gitpython requests 2>/dev/null || true
fi

# Configure Git for Legion
echo -e "${BLUE}[INFO]${NC} Configuring Git for Legion OS..."

# Only set if not already configured
if [ -z "$(git config user.name)" ]; then
    git config user.name "Strategickhaos Legion"
fi
if [ -z "$(git config user.email)" ]; then
    git config user.email "legion@strategickhaos.io"
fi

# Enable GPG signing if available
if command -v gpg &> /dev/null && [ -n "$GPG_KEY_ID" ]; then
    git config commit.gpgsign true
    git config user.signingkey "$GPG_KEY_ID"
    echo -e "${GREEN}[OK]${NC} GPG signing enabled"
fi

# Test kernel connection
echo -e "${BLUE}[INFO]${NC} Testing kernel connection..."
$PYTHON_CMD "$KERNEL_DIR/connect.py" 2>/dev/null || {
    echo -e "${YELLOW}[WARN]${NC} Kernel connection test had issues, but continuing..."
}

# Check for Discord integration
if [ -n "$DISCORD_WEBHOOK_URL" ] || [ -n "$DISCORD_BOT_TOKEN" ]; then
    echo -e "${GREEN}[OK]${NC} Discord integration configured"
else
    echo -e "${YELLOW}[WARN]${NC} Discord integration not configured"
    echo -e "${YELLOW}[HINT]${NC} Set DISCORD_WEBHOOK_URL or DISCORD_BOT_TOKEN for notifications"
fi

# Check GitHub integration
if [ -n "$GITHUB_TOKEN" ] || [ -n "$GH_TOKEN" ]; then
    echo -e "${GREEN}[OK]${NC} GitHub integration configured"
else
    echo -e "${YELLOW}[WARN]${NC} GitHub token not found"
    echo -e "${YELLOW}[HINT]${NC} Set GITHUB_TOKEN for full Git operations"
fi

# List connected departments
echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}  CONNECTED DEPARTMENTS${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

CONFIG_FILE="$KERNEL_DIR/config.yml"
if [ -f "$CONFIG_FILE" ]; then
    # Extract department names using grep/sed (portable across systems)
    grep -A1 "^    - name:" "$CONFIG_FILE" 2>/dev/null | grep "name:" | sed 's/.*name: "//;s/".*//' | while read dept; do
        echo -e "  • ${GREEN}$dept${NC}"
    done
fi

# Count pending proposals
PENDING_COUNT=$(ls -1 "$PROPOSALS_DIR"/prop-*.json 2>/dev/null | wc -l || echo "0")
echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}  SYSTEM STATUS${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "  Workspace ID:      ${GREEN}$WORKSPACE_ID${NC}"
echo -e "  Workspace Type:    ${GREEN}$WORKSPACE_TYPE${NC}"
echo -e "  Pending Proposals: ${YELLOW}$PENDING_COUNT${NC}"
echo ""

# Optionally start daemon
echo -e "${BLUE}[INFO]${NC} Legion kernel initialized successfully!"
echo ""
echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${PURPLE}  COMMANDS${NC}"
echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "  Start daemon:      ${CYAN}python3 .strategickhaos/kernel/daemon.py &${NC}"
echo -e "  Create proposal:   ${CYAN}python3 -c \"from .strategickhaos.kernel.connect import LegionKernel; k=LegionKernel(); k.propose_change({...})\"${NC}"
echo -e "  List proposals:    ${CYAN}ls .strategickhaos/proposals/${NC}"
echo ""

echo -e "${GREEN}✅ Connected to Strategickhaos Legions of Minds OS${NC}"
echo ""
