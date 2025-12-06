"""
FlameLang Sovereignty Protocol
Network isolation, coherence monitoring, boundary hardening, and audit logging
"""

import hashlib
import json
import time
import psutil
import socket
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class NetworkIsolationConfig:
    """Configuration for network isolation"""
    blocked_domains: List[str]
    blocked_patterns: List[str]
    default_policy: str = "BLOCK_ALL"


@dataclass
class ProcessMetrics:
    """Metrics for process analysis"""
    memory_usage: float  # MB
    thread_count: int
    open_connections: int
    cpu_percent: float


@dataclass
class SecurityEvent:
    """Security event for audit trail"""
    timestamp: str
    event_type: str
    severity: str
    details: Dict[str, Any]
    hash: str


class NetworkIsolation:
    """
    Network Isolation component
    Blocks telemetry and unwanted network access
    """
    
    DEFAULT_BLOCKED_DOMAINS = [
        "*.amazonaws.com",
        "analytics.*",
        "telemetry.*",
        "tracking.*",
        "ads.*",
        "metrics.*"
    ]
    
    def __init__(self, config: Optional[NetworkIsolationConfig] = None):
        if config is None:
            config = NetworkIsolationConfig(
                blocked_domains=self.DEFAULT_BLOCKED_DOMAINS,
                blocked_patterns=["telemetry", "analytics", "tracking"],
                default_policy="BLOCK_ALL"
            )
        self.config = config
        self.blocked_attempts = []
    
    def is_domain_allowed(self, domain: str) -> bool:
        """Check if a domain is allowed"""
        domain_lower = domain.lower()
        
        # Check blocked patterns
        for pattern in self.config.blocked_patterns:
            if pattern in domain_lower:
                self.blocked_attempts.append({
                    "domain": domain,
                    "reason": f"Pattern match: {pattern}",
                    "timestamp": datetime.now().isoformat()
                })
                return False
        
        # Check blocked domains (with wildcard support)
        for blocked in self.config.blocked_domains:
            if blocked.startswith("*."):
                suffix = blocked[2:]
                if domain_lower.endswith(suffix):
                    self.blocked_attempts.append({
                        "domain": domain,
                        "reason": f"Domain match: {blocked}",
                        "timestamp": datetime.now().isoformat()
                    })
                    return False
            elif blocked == domain_lower:
                self.blocked_attempts.append({
                    "domain": domain,
                    "reason": f"Exact match: {blocked}",
                    "timestamp": datetime.now().isoformat()
                })
                return False
        
        # Default policy
        if self.config.default_policy == "BLOCK_ALL":
            self.blocked_attempts.append({
                "domain": domain,
                "reason": "Default policy: BLOCK_ALL",
                "timestamp": datetime.now().isoformat()
            })
            return False
        
        return True
    
    def get_blocked_attempts(self) -> List[Dict[str, Any]]:
        """Get list of blocked network attempts"""
        return self.blocked_attempts


class CoherenceMonitor:
    """
    Coherence Monitoring component
    Analyzes process memory, threads, connections, and file integrity
    """
    
    def __init__(self):
        self.baseline_metrics: Optional[ProcessMetrics] = None
    
    def capture_metrics(self) -> ProcessMetrics:
        """Capture current process metrics"""
        process = psutil.Process()
        
        # Memory usage in MB
        memory_info = process.memory_info()
        memory_mb = memory_info.rss / (1024 * 1024)
        
        # Thread count
        thread_count = process.num_threads()
        
        # Open connections
        try:
            connections = process.connections()
            connection_count = len(connections)
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            connection_count = 0
        
        # CPU percentage
        cpu_percent = process.cpu_percent(interval=0.1)
        
        return ProcessMetrics(
            memory_usage=memory_mb,
            thread_count=thread_count,
            open_connections=connection_count,
            cpu_percent=cpu_percent
        )
    
    def set_baseline(self):
        """Set baseline metrics for comparison"""
        self.baseline_metrics = self.capture_metrics()
    
    def check_coherence(self, threshold_multiplier: float = 2.0) -> Dict[str, Any]:
        """
        Check process coherence against baseline
        
        Args:
            threshold_multiplier: Alert if metrics exceed baseline by this factor
            
        Returns:
            Dictionary with coherence status and anomalies
        """
        current = self.capture_metrics()
        
        if self.baseline_metrics is None:
            self.set_baseline()
            return {
                "status": "baseline_set",
                "metrics": asdict(current),
                "anomalies": []
            }
        
        anomalies = []
        
        # Check memory
        if current.memory_usage > self.baseline_metrics.memory_usage * threshold_multiplier:
            anomalies.append({
                "type": "memory",
                "baseline": self.baseline_metrics.memory_usage,
                "current": current.memory_usage,
                "factor": current.memory_usage / self.baseline_metrics.memory_usage
            })
        
        # Check threads
        if current.thread_count > self.baseline_metrics.thread_count * threshold_multiplier:
            anomalies.append({
                "type": "threads",
                "baseline": self.baseline_metrics.thread_count,
                "current": current.thread_count,
                "factor": current.thread_count / self.baseline_metrics.thread_count
            })
        
        # Check connections
        if current.open_connections > self.baseline_metrics.open_connections * threshold_multiplier:
            anomalies.append({
                "type": "connections",
                "baseline": self.baseline_metrics.open_connections,
                "current": current.open_connections,
                "factor": current.open_connections / (self.baseline_metrics.open_connections or 1)
            })
        
        status = "coherent" if len(anomalies) == 0 else "anomalies_detected"
        
        return {
            "status": status,
            "metrics": asdict(current),
            "baseline": asdict(self.baseline_metrics),
            "anomalies": anomalies
        }


