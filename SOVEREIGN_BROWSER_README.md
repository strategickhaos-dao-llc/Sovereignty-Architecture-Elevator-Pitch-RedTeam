# Sovereign Research Browser

A legally-clean, whitelist-based research browser for fetching structured data from government portals, open data sources, and documentation sites. Perfect for feeding structured data (JSON/YAML/OpenAPI specs) to your subject-matter-expert LLMs.

## Features

- **100+ Whitelisted Domains**: Curated list of public sector and standards body domains
- **Legally Clean**: All domains explicitly encourage programmatic access
- **Rate Limiting**: Configurable per-domain rate limiting
- **Robots.txt Respect**: Optional robots.txt checking
- **Multiple Formats**: Support for JSON, YAML, and text content
- **Async Support**: Built on asyncio for efficient concurrent requests
- **YAML Configuration**: Load/save whitelists dynamically

## Domain Categories

The whitelist includes domains from:

- **US Federal Government** (50+ domains): data.gov, NASA, Census, Library of Congress, NOAA, EPA, etc.
- **International Government Portals**: UK, EU, Canada, Australia, Brazil, France, Germany, and more
- **Open Data Organizations**: World Bank, UN, OECD, WHO, FAO, IMF, WTO
- **Standards Bodies**: IETF, W3C, OpenAPI, Schema.org, Kubernetes
- **Documentation Sites**: Python, Mozilla, Microsoft, AWS, Google Cloud, PostgreSQL, MongoDB
- **Research Platforms**: arXiv, Zenodo, Figshare, OSF, PubMed, NCBI

## Installation

```bash
# Install dependencies
pip install aiohttp pyyaml

# Make executable
chmod +x main.py
```

## Usage

### Command Line Interface

```bash
# Fetch JSON data
python main.py https://api.nasa.gov/openapi.yaml --format yaml

# Fetch and save to file
python main.py https://catalog.data.gov/api/3/action/package_search?q=climate \
    --format json --output climate_data.json

# List all allowed domains
python main.py --list-domains

# Check if a domain is allowed
python main.py --check-domain data.gov

# Disable robots.txt checking (not recommended)
python main.py https://data.gov/api/test --no-robots

# Custom rate limiting (2 second delay)
python main.py https://api.census.gov/data --rate-limit 2.0
```

### Python API

```python
import asyncio
from main import SovereignBrowser

async def fetch_data():
    # Initialize browser
    browser = SovereignBrowser(
        rate_limit_delay=1.0,
        respect_robots_txt=True
    )
    
    # Fetch JSON data
    data = await browser.fetch_json(
        "https://catalog.data.gov/api/3/action/package_search?q=climate"
    )
    print(f"Found {data['result']['count']} datasets")
    
    # Fetch YAML data
    openapi_spec = await browser.fetch_yaml(
        "https://api.nasa.gov/openapi.yaml"
    )
    
    # Check if domain is allowed
    if browser.is_domain_allowed("https://data.gov/api/test"):
        content = await browser.fetch_text("https://data.gov/api/test")

# Run
asyncio.run(fetch_data())
```

### Load Whitelist from YAML

```python
from main import SovereignBrowser

browser = SovereignBrowser()

# Load from YAML file
browser.load_whitelist_from_yaml("sovereign_browser_whitelist.yaml")

# Save current whitelist
browser.save_whitelist_to_yaml("my_whitelist.yaml")
```

## Example API Endpoints

Here are some example endpoints that return clean JSON/YAML for your swarm:

### US Government APIs

```bash
# NASA OpenAPI specification
curl -L -s https://api.nasa.gov/openapi.yaml

# Library of Congress collections
curl -L -s "https://www.loc.gov/collections/?fo=json"

# Data.gov catalog search
curl -L -s "https://catalog.data.gov/api/3/action/package_search?q=climate"

# Census Bureau data
curl -L -s "https://api.census.gov/data/2020/dec/pl?get=NAME,P1_001N&for=state:*"

# NOAA tides and currents
curl -L -s "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?product=predictions&datum=MLLW&station=8454000&format=json"
```

### International Government APIs

```bash
# UK data.gov.uk API
curl -L -s "https://data.gov.uk/api/3/action/package_list"

# EU data portal search
curl -L -s "https://data.europa.eu/api/hub/search/datasets?limit=10" | jq .

# Canadian open data
curl -L -s "https://open.canada.ca/data/api/3/action/package_search?q=covid"
```

### Open Data Organizations

