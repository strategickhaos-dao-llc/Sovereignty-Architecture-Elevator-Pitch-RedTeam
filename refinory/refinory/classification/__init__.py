"""
Classification module for per-agent view access control.
Implements security classification levels and policy enforcement.
"""

from .models import (
    ClassificationLevel,
    ClassificationRank,
    ArtifactClassification,
    UserClearance,
    AccessDecision,
    AccessReason,
)
from .policy import (
    PolicyEngine,
    AccessPolicy,
    PolicyDecision,
)
from .middleware import (
    ClassificationMiddleware,
    get_current_user_clearance,
    require_clearance,
)
from .redaction import (
    RedactionEngine,
    RedactedField,
    redact_artifact,
)
from .audit import (
    AuditLogger,
    AuditEvent,
    AuditEventType,
)

__all__ = [
    # Models
    "ClassificationLevel",
    "ClassificationRank",
    "ArtifactClassification",
    "UserClearance",
    "AccessDecision",
    "AccessReason",
    # Policy
    "PolicyEngine",
    "AccessPolicy",
    "PolicyDecision",
    # Middleware
    "ClassificationMiddleware",
    "get_current_user_clearance",
    "require_clearance",
    # Redaction
    "RedactionEngine",
    "RedactedField",
    "redact_artifact",
    # Audit
    "AuditLogger",
    "AuditEvent",
    "AuditEventType",
]
