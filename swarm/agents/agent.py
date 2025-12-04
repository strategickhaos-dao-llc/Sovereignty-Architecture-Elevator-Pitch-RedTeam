#!/usr/bin/env python3
"""
agent.py — SwarmGate v2.0 Agent
JWT-based authentication with NATS-backed revocation checking
Evolution #3: Revocable tokens + AI governance integration

Strategickhaos DAO LLC / Valoryield Engine
Author: Domenic Garza (Node 137)
"""

import asyncio
import json
import hashlib
import hmac
import base64
import time
import os
import logging
from datetime import datetime
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger('swarmgate')

# Configuration
SWARM_SECRET = os.environ.get('SWARM_SECRET', 'sovereign-swarm-default-key')
NATS_URL = os.environ.get('NATS_URL', 'nats://swarm:swarm@10.44.0.1:4222')
REVOCATION_SUBJECT = 'audit.revoke.check'
TOKEN_TTL_SECONDS = 86400  # 24 hours default


class TokenValidationError(Exception):
    """Raised when token validation fails."""
    pass


class TokenRevokedError(Exception):
    """Raised when token has been revoked."""
    pass


def base64url_decode(data: str) -> bytes:
    """Decode base64url data with padding correction."""
    padding = 4 - (len(data) % 4)
    if padding != 4:
        data += '=' * padding
    return base64.urlsafe_b64decode(data)


def base64url_encode(data: bytes) -> str:
    """Encode data as base64url without padding."""
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')


def verify_jwt_signature(token: str, secret: str) -> dict:
    """Verify JWT signature and return payload."""
    parts = token.split('.')
    if len(parts) != 3:
        raise TokenValidationError("Invalid token format")
    
    header_b64, payload_b64, signature_b64 = parts
    
    # Verify signature
    message = f"{header_b64}.{payload_b64}"
    expected_signature = hmac.new(
        secret.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).digest()
    expected_signature_b64 = base64url_encode(expected_signature)
    
    if not hmac.compare_digest(signature_b64, expected_signature_b64):
        raise TokenValidationError("Invalid signature")
    
    # Decode payload
    payload_json = base64url_decode(payload_b64).decode('utf-8')
    return json.loads(payload_json)


def validate_token_claims(claims: dict) -> None:
    """Validate token claims (exp, nbf, iat)."""
    now = int(time.time())
    
    # Check expiration
    if 'exp' in claims and claims['exp'] < now:
        raise TokenValidationError(f"Token expired at {claims['exp']}")
    
    # Check not-before
    if 'nbf' in claims and claims['nbf'] > now:
        raise TokenValidationError(f"Token not valid until {claims['nbf']}")
    
    # Check issued-at (with 5 minute clock skew tolerance)
    if 'iat' in claims and claims['iat'] > now + 300:
        raise TokenValidationError("Token issued in the future")
    
    # Check issuer
    if claims.get('iss') != 'sovereign-swarm':
        raise TokenValidationError("Invalid issuer")


async def check_revoked_nats(jti: str) -> bool:
    """
    Check if token is revoked via NATS request.
    Evolution #3: Dynamic revocation via NATS CRL-like system
    """
    try:
        # Try to import nats-py
        import nats
        from nats.errors import TimeoutError as NatsTimeoutError
        
        nc = await nats.connect(NATS_URL)
        try:
            msg = await nc.request(
                REVOCATION_SUBJECT,
                jti.encode('utf-8'),
                timeout=2.0
            )
            result = msg.data.decode('utf-8')
            return result == "OK"
        except NatsTimeoutError:
            logger.warning(f"Revocation check timed out for jti={jti}")
            # Fail open on timeout (configurable policy)
            return True
        finally:
            await nc.close()
    except ImportError:
        logger.warning("nats-py not installed, skipping revocation check")
        return True
    except Exception as e:
        logger.error(f"Revocation check failed: {e}")
        # Fail open on error (configurable policy)
        return True


async def validate_swarmgate_token(token: str) -> dict:
    """
    Full SwarmGate token validation with revocation check.
    
    Returns validated claims on success.
    Raises TokenValidationError or TokenRevokedError on failure.
    """
    # Step 1: Verify signature
    claims = verify_jwt_signature(token, SWARM_SECRET)
    logger.debug(f"Token signature valid for sub={claims.get('sub')}")
    
    # Step 2: Validate claims
    validate_token_claims(claims)
    logger.debug(f"Token claims valid for sub={claims.get('sub')}")
    
    # Step 3: Check revocation (Evolution #3)
    jti = claims.get('jti')
    if jti:
        is_valid = await check_revoked_nats(jti)
        if not is_valid:
            raise TokenRevokedError(f"Token {jti} has been revoked")
        logger.debug(f"Token not revoked: jti={jti}")
    
    return claims


