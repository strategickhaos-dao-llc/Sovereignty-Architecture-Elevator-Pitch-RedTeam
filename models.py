# models.py
"""Data models for artifact access control."""
from typing import List, Optional
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Column, JSON


class Artifact(SQLModel, table=True):
    """Artifact model representing classified documents."""
    id: str = Field(primary_key=True)
    classification: str = Field(default="Unclassified")
    summary: str = Field(default="")
    content: str = Field(default="")
    need_to_know: List[str] = Field(default_factory=list, sa_column=Column(JSON))


class RedactionResponse(BaseModel):
    """Response model for redacted artifact access."""
    id: str
    classification: str
    redacted: bool
    reason: str
    visible_preview: str


class PolicyDecision(BaseModel):
    """Policy decision result from OPA evaluation."""
    allowed: bool = False
    redacted: bool = False
    reason: str = ""


class User(BaseModel):
    """User model for access control."""
    id: str
    clearance_level: int = 0
    groups: List[str] = Field(default_factory=list)
