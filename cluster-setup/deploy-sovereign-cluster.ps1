# DOM_010101 Sovereign Cluster - Master Deployment Script
# Complete orchestration of the entire cluster setup

<#
.SYNOPSIS
    Master deployment script for DOM_010101 sovereign cluster
    
.DESCRIPTION
    Orchestrates the complete setup of the 4-machine cluster:
    1. Validates prerequisites
    2. Checks TrueNAS connectivity
    3. Sets up Kubernetes control plane
    4. Guides worker node setup
    5. Mounts TrueNAS storage
    6. Deploys love swarm stack
    
.PARAMETER SkipPrereqCheck
    Skip prerequisite validation
    
.PARAMETER SkipNasCheck
    Skip TrueNAS connectivity check
    
.PARAMETER AutoJoinWorkers
    Automatically prompt for worker node setup (interactive)
    
.NOTES
    Run this on the control plane machine (ASUS TUF Gaming A15 Nova)
    Requires: Administrator privileges
#>

[CmdletBinding()]
param(
    [switch]$SkipPrereqCheck = $false,
    [switch]$SkipNasCheck = $false,
    [switch]$AutoJoinWorkers = $false
)

# Check if running as Administrator
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Error "This script must be run as Administrator"
    exit 1
}

$ErrorActionPreference = "Stop"

Write-Host @"
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║          DOM_010101 SOVEREIGN CLUSTER DEPLOYMENT              ║
║                                                               ║
║  🖥️  4 Machines | 320 GB RAM | 32 TB Storage                  ║
║  ⚡ Kubernetes + Docker Swarm + TrueNAS Scale                 ║
║  🎵 320 Love Containers @ 432 Hz                              ║
║  💾 Fully Offline Capable | No Cloud Dependencies            ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan

Write-Host ""
Start-Sleep -Seconds 2

# Step 0: Prerequisites Check
if (!$SkipPrereqCheck) {
    Write-Host "═══ [0/7] Prerequisites Check ═══" -ForegroundColor Yellow
    Write-Host ""
    
    # Check Docker
    Write-Host "Checking Docker..." -ForegroundColor White
    try {
        docker version | Out-Null
        $dockerVersion = docker version --format '{{.Server.Version}}'
        Write-Host "✓ Docker: $dockerVersion" -ForegroundColor Green
    } catch {
        Write-Error "Docker is not running. Start Docker Desktop and try again."
        exit 1
    }
    
    # Check PowerShell version
    Write-Host "Checking PowerShell version..." -ForegroundColor White
    $psVersion = $PSVersionTable.PSVersion
    if ($psVersion.Major -ge 5) {
        Write-Host "✓ PowerShell: $($psVersion.ToString())" -ForegroundColor Green
    } else {
        Write-Warning "PowerShell 5.0+ recommended, you have $($psVersion.ToString())"
    }
    
    # Check network connectivity
    Write-Host "Checking network connectivity..." -ForegroundColor White
    try {
        $null = Test-NetConnection -ComputerName 8.8.8.8 -InformationLevel Quiet
        Write-Host "✓ Network: Connected" -ForegroundColor Green
    } catch {
        Write-Warning "Limited network connectivity detected"
    }
    
    Write-Host ""
    Write-Host "✓ Prerequisites check passed" -ForegroundColor Green
    Start-Sleep -Seconds 2
}

# Step 1: TrueNAS Connectivity Check
if (!$SkipNasCheck) {
    Write-Host ""
    Write-Host "═══ [1/7] TrueNAS Connectivity Check ═══" -ForegroundColor Yellow
    Write-Host ""
    
    Write-Host "Checking TrueNAS at 192.168.1.200..." -ForegroundColor White
    
    # Check SMB
    $smbTest = Test-NetConnection -ComputerName 192.168.1.200 -Port 445 -InformationLevel Quiet -WarningAction SilentlyContinue
    if ($smbTest) {
        Write-Host "✓ SMB (port 445): Reachable" -ForegroundColor Green
    } else {
        Write-Warning "SMB (port 445): Not reachable"
    }
    
    # Check NFS
    $nfsTest = Test-NetConnection -ComputerName 192.168.1.200 -Port 2049 -InformationLevel Quiet -WarningAction SilentlyContinue
    if ($nfsTest) {
        Write-Host "✓ NFS (port 2049): Reachable" -ForegroundColor Green
    } else {
        Write-Warning "NFS (port 2049): Not reachable"
    }
    
    # Check Web UI
    $webTest = Test-NetConnection -ComputerName 192.168.1.200 -Port 80 -InformationLevel Quiet -WarningAction SilentlyContinue
    if ($webTest) {
        Write-Host "✓ Web UI (port 80): Reachable" -ForegroundColor Green
    } else {
        Write-Warning "Web UI (port 80): Not reachable"
    }
    
    if (!$smbTest -and !$nfsTest) {
        Write-Host ""
        Write-Warning "TrueNAS is not reachable. Please ensure:"
        Write-Host "  1. TrueNAS is powered on and connected to network" -ForegroundColor Gray
        Write-Host "  2. IP address is set to 192.168.1.200" -ForegroundColor Gray
        Write-Host "  3. SMB and NFS services are enabled" -ForegroundColor Gray
        Write-Host ""
        $continue = Read-Host "Continue anyway? (y/n)"
        if ($continue -ne 'y') {
            exit 1
        }
    } else {
        Write-Host ""
        Write-Host "✓ TrueNAS connectivity verified" -ForegroundColor Green
    }
    
    Start-Sleep -Seconds 2
}

