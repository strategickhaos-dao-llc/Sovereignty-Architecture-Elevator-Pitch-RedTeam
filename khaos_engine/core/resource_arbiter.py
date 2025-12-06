#!/usr/bin/env python3
"""
KHAOS ENGINE - Sovereign Resource Arbiter
Core component for resource governance and process management.

Strategickhaos DAO LLC / Valoryield Engine
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path
import json
import logging
import os
import platform
import subprocess

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class ProcessProfile:
    """Sovereign process metadata - detailed profile of a running process."""
    
    pid: int
    name: str
    cpu_percent: float
    memory_mb: float
    gpu_usage: float = 0.0
    network_io: int = 0
    disk_io: int = 0
    parent_pid: int = 0
    commandline: str = ""
    environment: str = "native"
    priority_score: float = 100.0
    status: str = "unknown"
    create_time: float = 0.0
    username: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert process profile to dictionary."""
        return {
            "pid": self.pid,
            "name": self.name,
            "cpu_percent": self.cpu_percent,
            "memory_mb": round(self.memory_mb, 2),
            "gpu_usage": self.gpu_usage,
            "network_io": self.network_io,
            "disk_io": self.disk_io,
            "parent_pid": self.parent_pid,
            "commandline": self.commandline[:200] if self.commandline else "",
            "environment": self.environment,
            "priority_score": round(self.priority_score, 2),
            "status": self.status,
            "create_time": self.create_time,
            "username": self.username
        }


@dataclass
class SovereigntyPolicy:
    """Policy configuration for resource governance."""
    
    thermal_threshold: float = 85.0  # CPU temp in Celsius
    memory_threshold: float = 0.85  # 85% RAM usage
    auto_kill_enabled: bool = False  # Safe default
    auto_scale_enabled: bool = True
    
    # Priority matrix
    critical_infrastructure_priority: float = 1000.0
    strategickhaos_stack_priority: float = 900.0
    development_tools_priority: float = 700.0
    browsers_priority: float = 500.0
    idle_processes_priority: float = 200.0
    
    # Critical infrastructure process names
    critical_processes: List[str] = field(default_factory=lambda: [
        "wininit", "csrss", "services", "lsass", "smss", "winlogon",
        "System", "svchost", "init", "systemd", "kernel"
    ])
    
    # Strategickhaos stack identifiers
    sovereign_stack_identifiers: List[str] = field(default_factory=lambda: [
        "strategickhaos", "khaos", "legion", "valoryield", "refinory"
    ])
    
    # Development tools
    dev_tools: List[str] = field(default_factory=lambda: [
        "Code", "code", "rider", "jetbrains", "pycharm", "intellij",
        "webstorm", "goland", "vim", "nvim", "emacs", "sublime_text"
    ])
    
    # Browsers
    browsers: List[str] = field(default_factory=lambda: [
        "firefox", "chrome", "msedge", "brave", "opera", "chromium"
    ])


