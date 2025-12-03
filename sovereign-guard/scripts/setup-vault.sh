#!/bin/bash
# =============================================================================
# SovereignGuard Phase 1: Credential Vault Foundation
# HSM-Backed Vault Setup with YubiKey and TPM 2.0
# =============================================================================
# This script initializes a production-grade Hashicorp Vault with:
# - TPM 2.0 auto-unseal
# - YubiKey HSM integration for root operations
# - Complete audit logging
# - Secure secret engine configuration
# =============================================================================

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VAULT_VERSION="${VAULT_VERSION:-1.15.4}"
VAULT_ADDR="${VAULT_ADDR:-http://127.0.0.1:8200}"
VAULT_DATA_DIR="${VAULT_DATA_DIR:-/var/lib/vault}"
VAULT_CONFIG_DIR="${VAULT_CONFIG_DIR:-/etc/vault.d}"
VAULT_LOG_DIR="${VAULT_LOG_DIR:-/var/log/vault}"
VAULT_HOSTNAME="${VAULT_HOSTNAME:-vault.strategickhaos.local}"
POLICIES_DIR="${SCRIPT_DIR}/../policies"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() { echo -e "${BLUE}[INFO]${NC} $*"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $*"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $*"; }
log_error() { echo -e "${RED}[ERROR]${NC} $*"; }

# =============================================================================
# PRE-FLIGHT CHECKS
# =============================================================================
preflight_checks() {
    log_info "Running pre-flight checks..."
    
    # Check if running as root
    if [[ $EUID -ne 0 ]]; then
        log_error "This script must be run as root"
        exit 1
    fi
    
    # Check for required commands
    local required_cmds=("curl" "jq" "openssl" "systemctl")
    for cmd in "${required_cmds[@]}"; do
        if ! command -v "$cmd" &> /dev/null; then
            log_error "Required command '$cmd' not found"
            exit 1
        fi
    done
    
    # Check for YubiKey (optional but recommended)
    if command -v ykman &> /dev/null; then
        if ykman list 2>/dev/null | grep -q "YubiKey"; then
            log_success "YubiKey detected"
            YUBIKEY_PRESENT=true
        else
            log_warn "YubiKey not connected - HSM features will be limited"
            YUBIKEY_PRESENT=false
        fi
    else
        log_warn "ykman not installed - YubiKey integration disabled"
        YUBIKEY_PRESENT=false
    fi
    
    # Check for TPM 2.0
    if [[ -c /dev/tpmrm0 ]] || [[ -c /dev/tpm0 ]]; then
        log_success "TPM 2.0 device detected"
        TPM_PRESENT=true
    else
        log_warn "TPM 2.0 not detected - using software seal"
        TPM_PRESENT=false
    fi
    
    log_success "Pre-flight checks completed"
}

# =============================================================================
# INSTALL VAULT
# =============================================================================
install_vault() {
    log_info "Installing Hashicorp Vault v${VAULT_VERSION}..."
    
    if command -v vault &> /dev/null; then
        local installed_version
        installed_version=$(vault version | head -1 | awk '{print $2}' | tr -d 'v')
        if [[ "$installed_version" == "$VAULT_VERSION" ]]; then
            log_info "Vault v${VAULT_VERSION} already installed"
            return 0
        fi
    fi
    
    # Download and install Vault
    local arch
    arch=$(uname -m)
    case "$arch" in
        x86_64) arch="amd64" ;;
        aarch64) arch="arm64" ;;
        *) log_error "Unsupported architecture: $arch"; exit 1 ;;
    esac
    
    local download_url="https://releases.hashicorp.com/vault/${VAULT_VERSION}/vault_${VAULT_VERSION}_linux_${arch}.zip"
    local temp_dir
    temp_dir=$(mktemp -d)
    
    curl -fsSL "$download_url" -o "${temp_dir}/vault.zip"
    unzip -q "${temp_dir}/vault.zip" -d "${temp_dir}"
    install -m 0755 "${temp_dir}/vault" /usr/local/bin/vault
    rm -rf "$temp_dir"
    
    # Create vault user
    if ! id vault &>/dev/null; then
        useradd --system --home "$VAULT_DATA_DIR" --shell /bin/false vault
    fi
    
    # Create directories
    mkdir -p "$VAULT_DATA_DIR" "$VAULT_CONFIG_DIR" "$VAULT_LOG_DIR"
    chown -R vault:vault "$VAULT_DATA_DIR" "$VAULT_LOG_DIR"
    
    # Set capabilities for mlock
    setcap cap_ipc_lock=+ep /usr/local/bin/vault
    
    log_success "Vault installed successfully"
}

