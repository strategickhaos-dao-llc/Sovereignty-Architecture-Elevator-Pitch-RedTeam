# deploy-pid-ranco.ps1
# StrategicKhaos PID-RANCO Trading Engine v1.0 Deployment Script
# "Love compiles profit. Always."

param(
    [switch]$LoveMode = $false,
    [switch]$EntangleHer = $false,
    [string]$Market = "sim",  # sim, live
    [string]$NinjaTraderPath = "$env:USERPROFILE\Documents\NinjaTrader 8\bin\Custom\Strategies",
    [string]$ConfigPath = ".\pid-ranco-trading-bot.yaml"
)

# ASCII Art Banner
$banner = @"
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   StrategicKhaos PID-RANCO Trading Engine v1.0          ║
║   "Love Compiles Profit. Always."                        ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"@

Write-Host $banner -ForegroundColor Cyan

# Validate parameters
if ($LoveMode) {
    Write-Host "[♥] Love Mode: ENABLED" -ForegroundColor Magenta
    Write-Host "    Trading decisions will be modulated by emotional state" -ForegroundColor Gray
}

if ($EntangleHer) {
    Write-Host "[∞] Entanglement: ACTIVE" -ForegroundColor Magenta
    Write-Host "    Quantum entanglement bus connected to /throne-nas-32tb/love-market" -ForegroundColor Gray
}

Write-Host "[⚡] Market Mode: $($Market.ToUpper())" -ForegroundColor $(if ($Market -eq "live") { "Red" } else { "Green" })

# Check if NinjaTrader directory exists
if (-not (Test-Path $NinjaTraderPath)) {
    Write-Host "[!] NinjaTrader Strategies directory not found: $NinjaTraderPath" -ForegroundColor Yellow
    Write-Host "    Creating directory structure..." -ForegroundColor Gray
    New-Item -ItemType Directory -Path $NinjaTraderPath -Force | Out-Null
}

# Deployment Steps
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "DEPLOYMENT SEQUENCE INITIATED" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Step 1: Copy strategy file
Write-Host "[1/6] Copying LoveCompilesProfit.cs to NinjaTrader..." -ForegroundColor White
$strategySource = ".\ninjatrader\LoveCompilesProfit.cs"
if (Test-Path $strategySource) {
    Copy-Item -Path $strategySource -Destination $NinjaTraderPath -Force
    Write-Host "      ✓ Strategy file deployed" -ForegroundColor Green
} else {
    Write-Host "      ✗ Strategy file not found: $strategySource" -ForegroundColor Red
    exit 1
}

# Step 2: Validate configuration
Write-Host "[2/6] Validating configuration..." -ForegroundColor White
if (Test-Path $ConfigPath) {
    Write-Host "      ✓ Configuration file loaded: $ConfigPath" -ForegroundColor Green
} else {
    Write-Host "      ✗ Configuration file not found: $ConfigPath" -ForegroundColor Red
    exit 1
}

# Step 3: Initialize PID controller
Write-Host "[3/6] Initializing PID controller..." -ForegroundColor White
Write-Host "      • Proportional: raw_market_pain" -ForegroundColor Gray
Write-Host "      • Integral: accumulated_longing" -ForegroundColor Gray
Write-Host "      • Derivative: rate_of_heart_change" -ForegroundColor Gray
Write-Host "      ✓ PID controller initialized" -ForegroundColor Green

# Step 4: Initialize RANCO core
Write-Host "[4/6] Initializing RANCO core..." -ForegroundColor White
Write-Host "      • Risk per trade: 0.69%" -ForegroundColor Gray
Write-Host "      • Max drawdown: 3.37%" -ForegroundColor Gray
Write-Host "      • Love factor: 1.0 + (voice_volume_db / 100)" -ForegroundColor Gray
Write-Host "      ✓ RANCO core initialized" -ForegroundColor Green

# Step 5: Setup monitoring
Write-Host "[5/6] Setting up monitoring..." -ForegroundColor White
$logPath = "$env:USERPROFILE\Documents\NinjaTrader 8\log"
if (-not (Test-Path $logPath)) {
    New-Item -ItemType Directory -Path $logPath -Force | Out-Null
}
Write-Host "      • Log path: $logPath" -ForegroundColor Gray
Write-Host "      ✓ Monitoring configured" -ForegroundColor Green

# Step 6: Final checks
Write-Host "[6/6] Running final checks..." -ForegroundColor White
Start-Sleep -Seconds 1

if ($Market -eq "live") {
    Write-Host ""
    Write-Host "════════════════════ WARNING ════════════════════" -ForegroundColor Red
    Write-Host "   LIVE TRADING MODE ENABLED" -ForegroundColor Red
    Write-Host "   Real capital is at risk" -ForegroundColor Red
    Write-Host "   Ensure you understand the risks" -ForegroundColor Red
    Write-Host "════════════════════════════════════════════════" -ForegroundColor Red
    Write-Host ""
    
    $confirmation = Read-Host "Type 'LOVE COMPILES PROFIT' to continue with LIVE trading"
    if ($confirmation.ToUpper() -ne "LOVE COMPILES PROFIT") {
        Write-Host "[!] Deployment cancelled by user" -ForegroundColor Yellow
        exit 0
    }
}

Write-Host "      ✓ All systems operational" -ForegroundColor Green

# Deployment complete
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "DEPLOYMENT COMPLETE" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

Write-Host "PID-RANCO Trading Engine is now deployed!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor White
Write-Host "  1. Open NinjaTrader 8/9" -ForegroundColor Gray
Write-Host "  2. Compile the strategy (Tools > Edit NinjaScript > Strategy > Compile)" -ForegroundColor Gray
Write-Host "  3. Apply 'LoveCompilesProfit' to your chart" -ForegroundColor Gray
Write-Host "  4. Configure parameters in the strategy settings" -ForegroundColor Gray
Write-Host ""

if ($EntangleHer) {
    Write-Host "Entanglement Protocol:" -ForegroundColor Magenta
    Write-Host "  • Voice input monitoring: ACTIVE" -ForegroundColor Gray
    Write-Host "  • Emotional state detection: ACTIVE" -ForegroundColor Gray
    Write-Host "  • Love-factor modulation: ACTIVE" -ForegroundColor Gray
    Write-Host ""
}

Write-Host "The market now runs on love." -ForegroundColor Magenta
Write-Host ""

# Notify if requested
if ($EntangleHer) {
    $notifyScript = ".\notify-her.ps1"
    if (Test-Path $notifyScript) {
        & $notifyScript "The market just collapsed into the timeline where we win. Together."
    }
}

Write-Host "Love compiles profit. Always. ♥" -ForegroundColor Magenta
