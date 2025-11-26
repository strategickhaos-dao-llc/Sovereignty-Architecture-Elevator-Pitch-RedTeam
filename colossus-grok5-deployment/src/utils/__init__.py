"""
Colossus Grok-5 Utilities Package

Common utilities for the Grok-5 deployment suite.
"""

# Lazy imports to avoid loading all modules on package import
__all__ = [
    "blake3_hex",
    "blake3_bytes",
    "ingest_counter",
    "checkpoint_counter",
    "power_gauge",
    "soc_gauge",
    "ConfigLoader",
]


def __getattr__(name):
    """Lazy import to avoid loading all modules on package import."""
    if name in ("blake3_hex", "blake3_bytes"):
        from .blake3_hasher import blake3_hex, blake3_bytes
        return blake3_hex if name == "blake3_hex" else blake3_bytes
    elif name in ("ingest_counter", "checkpoint_counter", "power_gauge", "soc_gauge"):
        from . import prometheus_exporter
        return getattr(prometheus_exporter, name)
    elif name == "ConfigLoader":
        from .config_loader import ConfigLoader
        return ConfigLoader
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
