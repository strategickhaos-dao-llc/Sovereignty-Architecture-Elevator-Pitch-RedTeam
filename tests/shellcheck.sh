#!/usr/bin/env bash
# Run ShellCheck on all shell scripts
# Part of Sovereign Swarm — Zero-Trust AI Orchestration Mesh
# Apache-2.0 License

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "${SCRIPT_DIR}")"

log() { printf '[%s] %s\n' "$(date -u +%FT%TZ)" "$*"; }

main() {
    log "Running ShellCheck on shell scripts..."
    
    local exit_code=0
    local count=0
    local failed=0
    
    while IFS= read -r -d '' script; do
        count=$((count + 1))
        log "Checking: ${script#"${REPO_ROOT}/"}"
        
        if ! shellcheck -x -S warning "${script}"; then
            failed=$((failed + 1))
            exit_code=1
        fi
    done < <(find "${REPO_ROOT}" -name "*.sh" -type f ! -path "*/.git/*" ! -path "*/node_modules/*" -print0)
    
    log "ShellCheck complete: ${count} files checked, ${failed} failed"
    
    return ${exit_code}
}

main "$@"
