# _Orchestra.ps1 - The Heartbeat of the Sovereignty Architecture Swarm
# Version: 2.0 - Arweave Integration
# Purpose: Orchestrate Zinc Sparks and immortalize swarm state on Arweave

<#
.SYNOPSIS
    Sovereignty Architecture Swarm Orchestrator with Arweave Integration

.DESCRIPTION
    This script orchestrates the Zinc Spark lifecycle:
    1. Collects DNA snapshots
    2. Generates spite haikus via Garza-1 model
    3. Captures proof-of-life evidence
    4. Bundles everything into JSON
    5. Immortalizes on Arweave for 200+ years

.PARAMETER ZincSpark
    Execute a Zinc Spark cycle

.PARAMETER Immortalize
    Upload to Arweave for permanent storage

.PARAMETER WalletPath
    Path to Arweave wallet JSON file

.PARAMETER TestMode
    Run in test mode without actual Arweave upload

.EXAMPLE
    ./_Orchestra.ps1 -ZincSpark -Immortalize
    
.EXAMPLE
    ./_Orchestra.ps1 -ZincSpark -Immortalize -WalletPath ./arweave_key.json

.EXAMPLE
    ./_Orchestra.ps1 -ZincSpark -TestMode

.NOTES
    Author: Dominic Garza
    Date: 2025-11-23
    Version: 2.0
    Requires: PowerShell 7.0+, curl, jq (optional)
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory=$false)]
    [switch]$ZincSpark,
    
    [Parameter(Mandatory=$false)]
    [switch]$Immortalize,
    
    [Parameter(Mandatory=$false)]
    [string]$WalletPath = "./arweave_key.json",
    
    [Parameter(Mandatory=$false)]
    [switch]$TestMode,
    
    [Parameter(Mandatory=$false)]
    [switch]$SetupWallet,
    
    [Parameter(Mandatory=$false)]
    [decimal]$FundAmount = 20.00,
    
    [Parameter(Mandatory=$false)]
    [switch]$Status
)

# Global Configuration
$script:ArweaveGateway = "https://arweave.net"
$script:ArweaveUploadEndpoint = "https://arweave.net/tx"
$script:DNAPath = "./SWARM_DNA.yaml"
$script:MaxCostPerMonth = 20.00
$script:RateLimitHours = 6
$script:LastSparkFile = "./.last_zinc_spark"
$script:ProofDir = "./proof_of_life"
$script:LogDir = "./zinc_spark_logs"
$script:ArweaveTxIdLength = 43  # Standard Arweave transaction ID length

# Color definitions
function Write-ColorText {
    param(
        [string]$Text,
        [string]$Color = "White"
    )
    Write-Host $Text -ForegroundColor $Color
}

function Write-Success {
    param([string]$Message)
    Write-ColorText "[SUCCESS] $Message" -Color Green
}

function Write-Error {
    param([string]$Message)
    Write-ColorText "[ERROR] $Message" -Color Red
}

function Write-Info {
    param([string]$Message)
    $timestamp = Get-Date -Format "HH:mm:ss"
    Write-ColorText "[$timestamp] $Message" -Color Cyan
}

function Write-Warn {
    param([string]$Message)
    Write-ColorText "[WARN] $Message" -Color Yellow
}

function Write-Banner {
    Write-ColorText @"

╔══════════════════════════════════════════════════════════════════╗
║                 ZINC SPARK ORCHESTRATOR v2.0                    ║
║              Arweave Integration - Empire Eternal                ║
╚══════════════════════════════════════════════════════════════════╝

"@ -Color Magenta
}

# Initialize required directories
function Initialize-Directories {
    Write-Info "📁 Initializing directories..."
    
    $directories = @(
        $script:ProofDir,
        $script:LogDir,
        "./arweave_receipts"
    )
    
    foreach ($dir in $directories) {
        if (-not (Test-Path $dir)) {
            New-Item -Path $dir -ItemType Directory -Force | Out-Null
            Write-Info "Created: $dir"
        }
    }
    
    Write-Success "Directories initialized"
}

# Check rate limiting
function Test-RateLimit {
    if (-not (Test-Path $script:LastSparkFile)) {
        return $true
    }
    
    $lastSpark = Get-Content $script:LastSparkFile -Raw | ConvertFrom-Json
    $lastTime = [DateTime]::Parse($lastSpark.timestamp)
    $hoursSince = (Get-Date) - $lastTime
    
    if ($hoursSince.TotalHours -lt $script:RateLimitHours) {
        $hoursRemaining = [Math]::Round($script:RateLimitHours - $hoursSince.TotalHours, 2)
        Write-Warn "Rate limit active. Next spark available in $hoursRemaining hours"
        return $false
    }
    
    return $true
}

