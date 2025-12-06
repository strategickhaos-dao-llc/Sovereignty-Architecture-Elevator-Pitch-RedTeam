#!/usr/bin/env python3
"""
KHAOS ENGINE - Resource Arbiter Tests
Strategickhaos DAO LLC / Valoryield Engine
"""

import json
import os
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

import pytest

# Import the module under test
from khaos_engine.core.resource_arbiter import (
    KhaosArbiter,
    ProcessProfile,
    SovereigntyPolicy,
)


class TestProcessProfile:
    """Tests for ProcessProfile dataclass."""
    
    def test_create_basic_profile(self):
        """Test creating a basic process profile."""
        profile = ProcessProfile(
            pid=1234,
            name="test_process",
            cpu_percent=10.5,
            memory_mb=256.0
        )
        
        assert profile.pid == 1234
        assert profile.name == "test_process"
        assert profile.cpu_percent == 10.5
        assert profile.memory_mb == 256.0
        assert profile.priority_score == 100.0  # Default
        
    def test_profile_to_dict(self):
        """Test converting profile to dictionary."""
        profile = ProcessProfile(
            pid=1234,
            name="test_process",
            cpu_percent=10.5,
            memory_mb=256.0,
            environment="conda:myenv",
            priority_score=750.0
        )
        
        result = profile.to_dict()
        
        assert isinstance(result, dict)
        assert result["pid"] == 1234
        assert result["name"] == "test_process"
        assert result["cpu_percent"] == 10.5
        assert result["memory_mb"] == 256.0
        assert result["environment"] == "conda:myenv"
        assert result["priority_score"] == 750.0
        
    def test_profile_commandline_truncation(self):
        """Test that long commandlines are truncated."""
        long_cmdline = "x" * 500
        profile = ProcessProfile(
            pid=1234,
            name="test",
            cpu_percent=0.0,
            memory_mb=0.0,
            commandline=long_cmdline
        )
        
        result = profile.to_dict()
        assert len(result["commandline"]) == 200


class TestSovereigntyPolicy:
    """Tests for SovereigntyPolicy dataclass."""
    
    def test_default_policy(self):
        """Test default policy values."""
        policy = SovereigntyPolicy()
        
        assert policy.thermal_threshold == 85.0
        assert policy.memory_threshold == 0.85
        assert policy.auto_kill_enabled is False
        assert policy.auto_scale_enabled is True
        assert policy.critical_infrastructure_priority == 1000.0
        
    def test_policy_critical_processes(self):
        """Test critical processes list."""
        policy = SovereigntyPolicy()
        
        assert "csrss" in policy.critical_processes
        assert "lsass" in policy.critical_processes
        assert "systemd" in policy.critical_processes
        
    def test_policy_dev_tools(self):
        """Test development tools list."""
        policy = SovereigntyPolicy()
        
        assert "Code" in policy.dev_tools
        assert "vim" in policy.dev_tools
        assert "pycharm" in policy.dev_tools


