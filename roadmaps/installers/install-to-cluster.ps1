#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Install roadmap to all nodes in the cluster
.DESCRIPTION
    Deploys selected roadmap (A, B, or C) to specified nodes or auto-discovers
    nodes via Tailscale. Includes RAG indexing for heir knowledge transfer.
.PARAMETER Roadmap
    Which roadmap to install (A, B, or C)
.PARAMETER Nodes
    Array of node names/IPs to deploy to
.PARAMETER AutoDiscover
    Auto-discover nodes via Tailscale status
.PARAMETER IndexRAG
    Enable RAG indexing after installation
#>

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("A", "B", "C")]
    [string]$Roadmap,
    
    [string[]]$Nodes = @(),
    [switch]$AutoDiscover,
    [switch]$IndexRAG = $true
)

$ErrorActionPreference = "Stop"

Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  CLUSTER DEPLOYMENT - Roadmap $Roadmap" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Auto-discover nodes if requested
if ($AutoDiscover) {
    Write-Host "Auto-discovering nodes via Tailscale..." -ForegroundColor Yellow
    
    if (Get-Command tailscale -ErrorAction SilentlyContinue) {
        $status = tailscale status --json 2>$null | ConvertFrom-Json
        if ($status.Peer) {
            $Nodes = $status.Peer.PSObject.Properties | ForEach-Object {
                $peer = $_.Value
                if ($peer.HostName) {
                    $peer.HostName
                }
            }
            Write-Host "  Found $($Nodes.Count) nodes: $($Nodes -join ', ')" -ForegroundColor Green
        } else {
            Write-Host "  No peers found in Tailscale status" -ForegroundColor Red
            exit 1
        }
    } else {
        Write-Host "  Tailscale CLI not found. Please install or specify nodes manually." -ForegroundColor Red
        exit 1
    }
}

