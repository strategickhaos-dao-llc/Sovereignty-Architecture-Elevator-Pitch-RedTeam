#!/usr/bin/env bash
# Example Ingot - CLI Entry Point
# This script provides the CLI interface for the ingot

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INGOT_ROOT="$(dirname "$SCRIPT_DIR")"
INGOT_NAME="example_ingot"

# Enable debug mode if requested
DEBUG="${EXAMPLE_INGOT_DEBUG:-false}"

log() {
    echo "[${INGOT_NAME}] $*"
}

debug() {
    if [[ "$DEBUG" == "true" ]]; then
        echo "[${INGOT_NAME}][DEBUG] $*"
    fi
}

show_help() {
    cat << EOF
${INGOT_NAME} CLI - Example Ingot Command Line Interface

Usage: $(basename "$0") [command] [options]

Commands:
    help        Show this help message
    version     Show ingot version
    status      Show ingot status
    demo        Run a demo operation

Options:
    --debug     Enable debug output

Examples:
    $(basename "$0") help
    $(basename "$0") version
    $(basename "$0") demo --debug
EOF
}

cmd_version() {
    # Read version from manifest
    if command -v yq &> /dev/null; then
        local version
        version=$(yq -r '.version' "${INGOT_ROOT}/manifest.yaml" 2>/dev/null || echo "unknown")
        echo "${INGOT_NAME} version ${version}"
    else
        echo "${INGOT_NAME} version 1.0.0"
    fi
}

cmd_status() {
    log "Status: ACTIVE"
    log "Debug mode: ${DEBUG}"
}

cmd_demo() {
    log "Running demo operation..."
    debug "This is a debug message"
    log "Demo completed successfully!"
    log "This ingot is ready for customization."
}

# Main entry point
main() {
    local command="${1:-help}"
    shift || true
    
    # Check for --debug flag
    for arg in "$@"; do
        if [[ "$arg" == "--debug" ]]; then
            DEBUG="true"
            export EXAMPLE_INGOT_DEBUG="true"
        fi
    done
    
    case "$command" in
        help|--help|-h)
            show_help
            ;;
        version|--version|-v)
            cmd_version
            ;;
        status)
            cmd_status
            ;;
        demo)
            cmd_demo
            ;;
        *)
            echo "Unknown command: ${command}"
            echo "Run '$(basename "$0") help' for usage information."
            exit 1
            ;;
    esac
}

main "$@"
