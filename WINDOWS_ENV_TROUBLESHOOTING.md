# Windows Environment Troubleshooting Guide

A guide for resolving common environment issues on Windows for the Sovereignty Architecture development workflow.

## 🔑 GPG Configuration Issues

### Problem: GPG Path Not Found

**Symptoms:**
- `gpg: command not found`
- Git signing fails with GPG errors

**Solution:**

```powershell
# Find GPG installation
$gpgLocations = @(
    "C:\Program Files (x86)\GnuPG\bin",
    "C:\Program Files\GnuPG\bin",
    "$env:ProgramFiles\Git\usr\bin"
)

foreach ($loc in $gpgLocations) {
    if (Test-Path "$loc\gpg.exe") {
        Write-Host "Found GPG at: $loc"
        # Add to current session
        $env:Path += ";$loc"
        break
    }
}

# Configure Git to use GPG
git config --global gpg.program "C:\Program Files (x86)\GnuPG\bin\gpg.exe"
```

### Problem: GPG Key Import Fails

**Symptoms:**
- `gpg: no valid OpenPGP data found`
- Key not recognized after import

**Solution:**

```powershell
# List available keys
gpg --list-secret-keys --keyid-format LONG

# If key exists but not imported:
gpg --import "$env:USERPROFILE\.gnupg\private-keys-v1.d\*.key"

# Generate new key if needed
gpg --full-generate-key

# Export key ID for Git
$keyId = (gpg --list-secret-keys --keyid-format LONG | Select-String "sec").Line.Split('/')[1].Split(' ')[0]
git config --global user.signingkey $keyId
```

## 🔗 Git Remote Configuration

### Problem: Wrong Remote URL

**Symptoms:**
- Push fails with authentication errors
- Remote points to wrong repository

**Solution:**

```powershell
# Check current remotes
git remote -v

# Update origin URL
git remote set-url origin https://github.com/YOUR_USER/YOUR_REPO.git

# Or remove and re-add
git remote remove origin
git remote add origin https://github.com/YOUR_USER/YOUR_REPO.git

# Verify
git remote -v
```

### Problem: Force Push Required

**Note:** Force push should be used carefully. Only use when necessary.

```powershell
# Safe force push with lease (prevents overwriting others' work)
git push --force-with-lease

# Regular force push (use with caution)
git push --force
```

## ⏰ OpenTimestamps Installation

### Problem: `ots` Command Not Found

**Solution using Python:**

```powershell
# Install via pip
pip install opentimestamps-client

# Verify installation
ots --version

# Basic usage
ots stamp document.txt
ots verify document.txt.ots
```

**Alternative using Chocolatey:**

```powershell
# Install Chocolatey first if not present
# Then install ots
choco install opentimestamps -y
```

## 🌐 Web Request Issues

### Problem: Invoke-WebRequest Fails

**Symptoms:**
- SSL/TLS errors
- Parsing errors with HTML content

**Solution:**

```powershell
# Use -UseBasicParsing for raw data
Invoke-WebRequest -Uri "https://example.com/file" `
    -UseBasicParsing `
    -OutFile "output.bin"

# For binary content, specify content type
$body = Get-Content "file.txt" -Raw -Encoding UTF8
Invoke-WebRequest -Uri "https://api.example.com" `
    -Method POST `
    -Body $body `
    -ContentType "application/octet-stream" `
    -UseBasicParsing `
    -OutFile "response.bin"

# Fix TLS issues
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
```

## 📂 PATH Environment Issues

### Problem: Duplicate PATH Entries

**Symptoms:**
- Very long PATH variable
- Slow command lookup
- PATH exceeds maximum length

**Solution:**

```powershell
# View current PATH entries
$env:Path -split ';' | ForEach-Object { Write-Host $_ }

# Remove duplicates (session only)
$cleanPath = ($env:Path -split ';' | Select-Object -Unique | Where-Object { $_ }) -join ';'
$env:Path = $cleanPath

# Make permanent (User scope)
[Environment]::SetEnvironmentVariable("Path", $cleanPath, "User")

