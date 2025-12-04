#!/bin/bash
# =============================================================================
# Sovereignty Analysis Script
# Version: 1.0.0
# Description: Comprehensive automation for reverse engineering and 
#              sovereignty analysis workflows
# =============================================================================

set -euo pipefail

# =============================================================================
# Configuration
# =============================================================================
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="${SCRIPT_DIR}/sovereignty_analysis_config.yaml"
METHODOLOGY_FILE="${SCRIPT_DIR}/REVERSE_ENGINEERING_SOVEREIGNTY_METHODOLOGY.md"

# Default paths
CAPTURES_DIR="${SCRIPT_DIR}/captures"
ANALYSIS_DIR="${SCRIPT_DIR}/analysis"
REPORTS_DIR="${SCRIPT_DIR}/reports"
LOGS_DIR="${SCRIPT_DIR}/logs"
OBSIDIAN_VAULT="${HOME}/obsidian/vault"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Logging
LOG_FILE="${LOGS_DIR}/sovereignty-analysis-$(date +%Y%m%d).log"

# =============================================================================
# Helper Functions
# =============================================================================

log() {
    local level="$1"
    shift
    local message="$*"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    case "$level" in
        INFO)  color="$GREEN" ;;
        WARN)  color="$YELLOW" ;;
        ERROR) color="$RED" ;;
        DEBUG) color="$CYAN" ;;
        *)     color="$NC" ;;
    esac
    
    echo -e "${color}[$timestamp] [$level] $message${NC}"
    echo "[$timestamp] [$level] $message" >> "$LOG_FILE" 2>/dev/null || true
}

info() { log "INFO" "$@"; }
warn() { log "WARN" "$@"; }
error() { log "ERROR" "$@"; }
debug() { log "DEBUG" "$@"; }

