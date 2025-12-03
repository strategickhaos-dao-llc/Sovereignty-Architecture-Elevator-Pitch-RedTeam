#!/usr/bin/env python3
"""
LyraNode Manifest Validator and Signer

Provides functionality for:
- Parsing YAML manifests
- Validating against JSON Schema
- GPG signing and verification
- Manifest sanitization for public release

Usage:
    python manifest_validator.py validate manifest.yaml
    python manifest_validator.py sign manifest.yaml --key-id 0x137SOVEREIGN
    python manifest_validator.py verify manifest.yaml
    python manifest_validator.py sanitize manifest.yaml --output public.yaml

Requirements:
    pip install pyyaml jsonschema python-gnupg

Author: Strategickhaos DAO LLC
Version: 1.0.0
"""

import argparse
import copy
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

import yaml

try:
    import jsonschema
    from jsonschema import Draft7Validator, ValidationError
except ImportError:
    jsonschema = None
    Draft7Validator = None
    ValidationError = None

try:
    import gnupg
except ImportError:
    gnupg = None


# Default schema path relative to this script
DEFAULT_SCHEMA_PATH = Path(__file__).parent / "lyra-node-manifest.schema.json"


class ManifestValidator:
    """Validates LyraNode manifests against JSON Schema."""

    def __init__(self, schema_path: Optional[Path] = None):
        """
        Initialize the validator with a schema.

        Args:
            schema_path: Path to JSON Schema file. Uses default if not provided.
        """
        self.schema_path = schema_path or DEFAULT_SCHEMA_PATH
        self.schema = self._load_schema()
        self.validator = None
        if Draft7Validator and self.schema:
            self.validator = Draft7Validator(self.schema)

    def _load_schema(self) -> dict:
        """Load JSON Schema from file."""
        if not self.schema_path.exists():
            print(f"Warning: Schema file not found at {self.schema_path}")
            return {}
        with open(self.schema_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def validate(self, manifest: dict) -> tuple[bool, list[str]]:
        """
        Validate manifest against schema.

        Args:
            manifest: Parsed manifest dictionary

        Returns:
            Tuple of (is_valid, list of error messages)
        """
        if not self.validator:
            return False, ["jsonschema library not installed or schema not loaded"]

        errors = []
        for error in self.validator.iter_errors(manifest):
            path = ".".join(str(p) for p in error.absolute_path)
            errors.append(f"{path}: {error.message}" if path else error.message)

        return len(errors) == 0, errors


class ManifestParser:
    """Parses and loads LyraNode manifests."""

    @staticmethod
    def load(file_path: Path) -> dict:
        """
        Load manifest from YAML file.

        Args:
            file_path: Path to YAML manifest file

        Returns:
            Parsed manifest dictionary
        """
        with open(file_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    @staticmethod
    def dump(manifest: dict, file_path: Path) -> None:
        """
        Write manifest to YAML file.

        Args:
            manifest: Manifest dictionary
            file_path: Output file path
        """
        with open(file_path, "w", encoding="utf-8") as f:
            yaml.dump(manifest, f, default_flow_style=False, sort_keys=False)

    @staticmethod
    def compute_checksum(content: str, algorithm: str = "sha256") -> str:
        """
        Compute checksum of content.

        Args:
            content: String content to hash
            algorithm: Hash algorithm (sha256, sha512)

        Returns:
            Hex-encoded hash string
        """
        if algorithm == "sha256":
            return hashlib.sha256(content.encode("utf-8")).hexdigest()
        elif algorithm == "sha512":
            return hashlib.sha512(content.encode("utf-8")).hexdigest()
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}")


class ManifestSigner:
    """GPG signing and verification for manifests."""

    def __init__(self, gnupg_home: Optional[str] = None):
        """
        Initialize GPG signer.

        Args:
            gnupg_home: Path to GPG home directory
        """
        if gnupg is None:
            self.gpg = None
            print("Warning: python-gnupg not installed. Signing disabled.")
        else:
            self.gpg = gnupg.GPG(gnupghome=gnupg_home)

    def sign(self, manifest_path: Path, key_id: str, detach: bool = True) -> Optional[str]:
        """
        Sign manifest with GPG key.

        Args:
            manifest_path: Path to manifest file
            key_id: GPG key identifier
            detach: Create detached signature

        Returns:
            Signature string or None on failure
        """
        if not self.gpg:
            print("Error: GPG not available")
            return None

        with open(manifest_path, "rb") as f:
            signed_data = self.gpg.sign_file(
                f, keyid=key_id, detach=detach, clearsign=not detach
            )

        if signed_data.ok:
            # Write detached signature
            sig_path = manifest_path.with_suffix(manifest_path.suffix + ".asc")
            with open(sig_path, "w", encoding="utf-8") as f:
                f.write(str(signed_data))
            print(f"Signature written to: {sig_path}")
            return str(signed_data)
        else:
            print(f"Signing failed: {signed_data.status}")
            return None

    def verify(self, manifest_path: Path, signature_path: Optional[Path] = None) -> tuple[bool, str]:
        """
        Verify GPG signature of manifest.

        Args:
            manifest_path: Path to manifest file
            signature_path: Path to detached signature (optional)

        Returns:
            Tuple of (is_valid, verification message)
        """
        if not self.gpg:
            return False, "GPG not available"

        sig_path = signature_path or manifest_path.with_suffix(manifest_path.suffix + ".asc")

        if not sig_path.exists():
            return False, f"Signature file not found: {sig_path}"

        with open(manifest_path, "rb") as f:
            verified = self.gpg.verify_file(f, str(sig_path))

        if verified.valid:
            return True, f"Valid signature from {verified.username} (key: {verified.key_id})"
        else:
            return False, f"Invalid signature: {verified.status}"


class ManifestSanitizer:
    """Sanitizes manifests for public release."""

    # Patterns for sensitive data
    SENSITIVE_PATTERNS = {
        "gpg_key": re.compile(r"0x[A-Fa-f0-9]+"),
        "checksum": re.compile(r"[a-fA-F0-9]{64}"),
        "commit_ref": re.compile(r"[a-fA-F0-9]{7,40}"),
        "url": re.compile(r"https?://[^\s\"']+"),
        "ip_address": re.compile(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"),
        "vault_ref": re.compile(r"vault://[^\s\"']+"),
    }

    # Fields to redact
    REDACT_FIELDS = {
        "operator.name",
        "operator.gpg_key_id",
        "signature.key_id",
        "signature.sig",
    }

    # Fields to remove entirely
    REMOVE_FIELDS = {
        "research_vaults",
        "library_names",
        "internal_endpoints",
    }

    # Fields to tokenize
    TOKENIZE_FIELDS = {
        "models.*.model_id": "MODEL_TOKEN",
        "models.*.checksum": "checksum_ref",
        "milestones.*.commit_ref": "COMMIT",
        "hooks.*.url": "WEBHOOK_REF",
        "hooks.*.secret_ref": None,  # Remove entirely
    }

    def sanitize(self, manifest: dict) -> dict:
        """
        Sanitize manifest for public release.

        Args:
            manifest: Original manifest dictionary

        Returns:
            Sanitized manifest dictionary
        """
        sanitized = copy.deepcopy(manifest)

        # Remove sensitive fields
        for field in self.REMOVE_FIELDS:
            self._remove_field(sanitized, field)

        # Redact specific fields
        self._redact_operator(sanitized)
        self._tokenize_models(sanitized)
        self._tokenize_milestones(sanitized)
        self._sanitize_hooks(sanitized)
        self._sanitize_signature(sanitized)
        self._sanitize_provenance(sanitized)

        # Add sanitization metadata
        sanitized["_sanitization"] = {
            "sanitized_at": datetime.now(timezone.utc).isoformat(),
            "version": "1.0",
            "classification": "PUBLIC",
        }

        return sanitized

    def _remove_field(self, obj: dict, field: str) -> None:
        """Remove a field from nested dictionary."""
        parts = field.split(".")
        current = obj
        for part in parts[:-1]:
            if part in current:
                current = current[part]
            else:
                return
        if parts[-1] in current:
            del current[parts[-1]]

    def _redact_operator(self, manifest: dict) -> None:
        """Redact operator information."""
        if "operator" in manifest:
            op = manifest["operator"]
            if "name" in op:
                op["name"] = "[REDACTED]"
            if "gpg_key_id" in op:
                op["gpg_key_id"] = "[KEY_REF:operator_primary]"
            if "node_ref" in op:
                op["node_ref"] = "node-xxx"

    def _tokenize_models(self, manifest: dict) -> None:
        """Tokenize model identifiers and checksums."""
        if "models" not in manifest:
            return

        for i, model in enumerate(manifest["models"]):
            name = model.get("name", f"model_{i}")
            safe_name = re.sub(r"[^a-zA-Z0-9]", "_", name).lower()

            if "model_id" in model:
                model["model_id"] = f"[MODEL_TOKEN:{safe_name}]"

            if "checksum" in model:
                del model["checksum"]
                model["checksum_ref"] = f"verify://models/{safe_name}/integrity"

    def _tokenize_milestones(self, manifest: dict) -> None:
        """Tokenize milestone commit references."""
        if "milestones" not in manifest:
            return

        for i, milestone in enumerate(manifest["milestones"]):
            if "commit_ref" in milestone:
                milestone["commit_ref"] = f"[COMMIT:milestone_{i + 1}]"

    def _sanitize_hooks(self, manifest: dict) -> None:
        """Sanitize webhook URLs and secrets."""
        if "hooks" not in manifest:
            return

        for hook in manifest["hooks"]:
            event_type = hook.get("on", "unknown")
            if "url" in hook:
                hook["url"] = f"[WEBHOOK_REF:{event_type}]"
            if "secret_ref" in hook:
                del hook["secret_ref"]

    def _sanitize_signature(self, manifest: dict) -> None:
        """Sanitize signature block."""
        if "signature" not in manifest:
            return

        sig = manifest["signature"]
        if "key_id" in sig:
            sig["key_id"] = "[KEY_REF:signing_public]"
        if "sig" in sig:
            sig["sig"] = "[BASE64_SIGNATURE]"
        sig["verify_url"] = "https://verify.example.com/manifest"

    def _sanitize_provenance(self, manifest: dict) -> None:
        """Sanitize provenance checksums."""
        if "provenance" not in manifest:
            return

        prov = manifest["provenance"]
        if "checksums" in prov:
            prov["checksums"] = {"verification_token": "[INTEGRITY:manifest_v1]"}


def cmd_validate(args: argparse.Namespace) -> int:
    """Validate manifest command."""
    manifest_path = Path(args.manifest)
    if not manifest_path.exists():
        print(f"Error: File not found: {manifest_path}")
        return 1

    schema_path = Path(args.schema) if args.schema else None
    validator = ManifestValidator(schema_path)

    try:
        manifest = ManifestParser.load(manifest_path)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}")
        return 1

    is_valid, errors = validator.validate(manifest)

    if is_valid:
        print(f"✓ Manifest is valid: {manifest_path}")

        # Compute and display checksum
        with open(manifest_path, "r", encoding="utf-8") as f:
            content = f.read()
        checksum = ManifestParser.compute_checksum(content)
        print(f"  SHA256: {checksum}")

        return 0
    else:
        print(f"✗ Validation errors in {manifest_path}:")
        for error in errors:
            print(f"  - {error}")
        return 1


def cmd_sign(args: argparse.Namespace) -> int:
    """Sign manifest command."""
    manifest_path = Path(args.manifest)
    if not manifest_path.exists():
        print(f"Error: File not found: {manifest_path}")
        return 1

    signer = ManifestSigner(args.gnupg_home)
    signature = signer.sign(manifest_path, args.key_id, detach=True)

    if signature:
        print("✓ Manifest signed successfully")

        # Update manifest with signature metadata
        if args.update_manifest:
            manifest = ManifestParser.load(manifest_path)
            manifest["signature"] = {
                "method": "GPG",
                "key_id": args.key_id,
                "sig_ts": datetime.now(timezone.utc).isoformat(),
                "algorithm": "RSA",
            }
            ManifestParser.dump(manifest, manifest_path)
            print("  Updated manifest with signature metadata")

        return 0
    else:
        print("✗ Signing failed")
        return 1


def cmd_verify(args: argparse.Namespace) -> int:
    """Verify manifest signature command."""
    manifest_path = Path(args.manifest)
    if not manifest_path.exists():
        print(f"Error: File not found: {manifest_path}")
        return 1

    sig_path = Path(args.signature) if args.signature else None
    signer = ManifestSigner(args.gnupg_home)
    is_valid, message = signer.verify(manifest_path, sig_path)

    if is_valid:
        print(f"✓ {message}")
        return 0
    else:
        print(f"✗ {message}")
        return 1


def cmd_sanitize(args: argparse.Namespace) -> int:
    """Sanitize manifest command."""
    manifest_path = Path(args.manifest)
    if not manifest_path.exists():
        print(f"Error: File not found: {manifest_path}")
        return 1

    try:
        manifest = ManifestParser.load(manifest_path)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}")
        return 1

    sanitizer = ManifestSanitizer()
    sanitized = sanitizer.sanitize(manifest)

    output_path = Path(args.output) if args.output else manifest_path.with_stem(
        manifest_path.stem + "_public"
    )

    ManifestParser.dump(sanitized, output_path)
    print(f"✓ Sanitized manifest written to: {output_path}")

    # Compute checksum of sanitized output
    with open(output_path, "r", encoding="utf-8") as f:
        content = f.read()
    checksum = ManifestParser.compute_checksum(content)
    print(f"  SHA256: {checksum}")

    return 0


