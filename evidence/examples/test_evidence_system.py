#!/usr/bin/env python3
"""
Integration test for the evidence validation system
Tests all core functionality
"""

import json
import sys
import tempfile
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from evidence_logger import ConversationEvidenceLogger


def test_basic_logging():
    """Test basic conversation logging"""
    print("Test 1: Basic logging...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        logger = ConversationEvidenceLogger(base_dir=Path(tmpdir))
        
        entry = logger.log_conversation(
            share_url="https://claude.ai/share/test123",
            provider="anthropic",
            model="claude-3.5-sonnet",
            primary_topic="test",
            conclusion="Test conclusion"
        )
        
        assert entry['conversation_id']
        assert entry['ai_system']['provider'] == 'anthropic'
        assert entry['integration']['ledger_hash']
        assert entry['integration']['ledger_prev_hash'] is None  # First entry
        
    print("✅ Test 1 passed\n")


def test_chain_linking():
    """Test cryptographic chain linking"""
    print("Test 2: Chain linking...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        logger = ConversationEvidenceLogger(base_dir=Path(tmpdir))
        
        # Log first entry
        entry1 = logger.log_conversation(
            share_url="https://claude.ai/share/test1",
            model="claude-3.5",
            conclusion="First"
        )
        
        # Log second entry
        entry2 = logger.log_conversation(
            share_url="https://chatgpt.com/share/test2",
            model="gpt-4",
            conclusion="Second"
        )
        
        # Verify chain links
        assert entry1['integration']['ledger_prev_hash'] is None
        assert entry2['integration']['ledger_prev_hash'] == entry1['integration']['ledger_hash']
        
    print("✅ Test 2 passed\n")


def test_provider_detection():
    """Test automatic provider detection from URLs"""
    print("Test 3: Provider detection...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        logger = ConversationEvidenceLogger(base_dir=Path(tmpdir))
        
        test_cases = [
            ("https://claude.ai/share/abc", "anthropic"),
            ("https://chatgpt.com/share/def", "openai"),
            ("https://x.com/i/grok/share/ghi", "xai"),
            ("https://grok.x.ai/share/jkl", "xai"),
        ]
        
        for url, expected_provider in test_cases:
            entry = logger.log_conversation(
                share_url=url,
                model="test-model",
                conclusion="Test"
            )
            assert entry['ai_system']['provider'] == expected_provider, \
                f"Expected {expected_provider} for {url}, got {entry['ai_system']['provider']}"
        
    print("✅ Test 3 passed\n")


def test_chain_verification():
    """Test chain integrity verification"""
    print("Test 4: Chain verification...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        logger = ConversationEvidenceLogger(base_dir=Path(tmpdir))
        
        # Log multiple entries
        for i in range(5):
            logger.log_conversation(
                share_url=f"https://claude.ai/share/test{i}",
                model=f"model-{i}",
                conclusion=f"Test {i}"
            )
        
        # Verify chain
        is_valid = logger.verify_chain()
        assert is_valid, "Chain verification failed"
        
    print("✅ Test 4 passed\n")


def test_json_export():
    """Test JSON export functionality"""
    print("Test 5: JSON export...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        logger = ConversationEvidenceLogger(base_dir=Path(tmpdir))
        
        logger.log_conversation(
            share_url="https://claude.ai/share/export-test",
            model="claude-3.5",
            conclusion="Export test"
        )
        
        json_file = Path(tmpdir) / "test_export.json"
        logger.export_to_json(json_file)
        
        assert json_file.exists()
        
        with open(json_file) as f:
            data = json.load(f)
            assert 'conversations' in data
            assert len(data['conversations']) == 1
        
    print("✅ Test 5 passed\n")


def run_all_tests():
    """Run all tests"""
    print("="*60)
    print("Evidence Validation System - Integration Tests")
    print("="*60)
    print()
    
    tests = [
        test_basic_logging,
        test_chain_linking,
        test_provider_detection,
        test_chain_verification,
        test_json_export,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"❌ Test failed: {e}\n")
            failed += 1
        except Exception as e:
            print(f"❌ Test error: {e}\n")
            failed += 1
    
    print("="*60)
    print(f"Results: {passed} passed, {failed} failed")
    print("="*60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
