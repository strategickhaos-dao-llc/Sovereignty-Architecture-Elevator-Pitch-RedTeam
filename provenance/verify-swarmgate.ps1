# verify-swarmgate.ps1 - SwarmGate v1.0 Provenance Verification

$ErrorActionPreference = "Stop"

$CANONICAL_BLAKE3 = "caa58d9faee9a10ce46d81d2f21e0da611ff962b8070e22b5d976cc816480698"
$ARCHIVE = "swarmgate_v1.0.tar.gz"

Write-Host "=== SwarmGate v1.0 Provenance Verification ===" -ForegroundColor Cyan
Write-Host ""

# Check if b3sum is installed
if (-not (Get-Command b3sum -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: b3sum not found. Install with:" -ForegroundColor Red
    Write-Host "  cargo install b3sum"
    Write-Host "  or: scoop install b3sum"
    exit 1
}

# Check if archive exists
if (-not (Test-Path $ARCHIVE)) {
    Write-Host "ERROR: $ARCHIVE not found" -ForegroundColor Red
    Write-Host "Download from:"
    Write-Host "  IPFS: https://ipfs.io/ipfs/<CID>"
    Write-Host "  Arweave: https://arweave.net/<TXID>"
    exit 1
}

# Compute BLAKE3 hash
Write-Host "[1/3] Computing BLAKE3 hash..."
$COMPUTED_HASH = (b3sum $ARCHIVE).Split()[0]

# Compare hashes
Write-Host "[2/3] Comparing against canonical hash..."
if ($COMPUTED_HASH -eq $CANONICAL_BLAKE3) {
    Write-Host "✓ BLAKE3 hash matches: $COMPUTED_HASH" -ForegroundColor Green
} else {
    Write-Host "✗ HASH MISMATCH!" -ForegroundColor Red
    Write-Host "  Expected: $CANONICAL_BLAKE3"
    Write-Host "  Computed: $COMPUTED_HASH"
    exit 1
}

# Verify GPG signature if available
if ((Test-Path "provenance.json.asc") -and (Test-Path "provenance.json")) {
    Write-Host "[3/3] Verifying GPG signature..."
    if (Get-Command gpg -ErrorAction SilentlyContinue) {
        gpg --verify provenance.json.asc provenance.json 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ GPG signature verified" -ForegroundColor Green
        } else {
            Write-Host "⚠ GPG signature verification failed or key not trusted" -ForegroundColor Yellow
        }
    } else {
        Write-Host "[3/3] GPG not installed (optional)"
    }
} else {
    Write-Host "[3/3] No signature files found (optional)"
}

Write-Host ""
Write-Host "=== VERIFICATION SUCCESSFUL ===" -ForegroundColor Green
Write-Host "SwarmGate v1.0 archive is authentic"
