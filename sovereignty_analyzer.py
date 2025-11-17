#!/usr/bin/env python3
"""
Sovereignty Analyzer - Advanced Analysis Tools
Version: 1.0.0
Purpose: Python-based advanced analysis for reverse engineering and sovereignty assessment
"""

import json
import sys
import argparse
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import hashlib
import re


class SovereigntyAnalyzer:
    """Main analyzer class for sovereignty assessment"""
    
    def __init__(self, vault_path: str = None):
        self.vault_path = Path(vault_path or os.path.expanduser("~/obsidian/vault"))
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def analyze_har_file(self, har_path: str) -> Dict[str, Any]:
        """Analyze HAR file for security and performance metrics"""
        print(f"[INFO] Analyzing HAR file: {har_path}")
        
        with open(har_path, 'r') as f:
            har_data = json.load(f)
        
        entries = har_data.get('log', {}).get('entries', [])
        
        analysis = {
            'timestamp': self.timestamp,
            'total_requests': len(entries),
            'security': self._analyze_security(entries),
            'performance': self._analyze_performance(entries),
            'resources': self._analyze_resources(entries),
            'vulnerabilities': self._check_vulnerabilities(entries),
        }
        
        return analysis
    
    def _analyze_security(self, entries: List[Dict]) -> Dict[str, Any]:
        """Analyze security aspects of requests"""
        security_headers = [
            'strict-transport-security',
            'content-security-policy',
            'x-frame-options',
            'x-content-type-options',
            'x-xss-protection',
            'referrer-policy',
            'permissions-policy'
        ]
        
        https_count = 0
        header_presence = {header: 0 for header in security_headers}
        insecure_cookies = 0
        
        for entry in entries:
            # Check HTTPS
            if entry['request']['url'].startswith('https://'):
                https_count += 1
            
            # Check security headers
            for header in entry['response']['headers']:
                header_name = header['name'].lower()
                if header_name in security_headers:
                    header_presence[header_name] += 1
            
            # Check cookies
            for cookie in entry['response'].get('cookies', []):
                if not cookie.get('secure', False):
                    insecure_cookies += 1
        
        return {
            'https_percentage': (https_count / len(entries) * 100) if entries else 0,
            'security_headers': header_presence,
            'insecure_cookies': insecure_cookies,
            'total_requests': len(entries),
        }
    
    def _analyze_performance(self, entries: List[Dict]) -> Dict[str, Any]:
        """Analyze performance metrics"""
        times = [entry['time'] for entry in entries]
        sizes = [entry['response'].get('bodySize', 0) for entry in entries]
        
        return {
            'avg_response_time': sum(times) / len(times) if times else 0,
            'max_response_time': max(times) if times else 0,
            'min_response_time': min(times) if times else 0,
            'total_size': sum(sizes),
            'avg_size': sum(sizes) / len(sizes) if sizes else 0,
            'request_count': len(entries),
        }
    
    def _analyze_resources(self, entries: List[Dict]) -> Dict[str, Any]:
        """Analyze resource types and usage"""
        mime_types = {}
        domains = {}
        
        for entry in entries:
            # Count MIME types
            mime_type = entry['response']['content'].get('mimeType', 'unknown')
            mime_types[mime_type] = mime_types.get(mime_type, 0) + 1
            
            # Count domains
            url = entry['request']['url']
            domain = url.split('/')[2] if '/' in url else 'unknown'
            domains[domain] = domains.get(domain, 0) + 1
        
        return {
            'mime_types': mime_types,
            'domains': domains,
            'unique_domains': len(domains),
        }
    
    def _check_vulnerabilities(self, entries: List[Dict]) -> List[Dict[str, str]]:
        """Check for common vulnerabilities"""
        vulnerabilities = []
        
        for entry in entries:
            url = entry['request']['url']
            
            # Check for sensitive data in URLs
            if any(keyword in url.lower() for keyword in ['password', 'token', 'api_key', 'secret']):
                vulnerabilities.append({
                    'type': 'sensitive_data_in_url',
                    'severity': 'high',
                    'url': url,
                    'description': 'Sensitive data detected in URL'
                })
            
            # Check for unencrypted requests
            if url.startswith('http://') and not url.startswith('http://localhost'):
                vulnerabilities.append({
                    'type': 'unencrypted_connection',
                    'severity': 'high',
                    'url': url,
                    'description': 'Unencrypted HTTP connection'
                })
            
            # Check for missing security headers
            headers = {h['name'].lower(): h['value'] for h in entry['response']['headers']}
            if 'strict-transport-security' not in headers and url.startswith('https://'):
                vulnerabilities.append({
                    'type': 'missing_hsts',
                    'severity': 'medium',
                    'url': url,
                    'description': 'Missing HSTS header'
                })
        
        return vulnerabilities
    
    def compare_versions(self, original_har: str, sovereign_har: str) -> Dict[str, Any]:
        """Compare original and sovereign versions"""
        print(f"[INFO] Comparing versions...")
        
        original = self.analyze_har_file(original_har)
        sovereign = self.analyze_har_file(sovereign_har)
        
        comparison = {
            'timestamp': self.timestamp,
            'performance_diff': {
                'response_time': {
                    'original': original['performance']['avg_response_time'],
                    'sovereign': sovereign['performance']['avg_response_time'],
                    'improvement_pct': self._calc_improvement(
                        original['performance']['avg_response_time'],
                        sovereign['performance']['avg_response_time']
                    )
                },
                'total_size': {
                    'original': original['performance']['total_size'],
                    'sovereign': sovereign['performance']['total_size'],
                    'improvement_pct': self._calc_improvement(
                        original['performance']['total_size'],
                        sovereign['performance']['total_size']
                    )
                }
            },
            'security_diff': {
                'vulnerabilities': {
                    'original': len(original['vulnerabilities']),
                    'sovereign': len(sovereign['vulnerabilities']),
                    'reduction_pct': self._calc_improvement(
                        len(original['vulnerabilities']),
                        len(sovereign['vulnerabilities'])
                    )
                },
                'https_usage': {
                    'original': original['security']['https_percentage'],
                    'sovereign': sovereign['security']['https_percentage'],
                }
            }
        }
        
        return comparison
    
    def _calc_improvement(self, original: float, sovereign: float) -> float:
        """Calculate improvement percentage (negative means worse)"""
        if original == 0:
            return 0
        return ((original - sovereign) / original) * 100
    
    def generate_obsidian_note(self, analysis: Dict[str, Any], output_path: str):
        """Generate Obsidian markdown note from analysis"""
        note = f"""# Sovereignty Analysis Report

## Overview
- **Timestamp**: {analysis['timestamp']}
- **Total Requests**: {analysis['total_requests']}

## Security Analysis

### HTTPS Usage
- **Percentage**: {analysis['security']['https_percentage']:.2f}%
- **Insecure Cookies**: {analysis['security']['insecure_cookies']}

### Security Headers
"""
        for header, count in analysis['security']['security_headers'].items():
            note += f"- **{header}**: {count} occurrences\n"
        
        note += f"""
## Performance Metrics
- **Average Response Time**: {analysis['performance']['avg_response_time']:.2f}ms
- **Max Response Time**: {analysis['performance']['max_response_time']:.2f}ms
- **Total Size**: {analysis['performance']['total_size']:,} bytes
- **Average Size**: {analysis['performance']['avg_size']:.2f} bytes

## Resource Analysis
- **Unique Domains**: {analysis['resources']['unique_domains']}

### MIME Types
"""
        for mime_type, count in sorted(analysis['resources']['mime_types'].items(), 
                                       key=lambda x: x[1], reverse=True):
            note += f"- **{mime_type}**: {count}\n"
        
        note += f"""
## Vulnerabilities Detected
Total: {len(analysis['vulnerabilities'])}

"""
        
        for vuln in analysis['vulnerabilities']:
            note += f"""### {vuln['type']} ({vuln['severity']})
- **URL**: {vuln['url']}
- **Description**: {vuln['description']}

"""
        
        note += """
## Recommendations
1. Enable HTTPS for all connections
2. Implement all security headers
3. Use secure cookies
4. Regular security audits
5. Performance optimization

---
Tags: #sovereignty-analysis #security #performance
"""
        
        # Save note
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(note)
        
        print(f"[SUCCESS] Analysis note saved to: {output_path}")
    
    def export_json(self, data: Dict[str, Any], output_path: str):
        """Export analysis data as JSON"""
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"[SUCCESS] JSON exported to: {output_path}")


