#!/usr/bin/env python3
"""
Test Script for Evidence Anchoring System
Strategickhaos DAO LLC

Tests the evidence logging system without requiring GPG/OTS installation.
This validates the core logic and data structures.
"""

import sys
import tempfile
import yaml
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from evidence_logger import EvidenceLogger


def test_schema_loading():
    """Test that the schema can be loaded and is valid."""
    print("🔍 Test 1: Schema Loading")
    schema_path = Path(__file__).parent.parent / "evidence/schemas/conversation_evidence.v1.2.0.yaml"
    
    try:
        with open(schema_path, 'r') as f:
            schema = yaml.safe_load(f)
        
        # Validate required fields
        assert "schema_version" in schema
        assert "metadata" in schema
        assert "conversation" in schema
        assert "evidence" in schema
        assert "integration" in schema
        assert "opentimestamps" in schema["integration"]
        assert "gpg_signature" in schema["integration"]
        
        print(f"   ✅ Schema loaded successfully: v{schema['schema_version']}")
        print(f"   ✅ Required fields present")
        return True
    except Exception as e:
        print(f"   ❌ Schema loading failed: {e}")
        return False


def test_evidence_logger_initialization():
    """Test that EvidenceLogger can be initialized."""
    print("\n🔍 Test 2: Evidence Logger Initialization")
    
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            logger = EvidenceLogger(
                evidence_dir=tmpdir,
                gpg_key="test@example.com",
                operator="Test User"
            )
            
            assert logger.operator == "Test User"
            assert logger.gpg_key == "test@example.com"
            assert Path(tmpdir).exists()
            
            print("   ✅ Logger initialized successfully")
            print(f"   ✅ Evidence directory created: {tmpdir}")
            return True
    except Exception as e:
        print(f"   ❌ Logger initialization failed: {e}")
        return False


def test_conversation_logging():
    """Test logging a conversation without anchoring."""
    print("\n🔍 Test 3: Conversation Logging (without anchoring)")
    
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            logger = EvidenceLogger(
                evidence_dir=tmpdir,
                gpg_key="test@example.com",
                operator="Test User"
            )
            
            # Log without auto_anchor to avoid requiring GPG/OTS
            result = logger.log_conversation(
                conversation_id="test_conv_001",
                participants=[
                    {"name": "Test User", "role": "operator"},
                    {"name": "AI System", "role": "assistant"}
                ],
                transcript="This is a test conversation.",
                context="Unit testing",
                summary="Test conversation for validation",
                auto_anchor=False  # Skip anchoring for this test
            )
            
            assert result["success"] == True
            assert result["conversation_id"] == "test_conv_001"
            assert "sha256" in result
            assert "file_path" in result
            
            # Verify file was created
            file_path = Path(result["file_path"])
            assert file_path.exists()
            
            # Verify content is valid YAML
            with open(file_path, 'r') as f:
                content = yaml.safe_load(f)
            
            assert content["metadata"]["conversation_id"] == "test_conv_001"
            assert content["conversation"]["participants"][0]["name"] == "Test User"
            assert content["evidence"]["transcript"] == "This is a test conversation."
            
            print(f"   ✅ Conversation logged successfully")
            print(f"   ✅ File created: {file_path.name}")
            print(f"   ✅ SHA256: {result['sha256'][:16]}...")
            print(f"   ✅ YAML structure valid")
            return True
    except Exception as e:
        print(f"   ❌ Conversation logging failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_hash_calculation():
    """Test SHA256 hash calculation."""
    print("\n🔍 Test 4: Hash Calculation")
    
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            logger = EvidenceLogger(evidence_dir=tmpdir)
            
            test_content = "Test content for hashing"
            hash_result = logger._calculate_hash(test_content)
            
            # Hash should be 64 characters (256 bits in hex)
            assert len(hash_result) == 64
            assert all(c in "0123456789abcdef" for c in hash_result)
            
            # Same content should produce same hash
            hash_result2 = logger._calculate_hash(test_content)
            assert hash_result == hash_result2
            
            print(f"   ✅ Hash calculation working")
            print(f"   ✅ Hash format valid: {hash_result[:16]}...")
            print(f"   ✅ Hash consistency verified")
            return True
    except Exception as e:
        print(f"   ❌ Hash calculation failed: {e}")
        return False


def test_yaml_structure():
    """Test that generated YAML matches schema structure."""
    print("\n🔍 Test 5: YAML Structure Validation")
    
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            logger = EvidenceLogger(evidence_dir=tmpdir)
            
            result = logger.log_conversation(
                conversation_id="test_structure",
                participants=[{"name": "Test", "role": "tester"}],
                transcript="Structure test",
                context="Validation",
                summary="Testing YAML structure",
                attachments=["file1.pdf", "file2.pdf"],
                related_documents=["doc1.yaml"],
                auto_anchor=False
            )
            
            # Load and validate structure
            with open(result["file_path"], 'r') as f:
                content = yaml.safe_load(f)
            
            # Check all major sections
            required_sections = [
                "schema_version",
                "schema_type",
                "metadata",
                "conversation",
                "evidence",
                "integration",
                "attestation",
                "audit"
            ]
            
            for section in required_sections:
                assert section in content, f"Missing section: {section}"
            
            # Check nested structures
            assert "opentimestamps" in content["integration"]
            assert "gpg_signature" in content["integration"]
            assert "participants" in content["conversation"]
            assert "transcript" in content["evidence"]
            assert "sha256_hash" in content["evidence"]
            
            # Check arrays were populated
            assert len(content["evidence"]["attachments"]) == 2
            assert len(content["evidence"]["related_documents"]) == 1
            
            print(f"   ✅ All required sections present")
            print(f"   ✅ Nested structures valid")
            print(f"   ✅ Arrays populated correctly")
            return True
    except Exception as e:
        print(f"   ❌ YAML structure validation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all tests and report results."""
    print("=" * 60)
    print("Evidence Anchoring System - Test Suite")
    print("=" * 60)
    
    tests = [
        test_schema_loading,
        test_evidence_logger_initialization,
        test_conversation_logging,
        test_hash_calculation,
        test_yaml_structure
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"❌ Test crashed: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("✅ All tests passed!")
        return 0
    else:
        print(f"❌ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
