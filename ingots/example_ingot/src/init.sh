#!/usr/bin/env bash
# Example Ingot - Initialization Script
# This script is called when the ingot is loaded by the smelter

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

# Main initialization
main() {
    log "Initializing ${INGOT_NAME}..."
    debug "INGOT_ROOT: ${INGOT_ROOT}"
    
    # Add your initialization logic here
    # Examples:
    # - Validate environment variables
    # - Set up directories
    # - Initialize state
    
    log "${INGOT_NAME} initialized successfully"
}

main "$@"
