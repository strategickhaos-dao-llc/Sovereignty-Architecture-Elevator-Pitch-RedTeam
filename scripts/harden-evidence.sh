#!/bin/bash
#
# harden-evidence.sh
# One-click script to harden legal evidence with cryptographic proofs
#
# This script:
# 1. Generates SHA-256 checksums for all legal/governance documents
# 2. Signs checksums with GPG
# 3. Creates OpenTimestamps blockchain anchors
# 4. Creates and pushes GPG-signed git tag
#
# Usage: ./scripts/harden-evidence.sh
#

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
EVIDENCE_DIR="${REPO_ROOT}/evidence"
LEGAL_DIR="${REPO_ROOT}/legal"
GOVERNANCE_DIR="${REPO_ROOT}/governance"
TAG_NAME="v$(date +%Y%m%d)-7percent-lock"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}7% CHARITABLE ROYALTY - EVIDENCE HARDENING${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo -e "${YELLOW}Checking prerequisites...${NC}"

if ! command_exists sha256sum; then
    echo -e "${RED}ERROR: sha256sum not found${NC}"
    exit 1
fi

if ! command_exists gpg; then
    echo -e "${RED}ERROR: gpg not found. Install GnuPG.${NC}"
    exit 1
fi

if ! command_exists git; then
    echo -e "${RED}ERROR: git not found${NC}"
    exit 1
fi

# Check for OpenTimestamps (optional)
HAS_OTS=false
if command_exists ots; then
    HAS_OTS=true
    echo -e "${GREEN}✓ OpenTimestamps client found${NC}"
else
    echo -e "${YELLOW}⚠ OpenTimestamps not found (optional). Install with: pip install opentimestamps-client${NC}"
fi

# Check GPG key configuration
if ! git config user.signingkey >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠ No GPG signing key configured for git${NC}"
    echo -e "${YELLOW}  Configure with: git config user.signingkey <your-key-id>${NC}"
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""

# Step 1: Generate SHA-256 checksums
echo -e "${YELLOW}Step 1: Generating SHA-256 checksums...${NC}"
cd "${REPO_ROOT}"

# Find all relevant files
FILES_TO_HASH=(
    "legal/2025-11-23_Board_Resolution_7Percent_Lock.md"
    "legal/2025-11-23_Board_Resolution_7Percent_Lock.pdf"
    "legal/Charitable_Royalty_Assignment_Agreement_DAO_to_501c3.md"
    "legal/Charitable_Royalty_Assignment_Agreement_DAO_to_501c3.pdf"
    "legal/IP_Assignment_Creator_to_DAO.md"
    "legal/IP_Assignment_Creator_to_DAO.pdf"
    "legal/Charity_Acknowledgment_Letter.md"
    "legal/Charity_Acknowledgment_Letter.pdf"
    "governance/royalty-lock.yaml"
    "governance/agents/enforce_7percent.py"
)

# Create checksums file
CHECKSUM_FILE="${EVIDENCE_DIR}/sha256sums.txt"
echo "# SHA-256 Checksums for Legal and Governance Documents" > "${CHECKSUM_FILE}"
echo "# Generated: $(date -u +"%Y-%m-%d %H:%M:%S UTC")" >> "${CHECKSUM_FILE}"
echo "# Repository: $(git config --get remote.origin.url)" >> "${CHECKSUM_FILE}"
echo "# Commit: $(git rev-parse HEAD)" >> "${CHECKSUM_FILE}"
echo "" >> "${CHECKSUM_FILE}"

for file in "${FILES_TO_HASH[@]}"; do
    if [ -f "${file}" ]; then
        sha256sum "${file}" >> "${CHECKSUM_FILE}"
        echo -e "${GREEN}  ✓ ${file}${NC}"
    else
        echo -e "${YELLOW}  ⚠ ${file} not found (skipped)${NC}"
    fi
done

echo -e "${GREEN}✓ Checksums generated: ${CHECKSUM_FILE}${NC}"
echo ""

# Step 2: Sign checksums with GPG
echo -e "${YELLOW}Step 2: Signing checksums with GPG...${NC}"

if gpg --clearsign --output "${CHECKSUM_FILE}.asc" "${CHECKSUM_FILE}"; then
    echo -e "${GREEN}✓ GPG signature created: ${CHECKSUM_FILE}.asc${NC}"
    
    # Verify the signature
    if gpg --verify "${CHECKSUM_FILE}.asc"; then
        echo -e "${GREEN}✓ GPG signature verified${NC}"
    else
        echo -e "${RED}✗ GPG signature verification failed${NC}"
        exit 1
    fi
else
    echo -e "${RED}✗ GPG signing failed${NC}"
    echo -e "${YELLOW}  Make sure you have a GPG key configured${NC}"
    exit 1
fi

echo ""

# Step 3: Create OpenTimestamps proofs
if [ "$HAS_OTS" = true ]; then
    echo -e "${YELLOW}Step 3: Creating OpenTimestamps proofs...${NC}"
    
    for file in "${FILES_TO_HASH[@]}"; do
        if [ -f "${file}" ]; then
            ots stamp "${file}" 2>/dev/null || true
            if [ -f "${file}.ots" ]; then
                # Move .ots file to evidence directory
                mv "${file}.ots" "${EVIDENCE_DIR}/opentimestamps/$(basename ${file}).ots"
                echo -e "${GREEN}  ✓ Timestamped: ${file}${NC}"
            fi
        fi
    done
    
    # Timestamp the checksum file too
    ots stamp "${CHECKSUM_FILE}" 2>/dev/null || true
    if [ -f "${CHECKSUM_FILE}.ots" ]; then
        mv "${CHECKSUM_FILE}.ots" "${EVIDENCE_DIR}/opentimestamps/"
        echo -e "${GREEN}  ✓ Timestamped: checksums${NC}"
    fi
    
    echo -e "${GREEN}✓ OpenTimestamps proofs created${NC}"
    echo -e "${YELLOW}  Note: Timestamps may take 1-24 hours to confirm on Bitcoin blockchain${NC}"
else
    echo -e "${YELLOW}Step 3: Skipped (OpenTimestamps not installed)${NC}"
fi

echo ""

# Step 4: Create signed git tag
echo -e "${YELLOW}Step 4: Creating GPG-signed git tag...${NC}"

# Check if there are uncommitted changes
if ! git diff-index --quiet HEAD --; then
    echo -e "${YELLOW}⚠ You have uncommitted changes. Commit them first.${NC}"
    git status --short
    read -p "Commit changes now? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git add evidence/ legal/ governance/
        git commit -S -m "Add cryptographic evidence for 7% charitable royalty lock"
        echo -e "${GREEN}✓ Changes committed${NC}"
    else
        echo -e "${RED}✗ Aborted. Commit changes manually and re-run this script.${NC}"
        exit 1
    fi
fi

# Create the signed tag
TAG_MESSAGE="7% Charitable Royalty Lock - Evidence Anchored

This tag marks the establishment of the irrevocable 7% charitable royalty commitment.

Included in this release:
- Board Resolution establishing 7% lock
- Charitable Royalty Assignment Agreement
- IP Assignment Agreement
- Charity Acknowledgment Letter template
- Machine-readable governance configuration
- Automated enforcement agent
- Cryptographic evidence (SHA-256, GPG, OpenTimestamps)

All documents are GPG-signed and blockchain-anchored for legal defensibility.

Date: $(date -u +"%Y-%m-%d")
Commit: $(git rev-parse HEAD)
"

if git tag -s "${TAG_NAME}" -m "${TAG_MESSAGE}"; then
    echo -e "${GREEN}✓ Signed tag created: ${TAG_NAME}${NC}"
    
    # Export tag to evidence directory
    git cat-file tag "${TAG_NAME}" > "${EVIDENCE_DIR}/signed-tags/${TAG_NAME}.asc"
    echo -e "${GREEN}✓ Tag exported to: ${EVIDENCE_DIR}/signed-tags/${TAG_NAME}.asc${NC}"
    
    # Verify the tag
    if git verify-tag "${TAG_NAME}"; then
        echo -e "${GREEN}✓ Tag signature verified${NC}"
    else
        echo -e "${RED}✗ Tag signature verification failed${NC}"
        exit 1
    fi
else
    echo -e "${RED}✗ Failed to create signed tag${NC}"
    exit 1
fi

echo ""

# Step 5: Push to remote
echo -e "${YELLOW}Step 5: Pushing to remote repository...${NC}"
read -p "Push commits and tags to origin? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    git push origin HEAD
    git push origin "${TAG_NAME}"
    echo -e "${GREEN}✓ Pushed to remote${NC}"
else
    echo -e "${YELLOW}⚠ Skipped push. Push manually with:${NC}"
    echo -e "${YELLOW}  git push origin HEAD${NC}"
    echo -e "${YELLOW}  git push origin ${TAG_NAME}${NC}"
fi

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}✓ EVIDENCE HARDENING COMPLETE${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${BLUE}Summary:${NC}"
echo -e "  • SHA-256 checksums: ${CHECKSUM_FILE}"
echo -e "  • GPG signature: ${CHECKSUM_FILE}.asc"
if [ "$HAS_OTS" = true ]; then
    echo -e "  • OpenTimestamps: ${EVIDENCE_DIR}/opentimestamps/*.ots"
fi
echo -e "  • Signed git tag: ${TAG_NAME}"
echo ""
echo -e "${BLUE}Verification:${NC}"
echo -e "  • Verify checksums: sha256sum -c ${CHECKSUM_FILE}"
echo -e "  • Verify GPG: gpg --verify ${CHECKSUM_FILE}.asc"
if [ "$HAS_OTS" = true ]; then
    echo -e "  • Verify timestamps: ots verify <file> -f <file>.ots"
fi
echo -e "  • Verify tag: git verify-tag ${TAG_NAME}"
echo ""
echo -e "${GREEN}The 7% charitable royalty lock is now cryptographically hardened! ⚔️🖤${NC}"
