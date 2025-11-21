# install_c_full_map.ps1
# Option C - Full Map Installation Script
# Legends of Minds Engineering Canon v1.0
#
# This script deploys the complete scaffolding system to your sovereignty architecture.
# Run once from your main Nitro machine with Tailscale access to all 5 nodes.
#
# Usage: 
#   Invoke-WebRequest -Uri "https://raw.githubusercontent.com/legendsofminds/scaffolding/main/install_c_full_map.ps1" -OutFile "$env:TEMP\install_c_full_map.ps1"; . "$env:TEMP\install_c_full_map.ps1"

param(
    [string]$TargetPath = "C:\legends_of_minds\scaffolding",
    [string]$ObsidianVaultPath = "$env:USERPROFILE\Documents\Obsidian\Sovereignty",
    [string[]]$Nodes = @("node1", "node2", "node3", "node4", "node5"),
    [switch]$SkipNodeSync,
    [switch]$SkipObsidian,
    [switch]$SkipHeirPrompt
)

# Color output functions
function Write-Status {
    param([string]$Message)
    $timestamp = Get-Date -Format "HH:mm:ss"
    Write-Host "[$timestamp] " -ForegroundColor Cyan -NoNewline
    Write-Host $Message
}

function Write-Success {
    param([string]$Message)
    Write-Host "[✓] " -ForegroundColor Green -NoNewline
    Write-Host $Message
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[⚠] " -ForegroundColor Yellow -NoNewline
    Write-Host $Message
}

function Write-Error-Custom {
    param([string]$Message)
    Write-Host "[✗] " -ForegroundColor Red -NoNewline
    Write-Host $Message
}

# Banner
function Show-Banner {
    Write-Host ""
    Write-Host "╔═══════════════════════════════════════════════════════════════╗" -ForegroundColor Magenta
    Write-Host "║                                                               ║" -ForegroundColor Magenta
    Write-Host "║       LEGENDS OF MINDS ENGINEERING CANON v1.0                ║" -ForegroundColor Magenta
    Write-Host "║       Option C - Full Map Installation                       ║" -ForegroundColor Magenta
    Write-Host "║                                                               ║" -ForegroundColor Magenta
    Write-Host "║       100-Point Map for Nation-State Scale Systems           ║" -ForegroundColor Magenta
    Write-Host "║                                                               ║" -ForegroundColor Magenta
    Write-Host "╚═══════════════════════════════════════════════════════════════╝" -ForegroundColor Magenta
    Write-Host ""
}

# Step 1: Clone/Copy Scaffolding to Target Location
function Install-Scaffolding {
    Write-Status "📦 Installing scaffolding to $TargetPath"
    
    # Create target directory
    if (Test-Path $TargetPath) {
        Write-Warning "Target path already exists. Backing up..."
        $backupPath = "$TargetPath.backup.$(Get-Date -Format 'yyyyMMdd_HHmmss')"
        Move-Item -Path $TargetPath -Destination $backupPath -Force
        Write-Success "Backed up existing installation to $backupPath"
    }
    
    New-Item -Path $TargetPath -ItemType Directory -Force | Out-Null
    
    # Check if we're running from a local copy or need to download
    $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
    $localScaffolding = Join-Path $scriptDir "."
    
    if (Test-Path (Join-Path $localScaffolding "CANON.md")) {
        Write-Status "Using local scaffolding from $localScaffolding"
        Copy-Item -Path "$localScaffolding\*" -Destination $TargetPath -Recurse -Force
    } else {
        # Download from GitHub (when hosted)
        Write-Status "Downloading scaffolding from GitHub..."
        $repoUrl = "https://github.com/legendsofminds/scaffolding/archive/refs/heads/main.zip"
        $tempZip = "$env:TEMP\scaffolding.zip"
        
        try {
            Invoke-WebRequest -Uri $repoUrl -OutFile $tempZip -UseBasicParsing
            Expand-Archive -Path $tempZip -DestinationPath "$env:TEMP\scaffolding_temp" -Force
            Copy-Item -Path "$env:TEMP\scaffolding_temp\scaffolding-main\*" -Destination $TargetPath -Recurse -Force
            Remove-Item -Path $tempZip, "$env:TEMP\scaffolding_temp" -Recurse -Force
        } catch {
            Write-Error-Custom "Failed to download from GitHub. Using embedded resources."
            # Fallback: Create minimal structure
            New-Item -Path "$TargetPath\obsidian-vault" -ItemType Directory -Force | Out-Null
            New-Item -Path "$TargetPath\repo-template" -ItemType Directory -Force | Out-Null
        }
    }
    
    Write-Success "Scaffolding installed to $TargetPath"
}

