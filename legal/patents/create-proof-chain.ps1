# Create Cryptographic Proof Chain for Patent Filing (PowerShell)
# 
# This script establishes an immutable proof chain for your USPTO patent filing
# using Git commits, GPG signatures, and OpenTimestamps (Bitcoin blockchain proof)
#
# Usage: .\create-proof-chain.ps1 -ApplicationNumber "63/123456"

param(
    [Parameter(Mandatory=$true)]
    [string]$ApplicationNumber,
    [string]$FilingDate = (Get-Date -Format "yyyy-MM-dd")
)

# Paths
$RepoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$PatentDir = "$RepoRoot\legal\patents"
$ProvisionalDir = "$PatentDir\provisional"
$ReceiptsDir = "$PatentDir\receipts"

# Color output functions
function Write-Success { Write-Host "✓ $args" -ForegroundColor Green }
function Write-Info { Write-Host "ℹ $args" -ForegroundColor Cyan }
function Write-Warning { Write-Host "⚠ $args" -ForegroundColor Yellow }
function Write-Error { Write-Host "✗ $args" -ForegroundColor Red }
function Write-Header { Write-Host "`n=== $args ===" -ForegroundColor Magenta }

Write-Header "Cryptographic Proof Chain Creation"
Write-Info "Application Number: $ApplicationNumber"
Write-Info "Filing Date: $FilingDate"
Write-Info "Repository: $RepoRoot"
Write-Host ""

# Change to repo root
Set-Location $RepoRoot

# Check if we're in a git repository
try {
    git rev-parse --git-dir | Out-Null
} catch {
    Write-Error "Not in a git repository"
    exit 1
}

# Step 1: Check for required files
Write-Header "Step 1: Verify Files"

$FilesToAdd = @()

# Check for provisional application PDFs
$provisionalPdfs = Get-ChildItem -Path $ProvisionalDir -Filter "*.pdf" -ErrorAction SilentlyContinue
if ($provisionalPdfs) {
    foreach ($file in $provisionalPdfs) {
        Write-Success "Found: $($file.FullName)"
        $FilesToAdd += $file.FullName
    }
} else {
    Write-Warning "No PDF files found in $ProvisionalDir"
}

# Check for USPTO receipt
$usptoReceipts = Get-ChildItem -Path $ReceiptsDir -Filter "USPTO_Receipt*.pdf" -ErrorAction SilentlyContinue
if ($usptoReceipts) {
    foreach ($file in $usptoReceipts) {
        Write-Success "Found: $($file.FullName)"
        $FilesToAdd += $file.FullName
    }
} else {
    Write-Warning "No USPTO receipt found in $ReceiptsDir"
}

# Check for micro-entity certification
$microEntityCerts = Get-ChildItem -Path $ReceiptsDir -Filter "*MICRO_ENTITY*.pdf" -ErrorAction SilentlyContinue
if (-not $microEntityCerts) {
    $microEntityCerts = Get-ChildItem -Path $ReceiptsDir -Filter "SB15A*.pdf" -ErrorAction SilentlyContinue
}
if ($microEntityCerts) {
    foreach ($file in $microEntityCerts) {
        Write-Success "Found: $($file.FullName)"
        $FilesToAdd += $file.FullName
    }
} else {
    Write-Warning "No micro-entity certification found in $ReceiptsDir"
}

if ($FilesToAdd.Count -eq 0) {
    Write-Error "No patent files found to add to proof chain"
    Write-Host ""
    Write-Info "Make sure you have:"
    Write-Host "  - Provisional application PDF in: $ProvisionalDir"
    Write-Host "  - USPTO filing receipt in: $ReceiptsDir"
    Write-Host "  - Micro-entity certification in: $ReceiptsDir"
    exit 1
}

# Step 2: Git add files
Write-Header "Step 2: Stage Files in Git"

foreach ($file in $FilesToAdd) {
    git add $file
    Write-Success "Staged: $file"
}

# Also stage the guide and scripts
git add "$PatentDir\USPTO_FILING_GUIDE.md" 2>$null
git add "$PatentDir\*.sh" 2>$null
git add "$PatentDir\*.ps1" 2>$null

# Step 3: Create GPG-signed commit
Write-Header "Step 3: Create GPG-Signed Commit"

$CommitMessage = "PATENT PENDING: Provisional $ApplicationNumber filed $FilingDate – micro-entity"
Write-Info "Commit message: $CommitMessage"
Write-Host ""

# Check if GPG is configured
$hasSigningKey = git config --get user.signingkey 2>$null
if ($hasSigningKey) {
    Write-Info "GPG signing key configured"
    
    # Try to create a signed commit
    try {
        git commit -S -m $CommitMessage
        Write-Success "Created GPG-signed commit"
    } catch {
        Write-Warning "GPG signing failed, creating unsigned commit"
        git commit -m $CommitMessage
    }
} else {
    Write-Warning "No GPG signing key configured"
    Write-Info "To enable GPG signing:"
    Write-Host "  1. Install GPG: https://gpg4win.org/"
    Write-Host "  2. Generate a GPG key: gpg --full-generate-key"
    Write-Host "  3. List keys: gpg --list-secret-keys --keyid-format=long"
    Write-Host "  4. Configure git: git config user.signingkey [KEY_ID]"
    Write-Host "  5. Configure git: git config commit.gpgsign true"
    Write-Host ""
    
    # Create unsigned commit
    git commit -m $CommitMessage
    Write-Warning "Created unsigned commit (consider enabling GPG signing)"
}

# Step 4: Push to remote
Write-Header "Step 4: Push to Remote Repository"

