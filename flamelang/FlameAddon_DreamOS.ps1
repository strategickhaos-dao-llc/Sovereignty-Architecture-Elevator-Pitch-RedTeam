# 🔥 FlameAddon_DreamOS.ps1: Device-Aware Bootstrap
# Strategickhaos Sovereign Symbolic Language
# FlameLang v1.0 - DreamOS Integration Component
#
# This script detects the current device and activates the appropriate
# virtual environment for DreamOS operations.
#
# Supported Nodes:
#   - DOM010101 (Primary)
#   - Lyra (Fractal Processing)
#   - Nova (Core AI)
#   - Athena (Strategy)
#   - iPower (Compute)

param(
    [switch]$Verbose,
    [switch]$Force
)

# Get machine identifier
$machine = $env:COMPUTERNAME.ToLower()

Write-Host "🔥 DreamOS Bootstrap Initializing..." -ForegroundColor Magenta
if ($Verbose) {
    Write-Host "  Detected machine: $machine" -ForegroundColor Cyan
}

# Define virtual environment paths for each node
$venvPaths = @{
    "*lyra*"      = @{
        Path = "C:\DreamOS_Bootstrap\DreamOS_Bootstrap_Scaffold\dreamos_fractal_env\Scripts\Activate.ps1"
        Role = "Fractal Processing Node"
    }
    "*nova*"      = @{
        Path = "C:\Users\garza\DreamOS_Bootstrap\DreamOS_Bootstrap_Scaffold\dreamos_nova_env\Scripts\Activate.ps1"
        Role = "Core AI Node"
    }
    "*athena*"    = @{
        Path = "C:\DreamOS_Bootstrap\DreamOS_Bootstrap_Scaffold\dreamos_athena_env\Scripts\Activate.ps1"
        Role = "Strategy Node"
    }
    "*dom010101*" = @{
        Path = "C:\DreamOS_Bootstrap\DreamOS_Bootstrap_Scaffold\dreamos_dom_env\Scripts\Activate.ps1"
        Role = "Primary Control Node"
    }
    "*ipower*"    = @{
        Path = "C:\DreamOS_Bootstrap\DreamOS_Bootstrap_Scaffold\dreamos_compute_env\Scripts\Activate.ps1"
        Role = "Compute Node"
    }
}

# Find matching node configuration
$matchedConfig = $null
$matchedPattern = $null

foreach ($pattern in $venvPaths.Keys) {
    if ($machine -like $pattern) {
        $matchedConfig = $venvPaths[$pattern]
        $matchedPattern = $pattern
        break
    }
}

if ($null -eq $matchedConfig) {
    if ($Verbose) {
        Write-Host "  ⚠️ Unknown device: $machine" -ForegroundColor Yellow
        Write-Host "  DreamOS bootstrap skipped - no matching node configuration" -ForegroundColor DarkGray
    }
    # Silent exit on unknown devices
    return
}

Write-Host "  🌐 Node Identified: $($matchedConfig.Role)" -ForegroundColor Green

# Check if virtual environment exists
$venvPath = $matchedConfig.Path

if (-not (Test-Path $venvPath)) {
    if ($Force) {
        Write-Host "  ⚠️ Virtual environment not found at: $venvPath" -ForegroundColor Yellow
        Write-Host "  Creating placeholder..." -ForegroundColor DarkGray
        
        # Create directory structure
        $venvDir = Split-Path $venvPath -Parent
        if (-not (Test-Path $venvDir)) {
            New-Item -ItemType Directory -Path $venvDir -Force | Out-Null
        }
        
        # Create placeholder activation script
        @"
# DreamOS Virtual Environment Placeholder
# Run: python -m venv $($venvDir | Split-Path -Parent) to create actual venv
Write-Host "⚠️ DreamOS virtual environment not yet configured" -ForegroundColor Yellow
"@ | Out-File -FilePath $venvPath -Encoding UTF8
        
        Write-Host "  ✅ Placeholder created" -ForegroundColor Green
    } else {
        Write-Host "  ❌ Virtual environment not found: $venvPath" -ForegroundColor Red
        Write-Host "  Use -Force to create placeholder" -ForegroundColor DarkGray
        return
    }
}

# Activate the virtual environment
try {
    Write-Host "  🚀 Activating DreamOS environment..." -ForegroundColor Cyan
    . $venvPath
    Write-Host "  ✅ DreamOS Bootstrap Complete" -ForegroundColor Green
    Write-Host "  Role: $($matchedConfig.Role)" -ForegroundColor Cyan
} catch {
    Write-Host "  ❌ Failed to activate environment: $_" -ForegroundColor Red
}

# Display node mesh status
function Show-NodeMeshStatus {
    Write-Host "`n🌐 Node Mesh Status" -ForegroundColor Magenta
    Write-Host "  ┌─────────────┬────────────┬─────────────────────┐" -ForegroundColor DarkGray
    Write-Host "  │ Node        │ Status     │ Role                │" -ForegroundColor DarkGray
    Write-Host "  ├─────────────┼────────────┼─────────────────────┤" -ForegroundColor DarkGray
    
    $nodes = @(
        @{ Name = "DOM010101"; Role = "Primary Control" },
        @{ Name = "Lyra"; Role = "Fractal Processing" },
        @{ Name = "Nova"; Role = "Core AI" },
        @{ Name = "Athena"; Role = "Strategy" },
        @{ Name = "iPower"; Role = "Compute" },
        @{ Name = "Jarvis-VM"; Role = "Cloud Backup" }
    )
    
    foreach ($node in $nodes) {
        $status = if ($machine -like "*$($node.Name.ToLower())*") { "✅ ACTIVE" } else { "⚪ OFFLINE" }
        $color = if ($machine -like "*$($node.Name.ToLower())*") { "Green" } else { "DarkGray" }
        $line = "  │ {0,-11} │ {1,-10} │ {2,-19} │" -f $node.Name, $status, $node.Role
        Write-Host $line -ForegroundColor $color
    }
    
    Write-Host "  └─────────────┴────────────┴─────────────────────┘" -ForegroundColor DarkGray
    Write-Host ""
}

if ($Verbose) {
    Show-NodeMeshStatus
}

Write-Host "`n🔥 DreamOS Ready. Reignite." -ForegroundColor Magenta
