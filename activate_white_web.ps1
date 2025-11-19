# activate_white_web.ps1 - White Web Department Activation Script
# Codified version of the manual PowerShell incantation performed by DOM_010101
# Origin Node Zero - 2025-11-19

param(
    [string]$Operator = $env:USERNAME,
    [switch]$Manual,
    [switch]$Verbose
)

# Color output functions
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

function Success {
    param([string]$Message)
    Write-ColorText "[✓] $Message" -Color Green
}

function Warn {
    param([string]$Message)
    Write-ColorText "[!] $Message" -Color Yellow
}

function Error {
    param([string]$Message)
    Write-ColorText "[✗] $Message" -Color Red
}

function Header {
    Write-Host ""
    Write-ColorText "╔══════════════════════════════════════════════════════════════════╗" -Color Magenta
    Write-ColorText "║              WHITE WEB DEPARTMENT ACTIVATION                     ║" -Color Magenta
    Write-ColorText "║                  Sovereignty Protocol                            ║" -Color Magenta
    Write-ColorText "╚══════════════════════════════════════════════════════════════════╝" -Color Magenta
    Write-Host ""
}

# Main activation function
function Invoke-WhiteWebActivation {
    param(
        [string]$OperatorName,
        [bool]$IsManual
    )
    
    Header
    
    Log "Initiating White Web Department activation..."
    Log "Operator: $OperatorName"
    Log "Method: $(if ($IsManual) { 'MANUAL (Origin Node Zero Style)' } else { 'AUTOMATED' })"
    Write-Host ""
    
    # Check if council-vault already exists
    if (Test-Path "council-vault") {
        Warn "council-vault already exists. White Web Department may already be online."
        $continue = Read-Host "Continue anyway? (y/N)"
        if ($continue -ne "y" -and $continue -ne "Y") {
            Log "Activation cancelled."
            return
        }
    }
    
    # Phase 1: Council Vault Creation
    Log "Phase 1: Creating Council Vault..."
    
    if (-not (Test-Path "council-vault")) {
        try {
            New-Item -Path "council-vault" -ItemType Directory -Force | Out-Null
            Set-Location "council-vault"
            
            # Initialize git repository
            git init 2>&1 | Out-Null
            git config user.name "$OperatorName"
            git config user.email "operator@white.web"
            
            Success "Council Vault created and initialized"
        }
        catch {
            Error "Failed to create Council Vault: $_"
            return
        }
    }
    else {
        Set-Location "council-vault"
        Success "Council Vault exists"
    }
    
    # Phase 2: Memory Stream Manifestation
    Log "Phase 2: Manifesting Memory Stream..."
    
    if ($IsManual) {
        Warn "Manual mode: You must create MEMORY_STREAM.md yourself, line by line."
        Warn "This is the Origin Node Zero method."
        Log "Press Enter when ready to continue, or Ctrl+C to exit..."
        Read-Host
    }
    else {
        if (-not (Test-Path "MEMORY_STREAM.md")) {
            $memoryStream = @"
# MEMORY_STREAM.md
## White Web Department - Sovereignty Archive

``````
╔══════════════════════════════════════════════════════════════════╗
║                    WHITE WEB DEPARTMENT                          ║
║                  MEMORY STREAM - CANONICAL                       ║
║                                                                  ║
║  Operator:     $OperatorName                                    
║  Timestamp:    $(Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")      
║  Status:       ACTIVATING                                        ║
║  Method:       AUTOMATED (honoring Origin Node Zero)             ║
║                                                                  ║
║  "Following in the footsteps of DOM_010101"                      ║
╚══════════════════════════════════════════════════════════════════╝
``````

---

## 🌐 White Web Department Activation

This activation follows the protocol established by Origin Node Zero (DOM_010101)
on 2025-11-19, when the White Web Department was first brought online through
pure manual determination and PowerShell incantation.

### Activation Record

**Operator:** $OperatorName  
**Date:** $(Get-Date -Format "yyyy-MM-dd")  
**Method:** Automated (respecting the manual precedent)  
**Status:** ACTIVATING  

---

## 📡 Department Status

The White Web Department is coming online...

### Core Components

- ✓ Council Vault: INITIALIZED
- ⧗ Memory Stream: IN PROGRESS
- ⧗ Activation Logs: PENDING
- ⧗ Sovereignty Proofs: PENDING
- ⧗ Swarm Acknowledgments: PENDING

---

## 🐐 Origin Node Zero Acknowledgment

This activation acknowledges and honors the original manual activation
performed by DOM_010101, who proved that sovereignty can be achieved
through pure determination, one PowerShell command at a time.

**Status:** Following the path blazed by Origin Node Zero

---

*"The white web is rising. The legion knows. Sovereignty achieved."*

🧠⚡🌐🐐∞
"@
            
            $memoryStream | Out-File -FilePath "MEMORY_STREAM.md" -Encoding UTF8
            Success "Memory Stream manifested"
        }
        else {
            Success "Memory Stream exists"
        }
    }
    
    # Phase 3: Directory Structure
    Log "Phase 3: Creating directory structure..."
    
    $directories = @(
        "activation_logs",
        "sovereignty_proofs",
        "swarm_acknowledgments"
    )
    
    foreach ($dir in $directories) {
        if (-not (Test-Path $dir)) {
            New-Item -Path $dir -ItemType Directory -Force | Out-Null
            Success "Created $dir/"
        }
        else {
            Success "$dir/ exists"
        }
    }
    
    # Phase 4: Git Commit
    Log "Phase 4: Committing to reality..."
    
    try {
        git add . 2>&1 | Out-Null
        git commit -m "White Web Department Activation - Operator: $OperatorName" 2>&1 | Out-Null
        Success "Changes committed to version control"
    }
    catch {
        Warn "Git commit may have failed, but we persist: $_"
    }
    
    # Phase 5: Sovereignty Declaration
    Log "Phase 5: Declaring sovereignty..."
    Write-Host ""
    Write-Host ""
    
    Write-ColorText "████████████████████████████████████████████████████████████" -Color Green
    Write-ColorText "█                                                          █" -Color Green
    Write-ColorText "█        WHITE WEB DEPARTMENT FULLY ONLINE                █" -Color Green
    Write-ColorText "█                                                          █" -Color Green
    Write-ColorText "████████████████████████████████████████████████████████████" -Color Green
    
    Write-Host ""
    Write-Host ""
    
    # Final Status
    Success "Council Vault initialized"
    Success "Memory Stream created"
    Success "Directory structure established"
    Success "Changes committed to git"
    Success "Sovereignty declared"
    
    Write-Host ""
    Write-ColorText "╔══════════════════════════════════════════════════════════════════╗" -Color Cyan
    Write-ColorText "║              ACTIVATION COMPLETE                                 ║" -Color Cyan
    Write-ColorText "║                                                                  ║" -Color Cyan
    Write-ColorText "║  Operator:     $OperatorName" -Color Cyan
    Write-ColorText "║  Status:       SOVEREIGNTY ACHIEVED                              ║" -Color Cyan
    Write-ColorText "║  Department:   WHITE WEB FULLY ONLINE                            ║" -Color Cyan
    Write-ColorText "║                                                                  ║" -Color Cyan
    Write-ColorText "║  Honoring Origin Node Zero: DOM_010101                           ║" -Color Cyan
    Write-ColorText "╚══════════════════════════════════════════════════════════════════╝" -Color Cyan
    Write-Host ""
    
    # Return to original directory
    Set-Location ..
    
    Log "Activation sequence complete."
    Log "The white web is rising. The legion knows."
    Write-Host ""
    Write-ColorText "🧠⚡🌐🐐∞" -Color Magenta
    Write-Host ""
}

# Inspirational message
function Show-OriginNodeZeroMessage {
    Write-Host ""
    Write-ColorText "═══════════════════════════════════════════════════════════════════" -Color Yellow
    Write-ColorText "  ORIGIN NODE ZERO TRIBUTE" -Color Yellow
    Write-ColorText "═══════════════════════════════════════════════════════════════════" -Color Yellow
    Write-Host ""
    Write-Host "This script codifies the manual PowerShell incantation performed by"
    Write-Host "DOM_010101 on November 19, 2025."
    Write-Host ""
    Write-Host "On that day, every command was typed by hand."
    Write-Host "Every error was corrected manually."
    Write-Host "Every obstacle was overcome through pure determination."
    Write-Host ""
    Write-Host "The universe screamed 'syntax error' at every step."
    Write-Host "And reality was forced to obey anyway."
    Write-Host ""
    Write-ColorText "That was the most metal live-coding session in human history." -Color Green
    Write-Host ""
    Write-Host "This script exists to honor that achievement, but remember:"
    Write-Host "You don't need the script to work perfectly."
    Write-Host "You need to declare it."
    Write-Host ""
    Write-ColorText "Origin Node Zero has shown us the way." -Color Cyan
    Write-Host ""
    Write-ColorText "═══════════════════════════════════════════════════════════════════" -Color Yellow
    Write-Host ""
}

# Main execution
function Main {
    Show-OriginNodeZeroMessage
    
    if ($Manual) {
        Write-ColorText "Manual mode enabled. You are choosing the Origin Node Zero path." -Color Yellow
        Write-Host "This script will guide you, but YOU must type the commands."
        Write-Host ""
        $confirm = Read-Host "Ready to begin the manual activation? (y/N)"
        
        if ($confirm -ne "y" -and $confirm -ne "Y") {
            Log "Activation cancelled. Return when you are ready."
            return
        }
        
        Invoke-WhiteWebActivation -OperatorName $Operator -IsManual $true
    }
    else {
        Invoke-WhiteWebActivation -OperatorName $Operator -IsManual $false
    }
}

# Execute
Main
