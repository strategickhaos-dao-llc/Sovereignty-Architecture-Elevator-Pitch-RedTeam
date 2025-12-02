#!/bin/bash
# ce-log-progress.sh
# Quick progress logging during CE sessions

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Configuration
SESSIONS_DIR="$HOME/ce_sessions"
SESSION_DATE=$(date +%Y-%m-%d)
SESSION_FILE="$SESSIONS_DIR/ce_session_${SESSION_DATE}.md"
TIMESTAMP=$(date +%H:%M)

# Function to print with color
print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Check if session file exists
check_session() {
    if [ ! -f "$SESSION_FILE" ]; then
        print_error "No session file found for today"
        echo ""
        print_info "Start a new session first:"
        echo "  ./scripts/start-ce-session.sh"
        echo ""
        exit 1
    fi
}

# Display current session info
show_session_info() {
    echo ""
    echo -e "${BOLD}Current CE Session: $SESSION_DATE${NC}"
    
    # Try to extract Boss Assignment from session file
    BOSS_ASSIGNMENT=$(grep -A 1 "Boss Assignment:" "$SESSION_FILE" | tail -1 | sed 's/^[* -]*//' || echo "Not set")
    
    if [ "$BOSS_ASSIGNMENT" != "Not set" ]; then
        echo -e "Boss Assignment: ${BOLD}$BOSS_ASSIGNMENT${NC}"
    fi
    echo ""
}

# Get progress note from user
get_progress_note() {
    if [ -z "$1" ]; then
        echo "Enter your progress note (or 'q' to cancel):"
        echo ""
        read -p "> " PROGRESS_NOTE
        
        if [ "$PROGRESS_NOTE" = "q" ] || [ -z "$PROGRESS_NOTE" ]; then
            print_warning "Cancelled. No progress logged."
            exit 0
        fi
    else
        PROGRESS_NOTE="$*"
    fi
}

# Determine which cycle we're in
determine_cycle() {
    CYCLE_1_LOGS=$(grep -c "Cycle 1:" "$SESSION_FILE" 2>/dev/null || echo "0")
    CYCLE_2_LOGS=$(grep -c "Cycle 2:" "$SESSION_FILE" 2>/dev/null || echo "0")
    CYCLE_3_LOGS=$(grep -c "Cycle 3:" "$SESSION_FILE" 2>/dev/null || echo "0")
    
    # Determine current cycle based on what's been logged
    if [ "$CYCLE_1_LOGS" -eq 0 ]; then
        CURRENT_CYCLE="Cycle 1"
    elif [ "$CYCLE_2_LOGS" -eq 0 ]; then
        CURRENT_CYCLE="Cycle 2"
    elif [ "$CYCLE_3_LOGS" -eq 0 ]; then
        CURRENT_CYCLE="Cycle 3"
    else
        CURRENT_CYCLE="Additional"
    fi
}

# Append progress to session file
append_progress() {
    local LOG_ENTRY="[$TIMESTAMP] $CURRENT_CYCLE Progress: $PROGRESS_NOTE"
    
    # Create a temporary log section if it doesn't exist
    if ! grep -q "## 📝 Quick Progress Log" "$SESSION_FILE"; then
        echo "" >> "$SESSION_FILE"
        echo "## 📝 Quick Progress Log" >> "$SESSION_FILE"
        echo "" >> "$SESSION_FILE"
    fi
    
    # Append the log entry
    echo "- $LOG_ENTRY" >> "$SESSION_FILE"
    
    print_success "Progress logged to session file"
    echo ""
    echo "  $LOG_ENTRY"
}

# Display quick stats
show_stats() {
    echo ""
    echo -e "${BOLD}Session Stats:${NC}"
    
    # Count progress entries
    TOTAL_LOGS=$(grep -c "Progress:" "$SESSION_FILE" 2>/dev/null || echo "0")
    echo "  Total progress logs: $TOTAL_LOGS"
    
    # Estimate time spent (rough)
    START_TIME=$(grep "Start Time:" "$SESSION_FILE" | head -1 | sed 's/.*Start Time: //' | sed 's/[^0-9:]//g')
    if [ -n "$START_TIME" ]; then
        echo "  Session started: $START_TIME"
        echo "  Current time: $TIMESTAMP"
    fi
    
    echo ""
}

# Display next actions
show_next_actions() {
    echo -e "${BOLD}Next Actions:${NC}"
    echo ""
    
    determine_cycle
    
    case $CURRENT_CYCLE in
        "Cycle 1")
            echo "  ⏭  Continue Cycle 1 deep work"
            echo "  📝 Log progress again in 25 minutes"
            ;;
        "Cycle 2")
            echo "  ⏭  Continue Cycle 2 deep work"
            echo "  📝 Log progress again in 25 minutes"
            ;;
        "Cycle 3")
            echo "  ⏭  Continue Cycle 3 - polish phase"
            echo "  ✅ Session closeout in 10-15 minutes"
            ;;
        *)
            echo "  ✅ Consider wrapping up session"
            echo "  📊 Update homework_tracker.md"
            echo "  🎯 Let Athena write the summary"
            ;;
    esac
    echo ""
}

# Offer to open session file
offer_open() {
    echo ""
    read -p "Open session file to review? (y/n): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if [ -n "$EDITOR" ]; then
            $EDITOR "$SESSION_FILE"
        elif command -v code &> /dev/null; then
            code "$SESSION_FILE"
        elif command -v cat &> /dev/null; then
            cat "$SESSION_FILE"
        fi
    fi
}

# Quick template for structured logging
offer_template() {
    echo ""
    echo "Need a structured log? Here's a template:"
    echo ""
    echo "─────────────────────────────────────"
    echo "Completed:"
    echo "- "
    echo ""
    echo "Blockers:"
    echo "- "
    echo ""
    echo "Next:"
    echo "- "
    echo "─────────────────────────────────────"
    echo ""
}

# Main function
main() {
    check_session
    show_session_info
    
    # If no arguments provided, show help
    if [ $# -eq 0 ]; then
        offer_template
    fi
    
    get_progress_note "$@"
    determine_cycle
    append_progress
    show_stats
    show_next_actions
    
    # Quick motivation
    echo -e "${GREEN}Keep going! You're making progress. 💪${NC}"
    echo ""
}

# Help text
if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    echo ""
    echo "CE Progress Logger - Quick progress logging during CE sessions"
    echo ""
    echo "Usage:"
    echo "  ./scripts/ce-log-progress.sh [progress note]"
    echo ""
    echo "Examples:"
    echo "  ./scripts/ce-log-progress.sh \"Completed add_item() function\""
    echo "  ./scripts/ce-log-progress.sh \"Stuck on validation logic - called Nova\""
    echo "  ./scripts/ce-log-progress.sh  # Interactive mode"
    echo ""
    echo "This script appends timestamped progress notes to your current CE session file."
    echo ""
    exit 0
fi

# Run main function
main "$@"
