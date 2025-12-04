#!/usr/bin/env python3
"""
mint_token.py - Generate JWT tokens for Sovereign Swarm nodes
Part of Sovereign Swarm — Zero-Trust AI Orchestration Mesh
Apache-2.0 License

Usage:
    python mint_token.py <node_id> [--expiry HOURS]
"""

import argparse
import base64
import hashlib
import hmac
import json
import os
import sys
import time
from typing import Optional


def b64url_encode(data: bytes) -> str:
    """URL-safe base64 encoding without padding."""
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def create_jwt_header() -> dict:
    """Create JWT header."""
    return {"alg": "HS256", "typ": "JWT"}


def create_jwt_payload(
    node_id: str,
    expiry_hours: int = 24,
    issuer: str = "sovereign-swarm",
) -> dict:
    """Create JWT payload for node authentication."""
    now = int(time.time())
    return {
        "iss": issuer,
        "sub": node_id,
        "iat": now,
        "exp": now + (expiry_hours * 3600),
        "nbf": now,
        "jti": hashlib.sha256(f"{node_id}{now}".encode()).hexdigest()[:16],
        "claims": {
            "node_id": node_id,
            "permissions": ["swarm.publish", "swarm.subscribe"],
        },
    }


def sign_jwt(header: dict, payload: dict, secret: bytes) -> str:
    """Sign JWT with HMAC-SHA256."""
    header_b64 = b64url_encode(json.dumps(header).encode())
    payload_b64 = b64url_encode(json.dumps(payload).encode())
    message = f"{header_b64}.{payload_b64}"
    signature = hmac.new(secret, message.encode(), hashlib.sha256).digest()
    signature_b64 = b64url_encode(signature)
    return f"{message}.{signature_b64}"


def mint_token(
    node_id: str,
    secret: Optional[bytes] = None,
    expiry_hours: int = 24,
) -> str:
    """Mint a new JWT token for a node."""
    if secret is None:
        # In production, load from secure storage
        secret_env = os.environ.get("SWARM_JWT_SECRET")
        if secret_env:
            secret = secret_env.encode()
        else:
            raise ValueError(
                "SWARM_JWT_SECRET environment variable is required. "
                "Generate a secure secret with: openssl rand -base64 32"
            )

    header = create_jwt_header()
    payload = create_jwt_payload(node_id, expiry_hours)
    return sign_jwt(header, payload, secret)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Mint JWT tokens for Sovereign Swarm nodes"
    )
    parser.add_argument("node_id", help="Node identifier")
    parser.add_argument(
        "--expiry",
        type=int,
        default=24,
        help="Token expiry in hours (default: 24)",
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Output file (default: stdout)",
    )

    args = parser.parse_args()

    token = mint_token(args.node_id, expiry_hours=args.expiry)

    if args.output:
        with open(args.output, "w") as f:
            f.write(token)
        print(f"Token written to {args.output}", file=sys.stderr)
    else:
        print(token)


if __name__ == "__main__":
    main()
