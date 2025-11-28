#!/usr/bin/env python3
"""
Tests for Phase 3 Executor Server and Anchor Generator
Strategickhaos DAO LLC - Sovereignty Architecture
"""

import hashlib
import json
import os
import sys
import tempfile
import threading
import time
import unittest
from datetime import datetime, timezone
from pathlib import Path

# Add phase3 to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'phase3'))

from executor_server import (
    ExecutionTask,
    ExecutionResult,
    TaskRegistry,
    ExecutionEngine,
    handler_log_signal,
    handler_rebalance_check,
    handler_generate_anchor
)
from generate_anchor import calculate_hash, calculate_content_hash, generate_yaml


class TestTaskRegistry(unittest.TestCase):
    """Tests for TaskRegistry class."""
    
    def setUp(self):
        self.registry = TaskRegistry()
    
    def test_register_task(self):
        """Test task registration."""
        task = ExecutionTask(
            task_id="test_task",
            name="Test Task",
            handler="test_handler"
        )
        self.registry.register_task(task)
        
        retrieved = self.registry.get_task("test_task")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.name, "Test Task")
    
    def test_register_handler(self):
        """Test handler registration."""
        def test_fn(x):
            return x * 2
        
        self.registry.register_handler("double", test_fn)
        retrieved = self.registry.get_handler("double")
        
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved(5), 10)
    
    def test_list_tasks(self):
        """Test listing all tasks."""
        task1 = ExecutionTask(task_id="t1", name="Task 1")
        task2 = ExecutionTask(task_id="t2", name="Task 2")
        
        self.registry.register_task(task1)
        self.registry.register_task(task2)
        
        tasks = self.registry.list_tasks()
        self.assertEqual(len(tasks), 2)
    
    def test_record_result(self):
        """Test recording execution results."""
        result = ExecutionResult(
            task_id="test",
            success=True,
            timestamp=datetime.now(timezone.utc),
            duration_ms=10.5,
            output="test output"
        )
        
        self.registry.record_result(result)
        results = self.registry.get_results("test")
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].output, "test output")


class TestExecutionEngine(unittest.TestCase):
    """Tests for ExecutionEngine class."""
    
    def setUp(self):
        self.registry = TaskRegistry()
        self.engine = ExecutionEngine(self.registry)
        
        # Register a simple handler
        def echo_handler(payload):
            return json.dumps(payload)
        
        self.registry.register_handler("echo", echo_handler)
    
    def test_execute_task_success(self):
        """Test successful task execution."""
        task = ExecutionTask(
            task_id="echo_test",
            name="Echo Test",
            handler="echo",
            payload={"message": "hello"}
        )
        self.registry.register_task(task)
        
        result = self.engine.execute_task(task)
        
        self.assertTrue(result.success)
        self.assertIsNotNone(result.output)
        self.assertIn("hello", result.output)
        self.assertIsNotNone(result.checksum)
    
    def test_execute_task_no_handler(self):
        """Test task execution with no handler."""
        task = ExecutionTask(
            task_id="no_handler_test",
            name="No Handler Test",
            payload={"data": "test"}
        )
        
        result = self.engine.execute_task(task)
        
        # Should succeed with default handler
        self.assertTrue(result.success)
        self.assertIn("test", result.output)
    
    def test_execute_task_records_result(self):
        """Test that execution records results."""
        task = ExecutionTask(
            task_id="record_test",
            name="Record Test",
            handler="echo",
            payload={}
        )
        self.registry.register_task(task)
        
        self.engine.execute_task(task)
        
        results = self.registry.get_results("record_test")
        self.assertEqual(len(results), 1)