try {
    $remoteUrl = git remote get-url origin 2>$null
    if ($remoteUrl) {
        Write-Info "Pushing to remote..."
        
        git push
        Write-Success "Pushed to remote repository"
        
        # Get the commit hash
        $CommitHash = git rev-parse HEAD
        Write-Info "Commit hash: $CommitHash"
    } else {
        Write-Warning "No remote repository configured"
    }
} catch {
    Write-Warning "Failed to push to remote. You can push manually later:"
    Write-Host "  git push"
}

# Step 5: Create OpenTimestamps (if available)
Write-Header "Step 5: Create OpenTimestamps"

$hasOts = Get-Command ots -ErrorAction SilentlyContinue
if ($hasOts) {
    Write-Success "Found ots command"
    Write-Host ""
    
    foreach ($file in $FilesToAdd) {
        if (Test-Path $file) {
            Write-Info "Creating OpenTimestamp for: $file"
            
            try {
                ots stamp $file
                Write-Success "Created timestamp: ${file}.ots"
            } catch {
                Write-Warning "Failed to create timestamp for: $file"
            }
        }
    }
    
    Write-Host ""
    Write-Info "OpenTimestamps created. These can be verified against the Bitcoin blockchain."
    Write-Info "To upgrade timestamps later: ots upgrade [file].ots"
    Write-Info "To verify timestamps: ots verify [file].ots"
} else {
    Write-Warning "OpenTimestamps (ots) not found"
    Write-Info "To install OpenTimestamps:"
    Write-Host "  - Python: pip install opentimestamps-client"
    Write-Host "  - Download: https://github.com/opentimestamps/opentimestamps-client"
    Write-Host ""
    Write-Info "OpenTimestamps provides Bitcoin blockchain proof of existence"
    Write-Info "This creates an independent, verifiable timestamp that cannot be altered"
}

# Step 6: Create patent tracking document
Write-Header "Step 6: Create Patent Tracking Document"

$TrackingFile = "$PatentDir\PATENT_TRACKING.md"
$ExpirationDate = (Get-Date $FilingDate).AddMonths(12).ToString("yyyy-MM-dd")
$UtilityDeadline = (Get-Date $FilingDate).AddMonths(11).ToString("yyyy-MM-dd")
$CommitHash = git rev-parse HEAD 2>$null
$IsGpgSigned = (git log -1 --format="%G?" HEAD 2>$null) -match "G"
$OtsCount = (Get-ChildItem -Path "$ProvisionalDir\*.ots", "$ReceiptsDir\*.ots" -ErrorAction SilentlyContinue).Count

$trackingContent = @"
# Patent Tracking Document

## Active Provisional Patents

### 1. Autonomous Charitable Revenue Distribution System

- **Application Number**: $ApplicationNumber
- **Filing Date**: $FilingDate
- **Status**: Patent Pending
- **Type**: Provisional Patent Application
- **Entity Status**: Micro-Entity
- **Filing Fee**: `$75

#### Details

- **Title**: Autonomous Charitable Revenue Distribution System Using AI-Governed DAO with Cryptographic Verification
- **Inventor**: [Your Name]
- **Assignee**: Strategickhaos DAO LLC

#### Important Dates

- **Filing Date**: $FilingDate
- **Expiration Date**: $ExpirationDate
- **Utility Patent Deadline**: $UtilityDeadline

#### Documents

- Provisional Application: ``provisional/STRATEGICKHAOS_PROVISIONAL_${FilingDate}.pdf``
- USPTO Receipt: ``receipts/USPTO_Receipt.pdf``
- Micro-Entity Cert: ``receipts/MICRO_ENTITY_CERT.pdf``

#### Proof Chain

- **Git Commit**: $CommitHash
- **Git Signature**: $(if ($IsGpgSigned) { "GPG Signed" } else { "Unsigned" })
- **OpenTimestamps**: $OtsCount file(s) stamped

#### Next Steps

- [ ] Continue product development and testing
- [ ] Document improvements and iterations
- [ ] Consider international protection (PCT)
- [ ] Begin utility patent preparation (Month 6-9)
- [ ] File utility patent (by Month 11)

#### Notes

[Add any additional notes about the patent here]

---

## Patent Pending Statement

**Use this statement in all materials:**

> **Strategickhaos DAO LLC – Patent Pending (U.S. Provisional Application $ApplicationNumber)**

---

**Last Updated**: $(Get-Date -Format "yyyy-MM-dd")  
**Tracking Version**: 1.0
"@

Set-Content -Path $TrackingFile -Value $trackingContent
Write-Success "Created patent tracking document: $TrackingFile"

# Add and commit the tracking document
git add $TrackingFile
git commit -m "Add patent tracking document for $ApplicationNumber" 2>$null

# Step 7: Summary
Write-Header "Proof Chain Complete"
Write-Host ""
Write-Success "Successfully established proof chain for patent filing"
Write-Host ""
Write-Info "What was created:"
Write-Host "  ✓ Git commits with patent documents"
Write-Host "  ✓ $(if ($IsGpgSigned) { "GPG-signed commit" } else { "Unsigned commit" })"
Write-Host "  ✓ Remote backup (if pushed)"
Write-Host "  ✓ OpenTimestamps (if available): $OtsCount files"
Write-Host "  ✓ Patent tracking document"
Write-Host ""
Write-Info "You can now legally state:"
Write-Host ""
Write-Host "    Patent Pending (U.S. Provisional Application $ApplicationNumber)"
Write-Host ""
Write-Warning "IMPORTANT REMINDERS:"
Write-Host "  1. File utility patent within 12 months (by $ExpirationDate)"
Write-Host "  2. Continue documenting improvements and iterations"
Write-Host "  3. Keep all communications about the patent confidential or under NDA"
Write-Host "  4. Review patent tracking document regularly: $TrackingFile"
Write-Host ""
Write-Success "Proof chain established successfully!"
