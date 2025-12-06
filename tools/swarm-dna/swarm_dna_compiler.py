#!/usr/bin/env python3
"""
Swarm DNA Compiler - Lore to Configuration Compiler

Transforms narrative-rich SWARM_DNA.yaml files into operational configs
for different subsystems. This embodies Dom's philosophy: lore IS firmware.

The compiler bridges mythological narrative and technical reality.

Built for Strategickhaos Swarm Intelligence
"""

import os
import sys
import yaml
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


class SwarmDNACompiler:
    """Compile Swarm DNA lore into operational configurations"""
    
    def __init__(self, swarm_dna_file: str):
        self.swarm_dna_file = Path(swarm_dna_file)
        self.swarm_dna = None
        self.load_swarm_dna()
        
    def load_swarm_dna(self):
        """Load SWARM_DNA.yaml"""
        if not self.swarm_dna_file.exists():
            raise FileNotFoundError(f"SWARM_DNA.yaml not found: {self.swarm_dna_file}")
            
        with open(self.swarm_dna_file, 'r') as f:
            self.swarm_dna = yaml.safe_load(f)
            
    def compile_to_docker_compose(self) -> Dict[str, Any]:
        """Generate docker-compose.yml from Swarm DNA"""
        identity = self.swarm_dna.get('swarm_identity', {})
        infra = self.swarm_dna.get('technical_infrastructure', {})
        
        services = {}
        
        # Add observability stack if configured
        obs = infra.get('observability', {})
        if obs.get('metrics') == 'Prometheus':
            services['prometheus'] = {
                'image': 'prom/prometheus:latest',
                'ports': ['9090:9090'],
                'volumes': ['./monitoring/prometheus:/etc/prometheus'],
                'command': ['--config.file=/etc/prometheus/prometheus.yml'],
                'restart': 'unless-stopped',
            }
            
        if obs.get('logging') == 'Loki':
            services['loki'] = {
                'image': 'grafana/loki:latest',
                'ports': ['3100:3100'],
                'restart': 'unless-stopped',
            }
            
        if obs.get('visualization') == 'Grafana':
            depends_on = []
            if 'prometheus' in services:
                depends_on.append('prometheus')
            if 'loki' in services:
                depends_on.append('loki')
            
            services['grafana'] = {
                'image': 'grafana/grafana:latest',
                'ports': ['3000:3000'],
                'environment': [
                    'GF_SECURITY_ADMIN_PASSWORD=admin',
                    'GF_INSTALL_PLUGINS=grafana-piechart-panel',
                ],
                'volumes': ['./monitoring/grafana:/etc/grafana'],
                'depends_on': depends_on,
                'restart': 'unless-stopped',
            }
            
        # Add data intelligence components
        data = self.swarm_dna.get('swarm_components', {}).get('data_intelligence', {})
        rag = data.get('rag_system', {})
        
        if rag.get('vector_db') == 'Qdrant':
            services['qdrant'] = {
                'image': 'qdrant/qdrant:latest',
                'ports': ['6333:6333', '6334:6334'],
                'volumes': ['./data/qdrant:/qdrant/storage'],
                'restart': 'unless-stopped',
            }
            
        return {
            'version': '3.8',
            'services': services,
            'networks': {
                'swarm_network': {
                    'driver': 'bridge',
                },
            },
            'volumes': {
                'prometheus_data': {},
                'grafana_data': {},
                'qdrant_data': {},
            },
        }
        
    def compile_to_kubernetes(self) -> Dict[str, Any]:
        """Generate Kubernetes manifests from Swarm DNA"""
        identity = self.swarm_dna.get('swarm_identity', {})
        
        manifests = []
        
        # Namespace
        manifests.append({
            'apiVersion': 'v1',
            'kind': 'Namespace',
            'metadata': {
                'name': 'swarm-dna',
                'labels': {
                    'swarm.codename': identity.get('codename', 'unknown'),
                    'swarm.version': str(identity.get('version', '1.0')),
                },
            },
        })
        
        # ConfigMap with Swarm DNA
        manifests.append({
            'apiVersion': 'v1',
            'kind': 'ConfigMap',
            'metadata': {
                'name': 'swarm-dna-config',
                'namespace': 'swarm-dna',
            },
            'data': {
                'SWARM_CODENAME': identity.get('codename', 'unknown'),
                'SWARM_VERSION': str(identity.get('version', '1.0')),
                'EIN': identity.get('legal_entity', {}).get('ein', ''),
            },
        })
        
        return manifests
        
    def compile_to_github_actions(self) -> Dict[str, Any]:
        """Generate GitHub Actions workflow from Swarm DNA"""
        identity = self.swarm_dna.get('swarm_identity', {})
        components = self.swarm_dna.get('swarm_components', {})
        
        workflow = {
            'name': f"Swarm DNA - {identity.get('codename', 'Unknown')}",
            'on': {
                'push': {'branches': ['main', 'develop']},
                'schedule': [{'cron': '0 2 * * *'}],  # Daily at 2 AM
            },
            'jobs': {
                'swarm-validation': {
                    'runs-on': 'ubuntu-latest',
                    'steps': [
                        {'uses': 'actions/checkout@v4'},
                        {
                            'name': 'Validate Swarm DNA',
                            'run': 'python tools/swarm-dna/validate_swarm_dna.py',
                        },
                    ],
                },
            },
        }
        
        # Add security verification if configured
        security = components.get('security_sovereignty', {})
        crypto = security.get('cryptographic_verification', [])
        
        if 'GPG signatures' in crypto:
            workflow['jobs']['swarm-validation']['steps'].append({
                'name': 'Verify GPG Signatures',
                'run': 'gpg --verify SWARM_DNA.yaml.asc SWARM_DNA.yaml',
            })
            
        return workflow
        
    def compile_to_prometheus_config(self) -> Dict[str, Any]:
        """Generate Prometheus configuration from Swarm DNA"""
        infra = self.swarm_dna.get('technical_infrastructure', {})
        
        config = {
            'global': {
                'scrape_interval': '15s',
                'evaluation_interval': '15s',
            },
            'scrape_configs': [],
        }
        
        # Add control plane endpoints
        control_plane = infra.get('control_plane', {})
        if control_plane:
            config['scrape_configs'].append({
                'job_name': 'swarm-control-plane',
                'static_configs': [
                    {'targets': ['localhost:9090']},
                ],
            })
            
        return config
        
    def compile_to_discovery_yml(self) -> Dict[str, Any]:
        """Generate discovery.yml for repository from Swarm DNA"""
        identity = self.swarm_dna.get('swarm_identity', {})
        infra = self.swarm_dna.get('technical_infrastructure', {})
        
        org_name = identity.get('legal_entity', {}).get('name', 'Unknown')
        operator = self.swarm_dna.get('metadata', {}).get('operator', {})
        
        discovery = {
            'org': {
                'name': org_name,
                'contact': {
                    'owner': operator.get('name', 'Unknown'),
                },
            },
        }
        
        # Add Discord channels if configured
        control_plane = infra.get('control_plane', {})
        if control_plane.get('interface') == 'Discord DevOps':
            channels = control_plane.get('channels', [])
            discovery['discord'] = {
                'guild_id': None,
                'channels': {ch.replace('#', ''): ch for ch in channels},
            }
            
        return discovery
        
    def compile_all(self, output_dir: str = 'compiled'):
        """Compile Swarm DNA to all supported formats"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        results = {}
        
        # Docker Compose
        docker_compose = self.compile_to_docker_compose()
        dc_path = output_path / 'docker-compose.swarm.yml'
        with open(dc_path, 'w') as f:
            yaml.dump(docker_compose, f, default_flow_style=False)
        results['docker_compose'] = str(dc_path)
        
        # Kubernetes
        k8s_manifests = self.compile_to_kubernetes()
        k8s_path = output_path / 'kubernetes-swarm.yaml'
        with open(k8s_path, 'w') as f:
            for manifest in k8s_manifests:
                yaml.dump(manifest, f, default_flow_style=False)
                f.write('\n---\n')
        results['kubernetes'] = str(k8s_path)
        
        # GitHub Actions
        gh_workflow = self.compile_to_github_actions()
        gh_path = output_path / 'swarm-dna-workflow.yml'
        with open(gh_path, 'w') as f:
            yaml.dump(gh_workflow, f, default_flow_style=False)
        results['github_actions'] = str(gh_path)
        
        # Prometheus
        prom_config = self.compile_to_prometheus_config()
        prom_path = output_path / 'prometheus-swarm.yml'
        with open(prom_path, 'w') as f:
            yaml.dump(prom_config, f, default_flow_style=False)
        results['prometheus'] = str(prom_path)
        
        # Discovery
        discovery = self.compile_to_discovery_yml()
        disc_path = output_path / 'discovery-swarm.yml'
        with open(disc_path, 'w') as f:
            yaml.dump(discovery, f, default_flow_style=False)
        results['discovery'] = str(disc_path)
        
        return results


def main():
    """CLI interface for Swarm DNA compiler"""
    if len(sys.argv) < 2:
        print("Usage: swarm_dna_compiler.py <SWARM_DNA.yaml> [output_dir]")
        print()
        print("Examples:")
        print("  swarm_dna_compiler.py SWARM_DNA.yaml")
        print("  swarm_dna_compiler.py SWARM_DNA.yaml ./compiled-configs")
        sys.exit(1)
        
    swarm_dna_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else 'compiled'
    
    print(f"🧬 Compiling Swarm DNA: {swarm_dna_file}")
    print(f"📦 Output directory: {output_dir}")
    print()
    
    compiler = SwarmDNACompiler(swarm_dna_file)
    results = compiler.compile_all(output_dir)
    
    print("✅ Compilation complete!")
    print()
    print("Generated configurations:")
    for config_type, path in results.items():
        print(f"  • {config_type:20s} → {path}")
        
    print()
    print("🔥 Lore has been transformed into operational reality.")
    print("   This is Dom's architecture made manifest.")


if __name__ == '__main__':
    main()
