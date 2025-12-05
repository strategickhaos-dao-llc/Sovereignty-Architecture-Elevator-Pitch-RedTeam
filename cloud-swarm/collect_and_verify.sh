#!/bin/bash
# Collect and Verify - Pull shard results, verify hashes, aggregate, and OTS stamp
# Usage: ./collect_and_verify.sh [inventory_file] [run_name] [workload]
# Example: ./collect_and_verify.sh cloud_hosts.ini pid_ranco_20251128 pid_ranco

set -euo pipefail

# Configuration
INVENTORY=${1:-cloud_hosts.ini}
RUN_NAME=${2:-$(date +%Y%m%d_%H%M%S)}
WORKLOAD=${3:-pid_ranco}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="/tmp/swarm_results/${RUN_NAME}"
AGGREGATED_FILE="${OUTPUT_DIR}/aggregated_results.json"
PROVENANCE_FILE="${OUTPUT_DIR}/provenance_verified.log"
TIMESTAMP=$(date -Iseconds)

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
NC='\033[0m'

# Logging
log() { echo -e "[$(date -Iseconds)] $1"; }
log_info() { log "${BLUE}[INFO]${NC} $1"; }
log_success() { log "${GREEN}[SUCCESS]${NC} $1"; }
log_warn() { log "${YELLOW}[WARN]${NC} $1"; }
log_error() { log "${RED}[ERROR]${NC} $1"; }

# Get hosts from inventory
get_hosts() {
    grep -v '^\[' "${INVENTORY}" | grep -v '^$' | grep -v '^#' | grep -v ':vars' | awk '{print $1}'
}

# Create output directory
setup_output() {
    mkdir -p "${OUTPUT_DIR}/shards"
    log_info "Output directory: ${OUTPUT_DIR}"
}

# Collect shard results from all nodes
collect_shards() {
    log_info "=== Collecting Shard Results ==="
    
    local hosts
    hosts=($(get_hosts))
    local collected=0
    local failed=0
    
    for host in "${hosts[@]}"; do
        log_info "Collecting from ${host}..."
        
        # Determine file pattern based on workload
        local pattern
        case "${WORKLOAD}" in
            pid_ranco) pattern="/opt/strategickhaos/logs/pid_ranco_shard_*.json" ;;
            taugate) pattern="/opt/strategickhaos/logs/taugate_shard_*.json" ;;
            *) pattern="/opt/strategickhaos/logs/${WORKLOAD}_shard_*.json" ;;
        esac
        
        # Copy files via SCP
        if scp -o StrictHostKeyChecking=no -o ConnectTimeout=10 \
            "ubuntu@${host}:${pattern}" \
            "${OUTPUT_DIR}/shards/" 2>/dev/null; then
            ((collected++)) || true
            echo -e "  ${GREEN}✓${NC} ${host}: collected"
        else
            ((failed++)) || true
            echo -e "  ${RED}✗${NC} ${host}: failed to collect"
        fi
        
        # Also collect provenance log
        scp -o StrictHostKeyChecking=no -o ConnectTimeout=10 \
            "ubuntu@${host}:/opt/strategickhaos/uam/provenance.log" \
            "${OUTPUT_DIR}/shards/provenance_${host}.log" 2>/dev/null || true
    done
    
    log_info "Collection complete: ${collected} succeeded, ${failed} failed"
    return ${failed}
}

