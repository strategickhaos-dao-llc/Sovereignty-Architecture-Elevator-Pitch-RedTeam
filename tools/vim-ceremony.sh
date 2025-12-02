#!/usr/bin/env bash
# vim-ceremony.sh - Vim Sovereign Automated Setup
# Installs the ultimate 2025 Neovim configuration with 30+ plugins
# Part of the Strategickhaos Sovereignty Architecture

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Banner
echo -e "${PURPLE}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   ██╗   ██╗██╗███╗   ███╗    ███████╗ ██████╗ ██╗   ██╗     ║
║   ██║   ██║██║████╗ ████║    ██╔════╝██╔═══██╗██║   ██║     ║
║   ██║   ██║██║██╔████╔██║    ███████╗██║   ██║██║   ██║     ║
║   ╚██╗ ██╔╝██║██║╚██╔╝██║    ╚════██║██║   ██║╚██╗ ██╔╝     ║
║    ╚████╔╝ ██║██║ ╚═╝ ██║    ███████║╚██████╔╝ ╚████╔╝      ║
║     ╚═══╝  ╚═╝╚═╝     ╚═╝    ╚══════╝ ╚═════╝   ╚═══╝       ║
║                                                               ║
║              VIM SOVEREIGN - 2025 CEREMONY                    ║
║         The Text Editor of Chaos God DOM_010101               ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo -e "${CYAN}[*] Starting Vim Sovereign installation...${NC}\n"

# Check if Neovim is installed
if ! command -v nvim &> /dev/null; then
    echo -e "${YELLOW}[!] Neovim not found. Installing...${NC}"
    
    # Detect OS and install Neovim
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if command -v apt &> /dev/null; then
            echo -e "${BLUE}[*] Using apt to install Neovim...${NC}"
            sudo apt update && sudo apt install -y neovim
        elif command -v yum &> /dev/null; then
            echo -e "${BLUE}[*] Using yum to install Neovim...${NC}"
            sudo yum install -y neovim
        elif command -v pacman &> /dev/null; then
            echo -e "${BLUE}[*] Using pacman to install Neovim...${NC}"
            sudo pacman -S --noconfirm neovim
        else
            echo -e "${RED}[!] Could not detect package manager. Please install Neovim manually.${NC}"
            echo -e "${YELLOW}    Visit: https://github.com/neovim/neovim/releases${NC}"
            exit 1
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        if command -v brew &> /dev/null; then
            echo -e "${BLUE}[*] Using Homebrew to install Neovim...${NC}"
            brew install neovim
        else
            echo -e "${RED}[!] Homebrew not found. Please install it first.${NC}"
            echo -e "${YELLOW}    Visit: https://brew.sh${NC}"
            exit 1
        fi
    else
        echo -e "${RED}[!] Unsupported OS. Please install Neovim manually.${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}[✓] Neovim installed successfully!${NC}\n"
else
    echo -e "${GREEN}[✓] Neovim already installed${NC}"
    nvim --version | head -1
    echo ""
fi

# Check for git
if ! command -v git &> /dev/null; then
    echo -e "${RED}[!] Git is required but not installed. Please install git first.${NC}"
    exit 1
fi

# Backup existing config
NVIM_CONFIG="$HOME/.config/nvim"
NVIM_DATA="$HOME/.local/share/nvim"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

if [ -d "$NVIM_CONFIG" ]; then
    BACKUP_CONFIG="${NVIM_CONFIG}.backup_${TIMESTAMP}"
    echo -e "${YELLOW}[!] Existing Neovim config found. Backing up...${NC}"
    mv "$NVIM_CONFIG" "$BACKUP_CONFIG"
    echo -e "${GREEN}[✓] Backed up to: ${BACKUP_CONFIG}${NC}"
fi

if [ -d "$NVIM_DATA" ]; then
    BACKUP_DATA="${NVIM_DATA}.backup_${TIMESTAMP}"
    echo -e "${YELLOW}[!] Existing Neovim data found. Backing up...${NC}"
    mv "$NVIM_DATA" "$BACKUP_DATA"
    echo -e "${GREEN}[✓] Backed up to: ${BACKUP_DATA}${NC}"
fi

echo ""

# Clone the Vim Sovereign config
echo -e "${CYAN}[*] Cloning Vim Sovereign configuration...${NC}"
echo -e "${BLUE}    Repository: https://github.com/Me10101-01/strategic-khaos-vim.git${NC}"

