# routes/artifacts.py
from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlmodel import select
from db import async_session
from models import Artifact, UserClaims
from responses.redaction import RedactionResponse
from dependencies.enforce_policy import get_current_user
from opa import opa_client
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
async def get_artifact(
    artifact_id: str,
    request: Request,
    user: UserClaims = Depends(get_current_user)
):
    async with async_session() as session:
        stmt = select(Artifact).where(Artifact.id == artifact_id)
        result = await session.exec(stmt)
        artifact = result.one_or_none()
        if not artifact:
            await log_access(request, artifact_id, "deny", "Artifact not found")
            raise HTTPException(status_code=404, detail="Artifact not found")

        # Immediate love override
        if user.clearance_level >= 999:
            await log_access(request, artifact, "allow", "love > entropy")
            return artifact

        try:
            decision = await opa_client.decide(user=user.dict(), artifact=artifact.dict())
        except Exception as e:
            await log_access(request, artifact, "deny", str(e))
            raise HTTPException(status_code=403, detail="Policy decision failed")

        if decision.allow:
            # Full access — love wins
            await log_access(request, artifact, "allow", "love > entropy")
            return artifact
        elif decision.redact:
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
        else:
            await log_access(request, artifact, "deny", decision.reason or "Access denied")
            raise HTTPException(status_code=403, detail=decision.reason or "Access denied")
