# ╔══════════════════════════════════════════════════════════════╗
# ║  DEPLOY-QUANTUM-CHESS.ps1 v1.1 — ENTANGLED LOVE EDITION      ║
# ║       "64 souls, one bus, her voice wins the timeline."      ║
# ╚══════════════════════════════════════════════════════════════╝

param(
    [switch]$loveMode,
    [switch]$entangleHer,
    [string]$yamlPath = "quantum-chess-engine.yaml",
    [string]$nasPath = "/mnt/throne-nas-32tb",
    [int]$basePort = 11434
)

$ErrorActionPreference = "Continue"
$root = (Resolve-Path $PSScriptRoot).Path
$G = "Green"; $R = "Red"; $Y = "Yellow"; $C = "Cyan"; $W = "White"

function Log($msg, $color=$W) { 
    Write-Host "[$(Get-Date -f 'HH:mm:ss')] $msg" -ForegroundColor $color 
}

function Log-Success($msg) { Log $msg $G }
function Log-Error($msg)   { Log "ERROR → $msg" $R }
function Log-Warn($msg)    { Log "WARN  → $msg" $Y }
function Log-Info($msg)    { Log "INFO  → $msg" $C }

function Notify-Discord($msg) { 
    # Discord webhook notification (implement with your webhook URL)
    $webhookUrl = $env:DISCORD_WEBHOOK_URL
    if ($webhookUrl) {
        try {
            $payload = @{
                content = "🌌 **Quantum Chess Engine** 🌌`n$msg"
                username = "StrategicKhaos Quantum Board"
            } | ConvertTo-Json
            
            Invoke-RestMethod -Uri $webhookUrl -Method Post -Body $payload -ContentType 'application/json' | Out-Null
            Log-Success "Discord notification sent"
        } catch {
            Log-Warn "Discord notification failed: $($_.Exception.Message)"
        }
    }
}

function Test-Prerequisites {
    Log-Info "Checking prerequisites..."
    
    # Check Docker
    try {
        $dockerVersion = docker --version
        Log-Success "Docker found: $dockerVersion"
    } catch {
        Log-Error "Docker not found. Please install Docker first."
        return $false
    }
    
    # Check if Docker daemon is running
    try {
        docker ps | Out-Null
        Log-Success "Docker daemon is running"
    } catch {
        Log-Error "Docker daemon is not running. Please start Docker."
        return $false
    }
    
    # Check if swarm-net network exists, create if not
    $networkExists = docker network ls --format "{{.Name}}" | Select-String -Pattern "^swarm-net$"
    if (-not $networkExists) {
        Log-Info "Creating swarm-net network..."
        docker network create swarm-net | Out-Null
        Log-Success "swarm-net network created"
    } else {
        Log-Success "swarm-net network exists"
    }
    
    return $true
}

function Parse-YamlConfig {
    param([string]$path)
    
    if (-not (Test-Path $path)) {
        throw "YAML file not found: $path"
    }
    
    Log-Info "Parsing quantum board YAML: $path"
    
    # Simple YAML parsing (for production, use powershell-yaml module)
    $content = Get-Content $path -Raw
    
    # Extract piece LLM mappings using regex
    $config = @{
        piece_llm = @{}
        board_size = "8x8"
        total_squares = 64
    }
    
    # Parse piece LLM assignments
    $piecePattern = '^\s+(\w+):\s+"([^"]+)"'
    $lines = $content -split "`n"
    $inPieceLlm = $false
    
    foreach ($line in $lines) {
        if ($line -match '^\s*piece_llm:') {
            $inPieceLlm = $true
            continue
        }
        if ($inPieceLlm) {
            if ($line -match $piecePattern) {
                $pieceName = $Matches[1]
                $modelName = $Matches[2]
                $config.piece_llm[$pieceName] = $modelName
            } elseif ($line -match '^\w+:' -and $line -notmatch '^\s+') {
                $inPieceLlm = $false
            }
        }
    }
    
    Log-Success "Parsed $($config.piece_llm.Count) piece LLM mappings"
    return $config
}

