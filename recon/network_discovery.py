#!/usr/bin/env python3
"""
network_discovery.py - Advanced Network Discovery & Service Mapping
Strategic Khaos Sovereignty Architecture
"""

import subprocess
import json
import socket
import sys
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import urllib.request
import urllib.error

class NetworkDiscovery:
    """Comprehensive network discovery and service mapping"""
    
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.services = []
        self.networks = []
        self.containers = []
        
    def run_command(self, cmd: List[str]) -> Tuple[Optional[str], Optional[str]]:
        """Execute shell command and return stdout, stderr"""
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.stdout, result.stderr
        except Exception as e:
            return None, str(e)
    
    def check_port(self, host: str, port: int, timeout: float = 2.0) -> bool:
        """Check if a port is open"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except Exception:
            return False
    
    def check_http_endpoint(self, url: str, timeout: int = 5) -> Dict:
        """Check HTTP endpoint and return status"""
        try:
            req = urllib.request.Request(url, method='GET')
            start = datetime.now()
            response = urllib.request.urlopen(req, timeout=timeout)
            end = datetime.now()
            
            return {
                'url': url,
                'status': response.getcode(),
                'response_time_ms': int((end - start).total_seconds() * 1000),
                'available': True
            }
        except urllib.error.HTTPError as e:
            return {
                'url': url,
                'status': e.code,
                'response_time_ms': 0,
                'available': False,
                'error': str(e)
            }
        except Exception as e:
            return {
                'url': url,
                'status': 0,
                'response_time_ms': 0,
                'available': False,
                'error': str(e)
            }
    
    def discover_docker_networks(self) -> List[Dict]:
        """Discover all Docker networks"""
        print("🔍 Discovering Docker networks...")
        
        stdout, stderr = self.run_command([
            'docker', 'network', 'ls', '--format', '{{json .}}'
        ])
        
        if not stdout:
            print("⚠️  No Docker networks found or Docker not available")
            return []
        
        networks = []
        for line in stdout.strip().split('\n'):
            if line:
                try:
                    network = json.loads(line)
                    
                    # Get detailed network info
                    detail_stdout, _ = self.run_command([
                        'docker', 'network', 'inspect', network['Name']
                    ])
                    
                    if detail_stdout:
                        detail = json.loads(detail_stdout)[0]
                        networks.append({
                            'name': network['Name'],
                            'driver': network['Driver'],
                            'scope': network['Scope'],
                            'subnet': detail.get('IPAM', {}).get('Config', [{}])[0].get('Subnet', 'N/A'),
                            'containers': len(detail.get('Containers', {}))
                        })
                except Exception as e:
                    print(f"⚠️  Error parsing network: {e}")
        
        print(f"✓ Found {len(networks)} networks")
        self.networks = networks
        return networks
    
    def discover_containers(self) -> List[Dict]:
        """Discover all Docker containers"""
        print("🐳 Discovering Docker containers...")
        
        stdout, stderr = self.run_command([
            'docker', 'ps', '-a', '--format', '{{json .}}'
        ])
        
        if not stdout:
            print("⚠️  No containers found")
            return []
        
        containers = []
        for line in stdout.strip().split('\n'):
            if line:
                try:
                    container = json.loads(line)
                    
                    # Get detailed container info
                    detail_stdout, _ = self.run_command([
                        'docker', 'inspect', container['Names']
                    ])
                    
                    if detail_stdout:
                        detail = json.loads(detail_stdout)[0]
                        
                        # Extract network info
                        networks = list(detail.get('NetworkSettings', {}).get('Networks', {}).keys())
                        
                        # Extract port mappings
                        ports = []
                        port_bindings = detail.get('NetworkSettings', {}).get('Ports', {})
                        if port_bindings:
                            for internal, external in port_bindings.items():
                                if external:
                                    for binding in external:
                                        ports.append({
                                            'internal': internal,
                                            'external': f"{binding.get('HostIp', '0.0.0.0')}:{binding.get('HostPort', 'N/A')}"
                                        })
                        
                        containers.append({
                            'name': container['Names'],
                            'image': container['Image'],
                            'status': container['Status'],
                            'state': container['State'],
                            'networks': networks,
                            'ports': ports,
                            'created': detail.get('Created', 'N/A')
                        })
                except Exception as e:
                    print(f"⚠️  Error parsing container: {e}")
        
        print(f"✓ Found {len(containers)} containers")
        self.containers = containers
        return containers
    
    def discover_services(self) -> List[Dict]:
        """Discover all services and check their availability"""
        print("🏥 Discovering services...")
        
        # Define known services
        known_services = [
            {'name': 'Event Gateway', 'host': 'localhost', 'port': 8080, 'http': 'http://localhost:8080/health'},
            {'name': 'Refinory API', 'host': 'localhost', 'port': 8085, 'http': 'http://localhost:8085/health'},
            {'name': 'RAG Retriever', 'host': 'localhost', 'port': 7000, 'http': 'http://localhost:7000/health'},
            {'name': 'Qdrant Vector DB', 'host': 'localhost', 'port': 6333, 'http': 'http://localhost:6333/healthz'},
            {'name': 'Embedder Service', 'host': 'localhost', 'port': 8081, 'http': 'http://localhost:8081/health'},
            {'name': 'Grafana', 'host': 'localhost', 'port': 3000, 'http': 'http://localhost:3000/api/health'},
            {'name': 'Prometheus', 'host': 'localhost', 'port': 9090, 'http': 'http://localhost:9090/-/healthy'},
            {'name': 'PostgreSQL', 'host': 'localhost', 'port': 5432, 'http': None},
            {'name': 'Redis', 'host': 'localhost', 'port': 6379, 'http': None},
            {'name': 'Nginx', 'host': 'localhost', 'port': 80, 'http': None},
        ]
        
        services = []
        for service in known_services:
            print(f"  Checking {service['name']}...", end=' ')
            
            # Check port first
            port_open = self.check_port(service['host'], service['port'])
            
            service_info = {
                'name': service['name'],
                'host': service['host'],
                'port': service['port'],
                'port_open': port_open
            }
            
            # If HTTP endpoint exists, check it
            if service['http'] and port_open:
                http_result = self.check_http_endpoint(service['http'])
                service_info.update({
                    'http_available': http_result['available'],
                    'http_status': http_result.get('status', 0),
                    'response_time_ms': http_result.get('response_time_ms', 0)
                })
                
                if http_result['available']:
                    print(f"✓ UP (HTTP {http_result['status']}, {http_result['response_time_ms']}ms)")
                else:
                    print(f"⚠️  Port open but HTTP failed")
            elif port_open:
                print("✓ UP (Port open)")
            else:
                print("✗ DOWN")
            
            services.append(service_info)
        
        self.services = services
        return services
    
    def generate_report(self) -> str:
        """Generate comprehensive discovery report"""
        report = []
        report.append("# Network Discovery Report")
        report.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"**Scan ID:** {self.timestamp}")
        report.append("")
        report.append("---")
        report.append("")
        
        # Networks
        report.append("## 🌐 Discovered Networks")
        report.append("")
        report.append("| Network | Driver | Scope | Subnet | Containers |")
        report.append("|---------|--------|-------|--------|------------|")
        for net in self.networks:
            report.append(f"| {net['name']} | {net['driver']} | {net['scope']} | {net['subnet']} | {net['containers']} |")
        report.append("")
        
        # Containers
        report.append("## 🐳 Discovered Containers")
        report.append("")
        report.append("| Name | Status | Image | Networks | Ports |")
        report.append("|------|--------|-------|----------|-------|")
        for container in self.containers:
            ports_str = ", ".join([f"{p['internal']}→{p['external']}" for p in container['ports']]) if container['ports'] else "None"
            networks_str = ", ".join(container['networks']) if container['networks'] else "None"
            report.append(f"| {container['name']} | {container['state']} | {container['image']} | {networks_str} | {ports_str} |")
        report.append("")
        
        # Services
        report.append("## 🏥 Service Status")
        report.append("")
        report.append("| Service | Host | Port | Status | Response Time |")
        report.append("|---------|------|------|--------|---------------|")
        for service in self.services:
            if service['port_open']:
                if 'http_available' in service:
                    status = f"✅ UP (HTTP {service['http_status']})" if service['http_available'] else "⚠️ Port open"
                    response_time = f"{service.get('response_time_ms', 0)}ms" if service.get('http_available') else "N/A"
                else:
                    status = "✅ UP"
                    response_time = "N/A"
            else:
                status = "❌ DOWN"
                response_time = "N/A"
            
            report.append(f"| {service['name']} | {service['host']} | {service['port']} | {status} | {response_time} |")
        report.append("")
        
        # Summary
        report.append("## 📊 Summary")
        report.append("")
        active_services = sum(1 for s in self.services if s['port_open'])
        running_containers = sum(1 for c in self.containers if c['state'].lower() == 'running')
        
        report.append(f"- **Active Services:** {active_services} / {len(self.services)}")
        report.append(f"- **Running Containers:** {running_containers} / {len(self.containers)}")
        report.append(f"- **Networks:** {len(self.networks)}")
        report.append("")
        
        return "\n".join(report)
    
    def save_report(self, filename: str):
        """Save report to file"""
        report = self.generate_report()
        with open(filename, 'w') as f:
            f.write(report)
        print(f"✓ Report saved to {filename}")
    
    def run_full_discovery(self):
        """Run complete network discovery"""
        print("🎯 Starting comprehensive network discovery...")
        print("")
        
        self.discover_docker_networks()
        self.discover_containers()
        self.discover_services()
        
        print("")
        print("✨ Discovery complete!")
        print("")
        
        # Generate and save report
        report_file = f"recon/reports/network_discovery_{self.timestamp}.md"
        self.save_report(report_file)
        
        # Print summary
        print("📊 Summary:")
        print(f"  - Networks: {len(self.networks)}")
        print(f"  - Containers: {len(self.containers)}")
        print(f"  - Services checked: {len(self.services)}")
        print(f"  - Active services: {sum(1 for s in self.services if s['port_open'])}")
        print("")
        print(f"📄 Full report: {report_file}")

def main():
    """Main entry point"""
    try:
        discovery = NetworkDiscovery()
        discovery.run_full_discovery()
        return 0
    except KeyboardInterrupt:
        print("\n\n⚠️  Discovery interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Error during discovery: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