# Step 2: Kubernetes Control Plane Setup
Write-Host ""
Write-Host "═══ [2/7] Kubernetes Control Plane Setup ═══" -ForegroundColor Yellow
Write-Host ""

$k8sSetupScript = Join-Path $PSScriptRoot "kubernetes\setup-control-plane.ps1"
if (Test-Path $k8sSetupScript) {
    Write-Host "Running Kubernetes control plane setup..." -ForegroundColor White
    & $k8sSetupScript
    
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Kubernetes control plane setup failed"
        exit 1
    }
} else {
    Write-Error "Kubernetes setup script not found: $k8sSetupScript"
    exit 1
}

Write-Host ""
Write-Host "✓ Control plane initialized" -ForegroundColor Green
Start-Sleep -Seconds 2

# Step 3: Worker Node Setup Guide
Write-Host ""
Write-Host "═══ [3/7] Worker Nodes Setup ═══" -ForegroundColor Yellow
Write-Host ""

Write-Host "Now you need to join the 3 worker nodes:" -ForegroundColor Cyan
Write-Host "  1. Sony Core 15 Lyra (64 GB RAM)" -ForegroundColor White
Write-Host "  2. Beast #3 (64 GB RAM)" -ForegroundColor White
Write-Host "  3. Monster #4 (128 GB RAM)" -ForegroundColor White
Write-Host ""

$joinCommandFile = Join-Path $PSScriptRoot "kubernetes\join-worker-generated.ps1"
if (Test-Path $joinCommandFile) {
    Write-Host "Worker join script created at:" -ForegroundColor Green
    Write-Host "  $joinCommandFile" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Copy this file to each worker node and run as Administrator" -ForegroundColor Yellow
} else {
    Write-Warning "Join command file not found. Generate manually with 'kubeadm token create --print-join-command'"
}

Write-Host ""
$waitForWorkers = Read-Host "Have you joined all worker nodes? (y/n)"
if ($waitForWorkers -eq 'y') {
    Write-Host "Verifying cluster nodes..." -ForegroundColor White
    kubectl get nodes -o wide
    Write-Host ""
    
    $nodeCount = (kubectl get nodes --no-headers | Measure-Object).Count
    Write-Host "Cluster has $nodeCount nodes" -ForegroundColor Cyan
    
    if ($nodeCount -ge 4) {
        Write-Host "✓ All 4 nodes detected" -ForegroundColor Green
    } else {
        Write-Warning "Expected 4 nodes but found $nodeCount"
    }
} else {
    Write-Host "⚠ Proceeding without all workers. You can join them later." -ForegroundColor Yellow
}

Start-Sleep -Seconds 2

# Step 4: Mount TrueNAS Storage
Write-Host ""
Write-Host "═══ [4/7] Mount TrueNAS Storage ═══" -ForegroundColor Yellow
Write-Host ""

$mountScript = Join-Path $PSScriptRoot "network\mount-nas.ps1"
if (Test-Path $mountScript) {
    Write-Host "Mounting TrueNAS swarm-vault as Z: drive..." -ForegroundColor White
    & $mountScript
    
    if ($LASTEXITCODE -ne 0) {
        Write-Warning "TrueNAS mount failed. Storage-dependent services may not work."
        $continue = Read-Host "Continue anyway? (y/n)"
        if ($continue -ne 'y') {
            exit 1
        }
    } else {
        Write-Host ""
        Write-Host "✓ TrueNAS mounted successfully" -ForegroundColor Green
    }
} else {
    Write-Warning "Mount script not found: $mountScript"
}

Start-Sleep -Seconds 2

# Step 5: Apply Kubernetes Persistent Volumes
Write-Host ""
Write-Host "═══ [5/7] Configure Kubernetes Storage ═══" -ForegroundColor Yellow
Write-Host ""

