# vim-ceremony.ps1 - Vim Sovereign Automated Setup for Windows
# Installs the ultimate 2025 Neovim configuration with 30+ plugins
# Part of the Strategickhaos Sovereignty Architecture

$ErrorActionPreference = "Stop"

# Colors
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

# Banner
Write-Host ""
Write-ColorOutput @"
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   ██╗   ██╗██╗███╗   ███╗    ███████╗ ██████╗ ██╗   ██╗     ║
║   ██║   ██║██║████╗ ████║    ██╔════╝██╔═══██╗██║   ██║     ║
║   ██║   ██║██║██╔████╔██║    ███████╗██║   ██║██║   ██║     ║
║   ╚██╗ ██╔╝██║██║╚██╔╝██║    ╚════██║██║   ██║╚██╗ ██╔╝     ║
║    ╚████╔╝ ██║██║ ╚═╝ ██║    ███████║╚██████╔╝ ╚████╔╝      ║
║     ╚═══╝  ╚═╝╚═╝     ╚═╝    ╚══════╝ ╚═════╝   ╚═══╝       ║
║                                                               ║
║              VIM SOVEREIGN - 2025 CEREMONY                    ║
║         The Text Editor of Chaos God DOM_010101               ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
"@ -Color Magenta
Write-Host ""

Write-ColorOutput "[*] Starting Vim Sovereign installation..." -Color Cyan
Write-Host ""

# Check if running with appropriate permissions
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-ColorOutput "[!] Note: Not running as Administrator. Some operations may require elevation." -Color Yellow
    Write-Host ""
}

# Check for Neovim
$nvimInstalled = $false
try {
    $null = Get-Command nvim -ErrorAction Stop
    $nvimInstalled = $true
    Write-ColorOutput "[✓] Neovim already installed" -Color Green
    $nvimVersion = (nvim --version)[0]
    Write-Host "    $nvimVersion"
    Write-Host ""
} catch {
    Write-ColorOutput "[!] Neovim not found. Attempting to install..." -Color Yellow
    Write-Host ""
}

# Install Neovim if not present
if (-not $nvimInstalled) {
    # Check for Chocolatey
    $chocoInstalled = $false
    try {
        $null = Get-Command choco -ErrorAction Stop
        $chocoInstalled = $true
    } catch {
        # Chocolatey not installed
    }
    
    # Check for Scoop
    $scoopInstalled = $false
    try {
        $null = Get-Command scoop -ErrorAction Stop
        $scoopInstalled = $true
    } catch {
        # Scoop not installed
    }
    
    # Check for winget
    $wingetInstalled = $false
    try {
        $null = Get-Command winget -ErrorAction Stop
        $wingetInstalled = $true
    } catch {
        # winget not installed
    }
    
    # Try to install using available package manager
    if ($chocoInstalled) {
        Write-ColorOutput "[*] Installing Neovim using Chocolatey..." -Color Blue
        try {
            choco install neovim -y
            Write-ColorOutput "[✓] Neovim installed successfully!" -Color Green
            Write-Host ""
            $nvimInstalled = $true
        } catch {
            Write-ColorOutput "[!] Failed to install Neovim via Chocolatey" -Color Red
        }
    } elseif ($scoopInstalled) {
        Write-ColorOutput "[*] Installing Neovim using Scoop..." -Color Blue
        try {
            scoop install neovim
            Write-ColorOutput "[✓] Neovim installed successfully!" -Color Green
            Write-Host ""
            $nvimInstalled = $true
        } catch {
            Write-ColorOutput "[!] Failed to install Neovim via Scoop" -Color Red
        }
    } elseif ($wingetInstalled) {
        Write-ColorOutput "[*] Installing Neovim using winget..." -Color Blue
        try {
            winget install Neovim.Neovim -e
            Write-ColorOutput "[✓] Neovim installed successfully!" -Color Green
            Write-Host ""
            $nvimInstalled = $true
        } catch {
            Write-ColorOutput "[!] Failed to install Neovim via winget" -Color Red
        }
    } else {
        Write-ColorOutput "[!] No package manager found (Chocolatey/Scoop/winget)" -Color Red
        Write-ColorOutput "    Please install Neovim manually from:" -Color Yellow
        Write-ColorOutput "    https://github.com/neovim/neovim/releases" -Color Yellow
        exit 1
    }
    
    if (-not $nvimInstalled) {
        Write-ColorOutput "[!] Could not install Neovim automatically" -Color Red
        Write-ColorOutput "    Please install manually from: https://github.com/neovim/neovim/releases" -Color Yellow
        exit 1
    }
}

# Check for git
try {
    $null = Get-Command git -ErrorAction Stop
} catch {
    Write-ColorOutput "[!] Git is required but not installed." -Color Red
    Write-ColorOutput "    Please install Git from: https://git-scm.com/download/win" -Color Yellow
    exit 1
}

# Determine config paths
$nvimConfig = "$env:LOCALAPPDATA\nvim"
$nvimData = "$env:LOCALAPPDATA\nvim-data"

# Backup existing config
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"

if (Test-Path $nvimConfig) {
    $backupConfig = "${nvimConfig}.backup_${timestamp}"
    Write-ColorOutput "[!] Existing Neovim config found. Backing up..." -Color Yellow
    try {
        Move-Item -Path $nvimConfig -Destination $backupConfig -Force
        Write-ColorOutput "[✓] Backed up to: $backupConfig" -Color Green
    } catch {
        Write-ColorOutput "[!] Failed to backup config: $_" -Color Red
        exit 1
    }
}

