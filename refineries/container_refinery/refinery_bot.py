#!/usr/bin/env python3
"""
Container Refinery Bot - The Immune System for Docker/Kubernetes Clusters
Always-watching heir that enforces GitOps and detects drift across all nodes

This is the nuclear solution for container sovereignty.
Every container birth, death, and mutation is tracked, validated, and enforced.
"""

import asyncio
import json
import subprocess
import sys
import time
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set
import hashlib
import yaml
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('refinery_bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('ContainerRefineryBot')


@dataclass
class ContainerState:
    """Represents the state of a container/pod"""
    name: str
    image: str
    image_sha: str
    node: str
    namespace: Optional[str]
    labels: Dict[str, str]
    created_at: str
    status: str
    config_hash: str
    
    def to_dict(self):
        return asdict(self)


@dataclass
class DriftAlert:
    """Represents a drift detection event"""
    timestamp: str
    node: str
    container_name: str
    drift_type: str
    expected_state: Dict
    actual_state: Dict
    action_taken: str
    
    def to_dict(self):
        return asdict(self)


class GitOpsEnforcer:
    """Enforces git as the source of truth for all container configs"""
    
    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
        self.manifests_path = repo_path / "manifests"
        self.manifests_path.mkdir(parents=True, exist_ok=True)
        
    def get_expected_state(self) -> Dict[str, Dict]:
        """Load expected state from git repository"""
        expected = {}
        
        # Load all YAML manifests from git
        for yaml_file in self.manifests_path.glob("**/*.yaml"):
            try:
                with open(yaml_file, 'r') as f:
                    docs = yaml.safe_load_all(f)
                    for doc in docs:
                        if doc and 'metadata' in doc:
                            name = doc['metadata'].get('name', 'unknown')
                            expected[name] = doc
            except Exception as e:
                logger.error(f"Error loading manifest {yaml_file}: {e}")
                
        return expected
    
    def commit_changes(self, message: str):
        """Commit changes to git"""
        try:
            subprocess.run(['git', 'add', '.'], cwd=self.repo_path, check=True)
            subprocess.run(['git', 'commit', '-m', message], cwd=self.repo_path, check=True)
            logger.info(f"Committed changes: {message}")
        except subprocess.CalledProcessError as e:
            logger.warning(f"Git commit failed: {e}")
    
    def get_manifest_hash(self, manifest: Dict) -> str:
        """Calculate hash of a manifest for comparison"""
        manifest_str = json.dumps(manifest, sort_keys=True)
        return hashlib.sha256(manifest_str.encode()).hexdigest()[:16]


class ContainerLedger:
    """Maintains the immutable ledger of all container operations"""
    
    def __init__(self, ledger_path: Path):
        self.ledger_path = ledger_path
        self.ledger_file = ledger_path / "container_ledger.jsonl"
        self.ledger_path.mkdir(parents=True, exist_ok=True)
        
    def log_event(self, event_type: str, details: Dict):
        """Append event to the ledger"""
        entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'event_type': event_type,
            'details': details
        }
        
        with open(self.ledger_file, 'a') as f:
            f.write(json.dumps(entry) + '\n')
            
        logger.info(f"Ledger: {event_type} - {details.get('name', 'unknown')}")
    
    def get_recent_events(self, limit: int = 100) -> List[Dict]:
        """Retrieve recent events from ledger"""
        events = []
        
        if not self.ledger_file.exists():
            return events
            
        with open(self.ledger_file, 'r') as f:
            lines = f.readlines()
            for line in lines[-limit:]:
                try:
                    events.append(json.loads(line.strip()))
                except json.JSONDecodeError:
                    continue
                    
        return events


