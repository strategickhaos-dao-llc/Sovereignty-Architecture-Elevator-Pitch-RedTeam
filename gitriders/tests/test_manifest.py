# GitRiders - FlameLang Sovereignty Export System
# Copyright (c) 2025 StrategicKhaos DAO LLC
# Licensed under MIT License
# Date: December 13, 2025

"""Tests for manifest generation and verification."""

import pytest
from sovereign_export.manifest import ManifestGenerator, verify_manifest, create_export_package


def test_manifest_generation():
    """Test basic manifest generation."""
    generator = ManifestGenerator()
    
    data = {
        "provider": "test",
        "conversations": [
            {"id": "1", "messages": [{"content": "Hello"}]}
        ]
    }
    
    manifest = generator.generate_manifest(data, "test")
    
    assert "version" in manifest
    assert "timestamp" in manifest
    assert "provider" in manifest
    assert "data_hash" in manifest
    assert "signature" in manifest
    assert "public_key" in manifest
    assert manifest["provider"] == "test"


def test_manifest_verification():
    """Test manifest verification."""
    generator = ManifestGenerator()
    
    data = {
        "provider": "test",
        "conversations": [
            {"id": "1", "messages": [{"content": "Hello"}]}
        ]
    }
    
    manifest = generator.generate_manifest(data, "test")
    
    # Should verify successfully
    assert verify_manifest(manifest, data) is True


def test_manifest_verification_tampered_data():
    """Test that verification fails with tampered data."""
    generator = ManifestGenerator()
    
    data = {
        "provider": "test",
        "conversations": [
            {"id": "1", "messages": [{"content": "Hello"}]}
        ]
    }
    
    manifest = generator.generate_manifest(data, "test")
    
    # Tamper with data
    data["conversations"][0]["messages"][0]["content"] = "Modified"
    
    # Should fail verification
    with pytest.raises(ValueError, match="Data hash mismatch"):
        verify_manifest(manifest, data)


def test_manifest_verification_invalid_signature():
    """Test that verification fails with invalid signature."""
    generator = ManifestGenerator()
    
    data = {
        "provider": "test",
        "conversations": [
            {"id": "1", "messages": [{"content": "Hello"}]}
        ]
    }
    
    manifest = generator.generate_manifest(data, "test")
    
    # Tamper with signature
    manifest["signature"] = "0" * 128
    
    # Should fail verification
    with pytest.raises(ValueError, match="Invalid signature"):
        verify_manifest(manifest, data)


def test_export_package_creation():
    """Test creating complete export package."""
    generator = ManifestGenerator()
    
    data = {
        "provider": "test",
        "conversations": [
            {"id": "1", "messages": [{"content": "Hello"}]}
        ]
    }
    
    package = create_export_package(data, "test", generator)
    
    assert "data" in package
    assert "manifest" in package
    assert package["data"] == data
    assert package["manifest"]["provider"] == "test"


def test_manifest_with_metadata():
    """Test manifest generation with metadata."""
    generator = ManifestGenerator()
    
    data = {"test": "data"}
    metadata = {"redacted": True, "version": "1.0"}
    
    manifest = generator.generate_manifest(data, "test", metadata)
    
    assert "metadata" in manifest
    assert manifest["metadata"]["redacted"] is True
    assert manifest["metadata"]["version"] == "1.0"
