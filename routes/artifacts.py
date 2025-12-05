# routes/artifacts.py
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import select
from db import async_session
from models import Artifact, RedactionResponse
from dependencies import enforce_policy
from audit import log_access

router = APIRouter(prefix="/artifacts", tags=["artifacts"])

@router.get(
    "/{artifact_id}",
    response_model=Artifact,
    responses={
        200: {"description": "Full access granted by policy"},
        206: {"model": RedactionResponse, "description": "Partial Content – content redacted"},
        403: {"description": "Forbidden by policy"},
        404: {"description": "Artifact not found"},
    },
)
async def get_artifact(artifact_id: str, request: Request):
    async with async_session() as session:
        result = await session.exec(select(Artifact).where(Artifact.id == artifact_id))
        artifact = result.one_or_none()
        if not artifact:
            await log_access(request, None, "deny", "Artifact not found")
            raise HTTPException(status_code=404)

        decision = await enforce_policy(request, artifact)

        if decision.allowed:
            await log_access(request, artifact, "allow", decision.reason)
            return artifact

        if decision.redacted:
            redaction = RedactionResponse(
                id=artifact.id,
                classification=artifact.classification,
                redacted=True,
                reason=decision.reason,
                visible_preview="Empire Eternal – access restricted by policy"
            )
            await log_access(request, artifact, "redact", redaction.reason)
            return JSONResponse(status_code=206, content=redaction.model_dump())

        await log_access(request, artifact, "deny", decision.reason)
        raise HTTPException(status_code=403, detail="Access denied by policy")