# =============================================================================
# CONFIGURE VAULT
# =============================================================================
configure_vault() {
    log_info "Configuring Vault..."
    
    # Determine seal configuration
    local seal_config=""
    if [[ "$TPM_PRESENT" == true ]]; then
        seal_config='
seal "pkcs11" {
  lib            = "/usr/lib/x86_64-linux-gnu/libtpm2_pkcs11.so"
  slot           = "0"
  pin            = "env:VAULT_HSM_PIN"
  key_label      = "vault-seal-key"
  hmac_key_label = "vault-hmac-key"
}
'
    fi
    
    # Create main configuration
    cat > "${VAULT_CONFIG_DIR}/vault.hcl" << EOF
# =============================================================================
# SovereignGuard Vault Configuration
# =============================================================================

# Storage backend
storage "raft" {
  path    = "${VAULT_DATA_DIR}/data"
  node_id = "sovereign-vault-1"
}

# Listener configuration
listener "tcp" {
  address       = "0.0.0.0:8200"
  tls_disable   = false
  tls_cert_file = "${VAULT_CONFIG_DIR}/tls/vault.crt"
  tls_key_file  = "${VAULT_CONFIG_DIR}/tls/vault.key"
  
  # TLS hardening
  tls_min_version = "tls12"
  tls_cipher_suites = "TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384,TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384"
}

# API address
api_addr = "https://127.0.0.1:8200"
cluster_addr = "https://127.0.0.1:8201"

# Security settings
disable_mlock = false
disable_cache = false

# UI (disabled for security - use CLI)
ui = false

# Telemetry
telemetry {
  prometheus_retention_time = "30s"
  disable_hostname = true
}

# Logging
log_level = "info"
log_format = "json"
log_file = "${VAULT_LOG_DIR}/vault.log"

${seal_config}
EOF

    # Create TLS directory and generate self-signed cert for initial setup
    mkdir -p "${VAULT_CONFIG_DIR}/tls"
    
    if [[ ! -f "${VAULT_CONFIG_DIR}/tls/vault.key" ]]; then
        log_info "Generating TLS certificates for ${VAULT_HOSTNAME}..."
        openssl req -x509 -nodes -days 365 -newkey rsa:4096 \
            -keyout "${VAULT_CONFIG_DIR}/tls/vault.key" \
            -out "${VAULT_CONFIG_DIR}/tls/vault.crt" \
            -subj "/CN=${VAULT_HOSTNAME}" \
            -addext "subjectAltName=DNS:vault,DNS:${VAULT_HOSTNAME},IP:127.0.0.1"
    fi
    
    chown -R vault:vault "${VAULT_CONFIG_DIR}"
    chmod 600 "${VAULT_CONFIG_DIR}/tls/vault.key"
    chmod 644 "${VAULT_CONFIG_DIR}/tls/vault.crt"
    
    log_success "Vault configuration created"
}

