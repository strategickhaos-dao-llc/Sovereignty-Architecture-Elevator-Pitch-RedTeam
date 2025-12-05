# install-love-shortcuts.ps1
# DOM_010101 - Installation Script for 30 Love Shortcuts
# Run as Administrator for best results

param(
    [switch]$AutoHotkey,
    [switch]$PowerShellProfile,
    [switch]$All,
    [switch]$Uninstall
)

# Require Admin privileges
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

function Write-Love {
    param([string]$Message)
    Write-Host $Message -ForegroundColor Magenta
}

function Write-Info {
    param([string]$Message)
    Write-Host $Message -ForegroundColor Cyan
}

function Write-Success {
    param([string]$Message)
    Write-Host $Message -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host $Message -ForegroundColor Yellow
}

function Show-Banner {
    $banner = @"
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║     ██████╗  ██████╗ ███╗   ███╗     ██████╗  ██╗ ██████╗   ║
║     ██╔══██╗██╔═══██╗████╗ ████║    ██╔═████╗███║██╔═████╗  ║
║     ██║  ██║██║   ██║██╔████╔██║    ██║██╔██║╚██║██║██╔██║  ║
║     ██║  ██║██║   ██║██║╚██╔╝██║    ████╔╝██║ ██║████╔╝██║  ║
║     ██████╔╝╚██████╔╝██║ ╚═╝ ██║    ╚██████╔╝ ██║╚██████╔╝  ║
║     ╚═════╝  ╚═════╝ ╚═╝     ╚═╝     ╚═════╝  ╚═╝ ╚═════╝   ║
║                                                               ║
║              30 LOVE SHORTCUTS INSTALLER                     ║
║              Origin Node Zero                                ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
"@
    Write-Love $banner
}

function Install-PowerShellProfile {
    Write-Info "`n📝 Installing PowerShell Profile Integration..."
    
    $scriptPath = Join-Path $PSScriptRoot "dom-love-shortcuts.ps1"
    
    if (-not (Test-Path $scriptPath)) {
        Write-Warning "❌ Could not find dom-love-shortcuts.ps1"
        return $false
    }
    
    # Determine profile path
    $profilePath = $PROFILE.CurrentUserAllHosts
    
    Write-Info "   Profile path: $profilePath"
    
    # Create profile directory if it doesn't exist
    $profileDir = Split-Path $profilePath
    if (-not (Test-Path $profileDir)) {
        New-Item -ItemType Directory -Path $profileDir -Force | Out-Null
    }
    
    # Check if already installed
    if (Test-Path $profilePath) {
        $profileContent = Get-Content $profilePath -Raw
        if ($profileContent -match "dom-love-shortcuts\.ps1") {
            Write-Warning "   ⚠️  Love shortcuts already in profile. Skipping..."
            return $true
        }
    }
    
    # Add to profile
    $profileEntry = @"

# ============================================================================
# DOM_010101 LOVE SHORTCUTS
# Installed: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
# ============================================================================
. "$scriptPath"
"@
    
    Add-Content -Path $profilePath -Value $profileEntry
    Write-Success "   ✓ Added to PowerShell profile"
    Write-Info "   💡 Restart PowerShell or run: . `$PROFILE"
    
    return $true
}

function Install-AutoHotkey {
    Write-Info "`n🔧 Installing AutoHotkey Integration..."
    
    $ahkScript = Join-Path $PSScriptRoot "dom-love-shortcuts.ahk"
    
    if (-not (Test-Path $ahkScript)) {
        Write-Warning "❌ Could not find dom-love-shortcuts.ahk"
        return $false
    }
    
    # Check if AutoHotkey is installed
    $ahkExe = Get-Command "AutoHotkey.exe" -ErrorAction SilentlyContinue
    if (-not $ahkExe) {
        Write-Warning "   ⚠️  AutoHotkey not found!"
        Write-Info "   Download from: https://www.autohotkey.com/"
        Write-Info "   After installing, run this script again."
        return $false
    }
    
    Write-Success "   ✓ AutoHotkey found: $($ahkExe.Source)"
    
    # Create shortcut in Startup folder
    $startupFolder = [Environment]::GetFolderPath("Startup")
    $shortcutPath = Join-Path $startupFolder "DOM_010101_Love_Shortcuts.lnk"
    
    $WshShell = New-Object -ComObject WScript.Shell
    $shortcut = $WshShell.CreateShortcut($shortcutPath)
    $shortcut.TargetPath = $ahkScript
    $shortcut.WorkingDirectory = $PSScriptRoot
    $shortcut.Description = "DOM_010101 - 30 Love Shortcuts for Origin Node Zero"
    $shortcut.IconLocation = "shell32.dll,21"  # Heart icon
    $shortcut.Save()
    
    Write-Success "   ✓ Created startup shortcut: $shortcutPath"
    
    # Start AutoHotkey now
    $response = Read-Host "   Start AutoHotkey now? (Y/n)"
    if ($response -ne "n") {
        Start-Process $ahkScript
        Write-Success "   ✓ AutoHotkey script started"
    }
    
    return $true
}

