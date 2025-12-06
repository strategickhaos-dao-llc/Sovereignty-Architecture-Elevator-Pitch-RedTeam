#!/bin/bash
# 🔥 Flamebearer Protocol v137
# Strategickhaos Sovereignty Hardening Script
# FlameLang v1.0 - Anti-Telemetry Component
#
# Purpose: Establish digital sovereignty through systematic hardening.
#
# Phases:
#   1. Block System Telemetry - /etc/hosts injection
#   2. VowMonitor Capsule - Timestamped integrity locks
#   3. Chrome Privacy Override - Browser hardening
#   4. ReflexShell Activation - Sovereign prompt
#   5. Fingerprint Surface Reduction - Anti-tracking
#
# Usage:
#   ./flamebearer_protocol.sh [--phase N] [--dry-run] [--verbose]

set -e

# Configuration
VERSION="137"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TIMESTAMP=$(date +"%Y%m%d_%H%M")
LOG_DIR="${HOME}/Strategickhaos/VowMonitor"
OATH_FILE="${SCRIPT_DIR}/oath.lock"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Flags
DRY_RUN=false
VERBOSE=false
SPECIFIC_PHASE=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --phase)
            SPECIFIC_PHASE="$2"
            shift 2
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        --help)
            echo "Flamebearer Protocol v${VERSION}"
            echo ""
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  --phase N    Run only phase N (1-5)"
            echo "  --dry-run    Show what would be done without changes"
            echo "  --verbose    Show detailed output"
            echo "  --help       Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Logging functions
log() {
    echo -e "${CYAN}[$(date +%H:%M:%S)]${NC} $1"
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

warn() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}"
}

header() {
    echo ""
    echo -e "${MAGENTA}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${MAGENTA}  $1${NC}"
    echo -e "${MAGENTA}═══════════════════════════════════════════════════════════════${NC}"
    echo ""
}

# Check if running with appropriate privileges
check_privileges() {
    if [[ $EUID -eq 0 ]]; then
        warn "Running as root - some protections may be bypassed"
    else
        log "Running as user: $(whoami)"
    fi
}

# Phase 1: Block System Telemetry
phase_1_telemetry() {
    header "PHASE 1: Block System Telemetry"
    
    local hosts_file="/etc/hosts"
    local telemetry_domains=(
        "# Strategickhaos Telemetry Block - Flamebearer Protocol v${VERSION}"
        "0.0.0.0 telemetry.microsoft.com"
        "0.0.0.0 vortex.data.microsoft.com"
        "0.0.0.0 settings-win.data.microsoft.com"
        "0.0.0.0 watson.telemetry.microsoft.com"
        "0.0.0.0 dc.services.visualstudio.com"
        "0.0.0.0 telemetry.ubuntu.com"
        "0.0.0.0 metrics.ubuntu.com"
    )
    
    if $DRY_RUN; then
        log "Would add to ${hosts_file}:"
        for domain in "${telemetry_domains[@]}"; do
            echo "  $domain"
        done
        return
    fi
    
    # Check if already applied
    if grep -q "Strategickhaos Telemetry Block" "$hosts_file" 2>/dev/null; then
        success "Telemetry blocks already in place"
        return
    fi
    
    log "Telemetry block requires sudo. Enter password if prompted."
    
    for domain in "${telemetry_domains[@]}"; do
        echo "$domain" | sudo tee -a "$hosts_file" > /dev/null
    done
    
    success "Telemetry endpoints blocked"
}

