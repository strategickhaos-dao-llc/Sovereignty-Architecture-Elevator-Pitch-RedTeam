"""
Policy engine for classification-based access control.
Implements ABAC (Attribute-Based Access Control) with clearance-level checks.
"""

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set

import structlog

from .models import (
    AccessDecision,
    AccessReason,
    ArtifactClassification,
    ClassificationRank,
    UserClearance,
)

logger = structlog.get_logger()


class PolicyEffect(str, Enum):
    """Policy evaluation result."""
    ALLOW = "allow"
    DENY = "deny"
    PARTIAL = "partial"


@dataclass
class PolicyCondition:
    """A condition that must be met for a policy to apply."""
    attribute: str
    operator: str
    value: Any

    def evaluate(self, context: Dict[str, Any]) -> bool:
        """Evaluate condition against context."""
        actual = self._get_nested_value(context, self.attribute)
        if actual is None:
            return self.operator == "is_none"

        if self.operator == "eq":
            return actual == self.value
        elif self.operator == "ne":
            return actual != self.value
        elif self.operator == "gt":
            return actual > self.value
        elif self.operator == "gte":
            return actual >= self.value
        elif self.operator == "lt":
            return actual < self.value
        elif self.operator == "lte":
            return actual <= self.value
        elif self.operator == "in":
            return actual in self.value
        elif self.operator == "contains":
            return self.value in actual
        elif self.operator == "intersects":
            if isinstance(actual, (set, list)) and isinstance(self.value, (set, list)):
                return bool(set(actual) & set(self.value))
            return False
        elif self.operator == "is_none":
            return actual is None
        elif self.operator == "is_not_none":
            return actual is not None
        return False

    def _get_nested_value(self, data: Dict[str, Any], path: str) -> Any:
        """Get value from nested dict using dot notation."""
        keys = path.split(".")
        result = data
        for key in keys:
            if isinstance(result, dict):
                result = result.get(key)
            else:
                return None
        return result


@dataclass
class AccessPolicy:
    """Access control policy definition."""
    policy_id: str
    name: str
    description: str
    effect: PolicyEffect
    conditions: List[PolicyCondition] = field(default_factory=list)
    priority: int = 0
    enabled: bool = True
    redacted_fields: List[str] = field(default_factory=list)

    def evaluate(self, context: Dict[str, Any]) -> Optional[PolicyEffect]:
        """Evaluate policy against context. Returns effect if all conditions match."""
        if not self.enabled:
            return None

        for condition in self.conditions:
            if not condition.evaluate(context):
                return None

        return self.effect

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "policy_id": self.policy_id,
            "name": self.name,
            "description": self.description,
            "effect": self.effect.value,
            "conditions": [
                {"attribute": c.attribute, "operator": c.operator, "value": c.value}
                for c in self.conditions
            ],
            "priority": self.priority,
            "enabled": self.enabled,
            "redacted_fields": self.redacted_fields,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "AccessPolicy":
        """Create from dictionary."""
        conditions = [
            PolicyCondition(
                attribute=c["attribute"],
                operator=c["operator"],
                value=c["value"],
            )
            for c in data.get("conditions", [])
        ]
        return cls(
            policy_id=data["policy_id"],
            name=data["name"],
            description=data.get("description", ""),
            effect=PolicyEffect(data["effect"]),
            conditions=conditions,
            priority=data.get("priority", 0),
            enabled=data.get("enabled", True),
            redacted_fields=data.get("redacted_fields", []),
        )


@dataclass
class PolicyDecision:
    """Result of policy engine evaluation."""
    effect: PolicyEffect
    matching_policies: List[str]
    redacted_fields: List[str]
    reason: str


