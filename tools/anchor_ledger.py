#!/usr/bin/env python3
"""
anchor_ledger.py - Sign and timestamp ledger entries with GPG and OpenTimestamps

This script provides cryptographic anchoring for evidence ledger entries by:
1. Creating GPG detached signatures for authenticity proof
2. Creating OpenTimestamps proofs for existence proof on Bitcoin blockchain
3. Generating SHA256 hashes for integrity verification

Usage:
    python anchor_ledger.py [entry_file]
    
If no file is specified, uses the default ledger location.

Requirements:
    - GPG installed and configured
    - OpenTimestamps client: pip install opentimestamps-client
    - Valid GPG key configured for signing

Author: Strategickhaos
Version: 1.0.0
"""

import os
import sys
import subprocess
import hashlib
import yaml
import argparse
from pathlib import Path
from datetime import datetime

# Configuration - adjust these for your environment
DEFAULT_LEDGER = Path("evidence/conversation_ledger.yaml")
GPG_KEY = os.environ.get("GPG_SIGNING_KEY", "Dom <dom@yourdomain.com>")

def hash_file(path: Path) -> str:
    """
    Calculate SHA256 hash of a file.
    
    Args:
        path: Path to the file to hash
        
    Returns:
        Hex string of the SHA256 hash
    """
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

