#!/usr/bin/env bash
# generate_docs.sh - Generate documentation for Sovereign Swarm
# Part of Sovereign Swarm — Zero-Trust AI Orchestration Mesh
# Apache-2.0 License

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "${SCRIPT_DIR}")"
DOCS_DIR="${REPO_ROOT}/docs"

log() { printf '[%s] %s\n' "$(date -u +%FT%TZ)" "$*"; }

generate_script_docs() {
    log "Generating script documentation..."
    
    local output="${DOCS_DIR}/SCRIPTS.md"
    
    cat > "${output}" <<EOF
# Script Reference

Auto-generated documentation for Sovereign Swarm scripts.

Generated: $(date -u +%FT%TZ)

## Shell Scripts

EOF
    
    # Document shell scripts
    while IFS= read -r -d '' script; do
        local name
        name=$(basename "${script}")
        log "  Processing: ${name}"
        
        cat >> "${output}" <<EOF
### ${name}

\`\`\`
$(head -20 "${script}" | grep '^#' | sed 's/^#\s*//' || true)
\`\`\`

EOF
    done < <(find "${REPO_ROOT}" -name "*.sh" -type f ! -path "*/.git/*" -print0 | sort -z)
    
    cat >> "${output}" <<EOF

## Python Scripts

EOF
    
    # Document Python scripts
    while IFS= read -r -d '' script; do
        local name
        name=$(basename "${script}")
        log "  Processing: ${name}"
        
        cat >> "${output}" <<EOF
### ${name}

\`\`\`
$(head -20 "${script}" | grep '^#\|^"""' | sed 's/^#\s*//' | sed 's/"""//g' || true)
\`\`\`

EOF
    done < <(find "${REPO_ROOT}/scripts" -name "*.py" -type f -print0 2>/dev/null | sort -z)
    
    log "Script documentation generated: ${output}"
}

generate_config_docs() {
    log "Generating configuration documentation..."
    
    local output="${DOCS_DIR}/CONFIGURATION.md"
    
    cat > "${output}" <<EOF
# Configuration Reference

Auto-generated documentation for Sovereign Swarm configuration templates.

Generated: $(date -u +%FT%TZ)

## Environment Variables

The following environment variables can be used to customize deployments:

| Variable | Default | Description |
|----------|---------|-------------|
| NODE_ID | command0 | Unique node identifier |
| SWARM_DOMAIN | localhost | Primary swarm domain |
| WG_PORT | 51820 | WireGuard listen port |
| NATS_PORT | 4222 | NATS listen port |
| MATRIX_PORT | 8008 | Matrix Synapse port |
| CA_DIR | /opt/sovereign-swarm/ca | CA directory |

## Configuration Templates

EOF
    
    # Document templates
    while IFS= read -r -d '' template; do
        local name
        name=$(basename "${template}")
        local dir
        dir=$(basename "$(dirname "${template}")")
        log "  Processing: ${dir}/${name}"
        
        cat >> "${output}" <<EOF
### ${dir}/${name}

\`\`\`
$(head -30 "${template}" || true)
\`\`\`

EOF
    done < <(find "${REPO_ROOT}" -name "*.tmpl" -type f ! -path "*/.git/*" -print0 | sort -z)
    
    log "Configuration documentation generated: ${output}"
}

main() {
    log "Starting documentation generation..."
    
    mkdir -p "${DOCS_DIR}"
    
    generate_script_docs
    generate_config_docs
    
    log "Documentation generation complete."
}

main "$@"
