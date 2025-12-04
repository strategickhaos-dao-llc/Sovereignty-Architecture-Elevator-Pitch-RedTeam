#!/usr/bin/env python3
"""
BLAKE3 Hash Computation for Legal Shield Bundle

This script computes the BLAKE3 hash of the deterministic tar bundle.
It supports the blake3 library (preferred) and falls back to hashlib.sha256
if blake3 is not available.

Usage:
  1. Create the deterministic tar bundle first:
     tar --sort=name --mtime='2025-11-27 00:00:00' --owner=0 --group=0 \
         --numeric-owner -cf bundle.tar LEGAL_SHIELD.yaml README.md governance_appendix.yaml
  
  2. Run this script:
     python compute_hash.py
     
  3. Copy the resulting hash to LEGAL_SHIELD.yaml and use for on-chain commit.

Requirements:
  - Python 3.8+ (uses walrus operator)
  - pip install blake3  (optional but recommended)
  - Fallback: uses hashlib.sha256 if blake3 not installed
"""

import os
import sys

# Require Python 3.8+ for walrus operator
if sys.version_info < (3, 8):
    print("Error: Python 3.8 or higher is required.")
    sys.exit(1)

BUNDLE_FILE = 'bundle.tar'
CHUNK_SIZE = 4096


def compute_blake3_hash(filepath):
    """Compute BLAKE3 hash using the blake3 library."""
    try:
        import blake3
        
        with open(filepath, 'rb') as f:
            hasher = blake3.blake3()
            while chunk := f.read(CHUNK_SIZE):
                hasher.update(chunk)
        return hasher.hexdigest(), 'blake3'
    except ImportError:
        return None, None


def compute_sha256_hash(filepath):
    """Compute SHA256 hash using hashlib (fallback)."""
    import hashlib
    
    with open(filepath, 'rb') as f:
        hasher = hashlib.sha256()
        while chunk := f.read(CHUNK_SIZE):
            hasher.update(chunk)
    return hasher.hexdigest(), 'sha256'


def main():
    # Check if bundle.tar exists
    if not os.path.exists(BUNDLE_FILE):
        print(f"Error: {BUNDLE_FILE} not found.")
        print("Create the bundle first with:")
        print("  tar --sort=name --mtime='2025-11-27 00:00:00' --owner=0 --group=0 \\")
        print("      --numeric-owner -cf bundle.tar LEGAL_SHIELD.yaml README.md governance_appendix.yaml")
        sys.exit(1)
    
    # Try BLAKE3 first, fall back to SHA256
    hash_value, algorithm = compute_blake3_hash(BUNDLE_FILE)
    
    if hash_value is None:
        print("Warning: blake3 library not installed. Using SHA256 as fallback.")
        print("For production, install blake3: pip install blake3")
        hash_value, algorithm = compute_sha256_hash(BUNDLE_FILE)
    
    print(f"\n{'='*60}")
    print(f"  Bundle: {BUNDLE_FILE}")
    print(f"  Algorithm: {algorithm.upper()}")
    print(f"  Hash: {hash_value}")
    print(f"{'='*60}")
    print(f"\nFor on-chain commit, use as bytes32:")
    print(f"  0x{hash_value}")
    print(f"\nUpdate LEGAL_SHIELD.yaml with this hash value.")


if __name__ == '__main__':
    main()
