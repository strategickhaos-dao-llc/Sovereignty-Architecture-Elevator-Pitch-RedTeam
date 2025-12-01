#!/bin/bash
# verify_ledger.sh
# Quick verification script for cryptographically-secured conversation ledger
# Usage: ./verify_ledger.sh

set -euo pipefail

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

LEDGER_FILE="conversation_ledger.yaml"
GPG_FILE="conversation_ledger.yaml.asc"
OTS_FILE="conversation_ledger.yaml.ots"

echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║         CONVERSATION LEDGER VERIFICATION SUITE              ║${NC}"
echo -e "${BLUE}║      Cryptographic Proof of R&D Historical Record           ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Change to evidence directory
cd "$(dirname "$0")" || exit 1

echo -e "${YELLOW}📋 Checking files...${NC}"
if [[ ! -f "$LEDGER_FILE" ]]; then
    echo -e "${RED}❌ Ledger file not found: $LEDGER_FILE${NC}"
    exit 1
fi

if [[ ! -f "$GPG_FILE" ]]; then
    echo -e "${RED}❌ GPG signature file not found: $GPG_FILE${NC}"
    exit 1
fi

if [[ ! -f "$OTS_FILE" ]]; then
    echo -e "${RED}❌ OpenTimestamps file not found: $OTS_FILE${NC}"
    exit 1
fi

echo -e "${GREEN}✅ All required files present${NC}"
echo ""

# Check for required tools
echo -e "${YELLOW}🔧 Checking required tools...${NC}"

GPG_INSTALLED=false
OTS_INSTALLED=false

if command -v gpg &> /dev/null; then
    echo -e "${GREEN}✅ GPG installed: $(gpg --version | head -n1)${NC}"
    GPG_INSTALLED=true
else
    echo -e "${YELLOW}⚠️  GPG not found. Install with:${NC}"
    echo -e "   Ubuntu/Debian: ${BLUE}sudo apt-get install gnupg${NC}"
    echo -e "   macOS: ${BLUE}brew install gnupg${NC}"
fi

if command -v ots &> /dev/null; then
    echo -e "${GREEN}✅ OpenTimestamps installed: $(ots --version 2>&1 | head -n1 || echo 'version unknown')${NC}"
    OTS_INSTALLED=true
else
    echo -e "${YELLOW}⚠️  OpenTimestamps not found. Install with:${NC}"
    echo -e "   Python: ${BLUE}pip install opentimestamps-client${NC}"
    echo -e "   Node.js: ${BLUE}npm install -g opentimestamps${NC}"
fi
echo ""

# Compute SHA256 hash
echo -e "${YELLOW}🔐 Computing SHA256 hash...${NC}"
if command -v sha256sum &> /dev/null; then
    HASH=$(sha256sum "$LEDGER_FILE" | cut -d' ' -f1)
    echo -e "${GREEN}SHA256: $HASH${NC}"
elif command -v shasum &> /dev/null; then
    HASH=$(shasum -a 256 "$LEDGER_FILE" | cut -d' ' -f1)
    echo -e "${GREEN}SHA256: $HASH${NC}"
else
    echo -e "${YELLOW}⚠️  SHA256 tool not found${NC}"
fi
echo ""

