#!/usr/bin/env python3
"""
scanner.py - SACSE Artifact Scanner and GPG Verification Tool

This module scans directories for .htm artifacts and verifies their GPG signatures.
Part of the Sovereign Autonomous Continuous Systems Engineering (SACSE) workflow.

Usage:
    python scanner.py --scan <directory>       # Scan for artifacts
    python scanner.py --verify <directory>     # Verify GPG signatures
    python scanner.py --manifest <directory>   # Generate verification manifest

Safety Notes:
    - All artifact paths are validated to prevent path traversal attacks
    - GPG verification uses subprocess with shell=False for security
    - Manifest checksums use SHA-256 for integrity verification
"""

import argparse
import hashlib
import json
import logging
import os
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


@dataclass
class ArtifactRecord:
    """Represents a scanned artifact with its verification status."""

    path: str
    size_bytes: int
    sha256: str
    mtime: str
    gpg_signature: Optional[str] = None
    gpg_verified: bool = False
    gpg_signer: Optional[str] = None
    errors: list = field(default_factory=list)


class ScannerConfig:
    """Configuration for the artifact scanner."""

    # File extensions to scan for artifacts
    ARTIFACT_EXTENSIONS = {".htm", ".html"}
    # Maximum file size to process (100 MB)
    MAX_FILE_SIZE = 100 * 1024 * 1024
    # GPG signature extension
    GPG_EXTENSION = ".gpg"

    def __init__(self, base_dir: str):
        """Initialize scanner configuration with a base directory."""
        self.base_dir = Path(base_dir).resolve()
        if not self.base_dir.is_dir():
            raise ValueError(f"Base directory does not exist: {self.base_dir}")


