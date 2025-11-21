#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Sovereignty Repository Verification - Full Refinery-Style Check
    
.DESCRIPTION
    Scans all repositories in a specified directory for:
    - LICENSE file presence and validity
    - artifacts/ folder or external_discussions.md
    - Git commit history for license additions
    - Generates comprehensive audit report
    
.PARAMETER RepoRoot
    Root directory containing repositories to scan (default: C:\repos\ or ~/repos/)
    
.PARAMETER AutoFix
    Automatically add missing LICENSE files (MIT default, with confirmation)
    
.PARAMETER GenerateReport
    Generate detailed report in JSON/Markdown format
    
.EXAMPLE
    ./verify-repo-sovereignty.ps1 -RepoRoot "C:\repos\" -GenerateReport
    
.EXAMPLE
    ./verify-repo-sovereignty.ps1 -AutoFix -RepoRoot "~/projects/"
#>

param(
    [Parameter(Mandatory=$false)]
    [string]$RepoRoot = $(if ($IsWindows) { "C:\repos\" } else { "$HOME/repos/" }),
    
    [Parameter(Mandatory=$false)]
    [switch]$AutoFix = $false,
    
    [Parameter(Mandatory=$false)]
    [switch]$GenerateReport = $false,
    
    [Parameter(Mandatory=$false)]
    [string]$OutputPath = "./sovereignty_verification_report.json"
)

# Color output functions
function Write-Success { param($msg) Write-Host "✓ $msg" -ForegroundColor Green }
function Write-Warning { param($msg) Write-Host "⚠ $msg" -ForegroundColor Yellow }
function Write-Error { param($msg) Write-Host "✗ $msg" -ForegroundColor Red }
function Write-Info { param($msg) Write-Host "ℹ $msg" -ForegroundColor Cyan }

# Check if repo root exists
if (-not (Test-Path $RepoRoot)) {
    Write-Error "Repository root directory not found: $RepoRoot"
    Write-Info "Please specify a valid directory with -RepoRoot parameter"
    exit 1
}

Write-Info "Scanning repositories in: $RepoRoot"
Write-Info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Find all directories that contain .git folders
$repos = Get-ChildItem -Path $RepoRoot -Directory -Recurse -Depth 3 | 
    Where-Object { Test-Path (Join-Path $_.FullName ".git") }

if ($repos.Count -eq 0) {
    Write-Warning "No git repositories found in $RepoRoot"
    exit 0
}

Write-Info "Found $($repos.Count) repositories to scan"
Write-Host ""

# Verification results
$results = @()
$stats = @{
    Total = $repos.Count
    Licensed = 0
    HasArtifacts = 0
    FullySovereign = 0
    NeedsAttention = 0
}

# MIT License template
$mitTemplate = @"
MIT License

Copyright (c) $(Get-Date -Format yyyy) [Your Name / Sovereign Heir]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"@

# Scan each repository
foreach ($repo in $repos) {
    $repoName = $repo.Name
    $repoPath = $repo.FullName
    $licensePath = Join-Path $repoPath "LICENSE"
    $artifactsPath = Join-Path $repoPath "artifacts"
    $extDiscussionsPath = Join-Path $repoPath "external_discussions.md"
    
    Write-Host "Scanning: $repoName" -ForegroundColor White
    
    $repoResult = @{
        Name = $repoName
        Path = $repoPath
        HasLicense = $false
        LicenseType = $null
        LicenseCommitDate = $null
        HasArtifacts = $false
        ArtifactLocation = $null
        Status = "unknown"
        Issues = @()
    }
    
    # Check for LICENSE file
    if (Test-Path $licensePath) {
        $repoResult.HasLicense = $true
        $stats.Licensed++
        
        # Try to determine license type
        $licenseContent = Get-Content $licensePath -Raw
        if ($licenseContent -match "MIT License") {
            $repoResult.LicenseType = "MIT"
        } elseif ($licenseContent -match "Apache License") {
            $repoResult.LicenseType = "Apache-2.0"
        } elseif ($licenseContent -match "GNU.*General Public License") {
            $repoResult.LicenseType = "GPL"
        } else {
            $repoResult.LicenseType = "Custom/Other"
        }
        
        # Get commit date for LICENSE
        Push-Location $repoPath
        try {
            $commitInfo = git log --follow --format="%ai" -- LICENSE 2>$null | Select-Object -Last 1
            if ($commitInfo) {
                $repoResult.LicenseCommitDate = $commitInfo
            }
        } catch {
            # Git log failed, continue
        }
        Pop-Location
        
        Write-Success "  LICENSE found: $($repoResult.LicenseType)"
    } else {
        $repoResult.Issues += "Missing LICENSE file"
        Write-Warning "  LICENSE file not found"
        
        # Auto-fix if requested
        if ($AutoFix) {
            Write-Info "  Adding MIT LICENSE..."
            $confirm = Read-Host "  Add MIT license to $repoName? (y/N)"
            if ($confirm -eq 'y' -or $confirm -eq 'Y') {
                Set-Content -Path $licensePath -Value $mitTemplate -Encoding UTF8
                Write-Success "  LICENSE created"
                $repoResult.HasLicense = $true
                $repoResult.LicenseType = "MIT"
                $stats.Licensed++
            }
        }
    }
    
    # Check for artifacts folder or external_discussions.md
    if (Test-Path $artifactsPath) {
        $repoResult.HasArtifacts = $true
        $repoResult.ArtifactLocation = "artifacts/"
        $artifactCount = (Get-ChildItem $artifactsPath -File).Count
        $stats.HasArtifacts++
        Write-Success "  artifacts/ folder found ($artifactCount files)"
    } elseif (Test-Path $extDiscussionsPath) {
        $repoResult.HasArtifacts = $true
        $repoResult.ArtifactLocation = "external_discussions.md"
        $stats.HasArtifacts++
        Write-Success "  external_discussions.md found"
    } else {
        $repoResult.Issues += "No artifact archive found"
        Write-Warning "  No artifacts/ folder or external_discussions.md"
    }
    
    # Determine overall status
    if ($repoResult.HasLicense -and $repoResult.HasArtifacts) {
        $repoResult.Status = "fully_sovereign"
        $stats.FullySovereign++
        Write-Success "  Status: Fully Sovereign ✓"
    } elseif ($repoResult.HasLicense) {
        $repoResult.Status = "needs_artifacts"
        $stats.NeedsAttention++
        Write-Warning "  Status: Licensed (needs artifacts)"
    } else {
        $repoResult.Status = "needs_attention"
        $stats.NeedsAttention++
        Write-Error "  Status: Needs Attention"
    }
    
    $results += $repoResult
    Write-Host ""
}

# Print summary
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "SOVEREIGNTY VERIFICATION SUMMARY" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""
Write-Host "Total Repositories:    $($stats.Total)" -ForegroundColor White
Write-Host "Licensed:              $($stats.Licensed)/$($stats.Total)" -ForegroundColor $(if ($stats.Licensed -eq $stats.Total) { "Green" } else { "Yellow" })
Write-Host "Has Artifacts:         $($stats.HasArtifacts)/$($stats.Total)" -ForegroundColor $(if ($stats.HasArtifacts -eq $stats.Total) { "Green" } else { "Yellow" })
Write-Host "Fully Sovereign:       $($stats.FullySovereign)/$($stats.Total)" -ForegroundColor $(if ($stats.FullySovereign -eq $stats.Total) { "Green" } else { "Yellow" })
Write-Host "Needs Attention:       $($stats.NeedsAttention)" -ForegroundColor $(if ($stats.NeedsAttention -eq 0) { "Green" } else { "Red" })
Write-Host ""

# Generate report if requested
if ($GenerateReport) {
    $report = @{
        Timestamp = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"
        ScanRoot = $RepoRoot
        Statistics = $stats
        Repositories = $results
    }
    
    $report | ConvertTo-Json -Depth 10 | Set-Content $OutputPath -Encoding UTF8
    Write-Success "Report generated: $OutputPath"
    
    # Also generate markdown report
    $mdPath = $OutputPath -replace '\.json$', '.md'
    $mdReport = @"
# Sovereignty Verification Report

Generated: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
Scan Root: $RepoRoot

## Summary Statistics

| Metric | Count | Percentage |
|--------|-------|------------|
| Total Repositories | $($stats.Total) | 100% |
| Licensed | $($stats.Licensed) | $([math]::Round(($stats.Licensed / $stats.Total) * 100, 1))% |
| Has Artifacts | $($stats.HasArtifacts) | $([math]::Round(($stats.HasArtifacts / $stats.Total) * 100, 1))% |
| Fully Sovereign | $($stats.FullySovereign) | $([math]::Round(($stats.FullySovereign / $stats.Total) * 100, 1))% |
| Needs Attention | $($stats.NeedsAttention) | $([math]::Round(($stats.NeedsAttention / $stats.Total) * 100, 1))% |

## Repository Details

"@
    
    foreach ($result in $results) {
        $mdReport += @"

### $($result.Name)

- **Status**: $($result.Status)
- **License**: $(if ($result.HasLicense) { $result.LicenseType } else { "❌ None" })
- **Artifacts**: $(if ($result.HasArtifacts) { "✓ " + $result.ArtifactLocation } else { "❌ None" })
- **Path**: ``$($result.Path)``
$(if ($result.Issues.Count -gt 0) { "- **Issues**: " + ($result.Issues -join ", ") } else { "" })

"@
    }
    
    $mdReport | Set-Content $mdPath -Encoding UTF8
    Write-Success "Markdown report generated: $mdPath"
}

Write-Host ""
Write-Host "Verification complete! 🎉" -ForegroundColor Green

# Exit with appropriate code
if ($stats.NeedsAttention -gt 0) {
    exit 1
} else {
    exit 0
}
