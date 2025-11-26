# models.py
from typing import Optional, List
from sqlmodel import SQLModel, Field


class Artifact(SQLModel, table=True):
    id: str = Field(primary_key=True)
    classification: str
    summary: str
    content: str
    owner_id: Optional[str] = None


class UserClaims(SQLModel):
    user_id: str
    clearance_level: int = 0
    groups: List[str] = Field(default_factory=list)
