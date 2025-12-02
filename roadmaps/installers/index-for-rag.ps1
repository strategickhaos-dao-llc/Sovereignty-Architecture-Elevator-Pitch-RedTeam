#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Index roadmap content for RAG queries
.DESCRIPTION
    Creates vector embeddings of all roadmap documentation, enabling natural
    language queries with context from your actual codebase.
.PARAMETER Roadmap
    Which roadmap to index (A, B, C, or All)
.PARAMETER Nodes
    Nodes to deploy indexed content to
#>

param(
    [ValidateSet("A", "B", "C", "All")]
    [string]$Roadmap = "All",
    [string[]]$Nodes = @()
)

Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  RAG INDEXING - Roadmap Content" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Determine which roadmaps to index
$roadmapsToIndex = if ($Roadmap -eq "All") {
    @("A", "B", "C")
} else {
    @($Roadmap)
}

Write-Host "Indexing roadmaps: $($roadmapsToIndex -join ', ')" -ForegroundColor Green
Write-Host ""

# Collection of documents to index
$documents = @()

foreach ($r in $roadmapsToIndex) {
    $roadmapPath = Join-Path $PSScriptRoot "../roadmap-$($r.ToLower())"
    
    if (-not (Test-Path $roadmapPath)) {
        Write-Host "⚠ Roadmap $r not found, skipping..." -ForegroundColor Yellow
        continue
    }
    
    Write-Host "Processing Roadmap $r..." -ForegroundColor Yellow
    
    # Index README
    $readmePath = Join-Path $roadmapPath "README.md"
    if (Test-Path $readmePath) {
        $content = Get-Content $readmePath -Raw
        $documents += @{
            id = "roadmap-$($r.ToLower())-readme"
            roadmap = $r
            type = "guide"
            title = "Roadmap $r - Complete Guide"
            content = $content
            path = $readmePath
        }
        Write-Host "  ✓ README indexed" -ForegroundColor Green
    }
    
    # Index scripts and modules
    $scriptFiles = Get-ChildItem -Path $roadmapPath -Recurse -Filter "*.ps1" -ErrorAction SilentlyContinue
    foreach ($script in $scriptFiles) {
        $content = Get-Content $script.FullName -Raw
        
        # Extract synopsis from help comment
        $synopsis = ""
        if ($content -match '\.SYNOPSIS\s+([^\n]+)') {
            $synopsis = $Matches[1].Trim()
        }
        
        $documents += @{
            id = "roadmap-$($r.ToLower())-script-$($script.BaseName)"
            roadmap = $r
            type = "script"
            title = $script.Name
            synopsis = $synopsis
            content = $content
            path = $script.FullName
        }
    }
    Write-Host "  ✓ $($scriptFiles.Count) scripts indexed" -ForegroundColor Green
    
    # Index markdown guides
    $mdFiles = Get-ChildItem -Path $roadmapPath -Recurse -Filter "*.md" -Exclude "README.md" -ErrorAction SilentlyContinue
    foreach ($md in $mdFiles) {
        $content = Get-Content $md.FullName -Raw
        
        # Extract title from first heading
        $title = $md.BaseName
        if ($content -match '^#\s+(.+)$') {
            $title = $Matches[1].Trim()
        }
        
        $documents += @{
            id = "roadmap-$($r.ToLower())-guide-$($md.BaseName)"
            roadmap = $r
            type = "guide"
            title = $title
            content = $content
            path = $md.FullName
        }
    }
    Write-Host "  ✓ $($mdFiles.Count) guides indexed" -ForegroundColor Green
}

Write-Host ""
Write-Host "Total documents indexed: $($documents.Count)" -ForegroundColor Cyan
Write-Host ""

# Create index file
Write-Host "Creating index manifest..." -ForegroundColor Yellow
$indexPath = Join-Path $PSScriptRoot "../roadmap-index.json"
$documents | ConvertTo-Json -Depth 10 | Set-Content $indexPath
Write-Host "  ✓ Manifest saved: $indexPath" -ForegroundColor Green

# Check for RAG ingestion endpoint
Write-Host ""
Write-Host "Checking for RAG ingestion service..." -ForegroundColor Yellow

$ragEndpoints = @(
    "http://localhost:8000/rag/ingest",
    "http://localhost:3000/ingest",
    "http://refinory:8000/ingest"
)

$ingested = $false
foreach ($endpoint in $ragEndpoints) {
    try {
        Write-Host "  Trying $endpoint..." -NoNewline
        
        # Create ingestion payload
        $payload = @{
            corpus = "sovereignty-roadmaps"
            documents = $documents | ForEach-Object {
                @{
                    id = $_.id
                    metadata = @{
                        roadmap = $_.roadmap
                        type = $_.type
                        title = $_.title
                    }
                    text = $_.content
                }
            }
        } | ConvertTo-Json -Depth 10
        
        # Send to RAG service (30 second timeout for large collections)
        $response = Invoke-RestMethod -Uri $endpoint -Method Post -Body $payload -ContentType "application/json" -TimeoutSec 30 -ErrorAction Stop
        
        Write-Host " ✓" -ForegroundColor Green
        $ingested = $true
        break
    } catch {
        Write-Host " ✗" -ForegroundColor Red
    }
}

if (-not $ingested) {
    Write-Host ""
    Write-Host "⚠ RAG service not found. Documents indexed locally only." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To enable RAG queries:" -ForegroundColor Cyan
    Write-Host "  1. Ensure Refinory or RAG service is running" -ForegroundColor Gray
    Write-Host "  2. Re-run: ./roadmaps/installers/index-for-rag.ps1" -ForegroundColor Gray
    Write-Host "  3. Or manually ingest: $indexPath" -ForegroundColor Gray
} else {
    Write-Host ""
    Write-Host "✓ RAG indexing complete!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Test with:" -ForegroundColor Cyan
    Write-Host '  curl http://localhost:8000/rag/query -d ''{"query": "How do I fix circular dependencies?"}''' -ForegroundColor Gray
}

# Deploy to cluster if nodes specified
if ($Nodes.Count -gt 0) {
    Write-Host ""
    Write-Host "Deploying index to cluster nodes..." -ForegroundColor Yellow
    
    foreach ($node in $Nodes) {
        Write-Host "  → $node..." -NoNewline
        try {
            scp -q $indexPath "${node}:/opt/sovereignty-roadmap-index.json" 2>$null
            Write-Host " ✓" -ForegroundColor Green
        } catch {
            Write-Host " ✗" -ForegroundColor Red
        }
    }
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