class DependencyAnalyzer:
    """Analyze software dependencies for vulnerabilities"""
    
    def __init__(self):
        self.known_vulns = self._load_known_vulns()
    
    def _load_known_vulns(self) -> Dict[str, List[str]]:
        """Load known vulnerability database (simplified)"""
        # In production, this would load from CVE database
        return {
            'example-package': ['CVE-2023-12345'],
        }
    
    def analyze_npm_package_json(self, package_json_path: str) -> Dict[str, Any]:
        """Analyze npm package.json for vulnerabilities"""
        with open(package_json_path, 'r') as f:
            package_data = json.load(f)
        
        dependencies = package_data.get('dependencies', {})
        dev_dependencies = package_data.get('devDependencies', {})
        
        all_deps = {**dependencies, **dev_dependencies}
        
        results = {
            'total_dependencies': len(all_deps),
            'dependencies': all_deps,
            'vulnerabilities': [],
            'recommendations': []
        }
        
        # Check each dependency
        for dep_name, dep_version in all_deps.items():
            if dep_name in self.known_vulns:
                results['vulnerabilities'].append({
                    'package': dep_name,
                    'version': dep_version,
                    'cves': self.known_vulns[dep_name]
                })
        
        return results


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Sovereignty Analyzer - Advanced Analysis Tools',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze HAR file
  %(prog)s analyze-har capture.har
  
  # Compare versions
  %(prog)s compare original.har sovereign.har
  
  # Analyze dependencies
  %(prog)s analyze-deps package.json
        """
    )
    
    parser.add_argument('command', choices=['analyze-har', 'compare', 'analyze-deps'],
                       help='Command to execute')
    parser.add_argument('files', nargs='+', help='Input file(s)')
    parser.add_argument('--vault', default=None, help='Obsidian vault path')
    parser.add_argument('--output', default=None, help='Output file path')
    
    args = parser.parse_args()
    
    try:
        if args.command == 'analyze-har':
            analyzer = SovereigntyAnalyzer(args.vault)
            analysis = analyzer.analyze_har_file(args.files[0])
            
            # Generate outputs
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_base = args.output or f"analysis_{timestamp}"
            
            analyzer.generate_obsidian_note(
                analysis, 
                f"{analyzer.vault_path}/analysis/security/{timestamp}/report.md"
            )
            analyzer.export_json(
                analysis,
                f"{analyzer.vault_path}/analysis/security/{timestamp}/data.json"
            )
            
            print("\n[SUCCESS] Analysis complete!")
            print(f"- Vulnerabilities found: {len(analysis['vulnerabilities'])}")
            print(f"- HTTPS usage: {analysis['security']['https_percentage']:.2f}%")
            print(f"- Average response time: {analysis['performance']['avg_response_time']:.2f}ms")
        
        elif args.command == 'compare':
            if len(args.files) < 2:
                print("[ERROR] Compare requires 2 HAR files")
                return 1
            
            analyzer = SovereigntyAnalyzer(args.vault)
            comparison = analyzer.compare_versions(args.files[0], args.files[1])
            
            print("\n[SUCCESS] Comparison complete!")
            print(f"Performance improvement: {comparison['performance_diff']['response_time']['improvement_pct']:.2f}%")
            print(f"Vulnerability reduction: {comparison['security_diff']['vulnerabilities']['reduction_pct']:.2f}%")
            
            # Export comparison
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            analyzer.export_json(
                comparison,
                f"{analyzer.vault_path}/analysis/comparisons/{timestamp}/comparison.json"
            )
        
        elif args.command == 'analyze-deps':
            dep_analyzer = DependencyAnalyzer()
            results = dep_analyzer.analyze_npm_package_json(args.files[0])
            
            print("\n[INFO] Dependency Analysis")
            print(f"Total dependencies: {results['total_dependencies']}")
            print(f"Vulnerabilities found: {len(results['vulnerabilities'])}")
            
            for vuln in results['vulnerabilities']:
                print(f"\n[WARNING] {vuln['package']} {vuln['version']}")
                print(f"  CVEs: {', '.join(vuln['cves'])}")
        
        return 0
    
    except Exception as e:
        print(f"[ERROR] {str(e)}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
