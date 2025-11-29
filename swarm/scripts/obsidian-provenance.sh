#!/bin/bash
# obsidian-provenance.sh — Sovereign Swarm v2.0
# BLAKE3 Provenance Chain for Obsidian Vault Sync (Evolution #6)
# Auto-hashes vault changes and publishes to audit.* NATS subjects
#
# Strategickhaos DAO LLC / Valoryield Engine
# Author: Domenic Garza (Node 137)

set -euo pipefail

# Configuration
VAULT_PATH="${VAULT_PATH:-/opt/sovereign-swarm/vaults}"
NATS_URL="${NATS_URL:-nats://swarm:swarm@10.44.0.1:4222}"
CHAIN_FILE="${CHAIN_FILE:-/opt/sovereign-swarm/provenance/chain.json}"
NODE_ID="${NODE_ID:-$(hostname)}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[✓]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Ensure dependencies
check_dependencies() {
    if ! command -v b3sum &> /dev/null; then
        log_warn "b3sum not found, installing..."
        # Try cargo install if available
        if command -v cargo &> /dev/null; then
            cargo install b3sum 2>/dev/null || true
        else
            log_warn "Using sha256sum as fallback (install b3sum for BLAKE3)"
        fi
    fi
}

# Hash a file with BLAKE3 (or SHA256 fallback)
# Supports both file paths and stdin via /dev/stdin or - argument
hash_file() {
    local input="$1"
    
    if [[ "$input" == "/dev/stdin" || "$input" == "-" ]]; then
        # Handle stdin input
        if command -v b3sum &> /dev/null; then
            b3sum - | awk '{print $1}'
        else
            sha256sum - | awk '{print $1}'
        fi
    else
        # Handle file path
        if command -v b3sum &> /dev/null; then
            b3sum "$input" | awk '{print $1}'
        else
            sha256sum "$input" | awk '{print $1}'
        fi
    fi
}

# Hash entire vault directory
hash_vault() {
    local vault_dir="$1"
    local hashes=""
    
    # Find all markdown files and hash them
    while IFS= read -r -d '' file; do
        local file_hash=$(hash_file "$file")
        local rel_path="${file#$vault_dir/}"
        hashes+="${rel_path}:${file_hash}\n"
    done < <(find "$vault_dir" -type f -name "*.md" -print0 2>/dev/null)
    
    # Hash the concatenated hashes (Merkle-ish root)
    echo -e "$hashes" | sort | hash_file /dev/stdin
}

# Load existing chain
load_chain() {
    if [[ -f "$CHAIN_FILE" ]]; then
        cat "$CHAIN_FILE"
    else
        echo '{"blocks": []}'
    fi
}

# Add a block to the chain
add_block() {
    local prev_hash="$1"
    local vault_hash="$2"
    local timestamp="$3"
    
    local chain=$(load_chain)
    local block_num=$(echo "$chain" | jq '.blocks | length')
    
    # Create block
    local block=$(cat << BLOCKJSON
{
    "index": $block_num,
    "timestamp": "$timestamp",
    "vault_hash": "$vault_hash",
    "prev_hash": "$prev_hash",
    "node_id": "$NODE_ID"
}
BLOCKJSON
)
    
    # Calculate block hash
    local block_hash=$(echo "$block" | hash_file /dev/stdin)
    block=$(echo "$block" | jq --arg h "$block_hash" '. + {"hash": $h}')
    
    # Append to chain
    echo "$chain" | jq --argjson b "$block" '.blocks += [$b]' > "$CHAIN_FILE"
    
    echo "$block_hash"
}

# Publish to NATS
publish_to_nats() {
    local subject="$1"
    local data="$2"
    
    if command -v nats &> /dev/null; then
        echo "$data" | nats pub "$subject" - 2>/dev/null || log_warn "NATS publish failed"
    else
        log_warn "nats CLI not available, skipping publish"
    fi
}

