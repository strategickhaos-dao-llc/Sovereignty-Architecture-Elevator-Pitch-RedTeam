"""Pydantic models for flow.yaml schema (v1)."""

from pathlib import Path
from typing import Dict, Literal

import yaml
from pydantic import BaseModel, Field, field_validator


class PortfolioTargets(BaseModel):
    """Portfolio target allocations and current state."""

    target: Dict[str, float] = Field(
        ..., description="symbol -> target weight 0..1"
    )
    current: Dict[str, float] = Field(
        default_factory=dict,
        description="symbol -> current value in base currency; populated upstream",
    )

    @field_validator("target")
    @classmethod
    def weights_sum_to_one(cls, v: Dict[str, float]) -> Dict[str, float]:
        """Validate that target weights sum to 1.0."""
        s = round(sum(v.values()), 6)
        if abs(s - 1.0) > 1e-6:
            raise ValueError(f"portfolio.target weights must sum to 1.0, got {s}")
        return v


class Settings(BaseModel):
    """Configuration settings for rebalancing."""

    paycheck_net: float = Field(..., description="Net paycheck amount in base currency")
    treasury_pct: float = Field(..., ge=0.0, le=1.0, description="Treasury allocation percentage")
    rebalance_threshold: float = Field(
        ..., ge=0.0, le=0.5, description="Deviation threshold to trigger rebalance"
    )
    dry_run: bool = Field(default=True, description="Whether to run in dry-run mode")
    treasury_address: str = Field(..., description="Treasury wallet address")
    base_currency: Literal["USD"] = Field(default="USD", description="Base currency")
    max_slippage_pct: float = Field(
        default=0.01, ge=0.0, le=0.1, description="Maximum slippage percentage"
    )
    max_single_order_usd: float = Field(
        default=5000, gt=0.0, description="Maximum single order size in USD"
    )


class FlowConfig(BaseModel):
    """Root configuration model for flow.yaml."""

    version: int = Field(default=1, description="Schema version")
    portfolio: PortfolioTargets
    settings: Settings


def load_flow_config(path: str | Path) -> FlowConfig:
    """Load and validate flow configuration from YAML file.

    Args:
        path: Path to the flow.yaml file.

    Returns:
        Validated FlowConfig instance.

    Raises:
        FileNotFoundError: If the file doesn't exist.
        ValidationError: If the configuration is invalid.
    """
    with open(path, "r") as f:
        data = yaml.safe_load(f)
    return FlowConfig.model_validate(data)
