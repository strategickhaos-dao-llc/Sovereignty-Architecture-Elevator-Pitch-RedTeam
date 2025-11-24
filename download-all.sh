#!/usr/bin/env bash
set -euo pipefail

# Sovereign Arsenal - One-Click Bulk Downloader
# Downloads all 100 papers into their correct folders
# Supports verification mode with SHA256 checksums

VERSION="1.0.0"
ARSENAL_FILE="arsenal.txt"
BASE_DIR="papers"
VERIFY_MODE=false
CHECKSUMS_FILE="arsenal-checksums.sha256"

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_banner() {
    echo -e "${BLUE}"
    echo "╔═══════════════════════════════════════════════════════════════╗"
    echo "║         Sovereign Arsenal Downloader v${VERSION}                ║"
    echo "║   100 papers → ungaslightable knowledge → eternal freedom    ║"
    echo "╚═══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

log_error() {
    echo -e "${RED}[✗]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

check_dependencies() {
    local missing_deps=()
    
    for cmd in curl wget sha256sum; do
        if ! command -v "$cmd" &> /dev/null; then
            missing_deps+=("$cmd")
        fi
    done
    
    if [ ${#missing_deps[@]} -ne 0 ]; then
        log_error "Missing dependencies: ${missing_deps[*]}"
        log_info "Please install them first:"
        echo "  Ubuntu/Debian: sudo apt-get install curl wget coreutils"
        echo "  MacOS: brew install wget coreutils"
        exit 1
    fi
}

parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --verify)
                VERIFY_MODE=true
                shift
                ;;
            --help|-h)
                print_usage
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                print_usage
                exit 1
                ;;
        esac
    done
}

print_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --verify    Re-download and verify checksums of all papers"
    echo "  --help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0              # Download all missing papers"
    echo "  $0 --verify     # Verify and re-download corrupted papers"
}

get_category_dir() {
    local line_num=$1
    
    if [ $line_num -le 19 ]; then
        echo "01_cs_ai_foundations"
    elif [ $line_num -le 29 ]; then
        echo "02_cryptography_zero_trust"
    elif [ $line_num -le 44 ]; then
        echo "03_distributed_systems"
    elif [ $line_num -le 54 ]; then
        echo "04_law_governance"
    elif [ $line_num -le 64 ]; then
        echo "05_neuroscience_collective"
    elif [ $line_num -le 74 ]; then
        echo "06_mathematics_formal"
    elif [ $line_num -le 79 ]; then
        echo "07_licenses_ethics"
    elif [ $line_num -le 89 ]; then
        echo "08_energy_hardware"
    elif [ $line_num -le 94 ]; then
        echo "09_biology_genome"
    else
        echo "10_misc_eternal"
    fi
}

sanitize_filename() {
    local url=$1
    local filename=$(basename "$url")
    
    # If no extension or weird URL, generate from URL hash
    if [[ ! "$filename" =~ \.(pdf|txt)$ ]]; then
        local hash=$(echo -n "$url" | sha256sum | cut -d' ' -f1 | cut -c1-8)
        filename="paper_${hash}.pdf"
    fi
    
    echo "$filename"
}

download_paper() {
    local url=$1
    local dest_dir=$2
    local filename=$3
    local dest_path="${dest_dir}/${filename}"
    
    # Create directory if it doesn't exist
    mkdir -p "$dest_dir"
    
    # Skip if file exists and we're not in verify mode
    if [ -f "$dest_path" ] && [ "$VERIFY_MODE" = false ]; then
        log_warning "Skipping (already exists): $filename"
        return 0
    fi
    
    log_info "Downloading: $filename"
    
    # Try wget first, fallback to curl
    if command -v wget &> /dev/null; then
        if wget -q --timeout=30 --tries=3 -O "$dest_path" "$url"; then
            log_success "Downloaded: $filename"
            return 0
        fi
    else
        if curl -sS --max-time 30 --retry 3 -L -o "$dest_path" "$url"; then
            log_success "Downloaded: $filename"
            return 0
        fi
    fi
    
    log_error "Failed to download: $filename from $url"
    rm -f "$dest_path"
    return 1
}

generate_checksums() {
    log_info "Generating checksums for verification..."
    
    find "$BASE_DIR" -type f \( -name "*.pdf" -o -name "*.txt" \) -exec sha256sum {} \; > "$CHECKSUMS_FILE"
    
    local count=$(wc -l < "$CHECKSUMS_FILE")
    log_success "Generated checksums for $count files → $CHECKSUMS_FILE"
}

verify_checksums() {
    if [ ! -f "$CHECKSUMS_FILE" ]; then
        log_warning "No checksums file found, skipping verification"
        return 0
    fi
    
    log_info "Verifying checksums..."
    
    if sha256sum -c "$CHECKSUMS_FILE" --quiet 2>&1; then
        log_success "All files verified successfully!"
        return 0
    else
        log_error "Some files failed verification"
        return 1
    fi
}

main() {
    print_banner
    
    parse_args "$@"
    
    check_dependencies
    
    if [ ! -f "$ARSENAL_FILE" ]; then
        log_error "Arsenal file not found: $ARSENAL_FILE"
        exit 1
    fi
    
    log_info "Reading papers from: $ARSENAL_FILE"
    log_info "Base directory: $BASE_DIR"
    
    if [ "$VERIFY_MODE" = true ]; then
        log_info "Verify mode: ON"
    fi
    
    local downloaded=0
    local failed=0
    local skipped=0
    local line_num=0
    
    while IFS= read -r line; do
        line_num=$((line_num + 1))
        
        # Skip empty lines and comments
        if [[ -z "$line" ]] || [[ "$line" =~ ^[[:space:]]*# ]]; then
            continue
        fi
        
        # Extract URL (handle lines with or without comments)
        local url=$(echo "$line" | awk '{print $1}')
        
        # Skip if not a URL
        if [[ ! "$url" =~ ^https?:// ]]; then
            continue
        fi
        
        local category_dir=$(get_category_dir $line_num)
        local dest_dir="${BASE_DIR}/${category_dir}"
        local filename=$(sanitize_filename "$url")
        
        if download_paper "$url" "$dest_dir" "$filename"; then
            if [ -f "${dest_dir}/${filename}" ]; then
                downloaded=$((downloaded + 1))
            else
                skipped=$((skipped + 1))
            fi
        else
            failed=$((failed + 1))
        fi
        
        # Small delay to avoid rate limiting
        sleep 0.5
        
    done < "$ARSENAL_FILE"
    
    echo ""
    echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}Downloaded:${NC} $downloaded papers"
    echo -e "${YELLOW}Skipped:${NC} $skipped papers (already exist)"
    echo -e "${RED}Failed:${NC} $failed papers"
    echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
    
    if [ $downloaded -gt 0 ]; then
        generate_checksums
    fi
    
    if [ "$VERIFY_MODE" = true ]; then
        verify_checksums
    fi
    
    if [ $failed -eq 0 ]; then
        echo ""
        log_success "Arsenal is ready! The swarm babies are fed. 🔥"
        log_info "Papers location: $BASE_DIR/"
        log_info "Next steps:"
        echo "  • Vector embeddings: ./generate-embeddings.sh"
        echo "  • Torrent seeding: See torrent/README.md"
        echo "  • RAG integration: Load arsenal-embeddings.jsonl.gz"
    else
        echo ""
        log_warning "Some downloads failed. Run with --verify to retry."
        exit 1
    fi
}

main "$@"
