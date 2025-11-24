# ╔══════════════════════════════════════════════════════════════╗
# ║                  STRATEGICKHAOS OPERATOR v1.0                ║
# ║                "Making history, one prompt at a time"        ║
# ╚══════════════════════════════════════════════════════════════╝

# Run this from the root of StrategicKhaos-OperatorWorkspace
# ./operator.ps1 --dashboard        → pure 1997 cyberdeck glory
# ./operator.ps1 --start           → full system bring-up
# ./operator.ps1 --status          → health check everything
# ./operator.ps1 --pull llama3.2   → grab a model safely
# ./operator.ps1 --nuke            → danger zone (you asked for it)

param (
    [switch]$dashboard,
    [switch]$start,
    [switch]$status,
    [string]$pull = "",
    [switch]$nuke
)

$ErrorActionPreference = "Continue"  # Changed from Stop to Continue for better error handling
$root = Get-Location

# Colors for that authentic CRT glow
$green  = "Green"
$cyan   = "Cyan"
$red    = "Red"
$yellow = "Yellow"
$mag    = "Magenta"

# Error counter for tracking failures
$script:errorCount = 0
$script:warningCount = 0

function Write-Retro {
    param([string]$text, [string]$color = "Cyan")
    try {
        Write-Host $text -ForegroundColor $color
    } catch {
        Write-Host $text
    }
}

function Write-ErrorLog {
    param([string]$message, [string]$context = "")
    $script:errorCount++
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logEntry = "[$timestamp] ERROR: $message"
    if ($context) {
        $logEntry += " | Context: $context"
    }
    Write-Retro $logEntry $red
    
    # Log to file
    $logDir = Join-Path $root "logs"
    if (-not (Test-Path $logDir)) {
        try {
            New-Item -ItemType Directory -Path $logDir -Force | Out-Null
        } catch {
            # Can't create log directory
        }
    }
    try {
        $logFile = Join-Path $logDir "operator-$(Get-Date -Format 'yyyy-MM-dd').log"
        Add-Content -Path $logFile -Value $logEntry -ErrorAction SilentlyContinue
    } catch {
        # Can't write to log file
    }
}

function Write-WarningLog {
    param([string]$message)
    $script:warningCount++
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logEntry = "[$timestamp] WARNING: $message"
    Write-Retro $logEntry $yellow
}

function Test-Administrator {
    try {
        $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
        $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
        return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
    } catch {
        Write-WarningLog "Cannot determine admin status: $_"
        return $false
    }
}

function Test-CommandExists {
    param([string]$command)
    try {
        $null = Get-Command $command -ErrorAction Stop
        return $true
    } catch {
        return $false
    }
}

function Test-Port {
    param($port)
    try {
        $test = Test-NetConnection localhost -Port $port -WarningAction SilentlyContinue -ErrorAction Stop -InformationLevel Quiet
        return $test.TcpTestSucceeded
    } catch {
        # Fallback method using System.Net.Sockets
        try {
            $tcpClient = New-Object System.Net.Sockets.TcpClient
            $tcpClient.Connect("localhost", $port)
            $tcpClient.Close()
            return $true
        } catch {
            return $false
        }
    }
}

function Get-NodeIP {
    try {
        $ip = kubectl get nodes -o jsonpath='{.items[0].status.addresses[?(@.type=="InternalIP")].address}' 2>$null
        if ($ip) {
            return $ip
        }
        return "N/A"
    } catch {
        return "N/A"
    }
}

function Get-ModelCount {
    try {
        if (-not (Test-CommandExists "ollama")) {
            return "N/A (ollama not found)"
        }
        $models = ollama list 2>$null
        if ($LASTEXITCODE -ne 0) {
            return "N/A (ollama error)"
        }
        $count = ($models | Measure-Object -Line).Lines
        if ($count -gt 0) {
            return "$($count - 1) models"
        }
        return "0 models"
    } catch {
        return "N/A (exception)"
    }
}

