# Sovereign Mesh Bootstrap - PowerShell Wrapper
# Automatically detects and launches the bootstrap in the correct environment
# This wrapper ensures bash scripts run properly on Windows

param(
    [switch]$Force,
    [switch]$WSL,
    [switch]$GitBash,
    [switch]$Help
)

# Color output functions
function Write-Status { 
    Write-Host "[STATUS] " -ForegroundColor Blue -NoNewline
    Write-Host $args[0]
}

function Write-Success { 
    Write-Host "[✓] " -ForegroundColor Green -NoNewline
    Write-Host $args[0]
}

function Write-Warning { 
    Write-Host "[⚠] " -ForegroundColor Yellow -NoNewline
    Write-Host $args[0]
}

function Write-Error-Custom { 
    Write-Host "[✗] " -ForegroundColor Red -NoNewline
    Write-Host $args[0]
}

function Write-Banner {
    Write-Host ""
    Write-Host "┌─────────────────────────────────────────────────────────────────┐" -ForegroundColor Cyan
    Write-Host "│      SOVEREIGN MESH BOOTSTRAP - POWERSHELL LAUNCHER             │" -ForegroundColor Cyan
    Write-Host "│             Windows Environment Handler                         │" -ForegroundColor Cyan
    Write-Host "└─────────────────────────────────────────────────────────────────┘" -ForegroundColor Cyan
    Write-Host ""
}

function Show-Help {
    Write-Host ""
    Write-Host "USAGE:" -ForegroundColor Cyan
    Write-Host "  .\sovereign-mesh-bootstrap.ps1 [-WSL] [-GitBash] [-Force] [-Help]"
    Write-Host ""
    Write-Host "OPTIONS:" -ForegroundColor Cyan
    Write-Host "  -WSL       Force execution in WSL"
    Write-Host "  -GitBash   Force execution in Git Bash"
    Write-Host "  -Force     Skip confirmation prompts"
    Write-Host "  -Help      Show this help message"
    Write-Host ""
    Write-Host "EXAMPLES:" -ForegroundColor Cyan
    Write-Host "  .\sovereign-mesh-bootstrap.ps1"
    Write-Host "  .\sovereign-mesh-bootstrap.ps1 -WSL"
    Write-Host "  .\sovereign-mesh-bootstrap.ps1 -GitBash -Force"
    Write-Host ""
}

# Check if bash script exists
function Test-BashScript {
    if (-not (Test-Path ".\sovereign-mesh-bootstrap.sh")) {
        Write-Error-Custom "sovereign-mesh-bootstrap.sh not found in current directory!"
        Write-Status "Please run this script from the repository root."
        exit 1
    }
}

# Check for WSL
function Test-WSL {
    try {
        $wslCheck = wsl --list --quiet 2>&1
        if ($LASTEXITCODE -eq 0) {
            return $true
        }
    } catch {
        return $false
    }
    return $false
}

# Find Git Bash
function Find-GitBash {
    $possiblePaths = @(
        "C:\Program Files\Git\bin\bash.exe",
        "C:\Program Files (x86)\Git\bin\bash.exe",
        "$env:ProgramFiles\Git\bin\bash.exe",
        "${env:ProgramFiles(x86)}\Git\bin\bash.exe",
        "$env:LOCALAPPDATA\Programs\Git\bin\bash.exe"
    )
    
    foreach ($path in $possiblePaths) {
        if (Test-Path $path) {
            return $path
        }
    }
    
    return $null
}

# Install GitHub CLI helper
function Show-InstallGHCLI {
    Write-Status "GitHub CLI Installation Options:"
    Write-Host ""
    Write-Host "  1. Via winget (recommended):" -ForegroundColor Yellow
    Write-Host "     winget install GitHub.cli"
    Write-Host ""
    Write-Host "  2. Via Chocolatey:" -ForegroundColor Yellow
    Write-Host "     choco install gh"
    Write-Host ""
    Write-Host "  3. Download installer:" -ForegroundColor Yellow
    Write-Host "     https://github.com/cli/cli/releases/latest"
    Write-Host ""
    
    if (-not $Force) {
        $installNow = Read-Host "Install gh CLI via winget now? (y/N)"
        if ($installNow -eq 'y' -or $installNow -eq 'Y') {
            Write-Status "Installing GitHub CLI..."
            winget install GitHub.cli
            Write-Success "GitHub CLI installed. You may need to restart your terminal."
        }
    }
}

