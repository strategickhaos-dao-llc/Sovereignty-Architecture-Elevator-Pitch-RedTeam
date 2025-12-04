#!/usr/bin/env bash
set -euo pipefail

#############################################################################
# Arsenal Bibliography Bulk Downloader
#############################################################################
# Downloads all 100 research papers from the Arsenal Bibliography
# Usage: ./arsenal-download.sh [output_directory]
#
# Example:
#   ./arsenal-download.sh                    # Downloads to ./arsenal_papers/
#   ./arsenal-download.sh /opt/arsenal       # Downloads to /opt/arsenal/
#############################################################################

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ARSENAL_TXT="${SCRIPT_DIR}/arsenal.txt"
DEFAULT_OUTPUT_DIR="${SCRIPT_DIR}/arsenal_papers"
OUTPUT_DIR="${1:-$DEFAULT_OUTPUT_DIR}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $*"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $*"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $*"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $*"
}

# Check dependencies
check_dependencies() {
    local missing_deps=()
    
    for cmd in curl wget; do
        if ! command -v "$cmd" &> /dev/null; then
            missing_deps+=("$cmd")
        fi
    done
    
    if [ ${#missing_deps[@]} -ne 0 ]; then
        log_error "Missing required dependencies: ${missing_deps[*]}"
        log_info "Please install missing tools and try again"
        exit 1
    fi
}

# Create output directory
setup_output_dir() {
    if [ ! -d "$OUTPUT_DIR" ]; then
        log_info "Creating output directory: $OUTPUT_DIR"
        mkdir -p "$OUTPUT_DIR"
    else
        log_info "Using existing output directory: $OUTPUT_DIR"
    fi
}

# Download a single URL
download_file() {
    local url="$1"
    local index="$2"
    local total="$3"
    
    log_info "[$index/$total] Downloading: $url"
    
    # Try curl first (follows redirects, silent mode)
    if curl -L -s -f -o /dev/null -w "%{http_code}" "$url" | grep -q "^[23]"; then
        # Extract filename from URL or generate one
        local filename
        filename=$(basename "$url" | sed 's/[?#].*$//')
        
        # If filename is too generic or empty, use index-based naming
        if [[ -z "$filename" || "$filename" == "final" || "$filename" == "index.html" ]]; then
            filename="paper_${index}.pdf"
        fi
        
        local output_path="${OUTPUT_DIR}/${filename}"
        
        # Download the file
        if curl -L -s -o "$output_path" "$url"; then
            log_success "Downloaded: $filename"
            return 0
        else
            log_warning "Failed with curl, trying wget: $url"
        fi
    fi
    
    # Fallback to wget
    if command -v wget &> /dev/null; then
        if wget -q -P "$OUTPUT_DIR" "$url"; then
            log_success "Downloaded with wget: $url"
            return 0
        fi
    fi
    
    log_error "Failed to download: $url"
    return 1
}

# Main download function
download_arsenal() {
    if [ ! -f "$ARSENAL_TXT" ]; then
        log_error "Arsenal URL list not found: $ARSENAL_TXT"
        exit 1
    fi
    
    local total_urls
    total_urls=$(wc -l < "$ARSENAL_TXT")
    log_info "Found $total_urls URLs to download"
    
    local success_count=0
    local fail_count=0
    local index=1
    
    while IFS= read -r url || [ -n "$url" ]; do
        # Skip empty lines and comments
        [[ -z "$url" || "$url" =~ ^[[:space:]]*# ]] && continue
        
        if download_file "$url" "$index" "$total_urls"; then
            ((success_count++))
        else
            ((fail_count++))
        fi
        
        ((index++))
        
        # Small delay to be respectful to servers
        sleep 0.5
    done < "$ARSENAL_TXT"
    
    # Summary
    echo ""
    log_info "=========================================="
    log_info "Download Summary"
    log_info "=========================================="
    log_success "Successfully downloaded: $success_count files"
    if [ $fail_count -gt 0 ]; then
        log_warning "Failed downloads: $fail_count files"
    fi
    log_info "Files saved to: $OUTPUT_DIR"
    log_info "=========================================="
}

# Display usage information
show_usage() {
    cat << EOF
Arsenal Bibliography Bulk Downloader

Usage:
    $0 [output_directory]

Arguments:
    output_directory    Optional. Directory where papers will be saved.
                        Default: ${DEFAULT_OUTPUT_DIR}

Examples:
    $0                              # Download to ./arsenal_papers/
    $0 /opt/arsenal                 # Download to /opt/arsenal/
    $0 ~/Documents/research         # Download to ~/Documents/research/

Description:
    Downloads all 100 research papers from the Arsenal Bibliography.
    All papers are freely accessible from .gov, .org, .edu, arXiv, or
    direct open-access sources.

Requirements:
    - curl or wget
    - Internet connection
    - ~500MB free disk space (estimated)

EOF
}

# Main execution
main() {
    # Show usage if help requested
    if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
        show_usage
        exit 0
    fi
    
    log_info "Arsenal Bibliography Bulk Downloader"
    log_info "======================================"
    echo ""
    
    check_dependencies
    setup_output_dir
    download_arsenal
    
    echo ""
    log_success "Download complete!"
    log_info "View the Arsenal Bibliography: ${SCRIPT_DIR}/ARSENAL_BIBLIOGRAPHY.md"
}

# Run main function
main "$@"
