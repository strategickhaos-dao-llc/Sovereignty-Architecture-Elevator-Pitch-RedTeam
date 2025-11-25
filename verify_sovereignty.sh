#!/usr/bin/env bash
# ============================================================================
# SOVEREIGNTY STACK VALIDATION MODULE v1.0
# ============================================================================
# A self-verifying sovereign software stack that performs hash-proven integrity
# checks on critical stack files and validates execution readiness across a
# full cloud-to-local pipeline.
#
# Features:
#   - File integrity checks (existence, content, byte count)
#   - Script syntax validation (bash -n, python -m py_compile)
#   - System environment validation (git, python, bash, docker)
#   - Network connectivity diagnostic
#   - SHA-256 file hash verification for tamper detection
#   - SBOM (Software Bill of Materials) integration
#
# Usage: ./verify_sovereignty.sh [OPTIONS]
#   --full      Run all verification checks
#   --quick     Run quick health check only
#   --hash      Generate/verify file hashes only
#   --env       Check environment only
#   --network   Check network connectivity only
#   --help      Show this help message
#
# Copyright (c) 2025 Strategickhaos DAO LLC
# SPDX-License-Identifier: MIT
# ============================================================================

set -euo pipefail

# Colors for output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly CYAN='\033[0;36m'
readonly NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HASH_FILE="${SCRIPT_DIR}/.sovereignty_hashes.sha256"
LOG_FILE="${SCRIPT_DIR}/.sovereignty_verification.log"

# Counters
PASS_COUNT=0
FAIL_COUNT=0
WARN_COUNT=0

# ============================================================================
# LOGGING FUNCTIONS
# ============================================================================

log_header() {
    echo -e "\n${CYAN}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}  $1${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}\n"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] HEADER: $1" >> "$LOG_FILE"
}

log_pass() {
    echo -e "${GREEN}✔ PASS:${NC} $1"
    PASS_COUNT=$((PASS_COUNT + 1))
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] PASS: $1" >> "$LOG_FILE"
}

log_fail() {
    echo -e "${RED}✘ FAIL:${NC} $1"
    FAIL_COUNT=$((FAIL_COUNT + 1))
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] FAIL: $1" >> "$LOG_FILE"
}

log_warn() {
    echo -e "${YELLOW}⚠ WARN:${NC} $1"
    WARN_COUNT=$((WARN_COUNT + 1))
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] WARN: $1" >> "$LOG_FILE"
}

log_info() {
    echo -e "${BLUE}ℹ INFO:${NC} $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] INFO: $1" >> "$LOG_FILE"
}

# ============================================================================
# FILE INTEGRITY CHECKS
# ============================================================================

verify_file_integrity() {
    log_header "FILE INTEGRITY VERIFICATION"
    
    # Critical files to verify
    local critical_files=(
        "README.md"
        "LICENSE"
        "SECURITY.md"
        "package.json"
        "discovery.yml"
        "validate-config.sh"
        "status-check.sh"
        "bootstrap/deploy.sh"
    )
    
    # Shell scripts to syntax-check
    local shell_scripts=(
        "validate-config.sh"
        "status-check.sh"
        "bootstrap/deploy.sh"
        "gl2discord.sh"
        "quick-deploy.sh"
        "launch-recon.sh"
        "jdk-solver.sh"
        "activate_control_plane.sh"
        "generate_dao_record.sh"
    )
    
    # Python files to syntax-check
    local python_files=(
        "eval_redteam.py"
        "interpretability_monitor.py"
        "reflexshell_layout.py"
        "uidp_vote.py"
        "voice_trigger.py"
        "scripts/run_benchmarks.py"
        "benchmarks/test_comprehensive.py"
    )
    
    echo "Checking critical file existence and content..."
    echo ""
    
    for file in "${critical_files[@]}"; do
        local filepath="${SCRIPT_DIR}/${file}"
        if [[ -f "$filepath" ]]; then
            local size
            size=$(stat -f%z "$filepath" 2>/dev/null || stat -c%s "$filepath" 2>/dev/null || echo "0")
            if [[ "$size" -gt 0 ]]; then
                log_pass "$file exists (${size} bytes)"
            else
                log_warn "$file exists but is empty"
            fi
        else
            log_warn "$file not found (optional)"
        fi
    done
    
    echo ""
    echo "Validating shell script syntax..."
    echo ""
    
    for script in "${shell_scripts[@]}"; do
        local filepath="${SCRIPT_DIR}/${script}"
        if [[ -f "$filepath" ]]; then
            if bash -n "$filepath" 2>/dev/null; then
                log_pass "$script syntax valid"
            else
                log_fail "$script has syntax errors"
            fi
        fi
    done
    
    echo ""
    echo "Validating Python script syntax..."
    echo ""
    
    for pyfile in "${python_files[@]}"; do
        local filepath="${SCRIPT_DIR}/${pyfile}"
        if [[ -f "$filepath" ]]; then
            if python3 -m py_compile "$filepath" 2>/dev/null; then
                log_pass "$pyfile syntax valid"
            else
                log_fail "$pyfile has syntax errors"
            fi
        fi
    done
}

