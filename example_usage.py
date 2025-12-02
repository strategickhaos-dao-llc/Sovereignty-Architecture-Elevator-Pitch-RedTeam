#!/usr/bin/env python3
"""
Example usage of the Sovereign Research Browser
Demonstrates fetching data from various government and open data sources
"""

import asyncio
import json
from main import SovereignBrowser


async def example_fetch_single():
    """Example: Fetch a single API endpoint"""
    print("=" * 60)
    print("Example 1: Fetching a single endpoint")
    print("=" * 60)
    
    browser = SovereignBrowser()
    
    # Try fetching from Library of Congress
    url = "https://www.loc.gov/collections/?fo=json"
    print(f"\nFetching: {url}")
    
    try:
        data = await browser.fetch_json(url)
        if data:
            print(f"✓ Success! Retrieved data with keys: {list(data.keys())}")
    except Exception as e:
        print(f"Note: Could not fetch (expected in test environment): {e}")


async def example_check_domains():
    """Example: Check if domains are whitelisted"""
    print("\n" + "=" * 60)
    print("Example 2: Checking domain whitelist")
    print("=" * 60)
    
    browser = SovereignBrowser()
    
    test_urls = [
        "https://data.gov/api/test",
        "https://api.nasa.gov/openapi.yaml",
        "https://example.com/api",
        "https://arxiv.org/pdf/1234.pdf",
        "https://malicious-site.com/data"
    ]
    
    for url in test_urls:
        allowed = browser.is_domain_allowed(url)
        status = "✓ ALLOWED" if allowed else "✗ BLOCKED"
        print(f"{status}: {url}")


async def example_concurrent_fetching():
    """Example: Fetch multiple endpoints concurrently"""
    print("\n" + "=" * 60)
    print("Example 3: Concurrent fetching (simulated)")
    print("=" * 60)
    
    browser = SovereignBrowser(rate_limit_delay=0.5)
    
    # These are examples - actual fetching would require network access
    example_urls = [
        "https://catalog.data.gov/api/3/action/package_list",
        "https://data.gov.uk/api/3/action/package_list",
        "https://api.worldbank.org/v2/country/all/indicator/SP.POP.TOTL?format=json"
    ]
    
    print("\nExample URLs that can be fetched concurrently:")
    for i, url in enumerate(example_urls, 1):
        print(f"{i}. {url}")
    
    print("\nWith concurrent fetching, these would be retrieved efficiently")
    print("while respecting rate limits per domain.")


async def example_whitelist_operations():
    """Example: Load and save whitelist"""
    print("\n" + "=" * 60)
    print("Example 4: Whitelist operations")
    print("=" * 60)
    
    browser = SovereignBrowser()
    
    print(f"\nDefault whitelist size: {len(browser.allowed_domains)} domains")
    
    # Show sample domains by category
    categories = {
        "US Government": [d for d in browser.allowed_domains if '.gov' in d][:5],
        "International": [d for d in browser.allowed_domains if any(x in d for x in ['.uk', '.eu', '.ca'])][:5],
        "Research": [d for d in browser.allowed_domains if any(x in d for x in ['arxiv', 'zenodo', 'pubmed'])][:3],
        "Documentation": [d for d in browser.allowed_domains if 'docs' in d][:5]
    }
    
    for category, domains in categories.items():
        print(f"\n{category} domains:")
        for domain in domains:
            print(f"  • {domain}")


async def example_domain_statistics():
    """Example: Show domain statistics"""
    print("\n" + "=" * 60)
    print("Example 5: Domain statistics")
    print("=" * 60)
    
    from main import ALLOWED_DOMAINS
    
    stats = {
        "Total domains": len(ALLOWED_DOMAINS),
        ".gov domains": len([d for d in ALLOWED_DOMAINS if '.gov' in d]),
        "International gov": len([d for d in ALLOWED_DOMAINS if any(x in d for x in ['gov.uk', 'gov.in', 'gov.au', 'gov.br', 'gov.il'])]),
        ".org domains": len([d for d in ALLOWED_DOMAINS if '.org' in d]),
        "Documentation sites": len([d for d in ALLOWED_DOMAINS if 'docs' in d or 'developer' in d]),
        "Research platforms": len([d for d in ALLOWED_DOMAINS if any(x in d for x in ['arxiv', 'zenodo', 'figshare', 'osf', 'pubmed'])])
    }
    
    print("\nDomain Statistics:")
    for key, value in stats.items():
        print(f"  {key:.<30} {value}")
    
    print("\n✓ All domains are legally-clean and research-friendly")
    print("✓ No authentication required")
    print("✓ Perfect for feeding to LLMs")


async def main():
    """Run all examples"""
    print("\n" + "=" * 60)
    print("SOVEREIGN RESEARCH BROWSER - USAGE EXAMPLES")
    print("=" * 60)
    
    # Run examples in sequence
    await example_check_domains()
    await example_domain_statistics()
    await example_whitelist_operations()
    await example_concurrent_fetching()
    await example_fetch_single()
    
    print("\n" + "=" * 60)
    print("Examples complete!")
    print("=" * 60)
    print("\nTo fetch real data, use:")
    print("  python main.py <URL> --format json")
    print("\nTo list all domains:")
    print("  python main.py --list-domains")
    print("\nTo check a domain:")
    print("  python main.py --check-domain <domain>")
    print()


if __name__ == '__main__':
    asyncio.run(main())
