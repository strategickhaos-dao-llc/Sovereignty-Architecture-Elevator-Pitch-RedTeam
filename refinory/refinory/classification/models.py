"""
Classification data models for security levels and access control.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, IntEnum
from typing import List, Optional, Set


class ClassificationLevel(str, Enum):
    """Security classification levels for artifacts."""
    UNCLASSIFIED = "unclassified"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    SECRET = "secret"
    TOP_SECRET = "top_secret"


class ClassificationRank(IntEnum):
    """Numeric ranking for classification levels (higher = more restricted)."""
    UNCLASSIFIED = 0
    INTERNAL = 1
    CONFIDENTIAL = 2
    SECRET = 3
    TOP_SECRET = 4

    @classmethod
    def from_level(cls, level: ClassificationLevel) -> "ClassificationRank":
        """Convert classification level to numeric rank."""
        mapping = {
            ClassificationLevel.UNCLASSIFIED: cls.UNCLASSIFIED,
            ClassificationLevel.INTERNAL: cls.INTERNAL,
            ClassificationLevel.CONFIDENTIAL: cls.CONFIDENTIAL,
            ClassificationLevel.SECRET: cls.SECRET,
            ClassificationLevel.TOP_SECRET: cls.TOP_SECRET,
        }
        return mapping[level]


class AccessReason(str, Enum):
    """Reasons for access decisions."""
    CLEARANCE_SUFFICIENT = "clearance_sufficient"
    CLEARANCE_INSUFFICIENT = "clearance_insufficient"
    NEED_TO_KNOW_GRANTED = "need_to_know_granted"
    NEED_TO_KNOW_DENIED = "need_to_know_denied"
    GROUP_ACCESS_GRANTED = "group_access_granted"
    GROUP_ACCESS_DENIED = "group_access_denied"
    POLICY_ALLOWED = "policy_allowed"
    POLICY_DENIED = "policy_denied"
    PARTIAL_ACCESS = "partial_access"


@dataclass
class ArtifactClassification:
    """Classification metadata for an artifact."""
    classification: ClassificationLevel
    need_to_know_tags: Set[str] = field(default_factory=set)
    allow_groups: Set[str] = field(default_factory=set)
    owner_id: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    classification_authority: Optional[str] = None
    declassification_date: Optional[datetime] = None
    handling_caveats: List[str] = field(default_factory=list)

    @property
    def rank(self) -> ClassificationRank:
        """Get numeric rank for this classification."""
        return ClassificationRank.from_level(self.classification)

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "classification": self.classification.value,
            "need_to_know_tags": list(self.need_to_know_tags),
            "allow_groups": list(self.allow_groups),
            "owner_id": self.owner_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "classification_authority": self.classification_authority,
            "declassification_date": (
                self.declassification_date.isoformat()
                if self.declassification_date
                else None
            ),
            "handling_caveats": self.handling_caveats,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ArtifactClassification":
        """Create from dictionary."""
        return cls(
            classification=ClassificationLevel(data["classification"]),
            need_to_know_tags=set(data.get("need_to_know_tags", [])),
            allow_groups=set(data.get("allow_groups", [])),
            owner_id=data.get("owner_id"),
            created_at=(
                datetime.fromisoformat(data["created_at"])
                if data.get("created_at")
                else datetime.now(timezone.utc)
            ),
            classification_authority=data.get("classification_authority"),
            declassification_date=(
                datetime.fromisoformat(data["declassification_date"])
                if data.get("declassification_date")
                else None
            ),
            handling_caveats=data.get("handling_caveats", []),
        )


@dataclass
class UserClearance:
    """User security clearance and access grants."""
    user_id: str
    clearance_level: ClassificationLevel
    groups: Set[str] = field(default_factory=set)
    need_to_know_grants: Set[str] = field(default_factory=set)
    roles: Set[str] = field(default_factory=set)
    issued_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: Optional[datetime] = None

    @property
    def clearance_rank(self) -> ClassificationRank:
        """Get numeric rank for user's clearance."""
        return ClassificationRank.from_level(self.clearance_level)

    def is_expired(self) -> bool:
        """Check if clearance has expired."""
        if self.expires_at is None:
            return False
        return datetime.now(timezone.utc) > self.expires_at

    def has_group(self, group: str) -> bool:
        """Check if user has a specific group membership."""
        return group in self.groups

    def has_need_to_know(self, tag: str) -> bool:
        """Check if user has a specific need-to-know grant."""
        return tag in self.need_to_know_grants

    def has_role(self, role: str) -> bool:
        """Check if user has a specific role."""
        return role in self.roles

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "user_id": self.user_id,
            "clearance_level": self.clearance_level.value,
            "groups": list(self.groups),
            "need_to_know_grants": list(self.need_to_know_grants),
            "roles": list(self.roles),
            "issued_at": self.issued_at.isoformat() if self.issued_at else None,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "UserClearance":
        """Create from dictionary."""
        return cls(
            user_id=data["user_id"],
            clearance_level=ClassificationLevel(data["clearance_level"]),
            groups=set(data.get("groups", [])),
            need_to_know_grants=set(data.get("need_to_know_grants", [])),
            roles=set(data.get("roles", [])),
            issued_at=(
                datetime.fromisoformat(data["issued_at"])
                if data.get("issued_at")
                else datetime.now(timezone.utc)
            ),
            expires_at=(
                datetime.fromisoformat(data["expires_at"])
                if data.get("expires_at")
                else None
            ),
        )

    @classmethod
    def from_jwt_claims(cls, claims: dict) -> "UserClearance":
        """Create from JWT token claims."""
        return cls(
            user_id=claims.get("sub", ""),
            clearance_level=ClassificationLevel(
                claims.get("clearance_level", "unclassified")
            ),
            groups=set(claims.get("groups", [])),
            need_to_know_grants=set(claims.get("ntk_grants", [])),
            roles=set(claims.get("roles", [])),
            issued_at=(
                datetime.fromtimestamp(claims["iat"], tz=timezone.utc)
                if "iat" in claims
                else datetime.now(timezone.utc)
            ),
            expires_at=(
                datetime.fromtimestamp(claims["exp"], tz=timezone.utc)
                if "exp" in claims
                else None
            ),
        )


@dataclass
class AccessDecision:
    """Result of an access control decision."""
    allowed: bool
    reason: AccessReason
    partial_access: bool = False
    redacted_fields: List[str] = field(default_factory=list)
    policy_ids: List[str] = field(default_factory=list)
    audit_id: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary for API response."""
        return {
            "allowed": self.allowed,
            "reason": self.reason.value,
            "partial_access": self.partial_access,
            "redacted_fields": self.redacted_fields,
            "policy_ids": self.policy_ids,
            "audit_id": self.audit_id,
        }
