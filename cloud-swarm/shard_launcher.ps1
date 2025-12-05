#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Shard Launcher - PowerShell launcher for shard orchestration from Windows control node.
.DESCRIPTION
    Launches PID-RANCO or TauGate shards across all discovered cloud terminals.
.PARAMETER Inventory
    Path to the Ansible inventory file (default: cloud_hosts.ini).
.PARAMETER Workload
    Workload to execute: pid_ranco, taugate (default: pid_ranco).
.PARAMETER CostGuard
    Trigger cost-guard shutdown after completion.
.EXAMPLE
    ./shard_launcher.ps1
    ./shard_launcher.ps1 -Inventory cloud_hosts.ini -Workload taugate
    ./shard_launcher.ps1 -CostGuard
#>

param(
    [string]$Inventory = "cloud_hosts.ini",
    [ValidateSet("pid_ranco", "taugate", "progress")]
    [string]$Workload = "pid_ranco",
    [switch]$CostGuard,
    [int]$Forks = 0
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$LogFile = "/tmp/shard_launcher_${Timestamp}.log"

# Colors
function Write-ColorHost {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
    Add-Content -Path $LogFile -Value "[$(Get-Date -Format 'o')] $Message"
}

function Write-Log { param([string]$Message) Write-ColorHost $Message "White" }
function Write-Success { param([string]$Message) Write-ColorHost "[SUCCESS] $Message" "Green" }
function Write-Info { param([string]$Message) Write-ColorHost "[INFO] $Message" "Cyan" }
function Write-Warn { param([string]$Message) Write-ColorHost "[WARN] $Message" "Yellow" }
function Write-Err { param([string]$Message) Write-ColorHost "[ERROR] $Message" "Red" }

# Header
function Show-Header {
    Write-Host ""
    Write-Host "╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║     Strategickhaos Cloud Swarm - Shard Launcher (PS)      ║" -ForegroundColor Cyan
    Write-Host "╚═══════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host ""
}

# Check prerequisites
function Test-Prerequisites {
    Write-Info "Checking prerequisites..."
    
    # Check for ansible-playbook
    try {
        $null = Get-Command ansible-playbook -ErrorAction Stop
    }
    catch {
        Write-Err "ansible-playbook not found. Please install Ansible."
        Write-Info "On Windows, install via WSL or use: pip install ansible"
        exit 1
    }
    
    # Check inventory file
    if (-not (Test-Path $Inventory)) {
        Write-Err "Inventory file not found: $Inventory"
        Write-Info "Run cloud_inventory.ps1 first to discover nodes."
        exit 1
    }
    
    # Check playbook
    $playbookPath = Join-Path $ScriptDir "cloud_swarm_playbook.yaml"
    if (-not (Test-Path $playbookPath)) {
        Write-Err "Playbook not found: $playbookPath"
        exit 1
    }
    
    Write-Success "Prerequisites check passed"
}

# Get hosts from inventory
function Get-InventoryHosts {
    $hosts = @()
    $content = Get-Content $Inventory
    
    foreach ($line in $content) {
        # Skip section headers, empty lines, comments, and vars
        if ($line -match '^\[' -or $line -match '^\s*$' -or $line -match '^#' -or $line -match ':vars') {
            continue
        }
        
        # Extract IP/hostname (first field)
        $parts = $line -split '\s+'
        if ($parts.Count -gt 0 -and $parts[0]) {
            $hosts += $parts[0]
        }
    }
    
    return $hosts
}

# Launch PID-RANCO shards
function Start-PidRancoShards {
    $hosts = Get-InventoryHosts
    $hostCount = $hosts.Count
    
    Write-Info "=== PID-RANCO Shard Launcher ==="
    Write-Info "Inventory: $Inventory"
    Write-Info "Total nodes: $hostCount"
    Write-Info "Workload: $Workload"
    Write-Info "Log file: $LogFile"
    Write-Host ""
    
    if ($hostCount -eq 0) {
        Write-Err "No hosts found in inventory"
        exit 1
    }
    
    Write-Info "Launching $hostCount shards in parallel..."
    
    # Calculate estimated time
    $estimatedMinutes = 11 + [math]::Floor($hostCount / 10)
    Write-Info "Estimated completion: ~${estimatedMinutes} minutes"
    Write-Host ""
    
    # Set forks if not specified
    if ($Forks -eq 0) { $Forks = $hostCount }
    
    # Run Ansible playbook
    Write-Info "Starting Ansible playbook execution..."
    
    $playbookPath = Join-Path $ScriptDir "cloud_swarm_playbook.yaml"
    
    $ansibleArgs = @(
        "-i", $Inventory,
        $playbookPath,
        "--tags", "pid_ranco",
        "--extra-vars", "shard_total=$hostCount",
        "--forks", "$Forks"
    )
    
    & ansible-playbook @ansibleArgs 2>&1 | Tee-Object -FilePath $LogFile -Append
    
    $exitCode = $LASTEXITCODE
    
    if ($exitCode -eq 0) {
        Write-Success "All $hostCount shards launched successfully!"
        
        # Show shard summary
        Write-Host ""
        Write-Info "Shards launched:"
        for ($i = 0; $i -lt $hostCount; $i++) {
            Write-Host "  [$i/$hostCount] $($hosts[$i])" -ForegroundColor Green
        }
    }
    else {
        Write-Warn "Some shards may have failed. Check log: $LogFile"
    }
    
    return $exitCode
}

# Launch TauGate shards
function Start-TauGateShards {
    $hosts = Get-InventoryHosts
    $hostCount = $hosts.Count
    
    Write-Info "=== TauGate Shard Launcher ==="
    Write-Info "Inventory: $Inventory"
    Write-Info "Total nodes: $hostCount"
    Write-Info "Workload: TauGate 10B Compound Screening"
    Write-Host ""
    
    Write-Info "Launching TauGate shards for 10B compound screening..."
    Write-Info "Estimated completion: ~16-18 hours"
    Write-Host ""
    
    if ($Forks -eq 0) { $Forks = $hostCount }
    
    $playbookPath = Join-Path $ScriptDir "cloud_swarm_playbook.yaml"
    
    $ansibleArgs = @(
        "-i", $Inventory,
        $playbookPath,
        "--tags", "taugate_shard",
        "--extra-vars", "shard_total=$hostCount run_taugate_screen=true",
        "--forks", "$Forks"
    )
    
    & ansible-playbook @ansibleArgs 2>&1 | Tee-Object -FilePath $LogFile -Append
    
    $exitCode = $LASTEXITCODE
    
    if ($exitCode -eq 0) {
        Write-Success "TauGate shards launched!"
    }
    else {
        Write-Warn "Some TauGate shards may have failed."
    }
    
    return $exitCode
}

# Show progress
function Show-Progress {
    $hosts = Get-InventoryHosts
    
    Write-Info "=== Shard Progress ==="
    Write-Host ""
    
    $completed = 0
    
    foreach ($host in $hosts) {
        try {
            $result = ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 `
                "ubuntu@$host" `
                "ls /opt/strategickhaos/logs/pid_ranco_shard_*.json 2>/dev/null | wc -l" 2>$null
            
            if ([int]$result -gt 0) {
                Write-Host "  ✓ ${host}: $result shard(s) complete" -ForegroundColor Green
                $completed++
            }
            else {
                Write-Host "  ○ ${host}: in progress" -ForegroundColor Yellow
            }
        }
        catch {
            Write-Host "  ✗ ${host}: unreachable" -ForegroundColor Red
        }
    }
    
    Write-Host ""
    Write-Info "Progress: $completed/$($hosts.Count) nodes reporting results"
}

# Trigger cost guard
function Invoke-CostGuard {
    Write-Info "Triggering cost-guard shutdown play..."
    
    $playbookPath = Join-Path $ScriptDir "cloud_swarm_playbook.yaml"
    
    & ansible-playbook -i $Inventory $playbookPath --tags cost_guard 2>&1 | Tee-Object -FilePath $LogFile -Append
    
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Cost-guard triggered on all nodes"
    }
    else {
        Write-Warn "Cost-guard may not have been applied to all nodes"
    }
}

# Main execution
Show-Header
Test-Prerequisites

$exitCode = 0

switch ($Workload) {
    "pid_ranco" {
        $exitCode = Start-PidRancoShards
    }
    "taugate" {
        $exitCode = Start-TauGateShards
    }
    "progress" {
        Show-Progress
    }
}

if ($CostGuard) {
    Write-Host ""
    Invoke-CostGuard
}

Write-Host ""
Write-Info "=== Launcher Complete ==="
Write-Info "Log file: $LogFile"
Write-Info ""
Write-Info "Next steps:"
Write-Info "  - Check progress: ./shard_launcher.ps1 -Workload progress"
Write-Info "  - Collect results: ./collect_and_verify.sh $Inventory ${Workload}_$Timestamp"
Write-Info "  - Trigger cost-guard: ./shard_launcher.ps1 -CostGuard"

exit $exitCode
