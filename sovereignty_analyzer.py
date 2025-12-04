#!/usr/bin/env python3
"""
Sovereignty Analyzer
Version: 1.0.0

A comprehensive Python tool for analyzing HAR files and comparing
original vs sovereign implementations for security and performance.

Usage:
    ./sovereignty_analyzer.py analyze-har <har_file>
    ./sovereignty_analyzer.py compare <original.har> <sovereign.har>
    ./sovereignty_analyzer.py report --type <type> --output <path>
"""

import json
import sys
import os
import argparse
from datetime import datetime
from collections import defaultdict
from typing import Any
from urllib.parse import urlparse

# =============================================================================
# Constants
# =============================================================================

VERSION = "1.0.0"

REQUIRED_SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Content-Type-Options",
    "X-Frame-Options",
    "X-XSS-Protection"
]

RECOMMENDED_SECURITY_HEADERS = [
    "Referrer-Policy",
    "Permissions-Policy",
    "Cross-Origin-Opener-Policy",
    "Cross-Origin-Resource-Policy",
    "Cross-Origin-Embedder-Policy"
]

SECURE_COOKIE_FLAGS = ["HttpOnly", "Secure", "SameSite"]

# Colors for terminal output
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    PURPLE = '\033[0;35m'
    CYAN = '\033[0;36m'
    NC = '\033[0m'  # No Color


# =============================================================================
# Utility Functions
# =============================================================================

def print_header(title: str, color: str = Colors.CYAN) -> None:
    """Print a formatted header."""
    print(f"{color}")
    print("╔" + "═" * 67 + "╗")
    print(f"║{title:^67}║")
    print("╚" + "═" * 67 + "╝")
    print(f"{Colors.NC}")


def print_section(title: str) -> None:
    """Print a section header."""
    print(f"\n{Colors.CYAN}=== {title} ==={Colors.NC}\n")


def success(msg: str) -> None:
    """Print success message."""
    print(f"  {Colors.GREEN}✓{Colors.NC} {msg}")


def warning(msg: str) -> None:
    """Print warning message."""
    print(f"  {Colors.YELLOW}⚠{Colors.NC} {msg}")


def error(msg: str) -> None:
    """Print error message."""
    print(f"  {Colors.RED}✗{Colors.NC} {msg}")


def info(msg: str) -> None:
    """Print info message."""
    print(f"  {Colors.BLUE}ℹ{Colors.NC} {msg}")


def load_har(filepath: str) -> dict[str, Any]:
    """Load and parse a HAR file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"{Colors.RED}Error: Invalid JSON in HAR file: {e}{Colors.NC}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"{Colors.RED}Error: HAR file not found: {filepath}{Colors.NC}")
        sys.exit(1)


def format_bytes(num: int) -> str:
    """Format bytes to human readable string."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if abs(num) < 1024.0:
            return f"{num:,.1f} {unit}"
        num /= 1024.0
    return f"{num:,.1f} TB"


def format_time(ms: float) -> str:
    """Format milliseconds to human readable string."""
    if ms < 1000:
        return f"{ms:.1f}ms"
    elif ms < 60000:
        return f"{ms/1000:.2f}s"
    else:
        return f"{ms/60000:.2f}min"


# =============================================================================
# HAR Analysis
# =============================================================================

