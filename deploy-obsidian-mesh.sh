#!/bin/bash
# Obsidian Neural Mesh Deployment Script
# Genesis Lock: Increment 3449 | Architect: 1067614449693569044
#
# This script sets up the Obsidian Neural Mesh system for
# sovereign knowledge graph management.

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
ORANGE='\033[0;33m'
NC='\033[0m' # No Color

# Genesis constants
GENESIS_INCREMENT=3449
ARCHITECT_SNOWFLAKE=1067614449693569044

# Default paths
DEFAULT_VAULT_PATH="/vault/legions-of-minds"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

echo -e "${ORANGE}🟠 OBSIDIAN NEURAL MESH DEPLOYMENT${NC}"
echo -e "${ORANGE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "Genesis Lock: Increment ${GENESIS_INCREMENT}"
echo -e "Architect: ${ARCHITECT_SNOWFLAKE}"
echo ""

# Function to print status
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Parse arguments
VAULT_PATH="${OBSIDIAN_VAULT_PATH:-$DEFAULT_VAULT_PATH}"
SKIP_VAULT=false
SKIP_GIT=false
SKIP_BOT=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --vault-path)
            VAULT_PATH="$2"
            shift 2
            ;;
        --skip-vault)
            SKIP_VAULT=true
            shift
            ;;
        --skip-git)
            SKIP_GIT=true
            shift
            ;;
        --skip-bot)
            SKIP_BOT=true
            shift
            ;;
        --help)
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  --vault-path PATH    Set Obsidian vault path (default: /vault/legions-of-minds)"
            echo "  --skip-vault         Skip vault directory creation"
            echo "  --skip-git           Skip Git initialization"
            echo "  --skip-bot           Skip Discord bot setup"
            echo "  --help               Show this help message"
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            exit 1
            ;;
    esac
done

echo "Configuration:"
echo "  Vault Path: $VAULT_PATH"
echo "  Repository: $REPO_ROOT"
echo ""

# Step 1: Create Obsidian vault structure
if [ "$SKIP_VAULT" = false ]; then
    echo -e "${ORANGE}Step 1: Creating Obsidian vault structure...${NC}"
    
    # Create main directories
    mkdir -p "$VAULT_PATH"/{brains,sandboxes,templates,api,licenses,mcp-tools,code,board-receipts}
    print_status "Created main vault directories"
    
    # Create department brain directories
    for dept in athena lyra nova ipower; do
        mkdir -p "$VAULT_PATH/brains/$dept"
        mkdir -p "$VAULT_PATH/sandboxes/$dept"
        
        # Create METHODOLOGY.md if it doesn't exist
        if [ ! -f "$VAULT_PATH/brains/$dept/METHODOLOGY.md" ]; then
            cat > "$VAULT_PATH/brains/$dept/METHODOLOGY.md" << EOF
---
type: methodology
department: $dept
genesis_increment: ${GENESIS_INCREMENT}
tags:
  - #$dept
  - #methodology
  - #genesis
---

# ${dept^} Department Methodology

## Overview
This document defines the methodology and operational procedures for the ${dept^} department.

## Core Principles
1. Sovereign knowledge management
2. Genesis-locked provenance
3. Collaborative intelligence

## Current Objectives
- [ ] Define department scope
- [ ] Establish workflow processes
- [ ] Document standard procedures

## Process Documentation
*To be completed*

## Quality Standards
*To be completed*

## Review Schedule
- Weekly methodology review
- Monthly alignment check
- Quarterly deep review

---
*Genesis Lock: Increment ${GENESIS_INCREMENT}*
*Last Updated: $(date -Iseconds)*
EOF
            print_status "Created $dept/METHODOLOGY.md"
        fi
    done
    
    # Create template files
    if [ ! -f "$VAULT_PATH/templates/brain-note.md" ]; then
        cat > "$VAULT_PATH/templates/brain-note.md" << 'EOF'
---
type: brain-note
department: "{{department}}"
created: "{{date}}"
genesis_increment: 3449
tags:
  - "#{{department}}"
  - "#brain-note"
---

# {{title}}

## Summary


## Details


## Related Notes
```dataview
LIST
FROM #{{department}}
WHERE file.name != this.file.name
LIMIT 5
```

---
*Genesis Lock: Increment 3449*
EOF
        print_status "Created brain-note template"
    fi
    
    # Copy board receipt template
    if [ -f "$REPO_ROOT/templates/board-receipts/base-receipt.md" ]; then
        cp "$REPO_ROOT/templates/board-receipts/base-receipt.md" \
           "$VAULT_PATH/templates/board-receipt-template.md"
        print_status "Copied board receipt template"
    fi
    
    echo ""
fi

# Step 2: Initialize Git repository
if [ "$SKIP_GIT" = false ]; then
    echo -e "${ORANGE}Step 2: Initializing Git repository...${NC}"
    
    cd "$VAULT_PATH"
    
    if [ ! -d ".git" ]; then
        git init
        print_status "Initialized Git repository"
        
        # Create .gitignore
        cat > .gitignore << 'EOF'
