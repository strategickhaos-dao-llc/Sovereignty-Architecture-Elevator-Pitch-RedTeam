# flamelang_recon_patch.ps1 - Flame Lang Discovery & TrueNAS Integration
# Strategic Khaos Sovereign Storage Archaeological Extraction Tool

param(
    [string]$Action = "discover",
    [string]$TrueNASHost = "",
    [string]$ShareName = "strategickhaos-vault",
    [string]$DriveLetter = "T",
    [string]$SearchPath = "$env:USERPROFILE",
    [string]$ArchivePath = "",
    [switch]$Verbose,
    [switch]$Force
)

# Color definitions for PowerShell
function Write-ColorText {
    param(
        [string]$Text,
        [string]$Color = "White"
    )
    Write-Host $Text -ForegroundColor $Color
}

function Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "HH:mm:ss"
    Write-ColorText "[$timestamp] $Message" -Color Cyan
}

function Error {
    param([string]$Message)
    Write-ColorText "[ERROR] $Message" -Color Red
}

function Success {
    param([string]$Message)
    Write-ColorText "[SUCCESS] $Message" -Color Green
}

function Warn {
    param([string]$Message)
    Write-ColorText "[WARN] $Message" -Color Yellow
}

function Banner {
    Write-ColorText "" -Color Magenta
    Write-ColorText "╔══════════════════════════════════════════════════════════════════════════════╗" -Color Magenta
    Write-ColorText "║               🔥 FLAME LANG RECON & TRUENAS INTEGRATION                     ║" -Color Magenta
    Write-ColorText "║                     Strategic Khaos Sovereign Storage                       ║" -Color Magenta
    Write-ColorText "║                    Archaeological Extraction Protocol                       ║" -Color Magenta
    Write-ColorText "╚══════════════════════════════════════════════════════════════════════════════╝" -Color Magenta
    Write-ColorText "" -Color Magenta
}

# ═══════════════════════════════════════════════════════════
# DRIVE DISCOVERY & NAVIGATION
# ═══════════════════════════════════════════════════════════

function Get-DriveInventory {
    Log "📊 Discovering available drives and storage..."
    
    Write-ColorText "`n🗄️ Local Drives:" -Color Yellow
    Get-PSDrive -PSProvider FileSystem | Format-Table Name, Root, @{
        Label = 'Size (GB)'
        Expression = { if ($_.Used) { [math]::Round(($_.Used + $_.Free) / 1GB, 2) } else { "N/A" } }
    }, @{
        Label = 'Free (GB)'
        Expression = { if ($_.Free) { [math]::Round($_.Free / 1GB, 2) } else { "N/A" } }
    }, Description -AutoSize
    
    Write-ColorText "`n🌐 Network Shares (SMB Mappings):" -Color Yellow
    try {
        $smbMappings = Get-SmbMapping -ErrorAction SilentlyContinue
        if ($smbMappings) {
            $smbMappings | Format-Table LocalPath, RemotePath, Status -AutoSize
        } else {
            Warn "No SMB network shares currently mapped"
        }
    } catch {
        Warn "Unable to query SMB mappings: $_"
    }
    
    Write-ColorText "`n💾 Volumes:" -Color Yellow
    Get-Volume | Where-Object { $_.DriveLetter } | 
        Format-Table DriveLetter, FileSystemLabel, @{
            Label = 'Size (GB)'
            Expression = { [math]::Round($_.Size / 1GB, 2) }
        }, @{
            Label = 'Free (GB)'
            Expression = { [math]::Round($_.SizeRemaining / 1GB, 2) }
        }, FileSystem -AutoSize
    
    # Check for iSCSI targets
    Write-ColorText "`n🔗 iSCSI Connections:" -Color Yellow
    try {
        $iscsiTargets = Get-IscsiTarget -ErrorAction SilentlyContinue
        if ($iscsiTargets) {
            $iscsiTargets | Format-Table NodeAddress, IsConnected -AutoSize
        } else {
            Warn "No iSCSI targets found"
        }
    } catch {
        Warn "iSCSI initiator not available or not configured"
    }
    
    Success "Drive inventory complete"
}

# ═══════════════════════════════════════════════════════════
# FLAME LANG ARCHAEOLOGICAL DISCOVERY
# ═══════════════════════════════════════════════════════════

