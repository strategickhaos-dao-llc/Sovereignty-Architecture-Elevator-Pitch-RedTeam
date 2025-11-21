#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Clean build artifacts and temporary files from all projects
.DESCRIPTION
    Removes __pycache__, *.pyc, node_modules (preserves package-lock.json),
    dist/, build/, and other build artifacts across the entire repository.
.PARAMETER DryRun
    Show what would be deleted without actually deleting
.PARAMETER Verbose
    Show detailed information about deletions
#>

param(
    [switch]$DryRun,
    [switch]$Verbose
)

$ErrorActionPreference = "Continue"

Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  ARTIFACT CLEANUP - Roadmap A" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

if ($DryRun) {
    Write-Host "DRY RUN MODE - No files will be deleted" -ForegroundColor Yellow
    Write-Host ""
}

$deletedCount = 0
$freedSpace = 0

function Remove-ArtifactDirectory {
    param($Pattern, $Description)
    
    Write-Host "Cleaning: $Description..." -ForegroundColor Green
    $dirs = Get-ChildItem -Recurse -Directory -Filter $Pattern -ErrorAction SilentlyContinue |
            Where-Object { $_.FullName -notmatch "node_modules.*node_modules" }
    
    foreach ($dir in $dirs) {
        $size = (Get-ChildItem -Recurse -File $dir.FullName -ErrorAction SilentlyContinue | 
                 Measure-Object -Property Length -Sum).Sum
        $sizeMB = [math]::Round($size / 1MB, 2)
        
        if ($Verbose -or $DryRun) {
            Write-Host "  - $($dir.FullName) ($sizeMB MB)" -ForegroundColor Gray
        }
        
        if (-not $DryRun) {
            Remove-Item -Recurse -Force $dir.FullName -ErrorAction SilentlyContinue
        }
        
        $script:deletedCount++
        $script:freedSpace += $size
    }
}

function Remove-ArtifactFiles {
    param($Pattern, $Description)
    
    Write-Host "Cleaning: $Description..." -ForegroundColor Green
    $files = Get-ChildItem -Recurse -File -Filter $Pattern -ErrorAction SilentlyContinue
    
    foreach ($file in $files) {
        if ($Verbose -or $DryRun) {
            $sizeMB = [math]::Round($file.Length / 1MB, 2)
            Write-Host "  - $($file.FullName) ($sizeMB MB)" -ForegroundColor Gray
        }
        
        if (-not $DryRun) {
            Remove-Item -Force $file.FullName -ErrorAction SilentlyContinue
        }
        
        $script:deletedCount++
        $script:freedSpace += $file.Length
    }
}

# Python artifacts
Remove-ArtifactDirectory "__pycache__" "Python cache directories"
Remove-ArtifactFiles "*.pyc" "Python compiled files"
Remove-ArtifactFiles "*.pyo" "Python optimized files"
Remove-ArtifactDirectory ".pytest_cache" "Pytest cache"
Remove-ArtifactDirectory ".mypy_cache" "MyPy cache"
Remove-ArtifactDirectory "*.egg-info" "Python egg info"

# JavaScript/Node artifacts
Write-Host "Cleaning: Node modules (preserving package-lock.json)..." -ForegroundColor Green
$nodeModules = Get-ChildItem -Recurse -Directory -Filter "node_modules" -ErrorAction SilentlyContinue |
               Where-Object { $_.FullName -notmatch "node_modules.*node_modules" }

foreach ($dir in $nodeModules) {
    $size = (Get-ChildItem -Recurse -File $dir.FullName -ErrorAction SilentlyContinue | 
             Measure-Object -Property Length -Sum).Sum
    $sizeMB = [math]::Round($size / 1MB, 2)
    
    if ($Verbose -or $DryRun) {
        Write-Host "  - $($dir.FullName) ($sizeMB MB)" -ForegroundColor Gray
    }
    
    if (-not $DryRun) {
        Remove-Item -Recurse -Force $dir.FullName -ErrorAction SilentlyContinue
    }
    
    $script:deletedCount++
    $script:freedSpace += $size
}

# Build directories
Remove-ArtifactDirectory "dist" "Distribution directories"
Remove-ArtifactDirectory "build" "Build directories"
Remove-ArtifactDirectory ".next" "Next.js build cache"
Remove-ArtifactDirectory ".nuxt" "Nuxt.js build cache"
Remove-ArtifactDirectory "out" "Output directories"

# TypeScript
Remove-ArtifactFiles "*.tsbuildinfo" "TypeScript build info"

# Coverage reports
Remove-ArtifactDirectory "coverage" "Coverage reports"
Remove-ArtifactDirectory ".coverage" "Python coverage data"
Remove-ArtifactFiles ".coverage.*" "Python coverage files"
Remove-ArtifactDirectory "htmlcov" "HTML coverage reports"

# IDE artifacts
Remove-ArtifactDirectory ".idea" "IntelliJ IDEA settings"
Remove-ArtifactFiles "*.swp" "Vim swap files"
Remove-ArtifactFiles "*.swo" "Vim swap files"
Remove-ArtifactFiles "*~" "Backup files"
Remove-ArtifactFiles ".DS_Store" "macOS metadata"
Remove-ArtifactFiles "Thumbs.db" "Windows thumbnails"

# Temporary files
Remove-ArtifactDirectory "tmp" "Temporary directories"
Remove-ArtifactDirectory "temp" "Temporary directories"
Remove-ArtifactFiles "*.tmp" "Temporary files"
Remove-ArtifactFiles "*.log" "Log files (in root only)" # Be careful with this

# Docker artifacts (dangling)
if (Get-Command docker -ErrorAction SilentlyContinue) {
    Write-Host "Cleaning: Docker dangling images..." -ForegroundColor Green
    if (-not $DryRun) {
        docker image prune -f 2>$null | Out-Null
    }
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  CLEANUP SUMMARY" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "Items cleaned: $deletedCount" -ForegroundColor Green
Write-Host "Space freed: $([math]::Round($freedSpace / 1MB, 2)) MB" -ForegroundColor Green

if ($DryRun) {
    Write-Host ""
    Write-Host "This was a DRY RUN. Run without -DryRun to actually delete files." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "✓ Cleanup complete!" -ForegroundColor Green
