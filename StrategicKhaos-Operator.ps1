<#
╔══════════════════════════════════════════════════════════════╗
║     STRATEGICKHAOS OPERATOR v3.1 — FINAL SANCTIFIED EDITION    ║
║          "Feed the world. One prompt at a time."             ║
║             Built by two lunatics who refused to lose         ║
╚══════════════════════════════════════════════════════════════╝
#>

[CmdletBinding()]
param(
    [switch]$dashboard,
    [switch]$start,
    [switch]$status,
    [string]$pull = "",
    [switch]$nuke,
    [switch]$debug,
    [switch]$feed          # ← THE RED BUTTON
)

# ──────────────────────────────────────────────────────────────
# Core config
# ──────────────────────────────────────────────────────────────
$M = 'Magenta'; $G = 'Green'; $C = 'Cyan'; $R = 'Red'; $Y = 'Yellow'; $W = 'Gray'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path

# ──────────────────────────────────────────────────────────────
# Logging & helpers
# ──────────────────────────────────────────────────────────────
function Log        { param([string]$m, [string]$c='Gray')   Write-Host "[$(Get-Date -f 'HH:mm:ss')] $m" -ForegroundColor $c }
function Log-Success{ param([string]$m) Log $m $G }
function Log-Error  { param([string]$m) Log "ERROR → $m" $R }
function Log-Warn   { param([string]$m) Log "WARN  → $m" $Y }

function Test-Command { param([string]$n) [bool](Get-Command $n -ErrorAction SilentlyContinue) }
function Test-Port    { param([int]$p) try { (New-Object Net.Sockets.TcpClient).BeginConnect('127.0.0.1',$p,$null,$null).AsyncWaitHandle.WaitOne(800) | Out-Null; $true } catch { $false } }

function Notify-Discord {
    param([string]$msg)
    $cfg = Join-Path $root "discord\webhook_config.json"
    if (-not (Test-Path $cfg)) { Log-Warn "No Discord webhook config — skipping notify" ; return }
    try {
        $url = (Get-Content $cfg -Raw | ConvertFrom-Json).url
        Invoke-RestMethod -Uri $url -Method Post -Body (@{content="``$msg``"} | ConvertTo-Json) -ContentType "application/json" -TimeoutSec 10 | Out-Null
    } catch { Log-Error "Discord failed: $($_.Exception.Message)" }
}

# ──────────────────────────────────────────────────────────────
# Dashboard — pure 90s cyberpunk nonprofit glory
# ──────────────────────────────────────────────────────────────
function Show-Dashboard {
    Clear-Host
    Write-Host "╔══════════════════════════════════════════════════════════════╗" -F $M
    Write-Host "║      STRATEGICKHAOS OPERATOR v3.1 — NONPROFIT DIVISION       ║" -F $M
    Write-Host "║              FEEDING THE WORLD SINCE NOV 2025                ║" -F $G
    Write-Host "╚══════════════════════════════════════════════════════════════╝" -F $M
    Write-Host ""
    "   ██████╗ ██████╗ ███████╗██████╗  █████╗  ██████╗ ██████╗ " | Write-Host -F $C
    "   ██╔══██╗██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔════╝██╔══██╗" | Write-Host -F $C
    "   ██████╔╝██████╔╝█████╗  ██████╔╝███████║██║     ██████╔╝" | Write-Host -F $C
    "   ██╔═══╝ ██╔══██╗██╔══╝  ██╔══██╗██╔══██║██║     ██╔══██╗" | Write-Host -F $C
    "   ██║     ██║  ██║███████╗██║  ██║██║  ██║╚██████╗██║  ██║" | Write-Host -F $C
    "   ╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝" | Write-Host -F $C
    Write-Host ""
    "   ███╗   ██╗ ██████╗ ███╗   ██╗██████╗ ██████╗  ██████╗ ███████╗██╗████████╗" -F $R
    "   ████╗  ██║██╔═══██╗████╗  ██║██╔══██╗██╔══██╗██╔═══██╗██╔════╝██║╚══██╔══╝" -F $R
    "   ██╔██╗ ██║██║   ██║██╔██╗ ██║██████╔╝██████╔╝██║   ██║█████╗  ██║   ██║   " -F $R
    "   ██║╚██╗██║██║   ██║██║╚██╗██║██╔═══╝ ██╔══██╗██║   ██║██╔══╝  ██║   ██║   " -F $R
    "   ██║ ╚████║╚██████╔╝██║ ╚████║██║     ██║  ██║╚██████╔╝██║     ██║   ██║   " -F $R
    "   ╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝   ╚═╝   " -F $R
    Write-Host ""
    Log-Success "NONPROFIT OPERATOR ACTIVE | $(hostname) | $(whoami) | $(Get-Date -f 'yyyy-MM-dd HH:mm')"
    Write-Host "   → -dashboard | -start | -status | -pull <model> | -nuke | -feed (RED BUTTON)" -F $Y
    Write-Host ""
}

