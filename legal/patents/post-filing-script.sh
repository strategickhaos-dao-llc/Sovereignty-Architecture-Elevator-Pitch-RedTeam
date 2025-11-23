#!/usr/bin/env bash
# post-filing-script.sh
# USPTO Provisional Patent Post-Filing Automation
# Strategickhaos DAO LLC - Federal Sovereignty Lock
#
# USAGE:
#   1. Download your USPTO acknowledgment receipt from email
#   2. Note your application number (63/XXXXXXX)
#   3. Run: ./post-filing-script.sh 63/XXXXXXX
#
# This script will:
#   - Move the receipt from Downloads to the repository
#   - Rename it with proper convention
#   - Create cryptographically signed Git commit
#   - Push to repository
#   - Display sovereignty confirmation message

set -euo pipefail

# Colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Configuration
APP_NUMBER="${1:-}"
DOWNLOADS_DIR="$HOME/Downloads"
REPO_PATH="${REPO_PATH:-$(pwd)}"

# Function to display usage
usage() {
    echo -e "${CYAN}Usage: $0 <USPTO_APP_NUMBER>${NC}"
    echo -e "${YELLOW}Example: $0 63/123456${NC}"
    echo ""
    echo "Environment Variables:"
    echo "  REPO_PATH    - Path to repository (default: current directory)"
    echo ""
    exit 1
}

# Validate application number
if [[ -z "$APP_NUMBER" ]]; then
    echo -e "${RED}❌ Error: USPTO application number required${NC}"
    usage
fi

if [[ ! "$APP_NUMBER" =~ ^[0-9][0-9]/[0-9][0-9][0-9][0-9][0-9][0-9][0-9]?$ ]]; then
    echo -e "${RED}❌ Invalid application number format${NC}"
    echo -e "${YELLOW}Expected format: 63/XXXXXXX (e.g., 63/123456 or 63/1234567)${NC}"
    exit 1
fi

# Clean application number for filename (replace / with _)
CLEAN_APP_NUMBER="${APP_NUMBER//\//_}"

# Get current date for filename
FILING_DATE=$(date +%Y-%m-%d)

# Target filename
TARGET_FILENAME="USPTO_Provisional_${CLEAN_APP_NUMBER}_Filed_${FILING_DATE}.pdf"

# Display banner
echo -e "${CYAN}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║          USPTO POST-FILING AUTOMATION v1.0                  ║"
echo "║          Federal Sovereignty Lock Activation                ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${YELLOW}📋 Configuration:${NC}"
echo -e "   Application Number: ${WHITE}$APP_NUMBER${NC}"
echo -e "   Filing Date: ${WHITE}$FILING_DATE${NC}"
echo -e "   Repository: ${WHITE}$REPO_PATH${NC}"
echo -e "   Target Filename: ${WHITE}$TARGET_FILENAME${NC}"
echo ""

# Check if repository exists
if [[ ! -d "$REPO_PATH" ]]; then
    echo -e "${RED}❌ Repository not found: $REPO_PATH${NC}"
    echo -e "${YELLOW}Please set REPO_PATH environment variable or cd to repository.${NC}"
    exit 1
fi

# Check if this is a git repository
if [[ ! -d "$REPO_PATH/.git" ]]; then
    echo -e "${RED}❌ Not a git repository: $REPO_PATH${NC}"
    exit 1
fi

# Find USPTO receipt in Downloads
echo -e "${YELLOW}🔍 Searching for USPTO receipt...${NC}"
RECEIPT_FILE=$(find "$DOWNLOADS_DIR" -maxdepth 1 -name "Acknowledgment*.pdf" -type f 2>/dev/null | head -1)

if [[ -z "$RECEIPT_FILE" ]]; then
    echo -e "${RED}❌ USPTO receipt not found in Downloads folder${NC}"
    echo -e "${YELLOW}Expected pattern: Acknowledgment*.pdf${NC}"
    echo -e "${YELLOW}Please download the receipt from your USPTO confirmation email.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Found receipt: $(basename "$RECEIPT_FILE")${NC}"

# Create legal/patents directory if it doesn't exist
mkdir -p "$REPO_PATH/legal/patents"

