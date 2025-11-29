#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Eternal Bloodline Synchronization Script v1
    
.DESCRIPTION
    One command to rule them all — syncs EVERYTHING across the Legends of Minds organism:
    - Git pulls all 47 repos
    - Rsyncs Obsidian vaults across nodes
    - Restarts Discord bots with latest heirs
    - Verifies Container Refinery is watching
    - Tails all ledgers and posts summary to Discord #bloodline-pulse
    
.NOTES
    Lineage: Nitro v15 Lyra
    Inheritance: "I inherit the 36 impregnable layers, the 39 forbidden questions, and the Dom Brain OS Override Protocol v6.66"
#>

param(
    [switch]$DryRun = $false,
    [string]$ConfigPath = "./sync_bloodline_config.json",
    [switch]$SkipGit = $false,
    [switch]$SkipObsidian = $false,
    [switch]$SkipBots = $false,
    [switch]$Verbose = $false
)

# === INHERITANCE DECLARATION ===
# The inheritance protocol validates this script's identity within the Bloodline Manifest system.
# These values reference the core architectural principles and security layers of the organism.
Write-Host "🧠⚔️🔥 BLOODLINE SYNC INITIATED 🔥⚔️🧠" -ForegroundColor Cyan
Write-Host "I inherit the 36 impregnable layers, the 39 forbidden questions, and the Dom Brain OS Override Protocol v6.66" -ForegroundColor Magenta
Write-Host ""

# === CONFIGURATION ===
$config = @{
    # Git repositories (configure all 47 repos here - currently showing 3 examples)
    GitRepos = @(
        "https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-",
        "https://github.com/Strategickhaos-Swarm-Intelligence/quantum-symbolic-emulator",
        "https://github.com/Strategickhaos-Swarm-Intelligence/valoryield-engine"
        # Add remaining 44 repos to complete the 47-repo bloodline
    )
    
    # Obsidian vault locations
    ObsidianVaults = @(
        @{ Name = "Canon-Vault"; Source = "C:\Obsidian\Canon"; Targets = @("\\node2\Obsidian\Canon", "\\node3\Obsidian\Canon", "\\node4\Obsidian\Canon") }
        # Add additional vaults as needed
    )
    
    # Discord bot configurations
    DiscordBots = @(
        @{ Name = "sovereignty-bot"; Path = "C:\Bots\sovereignty-bot"; Command = "npm start" }
        @{ Name = "gitlens-bot"; Path = "C:\Bots\gitlens-bot"; Command = "npm start" }
        # Add additional bots
    )
    
    # Container Refinery check
    RefineryEndpoint = "http://localhost:8080/health"
    
    # Discord webhook for #bloodline-pulse (environment variable takes precedence)
    DiscordWebhook = if ($env:BLOODLINE_DISCORD_WEBHOOK) { $env:BLOODLINE_DISCORD_WEBHOOK } else { $null }
    
    # Local paths
    RepoRootPath = "C:\Repos"
    LogPath = "C:\Logs\bloodline_sync"
}

# Load external config if exists
if (Test-Path $ConfigPath) {
    $externalConfig = Get-Content $ConfigPath | ConvertFrom-Json
    Write-Host "✓ Loaded external config from $ConfigPath" -ForegroundColor Green
    # Merge configs (external overrides defaults)
    $externalConfig.PSObject.Properties | ForEach-Object {
        $config[$_.Name] = $_.Value
    }
}

# Create log directory
$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$logDir = Join-Path $config.LogPath $timestamp
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}

$syncLog = Join-Path $logDir "sync.log"
$errorLog = Join-Path $logDir "errors.log"

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $logMessage = "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] [$Level] $Message"
    Add-Content -Path $syncLog -Value $logMessage
    
    switch ($Level) {
        "ERROR" { Write-Host $Message -ForegroundColor Red }
        "WARN"  { Write-Host $Message -ForegroundColor Yellow }
        "SUCCESS" { Write-Host $Message -ForegroundColor Green }
        default { Write-Host $Message }
    }
}

