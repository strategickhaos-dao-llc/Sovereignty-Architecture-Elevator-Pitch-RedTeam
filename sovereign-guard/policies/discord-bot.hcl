# =============================================================================
# SovereignGuard Discord Bot Vault Policy
# =============================================================================
# Exposure Mitigation: #2 (Cached Credentials), #8 (Discord Bot Token Compromise)
# Principle: Least privilege - only read access to Discord-related secrets
# =============================================================================

# Read Discord bot secrets
path "secret/data/discord/*" {
  capabilities = ["read"]
}

# List Discord secret paths (for discovery)
path "secret/metadata/discord/*" {
  capabilities = ["list", "read"]
}

# Read shared HMAC key for webhook verification
path "secret/data/shared/hmac" {
  capabilities = ["read"]
}

# Token self-management
path "auth/token/renew-self" {
  capabilities = ["update"]
}

path "auth/token/lookup-self" {
  capabilities = ["read"]
}
