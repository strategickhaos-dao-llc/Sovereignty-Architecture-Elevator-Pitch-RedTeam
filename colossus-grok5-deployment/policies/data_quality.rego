# policies/data_quality.rego
# OPA policy for data quality validation in Grok-5 training pipeline

package colossus.data_quality

default allow = false

# Allow data if all quality checks pass
allow {
    input.toxicity <= 0.30
    input.lang == "en"
    count(input.text) > 0
}

# Detailed check for toxicity threshold
toxicity_check {
    input.toxicity <= 0.30
}

# Detailed check for language requirement
language_check {
    input.lang == "en"
}

# Detailed check for non-empty content
content_check {
    count(input.text) > 0
}

# Provide detailed denial reasons
deny[reason] {
    input.toxicity > 0.30
    reason := sprintf("Toxicity score %v exceeds threshold 0.30", [input.toxicity])
}

deny[reason] {
    input.lang != "en"
    reason := sprintf("Language '%v' is not 'en'", [input.lang])
}

deny[reason] {
    count(input.text) == 0
    reason := "Text content is empty"
}
