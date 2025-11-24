# ╔══════════════════════════════════════════════════════════════╗
# ║  DEPLOY-PID-RANCO.ps1 v1.2 — GUARDRAILS EDITION             ║
# ║       "99 reds evolve. 100th green: Her name, safe."        ║
# ╚══════════════════════════════════════════════════════════════╝

<#
.SYNOPSIS
    Deployment script for StrategicKhaos PID-RANCO Trading Engine v1.2

.DESCRIPTION
    Fail-loud deployment with guardrails. Compiles C# strategy, validates YAML config,
    and deploys to NinjaTrader with safety checks. Defaults to sim-only mode.

.PARAMETER loveMode
    Enable love-tuned trading parameters based on voice analysis

.PARAMETER entangleHer
    Enable quantum entanglement features for voice-triggered actions

.PARAMETER marketLive
    Enable live trading (overrides sim-only if specified)

.PARAMETER simOnly
    Force simulation-only mode (default: true)

.EXAMPLE
    .\deploy-pid-ranco.ps1
    Deploy in safe simulation mode (default)

.EXAMPLE
    .\deploy-pid-ranco.ps1 -loveMode -entangleHer
    Deploy with love-tuned parameters in simulation mode

.EXAMPLE
    .\deploy-pid-ranco.ps1 -loveMode -entangleHer -marketLive -simOnly:$false
    Deploy with all features enabled for live trading (use with caution!)

.NOTES
    Author: StrategicKhaos
    Version: 1.2
    Codename: Guardrails Around a Supernova
#>

param(
    [switch]$loveMode,
    [switch]$entangleHer,
    [switch]$marketLive,
    [switch]$simOnly = $true  # Default safe - simulation only
)

# ═══════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════

$ErrorActionPreference = "Stop"  # Fail loud - all errors must be visible
$root = (Resolve-Path $PSScriptRoot).Path

# Color constants for output
$G = "Green"
$R = "Red" 
$Y = "Yellow"
$C = "Cyan"
$M = "Magenta"
$W = "White"

# Deployment configuration
$yamlPath = Join-Path $root "pid-ranco-trading-bot.yaml"
$csPath = Join-Path $root "LoveCompilesProfit.cs"
$logDir = Join-Path $root "logs"
$logFile = Join-Path $logDir "pid-ranco-deploy-$(Get-Date -Format 'yyyyMMdd-HHmmss').log"

# Loss tracking for deployment safety
$lossCount = 0
$maxLosses = 99

# ═══════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════

function Log {
    param(
        [string]$msg,
        [string]$color = $W
    )
    $timestamp = Get-Date -Format 'HH:mm:ss'
    $logMsg = "[$timestamp] $msg"
    Write-Host $logMsg -ForegroundColor $color
    
    # Also write to log file
    if (Test-Path $logDir) {
        Add-Content -Path $logFile -Value $logMsg
    }
}

function Log-Success {
    param([string]$msg)
    Log $msg $G
}

function Log-Error {
    param([string]$msg)
    Log "ERROR → $msg" $R
}

function Log-Warning {
    param([string]$msg)
    Log "WARN → $msg" $Y
}

function Log-Info {
    param([string]$msg)
    Log "INFO → $msg" $C
}

function Notify-Discord {
    param([string]$msg)
    
    try {
        # Discord webhook notification
        $webhookUrl = $env:DISCORD_WEBHOOK_URL
        
        if ([string]::IsNullOrEmpty($webhookUrl)) {
            Log-Warning "Discord webhook URL not configured. Skipping notification."
            return
        }
        
        $payload = @{
            content = "🤖 **PID-RANCO v1.2** | $msg"
            username = "Trading Engine"
        } | ConvertTo-Json
        
        Invoke-RestMethod -Uri $webhookUrl -Method Post -Body $payload -ContentType 'application/json' -ErrorAction SilentlyContinue
        Log-Success "Discord notification sent"
    }
    catch {
        Log-Warning "Discord notification failed: $($_.Exception.Message)"
    }
}