function Show-Dashboard {
    try {
        Clear-Host
    } catch {
        # Can't clear host
    }
    
    Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor $mag
    Write-Host "║               STRATEGICKHAOS OPERATOR COCKPIT                ║" -ForegroundColor $mag
    Write-Host "║                  23 NOV 2025 — ONLINE                        ║" -ForegroundColor $green
    Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor $mag
    Write-Host ""
    Write-Host "  ██████╗ ██████╗ ███████╗██████╗  █████╗  ██████╗ ██████╗ " -ForegroundColor $cyan
    Write-Host "  ██╔══██╗██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔════╝██╔══██╗" -ForegroundColor $cyan
    Write-Host "  ██████╔╝██████╔╝█████╗  ██████╔╝███████║██║     ██████╔╝" -ForegroundColor $cyan
    Write-Host "  ██╔═══╝ ██╔══██╗██╔══╝  ██╔══██╗██╔══██║██║     ██╔══██╗" -ForegroundColor $cyan
    Write-Host "  ██║     ██║  ██║███████╗██║  ██║██║  ██║╚██████╗██║  ██║" -ForegroundColor $cyan
    Write-Host "  ╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝" -ForegroundColor $cyan
    Write-Host ""
    Write-Host "  [OPERATOR ONLINE]  Local K8s + Ollama + Discord Relay Active" -ForegroundColor $green
    
    try {
        $hostname = hostname
        $nodeIP = Get-NodeIP
        Write-Host "  Node IP      : $hostname @ $nodeIP" -ForegroundColor $yellow
    } catch {
        Write-Host "  Node IP      : Unable to determine" -ForegroundColor $red
    }
    
    $ollamaStatus = if (Test-Port 11434) {'RUNNING'} else {'DOWN'}
    $ollamaColor = if (Test-Port 11434) {$green} else {$red}
    Write-Host "  Ollama Port  : 11434 → $ollamaStatus" -ForegroundColor $ollamaColor
    
    $modelCount = Get-ModelCount
    Write-Host "  Models Loaded: $modelCount" -ForegroundColor $cyan
    Write-Host ""
    Write-Host "  COMMANDS → ./operator.ps1 --start | --status | --pull <model> | --nuke" -ForegroundColor $mag
    Write-Host ""
    
    if ($script:errorCount -gt 0) {
        Write-Host "  ⚠ Errors: $($script:errorCount) | Warnings: $($script:warningCount)" -ForegroundColor $yellow
    }
}

function Test-Prerequisites {
    Write-Retro "[PREFLIGHT] Checking prerequisites..." $cyan
    $allGood = $true
    
    # Check if running on Windows
    if (-not $IsWindows -and -not ($PSVersionTable.PSVersion.Major -le 5)) {
        Write-ErrorLog "This script is designed for Windows PowerShell" "OS Check"
        $allGood = $false
    }
    
    # Check kubectl
    if (-not (Test-CommandExists "kubectl")) {
        Write-ErrorLog "kubectl not found in PATH" "kubectl check"
        Write-Retro "  → Install kubectl: https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/" $yellow
        $allGood = $false
    } else {
        Write-Retro "  ✓ kubectl found" $green
    }
    
    # Check ollama
    if (-not (Test-CommandExists "ollama")) {
        Write-ErrorLog "ollama not found in PATH" "ollama check"
        Write-Retro "  → Install Ollama: https://ollama.ai/download" $yellow
        $allGood = $false
    } else {
        Write-Retro "  ✓ ollama found" $green
    }
    
    # Check if K8s cluster is accessible
    try {
        $null = kubectl cluster-info 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-ErrorLog "kubectl cannot connect to cluster" "K8s connectivity"
            Write-Retro "  → Ensure K8s cluster is running (Docker Desktop, minikube, etc.)" $yellow
            $allGood = $false
        } else {
            Write-Retro "  ✓ K8s cluster accessible" $green
        }
    } catch {
        Write-ErrorLog "Error checking K8s cluster: $_" "K8s check"
        $allGood = $false
    }
    
    # Check if manifests exist
    $deployPath = Join-Path $root "k8s/deployments/ollama-deploy.yaml"
    $svcPath = Join-Path $root "k8s/services/ollama-svc.yaml"
    
    if (-not (Test-Path $deployPath)) {
        Write-ErrorLog "Deployment manifest not found: $deployPath" "Manifest check"
        $allGood = $false
    } else {
        Write-Retro "  ✓ Deployment manifest found" $green
    }
    
    if (-not (Test-Path $svcPath)) {
        Write-ErrorLog "Service manifest not found: $svcPath" "Manifest check"
        $allGood = $false
    } else {
        Write-Retro "  ✓ Service manifest found" $green
    }
    
    # Check admin privileges (warning only)
    if (-not (Test-Administrator)) {
        Write-WarningLog "Not running as Administrator - some operations may fail"
    }
    
    return $allGood
}

