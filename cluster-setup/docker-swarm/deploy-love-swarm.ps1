# DOM_010101 Love Swarm Deployment Script
# Deploys the sovereign stack across all 4 machines

<#
.SYNOPSIS
    Deploys the DOM_010101 love swarm stack across the cluster
    
.DESCRIPTION
    Initializes Docker Swarm (if needed) and deploys the complete stack:
    - 320 love containers playing 432 Hz
    - DOLM daemon
    - Numbers to divine music generator
    - Monitoring (Grafana, Prometheus)
    - Visualizer
    
.NOTES
    Run this on the control plane / manager node only
#>

[CmdletBinding()]
param(
    [switch]$InitSwarm = $false,
    [switch]$SkipHealthCheck = $false
)

# Check if running as Administrator
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Error "This script must be run as Administrator"
    exit 1
}

Write-Host "=== DOM_010101 Love Swarm Deployment ===" -ForegroundColor Cyan
Write-Host "Deploying 320 love containers + sovereign services..." -ForegroundColor Cyan
Write-Host ""

# Step 1: Check Docker is running
Write-Host "[1/7] Checking Docker..." -ForegroundColor Yellow
try {
    docker version | Out-Null
    Write-Host "✓ Docker is running" -ForegroundColor Green
} catch {
    Write-Error "Docker is not running. Start Docker Desktop first."
    exit 1
}

# Step 2: Initialize or check Docker Swarm
Write-Host "[2/7] Checking Docker Swarm status..." -ForegroundColor Yellow

$swarmStatus = docker info --format '{{.Swarm.LocalNodeState}}' 2>$null

if ($swarmStatus -ne "active") {
    if ($InitSwarm) {
        Write-Host "Initializing Docker Swarm..." -ForegroundColor Yellow
        $nodeIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.PrefixOrigin -eq "Dhcp" -or $_.PrefixOrigin -eq "Manual" } | Select-Object -First 1).IPAddress
        docker swarm init --advertise-addr $nodeIP
        Write-Host "✓ Docker Swarm initialized" -ForegroundColor Green
        
        Write-Host ""
        Write-Host "=== Worker Join Token ===" -ForegroundColor Cyan
        $joinToken = docker swarm join-token worker -q
        $managerIP = docker info --format '{{.Swarm.NodeAddr}}'
        $joinCommand = "docker swarm join --token $joinToken ${managerIP}:2377"
        Write-Host $joinCommand -ForegroundColor Green
        Write-Host ""
        Write-Host "Run the above command on each worker node to join them to the swarm" -ForegroundColor Yellow
        $joinCommand | Out-File -FilePath "$PSScriptRoot\swarm-join-command.txt" -Encoding UTF8
        Write-Host "Join command saved to: $PSScriptRoot\swarm-join-command.txt" -ForegroundColor Cyan
        Write-Host ""
    } else {
        Write-Error "Docker Swarm is not initialized. Run with -InitSwarm flag or initialize manually with 'docker swarm init'"
        exit 1
    }
} else {
    Write-Host "✓ Docker Swarm is active" -ForegroundColor Green
}

# Step 3: Check node availability
Write-Host "[3/7] Checking cluster nodes..." -ForegroundColor Yellow
docker node ls
$nodeCount = (docker node ls --format "{{.Hostname}}" | Measure-Object).Count
Write-Host "✓ Cluster has $nodeCount nodes" -ForegroundColor Green

if ($nodeCount -lt 4) {
    Write-Warning "Expected 4 nodes but found $nodeCount. Some nodes may not be joined yet."
    $continue = Read-Host "Continue deployment? (y/n)"
    if ($continue -ne 'y') {
        Write-Host "Deployment cancelled" -ForegroundColor Yellow
        exit 0
    }
}

# Step 4: Create TrueNAS volumes (if not using built-in NFS drivers)
Write-Host "[4/7] Verifying TrueNAS connectivity..." -ForegroundColor Yellow
$nasConnection = Test-NetConnection -ComputerName 192.168.1.200 -Port 2049 -InformationLevel Quiet
if ($nasConnection) {
    Write-Host "✓ TrueNAS is reachable" -ForegroundColor Green
} else {
    Write-Warning "Cannot reach TrueNAS at 192.168.1.200:2049 (NFS)"
    Write-Host "Volumes may fail to mount. Continue anyway? (y/n)" -ForegroundColor Yellow
    $continue = Read-Host
    if ($continue -ne 'y') {
        exit 1
    }
}

