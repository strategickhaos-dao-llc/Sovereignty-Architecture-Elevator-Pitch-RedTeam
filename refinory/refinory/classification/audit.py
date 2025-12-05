"""
Audit logging for classification access events.
Provides immutable audit trail for security compliance.
"""

import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

import structlog

logger = structlog.get_logger()


class AuditEventType(str, Enum):
    """Types of audit events."""
    ACCESS_GRANTED = "access_granted"
    ACCESS_DENIED = "access_denied"
    ACCESS_PARTIAL = "access_partial"
    CLASSIFICATION_CHANGED = "classification_changed"
    CLEARANCE_VERIFIED = "clearance_verified"
    CLEARANCE_EXPIRED = "clearance_expired"
    POLICY_EVALUATED = "policy_evaluated"
    REDACTION_APPLIED = "redaction_applied"
    ARTIFACT_CREATED = "artifact_created"
    ARTIFACT_DELETED = "artifact_deleted"
    ACCESS_REQUEST_SUBMITTED = "access_request_submitted"
    ACCESS_REQUEST_APPROVED = "access_request_approved"
    ACCESS_REQUEST_DENIED = "access_request_denied"


@dataclass
class AuditEvent:
    """Immutable audit event record."""
    event_id: str
    event_type: AuditEventType
    timestamp: datetime
    user_id: str
    resource_id: Optional[str]
    resource_type: Optional[str]
    action: str
    outcome: str
    details: Dict[str, Any] = field(default_factory=dict)
    classification_level: Optional[str] = None
    user_clearance: Optional[str] = None
    policy_ids: List[str] = field(default_factory=list)
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    session_id: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary for storage."""
        return {
            "event_id": self.event_id,
            "event_type": self.event_type.value,
            "timestamp": self.timestamp.isoformat(),
            "user_id": self.user_id,
            "resource_id": self.resource_id,
            "resource_type": self.resource_type,
            "action": self.action,
            "outcome": self.outcome,
            "details": self.details,
            "classification_level": self.classification_level,
            "user_clearance": self.user_clearance,
            "policy_ids": self.policy_ids,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "session_id": self.session_id,
        }

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data: dict) -> "AuditEvent":
        """Create from dictionary."""
        return cls(
            event_id=data["event_id"],
            event_type=AuditEventType(data["event_type"]),
            timestamp=datetime.fromisoformat(data["timestamp"]),
            user_id=data["user_id"],
            resource_id=data.get("resource_id"),
            resource_type=data.get("resource_type"),
            action=data["action"],
            outcome=data["outcome"],
            details=data.get("details", {}),
            classification_level=data.get("classification_level"),
            user_clearance=data.get("user_clearance"),
            policy_ids=data.get("policy_ids", []),
            ip_address=data.get("ip_address"),
            user_agent=data.get("user_agent"),
            session_id=data.get("session_id"),
        )


class AuditLogger:
    """
    Audit logger for classification access events.
    Supports multiple storage backends and async operations.
    """

    def __init__(
        self,
        storage_backends: Optional[List[Callable[[AuditEvent], None]]] = None,
        buffer_size: int = 100,
        flush_interval: int = 60,
    ):
        """
        Initialize audit logger.

        Args:
            storage_backends: List of storage backend functions
            buffer_size: Number of events to buffer before flush
            flush_interval: Seconds between automatic flushes
        """
        self.storage_backends = storage_backends or []
        self.buffer_size = buffer_size
        self.flush_interval = flush_interval
        self._buffer: List[AuditEvent] = []
        self._add_default_backend()

    def _add_default_backend(self):
        """Add default structlog backend."""
        def structlog_backend(event: AuditEvent):
            logger.info(
                "audit_event",
                event_id=event.event_id,
                event_type=event.event_type.value,
                user_id=event.user_id,
                resource_id=event.resource_id,
                action=event.action,
                outcome=event.outcome,
                classification=event.classification_level,
            )

        self.storage_backends.append(structlog_backend)

    def add_backend(self, backend: Callable[[AuditEvent], None]):
        """Add a storage backend."""
        self.storage_backends.append(backend)

    def log(
        self,
        event_type: AuditEventType,
        user_id: str,
        action: str,
        outcome: str,
        resource_id: Optional[str] = None,
        resource_type: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        classification_level: Optional[str] = None,
        user_clearance: Optional[str] = None,
        policy_ids: Optional[List[str]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        session_id: Optional[str] = None,
    ) -> str:
        """
        Log an audit event.

        Returns the event ID for reference.
        """
        event = AuditEvent(
            event_id=str(uuid.uuid4()),
            event_type=event_type,
            timestamp=datetime.now(timezone.utc),
            user_id=user_id,
            resource_id=resource_id,
            resource_type=resource_type,
            action=action,
            outcome=outcome,
            details=details or {},
            classification_level=classification_level,
            user_clearance=user_clearance,
            policy_ids=policy_ids or [],
            ip_address=ip_address,
            user_agent=user_agent,
            session_id=session_id,
        )

        # Write to all backends
        for backend in self.storage_backends:
            try:
                backend(event)
            except Exception as e:
                logger.error(
                    "Audit backend error",
                    backend=backend.__name__,
                    error=str(e),
                )

        # Buffer for batch operations
        self._buffer.append(event)
        if len(self._buffer) >= self.buffer_size:
            self.flush()

        return event.event_id

    def log_access_decision(
        self,
        user_id: str,
        resource_id: str,
        resource_type: str,
        classification_level: str,
        user_clearance: str,
        allowed: bool,
        partial: bool = False,
        reason: str = "",
        policy_ids: Optional[List[str]] = None,
        redacted_fields: Optional[List[str]] = None,
        ip_address: Optional[str] = None,
    ) -> str:
        """
        Log an access decision event.
        """
        if allowed:
            if partial:
                event_type = AuditEventType.ACCESS_PARTIAL
                outcome = "partial_access"
            else:
                event_type = AuditEventType.ACCESS_GRANTED
                outcome = "allowed"
        else:
            event_type = AuditEventType.ACCESS_DENIED
            outcome = "denied"

        details = {
            "reason": reason,
        }
        if redacted_fields:
            details["redacted_fields"] = redacted_fields

        return self.log(
            event_type=event_type,
            user_id=user_id,
            action="access_resource",
            outcome=outcome,
            resource_id=resource_id,
            resource_type=resource_type,
            details=details,
            classification_level=classification_level,
            user_clearance=user_clearance,
            policy_ids=policy_ids,
            ip_address=ip_address,
        )

    def log_classification_change(
        self,
        user_id: str,
        resource_id: str,
        resource_type: str,
        old_classification: str,
        new_classification: str,
        reason: str = "",
    ) -> str:
        """Log a classification level change."""
        return self.log(
            event_type=AuditEventType.CLASSIFICATION_CHANGED,
            user_id=user_id,
            action="change_classification",
            outcome="success",
            resource_id=resource_id,
            resource_type=resource_type,
            details={
                "old_classification": old_classification,
                "new_classification": new_classification,
                "reason": reason,
            },
            classification_level=new_classification,
        )

    def log_access_request(
        self,
        user_id: str,
        resource_id: str,
        requested_level: str,
        current_clearance: str,
        justification: str,
    ) -> str:
        """Log an access elevation request."""
        return self.log(
            event_type=AuditEventType.ACCESS_REQUEST_SUBMITTED,
            user_id=user_id,
            action="request_access",
            outcome="submitted",
            resource_id=resource_id,
            details={
                "requested_level": requested_level,
                "justification": justification,
            },
            classification_level=requested_level,
            user_clearance=current_clearance,
        )

    def flush(self):
        """Flush buffered events to persistent storage."""
        if not self._buffer:
            return

        # Here we would write to persistent storage
        # For now, just clear the buffer as events are already logged
        logger.debug("Flushing audit buffer", event_count=len(self._buffer))
        self._buffer.clear()

    def get_recent_events(
        self,
        user_id: Optional[str] = None,
        resource_id: Optional[str] = None,
        event_type: Optional[AuditEventType] = None,
        limit: int = 100,
    ) -> List[AuditEvent]:
        """
        Get recent audit events from buffer.
        For production, this should query persistent storage.
        """
        events = self._buffer.copy()

        if user_id:
            events = [e for e in events if e.user_id == user_id]
        if resource_id:
            events = [e for e in events if e.resource_id == resource_id]
        if event_type:
            events = [e for e in events if e.event_type == event_type]

        return events[-limit:]


# Global audit logger instance
_audit_logger: Optional[AuditLogger] = None


def get_audit_logger() -> AuditLogger:
    """Get or create the global audit logger."""
    global _audit_logger
    if _audit_logger is None:
        _audit_logger = AuditLogger()
    return _audit_logger


def log_access_event(
    user_id: str,
    resource_id: str,
    resource_type: str,
    classification_level: str,
    user_clearance: str,
    allowed: bool,
    partial: bool = False,
    reason: str = "",
    policy_ids: Optional[List[str]] = None,
    redacted_fields: Optional[List[str]] = None,
    ip_address: Optional[str] = None,
) -> str:
    """Convenience function to log access events."""
    audit_logger = get_audit_logger()
    return audit_logger.log_access_decision(
        user_id=user_id,
        resource_id=resource_id,
        resource_type=resource_type,
        classification_level=classification_level,
        user_clearance=user_clearance,
        allowed=allowed,
        partial=partial,
        reason=reason,
        policy_ids=policy_ids,
        redacted_fields=redacted_fields,
        ip_address=ip_address,
    )
