#!/usr/bin/env bash
# Smelter - Ingot Forge Loader and Manager
# Loads, registers, and manages ingots for the Sovereignty Architecture
#
# Usage: ./scripts/smelter.sh <command> [ingot_name] [args...]
#
# Commands:
#   list        List all available ingots
#   load        Load and initialize an ingot
#   unload      Unload an ingot
#   run         Run an ingot CLI command
#   test        Run tests for an ingot
#   info        Show ingot information
#   validate    Validate ingot structure
#   help        Show this help message

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
INGOTS_DIR="${REPO_ROOT}/ingots"
SMELTER_REGISTRY="${REPO_ROOT}/.smelter_registry"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}[SMELTER]${NC} $*"
}

log_success() {
    echo -e "${GREEN}[SMELTER]${NC} $*"
}

log_warn() {
    echo -e "${YELLOW}[SMELTER]${NC} $*"
}

log_error() {
    echo -e "${RED}[SMELTER]${NC} $*" >&2
}

# Ensure ingots directory exists
ensure_ingots_dir() {
    if [[ ! -d "$INGOTS_DIR" ]]; then
        log_info "Creating ingots directory..."
        mkdir -p "$INGOTS_DIR"
    fi
}

# List all available ingots
cmd_list() {
    ensure_ingots_dir
    log_info "Available ingots in ${INGOTS_DIR}:"
    echo ""
    
    local count=0
    for ingot_dir in "${INGOTS_DIR}"/*/; do
        if [[ -d "$ingot_dir" ]]; then
            local ingot_name
            ingot_name=$(basename "$ingot_dir")
            local manifest="${ingot_dir}manifest.yaml"
            
            if [[ -f "$manifest" ]]; then
                local version description
                # Try to extract version and description using grep/sed if yq not available
                if command -v yq &> /dev/null; then
                    version=$(yq -r '.version // "unknown"' "$manifest" 2>/dev/null || echo "unknown")
                    description=$(yq -r '.description // "No description"' "$manifest" 2>/dev/null | head -1 | tr -d '\n' || echo "No description")
                else
                    version=$(grep -m1 "^version:" "$manifest" 2>/dev/null | sed 's/version:\s*["'\'']\?\([^"'\'']*\)["'\'']\?/\1/' | tr -d ' "' || echo "unknown")
                    description=$(grep -m1 "^description:" "$manifest" 2>/dev/null | sed 's/description:\s*//' | head -c 60 || echo "No description")
                fi
                
                echo -e "  ${GREEN}●${NC} ${ingot_name} (v${version})"
                echo "      ${description:0:60}..."
            else
                echo -e "  ${YELLOW}○${NC} ${ingot_name} (no manifest)"
            fi
            ((count++))
        fi
    done
    
    echo ""
    if [[ $count -eq 0 ]]; then
        log_warn "No ingots found. Create one in ${INGOTS_DIR}/"
    else
        log_info "Total: ${count} ingot(s)"
    fi
}

# Validate ingot structure
cmd_validate() {
    local ingot_name="${1:-}"
    
    if [[ -z "$ingot_name" ]]; then
        log_error "Usage: smelter.sh validate <ingot_name>"
        exit 1
    fi
    
    local ingot_dir="${INGOTS_DIR}/${ingot_name}"
    local valid=true
    
    log_info "Validating ingot: ${ingot_name}"
    echo ""
    
    # Check directory exists
    if [[ ! -d "$ingot_dir" ]]; then
        log_error "Ingot directory not found: ${ingot_dir}"
        exit 1
    fi
    echo -e "  ${GREEN}✓${NC} Directory exists"
    
    # Check manifest
    if [[ -f "${ingot_dir}/manifest.yaml" ]]; then
        echo -e "  ${GREEN}✓${NC} manifest.yaml exists"
    else
        echo -e "  ${RED}✗${NC} manifest.yaml missing"
        valid=false
    fi
    
    # Check README
    if [[ -f "${ingot_dir}/README.md" ]]; then
        echo -e "  ${GREEN}✓${NC} README.md exists"
    else
        echo -e "  ${YELLOW}○${NC} README.md missing (recommended)"
    fi
    
    # Check src directory
    if [[ -d "${ingot_dir}/src" ]]; then
        echo -e "  ${GREEN}✓${NC} src/ directory exists"
    else
        echo -e "  ${YELLOW}○${NC} src/ directory missing (recommended)"
    fi
    
    # Check tests directory
    if [[ -d "${ingot_dir}/tests" ]]; then
        echo -e "  ${GREEN}✓${NC} tests/ directory exists"
    else
        echo -e "  ${YELLOW}○${NC} tests/ directory missing (recommended)"
    fi
    
    echo ""
    if [[ "$valid" == true ]]; then
        log_success "Ingot '${ingot_name}' is valid"
    else
        log_error "Ingot '${ingot_name}' has validation errors"
        exit 1
    fi
}

