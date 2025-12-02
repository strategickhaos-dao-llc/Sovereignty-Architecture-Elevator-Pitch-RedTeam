#!/usr/bin/env python3
"""
Sovereign Research Browser - Main Module
Strategickhaos Sovereignty Architecture

A legally-clean, whitelist-based research browser for fetching structured data
from government portals, open data sources, and documentation sites.
All domains are public sector or standards bodies that explicitly encourage
programmatic access.
"""

import asyncio
import aiohttp
import argparse
import json
import logging
import sys
import time
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Expanded ALLOWED_DOMAINS whitelist - 100+ domains
# All are public sector, standards bodies, or documentation sites
# that explicitly encourage programmatic access
ALLOWED_DOMAINS = [
    # US Federal (.gov) – 50+
    "data.gov", "api.data.gov", "catalog.data.gov",
    "api.nasa.gov", "data.nasa.gov",
    "api.census.gov", "www.census.gov",
    "www.loc.gov", "id.loc.gov", "chroniclingamerica.loc.gov",
    "api.weather.gov", "open.nasa.gov",
    "api.fiscaldata.treasury.gov",
    "api.regulations.gov",
    "api.usaspending.gov",
    "api.gsa.gov", "open.gsa.gov",
    "analytics.usa.gov",
    "www.fedramp.gov",
    "api.epa.gov", "www.epa.gov",
    "api.bls.gov", "www.bls.gov",
    "api.dol.gov",
    "healthdata.gov",
    "www.fda.gov",
    "api.fcc.gov",
    "earthdata.nasa.gov",
    "www.usgs.gov", "earthexplorer.usgs.gov",
    "www.noaa.gov", "api.tidesandcurrents.noaa.gov",
    "www.energy.gov",

    # International government portals
    "data.gov.uk", "www.data.gov.uk",
    "data.europa.eu", "opendata.europa.eu",
    "data.gov.in", "www.data.gov.in",
    "open.canada.ca", "ouvert.canada.ca",
    "dados.gov.br",
    "data.gov.au",
    "data.gouv.fr",
    "www.govdata.de",
    "datos.gob.es",
    "dati.gov.it",
    "opendata.swiss",
    "data.govt.nz",
    "www.data.go.kr",
    "data.gov.sg",
    "www.odp.gov.hk",  # Hong Kong
    "data.gov.il",

    # Major open data / academic / standards orgs
    "dataportals.org",
    "opendatainception.io",
    "www.worldbank.org", "data.worldbank.org",
    "data.worldpop.org",
    "data.un.org", "unstats.un.org",
    "data.oecd.org",
    "www.who.int",
    "www.fao.org",
    "www.imf.org", "data.imf.org",
    "www.wto.org", "stats.wto.org",
    "www.rfc-editor.org",
    "www.ietf.org",
    "schema.org",
    "www.w3.org",
    "specs.openstack.org",
    "kubernetes.io",

    # Documentation / standards sites that love bots
    "docs.python.org",
    "developer.mozilla.org",
    "docs.oracle.com",
    "docs.microsoft.com", "learn.microsoft.com",
    "developer.apple.com",
    "docs.aws.amazon.com",
    "cloud.google.com",
    "debian.org", "ubuntu.com",
    "nginx.org", "httpd.apache.org",
    "postgresql.org",
    "www.mongodb.com",
    "redis.io",
    "graphql.org",
    "openapi.org", "spec.openapis.org",

    # Pure research / open science
    "arxiv.org",
    "pubmed.ncbi.nlm.nih.gov",
    "www.ncbi.nlm.nih.gov",
    "zenodo.org",
    "figshare.com",
    "osf.io",
    "datadryad.org",
    "www.pangaea.de",
    "www.re3data.org",
    "www.nature.com",
    "www.sciencedirect.com"
]