class DockerMonitor:
    """Monitors Docker containers on local and remote nodes"""
    
    def __init__(self, node_name: str):
        self.node_name = node_name
        
    async def get_running_containers(self) -> List[ContainerState]:
        """Get list of running Docker containers"""
        containers = []
        
        try:
            # Get container list
            result = subprocess.run(
                ['docker', 'ps', '--format', '{{json .}}'],
                capture_output=True,
                text=True,
                check=True
            )
            
            for line in result.stdout.strip().split('\n'):
                if not line:
                    continue
                    
                try:
                    container_json = json.loads(line)
                    
                    # Get detailed inspect info
                    inspect_result = subprocess.run(
                        ['docker', 'inspect', container_json['ID']],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    
                    inspect_data = json.loads(inspect_result.stdout)[0]
                    
                    container = ContainerState(
                        name=container_json['Names'],
                        image=container_json['Image'],
                        image_sha=inspect_data['Image'],
                        node=self.node_name,
                        namespace=None,
                        labels=inspect_data['Config'].get('Labels', {}),
                        created_at=inspect_data['Created'],
                        status=container_json['Status'],
                        config_hash=self._compute_config_hash(inspect_data['Config'])
                    )
                    
                    containers.append(container)
                    
                except json.JSONDecodeError as e:
                    logger.error(f"Error parsing container JSON: {e}")
                    
        except subprocess.CalledProcessError as e:
            logger.error(f"Error getting Docker containers: {e}")
            
        return containers
    
    def _compute_config_hash(self, config: Dict) -> str:
        """Compute hash of container configuration"""
        config_str = json.dumps(config, sort_keys=True)
        return hashlib.sha256(config_str.encode()).hexdigest()[:16]


class KubernetesMonitor:
    """Monitors Kubernetes pods across clusters"""
    
    def __init__(self, node_name: str):
        self.node_name = node_name
        
    async def get_running_pods(self) -> List[ContainerState]:
        """Get list of running Kubernetes pods"""
        pods = []
        
        try:
            # Check if kubectl is available
            subprocess.run(['kubectl', 'version', '--client'], 
                         capture_output=True, check=True)
            
            # Get pod list
            result = subprocess.run(
                ['kubectl', 'get', 'pods', '--all-namespaces', '-o', 'json'],
                capture_output=True,
                text=True,
                check=True
            )
            
            pod_data = json.loads(result.stdout)
            
            for item in pod_data.get('items', []):
                metadata = item.get('metadata', {})
                spec = item.get('spec', {})
                status = item.get('status', {})
                
                for container in spec.get('containers', []):
                    pod = ContainerState(
                        name=f"{metadata.get('name', 'unknown')}/{container['name']}",
                        image=container['image'],
                        image_sha=self._get_image_sha(status, container['name']),
                        node=spec.get('nodeName', self.node_name),
                        namespace=metadata.get('namespace', 'default'),
                        labels=metadata.get('labels', {}),
                        created_at=metadata.get('creationTimestamp', ''),
                        status=status.get('phase', 'Unknown'),
                        config_hash=self._compute_pod_hash(spec)
                    )
                    
                    pods.append(pod)
                    
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.info("Kubernetes not available or not configured")
            
        return pods
    
    def _get_image_sha(self, status: Dict, container_name: str) -> str:
        """Extract image SHA from pod status"""
        for container_status in status.get('containerStatuses', []):
            if container_status.get('name') == container_name:
                return container_status.get('imageID', 'unknown')
        return 'unknown'
    
    def _compute_pod_hash(self, spec: Dict) -> str:
        """Compute hash of pod specification"""
        spec_str = json.dumps(spec, sort_keys=True)
        return hashlib.sha256(spec_str.encode()).hexdigest()[:16]


class DriftDetector:
    """Detects drift between expected (git) and actual (running) state"""
    
    def __init__(self):
        self.detected_drifts: List[DriftAlert] = []
        
    def detect_drift(self, expected: Dict[str, Dict], actual: List[ContainerState]) -> List[DriftAlert]:
        """Compare expected vs actual state and detect drift"""
        drifts = []
        
        # Build map of actual containers by name
        actual_map = {container.name: container for container in actual}
        
        # Check for unexpected containers (not in git)
        for container_name, container in actual_map.items():
            if container_name not in expected:
                drift = DriftAlert(
                    timestamp=datetime.utcnow().isoformat(),
                    node=container.node,
                    container_name=container_name,
                    drift_type='UNAUTHORIZED_CONTAINER',
                    expected_state={},
                    actual_state=container.to_dict(),
                    action_taken='PENDING'
                )
                drifts.append(drift)
                logger.warning(f"DRIFT DETECTED: Unauthorized container {container_name} on {container.node}")
        
        # Check for missing containers (in git but not running)
        for expected_name in expected.keys():
            if expected_name not in actual_map:
                drift = DriftAlert(
                    timestamp=datetime.utcnow().isoformat(),
                    node='unknown',
                    container_name=expected_name,
                    drift_type='MISSING_CONTAINER',
                    expected_state=expected[expected_name],
                    actual_state={},
                    action_taken='PENDING'
                )
                drifts.append(drift)
                logger.warning(f"DRIFT DETECTED: Missing container {expected_name}")
        
        # Check for configuration drift
        for container_name, container in actual_map.items():
            if container_name in expected:
                expected_config = expected[container_name]
                # Compare image versions
                expected_image = expected_config.get('spec', {}).get('containers', [{}])[0].get('image', '')
                if expected_image and container.image != expected_image:
                    drift = DriftAlert(
                        timestamp=datetime.utcnow().isoformat(),
                        node=container.node,
                        container_name=container_name,
                        drift_type='IMAGE_DRIFT',
                        expected_state={'image': expected_image},
                        actual_state={'image': container.image},
                        action_taken='PENDING'
                    )
                    drifts.append(drift)
                    logger.warning(f"DRIFT DETECTED: Image drift for {container_name}")
        
        self.detected_drifts.extend(drifts)
        return drifts


class AutoRollback:
    """Automatically rolls back containers to expected state"""
    
    def __init__(self, rollback_path: Path):
        self.rollback_path = rollback_path
        self.rollback_path.mkdir(parents=True, exist_ok=True)
        
    async def rollback_container(self, drift: DriftAlert) -> bool:
        """Execute rollback for a drifted container"""
        logger.info(f"Executing rollback for {drift.container_name}")
        
        if drift.drift_type == 'UNAUTHORIZED_CONTAINER':
            return await self._terminate_container(drift)
        elif drift.drift_type == 'MISSING_CONTAINER':
            return await self._restore_container(drift)
        elif drift.drift_type == 'IMAGE_DRIFT':
            return await self._update_image(drift)
        
        return False
    
    async def _terminate_container(self, drift: DriftAlert) -> bool:
        """Terminate unauthorized container"""
        container_name = drift.container_name
        
        try:
            # Try Docker first
            result = subprocess.run(
                ['docker', 'stop', container_name],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                subprocess.run(['docker', 'rm', container_name], check=False)
                logger.info(f"Terminated unauthorized container: {container_name}")
                return True
            
            # Try Kubernetes
            if '/' in container_name:
                namespace, pod_name = container_name.split('/', 1)
                subprocess.run(
                    ['kubectl', 'delete', 'pod', pod_name, '-n', namespace],
                    capture_output=True,
                    timeout=30
                )
                logger.info(f"Terminated unauthorized pod: {container_name}")
                return True
                
        except Exception as e:
            logger.error(f"Failed to terminate container {container_name}: {e}")
            
        return False
    
    async def _restore_container(self, drift: DriftAlert) -> bool:
        """Restore missing container from expected state"""
        logger.info(f"Restoring container: {drift.container_name}")
        
        # This would apply the manifest from git
        # Implementation depends on whether it's Docker Compose or Kubernetes
        
        return False
    
    async def _update_image(self, drift: DriftAlert) -> bool:
        """Update container to expected image version"""
        logger.info(f"Updating image for: {drift.container_name}")
        
        # This would restart the container with the correct image
        
        return False


class ContainerRefineryBot:
    """
    The main Container Refinery Bot - immune system for Docker/K8s clusters
    
    Responsibilities:
    1. Monitor all containers across all nodes
    2. Detect drift from git source of truth
    3. Auto-rollback unauthorized changes
    4. Maintain immutable ledger
    5. Enforce GitOps workflow
    """
    
    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.running = False
        self.check_interval = 60  # seconds
        
        # Initialize components
        self.git_enforcer = GitOpsEnforcer(config_path / 'manifests')
        self.ledger = ContainerLedger(config_path / 'ledger')
        self.drift_detector = DriftDetector()
        self.rollback_engine = AutoRollback(config_path / 'rollback')
        
        # Load configuration
        self.config = self._load_config()
        
        # Initialize monitors for each node
        self.nodes = self.config.get('nodes', ['local'])
        self.docker_monitors = {node: DockerMonitor(node) for node in self.nodes}
        self.k8s_monitors = {node: KubernetesMonitor(node) for node in self.nodes}
        
        logger.info(f"Container Refinery Bot initialized for nodes: {self.nodes}")
    
    def _load_config(self) -> Dict:
        """Load configuration from bloodline_manifest.yaml"""
        config_file = self.config_path / 'bloodline_manifest.yaml'
        
        if config_file.exists():
            with open(config_file, 'r') as f:
                return yaml.safe_load(f)
        
        # Default configuration
        return {
            'nodes': ['local'],
            'auto_rollback': True,
            'check_interval': 60,
            'enforcement_mode': 'active'
        }
    
    async def monitor_cycle(self):
        """Single monitoring cycle - checks all nodes"""
        logger.info("Starting monitoring cycle...")
        
        # Collect actual state from all nodes
        all_containers = []
        
        for node, docker_monitor in self.docker_monitors.items():
            containers = await docker_monitor.get_running_containers()
            all_containers.extend(containers)
            self.ledger.log_event('DOCKER_SCAN', {
                'node': node,
                'container_count': len(containers)
            })
        
        for node, k8s_monitor in self.k8s_monitors.items():
            pods = await k8s_monitor.get_running_pods()
            all_containers.extend(pods)
            self.ledger.log_event('K8S_SCAN', {
                'node': node,
                'pod_count': len(pods)
            })
        
        logger.info(f"Found {len(all_containers)} containers across all nodes")
        
        # Get expected state from git
        expected_state = self.git_enforcer.get_expected_state()
        logger.info(f"Expected state: {len(expected_state)} containers defined in git")
        
        # Detect drift
        drifts = self.drift_detector.detect_drift(expected_state, all_containers)
        
        if drifts:
            logger.warning(f"DRIFT DETECTED: {len(drifts)} drift events")
            
            # Log all drifts to ledger
            for drift in drifts:
                self.ledger.log_event('DRIFT_DETECTED', drift.to_dict())
            
            # Auto-rollback if enabled
            if self.config.get('auto_rollback', True):
                for drift in drifts:
                    success = await self.rollback_engine.rollback_container(drift)
                    drift.action_taken = 'ROLLED_BACK' if success else 'FAILED'
                    self.ledger.log_event('ROLLBACK', drift.to_dict())
        else:
            logger.info("No drift detected - all containers compliant")
        
        # Commit ledger to git
        self.git_enforcer.commit_changes(f"Refinery cycle - {len(all_containers)} containers, {len(drifts)} drifts")
    
    async def run(self):
        """Main run loop - monitors continuously"""
        self.running = True
        logger.info("🧠⚔️🔥 Container Refinery Bot starting... The immune system is online.")
        
        self.ledger.log_event('BOT_STARTED', {
            'nodes': self.nodes,
            'config': self.config
        })
        
        cycle_count = 0
        
        try:
            while self.running:
                cycle_count += 1
                logger.info(f"=== Monitoring Cycle #{cycle_count} ===")
                
                try:
                    await self.monitor_cycle()
                except Exception as e:
                    logger.error(f"Error in monitoring cycle: {e}", exc_info=True)
                    self.ledger.log_event('ERROR', {
                        'cycle': cycle_count,
                        'error': str(e)
                    })
                
                # Wait for next cycle
                logger.info(f"Next cycle in {self.check_interval} seconds...")
                await asyncio.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            logger.info("Shutdown signal received")
        finally:
            self.running = False
            self.ledger.log_event('BOT_STOPPED', {
                'cycles_completed': cycle_count
            })
            logger.info("Container Refinery Bot stopped")
    
    def stop(self):
        """Stop the monitoring loop"""
        self.running = False


async def main():
    """Main entry point"""
    # Get refinery path from environment or use platform-appropriate default
    import os
    import platform
    
    # Default path based on OS
    if platform.system() == 'Windows':
        default_path = r'C:\legends_of_minds\refineries\container_refinery'
    else:
        default_path = '/app/container_refinery'
    
    refinery_path = Path(os.getenv('REFINERY_PATH', default_path))
    
    # Create refinery instance
    bot = ContainerRefineryBot(refinery_path)
    
    # Run the bot
    await bot.run()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Received shutdown signal")
        sys.exit(0)
