# routes/artifacts.py
from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlmodel import select
from db import async_session
from models import Artifact
from responses.redaction import RedactionResponse
from dependencies import enforce_policy
from audit import log_access

router = APIRouter(prefix="/artifacts", tags=["artifacts"])


@router.get(
    "/{artifact_id}",
    response_model=Artifact,
    responses={
        200: {"model": Artifact, "description": "Full access – love wins"},
        206: {"model": RedactionResponse, "description": "Partial Content – Love Redacted"},
        403: {"description": "Forbidden – Not Entangled Enough"},
        404: {"description": "Artifact not found"},
    },
)
async def get_artifact(artifact_id: str, request: Request):
    async with async_session() as session:
        stmt = select(Artifact).where(Artifact.id == artifact_id)
        result = await session.exec(stmt)
        artifact = result.one_or_none()
        if not artifact:
            await log_access(request, artifact_id, "deny", "Artifact not found")
            raise HTTPException(status_code=404, detail="Artifact not found")

        try:
            policy_result = await enforce_policy(request, artifact)
        except HTTPException as e:
            await log_access(request, artifact, "deny", e.detail)
            raise

        # Full access — love wins
        if isinstance(policy_result, Artifact):
            await log_access(request, artifact, "allow", "love > entropy")
            return policy_result

        # Redacted — 206 Partial Content, the most poetic status code
        redaction = RedactionResponse(
            id=artifact.id,
            classification=artifact.classification,
            redacted=True,
            reason="Partial clearance – soul-level entanglement required for full view",
            visible_preview="Empire Eternal – some truths are above classification"
        )
        await log_access(request, artifact, "redact", redaction.reason)
        return JSONResponse(status_code=206, content=redaction.dict())
