# audit.py
import asyncio
from datetime import datetime
from sqlmodel import SQLModel, Field
from db import async_session


class AuditLog(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: str
    artifact_id: str | None
    action: str
    reason: str
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


async def log_access(request, artifact, action: str, reason: str):
    try:
        artifact_id = artifact.id if hasattr(artifact, "id") else str(artifact)
        log = AuditLog(
            user_id=getattr(request.state, "user_id", "anonymous"),
            artifact_id=artifact_id,
            action=action,
            reason=reason,
        )
        async with async_session() as session:
            session.add(log)
            await session.commit()
    except Exception:
        pass  # fire-and-forget — never block the response
