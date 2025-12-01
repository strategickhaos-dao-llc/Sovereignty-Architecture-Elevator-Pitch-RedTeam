#!/bin/bash
# view_recon_report.sh - Interactive Network Reconnaissance Report Viewer
# Displays the latest network recon report in a readable format

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

LATEST_REPORT="recon/reports/latest_network_scan/recon_report.md"

if [ ! -f "$LATEST_REPORT" ]; then
    echo -e "${RED}Error:${NC} No reconnaissance report found at $LATEST_REPORT"
    echo ""
    echo "Run ${GREEN}./network_recon.sh${NC} first to generate a report."
    exit 1
fi

banner() {
    echo -e "${CYAN}"
    echo "╔════════════════════════════════════════════════════════════════════════════╗"
    echo "║               📊 NETWORK RECONNAISSANCE REPORT VIEWER                     ║"
    echo "║                    Strategic Khaos Infrastructure                         ║"
    echo "╚════════════════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Display menu
show_menu() {
    echo -e "${YELLOW}Report Sections:${NC}"
    echo "  1) Executive Summary"
    echo "  2) Docker Networks"
    echo "  3) Container Inventory"
    echo "  4) Port Mapping"
    echo "  5) Service Health"
    echo "  6) Docker Compose Stacks"
    echo "  7) Environment Config"
    echo "  8) Requirements Check"
    echo "  9) Network Topology"
    echo " 10) Resource Usage"
    echo " 11) Security Analysis"
    echo " 12) Recommendations"
    echo " 13) View Full Report"
    echo "  q) Quit"
    echo ""
}

# Extract and display section
show_section() {
    local section="$1"
    
    echo -e "${GREEN}═══════════════════════════════════════════════════════════════════════${NC}"
    
    case "$section" in
        1)
            awk '/## 📊 Executive Summary/,/## 💡 Recommendations/' "$LATEST_REPORT" | head -n -1
            ;;
        2)
            awk '/## 🌐 Docker Networks/,/## 🐳 Container Inventory/' "$LATEST_REPORT" | head -n -1
            ;;
        3)
            awk '/## 🐳 Container Inventory/,/## 🔌 Port Mapping/' "$LATEST_REPORT" | head -n -1
            ;;
        4)
            awk '/## 🔌 Port Mapping/,/## 🏥 Service Health/' "$LATEST_REPORT" | head -n -1
            ;;
        5)
            awk '/## 🏥 Service Health/,/## 📦 Docker Compose/' "$LATEST_REPORT" | head -n -1
            ;;
        6)
            awk '/## 📦 Docker Compose/,/## ⚙️ Environment/' "$LATEST_REPORT" | head -n -1
            ;;
        7)
            awk '/## ⚙️ Environment/,/## 📋 Infrastructure Requirements/' "$LATEST_REPORT" | head -n -1
            ;;
        8)
            awk '/## 📋 Infrastructure Requirements/,/## 🗺️ Network Topology/' "$LATEST_REPORT" | head -n -1
            ;;
        9)
            awk '/## 🗺️ Network Topology/,/## 💾 Resource Usage/' "$LATEST_REPORT" | head -n -1
            ;;
        10)
            awk '/## 💾 Resource Usage/,/## 🔒 Security/' "$LATEST_REPORT" | head -n -1
            ;;
        11)
            awk '/## 🔒 Security/,/## 💡 Recommendations/' "$LATEST_REPORT" | head -n -1
            ;;
        12)
            awk '/## 💡 Recommendations/,/## 📊 Executive Summary/' "$LATEST_REPORT" | head -n -1
            ;;
        13)
            cat "$LATEST_REPORT"
            ;;
        *)
            echo "Invalid selection"
            return
            ;;
    esac
    
    echo -e "${GREEN}═══════════════════════════════════════════════════════════════════════${NC}"
    echo ""
}

# Main interactive loop
main() {
    banner
    
    echo -e "${CYAN}Latest Report:${NC} $(basename $(dirname $(readlink -f "$LATEST_REPORT")))"
    echo ""
    
    if [ "${1:-}" == "--summary" ] || [ "${1:-}" == "-s" ]; then
        # Just show summary
        show_section 1
        exit 0
    fi
    
    if [ "${1:-}" == "--full" ] || [ "${1:-}" == "-f" ]; then
        # Show full report
        show_section 13
        exit 0
    fi
    
    # Interactive mode
    while true; do
        show_menu
        read -p "Select a section (1-13, q to quit): " choice
        
        case "$choice" in
            q|Q)
                echo "Goodbye!"
                exit 0
                ;;
            [1-9]|1[0-3])
                clear
                banner
                show_section "$choice"
                read -p "Press Enter to continue..."
                clear
                banner
                ;;
            *)
                echo -e "${RED}Invalid selection. Please try again.${NC}"
                sleep 1
                ;;
        esac
    done
}

# Show help
if [ "${1:-}" == "--help" ] || [ "${1:-}" == "-h" ]; then
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -s, --summary   Show executive summary only"
    echo "  -f, --full      Show full report"
    echo "  -h, --help      Show this help message"
    echo "  (no options)    Interactive menu mode"
    echo ""
    exit 0
fi

main "$@"
