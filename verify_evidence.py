#!/usr/bin/env python3
"""
StrategicKhaos Evidence Verifier

Verifies the integrity of evidence files by comparing actual hashes
against the manifest in evidence/hashes.txt.

Usage:
    python3 verify_evidence.py              # Verify all hashes
    python3 verify_evidence.py --generate   # Generate new hashes.txt
    python3 verify_evidence.py --check FILE # Check single file
"""

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path


def get_repo_root() -> Path:
    """Find the repository root by looking for .git directory."""
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    # Fallback to script directory's parent
    return Path(__file__).resolve().parent


def compute_sha256(filepath: Path) -> str:
    """Compute SHA256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def parse_hashes_file(hashes_path: Path) -> dict:
    """Parse hashes.txt into a dict of {filepath: expected_hash}."""
    hashes = {}
    if not hashes_path.exists():
        return hashes
    
    with open(hashes_path, "r") as f:
        for line in f:
            line = line.strip()
            # Skip empty lines and comments
            if not line or line.startswith("#"):
                continue
            # Parse "hash  filepath" format
            parts = line.split(maxsplit=1)
            if len(parts) == 2:
                expected_hash, filepath = parts
                hashes[filepath.strip()] = expected_hash.strip()
    return hashes


def verify_hashes(repo_root: Path, verbose: bool = True) -> tuple:
    """
    Verify all files in hashes.txt against actual computed hashes.
    Returns (passed, failed, missing) as lists of filenames.
    """
    hashes_path = repo_root / "evidence" / "hashes.txt"
    expected_hashes = parse_hashes_file(hashes_path)
    
    passed = []
    failed = []
    missing = []
    
    for filepath, expected_hash in expected_hashes.items():
        full_path = repo_root / filepath
        
        if not full_path.exists():
            missing.append(filepath)
            if verbose:
                print(f"❌ {filepath}: FILE NOT FOUND")
            continue
        
        actual_hash = compute_sha256(full_path)
        
        if actual_hash == expected_hash:
            passed.append(filepath)
            if verbose:
                print(f"✅ {filepath}: VERIFIED")
        else:
            failed.append(filepath)
            if verbose:
                print(f"❌ {filepath}: HASH MISMATCH")
                print(f"   Expected: {expected_hash}")
                print(f"   Actual:   {actual_hash}")
    
    return passed, failed, missing


def generate_hashes(repo_root: Path, files: list = None) -> dict:
    """Generate hashes for specified files (or default set)."""
    if files is None:
        # Default files to hash
        files = [
            "evidence/status_snapshot.json",
            "dao_record.yaml",
            "governance/access_matrix.yaml",
        ]
    
    hashes = {}
    for filepath in files:
        full_path = repo_root / filepath
        if full_path.exists():
            hashes[filepath] = compute_sha256(full_path)
    
    return hashes


def write_hashes_file(repo_root: Path, hashes: dict):
    """Write hashes to evidence/hashes.txt."""
    hashes_path = repo_root / "evidence" / "hashes.txt"
    
    with open(hashes_path, "w") as f:
        f.write("# StrategicKhaos Evidence Hash Manifest\n")
        f.write("# Algorithm: SHA256\n")
        f.write(f"# Generated: {get_timestamp()}\n")
        f.write("# Re-verified on every CI push via .github/workflows/verify.yaml\n")
        f.write("\n")
        
        for filepath, file_hash in sorted(hashes.items()):
            f.write(f"{file_hash}  {filepath}\n")
    
    print(f"✅ Wrote {len(hashes)} hashes to {hashes_path}")


def get_timestamp() -> str:
    """Get current UTC timestamp in ISO format."""
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def validate_json(repo_root: Path) -> bool:
    """Validate that status_snapshot.json is valid JSON."""
    json_path = repo_root / "evidence" / "status_snapshot.json"
    if not json_path.exists():
        print("⚠️  status_snapshot.json not found")
        return False
    
    try:
        with open(json_path, "r") as f:
            data = json.load(f)
        
        # Check for required top-level keys
        required_keys = ["schema_version", "generated_at", "organization", "infrastructure"]
        missing_keys = [k for k in required_keys if k not in data]
        
        if missing_keys:
            print(f"⚠️  status_snapshot.json missing keys: {missing_keys}")
            return False
        
        print("✅ status_snapshot.json: Valid JSON with required schema")
        return True
    except json.JSONDecodeError as e:
        print(f"❌ status_snapshot.json: Invalid JSON - {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="StrategicKhaos Evidence Verifier"
    )
    parser.add_argument(
        "--generate", "-g",
        action="store_true",
        help="Generate new hashes.txt from current files"
    )
    parser.add_argument(
        "--check", "-c",
        type=str,
        help="Check hash of a single file"
    )
    parser.add_argument(
        "--validate-json", "-j",
        action="store_true",
        help="Validate status_snapshot.json schema"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Minimal output (exit code only)"
    )
    
    args = parser.parse_args()
    repo_root = get_repo_root()
    
    print(f"📂 Repository root: {repo_root}")
    print("━" * 50)
    
    if args.generate:
        hashes = generate_hashes(repo_root)
        write_hashes_file(repo_root, hashes)
        return 0
    
    if args.check:
        filepath = args.check
        full_path = repo_root / filepath
        if not full_path.exists():
            print(f"❌ File not found: {filepath}")
            return 1
        file_hash = compute_sha256(full_path)
        print(f"{file_hash}  {filepath}")
        return 0
    
    if args.validate_json:
        valid = validate_json(repo_root)
        return 0 if valid else 1
    
    # Default: verify all hashes
    passed, failed, missing = verify_hashes(repo_root, verbose=not args.quiet)
    
    print("━" * 50)
    
    # Also validate JSON schema
    validate_json(repo_root)
    
    print("━" * 50)
    
    total = len(passed) + len(failed) + len(missing)
    if total == 0:
        print("⚠️  No files to verify (hashes.txt may be empty)")
        return 1
    
    if failed or missing:
        print(f"❌ Verification FAILED: {len(passed)} passed, {len(failed)} failed, {len(missing)} missing")
        return 1
    else:
        print(f"✅ All {len(passed)} files verified successfully")
        return 0


if __name__ == "__main__":
    sys.exit(main())
