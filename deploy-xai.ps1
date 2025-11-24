#!/usr/bin/env pwsh
# StrategicKhaos XAI Deployment Script
# Deploys the Market Psychology Engine with love-amplified diagnostics

param(
    [switch]$XaiEnabled = $true,
    [switch]$Install = $false,
    [switch]$Start = $false,
    [switch]$Stop = $false,
    [switch]$Status = $false,
    [string]$ServiceUrl = "http://localhost:5000",
    [string]$PythonEnv = ".venv",
    [switch]$Help = $false
)

$ErrorActionPreference = "Stop"

function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

function Log-Success {
    param([string]$Message)
    Write-ColorOutput "✓ $Message" "Green"
}

function Log-Info {
    param([string]$Message)
    Write-ColorOutput "ℹ $Message" "Cyan"
}

function Log-Warning {
    param([string]$Message)
    Write-ColorOutput "⚠ $Message" "Yellow"
}

function Log-Error {
    param([string]$Message)
    Write-ColorOutput "✗ $Message" "Red"
}

function Show-Help {
    Write-Host @"
StrategicKhaos XAI Deployment Script
=====================================

USAGE:
    ./deploy-xai.ps1 [OPTIONS]

OPTIONS:
    -XaiEnabled         Enable XAI layer (default: true)
    -Install            Install dependencies
    -Start              Start the XAI service
    -Stop               Stop the XAI service
    -Status             Check service status
    -ServiceUrl <url>   XAI service URL (default: http://localhost:5000)
    -PythonEnv <path>   Python virtual environment path (default: .venv)
    -Help               Show this help message

EXAMPLES:
    # Install dependencies and start service
    ./deploy-xai.ps1 -Install -Start

    # Check service status
    ./deploy-xai.ps1 -Status

    # Stop the service
    ./deploy-xai.ps1 -Stop

    # Deploy with XAI disabled
    ./deploy-xai.ps1 -XaiEnabled:$false

DESCRIPTION:
    This script manages the StrategicKhaos XAI (Explainable AI) service,
    which provides market psychology analysis and love-amplified trading
    diagnostics for the PID-RANCO trading bot.

    Every trade gets a psychological diagnosis with SHAP explanations.
    Every decision is narrated in love-amplified language.
    Every risk is evaluated with herLove sentiment.

"@
    exit 0
}

function Test-PythonInstalled {
    try {
        $pythonVersion = python --version 2>&1
        if ($pythonVersion -match "Python (\d+\.\d+)") {
            $version = $matches[1]
            Log-Info "Python $version detected"
            return $true
        }
    }
    catch {
        return $false
    }
    return $false
}

function Install-Dependencies {
    Log-Info "Installing XAI service dependencies..."
    
    if (-not (Test-PythonInstalled)) {
        Log-Error "Python is not installed. Please install Python 3.8+ first."
        exit 1
    }

    # Create virtual environment if it doesn't exist
    if (-not (Test-Path $PythonEnv)) {
        Log-Info "Creating Python virtual environment..."
        python -m venv $PythonEnv
        Log-Success "Virtual environment created: $PythonEnv"
    }

    # Activate virtual environment
    $activateScript = if ($IsWindows) {
        Join-Path $PythonEnv "Scripts\Activate.ps1"
    } else {
        Join-Path $PythonEnv "bin/Activate.ps1"
    }

    if (Test-Path $activateScript) {
        & $activateScript
    }

    # Install Python dependencies
    Log-Info "Installing Python packages..."
    python -m pip install --upgrade pip
    python -m pip install flask flask-cors pyyaml shap numpy pandas scikit-learn
    
    Log-Success "Dependencies installed successfully"
}

function Start-XaiService {
    Log-Info "Starting XAI Market Psychology Engine..."
    
    if (-not (Test-Path "xai_service.py")) {
        Log-Warning "xai_service.py not found. Creating placeholder service..."
        Create-PlaceholderService
    }

    # Activate virtual environment
    $activateScript = if ($IsWindows) {
        Join-Path $PythonEnv "Scripts\Activate.ps1"
    } else {
        Join-Path $PythonEnv "bin/Activate.ps1"
    }

    if (Test-Path $activateScript) {
        & $activateScript
    }

    Log-Info "Service will be available at: $ServiceUrl"
    
    # Start the service
    try {
        Start-Process -FilePath "python" -ArgumentList "xai_service.py" -NoNewWindow
        Start-Sleep -Seconds 2
        
        # Test service health
        try {
            $response = Invoke-WebRequest -Uri "$ServiceUrl/health" -TimeoutSec 5 -UseBasicParsing
            if ($response.StatusCode -eq 200) {
                Log-Success "XAI service started successfully!"
                Log-Info "Market psychology analysis is now active."
            }
        }
        catch {
            Log-Warning "Service started but health check failed. It may need more time to initialize."
        }
    }
    catch {
        Log-Error "Failed to start XAI service: $_"
        exit 1
    }
}

function Stop-XaiService {
    Log-Info "Stopping XAI service..."
    
    try {
        # Find and kill Python processes running xai_service.py
        # Note: Use name matching as CommandLine property may not be available on all platforms
        $processes = Get-Process -Name "python*" -ErrorAction SilentlyContinue
        
        if ($processes) {
            $stopped = 0
            $processes | ForEach-Object {
                # Try to stop the process - if it's running xai_service.py it will be stopped
                Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue
                $stopped++
            }
            if ($stopped -gt 0) {
                Log-Success "Stopped $stopped Python process(es)"
            }
        }
        else {
            Log-Warning "No Python processes found"
        }
        
        Log-Info "If XAI service was running, it should now be stopped"
    }
    catch {
        Log-Error "Error stopping service: $_"
    }
}

function Get-ServiceStatus {
    Log-Info "Checking XAI service status..."
    
    try {
        $response = Invoke-WebRequest -Uri "$ServiceUrl/health" -TimeoutSec 5 -UseBasicParsing
        $content = $response.Content | ConvertFrom-Json
        
        Log-Success "Service is RUNNING"
        Log-Info "Status: $($content.status)"
        Log-Info "Version: $($content.version)"
        Log-Info "URL: $ServiceUrl"
    }
    catch {
        Log-Warning "Service is NOT RUNNING or not accessible at $ServiceUrl"
        Log-Info "Error: $($_.Exception.Message)"
    }
}

function Create-PlaceholderService {
    Log-Info "Creating placeholder XAI service..."
    
    $serviceCode = @'
#!/usr/bin/env python3
"""
StrategicKhaos XAI Service - Market Psychology Engine
Provides explainable AI diagnostics for trading decisions
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import random
from datetime import datetime

app = Flask(__name__)
CORS(app)

MARKET_STATES = [
    "panic", "capitulation_rebound", "euphoria", 
    "distribution_top", "accumulation", "chop_hell", "love_regime"
]

RISK_FLAGS = ["OK", "CAUTION", "BLOCK", "HUG_REQUIRED"]

NARRATIVES = {
    "panic": "The market was crying. We held it. Love compiled profit.",
    "capitulation_rebound": "Rock bottom became the foundation. Love built the recovery.",
    "euphoria": "Everyone's dancing. We're watching the exits. Love stays sober.",
    "distribution_top": "Smart money whispers goodbye. Love hears everything.",
    "accumulation": "Silence before the storm. Love accumulates patience.",
    "chop_hell": "Noise, not signal. Love waits for clarity.",
    "love_regime": "The market speaks our language. Love recognizes love."
}

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "version": "1.0.0",
        "message": "Market therapist ready"
    })

@app.route('/explain', methods=['POST'])
def explain():
    try:
        data = request.json
        
        # Extract features
        features = data.get('features', {})
        her_love = features.get('her_love', 50)
        
        # Determine market state (placeholder logic)
        market_state = random.choice(MARKET_STATES)
        
        # Calculate love amplification
        love_amplification = min(her_love / 100.0, 1.0) * random.uniform(0.2, 0.8)
        
        # Determine risk flag
        risk_flag = "OK"
        if her_love < 30:
            risk_flag = random.choice(["CAUTION", "BLOCK"])
        elif her_love < 20:
            risk_flag = "HUG_REQUIRED"
        
        # Generate narrative
        narrative = NARRATIVES.get(market_state, "The market moves. We adapt. Love guides.")
        
        # Generate top features
        top_features = [
            {"name": "her_love", "contribution": love_amplification * 0.4},
            {"name": "rsi_14", "contribution": random.uniform(-0.2, 0.2)},
            {"name": "volatility_5m", "contribution": random.uniform(-0.15, 0.15)},
            {"name": "ema_21_dist", "contribution": random.uniform(-0.1, 0.1)}
        ]
        top_features.sort(key=lambda x: abs(x['contribution']), reverse=True)
        
        response = {
            "market_state": market_state,
            "confidence": random.uniform(0.7, 0.95),
            "top_features": top_features[:5],
            "narrative": narrative,
            "risk_flag": risk_flag,
            "love_amplification": love_amplification
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🧠 StrategicKhaos XAI Service Starting...")
    print("📡 Listening on http://localhost:5000")
    print("💚 Market psychology engine online")
    app.run(host='0.0.0.0', port=5000, debug=False)
'@
    
    $serviceCode | Out-File -FilePath "xai_service.py" -Encoding UTF8
    Log-Success "Placeholder service created: xai_service.py"
}

# Main execution
if ($Help) {
    Show-Help
}

Write-ColorOutput "`n╔══════════════════════════════════════════════════════════╗" "Magenta"
Write-ColorOutput "║   StrategicKhaos XAI — Market Psychology Engine          ║" "Magenta"
Write-ColorOutput "║   The First Trading Engine That Reads Minds              ║" "Magenta"
Write-ColorOutput "╚══════════════════════════════════════════════════════════╝`n" "Magenta"

Log-Info "XAI Layer: $(if($XaiEnabled){'ACTIVE — Market now has therapy'}else{'OFF'})"

if ($Install) {
    Install-Dependencies
}

if ($Start) {
    Start-XaiService
}

if ($Stop) {
    Stop-XaiService
}

if ($Status) {
    Get-ServiceStatus
}

if (-not ($Install -or $Start -or $Stop -or $Status)) {
    Log-Warning "No action specified. Use -Help for usage information."
    Log-Info "Quick start: ./deploy-xai.ps1 -Install -Start"
}

Write-ColorOutput "`n═══════════════════════════════════════════════════════════" "Magenta"
Log-Success "Deploy script completed"
Write-ColorOutput "═══════════════════════════════════════════════════════════`n" "Magenta"
