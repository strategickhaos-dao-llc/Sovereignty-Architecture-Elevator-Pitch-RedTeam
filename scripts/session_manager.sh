#!/bin/bash
# Session Manager - Manage reasoning trace sessions

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
SESSIONS_DIR="$REPO_ROOT/sessions"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

function print_help() {
    cat <<EOF
Session Manager - Manage reasoning trace sessions

Usage: $0 <command> [options]

Commands:
    status              Show status of all sessions
    show <session>      Show details of a specific session
    create <name>       Create a new session (not in original 12)
    add-artifact <session> <file>  Add artifact to a session
    add-transcript <session> <file> Add transcript to a session
    update-status <session> <percentage> Update session completion status
    validate            Validate all sessions have required files

Examples:
    $0 status
    $0 show 01-sovereignty-mirror
    $0 update-status 05-mojo-k8s 85
    $0 add-transcript 06-dialectical-engine chat-export.md

EOF
}

function show_status() {
    echo -e "${BLUE}=== Session Status ===${NC}\n"
    
    for session_dir in "$SESSIONS_DIR"/[0-9][0-9]-*; do
        if [ ! -d "$session_dir" ]; then
            continue
        fi
        
        session_name=$(basename "$session_dir")
        readme="$session_dir/README.md"
        
        if [ -f "$readme" ]; then
            # Extract status from README
            status=$(grep "^## Status" "$readme" -A 1 | tail -1 | sed 's/^[*[:space:]]*//')
            
            # Determine status icon
            if echo "$status" | grep -q "Complete"; then
                icon="✅"
                color=$GREEN
            elif echo "$status" | grep -q "In Progress\|80%"; then
                icon="🔧"
                color=$YELLOW
            else
                icon="📋"
                color=$NC
            fi
            
            echo -e "${color}${icon} ${session_name}${NC}"
            echo -e "   ${status}"
        else
            echo -e "${RED}❌ ${session_name}${NC}"
            echo -e "   Missing README.md"
        fi
        echo ""
    done
}

function show_session() {
    local session_name=$1
    local session_dir="$SESSIONS_DIR/$session_name"
    
    if [ ! -d "$session_dir" ]; then
        echo -e "${RED}Error: Session $session_name not found${NC}"
        exit 1
    fi
    
    echo -e "${BLUE}=== Session: $session_name ===${NC}\n"
    
    # Show README if exists
    if [ -f "$session_dir/README.md" ]; then
        echo -e "${GREEN}README.md:${NC}"
        head -20 "$session_dir/README.md"
        echo -e "\n... (showing first 20 lines)\n"
    fi
    
    # List files
    echo -e "${GREEN}Files:${NC}"
    find "$session_dir" -type f -exec basename {} \; | sort | sed 's/^/  - /'
    echo ""
    
    # Check for artifacts
    if [ -d "$session_dir/artifacts" ]; then
        echo -e "${GREEN}Artifacts:${NC}"
        find "$session_dir/artifacts" -type f | sed "s|$session_dir/artifacts/||" | sed 's/^/  - /'
    else
        echo -e "${YELLOW}No artifacts directory${NC}"
    fi
}