check_dependencies() {
    local deps=("python3" "curl" "jq" "git")
    local missing=()
    
    for dep in "${deps[@]}"; do
        if ! command -v "$dep" &> /dev/null; then
            missing+=("$dep")
        fi
    done
    
    if [ ${#missing[@]} -ne 0 ]; then
        error "Missing dependencies: ${missing[*]}"
        error "Please install them before continuing."
        return 1
    fi
    
    info "All dependencies satisfied"
    return 0
}

ensure_directories() {
    local dirs=("$CAPTURES_DIR" "$ANALYSIS_DIR" "$REPORTS_DIR" "$LOGS_DIR")
    
    for dir in "${dirs[@]}"; do
        if [ ! -d "$dir" ]; then
            mkdir -p "$dir"
            info "Created directory: $dir"
        fi
    done
}

# =============================================================================
# Initialization
# =============================================================================

cmd_init() {
    echo -e "${PURPLE}"
    echo "╔═══════════════════════════════════════════════════════════════════╗"
    echo "║       Sovereignty Analysis Framework - Initialization             ║"
    echo "╚═══════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    info "Initializing Sovereignty Analysis environment..."
    
    # Check dependencies
    check_dependencies || exit 1
    
    # Create directories
    ensure_directories
    
    # Create Obsidian vault structure if it doesn't exist
    if [ ! -d "$OBSIDIAN_VAULT" ]; then
        info "Creating Obsidian vault structure..."
        mkdir -p "$OBSIDIAN_VAULT/analysis/security"
        mkdir -p "$OBSIDIAN_VAULT/analysis/performance"
        mkdir -p "$OBSIDIAN_VAULT/analysis/comparison"
        mkdir -p "$OBSIDIAN_VAULT/analysis/methodology"
        mkdir -p "$OBSIDIAN_VAULT/reports/daily"
        mkdir -p "$OBSIDIAN_VAULT/reports/weekly"
        mkdir -p "$OBSIDIAN_VAULT/templates"
    fi
    
    # Check if config exists
    if [ ! -f "$CONFIG_FILE" ]; then
        warn "Configuration file not found: $CONFIG_FILE"
        warn "Please ensure sovereignty_analysis_config.yaml exists"
    else
        info "Configuration file found: $CONFIG_FILE"
    fi
    
    # Check if methodology exists
    if [ ! -f "$METHODOLOGY_FILE" ]; then
        warn "Methodology file not found: $METHODOLOGY_FILE"
    else
        info "Methodology file found: $METHODOLOGY_FILE"
    fi
    
    # Create attestation template
    cat > "${SCRIPT_DIR}/ATTESTATION_TEMPLATE.md" << 'ATTESTATION'
# Clean Room Implementation Attestation

Date: _______________
Analyst: _______________
Target System: _______________

## Attestation Statement

I, the undersigned, hereby attest that:

1. [ ] I have NOT viewed any proprietary source code of the analyzed system
2. [ ] All implementations are derived from publicly available specifications
3. [ ] Analysis is performed only on software for which we have proper licensing
4. [ ] All work complies with applicable laws and regulations
5. [ ] I have documented my methodology for audit purposes

## Analysis Scope

- [ ] Security header analysis
- [ ] API endpoint enumeration
- [ ] Authentication flow mapping
- [ ] Performance benchmarking
- [ ] Other: _______________

## Tools Used

List all tools used during analysis:
1. 
2. 
3. 

## Signatures

Analyst Signature: _______________
Date: _______________

Reviewer Signature: _______________
Date: _______________
ATTESTATION

    info "Created attestation template: ${SCRIPT_DIR}/ATTESTATION_TEMPLATE.md"
    
    # Initialize git tracking for analysis files if not already tracked
    if [ -d "${SCRIPT_DIR}/.git" ]; then
        info "Git repository detected, adding analysis directories..."
        git add -N "$CAPTURES_DIR" "$ANALYSIS_DIR" "$REPORTS_DIR" 2>/dev/null || true
    fi
    
    echo ""
    echo -e "${GREEN}✓ Initialization complete!${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Review REVERSE_ENGINEERING_SOVEREIGNTY_METHODOLOGY.md"
    echo "  2. Configure sovereignty_analysis_config.yaml"
    echo "  3. Complete ATTESTATION_TEMPLATE.md before analysis"
    echo "  4. Run: ./sovereignty-analysis.sh capture <url>"
    echo ""
}

# =============================================================================
# HAR Capture
# =============================================================================

cmd_capture() {
    local target_url="${1:-}"
    
    if [ -z "$target_url" ]; then
        error "Usage: $0 capture <url>"
        exit 1
    fi
    
    echo -e "${BLUE}"
    echo "╔═══════════════════════════════════════════════════════════════════╗"
    echo "║            HAR Capture - Web Intelligence Gathering               ║"
    echo "╚═══════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    info "Target URL: $target_url"
    
    # Create capture directory with timestamp
    local capture_timestamp=$(date +%Y%m%d_%H%M%S)
    local capture_name=$(echo "$target_url" | sed 's/[^a-zA-Z0-9]/_/g' | cut -c1-50)
    local capture_dir="${CAPTURES_DIR}/${capture_name}_${capture_timestamp}"
    mkdir -p "$capture_dir"
    
    info "Capture directory: $capture_dir"
    
    # Create capture instructions file
    cat > "${capture_dir}/CAPTURE_INSTRUCTIONS.md" << INSTRUCTIONS
# HAR Capture Instructions

**Target**: $target_url
**Date**: $(date)
**Capture ID**: ${capture_name}_${capture_timestamp}

## Firefox Instructions

1. Open Firefox
2. Press F12 to open Developer Tools
3. Navigate to the **Network** tab
4. Check "**Persist Logs**" (gear icon or right-click)
5. Navigate to: $target_url
6. Perform all user actions (login, navigation, etc.)
7. Right-click in the Network panel
8. Select "**Save All As HAR**"
9. Save as: ${capture_dir}/capture.har

## Chrome Instructions

1. Open Chrome
2. Press F12 to open DevTools
3. Navigate to the **Network** tab
4. Check "**Preserve log**"
5. Navigate to: $target_url
6. Perform all user actions
7. Right-click in the Network panel
8. Select "**Save all as HAR with content**"
9. Save as: ${capture_dir}/capture.har

## After Capture

Run the following to analyze:
\`\`\`bash
./sovereignty_analyzer.py analyze-har ${capture_dir}/capture.har
\`\`\`

## Notes

INSTRUCTIONS

    # Create metadata file
    cat > "${capture_dir}/metadata.json" << METADATA
{
    "target_url": "$target_url",
    "capture_timestamp": "$capture_timestamp",
    "capture_id": "${capture_name}_${capture_timestamp}",
    "created_by": "${USER:-unknown}",
    "hostname": "$(hostname)",
    "methodology_version": "1.0.0"
}
METADATA

    info "Created capture instructions: ${capture_dir}/CAPTURE_INSTRUCTIONS.md"
    info "Created metadata file: ${capture_dir}/metadata.json"
    
    # Check if we can do automated capture with curl
    echo ""
    info "Attempting basic reconnaissance..."
    
    # Fetch headers
    local headers_file="${capture_dir}/initial_headers.txt"
    if curl -s -I -L --max-time 10 "$target_url" > "$headers_file" 2>/dev/null; then
        info "Captured initial headers to: $headers_file"
        
        # Quick security header check
        echo ""
        echo -e "${CYAN}=== Initial Security Header Analysis ===${NC}"
        
        local required_headers=("Strict-Transport-Security" "Content-Security-Policy" "X-Content-Type-Options" "X-Frame-Options")
        
        for header in "${required_headers[@]}"; do
            if grep -qi "^${header}:" "$headers_file"; then
                echo -e "  ${GREEN}✓${NC} $header: Present"
            else
                echo -e "  ${RED}✗${NC} $header: Missing"
            fi
        done
        echo ""
    else
        warn "Could not fetch initial headers (target may require authentication)"
    fi
    
    # Check for robots.txt
    local robots_url="${target_url%/}/robots.txt"
    local robots_file="${capture_dir}/robots.txt"
    if curl -s -L --max-time 10 "$robots_url" -o "$robots_file" 2>/dev/null; then
        if [ -s "$robots_file" ] && ! grep -q "<!DOCTYPE" "$robots_file"; then
            info "Captured robots.txt"
        else
            rm -f "$robots_file"
        fi
    fi
    
    # Check for sitemap.xml
    local sitemap_url="${target_url%/}/sitemap.xml"
    local sitemap_file="${capture_dir}/sitemap.xml"
    if curl -s -L --max-time 10 "$sitemap_url" -o "$sitemap_file" 2>/dev/null; then
        if [ -s "$sitemap_file" ] && grep -q "<?xml" "$sitemap_file"; then
            info "Captured sitemap.xml"
        else
            rm -f "$sitemap_file"
        fi
    fi
    
    echo ""
    echo -e "${GREEN}✓ Capture setup complete!${NC}"
    echo ""
    echo "Manual steps required:"
    echo "  1. Open browser and navigate to: $target_url"
    echo "  2. Follow instructions in: ${capture_dir}/CAPTURE_INSTRUCTIONS.md"
    echo "  3. Save HAR file as: ${capture_dir}/capture.har"
    echo ""
    echo "Then analyze with:"
    echo "  ./sovereignty_analyzer.py analyze-har ${capture_dir}/capture.har"
    echo ""
}

# =============================================================================
# HAR Analysis
# =============================================================================

cmd_analyze_har() {
    local har_file="${1:-}"
    
    if [ -z "$har_file" ]; then
        error "Usage: $0 analyze-har <har_file>"
        exit 1
    fi
    
    if [ ! -f "$har_file" ]; then
        error "HAR file not found: $har_file"
        exit 1
    fi
    
    echo -e "${CYAN}"
    echo "╔═══════════════════════════════════════════════════════════════════╗"
    echo "║               HAR Analysis - Security Assessment                   ║"
    echo "╚═══════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    info "Analyzing HAR file: $har_file"
    
    # Check if Python analyzer exists
    local analyzer="${SCRIPT_DIR}/sovereignty_analyzer.py"
    if [ -f "$analyzer" ]; then
        info "Using Python analyzer..."
        python3 "$analyzer" analyze-har "$har_file"
    else
        warn "Python analyzer not found, using basic analysis..."
        basic_har_analysis "$har_file"
    fi
}

basic_har_analysis() {
    local har_file="$1"
    
    info "Running basic HAR analysis..."
    
    # Extract basic statistics using jq
    if command -v jq &> /dev/null; then
        echo ""
        echo -e "${CYAN}=== Basic HAR Statistics ===${NC}"
        
        # Count entries
        local entry_count=$(jq '.log.entries | length' "$har_file" 2>/dev/null || echo "0")
        echo "  Total requests: $entry_count"
        
        # Count by content type
        echo ""
        echo "  Content types:"
        jq -r '.log.entries[].response.content.mimeType // "unknown"' "$har_file" 2>/dev/null | sort | uniq -c | sort -rn | head -10 | while read count type; do
            echo "    $count - $type"
        done
        
        # Extract unique domains
        echo ""
        echo "  Unique domains:"
        jq -r '.log.entries[].request.url' "$har_file" 2>/dev/null | sed 's|https\?://||' | cut -d'/' -f1 | sort -u | head -10 | while read domain; do
            echo "    - $domain"
        done
        
        # Check for potential issues
        echo ""
        echo -e "${CYAN}=== Security Observations ===${NC}"
        
        # Check for HTTP (non-HTTPS) requests
        local http_count=$(jq -r '.log.entries[].request.url' "$har_file" 2>/dev/null | grep -c "^http://" || echo "0")
        if [ "$http_count" -gt 0 ]; then
            echo -e "  ${RED}⚠${NC}  Found $http_count unencrypted HTTP requests"
        else
            echo -e "  ${GREEN}✓${NC}  All requests use HTTPS"
        fi
        
        # Check for cookies without Secure flag
        local insecure_cookies=$(jq -r '.log.entries[].response.cookies[]? | select(.secure != true) | .name' "$har_file" 2>/dev/null | wc -l || echo "0")
        if [ "$insecure_cookies" -gt 0 ]; then
            echo -e "  ${YELLOW}⚠${NC}  Found $insecure_cookies cookies without Secure flag"
        else
            echo -e "  ${GREEN}✓${NC}  All cookies have Secure flag"
        fi
        
        echo ""
    else
        warn "jq not available, skipping detailed HAR analysis"
        warn "Install jq for detailed analysis: apt-get install jq"
    fi
}

# =============================================================================
# Comparison
# =============================================================================

cmd_compare() {
    local original="${1:-}"
    local sovereign="${2:-}"
    
    if [ -z "$original" ] || [ -z "$sovereign" ]; then
        error "Usage: $0 compare <original.har> <sovereign.har>"
        exit 1
    fi
    
    if [ ! -f "$original" ]; then
        error "Original HAR not found: $original"
        exit 1
    fi
    
    if [ ! -f "$sovereign" ]; then
        error "Sovereign HAR not found: $sovereign"
        exit 1
    fi
    
    echo -e "${PURPLE}"
    echo "╔═══════════════════════════════════════════════════════════════════╗"
    echo "║           Version Comparison - Original vs Sovereign               ║"
    echo "╚═══════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    info "Original: $original"
    info "Sovereign: $sovereign"
    
    # Check if Python analyzer exists
    local analyzer="${SCRIPT_DIR}/sovereignty_analyzer.py"
    if [ -f "$analyzer" ]; then
        info "Using Python analyzer for comparison..."
        python3 "$analyzer" compare "$original" "$sovereign"
    else
        warn "Python analyzer not found, using basic comparison..."
        basic_comparison "$original" "$sovereign"
    fi
}

basic_comparison() {
    local original="$1"
    local sovereign="$2"
    
    if command -v jq &> /dev/null; then
        echo ""
        echo -e "${CYAN}=== Basic Comparison ===${NC}"
        
        # Compare request counts
        local orig_count=$(jq '.log.entries | length' "$original" 2>/dev/null || echo "0")
        local sov_count=$(jq '.log.entries | length' "$sovereign" 2>/dev/null || echo "0")
        
        echo "  Request counts:"
        echo "    Original:  $orig_count"
        echo "    Sovereign: $sov_count"
        
        # Compare total transfer size
        local orig_size=$(jq '[.log.entries[].response.content.size // 0] | add' "$original" 2>/dev/null || echo "0")
        local sov_size=$(jq '[.log.entries[].response.content.size // 0] | add' "$sovereign" 2>/dev/null || echo "0")
        
        echo ""
        echo "  Total transfer size:"
        echo "    Original:  $(numfmt --to=iec $orig_size 2>/dev/null || echo $orig_size) bytes"
        echo "    Sovereign: $(numfmt --to=iec $sov_size 2>/dev/null || echo $sov_size) bytes"
        
        # Calculate improvement
        if [ "$orig_size" -gt 0 ] && [ "$orig_size" -eq "$orig_size" ] 2>/dev/null; then
            local improvement=$(echo "scale=2; (($orig_size - $sov_size) / $orig_size) * 100" | bc 2>/dev/null || echo "N/A")
            if [ "$improvement" != "N/A" ]; then
                echo "    Improvement: ${improvement}%"
            fi
        fi
        
        echo ""
    else
        warn "jq not available for comparison"
    fi
}

# =============================================================================
# Report Generation
# =============================================================================

cmd_report() {
    local report_type="${1:-full}"
    local output="${2:-}"
    
    echo -e "${GREEN}"
    echo "╔═══════════════════════════════════════════════════════════════════╗"
    echo "║                  Report Generation                                 ║"
    echo "╚═══════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local report_file="${output:-${REPORTS_DIR}/report_${report_type}_${timestamp}.md}"
    
    info "Generating $report_type report..."
    
    # Create report header
    cat > "$report_file" << HEADER
# Sovereignty Analysis Report

**Report Type**: $report_type
**Generated**: $(date)
**Generator**: sovereignty-analysis.sh v1.0.0

---

## Summary

HEADER

    # Add analysis data
    if [ -d "$ANALYSIS_DIR" ]; then
        echo "### Recent Analyses" >> "$report_file"
        echo "" >> "$report_file"
        find "$ANALYSIS_DIR" -name "*.md" -mtime -7 -type f 2>/dev/null | while read analysis; do
            echo "- $(basename "$analysis")" >> "$report_file"
        done
        echo "" >> "$report_file"
    fi
    
    # Add capture data
    if [ -d "$CAPTURES_DIR" ]; then
        echo "### Recent Captures" >> "$report_file"
        echo "" >> "$report_file"
        find "$CAPTURES_DIR" -name "metadata.json" -mtime -7 -type f 2>/dev/null | while read meta; do
            if command -v jq &> /dev/null; then
                local target=$(jq -r '.target_url' "$meta" 2>/dev/null)
                local ts=$(jq -r '.capture_timestamp' "$meta" 2>/dev/null)
                echo "- $target ($ts)" >> "$report_file"
            fi
        done
        echo "" >> "$report_file"
    fi
    
    # Add footer
    cat >> "$report_file" << FOOTER

---

## Methodology Reference

See [REVERSE_ENGINEERING_SOVEREIGNTY_METHODOLOGY.md](REVERSE_ENGINEERING_SOVEREIGNTY_METHODOLOGY.md) for complete methodology documentation.

## Configuration Reference

See [sovereignty_analysis_config.yaml](sovereignty_analysis_config.yaml) for configuration details.

---

*Generated by Sovereignty Analysis Framework*
FOOTER

    info "Report generated: $report_file"
    
    # Copy to Obsidian vault if it exists
    if [ -d "$OBSIDIAN_VAULT" ]; then
        cp "$report_file" "${OBSIDIAN_VAULT}/reports/"
        info "Report copied to Obsidian vault"
    fi
}

# =============================================================================
# Obsidian Sync
# =============================================================================

cmd_sync() {
    echo -e "${BLUE}"
    echo "╔═══════════════════════════════════════════════════════════════════╗"
    echo "║                  Obsidian Vault Sync                               ║"
    echo "╚═══════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    if [ ! -d "$OBSIDIAN_VAULT" ]; then
        warn "Obsidian vault not found at: $OBSIDIAN_VAULT"
        warn "Run 'init' first to create vault structure"
        return 1
    fi
    
    info "Syncing to Obsidian vault..."
    
    # Sync analysis files
    if [ -d "$ANALYSIS_DIR" ]; then
        find "$ANALYSIS_DIR" -name "*.md" -type f | while read file; do
            local filename=$(basename "$file")
            local category=$(dirname "$file" | xargs basename)
            local dest="${OBSIDIAN_VAULT}/analysis/${category}/${filename}"
            mkdir -p "$(dirname "$dest")"
            cp "$file" "$dest"
            debug "Synced: $filename"
        done
        info "Analysis files synced"
    fi
    
    # Sync report files
    if [ -d "$REPORTS_DIR" ]; then
        find "$REPORTS_DIR" -name "*.md" -type f -mtime -7 | while read file; do
            local filename=$(basename "$file")
            cp "$file" "${OBSIDIAN_VAULT}/reports/${filename}"
            debug "Synced: $filename"
        done
        info "Report files synced"
    fi
    
    # Sync methodology and config
    if [ -f "$METHODOLOGY_FILE" ]; then
        cp "$METHODOLOGY_FILE" "${OBSIDIAN_VAULT}/analysis/methodology/"
        info "Methodology synced"
    fi
    
    echo ""
    echo -e "${GREEN}✓ Sync complete!${NC}"
}

# =============================================================================
# Git Operations
# =============================================================================

cmd_git() {
    local operation="${1:-status}"
    shift
    
    case "$operation" in
        status)
            git --no-pager status
            ;;
        commit)
            local message="${1:-Analysis update}"
            git add "$CAPTURES_DIR" "$ANALYSIS_DIR" "$REPORTS_DIR"
            git commit -m "$message"
            info "Changes committed: $message"
            ;;
        diff)
            git --no-pager diff
            ;;
        log)
            git --no-pager log --oneline -10
            ;;
        *)
            error "Unknown git operation: $operation"
            echo "Available: status, commit <message>, diff, log"
            ;;
    esac
}

# =============================================================================
# Discord Notification
# =============================================================================

cmd_notify() {
    local message="${1:-}"
    local channel="${2:-general}"
    
    if [ -z "$message" ]; then
        error "Usage: $0 notify <message> [channel]"
        exit 1
    fi
    
    # Check for Discord webhook
    local webhook="${DISCORD_WEBHOOK:-}"
    
    if [ -z "$webhook" ]; then
        warn "DISCORD_WEBHOOK not set, cannot send notification"
        warn "Set DISCORD_WEBHOOK environment variable to enable notifications"
        return 1
    fi
    
    # Validate webhook URL format (must be Discord webhook URL)
    if ! echo "$webhook" | grep -qE '^https://discord(app)?\.com/api/webhooks/[0-9]+/[a-zA-Z0-9_-]+$'; then
        error "Invalid Discord webhook URL format"
        error "Expected format: https://discord.com/api/webhooks/{id}/{token}"
        return 1
    fi
    
    info "Sending Discord notification..."
    
    # Escape message for JSON (basic escaping)
    local escaped_message
    escaped_message=$(echo "$message" | sed 's/\\/\\\\/g; s/"/\\"/g; s/\n/\\n/g')
    
    local payload
    payload=$(printf '{"content": "%s", "username": "Sovereignty Analyzer"}' "$escaped_message")
    
    if curl -s --fail -H "Content-Type: application/json" -d "$payload" "$webhook" > /dev/null 2>&1; then
        info "Notification sent to Discord"
    else
        error "Failed to send Discord notification"
    fi
}

# =============================================================================
# Status Check
# =============================================================================

cmd_status() {
    echo -e "${CYAN}"
    echo "╔═══════════════════════════════════════════════════════════════════╗"
    echo "║                 Sovereignty Analysis Status                        ║"
    echo "╚═══════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    # Check files
    echo -e "${CYAN}=== Core Files ===${NC}"
    
    if [ -f "$METHODOLOGY_FILE" ]; then
        echo -e "  ${GREEN}✓${NC} Methodology: $(wc -l < "$METHODOLOGY_FILE") lines"
    else
        echo -e "  ${RED}✗${NC} Methodology: Not found"
    fi
    
    if [ -f "$CONFIG_FILE" ]; then
        echo -e "  ${GREEN}✓${NC} Configuration: $(wc -l < "$CONFIG_FILE") lines"
    else
        echo -e "  ${RED}✗${NC} Configuration: Not found"
    fi
    
    if [ -f "${SCRIPT_DIR}/sovereignty_analyzer.py" ]; then
        echo -e "  ${GREEN}✓${NC} Python Analyzer: $(wc -l < "${SCRIPT_DIR}/sovereignty_analyzer.py") lines"
    else
        echo -e "  ${RED}✗${NC} Python Analyzer: Not found"
    fi
    
    # Check directories
    echo ""
    echo -e "${CYAN}=== Directories ===${NC}"
    
    for dir in "$CAPTURES_DIR" "$ANALYSIS_DIR" "$REPORTS_DIR" "$LOGS_DIR"; do
        if [ -d "$dir" ]; then
            local count=$(find "$dir" -type f 2>/dev/null | wc -l)
            echo -e "  ${GREEN}✓${NC} $(basename "$dir"): $count files"
        else
            echo -e "  ${YELLOW}○${NC} $(basename "$dir"): Not created"
        fi
    done
    
    # Check Obsidian vault
    echo ""
    echo -e "${CYAN}=== Obsidian Vault ===${NC}"
    
    if [ -d "$OBSIDIAN_VAULT" ]; then
        local vault_files=$(find "$OBSIDIAN_VAULT" -name "*.md" -type f 2>/dev/null | wc -l)
        echo -e "  ${GREEN}✓${NC} Vault exists: $vault_files markdown files"
    else
        echo -e "  ${YELLOW}○${NC} Vault not created (run 'init' to create)"
    fi
    
    # Check dependencies
    echo ""
    echo -e "${CYAN}=== Dependencies ===${NC}"
    
    for dep in python3 curl jq git; do
        if command -v "$dep" &> /dev/null; then
            local version=$("$dep" --version 2>&1 | head -1 || echo "unknown")
            echo -e "  ${GREEN}✓${NC} $dep: $version"
        else
            echo -e "  ${RED}✗${NC} $dep: Not installed"
        fi
    done
    
    echo ""
}

# =============================================================================
# Help
# =============================================================================

cmd_help() {
    echo -e "${PURPLE}"
    echo "╔═══════════════════════════════════════════════════════════════════╗"
    echo "║           Sovereignty Analysis Framework - Help                    ║"
    echo "╚═══════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    cat << HELP
Usage: $0 <command> [options]

Commands:
  init              Initialize the analysis environment
  capture <url>     Set up HAR capture for a target URL
  analyze-har <har> Analyze a HAR file for security issues
  compare <a> <b>   Compare original and sovereign HAR files
  report [type]     Generate analysis report
  sync              Sync analysis to Obsidian vault
  git <op> [args]   Git operations (status, commit, diff, log)
  notify <msg>      Send Discord notification
  status            Show framework status
  help              Show this help message

Examples:
  $0 init
  $0 capture https://app.example.com
  $0 analyze-har captures/app/capture.har
  $0 compare original.har sovereign.har
  $0 report security
  $0 sync
  $0 git commit "Analysis complete"
  $0 notify "Analysis finished"

Environment Variables:
  DISCORD_WEBHOOK   Discord webhook URL for notifications
  OBSIDIAN_VAULT    Custom Obsidian vault path (default: ~/obsidian/vault)

For detailed methodology, see:
  REVERSE_ENGINEERING_SOVEREIGNTY_METHODOLOGY.md

For configuration options, see:
  sovereignty_analysis_config.yaml
HELP
}

# =============================================================================
# Main Entry Point
# =============================================================================

main() {
    local command="${1:-help}"
    shift || true
    
    case "$command" in
        init)
            cmd_init "$@"
            ;;
        capture)
            cmd_capture "$@"
            ;;
        analyze-har|analyze)
            cmd_analyze_har "$@"
            ;;
        compare)
            cmd_compare "$@"
            ;;
        report)
            cmd_report "$@"
            ;;
        sync)
            cmd_sync "$@"
            ;;
        git)
            cmd_git "$@"
            ;;
        notify)
            cmd_notify "$@"
            ;;
        status)
            cmd_status "$@"
            ;;
        help|--help|-h)
            cmd_help "$@"
            ;;
        *)
            error "Unknown command: $command"
            echo "Run '$0 help' for usage information"
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
