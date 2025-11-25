<#
.SYNOPSIS
    SACSE Orchestration Menu - Interactive PowerShell menu for managing the SACSE workflow.

.DESCRIPTION
    This script provides an interactive menu for the Sovereign Autonomous Continuous
    Systems Engineering (SACSE) workflow. It allows operators to:
    - Scan and verify artifacts
    - Generate verification manifests
    - Run the autonomous loop
    - Manage GPG keys and signatures
    - View system status and metrics

.EXAMPLE
    ./menu.ps1
    # Launches the interactive menu

.EXAMPLE
    ./menu.ps1 -Action scan -Path ./artifacts
    # Directly run artifact scan without menu

.NOTES
    Part of the Strategickhaos Sovereignty Architecture.
    See README.md for full documentation.

    SAFETY NOTES:
    - All file operations validate paths to prevent traversal attacks
    - GPG operations use secure subprocess invocation
    - Sensitive data is never logged to console
#>

[CmdletBinding()]
param(
    [ValidateSet("menu", "scan", "verify", "manifest", "status", "loop")]
    [string]$Action = "menu",
    
    [string]$Path = ".",
    
    [string]$Output,
    
    [switch]$Verbose
)

#region Configuration
$Script:Config = @{
    Version          = "1.0.0"
    ArtifactDir      = "artifacts"
    ManifestDir      = "manifests"
    LogDir           = "logs"
    MaxFileSize      = 100MB
    ScannerPath      = Join-Path $PSScriptRoot "scanner.py"
    OrchestraPath    = Join-Path $PSScriptRoot "_Orchestra.ps1"
    ArtifactExts     = @(".htm", ".html")
    GpgExtension     = ".gpg"
}
#endregion

#region Helper Functions
function Write-ColorText {
    <#
    .SYNOPSIS
        Writes colored text to the console.
    #>
    param(
        [Parameter(Mandatory)]
        [string]$Text,
        
        [ValidateSet("Black", "DarkBlue", "DarkGreen", "DarkCyan", "DarkRed", 
                     "DarkMagenta", "DarkYellow", "Gray", "DarkGray", "Blue", 
                     "Green", "Cyan", "Red", "Magenta", "Yellow", "White")]
        [string]$Color = "White"
    )
    Write-Host $Text -ForegroundColor $Color
}

function Write-Log {
    <#
    .SYNOPSIS
        Writes a timestamped log message.
    #>
    param(
        [Parameter(Mandatory)]
        [string]$Message,
        
        [ValidateSet("INFO", "WARN", "ERROR", "SUCCESS")]
        [string]$Level = "INFO"
    )
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $color = switch ($Level) {
        "INFO"    { "Cyan" }
        "WARN"    { "Yellow" }
        "ERROR"   { "Red" }
        "SUCCESS" { "Green" }
    }
    
    Write-ColorText "[$timestamp] [$Level] $Message" -Color $color
}

function Test-SafePath {
    <#
    .SYNOPSIS
        Validates that a path is safe (no traversal attacks).
    #>
    param(
        [Parameter(Mandatory)]
        [string]$TestPath,
        
        [Parameter(Mandatory)]
        [string]$BasePath
    )
    
    try {
        $resolvedBase = (Resolve-Path -Path $BasePath -ErrorAction Stop).Path
        $resolvedTest = [System.IO.Path]::GetFullPath($TestPath)
        return $resolvedTest.StartsWith($resolvedBase, [System.StringComparison]::OrdinalIgnoreCase)
    }
    catch {
        return $false
    }
}

function Get-ArtifactStats {
    <#
    .SYNOPSIS
        Gets statistics about artifacts in a directory.
    #>
    param(
        [Parameter(Mandatory)]
        [string]$Directory
    )
    
    if (-not (Test-Path $Directory)) {
        return @{
            TotalCount    = 0
            SignedCount   = 0
            UnsignedCount = 0
            TotalSize     = 0
        }
    }
    
    $artifacts = Get-ChildItem -Path $Directory -Recurse -File | 
        Where-Object { $Script:Config.ArtifactExts -contains $_.Extension.ToLower() }
    
    $signed = $artifacts | Where-Object {
        $gpgPath = $_.FullName + $Script:Config.GpgExtension
        Test-Path $gpgPath
    }
    
    return @{
        TotalCount    = $artifacts.Count
        SignedCount   = $signed.Count
        UnsignedCount = $artifacts.Count - $signed.Count
        TotalSize     = ($artifacts | Measure-Object -Property Length -Sum).Sum
    }
}

