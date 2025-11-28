# setup-windows-env.ps1 - Windows Environment Setup Script
# Strategic Khaos Sovereignty Architecture
# This script sets up GPG, Git signing, and development tools

param(
    [switch]$SkipGPG,
    [switch]$SkipTimestamping,
    [switch]$SkipNetworkDiag,
    [switch]$Verbose
)

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

# Color utility functions
function Write-Status {
    param([string]$Message, [string]$Type = "Info")
    $timestamp = Get-Date -Format "HH:mm:ss"
    switch ($Type) {
        "Success" { Write-Host "[$timestamp] ✓ $Message" -ForegroundColor Green }
        "Warning" { Write-Host "[$timestamp] ⚠ $Message" -ForegroundColor Yellow }
        "Error"   { Write-Host "[$timestamp] ✗ $Message" -ForegroundColor Red }
        default   { Write-Host "[$timestamp] ℹ $Message" -ForegroundColor Cyan }
    }
}

function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# ============================================================================
# SECTION 1: GPG Setup and Configuration
# ============================================================================

function Initialize-GPGEnvironment {
    if ($SkipGPG) {
        Write-Status "Skipping GPG setup" "Warning"
        return
    }
    
    Write-Status "Setting up GPG environment..."
    
    # Common GPG installation paths on Windows
    $gpgPaths = @(
        "C:\Program Files (x86)\GnuPG\bin",
        "C:\Program Files\GnuPG\bin",
        "$env:ProgramFiles\Git\usr\bin",
        "$env:LOCALAPPDATA\Programs\Git\usr\bin"
    )
    
    $gpgExe = $null
    foreach ($path in $gpgPaths) {
        $testPath = Join-Path $path "gpg.exe"
        if (Test-Path $testPath) {
            $gpgExe = $testPath
            Write-Status "Found GPG at: $path" "Success"
            
            # Add to PATH if not already present
            if ($env:Path -notlike "*$path*") {
                $env:Path = "$path;$env:Path"
                Write-Status "Added GPG to session PATH"
            }
            break
        }
    }
    
    if (-not $gpgExe) {
        Write-Status "GPG not found. Install from: https://gnupg.org/download/" "Warning"
        return
    }
    
    # List existing keys
    try {
        $keys = & $gpgExe --list-secret-keys --keyid-format LONG 2>&1
        if ($keys) {
            Write-Status "Existing GPG keys found:" "Success"
            Write-Host $keys -ForegroundColor Gray
        } else {
            Write-Status "No GPG keys found. Generate one with: gpg --full-generate-key" "Warning"
        }
    } catch {
        Write-Status "Error listing GPG keys: $_" "Error"
    }
}

# ============================================================================
# SECTION 2: Git Configuration and Signing
# ============================================================================

function Initialize-GitConfiguration {
    Write-Status "Configuring Git signing..."
    
    # Check if Git is available
    $gitPath = Get-Command git -ErrorAction SilentlyContinue
    if (-not $gitPath) {
        Write-Status "Git not found in PATH" "Error"
        return
    }
    
    # Get current remote configuration
    $currentOrigin = & git remote get-url origin 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Status "Current origin: $currentOrigin"
    } else {
        Write-Status "No origin remote configured" "Warning"
    }
    
    # Check commit signing configuration
    $signKey = & git config --get user.signingkey 2>&1
    if ($signKey) {
        Write-Status "Signing key configured: $signKey" "Success"
    } else {
        Write-Status "No signing key configured. Set with: git config --global user.signingkey <KEY_ID>" "Warning"
    }
    
    # Verify GPG program configuration
    $gpgProgram = & git config --get gpg.program 2>&1
    if ($gpgProgram) {
        Write-Status "GPG program: $gpgProgram"
    } else {
        Write-Status "GPG program not configured. May need: git config --global gpg.program 'C:\Program Files (x86)\GnuPG\bin\gpg.exe'" "Warning"
    }
}

# ============================================================================
# SECTION 3: OpenTimestamps Setup
# ============================================================================

function Initialize-TimestampingTools {
    if ($SkipTimestamping) {
        Write-Status "Skipping timestamping setup" "Warning"
        return
    }
    
    Write-Status "Setting up OpenTimestamps..."
    
    # Check for Python (required for ots-cli)
    $python = Get-Command python -ErrorAction SilentlyContinue
    if (-not $python) {
        Write-Status "Python not found. Install Python 3.x for OpenTimestamps client" "Warning"
        return
    }
    
    # Check if opentimestamps-client is installed
    try {
        $otsVersion = & python -c "import opentimestamps; print(opentimestamps.__version__)" 2>&1
        Write-Status "OpenTimestamps client installed: $otsVersion" "Success"
    } catch {
        Write-Status "OpenTimestamps not installed. Install with: pip install opentimestamps-client" "Warning"
    }
}

