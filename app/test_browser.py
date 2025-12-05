"""
Basic tests for Sovereign Research Browser
"""

import asyncio
from pathlib import Path

from browser import ResearchBrowser


def test_load_allowed_domains():
    """Test that allowed domains are loaded correctly"""
    browser = ResearchBrowser()
    assert len(browser.allowed_domains) > 0
    assert "github.com" in browser.allowed_domains
    assert "arxiv.org" in browser.allowed_domains


def test_domain_whitelist_checking():
    """Test domain whitelist logic"""
    browser = ResearchBrowser()
    
    # Test allowed domains
    assert browser._is_domain_allowed("https://github.com/test/repo")
    assert browser._is_domain_allowed("https://arxiv.org/abs/1234.5678")
    assert browser._is_domain_allowed("https://developer.mozilla.org/en-US/docs/Web")
    
    # Test subdomains
    assert browser._is_domain_allowed("https://docs.python.org/3/")
    
    # Test disallowed domains
    assert not browser._is_domain_allowed("https://evil.com/malware")
    assert not browser._is_domain_allowed("https://random-site.net/")


def test_rate_limiting():
    """Test rate limiting logic"""
    browser = ResearchBrowser(rate_limit_requests_per_minute=5)
    
    # Should not be rate limited initially
    is_limited, wait_time = browser._check_rate_limit("example.com")
    assert not is_limited
    
    # Record multiple requests
    for _ in range(5):
        browser._record_request("example.com")
    
    # Should be rate limited now
    is_limited, wait_time = browser._check_rate_limit("example.com")
    assert is_limited
    assert wait_time > 0


async def test_browse_disallowed_domain():
    """Test browsing a disallowed domain"""
    browser = ResearchBrowser()
    
    response = await browser.browse("https://evil.com/test")
    
    assert not response.research_allowed
    assert response.error is not None
    assert "whitelist" in response.error.lower()
    
    await browser.close()


async def test_browse_allowed_domain():
    """Test browsing an allowed domain (with actual network call)"""
    browser = ResearchBrowser()
    
    # Use a reliable, fast endpoint
    response = await browser.browse("https://www.python.org/")
    
    # If not rate limited or blocked by robots.txt
    if response.research_allowed and response.robots_compliant and not response.rate_limited:
        assert response.status_code == 200
        assert response.title is not None
        assert len(response.text_preview) > 0
    
    await browser.close()


if __name__ == "__main__":
    # Run basic tests
    print("Testing allowed domains loading...")
    test_load_allowed_domains()
    print("✓ Passed\n")
    
    print("Testing domain whitelist checking...")
    test_domain_whitelist_checking()
    print("✓ Passed\n")
    
    print("Testing rate limiting...")
    test_rate_limiting()
    print("✓ Passed\n")
    
    print("Testing browse with disallowed domain...")
    asyncio.run(test_browse_disallowed_domain())
    print("✓ Passed\n")
    
    print("Testing browse with allowed domain (requires network)...")
    asyncio.run(test_browse_allowed_domain())
    print("✓ Passed\n")
    
    print("All tests passed!")