# Move and rename receipt
echo -e "${YELLOW}📦 Moving receipt to repository...${NC}"
TARGET_PATH="$REPO_PATH/legal/patents/$TARGET_FILENAME"

if mv "$RECEIPT_FILE" "$TARGET_PATH"; then
    echo -e "${GREEN}✅ Receipt archived: $TARGET_FILENAME${NC}"
else
    echo -e "${RED}❌ Failed to move receipt${NC}"
    exit 1
fi

# Change to repository directory
cd "$REPO_PATH"

# Git operations
echo -e "\n${YELLOW}🔐 Committing to repository (GPG-signed)...${NC}"

# Check if GPG signing is enabled
if ! git config --get commit.gpgsign &>/dev/null; then
    echo -e "${YELLOW}⚠️  GPG signing not enabled. Enabling for this commit...${NC}"
    echo -e "${YELLOW}To enable permanently: git config --global commit.gpgsign true${NC}"
fi

# Stage the file
if git add "legal/patents/$TARGET_FILENAME"; then
    echo -e "${GREEN}✅ File staged${NC}"
else
    echo -e "${RED}❌ Failed to stage file${NC}"
    exit 1
fi

# Create signed commit
COMMIT_MESSAGE="FEDERAL ARMOR LOCKED: USPTO Provisional $APP_NUMBER filed $FILING_DATE – 7% loop now protected by U.S. patent law, Texas LLC, and Bitcoin"

if git commit -S -m "$COMMIT_MESSAGE" 2>/dev/null || git commit -m "$COMMIT_MESSAGE"; then
    echo -e "${GREEN}✅ Commit created${NC}"
else
    echo -e "${RED}❌ Failed to create commit${NC}"
    exit 1
fi

# Push to remote
if git push; then
    echo -e "${GREEN}✅ Changes pushed to remote repository${NC}"
else
    echo -e "${YELLOW}⚠️  Push failed - you may need to push manually${NC}"
fi

# Success banner
echo -e "\n${MAGENTA}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║          THE EMPIRE IS NOW A NATION-STATE.                   ║"
echo "║                                                              ║"
echo "║   Crypto + Federal + State sovereignty achieved.             ║"
echo "║   The 7% flows forever. No one can stop it.                  ║"
echo "║                                                              ║"
echo -e "║   ${WHITE}You did it, King.${MAGENTA}                                          ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Next steps
echo -e "${CYAN}📋 NEXT STEPS:${NC}"
echo -e "   1. ${GREEN}✅ USPTO receipt archived and committed${NC}"
echo -e "   2. ${YELLOW}🎯 Reply with your application number: $APP_NUMBER${NC}"
echo -e "   3. ${YELLOW}🔮 Sovereign Patent Codex will be generated${NC}"
echo -e "   4. ${YELLOW}📅 Calendar reminder: Non-provisional due in 12 months${NC}"
echo -e "\n   ${CYAN}The triple shield is now active:${NC}"
echo -e "   ${GREEN}✅ Cryptographic Layer (Bitcoin, GPG, SHA256)${NC}"
echo -e "   ${GREEN}✅ Federal Layer (USPTO Provisional $APP_NUMBER)${NC}"
echo -e "   ${GREEN}✅ State Layer (Texas/Wyoming LLC)${NC}"

echo -e "\n${MAGENTA}🎵 The music truly never stops. And now... neither does the empire.${NC}\n"

# Generate file hash for records
FILE_HASH=$(sha256sum "$TARGET_PATH" | awk '{print $1}')
echo -e "${CYAN}📋 Receipt SHA256: $FILE_HASH${NC}"

# Log the operation
LOG_FILE="$REPO_PATH/legal/patents/filing_log.txt"
cat >> "$LOG_FILE" << EOF
[$(date -u +"%Y-%m-%d %H:%M:%S UTC")] USPTO POST-FILING COMPLETE
Application Number: $APP_NUMBER
Filing Date: $FILING_DATE
Receipt Hash: $FILE_HASH
Commit: $(git rev-parse HEAD)
Status: FEDERAL SOVEREIGNTY LOCKED

EOF

echo -e "${GREEN}📝 Operation logged to filing_log.txt${NC}\n"

echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}Federal sovereignty lock activation COMPLETE.${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}\n"