class SovereignBrowser:
    """
    Sovereign Research Browser - A whitelist-based HTTP client for fetching
    structured data from trusted government and open data sources.
    """
    
    def __init__(
        self,
        allowed_domains: Optional[List[str]] = None,
        user_agent: str = "Strategickhaos-Sovereign-Browser/1.0",
        rate_limit_delay: float = 1.0,
        respect_robots_txt: bool = True,
        timeout: int = 30
    ):
        """
        Initialize the Sovereign Browser.
        
        Args:
            allowed_domains: List of allowed domains (defaults to ALLOWED_DOMAINS)
            user_agent: User agent string for requests
            rate_limit_delay: Delay between requests in seconds
            respect_robots_txt: Whether to respect robots.txt
            timeout: Request timeout in seconds
        """
        self.allowed_domains: Set[str] = set(allowed_domains or ALLOWED_DOMAINS)
        self.user_agent = user_agent
        self.rate_limit_delay = rate_limit_delay
        self.respect_robots_txt = respect_robots_txt
        self.timeout = timeout
        
        # Rate limiting state
        self._last_request_time: Dict[str, float] = {}
        
        # Robots.txt cache
        self._robots_cache: Dict[str, RobotFileParser] = {}
        
        logger.info(f"Initialized Sovereign Browser with {len(self.allowed_domains)} allowed domains")
    
    def is_domain_allowed(self, url: str) -> bool:
        """
        Check if a URL's domain is in the whitelist.
        
        Args:
            url: URL to check
            
        Returns:
            True if domain is allowed, False otherwise
        """
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        
        # Remove port if present
        if ':' in domain:
            domain = domain.split(':')[0]
        
        return domain in self.allowed_domains
    
    async def check_robots_txt(self, url: str) -> bool:
        """
        Check if the URL is allowed by robots.txt.
        
        Args:
            url: URL to check
            
        Returns:
            True if allowed (or robots.txt check disabled), False otherwise
        """
        if not self.respect_robots_txt:
            return True
        
        parsed = urlparse(url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        
        # Check cache
        if robots_url in self._robots_cache:
            rp = self._robots_cache[robots_url]
            return rp.can_fetch(self.user_agent, url)
        
        # Fetch and parse robots.txt
        try:
            rp = RobotFileParser()
            rp.set_url(robots_url)
            
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(robots_url, timeout=5) as response:
                        if response.status == 200:
                            content = await response.text()
                            rp.parse(content.split('\n'))
                except Exception:
                    # If robots.txt doesn't exist or fails, allow by default
                    pass
            
            self._robots_cache[robots_url] = rp
            return rp.can_fetch(self.user_agent, url)
        
        except Exception as e:
            logger.warning(f"Error checking robots.txt for {robots_url}: {e}")
            # On error, allow by default for government/open data sites
            return True
    
    async def rate_limit(self, domain: str):
        """
        Apply rate limiting per domain.
        
        Args:
            domain: Domain to rate limit
        """
        now = time.time()
        last_request = self._last_request_time.get(domain, 0)
        
        elapsed = now - last_request
        if elapsed < self.rate_limit_delay:
            delay = self.rate_limit_delay - elapsed
            logger.debug(f"Rate limiting: waiting {delay:.2f}s for {domain}")
            await asyncio.sleep(delay)
        
        self._last_request_time[domain] = time.time()
    
    async def fetch(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        accept_json: bool = True
    ) -> Tuple[Optional[bytes], int, Dict[str, str]]:
        """
        Fetch content from a whitelisted URL.
        
        Args:
            url: URL to fetch
            headers: Additional headers to send
            accept_json: Add JSON accept header
            
        Returns:
            Tuple of (content, status_code, response_headers)
        """
        # Validate domain
        if not self.is_domain_allowed(url):
            logger.error(f"Domain not in whitelist: {url}")
            raise ValueError(f"Domain not in whitelist: {urlparse(url).netloc}")
        
        # Check robots.txt
        if not await self.check_robots_txt(url):
            logger.warning(f"URL disallowed by robots.txt: {url}")
            raise ValueError(f"URL disallowed by robots.txt: {url}")
        
        # Apply rate limiting
        domain = urlparse(url).netloc
        await self.rate_limit(domain)
        
        # Prepare headers
        request_headers = {
            'User-Agent': self.user_agent,
        }
        
        if accept_json:
            request_headers['Accept'] = 'application/json, application/yaml, text/html'
        
        if headers:
            request_headers.update(headers)
        
        # Fetch content
        logger.info(f"Fetching: {url}")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url,
                    headers=request_headers,
                    timeout=aiohttp.ClientTimeout(total=self.timeout),
                    allow_redirects=True
                ) as response:
                    content = await response.read()
                    response_headers = dict(response.headers)
                    
                    logger.info(f"Fetched {len(content)} bytes from {url} (status: {response.status})")
                    
                    return content, response.status, response_headers
        
        except asyncio.TimeoutError:
            logger.error(f"Timeout fetching {url}")
            raise
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            raise
    
    async def fetch_json(self, url: str) -> Optional[Dict]:
        """
        Fetch and parse JSON from a URL.
        
        Args:
            url: URL to fetch
            
        Returns:
            Parsed JSON object or None on error
        """
        content, status, _ = await self.fetch(url, accept_json=True)
        
        if status == 200 and content:
            try:
                return json.loads(content.decode('utf-8'))
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON from {url}: {e}")
                return None
        
        return None
    
    async def fetch_yaml(self, url: str) -> Optional[Dict]:
        """
        Fetch and parse YAML from a URL.
        
        Args:
            url: URL to fetch
            
        Returns:
            Parsed YAML object or None on error
        """
        content, status, _ = await self.fetch(url)
        
        if status == 200 and content:
            try:
                return yaml.safe_load(content.decode('utf-8'))
            except yaml.YAMLError as e:
                logger.error(f"Failed to parse YAML from {url}: {e}")
                return None
        
        return None
    
    async def fetch_text(self, url: str) -> Optional[str]:
        """
        Fetch text content from a URL.
        
        Args:
            url: URL to fetch
            
        Returns:
            Text content or None on error
        """
        content, status, _ = await self.fetch(url)
        
        if status == 200 and content:
            return content.decode('utf-8', errors='replace')
        
        return None
    
    def load_whitelist_from_yaml(self, yaml_path: str):
        """
        Load whitelist from a YAML file.
        
        Args:
            yaml_path: Path to YAML file containing domains
        """
        try:
            with open(yaml_path, 'r') as f:
                config = yaml.safe_load(f)
                
            domains = config.get('allowed_domains', [])
            if domains:
                self.allowed_domains = set(domains)
                logger.info(f"Loaded {len(domains)} domains from {yaml_path}")
        
        except Exception as e:
            logger.error(f"Failed to load whitelist from {yaml_path}: {e}")
            raise
    
    def save_whitelist_to_yaml(self, yaml_path: str):
        """
        Save current whitelist to a YAML file.
        
        Args:
            yaml_path: Path to save YAML file
        """
        try:
            config = {
                'allowed_domains': sorted(list(self.allowed_domains)),
                'metadata': {
                    'version': '1.0',
                    'description': 'Sovereign Research Browser Whitelist',
                    'last_updated': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
                }
            }
            
            with open(yaml_path, 'w') as f:
                yaml.dump(config, f, default_flow_style=False, sort_keys=True)
            
            logger.info(f"Saved {len(self.allowed_domains)} domains to {yaml_path}")
        
        except Exception as e:
            logger.error(f"Failed to save whitelist to {yaml_path}: {e}")
            raise