# Main provenance update
update_provenance() {
    local vault_dir="$1"
    
    if [[ ! -d "$vault_dir" ]]; then
        log_error "Vault directory not found: $vault_dir"
        return 1
    fi
    
    log_info "Computing vault hash for: $vault_dir"
    
    local vault_hash=$(hash_vault "$vault_dir")
    local timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    
    # Get previous block hash
    local chain=$(load_chain)
    local prev_hash=$(echo "$chain" | jq -r '.blocks[-1].hash // "genesis"')
    
    # Check if vault changed
    local last_vault_hash=$(echo "$chain" | jq -r '.blocks[-1].vault_hash // "none"')
    if [[ "$vault_hash" == "$last_vault_hash" ]]; then
        log_info "Vault unchanged, skipping block"
        return 0
    fi
    
    log_info "Vault changed, adding new block..."
    
    # Add block
    local block_hash=$(add_block "$prev_hash" "$vault_hash" "$timestamp")
    
    log_success "Block added: $block_hash"
    
    # Publish to NATS
    local event=$(cat << EVENTJSON
{
    "event": "vault_update",
    "node_id": "$NODE_ID",
    "vault_path": "$vault_dir",
    "vault_hash": "$vault_hash",
    "block_hash": "$block_hash",
    "timestamp": "$timestamp"
}
EVENTJSON
)
    
    publish_to_nats "audit.provenance.$NODE_ID" "$event"
    log_success "Published to NATS: audit.provenance.$NODE_ID"
}

# Syncthing post-hook handler
syncthing_post_hook() {
    # Called by Syncthing after sync completion
    local folder_id="$1"
    local folder_path="$2"
    
    log_info "Syncthing hook triggered for: $folder_id"
    update_provenance "$folder_path"
}

# Verify chain integrity
verify_chain() {
    local chain=$(load_chain)
    local block_count=$(echo "$chain" | jq '.blocks | length')
    
    log_info "Verifying provenance chain ($block_count blocks)..."
    
    local prev_hash="genesis"
    local valid=true
    
    for i in $(seq 0 $((block_count - 1))); do
        local block=$(echo "$chain" | jq ".blocks[$i]")
        local stored_prev=$(echo "$block" | jq -r '.prev_hash')
        local stored_hash=$(echo "$block" | jq -r '.hash')
        
        # Verify prev_hash links
        if [[ "$stored_prev" != "$prev_hash" ]]; then
            log_error "Chain broken at block $i: prev_hash mismatch"
            valid=false
            break
        fi
        
        # Verify block hash
        local block_data=$(echo "$block" | jq 'del(.hash)')
        local computed_hash=$(echo "$block_data" | hash_file /dev/stdin)
        
        if [[ "$stored_hash" != "$computed_hash" ]]; then
            log_error "Chain broken at block $i: hash mismatch"
            valid=false
            break
        fi
        
        prev_hash="$stored_hash"
    done
    
    if $valid; then
        log_success "Chain integrity verified: $block_count blocks"
    else
        log_error "Chain integrity FAILED"
        return 1
    fi
}

# Watch mode for continuous monitoring
watch_vault() {
    local vault_dir="$1"
    
    log_info "Watching vault for changes: $vault_dir"
    
    if command -v inotifywait &> /dev/null; then
        while true; do
            inotifywait -r -e modify,create,delete "$vault_dir" 2>/dev/null
            sleep 2  # Debounce
            update_provenance "$vault_dir"
        done
    else
        log_warn "inotifywait not available, using polling..."
        while true; do
            update_provenance "$vault_dir"
            sleep 60
        done
    fi
}

# Main
main() {
    mkdir -p "$(dirname "$CHAIN_FILE")"
    check_dependencies
    
    case "${1:-}" in
        update)
            update_provenance "${2:-$VAULT_PATH}"
            ;;
        verify)
            verify_chain
            ;;
        watch)
            watch_vault "${2:-$VAULT_PATH}"
            ;;
        hook)
            syncthing_post_hook "${2:-}" "${3:-$VAULT_PATH}"
            ;;
        *)
            echo "Usage: $0 {update|verify|watch|hook} [vault_path]"
            echo ""
            echo "Commands:"
            echo "  update [path]  - Update provenance for vault"
            echo "  verify         - Verify chain integrity"
            echo "  watch [path]   - Watch vault for changes"
            echo "  hook <id> <path> - Syncthing post-sync hook"
            exit 1
            ;;
    esac
}

main "$@"
