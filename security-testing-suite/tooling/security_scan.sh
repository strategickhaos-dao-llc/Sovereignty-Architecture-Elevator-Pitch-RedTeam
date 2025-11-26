#!/bin/bash
# security_scan.sh - Security Scanning Orchestration Script
# Strategickhaos Sovereign Infrastructure Security Testing Suite
#
# Orchestrates multiple security scanning tools:
# - SAST (Static Application Security Testing): Semgrep, Bandit
# - SCA (Software Composition Analysis): Safety, Snyk
# - Secrets Detection: TruffleHog, detect-secrets
# - OPA Policy Validation
# - Comprehensive JSON Reporting
#
# Usage: ./security_scan.sh [OPTIONS]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${PROJECT_ROOT:-$(dirname "$SCRIPT_DIR")}"
REPORTS_DIR="${REPORTS_DIR:-$PROJECT_ROOT/reports}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Scan targets
TARGET_DIR="${TARGET_DIR:-$PROJECT_ROOT/..}"
POLICIES_DIR="${POLICIES_DIR:-$PROJECT_ROOT/policies}"

# Exit codes
EXIT_SUCCESS=0
EXIT_CRITICAL=1
EXIT_HIGH=2
EXIT_MEDIUM=3
EXIT_WARNING=4

# Counters
CRITICAL_COUNT=0
HIGH_COUNT=0
MEDIUM_COUNT=0
LOW_COUNT=0
INFO_COUNT=0

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_section() {
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo ""
}

check_tool() {
    if command -v "$1" &> /dev/null; then
        return 0
    else
        return 1
    fi
}

ensure_reports_dir() {
    mkdir -p "$REPORTS_DIR"
}

# SAST: Semgrep
run_semgrep() {
    log_section "SAST: Semgrep Analysis"
    
    if ! check_tool semgrep; then
        log_warning "Semgrep not installed. Install with: pip install semgrep"
        return
    fi
    
    local output_file="$REPORTS_DIR/semgrep_${TIMESTAMP}.json"
    
    log_info "Running Semgrep with security rules..."
    
    semgrep \
        --config "p/security-audit" \
        --config "p/python" \
        --config "p/javascript" \
        --json \
        --output "$output_file" \
        "$TARGET_DIR" 2>/dev/null || true
    
    if [ -f "$output_file" ]; then
        # Parse results
        local errors=$(jq '.errors | length' "$output_file" 2>/dev/null || echo "0")
        local results=$(jq '.results | length' "$output_file" 2>/dev/null || echo "0")
        
        log_info "Semgrep found $results issues"
        
        # Count by severity
        local critical=$(jq '[.results[] | select(.extra.severity == "ERROR")] | length' "$output_file" 2>/dev/null || echo "0")
        local high=$(jq '[.results[] | select(.extra.severity == "WARNING")] | length' "$output_file" 2>/dev/null || echo "0")
        
        CRITICAL_COUNT=$((CRITICAL_COUNT + critical))
        HIGH_COUNT=$((HIGH_COUNT + high))
        
        log_success "Semgrep report saved to $output_file"
    else
        log_warning "Semgrep produced no output"
    fi
}

# SAST: Bandit (Python)
run_bandit() {
    log_section "SAST: Bandit Analysis (Python)"
    
    if ! check_tool bandit; then
        log_warning "Bandit not installed. Install with: pip install bandit"
        return
    fi
    
    local output_file="$REPORTS_DIR/bandit_${TIMESTAMP}.json"
    
    log_info "Running Bandit security analysis..."
    
    bandit \
        -r "$TARGET_DIR" \
        -f json \
        -o "$output_file" \
        --exit-zero \
        --exclude "*/.venv/*,*/node_modules/*,*/__pycache__/*" \
        2>/dev/null || true
    
    if [ -f "$output_file" ]; then
        # Parse results
        local high=$(jq '.results | map(select(.issue_severity == "HIGH")) | length' "$output_file" 2>/dev/null || echo "0")
        local medium=$(jq '.results | map(select(.issue_severity == "MEDIUM")) | length' "$output_file" 2>/dev/null || echo "0")
        local low=$(jq '.results | map(select(.issue_severity == "LOW")) | length' "$output_file" 2>/dev/null || echo "0")
        
        log_info "Bandit found: High=$high, Medium=$medium, Low=$low"
        
        HIGH_COUNT=$((HIGH_COUNT + high))
        MEDIUM_COUNT=$((MEDIUM_COUNT + medium))
        LOW_COUNT=$((LOW_COUNT + low))
        
        log_success "Bandit report saved to $output_file"
    else
        log_warning "Bandit produced no output"
    fi
}