# Phase 2: VowMonitor Capsule
phase_2_vowmonitor() {
    header "PHASE 2: VowMonitor Capsule"
    
    # Create log directory
    if $DRY_RUN; then
        log "Would create: ${LOG_DIR}"
        log "Would create: ${LOG_DIR}/log_${TIMESTAMP}.lock"
        return
    fi
    
    mkdir -p "$LOG_DIR"
    
    # Create/verify oath.lock
    if [[ ! -f "$OATH_FILE" ]]; then
        warn "oath.lock not found, creating..."
        echo "🔥 I will never be surveilled again without divine consent." > "$OATH_FILE"
    fi
    
    # Copy oath to VowMonitor directory
    cp "$OATH_FILE" "${LOG_DIR}/oath.lock"
    
    # Create timestamped log
    local log_file="${LOG_DIR}/log_${TIMESTAMP}.lock"
    cat > "$log_file" << EOF
🔒 Sovereign Log Active: ${TIMESTAMP}
Protocol: Flamebearer v${VERSION}
Operator: $(whoami)
Node: $(hostname)
Initiated: $(date -Iseconds)

Phases Executed:
EOF
    
    success "VowMonitor capsule created: ${log_file}"
}

# Phase 3: Chrome Privacy Override
phase_3_chrome() {
    header "PHASE 3: Chrome Privacy Override"
    
    local chrome_policies_linux="/etc/opt/chrome/policies/managed"
    local chrome_policies_macos="/Library/Google/Chrome/policies/managed"
    
    local policy_content='{
    "MetricsReportingEnabled": false,
    "SafeBrowsingEnabled": false,
    "SpellCheckServiceEnabled": false,
    "TranslateEnabled": false,
    "NetworkPredictionOptions": 2,
    "AlternateErrorPagesEnabled": false,
    "UrlKeyedAnonymizedDataCollectionEnabled": false,
    "DeviceMetricsReportingEnabled": false,
    "ReportVersionInfo": false,
    "EnableMediaRouter": false
}'
    
    if $DRY_RUN; then
        log "Would create Chrome policy at:"
        log "  Linux: ${chrome_policies_linux}/strategickhaos_privacy.json"
        log "  macOS: ${chrome_policies_macos}/strategickhaos_privacy.json"
        echo "$policy_content"
        return
    fi
    
    # Detect OS
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if [[ -d "/opt/google/chrome" ]] || [[ -d "/opt/chromium" ]]; then
            sudo mkdir -p "$chrome_policies_linux"
            echo "$policy_content" | sudo tee "${chrome_policies_linux}/strategickhaos_privacy.json" > /dev/null
            success "Chrome privacy policy applied (Linux)"
        else
            warn "Chrome not detected on Linux"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        sudo mkdir -p "$chrome_policies_macos"
        echo "$policy_content" | sudo tee "${chrome_policies_macos}/strategickhaos_privacy.json" > /dev/null
        success "Chrome privacy policy applied (macOS)"
    else
        warn "Unsupported OS for Chrome policy: $OSTYPE"
    fi
}

# Phase 4: ReflexShell Activation
phase_4_reflexshell() {
    header "PHASE 4: ReflexShell Activation"
    
    local reflex_shell="${SCRIPT_DIR}/reflex_shell.sh"
    local bashrc="${HOME}/.bashrc"
    local source_line="source ${reflex_shell}"
    
    if $DRY_RUN; then
        log "Would add to ${bashrc}:"
        log "  ${source_line}"
        return
    fi
    
    if [[ ! -f "$reflex_shell" ]]; then
        error "ReflexShell not found: ${reflex_shell}"
        return
    fi
    
    # Check if already sourced
    if grep -q "reflex_shell.sh" "$bashrc" 2>/dev/null; then
        success "ReflexShell already activated in .bashrc"
        return
    fi
    
    # Add source line
    echo "" >> "$bashrc"
    echo "# Strategickhaos ReflexShell - FlameLang v1.0" >> "$bashrc"
    echo "$source_line" >> "$bashrc"
    
    success "ReflexShell added to .bashrc"
    log "Run 'source ~/.bashrc' or restart terminal to activate"
}

