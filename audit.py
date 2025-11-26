# audit.py
"""Tamper-evident audit logging with SHA-256 hash chain."""
import hashlib
import json
from datetime import datetime, UTC
from typing import Optional
from fastapi import Request
from models import Artifact


# In-memory audit log for testing; replace with database in production
_audit_log: list = []
_previous_hash: str = "genesis"


async def log_access(
    request: Request,
    artifact: Optional[Artifact],
    decision: str,
    reason: str,
) -> dict:
    """Log access attempt with tamper-evident hash chain."""
    global _previous_hash
    
    entry = {
        "timestamp": datetime.now(UTC).isoformat(),
        "artifact_id": artifact.id if artifact else None,
        "classification": artifact.classification if artifact else None,
        "decision": decision,
        "reason": reason,
        "client_ip": request.client.host if request.client else None,
        "user_agent": request.headers.get("User-Agent", ""),
        "policy_version": "v1",
        "previous_hash": _previous_hash,
    }
    
    # Compute current hash from entry + previous hash
    entry_str = json.dumps(entry, sort_keys=True)
    entry["current_hash"] = hashlib.sha256(entry_str.encode()).hexdigest()
    
    # Update chain
    _previous_hash = entry["current_hash"]
    
    # Append to audit log
    _audit_log.append(entry)
    
    return entry


def get_audit_log() -> list:
    """Retrieve full audit log for inspection."""
    return _audit_log.copy()


def verify_audit_chain() -> bool:
    """Verify integrity of audit log hash chain."""
    if not _audit_log:
        return True
    
    expected_previous = "genesis"
    for entry in _audit_log:
        if entry["previous_hash"] != expected_previous:
            return False
        
        # Recompute hash to verify
        verify_entry = {k: v for k, v in entry.items() if k != "current_hash"}
        entry_str = json.dumps(verify_entry, sort_keys=True)
        computed_hash = hashlib.sha256(entry_str.encode()).hexdigest()
        
        if entry["current_hash"] != computed_hash:
            return False
        
        expected_previous = entry["current_hash"]
    
    return True


def clear_audit_log():
    """Clear audit log (for testing purposes only)."""
    global _audit_log, _previous_hash
    _audit_log = []
    _previous_hash = "genesis"