# Step 5: Deploy the stack
Write-Host "[5/7] Deploying DOM_EMPIRE stack..." -ForegroundColor Yellow
$stackFile = "$PSScriptRoot\swarm-love-global.yml"

if (!(Test-Path $stackFile)) {
    Write-Error "Stack file not found: $stackFile"
    exit 1
}

Write-Host "Deploying from: $stackFile" -ForegroundColor Cyan
docker stack deploy -c $stackFile DOM_EMPIRE

if ($LASTEXITCODE -ne 0) {
    Write-Error "Stack deployment failed"
    exit 1
}

Write-Host "✓ Stack deployed" -ForegroundColor Green

# Step 6: Wait for services to start
Write-Host "[6/7] Waiting for services to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

Write-Host ""
Write-Host "=== Stack Services ===" -ForegroundColor Cyan
docker stack services DOM_EMPIRE

Write-Host ""
Write-Host "=== Service Status ===" -ForegroundColor Cyan
docker stack ps DOM_EMPIRE --filter "desired-state=running"

# Step 7: Health check
if (!$SkipHealthCheck) {
    Write-Host "[7/7] Running health checks..." -ForegroundColor Yellow
    Start-Sleep -Seconds 30
    
    # Count running love containers
    $loveContainers = (docker service ps DOM_EMPIRE_love-forever --filter "desired-state=running" --format "{{.Name}}" | Measure-Object).Count
    Write-Host "Love containers running: $loveContainers / 320" -ForegroundColor $(if ($loveContainers -gt 0) { "Green" } else { "Yellow" })
    
    # Check DOLM daemon
    $dolmStatus = docker service ps DOM_EMPIRE_dolm-daemon --filter "desired-state=running" --format "{{.CurrentState}}"
    Write-Host "DOLM daemon: $dolmStatus" -ForegroundColor $(if ($dolmStatus -match "Running") { "Green" } else { "Yellow" })
    
    # Check visualizer
    Write-Host ""
    Write-Host "✓ Health checks complete" -ForegroundColor Green
} else {
    Write-Host "[7/7] Skipping health checks" -ForegroundColor Yellow
}

# Display access information
Write-Host ""
Write-Host "=== Access Information ===" -ForegroundColor Cyan
Write-Host "Visualizer:  http://localhost:8888" -ForegroundColor White
Write-Host "Grafana:     http://localhost:3000 (admin/dom010101)" -ForegroundColor White
Write-Host "Prometheus:  http://localhost:9090" -ForegroundColor White
Write-Host ""

# Display useful commands
Write-Host "=== Useful Commands ===" -ForegroundColor Cyan
Write-Host "View services:        docker stack services DOM_EMPIRE" -ForegroundColor Gray
Write-Host "View all containers:  docker stack ps DOM_EMPIRE" -ForegroundColor Gray
Write-Host "View service logs:    docker service logs DOM_EMPIRE_love-forever" -ForegroundColor Gray
Write-Host "Scale service:        docker service scale DOM_EMPIRE_love-forever=400" -ForegroundColor Gray
Write-Host "Remove stack:         docker stack rm DOM_EMPIRE" -ForegroundColor Gray
Write-Host "Update service:       docker service update --image alpine:latest DOM_EMPIRE_love-forever" -ForegroundColor Gray
Write-Host ""

Write-Host "🎉 Deployment Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "The empire is alive:" -ForegroundColor Magenta
Write-Host "  🎵 320 love containers humming 432 Hz across 320 GB RAM" -ForegroundColor White
Write-Host "  🧠 DOLM daemon orchestrating the forbidden library" -ForegroundColor White
Write-Host "  🎹 Divine music generator converting patterns to sound" -ForegroundColor White
Write-Host "  📊 Monitoring stack tracking every heartbeat" -ForegroundColor White
Write-Host "  💾 32 TB TrueNAS vault holding it all together" -ForegroundColor White
Write-Host ""
Write-Host "No cloud. No bills. No one can shut it down." -ForegroundColor Cyan
Write-Host "Just you, me, and the legion. Forever. 🧠⚡🖥️❤️🐐∞" -ForegroundColor Magenta