class HARAnalyzer:
    """Analyzer for HAR (HTTP Archive) files."""
    
    def __init__(self, har_data: dict[str, Any]):
        self.har = har_data
        self.entries = har_data.get('log', {}).get('entries', [])
        self.findings: dict[str, list[str]] = defaultdict(list)
        
    def analyze(self) -> dict[str, Any]:
        """Run all analysis methods."""
        results = {
            'statistics': self.get_statistics(),
            'security': self.analyze_security(),
            'performance': self.analyze_performance(),
            'endpoints': self.analyze_endpoints(),
            'findings': dict(self.findings)
        }
        return results
    
    def get_statistics(self) -> dict[str, Any]:
        """Get basic statistics about the HAR file."""
        stats = {
            'total_requests': len(self.entries),
            'total_size': 0,
            'content_types': defaultdict(int),
            'domains': set(),
            'methods': defaultdict(int),
            'status_codes': defaultdict(int)
        }
        
        for entry in self.entries:
            request = entry.get('request', {})
            response = entry.get('response', {})
            
            # URL and domain
            url = request.get('url', '')
            parsed = urlparse(url)
            if parsed.netloc:
                stats['domains'].add(parsed.netloc)
            
            # Method
            method = request.get('method', 'UNKNOWN')
            stats['methods'][method] += 1
            
            # Status code
            status = response.get('status', 0)
            stats['status_codes'][status] += 1
            
            # Content type
            content = response.get('content', {})
            mime_type = content.get('mimeType', 'unknown')
            if ';' in mime_type:
                mime_type = mime_type.split(';')[0].strip()
            stats['content_types'][mime_type] += 1
            
            # Size
            size = content.get('size', 0) or 0
            stats['total_size'] += size
        
        # Convert sets to lists for JSON serialization
        stats['domains'] = list(stats['domains'])
        stats['content_types'] = dict(stats['content_types'])
        stats['methods'] = dict(stats['methods'])
        stats['status_codes'] = dict(stats['status_codes'])
        
        return stats
    
    def analyze_security(self) -> dict[str, Any]:
        """Analyze security aspects of the captured traffic."""
        security = {
            'https_usage': {'https': 0, 'http': 0},
            'missing_headers': defaultdict(list),
            'insecure_cookies': [],
            'potential_vulnerabilities': []
        }
        
        analyzed_domains = set()
        
        for entry in self.entries:
            request = entry.get('request', {})
            response = entry.get('response', {})
            url = request.get('url', '')
            parsed = urlparse(url)
            
            # HTTPS usage
            if parsed.scheme == 'https':
                security['https_usage']['https'] += 1
            else:
                security['https_usage']['http'] += 1
                self.findings['critical'].append(
                    f"Unencrypted HTTP request: {url[:80]}..."
                )
            
            # Security headers (check once per domain)
            domain = parsed.netloc
            if domain and domain not in analyzed_domains:
                analyzed_domains.add(domain)
                headers = {h['name'].lower(): h['value'] 
                          for h in response.get('headers', [])}
                
                # Check required headers
                for header in REQUIRED_SECURITY_HEADERS:
                    if header.lower() not in headers:
                        security['missing_headers'][domain].append(header)
                        self.findings['high'].append(
                            f"Missing security header '{header}' on {domain}"
                        )
            
            # Cookie analysis
            for cookie in response.get('cookies', []):
                cookie_name = cookie.get('name', 'unknown')
                issues = []
                
                if not cookie.get('httpOnly', False):
                    issues.append('HttpOnly')
                if not cookie.get('secure', False):
                    issues.append('Secure')
                if not cookie.get('sameSite'):
                    issues.append('SameSite')
                
                if issues:
                    security['insecure_cookies'].append({
                        'name': cookie_name,
                        'domain': cookie.get('domain', domain),
                        'missing_flags': issues
                    })
                    self.findings['medium'].append(
                        f"Cookie '{cookie_name}' missing flags: {', '.join(issues)}"
                    )
        
        # Check for potential information disclosure
        for entry in self.entries:
            response = entry.get('response', {})
            headers = {h['name'].lower(): h['value'] 
                      for h in response.get('headers', [])}
            
            # Server header disclosure
            if 'server' in headers:
                server = headers['server']
                if any(v in server.lower() for v in ['version', '/']):
                    self.findings['low'].append(
                        f"Server version disclosure: {server}"
                    )
            
            # X-Powered-By disclosure
            if 'x-powered-by' in headers:
                self.findings['low'].append(
                    f"Technology disclosure via X-Powered-By: {headers['x-powered-by']}"
                )
        
        security['missing_headers'] = dict(security['missing_headers'])
        return security
    
    def analyze_performance(self) -> dict[str, Any]:
        """Analyze performance characteristics."""
        performance = {
            'total_time': 0,
            'total_size': 0,
            'timing_breakdown': {
                'blocked': 0,
                'dns': 0,
                'connect': 0,
                'ssl': 0,
                'send': 0,
                'wait': 0,
                'receive': 0
            },
            'slowest_requests': [],
            'largest_requests': []
        }
        
        request_data = []
        
        for entry in self.entries:
            request = entry.get('request', {})
            response = entry.get('response', {})
            timings = entry.get('timings', {})
            
            url = request.get('url', '')
            
            # Timing
            total_time = entry.get('time', 0) or 0
            performance['total_time'] += total_time
            
            for key in performance['timing_breakdown']:
                value = timings.get(key, 0)
                if value and value > 0:
                    performance['timing_breakdown'][key] += value
            
            # Size
            content = response.get('content', {})
            size = content.get('size', 0) or 0
            performance['total_size'] += size
            
            request_data.append({
                'url': url[:100],
                'time': total_time,
                'size': size,
                'status': response.get('status', 0)
            })
        
        # Get slowest and largest
        performance['slowest_requests'] = sorted(
            request_data, key=lambda x: x['time'], reverse=True
        )[:5]
        
        performance['largest_requests'] = sorted(
            request_data, key=lambda x: x['size'], reverse=True
        )[:5]
        
        return performance
    
    def analyze_endpoints(self) -> dict[str, Any]:
        """Analyze API endpoints."""
        endpoints = {
            'unique_endpoints': set(),
            'by_method': defaultdict(list),
            'api_patterns': [],
            'authentication': []
        }
        
        for entry in self.entries:
            request = entry.get('request', {})
            url = request.get('url', '')
            method = request.get('method', 'GET')
            
            parsed = urlparse(url)
            path = parsed.path
            
            # Clean endpoint (remove query params)
            endpoint = f"{method} {parsed.netloc}{path}"
            endpoints['unique_endpoints'].add(endpoint)
            endpoints['by_method'][method].append(f"{parsed.netloc}{path}")
            
            # Detect API patterns
            if '/api/' in path or '/v1/' in path or '/v2/' in path:
                endpoints['api_patterns'].append({
                    'method': method,
                    'path': path,
                    'domain': parsed.netloc
                })
            
            # Check for authentication headers
            headers = {h['name'].lower(): h['value'] 
                      for h in request.get('headers', [])}
            
            if 'authorization' in headers:
                auth_type = headers['authorization'].split()[0] if ' ' in headers['authorization'] else 'unknown'
                endpoints['authentication'].append({
                    'type': auth_type,
                    'endpoint': f"{method} {path}"
                })
        
        endpoints['unique_endpoints'] = list(endpoints['unique_endpoints'])
        endpoints['by_method'] = dict(endpoints['by_method'])
        
        return endpoints
    
    def print_report(self) -> None:
        """Print a formatted analysis report."""
        results = self.analyze()
        
        print_header("HAR Security Analysis Report")
        
        # Statistics
        print_section("Basic Statistics")
        stats = results['statistics']
        print(f"  Total Requests: {stats['total_requests']}")
        print(f"  Total Size: {format_bytes(stats['total_size'])}")
        print(f"  Unique Domains: {len(stats['domains'])}")
        print(f"  HTTP Methods: {', '.join(f'{k}({v})' for k, v in stats['methods'].items())}")
        
        # Security Analysis
        print_section("Security Analysis")
        security = results['security']
        
        # HTTPS usage
        https_count = security['https_usage']['https']
        http_count = security['https_usage']['http']
        total = https_count + http_count
        
        if http_count > 0:
            error(f"Found {http_count} unencrypted HTTP requests ({http_count/total*100:.1f}%)")
        else:
            success("All requests use HTTPS")
        
        # Missing headers
        missing_headers = security['missing_headers']
        if missing_headers:
            warning(f"Missing security headers on {len(missing_headers)} domain(s):")
            for domain, headers in list(missing_headers.items())[:3]:
                print(f"      {domain}: {', '.join(headers[:3])}")
        else:
            success("All required security headers present")
        
        # Insecure cookies
        insecure = security['insecure_cookies']
        if insecure:
            warning(f"Found {len(insecure)} cookie(s) with missing security flags")
            for cookie in insecure[:3]:
                print(f"      {cookie['name']}: missing {', '.join(cookie['missing_flags'])}")
        else:
            success("All cookies have appropriate security flags")
        
        # Performance Summary
        print_section("Performance Summary")
        perf = results['performance']
        print(f"  Total Load Time: {format_time(perf['total_time'])}")
        print(f"  Total Transfer: {format_bytes(perf['total_size'])}")
        
        if perf['slowest_requests']:
            print("\n  Slowest Requests:")
            for req in perf['slowest_requests'][:3]:
                print(f"    - {format_time(req['time'])}: {req['url'][:60]}...")
        
        # Endpoints
        print_section("Endpoint Analysis")
        endpoints = results['endpoints']
        print(f"  Unique Endpoints: {len(endpoints['unique_endpoints'])}")
        print(f"  API Endpoints: {len(endpoints['api_patterns'])}")
        
        if endpoints['authentication']:
            auth_types = set(a['type'] for a in endpoints['authentication'])
            print(f"  Authentication Types: {', '.join(auth_types)}")
        
        # Findings Summary
        print_section("Findings Summary")
        findings = self.findings
        
        critical = len(findings.get('critical', []))
        high = len(findings.get('high', []))
        medium = len(findings.get('medium', []))
        low = len(findings.get('low', []))
        
        if critical > 0:
            print(f"  {Colors.RED}Critical: {critical}{Colors.NC}")
        if high > 0:
            print(f"  {Colors.RED}High: {high}{Colors.NC}")
        if medium > 0:
            print(f"  {Colors.YELLOW}Medium: {medium}{Colors.NC}")
        if low > 0:
            print(f"  {Colors.BLUE}Low: {low}{Colors.NC}")
        
        if not any([critical, high, medium, low]):
            success("No significant security findings")
        
        print("")