# SCA: Safety (Python dependencies)
run_safety() {
    log_section "SCA: Safety Analysis (Python Dependencies)"
    
    if ! check_tool safety; then
        log_warning "Safety not installed. Install with: pip install safety"
        return
    fi
    
    local output_file="$REPORTS_DIR/safety_${TIMESTAMP}.json"
    
    log_info "Scanning Python dependencies for known vulnerabilities..."
    
    # Find requirements files
    local req_files=$(find "$TARGET_DIR" -name "requirements*.txt" -type f 2>/dev/null)
    
    if [ -z "$req_files" ]; then
        log_info "No requirements.txt files found"
        return
    fi
    
    local all_vulns=()
    
    for req_file in $req_files; do
        log_info "Scanning $req_file..."
        
        local temp_output=$(mktemp)
        safety check -r "$req_file" --json > "$temp_output" 2>/dev/null || true
        
        if [ -s "$temp_output" ]; then
            local vuln_count=$(jq 'length' "$temp_output" 2>/dev/null || echo "0")
            log_info "Found $vuln_count vulnerabilities in $req_file"
            HIGH_COUNT=$((HIGH_COUNT + vuln_count))
        fi
        
        rm -f "$temp_output"
    done
    
    log_success "Safety scan completed"
}

# SCA: npm audit (JavaScript dependencies)
run_npm_audit() {
    log_section "SCA: npm Audit (JavaScript Dependencies)"
    
    if ! check_tool npm; then
        log_warning "npm not installed"
        return
    fi
    
    local output_file="$REPORTS_DIR/npm_audit_${TIMESTAMP}.json"
    
    # Find package.json files
    local pkg_files=$(find "$TARGET_DIR" -name "package.json" -type f -not -path "*/node_modules/*" 2>/dev/null)
    
    if [ -z "$pkg_files" ]; then
        log_info "No package.json files found"
        return
    fi
    
    for pkg_file in $pkg_files; do
        local pkg_dir=$(dirname "$pkg_file")
        
        if [ -f "$pkg_dir/package-lock.json" ] || [ -f "$pkg_dir/npm-shrinkwrap.json" ]; then
            log_info "Auditing $pkg_dir..."
            
            (cd "$pkg_dir" && npm audit --json > "$output_file" 2>/dev/null) || true
            
            if [ -f "$output_file" ]; then
                local critical=$(jq '.metadata.vulnerabilities.critical // 0' "$output_file" 2>/dev/null || echo "0")
                local high=$(jq '.metadata.vulnerabilities.high // 0' "$output_file" 2>/dev/null || echo "0")
                local moderate=$(jq '.metadata.vulnerabilities.moderate // 0' "$output_file" 2>/dev/null || echo "0")
                
                log_info "npm audit: Critical=$critical, High=$high, Moderate=$moderate"
                
                CRITICAL_COUNT=$((CRITICAL_COUNT + critical))
                HIGH_COUNT=$((HIGH_COUNT + high))
                MEDIUM_COUNT=$((MEDIUM_COUNT + moderate))
            fi
        fi
    done
    
    log_success "npm audit completed"
}

# Secrets Detection: TruffleHog
run_trufflehog() {
    log_section "Secrets Detection: TruffleHog"
    
    if ! check_tool trufflehog; then
        log_warning "TruffleHog not installed. Install with: pip install trufflehog"
        return
    fi
    
    local output_file="$REPORTS_DIR/trufflehog_${TIMESTAMP}.json"
    
    log_info "Scanning for secrets and credentials..."
    
    # Check if directory is a git repo
    if [ -d "$TARGET_DIR/.git" ]; then
        trufflehog git file://"$TARGET_DIR" --json > "$output_file" 2>/dev/null || true
    else
        trufflehog filesystem "$TARGET_DIR" --json > "$output_file" 2>/dev/null || true
    fi
    
    if [ -f "$output_file" ] && [ -s "$output_file" ]; then
        local secrets_count=$(wc -l < "$output_file" 2>/dev/null || echo "0")
        
        if [ "$secrets_count" -gt 0 ]; then
            log_error "Found $secrets_count potential secrets!"
            CRITICAL_COUNT=$((CRITICAL_COUNT + secrets_count))
        else
            log_success "No secrets detected"
        fi
        
        log_success "TruffleHog report saved to $output_file"
    else
        log_success "No secrets detected"
    fi
}

