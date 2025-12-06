# =============================================================================
# SovereignGuard Admin/Operations Policy
# =============================================================================
# WARNING: Full access policy - use sparingly and with MFA
# Purpose: Emergency operations and system administration
# =============================================================================

# Full access to secrets
path "secret/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

# Database secret engine administration
path "database/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

# Policy management
path "sys/policies/acl/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

# Auth method management
path "auth/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

# Mount management
path "sys/mounts/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

# Transit secrets engine
path "transit/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

# PKI secrets engine
path "pki/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

# SSH secrets engine
path "ssh/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

# Audit log access
path "sys/audit" {
  capabilities = ["read", "list"]
}

path "sys/audit/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

# System health and metrics
path "sys/health" {
  capabilities = ["read"]
}

path "sys/metrics" {
  capabilities = ["read"]
}

# Seal/unseal operations
path "sys/seal" {
  capabilities = ["update", "sudo"]
}

path "sys/unseal" {
  capabilities = ["update", "sudo"]
}

# Leader status
path "sys/leader" {
  capabilities = ["read"]
}
