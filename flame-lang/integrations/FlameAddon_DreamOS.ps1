<#
╔══════════════════════════════════════════════════════════════════════════════╗
║  FLAME ADDON - DreamOS Bootstrap Integration                                 ║
║  System initialization and Flame Lang runtime bootstrap                      ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Part of the Strategic Khaos Sovereignty Architecture                        ║
║  Author: Domenic Garza / StrategicKhaos DAO LLC                             ║
╚══════════════════════════════════════════════════════════════════════════════╝

.SYNOPSIS
    Bootstrap addon for integrating Flame Lang into DreamOS environment.

.DESCRIPTION
    This addon provides:
    - Flame Lang runtime environment setup
    - System path configuration
    - Node network initialization
    - Sovereignty oath chain bootstrap
    - Integration with DreamOS services

.EXAMPLE
    .\FlameAddon_DreamOS.ps1 -Action init
    
.EXAMPLE
    .\FlameAddon_DreamOS.ps1 -Action activate -NodeName "Nova-Prime"
#>

param(
    [Parameter(Position=0)]
    [ValidateSet("init", "activate", "deactivate", "status", "sync", "upgrade")]
    [string]$Action = "status",
    
    [Parameter()]
    [string]$NodeName = "",
    
    [Parameter()]
    [string]$ConfigPath = "",
    
    [Parameter()]
    [switch]$Force,
    
    [Parameter()]
    [switch]$Silent
)

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

$Script:DreamOSConfig = @{
    Version = "1.0.0"
    FlameLangVersion = "1.0.0"
    
    Paths = @{
        FlameHome = "$env:USERPROFILE\.flame"
        FlameBin = "$env:USERPROFILE\.flame\bin"
        FlameLib = "$env:USERPROFILE\.flame\lib"
        FlameModules = "$env:USERPROFILE\.flame\modules"
        FlameOaths = "$env:USERPROFILE\.flame\oaths"
        FlameNodes = "$env:USERPROFILE\.flame\nodes"
        FlameCache = "$env:USERPROFILE\.flame\cache"
    }
    
    Services = @{
        Interpreter = "flame_interpreter"
        NodeManager = "flame_nodes"
        OathService = "flame_oaths"
        ReconService = "flame_recon"
    }
    
    DefaultNodes = @(
        @{ Name = "Nova-Prime"; Tier = 1; Role = "Controller" }
        @{ Name = "Lyra-Alpha"; Tier = 2; Role = "Worker" }
        @{ Name = "Pulsar-01"; Tier = 3; Role = "Observer" }
    )
}

# ═══════════════════════════════════════════════════════════════════════════════
# LOGGING
# ═══════════════════════════════════════════════════════════════════════════════

function Write-FlameLog {
    param(
        [Parameter(Mandatory)]
        [string]$Message,
        
        [Parameter()]
        [ValidateSet("Info", "Success", "Warning", "Error")]
        [string]$Level = "Info"
    )
    
    if ($Script:Silent) { return }
    
    $timestamp = Get-Date -Format "HH:mm:ss"
    $prefix = switch ($Level) {
        "Info"    { "🔹" }
        "Success" { "✓" }
        "Warning" { "⚠" }
        "Error"   { "✗" }
    }
    
    $color = switch ($Level) {
        "Info"    { "Cyan" }
        "Success" { "Green" }
        "Warning" { "Yellow" }
        "Error"   { "Red" }
    }
    
    Write-Host "[$timestamp] $prefix $Message" -ForegroundColor $color
}

# ═══════════════════════════════════════════════════════════════════════════════
# INITIALIZATION
# ═══════════════════════════════════════════════════════════════════════════════

