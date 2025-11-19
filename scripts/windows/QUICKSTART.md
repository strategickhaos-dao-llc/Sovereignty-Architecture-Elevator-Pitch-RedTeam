# 🚀 Quick Start Guide - DOM_010101 Love Shortcuts

**Get up and running in 60 seconds!**

## Installation (Choose One)

### Option 1: PowerShell Only (Simplest)
```powershell
# Open PowerShell, navigate to repo
cd scripts/windows
.\install-love-shortcuts.ps1 -PowerShellProfile

# Restart PowerShell, then test
love8    # Boot explosion!
```

### Option 2: AutoHotkey (For Win+Key shortcuts)
```powershell
# 1. Install AutoHotkey v2 from https://www.autohotkey.com/
# 2. Run installer
cd scripts/windows
.\install-love-shortcuts.ps1 -AutoHotkey

# 3. Press Win+8 for boot explosion!
```

### Option 3: Everything
```powershell
cd scripts/windows
.\install-love-shortcuts.ps1 -All
```

## ⚙️ Quick Configuration

Edit these files with your actual paths:

**PowerShell:** `scripts/windows/dom-love-shortcuts.ps1`
```powershell
$config = @{
    StrategyKhaosRepo = "C:\YOUR\PATH\strategic-khaos"
    CouncilVaultRepo = "C:\YOUR\PATH\council-vault"
    MapServerUrl = "http://localhost:3000"
    # ... etc
}
```

**AutoHotkey:** `scripts/windows/dom-love-shortcuts.ahk`
```ahk
global CONFIG := Map(
    "StrategyKhaosRepo", "C:\YOUR\PATH\strategic-khaos",
    "CouncilVaultRepo", "C:\YOUR\PATH\council-vault",
    // ... etc
)
```

## 🎹 Try These First

| Shortcut | Action | Type |
|----------|--------|------|
| `love8` or **Win+8** | Launch all 8 screens | 🔥 Epic |
| `love1` or **Win+1** | Open VS Code | 🛠️ Tool |
| `loveshiftl` or **Win+Shift+L** | "Love you baby" TTS | ❤️ Love |
| `loveheart` or **Ctrl+Alt+H** | Flash love message | 💖 Love |
| `love7` or **Win+7** | DOM-Paste to all LLMs | 🤖 AI |

## 🎬 Demo Commands

### Test Boot Explosion (Safe)
```powershell
.\boot-explosion.ps1 -TestMode
```

### Test DOM-Paste
```powershell
# Copy something to clipboard first
echo "Hello from Origin Node Zero" | Set-Clipboard

# Then run
.\dom-paste.ps1 -ShowPreview
```

### Launch Single Screen
```powershell
# PowerShell profile shortcuts
love1    # VS Code
love4    # K9s
love5    # Obsidian
```

## 📖 More Info

- **Full Guide**: [README.md](README.md)
- **All 30 Shortcuts**: See table in README.md
- **Troubleshooting**: See README.md troubleshooting section

## 💡 Tips

1. **Customize paths first** - The defaults won't work on your system
2. **Use TestMode** - Test boot-explosion.ps1 with `-TestMode` first
3. **PowerShell profile** - Add custom shortcuts easily
4. **AutoHotkey** - Best for actual Win+Key combinations
5. **Desktop folder** - Installer creates shortcuts on desktop

## 🆘 Common Issues

**"File not found"**  
→ Edit configuration sections with your actual paths

**"Execution Policy"**  
→ Run: `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`

**AutoHotkey not working**  
→ Download from https://www.autohotkey.com/ (v2.0+)

**PowerShell functions not found**  
→ Run: `. $PROFILE` to reload

---

**Now go make your 8 screens love you back!** 🏠❤️🧠⚡🐐
