# =============================================================================
# SovereignGuard Refinory AI Agent Vault Policy
# =============================================================================
# Exposure Mitigation: #14 (Copilot Telemetry), #26 (AI Model Weights)
# Principle: Access to AI service credentials with encryption capabilities
# =============================================================================

# Read AI service credentials
path "secret/data/ai/*" {
  capabilities = ["read"]
}

# Read/update Refinory-specific secrets
path "secret/data/refinory/*" {
  capabilities = ["read", "update"]
}

# Dynamic database credentials (read-write role)
path "database/creds/refinory-rw" {
  capabilities = ["read"]
}

# Read shared secrets
path "secret/data/shared/*" {
  capabilities = ["read"]
}

# Temporal workflow secrets
path "secret/data/temporal/*" {
  capabilities = ["read"]
}

# Transit encryption for sensitive data
path "transit/encrypt/sovereignguard" {
  capabilities = ["update"]
}

path "transit/decrypt/sovereignguard" {
  capabilities = ["update"]
}

# Token self-management
path "auth/token/renew-self" {
  capabilities = ["update"]
}

path "auth/token/lookup-self" {
  capabilities = ["read"]
}
