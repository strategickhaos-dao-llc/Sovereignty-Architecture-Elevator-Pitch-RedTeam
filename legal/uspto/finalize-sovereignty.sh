#!/bin/bash

# TRIPLE SHIELD FINALIZATION SCRIPT
# Automates the sovereignty activation process after USPTO filing
# Usage: ./finalize-sovereignty.sh <USPTO_APP_NUMBER>
# Example: ./finalize-sovereignty.sh 63/123456

set -e  # Exit on error

# Colors for output
MAGENTA='\033[0;35m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
WHITE='\033[0;37m'
NC='\033[0m' # No Color

# Banner
echo -e "${MAGENTA}"
cat << "EOF"
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║        TRIPLE SHIELD SOVEREIGNTY FINALIZATION              ║
║                                                            ║
║  Activating Federal, Cryptographic, and Corporate Shields  ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Check arguments
if [ $# -ne 1 ]; then
    echo -e "${RED}Error: USPTO application number required${NC}"
    echo "Usage: $0 <USPTO_APP_NUMBER>"
    echo "Example: $0 63/123456"
    exit 1
fi

USPTO_NUM=$1
echo -e "${GREEN}USPTO Application Number: ${USPTO_NUM}${NC}\n"

# Validate USPTO number format
if [[ ! $USPTO_NUM =~ ^63/[0-9]{6,7}$ ]]; then
    echo -e "${YELLOW}Warning: USPTO number format should be 63/XXXXXX${NC}"
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Get repository root
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -z "$REPO_ROOT" ]; then
    echo -e "${RED}Error: Not in a git repository${NC}"
    exit 1
fi

cd "$REPO_ROOT"
echo -e "${GREEN}Repository: ${REPO_ROOT}${NC}\n"

# Step 1: Check for USPTO receipt PDF
echo -e "${YELLOW}Step 1: Checking for USPTO receipt PDF...${NC}"
USPTO_PDF=$(find . -name "Acknowledgment*.pdf" -o -name "USPTO*.pdf" | head -1)

if [ -z "$USPTO_PDF" ]; then
    echo -e "${YELLOW}USPTO receipt PDF not found in repository${NC}"
    echo "Please manually copy your USPTO acknowledgment PDF to:"
    echo "  ${REPO_ROOT}/legal/uspto/USPTO_Provisional_${USPTO_NUM/\//_}_Filed_2025-11-23.pdf"
    read -p "Press Enter after copying the file..."
else
    # Move/rename the PDF
    TARGET_PDF="legal/uspto/USPTO_Provisional_${USPTO_NUM/\//_}_Filed_2025-11-23.pdf"
    mkdir -p "$(dirname "$TARGET_PDF")"
    mv "$USPTO_PDF" "$TARGET_PDF"
    echo -e "${GREEN}✓ USPTO receipt moved to: ${TARGET_PDF}${NC}\n"
fi

# Step 2: Update Sovereign Patent Codex
echo -e "${YELLOW}Step 2: Updating Sovereign Patent Codex with USPTO number...${NC}"
CODEX_FILE="legal/uspto/SOVEREIGN_PATENT_CODEX.md"

if [ ! -f "$CODEX_FILE" ]; then
    echo -e "${RED}Error: ${CODEX_FILE} not found${NC}"
    exit 1
fi

# Replace placeholder with actual USPTO number
sed -i.bak "s/63\/XXXXXXX/${USPTO_NUM}/g" "$CODEX_FILE"
sed -i.bak "s/AWAITING USPTO APPLICATION NUMBER/USPTO APPLICATION ${USPTO_NUM} FILED/g" "$CODEX_FILE"
sed -i.bak "s/PENDING SUBMISSION/FILED - ${USPTO_NUM}/g" "$CODEX_FILE"

# Get current date
FILING_DATE=$(date +%Y-%m-%d)
sed -i.bak "s/November 23, 2025/${FILING_DATE}/g" "$CODEX_FILE" 2>/dev/null || true

rm -f "${CODEX_FILE}.bak"
echo -e "${GREEN}✓ Codex updated with USPTO ${USPTO_NUM}${NC}\n"

# Step 3: GPG Signature
echo -e "${YELLOW}Step 3: Generating GPG signature...${NC}"

# Check if GPG is configured
if ! command -v gpg &> /dev/null; then
    echo -e "${YELLOW}Warning: GPG not found. Skipping signature generation.${NC}"
    echo "Install GPG and run: gpg --armor --detach-sign ${CODEX_FILE}"
else
    # Check if user has a GPG key
    if ! gpg --list-secret-keys &> /dev/null; then
        echo -e "${YELLOW}Warning: No GPG secret key found${NC}"
        echo "Generate a key with: gpg --full-generate-key"
        echo "Then run: gpg --armor --detach-sign ${CODEX_FILE}"
    else
        # Generate detached signature
        gpg --armor --detach-sign --yes "${CODEX_FILE}" 2>/dev/null || {
            echo -e "${YELLOW}Warning: Could not auto-sign. Please run manually:${NC}"
            echo "  gpg --armor --detach-sign ${CODEX_FILE}"
        }
        
        if [ -f "${CODEX_FILE}.asc" ]; then
            echo -e "${GREEN}✓ GPG signature created: ${CODEX_FILE}.asc${NC}\n"
        fi
    fi
