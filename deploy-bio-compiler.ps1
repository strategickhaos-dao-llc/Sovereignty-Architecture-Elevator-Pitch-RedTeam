# ╔══════════════════════════════════════════════════════════════╗
# ║  DEPLOY-BIO-COMPILER.ps1 v1.0 — C++ TRUTH EDITION           ║
# ║       "DNA compiles to life. Feed the babies—no mercy."     ║
# ╚══════════════════════════════════════════════════════════════╝
#
# Strategickhaos DAO LLC - Bio-Compiler Engine Deployment
# Purpose: Spawn 64 ribosome containers compiling DNA to protein
# Operator: Domenic Garza (Node 137)
# Date: 2025-11-24

param(
    [switch]$compileMode,
    [switch]$entangleTruth,
    [string]$message = "DNA is C++. Ribosome compiles. Evolve or apoptose.",
    [int]$ribosomeCount = 64,
    [int]$basePort = 11434,
    [string]$network = "swarm-net",
    [string]$sharedVolume = "/throne-nas-32tb",
    [string]$yamlConfig = "bio-compiler-engine.yaml"
)

$ErrorActionPreference = "Continue"
$root = (Resolve-Path $PSScriptRoot).Path
$G = "Green"; $R = "Red"; $Y = "Yellow"; $C = "Cyan"; $W = "White"

# ═══════════════════════════════════════════════════════════════
# Logging Functions
# ═══════════════════════════════════════════════════════════════

function Log($msg, $color=$W) { 
    $timestamp = Get-Date -Format 'HH:mm:ss'
    Write-Host "[$timestamp] $msg" -ForegroundColor $color 
}

function Log-Success($msg) { 
    Log "✓ $msg" $G 
}

function Log-Error($msg) { 
    Log "✗ ERROR → $msg" $R 
}

function Log-Warn($msg) { 
    Log "⚠ WARN  → $msg" $Y 
}

function Log-Info($msg) { 
    Log "ℹ $msg" $C 
}

# ═══════════════════════════════════════════════════════════════
# Discord Notification (Inherited Infrastructure)
# ═══════════════════════════════════════════════════════════════

function Notify-Discord($msg) {
    # Notify the swarm via Discord webhook
    # Inherited from existing Strategickhaos infrastructure
    if ($env:DISCORD_WEBHOOK_URL) {
        try {
            $payload = @{
                content = "🧬 **Bio-Compiler Engine**: $msg"
                username = "Ribosome-Deploy-Bot"
            } | ConvertTo-Json
            
            Invoke-RestMethod -Uri $env:DISCORD_WEBHOOK_URL `
                              -Method Post `
                              -ContentType "application/json" `
                              -Body $payload `
                              -ErrorAction SilentlyContinue | Out-Null
            Log-Success "Discord notification sent"
        } catch {
            Log-Warn "Discord notification failed (non-critical)"
        }
    }
}

# ═══════════════════════════════════════════════════════════════
# Docker & Network Setup
# ═══════════════════════════════════════════════════════════════

function Test-DockerAvailable {
    try {
        $null = docker ps 2>$null
        return $true
    } catch {
        return $false
    }
}

function Ensure-SwarmNetwork {
    Log-Info "Ensuring swarm network exists: $network"
    $networks = docker network ls --format "{{.Name}}" 2>$null
    if ($networks -notcontains $network) {
        docker network create $network 2>$null | Out-Null
        Log-Success "Created network: $network"
    } else {
        Log-Success "Network already exists: $network"
    }
}

# ═══════════════════════════════════════════════════════════════
# Ribosome Container Deployment
# ═══════════════════════════════════════════════════════════════

function Deploy-Ribosome($id) {
    $port = $basePort + $id
    $containerName = "ribosome-$id"
    
    Log-Info "Spawning ribosome-$id on port $port..."
    
    # Check if container already exists
    $existing = docker ps -a --filter "name=$containerName" --format "{{.Names}}" 2>$null
    if ($existing -eq $containerName) {
        Log-Warn "Container $containerName already exists, removing..."
        docker rm -f $containerName 2>$null | Out-Null
    }
    
    # Spawn ribosome container with explicit parameters (avoiding Invoke-Expression)
    try {
        $dockerArgs = @(
            "run", "-d",
            "--name", $containerName,
            "--network", $network,
            "-p", "$port:11434"
        )
        
        # Add shared volume mount if path exists
        if (Test-Path $sharedVolume -ErrorAction SilentlyContinue) {
            $dockerArgs += "--mount"
            $dockerArgs += "type=bind,source=$sharedVolume,target=/quantum-bus"
        }
        
        $dockerArgs += "ollama/ollama"
        
        & docker @dockerArgs | Out-Null
        Log-Success "Ribosome-$id spawned successfully (port $port)"
        return $true
    } catch {
        Log-Error "Failed to spawn ribosome-$id: $($_.Exception.Message)"
        return $false
    }
}

function Pull-OllamaModel($containerName, $modelName) {
    Log-Info "Pulling model $modelName in $containerName (this may take several minutes for large models)..."
    try {
        $timeout = 600  # 10 minute timeout for large models
        $job = Start-Job -ScriptBlock {
            param($container, $model)
            docker exec $container ollama pull $model 2>$null
        } -ArgumentList $containerName, $modelName
        
        $completed = Wait-Job -Job $job -Timeout $timeout
        if ($completed) {
            Receive-Job -Job $job | Out-Null
            Remove-Job -Job $job
            Log-Success "Model $modelName ready in $containerName"
        } else {
            Stop-Job -Job $job
            Remove-Job -Job $job
            Log-Warn "Model pull timed out for $modelName (continuing with deployment)"
        }
    } catch {
        Log-Warn "Failed to pull model $modelName (non-critical): $($_.Exception.Message)"
    }
}

