"""
HMAC Verification Module

Provides cryptographic signature verification for webhooks.

LLM Directive: When adding new webhook sources:
1. Add source-specific verification function
2. Use constant-time comparison to prevent timing attacks
3. Support multiple signature algorithms if needed
"""

import hmac
import hashlib
import logging
from typing import Optional

logger = logging.getLogger(__name__)


def verify_signature(
    body: bytes,
    signature: str,
    secret: str,
    algorithm: str = "sha256"
) -> bool:
    """
    Verify HMAC signature for a webhook payload.
    
    Args:
        body: Raw request body bytes
        signature: Signature from request header
        secret: Shared secret key
        algorithm: Hash algorithm (default: sha256)
        
    Returns:
        True if signature is valid, False otherwise
    """
    if not secret:
        logger.warning("No secret configured - skipping verification")
        return True
    
    if not signature:
        logger.warning("No signature provided")
        return False
    
    try:
        # Compute expected signature
        expected = hmac.new(
            secret.encode(),
            body,
            getattr(hashlib, algorithm)
        ).hexdigest()
        
        # Handle different signature formats
        if signature.startswith(f"{algorithm}="):
            signature = signature[len(algorithm) + 1:]
        
        # Constant-time comparison to prevent timing attacks
        return hmac.compare_digest(expected, signature)
    except Exception as e:
        logger.error("Signature verification error: %s", e)
        return False


def verify_github_signature(
    body: bytes,
    signature: str,
    secret: str
) -> bool:
    """
    Verify GitHub webhook signature.
    
    GitHub uses X-Hub-Signature-256 header with format: sha256=<hex>
    
    Args:
        body: Raw request body bytes
        signature: X-Hub-Signature-256 header value
        secret: GitHub webhook secret
        
    Returns:
        True if signature is valid, False otherwise
    """
    if not secret:
        logger.warning("No GitHub webhook secret configured")
        return True
    
    if not signature:
        logger.warning("No GitHub signature provided")
        return False
    
    try:
        # Compute expected signature
        expected = "sha256=" + hmac.new(
            secret.encode(),
            body,
            hashlib.sha256
        ).hexdigest()
        
        # Constant-time comparison
        return hmac.compare_digest(expected, signature)
    except Exception as e:
        logger.error("GitHub signature verification error: %s", e)
        return False


def verify_gitlab_signature(
    token: str,
    expected_token: str
) -> bool:
    """
    Verify GitLab webhook token.
    
    GitLab uses X-Gitlab-Token header with a secret token.
    
    Args:
        token: X-Gitlab-Token header value
        expected_token: Configured webhook token
        
    Returns:
        True if token matches, False otherwise
    """
    if not expected_token:
        logger.warning("No GitLab webhook token configured")
        return True
    
    if not token:
        logger.warning("No GitLab token provided")
        return False
    
    return hmac.compare_digest(token, expected_token)


def verify_alertmanager_signature(
    body: bytes,
    signature: str,
    secret: str
) -> bool:
    """
    Verify Alertmanager webhook signature.
    
    LLM Directive: Alertmanager doesn't have built-in signing.
    If you need authentication, use:
    - HTTP Basic Auth
    - Custom HMAC signing
    - Network policies
    """
    # Alertmanager typically doesn't use signatures
    # This is a placeholder for custom implementations
    if not secret:
        return True
    
    return verify_signature(body, signature, secret)


def generate_signature(
    body: bytes,
    secret: str,
    algorithm: str = "sha256"
) -> str:
    """
    Generate an HMAC signature for a payload.
    
    Useful for testing or sending signed webhooks.
    
    Args:
        body: Payload bytes
        secret: Shared secret key
        algorithm: Hash algorithm
        
    Returns:
        Signature string with algorithm prefix
    """
    sig = hmac.new(
        secret.encode(),
        body,
        getattr(hashlib, algorithm)
    ).hexdigest()
    
    return f"{algorithm}={sig}"
