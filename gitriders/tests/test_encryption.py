# GitRiders - FlameLang Sovereignty Export System
# Copyright (c) 2025 StrategicKhaos DAO LLC
# Licensed under MIT License
# Date: December 13, 2025

"""Tests for encryption and decryption."""

import pytest
from sovereign_export.encrypt import EncryptionManager, encrypt_export_package


def test_key_generation():
    """Test encryption key generation."""
    manager = EncryptionManager()
    key = manager.generate_key()
    
    assert isinstance(key, bytes)
    assert len(key) == 32  # XChaCha20-Poly1305 requires 32-byte key


def test_key_derivation_from_passphrase():
    """Test key derivation from passphrase."""
    manager = EncryptionManager()
    
    passphrase = "test-passphrase-123"
    key1, salt1 = manager.derive_key_from_passphrase(passphrase)
    
    assert isinstance(key1, bytes)
    assert len(key1) == 32
    assert isinstance(salt1, bytes)
    
    # Same passphrase with same salt should produce same key
    key2, salt2 = manager.derive_key_from_passphrase(passphrase, salt1)
    assert key1 == key2


def test_encryption_decryption():
    """Test basic encryption and decryption."""
    manager = EncryptionManager()
    key = manager.generate_key()
    
    data = {
        "test": "data",
        "conversations": [{"id": "1", "content": "Hello"}]
    }
    
    # Encrypt
    encrypted = manager.encrypt(data, key)
    
    assert "version" in encrypted
    assert "algorithm" in encrypted
    assert "ciphertext" in encrypted
    assert "nonce" in encrypted
    assert encrypted["algorithm"] == "XChaCha20-Poly1305"
    
    # Decrypt
    decrypted = manager.decrypt(encrypted, key)
    
    assert decrypted == data


def test_decryption_with_wrong_key():
    """Test that decryption fails with wrong key."""
    manager = EncryptionManager()
    key1 = manager.generate_key()
    key2 = manager.generate_key()
    
    data = {"test": "data"}
    
    # Encrypt with key1
    encrypted = manager.encrypt(data, key1)
    
    # Try to decrypt with key2
    with pytest.raises(ValueError, match="Decryption failed"):
        manager.decrypt(encrypted, key2)


def test_encrypt_export_package():
    """Test encrypting a complete export package."""
    package = {
        "data": {"conversations": []},
        "manifest": {"version": "1.0"}
    }
    
    encrypted, key, escrow = encrypt_export_package(package)
    
    assert isinstance(encrypted, dict)
    assert isinstance(key, bytes)
    assert len(key) == 32
    assert escrow is None  # No escrow requested


def test_encrypt_export_package_with_passphrase():
    """Test encrypting with passphrase."""
    package = {
        "data": {"conversations": []},
        "manifest": {"version": "1.0"}
    }
    
    passphrase = "my-secure-passphrase"
    encrypted, key, escrow = encrypt_export_package(package, passphrase=passphrase)
    
    assert isinstance(encrypted, dict)
    assert isinstance(key, bytes)
    assert "encryption_salt" in package


def test_encrypt_export_package_with_escrow():
    """Test encrypting with key escrow."""
    package = {
        "data": {"conversations": []},
        "manifest": {"version": "1.0"}
    }
    
    escrow_keys = ["abc123", "def456"]
    encrypted, key, escrow = encrypt_export_package(
        package,
        escrow_keys=escrow_keys
    )
    
    assert isinstance(escrow, dict)
    assert "shares" in escrow
    assert len(escrow["shares"]) == len(escrow_keys)