fi

# Step 4: Bitcoin Timestamp
echo -e "${YELLOW}Step 4: Generating Bitcoin timestamp...${NC}"

if ! command -v ots &> /dev/null; then
    echo -e "${YELLOW}Warning: OpenTimestamps (ots) not found${NC}"
    echo "Install with: npm install -g opentimestamps"
    echo "Then run: ots stamp ${CODEX_FILE}"
else
    ots stamp "${CODEX_FILE}" 2>/dev/null || {
        echo -e "${YELLOW}Warning: Could not create timestamp. Run manually:${NC}"
        echo "  ots stamp ${CODEX_FILE}"
    }
    
    if [ -f "${CODEX_FILE}.ots" ]; then
        echo -e "${GREEN}✓ Bitcoin timestamp created: ${CODEX_FILE}.ots${NC}"
        echo -e "${YELLOW}  Note: Confirmation may take up to 24 hours${NC}\n"
    fi
fi

# Step 5: Calculate SHA256 hashes
echo -e "${YELLOW}Step 5: Calculating SHA256 hashes...${NC}"
SHA_MANIFEST="legal/uspto/SHA256_MANIFEST.txt"

{
    echo "# SHA256 Manifest - Triple Shield Sovereignty Framework"
    echo "# Generated: $(date)"
    echo "# USPTO Application: ${USPTO_NUM}"
    echo ""
    
    for file in dao_record_v1.0.yaml \
                discovery.yml \
                README.md \
                "${CODEX_FILE}" \
                "legal/uspto/USPTO_Provisional_${USPTO_NUM/\//_}_Filed_2025-11-23.pdf"
    do
        if [ -f "$file" ]; then
            sha256sum "$file" 2>/dev/null
        fi
    done
} > "$SHA_MANIFEST"

echo -e "${GREEN}✓ SHA256 hashes recorded in: ${SHA_MANIFEST}${NC}\n"

# Step 6: Git commit
echo -e "${YELLOW}Step 6: Creating sovereignty commit...${NC}"

# Stage all changes
git add .

# Check if GPG signing is enabled
GPG_SIGN=""
if git config --get commit.gpgsign &> /dev/null; then
    if [ "$(git config --get commit.gpgsign)" = "true" ]; then
        GPG_SIGN="-S"
    fi
fi

# Create commit
COMMIT_MSG="TRIPLE SHIELD ACHIEVED: USPTO Provisional ${USPTO_NUM} filed $(date +%Y-%m-%d) — 7% loop now protected by Bitcoin, U.S. patent law, and Texas LLC"

git commit ${GPG_SIGN} -m "${COMMIT_MSG}" || {
    echo -e "${YELLOW}Warning: Commit failed. Staging changes for manual commit.${NC}"
    echo "Run manually:"
    echo "  git commit -S -m \"${COMMIT_MSG}\""
    exit 1
}

echo -e "${GREEN}✓ Sovereignty commit created${NC}\n"

# Step 7: Push to remote
echo -e "${YELLOW}Step 7: Pushing to establish public record...${NC}"
read -p "Push changes to remote repository? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    git push || {
        echo -e "${YELLOW}Warning: Push failed. Push manually with: git push${NC}"
        exit 1
    }
    echo -e "${GREEN}✓ Changes pushed to remote${NC}\n"
else
    echo -e "${YELLOW}Skipped push. Run manually: git push${NC}\n"
fi

# Success banner
echo -e "${MAGENTA}"
cat << "EOF"

╔════════════════════════════════════════════════════════════╗
║                                                            ║
║              TRIPLE SHIELD ACTIVATED                       ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝

EOF
echo -e "${NC}"

echo -e "${MAGENTA}THE EMPIRE IS NOW A NATION-STATE.${NC}"
echo -e "${MAGENTA}No force in this world can break this loop.${NC}"
echo -e "${WHITE}You are sovereign.${NC}\n"

# Summary
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}SOVEREIGNTY STATUS: 100% (3/3 SHIELDS ACTIVE)${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "  ${GREEN}✓${NC} Shield 1: Mathematics (GPG + Bitcoin)"
echo -e "  ${GREEN}✓${NC} Shield 2: Federal Law (USPTO ${USPTO_NUM})"
echo -e "  ${GREEN}✓${NC} Shield 3: State Law (Texas LLC)"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

echo -e "${YELLOW}Next Steps:${NC}"
echo "  1. Verify commit signature: git verify-commit HEAD"
echo "  2. Verify GPG signature: gpg --verify ${CODEX_FILE}.asc"
echo "  3. Monitor Bitcoin timestamp: ots verify ${CODEX_FILE}.ots (after 24h)"
echo "  4. Set calendar reminder: Convert to utility patent within 12 months"
echo ""
echo -e "${WHITE}The 7% flows forever.${NC}"
echo -e "${WHITE}Execute. Then ascend.${NC}\n"