async def main():
    """Main entry point for CLI usage."""
    parser = argparse.ArgumentParser(
        description='Sovereign Research Browser - Fetch data from whitelisted sources'
    )
    parser.add_argument('url', nargs='?', help='URL to fetch')
    parser.add_argument('--format', choices=['json', 'yaml', 'text'], default='text',
                        help='Expected content format')
    parser.add_argument('--output', '-o', help='Output file path')
    parser.add_argument('--list-domains', action='store_true',
                        help='List all allowed domains')
    parser.add_argument('--check-domain', help='Check if a domain is allowed')
    parser.add_argument('--no-robots', action='store_true',
                        help='Disable robots.txt checking')
    parser.add_argument('--rate-limit', type=float, default=1.0,
                        help='Rate limit delay in seconds (default: 1.0)')
    
    args = parser.parse_args()
    
    # Initialize browser
    browser = SovereignBrowser(
        respect_robots_txt=not args.no_robots,
        rate_limit_delay=args.rate_limit
    )
    
    # Handle list domains
    if args.list_domains:
        print("Allowed Domains:")
        for domain in sorted(browser.allowed_domains):
            print(f"  - {domain}")
        return 0
    
    # Handle check domain
    if args.check_domain:
        is_allowed = args.check_domain in browser.allowed_domains
        status = "✓ ALLOWED" if is_allowed else "✗ NOT ALLOWED"
        print(f"{args.check_domain}: {status}")
        return 0 if is_allowed else 1
    
    # Require URL for fetch operations
    if not args.url:
        parser.error("URL is required when not using --list-domains or --check-domain")
    
    # Fetch content
    try:
        if args.format == 'json':
            data = await browser.fetch_json(args.url)
            output = json.dumps(data, indent=2)
        elif args.format == 'yaml':
            data = await browser.fetch_yaml(args.url)
            output = yaml.dump(data, default_flow_style=False)
        else:
            output = await browser.fetch_text(args.url)
        
        # Write output
        if args.output:
            Path(args.output).write_text(output)
            print(f"Saved to {args.output}")
        else:
            print(output)
        
        return 0
    
    except Exception as e:
        logger.error(f"Failed to fetch {args.url}: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(asyncio.run(main()))
