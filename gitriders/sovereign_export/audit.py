# GitRiders - FlameLang Sovereignty Export System
# Copyright (c) 2025 StrategicKhaos DAO LLC
# Licensed under MIT License
# Date: December 13, 2025

"""
Immutable audit logging with hash chain verification.
"""

import json
import hashlib
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
from pathlib import Path


class AuditLogger:
    """Immutable append-only audit log with hash chain."""
    
    def __init__(self, log_path: Path):
        """
        Initialize audit logger.
        
        Args:
            log_path: Path to audit log file
        """
        self.log_path = log_path
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize with genesis entry if new
        if not self.log_path.exists():
            self._write_genesis()
    
    def _write_genesis(self) -> None:
        """Write genesis entry to new log."""
        genesis = {
            "index": 0,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": "genesis",
            "data": {"message": "GitRiders audit log initialized"},
            "previous_hash": "0" * 64,
            "hash": "",
        }
        genesis["hash"] = self._compute_hash(genesis)
        
        with open(self.log_path, "w") as f:
            f.write(json.dumps(genesis) + "\n")
    
    def log_event(
        self,
        event_type: str,
        data: Dict[str, Any],
        user: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Log an audit event.
        
        Args:
            event_type: Type of event (e.g., "export", "decrypt", "verify")
            data: Event data
            user: Optional user identifier
        
        Returns:
            The logged entry
        """
        # Get previous entry
        previous_entry = self._get_last_entry()
        
        # Create new entry
        entry = {
            "index": previous_entry["index"] + 1,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "user": user,
            "data": data,
            "previous_hash": previous_entry["hash"],
            "hash": "",
        }
        
        # Compute hash
        entry["hash"] = self._compute_hash(entry)
        
        # Append to log
        with open(self.log_path, "a") as f:
            f.write(json.dumps(entry) + "\n")
        
        return entry
    
    def _get_last_entry(self) -> Dict[str, Any]:
        """
        Get the last entry in the log.
        
        Returns:
            Last log entry
        """
        with open(self.log_path, "r") as f:
            lines = f.readlines()
            if lines:
                return json.loads(lines[-1])
        
        raise ValueError("Log is empty")
    
    def _compute_hash(self, entry: Dict[str, Any]) -> str:
        """
        Compute hash of an entry.
        
        Args:
            entry: Log entry (without hash field)
        
        Returns:
            SHA-256 hash hex
        """
        # Create deterministic string representation
        entry_copy = entry.copy()
        entry_copy.pop("hash", None)
        entry_str = json.dumps(entry_copy, sort_keys=True)
        
        return hashlib.sha256(entry_str.encode("utf-8")).hexdigest()
    
    def verify_integrity(self) -> bool:
        """
        Verify the integrity of the entire audit log.
        
        Returns:
            True if all hashes are valid
        
        Raises:
            ValueError: If integrity check fails
        """
        entries = self.read_log()
        
        for i, entry in enumerate(entries):
            # Verify hash
            expected_hash = self._compute_hash(entry)
            if entry["hash"] != expected_hash:
                raise ValueError(
                    f"Hash mismatch at index {i}: "
                    f"expected {expected_hash}, got {entry['hash']}"
                )
            
            # Verify chain linkage
            if i > 0:
                if entry["previous_hash"] != entries[i - 1]["hash"]:
                    raise ValueError(
                        f"Chain broken at index {i}: "
                        f"previous_hash {entry['previous_hash']} != "
                        f"actual previous hash {entries[i - 1]['hash']}"
                    )
        
        return True
    
    def read_log(self) -> List[Dict[str, Any]]:
        """
        Read all entries from the log.
        
        Returns:
            List of log entries
        """
        entries = []
        with open(self.log_path, "r") as f:
            for line in f:
                if line.strip():
                    entries.append(json.loads(line))
        return entries
    
    def get_entries_by_type(self, event_type: str) -> List[Dict[str, Any]]:
        """
        Get all entries of a specific type.
        
        Args:
            event_type: Event type to filter by
        
        Returns:
            List of matching entries
        """
        return [e for e in self.read_log() if e["event_type"] == event_type]
    
    def get_entries_by_user(self, user: str) -> List[Dict[str, Any]]:
        """
        Get all entries for a specific user.
        
        Args:
            user: User identifier
        
        Returns:
            List of matching entries
        """
        return [e for e in self.read_log() if e.get("user") == user]


def create_audit_entry(
    event_type: str,
    provider: str,
    operation: str,
    success: bool,
    details: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Create a standardized audit entry.
    
    Args:
        event_type: Type of event
        provider: Provider name
        operation: Operation performed
        success: Whether operation succeeded
        details: Optional additional details
    
    Returns:
        Audit entry data
    """
    return {
        "provider": provider,
        "operation": operation,
        "success": success,
        "details": details or {},
    }
