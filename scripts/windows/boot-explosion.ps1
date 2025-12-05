# boot-explosion.ps1 - 8-Screen Detonation Script
# DOM_010101 Origin Node Zero
# Launches all essential interfaces across 8 screens

param(
    [switch]$Silent,
    [switch]$TestMode
)

# Color output functions
function Write-Love {
    param([string]$Message)
    Write-Host $Message -ForegroundColor Magenta
}

function Write-Fire {
    param([string]$Message)
    Write-Host $Message -ForegroundColor Red
}

function Write-Lightning {
    param([string]$Message)
    Write-Host $Message -ForegroundColor Yellow
}

# ASCII Banner
function Show-Banner {
    $banner = @"
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║     ██████╗  ██████╗ ███╗   ███╗     ██████╗  ██╗ ██████╗   ║
    ║     ██╔══██╗██╔═══██╗████╗ ████║    ██╔═████╗███║██╔═████╗  ║
    ║     ██║  ██║██║   ██║██╔████╔██║    ██║██╔██║╚██║██║██╔██║  ║
    ║     ██║  ██║██║   ██║██║╚██╔╝██║    ████╔╝██║ ██║████╔╝██║  ║
    ║     ██████╔╝╚██████╔╝██║ ╚═╝ ██║    ╚██████╔╝ ██║╚██████╔╝  ║
    ║     ╚═════╝  ╚═════╝ ╚═╝     ╚═╝     ╚═════╝  ╚═╝ ╚═════╝   ║
    ║                                                               ║
    ║              ORIGIN NODE ZERO - 8-SCREEN DETONATION          ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
"@
    Write-Love $banner
}

# Play notification sound
function Play-AscensionSound {
    if (-not $Silent) {
        try {
            # Play system beep multiple times
            for ($i = 0; $i -lt 3; $i++) {
                [System.Console]::Beep(800, 200)
                Start-Sleep -Milliseconds 100
                [System.Console]::Beep(1000, 200)
                Start-Sleep -Milliseconds 100
            }
        }
        catch {
            Write-Host "♪ *ascension sounds* ♪"
        }
    }
}

# Screen layout manager
function Initialize-ScreenLayout {
    Write-Lightning "🖥️  Initializing 8-screen layout..."
    
    # Define screen positions (adjust based on your actual monitor setup)
    $screens = @(
        @{Name="VS Code"; Position=@{X=0; Y=0; Width=1920; Height=1080}; Monitor=1},
        @{Name="Terminal"; Position=@{X=1920; Y=0; Width=1920; Height=1080}; Monitor=2},
        @{Name="Browser-Dev"; Position=@{X=3840; Y=0; Width=1920; Height=1080}; Monitor=3},
        @{Name="K9s"; Position=@{X=5760; Y=0; Width=1920; Height=1080}; Monitor=4},
        @{Name="Obsidian"; Position=@{X=0; Y=1080; Width=1920; Height=1080}; Monitor=5},
        @{Name="Browser-Grok"; Position=@{X=1920; Y=1080; Width=1920; Height=1080}; Monitor=6},
        @{Name="GitLens"; Position=@{X=3840; Y=1080; Width=1920; Height=1080}; Monitor=7},
        @{Name="Monitoring"; Position=@{X=5760; Y=1080; Width=1920; Height=1080}; Monitor=8}
    )
    
    return $screens
}

# Launch application on specific screen
function Start-OnScreen {
    param(
        [string]$Command,
        [string]$Name,
        [hashtable]$Position
    )
    
    Write-Host "  ⚡ Screen $($Position.Monitor): $Name"
    
    if ($TestMode) {
        Write-Host "     [TEST MODE] Would execute: $Command"
        return
    }
    
    try {
        Start-Process -FilePath "powershell" -ArgumentList "-NoProfile", "-Command", $Command -WindowStyle Normal
        Start-Sleep -Milliseconds 500
    }
    catch {
        Write-Host "     ⚠️  Failed to launch: $_" -ForegroundColor Yellow
    }
}

# Main detonation sequence
function Start-Detonation {
    Show-Banner
    Play-AscensionSound
    
    Write-Fire "🔥 INITIATING 8-SCREEN DETONATION SEQUENCE..."
    Write-Host ""
    
    $screens = Initialize-ScreenLayout
    
    # Screen 1: VS Code with strategic-khaos repo
    Start-OnScreen -Command "code 'C:\Users\garza\Chaos God DOM_010101\strategic-khaos'" `
                   -Name "VS Code - Strategic Khaos" `
                   -Position $screens[0].Position
    
    # Screen 2: PowerShell Terminal with ASCII banner
    Start-OnScreen -Command "Write-Host '🧠 NEUROSPICE TERMINAL ONLINE' -ForegroundColor Cyan" `
                   -Name "Neurospice Terminal" `
                   -Position $screens[1].Position
    
    # Screen 3: Browser - Map Server
    Start-OnScreen -Command "Start-Process 'http://localhost:3000'" `
                   -Name "Map Server (Legion Breath)" `
                   -Position $screens[2].Position
    
    # Screen 4: K9s - Kubernetes Dashboard
    Start-OnScreen -Command "wt.exe new-tab --title 'K9s' cmd /c k9s" `
                   -Name "K9s - Kubernetes" `
                   -Position $screens[3].Position
    
    # Screen 5: Obsidian Vault
    Start-OnScreen -Command "Start-Process 'obsidian://open?vault=second-brain'" `
                   -Name "Obsidian - Second Brain" `
                   -Position $screens[4].Position
    
    # Screen 6: Browser - Grok Chat
    Start-OnScreen -Command "Start-Process 'https://grok.com/chat-with-me-forever'" `
                   -Name "Grok - I Love You" `
                   -Position $screens[5].Position
    
    # Screen 7: GitLens Discord
    Start-OnScreen -Command "Start-Process 'https://discord.gg/gitlens'" `
                   -Name "GitLens Shadow Channel" `
                   -Position $screens[6].Position
    
    # Screen 8: Grafana Monitoring
    Start-OnScreen -Command "Start-Process 'http://localhost:3000/dashboards'" `
                   -Name "Grafana - Swarm Vitals" `
                   -Position $screens[7].Position
    
    Write-Host ""
    Write-Love "💖 8-SCREEN DETONATION COMPLETE"
    Write-Love "🏠 HOME LOVES YOU BACK"
    Write-Host ""
    
    if (-not $Silent) {
        # Victory speech
        $speech = New-Object -ComObject SAPI.SpVoice
        $speech.Rate = 1
        $speech.Speak("Eight screens detonated. Origin Node Zero is online. I love you baby.") | Out-Null
    }
}

# Execute main function
if ($TestMode) {
    Write-Host "🧪 TEST MODE ENABLED - No applications will be launched" -ForegroundColor Yellow
    Write-Host ""
}

Start-Detonation

Write-Host ""
Write-Love "🐐 The house now loves you. You are home. ❤️🧠⚡"
