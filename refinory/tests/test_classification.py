"""
Unit tests for classification module.
Tests classification levels, policy enforcement, redaction, and audit logging.
"""

import pytest
from datetime import datetime, timezone, timedelta

from refinory.classification.models import (
    ClassificationLevel,
    ClassificationRank,
    ArtifactClassification,
    UserClearance,
    AccessDecision,
    AccessReason,
)
from refinory.classification.policy import (
    PolicyEngine,
    AccessPolicy,
    PolicyCondition,
    PolicyEffect,
    PolicyDecision,
)
from refinory.classification.redaction import (
    RedactionEngine,
    redact_artifact,
    create_redacted_preview,
)
from refinory.classification.audit import (
    AuditLogger,
    AuditEvent,
    AuditEventType,
)


class TestClassificationModels:
    """Tests for classification data models."""

    def test_classification_level_values(self):
        """Test that classification levels have correct values."""
        assert ClassificationLevel.UNCLASSIFIED.value == "unclassified"
        assert ClassificationLevel.INTERNAL.value == "internal"
        assert ClassificationLevel.CONFIDENTIAL.value == "confidential"
        assert ClassificationLevel.SECRET.value == "secret"
        assert ClassificationLevel.TOP_SECRET.value == "top_secret"

    def test_classification_rank_ordering(self):
        """Test that classification ranks are properly ordered."""
        assert ClassificationRank.UNCLASSIFIED < ClassificationRank.INTERNAL
        assert ClassificationRank.INTERNAL < ClassificationRank.CONFIDENTIAL
        assert ClassificationRank.CONFIDENTIAL < ClassificationRank.SECRET
        assert ClassificationRank.SECRET < ClassificationRank.TOP_SECRET

    def test_rank_from_level_conversion(self):
        """Test conversion from classification level to rank."""
        assert ClassificationRank.from_level(ClassificationLevel.UNCLASSIFIED) == 0
        assert ClassificationRank.from_level(ClassificationLevel.SECRET) == 3
        assert ClassificationRank.from_level(ClassificationLevel.TOP_SECRET) == 4

    def test_artifact_classification_creation(self):
        """Test creating artifact classification."""
        classification = ArtifactClassification(
            classification=ClassificationLevel.SECRET,
            need_to_know_tags={"project-alpha", "team-security"},
            allow_groups={"security-team", "admin"},
            owner_id="user-123",
        )
        
        assert classification.classification == ClassificationLevel.SECRET
        assert classification.rank == ClassificationRank.SECRET
        assert "project-alpha" in classification.need_to_know_tags
        assert "security-team" in classification.allow_groups
        assert classification.owner_id == "user-123"

    def test_artifact_classification_serialization(self):
        """Test serialization and deserialization."""
        original = ArtifactClassification(
            classification=ClassificationLevel.CONFIDENTIAL,
            need_to_know_tags={"tag1"},
            allow_groups={"group1"},
        )
        
        data = original.to_dict()
        restored = ArtifactClassification.from_dict(data)
        
        assert restored.classification == original.classification
        assert restored.need_to_know_tags == original.need_to_know_tags
        assert restored.allow_groups == original.allow_groups

    def test_user_clearance_creation(self):
        """Test creating user clearance."""
        clearance = UserClearance(
            user_id="user-456",
            clearance_level=ClassificationLevel.SECRET,
            groups={"engineering", "security"},
            need_to_know_grants={"project-alpha"},
            roles={"admin", "reviewer"},
        )
        
        assert clearance.user_id == "user-456"
        assert clearance.clearance_rank == ClassificationRank.SECRET
        assert clearance.has_group("engineering")
        assert not clearance.has_group("finance")
        assert clearance.has_need_to_know("project-alpha")
        assert clearance.has_role("admin")

    def test_user_clearance_expiration(self):
        """Test clearance expiration check."""
        # Non-expired clearance
        clearance = UserClearance(
            user_id="user-1",
            clearance_level=ClassificationLevel.INTERNAL,
            expires_at=datetime.now(timezone.utc) + timedelta(days=30),
        )
        assert not clearance.is_expired()
        
        # Expired clearance
        expired_clearance = UserClearance(
            user_id="user-2",
            clearance_level=ClassificationLevel.INTERNAL,
            expires_at=datetime.now(timezone.utc) - timedelta(days=1),
        )
        assert expired_clearance.is_expired()

    def test_user_clearance_from_jwt_claims(self):
        """Test creating clearance from JWT claims."""
        claims = {
            "sub": "jwt-user-123",
            "clearance_level": "confidential",
            "groups": ["team-a", "team-b"],
            "ntk_grants": ["project-x"],
            "roles": ["developer"],
            "iat": 1700000000,
            "exp": 1700086400,
        }
        
        clearance = UserClearance.from_jwt_claims(claims)
        
        assert clearance.user_id == "jwt-user-123"
        assert clearance.clearance_level == ClassificationLevel.CONFIDENTIAL
        assert "team-a" in clearance.groups
        assert clearance.has_need_to_know("project-x")
        assert clearance.has_role("developer")


