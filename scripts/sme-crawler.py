#!/usr/bin/env python3
"""
SME Resource Crawler
Fetches content from all 100 authoritative sources in sme-resources.yaml
"""

import os
import time
import yaml
import json
import hashlib
from pathlib import Path
from typing import Dict, List
import requests
from bs4 import BeautifulSoup

# Configuration
DATA_DIR = Path("/app/data")
RESOURCES_FILE = Path("/app/sme-resources.yaml")
USER_AGENT = os.getenv("USER_AGENT", "SovereignArchitecture-SME-Bot/1.0")
RATE_LIMIT = float(os.getenv("RATE_LIMIT", "2"))  # requests per second
TIMEOUT = int(os.getenv("TIMEOUT", "30"))
RETRY_ATTEMPTS = int(os.getenv("RETRY_ATTEMPTS", "3"))

# Create output directory
DATA_DIR.mkdir(parents=True, exist_ok=True)
(DATA_DIR / "raw").mkdir(exist_ok=True)
(DATA_DIR / "processed").mkdir(exist_ok=True)


def load_resources() -> Dict:
    """Load SME resources from YAML file"""
    with open(RESOURCES_FILE, 'r') as f:
        return yaml.safe_load(f)


def fetch_url(url: str, attempt: int = 1) -> Dict:
    """Fetch content from URL with retries"""
    headers = {
        'User-Agent': USER_AGENT,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }
    
    try:
        print(f"  Fetching (attempt {attempt}/{RETRY_ATTEMPTS})...")
        response = requests.get(url, headers=headers, timeout=TIMEOUT, allow_redirects=True)
        response.raise_for_status()
        
        content_type = response.headers.get('Content-Type', '')
        
        return {
            'success': True,
            'status_code': response.status_code,
            'content_type': content_type,
            'content': response.text,
            'url': response.url,  # Final URL after redirects
            'headers': dict(response.headers)
        }
    
    except requests.exceptions.Timeout:
        if attempt < RETRY_ATTEMPTS:
            time.sleep(2 ** attempt)  # Exponential backoff
            return fetch_url(url, attempt + 1)
        return {'success': False, 'error': 'Timeout'}
    
    except requests.exceptions.RequestException as e:
        if attempt < RETRY_ATTEMPTS:
            time.sleep(2 ** attempt)
            return fetch_url(url, attempt + 1)
        return {'success': False, 'error': str(e)}


def extract_text(html: str) -> Dict:
    """Extract text content from HTML"""
    try:
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Get text
        text = soup.get_text(separator='\n', strip=True)
        
        # Extract links
        links = []
        for link in soup.find_all('a', href=True):
            links.append({
                'text': link.get_text(strip=True),
                'href': link['href']
            })
        
        # Extract headings for structure
        headings = []
        for i in range(1, 7):
            for heading in soup.find_all(f'h{i}'):
                headings.append({
                    'level': i,
                    'text': heading.get_text(strip=True)
                })
        
        return {
            'text': text,
            'links': links[:100],  # Limit to first 100 links
            'headings': headings[:50],  # Limit to first 50 headings
            'title': soup.title.string if soup.title else None
        }
    
    except Exception as e:
        return {'error': str(e)}


def crawl_resource(resource: Dict) -> Dict:
    """Crawl a single resource"""
    resource_id = resource['id']
    url = resource['url']
    category = resource.get('category', 'unknown')
    
    print(f"\n[{resource_id}] {resource['title']}")
    print(f"  URL: {url}")
    print(f"  Category: {category}")
    
    # Generate unique filename
    url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
    filename = f"{resource_id:03d}_{url_hash}_{category}"
    
    # Fetch content
    result = fetch_url(url)
    
    if result['success']:
        print(f"  ✓ Fetched {len(result['content'])} bytes")
        
        # Save raw HTML
        raw_file = DATA_DIR / "raw" / f"{filename}.html"
        with open(raw_file, 'w', encoding='utf-8') as f:
            f.write(result['content'])
        
        # Extract and save processed content
        extracted = extract_text(result['content'])
        processed_data = {
            'resource_id': resource_id,
            'title': resource['title'],
            'url': url,
            'final_url': result['url'],
            'category': category,
            'sme_topics': resource.get('sme_topics', []),
            'fetched_at': time.time(),
            'status_code': result['status_code'],
            'content_type': result['content_type'],
            **extracted
        }
        
        processed_file = DATA_DIR / "processed" / f"{filename}.json"
        with open(processed_file, 'w', encoding='utf-8') as f:
            json.dump(processed_data, f, indent=2)
        
        print(f"  ✓ Processed and saved")
        return {'success': True, 'resource_id': resource_id}
    
    else:
        print(f"  ✗ Failed: {result.get('error', 'Unknown error')}")
        return {'success': False, 'resource_id': resource_id, 'error': result.get('error')}


def main():
    """Main crawler function"""
    print("=" * 80)
    print("SME Resource Crawler")
    print("=" * 80)
    print(f"Output directory: {DATA_DIR}")
    print(f"Rate limit: {RATE_LIMIT} req/s")
    print(f"Timeout: {TIMEOUT}s")
    print()
    
    # Load resources
    data = load_resources()
    resources = data.get('resources', [])
    
    print(f"Found {len(resources)} resources to crawl\n")
    
    # Crawl each resource
    results = []
    for i, resource in enumerate(resources, 1):
        result = crawl_resource(resource)
        results.append(result)
        
        # Rate limiting
        if i < len(resources):
            sleep_time = 1.0 / RATE_LIMIT
            time.sleep(sleep_time)
    
    # Summary
    print("\n" + "=" * 80)
    print("CRAWL SUMMARY")
    print("=" * 80)
    successful = sum(1 for r in results if r['success'])
    failed = len(results) - successful
    print(f"Total resources: {len(results)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    
    if failed > 0:
        print("\nFailed resources:")
        for result in results:
            if not result['success']:
                print(f"  - {result['resource_id']}: {result.get('error', 'Unknown')}")
    
    # Save summary
    summary_file = DATA_DIR / "crawl_summary.json"
    with open(summary_file, 'w') as f:
        json.dump({
            'total': len(results),
            'successful': successful,
            'failed': failed,
            'results': results,
            'timestamp': time.time()
        }, f, indent=2)
    
    print(f"\nSummary saved to: {summary_file}")
    print("\n✓ Crawl complete!")


if __name__ == "__main__":
    main()