function Notify-Discord {
    param([string]$msg)
    
    try {
        $configPath = Join-Path $root "discord/webhook_config.json"
        
        if (-not (Test-Path $configPath)) {
            # Discord webhook not configured, skip silently
            return
        }
        
        $webhook = Get-Content $configPath -ErrorAction Stop | ConvertFrom-Json
        
        if (-not $webhook.enabled) {
            return
        }
        
        if (-not $webhook.url) {
            Write-WarningLog "Discord webhook URL not configured"
            return
        }
        
        $body = @{
            content = "``````$msg``````"
            username = if ($webhook.name) { $webhook.name } else { "StrategicKhaos Operator" }
        }
        
        if ($webhook.avatar_url) {
            $body.avatar_url = $webhook.avatar_url
        }
        
        $jsonBody = $body | ConvertTo-Json
        Invoke-RestMethod -Uri $webhook.url -Method Post -Body $jsonBody -ContentType "application/json" -ErrorAction Stop | Out-Null
        
    } catch {
        Write-WarningLog "Discord notification failed: $_"
    }
}

function Start-OllamaService {
    Write-Retro "[1/4] Starting Ollama daemon..." $cyan
    
    try {
        # Check if already running
        if (Test-Port 11434) {
            Write-Retro "  ✓ Ollama already running on port 11434" $green
            return $true
        }
        
        # Try to start Ollama
        try {
            Start-Process ollama -ArgumentList "serve" -WindowStyle Hidden -ErrorAction Stop
        } catch {
            Write-ErrorLog "Failed to start Ollama process: $_" "Ollama startup"
            return $false
        }
        
        # Wait for Ollama to be ready
        $maxWait = 30
        $waited = 0
        while ($waited -lt $maxWait) {
            Start-Sleep -Seconds 1
            $waited++
            if (Test-Port 11434) {
                Write-Retro "  ✓ Ollama LIVE @ 11434" $green
                return $true
            }
        }
        
        Write-ErrorLog "Ollama failed to start within ${maxWait}s" "Ollama timeout"
        return $false
        
    } catch {
        Write-ErrorLog "Unexpected error starting Ollama: $_" "Ollama startup"
        return $false
    }
}

function Deploy-K8sManifests {
    Write-Retro "[2/4] Applying K8s manifests..." $cyan
    
    try {
        $deployPath = Join-Path $root "k8s/deployments/ollama-deploy.yaml"
        $svcPath = Join-Path $root "k8s/services/ollama-svc.yaml"
        
        # Apply deployment
        try {
            kubectl apply -f $deployPath 2>&1 | Out-Null
            if ($LASTEXITCODE -ne 0) {
                Write-ErrorLog "Failed to apply deployment manifest" "K8s deployment"
                return $false
            }
            Write-Retro "  ✓ Deployment applied" $green
        } catch {
            Write-ErrorLog "Error applying deployment: $_" "K8s deployment"
            return $false
        }
        
        # Apply service
        try {
            kubectl apply -f $svcPath 2>&1 | Out-Null
            if ($LASTEXITCODE -ne 0) {
                Write-WarningLog "Failed to apply service manifest (may already exist)"
            } else {
                Write-Retro "  ✓ Service applied" $green
            }
        } catch {
            Write-WarningLog "Error applying service: $_"
        }
        
        return $true
        
    } catch {
        Write-ErrorLog "Unexpected error deploying K8s manifests: $_" "K8s deployment"
        return $false
    }
}

