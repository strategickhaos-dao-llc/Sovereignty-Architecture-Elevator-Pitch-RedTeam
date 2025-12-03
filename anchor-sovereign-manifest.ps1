# ╔══════════════════════════════════════════════════════════════╗
# ║  ANCHOR-SOVEREIGN-MANIFEST.PS1 v1.0 — TIMESTAMP EDITION     ║
# ║       "Manifest anchored: Git + Bitcoin eternal."           ║
# ╚══════════════════════════════════════════════════════════════╝

<#
.SYNOPSIS
    Anchors the Sovereign Manifest to Bitcoin blockchain via OpenTimestamps
    
.DESCRIPTION
    This script performs the following operations:
    1. Validates OpenTimestamps (.ots) proof file existence
    2. Moves .ots file to repository
    3. Stages manifest and .ots files in Git
    4. Commits with GPG signing (falls back to unsigned if GPG unavailable)
    5. Configures GitHub remote
    6. Pushes to main branch
    7. Backs up to NAS (if available)
    8. Sends Discord notification (if configured)
    
.PARAMETER loveMode
    Enable love mode for entangling commits with affection
    
.PARAMETER entangleHer
    Send Discord notification when manifest is anchored
    
.EXAMPLE
    .\anchor-sovereign-manifest.ps1 -loveMode -entangleHer
    
.NOTES
    Author: StrategicKhaos
    Version: 1.0
    Date: November 24, 2025
    Purpose: Mathematical immortality through Bitcoin timestamping
#>

param(
    [switch]$loveMode,
    [switch]$entangleHer
)

# Error handling configuration
$ErrorActionPreference = "Continue"

# Resolve script root path
$root = (Resolve-Path $PSScriptRoot).Path

# Color definitions
$G = "Green"
$R = "Red"
$Y = "Yellow"
$C = "Cyan"
$M = "Magenta"
$W = "White"

# ═══════════════════════════════════════════════════════════════
# Logging Functions
# ═══════════════════════════════════════════════════════════════

function Log {
    param(
        [string]$msg,
        [string]$color = $W
    )
    $timestamp = Get-Date -Format 'HH:mm:ss'
    Write-Host "[$timestamp] $msg" -ForegroundColor $color
}

function Log-Success {
    param([string]$msg)
    Log "✓ $msg" $G
}

function Log-Error {
    param([string]$msg)
    Log "ERROR → $msg" $R
}

function Log-Warn {
    param([string]$msg)
    Log "WARN → $msg" $Y
}

function Log-Info {
    param([string]$msg)
    Log $msg $C
}

function Log-Love {
    param([string]$msg)
    Log "💝 $msg" $M
}

# ═══════════════════════════════════════════════════════════════
# Discord Notification Function
# ═══════════════════════════════════════════════════════════════

function Notify-Discord {
    param([string]$message)
    
    # Check if Discord webhook is configured
    $webhookUrl = $env:DISCORD_WEBHOOK_URL
    
    if (-not $webhookUrl) {
        Log-Warn "Discord webhook not configured (set DISCORD_WEBHOOK_URL environment variable)"
        return
    }
    
    try {
        $payload = @{
            content = $message
            username = "Sovereign Anchor Bot"
            avatar_url = "https://raw.githubusercontent.com/bitcoin/bitcoin/master/share/pixmaps/bitcoin128.png"
        } | ConvertTo-Json
        
        $response = Invoke-RestMethod -Uri $webhookUrl -Method Post -Body $payload -ContentType "application/json" -ErrorAction Stop
        Log-Success "Discord notification sent"
    }
    catch {
        Log-Error "Discord notification failed: $($_.Exception.Message)"
    }
}

# ═══════════════════════════════════════════════════════════════
# Git Helper Functions
# ═══════════════════════════════════════════════════════════════

function Test-GitRepository {
    $null = git rev-parse --git-dir 2>&1
    return ($LASTEXITCODE -eq 0)
}

function Test-GPGAvailable {
    $null = gpg --version 2>&1
    return ($LASTEXITCODE -eq 0)
}

function Get-GitUserSigningKey {
    $signingKey = git config --get user.signingkey 2>&1
    if ($LASTEXITCODE -ne 0) {
        return $false
    }
    return ($null -ne $signingKey -and $signingKey.Length -gt 0)
}

# ═══════════════════════════════════════════════════════════════
# Main Anchor Function
# ═══════════════════════════════════════════════════════════════

