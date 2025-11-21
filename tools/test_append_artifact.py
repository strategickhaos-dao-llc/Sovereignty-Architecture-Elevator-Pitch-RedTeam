#!/usr/bin/env python3
"""
Test suite for append_artifact.py
"""

import json
import tempfile
from pathlib import Path
from datetime import datetime, timezone
import sys

# Import the module
from append_artifact import append_artifact


def test_append_artifact_basic():
    """Test basic artifact appending functionality"""
    print("🧪 Test: Basic artifact appending")
    
    # Create a temporary ledger file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.jsonl') as f:
        temp_ledger = Path(f.name)
    
    try:
        # Append an artifact
        source = "https://example.com/test"
        summary = "Test artifact for validation"
        append_artifact(source, summary, ledger_path=temp_ledger)
        
        # Verify the entry
        with temp_ledger.open('r') as f:
            lines = f.readlines()
            assert len(lines) == 1, "Expected exactly one entry"
            
            entry = json.loads(lines[0])
            assert entry['source'] == source, f"Source mismatch: {entry['source']}"
            assert entry['summary'] == summary, f"Summary mismatch: {entry['summary']}"
            assert entry['type'] == "external_ai_discussion", f"Type mismatch: {entry['type']}"
            assert 'timestamp' in entry, "Missing timestamp"
            
            # Verify timestamp format
            timestamp = datetime.fromisoformat(entry['timestamp'].replace('Z', '+00:00'))
            assert timestamp.tzinfo is not None, "Timestamp should be timezone-aware"
        
        print("✅ Test passed: Basic artifact appending")
        return True
        
    finally:
        # Cleanup
        if temp_ledger.exists():
            temp_ledger.unlink()


def test_append_multiple_artifacts():
    """Test appending multiple artifacts"""
    print("🧪 Test: Multiple artifact appending")
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.jsonl') as f:
        temp_ledger = Path(f.name)
    
    try:
        # Append multiple artifacts
        artifacts = [
            ("https://example.com/test1", "First test artifact"),
            ("https://example.com/test2", "Second test artifact"),
            ("https://example.com/test3", "Third test artifact"),
        ]
        
        for source, summary in artifacts:
            append_artifact(source, summary, ledger_path=temp_ledger)
        
        # Verify all entries
        with temp_ledger.open('r') as f:
            lines = f.readlines()
            assert len(lines) == 3, f"Expected 3 entries, got {len(lines)}"
            
            for i, line in enumerate(lines):
                entry = json.loads(line)
                expected_source, expected_summary = artifacts[i]
                assert entry['source'] == expected_source
                assert entry['summary'] == expected_summary
        
        print("✅ Test passed: Multiple artifact appending")
        return True
        
    finally:
        if temp_ledger.exists():
            temp_ledger.unlink()


def test_custom_artifact_type():
    """Test appending with custom artifact type"""
    print("🧪 Test: Custom artifact type")
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.jsonl') as f:
        temp_ledger = Path(f.name)
    
    try:
        source = "https://example.com/doc"
        summary = "Custom type artifact"
        custom_type = "documentation"
        
        append_artifact(source, summary, artifact_type=custom_type, ledger_path=temp_ledger)
        
        with temp_ledger.open('r') as f:
            entry = json.loads(f.read())
            assert entry['type'] == custom_type, f"Type mismatch: {entry['type']}"
        
        print("✅ Test passed: Custom artifact type")
        return True
        
    finally:
        if temp_ledger.exists():
            temp_ledger.unlink()


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("Running append_artifact.py test suite")
    print("="*60 + "\n")
    
    tests = [
        test_append_artifact_basic,
        test_append_multiple_artifacts,
        test_custom_artifact_type,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed: {test.__name__}")
            print(f"   Error: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("="*60 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
