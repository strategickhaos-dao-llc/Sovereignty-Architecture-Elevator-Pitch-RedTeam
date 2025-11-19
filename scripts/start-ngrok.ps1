# Start ngrok tunnels for Sovereignty Architecture local development
# PowerShell version for Windows users
# Usage: .\scripts\start-ngrok.ps1

# Color functions
function Write-ColorOutput($ForegroundColor) {
    $fc = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor
    if ($args) {
        Write-Output $args
    }
    $host.UI.RawUI.ForegroundColor = $fc
}

Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Blue
Write-Host "║  Sovereignty Architecture - ngrok Tunnel Setup            ║" -ForegroundColor Blue
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Blue
Write-Host ""

# Check if ngrok is installed
$ngrokInstalled = Get-Command ngrok -ErrorAction SilentlyContinue

if (-not $ngrokInstalled) {
    Write-Host "❌ ngrok is not installed" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install ngrok:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Using Chocolatey (recommended):" -ForegroundColor Yellow
    Write-Host "  choco install ngrok" -ForegroundColor White
    Write-Host ""
    Write-Host "OR download manually:" -ForegroundColor Yellow
    Write-Host "  1. Visit: https://ngrok.com/download" -ForegroundColor White
    Write-Host "  2. Download the Windows installer" -ForegroundColor White
    Write-Host "  3. Extract ngrok.exe to C:\ngrok or add to PATH" -ForegroundColor White
    Write-Host ""
    Write-Host "After installation, restart PowerShell and run this script again" -ForegroundColor Yellow
    Write-Host ""
    exit 1
}

Write-Host "✓ ngrok is installed" -ForegroundColor Green

# Check if ngrok config exists
$configFile = "ngrok.yml"
if (-not (Test-Path $configFile)) {
    Write-Host "❌ ngrok.yml configuration file not found" -ForegroundColor Red
    Write-Host "Please create ngrok.yml in the repository root" -ForegroundColor Yellow
    exit 1
}

Write-Host "✓ Configuration file found" -ForegroundColor Green

# Check if authtoken is configured
$configContent = Get-Content $configFile -Raw
if ($configContent -match "YOUR_NGROK_AUTHTOKEN") {
    Write-Host "⚠ Warning: Default authtoken detected" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Please update ngrok.yml with your authtoken:" -ForegroundColor Yellow
    Write-Host "  1. Sign up at https://ngrok.com" -ForegroundColor White
    Write-Host "  2. Get your authtoken from https://dashboard.ngrok.com/get-started/your-authtoken" -ForegroundColor White
    Write-Host "  3. Replace YOUR_NGROK_AUTHTOKEN in ngrok.yml" -ForegroundColor White
    Write-Host ""
    $response = Read-Host "Continue anyway? (y/N)"
    if ($response -ne "y" -and $response -ne "Y") {
        exit 1
    }
}

# Create logs directory if it doesn't exist
if (-not (Test-Path "logs")) {
    New-Item -ItemType Directory -Path "logs" | Out-Null
}

Write-Host ""
Write-Host "Starting ngrok tunnels..." -ForegroundColor Blue
Write-Host ""

# Start ngrok with the configuration
$ngrokProcess = Start-Process -FilePath "ngrok" -ArgumentList "start", "--all", "--config=$configFile" -NoNewWindow -PassThru

# Wait for ngrok to start
Start-Sleep -Seconds 3

# Check if ngrok is running
if (-not $ngrokProcess -or $ngrokProcess.HasExited) {
    Write-Host "❌ Failed to start ngrok" -ForegroundColor Red
    exit 1
}

Write-Host "✓ ngrok tunnels started successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Blue
Write-Host "🌐 Tunnel URLs:" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Blue
Write-Host ""

# Get tunnel information
Start-Sleep -Seconds 2
try {
    $tunnels = Invoke-RestMethod -Uri "http://localhost:4040/api/tunnels" -ErrorAction SilentlyContinue
    foreach ($tunnel in $tunnels.tunnels) {
        $name = $tunnel.name.PadRight(20)
        $url = $tunnel.public_url
        Write-Host "  $name $url" -ForegroundColor White
    }
} catch {
    Write-Host "  Unable to fetch tunnel info. Check http://localhost:4040" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Blue
Write-Host "📊 Inspection Interface:" -ForegroundColor Yellow
Write-Host "  http://localhost:4040"
Write-Host ""
Write-Host "📝 Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Visit http://localhost:4040 to see tunnel status"
Write-Host "  2. Copy the event-gateway URL for GitHub webhook configuration"
Write-Host "  3. Configure GitHub webhook with URL: https://your-tunnel.ngrok.io/webhook"
Write-Host "  4. Ensure your local services are running:"
Write-Host "     - Event Gateway on port 8080"
Write-Host "     - Discord Bot on port 3000"
Write-Host "     - Refinory on port 8000"
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Blue
Write-Host ""
Write-Host "Opening ngrok web interface..." -ForegroundColor Green
Start-Process "http://localhost:4040"
Write-Host ""
Write-Host "Press Ctrl+C to stop all tunnels" -ForegroundColor Green
Write-Host ""

# Keep the script running
try {
    while ($true) {
        Start-Sleep -Seconds 1
        if ($ngrokProcess.HasExited) {
            Write-Host "ngrok process has exited" -ForegroundColor Yellow
            break
        }
    }
} finally {
    # Cleanup
    if (-not $ngrokProcess.HasExited) {
        Write-Host ""
        Write-Host "Stopping ngrok..." -ForegroundColor Yellow
        Stop-Process -Id $ngrokProcess.Id -Force -ErrorAction SilentlyContinue
    }
    Write-Host "Tunnels stopped" -ForegroundColor Green
}
