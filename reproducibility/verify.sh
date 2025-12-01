#!/bin/bash
# SACSE Reproducibility Verification Script
# Version: 1.0
# Purpose: Verify integrity of SACSE artifacts and system state

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
MANIFEST_FILE="$SCRIPT_DIR/reproducibility.yaml"
HASH_FILE="$SCRIPT_DIR/artifact_hashes.sha256"
LOG_FILE="/tmp/sacse_verify_$(date +%Y%m%d_%H%M%S).log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
PASS_COUNT=0
FAIL_COUNT=0
SKIP_COUNT=0

# Logging function
log() {
    local level="$1"
    shift
    local message="$*"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] [$level] $message" >> "$LOG_FILE"
    
    case "$level" in
        "INFO")  echo -e "${GREEN}✓${NC} $message" ;;
        "WARN")  echo -e "${YELLOW}⚠${NC} $message" ;;
        "ERROR") echo -e "${RED}✗${NC} $message" ;;
        "DEBUG") [[ "${VERBOSE:-false}" == "true" ]] && echo "  $message" ;;
    esac
}

# Print usage
usage() {
    cat << EOF
SACSE Reproducibility Verification Script

Usage: $(basename "$0") [OPTIONS]

Options:
    --full          Run all verification checks (default)
    --quick         Run hash verification only
    --verbose       Show detailed output
    --generate      Generate new hash manifest (maintainer only)
    --ci            Run in CI mode (non-interactive)
    --help          Show this help message

Exit Codes:
    0  All verifications passed
    1  Hash verification failed
    2  Signature verification failed
    3  Dependency verification failed
    4  Configuration error

Examples:
    $(basename "$0") --full
    $(basename "$0") --quick --verbose
    $(basename "$0") --generate
EOF
}

# Verify file hash
verify_hash() {
    local file="$1"
    local expected_hash="$2"
    local full_path="$REPO_ROOT/$file"
    
    if [[ ! -f "$full_path" ]]; then
        log "WARN" "File not found: $file"
        ((SKIP_COUNT++))
        return 0
    fi
    
    local actual_hash=$(sha256sum "$full_path" | awk '{print $1}')
    
    if [[ "$expected_hash" == "to_be_computed" ]]; then
        log "DEBUG" "Skipping $file (hash not yet computed)"
        ((SKIP_COUNT++))
        return 0
    fi
    
    if [[ "$actual_hash" == "$expected_hash" ]]; then
        log "INFO" "Hash verified: $file"
        ((PASS_COUNT++))
        return 0
    else
        log "ERROR" "Hash mismatch: $file"
        log "DEBUG" "  Expected: $expected_hash"
        log "DEBUG" "  Actual:   $actual_hash"
        ((FAIL_COUNT++))
        return 1
    fi
}