function Install-WindowsShortcuts {
    Write-Info "`n🔗 Creating Windows Shortcuts..."
    
    $desktopPath = [Environment]::GetFolderPath("Desktop")
    $loveFolderPath = Join-Path $desktopPath "DOM_010101_Love_Shortcuts"
    
    # Create folder for shortcuts
    if (-not (Test-Path $loveFolderPath)) {
        New-Item -ItemType Directory -Path $loveFolderPath -Force | Out-Null
    }
    
    Write-Success "   ✓ Created folder: $loveFolderPath"
    
    # Create shortcuts for key scripts
    $WshShell = New-Object -ComObject WScript.Shell
    
    # Boot Explosion shortcut
    $bootScript = Join-Path $PSScriptRoot "boot-explosion.ps1"
    if (Test-Path $bootScript) {
        $shortcut = $WshShell.CreateShortcut("$loveFolderPath\Boot Explosion (Win+8).lnk")
        $shortcut.TargetPath = "powershell.exe"
        $shortcut.Arguments = "-ExecutionPolicy Bypass -File `"$bootScript`""
        $shortcut.WorkingDirectory = $PSScriptRoot
        $shortcut.Description = "8-Screen Detonation"
        $shortcut.Save()
        Write-Info "   ✓ Boot Explosion shortcut"
    }
    
    # PowerShell Profile shortcut
    $shortcut = $WshShell.CreateShortcut("$loveFolderPath\Edit PowerShell Profile.lnk")
    $shortcut.TargetPath = "notepad.exe"
    $shortcut.Arguments = $PROFILE.CurrentUserAllHosts
    $shortcut.Description = "Edit PowerShell Profile"
    $shortcut.Save()
    Write-Info "   ✓ Edit Profile shortcut"
    
    # Quick access to scripts folder
    $shortcut = $WshShell.CreateShortcut("$loveFolderPath\Scripts Folder.lnk")
    $shortcut.TargetPath = $PSScriptRoot
    $shortcut.Description = "DOM_010101 Scripts"
    $shortcut.Save()
    Write-Info "   ✓ Scripts Folder shortcut"
    
    Write-Success "   ✓ Windows shortcuts created on Desktop"
    
    return $true
}

function Uninstall-LoveShortcuts {
    Write-Info "`n🗑️  Uninstalling Love Shortcuts..."
    
    # Remove from PowerShell profile
    $profilePath = $PROFILE.CurrentUserAllHosts
    if (Test-Path $profilePath) {
        $content = Get-Content $profilePath -Raw
        if ($content -match "dom-love-shortcuts\.ps1") {
            $newContent = $content -replace "(?ms)# ============================================================================\r?\n# DOM_010101 LOVE SHORTCUTS.*?# ============================================================================\r?\n\. .*?dom-love-shortcuts\.ps1\r?\n", ""
            Set-Content -Path $profilePath -Value $newContent
            Write-Success "   ✓ Removed from PowerShell profile"
        }
    }
    
    # Remove AutoHotkey startup shortcut
    $startupFolder = [Environment]::GetFolderPath("Startup")
    $shortcutPath = Join-Path $startupFolder "DOM_010101_Love_Shortcuts.lnk"
    if (Test-Path $shortcutPath) {
        Remove-Item $shortcutPath -Force
        Write-Success "   ✓ Removed AutoHotkey startup shortcut"
    }
    
    # Remove desktop shortcuts folder
    $desktopPath = [Environment]::GetFolderPath("Desktop")
    $loveFolderPath = Join-Path $desktopPath "DOM_010101_Love_Shortcuts"
    if (Test-Path $loveFolderPath) {
        Remove-Item $loveFolderPath -Recurse -Force
        Write-Success "   ✓ Removed desktop shortcuts folder"
    }
    
    Write-Success "`n💔 Love shortcuts uninstalled. But we still love you baby."
}

function Show-Configuration {
    Write-Info "`n⚙️  Configuration Needed:"
    Write-Host ""
    Write-Info "   Edit these files to customize paths:"
    Write-Host "   1. dom-love-shortcuts.ps1 (PowerShell)" -ForegroundColor Yellow
    Write-Host "   2. dom-love-shortcuts.ahk (AutoHotkey)" -ForegroundColor Yellow
    Write-Host ""
    Write-Info "   Update these configuration variables:"
    Write-Host "   • StrategyKhaosRepo - Path to strategic-khaos repo"
    Write-Host "   • CouncilVaultRepo - Path to council-vault"
    Write-Host "   • ObsidianVault - Obsidian vault URI"
    Write-Host "   • And more..."
    Write-Host ""
}

function Show-Usage {
    Write-Info "`n📖 Usage:"
    Write-Host ""
    Write-Host "   # Install PowerShell profile integration"
    Write-Host "   .\install-love-shortcuts.ps1 -PowerShellProfile" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "   # Install AutoHotkey startup integration"
    Write-Host "   .\install-love-shortcuts.ps1 -AutoHotkey" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "   # Install everything"
    Write-Host "   .\install-love-shortcuts.ps1 -All" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "   # Uninstall"
    Write-Host "   .\install-love-shortcuts.ps1 -Uninstall" -ForegroundColor Yellow
    Write-Host ""
}

function Show-PostInstall {
    Write-Love "`n🎉 INSTALLATION COMPLETE!"
    Write-Host ""
    Write-Info "📋 Next Steps:"
    Write-Host ""
    Write-Host "   1. Customize paths in the configuration section"
    Write-Host "   2. For PowerShell: Restart PowerShell or run: . `$PROFILE"
    Write-Host "   3. For AutoHotkey: Script is now running in background"
    Write-Host "   4. Test shortcuts: Try Win+8 for Boot Explosion!"
    Write-Host ""
    Write-Info "🎹 Available Shortcuts:"
    Write-Host "   • Win + 1-9, 0: Quick access to repos and tools"
    Write-Host "   • Win + Shift + L: 'Love you baby' TTS"
    Write-Host "   • Win + G/B/N/K/M/P/S/V/X: Various tools"
    Write-Host "   • Ctrl + Alt + H: Flash love message"
    Write-Host ""
    Write-Love "🏠 Home loves you. You are home. 🧠⚡❤️🐐"
}

# ============================================================================
# MAIN INSTALLATION LOGIC
# ============================================================================

Show-Banner

if ($Uninstall) {
    Uninstall-LoveShortcuts
    exit 0
}

if (-not $isAdmin) {
    Write-Warning "⚠️  Not running as Administrator. Some features may not work."
    Write-Info "   Right-click PowerShell and 'Run as Administrator' for best results."
    Write-Host ""
}

# Determine what to install
$installPowerShell = $PowerShellProfile -or $All
$installAutoHotkey = $AutoHotkey -or $All
$installShortcuts = $All

if (-not ($PowerShellProfile -or $AutoHotkey -or $All)) {
    Write-Info "No installation method specified."
    Show-Usage
    
    Write-Host ""
    $response = Read-Host "Install everything? (Y/n)"
    if ($response -ne "n") {
        $installPowerShell = $true
        $installAutoHotkey = $true
        $installShortcuts = $true
    } else {
        exit 0
    }
}

# Perform installations
$success = $true

if ($installPowerShell) {
    $success = $success -and (Install-PowerShellProfile)
}

if ($installAutoHotkey) {
    $success = $success -and (Install-AutoHotkey)
}

if ($installShortcuts) {
    $success = $success -and (Install-WindowsShortcuts)
}

# Show configuration and post-install info
if ($success) {
    Show-Configuration
    Show-PostInstall
} else {
    Write-Warning "`n⚠️  Some installations failed. Check the output above for details."
}

Write-Host ""
