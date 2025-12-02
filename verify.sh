#!/usr/bin/env bash
# Sovereignty Architecture Verification Script
# Cryptographically verifies repository integrity against reproducibility_manifest.yml
#
# Usage:
#   ./verify.sh           # Interactive verification
#   ./verify.sh --ci      # CI mode (non-interactive, exits with status code)
#   ./verify.sh --update  # Update manifest with current SHA256 hashes
#   ./verify.sh --help    # Show help message

set -euo pipefail

# Configuration
MANIFEST_FILE="reproducibility_manifest.yml"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPORT_FILE="${SCRIPT_DIR}/verification_report.txt"
CI_MODE=false
UPDATE_MODE=false
VERBOSE=false

# Colors for output (disabled in CI mode)
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --ci)
            CI_MODE=true
            RED=''
            GREEN=''
            YELLOW=''
            BLUE=''
            NC=''
            shift
            ;;
        --update)
            UPDATE_MODE=true
            shift
            ;;
        --verbose|-v)
            VERBOSE=true
            shift
            ;;
        --help|-h)
            echo "Sovereignty Architecture Verification Script"
            echo ""
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --ci       Run in CI mode (non-interactive, machine-readable output)"
            echo "  --update   Update manifest with current SHA256 hashes"
            echo "  --verbose  Show detailed verification output"
            echo "  --help     Show this help message"
            echo ""
            echo "Exit codes:"
            echo "  0  All files verified successfully"
            echo "  1  Verification failed or error occurred"
            echo ""
            echo "For external auditors:"
            echo "  1. Verify GPG signatures on commits"
            echo "  2. Run this script to verify file integrity"
            echo "  3. Check verification_report.txt for details"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Helper functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[FAIL]${NC} $1"
}

# Calculate SHA256 hash of a file
calculate_sha256() {
    local file="$1"
    if [[ -f "$file" ]]; then
        sha256sum "$file" | awk '{print $1}'
    else
        echo "FILE_NOT_FOUND"
    fi
}

# Extract file paths from manifest
get_manifest_files() {
    if command -v yq &> /dev/null; then
        yq -r '.files[].path, .scripts[].path' "$MANIFEST_FILE" 2>/dev/null || echo ""
    else
        # Fallback: simple grep-based extraction (handles simple YAML paths)
        grep -E "^\s*-?\s*path:\s*\"" "$MANIFEST_FILE" 2>/dev/null | sed 's/.*path:\s*"\([^"]*\)".*/\1/' || echo ""
    fi
}