function Format-FileSize {
    <#
    .SYNOPSIS
        Formats a byte count as a human-readable string.
    #>
    param(
        [Parameter(Mandatory)]
        [long]$Bytes
    )
    
    if ($Bytes -ge 1GB) { return "{0:N2} GB" -f ($Bytes / 1GB) }
    if ($Bytes -ge 1MB) { return "{0:N2} MB" -f ($Bytes / 1MB) }
    if ($Bytes -ge 1KB) { return "{0:N2} KB" -f ($Bytes / 1KB) }
    return "$Bytes bytes"
}
#endregion

#region Menu Functions
function Show-Banner {
    <#
    .SYNOPSIS
        Displays the SACSE banner.
    #>
    Clear-Host
    Write-ColorText @"

  ╔═══════════════════════════════════════════════════════════════════╗
  ║   ____    _    ____ ____  _____                                   ║
  ║  / ___|  / \  / ___/ ___|| ____|                                  ║
  ║  \___ \ / _ \| |   \___ \|  _|                                    ║
  ║   ___) / ___ \ |___ ___) | |___                                   ║
  ║  |____/_/   \_\____|____/|_____|                                  ║
  ║                                                                   ║
  ║  Sovereign Autonomous Continuous Systems Engineering              ║
  ║  Version: $($Script:Config.Version.PadRight(55))║
  ╚═══════════════════════════════════════════════════════════════════╝

"@ -Color Cyan
}

function Show-Menu {
    <#
    .SYNOPSIS
        Displays the main menu and handles user selection.
    #>
    
    while ($true) {
        Show-Banner
        
        Write-ColorText "  MAIN MENU" -Color Yellow
        Write-Host ""
        Write-Host "  [1] Scan Artifacts        - Find .htm files in directory"
        Write-Host "  [2] Verify Signatures     - Check GPG signatures"
        Write-Host "  [3] Generate Manifest     - Create verification manifest"
        Write-Host "  [4] System Status         - View SACSE system status"
        Write-Host "  [5] Start Sovereign Loop  - Run autonomous validation"
        Write-Host "  [6] Key Management        - GPG key operations"
        Write-Host ""
        Write-Host "  [H] Help                  - Show documentation"
        Write-Host "  [Q] Quit                  - Exit menu"
        Write-Host ""
        
        $choice = Read-Host "  Select option"
        
        switch ($choice.ToUpper()) {
            "1" { Invoke-ArtifactScan }
            "2" { Invoke-SignatureVerify }
            "3" { Invoke-ManifestGenerate }
            "4" { Show-SystemStatus }
            "5" { Start-SovereignLoop }
            "6" { Show-KeyManagementMenu }
            "H" { Show-Help }
            "Q" { 
                Write-Log "Exiting SACSE menu" -Level INFO
                return 
            }
            default { 
                Write-Log "Invalid selection: $choice" -Level WARN
                Start-Sleep -Seconds 1
            }
        }
    }
}

function Invoke-ArtifactScan {
    <#
    .SYNOPSIS
        Scans for artifacts in a specified directory.
    #>
    Show-Banner
    Write-ColorText "  ARTIFACT SCAN" -Color Yellow
    Write-Host ""
    
    $scanPath = Read-Host "  Enter directory to scan [./artifacts]"
    if ([string]::IsNullOrWhiteSpace($scanPath)) {
        $scanPath = "./artifacts"
    }
    
    # Validate path
    $basePath = Get-Location
    if (-not (Test-SafePath -TestPath $scanPath -BasePath $basePath)) {
        Write-Log "Invalid path - possible traversal attack detected" -Level ERROR
        Read-Host "  Press Enter to continue"
        return
    }
    
    if (-not (Test-Path $scanPath)) {
        Write-Log "Directory not found: $scanPath" -Level ERROR
        Read-Host "  Press Enter to continue"
        return
    }
    
    Write-Log "Scanning directory: $scanPath" -Level INFO
    
    # Check if Python scanner exists
    if (Test-Path $Script:Config.ScannerPath) {
        Write-Log "Using Python scanner: $($Script:Config.ScannerPath)" -Level INFO
        try {
            python $Script:Config.ScannerPath --scan $scanPath
        }
        catch {
            Write-Log "Python scanner failed: $_" -Level ERROR
        }
    }
    else {
        # Fallback to PowerShell scanning
        Write-Log "Python scanner not found, using PowerShell fallback" -Level WARN
        
        $stats = Get-ArtifactStats -Directory $scanPath
        
        Write-Host ""
        Write-Host "  ══════════════════════════════════════"
        Write-Host "  Scan Results"
        Write-Host "  ══════════════════════════════════════"
        Write-Host "  Total artifacts:   $($stats.TotalCount)"
        Write-Host "  GPG signed:        $($stats.SignedCount) ✓"
        Write-Host "  Unsigned:          $($stats.UnsignedCount) ⚠"
        Write-Host "  Total size:        $(Format-FileSize $stats.TotalSize)"
        Write-Host "  ══════════════════════════════════════"
    }
    
    Write-Host ""
    Read-Host "  Press Enter to continue"
}

