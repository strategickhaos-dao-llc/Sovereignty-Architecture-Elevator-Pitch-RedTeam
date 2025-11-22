#!/bin/bash
# Strategickhaos Cluster Auto-Failover Script
# Automatically switches to backup nodes when primary fails

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
PRIMARY_NODE="nitro-lyra.tail-scale.ts.net"
BACKUP_NODE="athina-throne.tail-scale.ts.net"
CHECK_INTERVAL=60  # seconds
LOG_FILE="/var/log/strategickhaos-failover.log"
STATE_FILE="/var/run/strategickhaos-failover.state"

log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

check_node_health() {
    local node=$1
    
    # Try to reach Ollama API
    if curl -s -m 5 "http://$node:11434/api/health" >/dev/null 2>&1; then
        return 0  # Healthy
    else
        return 1  # Unhealthy
    fi
}

get_current_state() {
    if [ -f "$STATE_FILE" ]; then
        cat "$STATE_FILE"
    else
        echo "primary"
    fi
}

set_current_state() {
    echo "$1" > "$STATE_FILE"
}

switch_to_backup() {
    log_message "🔄 Switching to backup node: $BACKUP_NODE"
    
    # Update Open-WebUI configuration
    if docker ps | grep -q open-webui; then
        docker exec open-webui sh -c "
            if [ -f /app/backend/data/config.json ]; then
                sed -i 's|$PRIMARY_NODE|$BACKUP_NODE|g' /app/backend/data/config.json
            fi
        " 2>/dev/null || log_message "⚠️  Could not update Open-WebUI config"
        
        docker restart open-webui >/dev/null 2>&1
        log_message "✅ Open-WebUI restarted with backup endpoint"
    fi
    
    set_current_state "backup"
    log_message "📝 State changed to: backup"
}

switch_to_primary() {
    log_message "🔄 Switching back to primary node: $PRIMARY_NODE"
    
    # Update Open-WebUI configuration
    if docker ps | grep -q open-webui; then
        docker exec open-webui sh -c "
            if [ -f /app/backend/data/config.json ]; then
                sed -i 's|$BACKUP_NODE|$PRIMARY_NODE|g' /app/backend/data/config.json
            fi
        " 2>/dev/null || log_message "⚠️  Could not update Open-WebUI config"
        
        docker restart open-webui >/dev/null 2>&1
        log_message "✅ Open-WebUI restarted with primary endpoint"
    fi
    
    set_current_state "primary"
    log_message "📝 State changed to: primary"
}

monitor_cluster() {
    log_message "🚀 Starting cluster failover monitor"
    log_message "📊 Primary: $PRIMARY_NODE, Backup: $BACKUP_NODE"
    log_message "⏱️  Check interval: ${CHECK_INTERVAL}s"
    
    while true; do
        current_state=$(get_current_state)
        
        if [ "$current_state" = "primary" ]; then
            # Currently using primary, check if it's healthy
            if ! check_node_health "$PRIMARY_NODE"; then
                log_message "❌ Primary node unhealthy: $PRIMARY_NODE"
                
                # Check if backup is available
                if check_node_health "$BACKUP_NODE"; then
                    switch_to_backup
                else
                    log_message "❌ Backup node also unhealthy: $BACKUP_NODE"
                    log_message "⚠️  No healthy nodes available!"
                fi
            fi
        else
            # Currently using backup, check if primary has recovered
            if check_node_health "$PRIMARY_NODE"; then
                log_message "✅ Primary node recovered: $PRIMARY_NODE"
                switch_to_primary
            else
                # Still on backup, verify it's healthy
                if ! check_node_health "$BACKUP_NODE"; then
                    log_message "❌ Backup node unhealthy: $BACKUP_NODE"
                    log_message "⚠️  No healthy nodes available!"
                fi
            fi
        fi
        
        sleep "$CHECK_INTERVAL"
    done
}

install_service() {
    echo -e "${BLUE}Installing auto-failover as systemd service...${NC}"
    
    # Create log file
    sudo touch "$LOG_FILE"
    sudo chmod 666 "$LOG_FILE"
    
    # Create state file directory
    sudo mkdir -p "$(dirname "$STATE_FILE")"
    
    # Copy script to system location
    sudo cp "$0" /usr/local/bin/strategickhaos-failover.sh
    sudo chmod +x /usr/local/bin/strategickhaos-failover.sh
    
    # Create systemd service
    sudo tee /etc/systemd/system/strategickhaos-failover.service > /dev/null <<EOF
[Unit]
Description=Strategickhaos Cluster Auto-Failover
After=docker.service network-online.target
Wants=network-online.target
Requires=docker.service

[Service]
Type=simple
User=$USER
ExecStart=/usr/local/bin/strategickhaos-failover.sh monitor
Restart=always
RestartSec=10
StandardOutput=append:$LOG_FILE
StandardError=append:$LOG_FILE

[Install]
WantedBy=multi-user.target
EOF
    
    # Enable and start service
    sudo systemctl daemon-reload
    sudo systemctl enable strategickhaos-failover.service
    sudo systemctl start strategickhaos-failover.service
    
    echo -e "${GREEN}✅ Auto-failover service installed and started${NC}"
    echo -e "${YELLOW}View logs: sudo journalctl -u strategickhaos-failover -f${NC}"
    echo -e "${YELLOW}Or: tail -f $LOG_FILE${NC}"
}