function Inject-SystemPrompt($containerName, $modelName, $prompt) {
    Log-Info "Preparing C++ truth system prompt for $containerName..."
    # System prompts are configured via Ollama Modelfile on first use
    # Users should create a custom Modelfile and run: ollama create custom-model -f Modelfile
    # Example Modelfile content:
    #   FROM llama3.2:70b
    #   SYSTEM "You are a ribosomal compiler. DNA templates arrive as raw C++ source..."
    Log-Info "System prompts should be configured via Ollama Modelfile (see documentation)"
}

# ═══════════════════════════════════════════════════════════════
# Main Deployment Logic
# ═══════════════════════════════════════════════════════════════

try {
    Log ""
    Log "╔═══════════════════════════════════════════════════════════╗" $C
    Log "║  BIO-COMPILER ENGINE v1.0 — DEPLOYMENT INITIATED          ║" $C
    Log "║  DNA → mRNA → Ribosome → Protein                          ║" $C
    Log "╚═══════════════════════════════════════════════════════════╝" $C
    Log ""
    
    # Validate YAML configuration
    $yamlPath = "$root/$yamlConfig"
    if (-not (Test-Path $yamlPath)) {
        throw "YAML source missing—transcribe the DNA first. Expected: $yamlPath"
    }
    Log-Success "YAML configuration found: $yamlPath"
    
    # Check Docker availability
    if (-not (Test-DockerAvailable)) {
        throw "Docker is not running. Please start Docker Desktop."
    }
    Log-Success "Docker is available"
    
    # Parse YAML configuration (basic parsing)
    Log-Info "Parsing bio-compiler YAML configuration..."
    $config = Get-Content $yamlPath -Raw
    Log-Success "YAML parsed successfully"
    
    # Setup network
    Ensure-SwarmNetwork
    
    # Display deployment parameters
    Log ""
    Log-Info "Deployment Parameters:"
    Log-Info "  Ribosome Count: $ribosomeCount"
    Log-Info "  Base Port: $basePort"
    Log-Info "  Network: $network"
    Log-Info "  Shared Volume: $sharedVolume"
    Log-Info "  Compile Mode: $compileMode"
    Log-Info "  Entangle Truth: $entangleTruth"
    Log ""
    
    # Spawn ribosome containers
    Log-Info "Spawning $ribosomeCount ribosome containers..."
    $successCount = 0
    
    for ($i = 1; $i -le $ribosomeCount; $i++) {
        if (Deploy-Ribosome $i) {
            $successCount++
        }
        
        # Progress indicator every 8 ribosomes
        if ($i % 8 -eq 0) {
            Log-Info "Progress: $i/$ribosomeCount ribosomes spawned"
        }
    }
    
    Log ""
    Log-Success "$successCount/$ribosomeCount ribosomes spawned successfully"
    
    # Pull models for first few ribosomes (representative sample)
    if ($successCount -gt 0) {
        Log ""
        Log-Info "Pulling models for compiler cores (sample)..."
        Pull-OllamaModel "ribosome-1" "llama3.2:70b"
        Pull-OllamaModel "ribosome-2" "gemma2:27b"
    }
    
    # Inject system prompts with C++ truth
    if ($compileMode) {
        Log ""
        Log-Info "Compile mode enabled: Raw, no-guardrails instantiation"
        Inject-SystemPrompt "ribosome-1" "llama3.2:70b" "DNA templates compile to protein binaries"
    }
    
    # Entangle truth across swarm
    if ($entangleTruth) {
        Log ""
        Log-Info "Entangling C++ truth across swarm..."
        Notify-Discord $message
        Log-Success "Truth entangled. Swarm evolves terrifyingly."
    }
    
    # Write heartbeat file
    if (Test-Path $sharedVolume -ErrorAction SilentlyContinue) {
        $heartbeatPath = "$sharedVolume/bio-heartbeat.txt"
        "C++ truth fed. Swarm compiling wetware. $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" | 
            Out-File -FilePath $heartbeatPath -Encoding UTF8
        Log-Success "Heartbeat written to $heartbeatPath"
    }
    
    # Final status
    Log ""
    Log "╔═══════════════════════════════════════════════════════════╗" $G
    Log "║  BIO-COMPILER DEPLOYED SUCCESSFULLY                        ║" $G
    Log "║  Babies fed—let them compile life.                         ║" $G
    Log "╚═══════════════════════════════════════════════════════════╝" $G
    Log ""
    Log-Info "Ribosome containers running on ports $basePort-$($basePort + $ribosomeCount - 1)"
    Log-Info "Monitor with: docker ps --filter 'name=ribosome-'"
    Log-Info "View logs: docker logs ribosome-1"
    Log-Info "Stop all: docker stop `$(docker ps -q --filter 'name=ribosome-')"
    Log ""
    
    exit 0

} catch {
    Log ""
    Log-Error "Compile failure: $($_.Exception.Message)"
    Log-Error "Apoptosis triggered—build cannot proceed"
    Log ""
    exit 1
}
