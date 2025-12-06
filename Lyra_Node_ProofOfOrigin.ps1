# Lyra Node Proof of Origin - Heartbeat Monitor
# Part of the Biomimetic Multi-Agent Architecture
# This script serves as the heartbeat of the computational organism,
# continuously verifying the system is alive and maintaining proof of origin.

<#
.SYNOPSIS
    Heartbeat monitor and proof-of-origin validator for the Strategickhaos Sovereignty Architecture
    
.DESCRIPTION
    This PowerShell script serves as the heartbeat of the living computational organism,
    monitoring vital signs, verifying system integrity, and maintaining cryptographic
    proof of origin for the biomimetic multi-agent architecture.
    
.NOTES
    Component: Heartbeat System
    Architecture: Neurodivergent Biomimetic Multi-Agent Architecture
    Patent: Provisional Patent #2 - Addendum
    
.EXAMPLE
    .\Lyra_Node_ProofOfOrigin.ps1 -Monitor
    Runs continuous heartbeat monitoring
    
.EXAMPLE
    .\Lyra_Node_ProofOfOrigin.ps1 -CheckOrigin
    Verifies proof of origin for all components
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory=$false)]
    [switch]$Monitor,
    
    [Parameter(Mandatory=$false)]
    [switch]$CheckOrigin,
    
    [Parameter(Mandatory=$false)]
    [int]$HeartbeatInterval = 60
)

# Colors for output
$ColorHeart = "Red"
$ColorOK = "Green"
$ColorWarning = "Yellow"
$ColorError = "Red"

function Write-Heartbeat {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "💓 [$timestamp] $Message" -ForegroundColor $ColorHeart
}

function Write-SystemOK {
    param([string]$Message)
    Write-Host "✓ $Message" -ForegroundColor $ColorOK
}

function Write-SystemWarning {
    param([string]$Message)
    Write-Host "⚠ $Message" -ForegroundColor $ColorWarning
}

function Write-SystemError {
    param([string]$Message)
    Write-Host "✗ $Message" -ForegroundColor $ColorError
}

function Test-OrganismVitals {
    <#
    .SYNOPSIS
        Check vital signs of the computational organism
    #>
    
    Write-Heartbeat "Checking organism vitals..."
    
    $vitals = @{
        DNA = $false
        CellMembranes = $false
        Skeleton = $false
        Circulation = $false
        Immunity = $false
        NervousSystem = $false
    }
    
    # Check DNA (docker-compose.yml)
    if (Test-Path ".\docker-compose.yml") {
        Write-SystemOK "DNA (docker-compose.yml) present"
        $vitals.DNA = $true
    } else {
        Write-SystemError "DNA (docker-compose.yml) missing!"
    }
    
    # Check Cell Membranes (Dockerfiles)
    $dockerfiles = Get-ChildItem -Filter "Dockerfile.*" -ErrorAction SilentlyContinue
    if ($dockerfiles.Count -gt 0) {
        Write-SystemOK "Cell membranes (Dockerfiles) present: $($dockerfiles.Count)"
        $vitals.CellMembranes = $true
    } else {
        Write-SystemWarning "No cell membranes (Dockerfiles) detected"
    }
    
    # Check Skeleton (.git)
    if (Test-Path ".\.git") {
        Write-SystemOK "Skeletal system (.git) present"
        $vitals.Skeleton = $true
    } else {
        Write-SystemError "Skeletal system (.git) missing!"
    }
    
    # Check Circulation (bots/circulation/)
    if (Test-Path ".\bots\circulation") {
        Write-SystemOK "Circulatory system present"
        $vitals.Circulation = $true
    } else {
        Write-SystemWarning "Circulatory system not found"
    }
    
    # Check Immunity (bots/immunity/)
    if (Test-Path ".\bots\immunity") {
        Write-SystemOK "Immune system present"
        $vitals.Immunity = $true
    } else {
        Write-SystemWarning "Immune system not found"
    }
    
    # Check Nervous System (bots/discord_dao_monitor.py)
    if (Test-Path ".\bots\discord_dao_monitor.py") {
        Write-SystemOK "Nervous system endpoint present"
        $vitals.NervousSystem = $true
    } else {
        Write-SystemWarning "Nervous system endpoint not found"
    }
    
    return $vitals
}