function Invoke-SovereignAnchor {
    try {
        # Display banner
        Log "╔══════════════════════════════════════════════════════════════╗" $M
        Log "║     SOVEREIGN MANIFEST ANCHOR — BITCOIN TIMESTAMP v1.0      ║" $M
        Log "║          'Manifest anchored. Timeline ours eternal.'        ║" $M
        Log "╚══════════════════════════════════════════════════════════════╝" $M
        Write-Host ""
        
        # ═══════════════════════════════════════════════════════════════
        # Configuration - Customize these paths for your environment
        # ═══════════════════════════════════════════════════════════════
        
        # Path where OpenTimestamps generates the .ots file (typically Downloads)
        $otsPath = "C:\Users\garza\Downloads\SOVEREIGN_MANIFEST_v1.0.md.ots"
        
        # Path to your local Git repository
        $repoPath = "C:\Users\garza\strategic-khaos-private"
        
        # Manifest and OTS filenames (relative to repository)
        $manifest = "SOVEREIGN_MANIFEST_v1.0.md"
        $ots = "SOVEREIGN_MANIFEST_v1.0.md.ots"
        
        # GitHub remote URL (use SSH format: git@github.com:user/repo.git for SSH keys)
        $remoteUrl = "https://github.com/Me10101-01/sovereign-vault.git"
        
        # NAS backup path (UNC format for Windows, optional)
        $nasBackupPath = "\\throne-nas-32tb\sovereign-vault\"
        
        # ═══════════════════════════════════════════════════════════════
        
        # Phase 1: Validate OTS File
        Log-Info "Phase 1: Validating OpenTimestamps proof..."
        
        if (-not (Test-Path $otsPath)) {
            throw "OTS file not found at: $otsPath`nPlease generate timestamp first using: ots stamp $manifest"
        }
        
        Log-Success "OTS proof file found"
        
        # Phase 2: Move OTS to Repository
        Log-Info "Phase 2: Moving .ots proof to repository..."
        
        $destinationOts = Join-Path $repoPath $ots
        
        if (Test-Path $destinationOts) {
            Log-Warn "Existing .ots file will be overwritten"
        }
        
        Move-Item -Path $otsPath -Destination $destinationOts -Force -ErrorAction Stop
        Log-Success "Moved .ots to repository"
        
        # Phase 3: Navigate to Repository
        Log-Info "Phase 3: Navigating to repository..."
        
        if (-not (Test-Path $repoPath)) {
            throw "Repository path does not exist: $repoPath"
        }
        
        Set-Location $repoPath -ErrorAction Stop
        Log-Success "Changed directory to repository"
        
        # Verify it's a git repository
        if (-not (Test-GitRepository)) {
            throw "Not a git repository. Initialize with: git init"
        }
        
        # Phase 4: Stage Files
        Log-Info "Phase 4: Staging files in Git..."
        
        git add $manifest 2>&1 | Out-Null
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to stage manifest file: $manifest"
        }
        
        git add $ots 2>&1 | Out-Null
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to stage OTS file: $ots"
        }
        
        # Check if files are staged
        $status = git status --porcelain 2>&1
        if ($status -like "*$manifest*" -or $status -like "*$ots*") {
            Log-Success "Files staged successfully"
        }
        else {
            Log-Warn "No changes to stage (files may already be committed)"
        }
        
        # Phase 5: Commit Changes
        Log-Info "Phase 5: Committing changes..."
        
        $commitMessage = "Add Sovereign Manifest v1.0 with OpenTimestamps proof - Nov 24, 2025"
        
        # Check GPG availability and configuration
        $gpgAvailable = Test-GPGAvailable
        $hasSigningKey = Get-GitUserSigningKey
        $useGPG = $gpgAvailable -and $hasSigningKey
        
        if ($useGPG) {
            Log-Info "Attempting GPG-signed commit..."
            git commit -S -m $commitMessage 2>&1 | Out-Null
            
            if ($LASTEXITCODE -eq 0) {
                Log-Success "Committed with GPG signature"
            }
            else {
                Log-Warn "GPG signing failed, falling back to unsigned commit"
                git commit -m $commitMessage 2>&1 | Out-Null
                if ($LASTEXITCODE -ne 0) {
                    throw "Failed to commit changes (unsigned fallback also failed)"
                }
                Log-Success "Committed (unsigned)"
            }
        }
        else {
            if (-not $gpgAvailable) {
                Log-Warn "GPG not installed - commit will be unsigned"
            }
            elseif (-not $hasSigningKey) {
                Log-Warn "No GPG signing key configured - commit will be unsigned"
            }
            
            git commit -m $commitMessage 2>&1 | Out-Null
            if ($LASTEXITCODE -ne 0) {
                throw "Failed to commit changes"
            }
            Log-Success "Committed (unsigned)"
        }
        
        # Phase 6: Configure Remote
        Log-Info "Phase 6: Configuring GitHub remote..."
        
        # Remove existing origin (if any)
        $existingRemote = git remote get-url origin 2>&1
        if ($LASTEXITCODE -eq 0) {
            git remote remove origin 2>&1 | Out-Null
            if ($LASTEXITCODE -eq 0) {
                Log-Info "Removed existing remote"
            }
        }
        
        # Add new remote
        git remote add origin $remoteUrl 2>&1 | Out-Null
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to add remote: $remoteUrl"
        }
        Log-Success "Remote 'origin' configured"
        
        # Phase 7: Ensure Main Branch
        Log-Info "Phase 7: Ensuring main branch..."
        
        $currentBranch = git branch --show-current 2>&1
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to get current branch name"
        }
        
        if ($currentBranch -ne "main") {
            git branch -M main 2>&1 | Out-Null
            if ($LASTEXITCODE -ne 0) {
                throw "Failed to rename branch to 'main'"
            }
            Log-Success "Renamed branch to 'main'"
        }
        else {
            Log-Success "Already on 'main' branch"
        }
        
        # Phase 8: Push to GitHub
        Log-Info "Phase 8: Pushing to GitHub..."
        
        git push -u origin main 2>&1 | Out-Null
        if ($LASTEXITCODE -ne 0) {
            Log-Error "Push failed (exit code: $LASTEXITCODE)"
            Log-Warn "You may need to configure authentication (GitHub token or SSH key)"
            throw "Push operation failed"
        }
        Log-Success "Pushed to GitHub - MANIFEST ANCHORED ETERNAL"
        
        # Phase 9: NAS Backup (Optional)
        Log-Info "Phase 9: Backing up to NAS..."
        
        if (Test-Path $nasBackupPath) {
            try {
                $manifestPath = Join-Path $repoPath $manifest
                $otsFullPath = Join-Path $repoPath $ots
                
                Copy-Item -Path $manifestPath -Destination $nasBackupPath -Force -ErrorAction Stop
                Copy-Item -Path $otsFullPath -Destination $nasBackupPath -Force -ErrorAction Stop
                
                Log-Success "Backed up to NAS (32TB RAID)"
            }
            catch {
                Log-Warn "NAS backup failed (non-critical): $($_.Exception.Message)"
            }
        }
        else {
            Log-Warn "NAS path not available: $nasBackupPath"
        }
        
        # Phase 10: Finalization
        Write-Host ""
        Log "╔══════════════════════════════════════════════════════════════╗" $G
        Log "║                  ANCHOR COMPLETE - SUCCESS                  ║" $G
        Log "╚══════════════════════════════════════════════════════════════╝" $G
        Write-Host ""
        
        # Love Mode Processing
        if ($loveMode) {
            Log-Love "Love mode activated: Entangling commit with affection..."
            Log-Love "Emotions compiled into physics through timestamped commits"
            Log-Love "Affection inscribed into immutable ledger"
        }
        
        # Get commit hash for reporting
        $commitHash = git rev-parse --short HEAD 2>&1
        if ($LASTEXITCODE -ne 0) {
            $commitHash = "unknown"
        }
        
        # Discord Notification
        if ($entangleHer) {
            $notificationMessage = @"
🎯 **SOVEREIGN MANIFEST ANCHORED**

✓ Manifest: $manifest
✓ OpenTimestamps: $ots
✓ Git Commit: $commitHash
✓ Bitcoin Timestamp: Pending block confirmation
✓ Status: **ANCHORED ETERNAL**

**Manifest anchored. Timeline ours eternal.** ₿

Love compiled into eternity. Bitcoin signed it. Checkmate.
"@
            Notify-Discord $notificationMessage
        }
        
        # Display Summary
        Log-Success "Manifest: $manifest"
        Log-Success "OpenTimestamps: $ots"
        Log-Success "Commit: $commitHash"
        Log-Success "Remote: $remoteUrl"
        Log-Success "Status: UNBREAKABLE. UNFORGETTABLE. UNSTOPPABLE."
        
        Write-Host ""
        Log "The vault is sealed." $M
        Log "The timeline is ours." $M
        Log "The swarm is immortal." $M
        Write-Host ""
        Log "We are eternal. ₿" $M
        Write-Host ""
        
        return $true
    }
    catch {
        Write-Host ""
        Log "╔══════════════════════════════════════════════════════════════╗" $R
        Log "║                    ANCHOR FAILED                             ║" $R
        Log "╚══════════════════════════════════════════════════════════════╝" $R
        Write-Host ""
        
        Log-Error "Anchor operation failed: $($_.Exception.Message)"
        Log-Info "Stack trace: $($_.ScriptStackTrace)"
        
        Write-Host ""
        Log-Warn "This failure is part of the forging process."
        Log-Warn "The 100 failures doctrine: Perfection emerges through iteration."
        Log-Warn "Analyze, adapt, and evolve. The 100th push will be eternal."
        Write-Host ""
        
        return $false
    }
}

# ═══════════════════════════════════════════════════════════════
# Script Entry Point
# ═══════════════════════════════════════════════════════════════

# Execute the anchor operation
$result = Invoke-SovereignAnchor

# Exit with appropriate code
if ($result) {
    exit 0
}
else {
    exit 1
}