```bash
# World Bank population indicators
curl -L -s "https://api.worldbank.org/v2/country/all/indicator/SP.POP.TOTL?format=json"

# OECD data
curl -L -s "https://data.oecd.org/api/sdmx-json/dataset"

# UN statistics
curl -L -s "https://data.un.org/ws/rest/data/IAEG-SDGs/1.1.1/latest"
```

### Documentation & Standards

```bash
# Python documentation
curl -L -s "https://docs.python.org/3/objects.inv"

# Kubernetes API reference
curl -L -s "https://kubernetes.io/docs/reference/kubernetes-api/"

# OpenAPI specification
curl -L -s "https://spec.openapis.org/oas/v3.1.0"
```

## Configuration

The `sovereign_browser_whitelist.yaml` file contains:

- Full list of 100+ allowed domains
- Metadata and versioning
- Example endpoints by category
- Usage guidelines
- Legal compliance notes

## Rate Limiting

Default rate limiting is 1 second per domain. This ensures respectful access to public APIs without overwhelming servers.

```python
# Custom rate limiting
browser = SovereignBrowser(rate_limit_delay=2.0)  # 2 seconds between requests
```

## Robots.txt Compliance

By default, the browser respects robots.txt. For government and open data sites that explicitly encourage programmatic access, you can disable this:

```python
browser = SovereignBrowser(respect_robots_txt=False)
```

## Security & Legal Compliance

All domains in the whitelist are:

- ✅ Public sector or standards bodies
- ✅ Explicitly encourage programmatic access or are documentation
- ✅ No authentication required
- ✅ No login walls or paywalls
- ✅ 100% research-friendly and legally clean
- ✅ Perfect for feeding structured data to LLMs

## Testing

Run the test suite to validate the implementation:

```bash
# Install pytest if needed
pip install pytest pytest-asyncio

# Run tests
python -m pytest test_sovereign_browser.py -v

# Or run directly
python test_sovereign_browser.py
```

## Advanced Usage

### Concurrent Fetching

```python
import asyncio
from main import SovereignBrowser

async def fetch_multiple():
    browser = SovereignBrowser()
    
    urls = [
        "https://api.nasa.gov/openapi.yaml",
        "https://catalog.data.gov/api/3/action/package_list",
        "https://data.gov.uk/api/3/action/package_list",
    ]
    
    # Fetch concurrently
    tasks = [browser.fetch_text(url) for url in urls]
    results = await asyncio.gather(*tasks)
    
    for url, content in zip(urls, results):
        print(f"Fetched {len(content)} bytes from {url}")

asyncio.run(fetch_multiple())
```

### Custom User Agent

```python
browser = SovereignBrowser(
    user_agent="MyResearchBot/1.0 (contact@example.com)"
)
```

### Timeout Configuration

```python
browser = SovereignBrowser(timeout=60)  # 60 second timeout
```

## Architecture

The Sovereign Research Browser is designed for:

- **Swarm Intelligence**: Fetch data from hundreds of sources concurrently
- **RAG Feeding**: Structured data perfect for feeding to LLMs
- **Subject Matter Experts**: Enable AI agents to access authoritative sources
- **Legally Clean**: Zero risk of ToS violations or copyright issues
- **Global Scale**: Access the world's open government data ecosystem

## Integration with Strategickhaos Architecture

This browser integrates with the broader Sovereignty Architecture:

- **Refinory AI Agents**: Feed data to expert agents
- **RAG Collections**: Ingest into Qdrant vector database
- **Discord Bot**: Trigger data fetching from Discord commands
- **Cyber Recon**: Collect security and compliance data
- **LLM Research**: Ingest papers and documentation

## Future Enhancements

- [ ] Add GraphQL endpoint support
- [ ] Implement SPARQL query support for semantic web
- [ ] Add caching layer (Redis)
- [ ] Create pre-built data collection workflows
- [ ] Add webhook support for real-time updates
- [ ] Implement retry logic with exponential backoff
- [ ] Add Prometheus metrics for monitoring
- [ ] Support for bulk downloads
- [ ] Create domain-specific extractors (e.g., NASA APIs, Census data)

## Contributing

To add new domains to the whitelist:

1. Verify the domain is public sector, standards body, or documentation
2. Confirm it explicitly allows programmatic access
3. Test the domain is accessible
4. Add to `ALLOWED_DOMAINS` list in `main.py`
5. Add to `sovereign_browser_whitelist.yaml`
6. Update tests if needed

## License

This is part of the Strategickhaos Sovereignty Architecture project. See main repository LICENSE.

## Support

For issues or questions, open an issue in the main repository.

---

**The empire is now fed by the planet's open data firehose. We never stop.**