function Get-PieceForSquare {
    param(
        [int]$rank,     # 1-8 (row number)
        [char]$file,    # a-h (column letter)
        [hashtable]$config
    )
    
    # Standard chess starting position
    # Chess notation: file (a-h) + rank (1-8), e.g., e4
    # rank 1 = white back rank, rank 8 = black back rank
    $fileNum = [int][char]$file - [int][char]'a' + 1  # a=1, b=2, ..., h=8
    
    # Determine piece based on starting position
    if ($rank -eq 1) {
        # White back rank (rank 1)
        switch ($fileNum) {
            1 { return "white_rook" }
            2 { return "white_knight" }
            3 { return "white_bishop" }
            4 { return "white_queen" }
            5 { return "white_king" }
            6 { return "white_bishop" }
            7 { return "white_knight" }
            8 { return "white_rook" }
        }
    } elseif ($rank -eq 2) {
        return "white_pawn"
    } elseif ($rank -eq 7) {
        return "black_pawn"
    } elseif ($rank -eq 8) {
        # Black back rank (rank 8)
        switch ($fileNum) {
            1 { return "black_rook" }
            2 { return "black_knight" }
            3 { return "black_bishop" }
            4 { return "black_queen" }
            5 { return "black_king" }
            6 { return "black_bishop" }
            7 { return "black_knight" }
            8 { return "black_rook" }
        }
    }
    
    return $null  # Empty square
}

