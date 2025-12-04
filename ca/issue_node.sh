#!/usr/bin/env bash
# issue_node.sh - Issue node certificate from Sovereign Swarm CA
# Part of Sovereign Swarm — Zero-Trust AI Orchestration Mesh
# Apache-2.0 License

set -euo pipefail

CA_DIR="${CA_DIR:-/opt/sovereign-swarm/ca}"
CA_STATE="${CA_DIR}/state"
CERT_DAYS="${CERT_DAYS:-365}"

log() { printf '[%s] %s\n' "$(date -u +%FT%TZ)" "$*"; }

die() { log "ERROR: $*" >&2; exit 1; }

usage() {
    cat <<EOF
Usage: $0 <node_id> [options]

Options:
    -o, --output DIR    Output directory for certificates (default: ./certs)
    -d, --days DAYS     Certificate validity in days (default: ${CERT_DAYS})
    -h, --help          Show this help message

Example:
    $0 edge1 --output /opt/sovereign-swarm/nodes/edge1/certs
EOF
    exit 1
}

issue_certificate() {
    local node_id="$1"
    local output_dir="${2:-./certs}"
    
    [[ -z "${node_id}" ]] && die "Node ID is required"
    
    [[ -f "${CA_STATE}/certs/ca.crt" ]] || die "CA not initialized. Run init_ca.sh first."
    
    mkdir -p "${output_dir}"
    
    log "Issuing certificate for node: ${node_id}"
    
    # Generate node private key
    if [[ ! -f "${output_dir}/${node_id}.key" ]]; then
        openssl genrsa -out "${output_dir}/${node_id}.key" 2048
        chmod 600 "${output_dir}/${node_id}.key"
    fi
    
    # Generate CSR
    openssl req -new \
        -key "${output_dir}/${node_id}.key" \
        -out "${output_dir}/${node_id}.csr" \
        -subj "/CN=${node_id}/O=Legion of Minds/OU=Swarm Nodes"
    
    # Sign with CA
    openssl x509 -req \
        -in "${output_dir}/${node_id}.csr" \
        -CA "${CA_STATE}/certs/ca.crt" \
        -CAkey "${CA_STATE}/private/ca.key" \
        -CAcreateserial \
        -out "${output_dir}/${node_id}.crt" \
        -days "${CERT_DAYS}"
    
    # Clean up CSR
    rm -f "${output_dir}/${node_id}.csr"
    
    # Copy CA cert for chain verification
    cp "${CA_STATE}/certs/ca.crt" "${output_dir}/ca.crt"
    
    log "Certificate issued successfully:"
    log "  Key: ${output_dir}/${node_id}.key"
    log "  Cert: ${output_dir}/${node_id}.crt"
    log "  CA: ${output_dir}/ca.crt"
}

# Parse arguments
OUTPUT_DIR="./certs"
NODE_ID=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        -o|--output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        -d|--days)
            CERT_DAYS="$2"
            shift 2
            ;;
        -h|--help)
            usage
            ;;
        *)
            NODE_ID="$1"
            shift
            ;;
    esac
done

# Main
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    issue_certificate "${NODE_ID}" "${OUTPUT_DIR}"
fi
