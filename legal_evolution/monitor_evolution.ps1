# Legal Evolution Monitor (PowerShell)
# Monitors legal_evolution_ledger.jsonl in real-time and displays key metrics

param(
    [string]$LedgerPath = "legal_evolution_ledger.jsonl",
    [switch]$Follow,
    [int]$Lines = 10
)

Write-Host "⚖️  Legal Evolution Monitor" -ForegroundColor Cyan
Write-Host "=" -NoNewline -ForegroundColor Gray
Write-Host ("=" * 69) -ForegroundColor Gray
Write-Host ""

if (-not (Test-Path $LedgerPath)) {
    Write-Host "❌ Ledger file not found: $LedgerPath" -ForegroundColor Red
    Write-Host "Run legal_evolution_synthesizer.py first." -ForegroundColor Yellow
    exit 1
}

function Format-Entry {
    param($Entry)
    
    $compliantIcon = if ($Entry.compliant) { "✅" } else { "⚠️ " }
    $timestamp = [DateTime]::Parse($Entry.timestamp).ToString("HH:mm:ss")
    
    Write-Host "$compliantIcon " -NoNewline
    Write-Host "[Gen $($Entry.generation)] " -NoNewline -ForegroundColor Yellow
    Write-Host "$($Entry.strategy_type) " -NoNewline -ForegroundColor Cyan
    Write-Host "Fitness: $($Entry.fitness) " -NoNewline -ForegroundColor Green
    Write-Host "($timestamp)" -ForegroundColor Gray
}

function Get-Statistics {
    param($Entries)
    
    $total = $Entries.Count
    $compliant = ($Entries | Where-Object { $_.compliant -eq $true }).Count
    $avgFitness = ($Entries | Measure-Object -Property fitness -Average).Average
    
    Write-Host "`n📊 Statistics:" -ForegroundColor Cyan
    Write-Host "   Total Entries: $total"
    Write-Host "   Compliant: $compliant / $total ($([math]::Round($compliant/$total*100, 1))%)"
    Write-Host "   Avg Fitness: $([math]::Round($avgFitness, 2))"
    
    # Group by type
    $byType = $Entries | Group-Object -Property strategy_type
    Write-Host "`n📋 By Type:" -ForegroundColor Cyan
    foreach ($group in $byType) {
        $typeCompliant = ($group.Group | Where-Object { $_.compliant -eq $true }).Count
        $typeAvgFitness = ($group.Group | Measure-Object -Property fitness -Average).Average
        Write-Host "   $($group.Name): " -NoNewline
        Write-Host "$typeCompliant/$($group.Count) compliant, " -NoNewline
        Write-Host "avg $([math]::Round($typeAvgFitness, 2))" -ForegroundColor Green
    }
}

if ($Follow) {
    Write-Host "Following ledger (Ctrl+C to stop)..." -ForegroundColor Yellow
    Write-Host ""
    
    Get-Content $LedgerPath -Wait | ForEach-Object {
        $entry = $_ | ConvertFrom-Json
        Format-Entry $entry
    }
} else {
    # Load all entries
    $entries = Get-Content $LedgerPath | ForEach-Object {
        $_ | ConvertFrom-Json
    }
    
    # Show last N entries
    Write-Host "📝 Last $Lines entries:" -ForegroundColor Cyan
    Write-Host ""
    
    $entries | Select-Object -Last $Lines | ForEach-Object {
        Format-Entry $_
    }
    
    # Show statistics
    Get-Statistics $entries
}

Write-Host ""
Write-Host "=" -NoNewline -ForegroundColor Gray
Write-Host ("=" * 69) -ForegroundColor Gray
