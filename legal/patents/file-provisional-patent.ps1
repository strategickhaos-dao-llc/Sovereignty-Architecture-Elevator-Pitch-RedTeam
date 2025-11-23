# USPTO Provisional Patent Filing Automation Script (PowerShell)
# For Strategickhaos DAO LLC - Autonomous Charitable Revenue Distribution System
# 
# This script automates the preparation steps for filing a provisional patent application
# with the USPTO. It does NOT submit the application (that must be done manually via EFS-Web).
#
# Usage: .\file-provisional-patent.ps1

param(
    [string]$InventorName = "Domenic Garza",
    [string]$PatentTitle = "Autonomous Charitable Revenue Distribution System Using AI-Governed DAO with Cryptographic Verification",
    [string]$ApplicationDate = (Get-Date -Format "yyyy-MM-dd")
)

# Color output functions
function Write-Success { Write-Host "✓ $args" -ForegroundColor Green }
function Write-Info { Write-Host "ℹ $args" -ForegroundColor Cyan }
function Write-Warning { Write-Host "⚠ $args" -ForegroundColor Yellow }
function Write-Error { Write-Host "✗ $args" -ForegroundColor Red }
function Write-Header { Write-Host "`n=== $args ===" -ForegroundColor Magenta }

# Configuration
$RepoRoot = Split-Path -Parent $PSScriptRoot
$PatentDir = "$RepoRoot\legal\patents"
$ProvisionalDir = "$PatentDir\provisional"
$ReceiptsDir = "$PatentDir\receipts"
$TemplatesDir = "$PatentDir\templates"

Write-Header "USPTO Provisional Patent Filing Preparation"
Write-Info "Inventor: $InventorName"
Write-Info "Title: $PatentTitle"
Write-Info "Date: $ApplicationDate"
Write-Host ""

# Step 0: Check and create directories
Write-Header "Step 0: Directory Setup"
$directories = @($ProvisionalDir, $ReceiptsDir, $TemplatesDir)
foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Success "Created directory: $dir"
    } else {
        Write-Info "Directory exists: $dir"
    }
}

# Step 1: Download Micro-Entity Certification Form
Write-Header "Step 1: Micro-Entity Certification (SB/15A)"
$MicroEntityFormUrl = "https://www.uspto.gov/sites/default/files/documents/sb0015a.pdf"
$MicroEntityFormPath = "$ReceiptsDir\SB15A_MICRO_ENTITY_FORM.pdf"

if (-not (Test-Path $MicroEntityFormPath)) {
    Write-Info "Downloading micro-entity certification form..."
    try {
        Start-Process $MicroEntityFormUrl
        Write-Success "Opened micro-entity form in browser"
        Write-Warning "ACTION REQUIRED: Download and save the form as: $MicroEntityFormPath"
        Write-Warning "Fill in your name, sign, and date the form"
    } catch {
        Write-Error "Failed to open browser. Please manually download from: $MicroEntityFormUrl"
    }
} else {
    Write-Info "Micro-entity form already exists: $MicroEntityFormPath"
}

# Step 2: Check for provisional application document
Write-Header "Step 2: Provisional Application Document"
$ProvisionalAppPath = "$ProvisionalDir\PROVISIONAL_PATENT_APPLICATION.md"
$ProvisionalPdfPath = "$ProvisionalDir\STRATEGICKHAOS_PROVISIONAL_$ApplicationDate.pdf"

