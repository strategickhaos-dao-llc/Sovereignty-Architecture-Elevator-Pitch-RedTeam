#!/usr/bin/env python3
"""
test_anchoring.py - Tests for evidence anchoring functionality

Tests the anchor_ledger.py and evidence_logger.py modules without requiring
actual GPG keys or OpenTimestamps to be installed. These are integration
tests that can be run with actual tools installed.

Usage:
    python tools/test_anchoring.py

Author: Strategickhaos
Version: 1.0.0
"""

import sys
import unittest
import tempfile
import yaml
from pathlib import Path
from datetime import datetime

# Add tools directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Import the modules to test
try:
    from evidence_logger import EvidenceLogger
except ImportError as e:
    print(f"Warning: Could not import evidence_logger: {e}")
    EvidenceLogger = None


class TestSchemaStructure(unittest.TestCase):
    """Test the conversation evidence schema structure."""
    
    def setUp(self):
        """Load the schema."""
        schema_path = Path(__file__).parent.parent / "schemas" / "conversation_evidence.v1.2.0.yaml"
        with open(schema_path, 'r') as f:
            self.schema = yaml.safe_load(f)
    
    def test_schema_version(self):
        """Test that schema has correct version."""
        self.assertEqual(self.schema['schema_version'], "1.2.0")
    
    def test_schema_has_required_sections(self):
        """Test that schema defines all required sections."""
        # Schema should document these sections
        schema_content = Path(__file__).parent.parent / "schemas" / "conversation_evidence.v1.2.0.yaml"
        content = schema_content.read_text()
        
        required_sections = [
            'metadata:',
            'conversation:',
            'evidence:',
            'integration:',
            'gpg_signature:',
            'opentimestamps:',
            'provenance:',
            'verification:',
            'compliance:'
        ]
        
        for section in required_sections:
            self.assertIn(section, content, f"Schema should document {section}")
    
    def test_opentimestamps_fields(self):
        """Test that schema documents OpenTimestamps fields."""
        schema_content = Path(__file__).parent.parent / "schemas" / "conversation_evidence.v1.2.0.yaml"
        content = schema_content.read_text()
        
        ots_fields = [
            'stamp_file:',
            'stamp_hash:',
            'bitcoin_txid:',
            'status:'
        ]
        
        for field in ots_fields:
            self.assertIn(field, content, f"Schema should document OpenTimestamps field {field}")


class TestEvidenceLogger(unittest.TestCase):
    """Test the EvidenceLogger class (without actual GPG/OTS)."""
    
    def setUp(self):
        """Create a temporary directory for testing."""
        self.temp_dir = tempfile.mkdtemp()
        if EvidenceLogger:
            self.logger = EvidenceLogger(
                evidence_dir=self.temp_dir,
                auto_anchor=False  # Disable anchoring for unit tests
            )
    
    def tearDown(self):
        """Clean up temporary directory."""
        import shutil
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)
    
    @unittest.skipIf(EvidenceLogger is None, "EvidenceLogger not available")
    def test_logger_initialization(self):
        """Test that logger initializes correctly."""
        self.assertIsNotNone(self.logger)
        self.assertTrue(Path(self.temp_dir).exists())
        self.assertTrue((Path(self.temp_dir) / "anchored").exists())
    
    @unittest.skipIf(EvidenceLogger is None, "EvidenceLogger not available")
    def test_log_conversation(self):
        """Test logging a conversation (without anchoring)."""
        conv_id = f"test-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        result = self.logger.log_conversation(
            conversation_id=conv_id,
            messages=[
                {
                    "message_id": "msg-001",
                    "sender": "Alice",
                    "timestamp": self.logger._generate_timestamp(),
                    "content": "Test message",
                    "attachments": []
                }
            ],
            participants=["Alice", "Bob"],
            platform="Discord",
            channel="#test",
            evidence_type="conversation",
            category="test",
            tags=["test"]
        )
        
        self.assertIsNotNone(result)
        self.assertEqual(result['conversation_id'], conv_id)
        self.assertFalse(result['anchored'])  # Should not be anchored
        
        # Verify file was created
        entry_file = Path(self.temp_dir) / f"{conv_id}.yaml"
        self.assertTrue(entry_file.exists())
        
        # Verify content is valid YAML
        with open(entry_file, 'r') as f:
            data = yaml.safe_load(f)
            self.assertEqual(data['metadata']['conversation_id'], conv_id)
            self.assertEqual(data['schema_version'], "1.2.0")
    
    @unittest.skipIf(EvidenceLogger is None, "EvidenceLogger not available")
    def test_list_evidence(self):
        """Test listing evidence entries."""
        # Create a test entry
        conv_id = f"test-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        self.logger.log_conversation(
            conversation_id=conv_id,
            messages=[{"message_id": "1", "sender": "A", "timestamp": self.logger._generate_timestamp(), "content": "test", "attachments": []}],
            participants=["A"],
            platform="Test"
        )
        
        # List evidence
        entries = self.logger.list_evidence()
        self.assertIn(conv_id, entries)
    
    @unittest.skipIf(EvidenceLogger is None, "EvidenceLogger not available")
    def test_hash_generation(self):
        """Test SHA256 hash generation."""
        test_content = "test content"
        hash1 = self.logger._hash_content(test_content)
        hash2 = self.logger._hash_content(test_content)
        
        # Same content should produce same hash
        self.assertEqual(hash1, hash2)
        
        # Different content should produce different hash
        hash3 = self.logger._hash_content("different content")
        self.assertNotEqual(hash1, hash3)
        
        # Hash should be 64 characters (256 bits in hex)
        self.assertEqual(len(hash1), 64)
    
    @unittest.skipIf(EvidenceLogger is None, "EvidenceLogger not available")
    def test_timestamp_format(self):
        """Test timestamp generation."""
        timestamp = self.logger._generate_timestamp()
        
        # Should be ISO8601 format
        self.assertIn('T', timestamp)
        self.assertTrue(timestamp.endswith('Z') or '+' in timestamp or timestamp.endswith('+00:00'))