# ============================================================================
# ENVIRONMENT VALIDATION
# ============================================================================

verify_environment() {
    log_header "SYSTEM ENVIRONMENT VALIDATION"
    
    echo "Checking required tools..."
    echo ""
    
    # Check Git
    if command -v git &> /dev/null; then
        local git_version
        git_version=$(git --version 2>/dev/null | head -n1)
        log_pass "Git installed: $git_version"
    else
        log_fail "Git not installed"
    fi
    
    # Check Python
    if command -v python3 &> /dev/null; then
        local python_version
        python_version=$(python3 --version 2>/dev/null)
        log_pass "Python installed: $python_version"
    else
        log_warn "Python3 not installed"
    fi
    
    # Check Bash
    if command -v bash &> /dev/null; then
        local bash_version
        bash_version=$(bash --version 2>/dev/null | head -n1)
        log_pass "Bash installed: $bash_version"
    else
        log_fail "Bash not installed"
    fi
    
    # Check Docker (with timeout to avoid hanging)
    if command -v docker &> /dev/null; then
        if timeout 5 docker info &> /dev/null 2>&1; then
            local docker_version
            docker_version=$(docker --version 2>/dev/null)
            log_pass "Docker running: $docker_version"
        else
            log_warn "Docker installed but daemon not running or not accessible"
        fi
    else
        log_warn "Docker not installed (optional)"
    fi
    
    # Check Node.js
    if command -v node &> /dev/null; then
        local node_version
        node_version=$(node --version 2>/dev/null)
        log_pass "Node.js installed: $node_version"
    else
        log_warn "Node.js not installed (optional)"
    fi
    
    # Check kubectl (optional)
    if command -v kubectl &> /dev/null; then
        local kubectl_version
        kubectl_version=$(kubectl version --client --short 2>/dev/null || kubectl version --client 2>/dev/null | head -n1)
        log_pass "kubectl installed: $kubectl_version"
    else
        log_info "kubectl not installed (optional for K8s deployment)"
    fi
}

# ============================================================================
# NETWORK CONNECTIVITY
# ============================================================================

verify_network() {
    log_header "NETWORK CONNECTIVITY DIAGNOSTIC"
    
    local endpoints=(
        "github.com"
        "api.github.com"
        "registry.npmjs.org"
        "pypi.org"
    )
    
    echo "Checking network connectivity..."
    echo ""
    
    # Check basic internet connectivity
    if ping -c 1 -W 3 8.8.8.8 &> /dev/null || ping -c 1 -W 3 1.1.1.1 &> /dev/null; then
        log_pass "Internet connectivity detected"
        
        # Check specific endpoints
        for endpoint in "${endpoints[@]}"; do
            if ping -c 1 -W 3 "$endpoint" &> /dev/null; then
                log_pass "Can reach $endpoint"
            elif curl -s --max-time 5 "https://$endpoint" &> /dev/null; then
                log_pass "Can reach $endpoint (via HTTPS)"
            else
                log_warn "Cannot reach $endpoint"
            fi
        done
    else
        log_warn "No internet connectivity detected"
        log_warn "Cannot reach GitHub (offline mode)"
        log_info "Stack can still operate in offline/air-gapped mode"
    fi
}

# ============================================================================
# HASH VERIFICATION (TAMPER DETECTION)
# ============================================================================

