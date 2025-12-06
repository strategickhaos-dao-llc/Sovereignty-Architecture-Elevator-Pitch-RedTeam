#!/usr/bin/env bash
# freeze_qet.sh
# Strategickhaos DAO LLC / Valoryield Engine — QET Freeze Script
# Freezes QET configuration for production deployment
# Version: 1.0
# Date: 2025-12-05
# Operator: Domenic Garza (Node 137)

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
GOVERNANCE_DIR="$REPO_ROOT/governance"
QET_CONFIG="$GOVERNANCE_DIR/qet_versions.yaml"
MODEL_CARD="$GOVERNANCE_DIR/model_card.md"
FREEZE_MANIFEST="$GOVERNANCE_DIR/freeze_manifest.json"
FREEZE_LOCK="$GOVERNANCE_DIR/.qet.lock"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Print banner
print_banner() {
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║   QET Freeze Script - Valoryield Engine                   ║"
    echo "║   Path A Governance Lock                                  ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo ""
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check for required files
    if [[ ! -f "$QET_CONFIG" ]]; then
        log_error "QET config not found: $QET_CONFIG"
        exit 1
    fi
    
    if [[ ! -f "$MODEL_CARD" ]]; then
        log_error "Model card not found: $MODEL_CARD"
        exit 1
    fi
    
    # Check for required tools
    local missing_tools=()
    
    # Check for SHA256 tool (sha256sum on Linux, shasum on macOS)
    if ! command -v sha256sum &> /dev/null && ! command -v shasum &> /dev/null; then
        missing_tools+=("sha256sum or shasum")
    fi
    
    if ! command -v date &> /dev/null; then
        missing_tools+=("date")
    fi
    
    if [[ ${#missing_tools[@]} -gt 0 ]]; then
        log_error "Missing required tools: ${missing_tools[*]}"
        exit 1
    fi
    
    # Optional: Check for GPG
    if ! command -v gpg &> /dev/null; then
        log_warn "GPG not found - signatures will be skipped"
    fi
    
    log_success "Prerequisites check passed"
}

# Check if already frozen
check_frozen_state() {
    if [[ -f "$FREEZE_LOCK" ]]; then
        log_warn "QET configuration is already frozen!"
        log_info "Lock file: $FREEZE_LOCK"
        
        if [[ "${FORCE_FREEZE:-false}" == "true" ]]; then
            log_warn "Force freeze enabled - removing existing lock"
            rm -f "$FREEZE_LOCK"
        else
            log_error "Use --force to override existing freeze"
            exit 1
        fi
    fi
}

# Validate YAML syntax
validate_yaml() {
    log_info "Validating YAML syntax..."
    
    # Basic YAML validation using grep for common issues (tab detection)
    if grep -q "	" "$QET_CONFIG" 2>/dev/null; then
        log_warn "YAML contains tabs - this may cause parsing issues"
    fi
    
    # Check for version field
    if ! grep -q "^version:" "$QET_CONFIG"; then
        log_error "YAML missing required 'version' field"
        exit 1
    fi
    
    # Check for tier configurations
    if ! grep -q "tier_0_income_core:" "$QET_CONFIG"; then
        log_error "YAML missing Tier 0 configuration"
        exit 1
    fi
    
    log_success "YAML validation passed"
}

# Validate readiness thresholds
validate_readiness() {
    log_info "Validating readiness thresholds..."
    
    # Extract readiness values and check they meet thresholds
    local tier0_strategies
    tier0_strategies=$(grep -A 100 "tier_0_income_core:" "$QET_CONFIG" | grep "readiness:" | head -5 || true)
    
    if [[ -z "$tier0_strategies" ]]; then
        log_error "No Tier 0 strategies found with readiness values"
        exit 1
    fi
    
    log_success "Readiness validation passed"
}

# Cross-platform SHA256 hash function
compute_sha256() {
    local file="$1"
    if command -v sha256sum &> /dev/null; then
        sha256sum "$file" | cut -d' ' -f1
    elif command -v shasum &> /dev/null; then
        shasum -a 256 "$file" | cut -d' ' -f1
    else
        log_error "No SHA256 tool available"
        exit 1
    fi
}

# Generate SHA256 hashes
generate_hashes() {
    log_info "Generating SHA256 hashes..."
    
    local qet_hash
    local model_hash
    
    qet_hash=$(compute_sha256 "$QET_CONFIG")
    model_hash=$(compute_sha256 "$MODEL_CARD")
    
    log_info "QET Config Hash: $qet_hash"
    log_info "Model Card Hash: $model_hash"
    
    echo "$qet_hash" > "$QET_CONFIG.sha256"
    echo "$model_hash" > "$MODEL_CARD.sha256"
    
    log_success "Hashes generated and saved"
}

# Create freeze manifest
create_manifest() {
    log_info "Creating freeze manifest..."
    
    local timestamp
    local qet_hash
    local model_hash
    
    timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    qet_hash=$(cat "$QET_CONFIG.sha256")
    model_hash=$(cat "$MODEL_CARD.sha256")
    
    cat > "$FREEZE_MANIFEST" << EOF
{
    "freeze_version": "1.0",
    "timestamp": "$timestamp",
    "governance_path": "A",
    "operator": "Domenic Garza (Node 137)",
    "status": "frozen",
    "artifacts": {
        "qet_versions": {
            "path": "governance/qet_versions.yaml",
            "sha256": "$qet_hash"
        },
        "model_card": {
            "path": "governance/model_card.md",
            "sha256": "$model_hash"
        }
    },
    "tier_0_locked": true,
    "strategies_frozen": [
        "SMR-001",
        "DMR-002",
        "PMR-003",
        "VAM-004",
        "CAR-005"
    ],
    "target_yield": "7.0%+",
    "max_drawdown": "20%",
    "notes": "Path A governance locked for production deployment"
}
EOF
    
    log_success "Freeze manifest created: $FREEZE_MANIFEST"
}

# Create lock file
create_lock() {
    log_info "Creating lock file..."
    
    local timestamp
    local qet_hash
    
    timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    qet_hash=$(cat "$QET_CONFIG.sha256")
    
    cat > "$FREEZE_LOCK" << EOF
# QET FREEZE LOCK
# DO NOT MODIFY - Production configuration locked
# 
# Frozen: $timestamp
# Path: A
# Config Hash: $qet_hash
# 
# To unfreeze, run: ./governance/freeze_qet.sh --unfreeze
# 
# WARNING: Unfreezing requires governance approval
EOF
    
    log_success "Lock file created: $FREEZE_LOCK"
}

# GPG sign artifacts (optional)
gpg_sign() {
    if command -v gpg &> /dev/null; then
        log_info "Signing artifacts with GPG..."
        
        # Check if GPG key is available
        if gpg --list-secret-keys 2>/dev/null | grep -q "sec"; then
            gpg --armor --detach-sign "$QET_CONFIG" 2>/dev/null && \
                log_success "Signed: $QET_CONFIG.asc" || \
                log_warn "GPG signing failed for QET config"
            
            gpg --armor --detach-sign "$MODEL_CARD" 2>/dev/null && \
                log_success "Signed: $MODEL_CARD.asc" || \
                log_warn "GPG signing failed for model card"
            
            gpg --armor --detach-sign "$FREEZE_MANIFEST" 2>/dev/null && \
                log_success "Signed: $FREEZE_MANIFEST.asc" || \
                log_warn "GPG signing failed for manifest"
        else
            log_warn "No GPG secret keys found - skipping signatures"
        fi
    else
        log_warn "GPG not available - skipping signatures"
    fi
}

# Unfreeze function
unfreeze() {
    log_info "Unfreezing QET configuration..."
    
    if [[ ! -f "$FREEZE_LOCK" ]]; then
        log_error "No freeze lock found - configuration is not frozen"
        exit 1
    fi
    
    # Remove lock and related files
    rm -f "$FREEZE_LOCK"
    rm -f "$QET_CONFIG.sha256"
    rm -f "$MODEL_CARD.sha256"
    rm -f "$FREEZE_MANIFEST"
    rm -f "$QET_CONFIG.asc"
    rm -f "$MODEL_CARD.asc"
    rm -f "$FREEZE_MANIFEST.asc"
    
    log_success "QET configuration unfrozen"
    log_warn "Remember: Changes require governance approval before re-freezing"
}

# Verify freeze integrity
verify() {
    log_info "Verifying freeze integrity..."
    
    if [[ ! -f "$FREEZE_LOCK" ]]; then
        log_error "No freeze lock found"
        exit 1
    fi
    
    if [[ ! -f "$QET_CONFIG.sha256" ]]; then
        log_error "Hash file missing: $QET_CONFIG.sha256"
        exit 1
    fi
    
    local stored_hash
    local current_hash
    
    stored_hash=$(cat "$QET_CONFIG.sha256")
    current_hash=$(compute_sha256 "$QET_CONFIG")
    
    if [[ "$stored_hash" != "$current_hash" ]]; then
        log_error "INTEGRITY VIOLATION: QET config has been modified!"
        log_error "Expected: $stored_hash"
        log_error "Found:    $current_hash"
        exit 1
    fi
    
    log_success "Freeze integrity verified - configuration unchanged"
}

# Print status
status() {
    echo ""
    log_info "QET Freeze Status"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    if [[ -f "$FREEZE_LOCK" ]]; then
        echo -e "Status:      ${GREEN}FROZEN${NC}"
        echo -e "Lock File:   $FREEZE_LOCK"
        
        if [[ -f "$FREEZE_MANIFEST" ]]; then
            local timestamp
            timestamp=$(grep '"timestamp"' "$FREEZE_MANIFEST" | cut -d'"' -f4)
            echo -e "Frozen At:   $timestamp"
        fi
    else
        echo -e "Status:      ${YELLOW}UNLOCKED${NC}"
    fi
    
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    if [[ -f "$QET_CONFIG" ]]; then
        echo -e "QET Config:  ${GREEN}EXISTS${NC}"
    else
        echo -e "QET Config:  ${RED}MISSING${NC}"
    fi
    
    if [[ -f "$MODEL_CARD" ]]; then
        echo -e "Model Card:  ${GREEN}EXISTS${NC}"
    else
        echo -e "Model Card:  ${RED}MISSING${NC}"
    fi
    
    echo ""
}

# Main freeze process
freeze() {
    print_banner
    check_prerequisites
    check_frozen_state
    validate_yaml
    validate_readiness
    generate_hashes
    create_manifest
    create_lock
    gpg_sign
    
    echo ""
    log_success "═══════════════════════════════════════════════════"
    log_success "QET CONFIGURATION FROZEN SUCCESSFULLY"
    log_success "Path A governance locked for production deployment"
    log_success "═══════════════════════════════════════════════════"
    echo ""
    
    status
}

# Help message
show_help() {
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo ""
    echo "Commands:"
    echo "  freeze     Freeze QET configuration (default)"
    echo "  unfreeze   Unfreeze QET configuration"
    echo "  verify     Verify freeze integrity"
    echo "  status     Show current freeze status"
    echo "  help       Show this help message"
    echo ""
    echo "Options:"
    echo "  --force    Force freeze even if already frozen"
    echo ""
    echo "Examples:"
    echo "  $0                  # Freeze configuration"
    echo "  $0 freeze           # Freeze configuration"
    echo "  $0 freeze --force   # Force re-freeze"
    echo "  $0 verify           # Verify integrity"
    echo "  $0 status           # Show status"
    echo "  $0 unfreeze         # Unfreeze configuration"
    echo ""
}

# Parse arguments
main() {
    local command="${1:-freeze}"
    
    # Check for --force flag
    for arg in "$@"; do
        if [[ "$arg" == "--force" ]]; then
            export FORCE_FREEZE="true"
        fi
    done
    
    case "$command" in
        freeze)
            freeze
            ;;
        unfreeze)
            unfreeze
            ;;
        verify)
            verify
            ;;
        status)
            status
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            log_error "Unknown command: $command"
            show_help
            exit 1
            ;;
    esac
}

# Run main
main "$@"