# Show ingot information
cmd_info() {
    local ingot_name="${1:-}"
    
    if [[ -z "$ingot_name" ]]; then
        log_error "Usage: smelter.sh info <ingot_name>"
        exit 1
    fi
    
    local ingot_dir="${INGOTS_DIR}/${ingot_name}"
    local manifest="${ingot_dir}/manifest.yaml"
    
    if [[ ! -d "$ingot_dir" ]]; then
        log_error "Ingot not found: ${ingot_name}"
        exit 1
    fi
    
    if [[ ! -f "$manifest" ]]; then
        log_error "No manifest.yaml found for ingot: ${ingot_name}"
        exit 1
    fi
    
    log_info "Ingot Information: ${ingot_name}"
    echo ""
    echo "========================================"
    cat "$manifest"
    echo "========================================"
}

# Load and initialize an ingot
cmd_load() {
    local ingot_name="${1:-}"
    
    if [[ -z "$ingot_name" ]]; then
        log_error "Usage: smelter.sh load <ingot_name>"
        exit 1
    fi
    
    local ingot_dir="${INGOTS_DIR}/${ingot_name}"
    local manifest="${ingot_dir}/manifest.yaml"
    
    if [[ ! -d "$ingot_dir" ]]; then
        log_error "Ingot not found: ${ingot_name}"
        exit 1
    fi
    
    log_info "Loading ingot: ${ingot_name}"
    
    # Validate first
    cmd_validate "$ingot_name" || exit 1
    
    # Look for init script
    local init_script="${ingot_dir}/src/init.sh"
    if [[ -f "$init_script" ]]; then
        chmod +x "$init_script"
        log_info "Running initialization script..."
        if "$init_script"; then
            log_success "Ingot '${ingot_name}' loaded successfully"
        else
            log_error "Ingot initialization failed"
            exit 1
        fi
    else
        log_info "No init.sh found, skipping initialization"
        log_success "Ingot '${ingot_name}' registered"
    fi
    
    # Register in smelter registry
    echo "${ingot_name}:loaded:$(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$SMELTER_REGISTRY"
}

# Run an ingot CLI command
cmd_run() {
    local ingot_name="${1:-}"
    local cli_name="${2:-}"
    shift 2 || true
    
    if [[ -z "$ingot_name" ]]; then
        log_error "Usage: smelter.sh run <ingot_name> <cli_command> [args...]"
        exit 1
    fi
    
    local ingot_dir="${INGOTS_DIR}/${ingot_name}"
    local manifest="${ingot_dir}/manifest.yaml"
    
    if [[ ! -d "$ingot_dir" ]]; then
        log_error "Ingot not found: ${ingot_name}"
        exit 1
    fi
    
    # If no CLI name specified, try default cli.sh
    if [[ -z "$cli_name" ]]; then
        local default_cli="${ingot_dir}/src/cli.sh"
        if [[ -f "$default_cli" ]]; then
            chmod +x "$default_cli"
            exec "$default_cli" "$@"
        else
            log_error "No CLI command specified and no default cli.sh found"
            exit 1
        fi
    fi
    
    # Look for CLI script by name in src directory
    local cli_script="${ingot_dir}/src/${cli_name}.sh"
    if [[ ! -f "$cli_script" ]]; then
        # Try without .sh extension
        cli_script="${ingot_dir}/src/${cli_name}"
    fi
    
    if [[ -f "$cli_script" ]]; then
        chmod +x "$cli_script"
        exec "$cli_script" "$@"
    else
        # Fallback to cli.sh with command as first arg
        local default_cli="${ingot_dir}/src/cli.sh"
        if [[ -f "$default_cli" ]]; then
            chmod +x "$default_cli"
            exec "$default_cli" "$cli_name" "$@"
        else
            log_error "CLI script not found: ${cli_script}"
            exit 1
        fi
    fi
}

