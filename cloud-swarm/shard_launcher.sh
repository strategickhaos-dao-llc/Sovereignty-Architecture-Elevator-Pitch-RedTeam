#!/bin/bash
# Shard Launcher - Unix launcher to fan out N PID-RANCO shards across inventory
# Usage: ./shard_launcher.sh [inventory_file] [workload]
# Example: ./shard_launcher.sh cloud_hosts.ini pid_ranco

set -euo pipefail

# Configuration
INVENTORY=${1:-cloud_hosts.ini}
WORKLOAD=${2:-pid_ranco}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="/tmp/shard_launcher_${TIMESTAMP}.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log() {
    local msg="[$(date -Iseconds)] $1"
    echo -e "${msg}"
    echo "${msg}" >> "${LOG_FILE}"
}

log_info() { log "${BLUE}[INFO]${NC} $1"; }
log_success() { log "${GREEN}[SUCCESS]${NC} $1"; }
log_warn() { log "${YELLOW}[WARN]${NC} $1"; }
log_error() { log "${RED}[ERROR]${NC} $1"; }

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    if ! command -v ansible-playbook >/dev/null 2>&1; then
        log_error "ansible-playbook not found. Please install Ansible."
        exit 1
    fi
    
    if [ ! -f "${INVENTORY}" ]; then
        log_error "Inventory file not found: ${INVENTORY}"
        log_info "Run cloud_inventory.ps1 first to discover nodes."
        exit 1
    fi
    
    if [ ! -f "${SCRIPT_DIR}/cloud_swarm_playbook.yaml" ]; then
        log_error "Playbook not found: ${SCRIPT_DIR}/cloud_swarm_playbook.yaml"
        exit 1
    fi
    
    log_success "Prerequisites check passed"
}

# Parse inventory to get host count
get_host_count() {
    local hosts
    hosts=$(grep -v '^\[' "${INVENTORY}" | grep -v '^$' | grep -v '^#' | grep -v ':vars' | wc -l)
    echo "${hosts}"
}

# Get hosts from inventory
get_hosts() {
    grep -v '^\[' "${INVENTORY}" | grep -v '^$' | grep -v '^#' | grep -v ':vars' | awk '{print $1}'
}

# Launch PID-RANCO shards
launch_pid_ranco() {
    local host_count
    host_count=$(get_host_count)
    
    log_info "=== PID-RANCO Shard Launcher ==="
    log_info "Inventory: ${INVENTORY}"
    log_info "Total nodes: ${host_count}"
    log_info "Workload: ${WORKLOAD}"
    log_info "Log file: ${LOG_FILE}"
    echo ""
    
    if [ "${host_count}" -eq 0 ]; then
        log_error "No hosts found in inventory"
        exit 1
    fi
    
    log_info "Launching ${host_count} shards in parallel..."
    
    # Calculate estimated time
    local estimated_minutes=$((11 + (host_count / 10)))
    log_info "Estimated completion: ~${estimated_minutes} minutes"
    echo ""
    
    # Run Ansible playbook with all hosts in parallel
    log_info "Starting Ansible playbook execution..."
    
    ansible-playbook \
        -i "${INVENTORY}" \
        "${SCRIPT_DIR}/cloud_swarm_playbook.yaml" \
        --tags "pid_ranco" \
        --extra-vars "shard_total=${host_count}" \
        --forks "${host_count}" \
        2>&1 | tee -a "${LOG_FILE}"
    
    local ansible_status=${PIPESTATUS[0]}
    
    if [ "${ansible_status}" -eq 0 ]; then
        log_success "All ${host_count} shards launched successfully!"
    else
        log_warn "Some shards may have failed. Check log: ${LOG_FILE}"
    fi
    
    return ${ansible_status}
}