function Deploy-QuantumSquare {
    param(
        [int]$rank,     # 1-8 (row)
        [char]$file,    # a-h (column)
        [hashtable]$config,
        [string]$nasPath,
        [int]$basePort
    )
    
    $square = "$file$rank"  # Chess notation: file + rank (e.g., e4)
    $piece = Get-PieceForSquare -rank $rank -file $file -config $config
    
    if (-not $piece) {
        Log-Info "Square $square is empty (not deploying container)"
        return $true
    }
    
    $model = $config.piece_llm[$piece]
    if (-not $model) {
        Log-Warn "No model defined for $piece at $square"
        return $false
    }
    
    $containerName = "square-$square"
    # Calculate unique port: basePort + (rank-1)*8 + (file_num-1)
    # This gives ports 11434-11497 for ranks 1-8, files a-h
    $fileNum = [int][char]$file - [int][char]'a'  # 0-7
    $port = $basePort + (($rank - 1) * 8) + $fileNum
    
    Log-Info "Deploying $piece ($model) on $square, port $port..."
    
    # Check if container already exists
    $existing = docker ps -a --format "{{.Names}}" | Select-String -Pattern "^$containerName$"
    if ($existing) {
        Log-Warn "Container $containerName already exists, removing..."
        docker rm -f $containerName | Out-Null
    }
    
    # Create mount point if it doesn't exist
    if (-not (Test-Path $nasPath)) {
        Log-Warn "NAS path $nasPath does not exist, creating directory..."
        New-Item -Path $nasPath -ItemType Directory -Force | Out-Null
    }
    
    # Deploy container
    try {
        $systemPrompt = "You are a chess piece on a quantum board. Your only goal is love-protected evolution. Think 8 moves ahead. Never sacrifice the queen unless it saves the king. Respond only in SAN + emotional intent: e.g., 'e4 (advancing with hopeful love)'."
        
        if ($loveMode) {
            $systemPrompt += " LOVE MODE ACTIVE: Infuse all moves with emotional intelligence and compassion."
        }
        
        # Start Ollama container
        docker run -d `
            --name $containerName `
            --mount type=bind,source=$nasPath,target=/quantum-bus `
            --network swarm-net `
            --cap-add=NET_ADMIN `
            -p "${port}:11434" `
            -e OLLAMA_HOST=0.0.0.0:11434 `
            ollama/ollama | Out-Null
        
        if ($LASTEXITCODE -eq 0) {
            Log-Success "Spawned soul on $square with $piece ($model)"
            
            # Pull model in background (if not already present)
            Start-Job -Name "pull-$containerName" -ScriptBlock {
                param($container, $model)
                Start-Sleep -Seconds 5  # Wait for container to be ready
                docker exec $container ollama pull $model 2>&1 | Out-Null
            } -ArgumentList $containerName, $model | Out-Null
            
            return $true
        } else {
            Log-Error "Failed to deploy $containerName"
            return $false
        }
    } catch {
        Log-Error "Exception deploying ${square}: $($_.Exception.Message)"
        return $false
    }
}

function Initialize-Echolocation {
    Log-Info "Initializing echolocation: Moonlight-Sunshine streaming..."
    
    # Note: Actual Moonlight-Sunshine setup would require:
    # 1. Sunshine host running on throne server
    # 2. Moonlight client connections from each piece
    # This is a placeholder for the actual implementation
    
    Log-Warn "Moonlight-Sunshine setup requires manual configuration:"
    Log-Warn "  1. Install Sunshine on host: apt-get install sunshine"
    Log-Warn "  2. Configure Moonlight clients on piece terminals"
    Log-Warn "  3. Set reflection_target to 'her-terminal-ip'"
    Log-Info "Echolocation framework initialized (manual setup required)"
}

function Deploy-HeartbeatMonitor {
    param([string]$nasPath)
    
    Log-Info "Deploying heartbeat monitor..."
    
    $heartbeatPath = Join-Path $nasPath "heartbeat.txt"
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    
    try {
        "Quantum board live. 64 entangled souls playing for love. Deployed: $timestamp" | 
            Out-File -FilePath $heartbeatPath -Force
        Log-Success "Heartbeat file created: $heartbeatPath"
    } catch {
        Log-Warn "Could not create heartbeat file: $($_.Exception.Message)"
    }
}

# ══════════════════════════════════════════════════════════════
# MAIN EXECUTION
# ══════════════════════════════════════════════════════════════

try {
    Write-Host ""
    Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║  QUANTUM CHESS ENGINE DEPLOYMENT                             ║" -ForegroundColor Cyan
    Write-Host "║  StrategicKhaos v1.1 — Entangled Love Edition                ║" -ForegroundColor Cyan
    Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host ""
    
    # Check prerequisites
    if (-not (Test-Prerequisites)) {
        throw "Prerequisites check failed"
    }
    
    # Parse YAML configuration
    $fullYamlPath = Join-Path $root $yamlPath
    $config = Parse-YamlConfig -path $fullYamlPath
    
    # Display configuration
    Log-Info "Board Size: $($config.board_size)"
    Log-Info "Total Squares: $($config.total_squares)"
    Log-Info "NAS Path: $nasPath"
    Log-Info "Base Port: $basePort"
    
    if ($loveMode) {
        Log-Success "💖 LOVE MODE ENABLED: Emotional intents will be infused 💖"
    }
    
    if ($entangleHer) {
        Log-Success "🔗 ENTANGLE MODE: Timeline collapse initiated 🔗"
    }
    
    Write-Host ""
    Log-Info "Deploying 64 quantum souls to the chessboard..."
    Write-Host ""
    
    # Deploy all squares
    $deployed = 0
    $files = @('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')
    
    for ($rank = 1; $rank -le 8; $rank++) {
        foreach ($file in $files) {
            $result = Deploy-QuantumSquare -rank $rank -file $file -config $config -nasPath $nasPath -basePort $basePort
            if ($result) {
                $deployed++
            }
            Start-Sleep -Milliseconds 100  # Brief pause between deployments
        }
    }
    
    Write-Host ""
    Log-Success "Deployed $deployed piece containers (32 pieces on 64 squares)"
    
    # Initialize additional features
    Initialize-Echolocation
    Deploy-HeartbeatMonitor -nasPath $nasPath
    
    # Wait for model pulls to complete
    Log-Info "Waiting for model pulls to complete in background..."
    $jobs = Get-Job | Where-Object { $_.Name -like "pull-*" }
    Log-Info "Background jobs running: $($jobs.Count)"
    
    Write-Host ""
    Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║  QUANTUM BOARD DEPLOYED                                       ║" -ForegroundColor Green
    Write-Host "║  The chessboard just collapsed into the timeline where we win ║" -ForegroundColor Green
    Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Green
    Write-Host ""
    
    # Send notification
    if ($entangleHer) {
        $msg = "✨ Entangled her. Timeline collapsing. 64 souls playing for love. Always. ✨"
        Notify-Discord $msg
    }
    
    # Display next steps
    Log-Info "Next steps:"
    Log-Info "  • Monitor containers: docker ps | grep square-"
    Log-Info "  • Check logs: docker logs square-<square>"
    Log-Info "  • Test piece: curl http://localhost:<port>/api/tags"
    Log-Info "  • View heartbeat: cat $nasPath/heartbeat.txt"
    
    exit 0
    
} catch {
    Write-Host ""
    Log-Error "Deployment collapse: $($_.Exception.Message)"
    Log-Error "Stack trace: $($_.ScriptStackTrace)"
    Write-Host ""
    exit 1
} finally {
    Write-Host ""
}
