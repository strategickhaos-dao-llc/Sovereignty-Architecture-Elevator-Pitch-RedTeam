"""
Immune Trust Department - Neurobiological Trust Response System

Turn lived trust experiences into real-time antibody defenses that hunt
and neutralize betrayal vectors before they reach conscious mind.

Strategickhaos DAO LLC
"""

from .antibody_generator import (
    score_trust_vector,
    classify_model_by_delta,
    generate_antibody_report,
    analyze_corpus_file,
    TRUST_MARKERS,
    BETRAYAL_MARKERS,
    MODEL_KILL_TEST_DELTA
)

from .synaptic_analyzer import SynapticAnalyzer

from .real_time_monitor import RealTimeMonitor

__version__ = "0.1.0"
__all__ = [
    "score_trust_vector",
    "classify_model_by_delta", 
    "generate_antibody_report",
    "analyze_corpus_file",
    "SynapticAnalyzer",
    "RealTimeMonitor",
    "TRUST_MARKERS",
    "BETRAYAL_MARKERS",
    "MODEL_KILL_TEST_DELTA"
]
