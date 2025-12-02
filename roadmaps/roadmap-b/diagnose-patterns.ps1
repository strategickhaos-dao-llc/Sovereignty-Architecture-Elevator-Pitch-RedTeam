#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Diagnose design patterns in your codebase
.DESCRIPTION
    Analyzes your codebase to identify which design patterns you're already using,
    providing concrete examples from your actual code.
#>

Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  PATTERN DIAGNOSIS - Roadmap B" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

Write-Host "Analyzing your codebase for design patterns..." -ForegroundColor Yellow
Write-Host ""

$patterns = @()

# Check for Strategy Pattern
Write-Host "[1/5] Checking for Strategy Pattern..." -ForegroundColor Green
$strategyFiles = Get-ChildItem -Recurse -Filter "*processor*.py","*handler*.py" -ErrorAction SilentlyContinue
if ($strategyFiles) {
    Write-Host "  ✓ Found potential Strategy pattern in:" -ForegroundColor Cyan
    $strategyFiles | Select-Object -First 3 | ForEach-Object {
        Write-Host "    - $($_.FullName)" -ForegroundColor Gray
    }
    $patterns += "Strategy"
}

# Check for Observer Pattern
Write-Host ""
Write-Host "[2/5] Checking for Observer Pattern..." -ForegroundColor Green
$observerFiles = Get-ChildItem -Recurse -ErrorAction SilentlyContinue | 
                 Get-Content -ErrorAction SilentlyContinue | 
                 Select-String "notify|subscribe|observer|listener" -Quiet
if ($observerFiles) {
    Write-Host "  ✓ Found potential Observer pattern" -ForegroundColor Cyan
    $patterns += "Observer"
}

# Check for Factory Pattern
Write-Host ""
Write-Host "[3/5] Checking for Factory Pattern..." -ForegroundColor Green
$factoryFiles = Get-ChildItem -Recurse -Filter "*factory*.py","*builder*.py" -ErrorAction SilentlyContinue
if ($factoryFiles) {
    Write-Host "  ✓ Found potential Factory pattern in:" -ForegroundColor Cyan
    $factoryFiles | Select-Object -First 3 | ForEach-Object {
        Write-Host "    - $($_.FullName)" -ForegroundColor Gray
    }
    $patterns += "Factory"
}

# Check for Singleton Pattern
Write-Host ""
Write-Host "[4/5] Checking for Singleton Pattern..." -ForegroundColor Green
$singletonFiles = Get-ChildItem -Recurse -Filter "*.py" -ErrorAction SilentlyContinue | 
                  Get-Content -ErrorAction SilentlyContinue | 
                  Select-String "_instance.*None|__new__" -Quiet
if ($singletonFiles) {
    Write-Host "  ✓ Found potential Singleton pattern" -ForegroundColor Cyan
    $patterns += "Singleton"
}

# Check for Decorator Pattern
Write-Host ""
Write-Host "[5/5] Checking for Decorator Pattern..." -ForegroundColor Green
$decoratorFiles = Get-ChildItem -Recurse -Filter "*.py" -ErrorAction SilentlyContinue | 
                  Get-Content -ErrorAction SilentlyContinue | 
                  Select-String "@\w+|def decorator" -Quiet
if ($decoratorFiles) {
    Write-Host "  ✓ Found potential Decorator pattern" -ForegroundColor Cyan
    $patterns += "Decorator"
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  DIAGNOSIS SUMMARY" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

if ($patterns.Count -gt 0) {
    Write-Host "✓ Detected $($patterns.Count) design patterns in your code:" -ForegroundColor Green
    Write-Host ""
    $patterns | ForEach-Object { Write-Host "  • $_" -ForegroundColor Cyan }
    Write-Host ""
    Write-Host "These patterns are covered in Roadmap B, items 21-40." -ForegroundColor Gray
    Write-Host "Read: roadmaps/roadmap-b/README.md for detailed explanations." -ForegroundColor Gray
} else {
    Write-Host "No obvious design patterns detected." -ForegroundColor Yellow
    Write-Host "This is normal for early-stage code. Roadmap B will help you recognize them as they emerge." -ForegroundColor Gray
}

Write-Host ""