def cmd_checksum(args: argparse.Namespace) -> int:
    """Compute checksum command."""
    manifest_path = Path(args.manifest)
    if not manifest_path.exists():
        print(f"Error: File not found: {manifest_path}")
        return 1

    with open(manifest_path, "r", encoding="utf-8") as f:
        content = f.read()

    sha256 = ManifestParser.compute_checksum(content, "sha256")
    sha512 = ManifestParser.compute_checksum(content, "sha512")

    print(f"Checksums for: {manifest_path}")
    print(f"  SHA256: {sha256}")
    print(f"  SHA512: {sha512}")

    return 0


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="LyraNode Manifest Validator and Signer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    %(prog)s validate manifest.yaml
    %(prog)s validate manifest.yaml --schema custom-schema.json
    %(prog)s sign manifest.yaml --key-id 0x137SOVEREIGN
    %(prog)s verify manifest.yaml
    %(prog)s sanitize manifest.yaml --output public.yaml
    %(prog)s checksum manifest.yaml
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate manifest against schema")
    validate_parser.add_argument("manifest", help="Path to manifest YAML file")
    validate_parser.add_argument("--schema", help="Path to JSON Schema file")

    # Sign command
    sign_parser = subparsers.add_parser("sign", help="Sign manifest with GPG")
    sign_parser.add_argument("manifest", help="Path to manifest YAML file")
    sign_parser.add_argument("--key-id", required=True, help="GPG key identifier")
    sign_parser.add_argument("--gnupg-home", help="Path to GPG home directory")
    sign_parser.add_argument(
        "--update-manifest",
        action="store_true",
        help="Update manifest with signature metadata",
    )

    # Verify command
    verify_parser = subparsers.add_parser("verify", help="Verify manifest GPG signature")
    verify_parser.add_argument("manifest", help="Path to manifest YAML file")
    verify_parser.add_argument("--signature", help="Path to detached signature file")
    verify_parser.add_argument("--gnupg-home", help="Path to GPG home directory")

    # Sanitize command
    sanitize_parser = subparsers.add_parser(
        "sanitize", help="Sanitize manifest for public release"
    )
    sanitize_parser.add_argument("manifest", help="Path to manifest YAML file")
    sanitize_parser.add_argument("--output", "-o", help="Output file path")

    # Checksum command
    checksum_parser = subparsers.add_parser("checksum", help="Compute manifest checksums")
    checksum_parser.add_argument("manifest", help="Path to manifest YAML file")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    commands = {
        "validate": cmd_validate,
        "sign": cmd_sign,
        "verify": cmd_verify,
        "sanitize": cmd_sanitize,
        "checksum": cmd_checksum,
    }

    return commands[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
