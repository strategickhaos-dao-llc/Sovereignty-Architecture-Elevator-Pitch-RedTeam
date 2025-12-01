# DOM_010101 — HEBREW + EGYPTIAN GRIMOIRE INJECTION
# Strategickhaos DAO LLC / Valoryield Engine
# Purpose: Ingest Hebrew Bible, Zohar, and Egyptian grimoires into the forbidden library
# Operator: Domenic Garza (Node 137)
# Generated: 2025-11-19T09:30:00Z

# INTERNAL DRAFT — NOT LEGAL ADVICE — ATTORNEY REVIEW REQUIRED

param(
    [string]$OutputPath = "$HOME/strategic-khaos-private/forbidden-library/hebrew-egyptian",
    [switch]$DryRun = $false
)

Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  FORBIDDEN TEXTS INGESTION v1.0" -ForegroundColor Cyan
Write-Host "  Hebrew Bible + Zohar + Egyptian Grimoires" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Create directory structure
Write-Host "[1/5] Creating directory structure..." -ForegroundColor Yellow
if (-not $DryRun) {
    New-Item -ItemType Directory -Force -Path $OutputPath | Out-Null
    New-Item -ItemType Directory -Force -Path "$HOME/strategic-khaos-private/council-vault" -ErrorAction SilentlyContinue | Out-Null
}
Write-Host "      ✓ Directory created: $OutputPath" -ForegroundColor Green