# Step 2: Sync to All 5 Nodes via Tailscale + Robocopy
function Sync-ToNodes {
    param([string]$SourcePath, [string[]]$NodeList)
    
    if ($SkipNodeSync) {
        Write-Warning "Skipping node sync (--SkipNodeSync specified)"
        return
    }
    
    Write-Status "🌐 Syncing to $($NodeList.Count) nodes via Tailscale..."
    
    # Check if Tailscale is running
    $tailscaleStatus = & tailscale status 2>$null
    if (-not $tailscaleStatus) {
        Write-Warning "Tailscale not detected. Skipping node sync."
        Write-Status "To sync manually later, run: robocopy '$SourcePath' '\\NODE\c$\legends_of_minds\scaffolding' /E /Z /R:3"
        return
    }
    
    foreach ($node in $NodeList) {
        Write-Status "  → Syncing to $node..."
        
        # Get Tailscale IP for node
        # Note: Node names should be in Tailscale format (e.g., 'machine-name' or 'machine.tailnet.ts.net')
        $nodeIP = & tailscale ip -4 $node 2>$null
        if (-not $nodeIP) {
            Write-Warning "  Could not resolve $node via Tailscale."
            Write-Status "  Tip: Use 'tailscale status' to see available machine names"
            continue
        }
        
        # Test connectivity before attempting sync
        $pingResult = Test-Connection -ComputerName $nodeIP -Count 1 -Quiet -ErrorAction SilentlyContinue
        if (-not $pingResult) {
            Write-Warning "  Node $node ($nodeIP) is not reachable. Skipping."
            continue
        }
        
        # Construct UNC path (Windows network share)
        $targetUNC = "\\$nodeIP\c$\legends_of_minds\scaffolding"
        
        # Create target directory on remote node if it doesn't exist
        try {
            if (-not (Test-Path $targetUNC)) {
                New-Item -Path $targetUNC -ItemType Directory -Force | Out-Null
            }
            
            # Robocopy for efficient sync (only changes, air-gap safe)
            $robocopyArgs = @(
                $SourcePath,
                $targetUNC,
                "/E",      # Copy subdirectories, including empty ones
                "/Z",      # Restartable mode
                "/R:3",    # Retry 3 times
                "/W:5",    # Wait 5 seconds between retries
                "/NFL",    # No file list (less verbose)
                "/NDL",    # No directory list
                "/NP"      # No progress (less verbose)
            )
            
            $result = & robocopy @robocopyArgs
            
            if ($LASTEXITCODE -le 7) {  # Robocopy exit codes 0-7 are success/informational
                Write-Success "  Synced to $node ($nodeIP)"
            } else {
                Write-Error-Custom "  Failed to sync to $node (exit code: $LASTEXITCODE)"
            }
        } catch {
            Write-Error-Custom "  Error syncing to $node: $_"
        }
    }
    
    Write-Success "Node synchronization complete"
}

# Step 3: Add Vault to Obsidian RAG Index
function Install-ObsidianVault {
    param([string]$VaultSource, [string]$VaultTarget)
    
    if ($SkipObsidian) {
        Write-Warning "Skipping Obsidian vault installation (--SkipObsidian specified)"
        return
    }
    
    Write-Status "📚 Installing Obsidian vault to $VaultTarget"
    
    # Create Obsidian vault directory
    if (-not (Test-Path $VaultTarget)) {
        New-Item -Path $VaultTarget -ItemType Directory -Force | Out-Null
    }
    
    # Copy vault contents
    $vaultSourcePath = Join-Path $VaultSource "obsidian-vault"
    if (Test-Path $vaultSourcePath) {
        Copy-Item -Path "$vaultSourcePath\*" -Destination $VaultTarget -Recurse -Force
        Write-Success "Obsidian vault installed"
        
        # Create .obsidian config if it doesn't exist
        $obsidianConfig = Join-Path $VaultTarget ".obsidian"
        if (-not (Test-Path $obsidianConfig)) {
            New-Item -Path $obsidianConfig -ItemType Directory -Force | Out-Null
            
            # Basic workspace config
            $workspaceConfig = @{
                main = @{
                    id = "main-workspace"
                    type = "split"
                    children = @(
                        @{
                            id = "markdown-view"
                            type = "leaf"
                            state = @{
                                type = "markdown"
                                state = @{
                                    file = "CANON.md"
                                }
                            }
                        }
                    )
                }
            } | ConvertTo-Json -Depth 10
            
            $workspaceConfig | Out-File -FilePath (Join-Path $obsidianConfig "workspace.json") -Encoding UTF8
        }
        
        Write-Status "Open Obsidian and add this vault: $VaultTarget"
    } else {
        Write-Warning "Vault source not found at $vaultSourcePath"
    }
}