function Get-ProofOfOrigin {
    <#
    .SYNOPSIS
        Generate cryptographic proof of origin
    #>
    
    Write-Heartbeat "Generating proof of origin..."
    
    $proofDir = ".\.strategickhaos\proof_of_origin"
    if (-not (Test-Path $proofDir)) {
        New-Item -ItemType Directory -Path $proofDir -Force | Out-Null
        Write-SystemOK "Created proof of origin directory"
    }
    
    $proof = @{
        Timestamp = Get-Date -Format "o"
        OriginNode = $env:COMPUTERNAME
        Repository = "Sovereignty-Architecture-Elevator-Pitch"
        Architecture = "Neurodivergent Biomimetic Multi-Agent"
        PatentReference = "Provisional Patent #2 - Addendum"
        ComponentsVerified = @()
    }
    
    # Verify core components
    if (Test-Path ".\docker-compose.yml") {
        $dnaHash = (Get-FileHash ".\docker-compose.yml" -Algorithm SHA256).Hash
        $proof.ComponentsVerified += @{
            Component = "DNA"
            File = "docker-compose.yml"
            Hash = $dnaHash
        }
    }
    
    if (Test-Path ".\.env") {
        # Don't hash .env (contains secrets), just verify existence
        $proof.ComponentsVerified += @{
            Component = "Epigenetic Switches"
            File = ".env"
            Hash = "REDACTED_CONTAINS_SECRETS"
        }
    }
    
    # Save proof
    $proofFile = Join-Path $proofDir "heartbeat_$(Get-Date -Format 'yyyyMMdd_HHmmss').json"
    $proof | ConvertTo-Json -Depth 4 | Out-File -FilePath $proofFile -Encoding UTF8
    
    Write-SystemOK "Proof of origin saved: $proofFile"
    return $proof
}

function Start-HeartbeatMonitor {
    param([int]$Interval = 60)
    
    Write-Host ""
    Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host "  HEARTBEAT MONITOR - LYRA NODE PROOF OF ORIGIN" -ForegroundColor Cyan
    Write-Host "  Biomimetic Multi-Agent Architecture" -ForegroundColor Cyan
    Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host ""
    Write-Heartbeat "Starting continuous heartbeat monitoring..."
    Write-Host "Interval: $Interval seconds" -ForegroundColor Gray
    Write-Host "Press Ctrl+C to stop" -ForegroundColor Gray
    Write-Host ""
    
    $cycle = 0
    
    while ($true) {
        try {
            $cycle++
            Write-Host "─────────────────────────────────────────────────────────" -ForegroundColor DarkGray
            Write-Heartbeat "Heartbeat cycle #$cycle"
            
            # Check vitals
            $vitals = Test-OrganismVitals
            
            # Count healthy systems
            $healthyCount = ($vitals.Values | Where-Object { $_ -eq $true }).Count
            $totalCount = $vitals.Count
            
            Write-Host ""
            Write-Host "Health Status: $healthyCount/$totalCount systems operational" -ForegroundColor $(if ($healthyCount -eq $totalCount) { $ColorOK } else { $ColorWarning })
            
            # Generate proof of origin every 10 cycles
            if ($cycle % 10 -eq 0) {
                Get-ProofOfOrigin | Out-Null
            }
            
            Write-Host ""
            Write-Host "Next heartbeat in $Interval seconds..." -ForegroundColor Gray
            
            Start-Sleep -Seconds $Interval
            
        } catch {
            Write-SystemError "Heartbeat error: $_"
            Start-Sleep -Seconds 5
        }
    }
}

# Main execution
try {
    if ($Monitor) {
        Start-HeartbeatMonitor -Interval $HeartbeatInterval
    }
    elseif ($CheckOrigin) {
        Write-Host ""
        Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
        Write-Host "  PROOF OF ORIGIN CHECK" -ForegroundColor Cyan
        Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
        Write-Host ""
        
        $proof = Get-ProofOfOrigin
        Write-Host ""
        Write-Host "Origin verified for:" -ForegroundColor Green
        Write-Host "  Node: $($proof.OriginNode)" -ForegroundColor Gray
        Write-Host "  Repository: $($proof.Repository)" -ForegroundColor Gray
        Write-Host "  Components: $($proof.ComponentsVerified.Count)" -ForegroundColor Gray
        Write-Host ""
    }
    else {
        # Default: Single heartbeat check
        Write-Host ""
        Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
        Write-Host "  SINGLE HEARTBEAT CHECK" -ForegroundColor Cyan
        Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
        Write-Host ""
        
        $vitals = Test-OrganismVitals
        
        $healthyCount = ($vitals.Values | Where-Object { $_ -eq $true }).Count
        $totalCount = $vitals.Count
        
        Write-Host ""
        if ($healthyCount -eq $totalCount) {
            Write-Host "💚 ORGANISM HEALTHY: All $totalCount systems operational" -ForegroundColor Green
        } else {
            Write-Host "💛 ORGANISM DEGRADED: $healthyCount/$totalCount systems operational" -ForegroundColor Yellow
        }
        Write-Host ""
        
        Write-Host "Use -Monitor to start continuous heartbeat monitoring" -ForegroundColor Gray
        Write-Host "Use -CheckOrigin to verify proof of origin" -ForegroundColor Gray
        Write-Host ""
    }
}
catch {
    Write-SystemError "Fatal error: $_"
    exit 1
}
