#!/bin/bash
#
# Quick Start Script for Honeypot Security System
# Deploys the invite-only honeypot infrastructure
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${SCRIPT_DIR}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Banner
echo -e "${GREEN}"
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                                                                ║"
echo "║     🔥 HONEYPOT SECURITY SYSTEM - OPSPEC DEPARTMENT 🔥        ║"
echo "║                                                                ║"
echo "║     Invite-Only Access | Leak Detection | Forensic Tracking   ║"
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker is not installed${NC}"
    exit 1
fi

if ! command -v docker compose &> /dev/null && ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Error: Docker Compose is not installed${NC}"
    exit 1
fi

# Function to show menu
show_menu() {
    echo ""
    echo -e "${BLUE}What would you like to do?${NC}"
    echo ""
    echo "  1) 🚀 Start Honeypot System"
    echo "  2) 🛑 Stop Honeypot System"
    echo "  3) 📊 View Logs (Real-time)"
    echo "  4) 📈 Show Status"
    echo "  5) 🔍 View Events Log"
    echo "  6) 📦 Build Lab Packages"
    echo "  7) 🧹 Clean Up (Remove all containers and data)"
    echo "  8) ❌ Exit"
    echo ""
    echo -n "Enter choice [1-8]: "
}

# Start system
start_honeypot() {
    echo -e "${YELLOW}🚀 Starting Honeypot Security System...${NC}"
    
    # Create required directories
    mkdir -p logs honeypot-keys honeypot-repos
    
    # Start services
    docker compose -f docker-compose-honeypot.yml up -d
    
    echo ""
    echo -e "${GREEN}✅ Honeypot system started successfully!${NC}"
    echo ""
    echo "Access points:"
    echo "  - Landing Page: http://localhost:8080"
    echo "  - Git Server: ssh://git@localhost:2222"
    echo ""
    echo "Monitoring:"
    echo "  docker compose -f docker-compose-honeypot.yml logs -f visitor-logger"
    echo ""
}

# Stop system
stop_honeypot() {
    echo -e "${YELLOW}🛑 Stopping Honeypot Security System...${NC}"
    docker compose -f docker-compose-honeypot.yml down
    echo -e "${GREEN}✅ System stopped${NC}"
}

# View logs
view_logs() {
    echo -e "${YELLOW}📊 Streaming logs (Ctrl+C to exit)...${NC}"
    docker compose -f docker-compose-honeypot.yml logs -f visitor-logger
}

# Show status
show_status() {
    echo -e "${YELLOW}📈 System Status:${NC}"
    echo ""
    docker compose -f docker-compose-honeypot.yml ps
    echo ""
    
    # Check if logs exist
    if [ -f "logs/honeypot_events.log" ]; then
        event_count=$(wc -l < logs/honeypot_events.log)
        echo -e "${BLUE}Total events logged: ${event_count}${NC}"
    fi
}

# View events
view_events() {
    if [ ! -f "logs/honeypot_events.log" ]; then
        echo -e "${YELLOW}No events logged yet${NC}"
        return
    fi
    
    echo -e "${YELLOW}📋 Recent Honeypot Events:${NC}"
    echo ""
    
    # Show last 20 events formatted
    if command -v jq &> /dev/null; then
        tail -n 20 logs/honeypot_events.log | jq -r '. | "\(.timestamp) - \(.event_type) - IP: \(.data.ip)"'
    else
        tail -n 20 logs/honeypot_events.log
    fi
}

# Build packages
build_packages() {
    echo -e "${YELLOW}📦 Building lab packages...${NC}"
    
    if [ ! -f "scripts/build-lab-packages.sh" ]; then
        echo -e "${RED}Error: Build script not found${NC}"
        return
    fi
    
    bash scripts/build-lab-packages.sh
}

# Clean up
cleanup() {
    echo -e "${YELLOW}🧹 Cleaning up...${NC}"
    echo -e "${RED}Warning: This will remove all containers and data!${NC}"
    echo -n "Are you sure? (y/N): "
    read -r confirm
    
    if [[ "$confirm" =~ ^[Yy]$ ]]; then
        docker compose -f docker-compose-honeypot.yml down -v
        echo -e "${GREEN}✅ Cleanup complete${NC}"
    else
        echo "Cancelled"
    fi
}

# Main loop
main() {
    while true; do
        show_menu
        read -r choice
        
        case $choice in
            1)
                start_honeypot
                ;;
            2)
                stop_honeypot
                ;;
            3)
                view_logs
                ;;
            4)
                show_status
                ;;
            5)
                view_events
                ;;
            6)
                build_packages
                ;;
            7)
                cleanup
                ;;
            8)
                echo -e "${GREEN}Goodbye!${NC}"
                exit 0
                ;;
            *)
                echo -e "${RED}Invalid choice. Please try again.${NC}"
                ;;
        esac
        
        echo ""
        echo -n "Press Enter to continue..."
        read -r
    done
}

# Run main
main