if ($Nodes.Count -eq 0) {
    Write-Host "No nodes specified. Use -Nodes or -AutoDiscover" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Deploying Roadmap $Roadmap to $($Nodes.Count) nodes..." -ForegroundColor Green
Write-Host ""

# Get roadmap path
$roadmapPath = Join-Path $PSScriptRoot "../roadmap-$($Roadmap.ToLower())"
if (-not (Test-Path $roadmapPath)) {
    Write-Host "Roadmap $Roadmap not found at: $roadmapPath" -ForegroundColor Red
    exit 1
}

# Create deployment package
Write-Host "[1/4] Creating deployment package..." -ForegroundColor Yellow
$tempDir = Join-Path ([System.IO.Path]::GetTempPath()) "roadmap-$Roadmap-deploy"
if (Test-Path $tempDir) {
    Remove-Item -Recurse -Force $tempDir
}
New-Item -ItemType Directory -Path $tempDir | Out-Null

# Copy roadmap files
Copy-Item -Recurse "$roadmapPath/*" $tempDir

# Create deployment manifest
$manifest = @{
    Roadmap = $Roadmap
    DeployedAt = Get-Date -Format "o"
    DeployedBy = $env:USERNAME
    DeployedFrom = $env:COMPUTERNAME
    Version = "1.0.0"
    Nodes = $Nodes
}
$manifest | ConvertTo-Json | Set-Content (Join-Path $tempDir "deployment-manifest.json")

Write-Host "  ✓ Package created: $tempDir" -ForegroundColor Green

# Deploy to each node
Write-Host ""
Write-Host "[2/4] Deploying to nodes..." -ForegroundColor Yellow

$successCount = 0
$failCount = 0

foreach ($node in $Nodes) {
    Write-Host "  → $node..." -NoNewline
    
    try {
        # Check if node is reachable
        $pingResult = Test-Connection -ComputerName $node -Count 1 -Quiet -ErrorAction SilentlyContinue
        
        if ($pingResult) {
            # Use rsync if available, otherwise scp
            $targetPath = "/opt/sovereignty-roadmap-$($Roadmap.ToLower())"
            
            if (Get-Command rsync -ErrorAction SilentlyContinue) {
                rsync -avz --quiet $tempDir/ "${node}:${targetPath}/" 2>$null
            } elseif (Get-Command scp -ErrorAction SilentlyContinue) {
                scp -r -q $tempDir/* "${node}:${targetPath}/" 2>$null
            } else {
                # Fallback: Create archive and transfer
                $archivePath = Join-Path ([System.IO.Path]::GetTempPath()) "roadmap-$Roadmap.tar.gz"
                tar -czf $archivePath -C $tempDir . 2>$null
                scp -q $archivePath "${node}:/tmp/" 2>$null
                ssh $node "mkdir -p $targetPath && tar -xzf /tmp/roadmap-$Roadmap.tar.gz -C $targetPath && rm /tmp/roadmap-$Roadmap.tar.gz" 2>$null
                Remove-Item $archivePath -ErrorAction SilentlyContinue
            }
            
            Write-Host " ✓" -ForegroundColor Green
            $successCount++
        } else {
            Write-Host " ✗ (unreachable)" -ForegroundColor Red
            $failCount++
        }
    } catch {
        Write-Host " ✗ ($($_.Exception.Message))" -ForegroundColor Red
        $failCount++
    }
}

Write-Host ""
Write-Host "  Deployed: $successCount/$($Nodes.Count) nodes" -ForegroundColor $(if ($failCount -eq 0) { "Green" } else { "Yellow" })

# Index for RAG if requested
if ($IndexRAG -and $successCount -gt 0) {
    Write-Host ""
    Write-Host "[3/4] Indexing for RAG..." -ForegroundColor Yellow
    
    $indexScript = Join-Path $PSScriptRoot "index-for-rag.ps1"
    if (Test-Path $indexScript) {
        & $indexScript -Roadmap $Roadmap -Nodes $Nodes
        Write-Host "  ✓ RAG indexing complete" -ForegroundColor Green
    } else {
        Write-Host "  ⚠ RAG indexing script not found, skipping..." -ForegroundColor Yellow
    }
}

# Verify installation
Write-Host ""
Write-Host "[4/4] Verifying installation..." -ForegroundColor Yellow

foreach ($node in $Nodes) {
    Write-Host "  → $node..." -NoNewline
    
    try {
        $targetPath = "/opt/sovereignty-roadmap-$($Roadmap.ToLower())"
        $result = ssh $node "test -f $targetPath/README.md && echo 'OK' || echo 'FAIL'" 2>$null
        
        if ($result -match "OK") {
            Write-Host " ✓" -ForegroundColor Green
        } else {
            Write-Host " ✗" -ForegroundColor Red
        }
    } catch {
        Write-Host " ✗" -ForegroundColor Red
    }
}

# Cleanup
Remove-Item -Recurse -Force $tempDir -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  DEPLOYMENT COMPLETE" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

if ($failCount -eq 0) {
    Write-Host "✓ All nodes deployed successfully!" -ForegroundColor Green
} else {
    Write-Host "⚠ $failCount/$($Nodes.Count) nodes failed to deploy" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Roadmap installed at: /opt/sovereignty-roadmap-$($Roadmap.ToLower())" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps on each node:" -ForegroundColor Yellow

switch ($Roadmap) {
    "A" {
        Write-Host "  1. cd /opt/sovereignty-roadmap-a" -ForegroundColor Gray
        Write-Host "  2. ./scripts/02-clean-artifacts.ps1 -DryRun" -ForegroundColor Gray
    }
    "B" {
        Write-Host "  1. cd /opt/sovereignty-roadmap-b" -ForegroundColor Gray
        Write-Host "  2. ./diagnose-patterns.ps1" -ForegroundColor Gray
    }
    "C" {
        Write-Host "  1. cd /opt/sovereignty-roadmap-c" -ForegroundColor Gray
        Write-Host "  2. ./install-obsidian-vault.ps1" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "RAG queries available at: http://<node>:8000/rag/query" -ForegroundColor Cyan
Write-Host ""