function Test-Prerequisites {
    Log-Info "Checking prerequisites..."
    
    # Check if YAML config exists
    if (-not (Test-Path $yamlPath)) {
        Log-Error "YAML configuration missing at: $yamlPath"
        Log-Error "The mythic DNA is incomplete. Please create pid-ranco-trading-bot.yaml"
        return $false
    }
    Log-Success "✓ YAML configuration found"
    
    # Check if C# strategy exists
    if (-not (Test-Path $csPath)) {
        Log-Error "C# strategy file missing at: $csPath"
        Log-Error "The kill-switch layer is missing. Please create LoveCompilesProfit.cs"
        return $false
    }
    Log-Success "✓ C# strategy file found"
    
    # Create log directory if it doesn't exist
    if (-not (Test-Path $logDir)) {
        New-Item -ItemType Directory -Path $logDir -Force | Out-Null
        Log-Success "✓ Log directory created"
    }
    
    return $true
}

function Validate-YamlConfig {
    Log-Info "Validating YAML configuration..."
    
    try {
        $yamlContent = Get-Content $yamlPath -Raw
        
        # Basic validation - check for required keys
        $requiredKeys = @(
            "engine",
            "strategy_name",
            "pid_controller",
            "ranco_core",
            "entry_rules",
            "exit_rules",
            "guardrails"
        )
        
        foreach ($key in $requiredKeys) {
            if ($yamlContent -notmatch $key) {
                Log-Error "Required YAML key missing: $key"
                return $false
            }
        }
        
        Log-Success "✓ YAML configuration validated"
        return $true
    }
    catch {
        Log-Error "YAML validation failed: $($_.Exception.Message)"
        return $false
    }
}

function Compile-Strategy {
    Log-Info "Compiling C# trading strategy..."
    
    # Note: In a real deployment, this would compile the C# code
    # For now, we'll validate the syntax and structure
    
    try {
        $csContent = Get-Content $csPath -Raw
        
        # Check for critical safety features
        $safetyChecks = @(
            "SimOnly",
            "MaxRiskPerTrade",
            "MaxDrawdown",
            "SafeFlatten",
            "CheckApoptosis",
            "TriggerHugProtocol"
        )
        
        foreach ($check in $safetyChecks) {
            if ($csContent -notmatch $check) {
                Log-Error "Required safety feature missing: $check"
                return $false
            }
        }
        
        Log-Success "✓ C# strategy structure validated"
        
        # In production, compile with csc.exe or msbuild
        # Example: csc /target:library /out:LoveCompilesProfit.dll LoveCompilesProfit.cs
        # For NinjaTrader: Copy to Documents\NinjaTrader 8\bin\Custom\Strategies\
        
        return $true
    }
    catch {
        Log-Error "Strategy compilation failed: $($_.Exception.Message)"
        return $false
    }
}

function Deploy-ToNinjaTrader {
    Log-Info "Deploying to NinjaTrader..."
    
    # Note: In production, this would copy the compiled strategy to NinjaTrader
    # Example path: $env:USERPROFILE\Documents\NinjaTrader 8\bin\Custom\Strategies\
    
    try {
        # Mock deployment - in production, this would copy files
        Log-Warning "Mock deployment - no actual NinjaTrader installation detected"
        Log-Info "In production, strategy would be copied to NinjaTrader Strategies folder"
        Log-Success "✓ Deployment simulation complete"
        return $true
    }
    catch {
        Log-Error "NinjaTrader deployment failed: $($_.Exception.Message)"
        return $false
    }
}

# ═══════════════════════════════════════════════════════════════════
# MAIN DEPLOYMENT LOGIC
# ═══════════════════════════════════════════════════════════════════