# Launch TauGate shards
launch_taugate() {
    local host_count
    host_count=$(get_host_count)
    
    log_info "=== TauGate Shard Launcher ==="
    log_info "Inventory: ${INVENTORY}"
    log_info "Total nodes: ${host_count}"
    log_info "Workload: ${WORKLOAD}"
    echo ""
    
    log_info "Launching TauGate shards for 10B compound screening..."
    
    ansible-playbook \
        -i "${INVENTORY}" \
        "${SCRIPT_DIR}/cloud_swarm_playbook.yaml" \
        --tags "taugate_shard" \
        --extra-vars "shard_total=${host_count} run_taugate_screen=true" \
        --forks "${host_count}" \
        2>&1 | tee -a "${LOG_FILE}"
    
    local ansible_status=${PIPESTATUS[0]}
    
    if [ "${ansible_status}" -eq 0 ]; then
        log_success "TauGate shards launched!"
    else
        log_warn "Some TauGate shards may have failed."
    fi
    
    return ${ansible_status}
}

# Manual SSH-based shard launch (fallback)
launch_manual() {
    local host_count
    host_count=$(get_host_count)
    local hosts
    hosts=($(get_hosts))
    
    log_info "=== Manual Shard Launcher (SSH) ==="
    log_info "Launching ${host_count} shards via direct SSH..."
    echo ""
    
    local i=0
    local pids=()
    
    for host in "${hosts[@]}"; do
        log_info "Launching shard $i on ${host}..."
        
        ssh -o StrictHostKeyChecking=no -o ConnectTimeout=10 \
            "ubuntu@${host}" \
            "/opt/strategickhaos/scripts/run_pid_ranco.sh $i ${host_count}" \
            >> "${LOG_FILE}" 2>&1 &
        
        pids+=($!)
        ((i++)) || true
    done
    
    log_info "Waiting for ${#pids[@]} shards to complete..."
    
    local failed=0
    for pid in "${pids[@]}"; do
        if ! wait "${pid}"; then
            ((failed++)) || true
        fi
    done
    
    if [ "${failed}" -eq 0 ]; then
        log_success "All ${host_count} shards completed successfully!"
    else
        log_warn "${failed}/${host_count} shards failed"
    fi
}

# Display progress
show_progress() {
    log_info "=== Shard Progress ==="
    
    local hosts
    hosts=($(get_hosts))
    local completed=0
    
    for host in "${hosts[@]}"; do
        local status
        status=$(ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 \
            "ubuntu@${host}" \
            "ls /opt/strategickhaos/logs/pid_ranco_shard_*.json 2>/dev/null | wc -l" \
            2>/dev/null || echo "0")
        
        if [ "${status}" -gt 0 ]; then
            echo -e "${GREEN}✓${NC} ${host}: ${status} shard(s) complete"
            ((completed++)) || true
        else
            echo -e "${YELLOW}○${NC} ${host}: in progress"
        fi
    done
    
    echo ""
    log_info "Progress: ${completed}/${#hosts[@]} nodes reporting results"
}

# Main execution
main() {
    echo ""
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║     Strategickhaos Cloud Swarm - Shard Launcher           ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo ""
    
    check_prerequisites
    
    case "${WORKLOAD}" in
        pid_ranco|pidranco)
            launch_pid_ranco
            ;;
        taugate)
            launch_taugate
            ;;
        manual)
            launch_manual
            ;;
        progress|status)
            show_progress
            ;;
        *)
            log_error "Unknown workload: ${WORKLOAD}"
            log_info "Available workloads: pid_ranco, taugate, manual, progress"
            exit 1
            ;;
    esac
    
    echo ""
    log_info "=== Launcher Complete ==="
    log_info "Log file: ${LOG_FILE}"
    log_info "Next steps:"
    log_info "  - Check progress: ./shard_launcher.sh ${INVENTORY} progress"
    log_info "  - Collect results: ./collect_and_verify.sh ${INVENTORY} ${WORKLOAD}_${TIMESTAMP}"
    log_info "  - Trigger cost-guard: ansible-playbook -i ${INVENTORY} cloud_swarm_playbook.yaml --tags cost_guard"
}

main "$@"
