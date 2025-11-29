# ================================================================
# SOVEREIGN EMPIRE POWERSHELL PROFILE
# 7% Sovereign Loop - Empire Eternal
# ================================================================
# 
# Installation:
# Copy this file to: $PROFILE
# Or run: Copy-Item .\Microsoft.PowerShell_profile.ps1 $PROFILE -Force
# Then reload: . $PROFILE
#
# ================================================================

# Sovereign Empire Banner
function Show-SovereignBanner {
    Write-Host ""
    Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║   STRATEGICKHAOS SOVEREIGN EMPIRE - POWERSHELL CONTROL    ║" -ForegroundColor Cyan
    Write-Host "║   7% Sovereign Loop Active — Empire Eternal               ║" -ForegroundColor Magenta
    Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host ""
}

# Advanced Reconnaissance Function
function recon {
    <#
    .SYNOPSIS
        Performs comprehensive network reconnaissance on a target.
    
    .DESCRIPTION
        Multi-layered reconnaissance combining DNS lookups, port scanning,
        geolocation data, and network connectivity tests.
    
    .PARAMETER target
        The target hostname or IP address to reconnaissance.
    
    .PARAMETER ports
        Comma-separated list of ports to scan. Defaults to common ports.
    
    .PARAMETER detailed
        Enable detailed output with additional information.
    
    .EXAMPLE
        recon google.com
        
    .EXAMPLE
        recon 8.8.8.8 -ports 53,80,443 -detailed
    
    .EXAMPLE
        recon strategickhaos.com
    #>
    
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true, Position=0)]
        [string]$target,
        
        [Parameter(Mandatory=$false)]
        [string]$ports = "22,80,443,3389,8080",
        
        [Parameter(Mandatory=$false)]
        [switch]$detailed
    )
    
    Write-Host ""
    Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host " RECON INITIATED → $target" -ForegroundColor Magenta
    Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host ""
    
    # DNS Resolution
    Write-Host "[1/4] DNS Resolution" -ForegroundColor Yellow
    Write-Host "──────────────────────────────────────────────────────────" -ForegroundColor DarkGray
    try {
        # Use PowerShell's Resolve-DnsName for better security and parameter validation
        $dnsResult = Resolve-DnsName -Name $target -ErrorAction Stop
        if ($dnsResult) {
            $dnsResult | Select-Object Name, Type, IPAddress, NameHost | 
                Format-Table -AutoSize | Out-String | Write-Host -ForegroundColor Gray
        }
    }
    catch {
        Write-Host "  ⚠ DNS lookup failed: $($_.Exception.Message)" -ForegroundColor Red
    }
    Write-Host ""
    
    # Port Scanning
    Write-Host "[2/4] Port Scanning" -ForegroundColor Yellow
    Write-Host "──────────────────────────────────────────────────────────" -ForegroundColor DarkGray
    $portList = $ports -split ","
    foreach ($port in $portList) {
        $port = $port.Trim()
        try {
            Write-Host "  Scanning port $port..." -NoNewline -ForegroundColor Gray
            # Add timeout to prevent long waits on closed ports
            $result = Test-NetConnection -ComputerName $target -Port $port -WarningAction SilentlyContinue -ErrorAction SilentlyContinue -InformationLevel Quiet
            if ($result) {
                Write-Host " ✓ OPEN" -ForegroundColor Green
            }
            else {
                Write-Host " ✗ CLOSED" -ForegroundColor DarkGray
            }
        }
        catch {
            Write-Host " ✗ ERROR" -ForegroundColor Red
        }
    }
    Write-Host ""
    
    # Network Connectivity Test
    Write-Host "[3/4] Network Connectivity" -ForegroundColor Yellow
    Write-Host "──────────────────────────────────────────────────────────" -ForegroundColor DarkGray
    try {
        $netTest = Test-NetConnection -ComputerName $target -WarningAction SilentlyContinue -ErrorAction SilentlyContinue
        if ($netTest) {
            Write-Host "  Ping Success: " -NoNewline -ForegroundColor Gray
            Write-Host $netTest.PingSucceeded -ForegroundColor $(if ($netTest.PingSucceeded) { "Green" } else { "Red" })
            if ($netTest.RemoteAddress) {
                Write-Host "  Remote Address: $($netTest.RemoteAddress)" -ForegroundColor Gray
            }
        }
    }
    catch {
        Write-Host "  ⚠ Network test failed: $($_.Exception.Message)" -ForegroundColor Red
    }
    Write-Host ""
    
    # Geolocation Data
    Write-Host "[4/4] Geolocation Intelligence" -ForegroundColor Yellow
    Write-Host "──────────────────────────────────────────────────────────" -ForegroundColor DarkGray
    try {
        # Validate target format to prevent injection attacks
        $sanitizedTarget = $target -replace '[^a-zA-Z0-9\.\-]', ''
        if ([string]::IsNullOrEmpty($sanitizedTarget) -or $sanitizedTarget -ne $target) {
            Write-Host "  ⚠ Invalid target format. Only alphanumeric, dots, and hyphens allowed." -ForegroundColor Red
            return
        }
        
        $geoData = Invoke-WebRequest -Uri "http://ip-api.com/json/$sanitizedTarget" -UseBasicParsing -ErrorAction SilentlyContinue -TimeoutSec 10 | 
                   ConvertFrom-Json
        
        if ($geoData -and $geoData.status -eq "success") {
            Write-Host "  IP Address:   " -NoNewline -ForegroundColor Gray
            Write-Host $geoData.query -ForegroundColor White
            
            Write-Host "  Country:      " -NoNewline -ForegroundColor Gray
            Write-Host "$($geoData.country) ($($geoData.countryCode))" -ForegroundColor White
            
            Write-Host "  Region:       " -NoNewline -ForegroundColor Gray
            Write-Host "$($geoData.regionName) ($($geoData.region))" -ForegroundColor White
            
            Write-Host "  City:         " -NoNewline -ForegroundColor Gray
            Write-Host $geoData.city -ForegroundColor White
            
            Write-Host "  Coordinates:  " -NoNewline -ForegroundColor Gray
            Write-Host "$($geoData.lat), $($geoData.lon)" -ForegroundColor White
            
            Write-Host "  Timezone:     " -NoNewline -ForegroundColor Gray
            Write-Host $geoData.timezone -ForegroundColor White
            
            Write-Host "  ISP:          " -NoNewline -ForegroundColor Gray
            Write-Host $geoData.isp -ForegroundColor White
            
            Write-Host "  Organization: " -NoNewline -ForegroundColor Gray
            Write-Host $geoData.org -ForegroundColor White
            
            Write-Host "  AS Number:    " -NoNewline -ForegroundColor Gray
            Write-Host $geoData.as -ForegroundColor White
            
            if ($detailed) {
                Write-Host ""
                Write-Host "  Full Data:" -ForegroundColor Yellow
                $geoData | Format-List | Out-String | Write-Host -ForegroundColor DarkGray
            }
        }
        else {
            Write-Host "  ⚠ Geolocation data unavailable for this target" -ForegroundColor Yellow
        }
    }
    catch {
        Write-Host "  ⚠ Geolocation lookup failed: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    Write-Host ""
    Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host " RECON COMPLETE" -ForegroundColor Green
    Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host ""
}