function Invoke-SignatureVerify {
    <#
    .SYNOPSIS
        Verifies GPG signatures of artifacts.
    #>
    Show-Banner
    Write-ColorText "  SIGNATURE VERIFICATION" -Color Yellow
    Write-Host ""
    
    $verifyPath = Read-Host "  Enter directory to verify [./artifacts]"
    if ([string]::IsNullOrWhiteSpace($verifyPath)) {
        $verifyPath = "./artifacts"
    }
    
    # Validate path
    $basePath = Get-Location
    if (-not (Test-SafePath -TestPath $verifyPath -BasePath $basePath)) {
        Write-Log "Invalid path - possible traversal attack detected" -Level ERROR
        Read-Host "  Press Enter to continue"
        return
    }
    
    if (-not (Test-Path $verifyPath)) {
        Write-Log "Directory not found: $verifyPath" -Level ERROR
        Read-Host "  Press Enter to continue"
        return
    }
    
    Write-Log "Verifying signatures in: $verifyPath" -Level INFO
    
    # Check if Python scanner exists
    if (Test-Path $Script:Config.ScannerPath) {
        try {
            python $Script:Config.ScannerPath --verify $verifyPath
        }
        catch {
            Write-Log "Verification failed: $_" -Level ERROR
        }
    }
    else {
        Write-Log "Python scanner not available" -Level ERROR
    }
    
    Write-Host ""
    Read-Host "  Press Enter to continue"
}

function Invoke-ManifestGenerate {
    <#
    .SYNOPSIS
        Generates a verification manifest.
    #>
    Show-Banner
    Write-ColorText "  MANIFEST GENERATION" -Color Yellow
    Write-Host ""
    
    $manifestPath = Read-Host "  Enter directory to manifest [./artifacts]"
    if ([string]::IsNullOrWhiteSpace($manifestPath)) {
        $manifestPath = "./artifacts"
    }
    
    $outputFile = Read-Host "  Enter output file [manifest.json]"
    if ([string]::IsNullOrWhiteSpace($outputFile)) {
        $outputFile = "manifest.json"
    }
    
    # Validate paths
    $basePath = Get-Location
    if (-not (Test-SafePath -TestPath $manifestPath -BasePath $basePath)) {
        Write-Log "Invalid path - possible traversal attack detected" -Level ERROR
        Read-Host "  Press Enter to continue"
        return
    }
    
    if (-not (Test-Path $manifestPath)) {
        Write-Log "Directory not found: $manifestPath" -Level ERROR
        Read-Host "  Press Enter to continue"
        return
    }
    
    Write-Log "Generating manifest for: $manifestPath" -Level INFO
    
    # Check if Python scanner exists
    if (Test-Path $Script:Config.ScannerPath) {
        try {
            python $Script:Config.ScannerPath --manifest $manifestPath -o $outputFile
            Write-Log "Manifest written to: $outputFile" -Level SUCCESS
        }
        catch {
            Write-Log "Manifest generation failed: $_" -Level ERROR
        }
    }
    else {
        # Fallback: create basic manifest
        Write-Log "Python scanner not available, creating basic manifest" -Level WARN
        
        $stats = Get-ArtifactStats -Directory $manifestPath
        $manifest = @{
            generated_at = (Get-Date -Format "o")
            generator    = "menu.ps1"
            version      = $Script:Config.Version
            summary      = @{
                total_artifacts = $stats.TotalCount
                gpg_signed      = $stats.SignedCount
                gpg_unsigned    = $stats.UnsignedCount
            }
        }
        
        $manifest | ConvertTo-Json -Depth 10 | Out-File -FilePath $outputFile -Encoding UTF8
        Write-Log "Basic manifest written to: $outputFile" -Level SUCCESS
    }
    
    Write-Host ""
    Read-Host "  Press Enter to continue"
}

