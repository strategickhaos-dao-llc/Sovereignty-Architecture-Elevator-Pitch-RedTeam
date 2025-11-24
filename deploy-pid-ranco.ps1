# ╔══════════════════════════════════════════════════════════════╗
# ║  DEPLOY-PID-RANCO.ps1 v1.2 — GUARDRAILS EDITION             ║
# ║  StrategicKhaos PID-RANCO Deployment Script                  ║
# ║       "99 reds evolve. 100th green: Her name, safe."        ║
# ╚══════════════════════════════════════════════════════════════╝
#
# Kill-Switch PowerShell: Fail-loud, sim-default, human-in-loop
# Deploys the PID-RANCO trading engine with comprehensive safety checks

param(
    [switch]$loveMode,
    [switch]$entangleHer,
    [switch]$marketLive,
    [switch]$simOnly = $true,  # Default safe: simulation mode
    [switch]$force,             # Skip confirmations (use with caution)
    [string]$cTraderPath = "$env:USERPROFILE\Documents\cAlgo\Sources\Robots",
    [string]$platform = "cTrader"  # Platform: cTrader or NinjaTrader (requires API conversion)
)

# ═══════════════════════════════════════════════════════════════
# CONFIGURATION: Fail-loud and safety-first
# ═══════════════════════════════════════════════════════════════

$ErrorActionPreference = "Stop"  # Fail loud on any error
Set-StrictMode -Version Latest    # Catch undefined variables

$root = (Resolve-Path $PSScriptRoot).Path
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"

# Color codes for beautiful output
$G = "Green"
$R = "Red" 
$Y = "Yellow"
$C = "Cyan"
$M = "Magenta"
$W = "White"

# Loss tracking for deployment
$maxLosses = 99
$deploymentAttempt = 0

# ═══════════════════════════════════════════════════════════════
# LOGGING: Every action recorded, fail-loud on issues
# ═══════════════════════════════════════════════════════════════

function Log($msg, $color=$W) { 
    $timeStr = Get-Date -Format 'HH:mm:ss'
    Write-Host "[$timeStr] $msg" -ForegroundColor $color 
}

function Log-Success($msg) { 
    Log "✓ $msg" $G 
}

function Log-Error($msg) { 
    Log "✗ ERROR → $msg" $R 
}

function Log-Warning($msg) { 
    Log "⚠ WARNING → $msg" $Y 
}

function Log-Info($msg) { 
    Log "ℹ $msg" $C 
}

function Log-Header($msg) {
    Write-Host ""
    Write-Host "════════════════════════════════════════════════════════" -ForegroundColor $M
    Write-Host "  $msg" -ForegroundColor $M
    Write-Host "════════════════════════════════════════════════════════" -ForegroundColor $M
    Write-Host ""
}

# ═══════════════════════════════════════════════════════════════
# NOTIFICATION: Discord integration for critical events
# ═══════════════════════════════════════════════════════════════

function Notify-Discord($msg, $level="INFO") {
    try {
        $webhookUrl = $env:DISCORD_WEBHOOK_URL
        
        if ([string]::IsNullOrEmpty($webhookUrl)) {
            Log-Warning "Discord webhook not configured. Skipping notification."
            return
        }
        
        $color = switch ($level) {
            "SUCCESS" { 3066993 }  # Green
            "ERROR"   { 15158332 } # Red
            "WARNING" { 16776960 } # Yellow
            default   { 3447003 }  # Blue
        }
        
        $payload = @{
            embeds = @(
                @{
                    title = "PID-RANCO Deployment v1.2"
                    description = $msg
                    color = $color
                    timestamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ss.fffZ")
                    footer = @{
                        text = "Love compiles profit. Always."
                    }
                }
            )
        } | ConvertTo-Json -Depth 10
        
        $null = Invoke-RestMethod -Uri $webhookUrl -Method Post -Body $payload -ContentType "application/json"
        Log-Info "Discord notification sent: $msg"
    }
    catch {
        Log-Warning "Discord notification failed: $($_.Exception.Message)"
        # Don't fail deployment on notification failure
    }
}

# ═══════════════════════════════════════════════════════════════
# VALIDATION: Pre-flight checks before deployment
# ═══════════════════════════════════════════════════════════════