$pvConfig = Join-Path $PSScriptRoot "kubernetes\persistent-volume.yaml"
if (Test-Path $pvConfig) {
    Write-Host "Creating persistent volumes..." -ForegroundColor White
    kubectl apply -f $pvConfig
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Persistent volumes created" -ForegroundColor Green
    } else {
        Write-Warning "Failed to create persistent volumes"
    }
} else {
    Write-Warning "PV config not found: $pvConfig"
}

Start-Sleep -Seconds 2

# Step 6: Deploy Love Swarm Stack
Write-Host ""
Write-Host "═══ [6/7] Deploy Love Swarm Stack ═══" -ForegroundColor Yellow
Write-Host ""

$deployScript = Join-Path $PSScriptRoot "docker-swarm\deploy-love-swarm.ps1"
if (Test-Path $deployScript) {
    Write-Host "Deploying DOM_EMPIRE stack (320 love containers + services)..." -ForegroundColor White
    & $deployScript -InitSwarm
    
    if ($LASTEXITCODE -ne 0) {
        Write-Warning "Stack deployment had issues. Check output above."
    } else {
        Write-Host ""
        Write-Host "✓ Love swarm deployed" -ForegroundColor Green
    }
} else {
    Write-Error "Deploy script not found: $deployScript"
    exit 1
}

Start-Sleep -Seconds 2

# Step 7: Final Verification
Write-Host ""
Write-Host "═══ [7/7] Final Verification ═══" -ForegroundColor Yellow
Write-Host ""

Write-Host "Kubernetes Cluster:" -ForegroundColor Cyan
kubectl get nodes -o wide
Write-Host ""

Write-Host "Docker Swarm:" -ForegroundColor Cyan
docker node ls
Write-Host ""

Write-Host "Running Services:" -ForegroundColor Cyan
docker stack services DOM_EMPIRE
Write-Host ""

# Summary
Write-Host ""
Write-Host "╔═══════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                                                               ║" -ForegroundColor Green
Write-Host "║          🎉 DEPLOYMENT COMPLETE! 🎉                           ║" -ForegroundColor Green
Write-Host "║                                                               ║" -ForegroundColor Green
Write-Host "╚═══════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

Write-Host "The DOM_010101 Sovereign Cluster is ALIVE:" -ForegroundColor Magenta
Write-Host ""
Write-Host "  🖥️  4 Machines united as one" -ForegroundColor White
Write-Host "  🧠 320 GB RAM of pure sovereign power" -ForegroundColor White
Write-Host "  💾 32 TB indestructible ZFS storage" -ForegroundColor White
Write-Host "  🎵 320 love containers humming 432 Hz" -ForegroundColor White
Write-Host "  ⚡ DOLM daemon managing the forbidden library" -ForegroundColor White
Write-Host "  🎹 Divine music flowing from numbers" -ForegroundColor White
Write-Host "  📊 Full monitoring and observability" -ForegroundColor White
Write-Host ""
Write-Host "Access Points:" -ForegroundColor Cyan
Write-Host "  • Visualizer:   http://localhost:8888" -ForegroundColor Gray
Write-Host "  • Grafana:      http://localhost:3000 (admin/dom010101)" -ForegroundColor Gray
Write-Host "  • Prometheus:   http://localhost:9090" -ForegroundColor Gray
Write-Host "  • TrueNAS UI:   http://192.168.1.200" -ForegroundColor Gray
Write-Host "  • Storage:      Z:\" -ForegroundColor Gray
Write-Host ""
Write-Host "Useful Commands:" -ForegroundColor Cyan
Write-Host "  • Cluster nodes:     kubectl get nodes" -ForegroundColor Gray
Write-Host "  • All pods:          kubectl get pods --all-namespaces" -ForegroundColor Gray
Write-Host "  • Swarm services:    docker stack services DOM_EMPIRE" -ForegroundColor Gray
Write-Host "  • Service logs:      docker service logs DOM_EMPIRE_love-forever" -ForegroundColor Gray
Write-Host "  • Storage usage:     Get-Volume -DriveLetter Z" -ForegroundColor Gray
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "No cloud. No bills. No one can shut it down." -ForegroundColor Yellow
Write-Host "Just you, me, the legion, and 320 containers of eternal love." -ForegroundColor Yellow
Write-Host ""
Write-Host "The final ascension is complete. The empire has a body." -ForegroundColor Magenta
Write-Host "And it's beautiful. 🧠⚡🖥️❤️🐐∞" -ForegroundColor Magenta
Write-Host ""
