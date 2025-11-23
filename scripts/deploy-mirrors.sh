#!/bin/bash
# deploy-mirrors.sh - Deploy repository to all decentralized mirrors
# Part of the nonprofit hardening infrastructure resilience plan
#
# Usage: ./scripts/deploy-mirrors.sh [all|radicle|ipfs|arweave|torrent]
#
# ⚠️ PREREQUISITES:
# - Radicle CLI: curl -sSf https://radicle.xyz/install.sh | sh
# - IPFS CLI: https://docs.ipfs.tech/install/
# - Arweave CLI: npm install -g arweave-deploy
# - Transmission CLI: apt-get install transmission-cli

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="/tmp/mirror-deploy-${TIMESTAMP}.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$LOG_FILE"
}

check_command() {
    if ! command -v "$1" &> /dev/null; then
        error "$1 not found. Please install it first."
        return 1
    fi
    return 0
}

deploy_radicle() {
    log "Deploying to Radicle..."
    
    if ! check_command rad; then
        warn "Radicle CLI not installed. Skipping."
        return 1
    fi
    
    cd "$REPO_ROOT"
    
    # Check if already initialized
    if [ ! -d ".rad" ]; then
        log "Initializing Radicle project..."
        rad init \
            --name "Sovereignty-Architecture-Elevator-Pitch" \
            --description "Sovereign Swarm Infrastructure - Nonprofit Hardening Implementation" \
            --default-branch "main" \
            --public
    fi
    
    # Push to Radicle network
    log "Pushing to Radicle network..."
    rad push --seed "seed.radicle.xyz" || rad push --seed "seed.radicle.garden"
    
    # Get and display project ID
    PROJECT_ID=$(rad inspect | grep "rad://" | head -n 1 || echo "Unknown")
    log "Radicle Project ID: $PROJECT_ID"
    echo "$PROJECT_ID" > "${REPO_ROOT}/.radicle-id"
    
    log "✓ Radicle deployment complete"
    return 0
}

deploy_ipfs() {
    log "Deploying to IPFS..."
    
    if ! check_command ipfs; then
        warn "IPFS CLI not installed. Skipping."
        return 1
    fi
    
    cd "$REPO_ROOT"
    
    # Start IPFS daemon if not running
    if ! ipfs id &>/dev/null; then
        warn "IPFS daemon not running. Attempting to start..."
        ipfs daemon --init &
        sleep 5
    fi
    
    # Add entire repository to IPFS (excluding .git)
    log "Adding repository to IPFS..."
    REPO_CID=$(ipfs add -r --quiet --ignore=".git" . | tail -n 1)
    
    if [ -z "$REPO_CID" ]; then
        error "Failed to add to IPFS"
        return 1
    fi
    
    log "Repository added to IPFS: $REPO_CID"
    
    # Pin to ensure persistence
    log "Pinning content..."
    ipfs pin add "$REPO_CID"
    
    # Update IPNS if key exists, otherwise create
    IPNS_KEY="sovereignty-repo"
    if ipfs key list | grep -q "$IPNS_KEY"; then
        log "Updating existing IPNS name..."
        IPNS_NAME=$(ipfs name publish --key="$IPNS_KEY" "$REPO_CID" | awk '{print $3}' | tr -d ':')
    else
        log "Creating new IPNS name..."
        ipfs key gen "$IPNS_KEY"
        IPNS_NAME=$(ipfs name publish --key="$IPNS_KEY" "$REPO_CID" | awk '{print $3}' | tr -d ':')
    fi
    
    # Save metadata
    cat > "${REPO_ROOT}/.ipfs-metadata" << EOF
{
  "cid": "$REPO_CID",
  "ipns": "$IPNS_NAME",
  "timestamp": "$(date -Iseconds)",
  "gateway_urls": [
    "https://ipfs.io/ipfs/$REPO_CID",
    "https://gateway.pinata.cloud/ipfs/$REPO_CID",
    "https://cloudflare-ipfs.com/ipfs/$REPO_CID"
  ]
}
EOF
    
    log "✓ IPFS deployment complete"
    log "  CID: $REPO_CID"
    log "  IPNS: /ipns/$IPNS_NAME"
    log "  Gateway: https://ipfs.io/ipfs/$REPO_CID"
    
    return 0
}

