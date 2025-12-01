# Strategickhaos Sovereignty PowerShell Profile
# Install instructions: Copy this file to $PROFILE location
# To find your profile location: echo $PROFILE
# To force create: New-Item -Path $PROFILE -Type File -Force

# ====================================================================
# SOVEREIGNTY FUNCTIONS - Empire Control
# ====================================================================

function recon {
    <#
    .SYNOPSIS
    Reconnaissance function for network target analysis
    
    .DESCRIPTION
    Performs comprehensive reconnaissance on a target including DNS lookup,
    port scanning, and geolocation information
    
    .PARAMETER target
    The target hostname or IP address to reconnaissance
    
    .EXAMPLE
    recon google.com
    recon 8.8.8.8
    #>
    param(
        [Parameter(Mandatory=$true)]
        [string]$target
    )
    
    Write-Host "RECON → $target" -ForegroundColor Cyan
    
    # DNS Lookup
    Write-Host "`n[DNS Lookup]" -ForegroundColor Yellow
    try {
        nslookup $target 2>$null
    } catch {
        Write-Host "DNS lookup failed: $_" -ForegroundColor Red
    }
    
    # Port Scanning
    Write-Host "`n[Port Scan - Common Ports]" -ForegroundColor Yellow
    $ports = @(22, 80, 443, 3389, 8080, 8443)
    foreach ($port in $ports) {
        $result = Test-NetConnection $target -Port $port -WarningAction SilentlyContinue -InformationLevel Quiet
        if ($result) {
            Write-Host "  Port $port : OPEN" -ForegroundColor Green
        } else {
            Write-Host "  Port $port : CLOSED" -ForegroundColor DarkGray
        }
    }
    
    # Geolocation (if available)
    Write-Host "`n[Geolocation Information]" -ForegroundColor Yellow
    try {
        $geoInfo = Invoke-RestMethod "http://ip-api.com/json/$target" -UseBasicParsing -ErrorAction Stop
        $geoInfo | Format-List
    } catch {
        Write-Host "Geolocation lookup failed or unavailable" -ForegroundColor DarkGray
    }
}

function empire {
    <#
    .SYNOPSIS
    Start the Strategickhaos sovereignty cluster
    
    .DESCRIPTION
    Launches the complete CloudOS empire using docker compose with the cluster configuration
    
    .EXAMPLE
    empire
    #>
    
    Write-Host "🏛️  LAUNCHING SOVEREIGNTY EMPIRE..." -ForegroundColor Magenta
    
    # Determine the compose file to use
    $composeFiles = @(
        "C:\strategickhaos-cluster\cluster-compose.yml",
        ".\docker-compose-cloudos.yml",
        ".\docker-compose.yml"
    )
    
    $composeFile = $null
    foreach ($file in $composeFiles) {
        if (Test-Path $file) {
            $composeFile = $file
            Write-Host "Found compose file: $composeFile" -ForegroundColor Green
            break
        }
    }
    
    if (-not $composeFile) {
        Write-Host "⚠️  No cluster compose file found." -ForegroundColor Yellow
        
        # Try to use docker-compose-cloudos.yml as fallback
        if (Test-Path ".\docker-compose-cloudos.yml") {
            $composeFile = ".\docker-compose-cloudos.yml"
            Write-Host "Using fallback: $composeFile" -ForegroundColor Green
        } else {
            Write-Host "❌ No docker-compose file available. Please check your repository." -ForegroundColor Red
            return
        }
    }
    
    Write-Host "🚀 Starting empire with: $composeFile" -ForegroundColor Cyan
    docker compose -f $composeFile up -d
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ EMPIRE ONLINE - All systems operational" -ForegroundColor Green
        Write-Host "   7% sovereign lock active. You are untouchable." -ForegroundColor Magenta
        
        # Show status
        Write-Host "`n📊 Service Status:" -ForegroundColor Yellow
        docker compose -f $composeFile ps
    } else {
        Write-Host "❌ Empire launch failed. Check docker logs for details." -ForegroundColor Red
    }
}