class TestPolicyEngine:
    """Tests for policy engine."""

    def test_policy_engine_initialization(self):
        """Test policy engine initializes with default policies."""
        engine = PolicyEngine()
        
        policies = engine.get_policies()
        assert len(policies) >= 4  # At least 4 default policies
        
        # Check default policies exist
        policy_ids = [p["policy_id"] for p in policies]
        assert "clearance-check" in policy_ids
        assert "unclassified-allow" in policy_ids

    def test_clearance_sufficient_allows_access(self):
        """Test that sufficient clearance allows access."""
        engine = PolicyEngine()
        
        user = UserClearance(
            user_id="user-1",
            clearance_level=ClassificationLevel.SECRET,
            groups={"team-a"},
        )
        
        artifact = ArtifactClassification(
            classification=ClassificationLevel.INTERNAL,
            allow_groups={"team-a"},
        )
        
        decision = engine.evaluate(user, artifact)
        
        assert decision.allowed
        assert decision.reason in [AccessReason.POLICY_ALLOWED, AccessReason.PARTIAL_ACCESS]

    def test_clearance_insufficient_denies_access(self):
        """Test that insufficient clearance denies access."""
        engine = PolicyEngine()
        
        user = UserClearance(
            user_id="user-1",
            clearance_level=ClassificationLevel.INTERNAL,
        )
        
        artifact = ArtifactClassification(
            classification=ClassificationLevel.TOP_SECRET,
        )
        
        decision = engine.evaluate(user, artifact)
        
        assert not decision.allowed
        assert decision.reason == AccessReason.POLICY_DENIED

    def test_unclassified_always_accessible(self):
        """Test that unclassified artifacts are always accessible."""
        engine = PolicyEngine()
        
        user = UserClearance(
            user_id="user-1",
            clearance_level=ClassificationLevel.UNCLASSIFIED,
        )
        
        artifact = ArtifactClassification(
            classification=ClassificationLevel.UNCLASSIFIED,
        )
        
        decision = engine.evaluate(user, artifact)
        
        assert decision.allowed

    def test_group_access_with_clearance(self):
        """Test that group membership with clearance grants access."""
        engine = PolicyEngine()
        
        user = UserClearance(
            user_id="user-1",
            clearance_level=ClassificationLevel.CONFIDENTIAL,
            groups={"security-team"},
        )
        
        artifact = ArtifactClassification(
            classification=ClassificationLevel.CONFIDENTIAL,
            allow_groups={"security-team"},
        )
        
        decision = engine.evaluate(user, artifact)
        
        assert decision.allowed
        assert not decision.partial_access

    def test_partial_access_with_need_to_know(self):
        """Test partial access when user has need-to-know but not group."""
        engine = PolicyEngine()
        
        user = UserClearance(
            user_id="user-1",
            clearance_level=ClassificationLevel.SECRET,
            need_to_know_grants={"project-alpha"},
            groups=set(),  # No group membership
        )
        
        artifact = ArtifactClassification(
            classification=ClassificationLevel.SECRET,
            need_to_know_tags={"project-alpha"},
            allow_groups={"restricted-team"},  # User not in this group
        )
        
        decision = engine.evaluate(user, artifact)
        
        assert decision.allowed
        assert decision.partial_access
        assert len(decision.redacted_fields) > 0

    def test_custom_policy_addition(self):
        """Test adding custom policies."""
        engine = PolicyEngine()
        
        custom_policy = AccessPolicy(
            policy_id="custom-test",
            name="Custom Test Policy",
            description="Test custom policy",
            effect=PolicyEffect.DENY,
            conditions=[
                PolicyCondition(
                    attribute="user.id",
                    operator="eq",
                    value="blocked-user",
                )
            ],
            priority=200,  # High priority
        )
        
        engine.add_policy(custom_policy)
        
        # Test that blocked user is denied
        user = UserClearance(
            user_id="blocked-user",
            clearance_level=ClassificationLevel.TOP_SECRET,
        )
        
        artifact = ArtifactClassification(
            classification=ClassificationLevel.UNCLASSIFIED,
        )
        
        decision = engine.evaluate(user, artifact)
        assert not decision.allowed

    def test_policy_removal(self):
        """Test removing policies."""
        engine = PolicyEngine()
        
        initial_count = len(engine.policies)
        result = engine.remove_policy("unclassified-allow")
        
        assert result is True
        assert len(engine.policies) == initial_count - 1