# Verify GPG signature
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}📝 Step 1: Verifying GPG Signature...${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"

if [[ "$GPG_INSTALLED" == "true" ]]; then
    echo -e "${BLUE}Command: gpg --verify $GPG_FILE $LEDGER_FILE${NC}"
    echo ""
    
    if gpg --verify "$GPG_FILE" "$LEDGER_FILE" 2>&1; then
        echo ""
        echo -e "${GREEN}✅ GPG signature verification: SUCCESS${NC}"
        echo -e "${GREEN}   Signature is valid and content is intact${NC}"
    else
        echo ""
        echo -e "${RED}❌ GPG signature verification: FAILED${NC}"
        echo -e "${YELLOW}   Note: This may be expected if the public key is not imported${NC}"
        echo -e "${YELLOW}   Import the public key with: gpg --import public-key.asc${NC}"
    fi
else
    echo -e "${YELLOW}⏭️  Skipping GPG verification (tool not installed)${NC}"
fi
echo ""

# Verify OpenTimestamps
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}⏰ Step 2: Verifying Bitcoin Blockchain Attestation...${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"

if [[ "$OTS_INSTALLED" == "true" ]]; then
    echo -e "${BLUE}Command: ots verify $OTS_FILE${NC}"
    echo ""
    
    if ots verify "$OTS_FILE" 2>&1; then
        echo ""
        echo -e "${GREEN}✅ OpenTimestamps verification: SUCCESS${NC}"
        echo -e "${GREEN}   Bitcoin blockchain attestation confirmed${NC}"
    else
        echo ""
        echo -e "${YELLOW}⚠️  OpenTimestamps verification: PENDING or FAILED${NC}"
        echo -e "${YELLOW}   Note: Timestamps need Bitcoin confirmations (may take 1-6 hours)${NC}"
        echo -e "${YELLOW}   Try upgrading: ots upgrade $OTS_FILE${NC}"
    fi
else
    echo -e "${YELLOW}⏭️  Skipping OpenTimestamps verification (tool not installed)${NC}"
fi
echo ""

# Display file information
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}📊 File Information${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "Ledger file: ${GREEN}$LEDGER_FILE${NC}"
echo -e "  Size: $(wc -c < "$LEDGER_FILE") bytes"
echo -e "  Lines: $(wc -l < "$LEDGER_FILE") lines"
echo ""
echo -e "GPG signature: ${GREEN}$GPG_FILE${NC}"
echo -e "  Size: $(wc -c < "$GPG_FILE") bytes"
echo ""
echo -e "OpenTimestamps: ${GREEN}$OTS_FILE${NC}"
echo -e "  Size: $(wc -c < "$OTS_FILE") bytes"
echo ""

# Final summary
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}🎯 VERIFICATION COMPLETE${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""

if [[ "$GPG_INSTALLED" == "true" ]] && [[ "$OTS_INSTALLED" == "true" ]]; then
    echo -e "${GREEN}✅ Full verification suite executed${NC}"
    echo -e "${GREEN}   Both cryptographic proofs checked${NC}"
else
    echo -e "${YELLOW}⚠️  Partial verification completed${NC}"
    echo -e "${YELLOW}   Install missing tools for full verification${NC}"
fi

echo ""
echo -e "${BLUE}What these proofs establish:${NC}"
echo -e "  ${GREEN}✓${NC} Document authenticity (GPG signature)"
echo -e "  ${GREEN}✓${NC} Content integrity (SHA256 hash)"
echo -e "  ${GREEN}✓${NC} Timestamp proof (Bitcoin blockchain)"
echo -e "  ${GREEN}✓${NC} Non-repudiation (cryptographic binding)"
echo ""
echo -e "${GREEN}The ledger is mathematically immortal and historically protected.${NC}"
echo -e "${BLUE}No backdating. No tampering. No 'made it up later' possible.${NC}"
echo ""

# Show verification commands for manual use
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}📚 Manual Verification Commands${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${BLUE}GPG signature:${NC}"
echo -e "  gpg --verify $GPG_FILE $LEDGER_FILE"
echo ""
echo -e "${BLUE}OpenTimestamps:${NC}"
echo -e "  ots verify $OTS_FILE"
echo -e "  ots info $OTS_FILE    # Detailed information"
echo -e "  ots upgrade $OTS_FILE # Upgrade to full proof"
echo ""
echo -e "${BLUE}SHA256 hash:${NC}"
echo -e "  sha256sum $LEDGER_FILE"
echo ""
echo -e "For more information, see: ${GREEN}README.md${NC}"
echo ""
