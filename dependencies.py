# dependencies.py
"""Dependencies for policy enforcement."""
import hashlib
import json
import os
from typing import Optional
import httpx
from fastapi import Request
from models import Artifact, PolicyDecision, User


OPA_URL = os.getenv("OPA_URL", "http://localhost:8181/v1/data/artifact/access")


async def get_current_user(request: Request) -> User:
    """Extract user information from request authorization header."""
    auth_header = request.headers.get("Authorization", "")
    
    # In production, decode JWT token to get user info
    # This is a simplified extraction for demonstration
    if not auth_header.startswith("Bearer "):
        return User(id="anonymous", clearance_level=0, groups=[])
    
    token = auth_header[7:]
    
    # Simulate different access levels based on token prefix
    if token.startswith("full_"):
        return User(id="authorized_user", clearance_level=4, groups=["admin", "top-secret"])
    elif token.startswith("partial_"):
        return User(id="partial_user", clearance_level=2, groups=["internal"])
    else:
        return User(id="basic_user", clearance_level=0, groups=[])


async def enforce_policy(request: Request, artifact: Artifact) -> PolicyDecision:
    """Evaluate OPA policy to determine access decision."""
    user = await get_current_user(request)
    
    policy_input = {
        "user": {
            "id": user.id,
            "clearance_level": user.clearance_level,
            "groups": user.groups,
        },
        "artifact": {
            "id": artifact.id,
            "classification": artifact.classification,
            "need_to_know": artifact.need_to_know if artifact.need_to_know else [],
        },
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                OPA_URL,
                json={"input": policy_input},
                timeout=5.0,
            )
            if response.status_code == 200:
                result = response.json().get("result", {})
                return PolicyDecision(
                    allowed=result.get("allow", False),
                    redacted=result.get("redacted", False),
                    reason=result.get("reason", "policy evaluation completed"),
                )
    except httpx.RequestError:
        # Fallback to local policy evaluation if OPA is unavailable
        pass
    
    # Local fallback policy evaluation
    return evaluate_local_policy(user, artifact)


def evaluate_local_policy(user: User, artifact: Artifact) -> PolicyDecision:
    """Local fallback policy evaluation when OPA is unavailable."""
    classification_rank = {
        "Unclassified": 0,
        "Internal": 1,
        "Confidential": 2,
        "Secret": 3,
        "Top-Secret": 4,
    }
    
    rank = classification_rank.get(artifact.classification, 0)
    need_to_know = artifact.need_to_know if artifact.need_to_know else []
    
    # Check full access
    if user.clearance_level >= rank:
        if len(need_to_know) == 0:
            return PolicyDecision(
                allowed=True,
                redacted=False,
                reason="full clearance and NTK satisfied"
            )
        if any(group in need_to_know for group in user.groups):
            return PolicyDecision(
                allowed=True,
                redacted=False,
                reason="full clearance and NTK satisfied"
            )
    
    # Check redacted access
    if user.clearance_level >= rank - 1:
        return PolicyDecision(
            allowed=False,
            redacted=True,
            reason="partial clearance – redacted preview"
        )
    
    return PolicyDecision(
        allowed=False,
        redacted=False,
        reason="insufficient clearance or NTK"
    )
