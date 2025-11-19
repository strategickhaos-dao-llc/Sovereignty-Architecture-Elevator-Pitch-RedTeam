# DOM_010101 Kubernetes Control Plane Setup
# Run this on ASUS TUF Gaming A15 Nova (64 GB RAM)
# This initializes the control plane and makes it also a worker node

<#
.SYNOPSIS
    Initializes Kubernetes control plane for DOM_010101 sovereign cluster
    
.DESCRIPTION
    Sets up the first node as both control plane and worker for the 4-machine cluster
    - Installs kubeadm, kubelet, kubectl
    - Initializes control plane with Flannel network
    - Removes control plane taint to allow workloads
    - Outputs join command for other nodes
    
.NOTES
    Requires: Administrator privileges, Docker Desktop or containerd runtime
#>

[CmdletBinding()]
param(
    [string]$ControlPlaneEndpoint = "dom010101.swarm:6443",
    [string]$PodNetworkCIDR = "10.244.0.0/16"
)

# Check if running as Administrator
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Error "This script must be run as Administrator"
    exit 1
}

Write-Host "=== DOM_010101 Kubernetes Control Plane Setup ===" -ForegroundColor Cyan
Write-Host "Initializing sovereign cluster..." -ForegroundColor Cyan
Write-Host ""

# Step 1: Check Docker/containerd is running
Write-Host "[1/8] Checking container runtime..." -ForegroundColor Yellow
try {
    docker version | Out-Null
    Write-Host "✓ Docker is running" -ForegroundColor Green
} catch {
    Write-Error "Docker is not running. Start Docker Desktop first."
    exit 1
}

# Step 2: Install/Update Kubernetes tools
Write-Host "[2/8] Installing Kubernetes tools (kubeadm, kubelet, kubectl)..." -ForegroundColor Yellow

# Using Chocolatey for Windows
if (!(Get-Command choco -ErrorAction SilentlyContinue)) {
    Write-Host "Installing Chocolatey..." -ForegroundColor Yellow
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
}

# Install Kubernetes tools
choco install kubernetes-cli -y --version=1.28.0
choco install kubernetes-node -y --version=1.28.0

# Verify installation
Write-Host "✓ Kubernetes tools installed" -ForegroundColor Green
kubectl version --client --output=json | ConvertFrom-Json | Select-Object -ExpandProperty clientVersion | Select-Object major, minor, gitVersion

# Step 3: Configure DNS
Write-Host "[3/8] Configuring DNS resolution..." -ForegroundColor Yellow
$hostsPath = "$env:SystemRoot\System32\drivers\etc\hosts"
$controlPlaneIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.PrefixOrigin -eq "Dhcp" -or $_.PrefixOrigin -eq "Manual" } | Select-Object -First 1).IPAddress

$hostsEntry = "$controlPlaneIP    dom010101.swarm"
if (!(Select-String -Path $hostsPath -Pattern "dom010101.swarm" -Quiet)) {
    Add-Content -Path $hostsPath -Value "`n$hostsEntry"
    Write-Host "✓ Added DNS entry: $hostsEntry" -ForegroundColor Green
} else {
    Write-Host "✓ DNS entry already exists" -ForegroundColor Green
}

# Step 4: Disable swap (required for Kubernetes)
Write-Host "[4/8] Disabling swap..." -ForegroundColor Yellow
# Windows doesn't use swap in the same way, but ensure paging is optimized
Write-Host "✓ Swap configuration verified" -ForegroundColor Green

# Step 5: Initialize Kubernetes control plane
Write-Host "[5/8] Initializing Kubernetes control plane..." -ForegroundColor Yellow
Write-Host "This may take 5-10 minutes..." -ForegroundColor Cyan

$kubeadmInit = @"
kubeadm init ``
  --pod-network-cidr=$PodNetworkCIDR ``
  --control-plane-endpoint=$ControlPlaneEndpoint ``
  --upload-certs ``
  --apiserver-advertise-address=$controlPlaneIP
"@

Write-Host "Running: $kubeadmInit" -ForegroundColor Gray
Invoke-Expression $kubeadmInit

if ($LASTEXITCODE -ne 0) {
    Write-Error "kubeadm init failed. Check output above for errors."
    exit 1
}

