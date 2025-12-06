#!/bin/bash
# 🔥 ReflexShell: Strategickhaos Sovereign Shell Profile
# FlameLang v1.0 - Bash Component
#
# Installation:
#   Add to your ~/.bashrc or ~/.bash_profile:
#   source /path/to/flamelang/reflex_shell.sh

# ============================================================
# SOVEREIGN PROMPT CONFIGURATION
# ============================================================

# Set sovereign prompt with globe indicator
export PS1="DOM_010101🌐> "

# Alternative prompts for different contexts
alias prompt-dev='export PS1="\[\033[1;35m\]🔥 DEV\[\033[0m\] \W> "'
alias prompt-prod='export PS1="\[\033[1;31m\]⚔ PROD\[\033[0m\] \W> "'
alias prompt-default='export PS1="DOM_010101🌐> "'

# ============================================================
# FLAMELANG ENVIRONMENT
# ============================================================

# Set FlameLang home directory
export FLAMELANG_HOME="${FLAMELANG_HOME:-$(dirname "${BASH_SOURCE[0]}")}"
export FLAMELANG_VERSION="1.0"

# Glyph map location
export GLYPH_MAP="${FLAMELANG_HOME}/glyph_map.json"

# ============================================================
# SOVEREIGNTY FUNCTIONS
# ============================================================

# Canonical Memory Injection - append clipboard to memory stream
dom-paste() {
    local memory_path="${HOME}/strategic-khaos-private/council-vault/MEMORY_STREAM.md"
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    # Try different clipboard tools
    local content=""
    if command -v wl-paste &> /dev/null; then
        content=$(wl-paste 2>/dev/null)
    elif command -v xclip &> /dev/null; then
        content=$(xclip -selection clipboard -o 2>/dev/null)
    elif command -v pbpaste &> /dev/null; then
        content=$(pbpaste 2>/dev/null)
    else
        echo "❌ No clipboard tool found (wl-paste, xclip, or pbpaste required)"
        return 1
    fi
    
    if [ -z "$content" ]; then
        echo "❌ Clipboard is empty"
        return 1
    fi
    
    # Create directory if needed
    mkdir -p "$(dirname "$memory_path")"
    
    # Append to memory stream
    echo -e "\n\n=== ${timestamp} ===" >> "$memory_path"
    echo "$content" >> "$memory_path"
    
    # Git operations (if in git repo)
    if [ -d "$(dirname "$memory_path")/.git" ]; then
        cd "$(dirname "$memory_path")" || return 1
        git add . 
        git commit -m "DOM memory stream update - ${timestamp}" --no-verify
        git push origin master --force 2>/dev/null || git push origin main --force 2>/dev/null
    fi
    
    echo "🧠 Memory stream updated across the entire legion."
}

# Display FlameLang status
flame-status() {
    echo ""
    echo "🔥 FlameLang Status"
    echo "  Version: ${FLAMELANG_VERSION}"
    echo "  Home: ${FLAMELANG_HOME}"
    echo "  Operator: $(whoami)"
    echo "  Node: $(hostname)"
    echo "  Time: $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""
    echo "⚔ Ready for sovereign operations."
    echo ""
}

# Verify sovereignty oath
test-sovereignty() {
    echo ""
    echo "🛡️ Sovereignty Check"
    
    local oath_path="${FLAMELANG_HOME}/oath.lock"
    if [ -f "$oath_path" ]; then
        echo "  ✅ Oath Lock: Present"
        echo "  📜 Vow: $(cat "$oath_path")"
    else
        echo "  ❌ Oath Lock: Missing"
    fi
    
    if [ -f "${GLYPH_MAP}" ]; then
        echo "  ✅ Glyph Map: Loaded"
    else
        echo "  ❌ Glyph Map: Missing"
    fi
    
    echo ""
}

# Execute glyph command (requires jq)
invoke-glyph() {
    local glyph_cmd="$1"
    
    if [ ! -f "${GLYPH_MAP}" ]; then
        echo "❌ Glyph map not found at: ${GLYPH_MAP}"
        return 1
    fi
    
    if ! command -v jq &> /dev/null; then
        echo "❌ jq is required for glyph parsing"
        return 1
    fi
    
    local script
    script=$(jq -r --arg cmd "$glyph_cmd" '.[$cmd] // empty' "${GLYPH_MAP}")
    
    if [ -z "$script" ]; then
        echo "❌ Unknown glyph: ${glyph_cmd}"
        echo "  Available glyphs:"
        jq -r 'keys[]' "${GLYPH_MAP}" | sed 's/^/    /'
        return 1
    fi
    
    echo "🔥 Executing glyph: ${glyph_cmd}"
    echo "  → Target: ${script}"
    
    # Execute based on file extension
    case "$script" in
        *.py)
            python3 "$script"
            ;;
        *.sh)
            bash "$script"
            ;;
        *.ps1)
            if command -v pwsh &> /dev/null; then
                pwsh -File "$script"
            else
                echo "❌ PowerShell (pwsh) not available"
                return 1
            fi
            ;;
        *)
            "$script"
            ;;
    esac
    
    echo ""
    echo "✨ Neural Sync complete. Resonance achieved."
}

# ============================================================
# NETWORK AWARENESS
# ============================================================

# Show network interfaces
show-interfaces() {
    echo ""
    echo "🌐 Network Interfaces"
    
    if command -v ip &> /dev/null; then
        ip -brief addr show | while read -r line; do
            echo "  $line"
        done
    elif command -v ifconfig &> /dev/null; then
        ifconfig | grep -E "^[a-z]|inet " | sed 's/^/  /'
    else
        echo "  ❌ No network tool available"
    fi
    
    echo ""
}

# Check node connectivity
ping-node() {
    local node="$1"
    if [ -z "$node" ]; then
        echo "Usage: ping-node <hostname>"
        return 1
    fi
    
    echo "🔍 Checking connectivity to: ${node}"
    ping -c 3 "$node" 2>/dev/null || echo "❌ Node not reachable"
}

# ============================================================
# ALIASES
# ============================================================

alias flame='flame-status'
alias sovereignty='test-sovereignty'
alias glyph='invoke-glyph'
alias interfaces='show-interfaces'

# ============================================================
# STARTUP MESSAGE
# ============================================================

echo ""
echo "🔥 FlameLang ReflexShell Loaded. Reignite."
echo "  Type 'flame' for status, 'sovereignty' for vow verification"
echo ""