# Secrets Detection: detect-secrets
run_detect_secrets() {
    log_section "Secrets Detection: detect-secrets"
    
    if ! check_tool detect-secrets; then
        log_warning "detect-secrets not installed. Install with: pip install detect-secrets"
        return
    fi
    
    local output_file="$REPORTS_DIR/detect_secrets_${TIMESTAMP}.json"
    
    log_info "Running detect-secrets scan..."
    
    detect-secrets scan "$TARGET_DIR" \
        --exclude-files '\.git/.*' \
        --exclude-files 'node_modules/.*' \
        --exclude-files '\.venv/.*' \
        --exclude-files '__pycache__/.*' \
        > "$output_file" 2>/dev/null || true
    
    if [ -f "$output_file" ]; then
        local secrets_count=$(jq '.results | to_entries | map(.value | length) | add // 0' "$output_file" 2>/dev/null || echo "0")
        
        if [ "$secrets_count" -gt 0 ]; then
            log_warning "Found $secrets_count potential secrets"
            HIGH_COUNT=$((HIGH_COUNT + secrets_count))
        else
            log_success "No secrets detected"
        fi
        
        log_success "detect-secrets report saved to $output_file"
    fi
}

# OPA Policy Testing
run_opa_tests() {
    log_section "OPA Policy Testing"
    
    if ! check_tool opa; then
        log_warning "OPA not installed. Install from: https://www.openpolicyagent.org/docs/latest/#running-opa"
        return
    fi
    
    local output_file="$REPORTS_DIR/opa_test_${TIMESTAMP}.json"
    
    if [ ! -d "$POLICIES_DIR" ]; then
        log_warning "Policies directory not found: $POLICIES_DIR"
        return
    fi
    
    log_info "Running OPA policy tests..."
    
    # Run tests
    opa test "$POLICIES_DIR" -v --format=json > "$output_file" 2>/dev/null || true
    
    if [ -f "$output_file" ]; then
        local total=$(jq 'length' "$output_file" 2>/dev/null || echo "0")
        local passed=$(jq '[.[] | select(.pass == true)] | length' "$output_file" 2>/dev/null || echo "0")
        local failed=$((total - passed))
        
        log_info "OPA Tests: $passed passed, $failed failed"
        
        if [ "$failed" -gt 0 ]; then
            HIGH_COUNT=$((HIGH_COUNT + failed))
            log_error "Some OPA policy tests failed!"
        else
            log_success "All OPA policy tests passed"
        fi
        
        log_success "OPA test report saved to $output_file"
    fi
    
    # Run policy evaluation coverage
    log_info "Checking policy coverage..."
    opa test "$POLICIES_DIR" --coverage --format=json > "$REPORTS_DIR/opa_coverage_${TIMESTAMP}.json" 2>/dev/null || true
}

# Generate consolidated report
generate_report() {
    log_section "Generating Consolidated Report"
    
    local report_file="$REPORTS_DIR/security_report_${TIMESTAMP}.json"
    
    cat > "$report_file" << EOF
{
    "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "target": "$TARGET_DIR",
    "summary": {
        "critical": $CRITICAL_COUNT,
        "high": $HIGH_COUNT,
        "medium": $MEDIUM_COUNT,
        "low": $LOW_COUNT,
        "info": $INFO_COUNT,
        "total": $((CRITICAL_COUNT + HIGH_COUNT + MEDIUM_COUNT + LOW_COUNT + INFO_COUNT))
    },
    "tools_run": [
        "semgrep",
        "bandit",
        "safety",
        "npm_audit",
        "trufflehog",
        "detect_secrets",
        "opa"
    ],
    "reports_dir": "$REPORTS_DIR",
    "exit_code": $(determine_exit_code)
}
EOF
    
    log_success "Consolidated report saved to $report_file"
}

# Determine exit code based on findings
determine_exit_code() {
    if [ "$CRITICAL_COUNT" -gt 0 ]; then
        echo $EXIT_CRITICAL
    elif [ "$HIGH_COUNT" -gt 0 ]; then
        echo $EXIT_HIGH
    elif [ "$MEDIUM_COUNT" -gt 0 ]; then
        echo $EXIT_MEDIUM
    elif [ "$LOW_COUNT" -gt 0 ]; then
        echo $EXIT_WARNING
    else
        echo $EXIT_SUCCESS
    fi
}