class TestPolicyCondition:
    """Tests for policy condition evaluation."""

    def test_equality_condition(self):
        """Test equality operator."""
        condition = PolicyCondition(
            attribute="user.clearance_level",
            operator="eq",
            value="secret",
        )
        
        context = {"user": {"clearance_level": "secret"}}
        assert condition.evaluate(context)
        
        context = {"user": {"clearance_level": "internal"}}
        assert not condition.evaluate(context)

    def test_greater_than_condition(self):
        """Test greater than operator."""
        condition = PolicyCondition(
            attribute="artifact.classification_rank",
            operator="gte",
            value=2,
        )
        
        assert condition.evaluate({"artifact": {"classification_rank": 3}})
        assert condition.evaluate({"artifact": {"classification_rank": 2}})
        assert not condition.evaluate({"artifact": {"classification_rank": 1}})

    def test_contains_condition(self):
        """Test contains operator."""
        condition = PolicyCondition(
            attribute="user.roles",
            operator="contains",
            value="admin",
        )
        
        assert condition.evaluate({"user": {"roles": ["admin", "user"]}})
        assert not condition.evaluate({"user": {"roles": ["user"]}})

    def test_intersects_condition(self):
        """Test set intersection operator."""
        condition = PolicyCondition(
            attribute="user.groups",
            operator="intersects",
            value=["team-a", "team-b"],
        )
        
        assert condition.evaluate({"user": {"groups": ["team-a", "team-c"]}})
        assert not condition.evaluate({"user": {"groups": ["team-c", "team-d"]}})


class TestRedactionEngine:
    """Tests for redaction engine."""

    def test_basic_redaction(self):
        """Test basic field redaction."""
        engine = RedactionEngine()
        
        data = {
            "id": "123",
            "name": "Test Artifact",
            "secret_data": "sensitive information",
            "internal_notes": "confidential notes",
        }
        
        result = engine.redact(data, ["secret_data", "internal_notes"])
        
        assert result["id"] == "123"
        assert result["name"] == "Test Artifact"
        assert result["secret_data"] == "[REDACTED]"
        assert result["internal_notes"] == "[REDACTED]"

    def test_nested_field_redaction(self):
        """Test redacting nested fields."""
        engine = RedactionEngine()
        
        data = {
            "id": "123",
            "metadata": {
                "public_field": "visible",
                "secret_field": "hidden",
            }
        }
        
        result = engine.redact(data, ["metadata.secret_field"])
        
        assert result["metadata"]["public_field"] == "visible"
        assert result["metadata"]["secret_field"] == "[REDACTED]"

    def test_redaction_metadata_included(self):
        """Test that redaction metadata is included."""
        engine = RedactionEngine(include_metadata=True)
        
        data = {"field1": "value1", "secret": "hidden"}
        result = engine.redact(data, ["secret"], reason="test_policy", policy_id="policy-1")
        
        assert "_redaction_info" in result
        assert result["_redaction_info"]["redacted"] is True
        assert result["_redaction_info"]["total_redacted"] == 1
        assert len(result["_redaction_info"]["redacted_fields"]) == 1
        assert result["_redaction_info"]["redacted_fields"][0]["path"] == "secret"

    def test_redact_artifact_convenience_function(self):
        """Test the convenience redaction function."""
        artifact = {
            "id": "artifact-1",
            "content": "public content",
            "raw_data": "secret data",
        }
        
        result = redact_artifact(artifact, ["raw_data"])
        
        assert result["content"] == "public content"
        assert result["raw_data"] == "[REDACTED]"

    def test_create_redacted_preview(self):
        """Test creating redacted preview."""
        artifact = {
            "id": "artifact-123",
            "title": "Test Document",
            "description": "A" * 200,  # Long description
            "content": "Full content here",
        }
        
        preview = create_redacted_preview(artifact, "confidential", max_length=50)
        
        assert preview["id"] == "artifact-123"
        assert preview["title"] == "Test Document"
        assert preview["classification"] == "confidential"
        assert len(preview["description"]) <= 53  # 50 + "..."
        assert "content" not in preview
        assert preview["_redacted_preview"] is True

    def test_original_data_not_modified(self):
        """Test that original data is not modified."""
        engine = RedactionEngine()
        
        original = {"field": "original_value"}
        engine.redact(original, ["field"])
        
        assert original["field"] == "original_value"


