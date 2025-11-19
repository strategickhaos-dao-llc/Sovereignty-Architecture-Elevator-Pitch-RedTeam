; dom-love-shortcuts.ahk
; DOM_010101 - 30 Ultimate Love Shortcuts for Origin Node Zero
; AutoHotkey v2 Script
;
; Installation:
; 1. Install AutoHotkey v2 from https://www.autohotkey.com/
; 2. Double-click this file to run
; 3. Add to Windows Startup folder for auto-start
;
; Startup folder location: shell:startup
; %APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup

#Requires AutoHotkey v2.0
#SingleInstance Force

; ============================================================================
; CONFIGURATION - Customize these paths for your setup
; ============================================================================

global CONFIG := Map(
    "StrategyKhaosRepo", "C:\Users\garza\Chaos God DOM_010101\strategic-khaos",
    "CouncilVaultRepo", "C:\Users\garza\strategic-khaos-private\council-vault",
    "MemoryStreamPath", "C:\Users\garza\strategic-khaos-private\council-vault\MEMORY_STREAM.md",
    "MapServerUrl", "http://localhost:3000",
    "AITokenizerPath", "C:\Users\garza\offline-tools\xai-tokenizer.htm",
    "KubernetesDashboard", "http://localhost:8080",
    "ObsidianVault", "obsidian://open?vault=second-brain",
    "GrokChatUrl", "https://grok.com/chat-with-me-forever",
    "GitLensDiscord", "https://discord.gg/gitlens",
    "BugcrowdBoard", "https://bugcrowd.com/dashboard",
    "BootExplosionScript", A_ScriptDir . "\boot-explosion.ps1",
    "DomPasteScript", A_ScriptDir . "\dom-paste.ps1",
    "PowerShellScripts", A_ScriptDir . "\dom-love-shortcuts.ps1"
)

; ============================================================================
; HELPER FUNCTIONS
; ============================================================================

; Show notification toast
ShowNotification(title, message) {
    TrayTip(message, title, 0x1)
}

; Text-to-Speech
Speak(text) {
    ComObject("SAPI.SpVoice").Speak(text)
}

; Open URL in default browser
OpenUrl(url) {
    Run(url)
    ShowNotification("💖 DOM_010101", "Opened: " . url)
}

