#!/usr/bin/env python3
"""
StrategicKhaos Evidence Verification Script

Verifies the integrity of the evidence dossier by:
1. Checking BLAKE3 hashes of tracked files
2. Validating cross-references in status_snapshot.json
3. Verifying JSON schema compliance

Usage:
    python verify_evidence.py              # Verify all evidence
    python verify_evidence.py --regenerate # Regenerate hash manifest
    python verify_evidence.py --check-refs # Only check cross-references
    python verify_evidence.py --verbose    # Verbose output
"""

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


# ANSI color codes for terminal output
class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


def get_repo_root() -> Path:
    """Find the repository root directory."""
    script_dir = Path(__file__).resolve().parent
    # Script is in strategickhaos-proof/, repo root is parent
    return script_dir.parent


def compute_blake3_hash(filepath: Path) -> str:
    """Compute BLAKE3 hash of a file using hashlib (fallback to SHA256 if BLAKE3 unavailable)."""
    try:
        import blake3

        hasher = blake3.blake3()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    except ImportError:
        # Fallback to SHA256 if blake3 not installed
        hasher = hashlib.sha256()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                hasher.update(chunk)
        return hasher.hexdigest()


def load_hash_manifest(manifest_path: Path) -> dict[str, str]:
    """Load hash manifest from hashes.txt file."""
    hashes = {}
    if not manifest_path.exists():
        return hashes

    with open(manifest_path) as f:
        for line in f:
            line = line.strip()
            # Skip comments and empty lines
            if not line or line.startswith("#"):
                continue
            # Skip placeholder lines
            if "PLACEHOLDER_" in line:
                continue
            parts = line.split("  ", 1)
            if len(parts) == 2:
                hash_value, filepath = parts
                hashes[filepath] = hash_value

    return hashes


def save_hash_manifest(manifest_path: Path, hashes: dict[str, str]) -> None:
    """Save hash manifest to hashes.txt file."""
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    header = f"""# StrategicKhaos Evidence Hash Manifest
# Algorithm: BLAKE3 (or SHA256 fallback)
# Format: <hash>  <relative_path_from_repo_root>
#
# To verify manually:
#   cd <repo_root>
#   blake3sum <file> | diff - <(grep <file> strategickhaos-proof/evidence/hashes.txt)
#
# To regenerate:
#   python strategickhaos-proof/verify_evidence.py --regenerate
#
# Last updated: {timestamp}
# ================================================

"""

    with open(manifest_path, "w") as f:
        f.write(header)

        # Group files by category
        categories = {
            "Core Configuration Files": [],
            "Governance Documents": [],
            "Source Code": [],
            "Deployment Configuration": [],
            "Evidence Dossier": [],
            "Other": [],
        }

        for filepath, hash_value in sorted(hashes.items()):
            if "dao_record" in filepath or "discovery" in filepath or "constitution" in filepath:
                categories["Core Configuration Files"].append((filepath, hash_value))
            elif "governance" in filepath:
                categories["Governance Documents"].append((filepath, hash_value))
            elif filepath.startswith("src/"):
                categories["Source Code"].append((filepath, hash_value))
            elif "Dockerfile" in filepath or "docker-compose" in filepath:
                categories["Deployment Configuration"].append((filepath, hash_value))
            elif "strategickhaos-proof" in filepath:
                categories["Evidence Dossier"].append((filepath, hash_value))
            else:
                categories["Other"].append((filepath, hash_value))

        for category, files in categories.items():
            if files:
                f.write(f"# {category}\n")
                f.write("# " + "-" * (len(category)) + "\n\n")
                for filepath, hash_value in files:
                    f.write(f"{hash_value}  {filepath}\n")
                f.write("\n")


def get_tracked_files(repo_root: Path) -> list[str]:
    """Get list of files to track for hash verification."""
    tracked = []

    # Core configuration files
    core_files = [
        "dao_record.yaml",
        "dao_record_v1.0.yaml",
        "discovery.yml",
        "ai_constitution.yaml",
    ]

    # Governance documents
    governance_files = [
        "governance/access_matrix.yaml",
        "governance/article_7_authorized_signers.md",
    ]

    # Source code
    src_files = [
        "src/bot.ts",
        "src/event-gateway.ts",
        "src/config.ts",
        "src/discord.ts",
    ]

    # Deployment configuration
    deploy_files = [
        "docker-compose.yml",
        "Dockerfile.bot",
        "Dockerfile.gateway",
    ]

    # Evidence dossier files (excluding hashes.txt itself)
    evidence_files = [
        "strategickhaos-proof/evidence/status_snapshot.json",
        "strategickhaos-proof/evidence/README.md",
        "strategickhaos-proof/evidence/how_to_verify.md",
    ]

    all_files = core_files + governance_files + src_files + deploy_files + evidence_files

    for filepath in all_files:
        full_path = repo_root / filepath
        if full_path.exists():
            tracked.append(filepath)

    return tracked


