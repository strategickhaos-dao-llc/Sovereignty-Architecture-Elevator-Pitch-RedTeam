"""
Audit Logger

Immutable audit logging for Grok-5 deployment activities.
"""

import json
import logging
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Optional, Protocol

try:
    from ..utils.blake3_hasher import blake3_hex
except ImportError:
    from utils.blake3_hasher import blake3_hex


class AuditStorage(Protocol):
    """Protocol for audit log storage."""

    def append(self, entry: dict) -> None:
        """Append entry to audit log."""
        ...

    def get_entries(
        self,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
    ) -> list[dict]:
        """Get entries in time range."""
        ...


@dataclass
class AuditEvent:
    """Audit event record."""

    event_type: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    deployment_id: Optional[str] = None
    user: Optional[str] = None
    details: dict[str, Any] = field(default_factory=dict)
    hash: Optional[str] = None
    previous_hash: Optional[str] = None

    def compute_hash(self, previous_hash: Optional[str] = None) -> str:
        """
        Compute hash of this event.

        Args:
            previous_hash: Hash of previous event in chain

        Returns:
            Hex-encoded hash
        """
        data = {
            "event_type": self.event_type,
            "timestamp": self.timestamp.isoformat(),
            "deployment_id": self.deployment_id,
            "user": self.user,
            "details": self.details,
            "previous_hash": previous_hash or "",
        }
        return blake3_hex(json.dumps(data, sort_keys=True).encode())


class AuditLogger:
    """
    Immutable audit logger for Grok-5 deployment.

    Features:
    - Chained hashing for tamper detection
    - Structured event logging
    - Multiple storage backends
    - Query support
    """

    def __init__(
        self,
        storage: Optional[AuditStorage] = None,
        log_dir: Optional[str] = None,
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initialize audit logger.

        Args:
            storage: Storage backend
            log_dir: Directory for local log files
            logger: Logger instance
        """
        self.storage = storage
        self.log_dir = Path(log_dir) if log_dir else Path("/var/log/grok5/audit")
        self.log = logger or logging.getLogger(__name__)
        self._chain: list[AuditEvent] = []
        self._last_hash: Optional[str] = None

    def log(self, event: AuditEvent) -> AuditEvent:
        """
        Log an audit event.

        Args:
            event: Event to log

        Returns:
            Event with hash computed
        """
        # Set previous hash and compute current hash
        event.previous_hash = self._last_hash
        event.hash = event.compute_hash(self._last_hash)

        # Update chain
        self._chain.append(event)
        self._last_hash = event.hash

        # Persist
        self._persist(event)

        self.log.info(
            f"[audit] type={event.event_type} "
            f"deployment={event.deployment_id} "
            f"hash={event.hash[:16]}..."
        )

        return event

    def _persist(self, event: AuditEvent) -> None:
        """Persist event to storage."""
        entry = asdict(event)
        entry["timestamp"] = event.timestamp.isoformat()

        if self.storage:
            try:
                self.storage.append(entry)
            except Exception as e:
                self.log.error(f"Failed to persist audit event: {e}")

        # Always write to local file as backup
        self._write_local(entry)

    def _write_local(self, entry: dict) -> None:
        """Write entry to local log file."""
        try:
            self.log_dir.mkdir(parents=True, exist_ok=True)
            log_file = self.log_dir / "audit.jsonl"

            with open(log_file, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            self.log.error(f"Failed to write local audit log: {e}")

    def verify_chain(self) -> bool:
        """
        Verify integrity of audit chain.

        Returns:
            True if chain is valid
        """
        previous_hash = None

        for event in self._chain:
            computed = event.compute_hash(previous_hash)
            if computed != event.hash:
                self.log.error(
                    f"Chain integrity violation: "
                    f"expected={event.hash} computed={computed}"
                )
                return False
            previous_hash = event.hash

        return True

    def get_events(
        self,
        event_type: Optional[str] = None,
        deployment_id: Optional[str] = None,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
    ) -> list[AuditEvent]:
        """
        Query audit events.

        Args:
            event_type: Filter by event type
            deployment_id: Filter by deployment
            start: Start of time range
            end: End of time range

        Returns:
            List of matching events
        """
        events = self._chain

        if event_type:
            events = [e for e in events if e.event_type == event_type]

        if deployment_id:
            events = [e for e in events if e.deployment_id == deployment_id]

        if start:
            events = [e for e in events if e.timestamp >= start]

        if end:
            events = [e for e in events if e.timestamp <= end]

        return events

    def get_chain_length(self) -> int:
        """Get number of events in chain."""
        return len(self._chain)

    def export(self, path: str) -> None:
        """
        Export audit chain to file.

        Args:
            path: Export file path
        """
        entries = [asdict(e) for e in self._chain]
        for entry in entries:
            if isinstance(entry.get("timestamp"), datetime):
                entry["timestamp"] = entry["timestamp"].isoformat()

        with open(path, "w") as f:
            json.dump(entries, f, indent=2)

        self.log.info(f"Exported {len(entries)} audit events to {path}")