class SwarmGateAgent:
    """
    SwarmGate Agent for mesh authentication.
    Handles peer authentication and capability enforcement.
    """
    
    def __init__(self):
        self.validated_peers: dict = {}
        self.revoked_tokens: set = set()
    
    async def authenticate_peer(self, peer_id: str, token: str) -> dict:
        """Authenticate a peer with their SwarmGate token."""
        try:
            claims = await validate_swarmgate_token(token)
            
            # Store validated peer
            self.validated_peers[peer_id] = {
                'claims': claims,
                'authenticated_at': datetime.utcnow().isoformat(),
                'capabilities': claims.get('capabilities', []),
            }
            
            logger.info(f"Peer authenticated: {peer_id} with caps={claims.get('capabilities')}")
            return claims
            
        except TokenValidationError as e:
            logger.warning(f"Authentication failed for {peer_id}: {e}")
            raise
        except TokenRevokedError as e:
            logger.warning(f"Revoked token used by {peer_id}: {e}")
            raise
    
    async def revoke_token(self, jti: str) -> None:
        """
        Revoke a token by publishing to NATS.
        Other agents will check this on handshake.
        """
        try:
            import nats
            nc = await nats.connect(NATS_URL)
            try:
                await nc.publish(
                    'audit.revoke.add',
                    json.dumps({'jti': jti, 'revoked_at': time.time()}).encode()
                )
                self.revoked_tokens.add(jti)
                logger.info(f"Token revoked: jti={jti}")
            finally:
                await nc.close()
        except Exception as e:
            logger.error(f"Failed to publish revocation: {e}")
            raise
    
    def check_capability(self, peer_id: str, capability: str) -> bool:
        """Check if a peer has a specific capability."""
        peer_info = self.validated_peers.get(peer_id)
        if not peer_info:
            return False
        return capability in peer_info.get('capabilities', [])
    
    async def subscribe_revocations(self) -> None:
        """Subscribe to token revocation events."""
        try:
            import nats
            
            nc = await nats.connect(NATS_URL)
            
            async def revocation_handler(msg):
                data = json.loads(msg.data.decode())
                jti = data.get('jti')
                if jti:
                    self.revoked_tokens.add(jti)
                    logger.info(f"Received revocation for jti={jti}")
                    
                    # Remove from validated peers
                    for peer_id, info in list(self.validated_peers.items()):
                        if info['claims'].get('jti') == jti:
                            del self.validated_peers[peer_id]
                            logger.info(f"Evicted peer {peer_id} due to revocation")
            
            await nc.subscribe('audit.revoke.add', cb=revocation_handler)
            logger.info("Subscribed to revocation events")
            
        except ImportError:
            logger.warning("nats-py not installed, revocation subscription disabled")
        except Exception as e:
            logger.error(f"Failed to subscribe to revocations: {e}")


class NATSRevocationService:
    """
    NATS-based token revocation service.
    Maintains CRL (Certificate Revocation List) for SwarmGate tokens.
    """
    
    def __init__(self):
        self.revoked_tokens: dict = {}  # jti -> revocation_info
    
    async def start(self) -> None:
        """Start the revocation service."""
        try:
            import nats
            
            nc = await nats.connect(NATS_URL)
            
            async def check_handler(msg):
                jti = msg.data.decode('utf-8')
                if jti in self.revoked_tokens:
                    await msg.respond(b"REVOKED")
                else:
                    await msg.respond(b"OK")
            
            async def add_handler(msg):
                data = json.loads(msg.data.decode())
                jti = data.get('jti')
                if jti:
                    self.revoked_tokens[jti] = {
                        'revoked_at': data.get('revoked_at', time.time()),
                        'reason': data.get('reason', 'manual'),
                    }
                    logger.info(f"Token added to CRL: jti={jti}")
            
            # Subscribe to check requests
            await nc.subscribe(REVOCATION_SUBJECT, cb=check_handler)
            
            # Subscribe to add revocations
            await nc.subscribe('audit.revoke.add', cb=add_handler)
            
            logger.info("Revocation service started")
            
            # Keep running
            while True:
                await asyncio.sleep(60)
                # Cleanup expired revocations (older than 30 days)
                cutoff = time.time() - (30 * 86400)
                self.revoked_tokens = {
                    jti: info for jti, info in self.revoked_tokens.items()
                    if info.get('revoked_at', 0) > cutoff
                }
                
        except ImportError:
            logger.error("nats-py required for revocation service")
        except Exception as e:
            logger.error(f"Revocation service error: {e}")


async def main():
    """Main entry point for testing."""
    import argparse
    parser = argparse.ArgumentParser(description='SwarmGate Agent')
    parser.add_argument('--mode', choices=['agent', 'service'], default='agent',
                       help='Run mode: agent (peer auth) or service (revocation CRL)')
    parser.add_argument('--test-token', help='Test token validation')
    args = parser.parse_args()
    
    if args.test_token:
        try:
            claims = await validate_swarmgate_token(args.test_token)
            print(f"Token valid: {json.dumps(claims, indent=2)}")
        except Exception as e:
            print(f"Token invalid: {e}")
        return
    
    if args.mode == 'service':
        service = NATSRevocationService()
        await service.start()
    else:
        agent = SwarmGateAgent()
        await agent.subscribe_revocations()
        # Keep running
        while True:
            await asyncio.sleep(60)


if __name__ == '__main__':
    asyncio.run(main())
