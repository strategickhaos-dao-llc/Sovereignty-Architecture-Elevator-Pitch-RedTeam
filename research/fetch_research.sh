#!/bin/bash
# Distributed Department Research Automation
# Fetches web pages silently for knowledge harvesting

set -e

# Configuration
DEPT=$1
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LINKS_FILE="${SCRIPT_DIR}/departments/${DEPT}_links.txt"
OUTPUT_DIR="${SCRIPT_DIR}/raw_pages/${DEPT}"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Usage information
usage() {
    echo "Usage: $0 <department>"
    echo ""
    echo "Available departments:"
    echo "  - science"
    echo "  - engineering"
    echo "  - legal"
    echo "  - medicine"
    echo "  - cybersecurity"
    echo ""
    echo "Example:"
    echo "  $0 science"
    exit 1
}

# Validate input
if [ -z "$DEPT" ]; then
    echo -e "${RED}Error: Department name required${NC}"
    usage
fi

if [ ! -f "$LINKS_FILE" ]; then
    echo -e "${RED}Error: Links file not found: $LINKS_FILE${NC}"
    echo ""
    echo "Available departments:"
    ls -1 "${SCRIPT_DIR}/departments/" | sed 's/_links.txt//' | sed 's/^/  - /'
    exit 1
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Statistics
total=0
success=0
failed=0
skipped=0
start_time=$(date +%s)

echo -e "${BLUE}╔════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  Distributed Research Automation v1.0     ║${NC}"
echo -e "${BLUE}║  Department: $(printf '%-28s' "$DEPT")║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}Starting research fetch...${NC}"
echo ""

i=1
while IFS= read -r line || [ -n "$line" ]; do
    # Skip empty lines and comments
    if [ -z "$line" ] || [[ "$line" =~ ^[[:space:]]*# ]]; then
        continue
    fi
    
    url="$line"
    total=$((total + 1))
    output_file="${OUTPUT_DIR}/page_${i}.html"
    
    # Progress indicator
    echo -ne "${BLUE}[$i]${NC} Fetching: $(echo "$url" | cut -c1-60)..."
    
    # Check if file already exists and is not empty
    if [ -f "$output_file" ] && [ -s "$output_file" ]; then
        size=$(stat -f%z "$output_file" 2>/dev/null || stat -c%s "$output_file" 2>/dev/null)
        if [ "$size" -gt 1000 ]; then
            echo -e " ${YELLOW}[CACHED]${NC} (${size} bytes)"
            skipped=$((skipped + 1))
            ((i++))
            continue
        fi
    fi
    
    # Fetch the URL silently with curl
    # -L: follow redirects
    # -s: silent mode
    # --max-time: timeout after 30 seconds
    # --retry: retry twice on failure
    # -H: set user agent
    if curl -L -s \
        --max-time 30 \
        --retry 2 \
        --retry-delay 1 \
        -H "User-Agent: Strategickhaos-Research-Bot/1.0" \
        -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" \
        "$url" > "$output_file" 2>/dev/null; then
        
        # Check if file has content
        if [ -s "$output_file" ]; then
            size=$(stat -f%z "$output_file" 2>/dev/null || stat -c%s "$output_file" 2>/dev/null)
            if [ "$size" -gt 1000 ]; then
                echo -e " ${GREEN}[OK]${NC} (${size} bytes)"
                success=$((success + 1))
            else
                echo -e " ${YELLOW}[WARN]${NC} (file too small: ${size} bytes)"
                failed=$((failed + 1))
            fi
        else
            echo -e " ${RED}[FAIL]${NC} (empty response)"
            rm -f "$output_file"
            failed=$((failed + 1))
        fi
    else
        echo -e " ${RED}[FAIL]${NC} (curl error)"
        rm -f "$output_file"
        failed=$((failed + 1))
    fi
    
    ((i++))
    
    # Rate limiting - be nice to servers
    sleep 0.5
    
done < "$LINKS_FILE"

end_time=$(date +%s)
duration=$((end_time - start_time))

# Summary
echo ""
echo -e "${BLUE}╔════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  Collection Summary                        ║${NC}"
echo -e "${BLUE}╠════════════════════════════════════════════╣${NC}"
echo -e "${BLUE}║${NC} Department:     ${DEPT}"
echo -e "${BLUE}║${NC} Total URLs:     ${total}"
echo -e "${BLUE}║${NC} Successful:     ${GREEN}${success}${NC}"
echo -e "${BLUE}║${NC} Failed:         ${RED}${failed}${NC}"
echo -e "${BLUE}║${NC} Cached:         ${YELLOW}${skipped}${NC}"
echo -e "${BLUE}║${NC} Success Rate:   $((total > 0 ? success * 100 / total : 0))%"
echo -e "${BLUE}║${NC} Duration:       ${duration}s"
echo -e "${BLUE}║${NC} Output Dir:     ${OUTPUT_DIR}"
echo -e "${BLUE}╚════════════════════════════════════════════╝${NC}"

# Create metadata file
cat > "${OUTPUT_DIR}/metadata.json" <<EOF
{
  "department": "$DEPT",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "total_urls": $total,
  "successful": $success,
  "failed": $failed,
  "cached": $skipped,
  "success_rate": $((total > 0 ? success * 100 / total : 0)),
  "duration_seconds": $duration,
  "output_directory": "$OUTPUT_DIR"
}
EOF

exit 0
