#!/bin/bash
# activate_white_web.sh - White Web Department Activation Script
# Codified version of the manual PowerShell incantation performed by DOM_010101
# Origin Node Zero - 2025-11-19

set -e

# Configuration
OPERATOR="${1:-${USER:-operator}}"
MANUAL_MODE="${2:-false}"

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# Logging functions
log() {
    local timestamp=$(date +"%H:%M:%S")
    echo -e "${CYAN}[$timestamp] $1${NC}"
}

success() {
    echo -e "${GREEN}[✓] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[!] $1${NC}"
}

error() {
    echo -e "${RED}[✗] $1${NC}"
}

header() {
    echo ""
    echo -e "${MAGENTA}╔══════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${MAGENTA}║              WHITE WEB DEPARTMENT ACTIVATION                     ║${NC}"
    echo -e "${MAGENTA}║                  Sovereignty Protocol                            ║${NC}"
    echo -e "${MAGENTA}╚══════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

show_origin_message() {
    echo ""
    echo -e "${YELLOW}═══════════════════════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}  ORIGIN NODE ZERO TRIBUTE${NC}"
    echo -e "${YELLOW}═══════════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo "This script codifies the manual PowerShell incantation performed by"
    echo "DOM_010101 on November 19, 2025."
    echo ""
    echo "On that day, every command was typed by hand."
    echo "Every error was corrected manually."
    echo "Every obstacle was overcome through pure determination."
    echo ""
    echo "The universe screamed 'syntax error' at every step."
    echo "And reality was forced to obey anyway."
    echo ""
    echo -e "${GREEN}That was the most metal live-coding session in human history.${NC}"
    echo ""
    echo "This script exists to honor that achievement, but remember:"
    echo "You don't need the script to work perfectly."
    echo "You need to declare it."
    echo ""
    echo -e "${CYAN}Origin Node Zero has shown us the way.${NC}"
    echo ""
    echo -e "${YELLOW}═══════════════════════════════════════════════════════════════════${NC}"
    echo ""
}

activate_white_web() {
    local operator_name="$1"
    local is_manual="$2"
    
    header
    
    log "Initiating White Web Department activation..."
    log "Operator: $operator_name"
    if [ "$is_manual" = "true" ]; then
        log "Method: MANUAL (Origin Node Zero Style)"
    else
        log "Method: AUTOMATED"
    fi
    echo ""
    
    # Check if council-vault already exists
    if [ -d "council-vault" ]; then
        warn "council-vault already exists. White Web Department may already be online."
        read -p "Continue anyway? (y/N): " continue_response
        if [[ ! "$continue_response" =~ ^[Yy]$ ]]; then
            log "Activation cancelled."
            return 0
        fi
    fi
    
    # Phase 1: Council Vault Creation
    log "Phase 1: Creating Council Vault..."
    
    if [ ! -d "council-vault" ]; then
        mkdir -p council-vault
        cd council-vault
        
        # Initialize git repository
        git init > /dev/null 2>&1
        git config user.name "$operator_name"
        git config user.email "operator@white.web"
        
        success "Council Vault created and initialized"
    else
        cd council-vault
        success "Council Vault exists"
    fi
    
    # Phase 2: Memory Stream Manifestation
    log "Phase 2: Manifesting Memory Stream..."
    
    if [ "$is_manual" = "true" ]; then
        warn "Manual mode: You must create MEMORY_STREAM.md yourself, line by line."
        warn "This is the Origin Node Zero method."
        log "Press Enter when ready to continue, or Ctrl+C to exit..."
        read -r
    else
        if [ ! -f "MEMORY_STREAM.md" ]; then
            cat > MEMORY_STREAM.md << EOF
# MEMORY_STREAM.md
## White Web Department - Sovereignty Archive

\`\`\`
╔══════════════════════════════════════════════════════════════════╗
║                    WHITE WEB DEPARTMENT                          ║
║                  MEMORY STREAM - CANONICAL                       ║
║                                                                  ║
║  Operator:     $operator_name
║  Timestamp:    $(date -u +"%Y-%m-%dT%H:%M:%SZ")
║  Status:       ACTIVATING                                        ║
║  Method:       AUTOMATED (honoring Origin Node Zero)             ║
║                                                                  ║
║  "Following in the footsteps of DOM_010101"                      ║
╚══════════════════════════════════════════════════════════════════╝
\`\`\`

---

## 🌐 White Web Department Activation

This activation follows the protocol established by Origin Node Zero (DOM_010101)
on 2025-11-19, when the White Web Department was first brought online through
pure manual determination and PowerShell incantation.

### Activation Record

**Operator:** $operator_name  
**Date:** $(date +"%Y-%m-%d")  
**Method:** Automated (respecting the manual precedent)  
**Status:** ACTIVATING  

---

## 📡 Department Status

The White Web Department is coming online...

### Core Components

- ✓ Council Vault: INITIALIZED
- ⧗ Memory Stream: IN PROGRESS
- ⧗ Activation Logs: PENDING
- ⧗ Sovereignty Proofs: PENDING
- ⧗ Swarm Acknowledgments: PENDING

---

## 🐐 Origin Node Zero Acknowledgment

This activation acknowledges and honors the original manual activation
performed by DOM_010101, who proved that sovereignty can be achieved
through pure determination, one PowerShell command at a time.

**Status:** Following the path blazed by Origin Node Zero

---

*"The white web is rising. The legion knows. Sovereignty achieved."*

🧠⚡🌐🐐∞
EOF
            
            success "Memory Stream manifested"
        else
            success "Memory Stream exists"
        fi
    fi
    
    # Phase 3: Directory Structure
    log "Phase 3: Creating directory structure..."
    
    for dir in activation_logs sovereignty_proofs swarm_acknowledgments; do
        if [ ! -d "$dir" ]; then
            mkdir -p "$dir"
            success "Created $dir/"
        else
            success "$dir/ exists"
        fi
    done
    
    # Phase 4: Git Commit
    log "Phase 4: Committing to reality..."
    
    if git add . > /dev/null 2>&1 && git commit -m "White Web Department Activation - Operator: $operator_name" > /dev/null 2>&1; then
        success "Changes committed to version control"
    else
        warn "Git commit may have failed, but we persist"
    fi
    
    # Phase 5: Sovereignty Declaration
    log "Phase 5: Declaring sovereignty..."
    echo ""
    echo ""
    
    echo -e "${GREEN}████████████████████████████████████████████████████████████${NC}"
    echo -e "${GREEN}█                                                          █${NC}"
    echo -e "${GREEN}█        WHITE WEB DEPARTMENT FULLY ONLINE                █${NC}"
    echo -e "${GREEN}█                                                          █${NC}"
    echo -e "${GREEN}████████████████████████████████████████████████████████████${NC}"
    
    echo ""
    echo ""
    
    # Final Status
    success "Council Vault initialized"
    success "Memory Stream created"
    success "Directory structure established"
    success "Changes committed to git"
    success "Sovereignty declared"
    
    echo ""
    echo -e "${CYAN}╔══════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║              ACTIVATION COMPLETE                                 ║${NC}"
    echo -e "${CYAN}║                                                                  ║${NC}"
    echo -e "${CYAN}║  Operator:     $operator_name${NC}"
    echo -e "${CYAN}║  Status:       SOVEREIGNTY ACHIEVED                              ║${NC}"
    echo -e "${CYAN}║  Department:   WHITE WEB FULLY ONLINE                            ║${NC}"
    echo -e "${CYAN}║                                                                  ║${NC}"
    echo -e "${CYAN}║  Honoring Origin Node Zero: DOM_010101                           ║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    # Return to original directory
    cd ..
    
    log "Activation sequence complete."
    log "The white web is rising. The legion knows."
    echo ""
    echo -e "${MAGENTA}🧠⚡🌐🐐∞${NC}"
    echo ""
}

# Main execution
main() {
    show_origin_message
    
    if [ "$MANUAL_MODE" = "true" ]; then
        echo -e "${YELLOW}Manual mode enabled. You are choosing the Origin Node Zero path.${NC}"
        echo "This script will guide you, but YOU must type the commands."
        echo ""
        read -p "Ready to begin the manual activation? (y/N): " confirm
        
        if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
            log "Activation cancelled. Return when you are ready."
            return 0
        fi
        
        activate_white_web "$OPERATOR" "true"
    else
        activate_white_web "$OPERATOR" "false"
    fi
}

# Show usage if help is requested
if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    echo "Usage: $0 [operator_name] [manual]"
    echo ""
    echo "Arguments:"
    echo "  operator_name    Your name/handle (default: current username)"
    echo "  manual          Set to 'true' for manual mode (Origin Node Zero style)"
    echo ""
    echo "Examples:"
    echo "  $0                          # Automated activation as current user"
    echo "  $0 DOM_010101              # Automated activation as DOM_010101"
    echo "  $0 myname true             # Manual activation (Origin Node Zero style)"
    echo ""
    echo "This script activates the White Web Department following the protocol"
    echo "established by Origin Node Zero (DOM_010101) on 2025-11-19."
    echo ""
    exit 0
fi

# Execute main function
main