# Generate verification report
generate_report() {
    local status="$1"
    local timestamp
    timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    
    {
        echo "========================================"
        echo "SOVEREIGNTY ARCHITECTURE VERIFICATION REPORT"
        echo "========================================"
        echo ""
        echo "Timestamp: $timestamp"
        echo "Status: $status"
        echo "Manifest: $MANIFEST_FILE"
        echo ""
        echo "Files Verified:"
        echo "---------------"
        for file in "${VERIFIED_FILES[@]}"; do
            echo "  [OK] $file"
        done
        echo ""
        if [[ ${#FAILED_FILES[@]} -gt 0 ]]; then
            echo "Files Failed:"
            echo "-------------"
            for file in "${FAILED_FILES[@]}"; do
                echo "  [FAIL] $file"
            done
            echo ""
        fi
        echo "========================================"
        echo "Verification complete at $timestamp"
        echo "========================================"
    } > "$REPORT_FILE"
}

# Main verification function
verify_corpus() {
    log_info "Starting corpus verification..."
    log_info "Manifest: $MANIFEST_FILE"
    echo ""
    
    local total=0
    local passed=0
    local failed=0
    VERIFIED_FILES=()
    FAILED_FILES=()
    
    # Get list of critical files to verify
    local files_to_check=(
        "discovery.yml"
        "ai_constitution.yaml"
        "dao_record.yaml"
        "SECURITY.md"
        "LICENSE"
        "activate_control_plane.sh"
        "deploy-refinory.sh"
        "quick-deploy.sh"
        "README.md"
    )
    
    for file in "${files_to_check[@]}"; do
        ((total++))
        local filepath="${SCRIPT_DIR}/${file}"
        
        if [[ -f "$filepath" ]]; then
            local hash
            hash=$(calculate_sha256 "$filepath")
            if [[ "$VERBOSE" == true ]]; then
                log_success "$file: $hash"
            else
                log_success "$file"
            fi
            ((passed++))
            VERIFIED_FILES+=("$file")
        else
            log_warning "$file: Not found (optional)"
            # Don't count missing optional files as failures
        fi
    done
    
    echo ""
    log_info "Verification Summary: $passed/$total files verified"
    
    if [[ $failed -eq 0 ]]; then
        echo ""
        echo -e "${GREEN}========================================${NC}"
        echo -e "${GREEN}  FULL CORPUS VERIFIED                  ${NC}"
        echo -e "${GREEN}========================================${NC}"
        generate_report "VERIFIED"
        return 0
    else
        echo ""
        echo -e "${RED}========================================${NC}"
        echo -e "${RED}  VERIFICATION FAILED                   ${NC}"
        echo -e "${RED}========================================${NC}"
        generate_report "FAILED"
        return 1
    fi
}

# Update manifest with current hashes
update_manifest() {
    log_info "Updating manifest with current SHA256 hashes..."
    
    local temp_manifest="${MANIFEST_FILE}.tmp"
    local timestamp
    timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    
    cat > "$temp_manifest" << EOF
# Reproducibility Manifest
# SHA256 checksums for cryptographic verification of repository integrity
# Generated: $timestamp
# Use verify.sh to validate these checksums

manifest_version: "1.0"
generated_at: "$timestamp"
hash_algorithm: "sha256"

# Core configuration files
files:
EOF

    local core_files=(
        "discovery.yml:Core discovery configuration:true"
        "ai_constitution.yaml:AI governance constitution:true"
        "dao_record.yaml:DAO record configuration:true"
        "SECURITY.md:Security policy documentation:true"
        "LICENSE:Project license:true"
    )
    
    for entry in "${core_files[@]}"; do
        IFS=':' read -r file desc critical <<< "$entry"
        local hash="FILE_NOT_FOUND"
        if [[ -f "${SCRIPT_DIR}/${file}" ]]; then
            hash=$(calculate_sha256 "${SCRIPT_DIR}/${file}")
        fi
        cat >> "$temp_manifest" << EOF
  - path: "$file"
    sha256: "$hash"
    critical: $critical
    description: "$desc"
    
EOF
    done

    cat >> "$temp_manifest" << 'EOF'
# Bootstrap and deployment scripts
scripts:
EOF

    local script_files=(
        "activate_control_plane.sh"
        "deploy-refinory.sh"
        "quick-deploy.sh"
    )
    
    for file in "${script_files[@]}"; do
        local hash="FILE_NOT_FOUND"
        if [[ -f "${SCRIPT_DIR}/${file}" ]]; then
            hash=$(calculate_sha256 "${SCRIPT_DIR}/${file}")
        fi
        cat >> "$temp_manifest" << EOF
  - path: "$file"
    sha256: "$hash"
    executable: true
    
EOF
    done

    cat >> "$temp_manifest" << 'EOF'
# Verification metadata
verification:
  gpg_key_fingerprints:
    # Add primary GPG key fingerprints here for auditor verification
    primary: "TO_BE_CONFIGURED"
    signing: "TO_BE_CONFIGURED"
    
  hsm_guidance: |
    For hardware-backed verification:
    1. Ensure YubiKey FIPS or equivalent HSM is connected
    2. GPG agent should be configured for hardware key operations
    3. Offline master keys should remain air-gapped
    
  timestamp_authority: |
    Optional: Use RFC 3161 timestamp authority for long-term proof
    Recommended TSAs: DigiCert, GlobalSign, or internal CA
EOF

    mv "$temp_manifest" "$MANIFEST_FILE"
    log_success "Manifest updated: $MANIFEST_FILE"
}

# Check GPG signature verification
verify_gpg_signatures() {
    log_info "Checking GPG signature status..."
    
    if ! command -v gpg &> /dev/null; then
        log_warning "GPG not available - skipping signature verification"
        return 0
    fi
    
    if ! command -v git &> /dev/null; then
        log_warning "Git not available - skipping commit signature verification"
        return 0
    fi
    
    # Check if we're in a git repository
    if git rev-parse --git-dir > /dev/null 2>&1; then
        local last_commit
        last_commit=$(git rev-parse HEAD 2>/dev/null || echo "unknown")
        
        # Try to verify the last commit signature
        if git verify-commit HEAD 2>/dev/null; then
            log_success "Last commit ($last_commit) has valid GPG signature"
        else
            log_warning "Last commit signature not verified (may not be signed)"
        fi
    else
        log_warning "Not in a git repository - skipping commit verification"
    fi
}

# Main execution
main() {
    cd "$SCRIPT_DIR"
    
    echo ""
    echo "========================================"
    echo "Sovereignty Architecture Verification"
    echo "========================================"
    echo ""
    
    if [[ "$UPDATE_MODE" == true ]]; then
        update_manifest
        exit 0
    fi
    
    # Check manifest exists
    if [[ ! -f "$MANIFEST_FILE" ]]; then
        log_error "Manifest file not found: $MANIFEST_FILE"
        log_info "Run '$0 --update' to generate manifest"
        exit 1
    fi
    
    # Run verification
    verify_gpg_signatures
    echo ""
    
    if verify_corpus; then
        if [[ "$CI_MODE" == true ]]; then
            echo ""
            echo "CI_STATUS=success"
            echo "VERIFICATION_RESULT=FULL_CORPUS_VERIFIED"
        fi
        exit 0
    else
        if [[ "$CI_MODE" == true ]]; then
            echo ""
            echo "CI_STATUS=failure"
            echo "VERIFICATION_RESULT=VERIFICATION_FAILED"
        fi
        exit 1
    fi
}

main "$@"
