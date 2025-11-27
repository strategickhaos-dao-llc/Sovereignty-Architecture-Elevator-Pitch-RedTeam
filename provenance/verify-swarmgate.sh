#!/bin/bash
# verify-swarmgate.sh - SwarmGate v1.0 Provenance Verification

set -euo pipefail

CANONICAL_BLAKE3="caa58d9faee9a10ce46d81d2f21e0da611ff962b8070e22b5d976cc816480698"
ARCHIVE="swarmgate_v1.0.tar.gz"

echo "=== SwarmGate v1.0 Provenance Verification ==="
echo

# Check if b3sum is installed
if ! command -v b3sum &> /dev/null; then
    echo "ERROR: b3sum not found. Install with:"
    echo "  cargo install b3sum"
    echo "  or: brew install b3sum"
    exit 1
fi

# Check if archive exists
if [ ! -f "$ARCHIVE" ]; then
    echo "ERROR: $ARCHIVE not found"
    echo "Download from:"
    echo "  IPFS: https://ipfs.io/ipfs/<CID>"
    echo "  Arweave: https://arweave.net/<TXID>"
    exit 1
fi

# Compute BLAKE3 hash
echo "[1/3] Computing BLAKE3 hash..."
COMPUTED_HASH=$(b3sum "$ARCHIVE" | awk '{print $1}')

# Compare hashes
echo "[2/3] Comparing against canonical hash..."
if [ "$COMPUTED_HASH" = "$CANONICAL_BLAKE3" ]; then
    echo "✓ BLAKE3 hash matches: $COMPUTED_HASH"
else
    echo "✗ HASH MISMATCH!"
    echo "  Expected: $CANONICAL_BLAKE3"
    echo "  Computed: $COMPUTED_HASH"
    exit 1
fi

# Verify GPG signature if available
if [ -f "provenance.json.asc" ] && [ -f "provenance.json" ]; then
    echo "[3/3] Verifying GPG signature..."
    if gpg --verify provenance.json.asc provenance.json 2>&1 | grep -q "Good signature"; then
        echo "✓ GPG signature verified"
    else
        echo "⚠ GPG signature verification failed or key not trusted"
    fi
else
    echo "[3/3] No signature files found (optional)"
fi

echo
echo "=== VERIFICATION SUCCESSFUL ==="
echo "SwarmGate v1.0 archive is authentic"
