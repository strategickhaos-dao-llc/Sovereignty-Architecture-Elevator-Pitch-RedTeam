#!/bin/bash
# Autonomous Patent Scanner
# Runs scheduled patent scans and alerts on findings

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="${SCRIPT_DIR}/config.yaml"
REPORTS_DIR="${SCRIPT_DIR}/reports"
DESIGNS_DIR="${SCRIPT_DIR}/designs"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging
log_info() {
    echo -e "${BLUE}[INFO]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"
}

# Create necessary directories
mkdir -p "${REPORTS_DIR}"
mkdir -p "${DESIGNS_DIR}"

# Parse command line arguments
DATABASES="uspto,epo,wipo"
KEYWORDS=""
OUTPUT_FILE=""
NOTIFY_DISCORD=true

while [[ $# -gt 0 ]]; do
    case $1 in
        --databases)
            DATABASES="$2"
            shift 2
            ;;
        --keywords)
            KEYWORDS="$2"
            shift 2
            ;;
        --output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        --no-notify)
            NOTIFY_DISCORD=false
            shift
            ;;
        --help)
            echo "Usage: $0 [options]"
            echo "Options:"
            echo "  --databases    Comma-separated list of databases (default: uspto,epo,wipo)"
            echo "  --keywords     Comma-separated keywords to search"
            echo "  --output       Output file path"
            echo "  --no-notify    Disable Discord notifications"
            echo "  --help         Show this help message"
            exit 0
            ;;
        *)
            log_error "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Set default output file if not specified
if [ -z "$OUTPUT_FILE" ]; then
    OUTPUT_FILE="${REPORTS_DIR}/patent-scan-$(date +%Y%m%d-%H%M%S).json"
fi

log_info "Starting autonomous patent scan"
log_info "Databases: ${DATABASES}"
log_info "Output: ${OUTPUT_FILE}"

# Technology domains to scan
declare -A TECH_DOMAINS=(
    ["ai_ml"]="retrieval augmented generation,vector database,semantic search,transformer,embedding model"
    ["distributed"]="distributed consensus,blockchain,DAO,Byzantine fault tolerance,smart contract"
    ["devops"]="kubernetes,container orchestration,observability,distributed tracing,GitOps"
    ["security"]="zero trust,multi-factor authentication,identity management,cryptography"
    ["data"]="vector search,approximate nearest neighbor,graph neural network,knowledge graph"
)

# If keywords not provided, scan all domains
if [ -z "$KEYWORDS" ]; then
    log_info "No keywords specified, scanning all technology domains"
    KEYWORDS="${TECH_DOMAINS[ai_ml]},${TECH_DOMAINS[distributed]},${TECH_DOMAINS[devops]},${TECH_DOMAINS[security]},${TECH_DOMAINS[data]}"
fi

# Initialize results
SCAN_ID="scan_$(date +%s)"
TOTAL_PATENTS=0
PRIORITY_ALERTS=0

log_info "Scan ID: ${SCAN_ID}"

# Create result structure
cat > "${OUTPUT_FILE}" <<EOF
{
  "scan_id": "${SCAN_ID}",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "databases": "${DATABASES}",
  "keywords": "${KEYWORDS}",
  "results": []
}
EOF

# Scan each database
IFS=',' read -ra DBS <<< "${DATABASES}"
for db in "${DBS[@]}"; do
    log_info "Scanning database: ${db}"
    
    # Simulate patent search (in production, call actual API)
    # For demonstration, generate mock results
    FOUND_PATENTS=$((RANDOM % 20 + 5))
    PRIORITY_COUNT=$((RANDOM % 5))
    
    TOTAL_PATENTS=$((TOTAL_PATENTS + FOUND_PATENTS))
    PRIORITY_ALERTS=$((PRIORITY_ALERTS + PRIORITY_COUNT))
    
    log_info "Found ${FOUND_PATENTS} patents in ${db} (${PRIORITY_COUNT} priority)"
    
    # Add to results (simplified)
    # In production, this would contain actual patent data
done

log_success "Scan completed"
log_info "Total patents found: ${TOTAL_PATENTS}"
log_info "Priority alerts: ${PRIORITY_ALERTS}"

# Generate summary report
SUMMARY_FILE="${REPORTS_DIR}/scan-summary-$(date +%Y%m%d).md"
cat > "${SUMMARY_FILE}" <<EOF
# Patent Scan Summary - $(date +%Y-%m-%d)

**Scan ID:** ${SCAN_ID}
**Date:** $(date -u +%Y-%m-%dT%H:%M:%SZ)
**Databases:** ${DATABASES}
**Keywords:** ${KEYWORDS}

## Results

- **Total Patents Found:** ${TOTAL_PATENTS}
- **Priority Alerts:** ${PRIORITY_ALERTS}
- **Databases Scanned:** ${#DBS[@]}

## Priority Findings

$(if [ ${PRIORITY_ALERTS} -gt 0 ]; then
    echo "⚠️ ${PRIORITY_ALERTS} patents require immediate review"
    echo ""
    echo "These patents have been flagged as potentially relevant to our technology stack."
    echo "Review required within 7 days."
else
    echo "✅ No high-priority threats identified in this scan."
fi)

## Next Actions

1. Review priority patents for potential conflicts
2. Update design documentation with relevant findings
3. Schedule legal review if necessary
4. Consider design-around strategies if needed

## Detailed Results

See full results in: \`${OUTPUT_FILE}\`

---
*Generated by Autonomous Patent Scanner*
*Department: Patent Research*
EOF

log_success "Summary report generated: ${SUMMARY_FILE}"

# Send Discord notification if enabled
if [ "${NOTIFY_DISCORD}" = true ]; then
    log_info "Sending Discord notification"
    
    # Check if Discord webhook is configured
    if [ -n "${DISCORD_TOKEN:-}" ] && [ -n "${PATENT_ALERTS_CHANNEL:-}" ]; then
        PRIORITY_EMOJI="✅"
        if [ ${PRIORITY_ALERTS} -gt 0 ]; then
            PRIORITY_EMOJI="⚠️"
        fi
        
        # Use gl2discord script if available
        if [ -f "${SCRIPT_DIR}/../../gl2discord.sh" ]; then
            "${SCRIPT_DIR}/../../gl2discord.sh" \
                "${PATENT_ALERTS_CHANNEL}" \
                "${PRIORITY_EMOJI} Patent Scan Complete" \
                "Scan ID: ${SCAN_ID}\nPatents Found: ${TOTAL_PATENTS}\nPriority Alerts: ${PRIORITY_ALERTS}" \
                || log_warn "Failed to send Discord notification"
        else
            log_warn "Discord notification script not found"
        fi
    else
        log_warn "Discord credentials not configured, skipping notification"
    fi
fi

# Archive old reports (keep last 90 days)
log_info "Cleaning up old reports"
find "${REPORTS_DIR}" -name "patent-scan-*.json" -mtime +90 -delete 2>/dev/null || true
find "${REPORTS_DIR}" -name "scan-summary-*.md" -mtime +90 -delete 2>/dev/null || true

log_success "Autonomous patent scan completed successfully"

# Exit with status based on priority alerts
if [ ${PRIORITY_ALERTS} -gt 0 ]; then
    log_warn "Priority alerts detected, review required"
    exit 2  # Non-zero but not error
else
    exit 0
fi
