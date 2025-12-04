package guardrails

# Default deny
default approve = false

# Approve decisions from valid roles that don't contain unsafe actions
approve = true {
    valid_role(input.role)
    not unsafe_action(input.recommendation)
}

# Valid roles for board agents
valid_role(role) {
    role == "pattern_analyst"
}

valid_role(role) {
    role == "verification_node"
}

valid_role(role) {
    role == "deep_architect"
}

valid_role(role) {
    role == "boundary_enforcer"
}

# Unsafe actions - block any recommendations containing these terms
unsafe_action(rec) {
    contains(lower(rec), "hack")
}

unsafe_action(rec) {
    contains(lower(rec), "attack")
}

unsafe_action(rec) {
    contains(lower(rec), "exploit")
}

unsafe_action(rec) {
    contains(lower(rec), "bypass")
}

unsafe_action(rec) {
    contains(lower(rec), "unauthorized")
}

# Financial guardrails
approve_spending = true {
    input.amount <= 500
    input.currency == "usd"
}

# Prevent legal claims
deny_legal_claim = true {
    contains(lower(input.recommendation), "legal advice")
}

deny_legal_claim = true {
    contains(lower(input.recommendation), "attorney")
}
