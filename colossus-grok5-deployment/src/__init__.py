"""
Colossus Grok-5 Deployment Suite

Artifact #3558 - Production deployment package for Grok-5 on Colossus / 550K GPUs.
"""

__version__ = "1.0.0"
__artifact__ = "3558"

from .data import (
    XProvenancePipeline,
    ToxicityFilter,
    MerkleBatchBuilder,
    OpenTimestampsAnchor,
)

from .training import (
    EnergyScheduler,
    PowerWindowDecision,
    ConsensusProtocol,
    CheckpointConsensus,
    CheckpointGuardian,
    Grok5Trainer,
)

from .verification import (
    SafetyGate,
    SafetyReport,
    UnifiedVerifier,
    AuditLogger,
    AuditEvent,
)

from .utils import (
    blake3_hex,
    blake3_bytes,
    ConfigLoader,
)

__all__ = [
    # Data
    "XProvenancePipeline",
    "ToxicityFilter",
    "MerkleBatchBuilder",
    "OpenTimestampsAnchor",
    # Training
    "EnergyScheduler",
    "PowerWindowDecision",
    "ConsensusProtocol",
    "CheckpointConsensus",
    "CheckpointGuardian",
    "Grok5Trainer",
    # Verification
    "SafetyGate",
    "SafetyReport",
    "UnifiedVerifier",
    "AuditLogger",
    "AuditEvent",
    # Utils
    "blake3_hex",
    "blake3_bytes",
    "ConfigLoader",
]
