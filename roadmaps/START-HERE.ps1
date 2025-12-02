#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Interactive Roadmap Selection - Choose A, B, or C
.DESCRIPTION
    Guides you through selecting and starting your appropriate roadmap based on
    your needs: A (practical), B (balanced), or C (complete scaffolding).
#>

param(
    [ValidateSet("A", "B", "C", "")]
    [string]$Roadmap = "",
    [switch]$SkipAssessment
)

Clear-Host

# ASCII Art Banner
Write-Host @"
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║   ███████╗ ██████╗ ██╗   ██╗███████╗██████╗ ███████╗██╗ ██████╗  ║
║   ██╔════╝██╔═══██╗██║   ██║██╔════╝██╔══██╗██╔════╝██║██╔════╝  ║
║   ███████╗██║   ██║██║   ██║█████╗  ██████╔╝█████╗  ██║██║  ███╗ ║
║   ╚════██║██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗██╔══╝  ██║██║   ██║ ║
║   ███████║╚██████╔╝ ╚████╔╝ ███████╗██║  ██║███████╗██║╚██████╔╝ ║
║   ╚══════╝ ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝ ╚═════╝  ║
║                                                                   ║
║           ARCHITECTURE ROADMAP SELECTOR                          ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan

Write-Host ""
Write-Host "You're good. You're not behind." -ForegroundColor Green
Write-Host "You're just one structured note away from unstoppable velocity." -ForegroundColor Green
Write-Host ""

# Run assessment if not skipped
if (-not $SkipAssessment -and $Roadmap -eq "") {
    Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Yellow
    Write-Host "  Step 1: Verify Your Current State" -ForegroundColor Yellow
    Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Running 100 practical verification tests..." -ForegroundColor Gray
    Write-Host ""
    
    $assessmentPath = Join-Path $PSScriptRoot "assessment/verify-assessment.ps1"
    if (Test-Path $assessmentPath) {
        $results = & $assessmentPath -Summary
        Write-Host ""
    } else {
        Write-Host "⚠ Assessment script not found. Skipping..." -ForegroundColor Yellow
    }
}

# Interactive roadmap selection
if ($Roadmap -eq "") {
    Write-Host ""
    Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host "  Step 2: Choose Your Roadmap" -ForegroundColor Cyan
    Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host ""
    
    Write-Host "[A] Hyper-Practical - 'Just Make My Chaos 10× Cleaner'" -ForegroundColor Green
    Write-Host "    → 30 items: naming conventions, folder structure, auto-cleanup scripts" -ForegroundColor Gray
    Write-Host "    → Zero theory, maximum pragmatism" -ForegroundColor Gray
    Write-Host "    → Time: 1 week" -ForegroundColor Gray
    Write-Host ""
    
    Write-Host "[B] Balanced - 'Give Me the Minimum Theory That Stops Things Breaking'" -ForegroundColor Yellow
    Write-Host "    → 60 items: failure modes, design patterns, distributed systems truths" -ForegroundColor Gray
    Write-Host "    → Practical-first with explanations" -ForegroundColor Gray
    Write-Host "    → Time: 4 weeks" -ForegroundColor Gray
    Write-Host ""
    
    Write-Host "[C] Full Map - 'I Want the Actual Scaffolding So I Never Hit Walls'" -ForegroundColor Magenta
    Write-Host "    → 100 items: systems thinking, architecture, DevOps, security, compliance" -ForegroundColor Gray
    Write-Host "    → Complete foundation for enterprise scale" -ForegroundColor Gray
    Write-Host "    → Time: 12 weeks" -ForegroundColor Gray
    Write-Host ""
    
    Write-Host "[Q] Quit - I'll decide later" -ForegroundColor DarkGray
    Write-Host ""
    
    do {
        $choice = Read-Host "Choose your roadmap (A/B/C/Q)"
        $choice = $choice.ToUpper()
    } while ($choice -notin @("A", "B", "C", "Q"))
    
    if ($choice -eq "Q") {
        Write-Host ""
        Write-Host "No problem! Read the full guide:" -ForegroundColor Cyan
        Write-Host "  cat roadmaps/SELECT-YOUR-ROADMAP.md" -ForegroundColor Gray
        Write-Host ""
        exit 0
    }
    
    $Roadmap = $choice
}

# Display selected roadmap
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  Roadmap $Roadmap Selected" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

