# GitRiders - FlameLang Sovereignty Export System
# Copyright (c) 2025 StrategicKhaos DAO LLC
# Licensed under MIT License
# Date: December 13, 2025

"""
Signed manifest generation and verification using Ed25519.
"""

import json
import hashlib
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from pathlib import Path

from nacl.signing import SigningKey, VerifyKey
from nacl.encoding import HexEncoder
import nacl.exceptions


class ManifestGenerator:
    """Generate cryptographically signed manifests for exports."""
    
    def __init__(self, signing_key: Optional[SigningKey] = None):
        """
        Initialize manifest generator.
        
        Args:
            signing_key: Ed25519 signing key. If None, generates new key.
        """
        self.signing_key = signing_key or SigningKey.generate()
        self.verify_key = self.signing_key.verify_key
    
    def generate_manifest(
        self,
        data: Dict[str, Any],
        provider: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate a signed manifest for export data.
        
        Args:
            data: The export data to manifest
            provider: Provider name (e.g., "openai", "anthropic")
            metadata: Optional additional metadata
        
        Returns:
            Manifest dictionary with signature
        """
        # Create manifest content
        manifest = {
            "version": "1.0",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "provider": provider,
            "data_hash": self._hash_data(data),
            "metadata": metadata or {},
        }
        
        # Sign the manifest
        manifest_bytes = json.dumps(manifest, sort_keys=True).encode("utf-8")
        signed = self.signing_key.sign(manifest_bytes)
        
        # Add signature and public key
        manifest["signature"] = signed.signature.hex()
        manifest["public_key"] = self.verify_key.encode(encoder=HexEncoder).decode("utf-8")
        
        return manifest
    
    def _hash_data(self, data: Dict[str, Any]) -> str:
        """
        Compute SHA-256 hash of data.
        
        Args:
            data: Data to hash
        
        Returns:
            Hex-encoded hash
        """
        data_bytes = json.dumps(data, sort_keys=True).encode("utf-8")
        return hashlib.sha256(data_bytes).hexdigest()
    
    def save_key(self, path: Path) -> None:
        """
        Save signing key to file.
        
        Args:
            path: Path to save key
        """
        with open(path, "wb") as f:
            f.write(self.signing_key.encode())
        # Set restrictive permissions
        path.chmod(0o600)
    
    @classmethod
    def load_key(cls, path: Path) -> "ManifestGenerator":
        """
        Load signing key from file.
        
        Args:
            path: Path to key file
        
        Returns:
            ManifestGenerator with loaded key
        """
        with open(path, "rb") as f:
            key_bytes = f.read()
        signing_key = SigningKey(key_bytes)
        return cls(signing_key)


def verify_manifest(
    manifest: Dict[str, Any],
    data: Dict[str, Any]
) -> bool:
    """
    Verify a signed manifest.
    
    Args:
        manifest: Manifest dictionary with signature
        data: The export data to verify against
    
    Returns:
        True if signature is valid and data hash matches
    
    Raises:
        ValueError: If verification fails
    """
    # Extract signature and public key
    signature_hex = manifest.get("signature")
    public_key_hex = manifest.get("public_key")
    
    if not signature_hex or not public_key_hex:
        raise ValueError("Manifest missing signature or public_key")
    
    # Reconstruct manifest without signature
    manifest_copy = manifest.copy()
    del manifest_copy["signature"]
    del manifest_copy["public_key"]
    
    # Verify data hash
    data_bytes = json.dumps(data, sort_keys=True).encode("utf-8")
    data_hash = hashlib.sha256(data_bytes).hexdigest()
    
    if data_hash != manifest_copy["data_hash"]:
        raise ValueError(
            f"Data hash mismatch: expected {manifest_copy['data_hash']}, "
            f"got {data_hash}"
        )
    
    # Verify signature
    try:
        verify_key = VerifyKey(public_key_hex, encoder=HexEncoder)
        manifest_bytes = json.dumps(manifest_copy, sort_keys=True).encode("utf-8")
        signature = bytes.fromhex(signature_hex)
        
        verify_key.verify(manifest_bytes, signature)
        return True
    
    except nacl.exceptions.BadSignatureError:
        raise ValueError("Invalid signature")
    except Exception as e:
        raise ValueError(f"Verification error: {e}")


def create_export_package(
    data: Dict[str, Any],
    provider: str,
    generator: ManifestGenerator,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Create a complete export package with data and manifest.
    
    Args:
        data: Export data
        provider: Provider name
        generator: ManifestGenerator instance
        metadata: Optional metadata
    
    Returns:
        Complete export package
    """
    manifest = generator.generate_manifest(data, provider, metadata)
    
    return {
        "data": data,
        "manifest": manifest,
    }


def save_export_package(package: Dict[str, Any], path: Path) -> None:
    """
    Save export package to file.
    
    Args:
        package: Export package
        path: Output file path
    """
    with open(path, "w") as f:
        json.dump(package, f, indent=2)


def load_export_package(path: Path) -> Dict[str, Any]:
    """
    Load export package from file.
    
    Args:
        path: Path to export file
    
    Returns:
        Export package
    """
    with open(path, "r") as f:
        return json.load(f)
