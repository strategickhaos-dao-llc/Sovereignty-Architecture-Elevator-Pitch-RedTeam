#!/usr/bin/env bash
# fxsnapshot.sh - Function/Effects Snapshot Utility
# Captures comprehensive system state snapshot for sovereignty architecture
# Issue: #4806204

set -euo pipefail

# Configuration
SNAPSHOT_DIR="./snapshots"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
SNAPSHOT_FILE="$SNAPSHOT_DIR/fxsnapshot_$TIMESTAMP.txt"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Ensure snapshot directory exists
mkdir -p "$SNAPSHOT_DIR"

# Helper functions
log() { 
    echo -e "${BLUE}[$(date +%H:%M:%S)]${NC} $*" | tee -a "$SNAPSHOT_FILE"
}

section() {
    echo "" | tee -a "$SNAPSHOT_FILE"
    echo "========================================" | tee -a "$SNAPSHOT_FILE"
    echo -e "${GREEN}$*${NC}" | tee -a "$SNAPSHOT_FILE"
    echo "========================================" | tee -a "$SNAPSHOT_FILE"
}

capture() {
    local title="$1"
    local command="$2"
    echo "" >> "$SNAPSHOT_FILE"
    echo "--- $title ---" >> "$SNAPSHOT_FILE"
    eval "$command" >> "$SNAPSHOT_FILE" 2>&1 || echo "Error capturing: $title" >> "$SNAPSHOT_FILE"
}

# Start snapshot
log "🔮 Starting FX Snapshot Capture"
log "Snapshot file: $SNAPSHOT_FILE"

# Header
{
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║     SOVEREIGNTY ARCHITECTURE - FX SNAPSHOT                 ║"
    echo "║     Issue #4806204                                         ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""
    echo "Snapshot Time: $(date)"
    echo "Hostname: $(hostname)"
    echo "User: $(whoami)"
    echo ""
} >> "$SNAPSHOT_FILE"

# System Information
section "🖥️  SYSTEM INFORMATION"
capture "Operating System" "uname -a"
capture "OS Release" "cat /etc/os-release 2>/dev/null || echo 'Not available'"
capture "Uptime" "uptime"
capture "System Resources" "free -h 2>/dev/null || echo 'free command not available'"

# Docker State
section "🐳 DOCKER STATE"
if command -v docker &> /dev/null; then
    capture "Docker Version" "docker --version"
    capture "Docker Info" "docker info --format '{{.ServerVersion}} | Containers: {{.Containers}} | Images: {{.Images}}' 2>/dev/null || echo 'Docker not running'"
    capture "Running Containers" "docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Image}}' 2>/dev/null || echo 'No containers'"
    capture "Docker Compose Services" "docker compose ps 2>/dev/null || echo 'No compose services'"
    capture "Container Resource Usage" "docker stats --no-stream --format 'table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}' 2>/dev/null | head -15 || echo 'Stats not available'"
else
    echo "Docker not installed" >> "$SNAPSHOT_FILE"
fi

# Git Repository State
section "📚 GIT REPOSITORY STATE"
if [ -d .git ]; then
    capture "Current Branch" "git branch --show-current"
    capture "Latest Commits" "git --no-pager log --oneline -10"
    capture "Repository Status" "git --no-pager status --short"
    capture "Remote URLs" "git remote -v"
    capture "Uncommitted Changes" "git --no-pager diff --stat"
else
    echo "Not a git repository" >> "$SNAPSHOT_FILE"
fi

# Process State
section "⚙️  PROCESS STATE"
capture "Top Processes by CPU" "ps aux --sort=-%cpu | head -11"
capture "Top Processes by Memory" "ps aux --sort=-%mem | head -11"
capture "Process Tree" "pstree -p 2>/dev/null | head -30 || ps auxf | head -30"

# Network State
section "🌐 NETWORK STATE"
capture "Network Interfaces" "ip -br addr 2>/dev/null || ifconfig -a 2>/dev/null || echo 'Network info not available'"
capture "Listening Ports" "ss -tunlp 2>/dev/null | head -20 || netstat -tunlp 2>/dev/null | head -20 || echo 'Port info not available'"
capture "Active Connections" "ss -tun 2>/dev/null | head -20 || netstat -tun 2>/dev/null | head -20 || echo 'Connection info not available'"

# Configuration Files
section "📝 CONFIGURATION STATE"
if [ -f discovery.yml ]; then
    capture "Discovery Config" "head -30 discovery.yml"
fi
if [ -f docker-compose.yml ]; then
    capture "Docker Compose Config" "head -30 docker-compose.yml"
fi
if [ -f package.json ]; then
    capture "Package.json" "cat package.json"
fi

# Environment
section "🔧 ENVIRONMENT VARIABLES"
capture "Node/NPM Versions" "node --version 2>/dev/null && npm --version 2>/dev/null || echo 'Node.js not installed'"
capture "Python Version" "python3 --version 2>/dev/null || python --version 2>/dev/null || echo 'Python not installed'"
capture "Java Version" "java -version 2>&1 | head -3 || echo 'Java not installed'"

# Service Health
section "🏥 SERVICE HEALTH"
capture "CloudOS Services" "docker compose -f docker-compose-cloudos.yml ps 2>/dev/null || echo 'CloudOS services not running'"
capture "RECON Services" "docker compose -f docker-compose-recon.yml ps 2>/dev/null || echo 'RECON services not running'"

# Disk Usage
section "💾 DISK USAGE"
capture "Filesystem Usage" "df -h | head -20"
capture "Directory Sizes" "du -sh ./* 2>/dev/null | sort -hr | head -20 || echo 'Cannot read directory sizes'"

# Recent Logs (if available)
section "📋 RECENT ACTIVITY"
capture "Docker Container Logs (last 20 lines)" "docker compose logs --tail=20 2>/dev/null || echo 'No docker logs available'"
capture "System Journal (last 20 lines)" "journalctl -n 20 --no-pager 2>/dev/null || echo 'Journalctl not available'"

# Footer
{
    echo ""
    echo "========================================="
    echo "Snapshot completed at: $(date)"
    echo "========================================="
} >> "$SNAPSHOT_FILE"

# Summary
echo ""
log "${GREEN}✅ Snapshot captured successfully${NC}"
log "📁 Location: $SNAPSHOT_FILE"
log "📊 Size: $(du -h "$SNAPSHOT_FILE" | cut -f1)"
echo ""

# Display recent snapshots
files=("$SNAPSHOT_DIR"/fxsnapshot_*.txt)
if [ ${#files[@]} -gt 1 ] && [ -e "${files[0]}" ]; then
    log "${YELLOW}Recent snapshots:${NC}"
    for file in "$SNAPSHOT_DIR"/fxsnapshot_*.txt; do
        [ -e "$file" ] && echo "  $file ($(du -h "$file" | cut -f1))"
    done | sort -r | head -5
fi

# Optional: Show snapshot file location for easy access
echo ""
echo -e "${BLUE}💡 View snapshot:${NC} cat $SNAPSHOT_FILE"
echo -e "${BLUE}💡 Compare snapshots:${NC} diff <(cat snapshot1.txt) <(cat snapshot2.txt)"
echo ""