class BoundaryHardening:
    """
    Boundary Hardening component
    Implements cryptographic boundaries using SHA3-512
    """
    
    def __init__(self):
        self.photon_sphere_radius = 1.5  # Metaphorical boundary
    
    def hash_data(self, data: bytes) -> str:
        """
        Hash data using SHA3-512
        
        Args:
            data: Bytes to hash
            
        Returns:
            Hex digest of hash
        """
        hasher = hashlib.sha3_512()
        hasher.update(data)
        return hasher.hexdigest()
    
    def create_boundary(self, data: str) -> Dict[str, Any]:
        """
        Create a cryptographic boundary around data
        
        Args:
            data: String data to protect
            
        Returns:
            Dictionary with hash and metadata
        """
        data_bytes = data.encode('utf-8')
        data_hash = self.hash_data(data_bytes)
        
        return {
            "hash": data_hash,
            "algorithm": "SHA3-512",
            "data_size": len(data_bytes),
            "timestamp": datetime.now().isoformat(),
            "photon_sphere_metaphor": f"Boundary at r={self.photon_sphere_radius}*rs"
        }
    
    def verify_boundary(self, data: str, expected_hash: str) -> bool:
        """
        Verify data integrity against a hash
        
        Args:
            data: Data to verify
            expected_hash: Expected hash value
            
        Returns:
            True if data matches hash
        """
        data_bytes = data.encode('utf-8')
        actual_hash = self.hash_data(data_bytes)
        return actual_hash == expected_hash


class AuditTrail:
    """
    Audit Trail component
    Logs all security events in JSON format with timestamps
    """
    
    def __init__(self, log_file: Optional[str] = None):
        self.log_file = log_file
        self.events: List[SecurityEvent] = []
    
    def log_event(self, event_type: str, severity: str, details: Dict[str, Any]) -> SecurityEvent:
        """
        Log a security event
        
        Args:
            event_type: Type of security event
            severity: Severity level (INFO, WARNING, CRITICAL)
            details: Event details dictionary
            
        Returns:
            SecurityEvent object
        """
        timestamp = datetime.now().isoformat()
        
        # Create event hash
        event_data = json.dumps({
            "timestamp": timestamp,
            "type": event_type,
            "severity": severity,
            "details": details
        }, sort_keys=True)
        
        event_hash = hashlib.sha3_512(event_data.encode()).hexdigest()
        
        event = SecurityEvent(
            timestamp=timestamp,
            event_type=event_type,
            severity=severity,
            details=details,
            hash=event_hash
        )
        
        self.events.append(event)
        
        # Write to file if configured
        if self.log_file:
            with open(self.log_file, 'a') as f:
                json.dump(asdict(event), f)
                f.write('\n')
        
        return event
    
    def get_events(self, event_type: Optional[str] = None, 
                   severity: Optional[str] = None) -> List[SecurityEvent]:
        """
        Retrieve events, optionally filtered
        
        Args:
            event_type: Filter by event type
            severity: Filter by severity
            
        Returns:
            List of matching security events
        """
        events = self.events
        
        if event_type:
            events = [e for e in events if e.event_type == event_type]
        
        if severity:
            events = [e for e in events if e.severity == severity]
        
        return events


class SovereigntyProtocol:
    """
    Main Sovereignty Protocol Stack
    Coordinates all sovereignty components
    """
    
    def __init__(self, log_file: Optional[str] = None):
        self.network_isolation = NetworkIsolation()
        self.coherence_monitor = CoherenceMonitor()
        self.boundary_hardening = BoundaryHardening()
        self.audit_trail = AuditTrail(log_file)
        
        # Initialize baseline
        self.coherence_monitor.set_baseline()
        
        # Log initialization
        self.audit_trail.log_event(
            "system_init",
            "INFO",
            {"message": "Sovereignty Protocol initialized"}
        )
    
    def check_network_access(self, domain: str) -> bool:
        """Check if network access is allowed"""
        allowed = self.network_isolation.is_domain_allowed(domain)
        
        if not allowed:
            self.audit_trail.log_event(
                "network_blocked",
                "WARNING",
                {"domain": domain, "reason": "Domain blocked by policy"}
            )
        
        return allowed
    
    def monitor_coherence(self) -> Dict[str, Any]:
        """Monitor system coherence"""
        result = self.coherence_monitor.check_coherence()
        
        if result["status"] == "anomalies_detected":
            self.audit_trail.log_event(
                "coherence_anomaly",
                "WARNING",
                {"anomalies": result["anomalies"]}
            )
        
        return result
    
    def protect_data(self, data: str) -> Dict[str, Any]:
        """Create cryptographic boundary around data"""
        boundary = self.boundary_hardening.create_boundary(data)
        
        self.audit_trail.log_event(
            "boundary_created",
            "INFO",
            {"hash": boundary["hash"], "size": boundary["data_size"]}
        )
        
        return boundary
    
    def get_audit_summary(self) -> Dict[str, Any]:
        """Get audit trail summary"""
        all_events = self.audit_trail.get_events()
        
        summary = {
            "total_events": len(all_events),
            "by_severity": {},
            "by_type": {},
            "blocked_domains": len(self.network_isolation.get_blocked_attempts())
        }
        
        for event in all_events:
            # Count by severity
            summary["by_severity"][event.severity] = \
                summary["by_severity"].get(event.severity, 0) + 1
            
            # Count by type
            summary["by_type"][event.event_type] = \
                summary["by_type"].get(event.event_type, 0) + 1
        
        return summary