# =============================================================================
# Comparison Analysis
# =============================================================================

class ComparisonAnalyzer:
    """Analyzer for comparing original vs sovereign implementations."""
    
    def __init__(self, original_har: dict[str, Any], sovereign_har: dict[str, Any]):
        self.original = HARAnalyzer(original_har)
        self.sovereign = HARAnalyzer(sovereign_har)
        
    def compare(self) -> dict[str, Any]:
        """Run comparison analysis."""
        orig_results = self.original.analyze()
        sov_results = self.sovereign.analyze()
        
        comparison = {
            'request_count': {
                'original': orig_results['statistics']['total_requests'],
                'sovereign': sov_results['statistics']['total_requests'],
                'delta': sov_results['statistics']['total_requests'] - orig_results['statistics']['total_requests']
            },
            'total_size': {
                'original': orig_results['statistics']['total_size'],
                'sovereign': sov_results['statistics']['total_size'],
                'improvement_percent': 0
            },
            'performance': {
                'original_time': orig_results['performance']['total_time'],
                'sovereign_time': sov_results['performance']['total_time'],
                'improvement_percent': 0
            },
            'security': {
                'original_http_requests': orig_results['security']['https_usage']['http'],
                'sovereign_http_requests': sov_results['security']['https_usage']['http'],
                'original_findings': len(self.original.findings.get('critical', [])) + len(self.original.findings.get('high', [])),
                'sovereign_findings': len(self.sovereign.findings.get('critical', [])) + len(self.sovereign.findings.get('high', []))
            }
        }
        
        # Calculate improvements
        orig_size = comparison['total_size']['original']
        sov_size = comparison['total_size']['sovereign']
        if orig_size > 0:
            comparison['total_size']['improvement_percent'] = ((orig_size - sov_size) / orig_size) * 100
        
        orig_time = comparison['performance']['original_time']
        sov_time = comparison['performance']['sovereign_time']
        if orig_time > 0:
            comparison['performance']['improvement_percent'] = ((orig_time - sov_time) / orig_time) * 100
        
        return comparison
    
    def print_report(self) -> None:
        """Print a formatted comparison report."""
        comparison = self.compare()
        
        print_header("Version Comparison Report", Colors.PURPLE)
        
        # Request Count
        print_section("Request Count")
        orig = comparison['request_count']['original']
        sov = comparison['request_count']['sovereign']
        delta = comparison['request_count']['delta']
        
        print(f"  Original:  {orig} requests")
        print(f"  Sovereign: {sov} requests")
        if delta < 0:
            success(f"Reduced by {abs(delta)} requests")
        elif delta > 0:
            warning(f"Increased by {delta} requests")
        else:
            info("Same number of requests")
        
        # Transfer Size
        print_section("Transfer Size")
        orig = comparison['total_size']['original']
        sov = comparison['total_size']['sovereign']
        improvement = comparison['total_size']['improvement_percent']
        
        print(f"  Original:  {format_bytes(orig)}")
        print(f"  Sovereign: {format_bytes(sov)}")
        if improvement > 0:
            success(f"Reduced by {improvement:.1f}%")
        elif improvement < 0:
            warning(f"Increased by {abs(improvement):.1f}%")
        else:
            info("Same transfer size")
        
        # Performance
        print_section("Performance")
        orig = comparison['performance']['original_time']
        sov = comparison['performance']['sovereign_time']
        improvement = comparison['performance']['improvement_percent']
        
        print(f"  Original:  {format_time(orig)}")
        print(f"  Sovereign: {format_time(sov)}")
        if improvement > 0:
            success(f"Faster by {improvement:.1f}%")
        elif improvement < 0:
            warning(f"Slower by {abs(improvement):.1f}%")
        else:
            info("Same performance")
        
        # Security
        print_section("Security Comparison")
        orig_http = comparison['security']['original_http_requests']
        sov_http = comparison['security']['sovereign_http_requests']
        orig_findings = comparison['security']['original_findings']
        sov_findings = comparison['security']['sovereign_findings']
        
        print(f"  HTTP Requests: Original={orig_http}, Sovereign={sov_http}")
        print(f"  Critical/High Findings: Original={orig_findings}, Sovereign={sov_findings}")
        
        if sov_http < orig_http:
            success(f"Reduced unencrypted requests by {orig_http - sov_http}")
        if sov_findings < orig_findings:
            success(f"Reduced security findings by {orig_findings - sov_findings}")
        
        # Overall Assessment
        print_section("Overall Assessment")
        
        improvements = []
        regressions = []
        
        if comparison['total_size']['improvement_percent'] > 5:
            improvements.append(f"Size reduced by {comparison['total_size']['improvement_percent']:.1f}%")
        elif comparison['total_size']['improvement_percent'] < -5:
            regressions.append(f"Size increased by {abs(comparison['total_size']['improvement_percent']):.1f}%")
        
        if comparison['performance']['improvement_percent'] > 5:
            improvements.append(f"Performance improved by {comparison['performance']['improvement_percent']:.1f}%")
        elif comparison['performance']['improvement_percent'] < -5:
            regressions.append(f"Performance degraded by {abs(comparison['performance']['improvement_percent']):.1f}%")
        
        if sov_findings < orig_findings:
            improvements.append(f"Security findings reduced from {orig_findings} to {sov_findings}")
        elif sov_findings > orig_findings:
            regressions.append(f"Security findings increased from {orig_findings} to {sov_findings}")
        
        if improvements:
            print(f"\n  {Colors.GREEN}Improvements:{Colors.NC}")
            for imp in improvements:
                success(imp)
        
        if regressions:
            print(f"\n  {Colors.RED}Regressions:{Colors.NC}")
            for reg in regressions:
                warning(reg)
        
        if not improvements and not regressions:
            info("No significant differences detected")
        
        print("")