class TestKhaosArbiter:
    """Tests for KhaosArbiter class."""
    
    def test_arbiter_initialization(self):
        """Test basic arbiter initialization."""
        arbiter = KhaosArbiter()
        
        assert arbiter.policy is not None
        assert isinstance(arbiter.policy, SovereigntyPolicy)
        assert arbiter.process_registry == {}
        
    def test_arbiter_with_custom_config_path(self):
        """Test arbiter with custom config path."""
        arbiter = KhaosArbiter(config_path="/tmp/nonexistent.yaml")
        
        # Should use defaults when file doesn't exist
        assert arbiter.policy.thermal_threshold == 85.0
        
    def test_load_policy_from_yaml(self):
        """Test loading policy from YAML file."""
        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.yaml', delete=False
        ) as f:
            f.write("""
sovereignty_rules:
  thermal_threshold: 90
  memory_threshold: 0.90
  auto_kill_enabled: true
  priority_matrix:
    critical_infrastructure: 999
    browsers: 400
""")
            config_path = f.name
            
        try:
            arbiter = KhaosArbiter(config_path=config_path)
            
            assert arbiter.policy.thermal_threshold == 90
            assert arbiter.policy.memory_threshold == 0.90
            assert arbiter.policy.auto_kill_enabled is True
            assert arbiter.policy.critical_infrastructure_priority == 999
            assert arbiter.policy.browsers_priority == 400
        finally:
            os.unlink(config_path)
    
    def test_calculate_priority_critical_infrastructure(self):
        """Test priority calculation for critical infrastructure."""
        arbiter = KhaosArbiter()
        
        profile = ProcessProfile(
            pid=4,
            name="csrss",
            cpu_percent=5.0,
            memory_mb=50.0
        )
        
        priority = arbiter._calculate_sovereignty_priority(profile)
        
        assert priority == 1000.0  # Critical infrastructure priority
        
    def test_calculate_priority_dev_tools(self):
        """Test priority calculation for development tools."""
        arbiter = KhaosArbiter()
        
        profile = ProcessProfile(
            pid=1234,
            name="Code",
            cpu_percent=15.0,
            memory_mb=500.0,
            commandline="/usr/bin/code --unity-launch"
        )
        
        priority = arbiter._calculate_sovereignty_priority(profile)
        
        assert priority == 700.0  # Dev tools priority
        
    def test_calculate_priority_sovereign_stack(self):
        """Test priority calculation for sovereign stack processes."""
        arbiter = KhaosArbiter()
        
        profile = ProcessProfile(
            pid=5678,
            name="python",
            cpu_percent=25.0,
            memory_mb=300.0,
            commandline="python -m khaos_engine.core.resource_arbiter"
        )
        
        priority = arbiter._calculate_sovereignty_priority(profile)
        
        assert priority == 900.0  # Sovereign stack priority
        
    def test_calculate_priority_idle_process(self):
        """Test priority calculation for idle processes."""
        arbiter = KhaosArbiter()
        
        profile = ProcessProfile(
            pid=9999,
            name="idle_app",
            cpu_percent=0.05,
            memory_mb=50.0
        )
        
        priority = arbiter._calculate_sovereignty_priority(profile)
        
        assert priority == 200.0  # Idle process priority
        
    def test_calculate_priority_resource_vampire(self):
        """Test priority penalty for resource-heavy processes."""
        arbiter = KhaosArbiter()
        
        profile = ProcessProfile(
            pid=8888,
            name="unknown_app",
            cpu_percent=75.0,  # High CPU
            memory_mb=3000.0  # High memory
        )
        
        priority = arbiter._calculate_sovereignty_priority(profile)
        
        # Should have penalties applied
        assert priority < 100.0
        
    def test_detect_environment_conda(self):
        """Test conda environment detection."""
        arbiter = KhaosArbiter()
        
        mock_proc = Mock()
        mock_proc.info = {
            'cmdline': ['/home/user/miniconda3/envs/myenv/bin/python', 'script.py'],
            'name': 'python',
            'pid': 1234
        }
        
        env = arbiter._detect_environment(mock_proc)
        
        assert env.startswith("conda:")
        
    def test_detect_environment_venv(self):
        """Test venv environment detection."""
        arbiter = KhaosArbiter()
        
        mock_proc = Mock()
        mock_proc.info = {
            'cmdline': ['/path/to/project/venv/bin/python', 'app.py'],
            'name': 'python',
            'pid': 1234
        }
        
        env = arbiter._detect_environment(mock_proc)
        
        assert "venv" in env
        
    @patch('khaos_engine.core.resource_arbiter.PSUTIL_AVAILABLE', True)
    @patch('khaos_engine.core.resource_arbiter.psutil')
    def test_get_system_metrics(self, mock_psutil):
        """Test system metrics collection."""
        # Setup mocks
        mock_psutil.cpu_percent.return_value = 25.0
        mock_psutil.cpu_count.return_value = 8
        
        mock_vm = Mock()
        mock_vm.total = 16 * 1024**3  # 16 GB
        mock_vm.available = 8 * 1024**3  # 8 GB
        mock_vm.percent = 50.0
        mock_vm.used = 8 * 1024**3
        mock_psutil.virtual_memory.return_value = mock_vm
        
        mock_disk = Mock()
        mock_disk.total = 500 * 1024**3
        mock_disk.used = 200 * 1024**3
        mock_disk.free = 300 * 1024**3
        mock_disk.percent = 40.0
        mock_psutil.disk_usage.return_value = mock_disk
        
        mock_psutil.sensors_temperatures.return_value = {}
        mock_psutil.disk_io_counters.return_value = None
        mock_psutil.net_io_counters.return_value = None
        
        arbiter = KhaosArbiter()
        metrics = arbiter.get_system_metrics()
        
        assert "timestamp" in metrics
        assert "platform" in metrics
        assert "cpu" in metrics
        assert "memory" in metrics
        
    def test_export_sovereignty_report(self):
        """Test report export functionality."""
        arbiter = KhaosArbiter()
        
        # Mock scan_biosphere to return test data
        with patch.object(arbiter, 'scan_biosphere') as mock_scan:
            mock_scan.return_value = [
                ProcessProfile(
                    pid=1,
                    name="test1",
                    cpu_percent=10.0,
                    memory_mb=100.0,
                    priority_score=500.0
                ),
                ProcessProfile(
                    pid=2,
                    name="test2",
                    cpu_percent=20.0,
                    memory_mb=200.0,
                    priority_score=300.0
                )
            ]
            
            with patch.object(arbiter, 'get_system_metrics') as mock_metrics:
                mock_metrics.return_value = {
                    "timestamp": "2024-01-01T00:00:00",
                    "cpu": {"percent": 15.0},
                    "memory": {"percent": 50.0}
                }
                
                report = arbiter.export_sovereignty_report()
                
        assert report["generator"] == "KHAOS ENGINE"
        assert report["sovereignty_status"] == "AUTONOMOUS"
        assert report["vendor_lock_in"] == "ZERO"
        assert report["process_summary"]["total_processes"] == 2
        assert len(report["top_processes_by_memory"]) == 2
        
    def test_export_report_to_file(self):
        """Test exporting report to a file."""
        arbiter = KhaosArbiter()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "reports", "test_report.json")
            
            with patch.object(arbiter, 'scan_biosphere') as mock_scan:
                mock_scan.return_value = []
                
                with patch.object(arbiter, 'get_system_metrics') as mock_metrics:
                    mock_metrics.return_value = {}
                    
                    report = arbiter.export_sovereignty_report(output_path)
                    
            assert os.path.exists(output_path)
            
            with open(output_path, 'r') as f:
                saved_report = json.load(f)
                
            assert saved_report["generator"] == "KHAOS ENGINE"
            
    def test_enforce_thermal_sovereignty_disabled(self):
        """Test that thermal enforcement respects auto_kill_enabled."""
        arbiter = KhaosArbiter()
        arbiter.policy.auto_kill_enabled = False
        
        with patch.object(arbiter, 'get_cpu_temperature') as mock_temp:
            mock_temp.return_value = 95.0  # Above threshold
            
            actions = arbiter.enforce_thermal_sovereignty()
            
        # Should only have alert action, no terminations
        assert len(actions) == 1
        assert actions[0]["action"] == "alert"
        assert actions[0]["auto_kill"] is False
        
    def test_enforce_memory_sovereignty_disabled(self):
        """Test that memory enforcement respects auto_kill_enabled."""
        arbiter = KhaosArbiter()
        arbiter.policy.auto_kill_enabled = False
        
        with patch.object(arbiter, 'get_memory_usage') as mock_mem:
            mock_mem.return_value = 0.95  # Above threshold
            
            actions = arbiter.enforce_memory_sovereignty()
            
        assert len(actions) == 1
        assert actions[0]["action"] == "alert"
        assert actions[0]["auto_kill"] is False
        
    def test_run_governance_cycle(self):
        """Test running a complete governance cycle."""
        arbiter = KhaosArbiter()
        
        with patch.object(arbiter, 'scan_biosphere') as mock_scan:
            mock_scan.return_value = []
            
            with patch.object(arbiter, 'enforce_thermal_sovereignty') as mock_thermal:
                mock_thermal.return_value = []
                
                with patch.object(arbiter, 'enforce_memory_sovereignty') as mock_memory:
                    mock_memory.return_value = []
                    
                    with patch.object(arbiter, 'get_system_metrics') as mock_metrics:
                        mock_metrics.return_value = {
                            "cpu": {"percent": 20.0, "temperature": 65.0},
                            "memory": {"percent": 40.0}
                        }
                        
                        result = arbiter.run_governance_cycle()
                        
        assert "timestamp" in result
        assert "processes_scanned" in result
        assert result["status"] == "HEALTHY"
        
    def test_get_environment_breakdown(self):
        """Test environment breakdown calculation."""
        arbiter = KhaosArbiter()
        
        profiles = [
            ProcessProfile(
                pid=1, name="p1", cpu_percent=0, memory_mb=0,
                environment="native:linux"
            ),
            ProcessProfile(
                pid=2, name="p2", cpu_percent=0, memory_mb=0,
                environment="native:linux"
            ),
            ProcessProfile(
                pid=3, name="p3", cpu_percent=0, memory_mb=0,
                environment="conda:myenv"
            ),
            ProcessProfile(
                pid=4, name="p4", cpu_percent=0, memory_mb=0,
                environment="docker:container"
            )
        ]
        
        breakdown = arbiter._get_environment_breakdown(profiles)
        
        assert breakdown["native"] == 2
        assert breakdown["conda"] == 1
        assert breakdown["docker"] == 1


class TestIntegration:
    """Integration tests (require psutil)."""
    
    @pytest.mark.skipif(
        not os.environ.get('RUN_INTEGRATION_TESTS'),
        reason="Integration tests disabled"
    )
    def test_scan_real_processes(self):
        """Test scanning real system processes."""
        arbiter = KhaosArbiter()
        profiles = arbiter.scan_biosphere()
        
        assert len(profiles) > 0
        
        # Check that profiles have valid data
        for profile in profiles[:5]:  # Check first 5
            assert profile.pid > 0
            assert profile.name
            assert profile.memory_mb >= 0
            
    @pytest.mark.skipif(
        not os.environ.get('RUN_INTEGRATION_TESTS'),
        reason="Integration tests disabled"
    )
    def test_real_system_metrics(self):
        """Test getting real system metrics."""
        arbiter = KhaosArbiter()
        metrics = arbiter.get_system_metrics()
        
        assert "cpu" in metrics
        assert "memory" in metrics
        assert metrics["cpu"]["percent"] >= 0
        assert metrics["memory"]["percent"] >= 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
