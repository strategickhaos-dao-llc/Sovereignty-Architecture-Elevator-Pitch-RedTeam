#!/usr/bin/env bash

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ARSENAL_FILE="${SCRIPT_DIR}/arsenal.txt"
PAPERS_DIR="${SCRIPT_DIR}/papers"
VERIFY_MODE=false
PARALLEL_JOBS=4

# Statistics
TOTAL_PAPERS=0
SUCCESS_COUNT=0
FAIL_COUNT=0
SKIP_COUNT=0

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --verify)
            VERIFY_MODE=true
            shift
            ;;
        -j|--jobs)
            PARALLEL_JOBS="$2"
            shift 2
            ;;
        -h|--help)
            echo "Sovereign Arsenal Downloader"
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --verify        Re-download and verify all papers"
            echo "  -j, --jobs N    Number of parallel downloads (default: 4)"
            echo "  -h, --help      Show this help message"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

# Check dependencies
check_dependencies() {
    local missing_deps=()
    
    for cmd in wget curl; do
        if ! command -v "$cmd" &> /dev/null; then
            missing_deps+=("$cmd")
        fi
    done
    
    if [ ${#missing_deps[@]} -gt 0 ]; then
        echo -e "${RED}Error: Missing required dependencies: ${missing_deps[*]}${NC}"
        echo "Please install them and try again."
        exit 1
    fi
}

# Create directory structure
create_directories() {
    echo -e "${BLUE}Creating directory structure...${NC}"
    mkdir -p "$PAPERS_DIR"/{01_cs_ai_foundations,02_cryptography_zero_trust,03_distributed_systems,04_law_governance,05_neuroscience_collective,06_mathematics_formal,07_licenses_ethics,08_energy_hardware,09_biology_genome,10_misc_eternal}
}

# Determine target directory based on line number
get_target_dir() {
    local line_num=$1
    local category_dirs=(
        "01_cs_ai_foundations"
        "02_cryptography_zero_trust"
        "03_distributed_systems"
        "04_law_governance"
        "05_neuroscience_collective"
        "06_mathematics_formal"
        "07_licenses_ethics"
        "08_energy_hardware"
        "09_biology_genome"
        "10_misc_eternal"
    )
    
    # Each category has 10 papers plus 1 header line
    local category_index=$(( (line_num - 1) / 11 ))
    
    if [ $category_index -lt ${#category_dirs[@]} ]; then
        echo "${category_dirs[$category_index]}"
    else
        echo "10_misc_eternal"  # Default to last category
    fi
}

# Extract filename from URL
get_filename_from_url() {
    local url=$1
    local filename=$(basename "$url" | sed 's/[?&].*//')
    
    # If URL doesn't end with a file extension, create a descriptive name
    if [[ ! "$filename" =~ \.(pdf|txt|html)$ ]]; then
        filename=$(echo "$url" | sed 's|https\?://||; s|/|_|g; s|[^a-zA-Z0-9._-]|_|g').html
    fi
    
    echo "$filename"
}

# Download a single paper
download_paper() {
    local url=$1
    local target_dir=$2
    local filename=$(get_filename_from_url "$url")
    local filepath="${PAPERS_DIR}/${target_dir}/${filename}"
    
    # Skip if file exists and not in verify mode
    if [ -f "$filepath" ] && [ "$VERIFY_MODE" = false ]; then
        echo -e "${YELLOW}⏭  Skipping (exists): $filename${NC}"
        SKIP_COUNT=$((SKIP_COUNT + 1))
        return 0
    fi
    
    echo -e "${BLUE}⬇  Downloading: $filename${NC}"
    
    # Try wget first, fall back to curl
    if wget -q --timeout=30 --tries=3 -O "$filepath" "$url" 2>/dev/null; then
        echo -e "${GREEN}✓  Success: $filename${NC}"
        SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
        return 0
    elif curl -fsSL --max-time 30 --retry 3 -o "$filepath" "$url" 2>/dev/null; then
        echo -e "${GREEN}✓  Success: $filename${NC}"
        SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
        return 0
    else
        echo -e "${RED}✗  Failed: $filename (URL: $url)${NC}"
        FAIL_COUNT=$((FAIL_COUNT + 1))
        rm -f "$filepath"  # Clean up partial download
        return 1
    fi
}

# Main download function
download_all() {
    echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║   Sovereign Arsenal Downloader v1.0   ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
    echo ""
    
    if [ ! -f "$ARSENAL_FILE" ]; then
        echo -e "${RED}Error: arsenal.txt not found at $ARSENAL_FILE${NC}"
        exit 1
    fi
    
    # Count total papers
    TOTAL_PAPERS=$(grep -E '^https://' "$ARSENAL_FILE" | wc -l)
    echo -e "${BLUE}Total papers to download: $TOTAL_PAPERS${NC}"
    echo -e "${BLUE}Parallel jobs: $PARALLEL_JOBS${NC}"
    echo -e "${BLUE}Verify mode: $VERIFY_MODE${NC}"
    echo ""
    
    local line_num=0
    local current_category=""
    
    while IFS= read -r line; do
        line_num=$((line_num + 1))
        
        # Skip empty lines
        if [ -z "$line" ]; then
            continue
        fi
        
        # Track category headers
        if [[ "$line" =~ ^#.*Category: ]]; then
            current_category=$(echo "$line" | sed 's/^#.*Category: //' | sed 's/ (.*//')
            echo -e "\n${YELLOW}═══ Category: $current_category ═══${NC}"
            continue
        fi
        
        # Skip other comments
        if [[ "$line" =~ ^# ]]; then
            continue
        fi
        
        # Extract URL (first field)
        local url=$(echo "$line" | awk '{print $1}')
        
        if [[ "$url" =~ ^https:// ]]; then
            local target_dir=$(get_target_dir $line_num)
            
            # Download in background if parallel mode
            if [ $PARALLEL_JOBS -gt 1 ]; then
                # Wait if we have too many background jobs
                while [ $(jobs -r | wc -l) -ge $PARALLEL_JOBS ]; do
                    sleep 0.1
                done
                download_paper "$url" "$target_dir" &
            else
                download_paper "$url" "$target_dir"
            fi
        fi
    done < "$ARSENAL_FILE"
    
    # Wait for all background jobs to complete
    wait
    
    # Print summary
    echo ""
    echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║         Download Complete              ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${GREEN}✓  Success: $SUCCESS_COUNT${NC}"
    echo -e "${YELLOW}⏭  Skipped: $SKIP_COUNT${NC}"
    echo -e "${RED}✗  Failed:  $FAIL_COUNT${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}Total:      $TOTAL_PAPERS${NC}"
    echo ""
    
    if [ $FAIL_COUNT -gt 0 ]; then
        echo -e "${YELLOW}Note: Some downloads failed. This is normal for:${NC}"
        echo -e "${YELLOW}  - Paywalled academic papers${NC}"
        echo -e "${YELLOW}  - Moved/deleted resources${NC}"
        echo -e "${YELLOW}  - Temporary network issues${NC}"
        echo ""
        echo -e "${YELLOW}Try running with --verify to retry failed downloads.${NC}"
    fi
    
    if [ $SUCCESS_COUNT -gt 0 ]; then
        echo -e "${GREEN}The swarm babies are fed! 🎉${NC}"
    fi
}

# Main execution
main() {
    check_dependencies
    create_directories
    download_all
}

main "$@"