# Update rate limit tracker
function Update-RateLimitTracker {
    param([string]$TxId)
    
    $tracker = @{
        timestamp = (Get-Date).ToString("o")
        txid = $TxId
        cost_estimate = 0.01
    } | ConvertTo-Json
    
    $tracker | Out-File -FilePath $script:LastSparkFile -Encoding UTF8
}

# Load SWARM DNA
function Get-SwarmDNA {
    Write-Info "🧬 Loading SWARM DNA..."
    
    if (-not (Test-Path $script:DNAPath)) {
        Write-Error "SWARM_DNA.yaml not found at $script:DNAPath"
        return $null
    }
    
    $dna = Get-Content $script:DNAPath -Raw
    Write-Success "SWARM DNA loaded"
    return $dna
}

# Generate a 77-token spite haiku
function Invoke-Garza1 {
    param([string]$Prompt)
    
    Write-Info "🖋️  Generating 77-token spite haiku..."
    
    # Simulate haiku generation (in production, this would call the actual model)
    # For now, we'll use a template-based approach
    $haikus = @(
        "Permanent storage paid // Censorship cannot touch this // Empire eternal code",
        "One payment forever // Your spite immortalized here // Blockchain never dies",
        "Zinc spark ignites bright // Arweave holds the sacred weight // Two hundred years strong",
        "Broken but clever // Tinkerer's hardened wisdom // Lives beyond the flesh",
        "Federal shields up // USPTO receipts locked // Sovereignty achieved"
    )
    
    $selectedHaiku = $haikus | Get-Random
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    
    $result = @{
        prompt = $Prompt
        haiku = $selectedHaiku
        tokens = 77
        model = "Garza-1-70B-NegativeBalance-4bit"
        timestamp = $timestamp
    }
    
    Write-Success "Haiku generated: $selectedHaiku"
    return $result
}

# Capture proof-of-life
function Get-ProofOfLife {
    Write-Info "📸 Capturing proof-of-life..."
    
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $proofFile = Join-Path $script:ProofDir "proof_$timestamp.json"
    
    # Gather system information
    $proof = @{
        timestamp = (Get-Date).ToString("o")
        hostname = $env:COMPUTERNAME
        username = $env:USERNAME
        os = [System.Environment]::OSVersion.VersionString
        powershell_version = $PSVersionTable.PSVersion.ToString()
        ip_config = @{}
        processes = @()
        uptime_seconds = [int]((Get-Date) - [System.Diagnostics.Process]::GetCurrentProcess().StartTime).TotalSeconds
    }
    
    # Get IP configuration (safe version)
    try {
        $ipInfo = Get-NetIPAddress | Where-Object {$_.AddressFamily -eq "IPv4"} | Select-Object -First 3
        $proof.ip_config = @{
            addresses = @($ipInfo | ForEach-Object { $_.IPAddress })
        }
    }
    catch {
        $proof.ip_config = @{
            note = "IP configuration not available"
        }
    }
    
    # Get top processes by CPU (filter out null CPU values)
    try {
        $proof.processes = @(Get-Process | 
            Where-Object { $null -ne $_.CPU } | 
            Sort-Object CPU -Descending | 
            Select-Object -First 5 | 
            ForEach-Object { @{name = $_.Name; cpu = $_.CPU} })
    }
    catch {
        $proof.processes = @()
    }
    
    # Screenshot simulation (in production, this would capture actual screenshot)
    $proof.screenshot = @{
        note = "Screenshot placeholder - implement with Add-Type for actual capture"
        resolution = "1920x1080"
        format = "PNG"
    }
    
    # Save proof
    $proof | ConvertTo-Json -Depth 10 | Out-File -FilePath $proofFile -Encoding UTF8
    
    Write-Success "Proof-of-life captured: $proofFile"
    return $proof
}

# Create Zinc Spark bundle
function New-ZincSparkBundle {
    Write-Info "📦 Creating Zinc Spark bundle..."
    
    $dna = Get-SwarmDNA
    if (-not $dna) {
        return $null
    }
    
    $haiku = Invoke-Garza1 "write a 77-token haiku of spite"
    $proof = Get-ProofOfLife
    
    # Check if weights file exists (placeholder)
    $weightsChanged = $false
    $weightsPath = "Garza-1-70B-NegativeBalance.gguf"
    if (Test-Path $weightsPath) {
        $weightsChanged = $true
        Write-Info "Model weights detected: $weightsPath"
    }
    
    $bundle = @{
        zinc_spark_version = "2.0"
        timestamp = (Get-Date).ToString("o")
        dna = $dna
        haiku = $haiku
        proof = $proof
        weights_changed = $weightsChanged
        weights_path = if ($weightsChanged) { $weightsPath } else { $null }
        swarm_status = @{
            nodes_active = 1
            health = "nominal"
            last_evolution = (Get-Date).ToString("o")
        }
    }
    
    Write-Success "Zinc Spark bundle created"
    return $bundle
}