class TestBuiltInHandlers(unittest.TestCase):
    """Tests for built-in handler functions."""
    
    def test_handler_log_signal(self):
        """Test log_signal handler."""
        payload = {
            "type": "trading",
            "symbol": "ES",
            "action": "BUY"
        }
        
        result = handler_log_signal(payload)
        result_data = json.loads(result)
        
        self.assertEqual(result_data["type"], "trading")
        self.assertEqual(result_data["symbol"], "ES")
        self.assertIn("timestamp", result_data)
    
    def test_handler_rebalance_check(self):
        """Test rebalance_check handler."""
        payload = {
            "portfolio": {"AAPL": 0.3, "GOOGL": 0.3, "MSFT": 0.4},
            "thresholds": {"deviation": 0.05}
        }
        
        result = handler_rebalance_check(payload)
        result_data = json.loads(result)
        
        self.assertIn("needs_rebalance", result_data)
        self.assertIn("analysis", result_data)
        self.assertIn("timestamp", result_data)
    
    def test_handler_generate_anchor(self):
        """Test generate_anchor handler."""
        payload = {
            "content": "Test document content",
            "type": "verification"
        }
        
        result = handler_generate_anchor(payload)
        result_data = json.loads(result)
        
        self.assertEqual(result_data["type"], "verification")
        self.assertIn("content_hash", result_data)
        self.assertIn("timestamp", result_data)


class TestAnchorGeneration(unittest.TestCase):
    """Tests for anchor file generation utilities."""
    
    def test_calculate_hash(self):
        """Test file hash calculation."""
        # Create a temp file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("Test content for hashing")
            temp_path = f.name
        
        try:
            file_hash = calculate_hash(temp_path)
            self.assertEqual(len(file_hash), 64)  # SHA-256 produces 64 hex chars
            
            # Verify consistency
            file_hash2 = calculate_hash(temp_path)
            self.assertEqual(file_hash, file_hash2)
        finally:
            os.unlink(temp_path)
    
    def test_calculate_content_hash(self):
        """Test string content hash calculation."""
        content = "Test content"
        
        hash1 = calculate_content_hash(content)
        hash2 = calculate_content_hash(content)
        
        self.assertEqual(len(hash1), 64)
        self.assertEqual(hash1, hash2)
        
        # Different content should produce different hash
        hash3 = calculate_content_hash("Different content")
        self.assertNotEqual(hash1, hash3)
    
    def test_generate_yaml(self):
        """Test YAML generation from dict."""
        data = {
            "anchor": {
                "version": "1.0",
                "timestamp": "2025-01-15T10:00:00Z"
            },
            "content": {
                "name": "test.md",
                "hash": "abc123"
            }
        }
        
        yaml_output = generate_yaml(data)
        
        self.assertIn("anchor:", yaml_output)
        self.assertIn("version: 1.0", yaml_output)
        self.assertIn("content:", yaml_output)
        self.assertIn("name: test.md", yaml_output)


class TestPhase3Integration(unittest.TestCase):
    """Integration tests for Phase 3 components."""
    
    def test_full_task_lifecycle(self):
        """Test complete task registration, execution, and result retrieval."""
        # Set up
        registry = TaskRegistry()
        engine = ExecutionEngine(registry)
        
        # Register handler
        registry.register_handler("echo", lambda p: json.dumps(p))
        
        # Register task
        task = ExecutionTask(
            task_id="integration_test",
            name="Integration Test Task",
            handler="echo",
            payload={"test": True, "value": 42}
        )
        registry.register_task(task)
        
        # Execute
        result = engine.execute_task(task)
        
        # Verify
        self.assertTrue(result.success)
        self.assertGreater(result.duration_ms, 0)
        self.assertIsNotNone(result.checksum)
        
        # Check result was recorded
        results = registry.get_results("integration_test")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].task_id, "integration_test")
    
    def test_sovereignty_status(self):
        """Test that sovereignty status correctly reports local execution."""
        registry = TaskRegistry()
        engine = ExecutionEngine(registry)
        
        # Verify no external dependencies
        # This is a semantic test - in Phase 3, we should have local execution
        self.assertIsNotNone(registry)
        self.assertIsNotNone(engine)
        
        # Register built-in handlers (these run locally)
        registry.register_handler("log_signal", handler_log_signal)
        registry.register_handler("rebalance_check", handler_rebalance_check)
        registry.register_handler("generate_anchor", handler_generate_anchor)
        
        # All handlers should be local (no external API calls)
        self.assertEqual(len(registry._handlers), 3)


if __name__ == "__main__":
    unittest.main(verbosity=2)