# Obsidian
.obsidian/workspace.json
.obsidian/workspace-mobile.json
.obsidian/plugins/*/data.json
.trash/
.DS_Store

# System
*.swp
*.swo
*~
.nfs*
Thumbs.db
EOF
        print_status "Created .gitignore"
        
        # Initial commit
        git add .
        git commit -m "🟠 Initial vault setup | Increment ${GENESIS_INCREMENT}"
        print_status "Created initial commit"
    else
        print_warning "Git repository already exists"
    fi
    
    # Add remote if GITHUB_REPO is set
    if [ -n "$GITHUB_REPO" ]; then
        if ! git remote get-url origin &>/dev/null; then
            git remote add origin "$GITHUB_REPO"
            print_status "Added remote origin: $GITHUB_REPO"
        fi
    else
        print_warning "GITHUB_REPO not set, skipping remote setup"
        echo "  Set GITHUB_REPO environment variable to configure remote"
    fi
    
    cd - > /dev/null
    echo ""
fi

# Step 3: Set up Discord bot
if [ "$SKIP_BOT" = false ]; then
    echo -e "${ORANGE}Step 3: Setting up Discord bot...${NC}"
    
    cd "$REPO_ROOT"
    
    # Check for Python
    if command -v python3 &>/dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &>/dev/null; then
        PYTHON_CMD="python"
    else
        print_error "Python not found. Please install Python 3.8+"
        exit 1
    fi
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        $PYTHON_CMD -m venv venv
        print_status "Created Python virtual environment"
    fi
    
    # Activate virtual environment and install dependencies
    source venv/bin/activate
    
    pip install --quiet discord.py pyyaml aiohttp
    print_status "Installed Python dependencies"
    
    deactivate
    
    # Check for Discord token
    if [ -z "$DISCORD_TOKEN" ]; then
        print_warning "DISCORD_TOKEN not set"
        echo "  Set DISCORD_TOKEN environment variable before running the bot"
    else
        print_status "DISCORD_TOKEN is configured"
    fi
    
    echo ""
fi

# Step 4: Create Obsidian configuration
echo -e "${ORANGE}Step 4: Creating Obsidian configuration...${NC}"

OBSIDIAN_CONFIG_DIR="$VAULT_PATH/.obsidian"
mkdir -p "$OBSIDIAN_CONFIG_DIR"

# Create app.json with recommended settings
if [ ! -f "$OBSIDIAN_CONFIG_DIR/app.json" ]; then
    cat > "$OBSIDIAN_CONFIG_DIR/app.json" << 'EOF'
{
  "legacyEditor": false,
  "strictLineBreaks": false,
  "showFrontmatter": true,
  "readableLineLength": true,
  "defaultViewMode": "preview",
  "livePreview": true,
  "showLineNumber": true
}
EOF
    print_status "Created Obsidian app.json"
fi

# Create graph.json with color groups
if [ ! -f "$OBSIDIAN_CONFIG_DIR/graph.json" ]; then
    cat > "$OBSIDIAN_CONFIG_DIR/graph.json" << 'EOF'
{
  "collapse-filter": false,
  "search": "",
  "showTags": true,
  "showAttachments": false,
  "hideUnresolved": false,
  "showOrphans": true,
  "collapse-color-groups": false,
  "colorGroups": [
    {
      "query": "tag:#athena",
      "color": {
        "a": 1,
        "rgb": 16729344
      }
    },
    {
      "query": "tag:#lyra",
      "color": {
        "a": 1,
        "rgb": 53199
      }
    },
    {
      "query": "tag:#nova",
      "color": {
        "a": 1,
        "rgb": 9699539
      }
    },
    {
      "query": "tag:#ipower",
      "color": {
        "a": 1,
        "rgb": 16766720
      }
    },
    {
      "query": "tag:#genesis",
      "color": {
        "a": 1,
        "rgb": 16777215
      }
    },
    {
      "query": "tag:#methodology",
      "color": {
        "a": 1,
        "rgb": 65280
      }
    }
  ],
  "collapse-display": false,
  "showArrow": true,
  "textFadeMultiplier": 0,
  "nodeSizeMultiplier": 1,
  "lineSizeMultiplier": 1,
  "collapse-forces": false,
  "centerStrength": 0.518713248970312,
  "repelStrength": 10,
  "linkStrength": 1,
  "linkDistance": 250,
  "scale": 1,
  "close": false
}
EOF
    print_status "Created Obsidian graph.json with department colors"
fi

# Create community-plugins.json
if [ ! -f "$OBSIDIAN_CONFIG_DIR/community-plugins.json" ]; then
    cat > "$OBSIDIAN_CONFIG_DIR/community-plugins.json" << 'EOF'
[
  "dataview",
  "obsidian-git",
  "templater-obsidian",
  "quickadd"
]
EOF
    print_status "Created community-plugins.json (install plugins in Obsidian)"
fi

echo ""

# Summary
echo -e "${ORANGE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✓ Obsidian Neural Mesh deployment complete!${NC}"
echo ""
echo "Next steps:"
echo "  1. Open Obsidian and select vault: $VAULT_PATH"
echo "  2. Install community plugins: Dataview, Obsidian Git, Templater, QuickAdd"
echo "  3. Configure Obsidian Git plugin for auto-commit"
echo "  4. Set environment variables:"
echo "     export DISCORD_TOKEN=\"your_token_here\""
echo "     export OBSIDIAN_VAULT_PATH=\"$VAULT_PATH\""
echo "  5. Run the Discord bot:"
echo "     cd $REPO_ROOT"
echo "     source venv/bin/activate"
echo "     python scripts/obsidian_bot.py"
echo ""
echo "Discord commands available:"
echo "  !receipt [department]  - Generate board receipt"
echo "  !brain [department]    - Show brain state"
echo "  !sync                  - Force Git sync"
echo "  !archive [query]       - Search vault"
echo "  !health                - Show mesh health"
echo "  !departments           - List all departments"
echo ""
echo -e "${ORANGE}Genesis Lock: Increment ${GENESIS_INCREMENT}${NC}"