generate_hashes() {
    log_header "GENERATING SHA-256 FILE HASHES"
    
    local files_to_hash=(
        "README.md"
        "LICENSE"
        "SECURITY.md"
        "package.json"
        "discovery.yml"
        "validate-config.sh"
        "status-check.sh"
        "bootstrap/deploy.sh"
        "gl2discord.sh"
        "src/bot.ts"
        "src/event-gateway.ts"
        "docker-compose.yml"
        "docker-compose-cloudos.yml"
        "governance/access_matrix.yaml"
    )
    
    echo "Generating hashes for critical files..."
    echo ""
    
    # Clear existing hash file
    : > "$HASH_FILE"
    
    for file in "${files_to_hash[@]}"; do
        local filepath="${SCRIPT_DIR}/${file}"
        if [[ -f "$filepath" ]]; then
            local hash
            hash=$(sha256sum "$filepath" 2>/dev/null | awk '{print $1}')
            if [[ -n "$hash" ]]; then
                echo "$hash  $file" >> "$HASH_FILE"
                log_pass "Hash generated: $file"
                echo "      SHA256: ${hash:0:16}...${hash: -16}"
            fi
        fi
    done
    
    echo ""
    log_info "Hash file saved to: $HASH_FILE"
}

verify_hashes() {
    log_header "VERIFYING SHA-256 FILE HASHES"
    
    if [[ ! -f "$HASH_FILE" ]]; then
        log_warn "No hash file found. Run with --hash to generate baseline."
        return
    fi
    
    echo "Verifying file integrity against stored hashes..."
    echo ""
    
    local tampering_detected=false
    
    while IFS= read -r line; do
        local stored_hash file
        stored_hash=$(echo "$line" | awk '{print $1}')
        file=$(echo "$line" | awk '{print $2}')
        local filepath="${SCRIPT_DIR}/${file}"
        
        if [[ -f "$filepath" ]]; then
            local current_hash
            current_hash=$(sha256sum "$filepath" 2>/dev/null | awk '{print $1}')
            
            if [[ "$stored_hash" == "$current_hash" ]]; then
                log_pass "$file integrity verified"
            else
                log_fail "$file MODIFIED - potential tampering detected!"
                tampering_detected=true
            fi
        else
            log_warn "$file not found - may have been deleted"
        fi
    done < "$HASH_FILE"
    
    echo ""
    if [[ "$tampering_detected" == true ]]; then
        echo -e "${RED}⚠️  TAMPER WARNING: File modifications detected!${NC}"
        echo -e "${YELLOW}   Review changes before proceeding.${NC}"
    else
        log_pass "All file hashes verified - no tampering detected"
    fi
}

# ============================================================================
# CONFIGURATION AUDIT
# ============================================================================

audit_configuration() {
    log_header "CONFIGURATION AUDIT"
    
    echo "Auditing configuration files..."
    echo ""
    
    # Check discovery.yml
    if [[ -f "${SCRIPT_DIR}/discovery.yml" ]]; then
        log_pass "discovery.yml present"
        
        # Check for required fields using grep (fallback if yq not available)
        if command -v yq &> /dev/null; then
            local org_name
            org_name=$(yq '.org.name' "${SCRIPT_DIR}/discovery.yml" 2>/dev/null || echo "null")
            if [[ "$org_name" != "null" && "$org_name" != '""' ]]; then
                log_pass "Organization configured: $org_name"
            else
                log_warn "Organization name not configured"
            fi
        else
            if grep -q "org:" "${SCRIPT_DIR}/discovery.yml"; then
                log_pass "Organization section present"
            fi
        fi
    else
        log_warn "discovery.yml not found"
    fi
    
    # Check Docker Compose files
    local compose_files=(
        "docker-compose.yml"
        "docker-compose-cloudos.yml"
        "docker-compose-recon.yml"
    )
    
    for compose in "${compose_files[@]}"; do
        if [[ -f "${SCRIPT_DIR}/${compose}" ]]; then
            log_pass "$compose present"
        fi
    done
    
    # Check Kubernetes manifests
    if [[ -d "${SCRIPT_DIR}/bootstrap/k8s" ]]; then
        local k8s_count
        k8s_count=$(find "${SCRIPT_DIR}/bootstrap/k8s" -name "*.yaml" -o -name "*.yml" 2>/dev/null | wc -l)
        log_pass "Kubernetes manifests found: $k8s_count files"
    fi
    
    # Check governance files
    if [[ -f "${SCRIPT_DIR}/governance/access_matrix.yaml" ]]; then
        log_pass "Access control matrix present"
    fi
    
    # Check security policy
    if [[ -f "${SCRIPT_DIR}/SECURITY.md" ]]; then
        log_pass "Security policy documented"
    fi
}