def check_prerequisites() -> tuple[bool, list[str]]:
    """
    Check if required tools are installed.
    
    Returns:
        Tuple of (all_ok: bool, errors: list[str])
    """
    errors = []
    
    # Check GPG
    try:
        result = subprocess.run(
            ["gpg", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✓ GPG found: {result.stdout.splitlines()[0]}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        errors.append("GPG not found. Install with: apt-get install gnupg (Linux) or brew install gnupg (Mac)")
    
    # Check OpenTimestamps
    try:
        result = subprocess.run(
            ["ots", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✓ OpenTimestamps found: {result.stdout.strip()}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        errors.append("OpenTimestamps not found. Install with: pip install opentimestamps-client")
    
    return len(errors) == 0, errors

def sign_with_gpg(entry_file: Path, gpg_key: str) -> Path:
    """
    Create a GPG detached signature for the file.
    
    Args:
        entry_file: Path to the file to sign
        gpg_key: GPG key identifier to use for signing
        
    Returns:
        Path to the signature file (.asc)
        
    Raises:
        subprocess.CalledProcessError: If GPG signing fails
    """
    sig_file = Path(str(entry_file) + ".asc")
    
    # Remove existing signature if present
    if sig_file.exists():
        sig_file.unlink()
    
    subprocess.run([
        "gpg",
        "--local-user", gpg_key,
        "--armor",
        "--detach-sign",
        "--output", str(sig_file),
        str(entry_file)
    ], check=True, capture_output=True)
    
    return sig_file

def timestamp_with_ots(entry_file: Path) -> Path:
    """
    Create an OpenTimestamps proof for the file.
    
    Args:
        entry_file: Path to the file to timestamp
        
    Returns:
        Path to the timestamp proof file (.ots)
        
    Raises:
        subprocess.CalledProcessError: If OTS stamping fails
    """
    ots_file = Path(str(entry_file) + ".ots")
    
    # Remove existing timestamp if present
    if ots_file.exists():
        ots_file.unlink()
    
    subprocess.run([
        "ots",
        "stamp",
        str(entry_file)
    ], check=True, capture_output=True)
    
    return ots_file

def verify_signature(entry_file: Path, sig_file: Path) -> bool:
    """
    Verify a GPG signature.
    
    Args:
        entry_file: Original file
        sig_file: Signature file
        
    Returns:
        True if signature is valid, False otherwise
    """
    try:
        result = subprocess.run([
            "gpg",
            "--verify",
            str(sig_file),
            str(entry_file)
        ], capture_output=True, text=True)
        return result.returncode == 0
    except subprocess.CalledProcessError:
        return False

def verify_timestamp(ots_file: Path) -> tuple[bool, str]:
    """
    Verify an OpenTimestamps proof.
    
    Args:
        ots_file: Path to the .ots proof file
        
    Returns:
        Tuple of (verified: bool, status: str)
    """
    try:
        result = subprocess.run([
            "ots",
            "verify",
            str(ots_file)
        ], capture_output=True, text=True)
        
        if "Success!" in result.stdout:
            return True, "verified"
        elif "pending" in result.stdout.lower():
            return False, "pending"
        else:
            return False, "failed"
    except subprocess.CalledProcessError as e:
        return False, f"error: {e}"

def upgrade_timestamps(directory: Path):
    """
    Upgrade all .ots files in a directory (aggregation with calendar servers).
    
    This should be run periodically (e.g., weekly) to aggregate pending
    timestamps with Bitcoin blockchain confirmations.
    
    Args:
        directory: Directory containing .ots files
    """
    ots_files = list(directory.glob("*.ots"))
    
    if not ots_files:
        print(f"No .ots files found in {directory}")
        return
    
    print(f"Upgrading {len(ots_files)} timestamp proofs...")
    
    for ots_file in ots_files:
        try:
            subprocess.run([
                "ots",
                "upgrade",
                str(ots_file)
            ], capture_output=True, check=True)
            print(f"  ✓ {ots_file.name}")
        except subprocess.CalledProcessError:
            print(f"  ✗ {ots_file.name} (not yet ready)")

def sign_and_stamp(entry_file: Path, gpg_key: str = GPG_KEY, verify: bool = True) -> dict:
    """
    Sign and timestamp a ledger entry.
    
    Args:
        entry_file: Path to the entry file
        gpg_key: GPG key to use for signing
        verify: Whether to verify the signature immediately
        
    Returns:
        Dictionary with anchoring information
    """
    if not entry_file.exists():
        raise FileNotFoundError(f"Entry file not found: {entry_file}")
    
    print(f"\n🔒 Anchoring ledger entry: {entry_file.name}")
    print("=" * 60)
    
    # Calculate hash
    file_hash = hash_file(entry_file)
    print(f"📋 SHA256: {file_hash}")
    
    # GPG signature
    print("\n1️⃣  Creating GPG signature...")
    try:
        sig_file = sign_with_gpg(entry_file, gpg_key)
        print(f"   ✅ Signature: {sig_file.name}")
        
        if verify:
            if verify_signature(entry_file, sig_file):
                print("   ✅ Signature verified")
            else:
                print("   ⚠️  Warning: Signature verification failed")
    except subprocess.CalledProcessError as e:
        print(f"   ❌ GPG signing failed: {e}")
        sig_file = None
    
    # OpenTimestamps
    print("\n2️⃣  Creating OpenTimestamps proof...")
    try:
        ots_file = timestamp_with_ots(entry_file)
        print(f"   ✅ Timestamp proof: {ots_file.name}")
        print(f"   ⏳ Status: pending (run 'ots verify {ots_file}' later)")
    except subprocess.CalledProcessError as e:
        print(f"   ❌ OTS stamping failed: {e}")
        ots_file = None
    
    print("\n" + "=" * 60)
    print("✅ Ledger entry anchored successfully!")
    print("\nTo verify later:")
    if sig_file:
        print(f"  GPG: gpg --verify {sig_file.name} {entry_file.name}")
    if ots_file:
        print(f"  OTS: ots verify {ots_file.name}")
    print("\nNote: OpenTimestamps proofs take time to aggregate to Bitcoin.")
    print("      Run 'ots upgrade *.ots' weekly to complete the process.")
    
    return {
        "file": str(entry_file),
        "sha256": file_hash,
        "signature_file": str(sig_file) if sig_file else None,
        "timestamp_file": str(ots_file) if ots_file else None,
        "anchored_at": datetime.utcnow().isoformat() + "Z"
    }

def main():
    parser = argparse.ArgumentParser(
        description="Sign and timestamp ledger entries with GPG and OpenTimestamps"
    )
    parser.add_argument(
        "entry_file",
        nargs="?",
        type=Path,
        default=DEFAULT_LEDGER,
        help="Path to the ledger entry file (default: evidence/conversation_ledger.yaml)"
    )
    parser.add_argument(
        "--gpg-key",
        default=GPG_KEY,
        help=f"GPG key to use for signing (default: {GPG_KEY})"
    )
    parser.add_argument(
        "--no-verify",
        action="store_true",
        help="Skip immediate signature verification"
    )
    parser.add_argument(
        "--upgrade",
        action="store_true",
        help="Upgrade all .ots files in the entry file's directory"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check prerequisites only"
    )
    
    args = parser.parse_args()
    
    # Check prerequisites
    print("Checking prerequisites...")
    all_ok, errors = check_prerequisites()
    
    if not all_ok:
        print("\n❌ Prerequisites check failed:")
        for error in errors:
            print(f"  • {error}")
        sys.exit(1)
    
    if args.check:
        print("\n✅ All prerequisites satisfied!")
        sys.exit(0)
    
    # Upgrade mode
    if args.upgrade:
        upgrade_timestamps(args.entry_file.parent if args.entry_file.is_file() else args.entry_file)
        sys.exit(0)
    
    # Sign and stamp
    try:
        result = sign_and_stamp(
            args.entry_file,
            gpg_key=args.gpg_key,
            verify=not args.no_verify
        )
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
