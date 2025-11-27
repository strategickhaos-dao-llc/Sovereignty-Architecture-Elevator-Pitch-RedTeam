#!/bin/bash
# scripts/verify_blake3.sh
# Verify BLAKE3 hash of a file against an expected value
# Usage: ./scripts/verify_blake3.sh <file> <expected_hash>

set -e

SCRIPT_NAME="$(basename "$0")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

usage() {
    echo "Usage: $SCRIPT_NAME <file> <expected_hash>"
    echo ""
    echo "Arguments:"
    echo "  file           Path to the file to verify"
    echo "  expected_hash  Expected BLAKE3 hash (64 hex characters)"
    echo ""
    echo "Example:"
    echo "  $SCRIPT_NAME swarmgate_v1.0.tar.gz caa58d9faee9a10ce46d81d2f21e0da611ff962b8070e22b5d976cc816480698"
    exit 1
}

# Check arguments
if [ $# -ne 2 ]; then
    usage
fi

FILE="$1"
EXPECTED_HASH="$2"

# Validate expected hash format (64 hex characters)
if ! echo "$EXPECTED_HASH" | grep -qE '^[a-fA-F0-9]{64}$'; then
    echo -e "${RED}Error: Expected hash must be 64 hexadecimal characters${NC}"
    exit 1
fi

# Check if file exists
if [ ! -f "$FILE" ]; then
    echo -e "${RED}Error: File not found: $FILE${NC}"
    exit 1
fi

# Check for b3sum
if ! command -v b3sum &> /dev/null; then
    echo -e "${YELLOW}Warning: b3sum not found. Installing via cargo...${NC}"
    if command -v cargo &> /dev/null; then
        cargo install b3sum
    else
        echo -e "${RED}Error: Neither b3sum nor cargo found.${NC}"
        echo "Please install b3sum manually:"
        echo "  - Linux: cargo install b3sum"
        echo "  - macOS: brew install b3sum"
        echo "  - Windows: scoop install blake3"
        exit 1
    fi
fi

# Compute hash
echo -e "${YELLOW}Computing BLAKE3 hash of $FILE...${NC}"
ACTUAL_HASH=$(b3sum "$FILE" | cut -d' ' -f1)

echo "Expected: $EXPECTED_HASH"
echo "Actual:   $ACTUAL_HASH"

# Compare hashes (case-insensitive)
EXPECTED_LOWER=$(echo "$EXPECTED_HASH" | tr '[:upper:]' '[:lower:]')
ACTUAL_LOWER=$(echo "$ACTUAL_HASH" | tr '[:upper:]' '[:lower:]')

if [ "$EXPECTED_LOWER" = "$ACTUAL_LOWER" ]; then
    echo -e "${GREEN}✅ VERIFICATION PASSED: Hash matches expected value${NC}"
    exit 0
else
    echo -e "${RED}❌ VERIFICATION FAILED: Hash does not match${NC}"
    exit 1
fi
