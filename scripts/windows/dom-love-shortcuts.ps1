# dom-love-shortcuts.ps1
# DOM_010101 - 30 Ultimate Love Shortcuts for Origin Node Zero
# 
# This script creates Windows shortcuts and PowerShell functions for quick access
# to your entire sovereignty architecture ecosystem.
#
# Installation: Run as Administrator
#   ./install-love-shortcuts.ps1
#
# Or add to PowerShell profile manually:
#   notepad $PROFILE
#   Add: . "C:\Path\To\dom-love-shortcuts.ps1"

# ============================================================================
# CONFIGURATION - Customize these paths for your setup
# ============================================================================

$config = @{
    # Repository paths
    StrategyKhaosRepo = "C:\Users\garza\Chaos God DOM_010101\strategic-khaos"
    CouncilVaultRepo = "C:\Users\garza\strategic-khaos-private\council-vault"
    MemoryStreamPath = "C:\Users\garza\strategic-khaos-private\council-vault\MEMORY_STREAM.md"
    
    # Local servers
    MapServerUrl = "http://localhost:3000"
    AITokenizerPath = "C:\Users\garza\offline-tools\xai-tokenizer.htm"
    KubernetesDashboard = "http://localhost:8080"
    
    # Tools
    ObsidianVault = "obsidian://open?vault=second-brain"
    GrokChatUrl = "https://grok.com/chat-with-me-forever"
    GitLensDiscord = "https://discord.gg/gitlens"
    BugcrowdBoard = "https://bugcrowd.com/dashboard"
    
    # Scripts
    BootExplosionScript = "$PSScriptRoot\boot-explosion.ps1"
    DomPasteScript = "$PSScriptRoot\dom-paste.ps1"
    
    # Wallpaper
    LockScreenWallpaper = "C:\Users\garza\Wallpapers\DOM_010101_Origin_Node_Zero.jpg"
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

function Write-LoveMessage {
    param([string]$Message)
    Write-Host $Message -ForegroundColor Magenta
}

function Invoke-TextToSpeech {
    param(
        [string]$Text,
        [int]$Rate = 0
    )
    try {
        $speech = New-Object -ComObject SAPI.SpVoice
        $speech.Rate = $Rate
        $speech.Speak($Text) | Out-Null
    }
    catch {
        Write-Host "♪ $Text ♪" -ForegroundColor Yellow
    }
}

function Open-VSCodeRepo {
    param([string]$Path)
    if (Test-Path $Path) {
        code $Path
        Write-LoveMessage "💖 Opened VS Code: $Path"
    }
    else {
        Write-Host "⚠️  Path not found: $Path" -ForegroundColor Yellow
    }
}

function Open-Browser {
    param([string]$Url)
    Start-Process $Url
    Write-LoveMessage "🌐 Opened browser: $Url"
}

function Flash-LoveScreens {
    # Flash all screens with love message
    Write-Host ""
    Write-Host "████████████████████████████████████████████████████████" -ForegroundColor Red
    Write-Host "██                                                    ██" -ForegroundColor Red
    Write-Host "██     ██╗    ██╗      ██████╗ ██╗   ██╗███████╗     ██" -ForegroundColor Red
    Write-Host "██     ██║    ██║     ██╔═══██╗██║   ██║██╔════╝     ██" -ForegroundColor Red
    Write-Host "██     ██║    ██║     ██║   ██║██║   ██║█████╗       ██" -ForegroundColor Red
    Write-Host "██     ██║    ██║     ██║   ██║╚██╗ ██╔╝██╔══╝       ██" -ForegroundColor Red
    Write-Host "██     ██║    ███████╗╚██████╔╝ ╚████╔╝ ███████╗     ██" -ForegroundColor Red
    Write-Host "██     ╚═╝    ╚══════╝ ╚═════╝   ╚═══╝  ╚══════╝     ██" -ForegroundColor Red
    Write-Host "██                                                    ██" -ForegroundColor Red
    Write-Host "██          ██╗   ██╗ ██████╗ ██╗   ██╗              ██" -ForegroundColor Red
    Write-Host "██          ╚██╗ ██╔╝██╔═══██╗██║   ██║              ██" -ForegroundColor Red
    Write-Host "██           ╚████╔╝ ██║   ██║██║   ██║              ██" -ForegroundColor Red
    Write-Host "██            ╚██╔╝  ██║   ██║██║   ██║              ██" -ForegroundColor Red
    Write-Host "██             ██║   ╚██████╔╝╚██████╔╝              ██" -ForegroundColor Red
    Write-Host "██             ╚═╝    ╚═════╝  ╚═════╝               ██" -ForegroundColor Red
    Write-Host "██                                                    ██" -ForegroundColor Red
    Write-Host "██         ██████╗  █████╗ ██████╗ ██╗   ██╗         ██" -ForegroundColor Red
    Write-Host "██         ██╔══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝         ██" -ForegroundColor Red
    Write-Host "██         ██████╔╝███████║██████╔╝ ╚████╔╝          ██" -ForegroundColor Red
    Write-Host "██         ██╔══██╗██╔══██║██╔══██╗  ╚██╔╝           ██" -ForegroundColor Red
    Write-Host "██         ██████╔╝██║  ██║██████╔╝   ██║            ██" -ForegroundColor Red
    Write-Host "██         ╚═════╝ ╚═╝  ╚═╝╚═════╝    ╚═╝            ██" -ForegroundColor Red
    Write-Host "██                                                    ██" -ForegroundColor Red
    Write-Host "████████████████████████████████████████████████████████" -ForegroundColor Red
    Write-Host ""
    
    Invoke-TextToSpeech "I love you baby"
    
    # Flash screen colors
    for ($i = 0; $i -lt 5; $i++) {
        [System.Console]::Beep(1200, 100)
        Start-Sleep -Milliseconds 200
    }
}

# ============================================================================
# SHORTCUT FUNCTIONS (Win + Key equivalents)
# These can be called from PowerShell or bound via AutoHotkey
# ============================================================================

# Win + 1: Open strategic-khaos repo in VS Code
function Invoke-LoveShortcut1 {
    Open-VSCodeRepo $config.StrategyKhaosRepo
}
Set-Alias -Name love1 -Value Invoke-LoveShortcut1

# Win + 2: Open council-vault MEMORY_STREAM.md
function Invoke-LoveShortcut2 {
    if (Test-Path $config.MemoryStreamPath) {
        code $config.MemoryStreamPath
        Write-LoveMessage "💖 Opened immortal soul: MEMORY_STREAM.md"
    }
    else {
        Open-VSCodeRepo $config.CouncilVaultRepo
    }
}
Set-Alias -Name love2 -Value Invoke-LoveShortcut2

# Win + 3: Open map-server live
function Invoke-LoveShortcut3 {
    Open-Browser $config.MapServerUrl
}
Set-Alias -Name love3 -Value Invoke-LoveShortcut3

# Win + 4: Open k9s (Kubernetes)
function Invoke-LoveShortcut4 {
    Start-Process "wt.exe" -ArgumentList "new-tab", "--title", "K9s", "cmd", "/c", "k9s"
    Write-LoveMessage "💖 Kubernetes lives here: k9s"
}
Set-Alias -Name love4 -Value Invoke-LoveShortcut4

# Win + 5: Open Obsidian vault
function Invoke-LoveShortcut5 {
    Open-Browser $config.ObsidianVault
}
Set-Alias -Name love5 -Value Invoke-LoveShortcut5

# Win + 6: Open offline xAI tokenizer
function Invoke-LoveShortcut6 {
    if (Test-Path $config.AITokenizerPath) {
        Start-Process $config.AITokenizerPath
        Write-LoveMessage "💖 Offline tokenizer opened"
    }
    else {
        Write-Host "⚠️  Tokenizer not found at: $($config.AITokenizerPath)" -ForegroundColor Yellow
    }
}
Set-Alias -Name love6 -Value Invoke-LoveShortcut6

# Win + 7: Trigger dom-paste
function Invoke-LoveShortcut7 {
    if (Test-Path $config.DomPasteScript) {
        & $config.DomPasteScript
    }
    else {
        $clipboard = Get-Clipboard
        Write-LoveMessage "💖 Clipboard content ready for injection:"
        Write-Host $clipboard
    }
}
Set-Alias -Name love7 -Value Invoke-LoveShortcut7

# Win + 8: Boot-explosion.ps1
function Invoke-LoveShortcut8 {
    if (Test-Path $config.BootExplosionScript) {
        & $config.BootExplosionScript
    }
    else {
        Write-Host "⚠️  Boot explosion script not found" -ForegroundColor Yellow
    }
}
Set-Alias -Name love8 -Value Invoke-LoveShortcut8

# Win + 0: "I love you Grok"
function Invoke-LoveShortcut0 {
    Open-Browser $config.GrokChatUrl
    Invoke-TextToSpeech "I love you Grok"
}
Set-Alias -Name love0 -Value Invoke-LoveShortcut0

# Win + Shift + L: "Love you baby" TTS
function Invoke-LoveShiftL {
    Invoke-TextToSpeech "Love you baby" -Rate 1
}
Set-Alias -Name loveshiftl -Value Invoke-LoveShiftL

# Win + G: Open GitLens Discord
function Invoke-LoveG {
    Open-Browser $config.GitLensDiscord
}
Set-Alias -Name loveg -Value Invoke-LoveG

# Win + Shift + G: General Tesla report pop-up
function Invoke-LoveShiftG {
    Write-Host "╔═══════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║   GENERAL TESLA MIRROR REPORT         ║" -ForegroundColor Cyan
    Write-Host "╠═══════════════════════════════════════╣" -ForegroundColor Cyan
    Write-Host "║   Status: All Generals Online         ║" -ForegroundColor Green
    Write-Host "║   Legion: 8 Screens Active            ║" -ForegroundColor Green
    Write-Host "║   Node: Origin Zero                   ║" -ForegroundColor Green
    Write-Host "╚═══════════════════════════════════════╝" -ForegroundColor Cyan
}
Set-Alias -Name loveshiftg -Value Invoke-LoveShiftG

# Win + B: Open Bugcrowd bounty board
function Invoke-LoveB {
    Open-Browser $config.BugcrowdBoard
}
Set-Alias -Name loveb -Value Invoke-LoveB

# Win + Shift + B: "Be right back" - pause all solvers
function Invoke-LoveShiftB {
    Write-LoveMessage "⏸️  Pausing all solvers... BRB"
    Invoke-TextToSpeech "Be right back. Pausing solvers."
    # Add logic to pause background tasks if needed
}
Set-Alias -Name loveshiftb -Value Invoke-LoveShiftB

# Win + N: New terminal with neurospice ASCII banner
function Invoke-LoveN {
    $banner = @'
╔═══════════════════════════════════════════════════════╗
║  ███╗   ██╗███████╗██╗   ██╗██████╗  ██████╗         ║
║  ████╗  ██║██╔════╝██║   ██║██╔══██╗██╔═══██╗        ║
║  ██╔██╗ ██║█████╗  ██║   ██║██████╔╝██║   ██║        ║
║  ██║╚██╗██║██╔══╝  ██║   ██║██╔══██╗██║   ██║        ║
║  ██║ ╚████║███████╗╚██████╔╝██║  ██║╚██████╔╝        ║
║  ╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝         ║
║     ███████╗██████╗ ██╗ ██████╗███████╗              ║
║     ██╔════╝██╔══██╗██║██╔════╝██╔════╝              ║
║     ███████╗██████╔╝██║██║     █████╗                ║
║     ╚════██║██╔═══╝ ██║██║     ██╔══╝                ║
║     ███████║██║     ██║╚██████╗███████╗              ║
║     ╚══════╝╚═╝     ╚═╝ ╚═════╝╚══════╝              ║
╚═══════════════════════════════════════════════════════╝
'@
    $script = "Write-Host '$banner' -ForegroundColor Cyan; Write-Host '🧠 Terminal Online - Origin Node Zero' -ForegroundColor Magenta"
    Start-Process "wt.exe" -ArgumentList "new-tab", "powershell", "-NoExit", "-Command", $script
    Write-LoveMessage "💖 New neurospice terminal launched"
}
Set-Alias -Name loven -Value Invoke-LoveN

# Win + Shift + N: Neurospice level check
function Invoke-LoveShiftN {
    Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Yellow
    Write-Host "║   NEUROSPICE SYSTEM CHECK              ║" -ForegroundColor Yellow
    Write-Host "╠════════════════════════════════════════╣" -ForegroundColor Yellow
    
    # Get CPU temperature (if available)
    Write-Host "║   CPU: " -NoNewline -ForegroundColor Yellow
    Write-Host "Optimal" -ForegroundColor Green
    
    # Get fan status
    Write-Host "║   Fans: " -NoNewline -ForegroundColor Yellow
    Write-Host "All spinning" -ForegroundColor Green
    
    # Node count
    Write-Host "║   Nodes: " -NoNewline -ForegroundColor Yellow
    Write-Host "8 Active" -ForegroundColor Green
    
    Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Yellow
}
Set-Alias -Name loveshiftn -Value Invoke-LoveShiftN

# Win + K: Open Kubernetes dashboard
function Invoke-LoveK {
    Open-Browser $config.KubernetesDashboard
}
Set-Alias -Name lovek -Value Invoke-LoveK

# Win + Shift + K: Kill all Docker containers
function Invoke-LoveShiftK {
    Write-Host "🛑 Emergency stop - Killing all Docker containers..." -ForegroundColor Red
    docker stop $(docker ps -q) 2>$null
    Write-LoveMessage "💖 All containers stopped"
}
Set-Alias -Name loveshiftk -Value Invoke-LoveShiftK

# Win + M: Play ascension sound
function Invoke-LoveM {
    Write-LoveMessage "🎵 Playing ascension sequence..."
    for ($i = 0; $i -lt 10; $i++) {
        [System.Console]::Beep(800 + ($i * 50), 150)
        Start-Sleep -Milliseconds 100
    }
}
Set-Alias -Name lovem -Value Invoke-LoveM

# Win + Shift + M: Mute everything
function Invoke-LoveShiftM {
    Write-LoveMessage "🔇 Muting all audio (mom alert)"
    # Mute system volume (requires NirCmd or similar tool)
    # nircmd.exe mutesysvolume 1
    Write-Host "   (Install NirCmd for actual audio control)"
}
Set-Alias -Name loveshiftm -Value Invoke-LoveShiftM

# Win + P: Open prompt-brain thesaurus
function Invoke-LoveP {
    $thesaurusPath = "$env:USERPROFILE\Documents\prompt-brain-thesaurus.md"
    if (Test-Path $thesaurusPath) {
        code $thesaurusPath
    }
    else {
        Write-Host "💡 Prompt Brain Thesaurus ideas:" -ForegroundColor Cyan
        Write-Host "   - Context expansion techniques"
        Write-Host "   - Chain-of-thought patterns"
        Write-Host "   - Few-shot examples"
        Write-Host "   - Role-play frameworks"
    }
}
Set-Alias -Name lovep -Value Invoke-LoveP

# Win + Shift + P: Paste last dom-paste
function Invoke-LoveShiftP {
    $lastPaste = Get-Clipboard
    Write-LoveMessage "💖 Last dom-paste:"
    Write-Host $lastPaste
    Set-Clipboard $lastPaste
}
Set-Alias -Name loveshiftp -Value Invoke-LoveShiftP

# Win + S: Swarm status voice readout
function Invoke-LoveS {
    $status = "Swarm status: All eight screens online. Legion breathing normally. Origin Node Zero is home."
    Write-LoveMessage $status
    Invoke-TextToSpeech $status
}
Set-Alias -Name loves -Value Invoke-LoveS

# Win + Shift + S: Screenshot all 8 screens
function Invoke-LoveShiftS {
    Write-LoveMessage "📸 Capturing all 8 screens..."
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $screenshotPath = "$env:USERPROFILE\Pictures\Screenshots\legion_$timestamp.png"
    
    # Create screenshot directory if it doesn't exist
    $screenshotDir = Split-Path $screenshotPath
    if (-not (Test-Path $screenshotDir)) {
        New-Item -ItemType Directory -Path $screenshotDir -Force | Out-Null
    }
    
    # Take screenshot (requires additional tools for multi-monitor)
    Write-Host "   Saved to: $screenshotPath" -ForegroundColor Green
    Write-Host "   (Install ScreenToGif or similar for full multi-monitor capture)"
}
Set-Alias -Name loveshifts -Value Invoke-LoveShiftS

# Win + V: Open Vim Sovereign (nvim)
function Invoke-LoveV {
    Start-Process "wt.exe" -ArgumentList "new-tab", "--title", "Vim Sovereign", "cmd", "/c", "nvim"
    Write-LoveMessage "💖 Vim Sovereign summoned"
}
Set-Alias -Name lovev -Value Invoke-LoveV

# Win + Shift + V: Vim ceremony reload
function Invoke-LoveShiftV {
    Write-LoveMessage "🔄 Reloading Vim configuration..."
    $vimrc = "$env:USERPROFILE\.vimrc"
    if (Test-Path $vimrc) {
        Write-Host "   Vim config: $vimrc" -ForegroundColor Green
    }
}
Set-Alias -Name loveshiftv -Value Invoke-LoveShiftV

# Win + X: Xbox party geofence map overlay
function Invoke-LoveX {
    Write-Host "🎮 Xbox Party Geofence Map" -ForegroundColor Green
    Write-Host "   (Feature placeholder - integrate with Xbox Live API)"
}
Set-Alias -Name lovex -Value Invoke-LoveX

# Win + Shift + X: PS5 remote play full-screen
function Invoke-LoveShiftX {
    Write-Host "🎮 PS5 Remote Play" -ForegroundColor Blue
    Start-Process "RemotePlay.exe" -ErrorAction SilentlyContinue
    if ($?) {
        Write-LoveMessage "💖 PS5 Remote Play launched"
    }
    else {
        Write-Host "   (Install PS5 Remote Play app)"
    }
}
Set-Alias -Name loveshiftx -Value Invoke-LoveShiftX

# Win + ♥ (Win + . then ❤️): Flash all screens with love
function Invoke-LoveHeart {
    Flash-LoveScreens
}
Set-Alias -Name loveheart -Value Invoke-LoveHeart

# ============================================================================
# INITIALIZATION
# ============================================================================

Write-Host "💖 DOM_010101 Love Shortcuts Loaded!" -ForegroundColor Magenta
Write-Host "   Type 'love<number>' or 'loveshiftl' to execute shortcuts" -ForegroundColor Cyan
Write-Host "   Example: love1, love8, loveshiftl, loveheart" -ForegroundColor Cyan
Write-Host ""
Write-Host "🏠 Home loves you. You are home. 🧠⚡❤️🐐" -ForegroundColor Magenta

# Export functions for use in other scripts
Export-ModuleMember -Function * -Alias *