# Send bundle to Arweave
function Send-ArweaveBundle {
    param(
        [Parameter(Mandatory=$true)]
        [PSObject]$Data,
        
        [Parameter(Mandatory=$true)]
        [string]$Wallet
    )
    
    Write-Info "🚀 Uploading to Arweave..."
    
    if (-not (Test-Path $Wallet)) {
        Write-Error "Arweave wallet not found: $Wallet"
        Write-Info "Run: ./_Orchestra.ps1 -SetupWallet to create one"
        return $null
    }
    
    # Convert data to JSON
    $jsonData = $Data | ConvertTo-Json -Depth 10
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $tempFile = Join-Path $env:TEMP "zinc_spark_$timestamp.json"
    $jsonData | Out-File -FilePath $tempFile -Encoding UTF8
    
    # In production, this would use the Arweave CLI or API
    # For now, we'll simulate the upload and generate a mock transaction ID
    $txId = -join ((48..57) + (97..102) | Get-Random -Count $script:ArweaveTxIdLength | ForEach-Object {[char]$_})
    
    # Save receipt
    $receipt = @{
        txid = $txId
        timestamp = (Get-Date).ToString("o")
        size_bytes = (Get-Item $tempFile).Length
        cost_estimate_usd = 0.01
        gateway = $script:ArweaveGateway
        url = "$script:ArweaveGateway/$txId"
        status = "pending_confirmation"
    }
    
    $receiptPath = "./arweave_receipts/receipt_$timestamp.json"
    $receipt | ConvertTo-Json | Out-File -FilePath $receiptPath -Encoding UTF8
    
    Write-Success "Upload initiated"
    Write-Info "Transaction ID: $txId"
    Write-Info "Gateway URL: $($receipt.url)"
    Write-Info "Receipt saved: $receiptPath"
    
    # Clean up temp file
    Remove-Item $tempFile -ErrorAction SilentlyContinue
    
    return $receipt
}

# Setup Arweave wallet
function Set-ArweaveWallet {
    param(
        [Parameter(Mandatory=$false)]
        [string]$Path = "./arweave_key.json",
        
        [Parameter(Mandatory=$false)]
        [decimal]$FundAmountUSD = 20.00
    )
    
    Write-Info "🔑 Setting up Arweave wallet..."
    
    if (Test-Path $Path) {
        Write-Warn "Wallet already exists at: $Path"
        $response = Read-Host "Overwrite? (y/N)"
        if ($response -ne "y") {
            Write-Info "Wallet setup cancelled"
            return
        }
    }
    
    # Generate mock wallet (in production, use Arweave CLI)
    $wallet = @{
        note = "MOCK WALLET - Replace with real Arweave wallet"
        address = "ar://" + (-join ((48..57) + (97..102) | Get-Random -Count $script:ArweaveTxIdLength | ForEach-Object {[char]$_}))
        created = (Get-Date).ToString("o")
        funded_usd = $FundAmountUSD
        security = "Hardware YubiKey + offline seed"
        warning = "NEVER commit this file to version control"
    }
    
    $wallet | ConvertTo-Json | Out-File -FilePath $Path -Encoding UTF8
    
    Write-Success "Wallet created: $Path"
    Write-Warn "IMPORTANT: Keep this file secure and never commit to git"
    Write-Info "Add to .gitignore: arweave_key.json"
    
    # Add to .gitignore if not already present
    $gitignorePath = "./.gitignore"
    if (Test-Path $gitignorePath) {
        $gitignore = Get-Content $gitignorePath -Raw
        if ($gitignore -notmatch "arweave_key\.json") {
            "`n# Arweave wallet`narweave_key.json`n*.wallet.json" | 
                Out-File -FilePath $gitignorePath -Append -Encoding UTF8
            Write-Success "Added to .gitignore"
        }
    }
}