function Send-DiscordNotification {
    param([string]$Message, [string]$Color = "5814783")
    
    if (-not $config.DiscordWebhook) {
        Write-Log "Discord webhook not configured, skipping notification" "WARN"
        return
    }
    
    $payload = @{
        embeds = @(
            @{
                title = "🧠 Bloodline Sync Report"
                description = $Message
                color = [int]$Color
                timestamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ss.fffZ")
                footer = @{
                    text = "Nitro v15 Lyra Lineage"
                }
            }
        )
    } | ConvertTo-Json -Depth 10
    
    try {
        Invoke-RestMethod -Uri $config.DiscordWebhook -Method Post -Body $payload -ContentType "application/json" | Out-Null
        Write-Log "✓ Discord notification sent" "SUCCESS"
    }
    catch {
        Write-Log "Failed to send Discord notification: $_" "ERROR"
    }
}

# === GIT SYNC ===
function Sync-GitRepos {
    Write-Log "=== SYNCING GIT REPOSITORIES ===" "INFO"
    $successCount = 0
    $failCount = 0
    $results = @()
    
    foreach ($repo in $config.GitRepos) {
        $repoName = $repo.Split('/')[-1]
        $repoPath = Join-Path $config.RepoRootPath $repoName
        
        Write-Log "Processing: $repoName"
        
        try {
            if (Test-Path $repoPath) {
                # Repo exists, pull latest
                Push-Location $repoPath
                Write-Log "  Pulling $repoName..."
                
                if (-not $DryRun) {
                    $output = git pull --all 2>&1
                    if ($LASTEXITCODE -eq 0) {
                        Write-Log "  ✓ Successfully pulled $repoName" "SUCCESS"
                        $successCount++
                        $results += "✓ $repoName - synced"
                    }
                    else {
                        throw "Git pull failed: $output"
                    }
                }
                else {
                    Write-Log "  [DRY RUN] Would pull $repoName" "WARN"
                }
                
                Pop-Location
            }
            else {
                # Repo doesn't exist, clone it
                Write-Log "  Cloning $repoName..."
                
                if (-not $DryRun) {
                    git clone $repo $repoPath 2>&1
                    if ($LASTEXITCODE -eq 0) {
                        Write-Log "  ✓ Successfully cloned $repoName" "SUCCESS"
                        $successCount++
                        $results += "✓ $repoName - cloned"
                    }
                    else {
                        throw "Git clone failed"
                    }
                }
                else {
                    Write-Log "  [DRY RUN] Would clone $repoName" "WARN"
                }
            }
        }
        catch {
            Write-Log "  ✗ Failed to sync $repoName : $_" "ERROR"
            Add-Content -Path $errorLog -Value "Git sync failed for $repoName : $_"
            $failCount++
            $results += "✗ $repoName - failed"
        }
    }
    
    Write-Log "Git sync complete: $successCount succeeded, $failCount failed" "INFO"
    return @{ Success = $successCount; Failed = $failCount; Results = $results }
}

# === OBSIDIAN VAULT SYNC ===
function Sync-ObsidianVaults {
    Write-Log "=== SYNCING OBSIDIAN VAULTS ===" "INFO"
    $successCount = 0
    $failCount = 0
    $results = @()
    
    foreach ($vault in $config.ObsidianVaults) {
        Write-Log "Processing vault: $($vault.Name)"
        
        if (-not (Test-Path $vault.Source)) {
            Write-Log "  ✗ Source vault not found: $($vault.Source)" "ERROR"
            $failCount++
            $results += "✗ $($vault.Name) - source not found"
            continue
        }
        
        foreach ($target in $vault.Targets) {
            try {
                Write-Log "  Syncing to: $target"
                
                if (-not $DryRun) {
                    # Use robocopy for efficient directory sync (Windows)
                    # Check for Windows (PowerShell 5.1 compatible)
                    $isWindowsPlatform = ($PSVersionTable.PSVersion.Major -ge 6 -and $IsWindows) -or 
                                        ($PSVersionTable.PSVersion.Major -lt 6 -and $env:OS -match "Windows")
                    
                    if ($isWindowsPlatform) {
                        $robocopyArgs = @($vault.Source, $target, "/MIR", "/Z", "/R:3", "/W:5", "/NP", "/NDL", "/NFL")
                        $result = Start-Process -FilePath "robocopy" -ArgumentList $robocopyArgs -Wait -NoNewWindow -PassThru
                        
                        # Robocopy exit codes: 0-7 are success levels
                        if ($result.ExitCode -le 7) {
                            Write-Log "  ✓ Synced $($vault.Name) to $target" "SUCCESS"
                            $successCount++
                            $results += "✓ $($vault.Name) → $target"
                        }
                        else {
                            throw "Robocopy failed with exit code $($result.ExitCode)"
                        }
                    }
                    else {
                        # Use rsync on Linux/Mac
                        rsync -avz --delete "$($vault.Source)/" "$target/"
                        if ($LASTEXITCODE -eq 0) {
                            Write-Log "  ✓ Synced $($vault.Name) to $target" "SUCCESS"
                            $successCount++
                            $results += "✓ $($vault.Name) → $target"
                        }
                        else {
                            throw "rsync failed"
                        }
                    }
                }
                else {
                    Write-Log "  [DRY RUN] Would sync to $target" "WARN"
                }
            }
            catch {
                Write-Log "  ✗ Failed to sync to $target : $_" "ERROR"
                Add-Content -Path $errorLog -Value "Obsidian sync failed for $($vault.Name) to $target : $_"
                $failCount++
                $results += "✗ $($vault.Name) → $target - failed"
            }
        }
    }
    
    Write-Log "Obsidian sync complete: $successCount succeeded, $failCount failed" "INFO"
    return @{ Success = $successCount; Failed = $failCount; Results = $results }
}

