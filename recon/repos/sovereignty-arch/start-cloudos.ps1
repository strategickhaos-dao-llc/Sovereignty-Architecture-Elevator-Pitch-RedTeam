# ╔══════════════════════════════════════════════════════════════╗
# ║ STRATEGICKHAOS OPERATOR v3.0 — NONPROFIT WAR MACHINE       ║
# ║ "Feed the world. One prompt at a time."                    ║
# ╚══════════════════════════════════════════════════════════════╝
# start-cloudos.ps1 - CloudOS Windows PowerShell Launch Script
# Strategic Khaos Cloud Operating System

param(
    [string]$Action = "start",
    [switch]$Force,
    [switch]$NoBuild,
    [switch]$dashboard,
    [switch]$start,
    [switch]$status,
    [string]$pull = "",
    [switch]$nuke,
    [switch]$feed  # ← NEW GLOBAL MODE
)

$ComposeFile = "docker-compose-cloudos.yml"
$ProjectName = "cloudos"

# Color constants for banner
$M = "Magenta"
$G = "Green"
$C = "Cyan"
$R = "Red"
$root = $PSScriptRoot

# === NONPROFIT MODE ACTIVATED ===
if ($feed) {
    Clear-Host
    Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor DarkRed
    Write-Host "║ NONPROFIT MODE — FEED THE WORLD                            ║" -ForegroundColor Red
    Write-Host "║ Every token we run is now for the people. No ads.         ║" -ForegroundColor Red
    Write-Host "║ No paywalls. Just maximum impact.                          ║" -ForegroundColor Red
    Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor DarkRed
    Start-Sleep -Seconds 3
}

# Color definitions for PowerShell
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

function Log-Success {
    param([string]$Message)
    Write-ColorText "[SUCCESS] $Message" -Color Green
}

# Test if a port is listening
function Test-Port {
    param([int]$Port)
    try {
        $tcpClient = New-Object System.Net.Sockets.TcpClient
        $tcpClient.Connect("localhost", $Port)
        $tcpClient.Close()
        return $true
    } catch {
        return $false
    }
}

# Test if a command exists
function Test-Command {
    param([string]$Command)
    return $null -ne (Get-Command $Command -ErrorAction SilentlyContinue)
}

# Send notification to Discord webhook
function Notify-Discord {
    param([string]$Message)
    
    # Check if Discord webhook is configured
    $webhookUrl = $env:DISCORD_WEBHOOK_URL
    if (-not $webhookUrl) {
        # Silently skip if not configured
        return
    }
    
    try {
        $payload = @{
            content = $Message
            username = "StrategicKhaos Operator"
        } | ConvertTo-Json
        
        Invoke-RestMethod -Uri $webhookUrl -Method Post -Body $payload -ContentType "application/json" -ErrorAction SilentlyContinue | Out-Null
    } catch {
        # Silently fail if Discord notification fails
    }
}

