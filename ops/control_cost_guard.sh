#!/bin/bash
# control_cost_guard.sh
# Cloud Swarm Operations - Cost Guard Auto-Shutdown Controller
# Strategickhaos DAO LLC — Automated Cost Control for Cloud Resources
#
# Usage: ./control_cost_guard.sh <inventory_file> <idle_minutes>
# Example: ./control_cost_guard.sh cloud_hosts.ini 15
#
# This script monitors cloud swarm nodes and shuts down idle instances
# to prevent unnecessary cloud costs.

set -euo pipefail

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Configuration
INVENTORY="${1:-}"
IDLE_THRESHOLD_MINUTES="${2:-15}"
LOG_FILE="/var/log/cost-guard.log"
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)

# Validate inputs
if [[ -z "$INVENTORY" ]]; then
    echo -e "${RED}❌ Usage: $0 <inventory_file> [idle_minutes]${NC}"
    exit 1
fi

if [[ ! -f "$INVENTORY" ]]; then
    echo -e "${RED}❌ Inventory file not found: $INVENTORY${NC}"
    exit 1
fi

log() {
    local level="$1"
    local message="$2"
    echo "[$TIMESTAMP] [$level] $message" | tee -a "$LOG_FILE" 2>/dev/null || echo "[$TIMESTAMP] [$level] $message"
}

log "INFO" "Cost Guard starting - Idle threshold: ${IDLE_THRESHOLD_MINUTES}m"

# Function to check if host is idle
check_host_idle() {
    local host="$1"
    # Note: threshold_minutes is handled at the caller level
    
    # Check load average and running processes
    local idle_check
    idle_check=$(ssh -o ConnectTimeout=5 -o BatchMode=yes "$host" \
        "uptime | awk -F'load average:' '{print \$2}' | awk -F',' '{print \$1}'" 2>/dev/null) || return 1
    
    # Convert load to comparable format (remove leading spaces)
    idle_check=$(echo "$idle_check" | tr -d ' ')
    
    # Check if load is below 0.1 (essentially idle)
    if awk "BEGIN {exit !($idle_check < 0.1)}"; then
        # Additional check: verify no swarm jobs are running
        local jobs_running
        jobs_running=$(ssh -o ConnectTimeout=5 -o BatchMode=yes "$host" \
            "pgrep -c 'swarm|compute|worker' 2>/dev/null || echo 0" 2>/dev/null) || jobs_running=0
        
        if [[ "$jobs_running" -eq 0 ]]; then
            return 0  # Host is idle
        fi
    fi
    
    return 1  # Host is active
}

# Function to get host idle duration
get_idle_duration() {
    local host="$1"
    
    # Check for idle marker file
    local idle_since
    idle_since=$(ssh -o ConnectTimeout=5 -o BatchMode=yes "$host" \
        "cat /var/lib/swarm/.idle_since 2>/dev/null || echo 0" 2>/dev/null) || echo 0
    
    if [[ "$idle_since" == "0" ]]; then
        # Mark as newly idle
        ssh -o ConnectTimeout=5 -o BatchMode=yes "$host" \
            "date +%s > /var/lib/swarm/.idle_since" 2>/dev/null || true
        echo 0
        return
    fi
    
    local now
    now=$(date +%s)
    local duration_seconds=$((now - idle_since))
    local duration_minutes=$((duration_seconds / 60))
    
    echo "$duration_minutes"
}

# Function to clear idle marker
clear_idle_marker() {
    local host="$1"
    ssh -o ConnectTimeout=5 -o BatchMode=yes "$host" \
        "rm -f /var/lib/swarm/.idle_since" 2>/dev/null || true
}

# Function to shutdown host
shutdown_host() {
    local host="$1"
    
    log "WARN" "Initiating shutdown for idle host: $host"
    
    # Try graceful shutdown first
    if ssh -o ConnectTimeout=10 -o BatchMode=yes "$host" \
        "sudo shutdown -h +1 'Cost guard: idle shutdown'" 2>/dev/null; then
        log "INFO" "Shutdown scheduled for: $host"
        return 0
    fi
    
    log "ERROR" "Failed to schedule shutdown for: $host"
    return 1
}

# Track statistics
TOTAL_HOSTS=0
IDLE_HOSTS=0
SHUTDOWN_HOSTS=0
ACTIVE_HOSTS=0

# Process each host in inventory
while IFS= read -r line || [[ -n "$line" ]]; do
    # Skip comments and empty lines
    [[ "$line" =~ ^[[:space:]]*# ]] && continue
    [[ -z "${line// }" ]] && continue
    
    # Extract host (first field, ignore ansible variables)
    host=$(echo "$line" | awk '{print $1}')
    
    # Skip group headers
    [[ "$host" =~ ^\[ ]] && continue
    [[ -z "$host" ]] && continue
    
    ((TOTAL_HOSTS++)) || true
    
    echo -e "${BLUE}🔍 Checking: $host${NC}"
    
    # Check if host is reachable
    if ! ssh -o ConnectTimeout=5 -o BatchMode=yes "$host" "echo ok" &>/dev/null; then
        log "WARN" "Host unreachable: $host"
        continue
    fi
    
    # Check if host is idle
    if check_host_idle "$host" "$IDLE_THRESHOLD_MINUTES"; then
        ((IDLE_HOSTS++)) || true
        
        # Get idle duration
        idle_duration=$(get_idle_duration "$host")
        
        log "INFO" "Host $host idle for ${idle_duration}m (threshold: ${IDLE_THRESHOLD_MINUTES}m)"
        
        if [[ "$idle_duration" -ge "$IDLE_THRESHOLD_MINUTES" ]]; then
            echo -e "${YELLOW}⚠️  $host idle for ${idle_duration}m - scheduling shutdown${NC}"
            
            if shutdown_host "$host"; then
                ((SHUTDOWN_HOSTS++)) || true
            fi
        else
            echo -e "${YELLOW}💤 $host idle for ${idle_duration}m (threshold: ${IDLE_THRESHOLD_MINUTES}m)${NC}"
        fi
    else
        ((ACTIVE_HOSTS++)) || true
        clear_idle_marker "$host"
        echo -e "${GREEN}✅ $host active${NC}"
    fi
done < "$INVENTORY"

# Summary
echo ""
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}📊 Cost Guard Summary${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "Total Hosts: $TOTAL_HOSTS"
echo -e "Active Hosts: $ACTIVE_HOSTS"
echo -e "Idle Hosts: $IDLE_HOSTS"
echo -e "Shutdown Initiated: $SHUTDOWN_HOSTS"
echo -e "Idle Threshold: ${IDLE_THRESHOLD_MINUTES} minutes"
echo ""

log "INFO" "Cost Guard complete - Active: $ACTIVE_HOSTS, Idle: $IDLE_HOSTS, Shutdown: $SHUTDOWN_HOSTS"

# Exit with success if any hosts were processed
if [[ "$TOTAL_HOSTS" -gt 0 ]]; then
    exit 0
else
    log "WARN" "No hosts found in inventory"
    exit 1
fi
