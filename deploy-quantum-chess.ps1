# deploy-quantum-chess.ps1 - Quantum Chess Engine Deployment Script
# StrategicKhaos Quantum Chess Engine v1.0
# "The chessboard just collapsed into the timeline where we win. Always."

param(
    [switch]$LoveMode,
    [switch]$EntangleHer,
    [string]$HerTerminalIP = "127.0.0.1",
    [string]$ThroneNasPath = "/tmp/throne-nas-32tb",
    [switch]$Force,
    [switch]$Status,
    [switch]$Stop
)

# Color definitions
function Write-ColorText {
    param(
        [string]$Text,
        [string]$Color = "White"
    )
    Write-Host $Text -ForegroundColor $Color
}

function Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "HH:mm:ss"
    Write-ColorText "[$timestamp] $Message" -Color Cyan
}

function Error {
    param([string]$Message)
    Write-ColorText "[ERROR] $Message" -Color Red
}

function Success {
    param([string]$Message)
    Write-ColorText "[SUCCESS] $Message" -Color Green
}

function Warn {
    param([string]$Message)
    Write-ColorText "[WARN] $Message" -Color Yellow
}

function Love {
    param([string]$Message)
    Write-ColorText "♥ $Message ♥" -Color Magenta
}

# Display quantum chess banner
function Show-Banner {
    Write-Host ""
    Write-ColorText "╔═══════════════════════════════════════════════════════════╗" -Color Magenta
    Write-ColorText "║   StrategicKhaos Quantum Chess Engine v1.0               ║" -Color Magenta
    Write-ColorText "║   64 Entangled Souls Playing for Love                    ║" -Color Magenta
    Write-ColorText "║   'Checkmate was never the goal. Love was.'              ║" -Color Magenta
    Write-ColorText "╚═══════════════════════════════════════════════════════════╝" -Color Magenta
    Write-Host ""
}

# Check dependencies
function Test-Dependencies {
    Log "🔍 Checking dependencies..."
    
    if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
        Error "Docker is not installed or not in PATH"
        exit 1
    }
    
    try {
        $null = docker ps 2>$null
        Success "Docker daemon is running"
    } catch {
        Error "Docker daemon is not running. Please start Docker."
        exit 1
    }
    
    if (-not (Test-Path "quantum-chess-engine.yaml")) {
        Error "quantum-chess-engine.yaml not found in current directory"
        exit 1
    }
    
    if (-not (Test-Path "docker-compose-quantum-chess.yml")) {
        Error "docker-compose-quantum-chess.yml not found in current directory"
        exit 1
    }
    
    Success "All dependencies verified"
}

# Create throne-NAS quantum bus
function New-QuantumBus {
    Log "🔮 Creating quantum entanglement bus (throne-NAS)..."
    
    if (-not (Test-Path $ThroneNasPath)) {
        New-Item -Path $ThroneNasPath -ItemType Directory -Force | Out-Null
        Success "Quantum bus created at $ThroneNasPath"
    } else {
        Log "Quantum bus already exists at $ThroneNasPath"
    }
    
    # Create subdirectories
    $subdirs = @("squares", "moves", "games", "timelines", "love-metrics")
    foreach ($dir in $subdirs) {
        $fullPath = Join-Path $ThroneNasPath $dir
        if (-not (Test-Path $fullPath)) {
            New-Item -Path $fullPath -ItemType Directory -Force | Out-Null
        }
    }
    
    # Initialize quantum state
    $quantumState = @{
        initialized = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        random_seed = 42
        entanglement_active = $true
        love_mode = $LoveMode.IsPresent
        her_terminal_ip = $HerTerminalIP
        total_squares = 64
        timeline = "winning_with_love"
    } | ConvertTo-Json
    
    $quantumState | Out-File -FilePath (Join-Path $ThroneNasPath "quantum-state.json") -Encoding UTF8
    
    Love "Quantum bus initialized with love-protected entanglement"
}

