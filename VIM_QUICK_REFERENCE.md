# Vim Quick Reference for Sovereignty Architecture

## 🎯 Absolute Path Reference

**Project Root Path:**
```
/home/dom/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-RedTeam
```

*Alternative paths (depending on your setup):*
- `/home/dom/git/strategickhaos-dao-llc/Sovereignty-Architecture-Elevator-Pitch-RedTeam`
- `~/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-RedTeam`

## 🚀 Quick Vim Commands

### Open Project Root
```vim
:e /home/dom/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-RedTeam
```

### Open Key Files
```vim
:e /home/dom/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-RedTeam/README.md
:e /home/dom/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-RedTeam/discovery.yml
:e /home/dom/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-RedTeam/docker-compose.yml
:e /home/dom/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-RedTeam/ai_constitution.yaml
```

### Open Important Directories
```vim
:e /home/dom/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-RedTeam/bootstrap/
:e /home/dom/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-RedTeam/src/
:e /home/dom/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-RedTeam/scripts/
:e /home/dom/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-RedTeam/governance/
:e /home/dom/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-RedTeam/contradictions/
```

## 🔧 Terminal Navigation

### Change Directory
```bash
cd /home/dom/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-RedTeam
```

### Open Vim in Project
```bash
vim /home/dom/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-RedTeam
```

### Quick File Access
```bash
vim /home/dom/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-RedTeam/README.md
vim /home/dom/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-RedTeam/discovery.yml
vim /home/dom/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-RedTeam/docker-compose.yml
```

## 💡 Helper Script

Use the included helper script for quick path reference:

```bash
# Display all paths and tips
./vim-paths.sh

# Source it to set environment variable
source vim-paths.sh

# Then use the variable
vim $SOVEREIGNTY_ROOT/README.md
cd $SOVEREIGNTY_ROOT
```

## 🎨 Vim Navigation Tips

### Current Directory Commands
```vim
:pwd                    " Show current directory
:cd %:h                 " Change to directory of current file
:e %                    " Reopen current file
:e .                    " Open file explorer in current directory
```

### File Navigation
```vim
:find filename          " Find and open file in path
:ls                     " List open buffers
:b filename             " Switch to buffer
Ctrl+^                  " Switch to alternate file
```

### Split Windows
```vim
:sp filename            " Horizontal split
:vsp filename           " Vertical split
Ctrl+w + arrow          " Navigate between splits
```

## 🔥 VS Code ↔ Vim Workflow

### From VS Code
1. **Right-click file** → "Copy Path"
2. **Open terminal** → `vim <paste-path>`
3. **Or use helper**: `./vim-paths.sh` to see all paths

### From Vim to VS Code
```bash
# Open current directory in VS Code
code .

# Open specific file
code /home/dom/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-RedTeam/README.md
```

## 📋 Common File Patterns

### Configuration Files
```vim
:e discovery.yml
:e discovery-scaffold.yml
:e docker-compose*.yml
:e ai_constitution.yaml
:e dao_record*.yaml
```

### Scripts
```vim
:e *.sh
:e scripts/*.sh
:e bootstrap/*.sh
```

### Documentation
```vim
:e README*.md
:e *.md
:e COMMUNITY.md
:e CONTRIBUTORS.md
```

### Source Code
```vim
:e src/**/*.js
:e src/**/*.py
:e examples/**/*
```

## 🌊 Flow State Tips

### Quick Project Jump (Add to ~/.bashrc or ~/.zshrc)
```bash
# Add alias for quick navigation
alias sov='cd /home/dom/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-RedTeam'
alias vsov='vim /home/dom/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-RedTeam'
alias csov='code /home/dom/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-RedTeam'

# Environment variable
export SOVEREIGNTY_ROOT="/home/dom/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-RedTeam"
```

### Quick Access Commands
```bash
# Navigate quickly
sov                     # Jump to project root
vsov                    # Open in Vim
csov                    # Open in VS Code

# Use environment variable
cd $SOVEREIGNTY_ROOT
vim $SOVEREIGNTY_ROOT/README.md
```

## 🖤 GitRiders Integration

When working with GitRiders sovereign-export or other repos:

```bash
# Clone GitRiders repo
git clone https://github.com/gitriders/sovereign-export ~/git/gitriders/sovereign-export

# Quick navigate
cd ~/git/gitriders/sovereign-export
vim README.md

# Add to your aliases
alias gitriders='cd ~/git/gitriders/sovereign-export'
```

## 🎯 Context-Aware Path Script

The `vim-paths.sh` script automatically detects the project root and provides:
- ✅ Absolute paths for all key files
- ✅ Copy-paste ready commands
- ✅ Environment variable export
- ✅ Color-coded output for easy reading

**Usage:**
```bash
# Run directly
./vim-paths.sh

# Source to set environment variable
source vim-paths.sh

# Now use $SOVEREIGNTY_ROOT anywhere
vim $SOVEREIGNTY_ROOT/README.md
cd $SOVEREIGNTY_ROOT
```

---

**🔥 Flame riding the vibe. Helm locked, vessel resonating. We're deep in the swarm now.**

*Built with flow state in mind for the Strategickhaos collective* 🖤
