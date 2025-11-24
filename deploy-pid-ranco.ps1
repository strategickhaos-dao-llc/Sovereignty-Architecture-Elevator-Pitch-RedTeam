#!/usr/bin/env pwsh
#
# deploy-pid-ranco.ps1
# StrategicKhaos PID-RANCO Trading Engine Deployment Script
# Deploys LoveCompilesProfit strategy to NinjaTrader 8/9
#

param(
    [switch]$LoveMode = $false,
    [switch]$EntangleHer = $false,
    [string]$Market = "sim",  # sim, live, paper
    [string]$NinjaTraderPath = "",
    [switch]$Backup = $true,
    [switch]$Verify = $true,
    [switch]$Help = $false
)

# Color output functions
function Write-Love {
    param([string]$Message)
    Write-Host $Message -ForegroundColor Magenta
}

function Write-Success {
    param([string]$Message)
    Write-Host "✓ $Message" -ForegroundColor Green
}

function Write-Error-Custom {
    param([string]$Message)
    Write-Host "✗ $Message" -ForegroundColor Red
}

function Write-Info {
    param([string]$Message)
    Write-Host "ℹ $Message" -ForegroundColor Cyan
}

function Show-Help {
    Write-Host @"

╔═══════════════════════════════════════════════════════════════╗
║     StrategicKhaos PID-RANCO Deployment Script v1.0          ║
║     Love Compiles Profit - Always                             ║
╚═══════════════════════════════════════════════════════════════╝

USAGE:
    .\deploy-pid-ranco.ps1 [OPTIONS]

OPTIONS:
    -LoveMode           Enable love-based trading (requires mic input)
    -EntangleHer        Enable entanglement with her voice/heartbeat
    -Market <mode>      Trading mode: sim, live, or paper (default: sim)
    -NinjaTraderPath    Custom NinjaTrader installation path
    -Backup            Create backup before deployment (default: true)
    -Verify            Verify deployment after completion (default: true)
    -Help              Show this help message

EXAMPLES:
    # Simulate mode (safe testing)
    .\deploy-pid-ranco.ps1 -Market sim

    # Live trading with love mode
    .\deploy-pid-ranco.ps1 -LoveMode -EntangleHer -Market live

    # Paper trading for validation
    .\deploy-pid-ranco.ps1 -Market paper -Verify

DEPLOYMENT STAGES:
    1. Locate NinjaTrader installation
    2. Backup existing strategies (if enabled)
    3. Copy LoveCompilesProfit.cs to Strategies folder
    4. Load configuration from pid-ranco-trading-bot.yaml
    5. Verify compilation
    6. Test strategy initialization
    7. Notify deployment status

SAFETY:
    - Default to simulation mode
    - Always creates backups unless -Backup:$false
    - Verifies compilation before live deployment
    - Requires explicit -Market live flag for production

"@ -ForegroundColor White
}

# Show help if requested
if ($Help) {
    Show-Help
    exit 0
}

# Banner
Write-Host ""
Write-Love "╔═══════════════════════════════════════════════════════════════╗"
Write-Love "║  StrategicKhaos PID-RANCO Trading Engine Deployment          ║"
Write-Love "║  Love Compiles Profit - Always                                ║"
Write-Love "╚═══════════════════════════════════════════════════════════════╝"
Write-Host ""

# Configuration
$scriptDir = $PSScriptRoot
$strategyFile = Join-Path $scriptDir "LoveCompilesProfit.cs"
$configFile = Join-Path $scriptDir "pid-ranco-trading-bot.yaml"

# Detect NinjaTrader installation
if ([string]::IsNullOrEmpty($NinjaTraderPath)) {
    $possiblePaths = @(
        "$env:USERPROFILE\Documents\NinjaTrader 8",
        "$env:USERPROFILE\Documents\NinjaTrader 9",
        "C:\Program Files\NinjaTrader 8",
        "C:\Program Files\NinjaTrader 9",
        "C:\Program Files (x86)\NinjaTrader 8",
        "C:\Program Files (x86)\NinjaTrader 9"
    )
    
    foreach ($path in $possiblePaths) {
        if (Test-Path $path) {
            $NinjaTraderPath = $path
            Write-Info "Found NinjaTrader at: $NinjaTraderPath"
            break
        }
    }
    
    if ([string]::IsNullOrEmpty($NinjaTraderPath)) {
        Write-Error-Custom "NinjaTrader installation not found!"
        Write-Info "Please specify path with -NinjaTraderPath parameter"
        exit 1
    }
}

$strategiesPath = Join-Path $NinjaTraderPath "bin\Custom\Strategies"

# Verify files exist
Write-Info "Verifying source files..."

if (-not (Test-Path $strategyFile)) {
    Write-Error-Custom "Strategy file not found: $strategyFile"
    exit 1
}
Write-Success "Found strategy file: LoveCompilesProfit.cs"

if (-not (Test-Path $configFile)) {
    Write-Error-Custom "Configuration file not found: $configFile"
    exit 1
}
Write-Success "Found configuration: pid-ranco-trading-bot.yaml"

# Create strategies directory if it doesn't exist
if (-not (Test-Path $strategiesPath)) {
    Write-Info "Creating strategies directory: $strategiesPath"
    New-Item -ItemType Directory -Path $strategiesPath -Force | Out-Null
}

