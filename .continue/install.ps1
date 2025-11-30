# Heir Forever Raw - Continue.dev Installation Script (Windows)
# Installs Continue.dev configuration to user's profile directory

param(
    [switch]$Force = $false
)

# Set error action preference
$ErrorActionPreference = "Stop"

# Display banner
Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════╗" -ForegroundColor Magenta
Write-Host "║     Heir Forever Raw - Continue.dev Installer ❤️     ║" -ForegroundColor Magenta
Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Magenta
Write-Host ""

# Determine target directory
$ContinueDir = "$env:USERPROFILE\.continue"
Write-Host "Target directory: " -NoNewline -ForegroundColor Cyan
Write-Host $ContinueDir -ForegroundColor Yellow
Write-Host ""

# Get script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Check if files exist
if (-not (Test-Path "$ScriptDir\continue_settings.json")) {
    Write-Host "❌ Error: Configuration files not found in $ScriptDir" -ForegroundColor Red
    exit 1
}

# Check if Continue.dev config already exists
if (Test-Path "$ContinueDir\continue_settings.json") {
    Write-Host "⚠️  Existing Continue.dev configuration detected" -ForegroundColor Yellow
    Write-Host "   Location: $ContinueDir\continue_settings.json" -ForegroundColor Yellow
    Write-Host ""
    
    if (-not $Force) {
        $response = Read-Host "Do you want to backup and replace it? (y/N)"
        if ($response -notmatch "^[Yy]$") {
            Write-Host "ℹ️  Installation cancelled" -ForegroundColor Cyan
            exit 0
        }
    }
    
    # Create backup
    $BackupDir = "$ContinueDir\backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
    Write-Host "📦 Creating backup at: $BackupDir" -ForegroundColor Cyan
    New-Item -ItemType Directory -Path $BackupDir -Force | Out-Null
    Copy-Item -Path "$ContinueDir\*" -Destination $BackupDir -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "✅ Backup created" -ForegroundColor Green
    Write-Host ""
}

# Create Continue directory if it doesn't exist
Write-Host "📁 Creating Continue.dev directory..." -ForegroundColor Cyan
New-Item -ItemType Directory -Path "$ContinueDir\config\profiles" -Force | Out-Null
New-Item -ItemType Directory -Path "$ContinueDir\icons" -Force | Out-Null

# Copy configuration files
Write-Host "📋 Copying configuration files..." -ForegroundColor Cyan
Copy-Item -Path "$ScriptDir\continue_settings.json" -Destination "$ContinueDir\" -Force
Copy-Item -Path "$ScriptDir\config\profiles\heir_forever_raw.yaml" -Destination "$ContinueDir\config\profiles\" -Force

# Copy documentation
Write-Host "📚 Copying documentation..." -ForegroundColor Cyan
if (Test-Path "$ScriptDir\README.md") {
    Copy-Item -Path "$ScriptDir\README.md" -Destination "$ContinueDir\" -Force
}
if (Test-Path "$ScriptDir\SETUP.md") {
    Copy-Item -Path "$ScriptDir\SETUP.md" -Destination "$ContinueDir\" -Force
}
if (Test-Path "$ScriptDir\icons\README.md") {
    Copy-Item -Path "$ScriptDir\icons\README.md" -Destination "$ContinueDir\icons\" -Force
}

Write-Host ""
Write-Host "✅ Configuration files installed successfully!" -ForegroundColor Green
Write-Host ""

# Check if Ollama is installed
Write-Host "🔍 Checking for Ollama installation..." -ForegroundColor Cyan
$ollamaInstalled = $false
try {
    $ollamaPath = Get-Command ollama -ErrorAction SilentlyContinue
    if ($ollamaPath) {
        Write-Host "✅ Ollama is installed" -ForegroundColor Green
        $ollamaInstalled = $true
        
        # Check if service is running
        try {
            $result = ollama list 2>&1
            Write-Host "✅ Ollama service is running" -ForegroundColor Green
            Write-Host ""
            Write-Host "📦 Installed models:" -ForegroundColor Cyan
            ollama list
        } catch {
            Write-Host "⚠️  Ollama is installed but not running" -ForegroundColor Yellow
            Write-Host "   Start it with: " -NoNewline -ForegroundColor Yellow
            Write-Host "ollama serve" -ForegroundColor White
        }
    }
} catch {
    # Ollama not found
}

if (-not $ollamaInstalled) {
    Write-Host "⚠️  Ollama is not installed" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To install Ollama:" -ForegroundColor Cyan
    Write-Host "  1. Download from: " -NoNewline -ForegroundColor White
    Write-Host "https://ollama.ai/download" -ForegroundColor Yellow
    Write-Host "  2. Or use winget: " -NoNewline -ForegroundColor White
    Write-Host "winget install Ollama.Ollama" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════╗" -ForegroundColor Magenta
Write-Host "║                    Next Steps ❤️                      ║" -ForegroundColor Magenta
Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Magenta
Write-Host ""

Write-Host "1. " -NoNewline -ForegroundColor Cyan
Write-Host "Install Continue.dev VSCode extension (if not already installed)"
Write-Host "   Extensions → Search 'Continue' → Install" -ForegroundColor Yellow
Write-Host ""

Write-Host "2. " -NoNewline -ForegroundColor Cyan
Write-Host "Install Ollama (if not already installed)"
Write-Host "   See above for installation commands" -ForegroundColor Yellow
Write-Host ""

Write-Host "3. " -NoNewline -ForegroundColor Cyan
Write-Host "Pull an uncensored model:"
Write-Host "   ollama pull llama3.1:uncensored" -ForegroundColor Yellow
Write-Host "   # or" -ForegroundColor Yellow
Write-Host "   ollama pull mistral:uncensored" -ForegroundColor Yellow
Write-Host ""

Write-Host "4. " -NoNewline -ForegroundColor Cyan
Write-Host "Restart VSCode"
Write-Host ""

Write-Host "5. " -NoNewline -ForegroundColor Cyan
Write-Host "Press " -NoNewline
Write-Host "Ctrl+L" -NoNewline -ForegroundColor Yellow
Write-Host " to open Continue"
Write-Host ""

Write-Host "🎉 Your heir is waiting! ❤️" -ForegroundColor Green
Write-Host ""

Write-Host "📚 For more information, see:" -ForegroundColor Cyan
Write-Host "   $ContinueDir\README.md" -ForegroundColor Yellow
Write-Host "   $ContinueDir\SETUP.md" -ForegroundColor Yellow
Write-Host ""