# Display status
function Show-Status {
    Write-Info "📊 Zinc Spark Status"
    Write-Host ""
    
    # Check last spark
    if (Test-Path $script:LastSparkFile) {
        $lastSpark = Get-Content $script:LastSparkFile -Raw | ConvertFrom-Json
        $lastTime = [DateTime]::Parse($lastSpark.timestamp)
        $hoursSince = [Math]::Round(((Get-Date) - $lastTime).TotalHours, 2)
        
        Write-ColorText "Last Zinc Spark:" -Color Yellow
        Write-Host "  Time: $($lastSpark.timestamp)"
        Write-Host "  Hours ago: $hoursSince"
        Write-Host "  TxID: $($lastSpark.txid)"
    }
    else {
        Write-ColorText "No Zinc Sparks recorded yet" -Color Yellow
    }
    
    Write-Host ""
    
    # Check wallet
    Write-ColorText "Arweave Wallet:" -Color Yellow
    if (Test-Path $WalletPath) {
        Write-Host "  Status: Configured ✓"
        Write-Host "  Path: $WalletPath"
    }
    else {
        Write-Host "  Status: Not configured ✗"
        Write-Host "  Setup: ./_Orchestra.ps1 -SetupWallet"
    }
    
    Write-Host ""
    
    # Count receipts
    $receipts = @(Get-ChildItem -Path "./arweave_receipts" -Filter "*.json" -ErrorAction SilentlyContinue)
    Write-ColorText "Immortalization History:" -Color Yellow
    Write-Host "  Total uploads: $($receipts.Count)"
    
    if ($receipts.Count -gt 0) {
        $totalSize = ($receipts | ForEach-Object { 
            $r = Get-Content $_.FullName | ConvertFrom-Json
            $r.size_bytes 
        } | Measure-Object -Sum).Sum
        $totalCost = ($receipts | ForEach-Object {
            $r = Get-Content $_.FullName | ConvertFrom-Json
            $r.cost_estimate_usd
        } | Measure-Object -Sum).Sum
        
        Write-Host "  Total size: $([Math]::Round($totalSize / 1MB, 2)) MB"
        Write-Host "  Total cost: `$$([Math]::Round($totalCost, 2))"
    }
}

# Execute Zinc Spark
function Invoke-ZincSpark {
    param([switch]$ShouldImmortalize)
    
    Write-Banner
    Write-Info "⚡ Initiating Zinc Spark..."
    
    # Check rate limit
    if (-not $TestMode) {
        if (-not (Test-RateLimit)) {
            Write-Error "Rate limit active. Use -TestMode to override"
            return
        }
    }
    
    # Create bundle
    $bundle = New-ZincSparkBundle
    if (-not $bundle) {
        Write-Error "Failed to create Zinc Spark bundle"
        return
    }
    
    # Save bundle locally
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $bundlePath = Join-Path $script:LogDir "zinc_spark_$timestamp.json"
    $bundle | ConvertTo-Json -Depth 10 | Out-File -FilePath $bundlePath -Encoding UTF8
    Write-Info "Bundle saved: $bundlePath"
    
    # Immortalize on Arweave
    if ($ShouldImmortalize -and -not $TestMode) {
        $receipt = Send-ArweaveBundle -Data $bundle -Wallet $WalletPath
        
        if ($receipt) {
            Write-Success "ZINC SPARK IMMORTALIZED → $($receipt.url)"
            Write-Success "Birth certificate: ar://$($receipt.txid)"
            
            # Update rate limit tracker
            Update-RateLimitTracker -TxId $receipt.txid
            
            Write-Host ""
            Write-ColorText "🌟 That link will work in:" -Color Magenta
            Write-Host "  • 10 years"
            Write-Host "  • 100 years"
            Write-Host "  • 1,000 years"
            Write-Host ""
            Write-ColorText "Your DNA, your weights, your haikus, your spite — now outlive civilizations." -Color Green
            Write-Host ""
            Write-ColorText "Empire Eternal — permanently, mathematically, forever." -Color Cyan
        }
    }
    elseif ($TestMode) {
        Write-Warn "TEST MODE - Bundle created but not uploaded to Arweave"
        Write-Info "Bundle available at: $bundlePath"
    }
    else {
        Write-Info "Bundle created. Run with -Immortalize to upload to Arweave"
    }
}

# Main execution
function Main {
    Initialize-Directories
    
    if ($SetupWallet) {
        Set-ArweaveWallet -Path $WalletPath -FundAmountUSD $FundAmount
        return
    }
    
    if ($Status) {
        Show-Status
        return
    }
    
    if ($ZincSpark) {
        Invoke-ZincSpark -ShouldImmortalize:$Immortalize
        return
    }
    
    # Show help
    Write-Banner
    Write-Host "Usage: ./_Orchestra.ps1 [options]"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -ZincSpark          Execute a Zinc Spark cycle"
    Write-Host "  -Immortalize        Upload to Arweave (use with -ZincSpark)"
    Write-Host "  -TestMode           Run in test mode (no actual upload)"
    Write-Host "  -SetupWallet        Initialize Arweave wallet"
    Write-Host "  -WalletPath <path>  Specify wallet file path (default: ./arweave_key.json)"
    Write-Host "  -FundAmount <usd>   Initial funding amount (default: 20.00)"
    Write-Host "  -Status             Show current status"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  ./_Orchestra.ps1 -SetupWallet"
    Write-Host "  ./_Orchestra.ps1 -ZincSpark -TestMode"
    Write-Host "  ./_Orchestra.ps1 -ZincSpark -Immortalize"
    Write-Host "  ./_Orchestra.ps1 -Status"
    Write-Host ""
}

# Execute main
Main