class TestExampleEvidence(unittest.TestCase):
    """Test the example evidence file."""
    
    def test_example_is_valid_yaml(self):
        """Test that example evidence file is valid YAML."""
        example_path = Path(__file__).parent.parent / "evidence" / "example-conversation.yaml"
        
        with open(example_path, 'r') as f:
            data = yaml.safe_load(f)
        
        self.assertIsNotNone(data)
        self.assertEqual(data['schema_version'], "1.2.0")
    
    def test_example_has_required_fields(self):
        """Test that example has all required fields."""
        example_path = Path(__file__).parent.parent / "evidence" / "example-conversation.yaml"
        
        with open(example_path, 'r') as f:
            data = yaml.safe_load(f)
        
        # Check required top-level keys
        required_keys = ['metadata', 'conversation', 'evidence', 'integration', 'provenance', 'compliance']
        for key in required_keys:
            self.assertIn(key, data, f"Example should have {key}")
        
        # Check integration has new fields
        self.assertIn('gpg_signature', data['integration'])
        self.assertIn('opentimestamps', data['integration'])
        
        # Check OpenTimestamps structure
        ots = data['integration']['opentimestamps']
        self.assertIn('stamp_file', ots)
        self.assertIn('stamp_hash', ots)
        self.assertIn('status', ots)


class TestFileStructure(unittest.TestCase):
    """Test that all required files exist."""
    
    def test_schema_exists(self):
        """Test that schema file exists."""
        schema_path = Path(__file__).parent.parent / "schemas" / "conversation_evidence.v1.2.0.yaml"
        self.assertTrue(schema_path.exists(), "Schema file should exist")
    
    def test_anchor_script_exists(self):
        """Test that anchor_ledger.py exists."""
        script_path = Path(__file__).parent / "anchor_ledger.py"
        self.assertTrue(script_path.exists(), "anchor_ledger.py should exist")
        
        # Check it's executable
        import stat
        mode = script_path.stat().st_mode
        self.assertTrue(mode & stat.S_IXUSR, "anchor_ledger.py should be executable")
    
    def test_evidence_logger_exists(self):
        """Test that evidence_logger.py exists."""
        script_path = Path(__file__).parent / "evidence_logger.py"
        self.assertTrue(script_path.exists(), "evidence_logger.py should exist")
        
        # Check it's executable
        import stat
        mode = script_path.stat().st_mode
        self.assertTrue(mode & stat.S_IXUSR, "evidence_logger.py should be executable")
    
    def test_readme_exists(self):
        """Test that README.md exists."""
        readme_path = Path(__file__).parent / "README.md"
        self.assertTrue(readme_path.exists(), "README.md should exist")
        
        # Check it has content
        content = readme_path.read_text()
        self.assertGreater(len(content), 1000, "README should have substantial content")
        self.assertIn("OpenTimestamps", content, "README should mention OpenTimestamps")
        self.assertIn("GPG", content, "README should mention GPG")
    
    def test_example_evidence_exists(self):
        """Test that example evidence file exists."""
        example_path = Path(__file__).parent.parent / "evidence" / "example-conversation.yaml"
        self.assertTrue(example_path.exists(), "Example evidence file should exist")
    
    def test_gitignore_updated(self):
        """Test that .gitignore was updated."""
        gitignore_path = Path(__file__).parent.parent / ".gitignore"
        content = gitignore_path.read_text()
        
        self.assertIn("*.ots", content, ".gitignore should exclude .ots files")
        self.assertIn("*.asc", content, ".gitignore should exclude .asc files")


def run_tests():
    """Run all tests."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestSchemaStructure))
    suite.addTests(loader.loadTestsFromTestCase(TestEvidenceLogger))
    suite.addTests(loader.loadTestsFromTestCase(TestExampleEvidence))
    suite.addTests(loader.loadTestsFromTestCase(TestFileStructure))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())
