#!/bin/bash
# vim-paths.sh - Quick reference for Vim absolute paths in Sovereignty Architecture
# Usage: source vim-paths.sh or ./vim-paths.sh

# Get the absolute path of the project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Color output
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${CYAN}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║  Sovereignty Architecture - Vim Absolute Paths                ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}Project Root:${NC} $PROJECT_ROOT"
echo ""
echo -e "${YELLOW}Quick Vim Commands:${NC}"
echo ""
echo "# Navigate to project root:"
echo -e "${CYAN}:e $PROJECT_ROOT${NC}"
echo ""
echo "# Open key files:"
echo -e "${CYAN}:e $PROJECT_ROOT/README.md${NC}"
echo -e "${CYAN}:e $PROJECT_ROOT/discovery.yml${NC}"
echo -e "${CYAN}:e $PROJECT_ROOT/docker-compose.yml${NC}"
echo -e "${CYAN}:e $PROJECT_ROOT/ai_constitution.yaml${NC}"
echo ""
echo "# Open directories:"
echo -e "${CYAN}:e $PROJECT_ROOT/bootstrap/${NC}"
echo -e "${CYAN}:e $PROJECT_ROOT/src/${NC}"
echo -e "${CYAN}:e $PROJECT_ROOT/scripts/${NC}"
echo -e "${CYAN}:e $PROJECT_ROOT/governance/${NC}"
echo ""
echo -e "${YELLOW}Terminal Commands:${NC}"
echo ""
echo "# Change to project root:"
echo -e "${CYAN}cd $PROJECT_ROOT${NC}"
echo ""
echo "# Open vim in project root:"
echo -e "${CYAN}vim $PROJECT_ROOT${NC}"
echo ""
echo "# Open specific file:"
echo -e "${CYAN}vim $PROJECT_ROOT/README.md${NC}"
echo ""
echo -e "${YELLOW}Copy-Paste Ready:${NC}"
echo ""
echo "$PROJECT_ROOT"
echo ""
echo -e "${GREEN}💡 Tip:${NC} In VS Code, right-click any file → 'Copy Path' to get absolute path"
echo -e "${GREEN}💡 Tip:${NC} Use ${CYAN}:pwd${NC} in Vim to show current directory"
echo -e "${GREEN}💡 Tip:${NC} Use ${CYAN}:e %${NC} in Vim to reopen current file"
echo ""

# Export as environment variable for easy access
export SOVEREIGNTY_ROOT="$PROJECT_ROOT"
echo -e "${GREEN}Environment variable set:${NC} \$SOVEREIGNTY_ROOT"