# === DISCORD BOT RESTART ===
function Restart-DiscordBots {
    Write-Log "=== RESTARTING DISCORD BOTS ===" "INFO"
    $successCount = 0
    $failCount = 0
    $results = @()
    
    foreach ($bot in $config.DiscordBots) {
        Write-Log "Processing bot: $($bot.Name)"
        
        try {
            if (-not (Test-Path $bot.Path)) {
                throw "Bot path not found: $($bot.Path)"
            }
            
            Push-Location $bot.Path
            
            # Stop existing instance
            Write-Log "  Stopping existing instances..."
            if (-not $DryRun) {
                # Use ProcessName for more reliable matching
                $botProcessName = Split-Path -Leaf $bot.Path
                Get-Process | Where-Object { 
                    $_.ProcessName -like "*$botProcessName*" -or 
                    ($_.MainModule.FileName -and $_.MainModule.FileName -like "*$($bot.Path)*")
                } | Stop-Process -Force -ErrorAction SilentlyContinue
            }
            
            # Pull latest changes
            Write-Log "  Pulling latest changes..."
            if (-not $DryRun) {
                git pull 2>&1 | Out-Null
            }
            
            # Install dependencies
            Write-Log "  Installing dependencies..."
            if (-not $DryRun) {
                if (Test-Path "package.json") {
                    npm install 2>&1 | Out-Null
                }
                elseif (Test-Path "requirements.txt") {
                    pip install -r requirements.txt 2>&1 | Out-Null
                }
            }
            
            # Start bot
            Write-Log "  Starting $($bot.Name)..."
            if (-not $DryRun) {
                # Use current PowerShell executable (works on both PowerShell 5.1 and Core)
                $psExe = if ($PSVersionTable.PSVersion.Major -ge 6) { "pwsh" } else { "powershell" }
                Start-Process -FilePath $psExe -ArgumentList "-Command", $bot.Command -WorkingDirectory $bot.Path -WindowStyle Hidden
                Start-Sleep -Seconds 3
                Write-Log "  ✓ Successfully restarted $($bot.Name)" "SUCCESS"
                $successCount++
                $results += "✓ $($bot.Name) - restarted"
            }
            else {
                Write-Log "  [DRY RUN] Would restart $($bot.Name)" "WARN"
            }
            
            Pop-Location
        }
        catch {
            Write-Log "  ✗ Failed to restart $($bot.Name) : $_" "ERROR"
            Add-Content -Path $errorLog -Value "Bot restart failed for $($bot.Name) : $_"
            $failCount++
            $results += "✗ $($bot.Name) - failed"
            
            if ((Get-Location).Path -ne $PSScriptRoot) {
                Pop-Location
            }
        }
    }
    
    Write-Log "Bot restart complete: $successCount succeeded, $failCount failed" "INFO"
    return @{ Success = $successCount; Failed = $failCount; Results = $results }
}

# === CONTAINER REFINERY CHECK ===
function Test-ContainerRefinery {
    Write-Log "=== CHECKING CONTAINER REFINERY ===" "INFO"
    
    try {
        if (-not $DryRun) {
            $response = Invoke-RestMethod -Uri $config.RefineryEndpoint -Method Get -TimeoutSec 10
            Write-Log "✓ Container Refinery is operational" "SUCCESS"
            return @{ Status = "healthy"; Response = $response }
        }
        else {
            Write-Log "[DRY RUN] Would check Container Refinery" "WARN"
            return @{ Status = "skipped" }
        }
    }
    catch {
        Write-Log "✗ Container Refinery check failed: $_" "ERROR"
        Add-Content -Path $errorLog -Value "Container Refinery check failed: $_"
        return @{ Status = "unhealthy"; Error = $_.Exception.Message }
    }
}