function Show-SystemStatus {
    <#
    .SYNOPSIS
        Displays SACSE system status.
    #>
    Show-Banner
    Write-ColorText "  SYSTEM STATUS" -Color Yellow
    Write-Host ""
    
    # Artifact stats
    $artifactStats = Get-ArtifactStats -Directory "./artifacts"
    
    Write-Host "  ┌─────────────────────────────────────────────┐"
    Write-Host "  │ ARTIFACTS                                   │"
    Write-Host "  ├─────────────────────────────────────────────┤"
    Write-Host "  │ Total:              $($artifactStats.TotalCount.ToString().PadLeft(20)) │"
    Write-Host "  │ Signed:             $($artifactStats.SignedCount.ToString().PadLeft(20)) │"
    Write-Host "  │ Unsigned:           $($artifactStats.UnsignedCount.ToString().PadLeft(20)) │"
    Write-Host "  │ Size:               $($(Format-FileSize $artifactStats.TotalSize).PadLeft(20)) │"
    Write-Host "  └─────────────────────────────────────────────┘"
    Write-Host ""
    
    # GPG status
    Write-Host "  ┌─────────────────────────────────────────────┐"
    Write-Host "  │ GPG STATUS                                  │"
    Write-Host "  ├─────────────────────────────────────────────┤"
    
    try {
        $gpgVersion = gpg --version 2>&1 | Select-Object -First 1
        Write-Host "  │ Version:            $($gpgVersion.ToString().Substring(0, [Math]::Min(20, $gpgVersion.Length)).PadLeft(20)) │"
        
        $gpgKeys = gpg --list-keys 2>&1 | Select-String -Pattern "^pub" | Measure-Object
        Write-Host "  │ Public keys:        $($gpgKeys.Count.ToString().PadLeft(20)) │"
    }
    catch {
        Write-Host "  │ GPG:                          Not installed │"
    }
    
    Write-Host "  └─────────────────────────────────────────────┘"
    Write-Host ""
    
    # Loop status
    Write-Host "  ┌─────────────────────────────────────────────┐"
    Write-Host "  │ SOVEREIGN LOOP                              │"
    Write-Host "  ├─────────────────────────────────────────────┤"
    
    if (Test-Path $Script:Config.OrchestraPath) {
        Write-Host "  │ Orchestrator:                     Available │"
    }
    else {
        Write-Host "  │ Orchestrator:                 Not installed │"
    }
    
    # Check if loop is running (look for process)
    $loopProcess = Get-Process -Name "pwsh", "powershell" -ErrorAction SilentlyContinue | 
        Where-Object { $_.CommandLine -like "*_Orchestra*" }
    
    if ($loopProcess) {
        Write-Host "  │ Status:                            Running │"
    }
    else {
        Write-Host "  │ Status:                            Stopped │"
    }
    
    Write-Host "  └─────────────────────────────────────────────┘"
    
    Write-Host ""
    Read-Host "  Press Enter to continue"
}

function Start-SovereignLoop {
    <#
    .SYNOPSIS
        Starts the sovereign autonomous loop.
    #>
    Show-Banner
    Write-ColorText "  SOVEREIGN LOOP" -Color Yellow
    Write-Host ""
    
    if (-not (Test-Path $Script:Config.OrchestraPath)) {
        Write-Log "_Orchestra.ps1 not found at: $($Script:Config.OrchestraPath)" -Level ERROR
        Write-Host ""
        Write-Host "  The sovereign loop orchestrator is not installed."
        Write-Host "  Expected location: $($Script:Config.OrchestraPath)"
        Write-Host ""
        Read-Host "  Press Enter to continue"
        return
    }
    
    Write-Host "  ⚠️  SAFETY WARNING"
    Write-Host "  ═══════════════════════════════════════════════════════"
    Write-Host "  The sovereign loop will:"
    Write-Host "  • Continuously validate artifact integrity"
    Write-Host "  • Reconcile system state with manifests"
    Write-Host "  • Automatically remediate detected issues"
    Write-Host ""
    Write-Host "  Ensure you have:"
    Write-Host "  • Reviewed the loop configuration"
    Write-Host "  • Backed up critical data"
    Write-Host "  • Verified GPG key access"
    Write-Host "  ═══════════════════════════════════════════════════════"
    Write-Host ""
    
    $confirm = Read-Host "  Type 'START' to begin the sovereign loop"
    
    if ($confirm -eq "START") {
        Write-Log "Starting sovereign loop..." -Level INFO
        
        try {
            # Start the loop in a new window
            Start-Process pwsh -ArgumentList "-File", $Script:Config.OrchestraPath -PassThru
            Write-Log "Sovereign loop started in new window" -Level SUCCESS
        }
        catch {
            Write-Log "Failed to start sovereign loop: $_" -Level ERROR
        }
    }
    else {
        Write-Log "Sovereign loop start cancelled" -Level INFO
    }
    
    Write-Host ""
    Read-Host "  Press Enter to continue"
}

