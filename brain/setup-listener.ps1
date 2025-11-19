# Strategickhaos Listener Setup Script (Windows PowerShell)
# This script creates a virtual environment and installs dependencies

param(
    [switch]$Force
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$VenvDir = Join-Path $ScriptDir "jarvis_venv"
$RequirementsFile = Join-Path $ScriptDir "requirements.txt"
$ListenerScript = Join-Path $ScriptDir "plugins\listener_bind_58563.py"
$LogsDir = Join-Path $ScriptDir "logs"

# Color output functions
function Write-ColorText {
    param(
        [string]$Text,
        [string]$Color = "White"
    )
    Write-Host $Text -ForegroundColor $Color
}

function Log {
    param([string]$Message)
    Write-ColorText $Message -Color Cyan
}

function Success {
    param([string]$Message)
    Write-ColorText $Message -Color Green
}

function Error {
    param([string]$Message)
    Write-ColorText $Message -Color Red
}

function Warn {
    param([string]$Message)
    Write-ColorText $Message -Color Yellow
}

# Main setup
Write-ColorText "🔧 Strategickhaos Listener Setup" -Color Magenta
Write-Host "================================="
Write-Host ""

# Check if Python is available
try {
    $pythonVersion = & py --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Python not found"
    }
    Success "✅ Found: $pythonVersion"
} catch {
    Error "❌ Error: Python is not installed or 'py' launcher is not available"
    Error "Please install Python 3.8 or higher from python.org"
    exit 1
}

Write-Host ""

# Create virtual environment
Log "📦 Creating virtual environment at: $VenvDir"
if (Test-Path $VenvDir) {
    if ($Force) {
        Warn "⚠️  Virtual environment already exists. Removing..."
        Remove-Item -Recurse -Force $VenvDir
    } else {
        Warn "⚠️  Virtual environment already exists."
        $response = Read-Host "Do you want to recreate it? (y/N)"
        if ($response -eq "y" -or $response -eq "Y") {
            Remove-Item -Recurse -Force $VenvDir
        } else {
            Log "Using existing virtual environment"
        }
    }
}

if (-not (Test-Path $VenvDir)) {
    & py -m venv $VenvDir
    if ($LASTEXITCODE -ne 0) {
        Error "❌ Failed to create virtual environment"
        exit 1
    }
    Success "✅ Virtual environment created"
}

Write-Host ""

# Activate virtual environment and install dependencies
Log "🔌 Installing dependencies..."
$activateScript = Join-Path $VenvDir "Scripts\Activate.ps1"
$pythonExe = Join-Path $VenvDir "Scripts\python.exe"
$pipExe = Join-Path $VenvDir "Scripts\pip.exe"

# Upgrade pip
Log "📥 Upgrading pip..."
& $pythonExe -m pip install --upgrade pip --quiet
if ($LASTEXITCODE -ne 0) {
    Warn "⚠️  Warning: Failed to upgrade pip"
}

# Install dependencies
Log "📥 Installing dependencies from requirements.txt..."
& $pipExe install -r $RequirementsFile
if ($LASTEXITCODE -ne 0) {
    Error "❌ Failed to install dependencies"
    exit 1
}

# Create logs directory if it doesn't exist
if (-not (Test-Path $LogsDir)) {
    New-Item -Path $LogsDir -ItemType Directory -Force | Out-Null
}

Write-Host ""
Success "✅ Setup complete!"
Write-Host ""
Write-ColorText "To use the listener:" -Color Yellow
Write-Host ""
Write-Host "  1. Activate the virtual environment:"
Write-Host "     .\jarvis_venv\Scripts\Activate.ps1"
Write-Host ""
Write-Host "  2. Run the listener:"
Write-Host "     .\jarvis_venv\Scripts\python.exe .\plugins\listener_bind_58563.py"
Write-Host ""
Write-Host "  Or run with logging:"
Write-Host "     .\jarvis_venv\Scripts\python.exe .\plugins\listener_bind_58563.py | Tee-Object -FilePath .\logs\listener_output.log"
Write-Host ""
Write-ColorText "🚀 Ready to launch!" -Color Green
