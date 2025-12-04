#!/usr/bin/env bash
# init_ca.sh - Initialize Certificate Authority for Sovereign Swarm
# Part of Sovereign Swarm — Zero-Trust AI Orchestration Mesh
# Apache-2.0 License

set -euo pipefail

CA_DIR="${CA_DIR:-/opt/sovereign-swarm/ca}"
CA_STATE="${CA_DIR}/state"
CA_DAYS="${CA_DAYS:-3650}"

log() { printf '[%s] %s\n' "$(date -u +%FT%TZ)" "$*"; }

die() { log "ERROR: $*" >&2; exit 1; }

init_ca() {
    log "Initializing Sovereign Swarm CA..."
    
    mkdir -p "${CA_STATE}"/{certs,newcerts,private}
    chmod 700 "${CA_STATE}/private"
    
    if [[ ! -f "${CA_STATE}/serial" ]]; then
        echo "01" > "${CA_STATE}/serial"
    fi
    
    if [[ ! -f "${CA_STATE}/index.txt" ]]; then
        touch "${CA_STATE}/index.txt"
    fi
    
    # Generate CA private key if not exists
    if [[ ! -f "${CA_STATE}/private/ca.key" ]]; then
        log "Generating CA private key..."
        openssl genrsa -out "${CA_STATE}/private/ca.key" 4096
        chmod 600 "${CA_STATE}/private/ca.key"
    fi
    
    # Generate CA certificate if not exists
    if [[ ! -f "${CA_STATE}/certs/ca.crt" ]]; then
        log "Generating CA certificate..."
        openssl req -new -x509 \
            -key "${CA_STATE}/private/ca.key" \
            -out "${CA_STATE}/certs/ca.crt" \
            -days "${CA_DAYS}" \
            -subj "/CN=Sovereign Swarm CA/O=Legion of Minds/OU=Infrastructure"
    fi
    
    log "CA initialization complete."
    log "CA Certificate: ${CA_STATE}/certs/ca.crt"
}

# Main
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    init_ca "$@"
fi