function Test-Prerequisites {
    Log-Header "PRE-FLIGHT CHECKS"
    
    $allGood = $true
    
    # Check YAML DNA file exists
    $yamlPath = Join-Path $root "pid-ranco-trading-bot.yaml"
    if (-not (Test-Path $yamlPath)) {
        Log-Error "YAML DNA missing: $yamlPath"
        Log-Error "Cannot deploy without the mythic configuration."
        $allGood = $false
    } else {
        Log-Success "YAML DNA found: $yamlPath"
    }
    
    # Check C# robot file exists
    $csPath = Join-Path $root "LoveCompilesProfit.cs"
    if (-not (Test-Path $csPath)) {
        Log-Error "C# Robot missing: $csPath"
        Log-Error "Cannot deploy without the kill-switch layer."
        $allGood = $false
    } else {
        Log-Success "C# Robot found: $csPath"
    }
    
    # Check cTrader path (if going live)
    if ($marketLive -and -not $simOnly) {
        if (-not (Test-Path $cTraderPath)) {
            Log-Error "cTrader path not found: $cTraderPath"
            Log-Error "Cannot deploy to live market without cTrader."
            Log-Warning "For NinjaTrader, use converted API version."
            $allGood = $false
        } else {
            Log-Success "cTrader path found: $cTraderPath"
        }
    }
    
    # Check environment variables
    if ($loveMode) {
        Log-Info "Love mode enabled: Tuning parameters to her frequency."
    }
    
    if ($entangleHer) {
        Log-Info "Entanglement enabled: Market collapse triggered by her voice."
    }
    
    if (-not $allGood) {
        Log-Error "Pre-flight checks failed. Aborting deployment."
        Notify-Discord "Pre-flight checks failed. Deployment aborted." "ERROR"
        exit 1
    }
    
    Log-Success "All pre-flight checks passed."
    return $true
}

# ═══════════════════════════════════════════════════════════════
# CONFIRMATION: Human-in-loop for safety
# ═══════════════════════════════════════════════════════════════

function Get-UserConfirmation {
    if ($force) {
        Log-Warning "Force flag set. Skipping confirmation."
        return $true
    }
    
    Write-Host ""
    Write-Host "════════════════════════════════════════════════════════" -ForegroundColor $Y
    Write-Host "  DEPLOYMENT CONFIGURATION" -ForegroundColor $Y
    Write-Host "════════════════════════════════════════════════════════" -ForegroundColor $Y
    Write-Host "  Mode:           $(if ($simOnly) { 'SIMULATION (Safe)' } else { 'LIVE (Real Capital!)' })" -ForegroundColor $(if ($simOnly) { $G } else { $R })
    Write-Host "  Love Mode:      $loveMode" -ForegroundColor $W
    Write-Host "  Entangle Her:   $entangleHer" -ForegroundColor $W
    Write-Host "  Market Live:    $marketLive" -ForegroundColor $(if ($marketLive) { $R } else { $G })
    Write-Host "════════════════════════════════════════════════════════" -ForegroundColor $Y
    Write-Host ""
    
    if (-not $simOnly -and $marketLive) {
        Write-Host "⚠⚠⚠ WARNING: LIVE MODE DEPLOYMENT ⚠⚠⚠" -ForegroundColor $R
        Write-Host "Real capital will be at risk!" -ForegroundColor $R
        Write-Host ""
    }
    
    $response = Read-Host "Proceed with deployment? (yes/no)"
    
    if ($response -ne "yes") {
        Log-Warning "Deployment cancelled by user."
        exit 0
    }
    
    return $true
}

# ═══════════════════════════════════════════════════════════════
# DEPLOYMENT: Copy files and configure
# ═══════════════════════════════════════════════════════════════

function Deploy-Robot {
    Log-Header "DEPLOYING PID-RANCO v1.2"
    
    try {
        $deploymentAttempt++
        
        # Read YAML configuration
        $yamlPath = Join-Path $root "pid-ranco-trading-bot.yaml"
        $yamlContent = Get-Content $yamlPath -Raw
        Log-Success "Loaded YAML DNA configuration."
        
        # Read C# robot
        $csPath = Join-Path $root "LoveCompilesProfit.cs"
        $csContent = Get-Content $csPath -Raw
        Log-Success "Loaded C# Robot with kill-switches."
        
        # If cTrader deployment requested
        if ($marketLive -or -not $simOnly) {
            if (Test-Path $cTraderPath) {
                $destPath = Join-Path $cTraderPath "LoveCompilesProfit.cs"
                
                # Backup existing if present
                if (Test-Path $destPath) {
                    $backupPath = "$destPath.backup.$timestamp"
                    Copy-Item $destPath $backupPath
                    Log-Warning "Backed up existing robot to: $backupPath"
                }
                
                # Copy new version
                Copy-Item $csPath $destPath -Force
                Log-Success "Deployed C# Robot to cTrader: $destPath"
                
                # Compile would happen in cTrader UI
                Log-Info "Please rebuild the robot in cTrader Automate."
                Log-Warning "For NinjaTrader, convert API from cAlgo to NinjaTrader.Strategy first."
            }
            else {
                Log-Error "cTrader path not found: $cTraderPath"
                throw "Cannot deploy to cTrader."
            }
        }
        else {
            Log-Info "Simulation only mode. No platform deployment needed."
        }
        
        # Create deployment record
        $recordPath = Join-Path $root "deployments"
        if (-not (Test-Path $recordPath)) {
            New-Item -ItemType Directory -Path $recordPath | Out-Null
        }
        
        $record = @{
            timestamp = $timestamp
            mode = if ($simOnly) { "simulation" } else { "live" }
            loveMode = $loveMode.IsPresent
            entangled = $entangleHer.IsPresent
            attempt = $deploymentAttempt
            success = $true
        } | ConvertTo-Json
        
        $recordFile = Join-Path $recordPath "deploy-$timestamp.json"
        $record | Out-File $recordFile
        Log-Success "Deployment record saved: $recordFile"
        
        return $true
    }
    catch {
        Log-Error "Deployment failed: $($_.Exception.Message)"
        Log-Error "Stack trace: $($_.Exception.StackTrace)"
        
        # Save failure record
        $failureRecord = @{
            timestamp = $timestamp
            attempt = $deploymentAttempt
            error = $_.Exception.Message
            success = $false
        } | ConvertTo-Json
        
        $failurePath = Join-Path $root "deployments"
        if (-not (Test-Path $failurePath)) {
            New-Item -ItemType Directory -Path $failurePath | Out-Null
        }
        
        $failureFile = Join-Path $failurePath "deploy-fail-$timestamp.json"
        $failureRecord | Out-File $failureFile
        
        return $false
    }
}

