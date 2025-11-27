# PowerShell Troubleshooting Guide

This guide addresses common issues when running PowerShell scripts in this repository on Windows systems.

## Table of Contents

1. [BLAKE3 Download Issues](#blake3-download-issues)
2. [PowerShell Syntax Errors](#powershell-syntax-errors)
3. [Git Remote Errors](#git-remote-errors)

---

## BLAKE3 Download Issues

### Problem

When downloading BLAKE3's `b3sum` tool, you may encounter errors if using incorrect URLs:

```
ERROR: The download URL for the zip was incorrect
```

### Cause

The official BLAKE3 releases provide a standalone `.exe` file for Windows, **not** a `.zip` archive.

### Solution

Use the correct URL for the Windows executable:

```powershell
# CORRECT: Download the standalone .exe
$b3Url = "https://github.com/BLAKE3-team/BLAKE3/releases/latest/download/b3sum_windows_x64_bin.exe"
$b3Exe = Join-Path $PWD "b3sum.exe"

Write-Host "Downloading b3sum..."
Invoke-WebRequest -Uri $b3Url -OutFile $b3Exe

# Verify download
if (Test-Path $b3Exe) {
    Write-Host "Download successful: $b3Exe"
}
```

### Using the Provided Script

Instead of manual downloads, use the provided script:

```powershell
# Compute hash for an artifact
.\scripts\compute-blake3-hash.ps1 -ArtifactPath "path\to\your\artifact.tar.gz"

# Compute hash and update PROVENANCE.md
.\scripts\compute-blake3-hash.ps1 -ArtifactPath "swarmgate_v1.0.tar.gz" -UpdateProvenance
```

---

## PowerShell Syntax Errors

### Problem

Commands with `<` and `>` characters fail with parser errors:

```
ParserError: 
Line |
   1 |  gh repo create <owner>/<repo> --private
     |                 ~
     | The '<' operator is reserved for future use.
```

### Cause

In PowerShell, `<` and `>` are reserved operators (redirection operators). Using them as placeholder markers in commands causes parser errors.

### Solution

**Never use `< >` as placeholder markers in PowerShell commands.** Use actual values or variables:

```powershell
# WRONG - causes parser error:
gh repo create <owner>/<repo> --private

# CORRECT - use actual values:
gh repo create strategickhaos/swarmgate --private --source=. --remote=origin --push

# CORRECT - use variables:
$owner = "strategickhaos"
$repo = "swarmgate"
gh repo create "$owner/$repo" --private --source=. --remote=origin --push
```

### Using the Provided Script

The provided `setup-github-repo.ps1` script handles this correctly:

```powershell
# Create a private repository and push code
.\scripts\setup-github-repo.ps1 -Owner "strategickhaos" -RepoName "swarmgate"

# Create a public repository
.\scripts\setup-github-repo.ps1 -Owner "strategickhaos" -RepoName "swarmgate" -Public

# Only configure remote (if repo already exists)
.\scripts\setup-github-repo.ps1 -Owner "strategickhaos" -RepoName "swarmgate" -SetRemoteOnly
```

---

## Git Remote Errors

### Problem

Pushing to a remote fails with a 404 error:

```
fatal: repository 'https://github.com/owner/repo.git/' not found
```

### Cause

This occurs when:
1. The repository doesn't exist on GitHub yet
2. You don't have permission to access the repository
3. The remote URL is incorrect

### Solution

#### Option 1: Create the Repository First

Ensure you're authenticated with GitHub CLI:

```powershell
# Login to GitHub CLI
gh auth login

# Create the repository and push
gh repo create strategickhaos/swarmgate --private --source=. --remote=origin --push
```

#### Option 2: If Repository Already Exists

Configure the remote URL and push:

```powershell
# Set the correct remote URL
git remote set-url origin https://github.com/strategickhaos/swarmgate.git

# Push to main branch
git push -u origin main

# Push tags if any
git push origin --tags
```

#### Option 3: Use the Provided Script

```powershell
# Full setup (creates repo if needed, configures remote, pushes)
.\scripts\setup-github-repo.ps1 -Owner "strategickhaos" -RepoName "swarmgate"

# Just configure remote and push (repo must exist)
.\scripts\setup-github-repo.ps1 -Owner "strategickhaos" -RepoName "swarmgate" -SetRemoteOnly
```

---

## Complete Workflow Example

Here's a complete workflow to set up a new project with BLAKE3 verification:

```powershell
# 1. Create your artifact
tar -czvf swarmgate_v1.0.tar.gz ./src

# 2. Compute and record BLAKE3 hash
.\scripts\compute-blake3-hash.ps1 -ArtifactPath "swarmgate_v1.0.tar.gz" -UpdateProvenance

# 3. Create GitHub repository and push
.\scripts\setup-github-repo.ps1 -Owner "strategickhaos" -RepoName "swarmgate"

# 4. Tag the release
git tag v1.0
git push origin v1.0
```

---

## Need Help?

If you encounter issues not covered here:

1. Check GitHub CLI authentication: `gh auth status`
2. Check git remote configuration: `git remote -v`
3. Verify file paths use backslashes on Windows: `path\to\file`
4. Run commands with verbose output when available