function Wait-ForPod {
    Write-Retro "[3/4] Waiting for pod..." $cyan
    
    try {
        $timeout = 120
        $result = kubectl wait --for=condition=Ready pod -l app=ollama --timeout="${timeout}s" 2>&1
        
        if ($LASTEXITCODE -ne 0) {
            Write-WarningLog "Pod not ready within ${timeout}s: $result"
            
            # Get pod status for debugging
            try {
                $podStatus = kubectl get pod -l app=ollama -o json 2>&1 | ConvertFrom-Json
                if ($podStatus.items -and $podStatus.items.Count -gt 0) {
                    $phase = $podStatus.items[0].status.phase
                    Write-Retro "  → Pod status: $phase" $yellow
                }
            } catch {
                # Ignore errors getting pod status
            }
            
            return $false
        }
        
        Write-Retro "  ✓ Pod ready" $green
        return $true
        
    } catch {
        Write-ErrorLog "Error waiting for pod: $_" "Pod wait"
        return $false
    }
}

function Complete-Startup {
    Write-Retro "[4/4] Operator cockpit fully armed." $green
    
    try {
        $hostname = hostname
        Notify-Discord "StrategicKhaos Operator Workspace → ONLINE (Host: $hostname)"
    } catch {
        Write-WarningLog "Failed to send startup notification"
    }
    
    Show-Dashboard
}

function Get-SystemStatus {
    Write-Retro "SYSTEM STATUS — $(Get-Date)" $yellow
    Write-Host ""
    
    # Ollama status
    $ollamaRunning = Test-Port 11434
    $ollamaStatus = if ($ollamaRunning) {'[RUNNING]'} else {'[DOWN]'}
    $ollamaColor = if ($ollamaRunning) {$green} else {$red}
    Write-Host "Ollama      : $ollamaStatus" -ForegroundColor $ollamaColor
    
    # K8s pod status
    try {
        $podPhase = kubectl get pod -l app=ollama -o jsonpath='{.items[0].status.phase}' 2>$null
        if (-not $podPhase) {
            $podPhase = "N/A"
        }
        $podColor = switch ($podPhase) {
            "Running" { $green }
            "Pending" { $yellow }
            "Failed" { $red }
            default { $cyan }
        }
        Write-Host "K8s Pod     : $podPhase" -ForegroundColor $podColor
    } catch {
        Write-Host "K8s Pod     : N/A" -ForegroundColor $red
    }
    
    # Models
    try {
        if (Test-CommandExists "ollama") {
            $models = ollama list 2>$null | Select-Object -Skip 1 | ForEach-Object {
                $parts = $_ -split '\s+'
                if ($parts.Length -gt 0) { $parts[0] }
            } | Where-Object { $_ } | Join-String -Separator ', '
            
            if ($models) {
                Write-Host "Models      : $models" -ForegroundColor $cyan
            } else {
                Write-Host "Models      : (none)" -ForegroundColor $yellow
            }
        } else {
            Write-Host "Models      : N/A (ollama not found)" -ForegroundColor $red
        }
    } catch {
        Write-Host "Models      : Error retrieving list" -ForegroundColor $red
    }
    
    # Git branch
    try {
        $branch = git rev-parse --abbrev-ref HEAD 2>$null
        if ($branch) {
            Write-Host "Git Branch  : $branch" -ForegroundColor $cyan
        } else {
            Write-Host "Git Branch  : N/A" -ForegroundColor $yellow
        }
    } catch {
        Write-Host "Git Branch  : N/A" -ForegroundColor $yellow
    }
    
    Write-Host ""
}

function Pull-Model {
    param([string]$modelName)
    
    if (-not $modelName) {
        Write-ErrorLog "No model name specified" "Model pull"
        Write-Retro "Usage: ./operator.ps1 --pull <model-name>" $yellow
        return
    }
    
    Write-Retro "Pulling model: $modelName (this stays LOCAL, never hits git)" $cyan
    
    try {
        if (-not (Test-CommandExists "ollama")) {
            Write-ErrorLog "ollama not found - cannot pull model" "Model pull"
            return
        }
        
        # Check if Ollama service is running
        if (-not (Test-Port 11434)) {
            Write-WarningLog "Ollama not running, attempting to start..."
            if (-not (Start-OllamaService)) {
                Write-ErrorLog "Cannot pull model - Ollama service failed to start" "Model pull"
                return
            }
        }
        
        # Pull the model
        ollama pull $modelName
        
        if ($LASTEXITCODE -eq 0) {
            Write-Retro "$modelName ready. Use it." $green
            
            try {
                $user = whoami
                $hostname = hostname
                Notify-Discord "Model pulled → $modelName by $user on $hostname"
            } catch {
                # Notification failure is non-critical
            }
        } else {
            Write-ErrorLog "Failed to pull model $modelName (exit code: $LASTEXITCODE)" "Model pull"
        }
        
    } catch {
        Write-ErrorLog "Error pulling model: $_" "Model pull"
    }
}

