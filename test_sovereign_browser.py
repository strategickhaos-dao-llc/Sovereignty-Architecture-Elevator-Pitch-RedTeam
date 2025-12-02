#!/usr/bin/env python3
"""
Tests for Sovereign Research Browser
Validates domain whitelist and basic functionality
"""

import pytest
import asyncio
from main import SovereignBrowser, ALLOWED_DOMAINS


class TestSovereignBrowser:
    """Test suite for Sovereign Research Browser"""
    
    def test_allowed_domains_count(self):
        """Test that we have 100+ allowed domains"""
        assert len(ALLOWED_DOMAINS) >= 100, f"Expected at least 100 domains, got {len(ALLOWED_DOMAINS)}"
    
    def test_domain_categories_present(self):
        """Test that key domain categories are present"""
        domains_set = set(ALLOWED_DOMAINS)
        
        # US Federal domains
        assert "data.gov" in domains_set
        assert "api.nasa.gov" in domains_set
        assert "www.census.gov" in domains_set
        assert "www.loc.gov" in domains_set
        
        # International government
        assert "data.gov.uk" in domains_set
        assert "data.europa.eu" in domains_set
        assert "open.canada.ca" in domains_set
        
        # Open data organizations
        assert "data.worldbank.org" in domains_set
        assert "data.un.org" in domains_set
        
        # Documentation sites
        assert "docs.python.org" in domains_set
        assert "developer.mozilla.org" in domains_set
        
        # Research/science
        assert "arxiv.org" in domains_set
        assert "zenodo.org" in domains_set
    
    def test_browser_initialization(self):
        """Test browser initializes correctly"""
        browser = SovereignBrowser()
        assert len(browser.allowed_domains) >= 100
        assert browser.user_agent == "Strategickhaos-Sovereign-Browser/1.0"
        assert browser.rate_limit_delay == 1.0
        assert browser.respect_robots_txt is True
    
    def test_domain_allowed_checking(self):
        """Test domain whitelist checking"""
        browser = SovereignBrowser()
        
        # Test allowed domains
        assert browser.is_domain_allowed("https://data.gov/api/test")
        assert browser.is_domain_allowed("https://api.nasa.gov/openapi.yaml")
        assert browser.is_domain_allowed("https://arxiv.org/pdf/1234.pdf")
        
        # Test not allowed domains
        assert not browser.is_domain_allowed("https://example.com/data")
        assert not browser.is_domain_allowed("https://malicious-site.com/")
        assert not browser.is_domain_allowed("https://random.org/api")
    
    def test_domain_checking_with_ports(self):
        """Test domain checking handles ports correctly"""
        browser = SovereignBrowser()
        
        # Ports should be stripped when checking
        assert browser.is_domain_allowed("https://data.gov:443/api/test")
        assert browser.is_domain_allowed("http://data.gov:80/api/test")
    
    def test_custom_whitelist(self):
        """Test browser with custom whitelist"""
        custom_domains = ["example.com", "test.org"]
        browser = SovereignBrowser(allowed_domains=custom_domains)
        
        assert len(browser.allowed_domains) == 2
        assert browser.is_domain_allowed("https://example.com/test")
        assert browser.is_domain_allowed("https://test.org/api")
        assert not browser.is_domain_allowed("https://data.gov/api")
    
    def test_whitelist_yaml_operations(self, tmp_path):
        """Test loading and saving whitelist from/to YAML"""
        browser = SovereignBrowser()
        
        # Save to YAML
        yaml_path = tmp_path / "test_whitelist.yaml"
        browser.save_whitelist_to_yaml(str(yaml_path))
        
        assert yaml_path.exists()
        
        # Load from YAML
        browser2 = SovereignBrowser(allowed_domains=["example.com"])
        browser2.load_whitelist_from_yaml(str(yaml_path))
        
        # Should have same domains
        assert browser.allowed_domains == browser2.allowed_domains
    
    @pytest.mark.asyncio
    async def test_fetch_requires_whitelisted_domain(self):
        """Test that fetch rejects non-whitelisted domains"""
        browser = SovereignBrowser()
        
        with pytest.raises(ValueError, match="Domain not in whitelist"):
            await browser.fetch("https://not-allowed-domain.com/api")
    
    def test_no_duplicate_domains(self):
        """Test that whitelist has no duplicate domains"""
        domains_list = ALLOWED_DOMAINS
        domains_set = set(ALLOWED_DOMAINS)
        
        assert len(domains_list) == len(domains_set), \
            "Whitelist contains duplicate domains"
    
    def test_all_domains_lowercase(self):
        """Test that all domains are lowercase for consistency"""
        for domain in ALLOWED_DOMAINS:
            assert domain == domain.lower(), \
                f"Domain {domain} should be lowercase"
    
    def test_gov_domains_present(self):
        """Test that .gov domains are properly included"""
        gov_domains = [d for d in ALLOWED_DOMAINS if '.gov' in d]
        assert len(gov_domains) >= 30, \
            f"Expected at least 30 .gov domains, got {len(gov_domains)}"
    
    def test_international_coverage(self):
        """Test that international domains are included"""
        intl_domains = [
            d for d in ALLOWED_DOMAINS 
            if any(tld in d for tld in ['.uk', '.eu', '.in', '.ca', '.br', '.au', '.fr', '.de', '.es', '.it', '.nz', '.kr', '.sg', '.hk', '.il'])
        ]
        assert len(intl_domains) >= 15, \
            f"Expected at least 15 international domains, got {len(intl_domains)}"


class TestDomainCategories:
    """Test specific domain categories"""
    
    def test_us_federal_domains(self):
        """Test US federal government domains"""
        required_federal = [
            "data.gov", "api.nasa.gov", "www.census.gov", "www.loc.gov",
            "api.weather.gov", "www.epa.gov", "healthdata.gov"
        ]
        
        for domain in required_federal:
            assert domain in ALLOWED_DOMAINS, f"Missing required federal domain: {domain}"
    
    def test_open_data_organizations(self):
        """Test major open data organizations"""
        required_orgs = [
            "data.worldbank.org", "data.un.org", "data.oecd.org",
            "www.who.int", "www.fao.org"
        ]
        
        for domain in required_orgs:
            assert domain in ALLOWED_DOMAINS, f"Missing required org domain: {domain}"
    
    def test_documentation_sites(self):
        """Test documentation sites"""
        required_docs = [
            "docs.python.org", "developer.mozilla.org", "docs.microsoft.com",
            "kubernetes.io", "postgresql.org"
        ]
        
        for domain in required_docs:
            assert domain in ALLOWED_DOMAINS, f"Missing required docs domain: {domain}"
    
    def test_research_platforms(self):
        """Test research and science platforms"""
        required_research = [
            "arxiv.org", "zenodo.org", "figshare.com", "osf.io",
            "pubmed.ncbi.nlm.nih.gov"
        ]
        
        for domain in required_research:
            assert domain in ALLOWED_DOMAINS, f"Missing required research domain: {domain}"


if __name__ == '__main__':
    # Run tests
    pytest.main([__file__, '-v'])
