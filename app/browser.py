"""
Sovereign Research Browser - Core functionality
Polite, whitelisted, robots.txt-respecting research browser
"""

import asyncio
import hashlib
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

import httpx
import structlog
import yaml
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field

logger = structlog.get_logger()


class BrowseResponse(BaseModel):
    """Response model for browse requests"""
    url: str
    title: Optional[str] = None
    text_preview: str = Field(default="", description="Preview of page content (max ~10k chars)")
    research_allowed: bool = Field(default=True, description="Whether domain is whitelisted")
    rate_limited: bool = Field(default=False, description="Whether request was rate limited")
    robots_compliant: bool = Field(default=True, description="Whether request respects robots.txt")
    error: Optional[str] = None
    status_code: Optional[int] = None
    content_type: Optional[str] = None


class PsycheLogEntry(BaseModel):
    """Structured log entry for psyche logging"""
    timestamp: str
    url: str
    domain: str
    path: str
    allowed: bool
    robots_compliant: bool
    rate_limited: bool
    status_code: Optional[int] = None
    error: Optional[str] = None
    response_time_ms: float


class ResearchBrowser:
    """
    Sovereign Research Browser
    
    Features:
    - Domain whitelist enforcement
    - robots.txt compliance
    - Per-domain rate limiting
    - Structured psyche logging
    - Polite user agent
    """
    
    def __init__(
        self,
        allowed_domains_path: str = None,
        rate_limit_requests_per_minute: int = 12,
        max_content_length: int = 10000,
        user_agent: str = "SovereignResearchBrowser/1.0 (Polite; +https://github.com/Strategickhaos)"
    ):
        # Load allowed domains
        if allowed_domains_path is None:
            allowed_domains_path = Path(__file__).parent / "allowed_domains.yaml"
        
        self.allowed_domains = self._load_allowed_domains(allowed_domains_path)
        self.rate_limit_rpm = rate_limit_requests_per_minute
        self.max_content_length = max_content_length
        self.user_agent = user_agent
        
        # Rate limiting state
        self.domain_request_times: Dict[str, List[float]] = defaultdict(list)
        
        # Robots.txt cache
        self.robots_cache: Dict[str, RobotFileParser] = {}
        
        # HTTP client
        self.client = httpx.AsyncClient(
            headers={"User-Agent": self.user_agent},
            timeout=httpx.Timeout(30.0),
            follow_redirects=True,
        )
        
        logger.info(
            "research_browser_initialized",
            allowed_domains=len(self.allowed_domains),
            rate_limit_rpm=rate_limit_requests_per_minute
        )
    
    def _load_allowed_domains(self, path: Path) -> List[str]:
        """Load allowed domains from YAML file"""
        try:
            with open(path, "r") as f:
                config = yaml.safe_load(f)
                domains = config.get("allowed_domains", [])
                logger.info("loaded_allowed_domains", count=len(domains), path=str(path))
                return domains
        except Exception as e:
            logger.error("failed_to_load_domains", error=str(e), path=str(path))
            return []
    
    def _is_domain_allowed(self, url: str) -> bool:
        """Check if domain is in whitelist"""
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        
        # Direct match
        if domain in self.allowed_domains:
            return True
        
        # Check if any allowed domain is a suffix (e.g., allows subdomains)
        for allowed in self.allowed_domains:
            if domain.endswith(f".{allowed}") or domain == allowed:
                return True
        
        return False
    
    def _check_rate_limit(self, domain: str) -> Tuple[bool, float]:
        """
        Check if request would exceed rate limit for domain
        Returns (is_limited, seconds_to_wait)
        """
        current_time = time.time()
        
        # Clean old requests (older than 60 seconds)
        self.domain_request_times[domain] = [
            t for t in self.domain_request_times[domain]
            if current_time - t < 60
        ]
        
        # Check rate limit
        request_count = len(self.domain_request_times[domain])
        if request_count >= self.rate_limit_rpm:
            # Calculate time to wait
            oldest_request = min(self.domain_request_times[domain])
            seconds_to_wait = 60 - (current_time - oldest_request)
            return True, max(0, seconds_to_wait)
        
        return False, 0
    
    def _record_request(self, domain: str):
        """Record a request for rate limiting"""
        self.domain_request_times[domain].append(time.time())
    
    async def _check_robots_txt(self, url: str) -> bool:
        """Check if URL is allowed by robots.txt"""
        parsed = urlparse(url)
        domain = parsed.netloc
        robots_url = f"{parsed.scheme}://{domain}/robots.txt"
        
        # Check cache
        if domain not in self.robots_cache:
            try:
                # Fetch robots.txt
                response = await self.client.get(robots_url, timeout=5.0)
                rp = RobotFileParser()
                rp.parse(response.text.splitlines())
                self.robots_cache[domain] = rp
            except Exception as e:
                logger.debug("robots_txt_fetch_failed", domain=domain, error=str(e))
                # If robots.txt can't be fetched, allow by default (be polite)
                rp = RobotFileParser()
                rp.allow_all = True
                self.robots_cache[domain] = rp
        
        # Check if URL is allowed
        rp = self.robots_cache[domain]
        return rp.can_fetch(self.user_agent, url)
    
    async def browse(self, url: str) -> BrowseResponse:
        """
        Browse a URL with whitelist, robots.txt, and rate limiting
        """
        start_time = time.time()
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        
        # Initialize response
        response = BrowseResponse(url=url)
        
        # 1. Check domain whitelist
        if not self._is_domain_allowed(url):
            response.research_allowed = False
            response.error = "Domain not in whitelist"
            self._log_psyche_entry(url, domain, parsed.path, response, start_time)
            return response
        
        # 2. Check robots.txt
        robots_allowed = await self._check_robots_txt(url)
        if not robots_allowed:
            response.robots_compliant = False
            response.error = "Disallowed by robots.txt"
            self._log_psyche_entry(url, domain, parsed.path, response, start_time)
            return response
        
        # 3. Check rate limit
        is_limited, wait_time = self._check_rate_limit(domain)
        if is_limited:
            response.rate_limited = True
            response.error = f"Rate limited. Retry after {wait_time:.1f} seconds"
            self._log_psyche_entry(url, domain, parsed.path, response, start_time)
            return response
        
        # 4. Fetch the page
        try:
            self._record_request(domain)
            
            http_response = await self.client.get(url)
            response.status_code = http_response.status_code
            response.content_type = http_response.headers.get("content-type", "")
            
            # Check if response is HTML
            if "text/html" not in response.content_type.lower():
                response.error = f"Non-HTML content type: {response.content_type}"
                self._log_psyche_entry(url, domain, parsed.path, response, start_time)
                return response
            
            # Parse HTML
            soup = BeautifulSoup(http_response.text, "html.parser")
            
            # Extract title
            title_tag = soup.find("title")
            if title_tag:
                response.title = title_tag.get_text(strip=True)
            
            # Extract text content
            # Remove script and style elements
            for script_or_style in soup(["script", "style"]):
                script_or_style.decompose()
            
            # Get text
            text = soup.get_text(separator="\n", strip=True)
            
            # Limit text preview
            response.text_preview = text[:self.max_content_length]
            if len(text) > self.max_content_length:
                response.text_preview += "\n\n[... content truncated ...]"
            
            logger.info(
                "browse_success",
                url=url,
                domain=domain,
                title=response.title,
                content_length=len(text),
                status_code=response.status_code
            )
            
        except httpx.TimeoutException:
            response.error = "Request timeout"
            logger.warning("browse_timeout", url=url, domain=domain)
        except httpx.HTTPError as e:
            response.error = f"HTTP error: {str(e)}"
            logger.warning("browse_http_error", url=url, domain=domain, error=str(e))
        except Exception as e:
            response.error = f"Unexpected error: {str(e)}"
            logger.error("browse_error", url=url, domain=domain, error=str(e))
        
        # Log psyche entry
        self._log_psyche_entry(url, domain, parsed.path, response, start_time)
        
        return response
    
    def _log_psyche_entry(
        self,
        url: str,
        domain: str,
        path: str,
        response: BrowseResponse,
        start_time: float
    ):
        """Log structured psyche entry"""
        response_time = (time.time() - start_time) * 1000  # Convert to ms
        
        entry = PsycheLogEntry(
            timestamp=datetime.utcnow().isoformat(),
            url=url,
            domain=domain,
            path=path,
            allowed=response.research_allowed,
            robots_compliant=response.robots_compliant,
            rate_limited=response.rate_limited,
            status_code=response.status_code,
            error=response.error,
            response_time_ms=response_time
        )
        
        logger.info("psyche_log", **entry.dict())
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()
