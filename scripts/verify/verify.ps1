# verify.ps1 - Swarmgate Archive Verification Script for Windows
# Strategickhaos Sovereignty Architecture
#
# This script verifies the integrity and authenticity of swarmgate_v1.0.tar.gz
# by computing BLAKE3 hash, comparing to canonical value, and verifying GPG signature.
#
# Usage: .\verify.ps1 [OPTIONS]
#   -Archive PATH      Path to archive (default: swarmgate_v1.0.tar.gz)
#   -Manifest PATH     Path to manifest (default: swarmgate.yaml)
#   -Provenance PATH   Path to provenance file (default: provenance\provenance.json)
#   -Signature PATH    Path to GPG signature (default: swarmgate_v1.0.tar.gz.sig)
#   -SkipGPG           Skip GPG signature verification
#   -SkipTimestamp     Skip RFC3161 timestamp verification
#   -Help              Show this help message
#
# Requirements:
#   - b3sum.exe (BLAKE3 hash utility) - Install via: winget install BLAKE3team.b3sum
#   - gpg.exe (GNU Privacy Guard) - Install via: winget install GnuPG.GnuPG
#   - PowerShell 5.1 or later

[CmdletBinding()]
param(
    [string]$Archive = "swarmgate_v1.0.tar.gz",
    [string]$Manifest = "swarmgate.yaml",
    [string]$Provenance = "provenance\provenance.json",
    [string]$Signature = "swarmgate_v1.0.tar.gz.sig",
    [switch]$SkipGPG,
    [switch]$SkipTimestamp,
    [switch]$Help
)

# Colors and formatting
$Host.UI.RawUI.ForegroundColor = "White"

function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

function Write-Banner {
    Write-ColorOutput "╔══════════════════════════════════════════════════════════════╗" "Cyan"
    Write-ColorOutput "║     Swarmgate Archive Verification - Strategickhaos         ║" "Cyan"
    Write-ColorOutput "╚══════════════════════════════════════════════════════════════╝" "Cyan"
    Write-Host ""
}

function Write-Summary {
    param(
        [int]$Passed,
        [int]$Warnings,
        [int]$Failed
    )
    Write-Host ""
    Write-ColorOutput "╔══════════════════════════════════════════════════════════════╗" "Cyan"
    Write-ColorOutput "║                    Verification Summary                       ║" "Cyan"
    Write-ColorOutput "╠══════════════════════════════════════════════════════════════╣" "Cyan"
    Write-Host "║  " -NoNewline -ForegroundColor Cyan
    Write-Host "Passed:   $Passed" -ForegroundColor Green
    Write-Host "║  " -NoNewline -ForegroundColor Cyan
    Write-Host "Warnings: $Warnings" -ForegroundColor Yellow
    Write-Host "║  " -NoNewline -ForegroundColor Cyan
    Write-Host "Failed:   $Failed" -ForegroundColor Red
    Write-ColorOutput "╚══════════════════════════════════════════════════════════════╝" "Cyan"
    Write-Host ""
}

if ($Help) {
    Get-Help $PSCommandPath -Detailed
    exit 0
}

Write-Banner

# Counters
$Passed = 0
$Warnings = 0
$Failed = 0

# Step 1: Check required tools
Write-ColorOutput "[1/4] Checking required tools..." "Cyan"

$b3sumPath = Get-Command b3sum -ErrorAction SilentlyContinue
$gpgPath = Get-Command gpg -ErrorAction SilentlyContinue

$missingTools = @()

if (-not $b3sumPath) {
    $missingTools += "b3sum"
}

if (-not $SkipGPG -and -not $gpgPath) {
    $missingTools += "gpg"
}

if ($missingTools.Count -gt 0) {
    Write-ColorOutput "  ✗ Missing required tools: $($missingTools -join ', ')" "Red"
    Write-Host ""
    Write-Host "Install with:"
    Write-Host "  b3sum: winget install BLAKE3team.b3sum"
    Write-Host "  gpg:   winget install GnuPG.GnuPG"
    Write-Host ""
    Write-Host "Or download manually from:"
    Write-Host "  b3sum: https://github.com/BLAKE3-team/BLAKE3/releases"
    Write-Host "  gpg:   https://gnupg.org/download/"
    exit 1
}

Write-ColorOutput "  ✓ All required tools available" "Green"
$Passed++
Write-Host ""

# Step 2: Check archive file
Write-ColorOutput "[2/4] Checking archive file..." "Cyan"

if (-not (Test-Path $Archive)) {
    Write-ColorOutput "  ✗ Archive not found: $Archive" "Red"
    Write-ColorOutput "    Download from IPFS or GitHub releases first." "Yellow"
    $Failed++
} else {
    $archiveInfo = Get-Item $Archive
    Write-ColorOutput "  ✓ Archive found: $Archive" "Green"
    Write-Host "    Size: $($archiveInfo.Length) bytes"
    $Passed++
}
Write-Host ""

# Step 3: Verify BLAKE3 hash
Write-ColorOutput "[3/4] Verifying BLAKE3 hash..." "Cyan"

