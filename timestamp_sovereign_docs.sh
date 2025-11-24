#!/bin/bash
#
# timestamp_sovereign_docs.sh
# Automate OpenTimestamps workflow for sovereign documents
#
# Usage:
#   ./timestamp_sovereign_docs.sh stamp     # Create new timestamps
#   ./timestamp_sovereign_docs.sh upgrade   # Upgrade pending timestamps
#   ./timestamp_sovereign_docs.sh verify    # Verify all timestamps
#   ./timestamp_sovereign_docs.sh info      # Show timestamp details
#   ./timestamp_sovereign_docs.sh all       # Run complete workflow

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Files to timestamp (sovereign documents)
SOVEREIGN_FILES=(
    "SOVEREIGN_MANIFEST_v1.0.md"
    "README.md"
    "SECURITY.md"
    "dao_record_v1.0.yaml"
    "CONTRIBUTORS.md"
)

# Check if ots client is installed
check_ots_installed() {
    if ! command -v ots &> /dev/null; then
        echo -e "${RED}Error: OpenTimestamps client not found${NC}"
        echo "Install with: pip install opentimestamps-client"
        exit 1
    fi
}

# Print banner
print_banner() {
    echo -e "${BLUE}================================================${NC}"
    echo -e "${BLUE}  OpenTimestamps Sovereign Document Workflow${NC}"
    echo -e "${BLUE}================================================${NC}"
    echo ""
}

# Stamp all sovereign documents
stamp_documents() {
    echo -e "${YELLOW}Stamping sovereign documents...${NC}"
    echo ""
    
    local count=0
    for file in "${SOVEREIGN_FILES[@]}"; do
        if [ -f "$file" ]; then
            echo -e "Timestamping: ${GREEN}$file${NC}"
            
            # Check if already timestamped
            if [ -f "${file}.ots" ]; then
                echo -e "  ${YELLOW}⚠ Timestamp file already exists: ${file}.ots${NC}"
                read -p "  Overwrite? (y/N): " -n 1 -r
                echo
                if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                    echo -e "  ${BLUE}Skipping${NC}"
                    continue
                fi
            fi
            
            # Create timestamp
            if ots stamp "$file" 2>&1 | tee /tmp/ots_output.txt; then
                echo -e "  ${GREEN}✓ Created: ${file}.ots${NC}"
                ((count++))
            else
                echo -e "  ${RED}✗ Failed to timestamp${NC}"
            fi
            echo ""
        else
            echo -e "${YELLOW}⚠ File not found: $file${NC}"
            echo ""
        fi
    done
    
    echo -e "${GREEN}Stamped $count document(s)${NC}"
    echo -e "${BLUE}Note: Run './timestamp_sovereign_docs.sh upgrade' after 1-2 hours to get Bitcoin confirmation${NC}"
    echo ""
}

# Upgrade all pending timestamps
upgrade_timestamps() {
    echo -e "${YELLOW}Upgrading timestamps to Bitcoin blockchain...${NC}"
    echo ""
    
    local upgraded=0
    local pending=0
    
    for file in "${SOVEREIGN_FILES[@]}"; do
        local ots_file="${file}.ots"
        if [ -f "$ots_file" ]; then
            echo -e "Upgrading: ${GREEN}$ots_file${NC}"
            
            # Try to upgrade
            if ots upgrade "$ots_file" 2>&1 | tee /tmp/ots_upgrade.txt | grep -q "Success"; then
                echo -e "  ${GREEN}✓ Upgraded successfully${NC}"
                ((upgraded++))
            elif grep -q "Pending" /tmp/ots_upgrade.txt; then
                echo -e "  ${YELLOW}⏳ Still pending Bitcoin confirmation${NC}"
                ((pending++))
            else
                echo -e "  ${BLUE}ℹ Already up to date${NC}"
            fi
            echo ""
        fi
    done
    
    echo -e "${GREEN}Upgraded: $upgraded${NC}"
    echo -e "${YELLOW}Pending: $pending${NC}"
    
    if [ $pending -gt 0 ]; then
        echo -e "${BLUE}Note: Pending timestamps will be confirmed after Bitcoin block inclusion (usually 1-2 hours)${NC}"
    fi
    echo ""
}

