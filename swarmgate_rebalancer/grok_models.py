"""Pydantic models for Grok JSON output contract."""

from typing import List

from pydantic import BaseModel, Field, field_validator


class Order(BaseModel):
    """Single order in the rebalancing plan."""

    symbol: str = Field(..., description="Asset symbol to trade")
    usd: float = Field(..., gt=0.0, description="Order amount in USD")


class GrokPlan(BaseModel):
    """Grok's rebalancing plan output format."""

    treasury_transfer_usd: float = Field(
        ..., ge=0.0, description="Amount to transfer to treasury in USD"
    )
    treasury_tx: str = Field(..., description="Treasury transaction description")
    orders: List[Order] = Field(default_factory=list, description="List of orders to execute")
    total_invested: float = Field(..., ge=0.0, description="Total amount invested in USD")
    new_cash_buffer: float = Field(..., ge=0.0, description="New cash buffer amount in USD")
    deviation_after: float = Field(
        ..., ge=0.0, description="Expected deviation after rebalancing"
    )

    @field_validator("orders")
    @classmethod
    def validate_orders(cls, v: List[Order]) -> List[Order]:
        """Validate orders list - allow empty if under rebalance threshold."""
        return v

    @field_validator("total_invested")
    @classmethod
    def positive_if_orders(cls, v: float, info) -> float:
        """Validate total_invested is positive if there are orders."""
        orders = info.data.get("orders", [])
        if orders and v <= 0:
            raise ValueError("total_invested must be > 0 if there are orders")
        return v