# Run tests for an ingot
cmd_test() {
    local ingot_name="${1:-}"
    
    if [[ -z "$ingot_name" ]]; then
        log_error "Usage: smelter.sh test <ingot_name>"
        exit 1
    fi
    
    local ingot_dir="${INGOTS_DIR}/${ingot_name}"
    local tests_dir="${ingot_dir}/tests"
    
    if [[ ! -d "$ingot_dir" ]]; then
        log_error "Ingot not found: ${ingot_name}"
        exit 1
    fi
    
    if [[ ! -d "$tests_dir" ]]; then
        log_warn "No tests directory found for ingot: ${ingot_name}"
        exit 0
    fi
    
    log_info "Running tests for ingot: ${ingot_name}"
    echo ""
    
    local test_count=0
    local test_passed=0
    local test_failed=0
    
    for test_file in "${tests_dir}"/test_*.sh; do
        if [[ -f "$test_file" ]]; then
            test_count=$((test_count + 1))
            local test_name
            test_name=$(basename "$test_file")
            log_info "Running: ${test_name}"
            
            chmod +x "$test_file"
            if "$test_file"; then
                test_passed=$((test_passed + 1))
            else
                test_failed=$((test_failed + 1))
            fi
            echo ""
        fi
    done
    
    if [[ $test_count -eq 0 ]]; then
        log_warn "No test files found (test_*.sh)"
    else
        echo "========================================"
        log_info "Test Results: ${test_passed}/${test_count} passed"
        if [[ $test_failed -gt 0 ]]; then
            log_error "${test_failed} test(s) failed"
            exit 1
        else
            log_success "All tests passed!"
        fi
    fi
}

# Show help
cmd_help() {
    cat << EOF
╔══════════════════════════════════════════════════════════════════╗
║                    🔥 SMELTER - Ingot Forge Manager 🔥             ║
║                                                                   ║
║   The Smelter loads, registers, and manages ingots for the        ║
║   Sovereignty Architecture. Each ingot is a self-contained        ║
║   module that can be plugged/unplugged from the system.           ║
╚══════════════════════════════════════════════════════════════════╝

Usage: $(basename "$0") <command> [ingot_name] [args...]

Commands:
    list                    List all available ingots
    load <ingot>           Load and initialize an ingot
    run <ingot> [cmd]      Run an ingot CLI command
    test <ingot>           Run tests for an ingot
    info <ingot>           Show ingot manifest information
    validate <ingot>       Validate ingot structure
    help                   Show this help message

Examples:
    $(basename "$0") list
    $(basename "$0") load example_ingot
    $(basename "$0") run example_ingot demo
    $(basename "$0") test example_ingot
    $(basename "$0") info example_ingot
    $(basename "$0") validate example_ingot

Ingot Structure:
    ingots/<ingot_name>/
    ├── manifest.yaml       Required: Ingot metadata
    ├── README.md          Recommended: Documentation
    ├── src/               Recommended: Source code
    │   ├── init.sh        Optional: Initialization hook
    │   └── cli.sh         Optional: CLI entry point
    └── tests/             Recommended: Test files
        └── test_*.sh      Test scripts

For more information, see: INGOT_FORGE.md
EOF
}

# Main entry point
main() {
    local command="${1:-help}"
    shift || true
    
    case "$command" in
        list)
            cmd_list "$@"
            ;;
        load)
            cmd_load "$@"
            ;;
        run)
            cmd_run "$@"
            ;;
        test)
            cmd_test "$@"
            ;;
        info)
            cmd_info "$@"
            ;;
        validate)
            cmd_validate "$@"
            ;;
        help|--help|-h)
            cmd_help
            ;;
        *)
            log_error "Unknown command: ${command}"
            echo "Run '$(basename "$0") help' for usage information."
            exit 1
            ;;
    esac
}

main "$@"
