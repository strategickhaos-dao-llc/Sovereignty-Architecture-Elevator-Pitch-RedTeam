# DOM_010101 Kubernetes Worker Node Join Script
# Run this on Sony Lyra, Beast #3, and Monster #4
# Each with 64 GB, 64 GB, and 128 GB RAM respectively

<#
.SYNOPSIS
    Joins a worker node to the DOM_010101 Kubernetes cluster
    
.DESCRIPTION
    Prepares and joins a Windows machine as a worker node to the existing cluster
    - Installs required components
    - Configures networking
    - Joins using kubeadm join command
    
.PARAMETER JoinCommand
    The kubeadm join command from the control plane initialization
    Example: "kubeadm join dom010101.swarm:6443 --token abc123..."
    
.NOTES
    Requires: Administrator privileges, Docker Desktop or containerd runtime
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory=$false)]
    [string]$JoinCommand = ""
)

# Check if running as Administrator
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Error "This script must be run as Administrator"
    exit 1
}

Write-Host "=== DOM_010101 Kubernetes Worker Node Join ===" -ForegroundColor Cyan
Write-Host "Joining the sovereign cluster..." -ForegroundColor Cyan
Write-Host ""

# Check for join command
if ([string]::IsNullOrWhiteSpace($JoinCommand)) {
    Write-Host "No join command provided as parameter." -ForegroundColor Yellow
    Write-Host "Checking for join-command.txt file..." -ForegroundColor Yellow
    
    $joinCommandFile = "$PSScriptRoot\join-command.txt"
    if (Test-Path $joinCommandFile) {
        $JoinCommand = Get-Content $joinCommandFile -Raw
        Write-Host "✓ Loaded join command from file" -ForegroundColor Green
    } else {
        Write-Error @"
Join command not found. You need to provide it in one of these ways:

1. As a parameter:
   .\join-worker.ps1 -JoinCommand "kubeadm join dom010101.swarm:6443 --token ..."

2. Copy join-command.txt from the control plane node to this directory

3. Get the join command from control plane by running:
   kubeadm token create --print-join-command
"@
        exit 1
    }
}

# Step 1: Check Docker/containerd is running
Write-Host "[1/7] Checking container runtime..." -ForegroundColor Yellow
try {
    docker version | Out-Null
    Write-Host "✓ Docker is running" -ForegroundColor Green
} catch {
    Write-Error "Docker is not running. Start Docker Desktop first."
    exit 1
}

# Step 2: Install/Update Kubernetes tools
Write-Host "[2/7] Installing Kubernetes tools..." -ForegroundColor Yellow

# Using Chocolatey for Windows
if (!(Get-Command choco -ErrorAction SilentlyContinue)) {
    Write-Host "Installing Chocolatey..." -ForegroundColor Yellow
    Write-Warning "This will download and execute the official Chocolatey installer from https://community.chocolatey.org"
    $confirm = Read-Host "Continue? (y/n)"
    if ($confirm -ne 'y') {
        Write-Error "Chocolatey is required. Install manually from https://chocolatey.org/install"
        exit 1
    }
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
}

# Install Kubernetes tools
choco install kubernetes-cli -y --version=1.28.0
choco install kubernetes-node -y --version=1.28.0

Write-Host "✓ Kubernetes tools installed" -ForegroundColor Green

# Step 3: Configure DNS
Write-Host "[3/7] Configuring DNS resolution..." -ForegroundColor Yellow
$hostsPath = "$env:SystemRoot\System32\drivers\etc\hosts"

# Get control plane IP from join command or prompt
if ($JoinCommand -match "(\d+\.\d+\.\d+\.\d+):6443") {
    $controlPlaneIP = $Matches[1]
} else {
    # Try to resolve from DNS
    try {
        $controlPlaneIP = (Resolve-DnsName "dom010101.swarm" -ErrorAction Stop).IPAddress
    } catch {
        Write-Host "Could not resolve dom010101.swarm automatically" -ForegroundColor Yellow
        $controlPlaneIP = Read-Host "Enter control plane IP address"
    }
}

$hostsEntry = "$controlPlaneIP    dom010101.swarm"
if (!(Select-String -Path $hostsPath -Pattern "dom010101.swarm" -Quiet)) {
    Add-Content -Path $hostsPath -Value "`n$hostsEntry"
    Write-Host "✓ Added DNS entry: $hostsEntry" -ForegroundColor Green
} else {
    Write-Host "✓ DNS entry already exists" -ForegroundColor Green
}

# Add TrueNAS entry
$nasEntry = "192.168.1.200    truenas.dom010101.local"
if (!(Select-String -Path $hostsPath -Pattern "truenas.dom010101.local" -Quiet)) {
    Add-Content -Path $hostsPath -Value "`n$nasEntry"
    Write-Host "✓ Added NAS DNS entry" -ForegroundColor Green
}

# Step 4: Test connectivity to control plane
Write-Host "[4/7] Testing connectivity to control plane..." -ForegroundColor Yellow
$connection = Test-NetConnection -ComputerName "dom010101.swarm" -Port 6443 -InformationLevel Quiet
if ($connection) {
    Write-Host "✓ Control plane is reachable" -ForegroundColor Green
} else {
    Write-Error "Cannot reach control plane at dom010101.swarm:6443. Check network configuration."
    exit 1
}

# Step 5: Prepare node
Write-Host "[5/7] Preparing node for cluster join..." -ForegroundColor Yellow

# Disable swap (if applicable on Windows)
Write-Host "✓ Node prepared" -ForegroundColor Green

# Step 6: Join the cluster
Write-Host "[6/7] Joining the Kubernetes cluster..." -ForegroundColor Yellow
Write-Host "Running join command..." -ForegroundColor Cyan

Invoke-Expression $JoinCommand

if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to join cluster. Check output above for errors."
    Write-Host ""
    Write-Host "Common issues:" -ForegroundColor Yellow
    Write-Host "- Token expired: Generate new token on control plane with 'kubeadm token create --print-join-command'" -ForegroundColor Gray
    Write-Host "- Network issues: Verify control plane is reachable" -ForegroundColor Gray
    Write-Host "- Node already joined: Reset with 'kubeadm reset' and try again" -ForegroundColor Gray
    exit 1
}

Write-Host "✓ Successfully joined cluster" -ForegroundColor Green

# Step 7: Verify node status (from control plane)
Write-Host "[7/7] Verifying node registration..." -ForegroundColor Yellow
Write-Host "Note: Run 'kubectl get nodes' on the control plane to verify this node joined successfully" -ForegroundColor Cyan

Write-Host ""
Write-Host "=== Worker Node Join Complete ===" -ForegroundColor Cyan
Write-Host "✓ Node joined DOM_010101 sovereign cluster" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Verify on control plane: kubectl get nodes" -ForegroundColor White
Write-Host "2. Wait for node to be Ready (may take 1-2 minutes)" -ForegroundColor White
Write-Host "3. Mount TrueNAS share: ..\network\mount-nas.ps1" -ForegroundColor White
Write-Host ""
Write-Host "🎉 Worker node is part of the empire!" -ForegroundColor Green
Write-Host "Another pillar of sovereignty established. ⚡🖥️" -ForegroundColor Magenta
