# =============================================================================
# SovereignGuard SwarmGate Financial Policy
# =============================================================================
# CRITICAL SECURITY: Protects financial trading credentials
# Exposure Mitigation: #11 (Financial Arbitrage), #12 (Paycheck Interception),
#                      #25 (Trading API Compromise), #30 (Algorithm Goes Rogue)
# Principle: Highest security for financial operations
# NOTE: MFA/approval workflows implemented at application layer via Discord
#       control interface since control_group requires Vault Enterprise.
# =============================================================================

# Trading API credentials
path "secret/data/trading/*" {
  capabilities = ["read"]
}

# Banking credentials
path "secret/data/banking/*" {
  capabilities = ["read"]
}

# Position limits configuration
path "secret/data/swarmgate/limits" {
  capabilities = ["read"]
}

# Transaction signing (for trade verification)
path "transit/sign/swarmgate-signing" {
  capabilities = ["update"]
}

path "transit/verify/swarmgate-signing" {
  capabilities = ["update"]
}

# Token self-management
path "auth/token/renew-self" {
  capabilities = ["update"]
}

path "auth/token/lookup-self" {
  capabilities = ["read"]
}