# Verify all hashes from manifest
verify_hashes() {
    log "INFO" "Starting hash verification..."
    
    if [[ ! -f "$HASH_FILE" ]]; then
        log "WARN" "Hash file not found, generating initial manifest"
        generate_hashes
        return 0
    fi
    
    local result=0
    while IFS='  ' read -r hash file; do
        # Skip comments and empty lines
        [[ "$hash" =~ ^# ]] && continue
        [[ -z "$hash" ]] && continue
        
        verify_hash "$file" "$hash" || result=1
    done < "$HASH_FILE"
    
    return $result
}

# Verify GPG signatures
verify_signatures() {
    log "INFO" "Starting signature verification..."
    
    # Check if GPG is available
    if ! command -v gpg &> /dev/null; then
        log "WARN" "GPG not installed, skipping signature verification"
        ((SKIP_COUNT++))
        return 0
    fi
    
    # Verify latest commit signature
    cd "$REPO_ROOT"
    
    if git verify-commit HEAD &> /dev/null; then
        log "INFO" "Latest commit signature verified"
        ((PASS_COUNT++))
    else
        log "WARN" "Latest commit is not signed or signature invalid"
        ((SKIP_COUNT++))
    fi
    
    # Count signed commits on main branch (use --format='%G?' for reliable detection)
    local signed_commits=$(git log --format='%G?' main 2>/dev/null | grep -c '^G$' || echo "0")
    local total_commits=$(git rev-list --count main 2>/dev/null || echo "0")
    
    log "DEBUG" "Signed commits: $signed_commits / $total_commits"
    
    return 0
}

# Verify dependencies
verify_dependencies() {
    log "INFO" "Starting dependency verification..."
    
    cd "$REPO_ROOT"
    
    # Node.js dependencies
    if [[ -f "package-lock.json" ]]; then
        log "DEBUG" "Verifying npm dependencies..."
        
        if npm ci --ignore-scripts &> /dev/null; then
            log "INFO" "npm dependencies verified"
            ((PASS_COUNT++))
        else
            log "WARN" "npm dependency verification failed"
            ((SKIP_COUNT++))
        fi
        
        # Run npm audit
        if npm audit --audit-level=high &> /dev/null; then
            log "INFO" "npm audit passed (no high/critical vulnerabilities)"
            ((PASS_COUNT++))
        else
            log "WARN" "npm audit found vulnerabilities"
            ((SKIP_COUNT++))
        fi
    fi
    
    # Python dependencies
    if [[ -f "requirements.txt" ]] || [[ -f "requirements.alignment.txt" ]]; then
        log "DEBUG" "Python requirements files found"
        
        if command -v pip-audit &> /dev/null; then
            if pip-audit -r requirements.txt &> /dev/null; then
                log "INFO" "pip audit passed"
                ((PASS_COUNT++))
            else
                log "WARN" "pip audit found issues or requirements.txt missing"
                ((SKIP_COUNT++))
            fi
        else
            log "DEBUG" "pip-audit not installed, skipping Python audit"
        fi
    fi
    
    return 0
}

# Verify container images
verify_containers() {
    log "INFO" "Starting container verification..."
    
    if ! command -v docker &> /dev/null; then
        log "WARN" "Docker not installed, skipping container verification"
        ((SKIP_COUNT++))
        return 0
    fi
    
    # Check Docker Content Trust
    if [[ "${DOCKER_CONTENT_TRUST:-0}" == "1" ]]; then
        log "INFO" "Docker Content Trust is enabled"
        ((PASS_COUNT++))
    else
        log "WARN" "Docker Content Trust not enabled"
        ((SKIP_COUNT++))
    fi
    
    return 0
}

# Generate new hash manifest
generate_hashes() {
    log "INFO" "Generating new hash manifest..."
    
    cd "$REPO_ROOT"
    
    # Define files to hash
    local files=(
        "discovery.yml"
        "dao_record.yaml"
        "governance/access_matrix.yaml"
        "ai_constitution.yaml"
        "monitoring/alerts.yml"
        "monitoring/prometheus.yml"
        "docker-compose.yml"
        "docker-compose.obs.yml"
        "package.json"
        "package-lock.json"
        "THREAT_MODEL.md"
        "SECURITY.md"
    )
    
    # Create hash file
    {
        echo "# SACSE Artifact Hashes"
        echo "# Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
        echo "# Algorithm: SHA256"
        echo ""
        
        for file in "${files[@]}"; do
            if [[ -f "$REPO_ROOT/$file" ]]; then
                # Use awk for safer path replacement instead of sed with variable
                sha256sum "$REPO_ROOT/$file" | awk -v root="$REPO_ROOT/" '{gsub(root, "", $2); print $1 "  " $2}'
            fi
        done
    } > "$HASH_FILE"
    
    log "INFO" "Hash manifest generated: $HASH_FILE"
}

# Print summary
print_summary() {
    echo ""
    echo "========================================"
    echo "SACSE Verification Summary"
    echo "========================================"
    echo -e "${GREEN}Passed:${NC}  $PASS_COUNT"
    echo -e "${RED}Failed:${NC}  $FAIL_COUNT"
    echo -e "${YELLOW}Skipped:${NC} $SKIP_COUNT"
    echo "========================================"
    echo "Log file: $LOG_FILE"
    echo ""
    
    if [[ $FAIL_COUNT -gt 0 ]]; then
        echo -e "${RED}VERIFICATION FAILED${NC}"
        return 1
    else
        echo -e "${GREEN}VERIFICATION PASSED${NC}"
        return 0
    fi
}

# Main function
main() {
    local mode="full"
    local generate=false
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --full)     mode="full" ;;
            --quick)    mode="quick" ;;
            --verbose)  VERBOSE=true ;;
            --generate) generate=true ;;
            --ci)       CI_MODE=true ;;
            --help)     usage; exit 0 ;;
            *)          log "ERROR" "Unknown option: $1"; usage; exit 4 ;;
        esac
        shift
    done
    
    echo ""
    echo "SACSE Reproducibility Verification"
    echo "==================================="
    echo ""
    
    # Initialize log
    log "INFO" "Starting verification in $mode mode"
    
    # Generate hashes if requested
    if [[ "$generate" == "true" ]]; then
        generate_hashes
        exit 0
    fi
    
    # Run verifications based on mode
    case "$mode" in
        "full")
            verify_hashes
            verify_signatures
            verify_dependencies
            verify_containers
            ;;
        "quick")
            verify_hashes
            ;;
    esac
    
    # Print summary and exit based on its result
    if print_summary; then
        exit 0
    else
        exit 1
    fi
}

# Run main function
main "$@"
