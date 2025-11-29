#!/usr/bin/env bash
# python_syntax.sh - Check Python syntax using pyflakes
# Part of Sovereign Swarm — Zero-Trust AI Orchestration Mesh
# Apache-2.0 License

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "${SCRIPT_DIR}")"

log() { printf '[%s] %s\n' "$(date -u +%FT%TZ)" "$*"; }

main() {
    log "Running pyflakes on Python scripts..."
    
    local exit_code=0
    local count=0
    local failed=0
    
    # Check if pyflakes is available
    if ! command -v pyflakes &>/dev/null; then
        log "WARNING: pyflakes not found, falling back to python -m py_compile"
        
        while IFS= read -r -d '' script; do
            count=$((count + 1))
            log "Checking syntax: ${script#"${REPO_ROOT}/"}"
            
            if ! python3 -m py_compile "${script}"; then
                failed=$((failed + 1))
                exit_code=1
            fi
        done < <(find "${REPO_ROOT}" -name "*.py" -type f ! -path "*/.git/*" ! -path "*/node_modules/*" -print0)
    else
        while IFS= read -r -d '' script; do
            count=$((count + 1))
            log "Checking: ${script#"${REPO_ROOT}/"}"
            
            if ! pyflakes "${script}"; then
                failed=$((failed + 1))
                exit_code=1
            fi
        done < <(find "${REPO_ROOT}" -name "*.py" -type f ! -path "*/.git/*" ! -path "*/node_modules/*" -print0)
    fi
    
    log "Python syntax check complete: ${count} files checked, ${failed} failed"
    
    return ${exit_code}
}

main "$@"
