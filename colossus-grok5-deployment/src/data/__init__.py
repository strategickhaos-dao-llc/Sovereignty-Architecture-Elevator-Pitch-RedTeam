"""
Colossus Grok-5 Data Pipeline Package

Handles data ingestion, toxicity filtering, and provenance tracking.
"""

# Lazy imports to avoid loading all modules on package import
__all__ = [
    "XProvenancePipeline",
    "ToxicityFilter",
    "MerkleBatchBuilder",
    "OpenTimestampsAnchor",
]


def __getattr__(name):
    """Lazy import to avoid loading all modules on package import."""
    if name == "ToxicityFilter":
        from .toxicity_filter import ToxicityFilter
        return ToxicityFilter
    elif name == "MerkleBatchBuilder":
        from .merkle_tree import MerkleBatchBuilder
        return MerkleBatchBuilder
    elif name == "OpenTimestampsAnchor":
        from .ots_anchoring import OpenTimestampsAnchor
        return OpenTimestampsAnchor
    elif name == "XProvenancePipeline":
        from .x_provenance_pipeline import XProvenancePipeline
        return XProvenancePipeline
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