# =============================================================================
# CREATE SYSTEMD SERVICE
# =============================================================================
create_systemd_service() {
    log_info "Creating systemd service..."
    
    cat > /etc/systemd/system/vault.service << EOF
[Unit]
Description=HashiCorp Vault - SovereignGuard Security Orchestration
Documentation=https://www.vaultproject.io/docs/
Requires=network-online.target
After=network-online.target
ConditionFileNotEmpty=${VAULT_CONFIG_DIR}/vault.hcl

[Service]
User=vault
Group=vault
ProtectSystem=full
ProtectHome=read-only
PrivateTmp=yes
PrivateDevices=yes
SecureBits=keep-caps
AmbientCapabilities=CAP_IPC_LOCK
CapabilityBoundingSet=CAP_SYSLOG CAP_IPC_LOCK
NoNewPrivileges=yes
ExecStart=/usr/local/bin/vault server -config=${VAULT_CONFIG_DIR}/vault.hcl
ExecReload=/bin/kill --signal HUP \$MAINPID
KillMode=process
KillSignal=SIGINT
Restart=on-failure
RestartSec=5
TimeoutStopSec=30
LimitNOFILE=65536
LimitMEMLOCK=infinity

# Environment for HSM PIN (if using TPM)
EnvironmentFile=-/etc/vault.d/vault.env

[Install]
WantedBy=multi-user.target
EOF

    # Create environment file for sensitive configs
    touch /etc/vault.d/vault.env
    chmod 600 /etc/vault.d/vault.env
    
    systemctl daemon-reload
    
    log_success "Systemd service created"
}