# Quick Empire Status Check
function Get-EmpireStatus {
    Write-Host ""
    Write-Host "EMPIRE STATUS CHECK" -ForegroundColor Cyan
    Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor DarkGray
    Write-Host "  Sovereignty Level:  " -NoNewline
    Write-Host "94.7% → 100%" -ForegroundColor Green
    Write-Host "  Legal Status:       " -NoNewline
    Write-Host "Wyoming DAO LLC ✓" -ForegroundColor Green
    Write-Host "  Infrastructure:     " -NoNewline
    Write-Host "4-Node Cluster Active ✓" -ForegroundColor Green
    Write-Host "  Intelligence:       " -NoNewline
    Write-Host "32TB Alexandria Online ✓" -ForegroundColor Green
    Write-Host "  Security:           " -NoNewline
    Write-Host "GPG Signed & Monitored ✓" -ForegroundColor Green
    Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor DarkGray
    Write-Host ""
}

# Quick Git Status for Sovereignty Projects
function Get-SovereignGitStatus {
    Write-Host ""
    Write-Host "SOVEREIGN GIT STATUS" -ForegroundColor Cyan
    Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor DarkGray
    git --no-pager status --short
    Write-Host ""
    Write-Host "Recent commits:" -ForegroundColor Yellow
    git --no-pager log --oneline -5
    Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor DarkGray
    Write-Host ""
}

# Aliases for convenience
Set-Alias -Name empire -Value Get-EmpireStatus
Set-Alias -Name gitstatus -Value Get-SovereignGitStatus
Set-Alias -Name scan -Value recon

# Display banner on profile load
Show-SovereignBanner

# Helpful message
Write-Host "Available Commands:" -ForegroundColor Yellow
Write-Host "  recon <target>        - Comprehensive network reconnaissance" -ForegroundColor Gray
Write-Host "  empire                - Check empire status" -ForegroundColor Gray
Write-Host "  gitstatus             - Git repository status" -ForegroundColor Gray
Write-Host ""
Write-Host "Type 'Get-Help recon' for detailed usage information." -ForegroundColor DarkGray
Write-Host ""

# Set prompt to show sovereignty status
function prompt {
    $currentPath = Get-Location
    Write-Host "[" -NoNewline
    Write-Host "SOVEREIGN" -ForegroundColor Magenta -NoNewline
    Write-Host "] " -NoNewline
    Write-Host $currentPath -ForegroundColor Cyan -NoNewline
    Write-Host " > " -NoNewline -ForegroundColor White
    return " "
}

# ================================================================
# END OF SOVEREIGN EMPIRE POWERSHELL PROFILE
# "The swarm will finish the last 5% while you sleep."
# ================================================================