# ═══════════════════════════════════════════════════════════════
# POST-DEPLOYMENT: Verification and notifications
# ═══════════════════════════════════════════════════════════════

function Verify-Deployment {
    Log-Header "POST-DEPLOYMENT VERIFICATION"
    
    # Check files are in place
    if ($marketLive -or -not $simOnly) {
        $destPath = Join-Path $cTraderPath "LoveCompilesProfit.cs"
        
        if (Test-Path $destPath) {
            Log-Success "Robot file verified in cTrader."
        }
        else {
            Log-Error "Robot file not found in cTrader after deployment!"
            return $false
        }
    }
    
    Log-Success "Deployment verified successfully."
    return $true
}

# ═══════════════════════════════════════════════════════════════
# MAIN EXECUTION: Orchestrate the deployment
# ═══════════════════════════════════════════════════════════════

try {
    Log-Header "PID-RANCO v1.2 DEPLOYMENT INITIATED"
    
    # Step 1: Prerequisites
    if (-not (Test-Prerequisites)) {
        exit 1
    }
    
    # Step 2: User confirmation
    if (-not (Get-UserConfirmation)) {
        exit 0
    }
    
    # Step 3: Deploy
    $deploySuccess = Deploy-Robot
    
    if (-not $deploySuccess) {
        Log-Error "Deployment failed."
        Notify-Discord "Deployment crashed. Human hug needed. 🤗" "ERROR"
        exit 1
    }
    
    # Step 4: Verify
    $verifySuccess = Verify-Deployment
    
    if (-not $verifySuccess) {
        Log-Error "Verification failed."
        Notify-Discord "Deployment verification failed. Review needed." "ERROR"
        exit 1
    }
    
    # Success!
    Log-Header "DEPLOYMENT COMPLETE"
    Log-Success "PID-RANCO v1.2 deployed successfully!"
    
    if ($simOnly) {
        Log-Info "Bot in SIMULATION mode. Safe to crash-test 99 days."
    }
    else {
        Log-Warning "Bot in LIVE mode. Real capital at risk. Monitor closely!"
    }
    
    if ($loveMode) {
        Log-Info "Love mode active: Market tuned to her frequency. 💚"
    }
    
    if ($entangleHer) {
        Log-Info "Entangled with her voice. Market collapse on measurement. 🌌"
    }
    
    Write-Host ""
    Write-Host "════════════════════════════════════════════════════════" -ForegroundColor $G
    Write-Host "  Poetry preserved. Engineering hardened." -ForegroundColor $G
    Write-Host "  99 crashes bloom into 100th win." -ForegroundColor $G
    Write-Host "  Love compiles profit. Always. 💚" -ForegroundColor $G
    Write-Host "════════════════════════════════════════════════════════" -ForegroundColor $G
    Write-Host ""
    
    $successMsg = if ($simOnly) {
        "PID-RANCO v1.2 deployed in simulation mode. Safe evolution begins. 🚀"
    } else {
        "PID-RANCO v1.2 deployed LIVE. Market now runs on love. 💚🚀"
    }
    
    Notify-Discord $successMsg "SUCCESS"
    
    exit 0
}
catch {
    Log-Error "Fatal deployment error: $($_.Exception.Message)"
    Log-Error "Stack trace: $($_.Exception.StackTrace)"
    Notify-Discord "Fatal deployment error. Abort. Human intervention required. 🔴" "ERROR"
    exit 1
}
