# =============================================================================
# SovereignGuard Event Gateway Vault Policy
# =============================================================================
# Exposure Mitigation: #7 (GitHub → ADO Pipeline), #19 (Supply Chain via Actions)
# Principle: Read-only access to webhook and GitHub integration secrets
# =============================================================================

# Read webhook secrets
path "secret/data/webhooks/*" {
  capabilities = ["read"]
}

# Read GitHub integration secrets
path "secret/data/github/*" {
  capabilities = ["read"]
}

# Read shared secrets (HMAC, etc.)
path "secret/data/shared/*" {
  capabilities = ["read"]
}

# Dynamic database credentials (read-only role)
path "database/creds/event-gateway-ro" {
  capabilities = ["read"]
}

# Token self-management
path "auth/token/renew-self" {
  capabilities = ["update"]
}

path "auth/token/lookup-self" {
  capabilities = ["read"]
}