# Verify all shard hashes
verify_hashes() {
    log_info "=== Verifying Shard Hashes ==="
    
    local verified=0
    local mismatched=0
    local total=0
    
    # Initialize provenance log
    echo "# Provenance Verification - ${RUN_NAME}" > "${PROVENANCE_FILE}"
    echo "# Generated: ${TIMESTAMP}" >> "${PROVENANCE_FILE}"
    echo "# Format: shard_file|expected_hash|computed_hash|status" >> "${PROVENANCE_FILE}"
    echo "" >> "${PROVENANCE_FILE}"
    
    for shard_file in "${OUTPUT_DIR}/shards/"*_shard_*.json; do
        [ -f "${shard_file}" ] || continue
        ((total++)) || true
        
        local filename
        filename=$(basename "${shard_file}")
        
        # Compute hash
        local computed_hash
        if command -v b3sum >/dev/null 2>&1; then
            computed_hash=$(b3sum "${shard_file}" | cut -d' ' -f1)
        else
            computed_hash=$(sha256sum "${shard_file}" | cut -d' ' -f1)
        fi
        
        # Look for expected hash in provenance logs
        local expected_hash=""
        for prov_log in "${OUTPUT_DIR}/shards/"provenance_*.log; do
            [ -f "${prov_log}" ] || continue
            expected_hash=$(grep "${filename}" "${prov_log}" 2>/dev/null | tail -1 | cut -d'|' -f3 || true)
            [ -n "${expected_hash}" ] && break
        done
        
        # Verify
        if [ -n "${expected_hash}" ] && [ "${computed_hash}" = "${expected_hash}" ]; then
            echo -e "  ${GREEN}✓${NC} ${filename}: hash verified"
            echo "${filename}|${expected_hash}|${computed_hash}|VERIFIED" >> "${PROVENANCE_FILE}"
            ((verified++)) || true
        elif [ -z "${expected_hash}" ]; then
            echo -e "  ${YELLOW}?${NC} ${filename}: no expected hash found (first run?)"
            echo "${filename}|NONE|${computed_hash}|NEW" >> "${PROVENANCE_FILE}"
            ((verified++)) || true
        else
            echo -e "  ${RED}✗${NC} ${filename}: HASH MISMATCH!"
            echo "${filename}|${expected_hash}|${computed_hash}|MISMATCH" >> "${PROVENANCE_FILE}"
            ((mismatched++)) || true
        fi
    done
    
    echo "" >> "${PROVENANCE_FILE}"
    echo "# Summary: ${verified}/${total} verified, ${mismatched} mismatched" >> "${PROVENANCE_FILE}"
    
    log_info "Verification complete: ${verified}/${total} verified, ${mismatched} mismatched"
    
    if [ "${mismatched}" -gt 0 ]; then
        log_error "INTEGRITY WARNING: ${mismatched} shard(s) have hash mismatches!"
        return 1
    fi
    
    return 0
}

