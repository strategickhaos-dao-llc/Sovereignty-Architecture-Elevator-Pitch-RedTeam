"""
Sovereign Research Browser Node - SAFE RESEARCH VERSION
Built for Strategickhaos Swarm Intelligence
Legally compliant research browser for public documentation (Van Buren v. US 2021 compliant)
"""

import asyncio
import datetime
import json
import os
from typing import Optional
from urllib.parse import urlparse

from fastapi import FastAPI, Query, HTTPException
from playwright.async_api import async_playwright
from pydantic import BaseModel, Field
import uvicorn


app = FastAPI(
    title="Sovereign Research Browser Node",
    description="Legally compliant research browser for public documentation sites",
    version="1.0.0"
)


# === SAFETY CONFIG – ONLY ALLOW RESEARCH DOMAINS ===
ALLOWED_DOMAINS = [
    "docs.python.org",
    "developer.mozilla.org",
    "pypi.org",
    "github.com",
    "wikipedia.org",
    "arxiv.org",
    "rfc-editor.org",
    "ietf.org",
    "nginx.com",
    "cloudflare.com",
    "proton.me",
    "tailscale.com",
    # Add your own infrastructure / open docs here
]

# Configure logs directory
LOGS_DIR = os.environ.get("LOGS_DIR", "/logs")
os.makedirs(LOGS_DIR, exist_ok=True)


class BrowseResponse(BaseModel):
    """Response model for browse endpoint"""
    url: str = Field(..., description="Final URL after navigation")
    title: str = Field(..., description="Page title")
    text_preview: str = Field(..., description="Preview of page text content")
    allowed: bool = Field(..., description="Whether domain is in allowed list")


def is_allowed(url: str) -> bool:
    """Check if URL domain is in allowed research domains list"""
    domain = urlparse(url).netloc.lower()
    return any(domain.endswith(d) for d in ALLOWED_DOMAINS) or domain in ALLOWED_DOMAINS


def psyche_log(event: str, **kwargs):
    """Log events to PsycheVille event log in JSONL format"""
    entry = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z"),
        "event": event,
        **kwargs
    }
    log_path = os.path.join(LOGS_DIR, "events.jsonl")
    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception as e:
        # Fail gracefully if logging fails
        print(f"Failed to write to log: {e}")


async def research_browse(url: str) -> BrowseResponse:
    """
    Browse a URL using Playwright and extract content
    
    Args:
        url: The URL to browse
        
    Returns:
        BrowseResponse with page content
        
    Raises:
        HTTPException: If domain is not in allowed list
    """
    if not is_allowed(url):
        domain = urlparse(url).netloc
        psyche_log("research_browse_blocked", url=url, domain=domain, reason="not_in_allowlist")
        raise HTTPException(
            status_code=403,
            detail=f"Domain {domain} not in allowed research list"
        )

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080}
        )
        page = await context.new_page()
        
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            await page.wait_for_timeout(2000)
            
            final_url = page.url
            title = await page.title()
            text_content = await page.eval_on_selector(
                "body",
                "el => el.innerText.substring(0, 8000)"
            )
            
            psyche_log("research_browse_success", url=final_url, title=title)
            
            return BrowseResponse(
                url=final_url,
                title=title,
                text_preview=text_content,
                allowed=True
            )
        except Exception as e:
            psyche_log("research_browse_error", url=url, error=str(e))
            raise HTTPException(
                status_code=500,
                detail=f"Failed to browse URL: {str(e)}"
            )
        finally:
            await browser.close()


@app.get("/browse", response_model=BrowseResponse)
async def browse(url: str = Query(..., description="URL to browse (must be in allowed domains)")):
    """
    Browse a public documentation URL and extract content
    
    This endpoint only allows browsing of pre-approved research domains to ensure
    legal compliance with CFAA (Computer Fraud and Abuse Act) per Van Buren v. US (2021).
    """
    return await research_browse(url)


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "sovereign_research_node",
        "node": os.uname().nodename,
        "allowed_domains_count": len(ALLOWED_DOMAINS)
    }


@app.get("/domains")
async def list_domains():
    """List all allowed research domains"""
    return {
        "allowed_domains": sorted(ALLOWED_DOMAINS),
        "count": len(ALLOWED_DOMAINS)
    }


if __name__ == "__main__":
    port = int(os.environ.get("SOVEREIGN_BROWSER_PORT", 8086))
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
