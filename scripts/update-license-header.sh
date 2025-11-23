#!/bin/bash
# Update License Header Script
# For use with JetBrains File Watcher
# Updates copyright headers in source files

set -e

FILE_PATH="${1:-}"
CURRENT_YEAR=$(date +%Y)

# Configuration
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
LICENSE_FILE="$REPO_ROOT/LICENSE"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Validate input
if [[ -z "$FILE_PATH" ]]; then
    echo -e "${RED}❌ Error: No file path provided${NC}"
    echo "Usage: $0 <file_path>"
    exit 1
fi

if [[ ! -f "$FILE_PATH" ]]; then
    echo -e "${RED}❌ Error: File not found: $FILE_PATH${NC}"
    exit 1
fi

# Extract copyright info from LICENSE
if [[ -f "$LICENSE_FILE" ]]; then
    COPYRIGHT_LINE=$(grep -i "Copyright" "$LICENSE_FILE" | head -1)
    COPYRIGHT_OWNER=$(echo "$COPYRIGHT_LINE" | sed -E 's/.*Copyright \(c\) [0-9]+ //' | sed 's/^ *//;s/ *$//')
else
    echo -e "${YELLOW}⚠️  Warning: LICENSE file not found${NC}"
    COPYRIGHT_OWNER="Strategickhaos"
fi

# Determine file type and comment style
FILE_EXT="${FILE_PATH##*.}"
COMMENT_START=""
COMMENT_END=""
COMMENT_LINE=""

case "$FILE_EXT" in
    js|ts|java|c|cpp|h|hpp|cs|go|rs|kt)
        COMMENT_START="/*"
        COMMENT_END=" */"
        COMMENT_LINE=" *"
        ;;
    py|sh|bash|yml|yaml|rb)
        COMMENT_LINE="#"
        ;;
    html|xml)
        COMMENT_START="<!--"
        COMMENT_END="-->"
        COMMENT_LINE=""
        ;;
    *)
        # Unknown file type, skip
        exit 0
        ;;
esac

# Check if file already has copyright header
if grep -q "Copyright.*${CURRENT_YEAR}.*${COPYRIGHT_OWNER}" "$FILE_PATH"; then
    echo -e "${GREEN}✅ Copyright header is current: $(basename $FILE_PATH)${NC}"
    exit 0
fi

# Generate copyright header based on file type
generate_header() {
    if [[ -n "$COMMENT_START" ]]; then
        cat << EOF
$COMMENT_START
$COMMENT_LINE Copyright (c) $CURRENT_YEAR $COPYRIGHT_OWNER
$COMMENT_LINE
$COMMENT_LINE MIT License
$COMMENT_LINE See LICENSE file in the project root for full license text.
$COMMENT_END
EOF
    else
        cat << EOF
$COMMENT_LINE Copyright (c) $CURRENT_YEAR $COPYRIGHT_OWNER
$COMMENT_LINE
$COMMENT_LINE MIT License
$COMMENT_LINE See LICENSE file in the project root for full license text.
EOF
    fi
}

# Check if file has any copyright header (even outdated)
if grep -q "Copyright" "$FILE_PATH"; then
    echo -e "${BLUE}🔄 Updating existing copyright header in: $(basename $FILE_PATH)${NC}"
    
    # Create temporary file
    TEMP_FILE=$(mktemp)
    
    # Remove old copyright header and add new one
    if [[ -n "$COMMENT_START" ]]; then
        # For multi-line comment languages (remove old /* ... */ block)
        sed '/\/\*/,/\*\//d' "$FILE_PATH" > "$TEMP_FILE"
    else
        # For single-line comment languages (remove consecutive comment lines at top)
        sed '/^[#]/d' "$FILE_PATH" > "$TEMP_FILE"
    fi
    
    # Add new header
    {
        generate_header
        echo ""
        cat "$TEMP_FILE"
    } > "$FILE_PATH"
    
    rm "$TEMP_FILE"
    echo -e "${GREEN}✅ Updated copyright header${NC}"
else
    # No existing header, check if we should add one
    
    # Skip if file is very small (< 10 lines) or doesn't look like source code
    LINE_COUNT=$(wc -l < "$FILE_PATH")
    if [[ $LINE_COUNT -lt 10 ]]; then
        exit 0
    fi
    
    echo -e "${BLUE}➕ Adding copyright header to: $(basename $FILE_PATH)${NC}"
    
    # Create temporary file with header
    TEMP_FILE=$(mktemp)
    {
        generate_header
        echo ""
        cat "$FILE_PATH"
    } > "$TEMP_FILE"
    
    mv "$TEMP_FILE" "$FILE_PATH"
    echo -e "${GREEN}✅ Added copyright header${NC}"
fi

# Preserve file permissions
chmod +x "$0" 2>/dev/null || true

exit 0