if (Test-Path $Archive) {
    # Compute BLAKE3 hash
    $b3sumOutput = & b3sum $Archive 2>&1
    $computedHash = ($b3sumOutput -split '\s+')[0]
    Write-Host "    Computed:  $computedHash"
    
    # Get canonical hash from provenance
    $canonicalHash = $null
    if (Test-Path $Provenance) {
        try {
            $provenanceContent = Get-Content $Provenance -Raw | ConvertFrom-Json
            $canonicalHash = $provenanceContent.subject[0].digest.blake3
            if (-not $canonicalHash) {
                $canonicalHash = $provenanceContent.predicate.digest.blake3
            }
        } catch {
            Write-ColorOutput "  ⚠ Could not parse provenance file" "Yellow"
        }
    }
    
    if ($canonicalHash -and $canonicalHash -ne "PLACEHOLDER_BLAKE3_HASH") {
        Write-Host "    Canonical: $canonicalHash"
        if ($computedHash -eq $canonicalHash) {
            Write-ColorOutput "  ✓ BLAKE3 hash matches canonical value" "Green"
            $Passed++
        } else {
            Write-ColorOutput "  ✗ BLAKE3 hash MISMATCH!" "Red"
            Write-ColorOutput "    Archive may be corrupted or tampered with." "Red"
            $Failed++
        }
    } else {
        Write-ColorOutput "  ⚠ No canonical hash found in provenance (placeholder present)" "Yellow"
        Write-ColorOutput "    This is expected before first release." "Yellow"
        $Warnings++
    }
    
    # Also compute SHA256 for reference
    $sha256Hash = (Get-FileHash -Path $Archive -Algorithm SHA256).Hash.ToLower()
    Write-Host "    SHA256:    $sha256Hash"
} else {
    Write-ColorOutput "  ⚠ Skipping hash verification (archive not found)" "Yellow"
    $Warnings++
}
Write-Host ""

# Step 4: Verify GPG signature
Write-ColorOutput "[4/4] Verifying GPG signature..." "Cyan"

if ($SkipGPG) {
    Write-ColorOutput "  ⚠ GPG verification skipped (-SkipGPG)" "Yellow"
    $Warnings++
} elseif (-not (Test-Path $Signature)) {
    Write-ColorOutput "  ⚠ Signature file not found: $Signature" "Yellow"
    Write-ColorOutput "    Run with -SkipGPG to skip this check." "Yellow"
    $Warnings++
} elseif (-not (Test-Path $Archive)) {
    Write-ColorOutput "  ⚠ Cannot verify signature (archive not found)" "Yellow"
    $Warnings++
} else {
    try {
        $gpgResult = & gpg --verify $Signature $Archive 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput "  ✓ GPG signature verified" "Green"
            $Passed++
        } else {
            Write-ColorOutput "  ✗ GPG signature verification FAILED" "Red"
            Write-ColorOutput "    The archive signature is invalid or the signing key is not trusted." "Red"
            $Failed++
        }
    } catch {
        Write-ColorOutput "  ✗ GPG verification error: $_" "Red"
        $Failed++
    }
}
Write-Host ""

# Summary
Write-Summary -Passed $Passed -Warnings $Warnings -Failed $Failed

if ($Failed -gt 0) {
    Write-ColorOutput "⚠ VERIFICATION FAILED" "Red"
    Write-ColorOutput "The archive may be corrupted or tampered with." "Red"
    Write-ColorOutput "Do NOT use this archive." "Red"
    exit 1
} elseif ($Warnings -gt 0) {
    Write-ColorOutput "⚠ VERIFICATION INCOMPLETE" "Yellow"
    Write-ColorOutput "Some checks could not be performed." "Yellow"
    Write-ColorOutput "Review warnings above before trusting this archive." "Yellow"
    exit 2
} else {
    Write-ColorOutput "✓ ALL VERIFICATIONS PASSED" "Green"
    Write-ColorOutput "The archive is authentic and unmodified." "Green"
    exit 0
}

<#
.SYNOPSIS
    Verifies the integrity and authenticity of swarmgate_v1.0.tar.gz

.DESCRIPTION
    This script computes the BLAKE3 hash of the archive, compares it to the
    canonical value in provenance.json, and verifies the GPG signature.

.PARAMETER Archive
    Path to the archive file to verify (default: swarmgate_v1.0.tar.gz)

.PARAMETER Manifest
    Path to the manifest file (default: swarmgate.yaml)

.PARAMETER Provenance
    Path to the provenance file (default: provenance\provenance.json)

.PARAMETER Signature
    Path to the GPG signature file (default: swarmgate_v1.0.tar.gz.sig)

.PARAMETER SkipGPG
    Skip GPG signature verification

.PARAMETER SkipTimestamp
    Skip RFC3161 timestamp verification

.EXAMPLE
    .\verify.ps1
    Runs full verification with default paths

.EXAMPLE
    .\verify.ps1 -Archive "C:\Downloads\swarmgate_v1.0.tar.gz" -SkipGPG
    Verifies specific archive without GPG check

.NOTES
    One-liner version (copy-paste ready):
    irm https://raw.githubusercontent.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-/main/scripts/verify/verify.ps1 | iex
#>
