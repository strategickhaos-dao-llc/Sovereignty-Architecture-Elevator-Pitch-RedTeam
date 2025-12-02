# Strategickhaos Tools

This directory contains automation tools and utilities for the Sovereignty Architecture ecosystem.

## Vim Sovereign Ceremony

Automated installation scripts for the ultimate 2025 Neovim configuration.

### Files

- **`vim-ceremony.sh`** - Bash installation script (Linux/macOS/WSL)
- **`vim-ceremony.ps1`** - PowerShell installation script (Windows)

### Quick Install

**Linux/macOS/WSL:**
```bash
curl -sSL https://raw.githubusercontent.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-/main/tools/vim-ceremony.sh | bash
```

**Windows PowerShell:**
```powershell
iwr -useb https://raw.githubusercontent.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-/main/tools/vim-ceremony.ps1 | iex
```

### Local Execution

You can also run the scripts directly from this repository:

**Bash:**
```bash
cd tools
./vim-ceremony.sh
```

**PowerShell:**
```powershell
cd tools
.\vim-ceremony.ps1
```

### What It Does

1. **Detects and installs Neovim** if not already present
2. **Backs up existing configuration** with timestamp
3. **Clones the Vim Sovereign config** from the strategic-khaos-vim repository
4. **Checks for optional dependencies** (ripgrep, fd, nodejs)
5. **Provides post-install instructions** for finalizing the setup

### Requirements

**Required:**
- Git
- Internet connection

**Installed automatically:**
- Neovim (if not present)

**Recommended (optional):**
- ripgrep - Faster grep for Telescope
- fd - Faster file finding
- Node.js - LSP support
- lazygit - Git TUI integration

### Documentation

For full documentation, keybindings, customization, and troubleshooting, see:

**📖 [VIM_SOVEREIGN_SETUP.md](../VIM_SOVEREIGN_SETUP.md)**

---

*Part of the Strategickhaos Sovereignty Architecture - Digital enlightenment through automation* 🧠⚡🐐
