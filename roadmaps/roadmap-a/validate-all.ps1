#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Validate all Roadmap A improvements
.DESCRIPTION
    Runs all validators to check naming conventions, structure, and configuration
.PARAMETER Fix
    Automatically fix issues where possible
#>

param(
    [switch]$Fix
)

Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  ROADMAP A VALIDATION" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

$issues = @()
$fixedIssues = @()

# 1. Check naming conventions
Write-Host "[1/5] Checking naming conventions..." -ForegroundColor Yellow

# Check for spaces in filenames
$filesWithSpaces = Get-ChildItem -Recurse -File | Where-Object { $_.Name -match '\s' }
if ($filesWithSpaces) {
    $count = ($filesWithSpaces | Measure-Object).Count
    $issues += "Found $count files with spaces in names"
    Write-Host "  ✗ $count files with spaces in names" -ForegroundColor Red
    
    if ($Fix) {
        foreach ($file in $filesWithSpaces) {
            $newName = $file.Name -replace '\s', '-'
            Rename-Item $file.FullName $newName
            $fixedIssues += "Renamed: $($file.Name) → $newName"
        }
        Write-Host "    ✓ Fixed $count filenames" -ForegroundColor Green
    }
} else {
    Write-Host "  ✓ No files with spaces" -ForegroundColor Green
}

# Check for uppercase in Python filenames (except constants)
$pythonFiles = Get-ChildItem -Recurse -Filter "*.py" -ErrorAction SilentlyContinue
$uppercasePython = $pythonFiles | Where-Object { $_.Name -cmatch '[A-Z]' -and $_.Name -notmatch '^[A-Z_]+\.py$' }
if ($uppercasePython) {
    $count = ($uppercasePython | Measure-Object).Count
    $issues += "Found $count Python files with uppercase (should be snake_case)"
    Write-Host "  ✗ $count Python files should use snake_case" -ForegroundColor Red
} else {
    Write-Host "  ✓ Python files follow naming convention" -ForegroundColor Green
}

# 2. Check folder structure
Write-Host ""
Write-Host "[2/5] Checking folder structure..." -ForegroundColor Yellow

$requiredDirs = @("src", "scripts", "docs")
$missingDirs = $requiredDirs | Where-Object { -not (Test-Path $_) }

if ($missingDirs) {
    $issues += "Missing recommended directories: $($missingDirs -join ', ')"
    Write-Host "  ⚠ Missing directories: $($missingDirs -join ', ')" -ForegroundColor Yellow
    
    if ($Fix) {
        foreach ($dir in $missingDirs) {
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
            $fixedIssues += "Created directory: $dir"
        }
        Write-Host "    ✓ Created missing directories" -ForegroundColor Green
    }
} else {
    Write-Host "  ✓ Basic folder structure exists" -ForegroundColor Green
}

# 3. Check for build artifacts
Write-Host ""
Write-Host "[3/5] Checking for build artifacts..." -ForegroundColor Yellow

$artifacts = @(
    (Get-ChildItem -Recurse -Directory -Filter "__pycache__" -ErrorAction SilentlyContinue),
    (Get-ChildItem -Recurse -Directory -Filter "node_modules" -ErrorAction SilentlyContinue),
    (Get-ChildItem -Recurse -File -Filter "*.pyc" -ErrorAction SilentlyContinue)
)

$totalArtifacts = ($artifacts | Measure-Object).Count
if ($totalArtifacts -gt 0) {
    $issues += "Found $totalArtifacts build artifacts (should be cleaned)"
    Write-Host "  ⚠ Found $totalArtifacts build artifacts" -ForegroundColor Yellow
    Write-Host "    Run: ./roadmaps/roadmap-a/scripts/02-clean-artifacts.ps1" -ForegroundColor Gray
} else {
    Write-Host "  ✓ No build artifacts found" -ForegroundColor Green
}

# 4. Check for LICENSE files
Write-Host ""
Write-Host "[4/5] Checking for LICENSE files..." -ForegroundColor Yellow

if (-not (Test-Path "LICENSE")) {
    $issues += "Missing LICENSE file"
    Write-Host "  ✗ No LICENSE file in root" -ForegroundColor Red
} else {
    Write-Host "  ✓ LICENSE file exists" -ForegroundColor Green
}

# 5. Check configuration files
Write-Host ""
Write-Host "[5/5] Checking configuration files..." -ForegroundColor Yellow

$yamlFiles = Get-ChildItem -Recurse -Filter "*.yml" -ErrorAction SilentlyContinue
$yamlErrors = @()

foreach ($yaml in $yamlFiles) {
    try {
        $null = Get-Content $yaml.FullName | ConvertFrom-Yaml -ErrorAction Stop 2>$null
    } catch {
        $yamlErrors += $yaml.Name
    }
}

if ($yamlErrors.Count -gt 0) {
    $issues += "Found $($yamlErrors.Count) YAML files with syntax errors"
    Write-Host "  ✗ $($yamlErrors.Count) YAML files with syntax errors" -ForegroundColor Red
    $yamlErrors | ForEach-Object { Write-Host "    - $_" -ForegroundColor Gray }
} else {
    Write-Host "  ✓ All YAML files valid" -ForegroundColor Green
}

# Summary
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  VALIDATION SUMMARY" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

if ($issues.Count -eq 0) {
    Write-Host "✓ All validations passed!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Your codebase follows Roadmap A conventions." -ForegroundColor Green
} else {
    Write-Host "Found $($issues.Count) issues:" -ForegroundColor Yellow
    Write-Host ""
    $issues | ForEach-Object { Write-Host "  • $_" -ForegroundColor Yellow }
    Write-Host ""
    
    if ($Fix) {
        Write-Host "Fixed $($fixedIssues.Count) issues:" -ForegroundColor Green
        $fixedIssues | ForEach-Object { Write-Host "  ✓ $_" -ForegroundColor Green }
        Write-Host ""
    } else {
        Write-Host "Run with -Fix to automatically fix some issues." -ForegroundColor Cyan
    }
}

Write-Host "Recommendations:" -ForegroundColor Cyan
Write-Host "  1. Run: ./roadmaps/roadmap-a/scripts/02-clean-artifacts.ps1" -ForegroundColor Gray
Write-Host "  2. Run: ./roadmaps/roadmap-a/scripts/07-generate-gitignore.ps1" -ForegroundColor Gray
Write-Host "  3. Review naming conventions in roadmaps/roadmap-a/README.md" -ForegroundColor Gray
Write-Host ""
