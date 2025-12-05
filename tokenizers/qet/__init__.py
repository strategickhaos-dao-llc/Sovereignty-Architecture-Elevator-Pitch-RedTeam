"""
QET (Quantum-Evolutionary Tokenizer) Module
Implements 36 concrete improvements for sovereign tokenization.

Strategickhaos DAO LLC - Sovereign AI Systems
"""

from .quantum_evo_tokenizer import QuantumEvoTokenizer
from .config import QETConfig
from .quantum_backend import (
    QuantumBackend,
    FakeQuantumBackend,
    ClassicalBoundaryOptimizer,
    create_backend,
)
from .ga_optimizer import GAOptimizer, HierarchicalGAOptimizer, Individual
from .vocab_manager import VocabManager, VocabMetrics, StableEncoder
from .safety import TokenizerSafetyChecker, DifferentialPrivacyManager
from .visualization import (
    generate_html_visualization,
    save_visualization,
    visualize_tokenizer_output,
)

__version__ = "1.0.0"

__all__ = [
    # Core
    "QuantumEvoTokenizer",
    "QETConfig",
    # Quantum
    "QuantumBackend",
    "FakeQuantumBackend",
    "ClassicalBoundaryOptimizer",
    "create_backend",
    # GA
    "GAOptimizer",
    "HierarchicalGAOptimizer",
    "Individual",
    # Vocab
    "VocabManager",
    "VocabMetrics",
    "StableEncoder",
    # Safety
    "TokenizerSafetyChecker",
    "DifferentialPrivacyManager",
    # Visualization
    "generate_html_visualization",
    "save_visualization",
    "visualize_tokenizer_output",
]
