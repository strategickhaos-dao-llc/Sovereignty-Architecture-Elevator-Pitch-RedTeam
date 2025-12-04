#!/bin/bash
# mirror-to-enterprise.sh
# Strategickhaos Swarm Intelligence — Repository Mirror Script
# Mirror repositories from personal accounts to enterprise organizations

set -euo pipefail

# Configuration
DEFAULT_ORG="Strategickhaos-Swarm-Intelligence"
GIT_HOST="github.com"
ENTERPRISE_NAME="strategickhaos-swarm-intelligence"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

echo_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
echo_success() { echo -e "${GREEN}[✓]${NC} $1"; }
echo_warning() { echo -e "${YELLOW}[!]${NC} $1"; }
echo_error() { echo -e "${RED}[✗]${NC} $1"; }
echo_step() { echo -e "${CYAN}[STEP]${NC} $1"; }

# Mirror a single repository
mirror_single() {
    local source="$1"
    local target_org="${2:-$DEFAULT_ORG}"
    local target_name="${3:-}"
    
    # Extract repo name from URL if not provided
    if [[ -z "$target_name" ]]; then
        target_name=$(basename "$source" .git)
    fi
    
    local target="https://${GIT_HOST}/${target_org}/${target_name}.git"
    
    echo_step "Mirroring: $source -> $target"
    
    # Create temp directory
    local temp_dir
    temp_dir=$(mktemp -d)
    
    # Setup cleanup trap after temp_dir is created
    cleanup() {
        rm -rf "$temp_dir"
    }
    trap cleanup EXIT
    
    echo_info "Cloning source (bare)..."
    if ! git clone --bare "$source" "$temp_dir"; then
        echo_error "Failed to clone: $source"
        return 1
    fi
    
    cd "$temp_dir"
    
    echo_info "Pushing to enterprise..."
    if ! git push --mirror "$target"; then
        echo_error "Failed to push to: $target"
        echo_warning "Make sure the repository exists in the target organization"
        return 1
    fi
    
    cd - > /dev/null
    
    echo_success "Mirrored: $target_name"
    echo_info "View: https://${GIT_HOST}/${target_org}/${target_name}"
}

# Mirror from current directory
mirror_current() {
    local target_org="${1:-$DEFAULT_ORG}"
    
    if [[ ! -d ".git" ]]; then
        echo_error "Not a git repository"
        exit 1
    fi
    
    local repo_name
    repo_name=$(basename "$(pwd)")
    local target="https://${GIT_HOST}/${target_org}/${repo_name}.git"
    
    echo_step "Mirroring current repo to: $target"
    
    # Check if remote exists
    if git remote get-url enterprise &> /dev/null; then
        echo_info "Enterprise remote already exists, updating..."
        git remote set-url enterprise "$target"
    else
        echo_info "Adding enterprise remote..."
        git remote add enterprise "$target"
    fi
    
    echo_info "Pushing all branches and tags..."
    git push enterprise --all
    git push enterprise --tags
    
    echo_success "Mirrored: $repo_name"
    echo_info "View: https://${GIT_HOST}/${target_org}/${repo_name}"
}

# Mirror multiple repositories from a list
mirror_batch() {
    local list_file="$1"
    local target_org="${2:-$DEFAULT_ORG}"
    
    if [[ ! -f "$list_file" ]]; then
        echo_error "List file not found: $list_file"
        exit 1
    fi
    
    echo_step "Batch mirroring from: $list_file"
    
    local count=0
    local failed=0
    
    while IFS= read -r repo || [[ -n "$repo" ]]; do
        # Skip empty lines and comments
        [[ -z "$repo" || "$repo" =~ ^# ]] && continue
        
        if mirror_single "$repo" "$target_org"; then
            ((count++))
        else
            ((failed++))
        fi
        
        echo ""
    done < "$list_file"
    
    echo_success "Batch complete: $count mirrored, $failed failed"
}

# Show help
show_help() {
    echo "Repository Mirror to Enterprise"
    echo ""
    echo "Usage: $0 <command> [options]"
    echo ""
    echo "Commands:"
    echo "  single <source_url> [org] [name]  - Mirror a single repository"
    echo "  current [org]                      - Mirror current directory repo"
    echo "  batch <list_file> [org]            - Mirror repos from a list file"
    echo ""
    echo "Options:"
    echo "  org   - Target organization (default: $DEFAULT_ORG)"
    echo "  name  - Target repository name (default: extracted from source)"
    echo ""
    echo "Examples:"
    echo "  $0 single https://github.com/user/repo.git"
    echo "  $0 single https://github.com/user/repo.git MyOrg my-repo"
    echo "  $0 current"
    echo "  $0 batch repos.txt"
    echo ""
    echo "List file format (one repo URL per line):"
    echo "  https://github.com/user/repo1.git"
    echo "  https://github.com/user/repo2.git"
    echo "  # Lines starting with # are ignored"
    echo ""
    echo "Enterprise: https://github.com/enterprises/${ENTERPRISE_NAME}"
}

# Main
case "${1:-help}" in
    "single"|"mirror")
        if [[ -z "${2:-}" ]]; then
            echo_error "Source URL required"
            show_help
            exit 1
        fi
        mirror_single "$2" "${3:-}" "${4:-}"
        ;;
    "current"|"this")
        mirror_current "${2:-}"
        ;;
    "batch"|"list")
        if [[ -z "${2:-}" ]]; then
            echo_error "List file required"
            show_help
            exit 1
        fi
        mirror_batch "$2" "${3:-}"
        ;;
    "help"|"--help"|"-h")
        show_help
        ;;
    *)
        echo_error "Unknown command: $1"
        show_help
        exit 1
        ;;
esac