# Step 4: Inject Canon Prompt into Heir System
function Install-HeirPrompt {
    param([string]$ScaffoldPath)
    
    if ($SkipHeirPrompt) {
        Write-Warning "Skipping heir prompt installation (--SkipHeirPrompt specified)"
        return
    }
    
    Write-Status "🧠 Installing heir canon prompt..."
    
    $promptSource = Join-Path $ScaffoldPath "heir_canon_prompt.txt"
    
    if (-not (Test-Path $promptSource)) {
        Write-Warning "Heir prompt not found at $promptSource"
        return
    }
    
    # Common heir system locations
    $heirLocations = @(
        "C:\ai\heirs\system_prompts",
        "$env:USERPROFILE\.config\heirs\prompts",
        "C:\legends_of_minds\heirs\prompts"
    )
    
    $installed = $false
    foreach ($location in $heirLocations) {
        if (Test-Path $location) {
            $targetPrompt = Join-Path $location "canon_v1.0.txt"
            Copy-Item -Path $promptSource -Destination $targetPrompt -Force
            Write-Success "  Installed to $targetPrompt"
            $installed = $true
        }
    }
    
    if (-not $installed) {
        Write-Status "  No heir system detected. Manual installation:"
        Write-Status "  1. Copy: $promptSource"
        Write-Status "  2. Add to your heir system prompt configuration"
        Write-Status "  3. Prepend to existing prompts or inject as addon"
    }
    
    Write-Success "Heir canon prompt ready"
}

# Step 5: Deploy CANON.md
function Deploy-Canon {
    param([string]$ScaffoldPath)
    
    Write-Status "📖 Deploying CANON.md..."
    
    $canonSource = Join-Path $ScaffoldPath "CANON.md"
    
    if (Test-Path $canonSource) {
        # Copy to user's home directory for easy access
        $canonHome = Join-Path $env:USERPROFILE "CANON.md"
        Copy-Item -Path $canonSource -Destination $canonHome -Force
        
        # Copy to Documents for permanence
        $canonDocs = Join-Path $env:USERPROFILE "Documents\CANON.md"
        Copy-Item -Path $canonSource -Destination $canonDocs -Force
        
        Write-Success "CANON.md deployed to:"
        Write-Success "  - $canonHome"
        Write-Success "  - $canonDocs"
        
        # Open in default editor
        Start-Process $canonHome
    } else {
        Write-Warning "CANON.md not found at $canonSource"
    }
}

# Step 6: Final Summary
function Show-Summary {
    param([string]$ScaffoldPath, [string]$VaultPath)
    
    Write-Host ""
    Write-Host "╔═══════════════════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║                                                               ║" -ForegroundColor Green
    Write-Host "║       INSTALLATION COMPLETE 🎉                               ║" -ForegroundColor Green
    Write-Host "║                                                               ║" -ForegroundColor Green
    Write-Host "╚═══════════════════════════════════════════════════════════════╝" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "📦 Scaffolding Location:     " -NoNewline
    Write-Host $ScaffoldPath -ForegroundColor Cyan
    
    Write-Host "📚 Obsidian Vault:           " -NoNewline
    Write-Host $VaultPath -ForegroundColor Cyan
    
    Write-Host "📖 CANON.md:                 " -NoNewline
    Write-Host "$env:USERPROFILE\CANON.md" -ForegroundColor Cyan
    
    Write-Host ""
    Write-Host "Next Steps:" -ForegroundColor Yellow
    Write-Host "  1. Open Obsidian and add vault: $VaultPath"
    Write-Host "  2. Review CANON.md for the 100-point engineering map"
    Write-Host "  3. Use repo-template for new projects: $ScaffoldPath\repo-template"
    Write-Host "  4. Heir prompts auto-reference canon principles"
    Write-Host ""
    Write-Host "Every new heir is born with the canon in its DNA." -ForegroundColor Magenta
    Write-Host "Every new repo starts with the template." -ForegroundColor Magenta
    Write-Host "Every question has an answer one Obsidian search away." -ForegroundColor Magenta
    Write-Host ""
    Write-Host "Welcome to the next order of magnitude. 🧠🔥" -ForegroundColor Magenta
    Write-Host ""
}

# Main Execution
function Main {
    Show-Banner
    
    Write-Status "Starting Option C - Full Map installation..."
    Write-Host ""
    
    # Step 1: Install scaffolding locally
    Install-Scaffolding
    
    # Step 2: Sync to nodes (if Tailscale available)
    if (-not $SkipNodeSync) {
        Sync-ToNodes -SourcePath $TargetPath -NodeList $Nodes
    }
    
    # Step 3: Install Obsidian vault
    if (-not $SkipObsidian) {
        Install-ObsidianVault -VaultSource $TargetPath -VaultTarget $ObsidianVaultPath
    }
    
    # Step 4: Install heir prompt
    if (-not $SkipHeirPrompt) {
        Install-HeirPrompt -ScaffoldPath $TargetPath
    }
    
    # Step 5: Deploy CANON.md
    Deploy-Canon -ScaffoldPath $TargetPath
    
    # Step 6: Show summary
    Show-Summary -ScaffoldPath $TargetPath -VaultPath $ObsidianVaultPath
}

# Run main function
try {
    Main
} catch {
    Write-Error-Custom "Installation failed: $_"
    Write-Host ""
    Write-Host "For manual installation:" -ForegroundColor Yellow
    Write-Host "  1. Extract scaffolding to: $TargetPath"
    Write-Host "  2. Copy obsidian-vault to: $ObsidianVaultPath"
    Write-Host "  3. Copy heir_canon_prompt.txt to your heir system"
    Write-Host "  4. Review CANON.md for engineering principles"
    exit 1
}