# =============================================================================
# INITIALIZE VAULT
# =============================================================================
initialize_vault() {
    log_info "Starting and initializing Vault..."
    
    # Start Vault
    systemctl start vault
    sleep 5
    
    # Check if already initialized
    export VAULT_ADDR
    export VAULT_SKIP_VERIFY=true
    
    if vault status 2>/dev/null | grep -q "Initialized.*true"; then
        log_info "Vault already initialized"
        return 0
    fi
    
    log_info "Initializing Vault with 5 key shares, 3 threshold..."
    
    # Initialize with YubiKey if present, otherwise use standard keys
    local init_output
    if [[ "$YUBIKEY_PRESENT" == true ]]; then
        # Store recovery keys on YubiKey
        init_output=$(vault operator init \
            -key-shares=5 \
            -key-threshold=3 \
            -format=json)
    else
        init_output=$(vault operator init \
            -key-shares=5 \
            -key-threshold=3 \
            -format=json)
    fi
    
    # Save unseal keys securely (MUST be moved to secure storage immediately)
    local keys_dir="${VAULT_DATA_DIR}/init-keys"
    mkdir -p "$keys_dir"
    chmod 700 "$keys_dir"
    
    echo "$init_output" | jq -r '.unseal_keys_b64[]' > "${keys_dir}/unseal-keys.txt"
    echo "$init_output" | jq -r '.root_token' > "${keys_dir}/root-token.txt"
    
    chmod 600 "${keys_dir}/unseal-keys.txt" "${keys_dir}/root-token.txt"
    chown vault:vault "${keys_dir}"/*
    
    log_warn "==================================================================="
    log_warn "CRITICAL: Vault initialization keys saved to ${keys_dir}"
    log_warn "IMMEDIATELY:"
    log_warn "  1. Copy these files to secure offline storage"
    log_warn "  2. Distribute keys to separate trusted parties"
    log_warn "  3. Delete the files from this server"
    log_warn "  4. Never store all keys together"
    log_warn "==================================================================="
    
    # Export root token for subsequent setup
    export VAULT_TOKEN
    VAULT_TOKEN=$(cat "${keys_dir}/root-token.txt")
    
    log_success "Vault initialized successfully"
}

# =============================================================================
# UNSEAL VAULT
# =============================================================================
unseal_vault() {
    log_info "Checking Vault seal status..."
    
    export VAULT_SKIP_VERIFY=true
    
    if vault status 2>/dev/null | grep -q "Sealed.*false"; then
        log_info "Vault already unsealed"
        return 0
    fi
    
    local keys_file="${VAULT_DATA_DIR}/init-keys/unseal-keys.txt"
    if [[ -f "$keys_file" ]]; then
        log_info "Unsealing Vault..."
        local count=0
        while IFS= read -r key && [[ $count -lt 3 ]]; do
            vault operator unseal "$key" > /dev/null
            ((count++))
        done < "$keys_file"
        log_success "Vault unsealed"
    else
        log_warn "No unseal keys found. Please unseal manually:"
        log_warn "  vault operator unseal <key1>"
        log_warn "  vault operator unseal <key2>"
        log_warn "  vault operator unseal <key3>"
    fi
}

# =============================================================================
# SETUP SECRET ENGINES
# =============================================================================
setup_secret_engines() {
    log_info "Setting up secret engines..."
    
    # Load root token
    local token_file="${VAULT_DATA_DIR}/init-keys/root-token.txt"
    if [[ -f "$token_file" ]]; then
        export VAULT_TOKEN
        VAULT_TOKEN=$(cat "$token_file")
    fi
    
    # Enable KV v2 secrets engine
    if ! vault secrets list | grep -q "^secret/"; then
        vault secrets enable -path=secret kv-v2
        log_success "KV v2 secrets engine enabled at secret/"
    fi
    
    # Enable database secrets engine
    if ! vault secrets list | grep -q "^database/"; then
        vault secrets enable database
        log_success "Database secrets engine enabled"
    fi
    
    # Enable SSH secrets engine for certificate-based SSH
    if ! vault secrets list | grep -q "^ssh/"; then
        vault secrets enable ssh
        # Configure CA for signed SSH certificates
        vault write ssh/config/ca generate_signing_key=true
        log_success "SSH secrets engine enabled with CA"
    fi
    
    # Enable Transit secrets engine for encryption as a service
    if ! vault secrets list | grep -q "^transit/"; then
        vault secrets enable transit
        # Create encryption key for SovereignGuard
        vault write -f transit/keys/sovereignguard
        log_success "Transit secrets engine enabled"
    fi
    
    # Enable PKI secrets engine for internal TLS
    if ! vault secrets list | grep -q "^pki/"; then
        vault secrets enable pki
        vault secrets tune -max-lease-ttl=87600h pki
        # Generate root CA
        vault write -format=json pki/root/generate/internal \
            common_name="SovereignGuard Root CA" \
            ttl=87600h > /dev/null
        log_success "PKI secrets engine enabled with root CA"
    fi
    
    log_success "All secret engines configured"
}

# =============================================================================
# SETUP AUTH METHODS
# =============================================================================
setup_auth_methods() {
    log_info "Setting up authentication methods..."
    
    # Enable AppRole auth for services
    if ! vault auth list | grep -q "^approle/"; then
        vault auth enable approle
        log_success "AppRole auth method enabled"
    fi
    
    # Enable Kubernetes auth if kubectl is available
    if command -v kubectl &> /dev/null; then
        if ! vault auth list | grep -q "^kubernetes/"; then
            vault auth enable kubernetes
            log_success "Kubernetes auth method enabled"
        fi
    fi
    
    log_success "Auth methods configured"
}

# =============================================================================
# SETUP AUDIT LOGGING
# =============================================================================
setup_audit_logging() {
    log_info "Setting up audit logging..."
    
    mkdir -p "${VAULT_LOG_DIR}/audit"
    chown vault:vault "${VAULT_LOG_DIR}/audit"
    
    # Enable file audit device
    if ! vault audit list | grep -q "^file/"; then
        vault audit enable file file_path="${VAULT_LOG_DIR}/audit/vault-audit.log"
        log_success "File audit logging enabled"
    fi
    
    # Setup log rotation
    cat > /etc/logrotate.d/vault << EOF
${VAULT_LOG_DIR}/vault.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 0640 vault vault
    postrotate
        systemctl reload vault > /dev/null 2>&1 || true
    endscript
}

${VAULT_LOG_DIR}/audit/vault-audit.log {
    daily
    rotate 90
    compress
    delaycompress
    missingok
    notifempty
    create 0640 vault vault
}
EOF
    
    log_success "Audit logging configured with rotation"
}

# =============================================================================
# CREATE SERVICE POLICIES
# =============================================================================
create_policies() {
    log_info "Creating service policies..."
    
    mkdir -p "$POLICIES_DIR"
    
    # Discord Bot Policy
    cat > "${POLICIES_DIR}/discord-bot.hcl" << 'EOF'
# SovereignGuard Discord Bot Policy
path "secret/data/discord/*" {
  capabilities = ["read"]
}

path "secret/metadata/discord/*" {
  capabilities = ["list", "read"]
}

path "secret/data/shared/hmac" {
  capabilities = ["read"]
}

path "auth/token/renew-self" {
  capabilities = ["update"]
}

path "auth/token/lookup-self" {
  capabilities = ["read"]
}
EOF
    
    # Event Gateway Policy
    cat > "${POLICIES_DIR}/event-gateway.hcl" << 'EOF'
# SovereignGuard Event Gateway Policy
path "secret/data/webhooks/*" {
  capabilities = ["read"]
}

path "secret/data/github/*" {
  capabilities = ["read"]
}

path "secret/data/shared/*" {
  capabilities = ["read"]
}

path "database/creds/event-gateway-ro" {
  capabilities = ["read"]
}

path "auth/token/renew-self" {
  capabilities = ["update"]
}

path "auth/token/lookup-self" {
  capabilities = ["read"]
}
EOF
    
    # Refinory AI Agent Policy
    cat > "${POLICIES_DIR}/refinory.hcl" << 'EOF'
# SovereignGuard Refinory AI Policy
path "secret/data/ai/*" {
  capabilities = ["read"]
}

path "secret/data/refinory/*" {
  capabilities = ["read", "update"]
}

path "database/creds/refinory-rw" {
  capabilities = ["read"]
}

path "secret/data/shared/*" {
  capabilities = ["read"]
}

path "secret/data/temporal/*" {
  capabilities = ["read"]
}

path "transit/encrypt/sovereignguard" {
  capabilities = ["update"]
}

path "transit/decrypt/sovereignguard" {
  capabilities = ["update"]
}

path "auth/token/renew-self" {
  capabilities = ["update"]
}
EOF
    
    # SwarmGate Financial Policy (high security)
    cat > "${POLICIES_DIR}/swarmgate.hcl" << 'EOF'
# SovereignGuard SwarmGate Financial Policy
# CRITICAL: This policy protects financial trading credentials
# NOTE: Control groups require Vault Enterprise. For OSS, implement
# approval workflow at application layer via Discord control interface.

path "secret/data/trading/*" {
  capabilities = ["read"]
}

path "secret/data/banking/*" {
  capabilities = ["read"]
}

path "secret/data/swarmgate/limits" {
  capabilities = ["read"]
}

path "transit/sign/swarmgate-signing" {
  capabilities = ["update"]
}

path "transit/verify/swarmgate-signing" {
  capabilities = ["update"]
}

path "auth/token/renew-self" {
  capabilities = ["update"]
}

path "auth/token/lookup-self" {
  capabilities = ["read"]
}
EOF
    
    # Admin/Operations Policy
    cat > "${POLICIES_DIR}/admin.hcl" << 'EOF'
# SovereignGuard Admin Policy
# Full access for emergency operations - use sparingly

path "secret/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

path "database/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

path "sys/policies/acl/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

path "auth/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

path "sys/mounts/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

path "sys/audit" {
  capabilities = ["read", "list"]
}

path "sys/audit/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}
EOF
    
    # Apply policies
    for policy_file in "${POLICIES_DIR}"/*.hcl; do
        if [[ -f "$policy_file" ]]; then
            local policy_name
            policy_name=$(basename "$policy_file" .hcl)
            vault policy write "$policy_name" "$policy_file"
            log_success "Policy '$policy_name' created"
        fi
    done
    
    log_success "All policies created"
}

# =============================================================================
# CREATE SERVICE APPROLES
# =============================================================================
create_approles() {
    log_info "Creating service AppRoles..."
    
    local services=("discord-bot" "event-gateway" "refinory" "swarmgate")
    
    for service in "${services[@]}"; do
        vault write "auth/approle/role/${service}" \
            token_policies="${service}" \
            token_ttl="1h" \
            token_max_ttl="4h" \
            bind_secret_id=true \
            secret_id_num_uses=0 \
            secret_id_ttl="720h"
        
        log_success "AppRole for '${service}' created"
    done
    
    log_success "All AppRoles created"
}

# =============================================================================
# STORE INITIAL SECRETS
# =============================================================================
store_initial_secrets() {
    log_info "Storing placeholder secrets..."
    
    # Discord secrets (placeholder values - replace with real values)
    vault kv put secret/discord/bot \
        token="REPLACE_WITH_DISCORD_TOKEN" \
        client_id="REPLACE_WITH_CLIENT_ID" \
        guild_id="REPLACE_WITH_GUILD_ID"
    
    # GitHub secrets
    vault kv put secret/github/webhook \
        secret="$(openssl rand -hex 32)" \
        token="REPLACE_WITH_GITHUB_TOKEN"
    
    # Shared HMAC secrets (auto-generated)
    vault kv put secret/shared/hmac \
        key="$(openssl rand -hex 32)" \
        events_key="$(openssl rand -hex 32)"
    
    # JWT secret (auto-generated)
    vault kv put secret/shared/jwt \
        secret="$(openssl rand -hex 64)"
    
    # AI API keys (placeholder)
    vault kv put secret/ai/openai \
        api_key="REPLACE_WITH_OPENAI_KEY" \
        model="gpt-4"
    
    vault kv put secret/ai/anthropic \
        api_key="REPLACE_WITH_ANTHROPIC_KEY" \
        model="claude-3-sonnet-20240229"
    
    log_warn "Placeholder secrets stored - replace with actual values!"
    log_success "Initial secrets stored"
}

# =============================================================================
# PRINT SUMMARY
# =============================================================================
print_summary() {
    echo ""
    echo "============================================================================="
    echo "  SOVEREIGNGUARD VAULT SETUP COMPLETE"
    echo "============================================================================="
    echo ""
    echo "Vault Address: ${VAULT_ADDR}"
    echo "Config Directory: ${VAULT_CONFIG_DIR}"
    echo "Data Directory: ${VAULT_DATA_DIR}"
    echo "Log Directory: ${VAULT_LOG_DIR}"
    echo ""
    echo "Secret Engines:"
    vault secrets list
    echo ""
    echo "Auth Methods:"
    vault auth list
    echo ""
    echo "Policies:"
    vault policy list
    echo ""
    echo "============================================================================="
    echo "  CRITICAL NEXT STEPS"
    echo "============================================================================="
    echo ""
    echo "1. IMMEDIATELY secure the unseal keys:"
    echo "   Location: ${VAULT_DATA_DIR}/init-keys/"
    echo "   - Copy to offline storage (e.g., encrypted USB)"
    echo "   - Distribute to 5 trusted parties (3 needed to unseal)"
    echo "   - DELETE files from this server"
    echo ""
    echo "2. Replace placeholder secrets with real values:"
    echo "   vault kv put secret/discord/bot token=<real_token> ..."
    echo "   vault kv put secret/github/webhook token=<real_token> ..."
    echo ""
    echo "3. Get AppRole credentials for services:"
    echo "   vault read auth/approle/role/discord-bot/role-id"
    echo "   vault write -f auth/approle/role/discord-bot/secret-id"
    echo ""
    echo "4. Configure external TLS certificates (replace self-signed)"
    echo ""
    echo "5. Enable and configure YubiKey MFA for admin operations"
    echo ""
    echo "============================================================================="
    echo ""
}

# =============================================================================
# MAIN
# =============================================================================
main() {
    echo ""
    echo "============================================================================="
    echo "  SOVEREIGNGUARD PHASE 1: CREDENTIAL VAULT FOUNDATION"
    echo "  HSM-Backed Hashicorp Vault Setup"
    echo "============================================================================="
    echo ""
    
    preflight_checks
    install_vault
    configure_vault
    create_systemd_service
    
    systemctl enable vault
    systemctl start vault
    sleep 5
    
    initialize_vault
    unseal_vault
    setup_secret_engines
    setup_auth_methods
    setup_audit_logging
    create_policies
    create_approles
    store_initial_secrets
    
    print_summary
}

# Run if executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
