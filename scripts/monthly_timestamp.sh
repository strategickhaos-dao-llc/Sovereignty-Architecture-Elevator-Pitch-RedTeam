#!/bin/bash
# monthly_timestamp.sh - Create monthly root hash timestamp for ledger entries
# Part of Appendix C: Legal Standards for AI Conversation Logs
# Usage: ./monthly_timestamp.sh [ledger_directory]

set -e

LEDGER_DIR="${1:-./ledger_entries}"
MONTH=$(date +%Y-%m)
ROOT_HASH_FILE="root_hash_${MONTH}.txt"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Creating monthly root hash timestamp for: ${MONTH}${NC}"

# Check if ledger directory exists
if [ ! -d "$LEDGER_DIR" ]; then
    echo -e "${RED}Error: Ledger directory not found: ${LEDGER_DIR}${NC}"
    echo "Usage: $0 [ledger_directory]"
    exit 1
fi

# Find all ledger entries for current month
ENTRIES=$(find "$LEDGER_DIR" -name "*${MONTH}*.yml" -o -name "*${MONTH}*.yaml" 2>/dev/null | sort)

if [ -z "$ENTRIES" ]; then
    echo -e "${YELLOW}No ledger entries found for ${MONTH}${NC}"
    exit 0
fi

ENTRY_COUNT=$(echo "$ENTRIES" | wc -l)
echo "Found $ENTRY_COUNT entries for $MONTH"

# Check if sha256sum is available
if ! command -v sha256sum &> /dev/null; then
    echo -e "${RED}Error: sha256sum not found${NC}"
    echo "Please install coreutils or use shasum -a 256 on macOS"
    exit 1
fi

# Calculate root hash (hash of all entry hashes concatenated)
if ! echo "$ENTRIES" | while read -r entry; do
    if [ -f "$entry" ]; then
        sha256sum "$entry" || { echo -e "${RED}Error hashing $entry${NC}"; exit 1; }
    fi
done | sha256sum | awk '{print $1}' > "$ROOT_HASH_FILE"; then
    echo -e "${RED}Error: Failed to calculate root hash${NC}"
    exit 1
fi

ROOT_HASH=$(cat "$ROOT_HASH_FILE")

# Add metadata
cat >> "$ROOT_HASH_FILE" << EOF

# Monthly Root Hash - $MONTH
# Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)
# Includes all ledger entries from: $MONTH
# Entry count: $ENTRY_COUNT
# Hash algorithm: SHA-256
# 
# Verification: Re-run this script to regenerate hash and compare
# Purpose: Cost-effective blockchain timestamping of entire month's entries
# 
# Entry files included:
EOF

echo "$ENTRIES" | while read -r entry; do
    echo "#   - $(basename "$entry")" >> "$ROOT_HASH_FILE"
done

echo -e "${GREEN}✓ Root hash calculated: ${ROOT_HASH}${NC}"
echo "  Saved to: $ROOT_HASH_FILE"
echo "  Entries: $ENTRY_COUNT"

# Sign the root hash
if command -v gpg &> /dev/null; then
    echo ""
    echo "Signing root hash..."
    if gpg --clearsign "$ROOT_HASH_FILE" 2>&1; then
        echo -e "${GREEN}✓ Root hash signed: ${ROOT_HASH_FILE}.asc${NC}"
    else
        echo -e "${YELLOW}Warning: GPG signing failed (signature not required but recommended)${NC}"
    fi
fi

# Timestamp with OpenTimestamps if available
if command -v ots &> /dev/null; then
    echo ""
    echo "Creating blockchain timestamp..."
    if [ -f "${ROOT_HASH_FILE}.asc" ]; then
        # Timestamp the signed version
        ots stamp "${ROOT_HASH_FILE}.asc"
        echo -e "${GREEN}✓ Timestamp created: ${ROOT_HASH_FILE}.asc.ots${NC}"
        echo ""
        echo "Wait ~1 hour for Bitcoin confirmation, then run:"
        echo "  ots upgrade ${ROOT_HASH_FILE}.asc.ots"
    else
        # Timestamp unsigned version
        ots stamp "$ROOT_HASH_FILE"
        echo -e "${GREEN}✓ Timestamp created: ${ROOT_HASH_FILE}.ots${NC}"
        echo ""
        echo "Wait ~1 hour for Bitcoin confirmation, then run:"
        echo "  ots upgrade ${ROOT_HASH_FILE}.ots"
    fi
else
    echo -e "${YELLOW}OpenTimestamps not installed. Skipping blockchain timestamp.${NC}"
    echo "Install with: pip3 install opentimestamps-client"
fi

# Commit to git if in repository
if git rev-parse --git-dir > /dev/null 2>&1; then
    echo ""
    echo "Committing to git repository..."
    git add "$ROOT_HASH_FILE"*
    if git commit -S -m "Monthly root hash timestamp: $MONTH" 2>&1; then
        echo -e "${GREEN}✓ Committed to git with signed commit${NC}"
    else
        echo -e "${YELLOW}Git commit not configured or failed${NC}"
    fi
fi

echo ""
echo -e "${GREEN}Monthly timestamp complete!${NC}"
echo ""
echo "Summary:"
echo "  Month: $MONTH"
echo "  Entries: $ENTRY_COUNT"
echo "  Root hash: $ROOT_HASH"
echo "  Hash file: $ROOT_HASH_FILE"
if [ -f "${ROOT_HASH_FILE}.asc" ]; then
    echo "  Signature: ${ROOT_HASH_FILE}.asc"
fi
if [ -f "${ROOT_HASH_FILE}.ots" ] || [ -f "${ROOT_HASH_FILE}.asc.ots" ]; then
    echo "  Timestamp: Created (upgrade in ~1 hour)"
fi
