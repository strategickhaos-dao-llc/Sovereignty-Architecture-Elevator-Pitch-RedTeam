#!/bin/bash
# start-ce-session.sh
# Initialize a new Commence Evolution Time (CET) session

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Configuration
SESSIONS_DIR="$HOME/ce_sessions"
TEMPLATES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/templates"
SESSION_DATE=$(date +%Y-%m-%d)
SESSION_TIME=$(date +%H:%M)
SESSION_FILE="$SESSIONS_DIR/ce_session_${SESSION_DATE}.md"

# Function to print header
print_header() {
    echo ""
    echo -e "${BOLD}${BLUE}╔════════════════════════════════════════════════╗${NC}"
    echo -e "${BOLD}${BLUE}║   🎯 Commence Evolution Time - Session Start  ║${NC}"
    echo -e "${BOLD}${BLUE}╚════════════════════════════════════════════════╝${NC}"
    echo ""
}

# Function to print section
print_section() {
    echo ""
    echo -e "${BOLD}${GREEN}▶ $1${NC}"
}

# Function to print info
print_info() {
    echo -e "  ${BLUE}ℹ${NC} $1"
}

# Function to print success
print_success() {
    echo -e "  ${GREEN}✓${NC} $1"
}

# Function to print warning
print_warning() {
    echo -e "  ${YELLOW}⚠${NC} $1"
}

# Function to print error
print_error() {
    echo -e "  ${RED}✗${NC} $1"
}

# Create sessions directory if it doesn't exist
setup_directories() {
    print_section "Setting up session environment..."
    
    if [ ! -d "$SESSIONS_DIR" ]; then
        mkdir -p "$SESSIONS_DIR"
        print_success "Created sessions directory: $SESSIONS_DIR"
    else
        print_info "Sessions directory exists: $SESSIONS_DIR"
    fi
}

# Check if template exists
check_template() {
    if [ ! -f "$TEMPLATES_DIR/ce_session_template.md" ]; then
        print_error "Template not found: $TEMPLATES_DIR/ce_session_template.md"
        exit 1
    fi
}

# Create new session file
create_session() {
    print_section "Creating new session file..."
    
    if [ -f "$SESSION_FILE" ]; then
        print_warning "Session file already exists for today"
        echo -e "  ${YELLOW}→${NC} $SESSION_FILE"
        read -p "  Continue editing existing session? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_info "Exiting. Use existing session file."
            exit 0
        fi
    else
        # Copy template and customize
        cp "$TEMPLATES_DIR/ce_session_template.md" "$SESSION_FILE"
        
        # Replace placeholders
        sed -i.bak "s/\[Date: YYYY-MM-DD\]/$SESSION_DATE/g" "$SESSION_FILE"
        sed -i.bak "s/___:___/$SESSION_TIME/g" "$SESSION_FILE" || true
        rm -f "$SESSION_FILE.bak"
        
        print_success "Created new session file"
    fi
    
    echo -e "  ${BLUE}→${NC} $SESSION_FILE"
}

# Display session options
show_options() {
    print_section "Session Type Selection"
    
    echo ""
    echo "  1) CE-75 (75 minutes) - Regular session"
    echo "     └─ 3 cycles: 25+5, 25+5, 10+5"
    echo ""
    echo "  2) CE-45 (45 minutes) - Express session"
    echo "     └─ 2 cycles: 25+5, 15+5"
    echo ""
    
    read -p "  Select session type (1 or 2): " -n 1 -r
    echo
    
    case $REPLY in
        1)
            SESSION_TYPE="CE-75"
            DURATION=75
            ;;
        2)
            SESSION_TYPE="CE-45"
            DURATION=45
            ;;
        *)
            print_error "Invalid selection. Defaulting to CE-75."
            SESSION_TYPE="CE-75"
            DURATION=75
            ;;
    esac
    
    print_success "Selected: $SESSION_TYPE ($DURATION minutes)"
}

# Ask for Boss Assignment
get_boss_assignment() {
    print_section "Boss Assignment Setup"
    
    echo ""
    read -p "  Course code (e.g., IT-140): " COURSE
    read -p "  Assignment name: " ASSIGNMENT
    read -p "  Due date (optional): " DUE_DATE
    
    echo ""
    print_success "Boss Assignment: $COURSE - $ASSIGNMENT"
}

