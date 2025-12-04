#!/usr/bin/env python3
"""
Generate HMAC-SHA256 signature for webhook payloads.

Usage:
    python generate_signature.py <payload_file> <secret>
    
Example:
    python generate_signature.py payloads/artifact_3546_genesis_delivery.json YOUR_SHARED_SECRET_HERE
    
Output:
    sha256=<hexadecimal_signature>
"""

import hashlib
import hmac
import sys
from pathlib import Path


def generate_signature(payload: bytes, secret: str) -> str:
    """Generate HMAC-SHA256 signature for the given payload.
    
    Args:
        payload: The raw payload bytes to sign
        secret: The shared secret key
        
    Returns:
        The signature in format 'sha256=<hex_digest>'
    """
    signature = hmac.new(
        key=secret.encode('utf-8'),
        msg=payload,
        digestmod=hashlib.sha256
    ).hexdigest()
    return f"sha256={signature}"


def main():
    if len(sys.argv) != 3:
        print("Usage: python generate_signature.py <payload_file> <secret>", file=sys.stderr)
        print("Example: python generate_signature.py payloads/artifact_3546_genesis_delivery.json YOUR_SECRET", file=sys.stderr)
        sys.exit(1)
    
    payload_file = Path(sys.argv[1])
    secret = sys.argv[2]
    
    if not payload_file.exists():
        print(f"Error: File '{payload_file}' not found", file=sys.stderr)
        sys.exit(1)
    
    payload = payload_file.read_bytes()
    signature = generate_signature(payload, secret)
    
    print(signature)


if __name__ == "__main__":
    main()