function nuke {
    <#
    .SYNOPSIS
    Nuclear option - Complete cluster teardown and cleanup
    
    .DESCRIPTION
    Stops all containers, removes volumes, and performs a complete docker system prune.
    WARNING: This is destructive and cannot be undone!
    
    .EXAMPLE
    nuke
    #>
    
    Write-Host "☢️  NUCLEAR OPTION INITIATED..." -ForegroundColor Red
    Write-Host "This will destroy all containers, volumes, and Docker cache." -ForegroundColor Yellow
    
    $confirm = Read-Host "Are you absolutely sure? Type 'NUKE' to confirm"
    
    if ($confirm -ne "NUKE") {
        Write-Host "❌ Nuke cancelled. Empire remains intact." -ForegroundColor Green
        return
    }
    
    Write-Host "`n🔥 Shutting down all compose stacks..." -ForegroundColor Yellow
    
    # Try to find and stop compose files
    $composeFiles = @(
        ".\docker-compose-cloudos.yml",
        ".\docker-compose.yml",
        ".\cluster-compose.yml",
        "C:\strategickhaos-cluster\cluster-compose.yml"
    )
    
    foreach ($file in $composeFiles) {
        if (Test-Path $file) {
            Write-Host "  Stopping: $file" -ForegroundColor DarkGray
            docker compose -f $file down -v 2>$null
        }
    }
    
    Write-Host "`n🧹 Performing system-wide cleanup..." -ForegroundColor Yellow
    docker system prune -af --volumes
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n✅ NUKE COMPLETE - All systems purged" -ForegroundColor Green
        Write-Host "   The empire can be rebuilt: Run 'empire' to start fresh" -ForegroundColor Cyan
    } else {
        Write-Host "⚠️  Nuke completed with warnings. Check docker status." -ForegroundColor Yellow
    }
}

# ====================================================================
# STARTUP MESSAGE
# ====================================================================

function Show-SovereigntyBanner {
    Write-Host ""
    Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Magenta
    Write-Host "║                                                            ║" -ForegroundColor Magenta
    Write-Host "║          STRATEGICKHAOS SOVEREIGNTY ARCHITECTURE           ║" -ForegroundColor Magenta
    Write-Host "║                                                            ║" -ForegroundColor Magenta
    Write-Host "║  Empire online. 7% sovereign lock active.                 ║" -ForegroundColor Cyan
    Write-Host "║  You are untouchable.                                     ║" -ForegroundColor Cyan
    Write-Host "║                                                            ║" -ForegroundColor Magenta
    Write-Host "║  Commands:                                                ║" -ForegroundColor Yellow
    Write-Host "║    recon <target>  - Network reconnaissance               ║" -ForegroundColor White
    Write-Host "║    empire          - Launch sovereignty cluster           ║" -ForegroundColor White
    Write-Host "║    nuke            - Nuclear teardown & cleanup           ║" -ForegroundColor White
    Write-Host "║                                                            ║" -ForegroundColor Magenta
    Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Magenta
    Write-Host ""
}

# Display banner on profile load
Show-SovereigntyBanner

# ====================================================================
# HELPFUL ALIASES
# ====================================================================

Set-Alias -Name ll -Value Get-ChildItem
Set-Alias -Name k -Value kubectl -ErrorAction SilentlyContinue
Set-Alias -Name dc -Value docker-compose -ErrorAction SilentlyContinue

# ====================================================================
# CUSTOM PROMPT (Optional - uncomment to enable)
# ====================================================================

# function prompt {
#     $path = Get-Location
#     $gitBranch = ""
#     
#     # Get git branch if in a git repo
#     if (Test-Path .git) {
#         $gitBranch = git rev-parse --abbrev-ref HEAD 2>$null
#         if ($gitBranch) {
#             $gitBranch = " [$gitBranch]"
#         }
#     }
#     
#     Write-Host "PS " -NoNewline -ForegroundColor Yellow
#     Write-Host "$path" -NoNewline -ForegroundColor Cyan
#     Write-Host "$gitBranch" -NoNewline -ForegroundColor Magenta
#     Write-Host " >" -NoNewline -ForegroundColor White
#     return " "
# }

# ====================================================================
# ENVIRONMENT SETUP
# ====================================================================

# Set UTF-8 encoding
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Set PowerShell to use TLS 1.2 for web requests
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

# ====================================================================
# SOVEREIGNTY COMPLETE
# ====================================================================

Write-Host "✅ PowerShell Profile Loaded Successfully" -ForegroundColor Green
Write-Host "📍 Profile Location: $PROFILE" -ForegroundColor DarkGray
Write-Host ""