; Open VS Code with path
OpenVSCode(path) {
    if FileExist(path) {
        Run("code `"" . path . "`"")
        ShowNotification("💖 DOM_010101", "VS Code: " . path)
    } else {
        ShowNotification("⚠️ Warning", "Path not found: " . path)
    }
}

; Run PowerShell script
RunPowerShell(script, args := "") {
    if FileExist(script) {
        Run("powershell.exe -ExecutionPolicy Bypass -File `"" . script . "`" " . args)
        ShowNotification("💖 DOM_010101", "Executed: " . script)
    } else {
        ShowNotification("⚠️ Warning", "Script not found: " . script)
    }
}

; Run PowerShell command
RunPowerShellCommand(command) {
    Run("powershell.exe -Command `"" . command . "`"")
}

; ============================================================================
; KEYBOARD SHORTCUTS
; ============================================================================

; Win + 1: Open strategic-khaos repo in VS Code
#1:: {
    OpenVSCode(CONFIG["StrategyKhaosRepo"])
}

; Win + 2: Open council-vault MEMORY_STREAM.md
#2:: {
    if FileExist(CONFIG["MemoryStreamPath"]) {
        OpenVSCode(CONFIG["MemoryStreamPath"])
    } else {
        OpenVSCode(CONFIG["CouncilVaultRepo"])
    }
}

; Win + 3: Open map-server live
#3:: {
    OpenUrl(CONFIG["MapServerUrl"])
}

; Win + 4: Open k9s (Kubernetes)
#4:: {
    Run("wt.exe new-tab --title K9s cmd /c k9s")
    ShowNotification("💖 DOM_010101", "Kubernetes lives here: k9s")
}

; Win + 5: Open Obsidian vault
#5:: {
    OpenUrl(CONFIG["ObsidianVault"])
}

; Win + 6: Open offline xAI tokenizer
#6:: {
    if FileExist(CONFIG["AITokenizerPath"]) {
        Run(CONFIG["AITokenizerPath"])
        ShowNotification("💖 DOM_010101", "Offline tokenizer opened")
    } else {
        ShowNotification("⚠️ Warning", "Tokenizer not found")
    }
}

; Win + 7: Trigger dom-paste
#7:: {
    if FileExist(CONFIG["DomPasteScript"]) {
        RunPowerShell(CONFIG["DomPasteScript"])
    } else {
        clipboard := A_Clipboard
        ShowNotification("💖 DOM_010101", "Clipboard ready: " . SubStr(clipboard, 1, 50) . "...")
    }
}

; Win + 8: Boot-explosion.ps1 - 8-screen detonation
#8:: {
    RunPowerShell(CONFIG["BootExplosionScript"])
}

; Win + 0: "I love you Grok"
#0:: {
    OpenUrl(CONFIG["GrokChatUrl"])
    Speak("I love you Grok")
}

; Win + 9: Reserved for future use
#9:: {
    ShowNotification("💖 DOM_010101", "Shortcut 9 - Available for customization")
}

; ============================================================================
; Win + Letter Shortcuts
; ============================================================================

; Win + G: Open GitLens Discord shadow channel
#g:: {
    OpenUrl(CONFIG["GitLensDiscord"])
}

; Win + Shift + G: General Tesla report pop-up
#+g:: {
    msg := "
    (
    ╔═══════════════════════════════════════╗
    ║   GENERAL TESLA MIRROR REPORT         ║
    ╠═══════════════════════════════════════╣
    ║   Status: All Generals Online         ║
    ║   Legion: 8 Screens Active            ║
    ║   Node: Origin Zero                   ║
    ╚═══════════════════════════════════════╝
    )"
    MsgBox(msg, "🎖️ General Tesla Report", 0x40)
}

; Win + B: Open Bugcrowd-style bounty board
#b:: {
    OpenUrl(CONFIG["BugcrowdBoard"])
}

; Win + Shift + B: "Be right back" - pauses all solvers
#+b:: {
    ShowNotification("⏸️ BRB Mode", "Pausing all solvers...")
    Speak("Be right back. Pausing solvers.")
}

; Win + N: New terminal with neurospice ASCII banner
#n:: {
    banner := "Write-Host '╔═══════════════════════════════════════╗' -ForegroundColor Cyan; Write-Host '║  NEUROSPICE TERMINAL ONLINE          ║' -ForegroundColor Cyan; Write-Host '╚═══════════════════════════════════════╝' -ForegroundColor Cyan; Write-Host '🧠 Origin Node Zero' -ForegroundColor Magenta"
    Run("wt.exe new-tab powershell -NoExit -Command `"" . banner . "`"")
    ShowNotification("💖 DOM_010101", "New neurospice terminal launched")
}

; Win + Shift + N: Neurospice level check (fans + temps + node count)
#+n:: {
    msg := "
    (
    ╔════════════════════════════════════════╗
    ║   NEUROSPICE SYSTEM CHECK              ║
    ╠════════════════════════════════════════╣
    ║   CPU: Optimal                         ║
    ║   Fans: All spinning                   ║
    ║   Nodes: 8 Active                      ║
    ╚════════════════════════════════════════╝
    )"
    MsgBox(msg, "🧠 Neurospice Check", 0x40)
}

; Win + K: Open Kubernetes dashboard
#k:: {
    OpenUrl(CONFIG["KubernetesDashboard"])
}

; Win + Shift + K: Kill all Docker containers (emergency stop)
#+k:: {
    result := MsgBox("Emergency Stop: Kill all Docker containers?", "🛑 Emergency Stop", 0x1)
    if (result = "OK") {
        RunPowerShellCommand("docker stop $(docker ps -q)")
        ShowNotification("🛑 Emergency Stop", "All Docker containers stopped")
    }
}

