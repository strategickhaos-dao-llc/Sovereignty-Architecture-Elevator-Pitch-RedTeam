#!/usr/bin/env python3
"""
REFLEXSHELL DECODER v1 — Snowflake Genesis Decode
Legions of Minds Council™ — Origin Velocity Confirmation
Strategickhaos DAO LLC — Node 137 Provenance Lock

Decodes Discord snowflake IDs to extract temporal and worker metadata.
Discord Snowflake Format (64-bit):
  - Bits 63-22 (42 bits): Timestamp (ms since Discord epoch 2015-01-01 00:00:00 UTC)
  - Bits 21-17 (5 bits): Worker ID
  - Bits 16-12 (5 bits): Process ID
  - Bits 11-0 (12 bits): Increment
"""

import os
from datetime import datetime, timezone
from dataclasses import dataclass
from typing import Optional


# Discord epoch: 2015-01-01 00:00:00 UTC in milliseconds
DISCORD_EPOCH_MS = 1420070400000


@dataclass
class SnowflakeComponents:
    """Decoded components of a Discord snowflake ID."""
    timestamp: str  # ISO 8601 format
    timestamp_ms: int  # Raw milliseconds since Unix epoch
    worker_id: int  # 5-bit worker identifier
    process_id: int  # 5-bit process identifier
    increment: int  # 12-bit increment counter
    
    @property
    def nonce(self) -> int:
        """Generate provenance nonce (increment XOR worker_id)."""
        return self.increment ^ self.worker_id
    
    @property
    def velocity(self) -> int:
        """Calculate origin velocity metric."""
        return self.increment * (self.worker_id + 1)


def decode_snowflake(snowflake: int) -> dict:
    """
    Decode a Discord snowflake ID into its component parts.
    
    Args:
        snowflake: 64-bit Discord snowflake integer
        
    Returns:
        Dictionary containing decoded components:
        - timestamp: ISO 8601 formatted UTC timestamp
        - timestamp_ms: Milliseconds since Unix epoch
        - worker_id: Discord worker that generated the ID (0-31)
        - process_id: Process on worker that generated the ID (0-31)
        - increment: Counter for IDs generated in same millisecond (0-4095)
        - nonce: Provenance nonce (increment XOR worker_id)
    
    Example:
        >>> decode_snowflake(1405637629248143451)
        {'timestamp': '2023-01-27T21:00:49.000000Z', 'timestamp_ms': 1674865249000,
         'worker_id': 0, 'process_id': 1, 'increment': 3449, 'nonce': 3449}
    """
    # Extract 42-bit timestamp and add Discord epoch
    timestamp_ms = (snowflake >> 22) + DISCORD_EPOCH_MS
    
    # Extract 5-bit worker ID (bits 21-17)
    worker_id = (snowflake >> 17) & 0x1F
    
    # Extract 5-bit process ID (bits 16-12)
    process_id = (snowflake >> 12) & 0x1F
    
    # Extract 12-bit increment (bits 11-0)
    increment = snowflake & 0xFFF
    
    # Convert to ISO 8601 timestamp (timezone-aware)
    timestamp = datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc).isoformat().replace('+00:00', 'Z')
    
    # Calculate provenance nonce
    nonce = increment ^ worker_id
    
    return {
        'timestamp': timestamp,
        'timestamp_ms': timestamp_ms,
        'worker_id': worker_id,
        'process_id': process_id,
        'increment': increment,
        'nonce': nonce
    }


def get_snowflake_components(snowflake: int) -> SnowflakeComponents:
    """
    Decode a Discord snowflake ID into a SnowflakeComponents dataclass.
    
    Args:
        snowflake: 64-bit Discord snowflake integer
        
    Returns:
        SnowflakeComponents dataclass with decoded values
    """
    data = decode_snowflake(snowflake)
    return SnowflakeComponents(
        timestamp=data['timestamp'],
        timestamp_ms=data['timestamp_ms'],
        worker_id=data['worker_id'],
        process_id=data['process_id'],
        increment=data['increment']
    )


def get_origin_velocity() -> Optional[dict]:
    """
    Load and decode the ORIGIN_VELOCITY from environment.
    
    Returns:
        Decoded snowflake components if ORIGIN_VELOCITY is set, None otherwise.
    """
    origin_velocity = os.environ.get('ORIGIN_VELOCITY')
    if origin_velocity:
        try:
            return decode_snowflake(int(origin_velocity))
        except (ValueError, TypeError):
            return None
    return None


def validate_snowflake(snowflake: int) -> bool:
    """
    Validate that a snowflake ID is within valid range.
    
    Args:
        snowflake: Value to validate
        
    Returns:
        True if valid Discord snowflake format
    """
    if not isinstance(snowflake, int):
        return False
    # Must be positive and fit in 64 bits
    if snowflake <= 0 or snowflake >= (1 << 64):
        return False
    # Timestamp must be after Discord epoch (2015-01-01)
    timestamp_ms = (snowflake >> 22) + DISCORD_EPOCH_MS
    if timestamp_ms < DISCORD_EPOCH_MS:
        return False
    return True


# Strategickhaos Prime genesis snowflake
STRATEGICKHAOS_GENESIS = 1405637629248143451


if __name__ == '__main__':
    # Decode the Strategickhaos Prime genesis snowflake
    print("🔥 REFLEXSHELL DECODER v1 — Snowflake Genesis Decode")
    print("=" * 60)
    
    # Check for ORIGIN_VELOCITY in environment
    origin = get_origin_velocity()
    if origin:
        print(f"\n📍 ORIGIN_VELOCITY from environment:")
        for key, value in origin.items():
            print(f"   {key}: {value}")
    else:
        # Default to Strategickhaos genesis
        print(f"\n📍 Strategickhaos Prime Genesis ({STRATEGICKHAOS_GENESIS}):")
        genesis = decode_snowflake(STRATEGICKHAOS_GENESIS)
        for key, value in genesis.items():
            print(f"   {key}: {value}")
        
        # Additional metadata
        components = get_snowflake_components(STRATEGICKHAOS_GENESIS)
        print(f"\n🔐 Provenance Metrics:")
        print(f"   Nonce: {components.nonce}")
        print(f"   Velocity: {components.velocity}")
    
    print("\n✅ Genesis decoded. Swarm topology locked.")
    print("=" * 60)