# ============================================================================
# SECTION 4: Network Diagnostics
# ============================================================================

function Invoke-NetworkDiagnostics {
    if ($SkipNetworkDiag) {
        Write-Status "Skipping network diagnostics" "Warning"
        return
    }
    
    Write-Status "Running network diagnostics..."
    
    # Test DNS resolution
    $testDomains = @("github.com", "api.github.com")
    foreach ($domain in $testDomains) {
        try {
            $resolved = [System.Net.Dns]::GetHostAddresses($domain)
            Write-Status "DNS OK: $domain -> $($resolved[0])" "Success"
        } catch {
            Write-Status "DNS failed for $domain" "Error"
        }
    }
    
    # Test HTTPS connectivity
    $testUrls = @(
        "https://api.github.com/zen",
        "https://raw.githubusercontent.com/octocat/Hello-World/master/README"
    )
    foreach ($url in $testUrls) {
        try {
            $response = Invoke-WebRequest -Uri $url -Method Head -TimeoutSec 10 -UseBasicParsing
            Write-Status "HTTPS OK: $url (Status: $($response.StatusCode))" "Success"
        } catch {
            Write-Status "HTTPS failed: $url - $_" "Warning"
        }
    }
}

# ============================================================================
# SECTION 5: PATH Cleanup
# ============================================================================

function Optimize-EnvironmentPath {
    Write-Status "Cleaning duplicate PATH entries..."
    
    $currentPath = $env:Path -split ';'
    $uniquePaths = $currentPath | Select-Object -Unique | Where-Object { $_ -ne '' }
    $cleanPath = $uniquePaths -join ';'
    
    $originalCount = $currentPath.Count
    $cleanCount = $uniquePaths.Count
    $removed = $originalCount - $cleanCount
    
    if ($removed -gt 0) {
        Write-Status "Removed $removed duplicate PATH entries" "Success"
        Write-Status "To make permanent, run: [Environment]::SetEnvironmentVariable('Path', `$cleanPath, 'User')" "Warning"
    } else {
        Write-Status "PATH already optimized" "Success"
    }
    
    return $cleanPath
}

# ============================================================================
# SECTION 6: Document Conversion Tools
# ============================================================================

function Test-DocumentTools {
    Write-Status "Checking document conversion tools..."
    
    # Check for Pandoc
    $pandoc = Get-Command pandoc -ErrorAction SilentlyContinue
    if ($pandoc) {
        $version = & pandoc --version | Select-Object -First 1
        Write-Status "Pandoc: $version" "Success"
    } else {
        Write-Status "Pandoc not found. Install from: https://pandoc.org/installing.html" "Warning"
    }
    
    # Check for PDF engines
    $pdfEngines = @("pdflatex", "xelatex", "weasyprint")
    foreach ($engine in $pdfEngines) {
        $found = Get-Command $engine -ErrorAction SilentlyContinue
        if ($found) {
            Write-Status "PDF engine available: $engine" "Success"
        }
    }
}

# ============================================================================
# Main Execution
# ============================================================================

function Main {
    Write-Host ""
    Write-Host "╔══════════════════════════════════════════════════════════════════╗" -ForegroundColor Magenta
    Write-Host "║    Strategic Khaos - Windows Environment Setup                   ║" -ForegroundColor Magenta
    Write-Host "╚══════════════════════════════════════════════════════════════════╝" -ForegroundColor Magenta
    Write-Host ""
    
    # Check for admin rights (only warn, don't require)
    if (-not (Test-Administrator)) {
        Write-Status "Running without admin rights. Some operations may require elevation." "Warning"
    }
    
    # Run setup tasks
    Initialize-GPGEnvironment
    Write-Host ""
    
    Initialize-GitConfiguration
    Write-Host ""
    
    Initialize-TimestampingTools
    Write-Host ""
    
    Invoke-NetworkDiagnostics
    Write-Host ""
    
    $cleanPath = Optimize-EnvironmentPath
    Write-Host ""
    
    Test-DocumentTools
    Write-Host ""
    
    Write-Host "╔══════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║    Environment setup complete!                                   ║" -ForegroundColor Green
    Write-Host "╚══════════════════════════════════════════════════════════════════╝" -ForegroundColor Green
    Write-Host ""
    Write-Status "Next steps:" "Info"
    Write-Host "  1. Ensure GPG key is generated and configured for Git signing"
    Write-Host "  2. Set up repository remotes correctly"
    Write-Host "  3. Install OpenTimestamps client if document timestamping needed"
    Write-Host "  4. Review PATH environment for any remaining issues"
    Write-Host ""
}

# Execute main function
Main
