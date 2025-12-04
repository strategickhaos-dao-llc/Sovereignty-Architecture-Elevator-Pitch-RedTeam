"""
Sovereign Swarm Cognitive OS Module

SPL (Sovereign Pattern Language) compliant implementation
of the Pattern-Dominant Cognitive Architecture.
"""

from .cognitive_os import (
    PatternEngine,
    SchemaSynthesizer,
    ContradictionResolver,
    ContextInterpreter,
    ExternalizationAdapter,
    CognitiveOS,
)

__all__ = [
    "PatternEngine",
    "SchemaSynthesizer",
    "ContradictionResolver",
    "ContextInterpreter",
    "ExternalizationAdapter",
    "CognitiveOS",
]

__version__ = "1.0.0"