function create_session() {
    local session_name=$1
    
    if [ -z "$session_name" ]; then
        echo -e "${RED}Error: Session name required${NC}"
        echo "Usage: $0 create <session-name>"
        exit 1
    fi
    
    # Generate next session number
    local last_num=$(ls -d "$SESSIONS_DIR"/[0-9][0-9]-* 2>/dev/null | tail -1 | sed 's/.*\/\([0-9][0-9]\)-.*/\1/' || echo "12")
    local next_num=$(printf "%02d" $((10#$last_num + 1)))
    
    local full_name="$next_num-$session_name"
    local session_dir="$SESSIONS_DIR/$full_name"
    
    if [ -d "$session_dir" ]; then
        echo -e "${RED}Error: Session $full_name already exists${NC}"
        exit 1
    fi
    
    echo -e "${BLUE}Creating session: $full_name${NC}"
    
    mkdir -p "$session_dir/artifacts"
    
    # Copy template
    cp "$SESSIONS_DIR/SESSION_TEMPLATE.md" "$session_dir/README.md"
    
    # Replace placeholders
    sed -i "s/\[NUMBER\]/$next_num/g" "$session_dir/README.md"
    sed -i "s/\[THEME NAME\]/$session_name/g" "$session_dir/README.md"
    
    echo -e "${GREEN}✓ Created $full_name${NC}"
    echo -e "  - README.md (from template)"
    echo -e "  - artifacts/ directory"
}

function add_artifact() {
    local session_name=$1
    local artifact_file=$2
    
    if [ -z "$session_name" ] || [ -z "$artifact_file" ]; then
        echo -e "${RED}Error: Session name and artifact file required${NC}"
        echo "Usage: $0 add-artifact <session-name> <file>"
        exit 1
    fi
    
    local session_dir="$SESSIONS_DIR/$session_name"
    
    if [ ! -d "$session_dir" ]; then
        echo -e "${RED}Error: Session $session_name not found${NC}"
        exit 1
    fi
    
    if [ ! -f "$artifact_file" ]; then
        echo -e "${RED}Error: Artifact file $artifact_file not found${NC}"
        exit 1
    fi
    
    mkdir -p "$session_dir/artifacts"
    cp "$artifact_file" "$session_dir/artifacts/"
    
    echo -e "${GREEN}✓ Added artifact to $session_name${NC}"
}

function add_transcript() {
    local session_name=$1
    local transcript_file=$2
    
    if [ -z "$session_name" ] || [ -z "$transcript_file" ]; then
        echo -e "${RED}Error: Session name and transcript file required${NC}"
        echo "Usage: $0 add-transcript <session-name> <file>"
        exit 1
    fi
    
    local session_dir="$SESSIONS_DIR/$session_name"
    
    if [ ! -d "$session_dir" ]; then
        echo -e "${RED}Error: Session $session_name not found${NC}"
        exit 1
    fi
    
    if [ ! -f "$transcript_file" ]; then
        echo -e "${RED}Error: Transcript file $transcript_file not found${NC}"
        exit 1
    fi
    
    cp "$transcript_file" "$session_dir/transcript.md"
    
    echo -e "${GREEN}✓ Added transcript to $session_name${NC}"
}

function update_status() {
    local session_name=$1
    local percentage=$2
    
    if [ -z "$session_name" ] || [ -z "$percentage" ]; then
        echo -e "${RED}Error: Session name and percentage required${NC}"
        echo "Usage: $0 update-status <session-name> <percentage>"
        exit 1
    fi
    
    local session_dir="$SESSIONS_DIR/$session_name"
    local readme="$session_dir/README.md"
    
    if [ ! -f "$readme" ]; then
        echo -e "${RED}Error: README.md not found for $session_name${NC}"
        exit 1
    fi
    
    # Update status line
    if [ "$percentage" -eq 100 ]; then
        sed -i "s/^## Status.*$/## Status\n✅ **Complete** - 100%/" "$readme"
    elif [ "$percentage" -gt 0 ]; then
        sed -i "s/^## Status.*$/## Status\n🔧 **In Progress** - ${percentage}%/" "$readme"
    else
        sed -i "s/^## Status.*$/## Status\n📋 **Planned** - 0%/" "$readme"
    fi
    
    echo -e "${GREEN}✓ Updated status for $session_name to ${percentage}%${NC}"
}

function validate_sessions() {
    echo -e "${BLUE}=== Validating Sessions ===${NC}\n"
    
    local errors=0
    
    for session_dir in "$SESSIONS_DIR"/[0-9][0-9]-*; do
        if [ ! -d "$session_dir" ]; then
            continue
        fi
        
        session_name=$(basename "$session_dir")
        
        # Check for README
        if [ ! -f "$session_dir/README.md" ]; then
            echo -e "${RED}✗ $session_name: Missing README.md${NC}"
            ((errors++))
        else
            echo -e "${GREEN}✓ $session_name: README.md present${NC}"
        fi
    done
    
    echo ""
    if [ $errors -eq 0 ]; then
        echo -e "${GREEN}All sessions valid!${NC}"
    else
        echo -e "${RED}Found $errors validation errors${NC}"
        exit 1
    fi
}

# Main command dispatcher
case "${1:-}" in
    status)
        show_status
        ;;
    show)
        show_session "$2"
        ;;
    create)
        create_session "$2"
        ;;
    add-artifact)
        add_artifact "$2" "$3"
        ;;
    add-transcript)
        add_transcript "$2" "$3"
        ;;
    update-status)
        update_status "$2" "$3"
        ;;
    validate)
        validate_sessions
        ;;
    help|--help|-h|"")
        print_help
        ;;
    *)
        echo -e "${RED}Error: Unknown command '$1'${NC}\n"
        print_help
        exit 1
        ;;
esac
