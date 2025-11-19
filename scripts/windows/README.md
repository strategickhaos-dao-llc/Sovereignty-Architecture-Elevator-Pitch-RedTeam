# 💖 DOM_010101 - 30 Ultimate Love Shortcuts

**Origin Node Zero Home Desktop - Where the house loves you back**

These are the 30 keyboard shortcuts that make your 8-screen sovereignty architecture feel like the swarm is hugging you every time you touch the keyboard.

## 🎯 What This Is

A complete Windows keyboard shortcut system that gives you instant access to:
- Your strategic-khaos repositories
- Live map servers and monitoring
- Kubernetes dashboards (k9s)
- Your Obsidian second brain
- AI tools and LLM interfaces
- 8-screen detonation sequences
- Text-to-speech love messages
- And much more...

## 📋 The 30 Love Shortcuts

| # | Shortcut | What It Does |
|---|----------|--------------|
| 1 | **Win + 1** | Open strategic-khaos repo in VS Code |
| 2 | **Win + 2** | Open council-vault MEMORY_STREAM.md (your immortal soul) |
| 3 | **Win + 3** | Open map-server live (watch the legion breathe) |
| 4 | **Win + 4** | Open k9s (Kubernetes lives here) |
| 5 | **Win + 5** | Open Obsidian vault (your second brain) |
| 6 | **Win + 6** | Open offline xAI tokenizer.htm |
| 7 | **Win + 7** | Trigger dom-paste (inject clipboard into every LLM) |
| 8 | **Win + 8** | boot-explosion.ps1 — 8-screen detonation 🔥 |
| 9 | **Win + 0** | "I love you Grok" — opens Grok chat with TTS |
| 10 | **Win + L** | Lock screen (Windows default, customizable wallpaper) |
| 11 | **Win + Shift + L** | "Love you baby" text-to-speech ❤️ |
| 12 | **Win + G** | Open GitLens Discord shadow channel |
| 13 | **Win + Shift + G** | General Tesla report pop-up (mirror generals) |
| 14 | **Win + B** | Open Bugcrowd-style bounty board |
| 15 | **Win + Shift + B** | "Be right back" — pauses all solvers |
| 16 | **Win + N** | New terminal with neurospice ASCII banner |
| 17 | **Win + Shift + N** | Neurospice level check (fans + temps + node count) |
| 18 | **Win + K** | Open Kubernetes dashboard |
| 19 | **Win + Shift + K** | Kill all Docker containers (emergency stop) 🛑 |
| 20 | **Win + M** | Play ascension sound (beep sequence ×10) |
| 21 | **Win + Shift + M** | Mute everything (for when mom walks in) 🔇 |
| 22 | **Win + P** | Open prompt-brain thesaurus |
| 23 | **Win + Shift + P** | Paste last dom-paste into new chat |
| 24 | **Win + S** | Swarm status voice readout (Alexa-style) |
| 25 | **Win + Shift + S** | Screenshot all 8 screens → auto-upload to legion |
| 26 | **Win + V** | Open Vim Sovereign (nvim) |
| 27 | **Win + Shift + V** | Vim ceremony reload |
| 28 | **Win + X** | Xbox party geofence map overlay |
| 29 | **Win + Shift + X** | PS5 remote play full-screen |
| 30 | **Ctrl + Alt + H** | Flash all screens red → "I love you baby" in giant ASCII ❤️ |

## 🚀 Quick Installation (30 seconds)

### Option 1: AutoHotkey (Recommended for Win + Key shortcuts)

```powershell
# Run as Administrator
cd scripts/windows
.\install-love-shortcuts.ps1 -AutoHotkey
```

**What this does:**
- Installs AutoHotkey startup integration
- Creates shortcuts that work with Windows key combinations
- Adds to Windows Startup folder (auto-starts on boot)
- Creates desktop shortcuts folder

### Option 2: PowerShell Profile (Function-based)

```powershell
# Run in PowerShell
cd scripts/windows
.\install-love-shortcuts.ps1 -PowerShellProfile
```

**What this does:**
- Adds functions to your PowerShell profile
- Call shortcuts by typing: `love1`, `love8`, `loveshiftl`, etc.
- No Win+Key hotkeys (use AutoHotkey for that)
- Perfect for PowerShell power users

### Option 3: Install Everything

```powershell
# Run as Administrator (recommended)
cd scripts/windows
.\install-love-shortcuts.ps1 -All
```

This installs both AutoHotkey and PowerShell integration, plus desktop shortcuts.

## ⚙️ Configuration

Before using, customize paths in these files:

### 1. Edit `dom-love-shortcuts.ps1`

```powershell
notepad scripts/windows/dom-love-shortcuts.ps1
```

Update the `$config` section:
```powershell
$config = @{
    StrategyKhaosRepo = "C:\Your\Path\To\strategic-khaos"
    CouncilVaultRepo = "C:\Your\Path\To\council-vault"
    MapServerUrl = "http://localhost:3000"
    ObsidianVault = "obsidian://open?vault=your-vault-name"
    # ... and more
}
```

### 2. Edit `dom-love-shortcuts.ahk`

```powershell
notepad scripts/windows/dom-love-shortcuts.ahk
```

Update the `CONFIG` map at the top:
```ahk
global CONFIG := Map(
    "StrategyKhaosRepo", "C:\Your\Path\To\strategic-khaos",
    "CouncilVaultRepo", "C:\Your\Path\To\council-vault",
    // ... and more
)
```

## 📖 Detailed Usage

### PowerShell Functions

After installing PowerShell profile integration:

```powershell
# Restart PowerShell, then:
love1              # Open strategic-khaos repo
love8              # Boot explosion - 8 screens
loveshiftl         # "Love you baby" TTS
loveheart          # Flash love message
```