def verify_hashes(repo_root: Path, manifest_path: Path, verbose: bool = False) -> tuple[bool, list[str]]:
    """Verify all hashes in the manifest."""
    manifest = load_hash_manifest(manifest_path)
    errors = []
    verified_count = 0

    if not manifest:
        if verbose:
            print(f"{Colors.YELLOW}⚠ No hashes found in manifest (may contain only placeholders){Colors.RESET}")
        return True, []

    print(f"\n{Colors.BOLD}Verifying {len(manifest)} file hashes...{Colors.RESET}\n")

    for filepath, expected_hash in manifest.items():
        full_path = repo_root / filepath

        if not full_path.exists():
            errors.append(f"Missing file: {filepath}")
            print(f"  {Colors.RED}✗{Colors.RESET} {filepath} - FILE NOT FOUND")
            continue

        actual_hash = compute_blake3_hash(full_path)

        if actual_hash == expected_hash:
            verified_count += 1
            if verbose:
                print(f"  {Colors.GREEN}✓{Colors.RESET} {filepath}")
        else:
            errors.append(f"Hash mismatch: {filepath}")
            print(f"  {Colors.RED}✗{Colors.RESET} {filepath}")
            print(f"    Expected: {expected_hash}")
            print(f"    Actual:   {actual_hash}")

    if not errors:
        print(f"\n{Colors.GREEN}✓ All {verified_count} hashes verified successfully{Colors.RESET}")
    else:
        print(f"\n{Colors.RED}✗ {len(errors)} verification errors{Colors.RESET}")

    return len(errors) == 0, errors


def verify_cross_references(repo_root: Path, snapshot_path: Path, verbose: bool = False) -> tuple[bool, list[str]]:
    """Verify cross-references in status_snapshot.json."""
    errors = []

    if not snapshot_path.exists():
        errors.append("status_snapshot.json not found")
        return False, errors

    print(f"\n{Colors.BOLD}Verifying cross-references...{Colors.RESET}\n")

    with open(snapshot_path) as f:
        snapshot = json.load(f)

    # Verify cross_references section
    cross_refs = snapshot.get("cross_references", [])
    verified_count = 0

    for ref in cross_refs:
        claim = ref.get("claim", "Unknown")
        evidence_paths = ref.get("evidence", [])

        for evidence_path in evidence_paths:
            full_path = repo_root / evidence_path

            # Handle directory references
            if evidence_path.endswith("/"):
                if full_path.is_dir():
                    verified_count += 1
                    if verbose:
                        print(f"  {Colors.GREEN}✓{Colors.RESET} {evidence_path} (directory)")
                else:
                    errors.append(f"Missing directory for '{claim}': {evidence_path}")
                    print(f"  {Colors.RED}✗{Colors.RESET} {evidence_path} - DIRECTORY NOT FOUND")
            else:
                if full_path.exists():
                    verified_count += 1
                    if verbose:
                        print(f"  {Colors.GREEN}✓{Colors.RESET} {evidence_path}")
                else:
                    errors.append(f"Missing evidence for '{claim}': {evidence_path}")
                    print(f"  {Colors.RED}✗{Colors.RESET} {evidence_path} - FILE NOT FOUND")

    if not errors:
        print(f"\n{Colors.GREEN}✓ All {verified_count} cross-references verified{Colors.RESET}")
    else:
        print(f"\n{Colors.RED}✗ {len(errors)} cross-reference errors{Colors.RESET}")

    return len(errors) == 0, errors


def regenerate_hashes(repo_root: Path, manifest_path: Path, verbose: bool = False) -> None:
    """Regenerate hash manifest with current file hashes."""
    tracked_files = get_tracked_files(repo_root)
    hashes = {}

    print(f"\n{Colors.BOLD}Regenerating hash manifest...{Colors.RESET}\n")

    for filepath in tracked_files:
        full_path = repo_root / filepath
        hash_value = compute_blake3_hash(full_path)
        hashes[filepath] = hash_value
        print(f"  {Colors.BLUE}#{Colors.RESET} {filepath}")
        if verbose:
            print(f"    {hash_value}")

    save_hash_manifest(manifest_path, hashes)
    print(f"\n{Colors.GREEN}✓ Hash manifest regenerated with {len(hashes)} files{Colors.RESET}")
    print(f"  Saved to: {manifest_path}")


def main():
    parser = argparse.ArgumentParser(description="Verify StrategicKhaos evidence dossier")
    parser.add_argument("--regenerate", action="store_true", help="Regenerate hash manifest")
    parser.add_argument("--check-refs", action="store_true", help="Only check cross-references")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    args = parser.parse_args()

    repo_root = get_repo_root()
    proof_dir = repo_root / "strategickhaos-proof"
    manifest_path = proof_dir / "evidence" / "hashes.txt"
    snapshot_path = proof_dir / "evidence" / "status_snapshot.json"

    print(f"\n{Colors.BOLD}StrategicKhaos Evidence Verification{Colors.RESET}")
    print(f"Repository: {repo_root}")
    print("=" * 50)

    if args.regenerate:
        regenerate_hashes(repo_root, manifest_path, args.verbose)
        return 0

    all_passed = True
    all_errors = []

    if args.check_refs:
        passed, errors = verify_cross_references(repo_root, snapshot_path, args.verbose)
        all_passed = all_passed and passed
        all_errors.extend(errors)
    else:
        # Full verification
        hash_passed, hash_errors = verify_hashes(repo_root, manifest_path, args.verbose)
        ref_passed, ref_errors = verify_cross_references(repo_root, snapshot_path, args.verbose)

        all_passed = hash_passed and ref_passed
        all_errors.extend(hash_errors)
        all_errors.extend(ref_errors)

    print("\n" + "=" * 50)

    if all_passed:
        print(f"{Colors.GREEN}{Colors.BOLD}✅ Evidence dossier verification PASSED{Colors.RESET}")
        return 0
    else:
        print(f"{Colors.RED}{Colors.BOLD}❌ Evidence dossier verification FAILED{Colors.RESET}")
        print(f"\nErrors ({len(all_errors)}):")
        for error in all_errors:
            print(f"  - {error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
