# /vault/policies/ghost7.hcl
# KLARK CLIENT — Portable Sovereign Field Node v2 GHOST-7 Vault Policy
# Classification: SOVEREIGN-ENCRYPTED
# Requires: Yubikey 5C NFC + passphrase + TPM2 attestation

# Read access to GHOST-7 configuration secrets
path "secret/data/ghost7/*" {
  capabilities = ["read", "update"]
}

# Read access to cryptographic keys
path "secret/data/ghost7/keys/*" {
  capabilities = ["read"]
}

# Emergency access (requires MFA + dual approval)
path "secret/data/ghost7/emergency/*" {
  capabilities = ["read"]
  # Requires identity/mfa/method_id/totp
}

# Satellite uplink credentials
path "secret/data/ghost7/uplinks/*" {
  capabilities = ["read"]
}

# DAO identity and signing keys
path "secret/data/ghost7/dao/*" {
  capabilities = ["read", "update"]
}

# Temporal workflow secrets
path "secret/data/ghost7/temporal/*" {
  capabilities = ["read"]
}

# Legal entity credentials
path "secret/data/ghost7/legal/*" {
  capabilities = ["read"]
}

# Boot chain verification keys
path "secret/data/ghost7/boot/*" {
  capabilities = ["read"]
}

# Auth token self-renewal
path "auth/token/renew-self" {
  capabilities = ["update"]
}

# Token lookup (for health checks)
path "auth/token/lookup-self" {
  capabilities = ["read"]
}
