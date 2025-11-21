#!/bin/bash
# Parallel Department Research Fetcher
# Processes all departments concurrently for efficient knowledge harvesting

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FETCH_SCRIPT="${SCRIPT_DIR}/fetch_research.sh"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Detect available departments
DEPARTMENTS=()
if [ -d "${SCRIPT_DIR}/departments" ]; then
    for file in "${SCRIPT_DIR}/departments"/*_links.txt; do
        if [ -f "$file" ]; then
            dept=$(basename "$file" | sed 's/_links.txt//')
            DEPARTMENTS+=("$dept")
        fi
    done
fi

if [ ${#DEPARTMENTS[@]} -eq 0 ]; then
    echo -e "${RED}Error: No department link files found${NC}"
    exit 1
fi

echo -e "${CYAN}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║  Distributed Department Research Automation              ║${NC}"
echo -e "${CYAN}║  Parallel Execution Mode                                 ║${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}Detected Departments:${NC}"
for dept in "${DEPARTMENTS[@]}"; do
    echo -e "  ${GREEN}✓${NC} $dept"
done
echo ""

# Usage options
usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -s, --sequential    Run departments sequentially (default: parallel)"
    echo "  -d, --departments   Specify departments to process (default: all)"
    echo "  -h, --help          Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                                    # Process all departments in parallel"
    echo "  $0 --sequential                       # Process all departments sequentially"
    echo "  $0 -d science,engineering             # Process specific departments"
    exit 0
}

# Parse arguments
PARALLEL=true
SELECTED_DEPTS=()

while [[ $# -gt 0 ]]; do
    case $1 in
        -s|--sequential)
            PARALLEL=false
            shift
            ;;
        -d|--departments)
            IFS=',' read -ra SELECTED_DEPTS <<< "$2"
            shift 2
            ;;
        -h|--help)
            usage
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            usage
            ;;
    esac
done

# Use selected departments or all
if [ ${#SELECTED_DEPTS[@]} -gt 0 ]; then
    DEPARTMENTS=("${SELECTED_DEPTS[@]}")
fi

echo -e "${YELLOW}Processing Mode:${NC} $([ "$PARALLEL" = true ] && echo "Parallel" || echo "Sequential")"
echo -e "${YELLOW}Departments to Process:${NC} ${#DEPARTMENTS[@]}"
echo ""

start_time=$(date +%s)
pids=()
failed_depts=()

# Process departments
if [ "$PARALLEL" = true ]; then
    echo -e "${BLUE}Starting parallel fetch for all departments...${NC}"
    echo ""
    
    for dept in "${DEPARTMENTS[@]}"; do
        echo -e "${CYAN}→ Launching fetch for: ${dept}${NC}"
        "$FETCH_SCRIPT" "$dept" > "${SCRIPT_DIR}/raw_pages/${dept}_fetch.log" 2>&1 &
        pids+=($!)
    done
    
    echo ""
    echo -e "${YELLOW}Waiting for all departments to complete...${NC}"
    
    # Wait for all background processes
    for i in "${!pids[@]}"; do
        pid=${pids[$i]}
        dept=${DEPARTMENTS[$i]}
        
        if wait "$pid"; then
            echo -e "${GREEN}✓${NC} ${dept} completed successfully"
        else
            echo -e "${RED}✗${NC} ${dept} failed"
            failed_depts+=("$dept")
        fi
    done
else
    echo -e "${BLUE}Starting sequential fetch...${NC}"
    echo ""
    
    for dept in "${DEPARTMENTS[@]}"; do
        echo -e "${CYAN}→ Processing: ${dept}${NC}"
        if "$FETCH_SCRIPT" "$dept"; then
            echo -e "${GREEN}✓${NC} ${dept} completed successfully"
        else
            echo -e "${RED}✗${NC} ${dept} failed"
            failed_depts+=("$dept")
        fi
        echo ""
    done
fi

end_time=$(date +%s)
duration=$((end_time - start_time))

# Final summary
echo ""
echo -e "${CYAN}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║  Batch Collection Summary                                ║${NC}"
echo -e "${CYAN}╠══════════════════════════════════════════════════════════╣${NC}"
echo -e "${CYAN}║${NC} Total Departments:  ${#DEPARTMENTS[@]}"
echo -e "${CYAN}║${NC} Successful:         ${GREEN}$((${#DEPARTMENTS[@]} - ${#failed_depts[@]}))${NC}"
echo -e "${CYAN}║${NC} Failed:             ${RED}${#failed_depts[@]}${NC}"
echo -e "${CYAN}║${NC} Total Duration:     ${duration}s"
echo -e "${CYAN}║${NC} Mode:               $([ "$PARALLEL" = true ] && echo "Parallel" || echo "Sequential")"
echo -e "${CYAN}╚══════════════════════════════════════════════════════════╝${NC}"

if [ ${#failed_depts[@]} -gt 0 ]; then
    echo ""
    echo -e "${YELLOW}Failed Departments:${NC}"
    for dept in "${failed_depts[@]}"; do
        echo -e "  ${RED}✗${NC} $dept (see ${SCRIPT_DIR}/raw_pages/${dept}_fetch.log)"
    done
fi

echo ""
echo -e "${GREEN}Research data collected in:${NC} ${SCRIPT_DIR}/raw_pages/"
echo -e "${YELLOW}Next Steps:${NC}"
echo "  1. Review collected data in raw_pages/"
echo "  2. Run post-processing to extract text"
echo "  3. Feed into embedding pipeline"
echo ""

# Create batch metadata
cat > "${SCRIPT_DIR}/raw_pages/batch_metadata.json" <<EOF
{
  "batch_timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "total_departments": ${#DEPARTMENTS[@]},
  "successful": $((${#DEPARTMENTS[@]} - ${#failed_depts[@]})),
  "failed": ${#failed_depts[@]},
  "duration_seconds": $duration,
  "mode": "$([ "$PARALLEL" = true ] && echo "parallel" || echo "sequential")",
  "departments_processed": [$(printf '"%s",' "${DEPARTMENTS[@]}" | sed 's/,$//')]
EOF

# Add failed_departments array if jq is available
if command -v jq &> /dev/null; then
    failed_json=$(printf '%s\n' "${failed_depts[@]}" | jq -R . | jq -s . 2>/dev/null || echo "[]")
else
    # Fallback JSON generation without jq
    if [ ${#failed_depts[@]} -eq 0 ]; then
        failed_json="[]"
    else
        failed_json="[$(printf '"%s",' "${failed_depts[@]}" | sed 's/,$//')]"
    fi
fi

cat >> "${SCRIPT_DIR}/raw_pages/batch_metadata.json" <<EOF
,
  "failed_departments": $failed_json
}
EOF

exit 0