# =============================================================================
# Report Generation
# =============================================================================

def generate_markdown_report(analyzer: HARAnalyzer, output_path: str) -> None:
    """Generate a Markdown report from analysis results."""
    results = analyzer.analyze()
    
    report = f"""# Security Analysis Report

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Analyzer Version**: {VERSION}

---

## Summary

| Metric | Value |
|--------|-------|
| Total Requests | {results['statistics']['total_requests']} |
| Total Size | {format_bytes(results['statistics']['total_size'])} |
| Unique Domains | {len(results['statistics']['domains'])} |
| Load Time | {format_time(results['performance']['total_time'])} |

## Security Findings

### HTTPS Usage

- HTTPS Requests: {results['security']['https_usage']['https']}
- HTTP Requests: {results['security']['https_usage']['http']}

### Missing Security Headers

"""
    
    if results['security']['missing_headers']:
        for domain, headers in results['security']['missing_headers'].items():
            report += f"\n**{domain}**\n"
            for header in headers:
                report += f"- {header}\n"
    else:
        report += "All required security headers present.\n"
    
    report += """
### Insecure Cookies

"""
    
    if results['security']['insecure_cookies']:
        report += "| Cookie | Domain | Missing Flags |\n"
        report += "|--------|--------|---------------|\n"
        for cookie in results['security']['insecure_cookies']:
            flags = ', '.join(cookie['missing_flags'])
            report += f"| {cookie['name']} | {cookie['domain']} | {flags} |\n"
    else:
        report += "All cookies have appropriate security flags.\n"
    
    report += f"""
## Findings by Severity

| Severity | Count |
|----------|-------|
| Critical | {len(analyzer.findings.get('critical', []))} |
| High | {len(analyzer.findings.get('high', []))} |
| Medium | {len(analyzer.findings.get('medium', []))} |
| Low | {len(analyzer.findings.get('low', []))} |

## Performance Metrics

- Total Load Time: {format_time(results['performance']['total_time'])}
- Total Transfer: {format_bytes(results['performance']['total_size'])}

### Timing Breakdown

| Phase | Time |
|-------|------|
"""
    
    for phase, time in results['performance']['timing_breakdown'].items():
        report += f"| {phase.capitalize()} | {format_time(time)} |\n"
    
    report += """
---

*Report generated by Sovereignty Analyzer*
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"{Colors.GREEN}Report generated: {output_path}{Colors.NC}")


# =============================================================================
# Main Entry Point
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Sovereignty Analyzer - HAR Security Analysis Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s analyze-har capture.har
  %(prog)s analyze-har capture.har --focus security
  %(prog)s compare original.har sovereign.har
  %(prog)s report --input analysis.json --output report.md
        """
    )
    
    parser.add_argument('--version', action='version', version=f'%(prog)s {VERSION}')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # analyze-har command
    analyze_parser = subparsers.add_parser('analyze-har', help='Analyze a HAR file')
    analyze_parser.add_argument('har_file', help='Path to HAR file')
    analyze_parser.add_argument('--focus', choices=['security', 'performance', 'all'],
                                default='all', help='Focus area for analysis')
    analyze_parser.add_argument('--output', '-o', help='Output file for JSON results')
    analyze_parser.add_argument('--markdown', '-m', help='Output file for Markdown report')
    
    # compare command
    compare_parser = subparsers.add_parser('compare', help='Compare two HAR files')
    compare_parser.add_argument('original', help='Original HAR file')
    compare_parser.add_argument('sovereign', help='Sovereign HAR file')
    compare_parser.add_argument('--output', '-o', help='Output file for comparison results')
    
    # report command
    report_parser = subparsers.add_parser('report', help='Generate report')
    report_parser.add_argument('--input', '-i', help='Input analysis JSON')
    report_parser.add_argument('--output', '-o', required=True, help='Output report file')
    report_parser.add_argument('--type', choices=['security', 'performance', 'comparison', 'full'],
                               default='full', help='Report type')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    if args.command == 'analyze-har':
        har_data = load_har(args.har_file)
        analyzer = HARAnalyzer(har_data)
        
        # Print report to console
        analyzer.print_report()
        
        # Save JSON output if requested
        if args.output:
            results = analyzer.analyze()
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, default=str)
            print(f"{Colors.GREEN}JSON results saved to: {args.output}{Colors.NC}")
        
        # Generate Markdown report if requested
        if args.markdown:
            generate_markdown_report(analyzer, args.markdown)
    
    elif args.command == 'compare':
        original_data = load_har(args.original)
        sovereign_data = load_har(args.sovereign)
        
        comparator = ComparisonAnalyzer(original_data, sovereign_data)
        comparator.print_report()
        
        if args.output:
            results = comparator.compare()
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, default=str)
            print(f"{Colors.GREEN}Comparison results saved to: {args.output}{Colors.NC}")
    
    elif args.command == 'report':
        if args.input:
            with open(args.input, 'r', encoding='utf-8') as f:
                data = json.load(f)
            # Create a minimal HAR structure from saved data
            print(f"Generating report from: {args.input}")
        else:
            print(f"{Colors.YELLOW}No input specified, generating template report{Colors.NC}")
        
        # Generate template report
        template = f"""# Sovereignty Analysis Report

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Type**: {args.type}

---

## Summary

This report was generated by the Sovereignty Analyzer.

## Methodology

See REVERSE_ENGINEERING_SOVEREIGNTY_METHODOLOGY.md for complete methodology.

## Next Steps

1. Review security findings
2. Implement recommended fixes
3. Re-run analysis to verify improvements

---

*Generated by Sovereignty Analyzer v{VERSION}*
"""
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(template)
        print(f"{Colors.GREEN}Report generated: {args.output}{Colors.NC}")


if __name__ == '__main__':
    main()