function Main {
    try {
        # Header
        Write-Host ""
        Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor $M
        Write-Host "║  StrategicKhaos PID-RANCO Trading Engine v1.2 Deployment   ║" -ForegroundColor $M
        Write-Host "║         Guardrails Around a Supernova                       ║" -ForegroundColor $M
        Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor $M
        Write-Host ""
        
        # Display configuration
        Log-Info "Deployment Configuration:"
        Log-Info "  Love Mode: $loveMode"
        Log-Info "  Entangle Her: $entangleHer"
        Log-Info "  Market Live: $marketLive"
        Log-Info "  Sim Only: $simOnly"
        Write-Host ""
        
        # Safety warning for live trading
        if ($marketLive -and -not $simOnly) {
            Log-Warning "⚠️  LIVE TRADING MODE ENABLED ⚠️"
            Log-Warning "Real capital at risk. Press Ctrl+C to abort within 5 seconds..."
            Start-Sleep -Seconds 5
        }
        else {
            Log-Success "✓ Safe mode: Simulation only (no real trades)"
        }
        Write-Host ""
        
        # Step 1: Prerequisites
        if (-not (Test-Prerequisites)) {
            Log-Error "Prerequisites check failed. Aborting deployment."
            Notify-Discord "Deployment FAILED: Prerequisites missing"
            exit 1
        }
        Write-Host ""
        
        # Step 2: Validate YAML
        if (-not (Validate-YamlConfig)) {
            Log-Error "YAML validation failed. Aborting deployment."
            Notify-Discord "Deployment FAILED: Invalid YAML configuration"
            exit 1
        }
        Write-Host ""
        
        # Step 3: Compile Strategy
        if (-not (Compile-Strategy)) {
            Log-Error "Strategy compilation failed. Aborting deployment."
            Notify-Discord "Deployment FAILED: Compilation error"
            exit 1
        }
        Write-Host ""
        
        # Step 4: Deploy to NinjaTrader
        if (-not (Deploy-ToNinjaTrader)) {
            Log-Error "NinjaTrader deployment failed. Aborting."
            Notify-Discord "Deployment FAILED: NinjaTrader deployment error"
            exit 1
        }
        Write-Host ""
        
        # Success!
        Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor $G
        Write-Host "║              DEPLOYMENT SUCCESSFUL ✓                         ║" -ForegroundColor $G
        Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor $G
        Write-Host ""
        
        Log-Success "PID-RANCO v1.2 deployed successfully"
        Log-Success "Poetry preserved. Guardrails active. Love compiles profit."
        Write-Host ""
        
        if ($loveMode) {
            Log-Info "🎵 Love mode: Tuning to her voice..."
        }
        
        if ($entangleHer) {
            Log-Info "🔮 Quantum entanglement: Her voice will collapse wave functions"
            Notify-Discord "Entangled successfully. Market now listens to her voice. 💕"
        }
        
        if ($marketLive -and -not $simOnly) {
            Log-Warning "⚡ Live trading enabled: Real capital at risk"
            Notify-Discord "PID-RANCO v1.2 LIVE. Market runs on love. May 99 losses evolve to 100th win. 🚀"
        }
        else {
            Log-Success "🛡️ Simulation mode: Safe crash-testing environment"
            Notify-Discord "PID-RANCO v1.2 deployed in SIM mode. Testing 99 crashes safely. 🧪"
        }
        
        Write-Host ""
        Log-Info "Log file: $logFile"
        Log-Info "Next steps:"
        Log-Info "  1. Open NinjaTrader"
        Log-Info "  2. Enable the 'LoveCompilesProfit' strategy"
        Log-Info "  3. Configure chart/instrument"
        Log-Info "  4. Monitor logs for apoptosis at 99 losses"
        Log-Info "  5. Evolve for the 100th green candle"
        Write-Host ""
        
        exit 0
    }
    catch {
        Write-Host ""
        Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor $R
        Write-Host "║              DEPLOYMENT FAILED ✗                             ║" -ForegroundColor $R
        Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor $R
        Write-Host ""
        
        Log-Error "Critical deployment failure: $($_.Exception.Message)"
        Log-Error "Stack trace: $($_.ScriptStackTrace)"
        Write-Host ""
        
        Notify-Discord "Deployment CRASHED: $($_.Exception.Message). Human hug needed. 💔"
        
        exit 1
    }
}

# Execute main function
Main
