# Bitcoin Timestamp Creation Script for SOVEREIGN_MANIFEST_v1.0.md
# This PowerShell script creates an OpenTimestamps .ots file anchoring the manifest to Bitcoin

$ErrorActionPreference = "Stop"

$ManifestFile = "SOVEREIGN_MANIFEST_v1.0.md"
$OtsFile = "$ManifestFile.ots"

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "🔐 SOVEREIGNTY ARCHITECTURE - BITCOIN TIMESTAMP CREATION" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""

# Check if manifest exists
if (-not (Test-Path $ManifestFile)) {
    Write-Host "❌ ERROR: $ManifestFile not found!" -ForegroundColor Red
    Write-Host "   Please run this script from the repository root directory." -ForegroundColor Red
    exit 1
}

# Display manifest info
$FileSize = (Get-Item $ManifestFile).Length
$Hash = (Get-FileHash $ManifestFile -Algorithm SHA256).Hash.ToLower()

# Check for Python command availability
$pythonCmd = $null
foreach ($cmd in @('python', 'python3', 'py')) {
    if (Get-Command $cmd -ErrorAction SilentlyContinue) {
        $pythonCmd = $cmd
        break
    }
}

Write-Host "📄 Manifest File: $ManifestFile" -ForegroundColor White
Write-Host "📊 File Size: $FileSize bytes" -ForegroundColor White
Write-Host "🔑 SHA256 Hash: $Hash" -ForegroundColor Yellow
Write-Host ""

# Method selection
Write-Host "Select timestamp creation method:" -ForegroundColor White
Write-Host "  1) Catallaxy Calendar Server (Invoke-WebRequest - recommended for Windows)" -ForegroundColor Gray
Write-Host "  2) OTS BTC Catallaxy (alternative endpoint)" -ForegroundColor Gray
Write-Host "  3) Alice Calendar (opentimestamps.org)" -ForegroundColor Gray
Write-Host "  4) OpenTimestamps CLI (requires Python + ots command)" -ForegroundColor Gray
Write-Host ""

$method = Read-Host "Enter choice [1-4] (default: 1)"
if ([string]::IsNullOrWhiteSpace($method)) {
    $method = "1"
}

Write-Host ""
Write-Host "🚀 Creating Bitcoin timestamp..." -ForegroundColor Green
Write-Host ""

try {
    switch ($method) {
        "1" {
            Write-Host "Using: https://btc.calendar.catallaxy.com" -ForegroundColor Cyan
            $FileContent = [System.Text.Encoding]::UTF8.GetBytes((Get-Content $ManifestFile -Raw))
            $Response = Invoke-WebRequest -Uri "https://btc.calendar.catallaxy.com" `
                -Method POST `
                -Body $FileContent `
                -ContentType "application/octet-stream" `
                -OutFile $OtsFile `
                -PassThru
            Write-Host "HTTP Status: $($Response.StatusCode)" -ForegroundColor Green
        }
        
        "2" {
            Write-Host "Using: https://ots.btc.catallaxy.com/timestamp" -ForegroundColor Cyan
            $FileContent = [System.Text.Encoding]::UTF8.GetBytes((Get-Content $ManifestFile -Raw))
            $Response = Invoke-WebRequest -Uri "https://ots.btc.catallaxy.com/timestamp" `
                -Method POST `
                -Body $FileContent `
                -ContentType "application/octet-stream" `
                -OutFile $OtsFile `
                -PassThru
            Write-Host "HTTP Status: $($Response.StatusCode)" -ForegroundColor Green
        }
        
        "3" {
            Write-Host "Using: https://alice.btc.calendar.opentimestamps.org/timestamp" -ForegroundColor Cyan
            $FileContent = [System.Text.Encoding]::UTF8.GetBytes((Get-Content $ManifestFile -Raw))
            $Response = Invoke-WebRequest -Uri "https://alice.btc.calendar.opentimestamps.org/timestamp" `
                -Method POST `
                -Body $FileContent `
                -ContentType "application/octet-stream" `
                -OutFile $OtsFile `
                -PassThru
            Write-Host "HTTP Status: $($Response.StatusCode)" -ForegroundColor Green
        }
        
        "4" {
            Write-Host "Using: ots stamp command" -ForegroundColor Cyan
            # Check if ots is installed
            $otsPath = Get-Command ots -ErrorAction SilentlyContinue
            if (-not $otsPath) {
                Write-Host "📦 OpenTimestamps CLI not found. Installing..." -ForegroundColor Yellow
                if (-not $pythonCmd) {
                    Write-Host "❌ ERROR: Python not found. Please install Python first." -ForegroundColor Red
                    exit 1
                }
                & $pythonCmd -m pip install --user opentimestamps-client
            }
            
            # Run ots stamp
            & ots stamp $ManifestFile
        }
        
        default {
            Write-Host "❌ Invalid choice!" -ForegroundColor Red
            exit 1
        }
    }
    
    Write-Host ""
    
    # Verify creation
    if (Test-Path $OtsFile) {
        $OtsSize = (Get-Item $OtsFile).Length
        
        Write-Host "✅ SUCCESS: Bitcoin timestamp created!" -ForegroundColor Green
        Write-Host ""
        Write-Host "📋 Timestamp Details:" -ForegroundColor White
        Write-Host "   File: $OtsFile" -ForegroundColor Gray
        Write-Host "   Size: $OtsSize bytes" -ForegroundColor Gray
        Write-Host ""
        
        # Try to get info if ots is available
        $otsPath = Get-Command ots -ErrorAction SilentlyContinue
        if ($otsPath) {
            Write-Host "🔍 Timestamp Information:" -ForegroundColor White
            try {
                & ots info $OtsFile
            } catch {
                Write-Host "   (Info will be available after Bitcoin confirmation)" -ForegroundColor Gray
            }
            Write-Host ""
        }
        
        Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
        Write-Host "🎉 SOVEREIGNTY: 100% COMPLETE" -ForegroundColor Green
        Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Next steps:" -ForegroundColor White
        Write-Host "  1. Verify timestamp: ots verify $OtsFile" -ForegroundColor Gray
        Write-Host "  2. Commit to repository: git add $OtsFile && git commit -m 'Add Bitcoin timestamp'" -ForegroundColor Gray
        Write-Host "  3. Push to GitHub: git push" -ForegroundColor Gray
        Write-Host ""
        Write-Host "⏰ Note: Bitcoin confirmation takes 10-60 minutes on average." -ForegroundColor Yellow
        Write-Host "        The timestamp is valid immediately but gains more security with each block." -ForegroundColor Yellow
        Write-Host ""
        Write-Host "🖤 You are sovereignty. Forever." -ForegroundColor Magenta
        Write-Host ""
    } else {
        Write-Host "❌ ERROR: Failed to create timestamp file!" -ForegroundColor Red
        Write-Host "   Please check network connectivity and try again." -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host ""
    Write-Host "❌ ERROR: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "Troubleshooting tips:" -ForegroundColor Yellow
    Write-Host "  - Ensure you have internet connectivity" -ForegroundColor Gray
    Write-Host "  - Try a different method (options 1-4)" -ForegroundColor Gray
    Write-Host "  - Check if firewall is blocking connections" -ForegroundColor Gray
    Write-Host "  - Verify the calendar server is accessible" -ForegroundColor Gray
    Write-Host ""
    exit 1
}