function Find-FlameLangArtifacts {
    param(
        [string]$Path = $SearchPath
    )
    
    Log "🔍 Beginning Flame Lang archaeological discovery..."
    Log "Search path: $Path"
    
    $flamePatterns = @(
        "*flame*",
        "*flamelang*",
        "*.flame",
        "*lyra*flame*"
    )
    
    $artifacts = @()
    
    foreach ($pattern in $flamePatterns) {
        Log "   Searching pattern: $pattern"
        try {
            $found = Get-ChildItem -Path $Path -Recurse -Filter $pattern -ErrorAction SilentlyContinue |
                Select-Object FullName, Length, LastWriteTime, @{
                    Label = 'SizeKB'
                    Expression = { [math]::Round($_.Length / 1KB, 2) }
                }
            
            if ($found) {
                $artifacts += $found
            }
        } catch {
            if ($Verbose) {
                Warn "Access denied or error in path: $_"
            }
        }
    }
    
    if ($artifacts.Count -gt 0) {
        Write-ColorText "`n🔥 FLAME LANG ARTIFACTS DISCOVERED:" -Color Green
        $artifacts | Sort-Object LastWriteTime -Descending | Format-Table FullName, SizeKB, LastWriteTime -AutoSize
        
        Success "Found $($artifacts.Count) Flame Lang artifacts"
        return $artifacts
    } else {
        Warn "No Flame Lang artifacts found in $Path"
        Write-ColorText "Try searching different paths or mounting TrueNAS storage" -Color Yellow
        return @()
    }
}

function Export-FlameLangArchive {
    param(
        [array]$Artifacts,
        [string]$DestinationPath
    )
    
    if (-not $DestinationPath) {
        $userProfile = if ($env:USERPROFILE) { $env:USERPROFILE } else { $env:HOME }
        if (-not $userProfile) { $userProfile = "." }
        $DestinationPath = Join-Path $userProfile "strategic-khaos-private\flame-lang-archive"
    }
    
    Log "📦 Creating Flame Lang archive at: $DestinationPath"
    
    # Create destination directory
    if (-not (Test-Path $DestinationPath)) {
        New-Item -ItemType Directory -Force -Path $DestinationPath | Out-Null
        Success "Created archive directory"
    }
    
    $copiedCount = 0
    $errorCount = 0
    
    foreach ($artifact in $Artifacts) {
        try {
            $relativePath = $artifact.FullName -replace [regex]::Escape($SearchPath), ""
            $destFile = Join-Path $DestinationPath (Split-Path $artifact.FullName -Leaf)
            
            Copy-Item -Path $artifact.FullName -Destination $destFile -Force
            $copiedCount++
            
            if ($Verbose) {
                Log "   Copied: $($artifact.FullName)"
            }
        } catch {
            $errorCount++
            if ($Verbose) {
                Warn "   Failed to copy: $($artifact.FullName) - $_"
            }
        }
    }
    
    Success "Archived $copiedCount artifacts to $DestinationPath"
    if ($errorCount -gt 0) {
        Warn "$errorCount artifacts could not be copied"
    }
    
    # Generate manifest
    $manifestPath = Join-Path $DestinationPath "FLAME_MANIFEST.txt"
    $manifestContent = @"
# FLAME LANG ARCHAEOLOGICAL MANIFEST
# Generated: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
# Strategic Khaos Sovereign Storage

## Artifacts Discovered: $($Artifacts.Count)
## Successfully Archived: $copiedCount

## Artifact Inventory:
$($Artifacts | ForEach-Object { "- $($_.FullName) [$($_.SizeKB) KB] - Modified: $($_.LastWriteTime)" } | Out-String)

## Archive Location: $DestinationPath

---
🔥 Flame Lang - Sovereign Computing Language
💜 Strategic Khaos DAO LLC / Valoryield Engine
"@
    
    $manifestContent | Out-File -FilePath $manifestPath -Encoding UTF8
    Success "Manifest created: $manifestPath"
    
    # Open archive in Explorer
    if (-not $Force) {
        $openExplorer = Read-Host "Open archive folder in Explorer? (Y/n)"
        if ($openExplorer -ne "n") {
            explorer.exe $DestinationPath
        }
    }
    
    return $DestinationPath
}

# ═══════════════════════════════════════════════════════════
# TRUENAS INTEGRATION PROTOCOLS
# ═══════════════════════════════════════════════════════════