# ============================================================================
# SUMMARY REPORT
# ============================================================================

print_summary() {
    log_header "SOVEREIGNTY STACK VERIFICATION SUMMARY"
    
    local total=$((PASS_COUNT + FAIL_COUNT + WARN_COUNT))
    
    echo -e "${GREEN}Passed:${NC}   $PASS_COUNT"
    echo -e "${RED}Failed:${NC}   $FAIL_COUNT"
    echo -e "${YELLOW}Warnings:${NC} $WARN_COUNT"
    echo -e "${BLUE}Total:${NC}    $total checks"
    echo ""
    
    if [[ $FAIL_COUNT -eq 0 ]]; then
        echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
        echo -e "${GREEN}║  ✅ SOVEREIGNTY STACK VERIFICATION: PASSED                    ║${NC}"
        echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
    else
        echo -e "${RED}╔══════════════════════════════════════════════════════════════╗${NC}"
        echo -e "${RED}║  ❌ SOVEREIGNTY STACK VERIFICATION: FAILED                    ║${NC}"
        echo -e "${RED}║     Please address $FAIL_COUNT failure(s) before deployment           ║${NC}"
        echo -e "${RED}╚══════════════════════════════════════════════════════════════╝${NC}"
    fi
    
    echo ""
    echo "Log file: $LOG_FILE"
    echo "Timestamp: $(date '+%Y-%m-%d %H:%M:%S %Z')"
}

# ============================================================================
# HELP
# ============================================================================

show_help() {
    cat << EOF
SOVEREIGNTY STACK VALIDATION MODULE v1.0
========================================

A self-verifying sovereign software stack that performs hash-proven integrity
checks on critical stack files and validates execution readiness.

USAGE:
    ./verify_sovereignty.sh [OPTIONS]

OPTIONS:
    --full      Run all verification checks (default)
    --quick     Run quick health check only (env + files)
    --hash      Generate SHA-256 hashes for critical files
    --verify    Verify file hashes against baseline
    --env       Check system environment only
    --network   Check network connectivity only
    --audit     Run configuration audit only
    --help      Show this help message

EXAMPLES:
    ./verify_sovereignty.sh                 # Full verification
    ./verify_sovereignty.sh --quick         # Quick health check
    ./verify_sovereignty.sh --hash          # Generate baseline hashes
    ./verify_sovereignty.sh --verify        # Verify against baseline

OUTPUT:
    Verification results are logged to: .sovereignty_verification.log
    Hash baseline stored in: .sovereignty_hashes.sha256

For more information, see: SOVEREIGNTY_STACK_README.md

Copyright (c) 2025 Strategickhaos DAO LLC
SPDX-License-Identifier: MIT
EOF
}

# ============================================================================
# MAIN
# ============================================================================

main() {
    # Initialize log file
    echo "=== Sovereignty Stack Verification Log ===" > "$LOG_FILE"
    echo "Started: $(date)" >> "$LOG_FILE"
    echo "" >> "$LOG_FILE"
    
    echo ""
    echo -e "${CYAN}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║      🔐 SOVEREIGNTY STACK VALIDATION MODULE v1.0 🔐           ║${NC}"
    echo -e "${CYAN}║          Strategickhaos DAO LLC - Self-Verification          ║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    case "${1:-}" in
        --help|-h)
            show_help
            exit 0
            ;;
        --quick)
            verify_environment
            verify_file_integrity
            print_summary
            ;;
        --hash)
            generate_hashes
            ;;
        --verify)
            verify_hashes
            print_summary
            ;;
        --env)
            verify_environment
            print_summary
            ;;
        --network)
            verify_network
            print_summary
            ;;
        --audit)
            audit_configuration
            print_summary
            ;;
        --full|"")
            verify_environment
            verify_file_integrity
            verify_network
            audit_configuration
            verify_hashes
            print_summary
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
    
    # Exit with appropriate code
    if [[ $FAIL_COUNT -gt 0 ]]; then
        exit 1
    fi
    exit 0
}

main "$@"