class PolicyEngine:
    """
    Policy Decision Point (PDP) for classification-based access control.
    Evaluates access requests against configured policies.
    """

    def __init__(self):
        self.policies: List[AccessPolicy] = []
        self._load_default_policies()

    def _load_default_policies(self):
        """Load default classification-based policies."""
        # Policy 1: Clearance level check
        self.policies.append(
            AccessPolicy(
                policy_id="clearance-check",
                name="Clearance Level Check",
                description="Deny access if user clearance is below artifact classification",
                effect=PolicyEffect.DENY,
                conditions=[
                    PolicyCondition(
                        attribute="clearance_insufficient",
                        operator="eq",
                        value=True,
                    )
                ],
                priority=100,
            )
        )

        # Policy 2: Need-to-know check (grants partial access)
        self.policies.append(
            AccessPolicy(
                policy_id="need-to-know-partial",
                name="Need-to-Know Partial Access",
                description="Grant partial access when user has need-to-know but lacks group",
                effect=PolicyEffect.PARTIAL,
                conditions=[
                    PolicyCondition(
                        attribute="has_clearance",
                        operator="eq",
                        value=True,
                    ),
                    PolicyCondition(
                        attribute="has_need_to_know",
                        operator="eq",
                        value=True,
                    ),
                    PolicyCondition(
                        attribute="has_group_access",
                        operator="eq",
                        value=False,
                    ),
                ],
                priority=50,
                redacted_fields=["internal_notes", "source_details", "raw_data"],
            )
        )

        # Policy 3: Full access for matching groups
        self.policies.append(
            AccessPolicy(
                policy_id="group-full-access",
                name="Group Full Access",
                description="Grant full access when user has clearance and group membership",
                effect=PolicyEffect.ALLOW,
                conditions=[
                    PolicyCondition(
                        attribute="has_clearance",
                        operator="eq",
                        value=True,
                    ),
                    PolicyCondition(
                        attribute="has_group_access",
                        operator="eq",
                        value=True,
                    ),
                ],
                priority=40,
            )
        )

        # Policy 4: Default allow for unclassified
        self.policies.append(
            AccessPolicy(
                policy_id="unclassified-allow",
                name="Unclassified Access",
                description="Allow access to unclassified artifacts",
                effect=PolicyEffect.ALLOW,
                conditions=[
                    PolicyCondition(
                        attribute="artifact.classification",
                        operator="eq",
                        value="unclassified",
                    )
                ],
                priority=10,
            )
        )

        # Sort by priority (higher first)
        self.policies.sort(key=lambda p: p.priority, reverse=True)

    def add_policy(self, policy: AccessPolicy):
        """Add a policy to the engine."""
        self.policies.append(policy)
        self.policies.sort(key=lambda p: p.priority, reverse=True)

    def remove_policy(self, policy_id: str) -> bool:
        """Remove a policy by ID."""
        original_len = len(self.policies)
        self.policies = [p for p in self.policies if p.policy_id != policy_id]
        return len(self.policies) < original_len

    def evaluate(
        self,
        user: UserClearance,
        artifact: ArtifactClassification,
    ) -> AccessDecision:
        """
        Evaluate access request for a user against an artifact's classification.
        Returns an AccessDecision with the result and reasoning.
        """
        # Build evaluation context
        context = self._build_context(user, artifact)

        # Track matching policies
        matching_policies: List[str] = []
        redacted_fields: List[str] = []
        final_effect: Optional[PolicyEffect] = None

        # Evaluate policies in priority order
        for policy in self.policies:
            effect = policy.evaluate(context)
            if effect is not None:
                matching_policies.append(policy.policy_id)
                logger.debug(
                    "Policy matched",
                    policy_id=policy.policy_id,
                    effect=effect.value,
                    user_id=user.user_id,
                )

                if effect == PolicyEffect.DENY:
                    return AccessDecision(
                        allowed=False,
                        reason=AccessReason.POLICY_DENIED,
                        partial_access=False,
                        redacted_fields=[],
                        policy_ids=matching_policies,
                    )
                elif effect == PolicyEffect.PARTIAL:
                    redacted_fields.extend(policy.redacted_fields)
                    if final_effect != PolicyEffect.ALLOW:
                        final_effect = PolicyEffect.PARTIAL
                elif effect == PolicyEffect.ALLOW:
                    final_effect = PolicyEffect.ALLOW

        # Determine final decision
        if final_effect == PolicyEffect.ALLOW:
            return AccessDecision(
                allowed=True,
                reason=AccessReason.POLICY_ALLOWED,
                partial_access=False,
                redacted_fields=[],
                policy_ids=matching_policies,
            )
        elif final_effect == PolicyEffect.PARTIAL:
            return AccessDecision(
                allowed=True,
                reason=AccessReason.PARTIAL_ACCESS,
                partial_access=True,
                redacted_fields=list(set(redacted_fields)),
                policy_ids=matching_policies,
            )
        else:
            # Default deny if no policy matched
            return AccessDecision(
                allowed=False,
                reason=AccessReason.POLICY_DENIED,
                partial_access=False,
                redacted_fields=[],
                policy_ids=[],
            )

    def _check_need_to_know_access(
        self,
        user: UserClearance,
        artifact: ArtifactClassification,
    ) -> bool:
        """
        Check if user has need-to-know access to the artifact.
        
        Returns True if:
        - User has at least one matching need-to-know grant, OR
        - Artifact has no need-to-know restrictions
        """
        if not artifact.need_to_know_tags:
            # No restrictions means access granted
            return True
        return bool(artifact.need_to_know_tags & user.need_to_know_grants)

    def _check_group_access(
        self,
        user: UserClearance,
        artifact: ArtifactClassification,
    ) -> bool:
        """
        Check if user has group-based access to the artifact.
        
        Returns True if:
        - User is a member of at least one allowed group, OR
        - Artifact has no group restrictions
        """
        if not artifact.allow_groups:
            # No restrictions means access granted
            return True
        return bool(artifact.allow_groups & user.groups)

    def _build_context(
        self,
        user: UserClearance,
        artifact: ArtifactClassification,
    ) -> Dict[str, Any]:
        """Build evaluation context from user clearance and artifact classification."""
        # Calculate access attributes
        has_clearance = user.clearance_rank >= artifact.rank
        clearance_insufficient = not has_clearance

        # Check need-to-know and group access using helper methods
        has_need_to_know = self._check_need_to_know_access(user, artifact)
        has_group_access = self._check_group_access(user, artifact)

        return {
            "user": {
                "id": user.user_id,
                "clearance_level": user.clearance_level.value,
                "clearance_rank": int(user.clearance_rank),
                "groups": list(user.groups),
                "need_to_know_grants": list(user.need_to_know_grants),
                "roles": list(user.roles),
            },
            "artifact": {
                "classification": artifact.classification.value,
                "classification_rank": int(artifact.rank),
                "need_to_know_tags": list(artifact.need_to_know_tags),
                "allow_groups": list(artifact.allow_groups),
                "owner_id": artifact.owner_id,
            },
            "has_clearance": has_clearance,
            "clearance_insufficient": clearance_insufficient,
            "has_need_to_know": has_need_to_know,
            "has_group_access": has_group_access,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def get_policies(self) -> List[Dict[str, Any]]:
        """Get all policies as dictionaries."""
        return [p.to_dict() for p in self.policies]

    def load_policies_from_json(self, json_str: str):
        """Load policies from JSON string."""
        data = json.loads(json_str)
        for policy_data in data.get("policies", []):
            policy = AccessPolicy.from_dict(policy_data)
            self.add_policy(policy)


# Global policy engine instance
_policy_engine: Optional[PolicyEngine] = None


def get_policy_engine() -> PolicyEngine:
    """Get or create the global policy engine instance."""
    global _policy_engine
    if _policy_engine is None:
        _policy_engine = PolicyEngine()
    return _policy_engine
