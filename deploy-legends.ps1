# deploy-legends.ps1
# Deployment script for Legends of Minds v1

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  Legends of Minds v1 - Deployment Script" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

# Configuration
$BigDrive = "F:"
$ProjectPath = "C:\legends_of_minds"

Write-Host "Step 1: Setting up storage directories..." -ForegroundColor Yellow

# 1. Move Ollama to your big drive (if not already done)
Write-Host "  Creating Ollama data directories on $BigDrive..." -ForegroundColor Gray
New-Item -ItemType Directory -Path "$BigDrive\OllamaData\models" -Force | Out-Null
New-Item -ItemType Directory -Path "$BigDrive\OllamaData\tmp" -Force | Out-Null

# Check if Ollama data needs to be moved
$OllamaSource = "$env:USERPROFILE\.ollama"
if (Test-Path $OllamaSource) {
    Write-Host "  Found existing Ollama data at $OllamaSource" -ForegroundColor Gray
    Write-Host "  Migrating to $BigDrive\OllamaData (this may take a while)..." -ForegroundColor Gray
    robocopy "$OllamaSource" "$BigDrive\OllamaData" /MIR /MT:32 /NFL /NDL /NJH /NJS
    Write-Host "  ✓ Ollama data migrated" -ForegroundColor Green
} else {
    Write-Host "  ✓ Ollama directories created" -ForegroundColor Green
}

# 2. Create storage folders
Write-Host ""
Write-Host "Step 2: Creating additional storage directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Path "$BigDrive\qdrant_storage" -Force | Out-Null
New-Item -ItemType Directory -Path "$BigDrive\uploads" -Force | Out-Null
Write-Host "  ✓ Storage directories created" -ForegroundColor Green

# 3. Check Docker is running
Write-Host ""
Write-Host "Step 3: Checking Docker..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version
    Write-Host "  ✓ Docker found: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Docker not found or not running!" -ForegroundColor Red
    Write-Host "  Please install Docker Desktop and try again." -ForegroundColor Red
    exit 1
}

# 4. Check if project directory exists
Write-Host ""
Write-Host "Step 4: Checking project directory..." -ForegroundColor Yellow
if (Test-Path $ProjectPath) {
    Write-Host "  ✓ Project directory found at $ProjectPath" -ForegroundColor Green
} else {
    Write-Host "  ✗ Project directory not found at $ProjectPath" -ForegroundColor Red
    Write-Host "  Please clone or copy the Legends of Minds repository to $ProjectPath" -ForegroundColor Red
    exit 1
}

# 5. Deploy the stack
Write-Host ""
Write-Host "Step 5: Deploying Legends of Minds stack..." -ForegroundColor Yellow
Set-Location $ProjectPath

# Stop any existing containers
Write-Host "  Stopping existing containers..." -ForegroundColor Gray
docker compose -f docker-compose.legends.yml down 2>$null

# Start the stack
Write-Host "  Starting services..." -ForegroundColor Gray
docker compose -f docker-compose.legends.yml up -d

if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Stack deployed successfully!" -ForegroundColor Green
} else {
    Write-Host "  ✗ Deployment failed!" -ForegroundColor Red
    exit 1
}

# 6. Wait for services to be ready
Write-Host ""
Write-Host "Step 6: Waiting for services to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Check service health
Write-Host "  Checking service health..." -ForegroundColor Gray
$services = @{
    "Control Center" = "http://localhost:8080/health"
    "File Ingest" = "http://localhost:8001/health"
    "Qdrant" = "http://localhost:6333/health"
    "Ollama" = "http://localhost:11434/api/tags"
}

$allHealthy = $true
foreach ($service in $services.GetEnumerator()) {
    try {
        $response = Invoke-WebRequest -Uri $service.Value -TimeoutSec 5 -UseBasicParsing
        if ($response.StatusCode -eq 200) {
            Write-Host "  ✓ $($service.Key): Online" -ForegroundColor Green
        } else {
            Write-Host "  ⚠ $($service.Key): Returned status $($response.StatusCode)" -ForegroundColor Yellow
            $allHealthy = $false
        }
    } catch {
        Write-Host "  ✗ $($service.Key): Offline or not ready yet" -ForegroundColor Red
        $allHealthy = $false
    }
}

# Summary
Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  Deployment Complete!" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

if ($allHealthy) {
    Write-Host "✓ All services are online and healthy" -ForegroundColor Green
} else {
    Write-Host "⚠ Some services may need more time to start" -ForegroundColor Yellow
    Write-Host "  Run ./verify-legends.ps1 to check status again" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Access your Legends of Minds system at:" -ForegroundColor Cyan
Write-Host "  • Control Center:  http://localhost:8080" -ForegroundColor White
Write-Host "  • File Ingest:     http://localhost:8001/docs" -ForegroundColor White
Write-Host "  • Qdrant UI:       http://localhost:6334" -ForegroundColor White
Write-Host "  • Ollama API:      http://localhost:11434" -ForegroundColor White
Write-Host ""
Write-Host "To view logs: docker compose -f docker-compose.legends.yml logs -f" -ForegroundColor Gray
Write-Host "To stop:      docker compose -f docker-compose.legends.yml down" -ForegroundColor Gray
Write-Host ""
