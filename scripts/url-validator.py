#!/usr/bin/env python3
"""
URL Validator
Validates all URLs in sme-resources.yaml are reachable
"""

import os
import time
import yaml
import json
from pathlib import Path
from typing import Dict, List
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuration
RESOURCES_FILE = Path("/app/sme-resources.yaml")
RESULTS_DIR = Path("/app/results")
VALIDATION_INTERVAL = int(os.getenv("VALIDATION_INTERVAL", "86400"))  # Daily
TIMEOUT = int(os.getenv("TIMEOUT", "10"))
RETRY_ATTEMPTS = int(os.getenv("RETRY_ATTEMPTS", "3"))
MAX_WORKERS = 10

# Create results directory
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def load_resources() -> Dict:
    """Load SME resources from YAML file"""
    with open(RESOURCES_FILE, 'r') as f:
        return yaml.safe_load(f)


def validate_url(resource: Dict) -> Dict:
    """Validate a single URL"""
    resource_id = resource['id']
    url = resource['url']
    title = resource['title']
    
    result = {
        'id': resource_id,
        'title': title,
        'url': url,
        'status': 'unknown',
        'status_code': None,
        'response_time': None,
        'error': None,
        'attempts': 0
    }
    
    headers = {
        'User-Agent': 'SovereignArchitecture-Validator/1.0'
    }
    
    # Try with retries
    for attempt in range(1, RETRY_ATTEMPTS + 1):
        result['attempts'] = attempt
        
        try:
            start_time = time.time()
            response = requests.head(url, headers=headers, timeout=TIMEOUT, allow_redirects=True)
            response_time = time.time() - start_time
            
            result['status_code'] = response.status_code
            result['response_time'] = round(response_time, 2)
            
            if response.status_code < 400:
                result['status'] = 'ok'
                return result
            elif response.status_code >= 500:
                # Server error, might be temporary, retry
                if attempt < RETRY_ATTEMPTS:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                else:
                    result['status'] = 'server_error'
                    result['error'] = f"HTTP {response.status_code}"
                    return result
            else:
                # Client error, probably permanent
                result['status'] = 'client_error'
                result['error'] = f"HTTP {response.status_code}"
                return result
                
        except requests.exceptions.Timeout:
            if attempt < RETRY_ATTEMPTS:
                time.sleep(2 ** attempt)
                continue
            else:
                result['status'] = 'timeout'
                result['error'] = 'Request timeout'
                return result
                
        except requests.exceptions.ConnectionError as e:
            if attempt < RETRY_ATTEMPTS:
                time.sleep(2 ** attempt)
                continue
            else:
                result['status'] = 'connection_error'
                result['error'] = str(e)[:100]
                return result
                
        except Exception as e:
            result['status'] = 'error'
            result['error'] = str(e)[:100]
            return result
    
    return result


def validate_all_resources(resources: List[Dict]) -> List[Dict]:
    """Validate all resources in parallel"""
    results = []
    
    print(f"Validating {len(resources)} URLs with {MAX_WORKERS} workers...\n")
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Submit all tasks
        future_to_resource = {
            executor.submit(validate_url, resource): resource 
            for resource in resources
        }
        
        # Process completed tasks
        for i, future in enumerate(as_completed(future_to_resource), 1):
            resource = future_to_resource[future]
            
            try:
                result = future.result()
                results.append(result)
                
                # Print progress
                status_symbol = {
                    'ok': '✓',
                    'timeout': '⏱',
                    'server_error': '⚠',
                    'client_error': '✗',
                    'connection_error': '✗',
                    'error': '✗',
                    'unknown': '?'
                }.get(result['status'], '?')
                
                print(f"[{i}/{len(resources)}] {status_symbol} [{result['id']}] {result['title'][:50]}")
                if result['status'] != 'ok':
                    print(f"  Error: {result['error']}")
                
            except Exception as e:
                print(f"[{i}/{len(resources)}] ✗ Error processing {resource['id']}: {e}")
    
    return results


def generate_report(results: List[Dict]) -> Dict:
    """Generate validation report"""
    total = len(results)
    
    status_counts = {}
    for result in results:
        status = result['status']
        status_counts[status] = status_counts.get(status, 0) + 1
    
    ok_count = status_counts.get('ok', 0)
    failed_count = total - ok_count
    
    # Find failures
    failures = [r for r in results if r['status'] != 'ok']
    
    # Calculate average response time for successful requests
    ok_times = [r['response_time'] for r in results if r.get('response_time')]
    avg_response_time = sum(ok_times) / len(ok_times) if ok_times else 0
    
    report = {
        'timestamp': time.time(),
        'total_resources': total,
        'successful': ok_count,
        'failed': failed_count,
        'success_rate': round(ok_count / total * 100, 2) if total > 0 else 0,
        'status_breakdown': status_counts,
        'avg_response_time': round(avg_response_time, 2),
        'failures': failures,
        'results': results
    }
    
    return report


def main():
    print("=" * 80)
    print("URL Validator")
    print("=" * 80)
    print(f"Resources file: {RESOURCES_FILE}")
    print(f"Results directory: {RESULTS_DIR}")
    print(f"Timeout: {TIMEOUT}s")
    print(f"Retry attempts: {RETRY_ATTEMPTS}")
    print()
    
    # Load resources
    data = load_resources()
    resources = data.get('resources', [])
    
    print(f"Loaded {len(resources)} resources\n")
    
    while True:
        print(f"Starting validation at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Validate all
        results = validate_all_resources(resources)
        
        # Generate report
        report = generate_report(results)
        
        # Save report
        report_file = RESULTS_DIR / f"url_validation_{int(time.time())}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Print summary
        print("\n" + "=" * 80)
        print("VALIDATION SUMMARY")
        print("=" * 80)
        print(f"Total resources: {report['total_resources']}")
        print(f"Successful: {report['successful']}")
        print(f"Failed: {report['failed']}")
        print(f"Success rate: {report['success_rate']}%")
        print(f"Avg response time: {report['avg_response_time']}s")
        print()
        print("Status breakdown:")
        for status, count in report['status_breakdown'].items():
            print(f"  {status}: {count}")
        
        if report['failures']:
            print(f"\nFailed resources ({len(report['failures'])}):")
            for failure in report['failures'][:10]:  # Show first 10
                print(f"  [{failure['id']}] {failure['title']}")
                print(f"    Status: {failure['status']}")
                print(f"    Error: {failure['error']}")
        
        print(f"\nReport saved to: {report_file}")
        print("=" * 80)
        
        # Wait for next validation
        print(f"\nNext validation in {VALIDATION_INTERVAL}s ({VALIDATION_INTERVAL/3600:.1f} hours)")
        print("Press Ctrl+C to stop\n")
        
        try:
            time.sleep(VALIDATION_INTERVAL)
        except KeyboardInterrupt:
            print("\n\nShutting down validator...")
            break


if __name__ == "__main__":
    main()
