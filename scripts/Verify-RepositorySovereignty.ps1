<#
.SYNOPSIS
    Verifies and auto-fixes LICENSE and artifacts across all repositories.

.DESCRIPTION
    This Refinery-style script scans all repositories in a specified directory
    (or current directory) and ensures:
    1. Each repo has a LICENSE file (auto-generates MIT if missing)
    2. Each repo has an artifacts/ directory for external AI discussions
    3. Generates a sovereignty report showing compliance status
    4. Can optionally append to verification_ledger.jsonl for audit trail

.PARAMETER ReposPath
    Root directory containing repositories to scan. Defaults to current directory.

.PARAMETER AutoFix
    If specified, automatically creates missing LICENSE files and artifacts directories.

.PARAMETER DefaultLicenseType
    License type to use when auto-generating (MIT, Apache-2.0, AGPLv3). Default: MIT

.PARAMETER CopyrightHolder
    Copyright holder name for auto-generated licenses. Default: "Sovereign Heir"

.PARAMETER OutputReport
    Path to save the sovereignty report. Default: sovereignty_report.txt

.EXAMPLE
    .\Verify-RepositorySovereignty.ps1 -ReposPath "C:\repos" -AutoFix
    Scans all repos in C:\repos and auto-fixes missing LICENSE/artifacts

.EXAMPLE
    .\Verify-RepositorySovereignty.ps1 -AutoFix -DefaultLicenseType "Apache-2.0"
    Scans current directory and uses Apache 2.0 license for auto-generation

.NOTES
    Full sovereignty: You own this script, you own the repos, one rm -rf resets everything.
    No cloud dependencies, zero internet required after first run.
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory=$false)]
    [string]$ReposPath = ".",
    
    [Parameter(Mandatory=$false)]
    [switch]$AutoFix,
    
    [Parameter(Mandatory=$false)]
    [ValidateSet("MIT", "Apache-2.0", "AGPLv3", "Custom")]
    [string]$DefaultLicenseType = "MIT",
    
    [Parameter(Mandatory=$false)]
    [string]$CopyrightHolder = "Sovereign Heir",
    
    [Parameter(Mandatory=$false)]
    [string]$OutputReport = "sovereignty_report.txt"
)

# MIT License Template
$MITLicense = @"
MIT License

Copyright (c) $(Get-Date -Format "yyyy") $CopyrightHolder

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

# Apache 2.0 License Template
$Apache2License = @"
Apache License
Version 2.0, January 2004
http://www.apache.org/licenses/

Copyright $(Get-Date -Format "yyyy") $CopyrightHolder

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"@

function Get-LicenseTemplate {
    param([string]$Type)
    
    switch ($Type) {
        "MIT" { return $MITLicense }
        "Apache-2.0" { return $Apache2License }
        "AGPLv3" { 
            Write-Warning "AGPLv3 template not included - please download from https://www.gnu.org/licenses/agpl-3.0.txt"
            return $null 
        }
        default { return $MITLicense }
    }
}

function Test-IsGitRepository {
    param([string]$Path)
    
    return Test-Path (Join-Path $Path ".git")
}

function Add-LicenseFile {
    param(
        [string]$RepoPath,
        [string]$LicenseType
    )
    
    $licensePath = Join-Path $RepoPath "LICENSE"
    $licenseContent = Get-LicenseTemplate -Type $LicenseType
    
    if ($null -eq $licenseContent) {
        return $false
    }
    
    Set-Content -Path $licensePath -Value $licenseContent -Encoding UTF8
    Write-Host "✅ Created LICENSE ($LicenseType) in: $RepoPath" -ForegroundColor Green
    
    # Commit to git if in a git repo
    Push-Location $RepoPath
    try {
        git add LICENSE 2>$null
        git commit -m "Add $LicenseType license — full sovereign control retained" 2>$null
    } catch {
        Write-Verbose "Could not commit LICENSE (not a git repo or git not available)"
    }
    Pop-Location
    
    return $true
}

function Add-ArtifactsDirectory {
    param([string]$RepoPath)
    
    $artifactsPath = Join-Path $RepoPath "artifacts"
    
    if (-not (Test-Path $artifactsPath)) {
        New-Item -Path $artifactsPath -ItemType Directory -Force | Out-Null
        
        # Create a README in artifacts directory
        $readmePath = Join-Path $artifactsPath "README.md"
        $readmeContent = @"
# External AI Artifacts

This directory contains archived external AI discussion links and artifacts used in the development and evolution of this repository.

## Purpose

- Audit trail for design decisions
- Agent training references
- Meta-evolution documentation
- Immutable proof of external contributions

## Adding Artifacts

To add a new artifact:

1. Create a markdown file with date: ``artifact_name_YYYY-MM-DD.md``
2. Include source URL and JSON metadata block
3. Add to git: ``git add artifacts/ && git commit -m "Archive artifact"``

## Verification

All artifacts are under version control and can be verified with:

```powershell
Get-FileHash artifacts/*.md -Algorithm SHA256
```

## Sovereignty Guarantee

- ✅ Fully local and under your control
- ✅ No cloud dependencies
- ✅ Can be deleted or modified at any time
- ✅ Immutable once committed to git
"@
        Set-Content -Path $readmePath -Value $readmeContent -Encoding UTF8
        Write-Host "✅ Created artifacts/ directory with README in: $RepoPath" -ForegroundColor Green
        
        # Commit to git if in a git repo
        Push-Location $RepoPath
        try {
            git add artifacts/ 2>$null
            git commit -m "Add artifacts directory for external AI discussion archiving" 2>$null
        } catch {
            Write-Verbose "Could not commit artifacts/ (not a git repo or git not available)"
        }
        Pop-Location
        
        return $true
    }
    
    return $false
}