class KhaosArbiter:
    """
    Sovereign Resource Governance Engine
    
    Replaces vendor lock-in task managers with policy-based autonomy.
    Provides deep process inspection, priority calculation, and
    thermal management capabilities.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the KHAOS Arbiter.
        
        Args:
            config_path: Optional path to YAML configuration file.
                        Defaults to ~/.strategickhaos/khaos.yaml
        """
        self.config_path = config_path or os.path.expanduser(
            "~/.strategickhaos/khaos.yaml"
        )
        self.policy = self._load_policy()
        self.process_registry: Dict[int, ProcessProfile] = {}
        self._docker_pids_cache: Optional[List[int]] = None
        self._docker_pids_cache_time: float = 0
        
        if not PSUTIL_AVAILABLE:
            logger.warning(
                "psutil not available - process scanning will be limited"
            )
    
    def _load_policy(self) -> SovereigntyPolicy:
        """Load sovereignty policy from configuration file."""
        policy = SovereigntyPolicy()
        
        if YAML_AVAILABLE and Path(self.config_path).exists():
            try:
                with open(self.config_path, 'r') as f:
                    config = yaml.safe_load(f)
                    
                if config and 'sovereignty_rules' in config:
                    rules = config['sovereignty_rules']
                    policy.thermal_threshold = rules.get(
                        'thermal_threshold', policy.thermal_threshold
                    )
                    policy.memory_threshold = rules.get(
                        'memory_threshold', policy.memory_threshold
                    )
                    policy.auto_kill_enabled = rules.get(
                        'auto_kill_enabled', policy.auto_kill_enabled
                    )
                    policy.auto_scale_enabled = rules.get(
                        'auto_scale_enabled', policy.auto_scale_enabled
                    )
                    
                    if 'priority_matrix' in rules:
                        pm = rules['priority_matrix']
                        policy.critical_infrastructure_priority = pm.get(
                            'critical_infrastructure', 
                            policy.critical_infrastructure_priority
                        )
                        policy.strategickhaos_stack_priority = pm.get(
                            'strategickhaos_stack',
                            policy.strategickhaos_stack_priority
                        )
                        policy.development_tools_priority = pm.get(
                            'development_tools',
                            policy.development_tools_priority
                        )
                        policy.browsers_priority = pm.get(
                            'browsers', policy.browsers_priority
                        )
                        policy.idle_processes_priority = pm.get(
                            'idle_processes', policy.idle_processes_priority
                        )
                        
                logger.info(f"Loaded policy from {self.config_path}")
                
            except Exception as e:
                logger.warning(f"Failed to load config: {e}, using defaults")
                
        return policy
    
    def scan_biosphere(self) -> List[ProcessProfile]:
        """
        Deep scan of all processes with sovereignty attribution.
        
        Returns:
            List of ProcessProfile objects for all accessible processes.
        """
        if not PSUTIL_AVAILABLE:
            logger.error("psutil required for process scanning")
            return []
            
        profiles: List[ProcessProfile] = []
        
        for proc in psutil.process_iter([
            'pid', 'name', 'cpu_percent', 'memory_info', 
            'cmdline', 'ppid', 'status', 'create_time', 'username'
        ]):
            try:
                info = proc.info
                
                # Build command line safely
                cmdline = ""
                if info.get('cmdline'):
                    cmdline = ' '.join(info['cmdline'])
                
                # Calculate memory in MB
                memory_mb = 0.0
                if info.get('memory_info'):
                    memory_mb = info['memory_info'].rss / 1024 / 1024
                
                profile = ProcessProfile(
                    pid=info.get('pid', 0),
                    name=info.get('name', 'unknown'),
                    cpu_percent=self._get_cpu_percent(proc),
                    memory_mb=memory_mb,
                    gpu_usage=self._get_gpu_usage(info.get('pid', 0)),
                    network_io=self._get_network_io(proc),
                    disk_io=self._get_disk_io(proc),
                    parent_pid=info.get('ppid', 0),
                    commandline=cmdline,
                    environment=self._detect_environment(proc),
                    priority_score=0.0,
                    status=info.get('status', 'unknown'),
                    create_time=info.get('create_time', 0.0),
                    username=info.get('username', '')
                )
                
                # Calculate priority based on sovereignty policy
                profile.priority_score = self._calculate_sovereignty_priority(
                    profile
                )
                
                # Store in registry
                self.process_registry[profile.pid] = profile
                profiles.append(profile)
                
            except (psutil.NoSuchProcess, psutil.AccessDenied, 
                    psutil.ZombieProcess):
                continue
            except Exception as e:
                logger.debug(f"Error scanning process: {e}")
                continue
                
        return profiles
    
    def _get_cpu_percent(self, proc) -> float:
        """Get CPU percent for a process safely."""
        try:
            return proc.cpu_percent(interval=0.1)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return 0.0
    
    def _get_gpu_usage(self, pid: int) -> float:
        """
        Get GPU usage for a process.
        
        Note: Requires nvidia-smi for NVIDIA GPUs.
        """
        # GPU monitoring requires specialized tools
        # This is a placeholder for nvidia-smi integration
        return 0.0
    
    def _get_network_io(self, proc) -> int:
        """
        Get estimated network I/O for a process.
        
        Note: Per-process network I/O is not directly available via psutil.
        This method attempts to count open network connections as a proxy.
        For accurate per-process network stats, consider using:
        - Linux: /proc/PID/net/dev or nethogs
        - Windows: ETW tracing
        
        Returns:
            Number of network connections * 1024 as a rough activity estimate,
            or 0 if unavailable.
        """
        try:
            connections = proc.net_connections()
            # Estimate based on number of active connections
            # More connections = likely more network activity
            return len(connections) * 1024
        except (psutil.NoSuchProcess, psutil.AccessDenied, AttributeError):
            pass
        return 0
    
    def _get_disk_io(self, proc) -> int:
        """
        Get disk I/O bytes for a process.
        
        Returns:
            Total read + write bytes, or 0 if unavailable.
        """
        try:
            io_counters = proc.io_counters()
            if io_counters:
                return io_counters.read_bytes + io_counters.write_bytes
        except (psutil.NoSuchProcess, psutil.AccessDenied, AttributeError):
            pass
        return 0
    
    def _get_docker_pids(self) -> List[int]:
        """Get PIDs of Docker containers with caching."""
        import time
        current_time = time.time()
        
        # Cache for 30 seconds
        if (self._docker_pids_cache is not None and 
            current_time - self._docker_pids_cache_time < 30):
            return self._docker_pids_cache
        
        docker_pids: List[int] = []
        try:
            result = subprocess.run(
                ['docker', 'ps', '-q'],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                container_ids = result.stdout.strip().split('\n')
                for cid in container_ids:
                    if cid:
                        pid_result = subprocess.run(
                            ['docker', 'inspect', '-f', '{{.State.Pid}}', cid],
                            capture_output=True, text=True, timeout=5
                        )
                        if pid_result.returncode == 0:
                            try:
                                docker_pids.append(int(pid_result.stdout.strip()))
                            except ValueError:
                                pass
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        self._docker_pids_cache = docker_pids
        self._docker_pids_cache_time = current_time
        return docker_pids
    
    def _detect_environment(self, proc) -> str:
        """
        Detect if process is in venv, conda, docker, WSL.
        
        Returns:
            Environment string like 'conda:myenv', 'docker:container', etc.
        """
        try:
            info = proc.info
            cmdline = ' '.join(info.get('cmdline') or []).lower()
            name = info.get('name', '').lower()
            
            # Conda detection
            if 'conda' in cmdline or 'miniconda' in cmdline:
                # Try to extract env name
                if 'envs/' in cmdline:
                    parts = cmdline.split('envs/')
                    if len(parts) > 1:
                        env_name = parts[1].split('/')[0]
                        return f"conda:{env_name}"
                return "conda:base"
            
            # Venv detection
            if 'venv' in cmdline or 'virtualenv' in cmdline:
                return "venv:active"
            
            # Docker detection
            pid = info.get('pid', 0)
            if pid in self._get_docker_pids():
                return "docker:container"
            
            # WSL detection
            if 'wsl' in name or 'wslhost' in name:
                return "wsl2:instance"
            
            # Check /proc/PID/cgroup for container detection on Linux
            if platform.system() == 'Linux':
                cgroup_path = Path(f'/proc/{pid}/cgroup')
                if cgroup_path.exists():
                    try:
                        content = cgroup_path.read_text()
                        if 'docker' in content:
                            return "docker:container"
                        if 'kubepods' in content:
                            return "kubernetes:pod"
                    except (PermissionError, FileNotFoundError):
                        pass
            
            return f"native:{platform.system().lower()}"
            
        except Exception:
            return "unknown"
    
    def _calculate_sovereignty_priority(
        self, profile: ProcessProfile
    ) -> float:
        """
        Calculate priority score based on sovereignty policy.
        
        Higher score = higher priority = protected from termination.
        
        Args:
            profile: ProcessProfile to evaluate
            
        Returns:
            Priority score (higher = more protected)
        """
        score = 100.0  # Start neutral
        name = profile.name.lower() if profile.name else ""
        cmdline = profile.commandline.lower() if profile.commandline else ""
        
        # CRITICAL INFRASTRUCTURE (never kill)
        if profile.name in self.policy.critical_processes:
            return self.policy.critical_infrastructure_priority
        
        # YOUR SOVEREIGN STACK (high priority)
        for identifier in self.policy.sovereign_stack_identifiers:
            if identifier in cmdline or identifier in name:
                return self.policy.strategickhaos_stack_priority
        
        # DEVELOPMENT TOOLS (medium-high priority)
        for tool in self.policy.dev_tools:
            if tool.lower() in name or tool.lower() in cmdline:
                return self.policy.development_tools_priority
        
        # BROWSERS (medium priority, but penalize multiple instances)
        for browser in self.policy.browsers:
            if browser.lower() in name:
                # Count browser instances
                browser_count = sum(
                    1 for p in self.process_registry.values()
                    if browser.lower() in p.name.lower()
                )
                score = self.policy.browsers_priority - (browser_count * 50)
                return max(score, 100.0)  # Don't go below 100
        
        # WSL/DOCKER (depends on what's running inside)
        if 'wsl' in name or 'docker' in name:
            return 600.0
        
        # IDLE PROCESSES (low priority)
        if profile.cpu_percent < 0.1 and profile.memory_mb < 100:
            score = self.policy.idle_processes_priority
        
        # RESOURCE VAMPIRES (negative modifiers)
        if profile.memory_mb > 2000:  # 2GB+
            score -= 100
        if profile.cpu_percent > 50:  # 50%+ CPU
            score -= 100
            
        return max(score, 10.0)  # Minimum score of 10
    
    def get_cpu_temperature(self) -> float:
        """
        Get CPU temperature (platform-specific).
        
        Returns:
            CPU temperature in Celsius, or safe default (60.0) if unavailable.
        """
        if not PSUTIL_AVAILABLE:
            return 60.0
        
        # Try psutil sensors (Linux)
        try:
            temps = psutil.sensors_temperatures()
            if temps:
                # Look for coretemp or cpu_thermal
                for name in ['coretemp', 'cpu_thermal', 'k10temp', 'acpitz']:
                    if name in temps:
                        return temps[name][0].current
                # Return first available
                for sensor_temps in temps.values():
                    if sensor_temps:
                        return sensor_temps[0].current
        except (AttributeError, IndexError):
            pass
        
        # Windows via WMI (fallback)
        if platform.system() == 'Windows':
            try:
                result = subprocess.run(
                    ['powershell', '-Command',
                     'Get-CimInstance MSAcpi_ThermalZoneTemperature '
                     '-Namespace root/wmi 2>$null | '
                     'Select-Object -First 1 -ExpandProperty CurrentTemperature'],
                    capture_output=True, text=True, timeout=5
                )
                if result.returncode == 0 and result.stdout.strip():
                    temp_kelvin = float(result.stdout.strip())
                    return (temp_kelvin / 10) - 273.15
            except (subprocess.TimeoutExpired, ValueError, FileNotFoundError):
                pass
        
        return 60.0  # Safe default
    
    def get_memory_usage(self) -> float:
        """
        Get system memory usage percentage.
        
        Returns:
            Memory usage as percentage (0.0 to 1.0)
        """
        if not PSUTIL_AVAILABLE:
            return 0.5
        
        return psutil.virtual_memory().percent / 100.0
    
    def enforce_thermal_sovereignty(self) -> List[Dict[str, Any]]:
        """
        Enforce thermal limits by terminating low-priority processes.
        
        Only acts if auto_kill_enabled is True in policy.
        
        Returns:
            List of actions taken (terminated processes).
        """
        actions: List[Dict[str, Any]] = []
        
        current_temp = self.get_cpu_temperature()
        
        if current_temp <= self.policy.thermal_threshold:
            return actions
        
        logger.warning(
            f"THERMAL CRISIS: {current_temp}°C - "
            f"Threshold: {self.policy.thermal_threshold}°C"
        )
        
        if not self.policy.auto_kill_enabled:
            logger.info("Auto-kill disabled - logging only")
            actions.append({
                "action": "alert",
                "reason": "thermal_threshold_exceeded",
                "temperature": current_temp,
                "threshold": self.policy.thermal_threshold,
                "auto_kill": False
            })
            return actions
        
        # Get all processes sorted by priority (lowest first)
        profiles = sorted(
            self.scan_biosphere(),
            key=lambda p: p.priority_score
        )
        
        # Terminate lowest priority until temp drops
        for profile in profiles:
            if current_temp <= self.policy.thermal_threshold:
                break
            
            # Only terminate low-priority processes
            if profile.priority_score < 500:
                logger.info(
                    f"Terminating: {profile.name} (PID {profile.pid}) - "
                    f"Priority: {profile.priority_score}"
                )
                
                try:
                    psutil.Process(profile.pid).terminate()
                    actions.append({
                        "action": "terminate",
                        "pid": profile.pid,
                        "name": profile.name,
                        "priority": profile.priority_score,
                        "reason": "thermal_management"
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
                
                # Recheck temperature
                import time
                time.sleep(1)
                current_temp = self.get_cpu_temperature()
        
        return actions
    
    def enforce_memory_sovereignty(self) -> List[Dict[str, Any]]:
        """
        Enforce memory limits by terminating low-priority processes.
        
        Only acts if auto_kill_enabled is True in policy.
        
        Returns:
            List of actions taken.
        """
        actions: List[Dict[str, Any]] = []
        
        memory_usage = self.get_memory_usage()
        
        if memory_usage <= self.policy.memory_threshold:
            return actions
        
        logger.warning(
            f"MEMORY CRISIS: {memory_usage*100:.1f}% - "
            f"Threshold: {self.policy.memory_threshold*100:.1f}%"
        )
        
        if not self.policy.auto_kill_enabled:
            actions.append({
                "action": "alert",
                "reason": "memory_threshold_exceeded",
                "usage": memory_usage,
                "threshold": self.policy.memory_threshold,
                "auto_kill": False
            })
            return actions
        
        # Get processes sorted by memory usage (highest first)
        profiles = sorted(
            self.scan_biosphere(),
            key=lambda p: (-p.memory_mb, p.priority_score)
        )
        
        for profile in profiles:
            if memory_usage <= self.policy.memory_threshold:
                break
            
            # Only terminate low-priority, high-memory processes
            if profile.priority_score < 500 and profile.memory_mb > 100:
                try:
                    psutil.Process(profile.pid).terminate()
                    actions.append({
                        "action": "terminate",
                        "pid": profile.pid,
                        "name": profile.name,
                        "memory_mb": profile.memory_mb,
                        "priority": profile.priority_score,
                        "reason": "memory_management"
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
                
                import time
                time.sleep(0.5)
                memory_usage = self.get_memory_usage()
        
        return actions
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """
        Get comprehensive system metrics.
        
        Returns:
            Dictionary containing CPU, memory, disk, and network metrics.
        """
        metrics: Dict[str, Any] = {
            "timestamp": datetime.now().isoformat(),
            "platform": platform.system(),
            "hostname": platform.node()
        }
        
        if not PSUTIL_AVAILABLE:
            return metrics
        
        # CPU metrics
        metrics["cpu"] = {
            "percent": psutil.cpu_percent(interval=0.1),
            "count": psutil.cpu_count(),
            "count_logical": psutil.cpu_count(logical=True),
            "temperature": self.get_cpu_temperature()
        }
        
        # Memory metrics
        vm = psutil.virtual_memory()
        metrics["memory"] = {
            "total_gb": round(vm.total / (1024**3), 2),
            "available_gb": round(vm.available / (1024**3), 2),
            "percent": vm.percent,
            "used_gb": round(vm.used / (1024**3), 2)
        }
        
        # Disk metrics
        try:
            disk = psutil.disk_usage('/')
            metrics["disk"] = {
                "total_gb": round(disk.total / (1024**3), 2),
                "used_gb": round(disk.used / (1024**3), 2),
                "free_gb": round(disk.free / (1024**3), 2),
                "percent": disk.percent
            }
        except Exception:
            metrics["disk"] = {}
        
        # Disk I/O
        try:
            disk_io = psutil.disk_io_counters()
            if disk_io:
                metrics["disk_io"] = {
                    "read_bytes": disk_io.read_bytes,
                    "write_bytes": disk_io.write_bytes,
                    "read_count": disk_io.read_count,
                    "write_count": disk_io.write_count
                }
        except Exception:
            pass
        
        # Network I/O
        try:
            net_io = psutil.net_io_counters()
            if net_io:
                metrics["network"] = {
                    "bytes_sent": net_io.bytes_sent,
                    "bytes_recv": net_io.bytes_recv,
                    "packets_sent": net_io.packets_sent,
                    "packets_recv": net_io.packets_recv
                }
        except Exception:
            pass
        
        return metrics
    
    def export_sovereignty_report(
        self, output_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate comprehensive sovereignty report for Legion analysis.
        
        Args:
            output_path: Optional path to write JSON report.
            
        Returns:
            Complete sovereignty report as dictionary.
        """
        profiles = self.scan_biosphere()
        
        report = {
            "report_version": "1.0.0",
            "generator": "KHAOS ENGINE",
            "timestamp": datetime.now().isoformat(),
            "system_metrics": self.get_system_metrics(),
            "policy": {
                "thermal_threshold": self.policy.thermal_threshold,
                "memory_threshold": self.policy.memory_threshold,
                "auto_kill_enabled": self.policy.auto_kill_enabled,
                "auto_scale_enabled": self.policy.auto_scale_enabled
            },
            "process_summary": {
                "total_processes": len(profiles),
                "high_priority": len([p for p in profiles 
                                     if p.priority_score >= 700]),
                "medium_priority": len([p for p in profiles 
                                       if 300 <= p.priority_score < 700]),
                "low_priority": len([p for p in profiles 
                                    if p.priority_score < 300]),
                "total_memory_mb": round(
                    sum(p.memory_mb for p in profiles), 2
                ),
                "avg_cpu_percent": round(
                    sum(p.cpu_percent for p in profiles) / len(profiles)
                    if profiles else 0, 2
                )
            },
            "top_processes_by_memory": [
                p.to_dict() for p in sorted(
                    profiles, key=lambda x: -x.memory_mb
                )[:10]
            ],
            "top_processes_by_cpu": [
                p.to_dict() for p in sorted(
                    profiles, key=lambda x: -x.cpu_percent
                )[:10]
            ],
            "sovereignty_status": "AUTONOMOUS",
            "vendor_lock_in": "ZERO",
            "environment_breakdown": self._get_environment_breakdown(profiles)
        }
        
        if output_path:
            output = Path(output_path)
            output.parent.mkdir(parents=True, exist_ok=True)
            with open(output, 'w') as f:
                json.dump(report, f, indent=2)
            logger.info(f"Report exported to {output_path}")
        
        return report
    
    def _get_environment_breakdown(
        self, profiles: List[ProcessProfile]
    ) -> Dict[str, int]:
        """Get breakdown of processes by environment type."""
        breakdown: Dict[str, int] = {}
        for profile in profiles:
            env_type = profile.environment.split(':')[0]
            breakdown[env_type] = breakdown.get(env_type, 0) + 1
        return breakdown
    
    def run_governance_cycle(self) -> Dict[str, Any]:
        """
        Run a complete governance cycle.
        
        Performs:
        1. Process scan
        2. Thermal check
        3. Memory check
        4. Report generation
        
        Returns:
            Cycle summary with actions taken.
        """
        logger.info("Starting governance cycle")
        
        # Scan processes
        profiles = self.scan_biosphere()
        
        # Check thermal limits
        thermal_actions = self.enforce_thermal_sovereignty()
        
        # Check memory limits  
        memory_actions = self.enforce_memory_sovereignty()
        
        # Get system state
        metrics = self.get_system_metrics()
        
        cycle_result = {
            "timestamp": datetime.now().isoformat(),
            "processes_scanned": len(profiles),
            "thermal_actions": thermal_actions,
            "memory_actions": memory_actions,
            "system_health": {
                "cpu_percent": metrics.get("cpu", {}).get("percent", 0),
                "cpu_temp": metrics.get("cpu", {}).get("temperature", 0),
                "memory_percent": metrics.get("memory", {}).get("percent", 0)
            },
            "status": "HEALTHY" if not (
                thermal_actions or memory_actions
            ) else "ACTION_TAKEN"
        }
        
        logger.info(f"Governance cycle complete: {cycle_result['status']}")
        
        return cycle_result


# CLI entrypoint
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="KHAOS ENGINE - Sovereign Resource Arbiter"
    )
    parser.add_argument(
        "--config", "-c",
        help="Path to configuration file",
        default=None
    )
    parser.add_argument(
        "--report", "-r",
        help="Generate and save report to path",
        default=None
    )
    parser.add_argument(
        "--cycle",
        help="Run governance cycle",
        action="store_true"
    )
    parser.add_argument(
        "--scan",
        help="Scan processes and print summary",
        action="store_true"
    )
    parser.add_argument(
        "--metrics",
        help="Print system metrics",
        action="store_true"
    )
    
    args = parser.parse_args()
    
    # Configure logging for CLI
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    arbiter = KhaosArbiter(config_path=args.config)
    
    if args.metrics:
        metrics = arbiter.get_system_metrics()
        print(json.dumps(metrics, indent=2))
        
    elif args.scan:
        profiles = arbiter.scan_biosphere()
        print(f"\nScanned {len(profiles)} processes:")
        print("-" * 60)
        for p in sorted(profiles, key=lambda x: -x.memory_mb)[:20]:
            print(f"  {p.name:20} PID:{p.pid:6} "
                  f"MEM:{p.memory_mb:8.1f}MB "
                  f"CPU:{p.cpu_percent:5.1f}% "
                  f"Priority:{p.priority_score:6.1f}")
        
    elif args.cycle:
        result = arbiter.run_governance_cycle()
        print(json.dumps(result, indent=2))
        
    elif args.report:
        report = arbiter.export_sovereignty_report(args.report)
        print(f"Report saved to {args.report}")
        
    else:
        # Default: print summary
        arbiter.scan_biosphere()
        report = arbiter.export_sovereignty_report()
        print(json.dumps(report, indent=2))
