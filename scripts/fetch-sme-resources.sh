#!/bin/bash
# Fetch all 100 SME resources using curl commands from sme-resources.yaml
# This script extracts and executes curl commands for each resource

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
RESOURCES_FILE="$PROJECT_ROOT/sme-resources.yaml"
OUTPUT_DIR="$PROJECT_ROOT/sme-resources-output"
LOG_FILE="$OUTPUT_DIR/fetch.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Create output directory
mkdir -p "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR/raw"
mkdir -p "$OUTPUT_DIR/logs"

# Initialize log
echo "SME Resources Fetch - $(date)" > "$LOG_FILE"
echo "======================================" >> "$LOG_FILE"

# Counter
total=0
success=0
failed=0

echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}SME Resources Fetcher${NC}"
echo -e "${BLUE}======================================${NC}"
echo -e "Resources file: ${RESOURCES_FILE}"
echo -e "Output directory: ${OUTPUT_DIR}"
echo ""

# Function to fetch a single resource
fetch_resource() {
    local id=$1
    local url=$2
    local title=$3
    local category=$4
    
    ((total++))
    
    echo -e "${YELLOW}[$id] ${title}${NC}"
    echo -e "  URL: ${url}"
    echo -e "  Category: ${category}"
    
    # Create filename
    local filename=$(printf "%03d_%s" "$id" "$(echo "$category" | tr '[:upper:]' '[:lower:]' | tr ' ' '_')")
    local output_file="$OUTPUT_DIR/raw/${filename}.html"
    
    # Log entry
    echo "[$id] $title" >> "$LOG_FILE"
    echo "  URL: $url" >> "$LOG_FILE"
    
    # Fetch with curl
    if curl -L -s \
        --max-time 30 \
        --retry 3 \
        --retry-delay 2 \
        -H "User-Agent: SovereignArchitecture-SME-Bot/1.0" \
        -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" \
        -o "$output_file" \
        "$url" 2>> "$OUTPUT_DIR/logs/error_$id.log"; then
        
        # Check if file has content
        if [ -s "$output_file" ]; then
            local size=$(du -h "$output_file" | cut -f1)
            echo -e "  ${GREEN}✓ Success${NC} (${size})"
            echo "  Status: SUCCESS ($size)" >> "$LOG_FILE"
            ((success++))
        else
            echo -e "  ${RED}✗ Failed${NC} (empty response)"
            echo "  Status: FAILED (empty)" >> "$LOG_FILE"
            ((failed++))
            rm -f "$output_file"
        fi
    else
        echo -e "  ${RED}✗ Failed${NC}"
        echo "  Status: FAILED (curl error)" >> "$LOG_FILE"
        ((failed++))
    fi
    
    echo "" >> "$LOG_FILE"
    
    # Rate limiting - 2 requests per second
    sleep 0.5
}

# Extract resources from YAML and fetch them
# This is a simple grep-based extraction
# For production use, consider using yq or a Python script for proper YAML parsing

echo -e "${BLUE}Extracting resources from YAML...${NC}\n"

# Parse YAML (simple approach - assumes specific format)
while IFS= read -r line; do
    if [[ "$line" =~ ^[[:space:]]*-[[:space:]]+id:[[:space:]]+([0-9]+) ]]; then
        current_id="${BASH_REMATCH[1]}"
    elif [[ "$line" =~ ^[[:space:]]+title:[[:space:]]+\"(.+)\" ]]; then
        current_title="${BASH_REMATCH[1]}"
    elif [[ "$line" =~ ^[[:space:]]+url:[[:space:]]+\"(.+)\" ]]; then
        current_url="${BASH_REMATCH[1]}"
    elif [[ "$line" =~ ^[[:space:]]+category:[[:space:]]+\"(.+)\" ]]; then
        current_category="${BASH_REMATCH[1]}"
        
        # When we have all fields, fetch the resource
        if [ -n "$current_id" ] && [ -n "$current_url" ]; then
            fetch_resource "$current_id" "$current_url" "$current_title" "$current_category"
            
            # Reset variables
            current_id=""
            current_title=""
            current_url=""
            current_category=""
        fi
    fi
done < "$RESOURCES_FILE"

# Summary
echo -e "\n${BLUE}======================================${NC}"
echo -e "${BLUE}FETCH SUMMARY${NC}"
echo -e "${BLUE}======================================${NC}"
echo -e "Total resources: ${total}"
echo -e "${GREEN}Successful: ${success}${NC}"
echo -e "${RED}Failed: ${failed}${NC}"

# Calculate percentage
if [ $total -gt 0 ]; then
    percent=$((success * 100 / total))
    echo -e "Success rate: ${percent}%"
fi

# Write summary to log
echo "" >> "$LOG_FILE"
echo "======================================" >> "$LOG_FILE"
echo "SUMMARY" >> "$LOG_FILE"
echo "======================================" >> "$LOG_FILE"
echo "Total: $total" >> "$LOG_FILE"
echo "Successful: $success" >> "$LOG_FILE"
echo "Failed: $failed" >> "$LOG_FILE"
if [ $total -gt 0 ]; then
    echo "Success rate: ${percent}%" >> "$LOG_FILE"
fi

echo -e "\nLog saved to: ${LOG_FILE}"
echo -e "Raw files saved to: ${OUTPUT_DIR}/raw/"

# Generate index
INDEX_FILE="$OUTPUT_DIR/index.html"
echo "<!DOCTYPE html>" > "$INDEX_FILE"
echo "<html><head><title>SME Resources Index</title></head><body>" >> "$INDEX_FILE"
echo "<h1>SME Resources - Fetched $(date)</h1>" >> "$INDEX_FILE"
echo "<p>Total: $total | Success: $success | Failed: $failed</p>" >> "$INDEX_FILE"
echo "<ul>" >> "$INDEX_FILE"

for file in "$OUTPUT_DIR/raw"/*.html; do
    if [ -f "$file" ]; then
        basename=$(basename "$file")
        echo "<li><a href='raw/$basename'>$basename</a></li>" >> "$INDEX_FILE"
    fi
done

echo "</ul></body></html>" >> "$INDEX_FILE"

echo -e "\nIndex created: ${INDEX_FILE}"
echo -e "\n${GREEN}✓ Fetch complete!${NC}\n"