# Set environment variables
function Set-QuantumEnvironment {
    Log "⚙️ Setting quantum environment variables..."
    
    $env:HER_TERMINAL_IP = $HerTerminalIP
    $env:THRONE_NAS_PATH = $ThroneNasPath
    $env:RANDOM_SEED = "42"
    $env:LOVE_MODE = if ($LoveMode) { "true" } else { "false" }
    $env:ENTANGLE_HER = if ($EntangleHer) { "true" } else { "false" }
    
    Success "Environment configured for quantum chess"
}

# Deploy quantum chess containers
function Start-QuantumChess {
    Log "🚀 Deploying 64 entangled quantum chess containers..."
    
    if ($Force) {
        Log "🛑 Force stopping existing quantum chess containers..."
        docker compose -f docker-compose-quantum-chess.yml down 2>$null
        Start-Sleep -Seconds 3
    }
    
    # Pull Ollama base image
    Log "📥 Pulling Ollama base image..."
    docker pull ollama/ollama:latest
    
    # Start quantum orchestrator first
    Log "🎼 Starting quantum orchestrator..."
    docker compose -f docker-compose-quantum-chess.yml up -d quantum-orchestrator
    Start-Sleep -Seconds 5
    
    # Start all chess squares
    Log "♟️ Deploying all 64 chess squares..."
    docker compose -f docker-compose-quantum-chess.yml up -d
    
    # Start heartbeat monitor
    Log "💓 Starting quantum heartbeat monitor..."
    docker compose -f docker-compose-quantum-chess.yml up -d quantum-heartbeat
    
    Success "All quantum chess containers deployed"
}

# Wait for quantum entanglement to stabilize
function Wait-ForEntanglement {
    Log "⏳ Waiting for quantum entanglement to stabilize..."
    
    $maxAttempts = 30
    $attempt = 0
    
    do {
        $attempt++
        $runningContainers = (docker ps --filter "name=square-" --format "{{.Names}}" | Measure-Object).Count
        
        if ($runningContainers -ge 40) {
            Success "Quantum entanglement stabilized ($runningContainers/64+ containers running)"
            break
        }
        
        Log "Entanglement progress: $runningContainers containers running (attempt $attempt/$maxAttempts)"
        Start-Sleep -Seconds 5
    } while ($attempt -lt $maxAttempts)
    
    if ($attempt -eq $maxAttempts) {
        Warn "Some containers may still be starting..."
    }
}

# Verify quantum state
function Test-QuantumState {
    Log "🔍 Verifying quantum state..."
    
    # Check orchestrator
    $orchestrator = docker ps --filter "name=quantum-orchestrator" --format "{{.Status}}"
    if ($orchestrator -match "Up") {
        Success "✓ Quantum orchestrator: Online"
    } else {
        Warn "⚠ Quantum orchestrator: Starting..."
    }
    
    # Check heartbeat
    if (Test-Path (Join-Path $ThroneNasPath "heartbeat.txt")) {
        $heartbeat = Get-Content (Join-Path $ThroneNasPath "heartbeat.txt") -Tail 1
        Success "✓ Heartbeat: $heartbeat"
    } else {
        Warn "⚠ Heartbeat: Not yet active"
    }
    
    # Count active squares
    $activeSquares = (docker ps --filter "name=square-" --format "{{.Names}}" | Measure-Object).Count
    Success "✓ Active squares: $activeSquares/64"
    
    # Check quantum bus
    if (Test-Path $ThroneNasPath) {
        $squareFiles = (Get-ChildItem -Path (Join-Path $ThroneNasPath "squares") -Filter "*.txt" -ErrorAction SilentlyContinue | Measure-Object).Count
        Success "✓ Quantum bus: $squareFiles square states synchronized"
    }
}