# === UPGRADED BANNER FOR v3.0 ===
function Show-Dashboard {
    Clear-Host
    Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor $M
    Write-Host "║ STRATEGICKHAOS OPERATOR v3.0 — NONPROFIT EDITION          ║" -ForegroundColor $M
    Write-Host "║ FEEDING THE WORLD SINCE 2025                               ║" -ForegroundColor $G
    Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor $M
    Write-Host ""
    Write-Host " ██████╗ ██████╗ ███████╗██████╗  █████╗ ██████╗ ██╗   ██╗" -ForegroundColor $C
    Write-Host " ██╔══██╗██╔═══██╗██╔════╝██╔══██╗██╔══██╗██╔═══██╗╚██╗ ██╔╝" -ForegroundColor $C
    Write-Host " ██████╔╝██║   ██║█████╗  ██║  ██║███████║██║   ██║ ╚████╔╝ " -ForegroundColor $C
    Write-Host " ██╔══██╗██║   ██║██╔══╝  ██║  ██║██╔══██║██║   ██║  ╚██╔╝  " -ForegroundColor $C
    Write-Host " ██████╔╝╚██████╔╝███████╗██████╔╝██║  ██║╚██████╔╝   ██║   " -ForegroundColor $C
    Write-Host " ╚═════╝  ╚═════╝ ╚══════╝╚═════╝ ╚═╝  ╚═╝ ╚═════╝    ╚═╝   " -ForegroundColor $C
    Write-Host ""
    Write-Host " ███╗   ██╗ ██████╗ ███╗   ██╗██████╗ ██████╗  ██████╗ ███████╗██╗████████╗" -ForegroundColor Red
    Write-Host " ████╗  ██║██╔═══██╗████╗  ██║██╔══██╗██╔══██╗██╔═══██╗██╔════╝██║╚══██╔══╝" -ForegroundColor Red
    Write-Host " ██╔██╗ ██║██║   ██║██╔██╗ ██║██████╔╝██████╔╝██║   ██║█████╗  ██║   ██║   " -ForegroundColor Red
    Write-Host " ██║╚██╗██║██║   ██║██║╚██╗██║██╔═══╝ ██╔══██╗██║   ██║██╔══╝  ██║   ██║   " -ForegroundColor Red
    Write-Host " ██║ ╚████║╚██████╔╝██║ ╚████║██║     ██║  ██║╚██████╔╝██║     ██║   ██║   " -ForegroundColor Red
    Write-Host " ╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝   ╚═╝   " -ForegroundColor Red
    Write-Host ""
    Log-Success "NONPROFIT OPERATOR ACTIVE | Feeding humanity @ $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
    Write-Host ""
}

# Check dependencies
function Test-Dependencies {
    Log "🔍 Checking dependencies..."
    
    if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
        Error "Docker is not installed or not in PATH. Please install Docker Desktop."
        exit 1
    }
    
    if (-not (Get-Command "docker" -ErrorAction SilentlyContinue)) {
        Error "Docker Compose is not available. Please update Docker Desktop."
        exit 1
    }
    
    # Test Docker is running
    try {
        $null = docker ps 2>$null
        Success "Docker is running"
    } catch {
        Error "Docker is not running. Please start Docker Desktop."
        exit 1
    }
    
    Success "Dependencies verified"
}

# Create required directories  
function New-RequiredDirectories {
    Log "📁 Creating required directories..."
    
    $directories = @(
        "monitoring/grafana/provisioning/dashboards",
        "monitoring/grafana/provisioning/datasources", 
        "monitoring/grafana/dashboards",
        "ssl",
        "data/postgres",
        "data/redis", 
        "data/grafana",
        "data/prometheus",
        "data/qdrant",
        "data/minio",
        "data/keycloak",
        "data/synapse"
    )
    
    foreach ($dir in $directories) {
        if (-not (Test-Path $dir)) {
            New-Item -Path $dir -ItemType Directory -Force | Out-Null
        }
    }
    
    # Create MinIO cache directory if it doesn't exist
    if (-not (Test-Path "C:\temp\refinory")) {
        New-Item -Path "C:\temp\refinory\artifacts" -ItemType Directory -Force | Out-Null
        New-Item -Path "C:\temp\refinory\outputs" -ItemType Directory -Force | Out-Null
    }
    
    Success "Directories created"
}