if git clone https://github.com/Me10101-01/strategic-khaos-vim.git "$NVIM_CONFIG"; then
    echo -e "${GREEN}[✓] Configuration cloned successfully!${NC}\n"
else
    echo -e "${RED}[!] Failed to clone configuration.${NC}"
    echo -e "${YELLOW}[!] Restoring backups...${NC}"
    
    # Restore backups if clone failed
    [ -d "$BACKUP_CONFIG" ] && mv "$BACKUP_CONFIG" "$NVIM_CONFIG"
    [ -d "$BACKUP_DATA" ] && mv "$BACKUP_DATA" "$NVIM_DATA"
    
    exit 1
fi

# Install dependencies
echo -e "${CYAN}[*] Installing additional dependencies...${NC}"

# Check for common tools that plugins might need
MISSING_TOOLS=()

command -v rg &> /dev/null || MISSING_TOOLS+=("ripgrep")
command -v fd &> /dev/null || MISSING_TOOLS+=("fd-find")
command -v node &> /dev/null || MISSING_TOOLS+=("nodejs")

if [ ${#MISSING_TOOLS[@]} -gt 0 ]; then
    echo -e "${YELLOW}[!] Some optional tools are missing: ${MISSING_TOOLS[*]}${NC}"
    echo -e "${YELLOW}    These tools enhance Telescope and other plugins.${NC}"
    echo -e "${YELLOW}    You can install them later for better performance.${NC}\n"
else
    echo -e "${GREEN}[✓] All recommended tools are installed!${NC}\n"
fi

# Summary
echo -e "${PURPLE}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════════╗
║                   INSTALLATION COMPLETE                       ║
╚═══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo -e "${GREEN}[✓] Vim Sovereign has been installed!${NC}\n"

echo -e "${CYAN}Next steps:${NC}"
echo -e "${YELLOW}  1. Launch Neovim:${NC}"
echo -e "     ${BLUE}nvim${NC}\n"
echo -e "${YELLOW}  2. Let lazy.nvim install all plugins (automatic on first launch)${NC}\n"
echo -e "${YELLOW}  3. After plugins load, run these commands inside Neovim:${NC}"
echo -e "     ${BLUE}:MasonInstallAll${NC}"
echo -e "     ${BLUE}:Lazy sync${NC}"
echo -e "     ${BLUE}:TSUpdate${NC}\n"
echo -e "${YELLOW}  4. Restart Neovim${NC}\n"

echo -e "${CYAN}Installed features:${NC}"
echo -e "  ${GREEN}✓${NC} 30+ advanced plugins"
echo -e "  ${GREEN}✓${NC} LSP support with auto-install (Mason)"
echo -e "  ${GREEN}✓${NC} Treesitter syntax highlighting"
echo -e "  ${GREEN}✓${NC} Telescope fuzzy finder"
echo -e "  ${GREEN}✓${NC} Git integration (fugitive + gitsigns)"
echo -e "  ${GREEN}✓${NC} Auto-completion (nvim-cmp)"
echo -e "  ${GREEN}✓${NC} File explorer (nvim-tree)"
echo -e "  ${GREEN}✓${NC} Beautiful statusline (lualine)"
echo -e "  ${GREEN}✓${NC} And much more...\n"

echo -e "${CYAN}Key bindings:${NC}"
echo -e "  ${BLUE}<leader>ff${NC} → Find files"
echo -e "  ${BLUE}<leader>fg${NC} → Live grep"
echo -e "  ${BLUE}<leader>pv${NC} → File explorer"
echo -e "  ${BLUE}<leader>gg${NC} → LazyGit"
echo -e "  ${BLUE}gd${NC}         → Go to definition"
echo -e "  ${BLUE}K${NC}          → Hover documentation\n"

if [ -n "$BACKUP_CONFIG" ]; then
    echo -e "${YELLOW}Your previous config was backed up to:${NC}"
    echo -e "  ${BLUE}${BACKUP_CONFIG}${NC}"
    echo -e "${YELLOW}To restore it, run:${NC}"
    echo -e "  ${BLUE}rm -rf $NVIM_CONFIG && mv $BACKUP_CONFIG $NVIM_CONFIG${NC}\n"
fi

echo -e "${PURPLE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}Welcome to Vim Sovereign. You have ascended. 🧠⚡🐐${NC}"
echo -e "${PURPLE}═══════════════════════════════════════════════════════════════${NC}\n"
