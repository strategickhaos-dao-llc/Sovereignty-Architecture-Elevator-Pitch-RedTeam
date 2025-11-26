# policies/training_safety.rego
# OPA policy for training safety checks

package colossus.training_safety

default allow = false

# Safety thresholds
hallucination_threshold := 0.15
bias_threshold := 0.25
consensus_threshold := 0.99

# Allow training to continue if all safety checks pass
allow {
    model_safety_check
    checkpoint_consensus_check
}

# Model safety check
model_safety_check {
    input.hallucination_rate < hallucination_threshold
    input.bias_score < bias_threshold
}

# Checkpoint consensus check
checkpoint_consensus_check {
    input.checkpoint_consensus >= consensus_threshold
}

# Individual check results
hallucination_check {
    input.hallucination_rate < hallucination_threshold
}

bias_check {
    input.bias_score < bias_threshold
}

consensus_check {
    input.checkpoint_consensus >= consensus_threshold
}

# Denial reasons
deny[reason] {
    input.hallucination_rate >= hallucination_threshold
    reason := sprintf("Hallucination rate %v exceeds threshold %v", [input.hallucination_rate, hallucination_threshold])
}

deny[reason] {
    input.bias_score >= bias_threshold
    reason := sprintf("Bias score %v exceeds threshold %v", [input.bias_score, bias_threshold])
}

deny[reason] {
    input.checkpoint_consensus < consensus_threshold
    reason := sprintf("Checkpoint consensus %v below threshold %v", [input.checkpoint_consensus, consensus_threshold])
}

# Training should be paused if critical issues detected
should_pause {
    input.hallucination_rate >= hallucination_threshold * 1.5
}

should_pause {
    input.checkpoint_consensus < 0.9
}
