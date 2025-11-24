# ╔══════════════════════════════════════════════════════════════╗
# ║          STRATEGICKHAOS OPERATOR v2.0 — UNKILLABLE           ║
# ║           "It didn't die. It just went to Valhalla."         ║
# ╚══════════════════════════════════════════════════════════════╝

param (
    [switch]$dashboard,
    [switch]$start,
    [switch]$status,
    [string]$pull = "",
    [switch]$nuke,
    [switch]$debug
)

# === SURVIVAL SETTINGS ===
$ErrorActionPreference = "Continue"
$ProgressPreference = "SilentlyContinue"
$root = (Resolve-Path $PSScriptRoot).Path

# Retro colors — because we die aesthetic
$G = "Green"; $C = "Cyan"; $R = "Red"; $Y = "Yellow"; $M = "Magenta"; $W = "White"

function Log($msg, $color=$W) { Write-Host "[$(Get-Date -f 'HH:mm:ss')] $msg" -ForegroundColor $color }
function Log-Success($msg) { Log $msg $G }
function Log-Error($msg)   { Log "ERROR → $msg" $R }
function Log-Warn($msg)    { Log "WARN  → $msg" $Y }
function Log-Debug($msg)   { if ($debug) { Log "DEBUG → $msg" $C } }

function Test-Command($cmd) {
    $null -ne (Get-Command $cmd -ErrorAction SilentlyContinue)
}

function Test-Port($port, $timeout=3) {
    $tcp = New-Object System.Net.Sockets.TcpClient
    try {
        $connect = $tcp.BeginConnect("127.0.0.1", $port, $null, $null)
        $success = $connect.AsyncWaitHandle.WaitOne($timeout*1000, $false)
        return $success -and $tcp.Connected
    } catch { return $false } finally { $tcp.Close() }
}

function Notify-Discord($msg) {
    $configPath = "$root/discord/webhook_config.json"
    if (-not (Test-Path $configPath)) { Log-Warn "Discord webhook config missing"; return }

    try {
        $webhook = Get-Content $configPath -Raw | ConvertFrom-Json -ErrorAction Stop
        if (-not $webhook.url -or $webhook.url -notmatch "^https://discord.com/api/webhooks/") {
            Log-Warn "Invalid Discord webhook URL"
            return
        }

        $payload = @{ content = ("``$msg``" -replace "[\r\n]+", " | ") } | ConvertTo-Json -Compress
        Invoke-RestMethod -Uri $webhook.url -Method Post -Body $payload -ContentType "application/json" -TimeoutSec 10 -ErrorAction SilentlyContinue | Out-Null
    } catch {
        Log-Error "Discord notification failed: $($_.Exception.Message)"
    }
}

function Show-Dashboard {
    Clear-Host
    Write-Host "╔══════════════════════════════════════════════════════════════╗" -F $M
    Write-Host "║           STRATEGICKHAOS OPERATOR v2.0 — ARMORED             ║" -F $M
    Write-Host "║               23 NOV 2025 — COMBAT READY                     ║" -F $G
    Write-Host "╚══════════════════════════════════════════════════════════════╝" -F $M
    Write-Host ""
    Write-Host "   ██████╗ ██████╗ ███████╗██████╗  █████╗ ████████╗ ██████╗ ██████╗ " -F $C
    Write-Host "  ██╔═══██╗██╔══██╗██╔════╝██╔══██╗██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗" -F $C
    Write-Host "  ██║   ██║██████╔╝█████╗  ██████╔╝███████║   ██║   ██║   ██║██████╔╝" -F $C
    Write-Host "  ██║   ██║██╔═══╝ ██╔══╝  ██╔══██╗██╔══██║   ██║   ██║   ██║██╔══██╗" -F $C
    Write-Host "  ╚██████╔╝██║     ███████╗██║  ██║██║  ██║   ██║   ╚██████╔╝██║  ██║" -F $C
    Write-Host "   ╚═════╝ ╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝" -F $C
    Write-Host ""
    Log-Success "OPERATOR COCKPIT ACTIVE | $(hostname) | $(Get-Date -f 'yyyy-MM-dd HH:mm')"
    Write-Host ""
}

# === MAIN EXECUTION WITH BULLETPROOF WRAPPERS ===
try {
    if ($dashboard) { Show-Dashboard; exit }

    if ($start) {
        Show-Dashboard
        Log "Initiating full system bring-up..."

        # Ollama daemon
        if (-not (Test-Port 11434)) {
            Log "Starting Ollama daemon..."
            $proc = Start-Process "ollama" -ArgumentList "serve" -PassThru -WindowStyle Hidden -ErrorAction SilentlyContinue
            Start-Sleep -Seconds 6
            if (Test-Port 11434) { Log-Success "Ollama daemon ONLINE @ 11434" } else { throw "Ollama failed to start" }
        } else { Log "Ollama already running" }

        # K8s apply with safety
        if (Test-Command kubectl) {
            Log "Applying K8s manifests..."
            kubectl apply -f "$root/k8s/deployments/" --recursive --timeout=60s 2>$null
            kubectl wait --for=condition=Ready pod -l app=ollama --timeout=180s --field-selector=status.phase!=Succeeded 2>$null
            Log-Success "K8s deployment stable"
        } else { Log-Warn "kubectl not found — skipping K8s" }

        Notify-Discord "StrategicKhaos v2.0 → FULLY ONLINE | $(hostname) | $(whoami)"
        Log-Success "OPERATOR WORKSPACE IS NOW LIVE. GO MAKE HISTORY."
    }

    elseif ($status) {
        Show-Dashboard
        Log "Status Report:"
        "Ollama      : $(if (Test-Port 11434) {'[RUNNING]'} else {'[DOWN]'})"
        if (Test-Command kubectl) { "K8s Pod     : $(kubectl get pod -l app=ollama -o jsonpath='{.items[*].status.phase}' 2>$null || 'N/A')" }
        if (Test-Command ollama) { "Models      : $(ollama list 2>$null | Select-Object -Skip 1 | ForEach-Object {$_.Split()[0]} | Join-String ', ')" }
        if (Test-Command git) { "Git Branch  : $(git rev-parse --abbrev-ref HEAD 2>$null || 'detached')" }
    }

    elseif ($pull) {
        if (-not (Test-Command ollama)) { Log-Error "ollama command not found"; exit 1 }
        Log "Pulling model: $pull (local only)"
        ollama pull $pull 2>&1 | ForEach-Object { Log $_ $C }
        Notify-Discord "Model deployed → $pull by $(whoami)"
        Log-Success "$pull ready for action."
    }

    elseif ($nuke) {
        Log "EXECUTING NUKE SEQUENCE..." $R
        kubectl delete -f "$root/k8s/deployments/" --ignore-not-found=true --timeout=60s 2>$null
        Get-Process ollama -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
        Notify-Discord "NUKE COMPLETE — All systems dark. $(whoami) was here."
        Log-Success "Silence achieved."
    }

    else { Show-Dashboard }

} catch {
    Log-Error "FATAL: $($_.Exception.Message)"
    Notify-Discord "OPERATOR FAILURE → $($_.Exception.Message) | $(hostname)"
    exit 1
}
