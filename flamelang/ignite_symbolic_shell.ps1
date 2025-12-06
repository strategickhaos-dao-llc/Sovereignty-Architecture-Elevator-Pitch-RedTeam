# 🔥 ignite_symbolic_shell.ps1: FlameLang Boot Sequence
# Strategickhaos Sovereign Symbolic Language
# FlameLang v1.0 - PowerShell Boot Component
#
# This script initializes the complete FlameLang environment, including:
#   - FlameProfile (sovereign prompt)
#   - DreamOS bootstrap (device-aware)
#   - Glyph map validation
#   - Sovereignty verification
#
# Usage:
#   .\ignite_symbolic_shell.ps1 [-Verbose] [-Force] [-SkipDreamOS]
#   
# Installation (add to PowerShell profile):
#   . C:\Path\To\flamelang\ignite_symbolic_shell.ps1

param(
    [switch]$Verbose,
    [switch]$Force,
    [switch]$SkipDreamOS,
    [switch]$SkipValidation
)

# Get script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Configuration
$FLAMELANG_VERSION = "1.0"
$FLAMELANG_HOME = $ScriptDir

# Color output functions
function Write-Flame {
    param([string]$Message)
    Write-Host $Message -ForegroundColor Magenta
}

function Write-Success {
    param([string]$Message)
    Write-Host "✅ $Message" -ForegroundColor Green
}

function Write-Warning2 {
    param([string]$Message)
    Write-Host "⚠️  $Message" -ForegroundColor Yellow
}

function Write-Error2 {
    param([string]$Message)
    Write-Host "❌ $Message" -ForegroundColor Red
}

function Write-Info {
    param([string]$Message)
    Write-Host "  $Message" -ForegroundColor Cyan
}

# Display boot banner
function Show-BootBanner {
    Write-Host ""
    Write-Flame "╔═══════════════════════════════════════════════════════════════╗"
    Write-Flame "║          🔥 FLAMELANG IGNITION SEQUENCE v$FLAMELANG_VERSION               ║"
    Write-Flame "║              Strategickhaos Sovereign Shell                   ║"
    Write-Flame "╚═══════════════════════════════════════════════════════════════╝"
    Write-Host ""
}

# Validate required files
function Test-RequiredFiles {
    Write-Host "🔍 Validating FlameLang components..." -ForegroundColor Cyan
    
    $requiredFiles = @(
        @{ Name = "FlameProfile.ps1"; Required = $true },
        @{ Name = "FlameAddon_DreamOS.ps1"; Required = $false },
        @{ Name = "glyph_map.json"; Required = $true },
        @{ Name = "oath.lock"; Required = $true },
        @{ Name = "flamelang_parser.py"; Required = $false },
        @{ Name = "flamebearer_protocol.sh"; Required = $false },
        @{ Name = "reflex_shell.sh"; Required = $false }
    )
    
    $allValid = $true
    
    foreach ($file in $requiredFiles) {
        $path = Join-Path $FLAMELANG_HOME $file.Name
        if (Test-Path $path) {
            if ($Verbose) {
                Write-Success "$($file.Name)"
            }
        } else {
            if ($file.Required) {
                Write-Error2 "Missing required: $($file.Name)"
                $allValid = $false
            } else {
                if ($Verbose) {
                    Write-Warning2 "Optional missing: $($file.Name)"
                }
            }
        }
    }
    
    return $allValid
}

# Validate glyph map JSON
function Test-GlyphMap {
    $glyphPath = Join-Path $FLAMELANG_HOME "glyph_map.json"
    
    try {
        $glyphMap = Get-Content $glyphPath -Raw | ConvertFrom-Json
        $glyphCount = ($glyphMap.PSObject.Properties | Where-Object { -not $_.Name.StartsWith("_") }).Count
        Write-Success "Glyph map loaded: $glyphCount glyphs"
        return $true
    } catch {
        Write-Error2 "Invalid glyph_map.json: $_"
        return $false
    }
}

# Load FlameProfile
function Initialize-FlameProfile {
    Write-Host "🔥 Loading FlameProfile..." -ForegroundColor Cyan
    
    $profilePath = Join-Path $FLAMELANG_HOME "FlameProfile.ps1"
    
    if (Test-Path $profilePath) {
        . $profilePath
        Write-Success "FlameProfile loaded"
        return $true
    } else {
        Write-Error2 "FlameProfile not found"
        return $false
    }
}

