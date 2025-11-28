# setup-tunnel.ps1 - Cloudflare Tunnel Quick Setup for Windows
# Strategic Khaos - Zero to Global in 12 Seconds

param(
    [int]$Port = 3000,
    [string]$Host = "localhost",
    [switch]$Help
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

function Show-Help {
    Write-ColorText "🌐 Cloudflare Tunnel Quick Setup" -Color Magenta
    Write-Host ""
    Write-Host "Usage: ./setup-tunnel.ps1 [-Port <port>] [-Host <host>] [-Help]"
    Write-Host ""
    Write-Host "Parameters:"
    Write-Host "  -Port    Port number to tunnel (default: 3000)"
    Write-Host "  -Host    Host address (default: localhost)"
    Write-Host "  -Help    Show this help message"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  ./setup-tunnel.ps1                    # Tunnel localhost:3000"
    Write-Host "  ./setup-tunnel.ps1 -Port 8080         # Tunnel localhost:8080"
    Write-Host "  ./setup-tunnel.ps1 -Port 3000 -Host 127.0.0.1"
    Write-Host ""
    exit 0
}

function Test-LocalService {
    param([string]$Url)
    
    Log "🔍 Checking if local service is running at $Url..."
    
    try {
        $response = Invoke-WebRequest -Uri $Url -Method Head -TimeoutSec 5 -ErrorAction Stop
        Success "✓ Local service is running (Status: $($response.StatusCode))"
        return $true
    }
    catch {
        Warn "⚠ Local service at $Url is not responding"
        Warn "   Make sure your application is running before starting the tunnel"
        Write-Host ""
        $continue = Read-Host "Continue anyway? (y/N)"
        if ($continue -ne "y" -and $continue -ne "Y") {
            exit 1
        }
        return $false
    }
}

function Test-Cloudflared {
    Log "🔍 Checking if cloudflared is installed..."
    
    try {
        $version = cloudflared --version 2>$null
        if ($LASTEXITCODE -eq 0) {
            Success "✓ cloudflared is installed: $version"
            return $true
        }
    }
    catch {
        return $false
    }
    
    return $false
}

function Install-Cloudflared {
    Log "📥 Installing cloudflared via winget..."
    
    # Check if winget is available
    if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
        Error "winget is not available. Please install App Installer from Microsoft Store."
        Write-Host "Alternative installation methods:"
        Write-Host "1. Download from: https://github.com/cloudflare/cloudflared/releases"
        Write-Host "2. Install manually and add to PATH"
        exit 1
    }
    
    try {
        Write-Host ""
        Log "Running: winget install cloudflare.cloudflared"
        winget install cloudflare.cloudflared --accept-package-agreements --accept-source-agreements
        
        if ($LASTEXITCODE -eq 0) {
            Success "✓ cloudflared installed successfully"
            
            # Refresh environment PATH
            $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
            
            # Verify installation
            Start-Sleep -Seconds 2
            if (Test-Cloudflared) {
                return $true
            }
            else {
                Warn "cloudflared was installed but not found in PATH"
                Warn "You may need to restart PowerShell or manually add cloudflared to PATH"
                Write-Host ""
                Write-Host "Please close this PowerShell window and open a new one, then run this script again."
                exit 1
            }
        }
        else {
            Error "Failed to install cloudflared"
            exit 1
        }
    }
    catch {
        Error "Installation failed: $_"
        exit 1
    }
}

function Start-Tunnel {
    param(
        [string]$Url
    )
    
    Log "🚀 Starting Cloudflare Tunnel to $Url..."
    Write-Host ""
    Write-ColorText "════════════════════════════════════════════════════════════════" -Color Yellow
    Write-ColorText "  CLOUDFLARE TUNNEL STARTING" -Color Yellow
    Write-ColorText "  Local URL:  $Url" -Color Cyan
    Write-ColorText "  Public URL: Will be displayed below..." -Color Cyan
    Write-ColorText "════════════════════════════════════════════════════════════════" -Color Yellow
    Write-Host ""
    Write-ColorText "Press Ctrl+C to stop the tunnel" -Color Gray
    Write-Host ""
    
    try {
        # Start cloudflared tunnel
        cloudflared tunnel --url $Url
    }
    catch {
        Error "Tunnel failed to start: $_"
        exit 1
    }
}

function Show-Banner {
    Write-Host ""
    Write-ColorText "╔══════════════════════════════════════════════════════════════╗" -Color Magenta
    Write-ColorText "║                                                              ║" -Color Magenta
    Write-ColorText "║        🌐 CLOUDFLARE TUNNEL QUICK SETUP 🌐                   ║" -Color Magenta
    Write-ColorText "║                                                              ║" -Color Magenta
    Write-ColorText "║        Strategic Khaos - Zero to Global in 12 Seconds       ║" -Color Magenta
    Write-ColorText "║                                                              ║" -Color Magenta
    Write-ColorText "╚══════════════════════════════════════════════════════════════╝" -Color Magenta
    Write-Host ""
}

function Main {
    if ($Help) {
        Show-Help
    }
    
    Show-Banner
    
    # Build URL
    $url = "http://${Host}:${Port}"
    
    Log "Target: $url"
    Write-Host ""
    
    # Check if local service is running
    Test-LocalService -Url $url
    Write-Host ""
    
    # Check if cloudflared is installed
    if (-not (Test-Cloudflared)) {
        Warn "cloudflared is not installed"
        Write-Host ""
        $install = Read-Host "Install cloudflared now? (Y/n)"
        if ($install -eq "n" -or $install -eq "N") {
            Error "cloudflared is required. Exiting."
            exit 1
        }
        
        Write-Host ""
        Install-Cloudflared
    }
    
    Write-Host ""
    
    # Start tunnel
    Start-Tunnel -Url $url
}

# Run main function
Main
