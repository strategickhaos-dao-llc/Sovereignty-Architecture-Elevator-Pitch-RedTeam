#!/bin/bash
# ============================================================================
# Sovereignty Architecture - WSL Network Auto-Capture Script
# Automated network configuration capture for Family Knowledge Vault
# Strategic Khaos DAO LLC - Domenic Garza (Node 137)
# ============================================================================
#
# PURPOSE: Auto-captures WSL network configuration and stores in encrypted
# vault for authorized family member access (omnipresent knowledge base)
#
# USAGE:
#   Direct:     ./wsl-auto-capture.sh
#   In .bashrc: source /path/to/wsl-auto-capture.sh
#
# ============================================================================

# Configuration
VAULT_BASE="${SOVEREIGNTY_VAULT_PATH:-/mnt/c/Users/$USER/.sovereignty-vault/network-knowledge}"
CAPTURE_DIR="$VAULT_BASE/wsl-captures"
LOG_DIR="$VAULT_BASE/logs"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
CAPTURE_FILE="$CAPTURE_DIR/network_capture_$TIMESTAMP.txt"
LOG_FILE="$LOG_DIR/wsl-capture-$(date +%Y%m%d).log"

# ANSI color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# Logging function
log_message() {
    local level="$1"
    local message="$2"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    # Console output with colors
    case "$level" in
        "INFO")    color="$CYAN" ;;
        "SUCCESS") color="$GREEN" ;;
        "WARNING") color="$YELLOW" ;;
        "ERROR")   color="$RED" ;;
        *)         color="$NC" ;;
    esac
    
    echo -e "${color}[$timestamp] [$level] $message${NC}"
    
    # File logging
    if [[ -d "$LOG_DIR" ]]; then
        echo "[$timestamp] [$level] $message" >> "$LOG_FILE"
    fi
}

# Initialize vault directories
init_vault_dirs() {
    mkdir -p "$CAPTURE_DIR" 2>/dev/null
    mkdir -p "$LOG_DIR" 2>/dev/null
    
    if [[ ! -d "$CAPTURE_DIR" ]]; then
        log_message "ERROR" "Could not create capture directory: $CAPTURE_DIR"
        return 1
    fi
    
    return 0
}

# Capture network configuration
capture_network_config() {
    log_message "INFO" "🔒 Sovereignty Network Capture initiating..."
    
    # Initialize directories
    if ! init_vault_dirs; then
        return 1
    fi
    
    # Create capture file with header
    cat > "$CAPTURE_FILE" << EOF
================================================================================
   SOVEREIGNTY ARCHITECTURE - WSL NETWORK CONFIGURATION SNAPSHOT
   Captured: $(date '+%Y-%m-%d %H:%M:%S %Z')
   Host: $(hostname 2>/dev/null || echo "unknown")
   User: $USER
   WSL Distro: $(cat /etc/os-release 2>/dev/null | grep PRETTY_NAME | cut -d= -f2 | tr -d '"')
================================================================================

EOF

    # Capture IP Address Configuration
    {
        echo "┌──────────────────────────────────────────────────────────────────┐"
        echo "│ IP ADDRESS CONFIGURATION (ip addr)                               │"
        echo "└──────────────────────────────────────────────────────────────────┘"
        echo ""
        ip addr 2>/dev/null || echo "Command not available"
        echo ""
    } >> "$CAPTURE_FILE"

    # Capture Network Statistics
    {
        echo "┌──────────────────────────────────────────────────────────────────┐"
        echo "│ NETWORK STATISTICS (netstat)                                     │"
        echo "└──────────────────────────────────────────────────────────────────┘"
        echo ""
        netstat 2>/dev/null | head -150 || echo "Command not available"
        echo ""
    } >> "$CAPTURE_FILE"

    # Capture Routing Table
    {
        echo "┌──────────────────────────────────────────────────────────────────┐"
        echo "│ ROUTING TABLE (ip route)                                         │"
        echo "└──────────────────────────────────────────────────────────────────┘"
        echo ""
        ip route 2>/dev/null || echo "Command not available"
        echo ""
    } >> "$CAPTURE_FILE"

    # Capture DNS Configuration
    {
        echo "┌──────────────────────────────────────────────────────────────────┐"
        echo "│ DNS CONFIGURATION (/etc/resolv.conf)                             │"
        echo "└──────────────────────────────────────────────────────────────────┘"
        echo ""
        cat /etc/resolv.conf 2>/dev/null || echo "File not accessible"
        echo ""
    } >> "$CAPTURE_FILE"

    # Capture Interface Configuration (ifconfig if available)
    {
        echo "┌──────────────────────────────────────────────────────────────────┐"
        echo "│ INTERFACE DETAILS (ifconfig)                                     │"
        echo "└──────────────────────────────────────────────────────────────────┘"
        echo ""
        ifconfig 2>/dev/null || echo "Command not available (use ip addr instead)"
        echo ""
    } >> "$CAPTURE_FILE"

    # Capture Active Connections
    {
        echo "┌──────────────────────────────────────────────────────────────────┐"
        echo "│ ACTIVE CONNECTIONS (ss -tulpn)                                   │"
        echo "└──────────────────────────────────────────────────────────────────┘"
        echo ""
        ss -tulpn 2>/dev/null || echo "Command not available"
        echo ""
    } >> "$CAPTURE_FILE"

    # Capture Docker Networks (if available)
    if command -v docker &> /dev/null; then
        {
            echo "┌──────────────────────────────────────────────────────────────────┐"
            echo "│ DOCKER NETWORKS (docker network ls)                              │"
            echo "└──────────────────────────────────────────────────────────────────┘"
            echo ""
            docker network ls 2>/dev/null || echo "Docker not accessible"
            echo ""
        } >> "$CAPTURE_FILE"
    fi

    # Add footer
    {
        echo "================================================================================"
        echo "   END OF CAPTURE - $(date '+%Y-%m-%d %H:%M:%S %Z')"
        echo "   Sovereignty Architecture Knowledge Vault - For Authorized Family Access"
        echo "================================================================================"
    } >> "$CAPTURE_FILE"

    log_message "SUCCESS" "📸 Network snapshot captured: $CAPTURE_FILE"
    
    # Cleanup old captures (keep last 30 days)
    find "$CAPTURE_DIR" -name "network_capture_*.txt" -mtime +30 -delete 2>/dev/null
    
    return 0
}

