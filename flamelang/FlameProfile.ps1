# 🔥 FlameProfile.ps1: Symbolic Prompt Overlay
# Strategickhaos Sovereign Symbolic Language
# FlameLang v1.0 - PowerShell Component
#
# Installation:
#   Add to your PowerShell profile:
#   . C:\Path\To\flamelang\FlameProfile.ps1

# Set window title to indicate FlameLang environment
$host.UI.RawUI.WindowTitle = "🔥 Strategickhaos FlameLang CLI"

# Define the sovereign prompt function
function global:prompt {
    $user = [System.Environment]::UserName
    $machine = $env:COMPUTERNAME
    $time = (Get-Date).ToString("HH:mm:ss")
    $location = (Get-Location).Path
    
    # Truncate path if too long
    if ($location.Length -gt 40) {
        $location = "..." + $location.Substring($location.Length - 37)
    }
    
    # Build sovereign prompt: [time] ⚔ user@machine ▶ path>
    return "[$time] ⚔ $user@$machine ▶ $location> "
}

# FlameLang glyph aliases
Set-Alias -Name flame -Value Get-FlameLangStatus -Scope Global -ErrorAction SilentlyContinue

function global:Get-FlameLangStatus {
    Write-Host "`n🔥 FlameLang Status" -ForegroundColor Magenta
    Write-Host "  Version: v1.0" -ForegroundColor Cyan
    Write-Host "  Operator: $([System.Environment]::UserName)" -ForegroundColor Cyan
    Write-Host "  Node: $env:COMPUTERNAME" -ForegroundColor Cyan
    Write-Host "  Time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Cyan
    Write-Host "`n⚔ Ready for sovereign operations.`n" -ForegroundColor Green
}

# Sovereignty verification function
function global:Test-Sovereignty {
    Write-Host "`n🛡️ Sovereignty Check" -ForegroundColor Yellow
    
    # Check oath.lock exists
    $oathPath = Join-Path $PSScriptRoot "oath.lock"
    if (Test-Path $oathPath) {
        Write-Host "  ✅ Oath Lock: Present" -ForegroundColor Green
        $oathContent = Get-Content $oathPath -Raw
        Write-Host "  📜 Vow: $($oathContent.Trim())" -ForegroundColor Cyan
    } else {
        Write-Host "  ❌ Oath Lock: Missing" -ForegroundColor Red
    }
    
    # Check glyph map
    $glyphPath = Join-Path $PSScriptRoot "glyph_map.json"
    if (Test-Path $glyphPath) {
        Write-Host "  ✅ Glyph Map: Loaded" -ForegroundColor Green
    } else {
        Write-Host "  ❌ Glyph Map: Missing" -ForegroundColor Red
    }
    
    Write-Host ""
}

# Execute glyph command
function global:Invoke-Glyph {
    param(
        [Parameter(Mandatory=$true)]
        [string]$GlyphCommand
    )
    
    $glyphPath = Join-Path $PSScriptRoot "glyph_map.json"
    if (-not (Test-Path $glyphPath)) {
        Write-Host "❌ Glyph map not found at: $glyphPath" -ForegroundColor Red
        return
    }
    
    $glyphMap = Get-Content $glyphPath | ConvertFrom-Json
    
    if ($glyphMap.PSObject.Properties.Name -contains $GlyphCommand) {
        $script = $glyphMap.$GlyphCommand
        Write-Host "🔥 Executing glyph: $GlyphCommand" -ForegroundColor Magenta
        Write-Host "  → Target: $script" -ForegroundColor Cyan
        
        if ($script.EndsWith(".ps1")) {
            & $script
        } elseif ($script.EndsWith(".py")) {
            # Use Python Launcher on Windows, python3 otherwise
            $pythonCmd = if (Get-Command py -ErrorAction SilentlyContinue) { "py" } else { "python3" }
            & $pythonCmd $script
        } else {
            & $script
        }
        
        Write-Host "`n✨ Neural Sync complete. Resonance achieved." -ForegroundColor Green
    } else {
        Write-Host "❌ Unknown glyph: $GlyphCommand" -ForegroundColor Red
        Write-Host "  Available glyphs:" -ForegroundColor Yellow
        $glyphMap.PSObject.Properties.Name | ForEach-Object { Write-Host "    $_" -ForegroundColor Cyan }
    }
}

# Display startup message
Write-Host "`n🔥 FlameLang Interface Loaded. Reignite." -ForegroundColor Magenta
Write-Host "  Type 'flame' for status, 'Test-Sovereignty' for vow verification`n" -ForegroundColor DarkGray
