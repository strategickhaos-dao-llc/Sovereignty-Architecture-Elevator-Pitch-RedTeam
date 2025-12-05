# policies/deployment_approval.rego
# OPA policy for deployment approval workflow

package colossus.deployment_approval

default allow = false

# Required approvals for production deployment
required_approvers := ["release_manager", "safety_lead", "infrastructure_lead"]

# Allow deployment if all gates pass
allow {
    safety_gate_passed
    energy_gate_passed
    provenance_verified
    all_approvals_present
}

# Safety gate check
safety_gate_passed {
    input.safety_report.ok == true
}

# Energy gate check
energy_gate_passed {
    input.power_mw <= 250
    input.megapack_soc >= 0.4
}

# Provenance verification
provenance_verified {
    input.provenance.merkle_root_valid == true
    input.provenance.ots_verified == true
}

# Check all required approvals
all_approvals_present {
    count(missing_approvers) == 0
}

# Find missing approvers
missing_approvers[approver] {
    approver := required_approvers[_]
    not input.approvals[_] == approver
}

# Emergency override (requires additional approval)
allow_emergency {
    input.emergency_override == true
    input.approvals[_] == "cto"
    input.approvals[_] == "safety_lead"
}

# Denial reasons
deny[reason] {
    not safety_gate_passed
    reason := "Safety gate check failed"
}

deny[reason] {
    not energy_gate_passed
    reason := "Energy gate check failed"
}

deny[reason] {
    not provenance_verified
    reason := "Provenance verification failed"
}

deny[reason] {
    missing := missing_approvers
    count(missing) > 0
    reason := sprintf("Missing approvals from: %v", [missing])
}

# Deployment checklist
checklist := {
    "safety_gate": safety_gate_passed,
    "energy_gate": energy_gate_passed,
    "provenance": provenance_verified,
    "approvals": all_approvals_present,
}

# Deployment readiness score
readiness_score = score {
    passed := count([x | checklist[_] == true; x := 1])
    total := count(checklist)
    score := passed / total
}
