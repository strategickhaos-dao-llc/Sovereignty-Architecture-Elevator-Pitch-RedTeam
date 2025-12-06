# Quick Start Script for Neural Heir Evolution System (PowerShell)
# Ensures dependencies are installed and provides easy launch commands

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

Write-Host "🧬 Neural Heir Evolution System - Quick Start" -ForegroundColor Cyan
Write-Host ("=" * 60)
Write-Host ""

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ $pythonVersion detected" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.8 or higher." -ForegroundColor Red
    exit 1
}

# Install dependencies if needed
try {
    python -c "import httpx" 2>$null
    Write-Host "✅ Dependencies already installed" -ForegroundColor Green
} catch {
    Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt --user
    Write-Host "✅ Dependencies installed" -ForegroundColor Green
}

Write-Host ""
Write-Host "Available Commands:" -ForegroundColor Cyan
Write-Host ("=" * 60)
Write-Host ""
Write-Host "1. Basic Evolution (MVP):"
Write-Host "   python evolution_engine.py"
Write-Host ""
Write-Host "2. Nuclear Evolution (All Level 10 features):"
Write-Host "   python evolution_nuclear.py --generations 100 --population 20"
Write-Host ""
Write-Host "3. Run Tests:"
Write-Host "   python test_evolution.py"
Write-Host ""
Write-Host "4. Monitor Progress (in another terminal):"
Write-Host "   Get-Content evolution_ledger.jsonl -Wait | ConvertFrom-Json | Select generation, avg_fitness, best_fitness"
Write-Host ""
Write-Host "5. View Lineage Report:"
Write-Host "   python -c `"from lineage import visualize_evolution_progress; visualize_evolution_progress()`""
Write-Host ""
Write-Host ("=" * 60)
Write-Host ""

# Offer to run tests
$runTests = Read-Host "Run tests now? (y/n)"
if ($runTests -eq "y" -or $runTests -eq "Y") {
    Write-Host ""
    Write-Host "Running tests..." -ForegroundColor Yellow
    python test_evolution.py
    Write-Host ""
}

# Offer to start basic evolution
$startEvolution = Read-Host "Start basic evolution now? (y/n)"
if ($startEvolution -eq "y" -or $startEvolution -eq "Y") {
    Write-Host ""
    Write-Host "🚀 Starting evolution engine..." -ForegroundColor Green
    Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
    Write-Host ""
    python evolution_engine.py
}
