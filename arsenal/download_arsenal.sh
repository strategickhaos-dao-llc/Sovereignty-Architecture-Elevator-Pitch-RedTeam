#!/bin/bash
# Arsenal Bibliography Bulk Download Script
# Downloads all 100 papers to the papers/ directory

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PAPERS_DIR="$SCRIPT_DIR/papers"
ARSENAL_FILE="$SCRIPT_DIR/arsenal.txt"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}   Arsenal Bibliography - Bulk Download Script${NC}"
echo -e "${BLUE}   100 Openly Accessible Research Papers${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""

# Create papers directory if it doesn't exist
if [ ! -d "$PAPERS_DIR" ]; then
    echo -e "${GREEN}Creating papers directory...${NC}"
    mkdir -p "$PAPERS_DIR"
fi

# Check if arsenal.txt exists
if [ ! -f "$ARSENAL_FILE" ]; then
    echo -e "${RED}Error: arsenal.txt not found at $ARSENAL_FILE${NC}"
    exit 1
fi

# Count total URLs (excluding comments and empty lines)
TOTAL_URLS=$(grep -v "^#" "$ARSENAL_FILE" | grep -v "^$" | wc -l)
echo -e "${GREEN}Found $TOTAL_URLS URLs to download${NC}"
echo ""

# Change to papers directory
cd "$PAPERS_DIR"

# Counter for progress
CURRENT=0
SUCCESSFUL=0
FAILED=0

# Read URLs from arsenal.txt and download
while IFS= read -r line; do
    # Skip comments and empty lines
    if [[ "$line" =~ ^#.*$ ]] || [[ -z "$line" ]]; then
        continue
    fi
    
    CURRENT=$((CURRENT + 1))
    
    # Extract filename from URL
    FILENAME=$(basename "$line")
    
    # If URL doesn't end with a file extension, generate a filename
    if [[ ! "$FILENAME" =~ \.[a-zA-Z0-9]+$ ]]; then
        # Use the last part of the path or a hash of the URL
        FILENAME="paper_${CURRENT}.pdf"
    fi
    
    echo -e "${BLUE}[$CURRENT/$TOTAL_URLS]${NC} Downloading: $FILENAME"
    echo -e "           From: $line"
    
    # Download with curl, following redirects, with timeout
    if curl -L -s -f -m 120 -o "$FILENAME" "$line" 2>/dev/null; then
        # Check if file was actually downloaded and has content
        if [ -s "$FILENAME" ]; then
            FILE_SIZE=$(du -h "$FILENAME" | cut -f1)
            echo -e "           ${GREEN}✓ Success${NC} (Size: $FILE_SIZE)"
            SUCCESSFUL=$((SUCCESSFUL + 1))
        else
            echo -e "           ${RED}✗ Failed${NC} (Empty file)"
            rm -f "$FILENAME"
            FAILED=$((FAILED + 1))
        fi
    else
        echo -e "           ${RED}✗ Failed${NC} (Download error)"
        FAILED=$((FAILED + 1))
    fi
    
    echo ""
    
    # Small delay to be respectful to servers
    sleep 0.5
done < "$ARSENAL_FILE"

# Summary
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}Download Complete!${NC}"
echo ""
echo -e "  Total URLs:       ${TOTAL_URLS}"
echo -e "  ${GREEN}Successful:       ${SUCCESSFUL}${NC}"
echo -e "  ${RED}Failed:           ${FAILED}${NC}"
echo ""
echo -e "Papers saved to: ${BLUE}$PAPERS_DIR${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"

# Exit with error if any downloads failed
if [ $FAILED -gt 0 ]; then
    exit 1
fi

exit 0