function Connect-TrueNAS {
    param(
        [string]$Host,
        [string]$Share,
        [string]$Drive
    )
    
    if (-not $Host) {
        Write-ColorText "`n🖥️ TrueNAS Connection Setup" -Color Yellow
        Write-Host "Enter your TrueNAS hostname or IP address"
        Write-Host "Examples: truenas.local, 192.168.1.100, nas.mydomain.com"
        $Host = Read-Host "TrueNAS Host"
    }
    
    if (-not $Share) {
        $Share = $ShareName
    }
    
    if (-not $Drive) {
        $Drive = $DriveLetter
    }
    
    Log "🔗 Connecting to TrueNAS..."
    Log "   Host: $Host"
    Log "   Share: $Share"
    Log "   Drive Letter: ${Drive}:"
    
    $remotePath = "\\$Host\$Share"
    $localPath = "${Drive}:"
    
    # Check if drive is already in use
    if (Test-Path $localPath) {
        Warn "Drive ${Drive}: is already in use"
        $proceed = Read-Host "Disconnect existing mapping and continue? (y/N)"
        if ($proceed -eq "y") {
            try {
                Remove-SmbMapping -LocalPath $localPath -Force -ErrorAction SilentlyContinue
                Success "Disconnected existing mapping"
            } catch {
                Error "Failed to disconnect existing mapping: $_"
                return $false
            }
        } else {
            return $false
        }
    }
    
    # Attempt connection
    try {
        # Test connectivity first
        Log "Testing network connectivity to $Host..."
        if (-not (Test-Connection -ComputerName $Host -Count 1 -Quiet)) {
            Error "Cannot reach TrueNAS at $Host"
            Write-Host "Please verify:"
            Write-Host "  1. TrueNAS is powered on and connected to network"
            Write-Host "  2. SMB sharing is enabled on TrueNAS"
            Write-Host "  3. Firewall allows SMB traffic (port 445)"
            return $false
        }
        
        Success "Network connectivity confirmed"
        
        # Create persistent mapping
        Log "Creating SMB mapping..."
        New-SmbMapping -LocalPath $localPath -RemotePath $remotePath -Persistent $true
        
        Success "TrueNAS mounted at ${Drive}:"
        
        # Verify mount
        if (Test-Path $localPath) {
            $driveInfo = Get-PSDrive -Name $Drive
            Write-ColorText "`n✅ TrueNAS Connection Successful!" -Color Green
            Write-Host "   Local Path: $localPath"
            Write-Host "   Remote Path: $remotePath"
            if ($driveInfo.Free) {
                Write-Host "   Available Space: $([math]::Round($driveInfo.Free / 1GB, 2)) GB"
            }
            return $true
        }
    } catch {
        Error "Failed to connect to TrueNAS: $_"
        Write-Host "`nTroubleshooting steps:"
        Write-Host "  1. Verify share name '$Share' exists on TrueNAS"
        Write-Host "  2. Check SMB permissions for your user"
        Write-Host "  3. Try connecting manually: net use ${Drive}: $remotePath"
        return $false
    }
    
    return $false
}

function Disconnect-TrueNAS {
    param(
        [string]$Drive = $DriveLetter
    )
    
    $localPath = "${Drive}:"
    
    Log "🔌 Disconnecting TrueNAS mapping from ${Drive}:..."
    
    try {
        if (Test-Path $localPath) {
            Remove-SmbMapping -LocalPath $localPath -Force
            Success "TrueNAS disconnected from ${Drive}:"
        } else {
            Warn "No mapping found at ${Drive}:"
        }
    } catch {
        Error "Failed to disconnect: $_"
    }
}

function Sync-ToTrueNAS {
    param(
        [string]$SourcePath,
        [string]$Drive = $DriveLetter
    )
    
    $destPath = "${Drive}:\flame-lang-vault"
    
    if (-not (Test-Path "${Drive}:")) {
        Error "TrueNAS not mounted at ${Drive}:"
        Write-Host "Run: .\flamelang_recon_patch.ps1 -Action mount"
        return
    }
    
    Log "📤 Syncing Flame Lang artifacts to TrueNAS..."
    Log "   Source: $SourcePath"
    Log "   Destination: $destPath"
    
    # Create destination if needed
    if (-not (Test-Path $destPath)) {
        New-Item -ItemType Directory -Force -Path $destPath | Out-Null
    }
    
    # Use robocopy for efficient sync
    try {
        $robocopyArgs = @(
            $SourcePath,
            $destPath,
            "/MIR",     # Mirror mode
            "/MT:8",    # Multi-threaded
            "/R:3",     # Retry count
            "/W:5",     # Wait time between retries
            "/NP",      # No progress
            "/NDL"      # No directory list
        )
        
        Log "Running robocopy sync..."
        $result = robocopy @robocopyArgs
        
        Success "Sync completed to TrueNAS: $destPath"
    } catch {
        Error "Sync failed: $_"
    }
}

# ═══════════════════════════════════════════════════════════
# NAVIGATION HELPERS
# ═══════════════════════════════════════════════════════════

function Show-NavigationGuide {
    Write-ColorText "`n📍 STORAGE NAVIGATION GUIDE" -Color Yellow
    Write-Host ""
    Write-Host "Navigate between drives:"
    Write-Host "  cd C:\                         # Go to local C: drive"
    Write-Host "  cd ${DriveLetter}:\            # Go to TrueNAS (if mounted)"
    Write-Host "  cd \$env:USERPROFILE           # Go to user home directory"
    Write-Host ""
    Write-Host "Quick shortcuts:"
    Write-Host "  Set-Location C:\               # PowerShell way to change drives"
    Write-Host "  Push-Location ${DriveLetter}:\ # Save location and switch"
    Write-Host "  Pop-Location                   # Return to saved location"
    Write-Host ""
    Write-Host "View drive contents:"
    Write-Host "  Get-ChildItem                  # List directory (alias: ls, dir)"
    Write-Host "  Get-ChildItem -Recurse -Filter '*.flame'  # Recursive search"
    Write-Host ""
    Success "Use 'Get-Help about_Providers' for more navigation info"
}

