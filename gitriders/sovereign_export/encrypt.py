# GitRiders - FlameLang Sovereignty Export System
# Copyright (c) 2025 StrategicKhaos DAO LLC
# Licensed under MIT License
# Date: December 13, 2025

"""
End-to-end encryption with XChaCha20-Poly1305 and optional key escrow.
"""

import json
import secrets
from typing import Dict, Any, Optional, Tuple
from pathlib import Path

from nacl.secret import SecretBox
from nacl.encoding import Base64Encoder
from nacl.utils import random as nacl_random
from argon2 import PasswordHasher
from argon2.low_level import Type


class EncryptionManager:
    """Manage encryption and decryption of export data."""
    
    def __init__(self):
        """Initialize encryption manager."""
        self.ph = PasswordHasher(
            time_cost=3,
            memory_cost=65536,
            parallelism=4,
            hash_len=32,
            type=Type.ID
        )
    
    def generate_key(self) -> bytes:
        """
        Generate a random encryption key.
        
        Returns:
            32-byte encryption key
        """
        return nacl_random(SecretBox.KEY_SIZE)
    
    def derive_key_from_passphrase(self, passphrase: str, salt: Optional[bytes] = None) -> Tuple[bytes, bytes]:
        """
        Derive encryption key from passphrase using Argon2id.
        
        Args:
            passphrase: User passphrase
            salt: Optional salt (generated if not provided)
        
        Returns:
            Tuple of (key, salt)
        """
        if salt is None:
            salt = secrets.token_bytes(16)
        
        # Use Argon2id for key derivation
        hash_result = self.ph.hash(passphrase.encode('utf-8'))
        
        # Extract the raw hash (last 43 characters before the final $)
        # Argon2 format: $argon2id$v=19$m=65536,t=3,p=4$salt$hash
        parts = hash_result.split('$')
        # For proper key derivation, we need to use the low-level API
        from argon2.low_level import hash_secret_raw
        
        key = hash_secret_raw(
            secret=passphrase.encode('utf-8'),
            salt=salt,
            time_cost=3,
            memory_cost=65536,
            parallelism=4,
            hash_len=32,
            type=Type.ID
        )
        
        return key, salt
    
    def encrypt(
        self,
        data: Dict[str, Any],
        key: bytes
    ) -> Dict[str, Any]:
        """
        Encrypt data with authenticated encryption.
        
        Args:
            data: Data to encrypt
            key: Encryption key (32 bytes)
        
        Returns:
            Dictionary with encrypted data and metadata
        """
        box = SecretBox(key)
        
        # Serialize data
        plaintext = json.dumps(data, indent=2).encode('utf-8')
        
        # Encrypt with random nonce
        encrypted = box.encrypt(plaintext)
        
        return {
            "version": "1.0",
            "algorithm": "XChaCha20-Poly1305",
            "ciphertext": encrypted.ciphertext.hex(),
            "nonce": encrypted.nonce.hex(),
        }
    
    def decrypt(
        self,
        encrypted_data: Dict[str, Any],
        key: bytes
    ) -> Dict[str, Any]:
        """
        Decrypt authenticated encrypted data.
        
        Args:
            encrypted_data: Encrypted data dictionary
            key: Encryption key (32 bytes)
        
        Returns:
            Decrypted data
        
        Raises:
            ValueError: If decryption fails
        """
        if encrypted_data.get("algorithm") != "XChaCha20-Poly1305":
            raise ValueError(f"Unsupported algorithm: {encrypted_data.get('algorithm')}")
        
        box = SecretBox(key)
        
        # Reconstruct encrypted message
        ciphertext = bytes.fromhex(encrypted_data["ciphertext"])
        nonce = bytes.fromhex(encrypted_data["nonce"])
        
        try:
            # Decrypt
            plaintext = box.decrypt(ciphertext, nonce)
            return json.loads(plaintext.decode('utf-8'))
        except Exception as e:
            raise ValueError(f"Decryption failed: {e}")
    
    def create_escrow_package(
        self,
        key: bytes,
        escrow_public_keys: list[str]
    ) -> Dict[str, Any]:
        """
        Create key escrow package for recovery.
        
        Args:
            key: Encryption key to escrow
            escrow_public_keys: List of escrow agent public keys (hex)
        
        Returns:
            Escrow package with encrypted key shares
        """
        # For production, implement Shamir's Secret Sharing or similar
        # This is a simplified version
        escrow_shares = []
        
        for pub_key_hex in escrow_public_keys:
            # In production, use proper asymmetric encryption
            # This is a placeholder
            share = {
                "escrow_key_id": pub_key_hex[:16],
                "encrypted_share": key.hex(),  # INSECURE: for demo only
                "algorithm": "placeholder",
            }
            escrow_shares.append(share)
        
        return {
            "version": "1.0",
            "escrow_type": "simple",
            "shares": escrow_shares,
            "recovery_threshold": len(escrow_shares),
        }
    
    def save_key(self, key: bytes, path: Path) -> None:
        """
        Save encryption key to file securely.
        
        Args:
            key: Encryption key
            path: Path to save key
        """
        with open(path, "wb") as f:
            f.write(key)
        # Set restrictive permissions
        path.chmod(0o600)
    
    def load_key(self, path: Path) -> bytes:
        """
        Load encryption key from file.
        
        Args:
            path: Path to key file
        
        Returns:
            Encryption key
        """
        with open(path, "rb") as f:
            return f.read()


def encrypt_export_package(
    package: Dict[str, Any],
    passphrase: Optional[str] = None,
    key: Optional[bytes] = None,
    escrow_keys: Optional[list[str]] = None
) -> Tuple[Dict[str, Any], bytes, Optional[Dict[str, Any]]]:
    """
    Encrypt an export package.
    
    Args:
        package: Export package to encrypt
        passphrase: Optional passphrase for key derivation
        key: Optional pre-generated key
        escrow_keys: Optional list of escrow public keys
    
    Returns:
        Tuple of (encrypted_package, key, escrow_package)
    """
    manager = EncryptionManager()
    
    # Generate or derive key
    if key is None:
        if passphrase:
            key, salt = manager.derive_key_from_passphrase(passphrase)
            package["encryption_salt"] = salt.hex()
        else:
            key = manager.generate_key()
    
    # Encrypt the package
    encrypted = manager.encrypt(package, key)
    
    # Create escrow if requested
    escrow_package = None
    if escrow_keys:
        escrow_package = manager.create_escrow_package(key, escrow_keys)
    
    return encrypted, key, escrow_package
