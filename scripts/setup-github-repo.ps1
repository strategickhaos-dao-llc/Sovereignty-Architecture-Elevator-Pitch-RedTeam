# setup-github-repo.ps1 - GitHub Repository Setup Script
# Properly handles repository creation and remote configuration
#
# Usage:
#   .\scripts\setup-github-repo.ps1 -Owner "strategickhaos" -RepoName "swarmgate"
#   .\scripts\setup-github-repo.ps1 -Owner "strategickhaos" -RepoName "swarmgate" -Public
#   .\scripts\setup-github-repo.ps1 -Owner "strategickhaos" -RepoName "swarmgate" -SetRemoteOnly

param(
    [Parameter(Mandatory = $true)]
    [string]$Owner,
    
    [Parameter(Mandatory = $true)]
    [string]$RepoName,
    
    [switch]$Public,
    
    [switch]$SetRemoteOnly,
    
    [string]$Branch = "main"
)

$ErrorActionPreference = "Stop"

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

# Check if GitHub CLI is installed and authenticated
function Test-GitHubCLI {
    Log "Checking GitHub CLI installation..."
    
    if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
        Error "GitHub CLI (gh) is not installed or not in PATH."
        Error "Install it from: https://cli.github.com/"
        exit 1
    }
    
    Log "Checking GitHub CLI authentication..."
    
    try {
        $authStatus = gh auth status 2>&1
        if ($LASTEXITCODE -ne 0) {
            Warn "GitHub CLI is not authenticated."
            Log "Running 'gh auth login' to authenticate..."
            gh auth login
            
            if ($LASTEXITCODE -ne 0) {
                Error "Authentication failed."
                exit 1
            }
        }
        Success "GitHub CLI is authenticated."
    }
    catch {
        Error "Failed to check authentication: $_"
        exit 1
    }
}

# Check if repository already exists
function Test-RepoExists {
    param(
        [string]$OwnerName,
        [string]$Repository
    )
    
    Log "Checking if repository $OwnerName/$Repository exists..."
    
    try {
        $repoCheck = gh repo view "$OwnerName/$Repository" 2>&1
        if ($LASTEXITCODE -eq 0) {
            return $true
        }
        return $false
    }
    catch {
        return $false
    }
}

# Create the repository
function New-GitHubRepository {
    param(
        [string]$OwnerName,
        [string]$Repository,
        [bool]$IsPublic
    )
    
    $repoFullName = "$OwnerName/$Repository"
    Log "Creating repository: $repoFullName"
    
    # Build the visibility flag
    $visibility = if ($IsPublic) { "--public" } else { "--private" }
    
    try {
        # Note: Do NOT use < > placeholders in PowerShell commands
        # These are reserved operators and will cause parser errors
        # Use actual values or properly escaped strings
        
        $result = gh repo create $repoFullName $visibility --source=. --remote=origin --push 2>&1
        
        if ($LASTEXITCODE -ne 0) {
            # Check if the error is because repo already exists
            if ($result -match "already exists") {
                Warn "Repository already exists. Will configure remote instead."
                return $false
            }
            Error "Failed to create repository: $result"
            throw "Repository creation failed"
        }
        
        Success "Repository created: $repoFullName"
        return $true
    }
    catch {
        Error "Failed to create repository: $_"
        throw
    }
}

# Configure git remote
function Set-GitRemote {
    param(
        [string]$OwnerName,
        [string]$Repository
    )
    
    $remoteUrl = "https://github.com/$OwnerName/$Repository.git"
    Log "Configuring git remote: $remoteUrl"
    
    try {
        # Check if origin remote exists
        $existingRemote = git remote get-url origin 2>&1
        
        if ($LASTEXITCODE -eq 0) {
            Log "Remote 'origin' exists, updating URL..."
            git remote set-url origin $remoteUrl
        }
        else {
            Log "Adding remote 'origin'..."
            git remote add origin $remoteUrl
        }
        
        Success "Git remote configured: $remoteUrl"
    }
    catch {
        Error "Failed to configure remote: $_"
        throw
    }
}

# Push code to remote
function Push-ToRemote {
    param(
        [string]$BranchName
    )
    
    Log "Pushing code to remote..."
    
    try {
        # Push main branch
        git push -u origin $BranchName 2>&1
        
        if ($LASTEXITCODE -ne 0) {
            Warn "Push failed. Trying with force..."
            git push -u origin $BranchName --force 2>&1
        }
        
        Success "Code pushed to $BranchName branch"
        
        # Check for tags and push them
        $tags = git tag -l 2>&1
        if ($tags) {
            Log "Pushing tags..."
            git push origin --tags 2>&1
            Success "Tags pushed"
        }
    }
    catch {
        Error "Failed to push: $_"
        throw
    }
}

# Main execution
function Main {
    Write-ColorText "🚀 GitHub Repository Setup Tool" -Color Magenta
    Write-Host ""
    
    $repoFullName = "$Owner/$RepoName"
    Write-ColorText "Repository: $repoFullName" -Color Yellow
    Write-ColorText "Visibility: $(if ($Public) { 'Public' } else { 'Private' })" -Color Yellow
    Write-Host ""
    
    try {
        # Check GitHub CLI
        Test-GitHubCLI
        
        if ($SetRemoteOnly) {
            # Only configure remote and push
            Log "SetRemoteOnly mode: Skipping repository creation..."
            Set-GitRemote -OwnerName $Owner -Repository $RepoName
            Push-ToRemote -BranchName $Branch
        }
        else {
            # Check if repo exists
            $repoExists = Test-RepoExists -OwnerName $Owner -Repository $RepoName
            
            if ($repoExists) {
                Warn "Repository already exists."
                Log "Configuring remote and pushing..."
                Set-GitRemote -OwnerName $Owner -Repository $RepoName
                Push-ToRemote -BranchName $Branch
            }
            else {
                # Create repo (this also pushes)
                $created = New-GitHubRepository -OwnerName $Owner -Repository $RepoName -IsPublic $Public
                
                if (-not $created) {
                    # Repo exists, configure remote
                    Set-GitRemote -OwnerName $Owner -Repository $RepoName
                    Push-ToRemote -BranchName $Branch
                }
            }
        }
        
        Write-Host ""
        Success "🎉 Repository setup complete!"
        Write-Host ""
        Write-ColorText "Repository URL: https://github.com/$repoFullName" -Color Yellow
        Write-ColorText "Clone command: git clone https://github.com/$repoFullName.git" -Color Yellow
    }
    catch {
        Error "Repository setup failed: $_"
        exit 1
    }
}

# Execute main function
Main