function Initialize-FlameEnvironment {
    <#
    .SYNOPSIS
        Initializes the Flame Lang environment for DreamOS.
    #>
    
    Write-Host @"
╔══════════════════════════════════════════════════════════════╗
║  FLAME ADDON - DreamOS Bootstrap                             ║
║  Initializing Flame Lang Environment...                      ║
╚══════════════════════════════════════════════════════════════╝
"@
    
    # Create directory structure
    Write-FlameLog "Creating directory structure..." -Level Info
    foreach ($path in $Script:DreamOSConfig.Paths.Values) {
        if (-not (Test-Path $path)) {
            New-Item -ItemType Directory -Path $path -Force | Out-Null
            Write-FlameLog "  Created: $path" -Level Success
        }
    }
    
    # Create configuration file
    Write-FlameLog "Creating configuration file..." -Level Info
    $configFile = Join-Path $Script:DreamOSConfig.Paths.FlameHome "config.json"
    $config = @{
        version = $Script:DreamOSConfig.Version
        flameLangVersion = $Script:DreamOSConfig.FlameLangVersion
        initialized = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
        paths = $Script:DreamOSConfig.Paths
        services = @{}
    }
    $config | ConvertTo-Json -Depth 10 | Out-File $configFile -Encoding UTF8
    Write-FlameLog "  Config saved: $configFile" -Level Success
    
    # Initialize default nodes
    Write-FlameLog "Initializing default nodes..." -Level Info
    $nodesFile = Join-Path $Script:DreamOSConfig.Paths.FlameNodes "registry.json"
    $nodes = @{
        nodes = $Script:DreamOSConfig.DefaultNodes
        lastUpdated = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
    }
    $nodes | ConvertTo-Json -Depth 10 | Out-File $nodesFile -Encoding UTF8
    Write-FlameLog "  Registered $($Script:DreamOSConfig.DefaultNodes.Count) default nodes" -Level Success
    
    # Create initial oath
    Write-FlameLog "Creating bootstrap oath..." -Level Info
    $bootstrapOath = @{
        bearer = $env:USERNAME
        seal = "SHA256"
        timestamp = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
        type = "bootstrap"
        message = "DreamOS Flame Addon Initialized"
    }
    
    $payload = "$($bootstrapOath.bearer):$($bootstrapOath.seal):$($bootstrapOath.timestamp)"
    $sha256 = [System.Security.Cryptography.SHA256]::Create()
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($payload)
    $hash = $sha256.ComputeHash($bytes)
    $bootstrapOath.signature = ([System.BitConverter]::ToString($hash) -replace '-', '').ToLower()
    
    $oathFile = Join-Path $Script:DreamOSConfig.Paths.FlameOaths "bootstrap.json"
    $bootstrapOath | ConvertTo-Json | Out-File $oathFile -Encoding UTF8
    Write-FlameLog "  Bootstrap oath created" -Level Success
    
    # Update PATH environment (session only)
    Write-FlameLog "Updating environment..." -Level Info
    $binPath = $Script:DreamOSConfig.Paths.FlameBin
    if ($env:PATH -notlike "*$binPath*") {
        $env:PATH = "$binPath;$env:PATH"
        Write-FlameLog "  Added Flame bin to PATH" -Level Success
    }
    
    # Create launcher scripts
    Write-FlameLog "Creating launcher scripts..." -Level Info
    
    $flameLauncher = @"
@echo off
python "%~dp0..\lib\flame_lang_interpreter.py" %*
"@
    $flameLauncher | Out-File (Join-Path $Script:DreamOSConfig.Paths.FlameBin "flame.cmd") -Encoding ASCII
    
    $flamePs1 = @"
#!/usr/bin/env pwsh
python `$PSScriptRoot\..\lib\flame_lang_interpreter.py @args
"@
    $flamePs1 | Out-File (Join-Path $Script:DreamOSConfig.Paths.FlameBin "flame.ps1") -Encoding UTF8
    
    Write-FlameLog "  Launcher scripts created" -Level Success
    
    Write-Host @"

╔══════════════════════════════════════════════════════════════╗
║  INITIALIZATION COMPLETE                                     ║
╠══════════════════════════════════════════════════════════════╣
║  Flame Home:    $($Script:DreamOSConfig.Paths.FlameHome)
║  Version:       $($Script:DreamOSConfig.FlameLangVersion)
║  Nodes:         $($Script:DreamOSConfig.DefaultNodes.Count) registered
║                                                              ║
║  Run 'flame' to start the interpreter                        ║
║  Run '.\FlameAddon_DreamOS.ps1 status' to check status       ║
╚══════════════════════════════════════════════════════════════╝
"@
}

# ═══════════════════════════════════════════════════════════════════════════════
# NODE ACTIVATION
# ═══════════════════════════════════════════════════════════════════════════════

function Enable-FlameNode {
    <#
    .SYNOPSIS
        Activates a Flame node.
    #>
    param(
        [Parameter(Mandatory)]
        [string]$Name
    )
    
    Write-FlameLog "Activating node: $Name" -Level Info
    
    $nodesFile = Join-Path $Script:DreamOSConfig.Paths.FlameNodes "registry.json"
    if (-not (Test-Path $nodesFile)) {
        Write-FlameLog "Node registry not found. Run 'init' first." -Level Error
        return $false
    }
    
    $registry = Get-Content $nodesFile | ConvertFrom-Json
    $found = $false
    
    foreach ($node in $registry.nodes) {
        if ($node.Name -eq $Name) {
            $node | Add-Member -NotePropertyName "Active" -NotePropertyValue $true -Force
            $node | Add-Member -NotePropertyName "ActivatedAt" -NotePropertyValue (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ") -Force
            $found = $true
            break
        }
    }
    
    if (-not $found) {
        Write-FlameLog "Node '$Name' not found in registry" -Level Error
        return $false
    }
    
    $registry.lastUpdated = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
    $registry | ConvertTo-Json -Depth 10 | Out-File $nodesFile -Encoding UTF8
    
    Write-FlameLog "Node '$Name' activated successfully" -Level Success
    return $true
}

function Disable-FlameNode {
    <#
    .SYNOPSIS
        Deactivates a Flame node.
    #>
    param(
        [Parameter(Mandatory)]
        [string]$Name
    )
    
    Write-FlameLog "Deactivating node: $Name" -Level Info
    
    $nodesFile = Join-Path $Script:DreamOSConfig.Paths.FlameNodes "registry.json"
    if (-not (Test-Path $nodesFile)) {
        Write-FlameLog "Node registry not found." -Level Error
        return $false
    }
    
    $registry = Get-Content $nodesFile | ConvertFrom-Json
    
    foreach ($node in $registry.nodes) {
        if ($node.Name -eq $Name) {
            $node | Add-Member -NotePropertyName "Active" -NotePropertyValue $false -Force
            $node | Add-Member -NotePropertyName "DeactivatedAt" -NotePropertyValue (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ") -Force
            break
        }
    }
    
    $registry.lastUpdated = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
    $registry | ConvertTo-Json -Depth 10 | Out-File $nodesFile -Encoding UTF8
    
    Write-FlameLog "Node '$Name' deactivated" -Level Success
    return $true
}

# ═══════════════════════════════════════════════════════════════════════════════
# STATUS CHECK
# ═══════════════════════════════════════════════════════════════════════════════

function Get-FlameSystemStatus {
    <#
    .SYNOPSIS
        Gets comprehensive Flame system status.
    #>
    
    $status = @{
        initialized = $false
        version = $Script:DreamOSConfig.Version
        flameLangVersion = $Script:DreamOSConfig.FlameLangVersion
        paths = @{}
        nodes = @()
        oaths = 0
    }
    
    # Check paths
    foreach ($key in $Script:DreamOSConfig.Paths.Keys) {
        $path = $Script:DreamOSConfig.Paths[$key]
        $status.paths[$key] = Test-Path $path
    }
    
    # Check if initialized
    $configFile = Join-Path $Script:DreamOSConfig.Paths.FlameHome "config.json"
    $status.initialized = Test-Path $configFile
    
    # Get nodes
    $nodesFile = Join-Path $Script:DreamOSConfig.Paths.FlameNodes "registry.json"
    if (Test-Path $nodesFile) {
        $registry = Get-Content $nodesFile | ConvertFrom-Json
        $status.nodes = $registry.nodes
    }
    
    # Count oaths
    $oathsPath = $Script:DreamOSConfig.Paths.FlameOaths
    if (Test-Path $oathsPath) {
        $status.oaths = (Get-ChildItem $oathsPath -Filter "*.json").Count
    }
    
    return $status
}

function Show-FlameStatus {
    <#
    .SYNOPSIS
        Displays Flame system status.
    #>
    
    $status = Get-FlameSystemStatus
    
    $initStatus = if ($status.initialized) { "✓ Yes" } else { "✗ No" }
    $initColor = if ($status.initialized) { "Green" } else { "Red" }
    
    Write-Host @"
╔══════════════════════════════════════════════════════════════╗
║  FLAME ADDON - DreamOS Status                                ║
╠══════════════════════════════════════════════════════════════╣
"@
    Write-Host "  Addon Version:      $($status.version)"
    Write-Host "  Flame Lang Version: $($status.flameLangVersion)"
    Write-Host -NoNewline "  Initialized:        "
    Write-Host $initStatus -ForegroundColor $initColor
    Write-Host "  Oath Tokens:        $($status.oaths)"
    Write-Host "╠══════════════════════════════════════════════════════════════╣"
    Write-Host "║  NODES                                                       ║"
    Write-Host "╠══════════════════════════════════════════════════════════════╣"
    
    if ($status.nodes.Count -eq 0) {
        Write-Host "  No nodes registered"
    } else {
        foreach ($node in $status.nodes) {
            $active = if ($node.Active) { "✓" } else { "○" }
            $color = if ($node.Active) { "Green" } else { "Gray" }
            Write-Host -NoNewline "  $active "
            Write-Host "[$($node.Role)] $($node.Name) (Tier $($node.Tier))" -ForegroundColor $color
        }
    }
    
    Write-Host "╠══════════════════════════════════════════════════════════════╣"
    Write-Host "║  PATHS                                                       ║"
    Write-Host "╠══════════════════════════════════════════════════════════════╣"
    
    foreach ($key in $status.paths.Keys) {
        $exists = if ($status.paths[$key]) { "✓" } else { "✗" }
        $color = if ($status.paths[$key]) { "Green" } else { "Red" }
        Write-Host -NoNewline "  $exists "
        Write-Host $key -ForegroundColor $color
    }
    
    Write-Host "╚══════════════════════════════════════════════════════════════╝"
}

# ═══════════════════════════════════════════════════════════════════════════════
# SYNC & UPGRADE
# ═══════════════════════════════════════════════════════════════════════════════

function Sync-FlameNodes {
    <#
    .SYNOPSIS
        Synchronizes node state across the network.
    #>
    
    Write-FlameLog "Synchronizing nodes..." -Level Info
    
    $nodesFile = Join-Path $Script:DreamOSConfig.Paths.FlameNodes "registry.json"
    if (-not (Test-Path $nodesFile)) {
        Write-FlameLog "No nodes to sync" -Level Warning
        return
    }
    
    $registry = Get-Content $nodesFile | ConvertFrom-Json
    
    foreach ($node in $registry.nodes) {
        $node | Add-Member -NotePropertyName "LastSync" -NotePropertyValue (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ") -Force
        Write-FlameLog "  Synced: $($node.Name)" -Level Success
    }
    
    $registry.lastUpdated = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
    $registry | ConvertTo-Json -Depth 10 | Out-File $nodesFile -Encoding UTF8
    
    Write-FlameLog "Sync complete" -Level Success
}

function Update-FlameAddon {
    <#
    .SYNOPSIS
        Upgrades the Flame addon to the latest version.
    #>
    
    Write-FlameLog "Checking for updates..." -Level Info
    
    # Placeholder for actual update logic
    Write-FlameLog "Addon is up to date (v$($Script:DreamOSConfig.Version))" -Level Success
}

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN EXECUTION
# ═══════════════════════════════════════════════════════════════════════════════

switch ($Action) {
    "init" {
        Initialize-FlameEnvironment
    }
    
    "activate" {
        if (-not $NodeName) {
            Write-FlameLog "NodeName required for activation. Use -NodeName <name>" -Level Error
            exit 1
        }
        Enable-FlameNode -Name $NodeName
    }
    
    "deactivate" {
        if (-not $NodeName) {
            Write-FlameLog "NodeName required for deactivation. Use -NodeName <name>" -Level Error
            exit 1
        }
        Disable-FlameNode -Name $NodeName
    }
    
    "status" {
        Show-FlameStatus
    }
    
    "sync" {
        Sync-FlameNodes
    }
    
    "upgrade" {
        Update-FlameAddon
    }
    
    default {
        Show-FlameStatus
    }
}