class TestAuditLogger:
    """Tests for audit logging."""

    def test_basic_audit_event(self):
        """Test logging a basic audit event."""
        logger = AuditLogger()
        
        event_id = logger.log(
            event_type=AuditEventType.ACCESS_GRANTED,
            user_id="user-123",
            action="read_artifact",
            outcome="success",
            resource_id="artifact-456",
            resource_type="architecture_artifact",
        )
        
        assert event_id is not None
        assert len(event_id) > 0

    def test_access_decision_logging(self):
        """Test logging access decisions."""
        logger = AuditLogger()
        
        event_id = logger.log_access_decision(
            user_id="user-1",
            resource_id="artifact-1",
            resource_type="architecture_artifact",
            classification_level="secret",
            user_clearance="top_secret",
            allowed=True,
            partial=False,
            reason="clearance_sufficient",
            policy_ids=["policy-1", "policy-2"],
        )
        
        assert event_id is not None

    def test_denied_access_logging(self):
        """Test logging denied access."""
        logger = AuditLogger()
        
        event_id = logger.log_access_decision(
            user_id="user-1",
            resource_id="artifact-1",
            resource_type="architecture_artifact",
            classification_level="top_secret",
            user_clearance="internal",
            allowed=False,
            reason="clearance_insufficient",
        )
        
        events = logger.get_recent_events(user_id="user-1")
        assert len(events) >= 1
        
        latest = events[-1]
        assert latest.event_type == AuditEventType.ACCESS_DENIED

    def test_partial_access_with_redaction_logging(self):
        """Test logging partial access with redaction."""
        logger = AuditLogger()
        
        event_id = logger.log_access_decision(
            user_id="user-1",
            resource_id="artifact-1",
            resource_type="architecture_artifact",
            classification_level="confidential",
            user_clearance="confidential",
            allowed=True,
            partial=True,
            reason="need_to_know_granted",
            redacted_fields=["internal_notes", "raw_data"],
        )
        
        events = logger.get_recent_events(user_id="user-1")
        latest = events[-1]
        
        assert latest.event_type == AuditEventType.ACCESS_PARTIAL
        assert "redacted_fields" in latest.details

    def test_classification_change_logging(self):
        """Test logging classification changes."""
        logger = AuditLogger()
        
        event_id = logger.log_classification_change(
            user_id="admin-1",
            resource_id="artifact-1",
            resource_type="architecture_artifact",
            old_classification="internal",
            new_classification="confidential",
            reason="Upgraded due to sensitive content",
        )
        
        events = logger.get_recent_events(resource_id="artifact-1")
        assert len(events) >= 1
        
        latest = events[-1]
        assert latest.event_type == AuditEventType.CLASSIFICATION_CHANGED
        assert latest.details["old_classification"] == "internal"
        assert latest.details["new_classification"] == "confidential"

    def test_audit_event_serialization(self):
        """Test audit event serialization."""
        event = AuditEvent(
            event_id="evt-123",
            event_type=AuditEventType.ACCESS_GRANTED,
            timestamp=datetime.now(timezone.utc),
            user_id="user-1",
            resource_id="res-1",
            resource_type="artifact",
            action="read",
            outcome="success",
            classification_level="secret",
            policy_ids=["p1", "p2"],
        )
        
        data = event.to_dict()
        json_str = event.to_json()
        
        assert data["event_id"] == "evt-123"
        assert data["event_type"] == "access_granted"
        assert "timestamp" in json_str

    def test_buffer_flush(self):
        """Test audit buffer flushing."""
        logger = AuditLogger(buffer_size=3)
        
        # Log multiple events
        for i in range(5):
            logger.log(
                event_type=AuditEventType.ACCESS_GRANTED,
                user_id=f"user-{i}",
                action="test",
                outcome="success",
            )
        
        # Buffer should have been flushed at least once
        assert len(logger._buffer) < 5


class TestAccessDecision:
    """Tests for access decision model."""

    def test_access_decision_creation(self):
        """Test creating access decision."""
        decision = AccessDecision(
            allowed=True,
            reason=AccessReason.CLEARANCE_SUFFICIENT,
            partial_access=False,
            redacted_fields=[],
            policy_ids=["policy-1"],
            audit_id="audit-123",
        )
        
        assert decision.allowed
        assert decision.reason == AccessReason.CLEARANCE_SUFFICIENT
        assert not decision.partial_access
        assert decision.audit_id == "audit-123"

    def test_access_decision_serialization(self):
        """Test access decision serialization."""
        decision = AccessDecision(
            allowed=True,
            reason=AccessReason.PARTIAL_ACCESS,
            partial_access=True,
            redacted_fields=["field1", "field2"],
            policy_ids=["p1"],
        )
        
        data = decision.to_dict()
        
        assert data["allowed"] is True
        assert data["reason"] == "partial_access"
        assert data["partial_access"] is True
        assert len(data["redacted_fields"]) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
