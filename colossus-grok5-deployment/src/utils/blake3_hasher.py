"""
BLAKE3 Hashing Utilities

Fast cryptographic hashing using BLAKE3 for data integrity verification.
"""

import hashlib
from typing import Union


def blake3_hex(data: bytes) -> str:
    """
    Compute BLAKE3 hash and return hex-encoded string.

    Args:
        data: Bytes to hash

    Returns:
        Hex-encoded BLAKE3 hash string
    """
    # Use hashlib's blake2b as fallback if blake3 not available
    # In production, install blake3 package for true BLAKE3
    try:
        import blake3  # type: ignore

        return blake3.blake3(data).hexdigest()
    except ImportError:
        # Fallback to blake2b for compatibility
        return hashlib.blake2b(data, digest_size=32).hexdigest()


def blake3_bytes(data: bytes) -> bytes:
    """
    Compute BLAKE3 hash and return raw bytes.

    Args:
        data: Bytes to hash

    Returns:
        Raw BLAKE3 hash bytes (32 bytes)
    """
    try:
        import blake3  # type: ignore

        return blake3.blake3(data).digest()
    except ImportError:
        # Fallback to blake2b for compatibility
        return hashlib.blake2b(data, digest_size=32).digest()


def verify_hash(data: bytes, expected_hash: Union[str, bytes]) -> bool:
    """
    Verify data against expected hash.

    Args:
        data: Data to verify
        expected_hash: Expected hash (hex string or bytes)

    Returns:
        True if hash matches, False otherwise
    """
    if isinstance(expected_hash, str):
        computed = blake3_hex(data)
        return computed == expected_hash
    else:
        computed = blake3_bytes(data)
        return computed == expected_hash