if (-not (Test-Path $ProvisionalAppPath)) {
    Write-Warning "Provisional application not found at: $ProvisionalAppPath"
    Write-Info "Creating template provisional application..."
    
    $templateContent = @"
# $PatentTitle

**Inventor**: $InventorName  
**Date**: $ApplicationDate  
**Application Type**: Provisional Patent Application

## Field of the Invention

This invention relates to autonomous charitable revenue distribution systems that utilize artificial intelligence governance, distributed autonomous organization (DAO) architecture, and cryptographic verification mechanisms.

## Background

[Describe the problem your invention solves and the current state of the art]

## Summary of the Invention

[Provide a brief summary of your invention - what it does and how it's novel]

## Detailed Description

### System Architecture

[Describe the technical architecture of your system]

### Components

#### 1. DAO Governance Layer
[Describe the DAO structure and governance mechanisms]

#### 2. AI Decision Engine
[Describe how AI is used in the system]

#### 3. Charitable Distribution Mechanism
[Describe how charitable distributions work]

#### 4. Cryptographic Verification System
[Describe the cryptographic elements]

### Operation

[Describe how the system operates step-by-step]

### Novel Features

1. [List novel feature 1]
2. [List novel feature 2]
3. [List novel feature 3]

## Claims (for future utility patent)

[Optional: Draft preliminary claims]

## Figures

[Include system diagrams, flowcharts, or screenshots]

## Best Mode

[Describe your preferred implementation method]

## Advantages

[List the advantages of your invention over prior art]

---

**End of Provisional Patent Application**
"@
    
    Set-Content -Path $ProvisionalAppPath -Value $templateContent
    Write-Success "Created template at: $ProvisionalAppPath"
    Write-Warning "ACTION REQUIRED: Edit the template with your invention details"
} else {
    Write-Info "Provisional application found: $ProvisionalAppPath"
}

# Step 3: Convert to PDF using available tools
Write-Header "Step 3: Convert to USPTO-Ready PDF"

if (Test-Path $ProvisionalAppPath) {
    Write-Info "Checking for PDF conversion tools..."
    
    # Check for Pandoc
    $hasPandoc = Get-Command pandoc -ErrorAction SilentlyContinue
    
    if ($hasPandoc) {
        Write-Success "Found Pandoc - attempting conversion..."
        try {
            & pandoc $ProvisionalAppPath -o $ProvisionalPdfPath --pdf-engine=weasyprint -V geometry:margin=1in
            Write-Success "Created PDF: $ProvisionalPdfPath"
        } catch {
            Write-Warning "Pandoc conversion failed. Try: pandoc $ProvisionalAppPath -o $ProvisionalPdfPath"
        }
    } else {
        Write-Warning "Pandoc not found. Install from: https://pandoc.org/"
        Write-Info "Alternative: Open the markdown file in Word/Google Docs and export as PDF"
        Write-Info "  - Set page size to US Letter (8.5 x 11)"
        Write-Info "  - Set margins to 1 inch on all sides"
        Write-Info "  - Use 12-point font or larger"
        Write-Info "  - Save as: $ProvisionalPdfPath"
    }
}

# Step 4: Open USPTO EFS-Web
Write-Header "Step 4: USPTO EFS-Web Filing"
$EfsWebUrl = "https://efs.uspto.gov/EFS-Web2/"

Write-Info "When you're ready to file, this script will open the USPTO EFS-Web portal"
Write-Host ""
Write-Warning "Before proceeding, ensure you have:"
Write-Host "  [1] Completed and signed micro-entity form (SB/15A)"
Write-Host "  [2] Your provisional application as a PDF"
Write-Host "  [3] USPTO.gov account credentials"
Write-Host "  [4] Payment method ready (\$75 for micro-entity)"
Write-Host ""

$ready = Read-Host "Open USPTO EFS-Web now? (y/N)"
if ($ready -eq "y" -or $ready -eq "Y") {
    Start-Process $EfsWebUrl
    Write-Success "Opened USPTO EFS-Web in browser"
    Write-Host ""
    Write-Info "Follow these steps in EFS-Web:"
    Write-Host "  1. Login or create account"
    Write-Host "  2. Click 'New Application'"
    Write-Host "  3. Select 'Provisional Application'"
    Write-Host "  4. Select 'Micro Entity (SB/15A)'"
    Write-Host "  5. Upload your micro-entity certification PDF"
    Write-Host "  6. Enter inventor information:"
    Write-Host "     - Name: $InventorName"
    Write-Host "     - Address: [Your Wyoming DAO address]"
    Write-Host "  7. Enter title: $PatentTitle"
    Write-Host "  8. Upload provisional application PDF: $ProvisionalPdfPath"
    Write-Host "  9. Validate submission"
    Write-Host " 10. Pay \$75 filing fee"
    Write-Host " 11. Submit application"
    Write-Host " 12. Save confirmation and filing receipt"
} else {
    Write-Info "Skipped opening EFS-Web. You can open it manually: $EfsWebUrl"
}

# Step 5: Post-filing instructions
Write-Header "Step 5: After Filing - Proof Chain Setup"
Write-Host ""
Write-Warning "AFTER you receive your USPTO filing receipt:"
Write-Host ""
Write-Info "1. Save your filing receipt as: $ReceiptsDir\USPTO_Receipt.pdf"
Write-Info "2. Note your application number (format: 63/XXXXXX)"
Write-Host ""
Write-Info "3. Run the proof chain script:"
Write-Host "   .\legal\patents\create-proof-chain.ps1 -ApplicationNumber '63/XXXXXX'"
Write-Host ""
Write-Info "Or manually:"
Write-Host "   git add legal/patents/provisional/*.pdf"
Write-Host "   git add legal/patents/receipts/*.pdf"
Write-Host "   git commit -S -m 'PATENT PENDING: Provisional 63/XXXXXX filed $ApplicationDate'"
Write-Host "   git push"
Write-Host ""
Write-Info "4. Create OpenTimestamps (if ots.exe available):"
Write-Host "   ots stamp $ProvisionalPdfPath"
Write-Host "   ots stamp $ReceiptsDir\USPTO_Receipt.pdf"

# Step 6: Summary
Write-Header "Summary"
Write-Host ""
Write-Success "Preparation complete!"
Write-Host ""
Write-Info "Next Steps:"
Write-Host "  1. Complete and sign micro-entity form if not done"
Write-Host "  2. Review and finalize your provisional application"
Write-Host "  3. Convert to PDF with proper formatting"
Write-Host "  4. File via USPTO EFS-Web (https://efs.uspto.gov/EFS-Web2/)"
Write-Host "  5. Save filing receipt when received"
Write-Host "  6. Run proof chain script to establish cryptographic verification"
Write-Host ""
Write-Info "Cost: \$75 (micro-entity filing fee)"
Write-Info "Time: 15-45 minutes to file"
Write-Info "Result: Patent Pending status + priority date"
Write-Host ""
Write-Success "You will be able to state: 'Patent Pending (U.S. Provisional Application 63/XXXXXX)'"
Write-Host ""
Write-Warning "IMPORTANT: File utility patent within 12 months to maintain priority!"
Write-Host ""

# Open the guide
$guidePath = "$PatentDir\USPTO_FILING_GUIDE.md"
if (Test-Path $guidePath) {
    Write-Info "Opening filing guide..."
    Start-Process $guidePath
}

Write-Host "Script complete. Review the USPTO_FILING_GUIDE.md for detailed instructions." -ForegroundColor Green