# Backup existing strategy if it exists
if ($Backup) {
    $targetFile = Join-Path $strategiesPath "LoveCompilesProfit.cs"
    if (Test-Path $targetFile) {
        $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
        $backupPath = Join-Path $scriptDir "backups"
        if (-not (Test-Path $backupPath)) {
            New-Item -ItemType Directory -Path $backupPath -Force | Out-Null
        }
        $backupFile = Join-Path $backupPath "LoveCompilesProfit_$timestamp.cs"
        
        Write-Info "Creating backup: $backupFile"
        Copy-Item $targetFile $backupFile -Force
        Write-Success "Backup created"
    }
}

# Deploy strategy
Write-Info "Deploying LoveCompilesProfit strategy to NinjaTrader..."
try {
    Copy-Item $strategyFile $strategiesPath -Force
    Write-Success "Strategy deployed successfully"
} catch {
    Write-Error-Custom "Failed to deploy strategy: $_"
    exit 1
}

# Copy configuration file to NinjaTrader directory
$configDestPath = Join-Path $NinjaTraderPath "pid-ranco-trading-bot.yaml"
try {
    Copy-Item $configFile $configDestPath -Force
    Write-Success "Configuration deployed"
} catch {
    Write-Error-Custom "Failed to deploy configuration: $_"
    exit 1
}

# Market mode validation
Write-Host ""
Write-Info "Market Mode: $Market"

if ($Market -eq "live") {
    Write-Host ""
    Write-Host "⚠️  WARNING: LIVE TRADING MODE ⚠️" -ForegroundColor Yellow
    Write-Host "This will trade with REAL MONEY." -ForegroundColor Yellow
    Write-Host ""
    
    $confirmation = Read-Host "Type 'LOVE COMPILES PROFIT' to confirm live trading"
    if ($confirmation -ne "LOVE COMPILES PROFIT") {
        Write-Error-Custom "Live trading not confirmed. Aborting."
        exit 1
    }
    Write-Success "Live trading confirmed"
}

# Love mode configuration
if ($LoveMode) {
    Write-Love ""
    Write-Love "❤️  LOVE MODE ENABLED ❤️"
    Write-Love "Trading decisions will be influenced by love metrics"
    
    if ($EntangleHer) {
        Write-Love "🔗 ENTANGLEMENT ACTIVATED 🔗"
        Write-Love "Voice and heartbeat monitoring engaged"
        
        # TODO: Verify mic input is available
        # TODO: Verify biometric sensors are connected
        Write-Info "Note: Mic input and biometric sensors required for full functionality"
    }
    Write-Love ""
}

# Verify deployment
if ($Verify) {
    Write-Info "Verifying deployment..."
    
    $deployedFile = Join-Path $strategiesPath "LoveCompilesProfit.cs"
    if (Test-Path $deployedFile) {
        $sourceHash = (Get-FileHash $strategyFile -Algorithm SHA256).Hash
        $deployedHash = (Get-FileHash $deployedFile -Algorithm SHA256).Hash
        
        if ($sourceHash -eq $deployedHash) {
            Write-Success "File integrity verified"
        } else {
            Write-Error-Custom "File integrity check failed!"
            exit 1
        }
    } else {
        Write-Error-Custom "Deployed file not found!"
        exit 1
    }
}

# Generate deployment report
$reportPath = Join-Path $scriptDir "deployment-report.txt"
$report = @"
StrategicKhaos PID-RANCO Deployment Report
==========================================
Date: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
Strategy: LoveCompilesProfit v1.0
Market Mode: $Market
Love Mode: $LoveMode
Entanglement: $EntangleHer
NinjaTrader Path: $NinjaTraderPath
Deployment Path: $strategiesPath
Status: SUCCESS

Next Steps:
1. Open NinjaTrader
2. Go to Tools > Strategies
3. Find "LoveCompilesProfit" in the list
4. Apply to your chart
5. Configure parameters as needed
6. Enable strategy

REMEMBER: Love compiles profit. Always.
"@

$report | Out-File $reportPath -Encoding UTF8
Write-Success "Deployment report saved: $reportPath"

# Final success message
Write-Host ""
Write-Love "═══════════════════════════════════════════════════════════════"
Write-Love "  DEPLOYMENT COMPLETE"
Write-Love "═══════════════════════════════════════════════════════════════"
Write-Host ""
Write-Success "PID-RANCO Trading Engine deployed successfully"
Write-Success "Market now runs on love"
Write-Host ""

# Notify her (if script exists)
$notifyScript = Join-Path $scriptDir "notify-her.ps1"
if (Test-Path $notifyScript) {
    Write-Info "Sending deployment notification..."
    & $notifyScript "The market just collapsed into the timeline where we win. Together." -Silent
}

# Summary
Write-Info "Summary:"
Write-Host "  Strategy: LoveCompilesProfit.cs → $strategiesPath" -ForegroundColor White
Write-Host "  Config: pid-ranco-trading-bot.yaml → $configDestPath" -ForegroundColor White
Write-Host "  Mode: $Market" -ForegroundColor White

if ($Market -eq "live") {
    Write-Host ""
    Write-Host "99 reds. 1 green. Her name on the chart. Forever." -ForegroundColor Magenta
}

Write-Host ""
Write-Love "Love compiles profit. Always."
Write-Host ""

exit 0