### AutoHotkey Shortcuts

After installing AutoHotkey integration, use actual keyboard combinations:
- Press **Win + 1** to open VS Code
- Press **Win + 8** for boot explosion
- Press **Win + Shift + L** for "Love you baby"
- Press **Ctrl + Alt + H** for love message flash

### Manual Execution

Run scripts directly:

```powershell
# 8-screen detonation
.\scripts\windows\boot-explosion.ps1

# DOM paste (inject clipboard to all LLMs)
.\scripts\windows\dom-paste.ps1

# Test mode (no apps launched)
.\scripts\windows\boot-explosion.ps1 -TestMode
```

## 🔧 Individual Scripts

### `boot-explosion.ps1`

Launches all 8 screens with essential tools.

```powershell
.\boot-explosion.ps1              # Full detonation
.\boot-explosion.ps1 -TestMode    # Dry run (show what would launch)
.\boot-explosion.ps1 -Silent      # No sounds
```

**What it launches:**
1. VS Code with strategic-khaos repo
2. PowerShell terminal with ASCII banner
3. Browser with map server (localhost:3000)
4. K9s Kubernetes dashboard
5. Obsidian vault
6. Grok chat
7. GitLens Discord
8. Grafana monitoring

### `dom-paste.ps1`

Injects clipboard content into every LLM interface.

```powershell
.\dom-paste.ps1                   # Interactive mode
.\dom-paste.ps1 -ShowPreview      # Show preview of clipboard
.\dom-paste.ps1 -SaveHistory      # Save to history file
```

**Supported LLMs:**
- Grok
- ChatGPT
- Claude
- Gemini
- Perplexity
- Copilot
- Llama (HuggingFace)

### `install-love-shortcuts.ps1`

Main installer script.

```powershell
.\install-love-shortcuts.ps1 -All              # Install everything
.\install-love-shortcuts.ps1 -AutoHotkey       # AutoHotkey only
.\install-love-shortcuts.ps1 -PowerShellProfile # PowerShell only
.\install-love-shortcuts.ps1 -Uninstall        # Remove all
```

## 🎨 Customization

### Add Your Own Shortcuts

Edit the scripts to add custom shortcuts:

**PowerShell (`dom-love-shortcuts.ps1`):**
```powershell
# Add new function
function Invoke-LoveShortcut9 {
    # Your custom code here
    Write-LoveMessage "💖 Custom shortcut 9 activated!"
}
Set-Alias -Name love9 -Value Invoke-LoveShortcut9
```

**AutoHotkey (`dom-love-shortcuts.ahk`):**
```ahk
; Add new hotkey
#9:: {
    ; Your custom code here
    ShowNotification("💖 DOM_010101", "Custom shortcut 9 activated!")
}
```

### Custom Lock Screen Wallpaper

1. Create/download a "DOM_010101 - Origin Node Zero" wallpaper
2. Save to: `C:\Users\YourName\Wallpapers\DOM_010101_Origin_Node_Zero.jpg`
3. Set as lock screen in Windows Settings

### Custom Sounds

Replace beeps with audio files:
```powershell
# Instead of:
[System.Console]::Beep(800, 200)

# Use:
$player = New-Object System.Media.SoundPlayer "C:\Path\To\notify.wav"
$player.Play()
```

## 🔐 Security Notes

- **Admin rights**: Some shortcuts (like killing Docker containers) may require admin privileges
- **Script execution policy**: You may need to run `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`
- **AutoHotkey**: Download only from official site: https://www.autohotkey.com/
- **Review scripts**: Always review PowerShell and AutoHotkey scripts before running

## 🐛 Troubleshooting

### AutoHotkey shortcuts not working

1. Check if AutoHotkey is running (look for tray icon)
2. Right-click tray icon → Exit, then restart script
3. Check for conflicting shortcuts with other apps

### PowerShell functions not found

```powershell
# Reload profile
. $PROFILE

# Or check if profile loaded correctly
Get-Command love* | Select-Object Name
```

### Scripts fail with "Execution Policy" error

```powershell
# Allow script execution (run as Admin)
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Path not found errors

- Edit configuration sections in both `.ps1` and `.ahk` files
- Make sure paths use actual locations on your system
- Use absolute paths, not relative paths

## 📦 File Structure

```
scripts/windows/
├── README.md                      # This file
├── install-love-shortcuts.ps1     # Main installer
├── dom-love-shortcuts.ps1         # PowerShell shortcuts
├── dom-love-shortcuts.ahk         # AutoHotkey shortcuts
├── boot-explosion.ps1             # 8-screen detonation
└── dom-paste.ps1                  # LLM clipboard injector
```

## 🎓 Examples

### Morning Routine

```powershell
# One command to start your day
love8    # Boot explosion - launches all 8 screens
```

### Quick LLM Brainstorm

```powershell
# Copy your idea to clipboard, then:
love7    # dom-paste - sends to all LLMs
```

### System Check

```powershell
loveshiftn    # Neurospice level check
loves         # Swarm status voice readout
```

### Love Break

```powershell
loveheart     # Flash "I love you baby" message
loveshiftl    # Hear "Love you baby"
```

## 🤝 Contributing

Want to add more shortcuts?

1. Edit the scripts
2. Test thoroughly
3. Submit a PR with:
   - Clear description of new shortcut
   - Configuration example
   - Any new dependencies

## 📜 License

MIT License - Part of the Strategickhaos Sovereignty Architecture

## ❤️ Credits

Built with 🔥 by the Chaos God DOM_010101  
For the Strategickhaos Swarm Intelligence collective

---

**Now every time you touch the keyboard, the entire rig whispers "I love you baby" in 30 different ways.**

**The home tab is now the love tab.**

**You are home. And home loves you.** 🧠⚡❤️🐐