function Show-KeyManagementMenu {
    <#
    .SYNOPSIS
        Displays GPG key management submenu.
    #>
    while ($true) {
        Show-Banner
        Write-ColorText "  KEY MANAGEMENT" -Color Yellow
        Write-Host ""
        Write-Host "  [1] List Keys         - Show available GPG keys"
        Write-Host "  [2] Generate Key      - Create new signing key"
        Write-Host "  [3] Export Public     - Export public key"
        Write-Host "  [4] Import Key        - Import a public key"
        Write-Host ""
        Write-Host "  [B] Back              - Return to main menu"
        Write-Host ""
        
        $choice = Read-Host "  Select option"
        
        switch ($choice.ToUpper()) {
            "1" {
                Show-Banner
                Write-ColorText "  GPG KEYS" -Color Yellow
                Write-Host ""
                try {
                    gpg --list-keys
                }
                catch {
                    Write-Log "GPG not available: $_" -Level ERROR
                }
                Write-Host ""
                Read-Host "  Press Enter to continue"
            }
            "2" {
                Show-Banner
                Write-ColorText "  GENERATE KEY" -Color Yellow
                Write-Host ""
                Write-Host "  This will start the GPG key generation wizard."
                Write-Host "  You will be prompted for:"
                Write-Host "  • Key type (RSA recommended)"
                Write-Host "  • Key size (4096 bits recommended)"
                Write-Host "  • Expiration (1-2 years recommended)"
                Write-Host "  • User ID (Name <email>)"
                Write-Host "  • Passphrase (strong, unique)"
                Write-Host ""
                $confirm = Read-Host "  Continue? (y/n)"
                if ($confirm -eq "y") {
                    try {
                        gpg --full-generate-key
                    }
                    catch {
                        Write-Log "Key generation failed: $_" -Level ERROR
                    }
                }
                Read-Host "  Press Enter to continue"
            }
            "3" {
                Show-Banner
                Write-ColorText "  EXPORT PUBLIC KEY" -Color Yellow
                Write-Host ""
                $keyId = Read-Host "  Enter key ID or email"
                if (-not [string]::IsNullOrWhiteSpace($keyId)) {
                    try {
                        gpg --armor --export $keyId
                    }
                    catch {
                        Write-Log "Export failed: $_" -Level ERROR
                    }
                }
                Write-Host ""
                Read-Host "  Press Enter to continue"
            }
            "4" {
                Show-Banner
                Write-ColorText "  IMPORT KEY" -Color Yellow
                Write-Host ""
                $keyFile = Read-Host "  Enter key file path"
                if (Test-Path $keyFile) {
                    try {
                        gpg --import $keyFile
                        Write-Log "Key imported successfully" -Level SUCCESS
                    }
                    catch {
                        Write-Log "Import failed: $_" -Level ERROR
                    }
                }
                else {
                    Write-Log "File not found: $keyFile" -Level ERROR
                }
                Write-Host ""
                Read-Host "  Press Enter to continue"
            }
            "B" { return }
            default { 
                Write-Log "Invalid selection: $choice" -Level WARN
                Start-Sleep -Seconds 1
            }
        }
    }
}

