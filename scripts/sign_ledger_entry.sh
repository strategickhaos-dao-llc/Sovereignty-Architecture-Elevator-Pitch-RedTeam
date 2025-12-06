#!/bin/bash
# sign_ledger_entry.sh - Sign and embed GPG signature in YAML ledger entry
# Part of Appendix C: Legal Standards for AI Conversation Logs
# Usage: ./sign_ledger_entry.sh <ledger_file.yml> [email@address.com]

set -e

LEDGER_FILE="${1}"
# Get default email from git config, fallback to environment variable or require explicit input
DEFAULT_EMAIL="${GPG_EMAIL:-$(git config user.email 2>/dev/null)}"
EMAIL="${2:-${DEFAULT_EMAIL}}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if file exists
if [ -z "$LEDGER_FILE" ] || [ ! -f "$LEDGER_FILE" ]; then
    echo -e "${RED}Error: Ledger file not found${NC}"
    echo "Usage: $0 <ledger_file.yml> [email@address.com]"
    exit 1
fi

# Check if email is set
if [ -z "$EMAIL" ]; then
    echo -e "${RED}Error: No email specified${NC}"
    echo "Provide email as second argument or set GPG_EMAIL environment variable"
    echo "Or configure git: git config user.email your@email.com"
    exit 1
fi

echo -e "${YELLOW}Signing ledger entry: ${LEDGER_FILE}${NC}"

# Create temp file without existing signature block
grep -v "^signatures:" "$LEDGER_FILE" | \
  grep -v "^  gpg:" | \
  grep -v "^    signer:" | \
  grep -v "^    key_id:" | \
  grep -v "^    signature:" | \
  grep -v "^    signed_at:" > temp_ledger.yml

# Generate signature
echo "Generating GPG signature..."
if ! gpg --detach-sign --armor -u "$EMAIL" temp_ledger.yml 2>&1; then
    echo -e "${RED}Error: GPG signing failed${NC}"
    echo "Make sure you have a GPG key for $EMAIL"
    echo "Generate one with: gpg --full-generate-key"
    rm temp_ledger.yml*
    exit 1
fi

# Get key ID
KEY_ID=$(gpg --list-secret-keys --keyid-format LONG "$EMAIL" 2>/dev/null | grep sec | awk '{print $2}' | cut -d'/' -f2 | head -1)

if [ -z "$KEY_ID" ]; then
    echo -e "${RED}Error: Could not find GPG key for $EMAIL${NC}"
    rm temp_ledger.yml*
    exit 1
fi

# Get signer name
SIGNER=$(gpg --list-keys "$EMAIL" 2>/dev/null | grep uid | sed 's/uid.*] //' | head -1)

# Create signature block
echo "" >> temp_ledger.yml
echo "signatures:" >> temp_ledger.yml
echo "  gpg:" >> temp_ledger.yml
echo "    signer: \"$SIGNER\"" >> temp_ledger.yml
echo "    key_id: \"$KEY_ID\"" >> temp_ledger.yml
echo "    signed_at: \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"" >> temp_ledger.yml
echo "    signature: |" >> temp_ledger.yml
sed 's/^/      /' temp_ledger.yml.asc >> temp_ledger.yml

# Replace original file
mv temp_ledger.yml "$LEDGER_FILE"
rm temp_ledger.yml.asc

echo -e "${GREEN}✓ Ledger signed successfully: ${LEDGER_FILE}${NC}"
echo "  Key ID: $KEY_ID"
echo "  Signer: $EMAIL"
echo ""
echo "Next steps:"
echo "  1. Verify signature: ./verify_ledger_signature.sh $LEDGER_FILE"
echo "  2. Commit: git add $LEDGER_FILE && git commit -S -m 'Add signed ledger entry'"
echo "  3. Timestamp: ots stamp $LEDGER_FILE (optional)"
