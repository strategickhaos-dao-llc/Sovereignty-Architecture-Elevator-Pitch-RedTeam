# timestamp_sovereign_docs.ps1
# PowerShell script for OpenTimestamps workflow on Windows
#
# Usage:
#   .\timestamp_sovereign_docs.ps1 -Action stamp
#   .\timestamp_sovereign_docs.ps1 -Action upgrade
#   .\timestamp_sovereign_docs.ps1 -Action verify
#   .\timestamp_sovereign_docs.ps1 -Action info
#   .\timestamp_sovereign_docs.ps1 -Action all

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("stamp", "upgrade", "verify", "info", "report", "all")]
    [string]$Action
)

# Files to timestamp
$SovereignFiles = @(
    "SOVEREIGN_MANIFEST_v1.0.md",
    "README.md",
    "SECURITY.md",
    "dao_record_v1.0.yaml",
    "CONTRIBUTORS.md"
)

# Color functions
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

function Write-Success {
    param([string]$Message)
    Write-ColorOutput "✓ $Message" "Green"
}

function Write-Warning {
    param([string]$Message)
    Write-ColorOutput "⚠ $Message" "Yellow"
}

function Write-Error {
    param([string]$Message)
    Write-ColorOutput "✗ $Message" "Red"
}

function Write-Info {
    param([string]$Message)
    Write-ColorOutput "ℹ $Message" "Cyan"
}

# Check if OTS is installed
function Test-OtsInstalled {
    try {
        $null = Get-Command ots -ErrorAction Stop
        return $true
    } catch {
        Write-Error "OpenTimestamps client not found"
        Write-Host "Install with: pip install opentimestamps-client"
        return $false
    }
}

# Print banner
function Show-Banner {
    Write-ColorOutput "================================================" "Blue"
    Write-ColorOutput "  OpenTimestamps Sovereign Document Workflow" "Blue"
    Write-ColorOutput "================================================" "Blue"
    Write-Host ""
}

# Stamp all documents
function Invoke-StampDocuments {
    Write-Warning "Stamping sovereign documents..."
    Write-Host ""
    
    $count = 0
    foreach ($file in $SovereignFiles) {
        if (Test-Path $file) {
            Write-ColorOutput "Timestamping: $file" "Green"
            
            $otsFile = "$file.ots"
            if (Test-Path $otsFile) {
                Write-Warning "  Timestamp file already exists: $otsFile"
                $response = Read-Host "  Overwrite? (y/N)"
                if ($response -ne 'y' -and $response -ne 'Y') {
                    Write-Info "  Skipping"
                    continue
                }
            }
            
            try {
                $output = ots stamp $file 2>&1
                if ($LASTEXITCODE -eq 0) {
                    Write-Success "  Created: $otsFile"
                    $count++
                } else {
                    Write-Error "  Failed to timestamp"
                }
            } catch {
                Write-Error "  Failed to timestamp: $_"
            }
            Write-Host ""
        } else {
            Write-Warning "File not found: $file"
            Write-Host ""
        }
    }
    
    Write-Success "Stamped $count document(s)"
    Write-Info "Note: Run with -Action upgrade after 1-2 hours to get Bitcoin confirmation"
    Write-Host ""
}

# Upgrade timestamps
function Invoke-UpgradeTimestamps {
    Write-Warning "Upgrading timestamps to Bitcoin blockchain..."
    Write-Host ""
    
    $upgraded = 0
    $pending = 0
    
    foreach ($file in $SovereignFiles) {
        $otsFile = "$file.ots"
        if (Test-Path $otsFile) {
            Write-ColorOutput "Upgrading: $otsFile" "Green"
            
            try {
                $output = ots upgrade $otsFile 2>&1 | Out-String
                
                if ($LASTEXITCODE -eq 0 -and $output -match "Success") {
                    Write-Success "  Upgraded successfully"
                    $upgraded++
                } elseif ($output -match "Pending") {
                    Write-Warning "  Still pending Bitcoin confirmation"
                    $pending++
                } else {
                    Write-Info "  Already up to date"
                }
            } catch {
                Write-Error "  Upgrade failed: $_"
            }
            Write-Host ""
        }
    }
    
    Write-Success "Upgraded: $upgraded"
    Write-Warning "Pending: $pending"
    
    if ($pending -gt 0) {
        Write-Info "Note: Pending timestamps will be confirmed after Bitcoin block inclusion (usually 1-2 hours)"
    }
    Write-Host ""
}