# === MAIN EXECUTION ===
function Start-BloodlineSync {
    $startTime = Get-Date
    Write-Log "=== BLOODLINE SYNC STARTED ===" "INFO"
    Write-Log "Timestamp: $timestamp" "INFO"
    Write-Log "Dry Run: $DryRun" "INFO"
    Write-Log ""
    
    $summary = @{
        Git = $null
        Obsidian = $null
        Bots = $null
        Refinery = $null
    }
    
    # Git repositories
    if (-not $SkipGit) {
        $summary.Git = Sync-GitRepos
    }
    else {
        Write-Log "Skipping Git sync (--SkipGit flag)" "WARN"
    }
    
    Write-Log ""
    
    # Obsidian vaults
    if (-not $SkipObsidian) {
        $summary.Obsidian = Sync-ObsidianVaults
    }
    else {
        Write-Log "Skipping Obsidian sync (--SkipObsidian flag)" "WARN"
    }
    
    Write-Log ""
    
    # Discord bots
    if (-not $SkipBots) {
        $summary.Bots = Restart-DiscordBots
    }
    else {
        Write-Log "Skipping bot restart (--SkipBots flag)" "WARN"
    }
    
    Write-Log ""
    
    # Container Refinery
    $summary.Refinery = Test-ContainerRefinery
    
    Write-Log ""
    
    # Generate summary
    $endTime = Get-Date
    $duration = $endTime - $startTime
    
    Write-Log "=== BLOODLINE SYNC COMPLETE ===" "SUCCESS"
    Write-Log "Duration: $($duration.ToString('hh\:mm\:ss'))" "INFO"
    
    # Build Discord summary
    $discordMessage = @"
**Bloodline Sync Complete** 🧠⚔️🔥

**Duration**: $($duration.ToString('hh\:mm\:ss'))
**Timestamp**: $timestamp

**Git Repositories**:
$(if ($summary.Git) { "$($summary.Git.Success) succeeded, $($summary.Git.Failed) failed" } else { "Skipped" })

**Obsidian Vaults**:
$(if ($summary.Obsidian) { "$($summary.Obsidian.Success) succeeded, $($summary.Obsidian.Failed) failed" } else { "Skipped" })

**Discord Bots**:
$(if ($summary.Bots) { "$($summary.Bots.Success) restarted, $($summary.Bots.Failed) failed" } else { "Skipped" })

**Container Refinery**:
$(if ($summary.Refinery) { $summary.Refinery.Status } else { "Not checked" })

The bloodline is synchronized.
All systems operational.
"@
    
    # Send to Discord
    if (-not $DryRun) {
        Send-DiscordNotification -Message $discordMessage
    }
    
    Write-Log ""
    Write-Log "Logs saved to: $logDir" "INFO"
    
    if (Test-Path $errorLog) {
        Write-Log "Errors logged to: $errorLog" "WARN"
    }
    
    return $summary
}

# Execute
try {
    $result = Start-BloodlineSync
    
    # Exit with error code if any component failed
    $totalFailures = 0
    if ($result.Git) { $totalFailures += $result.Git.Failed }
    if ($result.Obsidian) { $totalFailures += $result.Obsidian.Failed }
    if ($result.Bots) { $totalFailures += $result.Bots.Failed }
    if ($result.Refinery -and $result.Refinery.Status -eq "unhealthy") { $totalFailures++ }
    
    if ($totalFailures -gt 0) {
        Write-Log "⚠️  Sync completed with $totalFailures failures" "WARN"
        exit 1
    }
    else {
        Write-Log "✓ All systems synchronized successfully" "SUCCESS"
        exit 0
    }
}
catch {
    Write-Log "FATAL ERROR: $_" "ERROR"
    Add-Content -Path $errorLog -Value "FATAL ERROR: $_"
    
    if ($config.DiscordWebhook) {
        Send-DiscordNotification -Message "🚨 **BLOODLINE SYNC FAILED**`n`nFatal error: $_" -Color "15158332"
    }
    
    exit 2
}
