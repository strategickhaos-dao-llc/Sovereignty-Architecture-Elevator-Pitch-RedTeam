#!/usr/bin/env python3
"""
Example usage of the Sovereign Research Browser

This script demonstrates how to use the browser both as a Python API
and by calling the FastAPI /browse endpoint.
"""

import asyncio
import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

from browser import ResearchBrowser


async def example_direct_api():
    """Example using the Python API directly"""
    print("=" * 70)
    print("Example 1: Using Python API directly")
    print("=" * 70)
    
    browser = ResearchBrowser()
    
    # Example 1: Browse a Python documentation page
    print("\n1. Browsing Python documentation...")
    response = await browser.browse("https://docs.python.org/3/library/asyncio.html")
    
    if response.research_allowed and not response.error:
        print(f"✓ Success!")
        print(f"  Title: {response.title}")
        print(f"  Status: {response.status_code}")
        print(f"  Preview: {response.text_preview[:150]}...")
    else:
        print(f"✗ Error: {response.error}")
    
    # Example 2: Browse arXiv paper
    print("\n2. Browsing arXiv paper...")
    response = await browser.browse("https://arxiv.org/abs/2103.00020")
    
    if response.research_allowed and not response.error:
        print(f"✓ Success!")
        print(f"  Title: {response.title}")
        print(f"  Preview: {response.text_preview[:150]}...")
    else:
        print(f"✗ Error: {response.error}")
    
    # Example 3: Try a non-whitelisted domain
    print("\n3. Trying non-whitelisted domain...")
    response = await browser.browse("https://random-site.com/page")
    
    if not response.research_allowed:
        print(f"✓ Correctly blocked!")
        print(f"  Error: {response.error}")
    else:
        print(f"✗ Unexpectedly allowed")
    
    # Example 4: Test rate limiting (make multiple requests to same domain)
    print("\n4. Testing rate limiting...")
    domain_url = "https://github.com/"
    
    for i in range(3):
        response = await browser.browse(domain_url + f"?test={i}")
        if response.rate_limited:
            print(f"  Request {i+1}: Rate limited after {i} requests")
            break
        else:
            print(f"  Request {i+1}: Allowed")
    
    await browser.close()
    print("\n" + "=" * 70)


async def example_http_endpoint():
    """Example using the HTTP endpoint (requires FastAPI server running)"""
    print("\n" + "=" * 70)
    print("Example 2: Using HTTP /browse endpoint")
    print("=" * 70)
    
    try:
        import httpx
        
        print("\nNote: This requires the Refinory FastAPI server to be running.")
        print("Start it with: uvicorn refinory.main:app --host 0.0.0.0 --port 8000")
        print("\nExample cURL commands you can use:\n")
        
        examples = [
            ("Browse Python docs", "https://docs.python.org/3/"),
            ("Browse arXiv paper", "https://arxiv.org/abs/2103.00020"),
            ("Browse GitHub repo", "https://github.com/python/cpython"),
            ("Browse Kubernetes docs", "https://kubernetes.io/docs/"),
        ]
        
        for name, url in examples:
            curl_cmd = f'curl "http://localhost:8000/browse?url={url}"'
            print(f"# {name}")
            print(curl_cmd)
            print()
        
        # Try to actually call the endpoint if server is running
        print("\nAttempting to call the actual endpoint (if server is running)...")
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get(
                    "http://localhost:8000/browse",
                    params={"url": "https://docs.python.org/3/"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✓ Success!")
                    print(f"  Title: {data.get('title')}")
                    print(f"  Preview: {data.get('text_preview', '')[:150]}...")
                else:
                    print(f"✗ Error: HTTP {response.status_code}")
                    print(f"  {response.text}")
            except httpx.ConnectError:
                print("✗ Server not running (connection failed)")
                print("  Start server with: cd refinory && uvicorn refinory.main:app")
            except Exception as e:
                print(f"✗ Error: {str(e)}")
    
    except ImportError:
        print("\nNote: httpx not installed. Install with: pip install httpx")
        print("Showing example cURL commands instead:\n")
        
        examples = [
            ("Browse Python docs", "https://docs.python.org/3/"),
            ("Browse arXiv paper", "https://arxiv.org/abs/2103.00020"),
        ]
        
        for name, url in examples:
            curl_cmd = f'curl "http://localhost:8000/browse?url={url}"'
            print(f"# {name}")
            print(curl_cmd)
            print()
    
    print("=" * 70)


async def main():
    """Run all examples"""
    print("\n" + "=" * 70)
    print("SOVEREIGN RESEARCH BROWSER - Usage Examples")
    print("=" * 70)
    
    # Run direct API example
    await example_direct_api()
    
    # Show HTTP endpoint example
    await example_http_endpoint()
    
    print("\nFor more information, see:")
    print("  - app/README.md - General documentation")
    print("  - app/ATHENA_TOOL_INTEGRATION.md - Athena tool integration guide")
    print()


if __name__ == "__main__":
    asyncio.run(main())
