#!/usr/bin/env python3
"""
Generate HMAC-SHA256 signature for webhook payloads.

Usage:
    python generate_signature.py <payload_file> <secret>

Outputs a curl command to /tmp/curl_cmd.sh that includes the signature.
"""

import hashlib
import hmac
import sys
import os


def generate_signature(payload: bytes, secret: str) -> str:
    """Generate HMAC-SHA256 signature for the payload."""
    signature = hmac.new(
        secret.encode('utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest()
    return f"sha256={signature}"


def main():
    if len(sys.argv) < 3:
        print("Usage: python generate_signature.py <payload_file> <secret>", file=sys.stderr)
        sys.exit(1)

    payload_file = sys.argv[1]
    secret = sys.argv[2]

    if not os.path.exists(payload_file):
        print(f"Error: Payload file '{payload_file}' not found", file=sys.stderr)
        sys.exit(1)

    with open(payload_file, 'rb') as f:
        payload = f.read()

    signature = generate_signature(payload, secret)

    # Generate curl command
    curl_cmd = f'''#!/bin/bash
# Generated curl command with HMAC-SHA256 signature
# Payload: {payload_file}

WEBHOOK_URL="${{1:-http://localhost:8000/webhook}}"

curl -X POST "$WEBHOOK_URL" \\
  -H "Content-Type: application/json" \\
  -H "X-Hub-Signature-256: {signature}" \\
  --data-binary @{payload_file} \\
  -w "\\nHTTP Status: %{{http_code}}\\n" \\
  --fail

exit $?
'''

    print(curl_cmd)


if __name__ == "__main__":
    main()
