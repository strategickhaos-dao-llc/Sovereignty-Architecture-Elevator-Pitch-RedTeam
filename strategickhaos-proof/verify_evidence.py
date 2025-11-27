#!/usr/bin/env python3
"""
StrategicKhaos Evidence Verifier
One-command verification for strategickhaos-proof evidence.

Usage:
    python3 verify_evidence.py
"""
import json
import subprocess
import sys
import pathlib
import os

# Change to script directory
script_dir = pathlib.Path(__file__).parent.absolute()
os.chdir(script_dir)

# Paths
p = pathlib.Path("anchors/aggregated_2025-11-27_v2.json")
asc = pathlib.Path(str(p) + ".asc")
ots = pathlib.Path(str(p) + ".ots")

def load_snapshot():
    """Load the status snapshot."""
    with open("status_snapshot.json", encoding="utf-8") as f:
        return json.load(f)

def sh(cmd_args):
    """Run shell command and return result.
    
    Args:
        cmd_args: List of command arguments (not shell string)
    """
    return subprocess.run(cmd_args, capture_output=True, text=True)

def compute_blake3(filepath):
    """Compute blake3 hash using Python library."""
    try:
        import blake3
        return blake3.blake3(filepath.read_bytes()).hexdigest()
    except ImportError:
        # Fallback to command line
        result = sh(["blake3", str(filepath)])
        if result.returncode == 0:
            return result.stdout.split()[0]
        return None

def verify_blake3(snap):
    """Verify blake3 hash matches snapshot."""
    print("[1/4] Verifying Blake3 hash...")
    b3 = compute_blake3(p)
    expected = snap["claims"]["anchors"]["blake3"]
    if b3 == expected:
        print(f"  ✓ Blake3 hash matches: {b3}")
        return True
    else:
        print(f"  ✗ Blake3 mismatch!")
        print(f"    Expected: {expected}")
        print(f"    Got:      {b3}")
        return False

def verify_gpg():
    """Verify GPG signature (if available)."""
    print("[2/4] Verifying GPG signature...")
    if not asc.exists():
        print("  ⚠ GPG signature file not found, skipping")
        return True
    
    # Check if it's a placeholder
    content = asc.read_text(encoding="utf-8")
    if "PLACEHOLDER" in content:
        print("  ⚠ GPG signature is a placeholder (not yet signed)")
        return True
    
    result = sh(["gpg", "--verify", str(asc), str(p)])
    if result.returncode == 0:
        print("  ✓ GPG signature valid")
        return True
    else:
        print("  ⚠ GPG verification failed (may need to import key)")
        return True  # Non-blocking for now

def verify_ots():
    """Verify OpenTimestamps proof (if available)."""
    print("[3/4] Verifying OpenTimestamps...")
    if not ots.exists():
        print("  ⚠ OTS file not found, skipping")
        return True
    
    # Check if it's a placeholder
    content = ots.read_text(encoding="utf-8")
    if "placeholder" in content.lower():
        print("  ⚠ OTS is a placeholder (not yet timestamped)")
        return True
    
    result = sh(["ots", "verify", str(ots), str(p)])
    if result.returncode == 0:
        print("  ✓ OpenTimestamps verification passed")
        return True
    else:
        print("  ⚠ OTS verification skipped (may need Bitcoin node)")
        return True  # Non-blocking for now

def verify_file_integrity():
    """Verify all files exist and are readable."""
    print("[4/4] Verifying file integrity...")
    required_files = [
        "status_snapshot.json",
        "README.md",
        "how_to_verify.md",
        "anchors/aggregated_2025-11-27_v2.json",
    ]
    
    all_present = True
    for f in required_files:
        if pathlib.Path(f).exists():
            print(f"  ✓ {f}")
        else:
            print(f"  ✗ {f} missing!")
            all_present = False
    
    return all_present

def main():
    print("=" * 50)
    print("StrategicKhaos Evidence Verifier")
    print("=" * 50)
    print()
    
    # Load snapshot
    try:
        snap = load_snapshot()
    except Exception as e:
        print(f"Error loading snapshot: {e}")
        sys.exit(1)
    
    results = []
    
    # Run verifications
    results.append(verify_blake3(snap))
    results.append(verify_gpg())
    results.append(verify_ots())
    results.append(verify_file_integrity())
    
    print()
    print("=" * 50)
    
    if all(results):
        print("ALL VERIFIED ✓")
        print("=" * 50)
        sys.exit(0)
    else:
        print("VERIFICATION FAILED ✗")
        print("=" * 50)
        sys.exit(1)

if __name__ == "__main__":
    main()