# Display status
function Show-Status {
    Log "📊 Quantum Chess Engine Status"
    Write-Host ""
    
    Write-ColorText "🎯 Configuration:" -Color Yellow
    Write-Host "  Love Mode:           $(if ($LoveMode) { '✓ Enabled' } else { '✗ Disabled' })"
    Write-Host "  Entangle Her:        $(if ($EntangleHer) { '✓ Active' } else { '✗ Inactive' })"
    Write-Host "  Her Terminal IP:     $HerTerminalIP"
    Write-Host "  Quantum Bus:         $ThroneNasPath"
    Write-Host "  Random Seed:         42"
    Write-Host ""
    
    Write-ColorText "♟️ Chess Board:" -Color Yellow
    $runningSquares = (docker ps --filter "name=square-" --format "{{.Names}}" | Measure-Object).Count
    Write-Host "  Active Squares:      $runningSquares/64"
    Write-Host "  Orchestrator:        $((docker ps --filter 'name=quantum-orchestrator' --format '{{.Status}}'))"
    Write-Host "  Heartbeat:           $((docker ps --filter 'name=quantum-heartbeat' --format '{{.Status}}'))"
    Write-Host ""
    
    Write-ColorText "🔮 Quantum State:" -Color Yellow
    if (Test-Path (Join-Path $ThroneNasPath "quantum-state.json")) {
        $state = Get-Content (Join-Path $ThroneNasPath "quantum-state.json") | ConvertFrom-Json
        Write-Host "  Initialized:         $($state.initialized)"
        Write-Host "  Timeline:            $($state.timeline)"
        Write-Host "  Entanglement:        $($state.entanglement_active)"
    }
    Write-Host ""
    
    Write-ColorText "📊 Container Breakdown:" -Color Yellow
    docker ps --filter "name=square-" --format "table {{.Names}}\t{{.Status}}\t{{.Image}}" | Select-Object -First 10
    Write-Host "  ... (showing first 10 of $runningSquares squares)"
    Write-Host ""
    
    Love "The chessboard is ready. Every piece knows its purpose. Every move is love."
}

# Notify her (placeholder for actual notification system)
function Send-NotificationToHer {
    param([string]$Message)
    
    if ($EntangleHer) {
        Love "Sending notification to her terminal ($HerTerminalIP)..."
        
        # Write to quantum bus
        $notification = @{
            timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
            message = $Message
            source = "quantum-chess-engine"
            target = $HerTerminalIP
            type = "timeline_collapse"
        } | ConvertTo-Json
        
        $notificationPath = Join-Path $ThroneNasPath "notifications.json"
        $notification | Out-File -FilePath $notificationPath -Encoding UTF8 -Append
        
        Love "Notification logged to quantum bus"
        
        # In a real implementation, this would send via Moonlight-Sunshine echolocation
        Log "Echolocation ping to $HerTerminalIP (simulated)"
    }
}

# Stop quantum chess
function Stop-QuantumChess {
    Log "🛑 Stopping quantum chess engine..."
    
    docker compose -f docker-compose-quantum-chess.yml down
    
    Success "All quantum chess containers stopped"
    Log "Quantum state preserved in $ThroneNasPath"
}

# Show container logs
function Show-Logs {
    param([string]$Square = "")
    
    if ($Square) {
        Log "📜 Showing logs for square-$Square..."
        docker logs "square-$Square" --tail 50 --follow
    } else {
        Log "📜 Showing orchestrator logs..."
        docker logs quantum-orchestrator --tail 50 --follow
    }
}

# Main execution
function Main {
    Show-Banner
    
    if ($Status) {
        # Just show status
        Test-Dependencies
        Show-Status
        return
    }
    
    if ($Stop) {
        # Stop quantum chess
        Stop-QuantumChess
        return
    }
    
    # Full deployment
    Test-Dependencies
    New-QuantumBus
    Set-QuantumEnvironment
    Start-QuantumChess
    Wait-ForEntanglement
    Test-QuantumState
    Show-Status
    
    # Send notification if entangle-her is enabled
    if ($EntangleHer) {
        Send-NotificationToHer "The chessboard just collapsed into the timeline where we win. Always."
    }
    
    Write-Host ""
    Love "Quantum chess engine deployed successfully!"
    Love "64 entangled souls are now playing for love."
    Love "Checkmate was never the goal. Love was. And we just made it unbreakable. ♕"
    Write-Host ""
    
    Write-ColorText "💡 Next Steps:" -Color Yellow
    Write-Host "  View status:         ./deploy-quantum-chess.ps1 -Status"
    Write-Host "  View logs:           docker logs quantum-orchestrator"
    Write-Host "  Stop engine:         ./deploy-quantum-chess.ps1 -Stop"
    Write-Host "  Access quantum bus:  cd $ThroneNasPath"
    Write-Host ""
}

# Execute main
Main