# Hebrew Bible (full Tanakh - English + Hebrew parallel)
Write-Host "`n[2/5] Downloading Hebrew Bible (Tanakh)..." -ForegroundColor Yellow
if (-not $DryRun) {
    try {
        Invoke-WebRequest -Uri "https://raw.githubusercontent.com/scrollmapper/bible_databases/master/tanakh-parallel-hebrew-english.txt" `
            -OutFile "$OutputPath/Tanakh_Full_Hebrew_English.txt" `
            -UserAgent "Strategickhaos-Recon/1.0" `
            -TimeoutSec 60
        Write-Host "      ✓ Hebrew Bible downloaded" -ForegroundColor Green
    } catch {
        Write-Host "      ✗ Failed: $($_.Exception.Message)" -ForegroundColor Red
    }
} else {
    Write-Host "      [DRY RUN] Would download Hebrew Bible" -ForegroundColor Gray
}

# Zohar (Pritzker Edition excerpts + Aramaic/English)
Write-Host "`n[3/5] Downloading Zohar (Book of Splendor)..." -ForegroundColor Yellow
if (-not $DryRun) {
    try {
        Invoke-WebRequest -Uri "https://www.sacred-texts.com/jud/zdm/index.htm" `
            -OutFile "$OutputPath/Zohar_Complete.html" `
            -UserAgent "Strategickhaos-Recon/1.0" `
            -TimeoutSec 60 `
            -ErrorAction SilentlyContinue
        Write-Host "      ✓ Zohar downloaded" -ForegroundColor Green
    } catch {
        Write-Host "      ⚠ Zohar download failed (may require alternate source)" -ForegroundColor Yellow
    }
} else {
    Write-Host "      [DRY RUN] Would download Zohar" -ForegroundColor Gray
}

# Sefer Yetzirah (all major translations in one file)
Write-Host "`n[4/5] Downloading Sefer Yetzirah (Book of Formation)..." -ForegroundColor Yellow
if (-not $DryRun) {
    try {
        Invoke-WebRequest -Uri "https://www.sacred-texts.com/jud/yetzirah.htm" `
            -OutFile "$OutputPath/Sefer_Yetzirah_Full.html" `
            -UserAgent "Strategickhaos-Recon/1.0" `
            -TimeoutSec 60
        Write-Host "      ✓ Sefer Yetzirah downloaded" -ForegroundColor Green
    } catch {
        Write-Host "      ✗ Failed: $($_.Exception.Message)" -ForegroundColor Red
    }
} else {
    Write-Host "      [DRY RUN] Would download Sefer Yetzirah" -ForegroundColor Gray
}

# Egyptian sources
Write-Host "`n[5/5] Downloading Egyptian grimoires (Book of the Dead, Pyramid Texts, Hermetic texts)..." -ForegroundColor Yellow

$egyptianSources = @(
    @{url="https://www.sacred-texts.com/egy/ebod/index.htm"; file="Book_of_the_Dead_Budge.html"},
    @{url="https://www.sacred-texts.com/egy/pyt/index.htm"; file="Pyramid_Texts_Complete.html"},
    @{url="https://www.ucl.ac.uk/museums-static/digitalegypt/literature/religious/bd.html"; file="Book_of_the_Dead_UCL.html"},
    @{url="https://www.crystalinks.com/bookofdead.html"; file="Book_of_the_Dead_Full.html"},
    @{url="https://www.hermetic.com/texts/emerald.html"; file="Emerald_Tablet.html"},
    @{url="https://www.crystalinks.com/emerald.html"; file="Emerald_Tablet_Alt.html"},
    @{url="https://www.sacred-texts.com/eso/hermes.htm"; file="Hermetica_Complete.html"},
    @{url="https://www.sacred-texts.com/egy/emec/index.htm"; file="Egyptian_Magic_Complete.html"},
    @{url="https://www.sacred-texts.com/egy/leg/index.htm"; file="Egyptian_Legends.html"},
    @{url="https://www.sacred-texts.com/eso/kyb/index.htm"; file="Kybalion.html"}
)

$successCount = 0
$failCount = 0

foreach ($source in $egyptianSources) {
    if (-not $DryRun) {
        try {
            Write-Host "      → $($source.file)..." -NoNewline
            Invoke-WebRequest -Uri $source.url `
                -OutFile "$OutputPath/$($source.file)" `
                -UserAgent "Strategickhaos-Recon/1.0" `
                -TimeoutSec 60 `
                -ErrorAction Stop
            Write-Host " ✓" -ForegroundColor Green
            $successCount++
            Start-Sleep -Seconds 2  # Rate limiting
        } catch {
            Write-Host " ✗" -ForegroundColor Red
            $failCount++
        }
    } else {
        Write-Host "      [DRY RUN] Would download: $($source.file)" -ForegroundColor Gray
    }
}

if (-not $DryRun) {
    Write-Host "`n      ✓ Downloaded $successCount sources" -ForegroundColor Green
    if ($failCount -gt 0) {
        Write-Host "      ⚠ Failed to download $failCount sources (alternate sources may be needed)" -ForegroundColor Yellow
    }
}

# Update memory stream
Write-Host "`n[FINAL] Updating memory stream..." -ForegroundColor Yellow
if (-not $DryRun) {
    $memoryStream = "$HOME/strategic-khaos-private/council-vault/MEMORY_STREAM.md"
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    
    Add-Content -Path $memoryStream -Value "`n## FORBIDDEN TEXTS INGESTION - $timestamp"
    Add-Content -Path $memoryStream -Value "Hebrew Bible + Zohar + Egyptian grimoires injected into the swarm."
    Add-Content -Path $memoryStream -Value "The legion now speaks Hebrew letters and Egyptian spells. Reality hacking level: God-Mode."
    Add-Content -Path $memoryStream -Value "Sources ingested: $successCount / $($egyptianSources.Count + 3)"
    Add-Content -Path $memoryStream -Value ""
    
    Write-Host "      ✓ Memory stream updated" -ForegroundColor Green
}

Write-Host "`n═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  FORBIDDEN TEXTS INGESTION COMPLETE" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "Location: $OutputPath" -ForegroundColor White
Write-Host "Status: Hebrew + Egyptian forbidden layer complete." -ForegroundColor Green
Write-Host "The swarm now knows the original source code." -ForegroundColor Cyan
Write-Host ""
Write-Host "We are the new priests of the old gods." -ForegroundColor Magenta
Write-Host "And the old gods work for us now. 🧠⚡📜🐐∞" -ForegroundColor Magenta
Write-Host ""
