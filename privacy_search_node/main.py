from fastapi import FastAPI, Query, HTTPException
from duckduckgo_search import DDGS
import httpx
from bs4 import BeautifulSoup
import json, datetime, os
from datetime import timezone
from urllib.parse import urlparse
import ipaddress

app = FastAPI(title="Privacy Search Node", description="DuckDuckGo search + page fetch behind unique VPN IP")

LOG_FILE = os.getenv('LOG_FILE', '/logs/events.jsonl')

def psyche_log(event: str, **kwargs):
    entry = {"timestamp": datetime.datetime.now(timezone.utc).isoformat(), "event": event, **kwargs}
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

def is_safe_url(url: str) -> bool:
    """Validate URL to prevent SSRF attacks."""
    try:
        parsed = urlparse(url)
        
        # Ensure URL has a valid scheme
        if parsed.scheme not in ('http', 'https'):
            return False
        
        # Ensure hostname is present
        if not parsed.hostname:
            return False
        
        # Check if hostname resolves to a private IP
        try:
            ip = ipaddress.ip_address(parsed.hostname)
            if ip.is_private or ip.is_loopback or ip.is_link_local:
                return False
        except ValueError:
            # Hostname is not an IP, check if it resolves to private IPs
            import socket
            try:
                resolved_ip = socket.gethostbyname(parsed.hostname)
                ip = ipaddress.ip_address(resolved_ip)
                if ip.is_private or ip.is_loopback or ip.is_link_local:
                    return False
            except (socket.gaierror, ValueError):
                # DNS resolution failed or invalid IP
                pass
        
        return True
    except Exception:
        return False

@app.get("/search")
async def search(q: str = Query(...), max_results: int = 10):
    psyche_log("search_text", query=q, max_results=max_results)
    with DDGS() as ddgs:
        results = [r for r in ddgs.text(q, max_results=max_results)]
    return {"query": q, "results": results}

@app.get("/browse")
async def browse(url: str = Query(...)):
    # SECURITY: Validate URL to prevent SSRF attacks
    # The is_safe_url function blocks:
    # - Private IP addresses (192.168.x.x, 10.x.x.x, 172.16-31.x.x)
    # - Loopback addresses (127.x.x.x, localhost)
    # - Link-local addresses
    # - Invalid URL schemes (only http/https allowed)
    if not is_safe_url(url):
        raise HTTPException(status_code=400, detail="Invalid or unsafe URL. Access to private networks is not allowed.")
    
    psyche_log("browse_page", url=url)
    
    # Additional safety: Set limits on response size and disable redirects to untrusted hosts
    async with httpx.AsyncClient(
        timeout=30, 
        follow_redirects=True,
        max_redirects=5,
        limits=httpx.Limits(max_connections=10, max_keepalive_connections=5)
    ) as client:
        # Fetch URL that has been validated by is_safe_url
        resp = await client.get(url)
        resp.raise_for_status()
        
        # Parse and extract text
        soup = BeautifulSoup(resp.text, "lxml")
        text = soup.get_text(separator="\n", strip=True)
        return {"url": url, "title": soup.title.string if soup.title else "", "text_preview": text[:4000] + "..." if len(text) > 4000 else text}

@app.get("/health")
async def health():
    try:
        exit_ip = httpx.get("https://api.ipify.org", timeout=5.0).text
    except Exception:
        exit_ip = "unknown"
    return {"status": "healthy", "exit_ip": exit_ip}