# Verify timestamps
function Invoke-VerifyTimestamps {
    Write-Warning "Verifying all timestamps..."
    Write-Host ""
    
    $verified = 0
    $pending = 0
    $failed = 0
    
    foreach ($file in $SovereignFiles) {
        $otsFile = "$file.ots"
        if (Test-Path $otsFile) {
            Write-ColorOutput "Verifying: $otsFile" "Green"
            
            try {
                $output = ots verify $otsFile 2>&1 | Out-String
                
                if ($LASTEXITCODE -eq 0 -and $output -match "Success") {
                    Write-Success "  Verified"
                    if ($output -match "block (\d+)") {
                        $block = $Matches[1]
                        Write-Host "    Block: $block"
                    }
                    if ($output -match "(\d{4}-\d{2}-\d{2})") {
                        $date = $Matches[1]
                        Write-Host "    Date: $date"
                    }
                    $verified++
                } elseif ($output -match "Pending") {
                    Write-Warning "  Pending Bitcoin confirmation"
                    $pending++
                } else {
                    Write-Error "  Verification failed"
                    $failed++
                }
            } catch {
                Write-Error "  Verification failed: $_"
                $failed++
            }
            Write-Host ""
        } else {
            Write-Warning "Timestamp not found: $otsFile"
            Write-Host ""
        }
    }
    
    Write-Host "Summary:"
    Write-Success "  Verified: $verified"
    Write-Warning "  Pending: $pending"
    Write-Error "  Failed: $failed"
    Write-Host ""
}

# Show timestamp info
function Show-TimestampInfo {
    Write-Warning "Timestamp details..."
    Write-Host ""
    
    foreach ($file in $SovereignFiles) {
        $otsFile = "$file.ots"
        if (Test-Path $otsFile) {
            Write-ColorOutput "═══════════════════════════════════════" "Green"
            Write-ColorOutput "File: $otsFile" "Green"
            Write-ColorOutput "═══════════════════════════════════════" "Green"
            ots info $otsFile
            Write-Host ""
        }
    }
}

# Generate report
function New-TimestampReport {
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $reportFile = "timestamp_report_$timestamp.txt"
    
    Write-Warning "Generating timestamp report..."
    Write-Host ""
    
    $report = @"
========================================
OpenTimestamps Verification Report
Generated: $(Get-Date)
========================================

"@
    
    foreach ($file in $SovereignFiles) {
        $otsFile = "$file.ots"
        if (Test-Path $otsFile) {
            $report += "Document: $file`n"
            $report += "----------------------------------------`n"
            
            # File hash
            $hash = (Get-FileHash $file -Algorithm SHA256).Hash
            $report += "SHA256: $hash`n"
            
            # Verification status
            try {
                $output = ots verify $otsFile 2>&1 | Out-String
                if ($output -match "Success") {
                    $report += "Status: ✓ VERIFIED`n"
                    if ($output -match "block (\d+)") {
                        $report += "Block: $($Matches[1])`n"
                    }
                    if ($output -match "as of (.+)") {
                        $report += "Date: $($Matches[1])`n"
                    }
                } elseif ($output -match "Pending") {
                    $report += "Status: ⏳ PENDING`n"
                } else {
                    $report += "Status: ✗ VERIFICATION FAILED`n"
                }
            } catch {
                $report += "Status: ✗ ERROR`n"
            }
            
            $report += "`n"
        }
    }
    
    $report += @"
========================================
End of Report
========================================
"@
    
    $report | Out-File -FilePath $reportFile -Encoding UTF8
    
    Write-Success "Report generated: $reportFile"
    Write-Host ""
}

# Run complete workflow
function Invoke-CompleteWorkflow {
    Show-Banner
    
    Write-Info "Running complete OpenTimestamps workflow..."
    Write-Host ""
    
    # Step 1: Verify
    Write-ColorOutput "Step 1: Verify existing timestamps" "Blue"
    Invoke-VerifyTimestamps
    
    $response = Read-Host "Continue to stamping? (Y/n)"
    if ($response -eq 'n' -or $response -eq 'N') {
        return
    }
    
    # Step 2: Stamp
    Write-ColorOutput "Step 2: Stamp documents" "Blue"
    Invoke-StampDocuments
    
    $response = Read-Host "Continue to upgrade? (Y/n)"
    if ($response -eq 'n' -or $response -eq 'N') {
        return
    }
    
    # Step 3: Upgrade
    Write-ColorOutput "Step 3: Upgrade timestamps" "Blue"
    Invoke-UpgradeTimestamps
    
    # Step 4: Report
    Write-ColorOutput "Step 4: Generate report" "Blue"
    New-TimestampReport
    
    Write-Success "Workflow complete!"
}

# Main execution
Show-Banner

if (-not (Test-OtsInstalled)) {
    exit 1
}

switch ($Action) {
    "stamp" {
        Invoke-StampDocuments
    }
    "upgrade" {
        Invoke-UpgradeTimestamps
    }
    "verify" {
        Invoke-VerifyTimestamps
    }
    "info" {
        Show-TimestampInfo
    }
    "report" {
        New-TimestampReport
    }
    "all" {
        Invoke-CompleteWorkflow
    }
}
