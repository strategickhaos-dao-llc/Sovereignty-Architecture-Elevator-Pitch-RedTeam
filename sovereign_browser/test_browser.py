#!/usr/bin/env python3
"""
Test script for Sovereign Research Browser Node
Demonstrates API usage and validates functionality
"""

import requests
import json
import sys


def test_health_endpoint():
    """Test the health check endpoint"""
    print("Testing /health endpoint...")
    try:
        response = requests.get("http://localhost:8086/health")
        response.raise_for_status()
        data = response.json()
        print(f"✓ Health check passed: {json.dumps(data, indent=2)}")
        return True
    except Exception as e:
        print(f"✗ Health check failed: {e}")
        return False


def test_domains_endpoint():
    """Test the domains listing endpoint"""
    print("\nTesting /domains endpoint...")
    try:
        response = requests.get("http://localhost:8086/domains")
        response.raise_for_status()
        data = response.json()
        print(f"✓ Found {data['count']} allowed domains:")
        for domain in data['allowed_domains'][:5]:
            print(f"  - {domain}")
        if len(data['allowed_domains']) > 5:
            print(f"  ... and {len(data['allowed_domains']) - 5} more")
        return True
    except Exception as e:
        print(f"✗ Domains list failed: {e}")
        return False


def test_blocked_domain():
    """Test that blocked domains are rejected"""
    print("\nTesting domain blocking...")
    try:
        response = requests.get("http://localhost:8086/browse?url=https://example.com/")
        if response.status_code == 403:
            data = response.json()
            print(f"✓ Blocked domain correctly rejected: {data['detail']}")
            return True
        else:
            print(f"✗ Expected 403, got {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Domain blocking test failed: {e}")
        return False


def test_allowed_domain():
    """Test browsing an allowed domain (may fail if no network access)"""
    print("\nTesting allowed domain browsing...")
    try:
        response = requests.get("http://localhost:8086/browse?url=https://docs.python.org/3/")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Successfully browsed allowed domain:")
            print(f"  URL: {data['url']}")
            print(f"  Title: {data['title']}")
            print(f"  Text preview length: {len(data['text_preview'])} chars")
            return True
        elif response.status_code == 500:
            data = response.json()
            if "ERR_NAME_NOT_RESOLVED" in data['detail'] or "network" in data['detail'].lower():
                print(f"⚠ Network access not available (expected in sandboxed environment)")
                print(f"  Error: {data['detail']}")
                return True  # This is expected in CI/sandboxed environments
            else:
                print(f"✗ Unexpected error: {data['detail']}")
                return False
        else:
            print(f"✗ Expected 200 or 500, got {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Allowed domain test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("Sovereign Research Browser Node - Test Suite")
    print("=" * 60)
    
    tests = [
        test_health_endpoint,
        test_domains_endpoint,
        test_blocked_domain,
        test_allowed_domain,
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Test Results: {passed}/{total} passed")
    print("=" * 60)
    
    if passed == total:
        print("✓ All tests passed!")
        return 0
    else:
        print(f"✗ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
        sys.exit(1)