uninstall_service() {
    echo -e "${YELLOW}Uninstalling auto-failover service...${NC}"
    
    sudo systemctl stop strategickhaos-failover.service 2>/dev/null || true
    sudo systemctl disable strategickhaos-failover.service 2>/dev/null || true
    sudo rm -f /etc/systemd/system/strategickhaos-failover.service
    sudo rm -f /usr/local/bin/strategickhaos-failover.sh
    sudo systemctl daemon-reload
    
    echo -e "${GREEN}✅ Auto-failover service uninstalled${NC}"
}

test_failover() {
    echo -e "${BLUE}Testing failover logic...${NC}"
    echo ""
    
    echo -e "${YELLOW}Checking primary node ($PRIMARY_NODE)...${NC}"
    if check_node_health "$PRIMARY_NODE"; then
        echo -e "${GREEN}✅ Primary node is healthy${NC}"
    else
        echo -e "${RED}❌ Primary node is unreachable${NC}"
    fi
    echo ""
    
    echo -e "${YELLOW}Checking backup node ($BACKUP_NODE)...${NC}"
    if check_node_health "$BACKUP_NODE"; then
        echo -e "${GREEN}✅ Backup node is healthy${NC}"
    else
        echo -e "${RED}❌ Backup node is unreachable${NC}"
    fi
    echo ""
    
    echo -e "${YELLOW}Current state: $(get_current_state)${NC}"
    echo ""
    
    read -p "Simulate failover to backup? [y/N]: " confirm
    if [[ $confirm =~ ^[Yy]$ ]]; then
        switch_to_backup
        echo ""
        echo -e "${GREEN}Failover to backup complete${NC}"
        echo ""
        read -p "Switch back to primary? [y/N]: " confirm2
        if [[ $confirm2 =~ ^[Yy]$ ]]; then
            switch_to_primary
            echo ""
            echo -e "${GREEN}Failback to primary complete${NC}"
        fi
    fi
}

show_status() {
    echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║   Strategickhaos Cluster Failover Status                  ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    # Check if service is running
    if systemctl is-active --quiet strategickhaos-failover.service 2>/dev/null; then
        echo -e "${GREEN}Service Status: ✅ Running${NC}"
    else
        echo -e "${YELLOW}Service Status: ○ Not Running${NC}"
    fi
    echo ""
    
    # Show current state
    echo -e "${YELLOW}Current Active Node: $(get_current_state)${NC}"
    echo ""
    
    # Check node health
    echo -e "${BLUE}Node Health:${NC}"
    if check_node_health "$PRIMARY_NODE"; then
        echo -e "  Primary ($PRIMARY_NODE): ${GREEN}✅ Healthy${NC}"
    else
        echo -e "  Primary ($PRIMARY_NODE): ${RED}❌ Unhealthy${NC}"
    fi
    
    if check_node_health "$BACKUP_NODE"; then
        echo -e "  Backup ($BACKUP_NODE): ${GREEN}✅ Healthy${NC}"
    else
        echo -e "  Backup ($BACKUP_NODE): ${RED}❌ Unhealthy${NC}"
    fi
    echo ""
    
    # Show recent log entries
    if [ -f "$LOG_FILE" ]; then
        echo -e "${BLUE}Recent Events (last 5):${NC}"
        tail -n 5 "$LOG_FILE" 2>/dev/null | while read line; do
            echo "  $line"
        done
    fi
}

show_help() {
    cat << EOF
Strategickhaos Cluster Auto-Failover Script

Usage: ./auto-failover.sh [command]

Commands:
  monitor       Start monitoring (runs continuously)
  install       Install as systemd service
  uninstall     Remove systemd service
  test          Test failover logic
  status        Show current status
  help          Show this help message

Configuration:
  Primary Node:   $PRIMARY_NODE
  Backup Node:    $BACKUP_NODE
  Check Interval: ${CHECK_INTERVAL}s
  Log File:       $LOG_FILE

Examples:
  # Test failover manually
  ./auto-failover.sh test

  # Install as persistent service
  ./auto-failover.sh install

  # Check status
  ./auto-failover.sh status

  # View live logs
  tail -f $LOG_FILE

EOF
}

# Main script logic
case "${1:-help}" in
    monitor)
        # Ensure we can create log file
        if [ ! -f "$LOG_FILE" ]; then
            sudo touch "$LOG_FILE" 2>/dev/null || LOG_FILE="./failover.log"
            sudo chmod 666 "$LOG_FILE" 2>/dev/null || true
        fi
        monitor_cluster
        ;;
    install)
        install_service
        ;;
    uninstall)
        uninstall_service
        ;;
    test)
        test_failover
        ;;
    status)
        show_status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo -e "${RED}✗ Unknown command: $1${NC}"
        echo ""
        show_help
        exit 1
        ;;
esac