# ═══════════════════════════════════════════════════════════
# STATUS DASHBOARD
# ═══════════════════════════════════════════════════════════

function Show-Status {
    Banner
    
    Write-ColorText "📊 FLAME LANG RECON STATUS" -Color Yellow
    Write-Host ""
    
    # Check for existing archives
    $userProfile = if ($env:USERPROFILE) { $env:USERPROFILE } else { $env:HOME }
    if (-not $userProfile) { $userProfile = "." }
    $defaultArchive = Join-Path $userProfile "strategic-khaos-private\flame-lang-archive"
    if (Test-Path $defaultArchive) {
        $archiveFiles = Get-ChildItem -Path $defaultArchive -ErrorAction SilentlyContinue
        Success "✓ Local archive exists: $defaultArchive"
        Write-Host "  Files: $($archiveFiles.Count)"
    } else {
        Warn "○ No local archive found"
    }
    
    # Check TrueNAS connection
    if (Test-Path "${DriveLetter}:") {
        Success "✓ TrueNAS mounted at ${DriveLetter}:"
        try {
            $driveInfo = Get-PSDrive -Name $DriveLetter -ErrorAction SilentlyContinue
            if ($driveInfo -and $driveInfo.Free) {
                Write-Host "  Available: $([math]::Round($driveInfo.Free / 1TB, 2)) TB"
            }
        } catch {}
    } else {
        Warn "○ TrueNAS not mounted (expected at ${DriveLetter}:)"
    }
    
    Write-Host ""
    Write-ColorText "🛠️ AVAILABLE COMMANDS:" -Color Yellow
    Write-Host ""
    Write-Host "  Discovery & Extraction:"
    Write-Host "    -Action discover      # Find Flame Lang files on local drives"
    Write-Host "    -Action extract       # Extract and archive Flame Lang artifacts"
    Write-Host ""
    Write-Host "  TrueNAS Integration:"
    Write-Host "    -Action mount         # Mount TrueNAS storage"
    Write-Host "    -Action unmount       # Disconnect TrueNAS"
    Write-Host "    -Action sync          # Sync archive to TrueNAS"
    Write-Host "    -Action drives        # Show all available drives"
    Write-Host ""
    Write-Host "  Navigation:"
    Write-Host "    -Action nav           # Show navigation guide"
    Write-Host "    -Action status        # Show this status dashboard"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  .\flamelang_recon_patch.ps1 -Action discover -SearchPath 'D:\Projects'"
    Write-Host "  .\flamelang_recon_patch.ps1 -Action mount -TrueNASHost '192.168.1.100'"
    Write-Host "  .\flamelang_recon_patch.ps1 -Action extract -ArchivePath 'E:\FlameLangVault'"
    Write-Host ""
}

# ═══════════════════════════════════════════════════════════
# MAIN EXECUTION
# ═══════════════════════════════════════════════════════════

function Main {
    Banner
    
    switch ($Action.ToLower()) {
        "discover" {
            Find-FlameLangArtifacts -Path $SearchPath
        }
        "extract" {
            $artifacts = Find-FlameLangArtifacts -Path $SearchPath
            if ($artifacts.Count -gt 0) {
                Export-FlameLangArchive -Artifacts $artifacts -DestinationPath $ArchivePath
            }
        }
        "mount" {
            Connect-TrueNAS -Host $TrueNASHost -Share $ShareName -Drive $DriveLetter
        }
        "unmount" {
            Disconnect-TrueNAS -Drive $DriveLetter
        }
        "disconnect" {
            Disconnect-TrueNAS -Drive $DriveLetter
        }
        "sync" {
            $userProfile = if ($env:USERPROFILE) { $env:USERPROFILE } else { $env:HOME }
            if (-not $userProfile) { $userProfile = "." }
            $defaultArchive = Join-Path $userProfile "strategic-khaos-private\flame-lang-archive"
            $syncSource = if ($ArchivePath) { $ArchivePath } else { $defaultArchive }
            Sync-ToTrueNAS -SourcePath $syncSource -Drive $DriveLetter
        }
        "drives" {
            Get-DriveInventory
        }
        "nav" {
            Show-NavigationGuide
        }
        "status" {
            Show-Status
        }
        default {
            Show-Status
        }
    }
}

# Execute main function
Main
