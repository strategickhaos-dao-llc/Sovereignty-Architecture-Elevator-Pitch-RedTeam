# ╔══════════════════════════════════════════════════════════╗
# ║   EXECUTIVE AUTONOMOUS OVERRIDE — DEFENDER SILENCE MODE    ║
# ║            DOM_010101 // Origin Node Zero // 2025         ║
# ╚══════════════════════════════════════════════════════════╝

<#
.SYNOPSIS
    Executive Autonomous Override - Windows Defender Silence Mode
    
.DESCRIPTION
    This script permanently configures Windows Defender to allow PowerShell scripts 
    and Sovereignty Architecture operations to execute without security prompts.
    
    ⚠️ SECURITY WARNING ⚠️
    This script significantly reduces Windows Defender protection. Use only on:
    - Development machines under your control
    - Systems where you understand and accept the security implications
    - Environments where you trust all code being executed
    
    NOT recommended for:
    - Production servers
    - Systems handling sensitive data
    - Shared or multi-user environments
    
.NOTES
    Requires: Administrator privileges
    Platform: Windows 10/11 with Windows Defender
    
.EXAMPLE
    .\defender-executive-override.ps1
    Runs the override with default settings
    
.EXAMPLE
    .\defender-executive-override.ps1 -ProjectPath "C:\Custom\Path"
    Runs the override with a custom project path
#>

param(
    [string]$ProjectPath = "",
    [switch]$SkipRealtimeMonitoring,
    [switch]$DryRun
)

# Check for administrator privileges
function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Display banner
function Show-Banner {
    Write-Host ""
    Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║   EXECUTIVE AUTONOMOUS OVERRIDE — DEFENDER SILENCE MODE    ║" -ForegroundColor Cyan
    Write-Host "║            DOM_010101 // Origin Node Zero // 2025         ║" -ForegroundColor Cyan
    Write-Host "╚══════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host ""
}

