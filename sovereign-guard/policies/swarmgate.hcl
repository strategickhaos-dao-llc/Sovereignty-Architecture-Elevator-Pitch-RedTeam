# =============================================================================
# SovereignGuard SwarmGate Financial Policy
# =============================================================================
# CRITICAL SECURITY: Protects financial trading credentials
# Exposure Mitigation: #11 (Financial Arbitrage), #12 (Paycheck Interception),
#                      #25 (Trading API Compromise), #30 (Algorithm Goes Rogue)
# Principle: Highest security - MFA required for all financial secrets
# =============================================================================

# Trading API credentials (require MFA approval)
path "secret/data/trading/*" {
  capabilities = ["read"]
  # Control groups require approval from security team
  control_group = {
    factor "security-approval" {
      identity {
        group_names = ["security-team"]
        approvals = 1
      }
    }
  }
}

# Banking credentials (require MFA approval)
path "secret/data/banking/*" {
  capabilities = ["read"]
  control_group = {
    factor "security-approval" {
      identity {
        group_names = ["security-team"]
        approvals = 1
      }
    }
  }
}

# Transaction signing (for trade verification)
path "transit/sign/swarmgate-signing" {
  capabilities = ["update"]
}

path "transit/verify/swarmgate-signing" {
  capabilities = ["update"]
}

# Read position limits configuration
path "secret/data/swarmgate/limits" {
  capabilities = ["read"]
}

# Token self-management
path "auth/token/renew-self" {
  capabilities = ["update"]
}

path "auth/token/lookup-self" {
  capabilities = ["read"]
}
