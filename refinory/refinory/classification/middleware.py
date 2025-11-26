"""
FastAPI middleware for classification-based access control.
Extracts user clearance from JWT tokens and enforces access policies.
"""

from functools import wraps
from typing import Callable, List, Optional

import jwt
import structlog
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .models import (
    AccessDecision,
    ArtifactClassification,
    ClassificationLevel,
    UserClearance,
)
from .policy import PolicyEngine, get_policy_engine

logger = structlog.get_logger()

# Security scheme for Bearer token authentication
security = HTTPBearer(auto_error=False)


class ClassificationMiddleware:
    """
    Middleware for classification-based access control.
    Validates JWT tokens and extracts user clearance.
    """

    def __init__(
        self,
        jwt_secret: str,
        jwt_algorithm: str = "HS256",
        jwt_audience: Optional[str] = None,
        jwt_issuer: Optional[str] = None,
    ):
        self.jwt_secret = jwt_secret
        self.jwt_algorithm = jwt_algorithm
        self.jwt_audience = jwt_audience
        self.jwt_issuer = jwt_issuer

    def decode_token(self, token: str) -> dict:
        """Decode and validate JWT token."""
        try:
            # Build options dict with non-None values only
            options = {
                k: v for k, v in [
                    ("audience", self.jwt_audience),
                    ("issuer", self.jwt_issuer)
                ] if v is not None
            }

            payload = jwt.decode(
                token,
                self.jwt_secret,
                algorithms=[self.jwt_algorithm],
                **options,
            )
            return payload
        except jwt.ExpiredSignatureError as e:
            logger.warning("JWT token expired", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.InvalidTokenError as e:
            logger.warning("Invalid JWT token", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def get_user_clearance(self, token: str) -> UserClearance:
        """Extract user clearance from JWT token."""
        claims = self.decode_token(token)
        return UserClearance.from_jwt_claims(claims)


# Request-scoped clearance storage
_request_clearance: dict = {}


async def get_current_user_clearance(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> Optional[UserClearance]:
    """
    FastAPI dependency to extract user clearance from request.
    Returns None if no authentication provided.
    """
    if credentials is None:
        return None

    # Check if middleware is configured
    middleware = getattr(request.app.state, "classification_middleware", None)
    if middleware is None:
        logger.warning("Classification middleware not configured")
        return None

    try:
        clearance = middleware.get_user_clearance(credentials.credentials)
        # Store in request state for later use
        request.state.user_clearance = clearance
        return clearance
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to extract user clearance", error=str(e))
        return None


async def require_authentication(
    clearance: Optional[UserClearance] = Depends(get_current_user_clearance),
) -> UserClearance:
    """
    FastAPI dependency that requires authentication.
    Raises 401 if no valid clearance found.
    """
    if clearance is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if clearance.is_expired():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Clearance has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return clearance


def require_clearance(
    minimum_level: ClassificationLevel,
    required_groups: Optional[List[str]] = None,
    required_roles: Optional[List[str]] = None,
):
    """
    Decorator/dependency factory for requiring minimum clearance level.

    Usage:
        @app.get("/secret-data")
        async def get_secret(
            clearance: UserClearance = Depends(
                require_clearance(ClassificationLevel.SECRET)
            )
        ):
            ...
    """

    async def dependency(
        clearance: UserClearance = Depends(require_authentication),
    ) -> UserClearance:
        from .models import ClassificationRank

        minimum_rank = ClassificationRank.from_level(minimum_level)

        # Check clearance level
        if clearance.clearance_rank < minimum_rank:
            logger.warning(
                "Insufficient clearance",
                user_id=clearance.user_id,
                user_clearance=clearance.clearance_level.value,
                required_clearance=minimum_level.value,
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires {minimum_level.value} clearance or higher",
            )

        # Check required groups
        if required_groups:
            if not any(clearance.has_group(g) for g in required_groups):
                logger.warning(
                    "Missing required group",
                    user_id=clearance.user_id,
                    user_groups=list(clearance.groups),
                    required_groups=required_groups,
                )
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Missing required group membership",
                )

        # Check required roles
        if required_roles:
            if not any(clearance.has_role(r) for r in required_roles):
                logger.warning(
                    "Missing required role",
                    user_id=clearance.user_id,
                    user_roles=list(clearance.roles),
                    required_roles=required_roles,
                )
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Missing required role",
                )

        return clearance

    return dependency


async def check_artifact_access(
    user: UserClearance,
    artifact_classification: ArtifactClassification,
    policy_engine: Optional[PolicyEngine] = None,
) -> AccessDecision:
    """
    Check if a user can access an artifact based on classification.
    Returns an AccessDecision with the result.
    """
    if policy_engine is None:
        policy_engine = get_policy_engine()

    decision = policy_engine.evaluate(user, artifact_classification)

    logger.info(
        "Access decision made",
        user_id=user.user_id,
        artifact_classification=artifact_classification.classification.value,
        allowed=decision.allowed,
        reason=decision.reason.value,
        partial_access=decision.partial_access,
    )

    return decision


def enforce_classification(
    artifact_getter: Callable,
):
    """
    Decorator for endpoints that return classified artifacts.
    Automatically checks access and applies redaction if needed.

    Usage:
        @app.get("/artifacts/{artifact_id}")
        @enforce_classification(get_artifact_classification)
        async def get_artifact(artifact_id: str, ...):
            ...
    """

    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(
            *args,
            clearance: UserClearance = Depends(require_authentication),
            policy_engine: PolicyEngine = Depends(get_policy_engine),
            **kwargs,
        ):
            # Get artifact classification
            classification = await artifact_getter(*args, **kwargs)

            # Check access
            decision = await check_artifact_access(
                clearance, classification, policy_engine
            )

            if not decision.allowed:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Access denied: {decision.reason.value}",
                )

            # Call the original function
            result = await func(*args, clearance=clearance, **kwargs)

            # Apply redaction if partial access
            if decision.partial_access and decision.redacted_fields:
                from .redaction import redact_artifact

                result = redact_artifact(result, decision.redacted_fields)

            return result

        return wrapper

    return decorator