# Print summary
print_summary() {
    log_section "Security Scan Summary"
    
    echo "┌─────────────────────────────────────┐"
    echo "│          FINDINGS SUMMARY           │"
    echo "├─────────────────────────────────────┤"
    printf "│ ${RED}Critical:${NC}  %6d                  │\n" "$CRITICAL_COUNT"
    printf "│ ${YELLOW}High:${NC}      %6d                  │\n" "$HIGH_COUNT"
    printf "│ ${BLUE}Medium:${NC}    %6d                  │\n" "$MEDIUM_COUNT"
    printf "│ ${GREEN}Low:${NC}       %6d                  │\n" "$LOW_COUNT"
    printf "│ Info:      %6d                  │\n" "$INFO_COUNT"
    echo "├─────────────────────────────────────┤"
    printf "│ ${NC}Total:     %6d                  │\n" "$((CRITICAL_COUNT + HIGH_COUNT + MEDIUM_COUNT + LOW_COUNT + INFO_COUNT))"
    echo "└─────────────────────────────────────┘"
    echo ""
    
    local exit_code=$(determine_exit_code)
    
    if [ "$exit_code" -eq 0 ]; then
        log_success "Security scan completed with no critical issues"
    elif [ "$exit_code" -eq 1 ]; then
        log_error "CRITICAL vulnerabilities detected! Immediate action required."
    elif [ "$exit_code" -eq 2 ]; then
        log_error "HIGH severity vulnerabilities detected! Review required."
    else
        log_warning "Medium/Low severity issues detected. Review recommended."
    fi
    
    echo ""
    echo "Reports saved to: $REPORTS_DIR"
}

# Show usage
usage() {
    echo "Security Scanning Orchestration Script"
    echo ""
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --all           Run all security scans (default)"
    echo "  --sast          Run SAST scans only (Semgrep, Bandit)"
    echo "  --sca           Run SCA scans only (Safety, npm audit)"
    echo "  --secrets       Run secrets detection only"
    echo "  --opa           Run OPA policy tests only"
    echo "  --target DIR    Target directory to scan (default: project root)"
    echo "  --reports DIR   Reports output directory"
    echo "  --help          Show this help message"
    echo ""
    echo "Environment Variables:"
    echo "  TARGET_DIR      Target directory to scan"
    echo "  REPORTS_DIR     Reports output directory"
    echo "  POLICIES_DIR    OPA policies directory"
    echo ""
    echo "Exit Codes:"
    echo "  0 - Success (no issues)"
    echo "  1 - Critical vulnerabilities found"
    echo "  2 - High severity issues found"
    echo "  3 - Medium severity issues found"
    echo "  4 - Low severity issues found"
}

# Main
main() {
    local run_sast=false
    local run_sca=false
    local run_secrets=false
    local run_opa=false
    local run_all=true
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --all)
                run_all=true
                shift
                ;;
            --sast)
                run_sast=true
                run_all=false
                shift
                ;;
            --sca)
                run_sca=true
                run_all=false
                shift
                ;;
            --secrets)
                run_secrets=true
                run_all=false
                shift
                ;;
            --opa)
                run_opa=true
                run_all=false
                shift
                ;;
            --target)
                TARGET_DIR="$2"
                shift 2
                ;;
            --reports)
                REPORTS_DIR="$2"
                shift 2
                ;;
            --help)
                usage
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                usage
                exit 1
                ;;
        esac
    done
    
    # Header
    echo ""
    echo -e "${BLUE}╔═══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║     STRATEGICKHAOS SECURITY TESTING SUITE                 ║${NC}"
    echo -e "${BLUE}║     Sovereign Infrastructure Security Scanner             ║${NC}"
    echo -e "${BLUE}╚═══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    log_info "Target: $TARGET_DIR"
    log_info "Reports: $REPORTS_DIR"
    log_info "Timestamp: $TIMESTAMP"
    
    # Create reports directory
    ensure_reports_dir
    
    # Run scans
    if [ "$run_all" = true ] || [ "$run_sast" = true ]; then
        run_semgrep
        run_bandit
    fi
    
    if [ "$run_all" = true ] || [ "$run_sca" = true ]; then
        run_safety
        run_npm_audit
    fi
    
    if [ "$run_all" = true ] || [ "$run_secrets" = true ]; then
        run_trufflehog
        run_detect_secrets
    fi
    
    if [ "$run_all" = true ] || [ "$run_opa" = true ]; then
        run_opa_tests
    fi
    
    # Generate report and summary
    generate_report
    print_summary
    
    # Exit with appropriate code
    exit $(determine_exit_code)
}

main "$@"