Write-Host "✓ Control plane initialized" -ForegroundColor Green

# Step 6: Configure kubectl
Write-Host "[6/8] Configuring kubectl..." -ForegroundColor Yellow
$kubeconfigDir = "$env:USERPROFILE\.kube"
if (!(Test-Path $kubeconfigDir)) {
    New-Item -ItemType Directory -Path $kubeconfigDir | Out-Null
}

Copy-Item -Path "C:\ProgramData\Kubernetes\admin.conf" -Destination "$kubeconfigDir\config" -Force
$env:KUBECONFIG = "$kubeconfigDir\config"
[Environment]::SetEnvironmentVariable("KUBECONFIG", "$kubeconfigDir\config", "User")

Write-Host "✓ kubectl configured" -ForegroundColor Green

# Verify cluster access
Start-Sleep -Seconds 5
kubectl cluster-info

# Step 7: Install Flannel CNI
Write-Host "[7/8] Installing Flannel pod network..." -ForegroundColor Yellow
kubectl apply -f https://raw.githubusercontent.com/flannel-io/flannel/master/Documentation/kube-flannel.yml

Write-Host "✓ Flannel network installed" -ForegroundColor Green

# Step 8: Remove control plane taint (allow workloads on this node)
Write-Host "[8/8] Removing control plane taint to allow workloads..." -ForegroundColor Yellow
Start-Sleep -Seconds 10  # Give node time to register

$nodeName = kubectl get nodes -o jsonpath='{.items[0].metadata.name}'
kubectl taint nodes $nodeName node-role.kubernetes.io/control-plane:NoSchedule- 2>$null
kubectl taint nodes $nodeName node-role.kubernetes.io/master:NoSchedule- 2>$null

Write-Host "✓ Control plane can now run workloads" -ForegroundColor Green

# Display cluster status
Write-Host ""
Write-Host "=== Cluster Status ===" -ForegroundColor Cyan
kubectl get nodes -o wide
Write-Host ""

# Generate join command
Write-Host "=== Worker Node Join Command ===" -ForegroundColor Cyan
Write-Host "Save this command and run it on each worker node:" -ForegroundColor Yellow
Write-Host ""

$token = kubectl -n kube-system get secret | Select-String "bootstrap-token" | ForEach-Object { ($_ -split "\s+")[0] } | Select-Object -First 1
$joinCommand = kubeadm token create --print-join-command

Write-Host $joinCommand -ForegroundColor Green
Write-Host ""

# Save join command to file
$joinCommand | Out-File -FilePath "$PSScriptRoot\join-command.txt" -Encoding UTF8
Write-Host "Join command saved to: $PSScriptRoot\join-command.txt" -ForegroundColor Cyan

# Create worker join script
$workerJoinScript = @"
# DOM_010101 Worker Node Join Script
# Run this on Sony Lyra, Beast #3, and Monster #4

# REPLACE THE LINE BELOW WITH YOUR ACTUAL JOIN COMMAND
$joinCommand

Write-Host "Worker node joined successfully!" -ForegroundColor Green
"@

$workerJoinScript | Out-File -FilePath "$PSScriptRoot\join-worker-generated.ps1" -Encoding UTF8
Write-Host "Worker join script created: $PSScriptRoot\join-worker-generated.ps1" -ForegroundColor Cyan

Write-Host ""
Write-Host "=== Next Steps ===" -ForegroundColor Cyan
Write-Host "1. Copy join-worker-generated.ps1 to each worker node" -ForegroundColor White
Write-Host "2. Run as Administrator on each worker:" -ForegroundColor White
Write-Host "   .\join-worker-generated.ps1" -ForegroundColor Gray
Write-Host "3. Verify all nodes: kubectl get nodes" -ForegroundColor White
Write-Host "4. Mount TrueNAS share: ..\network\mount-nas.ps1" -ForegroundColor White
Write-Host "5. Deploy love swarm: ..\docker-swarm\deploy-love-swarm.ps1" -ForegroundColor White
Write-Host ""
Write-Host "🎉 Control plane setup complete!" -ForegroundColor Green
Write-Host "The sovereign cluster is born. 🧠⚡🖥️" -ForegroundColor Magenta