# Main execution
function Main {
    Write-Banner
    
    if ($Help) {
        Show-Help
        exit 0
    }
    
    # Verify bash script exists
    Test-BashScript
    
    Write-Status "Detecting Windows environment..."
    
    # Check for GitHub CLI
    $ghExists = Get-Command gh -ErrorAction SilentlyContinue
    if (-not $ghExists) {
        Write-Warning "GitHub CLI (gh) not found in PATH"
        Show-InstallGHCLI
    } else {
        $ghVersion = (gh --version | Select-Object -First 1).Split()[2]
        Write-Success "GitHub CLI found: version $ghVersion"
    }
    
    # Determine execution method
    $executionMethod = $null
    
    if ($WSL) {
        $executionMethod = "wsl"
    } elseif ($GitBash) {
        $executionMethod = "gitbash"
    } else {
        # Auto-detect best option
        if (Test-WSL) {
            Write-Success "WSL detected and available"
            $executionMethod = "wsl"
        } else {
            $gitBashPath = Find-GitBash
            if ($gitBashPath) {
                Write-Success "Git Bash detected at: $gitBashPath"
                $executionMethod = "gitbash"
            }
        }
    }
    
    # Execute based on method
    switch ($executionMethod) {
        "wsl" {
            Write-Status "Launching bootstrap in WSL..."
            Write-Host ""
            
            # Convert Windows path to WSL path
            $currentDir = (Get-Location).Path
            $wslPath = $currentDir -replace '\\', '/' -replace ':', ''
            $wslPath = "/mnt/$($wslPath.Substring(0,1).ToLower())$($wslPath.Substring(1))"
            
            Write-Status "Executing in WSL..."
            wsl bash -c "cd '$wslPath' && bash ./sovereign-mesh-bootstrap.sh"
            
            if ($LASTEXITCODE -eq 0) {
                Write-Success "Bootstrap completed successfully!"
            } else {
                Write-Error-Custom "Bootstrap encountered errors (exit code: $LASTEXITCODE)"
                exit $LASTEXITCODE
            }
        }
        
        "gitbash" {
            $gitBashPath = Find-GitBash
            if (-not $gitBashPath) {
                Write-Error-Custom "Git Bash not found!"
                Write-Status "Please install Git for Windows: https://git-scm.com/download/win"
                exit 1
            }
            
            Write-Status "Launching bootstrap in Git Bash..."
            Write-Status "Git Bash location: $gitBashPath"
            Write-Host ""
            
            & $gitBashPath -c "./sovereign-mesh-bootstrap.sh"
            
            if ($LASTEXITCODE -eq 0) {
                Write-Success "Bootstrap completed successfully!"
            } else {
                Write-Error-Custom "Bootstrap encountered errors (exit code: $LASTEXITCODE)"
                exit $LASTEXITCODE
            }
        }
        
        default {
            Write-Error-Custom "No suitable bash environment found!"
            Write-Host ""
            Write-Status "Please install one of the following:"
            Write-Host "  1. WSL (Windows Subsystem for Linux):" -ForegroundColor Yellow
            Write-Host "     wsl --install"
            Write-Host ""
            Write-Host "  2. Git for Windows (includes Git Bash):" -ForegroundColor Yellow
            Write-Host "     https://git-scm.com/download/win"
            Write-Host ""
            Write-Host "After installation, run this script again." -ForegroundColor Yellow
            exit 1
        }
    }
    
    Write-Host ""
    Write-Status "Bootstrap process complete!"
    Write-Host ""
    Write-Status "Next steps:"
    Write-Host "  1. Edit .env with your credentials"
    Write-Host "  2. Review the configuration in .sovereign-mesh/"
    Write-Host "  3. Check service status: docker compose ps"
    Write-Host ""
}

# Entry point
try {
    Main
} catch {
    Write-Error-Custom "Unexpected error: $_"
    Write-Host $_.ScriptStackTrace
    exit 1
}
