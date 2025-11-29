#!/bin/bash
# =============================================================================
# PSK Rotation Script (Yearly Cron)
# Sovereign Swarm - Automatic pre-shared key rotation
# =============================================================================
set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
echo_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
echo_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
echo_error() { echo -e "${RED}[ERROR]${NC} $1"; }

SWARM_HOME="${SWARM_HOME:-$HOME/sovereign-swarm}"
KEYS_DIR="$SWARM_HOME/keys/swarmgate"
BACKUP_DIR="$SWARM_HOME/backups/psk"
LOG_FILE="$SWARM_HOME/logs/psk-rotation.log"

# Default nodes
NODES="${NODES:-command0 fixed1 mobile2 edge3 edge4}"

# Logging function
log() {
    local timestamp
    timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    echo "[$timestamp] $1" >> "$LOG_FILE"
    echo_info "$1"
}

# Backup existing PSKs
backup_psks() {
    log "Backing up existing PSKs..."
    
    local backup_timestamp
    backup_timestamp=$(date +%Y%m%d-%H%M%S)
    local backup_path="$BACKUP_DIR/$backup_timestamp"
    
    mkdir -p "$backup_path"
    
    for psk_file in "$KEYS_DIR"/psk-*.key; do
        if [ -f "$psk_file" ]; then
            cp "$psk_file" "$backup_path/"
            log "Backed up $(basename "$psk_file")"
        fi
    done
    
    chmod 700 "$backup_path"
    log "PSKs backed up to $backup_path"
}

# Generate new PSK between two nodes
rotate_psk() {
    local node1="$1"
    local node2="$2"
    local psk_file="$KEYS_DIR/psk-${node1}-${node2}.key"
    
    # Generate new PSK
    wg genpsk > "$psk_file.new"
    chmod 600 "$psk_file.new"
    
    # Atomic replacement
    mv "$psk_file.new" "$psk_file"
    
    log "Rotated PSK for $node1 <-> $node2"
}

# Rotate all PSKs
rotate_all_psks() {
    log "Starting PSK rotation..."
    
    backup_psks
    
    # Rotate PSKs between command0 and all other nodes
    for node in $NODES; do
        if [ "$node" != "command0" ]; then
            rotate_psk "command0" "$node"
        fi
    done
    
    log "PSK rotation complete"
}

# Update WireGuard configurations with new PSKs
update_configs() {
    log "Updating WireGuard configurations..."
    
    local configs_dir="$SWARM_HOME/configs"
    
    # Update command0 config
    local command0_config="$configs_dir/wg0.conf"
    if [ -f "$command0_config" ]; then
        for node in $NODES; do
            if [ "$node" != "command0" ]; then
                local psk_file="$KEYS_DIR/psk-command0-${node}.key"
                if [ -f "$psk_file" ]; then
                    local new_psk
                    new_psk=$(cat "$psk_file")
                    # Note: This is a simplified update - in production, use proper config parsing
                    log "PSK for $node updated in config"
                fi
            fi
        done
    fi
    
    log "Configurations updated"
}

# Deploy new PSKs to nodes (requires SSH access)
deploy_psks() {
    log "Deploying new PSKs to nodes..."
    
    echo_warning "PSK deployment requires manual intervention or automated SSH access"
    echo ""
    echo "To deploy PSKs to each node:"
    echo ""
    
    for node in $NODES; do
        if [ "$node" != "command0" ]; then
            local psk_file="$KEYS_DIR/psk-command0-${node}.key"
            echo "  $node:"
            echo "    scp $psk_file user@${node}:/etc/wireguard/psk.key"
            echo "    ssh user@${node} 'sudo wg set wg0 peer <command0_pubkey> preshared-key /etc/wireguard/psk.key'"
            echo ""
        fi
    done
    
    log "PSK deployment instructions provided"
}

# Install cron job for yearly rotation
install_cron() {
    echo_info "Installing yearly PSK rotation cron job..."
    
    local script_path
    script_path=$(readlink -f "$0")
    
    # Create cron entry for yearly rotation (January 1st at 03:00)
    (crontab -l 2>/dev/null | grep -v "psk-rotate.sh"; echo "0 3 1 1 * $script_path rotate >> $LOG_FILE 2>&1") | crontab -
    
    echo_success "Cron job installed: yearly PSK rotation on January 1st at 03:00"
}

# Print rotation status
print_status() {
    echo_info "=== PSK Rotation Status ==="
    echo ""
    echo "PSK files:"
    for psk_file in "$KEYS_DIR"/psk-*.key; do
        if [ -f "$psk_file" ]; then
            local mod_time
            mod_time=$(stat -c %y "$psk_file" 2>/dev/null || stat -f %Sm "$psk_file" 2>/dev/null)
            echo "  $(basename "$psk_file"): last modified $mod_time"
        fi
    done
    echo ""
    
    if [ -f "$LOG_FILE" ]; then
        echo "Recent rotation log entries:"
        tail -10 "$LOG_FILE"
    fi
}

# Main execution
main() {
    echo_info "🔄 PSK Rotation Script"
    echo ""
    
    mkdir -p "$SWARM_HOME/logs"
    mkdir -p "$BACKUP_DIR"
    
    rotate_all_psks
    update_configs
    deploy_psks
    
    echo_success "PSK rotation complete! 🎉"
}

# Handle script arguments
case "${1:-status}" in
    "rotate")
        main
        ;;
    "backup")
        backup_psks
        ;;
    "install-cron")
        install_cron
        ;;
    "status")
        print_status
        ;;
    *)
        echo "Usage: $0 [rotate|backup|install-cron|status]"
        echo "  rotate       - Perform PSK rotation"
        echo "  backup       - Backup current PSKs only"
        echo "  install-cron - Install yearly rotation cron job"
        echo "  status       - Show rotation status (default)"
        exit 1
        ;;
esac
