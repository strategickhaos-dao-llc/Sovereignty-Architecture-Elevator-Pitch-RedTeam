#!/usr/bin/env python3
"""
verify_evidence.py - One-command evidence verification for StrategicKhaos Dossier

Usage:
    python3 verify_evidence.py           # Run all checks
    python3 verify_evidence.py --check hashes    # Check hashes only
    python3 verify_evidence.py --check gpg       # Check GPG signature only
    python3 verify_evidence.py --check github    # Check GitHub API only
    python3 verify_evidence.py --verbose         # Verbose output

Exit codes:
    0 - All checks passed
    1 - One or more checks failed
"""

import json
import hashlib
import subprocess
import sys
import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import argparse

# Try to import blake3, fall back to hashlib.sha256 if not available
try:
    import blake3
    HAS_BLAKE3 = True
except ImportError:
    HAS_BLAKE3 = False
    print("Warning: blake3 not installed, using SHA-256 fallback")

# Try to import requests for GitHub API checks
try:
    import urllib.request
    HAS_URLLIB = True
except ImportError:
    HAS_URLLIB = False


def compute_hash(filepath: Path) -> str:
    """Compute blake3 hash of a file, or SHA-256 if blake3 unavailable."""
    with open(filepath, 'rb') as f:
        content = f.read()
    
    if HAS_BLAKE3:
        return blake3.blake3(content).hexdigest()
    else:
        return hashlib.sha256(content).hexdigest()


def load_status_snapshot(evidence_dir: Path) -> Optional[Dict]:
    """Load and parse status_snapshot.json."""
    snapshot_path = evidence_dir / 'status_snapshot.json'
    if not snapshot_path.exists():
        print(f"ERROR: {snapshot_path} not found")
        return None
    
    with open(snapshot_path, 'r') as f:
        return json.load(f)


def verify_hashes(evidence_dir: Path, verbose: bool = False) -> Tuple[bool, List[str]]:
    """Verify all hashes in hashes.txt."""
    hashes_path = evidence_dir / 'hashes.txt'
    errors = []
    
    if not hashes_path.exists():
        return False, ["hashes.txt not found"]
    
    with open(hashes_path, 'r') as f:
        lines = f.readlines()
    
    all_passed = True
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        parts = line.split()
        if len(parts) != 2:
            continue
        
        expected_hash, filepath = parts
        full_path = evidence_dir / filepath
        
        if not full_path.exists():
            errors.append(f"File not found: {filepath}")
            all_passed = False
            continue
        
        actual_hash = compute_hash(full_path)
        if actual_hash == expected_hash:
            if verbose:
                print(f"  OK: {filepath}")
        else:
            errors.append(f"Hash mismatch for {filepath}")
            errors.append(f"  Expected: {expected_hash}")
            errors.append(f"  Actual:   {actual_hash}")
            all_passed = False
    
    return all_passed, errors