# Load DreamOS bootstrap
function Initialize-DreamOS {
    if ($SkipDreamOS) {
        if ($Verbose) {
            Write-Info "DreamOS bootstrap skipped (--SkipDreamOS)"
        }
        return $true
    }
    
    Write-Host "🌐 Loading DreamOS bootstrap..." -ForegroundColor Cyan
    
    $dreamOSPath = Join-Path $FLAMELANG_HOME "FlameAddon_DreamOS.ps1"
    
    if (Test-Path $dreamOSPath) {
        & $dreamOSPath -Verbose:$Verbose
        return $true
    } else {
        if ($Verbose) {
            Write-Warning2 "DreamOS bootstrap not found (optional)"
        }
        return $true
    }
}

# Verify sovereignty oath
function Test-Oath {
    Write-Host "🛡️ Verifying sovereignty oath..." -ForegroundColor Cyan
    
    $oathPath = Join-Path $FLAMELANG_HOME "oath.lock"
    
    if (Test-Path $oathPath) {
        $oath = Get-Content $oathPath -Raw
        Write-Success "Oath verified"
        if ($Verbose) {
            Write-Info "📜 $($oath.Trim())"
        }
        return $true
    } else {
        Write-Error2 "Oath lock missing - sovereignty not established"
        return $false
    }
}

# Set environment variables
function Set-FlameLangEnvironment {
    [System.Environment]::SetEnvironmentVariable("FLAMELANG_HOME", $FLAMELANG_HOME, "Process")
    [System.Environment]::SetEnvironmentVariable("FLAMELANG_VERSION", $FLAMELANG_VERSION, "Process")
    [System.Environment]::SetEnvironmentVariable("GLYPH_MAP", (Join-Path $FLAMELANG_HOME "glyph_map.json"), "Process")
    
    if ($Verbose) {
        Write-Info "Environment variables set"
    }
}

# Display final status
function Show-Status {
    Write-Host ""
    Write-Flame "═══════════════════════════════════════════════════════════════"
    Write-Host "  🔥 FlameLang Status" -ForegroundColor Magenta
    Write-Host "     Version: $FLAMELANG_VERSION" -ForegroundColor Cyan
    Write-Host "     Home: $FLAMELANG_HOME" -ForegroundColor Cyan
    Write-Host "     Operator: $([System.Environment]::UserName)" -ForegroundColor Cyan
    Write-Host "     Node: $env:COMPUTERNAME" -ForegroundColor Cyan
    Write-Host "     Time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Cyan
    Write-Flame "═══════════════════════════════════════════════════════════════"
    Write-Host ""
}

# Main ignition sequence
function Start-Ignition {
    Show-BootBanner
    
    # Phase 1: Validation
    if (-not $SkipValidation) {
        if (-not (Test-RequiredFiles)) {
            if (-not $Force) {
                Write-Error2 "Validation failed. Use -Force to continue anyway."
                return $false
            }
            Write-Warning2 "Continuing despite validation errors (-Force)"
        }
        
        if (-not (Test-GlyphMap)) {
            if (-not $Force) {
                Write-Error2 "Glyph map invalid. Use -Force to continue anyway."
                return $false
            }
        }
    } else {
        if ($Verbose) {
            Write-Info "Validation skipped (-SkipValidation)"
        }
    }
    
    # Phase 2: Environment
    Set-FlameLangEnvironment
    
    # Phase 3: Oath verification
    if (-not (Test-Oath)) {
        if (-not $Force) {
            Write-Error2 "Sovereignty not established. Create oath.lock file."
            return $false
        }
    }
    
    # Phase 4: Load profiles
    if (-not (Initialize-FlameProfile)) {
        if (-not $Force) {
            return $false
        }
    }
    
    # Phase 5: DreamOS bootstrap
    Initialize-DreamOS | Out-Null
    
    # Phase 6: Final status
    Show-Status
    
    Write-Host "⚔ Ready for sovereign operations." -ForegroundColor Green
    Write-Host ""
    Write-Flame "🔥 Reignite."
    Write-Host ""
    
    return $true
}

# Execute ignition
$result = Start-Ignition
if (-not $result) {
    Write-Host ""
    Write-Error2 "Ignition failed"
    exit 1
}
