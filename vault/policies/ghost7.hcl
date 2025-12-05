# /vault/policies/ghost7.hcl
# KLARK CLIENT — Portable Sovereign Field Node v2 GHOST-7 Vault Policy
# Classification: SOVEREIGN-ENCRYPTED
# Requires: Yubikey 5C NFC + passphrase + TPM2 attestation

# Read-only access to GHOST-7 configuration secrets (default)
path "secret/data/ghost7/config/*" {
  capabilities = ["read"]
}

# Read access to cryptographic keys (most sensitive, read-only)
path "secret/data/ghost7/keys/*" {
  capabilities = ["read"]
}

# Emergency access path - read-only
# MFA Enforcement: This path requires additional MFA validation
# Configure via: vault write sys/mfa/method/totp/ghost7-emergency ...
# Bind via: vault write identity/mfa/login-enforcement/ghost7-emergency ...
path "secret/data/ghost7/emergency/*" {
  capabilities = ["read"]
}

# Satellite uplink credentials - read-only
path "secret/data/ghost7/uplinks/*" {
  capabilities = ["read"]
}

# DAO identity signing - requires update for key rotation
path "secret/data/ghost7/dao/identity" {
  capabilities = ["read"]
}

# DAO signing state - update allowed for state management
path "secret/data/ghost7/dao/state" {
  capabilities = ["read", "update"]
}

# Temporal workflow secrets - read-only
path "secret/data/ghost7/temporal/*" {
  capabilities = ["read"]
}

# Legal entity credentials - read-only
path "secret/data/ghost7/legal/*" {
  capabilities = ["read"]
}

# Boot chain verification keys - read-only
path "secret/data/ghost7/boot/*" {
  capabilities = ["read"]
}

# Resurrection state - update allowed for self-healing
path "secret/data/ghost7/resurrection/state" {
  capabilities = ["read", "update"]
}

# Auth token self-renewal
path "auth/token/renew-self" {
  capabilities = ["update"]
}

# Token lookup (for health checks)
path "auth/token/lookup-self" {
  capabilities = ["read"]
}