# Start timer (optional)
start_timer() {
    print_section "Timer Setup"
    
    echo ""
    read -p "  Start $DURATION minute timer now? (y/n): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "Timer will notify you after $DURATION minutes..."
        
        # Try different notification methods based on what's available
        if command -v osascript &> /dev/null; then
            # macOS notification
            (sleep $((DURATION * 60)) && osascript -e "display notification \"Time to log progress and wrap up!\" with title \"CE Session Complete\"") &
        elif command -v notify-send &> /dev/null; then
            # Linux notification
            (sleep $((DURATION * 60)) && notify-send "CE Session Complete" "Time to log progress and wrap up!") &
        else
            # Fallback: just a beep
            (sleep $((DURATION * 60)) && echo -e "\a") &
        fi
        
        TIMER_PID=$!
        print_success "Timer started (PID: $TIMER_PID)"
        echo "$TIMER_PID" > "$SESSIONS_DIR/.current_timer_pid"
    else
        print_info "Skipping timer. Set your own timer for $DURATION minutes."
    fi
}

# Display session summary
show_summary() {
    echo ""
    print_section "Session Initialized! 🚀"
    echo ""
    echo -e "  ${BOLD}Session Type:${NC} $SESSION_TYPE"
    echo -e "  ${BOLD}Duration:${NC} $DURATION minutes"
    echo -e "  ${BOLD}Boss Assignment:${NC} $COURSE - $ASSIGNMENT"
    if [ -n "$DUE_DATE" ]; then
        echo -e "  ${BOLD}Due Date:${NC} $DUE_DATE"
    fi
    echo -e "  ${BOLD}Session File:${NC} $SESSION_FILE"
    echo ""
    
    print_section "Next Steps:"
    echo ""
    echo "  1. 📚 Open your LMS/course dashboard"
    echo "  2. 📝 Open the session file in your editor"
    echo "  3. 💬 Open AI assistant chat"
    echo "  4. 🚫 Close all other tabs/distractions"
    echo "  5. 🎯 Start Cycle 1: Deep Work (25 minutes)"
    echo ""
    
    print_section "Quick Commands:"
    echo ""
    echo -e "  ${BLUE}# Open session file${NC}"
    echo "  \$EDITOR $SESSION_FILE"
    echo ""
    echo -e "  ${BLUE}# Log progress during session${NC}"
    echo "  ./scripts/ce-log-progress.sh \"Your progress note\""
    echo ""
    echo -e "  ${BLUE}# View all sessions${NC}"
    echo "  ls -lh $SESSIONS_DIR"
    echo ""
}

# Open session file in editor (optional)
open_editor() {
    echo ""
    read -p "  Open session file in editor now? (y/n): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # Try to detect and use available editor
        if [ -n "$EDITOR" ]; then
            $EDITOR "$SESSION_FILE" &
            print_success "Opened in \$EDITOR"
        elif command -v code &> /dev/null; then
            code "$SESSION_FILE" &
            print_success "Opened in VS Code"
        elif command -v nano &> /dev/null; then
            nano "$SESSION_FILE"
        elif command -v vim &> /dev/null; then
            vim "$SESSION_FILE"
        else
            print_warning "No editor found. Please open manually:"
            echo "  $SESSION_FILE"
        fi
    fi
}

# Display motivation
show_motivation() {
    echo ""
    echo -e "${BOLD}${GREEN}╔════════════════════════════════════════════════╗${NC}"
    echo -e "${BOLD}${GREEN}║  💪 \"The babies are fancy, but school pays     ║${NC}"
    echo -e "${BOLD}${GREEN}║      the bills. Let's do this together.\"       ║${NC}"
    echo -e "${BOLD}${GREEN}╚════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "  ${BOLD}Go get 'em! Future You is counting on you. 🎯${NC}"
    echo ""
}

# Main execution
main() {
    print_header
    setup_directories
    check_template
    create_session
    show_options
    get_boss_assignment
    start_timer
    show_summary
    open_editor
    show_motivation
}

# Run main function
main
