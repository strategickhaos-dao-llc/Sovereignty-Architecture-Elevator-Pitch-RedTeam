"""
Tests for Sovereignty Protocol
"""

import unittest
from flamelang.core.sovereignty import (
    NetworkIsolation, CoherenceMonitor, BoundaryHardening, 
    AuditTrail, SovereigntyProtocol
)


class TestNetworkIsolation(unittest.TestCase):
    
    def test_blocks_analytics_domains(self):
        """Test that analytics domains are blocked"""
        isolation = NetworkIsolation()
        
        self.assertFalse(isolation.is_domain_allowed("analytics.google.com"))
        self.assertFalse(isolation.is_domain_allowed("tracking.example.com"))
        self.assertFalse(isolation.is_domain_allowed("telemetry.microsoft.com"))
    
    def test_blocks_aws_domains(self):
        """Test that AWS domains are blocked"""
        isolation = NetworkIsolation()
        
        self.assertFalse(isolation.is_domain_allowed("ec2.amazonaws.com"))
        self.assertFalse(isolation.is_domain_allowed("s3.amazonaws.com"))
    
    def test_default_block_all_policy(self):
        """Test that default policy blocks all"""
        isolation = NetworkIsolation()
        
        self.assertFalse(isolation.is_domain_allowed("example.com"))
        self.assertFalse(isolation.is_domain_allowed("safe-site.org"))
    
    def test_tracks_blocked_attempts(self):
        """Test that blocked attempts are tracked"""
        isolation = NetworkIsolation()
        
        isolation.is_domain_allowed("analytics.google.com")
        isolation.is_domain_allowed("tracking.example.com")
        
        attempts = isolation.get_blocked_attempts()
        self.assertEqual(len(attempts), 2)


class TestCoherenceMonitor(unittest.TestCase):
    
    def test_capture_metrics(self):
        """Test capturing process metrics"""
        monitor = CoherenceMonitor()
        metrics = monitor.capture_metrics()
        
        self.assertIsNotNone(metrics)
        self.assertGreater(metrics.memory_usage, 0)
        self.assertGreaterEqual(metrics.thread_count, 0)
        self.assertGreaterEqual(metrics.open_connections, 0)
        self.assertGreaterEqual(metrics.cpu_percent, 0)
    
    def test_set_baseline(self):
        """Test setting baseline metrics"""
        monitor = CoherenceMonitor()
        monitor.set_baseline()
        
        self.assertIsNotNone(monitor.baseline_metrics)
    
    def test_check_coherence(self):
        """Test coherence checking"""
        monitor = CoherenceMonitor()
        result = monitor.check_coherence()
        
        self.assertIn("status", result)
        self.assertIn("metrics", result)
        self.assertIn("anomalies", result)
        
        # First check should set baseline
        self.assertEqual(result["status"], "baseline_set")


class TestBoundaryHardening(unittest.TestCase):
    
    def test_hash_data(self):
        """Test SHA3-512 hashing"""
        hardening = BoundaryHardening()
        
        data = b"test data"
        hash1 = hardening.hash_data(data)
        hash2 = hardening.hash_data(data)
        
        # Same data should produce same hash
        self.assertEqual(hash1, hash2)
        
        # Hash should be 128 hex characters (512 bits / 4)
        self.assertEqual(len(hash1), 128)
    
    def test_create_boundary(self):
        """Test creating cryptographic boundary"""
        hardening = BoundaryHardening()
        
        boundary = hardening.create_boundary("sensitive data")
        
        self.assertIn("hash", boundary)
        self.assertIn("algorithm", boundary)
        self.assertIn("data_size", boundary)
        self.assertIn("timestamp", boundary)
        self.assertEqual(boundary["algorithm"], "SHA3-512")
    
    def test_verify_boundary(self):
        """Test verifying data integrity"""
        hardening = BoundaryHardening()
        
        data = "test data"
        boundary = hardening.create_boundary(data)
        
        # Should verify successfully
        self.assertTrue(hardening.verify_boundary(data, boundary["hash"]))
        
        # Should fail with different data
        self.assertFalse(hardening.verify_boundary("different data", boundary["hash"]))


class TestAuditTrail(unittest.TestCase):
    
    def test_log_event(self):
        """Test logging security events"""
        audit = AuditTrail()
        
        event = audit.log_event(
            "test_event",
            "INFO",
            {"detail": "test detail"}
        )
        
        self.assertIsNotNone(event)
        self.assertEqual(event.event_type, "test_event")
        self.assertEqual(event.severity, "INFO")
        self.assertIn("detail", event.details)
    
    def test_get_events(self):
        """Test retrieving events"""
        audit = AuditTrail()
        
        audit.log_event("event1", "INFO", {})
        audit.log_event("event2", "WARNING", {})
        audit.log_event("event1", "CRITICAL", {})
        
        # Get all events
        all_events = audit.get_events()
        self.assertEqual(len(all_events), 3)
        
        # Filter by type
        type_events = audit.get_events(event_type="event1")
        self.assertEqual(len(type_events), 2)
        
        # Filter by severity
        warning_events = audit.get_events(severity="WARNING")
        self.assertEqual(len(warning_events), 1)


class TestSovereigntyProtocol(unittest.TestCase):
    
    def test_initialization(self):
        """Test sovereignty protocol initialization"""
        protocol = SovereigntyProtocol()
        
        self.assertIsNotNone(protocol.network_isolation)
        self.assertIsNotNone(protocol.coherence_monitor)
        self.assertIsNotNone(protocol.boundary_hardening)
        self.assertIsNotNone(protocol.audit_trail)
    
    def test_check_network_access(self):
        """Test network access checking"""
        protocol = SovereigntyProtocol()
        
        result = protocol.check_network_access("analytics.google.com")
        self.assertFalse(result)
        
        # Should log to audit trail
        summary = protocol.get_audit_summary()
        self.assertGreater(summary["total_events"], 0)
    
    def test_monitor_coherence(self):
        """Test coherence monitoring"""
        protocol = SovereigntyProtocol()
        
        result = protocol.monitor_coherence()
        self.assertIn("status", result)
    
    def test_protect_data(self):
        """Test data protection"""
        protocol = SovereigntyProtocol()
        
        boundary = protocol.protect_data("sensitive data")
        self.assertIn("hash", boundary)
        
        # Should log to audit trail
        summary = protocol.get_audit_summary()
        self.assertIn("boundary_created", summary["by_type"])
    
    def test_audit_summary(self):
        """Test audit summary generation"""
        protocol = SovereigntyProtocol()
        
        protocol.check_network_access("test.com")
        protocol.protect_data("data")
        
        summary = protocol.get_audit_summary()
        
        self.assertIn("total_events", summary)
        self.assertIn("by_severity", summary)
        self.assertIn("by_type", summary)
        self.assertGreater(summary["total_events"], 0)


if __name__ == '__main__':
    unittest.main()