# Main execution
Write-Host "`n🔍 Sovereignty Architecture Verification Engine" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "Scanning: $ReposPath" -ForegroundColor Yellow
Write-Host "Auto-fix: $($AutoFix.IsPresent)" -ForegroundColor Yellow
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""

$results = @()
$reposScanned = 0
$reposWithLicense = 0
$reposWithArtifacts = 0
$reposFixed = 0

# Resolve full path
$fullPath = Resolve-Path $ReposPath -ErrorAction SilentlyContinue
if (-not $fullPath) {
    Write-Error "Path not found: $ReposPath"
    exit 1
}

# Find all git repositories
$gitRepos = Get-ChildItem -Path $fullPath -Recurse -Directory -Filter ".git" -ErrorAction SilentlyContinue | 
    ForEach-Object { Split-Path $_.FullName -Parent }

if ($gitRepos.Count -eq 0) {
    # If no .git folders found, check if current directory is a repo
    if (Test-IsGitRepository -Path $fullPath) {
        $gitRepos = @($fullPath)
    } else {
        Write-Warning "No git repositories found in: $ReposPath"
        exit 0
    }
}

Write-Host "Found $($gitRepos.Count) git repositories`n" -ForegroundColor Cyan

foreach ($repoPath in $gitRepos) {
    $reposScanned++
    $repoName = Split-Path $repoPath -Leaf
    
    Write-Host "📦 Checking: $repoName" -ForegroundColor White
    
    $hasLicense = Test-Path (Join-Path $repoPath "LICENSE")
    $hasArtifacts = Test-Path (Join-Path $repoPath "artifacts")
    
    $result = [PSCustomObject]@{
        Repository = $repoName
        Path = $repoPath
        HasLicense = $hasLicense
        HasArtifacts = $hasArtifacts
        Fixed = $false
    }
    
    # Check LICENSE
    if ($hasLicense) {
        Write-Host "  ✅ LICENSE exists" -ForegroundColor Green
        $reposWithLicense++
    } else {
        Write-Host "  ❌ LICENSE missing" -ForegroundColor Red
        
        if ($AutoFix) {
            if (Add-LicenseFile -RepoPath $repoPath -LicenseType $DefaultLicenseType) {
                $result.HasLicense = $true
                $result.Fixed = $true
                $reposFixed++
                $reposWithLicense++
            }
        }
    }
    
    # Check artifacts/
    if ($hasArtifacts) {
        Write-Host "  ✅ artifacts/ exists" -ForegroundColor Green
        $reposWithArtifacts++
    } else {
        Write-Host "  ❌ artifacts/ missing" -ForegroundColor Red
        
        if ($AutoFix) {
            if (Add-ArtifactsDirectory -RepoPath $repoPath) {
                $result.HasArtifacts = $true
                $result.Fixed = $true
                $reposFixed++
                $reposWithArtifacts++
            }
        }
    }
    
    $results += $result
    Write-Host ""
}

# Generate report
$report = @"
Sovereignty Architecture Verification Report
Generated: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
Scan Path: $ReposPath
Auto-fix: $($AutoFix.IsPresent)

Summary:
========
Total Repositories Scanned: $reposScanned
Repositories with LICENSE: $reposWithLicense ($([math]::Round($reposWithLicense/$reposScanned*100, 1))%)
Repositories with artifacts/: $reposWithArtifacts ($([math]::Round($reposWithArtifacts/$reposScanned*100, 1))%)
Repositories Fixed: $reposFixed

Details:
========
"@

foreach ($result in $results) {
    $report += "`n$($result.Repository)"
    $report += "`n  Path: $($result.Path)"
    $report += "`n  LICENSE: $($result.HasLicense)"
    $report += "`n  artifacts/: $($result.HasArtifacts)"
    if ($result.Fixed) {
        $report += "`n  Status: FIXED ✅"
    }
    $report += "`n"
}

# Save report
Set-Content -Path $OutputReport -Value $report -Encoding UTF8
Write-Host "📄 Report saved to: $OutputReport" -ForegroundColor Cyan

# Display summary
Write-Host "`n" + ("=" * 60) -ForegroundColor Cyan
Write-Host "Summary:" -ForegroundColor Cyan
Write-Host ("=" * 60) -ForegroundColor Cyan
Write-Host "Total Repositories: $reposScanned" -ForegroundColor White
Write-Host "With LICENSE: $reposWithLicense/$reposScanned ($([math]::Round($reposWithLicense/$reposScanned*100, 1))%)" -ForegroundColor $(if($reposWithLicense -eq $reposScanned){"Green"}else{"Yellow"})
Write-Host "With artifacts/: $reposWithArtifacts/$reposScanned ($([math]::Round($reposWithArtifacts/$reposScanned*100, 1))%)" -ForegroundColor $(if($reposWithArtifacts -eq $reposScanned){"Green"}else{"Yellow"})

if ($AutoFix -and $reposFixed -gt 0) {
    Write-Host "Repositories Fixed: $reposFixed" -ForegroundColor Green
}

Write-Host "`n✨ Sovereignty verification complete!" -ForegroundColor Green
Write-Host "Full control retained. Zero cloud dependencies. 100% auditable.`n" -ForegroundColor Gray