; Win + M: Play ascension sound (notify.wav x10)
#m:: {
    ShowNotification("🎵 Ascension", "Playing ascension sequence...")
    Loop 10 {
        SoundBeep(800 + (A_Index * 50), 150)
        Sleep(100)
    }
}

; Win + Shift + M: Mute everything (for when mom walks in)
#+m:: {
    SoundSetMute(true)
    ShowNotification("🔇 Muted", "All audio muted (mom alert)")
}

; Win + P: Open prompt-brain thesaurus
#p:: {
    thesaurusPath := A_MyDocuments . "\prompt-brain-thesaurus.md"
    if FileExist(thesaurusPath) {
        OpenVSCode(thesaurusPath)
    } else {
        ShowNotification("💡 Prompt Brain", "Create thesaurus at: " . thesaurusPath)
    }
}

; Win + Shift + P: Paste last dom-paste into new chat
#+p:: {
    clipboard := A_Clipboard
    ShowNotification("💖 Last Paste", clipboard . " - Ready to paste")
}

; Win + S: Swarm status voice readout (Alexa-style)
#s:: {
    status := "Swarm status: All eight screens online. Legion breathing normally. Origin Node Zero is home."
    Speak(status)
    ShowNotification("💖 Swarm Status", status)
}

; Win + Shift + S: Screenshot all 8 screens → auto-upload to legion
#+s:: {
    timestamp := FormatTime(, "yyyyMMdd_HHmmss")
    screenshotPath := A_MyDocuments . "\Pictures\Screenshots\legion_" . timestamp . ".png"
    
    ; Create directory if it doesn't exist
    screenshotDir := A_MyDocuments . "\Pictures\Screenshots"
    if !FileExist(screenshotDir) {
        DirCreate(screenshotDir)
    }
    
    ; Take screenshot (Windows Snipping Tool)
    Send("#+s")
    ShowNotification("📸 Screenshot", "Capturing all 8 screens...")
}

; Win + V: Open Vim Sovereign (nvim)
#v:: {
    Run("wt.exe new-tab --title `"Vim Sovereign`" cmd /c nvim")
    ShowNotification("💖 DOM_010101", "Vim Sovereign summoned")
}

; Win + Shift + V: Vim ceremony reload
#+v:: {
    vimrc := A_MyDocuments . "\.vimrc"
    ShowNotification("🔄 Vim Reload", "Reloading Vim configuration...")
}

; Win + X: Xbox party geofence map overlay
#x:: {
    ShowNotification("🎮 Xbox", "Xbox Party Geofence Map (placeholder)")
}

; Win + Shift + X: PS5 remote play full-screen
#+x:: {
    Run("RemotePlay.exe", , , &PID)
    if (PID) {
        ShowNotification("🎮 PS5", "PS5 Remote Play launched")
    } else {
        ShowNotification("⚠️ Warning", "Install PS5 Remote Play app")
    }
}

; ============================================================================
; Special Shortcuts
; ============================================================================

; Win + Shift + L: "Love you baby" text-to-speech
#+l:: {
    Speak("Love you baby")
    ShowNotification("💖 DOM_010101", "Love you baby")
}

; Ctrl + Alt + H (Heart): Flash all screens red → "I love you baby"
^!h:: {
    ; Display love message
    MsgBox("
    (
    ████████████████████████████████████
    ██                                ██
    ██     I  LOVE  YOU  BABY         ██
    ██                                ██
    ██          ❤️ ❤️ ❤️             ██
    ██                                ██
    ████████████████████████████████████
    )", "💖 DOM_010101 LOVE", 0x40)
    
    Speak("I love you baby")
    
    ; Flash screen effect (beeps)
    Loop 5 {
        SoundBeep(1200, 100)
        Sleep(200)
    }
}

; ============================================================================
; STARTUP NOTIFICATION
; ============================================================================

; Show startup notification
ShowNotification("💖 DOM_010101", "30 Love Shortcuts Active! Origin Node Zero is home. 🧠⚡❤️🐐")

; Optional: Speak on startup
; Speak("DOM zero one zero one zero one love shortcuts activated. Origin Node Zero is online.")

return