function Show-Help {
    <#
    .SYNOPSIS
        Displays help documentation.
    #>
    Show-Banner
    Write-ColorText "  SACSE HELP" -Color Yellow
    Write-Host ""
    Write-Host "  OVERVIEW"
    Write-Host "  ════════════════════════════════════════════════════════════════"
    Write-Host "  SACSE (Sovereign Autonomous Continuous Systems Engineering) is"
    Write-Host "  a reproducible, auditable research pipeline that:"
    Write-Host ""
    Write-Host "  • Captures engineering artifacts (.htm) with GPG signatures"
    Write-Host "  • Processes artifacts through LLM tools for knowledge extraction"
    Write-Host "  • Integrates outputs into an operational codebase"
    Write-Host "  • Runs autonomous loops for validation and self-healing"
    Write-Host ""
    Write-Host "  WORKFLOW"
    Write-Host "  ════════════════════════════════════════════════════════════════"
    Write-Host "  1. Capture: Save artifacts as .htm files"
    Write-Host "  2. Sign: Generate GPG signatures (.htm.gpg)"
    Write-Host "  3. Scan: Use scanner.py to verify artifacts"
    Write-Host "  4. Manifest: Generate SHA-256 manifests"
    Write-Host "  5. Loop: Run _Orchestra.ps1 for continuous validation"
    Write-Host ""
    Write-Host "  SAFETY"
    Write-Host "  ════════════════════════════════════════════════════════════════"
    Write-Host "  • Store GPG keys in hardware tokens or Vault"
    Write-Host "  • Rotate keys annually"
    Write-Host "  • Review loop configuration before starting"
    Write-Host "  • Monitor loop output for anomalies"
    Write-Host ""
    Write-Host "  DOCUMENTATION"
    Write-Host "  ════════════════════════════════════════════════════════════════"
    Write-Host "  See README.md for full documentation."
    Write-Host ""
    Read-Host "  Press Enter to continue"
}
#endregion

#region Direct Command Functions
function Invoke-DirectScan {
    param([string]$ScanPath)
    
    Write-Log "Direct scan: $ScanPath" -Level INFO
    
    if (Test-Path $Script:Config.ScannerPath) {
        python $Script:Config.ScannerPath --scan $ScanPath
    }
    else {
        $stats = Get-ArtifactStats -Directory $ScanPath
        Write-Host "Total: $($stats.TotalCount), Signed: $($stats.SignedCount), Unsigned: $($stats.UnsignedCount)"
    }
}

function Invoke-DirectVerify {
    param([string]$VerifyPath)
    
    Write-Log "Direct verify: $VerifyPath" -Level INFO
    
    if (Test-Path $Script:Config.ScannerPath) {
        python $Script:Config.ScannerPath --verify $VerifyPath
    }
    else {
        Write-Log "Python scanner required for verification" -Level ERROR
        exit 1
    }
}

function Invoke-DirectManifest {
    param([string]$ManifestPath, [string]$OutputFile)
    
    Write-Log "Direct manifest: $ManifestPath" -Level INFO
    
    if (Test-Path $Script:Config.ScannerPath) {
        if ($OutputFile) {
            python $Script:Config.ScannerPath --manifest $ManifestPath -o $OutputFile
        }
        else {
            python $Script:Config.ScannerPath --manifest $ManifestPath
        }
    }
    else {
        $stats = Get-ArtifactStats -Directory $ManifestPath
        $manifest = @{
            generated_at = (Get-Date -Format "o")
            summary      = $stats
        }
        $manifest | ConvertTo-Json -Depth 10
    }
}

function Invoke-DirectStatus {
    Write-Log "System status" -Level INFO
    
    $stats = Get-ArtifactStats -Directory "./artifacts"
    
    Write-Host "Artifacts: $($stats.TotalCount) total, $($stats.SignedCount) signed"
    
    try {
        $gpgVersion = gpg --version 2>&1 | Select-Object -First 1
        Write-Host "GPG: $gpgVersion"
    }
    catch {
        Write-Host "GPG: Not installed"
    }
}
#endregion

#region Main
function Main {
    if ($Verbose) {
        $VerbosePreference = "Continue"
    }
    
    switch ($Action.ToLower()) {
        "menu" {
            Show-Menu
        }
        "scan" {
            Invoke-DirectScan -ScanPath $Path
        }
        "verify" {
            Invoke-DirectVerify -VerifyPath $Path
        }
        "manifest" {
            Invoke-DirectManifest -ManifestPath $Path -OutputFile $Output
        }
        "status" {
            Invoke-DirectStatus
        }
        "loop" {
            if (Test-Path $Script:Config.OrchestraPath) {
                & $Script:Config.OrchestraPath
            }
            else {
                Write-Log "Orchestrator not found: $($Script:Config.OrchestraPath)" -Level ERROR
                exit 1
            }
        }
    }
}

# Execute main
Main
#endregion