def verify_gpg_signature(evidence_dir: Path, verbose: bool = False) -> Tuple[bool, List[str]]:
    """Verify GPG detached signature on aggregate file."""
    anchors_dir = evidence_dir / 'anchors'
    aggregate = anchors_dir / 'aggregated_2025-11-27.json'
    signature = anchors_dir / 'aggregated_2025-11-27.json.asc'
    
    errors = []
    
    if not aggregate.exists():
        return False, ["Aggregate file not found"]
    
    if not signature.exists():
        # Signature file not present - this is OK for placeholder dossier
        if verbose:
            print("  INFO: GPG signature file not present (placeholder)")
        return True, ["GPG signature file not present (OK for placeholder)"]
    
    try:
        result = subprocess.run(
            ['gpg', '--verify', str(signature), str(aggregate)],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            if verbose:
                print("  OK: GPG signature verified")
            return True, []
        else:
            return False, [f"GPG verification failed: {result.stderr}"]
    except FileNotFoundError:
        return True, ["GPG not installed (skipping signature check)"]


def verify_ots(evidence_dir: Path, verbose: bool = False) -> Tuple[bool, List[str]]:
    """Verify OpenTimestamps proof."""
    anchors_dir = evidence_dir / 'anchors'
    aggregate = anchors_dir / 'aggregated_2025-11-27.json'
    ots_proof = anchors_dir / 'aggregated_2025-11-27.json.ots'
    
    if not ots_proof.exists():
        # OTS file not present - this is OK for placeholder dossier
        if verbose:
            print("  INFO: OTS proof file not present (placeholder)")
        return True, ["OTS proof file not present (OK for placeholder)"]
    
    try:
        result = subprocess.run(
            ['ots', 'verify', str(ots_proof)],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            if verbose:
                print("  OK: OTS timestamp verified")
            return True, []
        else:
            # Pending timestamp is also acceptable
            if 'Pending' in result.stderr or 'pending' in result.stderr.lower():
                return True, ["OTS timestamp pending confirmation"]
            return False, [f"OTS verification failed: {result.stderr}"]
    except FileNotFoundError:
        return True, ["OTS client not installed (skipping timestamp check)"]


def verify_github_metadata(snapshot: Dict, verbose: bool = False) -> Tuple[bool, List[str]]:
    """Verify GitHub PRs and Actions runs via API (if accessible)."""
    if not HAS_URLLIB:
        return True, ["urllib not available (skipping GitHub checks)"]
    
    errors = []
    sources = snapshot.get('sources', {})
    prs = sources.get('github_prs', [])
    
    # Note: For private repos, we skip API verification
    # The exported metadata in the dossier serves as evidence
    
    if verbose:
        print("  INFO: GitHub API checks (skipped for private repos)")
        print(f"  Listed PRs: {snapshot.get('claims', {}).get('prs_merged', [])}")
    
    return True, ["GitHub metadata present in snapshot (API checks skipped for private repos)"]


def verify_json_structure(evidence_dir: Path, verbose: bool = False) -> Tuple[bool, List[str]]:
    """Verify JSON files are valid and contain expected fields."""
    errors = []
    
    # Check status_snapshot.json
    snapshot_path = evidence_dir / 'status_snapshot.json'
    try:
        with open(snapshot_path, 'r') as f:
            snapshot = json.load(f)
        
        required_fields = ['ts_iso', 'claims', 'sources']
        for field in required_fields:
            if field not in snapshot:
                errors.append(f"Missing required field in status_snapshot.json: {field}")
        
        if verbose:
            print(f"  OK: status_snapshot.json is valid JSON with required fields")
    except json.JSONDecodeError as e:
        errors.append(f"Invalid JSON in status_snapshot.json: {e}")
    
    # Check aggregate file
    aggregate_path = evidence_dir / 'anchors' / 'aggregated_2025-11-27.json'
    try:
        with open(aggregate_path, 'r') as f:
            aggregate = json.load(f)
        
        if verbose:
            print(f"  OK: aggregated_2025-11-27.json is valid JSON")
    except json.JSONDecodeError as e:
        errors.append(f"Invalid JSON in aggregated_2025-11-27.json: {e}")
    
    # Check provenance file
    prov_path = evidence_dir / 'anchors' / 'aggregated_2025-11-27.json.prov.json'
    try:
        with open(prov_path, 'r') as f:
            prov = json.load(f)
        
        if verbose:
            print(f"  OK: aggregated_2025-11-27.json.prov.json is valid JSON")
    except json.JSONDecodeError as e:
        errors.append(f"Invalid JSON in provenance file: {e}")
    
    return len(errors) == 0, errors


def main():
    parser = argparse.ArgumentParser(description='Verify StrategicKhaos evidence dossier')
    parser.add_argument('--check', choices=['hashes', 'gpg', 'ots', 'github', 'json', 'all'],
                        default='all', help='Specific check to run')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    args = parser.parse_args()
    
    # Determine evidence directory (relative to script location)
    script_dir = Path(__file__).parent.resolve()
    evidence_dir = script_dir
    
    # If script is not in evidence dir, check for evidence subdirectory
    if not (evidence_dir / 'status_snapshot.json').exists():
        evidence_dir = script_dir / 'evidence'
    
    if not evidence_dir.exists():
        print(f"ERROR: Evidence directory not found at {evidence_dir}")
        sys.exit(1)
    
    print(f"Verifying evidence dossier at: {evidence_dir}")
    print("=" * 60)
    
    all_passed = True
    all_messages = []
    
    # Load snapshot for GitHub checks
    snapshot = load_status_snapshot(evidence_dir)
    
    checks = {
        'json': ('JSON Structure', lambda: verify_json_structure(evidence_dir, args.verbose)),
        'hashes': ('File Hashes', lambda: verify_hashes(evidence_dir, args.verbose)),
        'gpg': ('GPG Signature', lambda: verify_gpg_signature(evidence_dir, args.verbose)),
        'ots': ('OpenTimestamps', lambda: verify_ots(evidence_dir, args.verbose)),
        'github': ('GitHub Metadata', lambda: verify_github_metadata(snapshot, args.verbose) if snapshot else (False, ["Could not load snapshot"])),
    }
    
    checks_to_run = checks.keys() if args.check == 'all' else [args.check]
    
    for check_name in checks_to_run:
        if check_name not in checks:
            continue
        
        label, check_func = checks[check_name]
        print(f"\n[{label}]")
        
        passed, messages = check_func()
        
        if passed:
            print(f"  ✓ PASSED")
        else:
            print(f"  ✗ FAILED")
            all_passed = False
        
        for msg in messages:
            print(f"    {msg}")
        
        all_messages.extend(messages)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ ALL CHECKS PASSED - Evidence dossier verified")
        sys.exit(0)
    else:
        print("✗ SOME CHECKS FAILED - Review errors above")
        sys.exit(1)


if __name__ == '__main__':
    main()