def calculate_sha256(file_path: Path) -> str:
    """Calculate SHA-256 checksum of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()


def validate_path(path: Path, base_dir: Path) -> bool:
    """
    Validate that a path is within the base directory (prevent path traversal).

    Args:
        path: The path to validate
        base_dir: The base directory that path must be within

    Returns:
        True if path is valid and within base_dir, False otherwise
    """
    try:
        resolved = path.resolve()
        return resolved.is_relative_to(base_dir)
    except (ValueError, RuntimeError):
        return False


def verify_gpg_signature(artifact_path: Path, signature_path: Path) -> dict:
    """
    Verify GPG signature of an artifact.

    Args:
        artifact_path: Path to the artifact file
        signature_path: Path to the GPG signature file

    Returns:
        Dict with verification status, signer info, and any errors
    """
    result = {
        "verified": False,
        "signer": None,
        "errors": [],
    }

    if not signature_path.exists():
        result["errors"].append(f"Signature file not found: {signature_path}")
        return result

    try:
        # Use gpg --verify with detached signature
        # shell=False for security
        cmd = [
            "gpg",
            "--verify",
            "--status-fd",
            "1",
            str(signature_path),
            str(artifact_path),
        ]
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
        )

        # Parse GPG output for verification status
        if proc.returncode == 0:
            result["verified"] = True
            # Extract signer from output if available
            for line in proc.stdout.split("\n"):
                if "GOODSIG" in line:
                    parts = line.split("GOODSIG")
                    if len(parts) > 1:
                        result["signer"] = parts[1].strip()
                    break
        else:
            result["errors"].append(f"GPG verification failed: {proc.stderr}")

    except subprocess.TimeoutExpired:
        result["errors"].append("GPG verification timed out")
    except FileNotFoundError:
        result["errors"].append("GPG executable not found - is GnuPG installed?")
    except subprocess.SubprocessError as e:
        result["errors"].append(f"GPG subprocess error: {e}")

    return result


def scan_artifacts(config: ScannerConfig) -> list[ArtifactRecord]:
    """
    Scan directory for .htm artifacts and their GPG signatures.

    Args:
        config: Scanner configuration

    Returns:
        List of ArtifactRecord objects
    """
    artifacts = []
    base_dir = config.base_dir

    logger.info(f"Scanning for artifacts in: {base_dir}")

    for root, _, files in os.walk(base_dir):
        root_path = Path(root)

        for filename in files:
            file_path = root_path / filename

            # Skip if not an artifact file
            if file_path.suffix.lower() not in ScannerConfig.ARTIFACT_EXTENSIONS:
                continue

            # Validate path security
            if not validate_path(file_path, base_dir):
                logger.warning(f"Skipping invalid path: {file_path}")
                continue

            # Check file size
            try:
                stat = file_path.stat()
                if stat.st_size > ScannerConfig.MAX_FILE_SIZE:
                    logger.warning(f"Skipping oversized file: {file_path}")
                    continue
            except OSError as e:
                logger.error(f"Cannot stat file {file_path}: {e}")
                continue

            # Create artifact record
            try:
                record = ArtifactRecord(
                    path=str(file_path.relative_to(base_dir)),
                    size_bytes=stat.st_size,
                    sha256=calculate_sha256(file_path),
                    mtime=datetime.fromtimestamp(
                        stat.st_mtime, tz=timezone.utc
                    ).isoformat(),
                )

                # Check for GPG signature
                gpg_path = Path(str(file_path) + ScannerConfig.GPG_EXTENSION)
                if gpg_path.exists() and validate_path(gpg_path, base_dir):
                    record.gpg_signature = str(gpg_path.relative_to(base_dir))

                    # Verify signature
                    gpg_result = verify_gpg_signature(file_path, gpg_path)
                    record.gpg_verified = gpg_result["verified"]
                    record.gpg_signer = gpg_result["signer"]
                    record.errors = gpg_result["errors"]

                artifacts.append(record)
                logger.debug(f"Scanned: {record.path}")

            except OSError as e:
                logger.error(f"Error processing {file_path}: {e}")
                continue

    logger.info(f"Found {len(artifacts)} artifacts")
    return artifacts


def generate_manifest(artifacts: list[ArtifactRecord], output_path: Optional[Path] = None) -> dict:
    """
    Generate a verification manifest from scanned artifacts.

    Args:
        artifacts: List of scanned artifact records
        output_path: Optional path to write manifest JSON

    Returns:
        Manifest dictionary
    """
    verified_count = sum(1 for a in artifacts if a.gpg_verified)
    unsigned_count = sum(1 for a in artifacts if a.gpg_signature is None)

    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "generator": "scanner.py",
        "version": "1.0.0",
        "summary": {
            "total_artifacts": len(artifacts),
            "gpg_verified": verified_count,
            "gpg_unsigned": unsigned_count,
            "gpg_failed": len(artifacts) - verified_count - unsigned_count,
        },
        "artifacts": [
            {
                "path": a.path,
                "sha256": a.sha256,
                "size_bytes": a.size_bytes,
                "mtime": a.mtime,
                "gpg_signature": a.gpg_signature,
                "gpg_verified": a.gpg_verified,
                "gpg_signer": a.gpg_signer,
            }
            for a in artifacts
        ],
    }

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)
        logger.info(f"Manifest written to: {output_path}")

    return manifest


def print_summary(artifacts: list[ArtifactRecord]) -> None:
    """Print a summary of scanned artifacts to stdout."""
    verified = sum(1 for a in artifacts if a.gpg_verified)
    unsigned = sum(1 for a in artifacts if a.gpg_signature is None)
    failed = len(artifacts) - verified - unsigned

    print("\n" + "=" * 60)
    print("SACSE Artifact Scanner - Summary")
    print("=" * 60)
    print(f"Total artifacts:     {len(artifacts)}")
    print(f"GPG verified:        {verified} ✓")
    print(f"GPG unsigned:        {unsigned} ⚠")
    print(f"GPG failed:          {failed} ✗")
    print("=" * 60)

    if failed > 0:
        print("\nFailed verifications:")
        for a in artifacts:
            if not a.gpg_verified and a.gpg_signature:
                print(f"  - {a.path}")
                for error in a.errors:
                    print(f"    Error: {error}")


def main():
    """Main entry point for the scanner CLI."""
    parser = argparse.ArgumentParser(
        description="SACSE Artifact Scanner - Scan and verify GPG-signed artifacts",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    %(prog)s --scan ./artifacts
    %(prog)s --verify ./artifacts
    %(prog)s --manifest ./artifacts -o manifest.json

For more information, see the SACSE documentation in README.md
        """,
    )

    parser.add_argument(
        "--scan",
        metavar="DIR",
        help="Scan directory for artifacts and print summary",
    )
    parser.add_argument(
        "--verify",
        metavar="DIR",
        help="Verify GPG signatures of artifacts in directory",
    )
    parser.add_argument(
        "--manifest",
        metavar="DIR",
        help="Generate verification manifest for artifacts",
    )
    parser.add_argument(
        "-o",
        "--output",
        metavar="FILE",
        help="Output file for manifest (default: stdout as JSON)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Determine which directory to use
    target_dir = args.scan or args.verify or args.manifest

    if not target_dir:
        parser.print_help()
        sys.exit(1)

    try:
        config = ScannerConfig(target_dir)
    except ValueError as e:
        logger.error(str(e))
        sys.exit(1)

    # Scan artifacts
    artifacts = scan_artifacts(config)

    if args.manifest:
        # Generate manifest
        output_path = Path(args.output) if args.output else None
        manifest = generate_manifest(artifacts, output_path)
        if not output_path:
            print(json.dumps(manifest, indent=2))
    else:
        # Print summary
        print_summary(artifacts)

    # Exit with error if any verifications failed
    failed = sum(1 for a in artifacts if not a.gpg_verified and a.gpg_signature)
    if failed > 0:
        sys.exit(2)


if __name__ == "__main__":
    main()