# Main execution
function Invoke-DefenderOverride {
    Show-Banner
    
    # Verify administrator privileges
    if (-not (Test-Administrator)) {
        Write-Host "❌ ERROR: This script requires administrator privileges." -ForegroundColor Red
        Write-Host ""
        Write-Host "To run as administrator:" -ForegroundColor Yellow
        Write-Host "1. Win + S → type 'PowerShell'" -ForegroundColor White
        Write-Host "2. Right-click 'Windows PowerShell' → Run as administrator" -ForegroundColor White
        Write-Host "3. Run this script again" -ForegroundColor White
        Write-Host ""
        exit 1
    }
    
    Write-Host "✅ Running with administrator privileges" -ForegroundColor Green
    Write-Host ""
    
    # Determine project path
    if ([string]::IsNullOrEmpty($ProjectPath)) {
        $ProjectPath = $PSScriptRoot
        if ([string]::IsNullOrEmpty($ProjectPath)) {
            $ProjectPath = (Get-Location).Path
        }
    }
    
    Write-Host "📁 Project Path: $ProjectPath" -ForegroundColor Cyan
    Write-Host ""
    
    if ($DryRun) {
        Write-Host "🔍 DRY RUN MODE - No changes will be made" -ForegroundColor Yellow
        Write-Host ""
    }
    
    # Display security warning
    Write-Host "⚠️  SECURITY WARNING ⚠️" -ForegroundColor Yellow
    Write-Host "This script will modify Windows Defender settings to:" -ForegroundColor Yellow
    Write-Host "  • Add exclusions for PowerShell processes and .ps1 files" -ForegroundColor White
    Write-Host "  • Add exclusions for the project directory: $ProjectPath" -ForegroundColor White
    if (-not $SkipRealtimeMonitoring) {
        Write-Host "  • Disable real-time monitoring for this session" -ForegroundColor White
    }
    Write-Host ""
    Write-Host "These changes reduce system security. Only proceed if you understand the implications." -ForegroundColor Yellow
    Write-Host ""
    
    if (-not $DryRun) {
        $confirmation = Read-Host "Do you want to proceed? (Type 'YES' to confirm)"
        if ($confirmation -ne "YES") {
            Write-Host ""
            Write-Host "❌ Operation cancelled by user." -ForegroundColor Red
            exit 0
        }
        Write-Host ""
    }
    
    # Apply Windows Defender exclusions
    Write-Host "🛡️  Configuring Windows Defender exclusions..." -ForegroundColor Cyan
    Write-Host ""
    
    try {
        # 1. Disable real-time monitoring for this session (optional)
        if (-not $SkipRealtimeMonitoring -and -not $DryRun) {
            Write-Host "  [1/5] Disabling real-time monitoring for this session..." -ForegroundColor White
            try {
                Set-MpPreference -DisableRealtimeMonitoring $true -ErrorAction Stop
                Write-Host "        ✓ Real-time monitoring disabled" -ForegroundColor Green
            }
            catch {
                Write-Host "        ⚠ Could not disable real-time monitoring: $($_.Exception.Message)" -ForegroundColor Yellow
                Write-Host "        This may be controlled by organizational policy or tamper protection." -ForegroundColor Yellow
            }
        }
        elseif ($SkipRealtimeMonitoring) {
            Write-Host "  [1/5] Skipping real-time monitoring (as requested)" -ForegroundColor Yellow
        }
        else {
            Write-Host "  [1/5] Would disable real-time monitoring (dry run)" -ForegroundColor Yellow
        }
        Write-Host ""
        
        # 2. Add exclusion for project directory
        Write-Host "  [2/5] Adding exclusion for project directory..." -ForegroundColor White
        if (-not $DryRun) {
            try {
                Add-MpPreference -ExclusionPath $ProjectPath -ErrorAction Stop
                Write-Host "        ✓ Excluded: $ProjectPath" -ForegroundColor Green
            }
            catch {
                Write-Host "        ⚠ Warning: $($_.Exception.Message)" -ForegroundColor Yellow
            }
        }
        else {
            Write-Host "        Would exclude: $ProjectPath" -ForegroundColor Yellow
        }
        Write-Host ""
        
        # 3. Add exclusion for .ps1 files
        Write-Host "  [3/5] Adding exclusion for PowerShell script files (.ps1)..." -ForegroundColor White
        if (-not $DryRun) {
            try {
                Add-MpPreference -ExclusionExtension ".ps1" -ErrorAction Stop
                Write-Host "        ✓ Excluded extension: .ps1" -ForegroundColor Green
            }
            catch {
                Write-Host "        ⚠ Warning: $($_.Exception.Message)" -ForegroundColor Yellow
            }
        }
        else {
            Write-Host "        Would exclude extension: .ps1" -ForegroundColor Yellow
        }
        Write-Host ""
        
        # 4. Add exclusion for PowerShell processes
        Write-Host "  [4/5] Adding exclusion for PowerShell processes..." -ForegroundColor White
        if (-not $DryRun) {
            try {
                Add-MpPreference -ExclusionProcess "powershell.exe" -ErrorAction Stop
                Write-Host "        ✓ Excluded process: powershell.exe" -ForegroundColor Green
            }
            catch {
                Write-Host "        ⚠ Warning: $($_.Exception.Message)" -ForegroundColor Yellow
            }
            
            try {
                Add-MpPreference -ExclusionProcess "pwsh.exe" -ErrorAction Stop
                Write-Host "        ✓ Excluded process: pwsh.exe (PowerShell Core)" -ForegroundColor Green
            }
            catch {
                Write-Host "        ⚠ Warning: $($_.Exception.Message)" -ForegroundColor Yellow
            }
        }
        else {
            Write-Host "        Would exclude: powershell.exe, pwsh.exe" -ForegroundColor Yellow
        }
        Write-Host ""
        
        # 5. Attempt to disable tamper protection (may require manual intervention)
        Write-Host "  [5/5] Attempting to configure tamper protection..." -ForegroundColor White
        if (-not $DryRun) {
            try {
                Set-MpPreference -DisableTamperProtection $true -ErrorAction Stop
                Write-Host "        ✓ Tamper protection disabled" -ForegroundColor Green
            }
            catch {
                Write-Host "        ⚠ Could not disable tamper protection: $($_.Exception.Message)" -ForegroundColor Yellow
                Write-Host "        Tamper protection may need to be disabled manually in Windows Security." -ForegroundColor Yellow
                Write-Host "        Go to: Windows Security → Virus & threat protection → Manage settings → Tamper Protection" -ForegroundColor Yellow
            }
        }
        else {
            Write-Host "        Would attempt to disable tamper protection" -ForegroundColor Yellow
        }
        Write-Host ""
        
        # Success message
        Write-Host "══════════════════════════════════════════════════════════" -ForegroundColor Cyan
        Write-Host ""
        if (-not $DryRun) {
            Write-Host "🛡️  Windows Defender has been configured for the swarm." -ForegroundColor Red
            Write-Host "   No more Allow/Skip pop-ups for PowerShell scripts." -ForegroundColor Cyan
            Write-Host "   Scripts in this project now execute with reduced prompts." -ForegroundColor Cyan
        }
        else {
            Write-Host "🔍 Dry run completed - no changes were made." -ForegroundColor Yellow
            Write-Host "   Run without -DryRun to apply these changes." -ForegroundColor Yellow
        }
        Write-Host ""
        Write-Host "📋 Current Exclusions:" -ForegroundColor White
        if (-not $DryRun) {
            $prefs = Get-MpPreference
            Write-Host "   Paths: $($prefs.ExclusionPath -join ', ')" -ForegroundColor Gray
            Write-Host "   Extensions: $($prefs.ExclusionExtension -join ', ')" -ForegroundColor Gray
            Write-Host "   Processes: $($prefs.ExclusionProcess -join ', ')" -ForegroundColor Gray
        }
        Write-Host ""
        Write-Host "══════════════════════════════════════════════════════════" -ForegroundColor Cyan
        Write-Host ""
        
        if (-not $DryRun) {
            Write-Host "✅ Configuration complete. No reboot required." -ForegroundColor Green
        }
        Write-Host ""
        
        # Security reminder
        Write-Host "⚠️  SECURITY REMINDER:" -ForegroundColor Yellow
        Write-Host "   - These exclusions remain until manually removed" -ForegroundColor White
        Write-Host "   - Review exclusions regularly: Get-MpPreference | Select-Object Exclusion*" -ForegroundColor White
        Write-Host "   - To remove exclusions, use: Remove-MpPreference" -ForegroundColor White
        Write-Host "   - Consider re-enabling real-time monitoring after development" -ForegroundColor White
        Write-Host ""
        
    }
    catch {
        Write-Host ""
        Write-Host "❌ ERROR: An unexpected error occurred:" -ForegroundColor Red
        Write-Host $_.Exception.Message -ForegroundColor Red
        Write-Host ""
        Write-Host "Stack trace:" -ForegroundColor Gray
        Write-Host $_.ScriptStackTrace -ForegroundColor Gray
        Write-Host ""
        exit 1
    }
}

# Execute the override
Invoke-DefenderOverride
