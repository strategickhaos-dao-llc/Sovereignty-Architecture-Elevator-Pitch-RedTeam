"""
Colossus Grok-5 Verification Package

Safety gates and audit logging for deployment verification.
"""

# Lazy imports to avoid loading all modules on package import
__all__ = [
    "SafetyGate",
    "SafetyReport",
    "UnifiedVerifier",
    "AuditLogger",
    "AuditEvent",
]


def __getattr__(name):
    """Lazy import to avoid loading all modules on package import."""
    if name in ("SafetyGate", "SafetyReport"):
        from .safety_gate import SafetyGate, SafetyReport
        return SafetyGate if name == "SafetyGate" else SafetyReport
    elif name == "UnifiedVerifier":
        from .unified_verifier import UnifiedVerifier
        return UnifiedVerifier
    elif name in ("AuditLogger", "AuditEvent"):
        from .audit_logger import AuditLogger, AuditEvent
        return AuditLogger if name == "AuditLogger" else AuditEvent
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