# Verify all timestamps
verify_timestamps() {
    echo -e "${YELLOW}Verifying all timestamps...${NC}"
    echo ""
    
    local verified=0
    local pending=0
    local failed=0
    
    for file in "${SOVEREIGN_FILES[@]}"; do
        local ots_file="${file}.ots"
        if [ -f "$ots_file" ]; then
            echo -e "Verifying: ${GREEN}$ots_file${NC}"
            
            # Verify timestamp
            if ots verify "$ots_file" 2>&1 | tee /tmp/ots_verify.txt | grep -q "Success"; then
                local block=$(grep "block" /tmp/ots_verify.txt | grep -oP '\d+' | head -1)
                local date=$(grep "as of" /tmp/ots_verify.txt | grep -oP '\d{4}-\d{2}-\d{2}' || echo "unknown")
                echo -e "  ${GREEN}✓ Verified${NC}"
                echo -e "    Block: $block | Date: $date"
                ((verified++))
            elif grep -q "Pending" /tmp/ots_verify.txt; then
                echo -e "  ${YELLOW}⏳ Pending Bitcoin confirmation${NC}"
                ((pending++))
            else
                echo -e "  ${RED}✗ Verification failed${NC}"
                ((failed++))
            fi
            echo ""
        else
            echo -e "${YELLOW}⚠ Timestamp not found: $ots_file${NC}"
            echo ""
        fi
    done
    
    echo -e "Summary:"
    echo -e "  ${GREEN}Verified: $verified${NC}"
    echo -e "  ${YELLOW}Pending: $pending${NC}"
    echo -e "  ${RED}Failed: $failed${NC}"
    echo ""
}

# Show detailed info for all timestamps
show_info() {
    echo -e "${YELLOW}Timestamp details...${NC}"
    echo ""
    
    for file in "${SOVEREIGN_FILES[@]}"; do
        local ots_file="${file}.ots"
        if [ -f "$ots_file" ]; then
            echo -e "${GREEN}═══════════════════════════════════════${NC}"
            echo -e "${GREEN}File: $ots_file${NC}"
            echo -e "${GREEN}═══════════════════════════════════════${NC}"
            ots info "$ots_file"
            echo ""
        fi
    done
}

# Generate report
generate_report() {
    local report_file="timestamp_report_$(date +%Y%m%d_%H%M%S).txt"
    
    echo -e "${YELLOW}Generating timestamp report...${NC}"
    echo ""
    
    {
        echo "========================================"
        echo "OpenTimestamps Verification Report"
        echo "Generated: $(date)"
        echo "========================================"
        echo ""
        
        for file in "${SOVEREIGN_FILES[@]}"; do
            local ots_file="${file}.ots"
            if [ -f "$ots_file" ]; then
                echo "Document: $file"
                echo "----------------------------------------"
                
                # File hash
                echo "SHA256: $(sha256sum "$file" | cut -d' ' -f1)"
                
                # Verification status
                if ots verify "$ots_file" 2>&1 | grep -q "Success"; then
                    echo "Status: ✓ VERIFIED"
                    ots verify "$ots_file" 2>&1 | grep "block\|as of"
                elif ots verify "$ots_file" 2>&1 | grep -q "Pending"; then
                    echo "Status: ⏳ PENDING"
                else
                    echo "Status: ✗ VERIFICATION FAILED"
                fi
                
                echo ""
            fi
        done
        
        echo "========================================"
        echo "End of Report"
        echo "========================================"
    } > "$report_file"
    
    echo -e "${GREEN}Report generated: $report_file${NC}"
    echo ""
}

# Run complete workflow
run_complete_workflow() {
    print_banner
    
    echo -e "${BLUE}Running complete OpenTimestamps workflow...${NC}"
    echo ""
    
    # Step 1: Verify existing timestamps
    echo -e "${BLUE}Step 1: Verify existing timestamps${NC}"
    verify_timestamps
    
    read -p "Continue to stamping? (Y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Nn]$ ]]; then
        exit 0
    fi
    
    # Step 2: Stamp new documents
    echo -e "${BLUE}Step 2: Stamp documents${NC}"
    stamp_documents
    
    read -p "Continue to upgrade? (Y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Nn]$ ]]; then
        exit 0
    fi
    
    # Step 3: Upgrade timestamps
    echo -e "${BLUE}Step 3: Upgrade timestamps${NC}"
    upgrade_timestamps
    
    # Step 4: Generate report
    echo -e "${BLUE}Step 4: Generate report${NC}"
    generate_report
    
    echo -e "${GREEN}Workflow complete!${NC}"
}

# Show usage
show_usage() {
    echo "Usage: $0 {stamp|upgrade|verify|info|report|all}"
    echo ""
    echo "Commands:"
    echo "  stamp    - Create timestamps for sovereign documents"
    echo "  upgrade  - Upgrade pending timestamps with Bitcoin confirmation"
    echo "  verify   - Verify all timestamps"
    echo "  info     - Show detailed timestamp information"
    echo "  report   - Generate verification report"
    echo "  all      - Run complete workflow (interactive)"
    echo ""
    echo "Documents timestamped:"
    for file in "${SOVEREIGN_FILES[@]}"; do
        echo "  - $file"
    done
    echo ""
}

# Main script
main() {
    check_ots_installed
    print_banner
    
    case "${1:-}" in
        stamp)
            stamp_documents
            ;;
        upgrade)
            upgrade_timestamps
            ;;
        verify)
            verify_timestamps
            ;;
        info)
            show_info
            ;;
        report)
            generate_report
            ;;
        all)
            run_complete_workflow
            ;;
        help|--help|-h)
            show_usage
            ;;
        *)
            show_usage
            exit 1
            ;;
    esac
}

main "$@"