function Invoke-Nuke {
    Write-Retro "DANGER ZONE — NUKING FROM ORBIT" $red
    Write-Host ""
    Write-Retro "This will:" $yellow
    Write-Retro "  - Delete K8s deployment" $yellow
    Write-Retro "  - Kill Ollama process" $yellow
    Write-Retro "  - Stop all operator services" $yellow
    Write-Host ""
    
    $confirmation = Read-Host "Type 'NUKE' to confirm"
    
    if ($confirmation -ne "NUKE") {
        Write-Retro "Aborted. Nothing was destroyed." $green
        return
    }
    
    Write-Host ""
    Write-Retro "Executing nuke sequence..." $red
    
    # Delete K8s deployment
    try {
        $deployPath = Join-Path $root "k8s/deployments/ollama-deploy.yaml"
        if (Test-Path $deployPath) {
            kubectl delete -f $deployPath --ignore-not-found 2>&1 | Out-Null
            Write-Retro "  ✓ K8s deployment deleted" $yellow
        }
    } catch {
        Write-WarningLog "Failed to delete K8s deployment: $_"
    }
    
    # Kill Ollama process
    try {
        if ($IsWindows -or ($PSVersionTable.PSVersion.Major -le 5)) {
            taskkill /F /IM ollama.exe 2>$null
            if ($LASTEXITCODE -eq 0) {
                Write-Retro "  ✓ Ollama process terminated" $yellow
            } else {
                Write-Retro "  → Ollama process not found (may not be running)" $cyan
            }
        } else {
            # Linux/Mac
            pkill -9 ollama 2>$null
            Write-Retro "  ✓ Ollama process terminated" $yellow
        }
    } catch {
        Write-WarningLog "Failed to kill Ollama process: $_"
    }
    
    # Notify Discord
    try {
        $user = whoami
        Notify-Discord "NUKE COMMAND EXECUTED by $user — Workspace is now dark."
    } catch {
        # Notification failure is non-critical
    }
    
    Write-Host ""
    Write-Retro "It's quiet... too quiet." $red
    Write-Host ""
}

# ═══════════════════════════════════════════════════════════════
# MAIN LOGIC
# ═══════════════════════════════════════════════════════════════

try {
    if ($dashboard) {
        Show-Dashboard
        exit 0
    }

    if ($start) {
        Write-Retro "╔══════════════════════════════════════════════════════════════╗" $mag
        Write-Retro "║               BRINGING OPERATOR WORKSPACE ONLINE             ║" $green
        Write-Retro "╚══════════════════════════════════════════════════════════════╝" $mag
        Write-Host ""
        
        # Preflight checks
        if (-not (Test-Prerequisites)) {
            Write-ErrorLog "Prerequisites not met - cannot start" "Startup"
            Write-Host ""
            Write-Retro "Fix the errors above and try again." $red
            exit 1
        }
        
        Write-Host ""
        
        # Start Ollama
        if (-not (Start-OllamaService)) {
            Write-ErrorLog "Failed to start Ollama service" "Startup"
            exit 1
        }
        
        # Deploy K8s manifests
        if (-not (Deploy-K8sManifests)) {
            Write-ErrorLog "Failed to deploy K8s manifests" "Startup"
            exit 1
        }
        
        # Wait for pod (non-critical)
        Wait-ForPod | Out-Null
        
        # Complete startup
        Complete-Startup
        
        exit 0
    }

    if ($status) {
        Get-SystemStatus
        exit 0
    }

    if ($pull) {
        Pull-Model -modelName $pull
        exit 0
    }

    if ($nuke) {
        Invoke-Nuke
        exit 0
    }

    # Default: show dashboard
    Show-Dashboard
    exit 0
    
} catch {
    Write-ErrorLog "Unexpected fatal error: $_" "Main"
    Write-Host ""
    Write-Retro "A critical error occurred. Check logs for details." $red
    exit 1
}