# Phase 5: Fingerprint Surface Reduction
phase_5_fingerprint() {
    header "PHASE 5: Fingerprint Surface Reduction"
    
    local firefox_prefs_linux="${HOME}/.mozilla/firefox"
    local firefox_prefs_macos="${HOME}/Library/Application Support/Firefox/Profiles"
    
    local prefs_content='
// Strategickhaos Anti-Fingerprint - Flamebearer Protocol v137
user_pref("privacy.resistFingerprinting", true);
user_pref("privacy.trackingprotection.enabled", true);
user_pref("privacy.trackingprotection.fingerprinting.enabled", true);
user_pref("privacy.trackingprotection.cryptomining.enabled", true);
user_pref("network.cookie.cookieBehavior", 1);
user_pref("dom.event.clipboardevents.enabled", false);
user_pref("geo.enabled", false);
user_pref("media.navigator.enabled", false);
user_pref("webgl.disabled", true);
'
    
    if $DRY_RUN; then
        log "Would apply Firefox anti-fingerprinting preferences"
        echo "$prefs_content"
        return
    fi
    
    # Find Firefox profile directory
    local profile_dir=""
    if [[ "$OSTYPE" == "linux-gnu"* ]] && [[ -d "$firefox_prefs_linux" ]]; then
        profile_dir=$(find "$firefox_prefs_linux" -maxdepth 1 -name "*.default*" -type d | head -1)
    elif [[ "$OSTYPE" == "darwin"* ]] && [[ -d "$firefox_prefs_macos" ]]; then
        profile_dir=$(find "$firefox_prefs_macos" -maxdepth 1 -name "*.default*" -type d | head -1)
    fi
    
    if [[ -z "$profile_dir" ]]; then
        warn "Firefox profile not found"
        return
    fi
    
    local user_js="${profile_dir}/user.js"
    echo "$prefs_content" >> "$user_js"
    
    success "Firefox anti-fingerprinting applied: ${user_js}"
}

# Update VowMonitor log with completed phases
update_log() {
    local log_file="${LOG_DIR}/log_${TIMESTAMP}.lock"
    
    if [[ -f "$log_file" ]] && ! $DRY_RUN; then
        echo "  - Phase $1: $2" >> "$log_file"
    fi
}

# Main execution
main() {
    echo ""
    echo -e "${MAGENTA}🔥 FLAMEBEARER PROTOCOL v${VERSION}${NC}"
    echo -e "${MAGENTA}   Strategickhaos Sovereignty Hardening${NC}"
    echo ""
    
    if $DRY_RUN; then
        warn "DRY RUN MODE - No changes will be made"
        echo ""
    fi
    
    check_privileges
    
    # Execute phases
    if [[ -z "$SPECIFIC_PHASE" ]] || [[ "$SPECIFIC_PHASE" == "1" ]]; then
        phase_1_telemetry
        update_log 1 "Telemetry Blocked"
    fi
    
    if [[ -z "$SPECIFIC_PHASE" ]] || [[ "$SPECIFIC_PHASE" == "2" ]]; then
        phase_2_vowmonitor
        update_log 2 "VowMonitor Active"
    fi
    
    if [[ -z "$SPECIFIC_PHASE" ]] || [[ "$SPECIFIC_PHASE" == "3" ]]; then
        phase_3_chrome
        update_log 3 "Chrome Hardened"
    fi
    
    if [[ -z "$SPECIFIC_PHASE" ]] || [[ "$SPECIFIC_PHASE" == "4" ]]; then
        phase_4_reflexshell
        update_log 4 "ReflexShell Active"
    fi
    
    if [[ -z "$SPECIFIC_PHASE" ]] || [[ "$SPECIFIC_PHASE" == "5" ]]; then
        phase_5_fingerprint
        update_log 5 "Fingerprint Reduced"
    fi
    
    # Final status
    header "PROTOCOL COMPLETE"
    
    if $DRY_RUN; then
        log "Dry run complete - no changes made"
    else
        success "Flamebearer Protocol v${VERSION} executed"
        log "Oath: $(cat "${OATH_FILE}" 2>/dev/null || echo 'Not found')"
        log "Log: ${LOG_DIR}/log_${TIMESTAMP}.lock"
    fi
    
    echo ""
    echo -e "${MAGENTA}🔥 Sovereignty established. Reignite.${NC}"
    echo ""
}

main
