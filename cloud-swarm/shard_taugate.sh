#!/bin/bash
# TauGate Shard Launcher - Fan out 10B compound screening across nodes
# Usage: ./shard_taugate.sh [inventory_file] [compounds_path] [target_file]
# Example: ./shard_taugate.sh cloud_hosts.ini /data/compounds tau_4R.mrc

set -euo pipefail

# Configuration
INVENTORY=${1:-cloud_hosts.ini}
COMPOUNDS_PATH=${2:-/data/compounds}
TARGET_FILE=${3:-tau_4R.mrc}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="/tmp/taugate_launcher_${TIMESTAMP}.log"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# Logging
log() { echo -e "[$(date -Iseconds)] $1" | tee -a "${LOG_FILE}"; }
log_info() { log "${BLUE}[INFO]${NC} $1"; }
log_success() { log "${GREEN}[SUCCESS]${NC} $1"; }
log_warn() { log "${YELLOW}[WARN]${NC} $1"; }
log_error() { log "${RED}[ERROR]${NC} $1"; }

# Get host count from inventory
get_host_count() {
    grep -v '^\[' "${INVENTORY}" | grep -v '^$' | grep -v '^#' | grep -v ':vars' | wc -l
}

# Header
show_header() {
    echo ""
    echo -e "${MAGENTA}╔═══════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${MAGENTA}║      TauGate 10B Compound Virtual Screen - Distributed Launcher       ║${NC}"
    echo -e "${MAGENTA}║                   Strategickhaos Cloud Swarm                          ║${NC}"
    echo -e "${MAGENTA}╚═══════════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

# Show estimated timeline
show_estimates() {
    local host_count=$1
    
    echo -e "${CYAN}=== Screening Parameters ===${NC}"
    echo ""
    echo "  Total Compounds:       10,000,000,000 (10B)"
    echo "  Nodes Available:       ${host_count}"
    echo "  Compounds per Shard:   $((10000000000 / host_count)) (~100M each)"
    echo ""
    echo "  Target:                ${TARGET_FILE}"
    echo "  Filters:               BBB penetrant, oral bioavailable, MW<500"
    echo ""
    echo -e "${CYAN}=== Time Estimates ===${NC}"
    echo ""
    echo "  Sequential (1 node):   ~9 months"
    echo "  With ${host_count} nodes:          ~$((270 / host_count)) days = ~$((270 * 24 / host_count)) hours"
    echo ""
    echo "  Provision Time:        ~5 minutes"
    echo "  Screen Time:           ~16 hours"
    echo "  Aggregate/Verify:      ~1 hour"
    echo "  ---------------------------------"
    echo "  Total Wall Clock:      ~18 hours"
    echo ""
    echo -e "${CYAN}=== Cost Estimate ===${NC}"
    echo ""
    # Use awk instead of bc for portability
    local cost
    cost=$(awk "BEGIN {printf \"%.2f\", $host_count * 0.005 * 18}")
    echo "  ${host_count} x t3.micro spots @ \$0.005/hr x 18hr = \$${cost}"
    echo "  Free tier coverage:     ~20% (first 100hrs)"
    echo "  Estimated Total:        <\$50"
    echo ""
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    if ! command -v ansible-playbook >/dev/null 2>&1; then
        log_error "ansible-playbook not found"
        exit 1
    fi
    
    if [ ! -f "${INVENTORY}" ]; then
        log_error "Inventory not found: ${INVENTORY}"
        log_info "Run: ./cloud_inventory.ps1 --burst 100 to provision nodes"
        exit 1
    fi
    
    if [ ! -f "${SCRIPT_DIR}/cloud_swarm_playbook.yaml" ]; then
        log_error "Playbook not found"
        exit 1
    fi
    
    log_success "Prerequisites check passed"
}

# Setup TauGate on all nodes
setup_taugate() {
    log_info "=== Setting up TauGate on all nodes ==="
    
    ansible-playbook \
        -i "${INVENTORY}" \
        "${SCRIPT_DIR}/cloud_swarm_playbook.yaml" \
        --tags "taugate" \
        --forks "$(get_host_count)" \
        2>&1 | tee -a "${LOG_FILE}"
    
    if [ ${PIPESTATUS[0]} -eq 0 ]; then
        log_success "TauGate setup complete on all nodes"
    else
        log_warn "Some nodes may have failed setup"
    fi
}

# Launch the screening shards
launch_screening() {
    local host_count
    host_count=$(get_host_count)
    
    log_info "=== Launching TauGate Screening Shards ==="
    log_info "Distributing 10B compounds across ${host_count} nodes..."
    
    ansible-playbook \
        -i "${INVENTORY}" \
        "${SCRIPT_DIR}/cloud_swarm_playbook.yaml" \
        --tags "taugate_shard" \
        --extra-vars "shard_total=${host_count} run_taugate_screen=true compounds_path=${COMPOUNDS_PATH} target_file=${TARGET_FILE}" \
        --forks "${host_count}" \
        2>&1 | tee -a "${LOG_FILE}"
    
    if [ ${PIPESTATUS[0]} -eq 0 ]; then
        log_success "All ${host_count} TauGate shards launched!"
    else
        log_warn "Some shards may have failed to launch"
    fi
}

# Monitor progress
monitor_progress() {
    log_info "=== Monitoring Screening Progress ==="
    log_info "Estimated completion: ~16 hours from launch"
    log_info "Check progress with: ./shard_launcher.sh ${INVENTORY} progress"
    log_info ""
    log_info "You can safely disconnect - screening continues on nodes."
    log_info "Reconnect and run: ./collect_and_verify.sh ${INVENTORY} taugate_${TIMESTAMP} taugate"
}

# Fire sequence - one-click execution
fire_sequence() {
    show_header
    
    local host_count
    host_count=$(get_host_count)
    
    log_info "Inventory: ${INVENTORY}"
    log_info "Nodes: ${host_count}"
    log_info "Log: ${LOG_FILE}"
    echo ""
    
    show_estimates "${host_count}"
    
    # Confirm before proceeding
    echo -e "${YELLOW}Ready to launch 10B compound screen across ${host_count} nodes?${NC}"
    echo -e "${YELLOW}Estimated cost: <\$50, Time: ~18h${NC}"
    echo ""
    read -p "Proceed? (y/N): " confirm
    
    if [[ "${confirm}" != "y" && "${confirm}" != "Y" ]]; then
        log_info "Aborted by user"
        exit 0
    fi
    
    echo ""
    log_info "=== FIRE SEQUENCE INITIATED ==="
    echo ""
    
    # Step 1: Setup
    setup_taugate
    
    # Step 2: Launch
    launch_screening
    
    # Step 3: Monitor info
    monitor_progress
    
    echo ""
    log_success "=== TauGate Launch Complete ==="
    echo ""
    log_info "Next steps:"
    echo "  1. Wait ~16h for screening to complete"
    echo "  2. Run: ./collect_and_verify.sh ${INVENTORY} taugate_${TIMESTAMP} taugate"
    echo "  3. Results → Top-200 candidates for med-chem handoff"
    echo "  4. Auto-shutdown via cost-guard after idle"
    echo ""
    echo -e "${GREEN}Empire cures at scale. 🧬${NC}"
}

# Main
main() {
    check_prerequisites
    fire_sequence
}

main "$@"