# Create here-string format output (for PowerShell ingestion)
export_powershell_format() {
    local capture_file="${1:-$CAPTURE_FILE}"
    
    if [[ ! -f "$capture_file" ]]; then
        log_message "ERROR" "Capture file not found: $capture_file"
        return 1
    fi
    
    local ps_file="${capture_file%.txt}_ps.txt"
    
    # Create PowerShell here-string format using heredoc for clarity
    {
        echo '$wslNetworkSnapshot = @'"'"
        cat "$capture_file"
        echo "'"
        echo ""
        echo "# To save to file:"
        echo '# $wslNetworkSnapshot | Out-File "C:\logs\wsl_network_snapshot.txt" -Encoding UTF8'
    } > "$ps_file"
    
    log_message "SUCCESS" "PowerShell format exported: $ps_file"
    return 0
}

# Display captured snapshots
list_snapshots() {
    echo -e "${MAGENTA}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${MAGENTA}   🔐 SOVEREIGNTY VAULT - WSL NETWORK SNAPSHOTS                ${NC}"
    echo -e "${MAGENTA}═══════════════════════════════════════════════════════════════${NC}"
    echo ""
    
    if [[ ! -d "$CAPTURE_DIR" ]]; then
        echo -e "${YELLOW}   Vault not initialized. Run: ./wsl-auto-capture.sh capture${NC}"
        return 1
    fi
    
    local count=0
    for file in "$CAPTURE_DIR"/network_capture_*.txt; do
        if [[ -f "$file" ]]; then
            local filename=$(basename "$file")
            local size=$(du -h "$file" | cut -f1)
            local date_part=${filename#network_capture_}
            date_part=${date_part%.txt}
            echo -e "   📄 ${CYAN}$filename${NC} ($size)"
            ((count++))
        fi
    done
    
    if [[ $count -eq 0 ]]; then
        echo -e "${YELLOW}   No snapshots found. Run: ./wsl-auto-capture.sh capture${NC}"
    else
        echo ""
        echo -e "   ${GREEN}Total snapshots: $count${NC}"
    fi
    
    echo ""
    echo -e "${MAGENTA}═══════════════════════════════════════════════════════════════${NC}"
}

# Display help
show_help() {
    cat << 'EOF'

🔐 WSL Network Auto-Capture - Sovereignty Architecture
   Encrypted Knowledge Vault for Family Access

USAGE:
    ./wsl-auto-capture.sh <command>

COMMANDS:
    capture         Capture current WSL network configuration
    list            List all stored snapshots
    export          Export latest capture in PowerShell format
    bashrc          Show .bashrc integration snippet
    status          Show vault status
    help            Show this help message

ENVIRONMENT VARIABLES:
    SOVEREIGNTY_VAULT_PATH  Override default vault location
                           (default: /mnt/c/Users/$USER/.sovereignty-vault/network-knowledge)

EXAMPLES:
    ./wsl-auto-capture.sh capture
    ./wsl-auto-capture.sh list
    ./wsl-auto-capture.sh export
    
    # Add to .bashrc for auto-capture on WSL startup:
    echo 'source /path/to/wsl-auto-capture.sh && sovereignty_auto_capture' >> ~/.bashrc

EOF
}

# Show .bashrc integration snippet
show_bashrc_snippet() {
    local script_path="$(realpath "$0" 2>/dev/null || echo "/path/to/wsl-auto-capture.sh")"
    
    cat << EOF

# ============================================================================
# Add the following to your ~/.bashrc for auto-capture on WSL startup:
# ============================================================================

# Sovereignty Architecture - WSL Network Auto-Capture
sovereignty_auto_capture() {
    local CAPTURE_DIR="/mnt/c/Users/\$USER/.sovereignty-vault/network-knowledge/wsl-captures"
    local LOG_FILE="/mnt/c/Users/\$USER/.sovereignty-vault/network-knowledge/logs/wsl-capture-\$(date +%Y%m%d).log"
    
    # Create directories
    mkdir -p "\$CAPTURE_DIR" 2>/dev/null
    mkdir -p "\$(dirname "\$LOG_FILE")" 2>/dev/null
    
    # Capture to log (silent)
    {
        echo ""
        echo "=========================================="
        echo "WSL Network Capture - \$(date '+%Y-%m-%d %H:%M:%S')"
        echo "=========================================="
        ip addr 2>/dev/null
        echo ""
        ip route 2>/dev/null
        echo "=========================================="
    } >> "\$LOG_FILE" 2>&1
    
    echo "🔒 Network snapshot captured to Sovereignty Vault"
}

# Run on interactive shell startup
if [[ \$- == *i* ]]; then
    sovereignty_auto_capture
fi

# ============================================================================
EOF
}

# Show vault status
show_status() {
    echo -e "${MAGENTA}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${MAGENTA}   🔐 SOVEREIGNTY NETWORK KNOWLEDGE VAULT - STATUS             ${NC}"
    echo -e "${MAGENTA}═══════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "   📍 Vault Base:     ${CYAN}$VAULT_BASE${NC}"
    echo -e "   📁 Capture Dir:    ${CYAN}$CAPTURE_DIR${NC}"
    echo -e "   📝 Log Dir:        ${CYAN}$LOG_DIR${NC}"
    echo ""
    
    if [[ -d "$CAPTURE_DIR" ]]; then
        local snapshot_count=$(find "$CAPTURE_DIR" -name "network_capture_*.txt" 2>/dev/null | wc -l)
        local total_size=$(du -sh "$CAPTURE_DIR" 2>/dev/null | cut -f1)
        echo -e "   📸 Snapshots:      ${GREEN}$snapshot_count${NC}"
        echo -e "   💾 Total Size:     ${GREEN}$total_size${NC}"
    else
        echo -e "   ${YELLOW}⚠️  Vault not initialized${NC}"
    fi
    
    echo ""
    echo -e "${MAGENTA}═══════════════════════════════════════════════════════════════${NC}"
}

# Main execution
main() {
    local command="${1:-capture}"
    
    case "$command" in
        capture)
            capture_network_config
            ;;
        list)
            list_snapshots
            ;;
        export)
            if [[ -z "$2" ]]; then
                # Export latest capture
                local latest=$(ls -t "$CAPTURE_DIR"/network_capture_*.txt 2>/dev/null | head -1)
                if [[ -n "$latest" ]]; then
                    export_powershell_format "$latest"
                else
                    capture_network_config
                    export_powershell_format "$CAPTURE_FILE"
                fi
            else
                export_powershell_format "$2"
            fi
            ;;
        bashrc)
            show_bashrc_snippet
            ;;
        status)
            show_status
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            log_message "ERROR" "Unknown command: $command"
            show_help
            exit 1
            ;;
    esac
}

# Execute if run directly (not sourced)
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