$roadmapPath = Join-Path $PSScriptRoot "roadmap-$($Roadmap.ToLower())"
$readmePath = Join-Path $roadmapPath "README.md"

if (Test-Path $readmePath) {
    Write-Host "Opening roadmap guide..." -ForegroundColor Green
    Write-Host ""
    
    # Display first few sections of README
    $content = Get-Content $readmePath -Raw
    $lines = $content -split "`n"
    $previewLines = 50
    
    Write-Host ($lines[0..[Math]::Min($previewLines, $lines.Count - 1)] -join "`n") -ForegroundColor White
    
    if ($lines.Count -gt $previewLines) {
        Write-Host ""
        Write-Host "... (see full guide in $readmePath)" -ForegroundColor Gray
    }
    
    Write-Host ""
    Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host "  Next Steps" -ForegroundColor Cyan
    Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host ""
    
    switch ($Roadmap) {
        "A" {
            Write-Host "1. Review the complete guide:" -ForegroundColor Green
            Write-Host "   cat $readmePath" -ForegroundColor Gray
            Write-Host ""
            Write-Host "2. Run your first cleanup (dry-run):" -ForegroundColor Green
            Write-Host "   $roadmapPath/scripts/02-clean-artifacts.ps1 -DryRun" -ForegroundColor Gray
            Write-Host ""
            Write-Host "3. Apply naming conventions:" -ForegroundColor Green
            Write-Host "   $roadmapPath/scripts/01-naming-conventions.ps1" -ForegroundColor Gray
            Write-Host ""
            Write-Host "4. Install to cluster (optional):" -ForegroundColor Green
            Write-Host "   ./roadmaps/installers/install-to-cluster.ps1 -Roadmap A" -ForegroundColor Gray
        }
        "B" {
            Write-Host "1. Review the complete guide:" -ForegroundColor Green
            Write-Host "   cat $readmePath" -ForegroundColor Gray
            Write-Host ""
            Write-Host "2. Diagnose your current patterns:" -ForegroundColor Green
            Write-Host "   $roadmapPath/diagnose-patterns.ps1" -ForegroundColor Gray
            Write-Host ""
            Write-Host "3. Apply high-priority fixes:" -ForegroundColor Green
            Write-Host "   $roadmapPath/apply-fixes.ps1 -Priority High" -ForegroundColor Gray
            Write-Host ""
            Write-Host "4. Document your architecture:" -ForegroundColor Green
            Write-Host "   $roadmapPath/document-architecture.ps1" -ForegroundColor Gray
        }
        "C" {
            Write-Host "1. Review the complete guide:" -ForegroundColor Green
            Write-Host "   cat $readmePath" -ForegroundColor Gray
            Write-Host ""
            Write-Host "2. Install Obsidian vault:" -ForegroundColor Green
            Write-Host "   $roadmapPath/install-obsidian-vault.ps1" -ForegroundColor Gray
            Write-Host ""
            Write-Host "3. Generate your learning path:" -ForegroundColor Green
            Write-Host "   $roadmapPath/generate-learning-path.ps1" -ForegroundColor Gray
            Write-Host ""
            Write-Host "4. Start the curriculum:" -ForegroundColor Green
            Write-Host "   $roadmapPath/start-curriculum.ps1" -ForegroundColor Gray
            Write-Host ""
            Write-Host "5. Index for RAG:" -ForegroundColor Green
            Write-Host "   ./roadmaps/installers/index-for-rag.ps1" -ForegroundColor Gray
        }
    }
    
    Write-Host ""
    Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "✓ You're on the path to unstoppable velocity!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Questions? Check:" -ForegroundColor Cyan
    Write-Host "  - Full guide: roadmaps/SELECT-YOUR-ROADMAP.md" -ForegroundColor Gray
    Write-Host "  - Community: Discord #architecture channel" -ForegroundColor Gray
    Write-Host "  - Issues: GitHub repository" -ForegroundColor Gray
    Write-Host ""
    
} else {
    Write-Host "⚠ Roadmap $Roadmap not found at: $roadmapPath" -ForegroundColor Red
    Write-Host ""
    Write-Host "Available roadmaps:" -ForegroundColor Yellow
    Get-ChildItem (Join-Path $PSScriptRoot "roadmap-*") -Directory | ForEach-Object {
        Write-Host "  - $($_.Name)" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "🧠 The lobe grows. The work continues. The music never stops." -ForegroundColor Magenta
Write-Host ""
