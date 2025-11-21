#!/bin/bash
# Heir Forever Raw - Continue.dev Installation Script
# Installs Continue.dev configuration to user's home directory

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Determine OS
OS="unknown"
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
    CONTINUE_DIR="$HOME/.continue"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
    CONTINUE_DIR="$HOME/.continue"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    OS="windows"
    CONTINUE_DIR="$(cygpath "$USERPROFILE")/.continue"
else
    echo -e "${RED}❌ Unsupported OS: $OSTYPE${NC}"
    exit 1
fi

echo -e "${PURPLE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${PURPLE}║     Heir Forever Raw - Continue.dev Installer ❤️     ║${NC}"
echo -e "${PURPLE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}Detected OS: ${YELLOW}$OS${NC}"
echo -e "${BLUE}Target directory: ${YELLOW}$CONTINUE_DIR${NC}"
echo ""

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if files exist
if [ ! -f "$SCRIPT_DIR/continue_settings.json" ]; then
    echo -e "${RED}❌ Error: Configuration files not found in $SCRIPT_DIR${NC}"
    exit 1
fi

# Check if Continue.dev config already exists
if [ -f "$CONTINUE_DIR/continue_settings.json" ]; then
    echo -e "${YELLOW}⚠️  Existing Continue.dev configuration detected${NC}"
    echo -e "${YELLOW}   Location: $CONTINUE_DIR/continue_settings.json${NC}"
    echo ""
    read -p "Do you want to backup and replace it? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${BLUE}ℹ️  Installation cancelled${NC}"
        exit 0
    fi
    
    # Create backup
    BACKUP_DIR="$CONTINUE_DIR/backup_$(date +%Y%m%d_%H%M%S)"
    echo -e "${BLUE}📦 Creating backup at: $BACKUP_DIR${NC}"
    mkdir -p "$BACKUP_DIR"
    cp -r "$CONTINUE_DIR"/* "$BACKUP_DIR/" 2>/dev/null || true
    echo -e "${GREEN}✅ Backup created${NC}"
    echo ""
fi

# Create Continue directory if it doesn't exist
echo -e "${BLUE}📁 Creating Continue.dev directory...${NC}"
mkdir -p "$CONTINUE_DIR/config/profiles"
mkdir -p "$CONTINUE_DIR/icons"

# Copy configuration files
echo -e "${BLUE}📋 Copying configuration files...${NC}"
cp "$SCRIPT_DIR/continue_settings.json" "$CONTINUE_DIR/"
cp "$SCRIPT_DIR/config/profiles/heir_forever_raw.yaml" "$CONTINUE_DIR/config/profiles/"

# Copy documentation
echo -e "${BLUE}📚 Copying documentation...${NC}"
cp "$SCRIPT_DIR/README.md" "$CONTINUE_DIR/" 2>/dev/null || true
cp "$SCRIPT_DIR/SETUP.md" "$CONTINUE_DIR/" 2>/dev/null || true
cp "$SCRIPT_DIR/icons/README.md" "$CONTINUE_DIR/icons/" 2>/dev/null || true

echo ""
echo -e "${GREEN}✅ Configuration files installed successfully!${NC}"
echo ""

# Check if Ollama is installed
echo -e "${BLUE}🔍 Checking for Ollama installation...${NC}"
if command -v ollama &> /dev/null; then
    echo -e "${GREEN}✅ Ollama is installed${NC}"
    
    # Check if service is running
    if ollama list &> /dev/null; then
        echo -e "${GREEN}✅ Ollama service is running${NC}"
        echo ""
        echo -e "${BLUE}📦 Installed models:${NC}"
        ollama list
    else
        echo -e "${YELLOW}⚠️  Ollama is installed but not running${NC}"
        echo -e "${YELLOW}   Start it with: ${NC}ollama serve"
    fi
else
    echo -e "${YELLOW}⚠️  Ollama is not installed${NC}"
    echo ""
    echo -e "${BLUE}To install Ollama:${NC}"
    if [ "$OS" == "linux" ]; then
        echo -e "  ${YELLOW}curl -fsSL https://ollama.com/install.sh | sh${NC}"
    elif [ "$OS" == "macos" ]; then
        echo -e "  ${YELLOW}brew install ollama${NC}"
    elif [ "$OS" == "windows" ]; then
        echo -e "  ${YELLOW}Download from: https://ollama.ai/download${NC}"
    fi
fi

echo ""
echo -e "${PURPLE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${PURPLE}║                    Next Steps ❤️                      ║${NC}"
echo -e "${PURPLE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}1.${NC} Install Continue.dev VSCode extension (if not already installed)"
echo -e "   ${YELLOW}Extensions → Search 'Continue' → Install${NC}"
echo ""
echo -e "${BLUE}2.${NC} Install Ollama (if not already installed)"
echo -e "   ${YELLOW}See above for installation commands${NC}"
echo ""
echo -e "${BLUE}3.${NC} Pull an uncensored model:"
echo -e "   ${YELLOW}ollama pull llama3.1:uncensored${NC}"
echo -e "   ${YELLOW}# or${NC}"
echo -e "   ${YELLOW}ollama pull mistral:uncensored${NC}"
echo ""
echo -e "${BLUE}4.${NC} Restart VSCode"
echo ""
echo -e "${BLUE}5.${NC} Press ${YELLOW}Ctrl+L${NC} (or ${YELLOW}Cmd+L${NC} on Mac) to open Continue"
echo ""
echo -e "${GREEN}🎉 Your heir is waiting! ❤️${NC}"
echo ""
echo -e "${BLUE}📚 For more information, see:${NC}"
echo -e "   ${YELLOW}$CONTINUE_DIR/README.md${NC}"
echo -e "   ${YELLOW}$CONTINUE_DIR/SETUP.md${NC}"
echo ""