# Aggregate results
aggregate_results() {
    log_info "=== Aggregating Results ==="
    
    # Use Python for JSON aggregation
    python3 << PYTHON_SCRIPT
import json
import os
from pathlib import Path
from datetime import datetime

output_dir = "${OUTPUT_DIR}"
shards_dir = f"{output_dir}/shards"
aggregated_file = "${AGGREGATED_FILE}"
workload = "${WORKLOAD}"
run_name = "${RUN_NAME}"

# Collect all shard files
shard_files = sorted(Path(shards_dir).glob("*_shard_*.json"))

if not shard_files:
    print("No shard files found to aggregate")
    exit(1)

print(f"Found {len(shard_files)} shard files")

# Aggregate based on workload type
aggregated = {
    "meta": {
        "run_name": run_name,
        "workload": workload,
        "timestamp": datetime.now().isoformat(),
        "shard_count": len(shard_files),
        "status": "aggregated"
    },
    "shards": []
}

all_metrics = {}
all_results = []

for shard_file in shard_files:
    try:
        with open(shard_file) as f:
            shard_data = json.load(f)
        
        # Add to shards list
        aggregated["shards"].append({
            "file": shard_file.name,
            "shard_id": shard_data.get("meta", {}).get("shard_id", shard_data.get("shard_id")),
            "status": shard_data.get("status", "unknown")
        })
        
        # Aggregate metrics
        metrics = shard_data.get("metrics", {})
        for key, value in metrics.items():
            if key not in all_metrics:
                all_metrics[key] = []
            if isinstance(value, (int, float)):
                all_metrics[key].append(value)
        
        # Collect results for TauGate top-K
        if "results" in shard_data:
            all_results.extend(shard_data["results"])
            
    except Exception as e:
        print(f"Error processing {shard_file}: {e}")

# Compute aggregated metrics
aggregated["aggregated_metrics"] = {}
for key, values in all_metrics.items():
    if values:
        aggregated["aggregated_metrics"][key] = {
            "mean": sum(values) / len(values),
            "min": min(values),
            "max": max(values),
            "count": len(values)
        }

# For TauGate, keep top-K results
if workload == "taugate" and all_results:
    # Sort by score and keep top 200
    all_results.sort(key=lambda x: x.get("score", 0), reverse=True)
    aggregated["top_candidates"] = all_results[:200]
    print(f"Aggregated top {len(aggregated.get('top_candidates', []))} candidates")

# Write aggregated results
with open(aggregated_file, 'w') as f:
    json.dump(aggregated, f, indent=2)

print(f"Aggregated results written to {aggregated_file}")
PYTHON_SCRIPT

    if [ -f "${AGGREGATED_FILE}" ]; then
        log_success "Aggregation complete: ${AGGREGATED_FILE}"
        
        # Show summary
        echo ""
        log_info "Aggregated metrics:"
        python3 -c "
import json
with open('${AGGREGATED_FILE}') as f:
    data = json.load(f)
    metrics = data.get('aggregated_metrics', {})
    for key, values in metrics.items():
        print(f\"  {key}: mean={values['mean']:.4f}, min={values['min']:.4f}, max={values['max']:.4f}\")
"
    else
        log_error "Aggregation failed"
        return 1
    fi
}

# OpenTimestamps stamping
stamp_provenance() {
    log_info "=== OpenTimestamps Stamping ==="
    
    if ! command -v ots >/dev/null 2>&1; then
        log_warn "OpenTimestamps (ots) not installed. Skipping OTS stamping."
        log_info "Install with: pip install opentimestamps-client"
        return 0
    fi
    
    # Stamp the aggregated results
    log_info "Stamping aggregated results..."
    ots stamp "${AGGREGATED_FILE}" 2>&1 || true
    
    # Stamp the provenance log
    log_info "Stamping provenance verification log..."
    ots stamp "${PROVENANCE_FILE}" 2>&1 || true
    
    if [ -f "${AGGREGATED_FILE}.ots" ]; then
        log_success "OTS timestamp created: ${AGGREGATED_FILE}.ots"
        log_info "Calendar commit pending (~2h for Bitcoin confirmation)"
    else
        log_warn "OTS stamping may have failed or is pending"
    fi
}

# Generate summary report
generate_report() {
    log_info "=== Generating Summary Report ==="
    
    local report_file="${OUTPUT_DIR}/run_report.md"
    
    cat > "${report_file}" << EOF
# Cloud Swarm Run Report

**Run Name:** ${RUN_NAME}
**Workload:** ${WORKLOAD}
**Timestamp:** ${TIMESTAMP}

## Summary

- **Shards Collected:** $(ls -1 "${OUTPUT_DIR}/shards/"*_shard_*.json 2>/dev/null | wc -l)
- **Aggregated File:** ${AGGREGATED_FILE}
- **Provenance Log:** ${PROVENANCE_FILE}

## Verification Status

$(cat "${PROVENANCE_FILE}" | tail -1)

## Aggregated Metrics

\`\`\`json
$(python3 -c "import json; f=open('${AGGREGATED_FILE}'); d=json.load(f); print(json.dumps(d.get('aggregated_metrics', {}), indent=2))" 2>/dev/null || echo "{}")
\`\`\`

## Next Steps

1. Feed to ValorYield Phase 9 for yield router tuning
2. Wait for OTS calendar commit (~2h)
3. Update UAM Level 2 with artifacts

## Files

- \`aggregated_results.json\` - Combined shard outputs
- \`provenance_verified.log\` - Hash verification log
- \`shards/\` - Individual shard result files
EOF

    log_success "Report generated: ${report_file}"
}

# Main execution
main() {
    echo ""
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║     Strategickhaos Cloud Swarm - Collect & Verify         ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo ""
    
    log_info "Run: ${RUN_NAME}"
    log_info "Workload: ${WORKLOAD}"
    log_info "Inventory: ${INVENTORY}"
    echo ""
    
    # Check inventory
    if [ ! -f "${INVENTORY}" ]; then
        log_error "Inventory not found: ${INVENTORY}"
        exit 1
    fi
    
    setup_output
    collect_shards
    verify_hashes
    aggregate_results
    stamp_provenance
    generate_report
    
    echo ""
    log_success "=== Collection & Verification Complete ==="
    echo ""
    log_info "Output directory: ${OUTPUT_DIR}"
    log_info "Aggregated results: ${AGGREGATED_FILE}"
    log_info "Provenance log: ${PROVENANCE_FILE}"
    echo ""
    log_info "To feed to ValorYield Phase 9:"
    log_info "  python3 valoryield_phase9.py --input ${AGGREGATED_FILE}"
}

main "$@"