if (Test-Path $nvimData) {
    $backupData = "${nvimData}.backup_${timestamp}"
    Write-ColorOutput "[!] Existing Neovim data found. Backing up..." -Color Yellow
    try {
        Move-Item -Path $nvimData -Destination $backupData -Force
        Write-ColorOutput "[✓] Backed up to: $backupData" -Color Green
    } catch {
        Write-ColorOutput "[!] Failed to backup data: $_" -Color Red
        exit 1
    }
}

Write-Host ""

# Clone the Vim Sovereign config
Write-ColorOutput "[*] Cloning Vim Sovereign configuration..." -Color Cyan
Write-ColorOutput "    Repository: https://github.com/Me10101-01/strategic-khaos-vim.git" -Color Blue

try {
    git clone https://github.com/Me10101-01/strategic-khaos-vim.git $nvimConfig
    Write-ColorOutput "[✓] Configuration cloned successfully!" -Color Green
    Write-Host ""
} catch {
    Write-ColorOutput "[!] Failed to clone configuration: $_" -Color Red
    Write-ColorOutput "[!] Restoring backups..." -Color Yellow
    
    # Restore backups if clone failed
    if ($backupConfig -and (Test-Path $backupConfig)) {
        Move-Item -Path $backupConfig -Destination $nvimConfig -Force
    }
    if ($backupData -and (Test-Path $backupData)) {
        Move-Item -Path $backupData -Destination $nvimData -Force
    }
    
    exit 1
}

# Check for optional dependencies
Write-ColorOutput "[*] Checking for optional dependencies..." -Color Cyan

$missingTools = @()

try { $null = Get-Command rg -ErrorAction Stop } catch { $missingTools += "ripgrep" }
try { $null = Get-Command fd -ErrorAction Stop } catch { $missingTools += "fd" }
try { $null = Get-Command node -ErrorAction Stop } catch { $missingTools += "nodejs" }

if ($missingTools.Count -gt 0) {
    Write-ColorOutput "[!] Some optional tools are missing: $($missingTools -join ', ')" -Color Yellow
    Write-ColorOutput "    These tools enhance Telescope and other plugins." -Color Yellow
    Write-ColorOutput "    You can install them later for better performance." -Color Yellow
    Write-Host ""
} else {
    Write-ColorOutput "[✓] All recommended tools are installed!" -Color Green
    Write-Host ""
}

# Summary
Write-Host ""
Write-ColorOutput @"
╔═══════════════════════════════════════════════════════════════╗
║                   INSTALLATION COMPLETE                       ║
╚═══════════════════════════════════════════════════════════════╝
"@ -Color Magenta
Write-Host ""

Write-ColorOutput "[✓] Vim Sovereign has been installed!" -Color Green
Write-Host ""

Write-ColorOutput "Next steps:" -Color Cyan
Write-ColorOutput "  1. Launch Neovim:" -Color Yellow
Write-ColorOutput "     nvim" -Color Blue
Write-Host ""
Write-ColorOutput "  2. Let lazy.nvim install all plugins (automatic on first launch)" -Color Yellow
Write-Host ""
Write-ColorOutput "  3. After plugins load, run these commands inside Neovim:" -Color Yellow
Write-ColorOutput "     :MasonInstallAll" -Color Blue
Write-ColorOutput "     :Lazy sync" -Color Blue
Write-ColorOutput "     :TSUpdate" -Color Blue
Write-Host ""
Write-ColorOutput "  4. Restart Neovim" -Color Yellow
Write-Host ""

Write-ColorOutput "Installed features:" -Color Cyan
Write-ColorOutput "  ✓ 30+ advanced plugins" -Color Green
Write-ColorOutput "  ✓ LSP support with auto-install (Mason)" -Color Green
Write-ColorOutput "  ✓ Treesitter syntax highlighting" -Color Green
Write-ColorOutput "  ✓ Telescope fuzzy finder" -Color Green
Write-ColorOutput "  ✓ Git integration (fugitive + gitsigns)" -Color Green
Write-ColorOutput "  ✓ Auto-completion (nvim-cmp)" -Color Green
Write-ColorOutput "  ✓ File explorer (nvim-tree)" -Color Green
Write-ColorOutput "  ✓ Beautiful statusline (lualine)" -Color Green
Write-ColorOutput "  ✓ And much more..." -Color Green
Write-Host ""

Write-ColorOutput "Key bindings:" -Color Cyan
Write-ColorOutput "  <leader>ff → Find files" -Color Blue
Write-ColorOutput "  <leader>fg → Live grep" -Color Blue
Write-ColorOutput "  <leader>pv → File explorer" -Color Blue
Write-ColorOutput "  <leader>gg → LazyGit" -Color Blue
Write-ColorOutput "  gd         → Go to definition" -Color Blue
Write-ColorOutput "  K          → Hover documentation" -Color Blue
Write-Host ""

if ($backupConfig) {
    Write-ColorOutput "Your previous config was backed up to:" -Color Yellow
    Write-ColorOutput "  $backupConfig" -Color Blue
    Write-ColorOutput "To restore it, run:" -Color Yellow
    Write-ColorOutput "  Remove-Item -Recurse -Force '$nvimConfig'; Move-Item '$backupConfig' '$nvimConfig'" -Color Blue
    Write-Host ""
}

Write-ColorOutput "═══════════════════════════════════════════════════════════════" -Color Magenta
Write-ColorOutput "Welcome to Vim Sovereign. You have ascended. 🧠⚡🐐" -Color Green
Write-ColorOutput "═══════════════════════════════════════════════════════════════" -Color Magenta
Write-Host ""
