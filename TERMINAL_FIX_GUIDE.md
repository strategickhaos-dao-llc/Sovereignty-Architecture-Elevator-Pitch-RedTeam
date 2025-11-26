# VS Code Terminal & PowerShell Troubleshooting Guide

This guide addresses common terminal and PowerShell issues when working with the Sovereignty Architecture project on Windows.

## Common Issue: PowerShell Extension Terminal Error (Exit Code -2147450743)

### Symptoms
```
The terminal process "C:\Program Files (x86)\PowerShell\7\pwsh.exe" terminated with exit code: -2147450743
```

### Root Causes
1. **PowerShell 7 Installation Issues** - Corrupted or incomplete installation
2. **PATH Conflicts** - Multiple PowerShell versions conflicting
3. **VS Code Extension Problems** - PowerShell Editor Services failing to start
4. **Permission Issues** - Insufficient permissions for extension modules

### Solutions

#### Solution 1: Repair/Reinstall PowerShell 7

```powershell
# Option A: Reinstall via winget (recommended)
winget uninstall Microsoft.PowerShell
winget install Microsoft.PowerShell

# Option B: Reinstall via MSI
# Download from: https://github.com/PowerShell/PowerShell/releases
# Choose the latest stable .msi installer for Windows x64
```

#### Solution 2: Use PowerShell 5.1 Instead

If PowerShell 7 continues to have issues, configure VS Code to use the built-in Windows PowerShell 5.1:

1. Open VS Code Settings (`Ctrl+,`)
2. Search for "terminal.integrated.defaultProfile.windows"
3. Set it to "Windows PowerShell"

Or add to your `settings.json`:
```json
{
    "terminal.integrated.defaultProfile.windows": "Windows PowerShell",
    "powershell.powerShellDefaultVersion": "Windows PowerShell"
}
```

#### Solution 3: Reset PowerShell Extension

1. Close VS Code completely
2. Delete the PowerShell extension storage:
   ```powershell
   Remove-Item -Recurse -Force "$env:APPDATA\Code\User\globalStorage\ms-vscode.powershell"
   ```
3. Clear VS Code extension cache:
   ```powershell
   Remove-Item -Recurse -Force "$env:USERPROFILE\.vscode\extensions\ms-vscode.powershell-*"
   ```
4. Reopen VS Code and reinstall the PowerShell extension

#### Solution 4: Fix PATH Environment Variable

Ensure PowerShell 7 is correctly in your PATH:

```powershell
# Check current PowerShell locations
Get-Command pwsh -All

# Add PowerShell 7 to PATH (run as Administrator)
$pwshPath = "C:\Program Files\PowerShell\7"
$currentPath = [Environment]::GetEnvironmentVariable("Path", "Machine")
if ($currentPath -notlike "*$pwshPath*") {
    [Environment]::SetEnvironmentVariable("Path", "$currentPath;$pwshPath", "Machine")
}
```

**Note:** The error shows PowerShell installed in `C:\Program Files (x86)\PowerShell\7` which is unusual (typically 64-bit apps go to `C:\Program Files`). Consider reinstalling to the correct location.

---

## Common Issue: Git Repository Opened at User Home Directory

### Symptoms
```
[Model][openRepository] Opened repository (path): c:\Users\Me10101Main
[Model][openRepository] Opened repository (real path): c:\Users\Me10101Main
```

VS Code's Git extension is treating your home directory as a repository.

### Root Cause
A `.git` folder exists in your user home directory, likely created accidentally.

### Solutions

#### Solution 1: Remove Accidental Git Repository

**WARNING:** Only do this if you're sure there's no intentional git repository in your home folder.

```powershell
# Check if .git exists in home directory
Test-Path "$env:USERPROFILE\.git"

# If true, remove it (backup first if unsure)
Move-Item "$env:USERPROFILE\.git" "$env:USERPROFILE\.git.backup"

# Or delete if you're certain
Remove-Item -Recurse -Force "$env:USERPROFILE\.git"
```

