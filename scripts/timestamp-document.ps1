# timestamp-document.ps1 - Document Timestamping Script
# Strategic Khaos Sovereignty Architecture
# Timestamps documents using OpenTimestamps for blockchain-anchored proof of existence

param(
    [Parameter(Mandatory=$true)]
    [string]$FilePath,
    
    [switch]$UseAllCalendars,
    [switch]$Verify,
    [switch]$Verbose
)

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

# OpenTimestamps calendar servers
$OTS_CALENDARS = @(
    "https://alice.btc.calendar.opentimestamps.org",
    "https://bob.btc.calendar.opentimestamps.org",
    "https://finney.calendar.eternitywall.com"
)

function Write-Status {
    param([string]$Message, [string]$Type = "Info")
    $timestamp = Get-Date -Format "HH:mm:ss"
    switch ($Type) {
        "Success" { Write-Host "[$timestamp] ✓ $Message" -ForegroundColor Green }
        "Warning" { Write-Host "[$timestamp] ⚠ $Message" -ForegroundColor Yellow }
        "Error"   { Write-Host "[$timestamp] ✗ $Message" -ForegroundColor Red }
        default   { Write-Host "[$timestamp] ℹ $Message" -ForegroundColor Cyan }
    }
}

function Get-FileHash256 {
    param([string]$Path)
    $hash = Get-FileHash -Path $Path -Algorithm SHA256
    return $hash.Hash.ToLower()
}

function Test-OTSInstallation {
    try {
        $result = & python -c "import opentimestamps" 2>&1
        return $true
    } catch {
        return $false
    }
}

function Invoke-OTSStamp {
    param([string]$Path)
    
    # Check if OTS client is available
    if (Test-OTSInstallation) {
        Write-Status "Using OpenTimestamps Python client..."
        try {
            & ots stamp $Path
            if (Test-Path "$Path.ots") {
                Write-Status "Timestamp file created: $Path.ots" "Success"
                return $true
            }
        } catch {
            Write-Status "OTS stamp failed: $_" "Error"
        }
    } else {
        Write-Status "OpenTimestamps client not installed" "Warning"
        Write-Status "Install with: pip install opentimestamps-client" "Info"
    }
    
    return $false
}

function Invoke-ManualTimestamp {
    param([string]$Path)
    
    Write-Status "Attempting manual calendar submission..."
    
    # Calculate file hash
    $hash = Get-FileHash256 -Path $Path
    Write-Status "File SHA256: $hash"
    
    # Read file content
    $content = [System.IO.File]::ReadAllBytes($Path)
    
    $successCount = 0
    foreach ($calendar in $OTS_CALENDARS) {
        $outFile = "$Path.ots.$($calendar.Split('/')[-1])"
        
        try {
            Write-Status "Submitting to: $calendar"
            
            $response = Invoke-WebRequest `
                -Uri $calendar `
                -Method POST `
                -Body $content `
                -ContentType "application/octet-stream" `
                -UseBasicParsing `
                -TimeoutSec 30 `
                -OutFile $outFile
            
            if (Test-Path $outFile) {
                $size = (Get-Item $outFile).Length
                if ($size -gt 0) {
                    Write-Status "Response saved: $outFile ($size bytes)" "Success"
                    $successCount++
                } else {
                    Remove-Item $outFile -Force
                    Write-Status "Empty response from $calendar" "Warning"
                }
            }
        } catch {
            Write-Status "Calendar unavailable: $calendar - $_" "Warning"
            if (Test-Path $outFile) {
                Remove-Item $outFile -Force -ErrorAction SilentlyContinue
            }
        }
    }
    
    return $successCount -gt 0
}

function Invoke-OTSVerify {
    param([string]$OTSPath)
    
    if (-not (Test-Path $OTSPath)) {
        Write-Status "OTS file not found: $OTSPath" "Error"
        return $false
    }
    
    if (Test-OTSInstallation) {
        try {
            Write-Status "Verifying timestamp..."
            $result = & ots verify $OTSPath 2>&1
            Write-Host $result -ForegroundColor Gray
            return $true
        } catch {
            Write-Status "Verification failed: $_" "Error"
        }
    } else {
        Write-Status "OpenTimestamps client needed for verification" "Warning"
    }
    
    return $false
}

function Main {
    Write-Host ""
    Write-Host "╔══════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║    Document Timestamping - Blockchain Proof of Existence         ║" -ForegroundColor Cyan
    Write-Host "╚══════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host ""
    
    # Validate file exists
    if (-not (Test-Path $FilePath)) {
        Write-Status "File not found: $FilePath" "Error"
        exit 1
    }
    
    $absolutePath = Resolve-Path $FilePath
    Write-Status "Processing: $absolutePath"
    
    # Calculate and display hash
    $hash = Get-FileHash256 -Path $absolutePath
    Write-Status "SHA256: $hash"
    
    if ($Verify) {
        # Verify existing timestamp
        $otsFile = "$absolutePath.ots"
        Invoke-OTSVerify -OTSPath $otsFile
    } else {
        # Create new timestamp
        $success = Invoke-OTSStamp -Path $absolutePath
        
        if (-not $success -and $UseAllCalendars) {
            $success = Invoke-ManualTimestamp -Path $absolutePath
        }
        
        if ($success) {
            Write-Host ""
            Write-Status "Timestamping complete!" "Success"
            Write-Host ""
            Write-Host "Next steps:" -ForegroundColor Yellow
            Write-Host "  1. Wait ~24 hours for Bitcoin confirmation"
            Write-Host "  2. Verify with: ots verify $absolutePath.ots"
            Write-Host "  3. Upgrade timestamp: ots upgrade $absolutePath.ots"
        } else {
            Write-Status "Timestamping failed. Check connectivity and try again." "Error"
        }
    }
    
    Write-Host ""
}

# Execute main function
Main