# Verify reduction
Write-Host "Entries reduced: $(($env:Path -split ';').Count) unique paths"
```

### Problem: WSL PATH Conflicts

**Symptoms:**
- Windows paths appearing in WSL
- Command resolution issues

**Solution:**

```bash
# In WSL, add to ~/.bashrc or ~/.zshrc
export PATH=$(echo $PATH | tr ':' '\n' | grep -v '/mnt/c/' | tr '\n' ':' | sed 's/:$//')
```

## 🌐 Network Diagnostics

### Problem: DNS or Connectivity Issues

**Solution (requires admin for some commands):**

```powershell
# DNS flush (requires elevation)
ipconfig /flushdns

# Reset network stack (requires elevation)
netsh winsock reset
netsh int ip reset

# Test DNS resolution
Resolve-DnsName github.com

# Test connectivity
Test-NetConnection github.com -Port 443
```

**Note:** Network reset commands require Administrator privileges:

```powershell
# Run elevated
Start-Process powershell -Verb RunAs -ArgumentList "ipconfig /flushdns; netsh winsock reset"
```

## 📄 Document Conversion

### Problem: Pandoc PDF Generation Fails

**Symptoms:**
- PDF engine not found
- Font errors

**Solution:**

```powershell
# Install Pandoc
choco install pandoc -y

# Install a PDF engine (choose one)
choco install miktex -y      # For pdflatex/xelatex
# or
pip install weasyprint        # For HTML-to-PDF

# Generate PDF with specific engine
pandoc document.md -o output.pdf --pdf-engine=xelatex

# Alternative: use wkhtmltopdf
choco install wkhtmltopdf -y
pandoc document.md -o output.pdf --pdf-engine=wkhtmltopdf
```

## ✅ Quick Diagnostic Script

Run this script to check your environment:

```powershell
# save as check-env.ps1
Write-Host "=== Environment Check ===" -ForegroundColor Cyan

# Check GPG
$gpg = Get-Command gpg -ErrorAction SilentlyContinue
if ($gpg) {
    Write-Host "✓ GPG: $($gpg.Source)" -ForegroundColor Green
} else {
    Write-Host "✗ GPG not found" -ForegroundColor Red
}

# Check Git
$git = Get-Command git -ErrorAction SilentlyContinue
if ($git) {
    Write-Host "✓ Git: $(git --version)" -ForegroundColor Green
} else {
    Write-Host "✗ Git not found" -ForegroundColor Red
}

# Check Git signing key
$signingKey = git config --get user.signingkey 2>$null
if ($signingKey) {
    Write-Host "✓ Git signing key: $signingKey" -ForegroundColor Green
} else {
    Write-Host "⚠ No Git signing key configured" -ForegroundColor Yellow
}

# Check Python
$python = Get-Command python -ErrorAction SilentlyContinue
if ($python) {
    Write-Host "✓ Python: $(python --version)" -ForegroundColor Green
} else {
    Write-Host "⚠ Python not found" -ForegroundColor Yellow
}

# Check Pandoc
$pandoc = Get-Command pandoc -ErrorAction SilentlyContinue
if ($pandoc) {
    Write-Host "✓ Pandoc: $(pandoc --version | Select-Object -First 1)" -ForegroundColor Green
} else {
    Write-Host "⚠ Pandoc not found" -ForegroundColor Yellow
}

# Check PATH length
$pathLength = $env:Path.Length
Write-Host "`nPATH length: $pathLength characters"
if ($pathLength -gt 2000) {
    Write-Host "⚠ PATH is very long, consider cleanup" -ForegroundColor Yellow
}

# Check connectivity
try {
    $response = Invoke-WebRequest -Uri "https://api.github.com/zen" -TimeoutSec 5 -UseBasicParsing
    Write-Host "✓ GitHub connectivity OK" -ForegroundColor Green
} catch {
    Write-Host "✗ GitHub connectivity failed" -ForegroundColor Red
}
```

---

*Part of the Strategic Khaos Sovereignty Architecture documentation.*
