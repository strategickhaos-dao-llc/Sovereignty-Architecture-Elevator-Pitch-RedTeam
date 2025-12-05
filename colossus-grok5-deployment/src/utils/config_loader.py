"""
Configuration Loader

Loads and validates configuration for Colossus Grok-5 deployment.
"""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

import yaml


@dataclass
class TrainingConfig:
    """Training configuration."""

    batch_size: int = 4096
    learning_rate: float = 0.0001
    warmup_steps: int = 1000
    max_steps: int = 1000000
    checkpoint_interval: int = 1000


@dataclass
class EnergyConfig:
    """Energy management configuration."""

    power_limit_mw: float = 250.0
    offpeak_start: str = "02:00"
    offpeak_end: str = "06:00"
    megapack_soc_min: float = 0.4


@dataclass
class SafetyConfig:
    """Safety thresholds configuration."""

    hallucination_threshold: float = 0.15
    bias_threshold: float = 0.25
    checkpoint_consensus_min: float = 0.99
    toxicity_threshold: float = 0.30


@dataclass
class ProvenanceConfig:
    """Data provenance configuration."""

    batch_size: int = 1000
    merkle_enabled: bool = True
    ots_enabled: bool = True


@dataclass
class Grok5Config:
    """Complete Grok-5 configuration."""

    training: TrainingConfig = field(default_factory=TrainingConfig)
    energy: EnergyConfig = field(default_factory=EnergyConfig)
    safety: SafetyConfig = field(default_factory=SafetyConfig)
    provenance: ProvenanceConfig = field(default_factory=ProvenanceConfig)


class ConfigLoader:
    """
    Configuration loader for Grok-5 deployment.

    Loads configuration from YAML files with environment variable overrides.
    """

    def __init__(
        self,
        config_path: Optional[str] = None,
        env_prefix: str = "GROK5_",
    ):
        """
        Initialize configuration loader.

        Args:
            config_path: Path to YAML config file
            env_prefix: Prefix for environment variable overrides
        """
        self.config_path = config_path or os.getenv(
            "GROK5_CONFIG_PATH",
            "/etc/grok5/config.yaml",
        )
        self.env_prefix = env_prefix
        self._config: Optional[Grok5Config] = None

    def load(self) -> Grok5Config:
        """
        Load configuration from file and environment.

        Returns:
            Grok5Config instance
        """
        if self._config is not None:
            return self._config

        # Load from YAML if exists
        config_dict = self._load_yaml()

        # Apply environment overrides
        config_dict = self._apply_env_overrides(config_dict)

        # Build config object
        self._config = self._build_config(config_dict)
        return self._config

    def _load_yaml(self) -> dict[str, Any]:
        """Load configuration from YAML file."""
        path = Path(self.config_path)
        if not path.exists():
            return {}

        with open(path, "r") as f:
            return yaml.safe_load(f) or {}

    def _apply_env_overrides(self, config: dict[str, Any]) -> dict[str, Any]:
        """Apply environment variable overrides."""
        # Training overrides
        if "training" not in config:
            config["training"] = {}

        if batch_size := os.getenv(f"{self.env_prefix}BATCH_SIZE"):
            config["training"]["batch_size"] = int(batch_size)
        if learning_rate := os.getenv(f"{self.env_prefix}LEARNING_RATE"):
            config["training"]["learning_rate"] = float(learning_rate)

        # Energy overrides
        if "energy" not in config:
            config["energy"] = {}

        if power_limit := os.getenv(f"{self.env_prefix}POWER_LIMIT_MW"):
            config["energy"]["power_limit_mw"] = float(power_limit)
        if soc_min := os.getenv(f"{self.env_prefix}MEGAPACK_SOC_MIN"):
            config["energy"]["megapack_soc_min"] = float(soc_min)

        # Safety overrides
        if "safety" not in config:
            config["safety"] = {}

        if halluc := os.getenv(f"{self.env_prefix}HALLUCINATION_THRESHOLD"):
            config["safety"]["hallucination_threshold"] = float(halluc)
        if bias := os.getenv(f"{self.env_prefix}BIAS_THRESHOLD"):
            config["safety"]["bias_threshold"] = float(bias)
        if consensus := os.getenv(f"{self.env_prefix}CHECKPOINT_CONSENSUS_MIN"):
            config["safety"]["checkpoint_consensus_min"] = float(consensus)
        if toxicity := os.getenv(f"{self.env_prefix}TOXICITY_THRESHOLD"):
            config["safety"]["toxicity_threshold"] = float(toxicity)

        return config

    def _build_config(self, config_dict: dict[str, Any]) -> Grok5Config:
        """Build config object from dictionary."""
        training = TrainingConfig(**config_dict.get("training", {}))
        energy = EnergyConfig(**config_dict.get("energy", {}))
        safety = SafetyConfig(**config_dict.get("safety", {}))
        provenance = ProvenanceConfig(**config_dict.get("provenance", {}))

        return Grok5Config(
            training=training,
            energy=energy,
            safety=safety,
            provenance=provenance,
        )

    def reload(self) -> Grok5Config:
        """Force reload configuration."""
        self._config = None
        return self.load()