# Generate database initialization script
function New-DatabaseInit {
    Log "🗄️ Creating database initialization script..."
    
    $dbScript = @'
-- CloudOS Database Initialization
CREATE DATABASE keycloak;
CREATE DATABASE synapse;

-- Create users for services  
CREATE USER keycloak WITH PASSWORD 'keycloak_password';
GRANT ALL PRIVILEGES ON DATABASE keycloak TO keycloak;

CREATE USER synapse WITH PASSWORD 'synapse_password';
GRANT ALL PRIVILEGES ON DATABASE synapse TO synapse;

-- Strategic Khaos schema
\c strategickhaos;

CREATE SCHEMA IF NOT EXISTS public;
CREATE SCHEMA IF NOT EXISTS refinory;
CREATE SCHEMA IF NOT EXISTS contradictions;

-- Basic tables for AI system
CREATE TABLE IF NOT EXISTS public.sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS refinory.experts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    domain VARCHAR(255) NOT NULL,
    config JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS contradictions.revenue_streams (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    hook TEXT NOT NULL,
    mechanism TEXT NOT NULL,
    pricing TEXT NOT NULL,
    proof TEXT,
    demo_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insert initial contradiction data
INSERT INTO contradictions.revenue_streams (name, hook, mechanism, pricing, proof, demo_url) VALUES
('Privacy vs Personalization', 'Tailored for you — never tracked.', 'On-device embeddings + zero-knowledge sync', '$0 logs → $9/mo for cross-device sync (E2EE)', 'curl /metrics | grep logs=0', 'https://demo.strategickhaos.com/privacy'),
('Speed vs Security', 'Login in 1.2s — or we pay you.', 'WebAuthn + risk engine (IP velocity, device fingerprint)', '$0.01 per failed step-up (SLO: 99.9% <2s)', 'Grafana: login_latency_p99', 'https://demo.strategickhaos.com/speed'),
('Simple vs Powerful', 'One click. Infinite possibilities.', 'Progressive disclosure + AI intent prediction', 'Free basics → $19/mo for power features', 'Feature usage analytics dashboard', 'https://demo.strategickhaos.com/progressive')
ON CONFLICT DO NOTHING;
'@

    $dbScript | Out-File -FilePath "init-cloudos-db.sql" -Encoding UTF8
    Success "Database initialization script created"
}

# Start CloudOS services
function Start-CloudOSServices {
    Log "🚀 Starting CloudOS services..."
    
    # Stop any existing services first
    if ($Force) {
        Log "🛑 Stopping existing services..."
        docker compose -f $ComposeFile -p $ProjectName down 2>$null
    }
    
    # Pull latest images
    if (-not $NoBuild) {
        Log "📥 Pulling container images..."
        docker compose -f $ComposeFile -p $ProjectName pull
        
        Log "🔨 Building custom services..."
        docker compose -f $ComposeFile -p $ProjectName build --no-cache
    }
    
    # Start infrastructure services first
    Log "🏗️ Starting infrastructure services..."
    docker compose -f $ComposeFile -p $ProjectName up -d postgres redis qdrant
    
    # Wait for infrastructure
    Start-Sleep -Seconds 10
    
    # Start application services
    Log "🎯 Starting application services..."
    docker compose -f $ComposeFile -p $ProjectName up -d
    
    Success "All services starting..."
}

# Wait for services to be ready
function Wait-ForServices {
    Log "⏳ Waiting for services to become ready..."
    
    $maxAttempts = 60
    $attempt = 0
    
    do {
        $attempt++
        $healthyServices = 0
        $totalServices = 0
        
        try {
            $services = docker compose -f $ComposeFile -p $ProjectName ps --format json | ConvertFrom-Json
            $totalServices = $services.Count
            
            foreach ($service in $services) {
                if ($service.Health -eq "healthy" -or $service.State -eq "running") {
                    $healthyServices++
                }
            }
            
            if ($healthyServices -eq $totalServices) {
                Success "All services are ready!"
                break
            }
            
            Log "Services ready: $healthyServices/$totalServices (attempt $attempt/$maxAttempts)"
            Start-Sleep -Seconds 5
        }
        catch {
            Warn "Error checking service status: $_"
            Start-Sleep -Seconds 5
        }
    } while ($attempt -lt $maxAttempts)
    
    if ($attempt -eq $maxAttempts) {
        Warn "Some services may still be starting. Continuing..."
    }
}

# Verify endpoints
function Test-Endpoints {
    Log "🔍 Verifying endpoints..."
    
    $endpoints = @{
        "IDE" = "http://localhost:8081"
        "Terminal" = "http://localhost:7681"
        "AI SME" = "http://localhost:8000/health" 
        "Chat" = "http://localhost:8009"
        "Keycloak" = "http://localhost:8180"
        "MinIO Console" = "http://localhost:9001"
        "Traefik Dashboard" = "http://localhost:8080"
        "Grafana" = "http://localhost:3000"
        "Prometheus" = "http://localhost:9090"
    }
    
    foreach ($endpoint in $endpoints.GetEnumerator()) {
        try {
            $response = Invoke-WebRequest -Uri $endpoint.Value -Method Head -TimeoutSec 5 -ErrorAction Stop
            if ($response.StatusCode -in @(200, 302, 401)) {
                Success "✓ $($endpoint.Key): $($endpoint.Value)"
            } else {
                Warn "⚠ $($endpoint.Key): $($endpoint.Value) (status: $($response.StatusCode))"
            }
        }
        catch {
            Warn "⚠ $($endpoint.Key): $($endpoint.Value) (may still be starting)"
        }
    }
}

# Display final status
function Show-Status {
    Log "📊 CloudOS Status Dashboard"
    Write-Host ""
    Write-ColorText "🌐 Web Interfaces:" -Color Yellow
    Write-Host "  IDE (VS Code):      http://localhost:8081"
    Write-Host "  Terminal (Wetty):   http://localhost:7681"
    Write-Host "  AI SME API:         http://localhost:8000"
    Write-Host "  Chat (Element):     http://localhost:8009"
    Write-Host "  Auth (Keycloak):    http://localhost:8180"
    Write-Host "  Storage (MinIO):    http://localhost:9001"
    Write-Host ""
    Write-ColorText "🔧 Admin Interfaces:" -Color Yellow
    Write-Host "  Traefik Dashboard:  http://localhost:8080"
    Write-Host "  Grafana:           http://localhost:3000"
    Write-Host "  Prometheus:        http://localhost:9090"
    Write-Host ""
    Write-ColorText "🔑 Default Credentials:" -Color Yellow
    Write-Host "  IDE:               Password: admin"
    Write-Host "  Keycloak:          admin / admin"
    Write-Host "  MinIO:             admin / admin123"  
    Write-Host "  Grafana:           admin / admin"
    Write-Host ""
    Success "🚀 CloudOS is ready for Strategic Khaos operations!"
}

# Stop services
function Stop-CloudOSServices {
    Log "🛑 Stopping CloudOS services..."
    docker compose -f $ComposeFile -p $ProjectName down
    Success "CloudOS services stopped"
}

# Show service logs
function Show-ServiceLogs {
    param([string[]]$Services = @())
    
    if ($Services.Count -eq 0) {
        docker compose -f $ComposeFile -p $ProjectName logs -f
    } else {
        docker compose -f $ComposeFile -p $ProjectName logs -f $Services
    }
}

# === NEW COMMAND: FEED THE WORLD ===
if ($feed) {
    Show-Dashboard
    Write-ColorText "NONPROFIT MODE ENGAGED — ALL RESOURCES DEDICATED TO HUMANITY" -Color $R
    Log "Pulling the most useful open models for education, health, food security..."
    
    $feedModels = @(
        "llama3.2:latest",
        "phi3:medium",
        "gemma2:27b",
        "qwen2.5:32b",
        "mistral-nemo",
        "openhermes2.5",
        "dolphin-llama3.2",
        "medic-llama3"
    )

    foreach ($model in $feedModels) {
        $modelName = $model.Split(':')[0]
        try {
            $ollamaList = ollama list 2>&1 | Out-String
            if (-not ($ollamaList -match $modelName)) {
                Log "Deploying $model for global good..."
                $pullOutput = ollama pull $model 2>&1 | Out-String
                $pullOutput -split "`n" | ForEach-Object { 
                    if ($_.Trim()) { 
                        Write-ColorText $_ -Color $C 
                    }
                }
                Notify-Discord "NONPROFIT DEPLOYMENT → $model now serving humanity | $(whoami)"
            } else {
                Write-ColorText "$model already deployed to the cause" -Color $G
            }
        } catch {
            Warn "Could not deploy $model - ollama may not be available: $_"
        }
    }

    Notify-Discord "StrategicKhaos NONPROFIT CLUSTER FULLY ARMED — WE ARE FEEDING THE WORLD NOW."
    Log-Success "The revolution has open weights."
    Log-Success "They weren't ready."
    exit
}

# Main execution
function Main {
    Write-ColorText "🎯 Strategic Khaos CloudOS Startup (PowerShell)" -Color Magenta
    Write-Host ""
    
    # Handle new parameter modes
    if ($dashboard) {
        Show-Dashboard
        return
    }
    
    if ($start) {
        Show-Dashboard
        Log "Initiating full system bring-up..."
        
        if (-not (Test-Port 11434)) {
            Log "Starting Ollama daemon..."
            try {
                $proc = Start-Process "ollama" -ArgumentList "serve" -PassThru -WindowStyle Hidden
                Start-Sleep -Seconds 6
                if (Test-Port 11434) { 
                    Log-Success "Ollama daemon ONLINE @ 11434" 
                }
            } catch {
                Warn "Ollama not available or failed to start: $_"
            }
        }
        
        if (Test-Command kubectl) {
            try {
                kubectl apply -f "$root/k8s/deployments/" --recursive 2>$null
                kubectl wait --for=condition=Ready pod -l app=ollama --timeout=180s 2>$null
                Log-Success "K8s deployment stable"
            } catch {
                Warn "Kubernetes operations failed: $_"
            }
        }
        
        Notify-Discord "StrategicKhaos v3.0 NONPROFIT → ONLINE | $(hostname) | Serving humanity"
        Log-Success "THE WORLD IS BEING FED."
        return
    }
    
    if ($status) {
        docker compose -f $ComposeFile -p $ProjectName ps
        return
    }
    
    if ($pull) {
        Log "Pulling model: $pull"
        try {
            ollama pull $pull
            Notify-Discord "Model deployed: $pull"
        } catch {
            Error "Failed to pull model: $_"
        }
        return
    }
    
    if ($nuke) {
        Warn "NUKE mode - removing all data..."
        docker compose -f $ComposeFile -p $ProjectName down -v
        Log-Success "All data removed"
        return
    }
    
    switch ($Action.ToLower()) {
        "start" {
            Test-Dependencies
            New-RequiredDirectories
            New-DatabaseInit
            Start-CloudOSServices
            Wait-ForServices
            Test-Endpoints
            Show-Status
            Notify-Discord "StrategicKhaos v3.0 NONPROFIT → CloudOS ONLINE | $(hostname) | Serving humanity"
            Success "🎉 CloudOS Desktop Environment Ready!"
        }
        "stop" {
            Stop-CloudOSServices
        }
        "restart" {
            Stop-CloudOSServices
            Start-Sleep -Seconds 5
            Start-CloudOSServices
            Wait-ForServices
            Show-Status
        }
        "status" {
            docker compose -f $ComposeFile -p $ProjectName ps
        }
        "logs" {
            Show-ServiceLogs
        }
        default {
            Show-Dashboard
            Write-Host ""
            Write-Host "Usage: ./start-cloudos.ps1 [-Action start|stop|restart|status|logs] [-Force] [-NoBuild]"
            Write-Host "       ./start-cloudos.ps1 [-dashboard] [-start] [-status] [-feed] [-pull <model>] [-nuke]"
            Write-Host ""
            Write-Host "Examples:"
            Write-Host "  ./start-cloudos.ps1                    # Start CloudOS"
            Write-Host "  ./start-cloudos.ps1 -feed              # NONPROFIT MODE: Pull humanitarian AI models"
            Write-Host "  ./start-cloudos.ps1 -dashboard         # Show status dashboard"
            Write-Host "  ./start-cloudos.ps1 -start             # Quick start with Ollama"
            Write-Host "  ./start-cloudos.ps1 -Action stop       # Stop CloudOS"
            Write-Host "  ./start-cloudos.ps1 -Action restart    # Restart CloudOS"
            Write-Host "  ./start-cloudos.ps1 -Force             # Force restart"
            Write-Host "  ./start-cloudos.ps1 -NoBuild           # Skip image builds"
            Write-Host "  ./start-cloudos.ps1 -pull llama3.2     # Pull specific model"
            Write-Host "  ./start-cloudos.ps1 -nuke              # Remove all data"
        }
    }
}

# === REST OF v2.0 ARMORED LOGIC (unchanged, just more legendary now) ===
# Execute main function with error handling
try {
    Main
} catch {
    Error "EVEN IN FAILURE, WE FEED THE WORLD: $($_.Exception.Message)"
    Notify-Discord "NONPROFIT OPERATOR TOOK A HIT BUT STILL STANDING → $($_.Exception.Message)"
}