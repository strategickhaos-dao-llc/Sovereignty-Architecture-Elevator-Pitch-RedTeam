# LeakHunter Swarm - PowerShell Launcher
# For Windows/Nitro Lyra node integration

param(
    [Parameter(Position=0)]
    [ValidateSet("quick-scan", "deep-scan", "darkweb", "magnet", "watermark", "alert", "global-sweep", "test")]
    [string]$Command = "quick-scan",
    
    [Parameter()]
    [string]$Config = "",
    
    [Parameter()]
    [string]$Output = "",
    
    [Parameter()]
    [string]$File = "",
    
    [Parameter()]
    [string]$Directory = "",
    
    [Parameter()]
    [string]$Webhook = ""
)

$ErrorActionPreference = "Stop"
$BaseDir = "C:\strategickhaos-cluster\swarm_agents\leakhunter"

# Fallback to current directory if standard path doesn't exist
if (-not (Test-Path $BaseDir)) {
    $BaseDir = $PSScriptRoot
}

Write-Host "🛡️  LeakHunter Swarm Control Panel" -ForegroundColor Cyan
Write-Host "="*70 -ForegroundColor Cyan
Write-Host ""

function Invoke-TorrentScan {
    param([string]$Mode)
    
    Write-Host "🔍 Launching Torrent Leak Scanner ($Mode mode)..." -ForegroundColor Yellow
    
    $args = @("--$Mode")
    if ($Config) { $args += "--config", $Config }
    if ($Output) { $args += "--output", $Output }
    
    & python3 "$BaseDir\torrent_leak_scanner.py" $args
}

function Invoke-DarkWebCrawl {
    Write-Host "🕸️  Launching Dark Web Crawler..." -ForegroundColor Yellow
    
    $args = @()
    if ($Config) { $args += "--config", $Config }
    if ($Output) { $args += "--output", $Output }
    
    & python3 "$BaseDir\darkweb_onion_crawler.py" $args
}

function Invoke-MagnetHarvest {
    Write-Host "🧲 Launching Magnet Harvester..." -ForegroundColor Yellow
    
    $args = @()
    if ($Config) { $args += "--config", $Config }
    if ($Output) { $args += "--output", $Output }
    
    & python3 "$BaseDir\magnet_harvester.py" $args
}

function Invoke-WatermarkScan {
    Write-Host "🔬 Launching Watermark Detector..." -ForegroundColor Yellow
    
    if (-not $File -and -not $Directory) {
        Write-Host "❌ Error: --File or --Directory required for watermark scanning" -ForegroundColor Red
        exit 1
    }
    
    $args = @()
    if ($File) { $args += "--file", $File }
    if ($Directory) { $args += "--directory", $Directory }
    if ($Config) { $args += "--config", $Config }
    if ($Output) { $args += "--output", $Output }
    
    & python3 "$BaseDir\watermark_detector.py" $args
}

function Invoke-DiscordAlert {
    Write-Host "📨 Testing Discord Alert System..." -ForegroundColor Yellow
    
    $args = @("--test")
    if ($Webhook) { $args += "--webhook", $Webhook }
    if ($Config) { $args += "--config", $Config }
    
    & python3 "$BaseDir\alert_to_discord.py" $args
}

function Invoke-GlobalSweep {
    Write-Host "🌍 Launching Full Global Sweep..." -ForegroundColor Yellow
    Write-Host "⚠️  This will take 4+ hours on a 64-core system" -ForegroundColor Yellow
    Write-Host ""
    
    $confirm = Read-Host "Continue? (y/N)"
    if ($confirm -ne "y") {
        Write-Host "Cancelled." -ForegroundColor Gray
        exit 0
    }
    
    $args = @()
    if ($Config) { $args += "--config", $Config }
    if ($Output) { $args += "--output-dir", $Output }
    
    & python3 "$BaseDir\full_global_sweep.py" $args
}

function Invoke-TestSuite {
    Write-Host "🧪 Running LeakHunter Test Suite..." -ForegroundColor Yellow
    
    & python3 "$BaseDir\test_suite.py"
}

# Execute command
switch ($Command) {
    "quick-scan" { Invoke-TorrentScan -Mode "quick-scan" }
    "deep-scan" { Invoke-TorrentScan -Mode "deep-scan" }
    "darkweb" { Invoke-DarkWebCrawl }
    "magnet" { Invoke-MagnetHarvest }
    "watermark" { Invoke-WatermarkScan }
    "alert" { Invoke-DiscordAlert }
    "global-sweep" { Invoke-GlobalSweep }
    "test" { Invoke-TestSuite }
}

Write-Host ""
Write-Host "="*70 -ForegroundColor Cyan
Write-Host "✅ LeakHunter Swarm operation complete" -ForegroundColor Green
