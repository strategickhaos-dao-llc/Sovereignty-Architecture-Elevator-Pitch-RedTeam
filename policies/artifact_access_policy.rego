package artifact.access

default allow = false
default redacted = false

classification_rank := {
    "Unclassified": 0,
    "Internal": 1,
    "Confidential": 2,
    "Secret": 3,
    "Top-Secret": 4,
}

rank := classification_rank[input.artifact.classification]

allow {
    input.user.clearance_level >= rank
    count(input.artifact.need_to_know) == 0
}

allow {
    input.user.clearance_level >= rank
    count(intersect(input.user.groups, input.artifact.need_to_know)) > 0
}

redacted {
    not allow
    input.user.clearance_level >= rank - 1
}

reason := "full clearance and NTK satisfied" { allow }
reason := "partial clearance – redacted preview" { redacted }
reason := "insufficient clearance or NTK" { not allow; not redacted }
