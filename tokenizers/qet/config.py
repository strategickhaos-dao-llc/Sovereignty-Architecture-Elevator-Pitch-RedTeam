"""
QET Configuration Module
Implements improvements: #8 (deterministic randomness), #18 (quantum config in YAML)
"""

import os
import json
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any
from pathlib import Path


@dataclass
class QuantumConfig:
    """Quantum layer configuration - Improvement #18"""
    num_qubits: int = 8
    ansatz_type: str = "QAOA"  # QAOA, VQE, HEA
    max_iterations: int = 100
    entropy_threshold: float = 0.5
    backend_type: str = "fake"  # fake, qutip, qiskit, hardware
    boundary_threshold: float = 0.5
    use_gradient: bool = False  # Improvement #13
    segment_size: int = 256  # Improvement #12
    cache_solutions: bool = True  # Improvement #16
    circuit_depth_low_entropy: int = 2  # Improvement #15
    circuit_depth_high_entropy: int = 8


@dataclass
class GAConfig:
    """Genetic Algorithm configuration"""
    population_size: int = 50
    generations: int = 100
    mutation_rate: float = 0.1
    crossover_rate: float = 0.8
    elite_size: int = 5
    stagnation_threshold: int = 10  # Improvement #9
    catastrophic_mutation_rate: float = 0.3
    byte_validity_check: bool = True  # Improvement #3
    ngram_guided_mutation: bool = True  # Improvement #3
    min_context_coverage: float = 0.1  # Improvement #5
    min_occurrence_count: int = 2  # Improvement #5


@dataclass
class FitnessConfig:
    """Multi-objective fitness configuration - Improvement #4"""
    use_pareto: bool = True
    compression_weight: float = 0.3
    sparsity_weight: float = 0.2
    oov_weight: float = 0.25
    perplexity_weight: float = 0.25


@dataclass
class EvolutionConfig:
    """Hierarchical evolution configuration - Improvement #6"""
    hierarchical: bool = True
    subword_generations: int = 50
    phrase_generations: int = 30
    subword_mutation_rate: float = 0.15
    phrase_mutation_rate: float = 0.08


@dataclass
class CompatibilityConfig:
    """Base tokenizer compatibility - Improvement #7"""
    enable_mapping: bool = False
    base_tokenizer: str = "cl100k_base"  # tiktoken model
    mapping_cache_path: Optional[str] = None


@dataclass
class SafetyConfig:
    """Safety and robustness configuration - Improvements #28-31"""
    max_tokens_per_char_ratio: float = 2.0  # Improvement #29
    enable_differential_privacy: bool = False  # Improvement #30
    dp_noise_scale: float = 1.0
    adversarial_fuzz_test: bool = True  # Improvement #28
    redteam_mode: bool = False  # Improvement #31
    injection_penalty_weight: float = 0.5


@dataclass
class QETConfig:
    """
    Master configuration for QuantumEvoTokenizer.
    Implements all 36 improvements in a YAML-configurable format.
    """
    # Mode configuration - Improvement #1
    mode: str = "analysis"  # "analysis" or "production"
    
    # Core settings
    vocab_size: int = 50000
    seed: int = 42  # Improvement #8
    
    # Sub-configurations
    quantum: QuantumConfig = field(default_factory=QuantumConfig)
    ga: GAConfig = field(default_factory=GAConfig)
    fitness: FitnessConfig = field(default_factory=FitnessConfig)
    evolution: EvolutionConfig = field(default_factory=EvolutionConfig)
    compatibility: CompatibilityConfig = field(default_factory=CompatibilityConfig)
    safety: SafetyConfig = field(default_factory=SafetyConfig)
    
    # Artifact management - Improvements #22, #36
    output_dir: str = "artifacts/qet"
    enable_notarization: bool = True
    version_tag: Optional[str] = None
    
    # Experiment tracking - Improvement #19
    experiment_name: Optional[str] = None
    contexts: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Ensure nested configs are proper dataclass instances."""
        if isinstance(self.quantum, dict):
            self.quantum = QuantumConfig(**self.quantum)
        if isinstance(self.ga, dict):
            self.ga = GAConfig(**self.ga)
        if isinstance(self.fitness, dict):
            self.fitness = FitnessConfig(**self.fitness)
        if isinstance(self.evolution, dict):
            self.evolution = EvolutionConfig(**self.evolution)
        if isinstance(self.compatibility, dict):
            self.compatibility = CompatibilityConfig(**self.compatibility)
        if isinstance(self.safety, dict):
            self.safety = SafetyConfig(**self.safety)
    
    @classmethod
    def from_yaml(cls, path: str) -> "QETConfig":
        """Load configuration from YAML file."""
        import yaml
        with open(path, "r") as f:
            data = yaml.safe_load(f)
        
        # Extract QET-specific config if nested under tokenizer_config
        if "tokenizer_config" in data:
            data = data["tokenizer_config"]
        elif "qet" in data:
            data = data["qet"]
        
        return cls(**data)
    
    @classmethod
    def from_json(cls, path: str) -> "QETConfig":
        """Load configuration from JSON file."""
        with open(path, "r") as f:
            data = json.load(f)
        return cls(**data)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return asdict(self)
    
    def to_yaml(self, path: str) -> None:
        """Save configuration to YAML file."""
        import yaml
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            yaml.safe_dump(self.to_dict(), f, default_flow_style=False)
    
    def to_json(self, path: str) -> None:
        """Save configuration to JSON file."""
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            json.dump(self.to_dict(), f, indent=2)
    
    def validate(self) -> List[str]:
        """Validate configuration and return list of warnings."""
        warnings = []
        
        if self.mode == "production" and self.ga.generations > 0:
            warnings.append(
                "Production mode with GA enabled may cause instability. "
                "Consider using frozen vocab."
            )
        
        if self.quantum.num_qubits > 16:
            warnings.append(
                f"High qubit count ({self.quantum.num_qubits}) may cause "
                "exponential slowdown in simulation."
            )
        
        if self.safety.max_tokens_per_char_ratio < 1.0:
            warnings.append(
                "max_tokens_per_char_ratio < 1.0 may cause encoding failures."
            )
        
        if self.evolution.hierarchical and not self.ga.ngram_guided_mutation:
            warnings.append(
                "Hierarchical evolution works better with n-gram guided mutation."
            )
        
        return warnings
    
    @classmethod
    def production_default(cls) -> "QETConfig":
        """Create a production-ready configuration."""
        config = cls(mode="production")
        config.ga.generations = 0  # Frozen vocab
        config.quantum.backend_type = "fake"  # Fast deterministic
        config.enable_notarization = True
        return config
    
    @classmethod
    def research_default(cls) -> "QETConfig":
        """Create a research/analysis configuration."""
        config = cls(mode="analysis")
        config.ga.generations = 100
        config.fitness.use_pareto = True
        config.evolution.hierarchical = True
        return config