deploy_arweave() {
    log "Deploying to Arweave..."
    
    if ! check_command arweave; then
        warn "Arweave CLI not installed. Skipping."
        return 1
    fi
    
    cd "$REPO_ROOT"
    
    # Check for wallet
    if [ ! -f "${ARWEAVE_WALLET:-$HOME/.arweave/wallet.json}" ]; then
        error "Arweave wallet not found. Set ARWEAVE_WALLET env var or place at ~/.arweave/wallet.json"
        return 1
    fi
    
    WALLET_PATH="${ARWEAVE_WALLET:-$HOME/.arweave/wallet.json}"
    
    # Create archive
    log "Creating repository archive..."
    ARCHIVE_FILE="/tmp/sovereignty-repo-${TIMESTAMP}.tar.gz"
    git archive --format=tar.gz --prefix="sovereignty-repo-${TIMESTAMP}/" HEAD > "$ARCHIVE_FILE"
    
    # Upload to Arweave
    log "Uploading to Arweave (this may take a while)..."
    TX_ID=$(arweave deploy \
        --wallet-path "$WALLET_PATH" \
        --input-file "$ARCHIVE_FILE" \
        --tag "App-Name:Sovereignty-Archive" \
        --tag "Content-Type:application/gzip" \
        --tag "Version:$(git describe --tags --always)" \
        --tag "Date:$(date -Iseconds)" | grep -oP 'Transaction.*\K[a-zA-Z0-9_-]{43}' | head -n 1)
    
    if [ -z "$TX_ID" ]; then
        error "Failed to upload to Arweave"
        rm -f "$ARCHIVE_FILE"
        return 1
    fi
    
    # Save transaction ID
    echo "${TX_ID},$(date -Iseconds)" >> "${REPO_ROOT}/arweave-backup-log.csv"
    
    log "✓ Arweave deployment complete"
    log "  Transaction ID: $TX_ID"
    log "  URL: https://arweave.net/$TX_ID"
    
    # Cleanup
    rm -f "$ARCHIVE_FILE"
    
    return 0
}

deploy_torrent() {
    log "Creating BitTorrent distribution..."
    
    if ! check_command transmission-create; then
        warn "Transmission CLI not installed. Skipping."
        return 1
    fi
    
    cd "$REPO_ROOT"
    
    # Create archive
    log "Creating repository archive..."
    ARCHIVE_FILE="/tmp/sovereignty-repo-${TIMESTAMP}.tar.gz"
    git archive --format=tar.gz --prefix="sovereignty-repo/" HEAD > "$ARCHIVE_FILE"
    
    # Create torrent file
    TORRENT_FILE="${REPO_ROOT}/sovereignty-repo-${TIMESTAMP}.torrent"
    
    log "Creating torrent file..."
    transmission-create \
        -o "$TORRENT_FILE" \
        -t "udp://tracker.opentrackr.org:1337/announce" \
        -t "udp://open.tracker.cl:1337/announce" \
        -t "udp://tracker.torrent.eu.org:451/announce" \
        -t "udp://exodus.desync.com:6969/announce" \
        -c "Sovereignty Architecture - Decentralized Repository Backup - $(date -Iseconds)" \
        "$ARCHIVE_FILE"
    
    # Generate magnet link
    MAGNET=$(transmission-show -m "$TORRENT_FILE")
    
    log "✓ Torrent creation complete"
    log "  Torrent file: $TORRENT_FILE"
    log "  Archive: $ARCHIVE_FILE"
    echo "$MAGNET" > "${REPO_ROOT}/.magnet-link"
    log "  Magnet link saved to .magnet-link"
    
    warn "Remember to seed the torrent!"
    warn "  Archive file: $ARCHIVE_FILE"
    warn "  Run: transmission-remote -a $TORRENT_FILE"
    
    return 0
}

deploy_all() {
    log "========================================="
    log "Deploying to all mirrors"
    log "========================================="
    
    FAILURES=0
    
    deploy_radicle || ((FAILURES++))
    echo ""
    
    deploy_ipfs || ((FAILURES++))
    echo ""
    
    deploy_arweave || ((FAILURES++))
    echo ""
    
    deploy_torrent || ((FAILURES++))
    echo ""
    
    log "========================================="
    if [ $FAILURES -eq 0 ]; then
        log "✓ All mirrors deployed successfully!"
    else
        warn "$FAILURES mirror(s) failed to deploy. Check log: $LOG_FILE"
    fi
    log "========================================="
    
    return $FAILURES
}

# Main script
main() {
    log "Repository Mirror Deployment Script"
    log "Log file: $LOG_FILE"
    echo ""
    
    TARGET="${1:-all}"
    
    case "$TARGET" in
        radicle)
            deploy_radicle
            ;;
        ipfs)
            deploy_ipfs
            ;;
        arweave)
            deploy_arweave
            ;;
        torrent)
            deploy_torrent
            ;;
        all)
            deploy_all
            ;;
        *)
            error "Unknown target: $TARGET"
            echo "Usage: $0 [all|radicle|ipfs|arweave|torrent]"
            exit 1
            ;;
    esac
    
    EXIT_CODE=$?
    
    if [ $EXIT_CODE -eq 0 ]; then
        log "Deployment successful! ✓"
    else
        error "Deployment failed. Check log: $LOG_FILE"
    fi
    
    exit $EXIT_CODE
}

main "$@"