#### Solution 2: Exclude Home Directory from Git Detection

Add to VS Code `settings.json`:
```json
{
    "git.ignoredRepositories": [
        "C:\\Users\\Me10101Main",
        "${env:USERPROFILE}"
    ],
    "git.scanRepositories": []
}
```

#### Solution 3: Configure Git to Ignore Home Directory

```powershell
# Add home directory to global Git exclude
git config --global core.excludesFile "$env:USERPROFILE\.gitignore_global"
echo "~/" >> "$env:USERPROFILE\.gitignore_global"
```

---

## Common Issue: Git Push Authentication Failure

### Symptoms
```
fatal: Could not read from remote repository.
Please make sure you have the correct access rights and the repository exists.
```

### Solutions

#### Solution 1: Configure Git Credential Manager

```powershell
# Ensure Git Credential Manager is configured
git config --global credential.helper manager

# For GitHub specifically
git config --global credential.https://github.com.provider generic
```

#### Solution 2: Use SSH Instead of HTTPS

```powershell
# Generate SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Start SSH agent
Start-Service ssh-agent
ssh-add "$env:USERPROFILE\.ssh\id_ed25519"

# Add the public key to GitHub: https://github.com/settings/keys

# Update remote URL
git remote set-url origin git@github.com:Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-.git
```

#### Solution 3: Use GitHub CLI

```powershell
# Install GitHub CLI
winget install GitHub.cli

# Authenticate
gh auth login

# Verify authentication
gh auth status
```

---

## Recommended VS Code Settings for This Project

Create or update `.vscode/settings.json` in your project:

```json
{
    "terminal.integrated.defaultProfile.windows": "PowerShell",
    "terminal.integrated.profiles.windows": {
        "PowerShell": {
            "source": "PowerShell",
            "icon": "terminal-powershell",
            "args": ["-NoProfile", "-ExecutionPolicy", "Bypass"]
        },
        "Windows PowerShell": {
            "path": "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe"
        },
        "Git Bash": {
            "source": "Git Bash"
        }
    },
    "powershell.powerShellDefaultVersion": "PowerShell (x64)",
    "git.autoRepositoryDetection": "openEditors",
    "git.ignoredRepositories": [],
    "files.associations": {
        "*.ps1": "powershell"
    }
}
```

---

## Quick Diagnostic Commands

Run these commands to diagnose your environment:

```powershell
# Check PowerShell version and location
$PSVersionTable.PSVersion
(Get-Command pwsh -ErrorAction SilentlyContinue).Source
(Get-Command powershell).Source

# Check Git version and config
git --version
git config --list --show-origin

# Check VS Code version
code --version

# List VS Code extensions
code --list-extensions | Select-String "powershell|gitlens"

# Check if home directory has .git folder
Get-ChildItem "$env:USERPROFILE" -Hidden | Where-Object { $_.Name -eq ".git" }

# Test Git remote connection
git ls-remote origin
```

---

## Project-Specific Setup

For the Sovereignty Architecture project, we recommend:

1. **Clone to a dedicated workspace folder** (not under OneDrive or home directory):
   ```powershell
   mkdir C:\Projects
   cd C:\Projects
   git clone https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-.git
   cd Sovereignty-Architecture-Elevator-Pitch-
   code .
   ```

2. **Use the provided scripts**:
   - Windows: `.\start-cloudos.ps1`
   - Linux/macOS: `./start-desktop.sh`

3. **Set up environment variables**:
   ```powershell
   Copy-Item .env.example .env
   # Edit .env with your Discord/GitHub tokens
   ```

---

## Getting Help

If you continue to experience issues:

1. **Check VS Code Output**: View → Output → Select "PowerShell Extension Logs"
2. **Check Git Logs**: View → Output → Select "Git"
3. **Discord Support**: Join our [Discord Server](https://discord.gg/strategickhaos)
4. **GitHub Issues**: [Open an issue](https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-/issues)

---

*Built with 🔥 by the Strategickhaos Swarm Intelligence collective*