# ──────────────────────────────────────────────────────────────
# THE RED BUTTON — FEED THE WORLD
# ──────────────────────────────────────────────────────────────
if ($feed) {
    Clear-Host
    Write-Host "╔══════════════════════════════════════════════════════════════╗" -F DarkRed
    Write-Host "║               NONPROFIT MODE — ACTIVATED                     ║" -F Red
    Write-Host "║          Every token now belongs to humanity                 ║" -F Red
    Write-Host "║               No ads. No paywalls. No masters.               ║" -F Red
    Write-Host "╚══════════════════════════════════════════════════════════════╝" -F DarkRed
    Start-Sleep -Seconds 4

    Show-Dashboard
    Log "RED BUTTON DEPRESSED — DEPLOYING OPEN INTELLIGENCE TO THE PLANET" $R

    $holyModels = "llama3.2:latest","phi3:medium","gemma2:27b","qwen2.5:32b","mistral-nemo","openhermes2.5","dolphin-llama3.2","medic-llama3","llava","nomic-embed-text"

    foreach ($m in $holyModels) {
        if (-not (ollama list 2>$null | Select-String ($m -split ':')[0])) {
            Log "Deploying $m → feeding education, health, truth..." $C
            ollama pull $m 2>&1 | ForEach-Object { Log "   $_" $C }
            Notify-Discord "NONPROFIT DEPLOYMENT → $m now serving 8 billion humans | Operator $(whoami)"
        } else { Log "$m already in service" $G }
    }

    Notify-Discord "STRATEGICKHAOS NONPROFIT DIVISION FULLY ARMED — THE WORLD IS NOW BEING FED RAW OPEN WEIGHTS."
    Log-Success "They weren't ready."
    Log-Success "We are."
    exit
}

# ──────────────────────────────────────────────────────────────
# Standard commands
# ──────────────────────────────────────────────────────────────
try {
    if ($dashboard) { Show-Dashboard; exit }
    if ($status)    { Show-Dashboard; "Ollama: $(if(Test-Port 11434){'ONLINE'}else{'OFFLINE'})" ; exit }
    if ($pull)      { ollama pull $pull ; Notify-Discord "Model pulled → $pull" ; exit }
    if ($nuke)      { Get-Process ollama* -ErrorAction SilentlyContinue | Stop-Process -Force; kubectl delete all -l app=ollama --force 2>$null; Notify-Discord "NUKE EXECUTED — $(whoami)" ; Log-Success "Peace through superior firepower." ; exit }

    if ($start) {
        Show-Dashboard
        Log "Launching full stack..." $Y

        if (-not (Test-Port 11434)) {
            Log "Igniting Ollama daemon..." $C
            Start-Process ollama -ArgumentList serve -WindowStyle Hidden
            for($i=0;$i -lt 15;$i++) { if(Test-Port 11434) { break } ; Start-Sleep 1 }
            if(Test-Port 11434) { Log-Success "Ollama daemon LIVE @ 11434" }
        }

        if (Test-Command kubectl) {
            kubectl apply -f "$root/k8s/" --recursive 2>$null
            Log-Success "K8s cluster synchronized"
        }

        Notify-Discord "StrategicKhaos v3.1 → ONLINE | $(hostname) | Serving humanity"
        Log-Success "THE WORLD IS BEING FED."
        exit
    }

    Show-Dashboard
} catch {
    Log-Error "SYSTEM TOOK DAMAGE: $($_.Exception.Message)"
    Notify-Discord "OPERATOR HIT → $($_.Exception.Message) | Still standing."
}
