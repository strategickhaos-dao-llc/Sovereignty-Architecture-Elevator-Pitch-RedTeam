# Sovereign Research Browser

A polite, robots.txt-respecting research browser for whitelisted domains only.

## Overview

The Sovereign Research Browser provides secure, rate-limited access to 160+ whitelisted research and documentation domains. It's designed for AI agents and research tools that need to fetch public content responsibly.

## Features

- **Domain Whitelist**: Only approved research domains are accessible
- **robots.txt Compliance**: Automatically respects website crawling preferences
- **Rate Limiting**: 12 requests per minute per domain (configurable)
- **Structured Logging**: All requests logged with psyche_log entries
- **Text Extraction**: Returns clean text preview (max 10k characters)
- **Polite User Agent**: Proper identification and contact information

## Quick Start

### Using the /browse Endpoint

The browser is integrated into the Refinory FastAPI service at the `/browse` endpoint:

```bash
# Example: Browse Python documentation
curl "http://localhost:8000/browse?url=https://docs.python.org/3/"

# Example: Browse arXiv paper
curl "http://localhost:8000/browse?url=https://arxiv.org/abs/2103.00020"
```

### Response Format

```json
{
  "url": "https://docs.python.org/3/",
  "title": "3.12.7 Documentation",
  "text_preview": "Welcome to Python.org...",
  "research_allowed": true,
  "rate_limited": false,
  "robots_compliant": true,
  "status_code": 200,
  "content_type": "text/html; charset=utf-8"
}
```

### Error Responses

**403 Forbidden** - Domain not whitelisted or disallowed by robots.txt:
```json
{
  "detail": "Domain not in whitelist"
}
```

**429 Too Many Requests** - Rate limit exceeded:
```json
{
  "detail": "Rate limited. Retry after 30.5 seconds"
}
```

## Whitelisted Domains

The browser has access to 160+ domains across these categories:

### Core Reference & Documentation (35+)
- Python, GitHub, GitLab, MDN, npm, PyPI
- Kubernetes, Docker, PostgreSQL, Redis
- React, Vue, Angular, Svelte, Tailwind
- Rust, Go, Dart, Flutter, Kotlin

### Standards & RFCs (5+)
- IETF, W3C, ECMA, Unicode

### Government & Open Data (16+)
- NASA, Census, NOAA, EPA, NIH, NSF
- Federal Register, Congress.gov

### International Organizations (11+)
- WHO, UN, World Bank, IMF, OECD, ESA

### Academic & Research (8+)
- arXiv, PubMed, Semantic Scholar, OpenReview
- HAL Science, DOI, CrossRef

### Scientific Publishers (12+)
- Nature, Science, Cell, Springer, IEEE, ACM
- APS Journals

### Learning Platforms (11+)
- Khan Academy, Coursera, edX, MIT OCW
- Brilliant, Stanford, Harvard, Berkeley

### Security & Standards (7+)
- NIST, CVE MITRE, OWASP, FIRST

### Knowledge Bases (5+)
- Wikipedia, Wikidata, Wiktionary, Wikibooks

### ML & AI Documentation (9+)
- PyTorch, TensorFlow, Hugging Face
- scikit-learn, pandas, NumPy

### Cloud Providers (8+)
- AWS, Google Cloud, Azure, DigitalOcean

### Developer Tools & Linux (15+)
- Linux kernel, Debian, Ubuntu, Arch
- Prometheus, Grafana, Elastic

### Utilities & Reference (9+)
- Stack Overflow, Archive.org, regex101
- explainshell, crontab.guru

### Economics & Markets (7+)
- BLS, Federal Reserve, Bloomberg, Reuters

See `allowed_domains.yaml` for the complete list.

## Configuration

### Rate Limiting

Default: 12 requests per minute per domain

To modify, edit the browser initialization in `refinory/refinory/main.py`:

```python
research_browser = ResearchBrowser(
    allowed_domains_path=str(browser_domains_path),
    rate_limit_requests_per_minute=20  # Increase limit
)
```

### Adding Domains

Edit `allowed_domains.yaml`:

```yaml
allowed_domains:
  - "newdomain.com"
  - "research.example.org"
```

For advanced configuration with per-domain settings:

```yaml
allowed_domains:
  - domain: "arxiv.org"
    intent: "primary_research"
    max_requests_per_minute: 12
  - domain: "bloomberg.com"
    intent: "news_meta_only"
    max_requests_per_minute: 2
```

### User Agent

Default: `SovereignResearchBrowser/1.0 (Polite; +https://github.com/Strategickhaos)`

To customize, modify the `user_agent` parameter in `browser.py`.

## Python API

You can also use the browser directly in Python:

```python
from app.browser import ResearchBrowser

async def main():
    browser = ResearchBrowser()
    
    # Browse a URL
    response = await browser.browse("https://arxiv.org/abs/2103.00020")
    
    if response.research_allowed and not response.error:
        print(f"Title: {response.title}")
        print(f"Preview: {response.text_preview[:200]}")
    else:
        print(f"Error: {response.error}")
    
    await browser.close()

# Run with asyncio
import asyncio
asyncio.run(main())
```

## Athena Tool Integration

See [ATHENA_TOOL_INTEGRATION.md](./ATHENA_TOOL_INTEGRATION.md) for detailed documentation on integrating this browser as a tool for Athena AI agents.

### Tool Schema (OpenAI Format)

```json
{
  "type": "function",
  "function": {
    "name": "sovereign_research_browse",
    "description": "Polite, robots.txt-respecting research browser for whitelisted domains only.",
    "parameters": {
      "type": "object",
      "properties": {
        "url": {
          "type": "string",
          "description": "HTTPS URL on an allowed domain for research-only retrieval."
        }
      },
      "required": ["url"]
    }
  }
}
```

### Agent Prompt

```
When you need to read a public webpage on a research domain (docs, standards, 
academic pages), call sovereign_research_browse. Do not use it for login pages, 
forms, or anything that looks non-public. Respect 403/429 as hard boundaries.
```

## Testing

Run the basic test suite:

```bash
cd app
python test_browser.py
```

Expected output:
```
Testing allowed domains loading...
✓ Passed

Testing domain whitelist checking...
✓ Passed

Testing rate limiting...
✓ Passed

Testing browse with disallowed domain...
✓ Passed

All tests passed!
```

## Logging

All requests are logged with structured data (psyche_log):

```json
{
  "timestamp": "2025-11-22T00:39:25.123456",
  "url": "https://docs.python.org/3/",
  "domain": "docs.python.org",
  "path": "/3/",
  "allowed": true,
  "robots_compliant": true,
  "rate_limited": false,
  "status_code": 200,
  "response_time_ms": 245.67
}
```

## Security Considerations

1. **Whitelist Only**: Only approved domains are accessible
2. **No Authentication**: Does not handle login or authenticated content
3. **Research Only**: For reading public research content, not automation
4. **Rate Limited**: Prevents abuse and excessive server load
5. **Audit Trail**: All requests logged for transparency
6. **robots.txt Compliance**: Respects website operator preferences

## Architecture

```
┌─────────────────────────────────────────┐
│  Athena AI Agent / Client               │
└──────────────┬──────────────────────────┘
               │
               │ GET /browse?url=...
               ▼
┌─────────────────────────────────────────┐
│  Refinory FastAPI Server                │
│  └─ /browse endpoint                    │
└──────────────┬──────────────────────────┘
               │
               │ ResearchBrowser.browse()
               ▼
┌─────────────────────────────────────────┐
│  Sovereign Research Browser             │
│  ├─ Domain Whitelist Check              │
│  ├─ robots.txt Check                    │
│  ├─ Rate Limit Check                    │
│  └─ HTTP Fetch + Text Extraction        │
└──────────────┬──────────────────────────┘
               │
               │ HTTPS Request
               ▼
┌─────────────────────────────────────────┐
│  Whitelisted Domain                     │
│  (arxiv.org, github.com, etc.)          │
└─────────────────────────────────────────┘
```

## Future Enhancements

Potential features for future development:

1. **Screenshot Endpoint** - Visual page capture for diffing
2. **PDF Parsing** - Extract text from PDF documents
3. **Link Extraction** - Follow links within whitelisted domains
4. **Content Caching** - Cache frequently accessed pages
5. **Custom Purpose Tags** - Track why each request was made
6. **Per-Domain Priorities** - Different rate limits per domain type
7. **Semantic HTML Parsing** - Better structure extraction
8. **Multi-page Fetching** - Batch requests for related pages

## Contributing

To add new domains or features:

1. Edit `allowed_domains.yaml` for domain whitelist
2. Modify `browser.py` for functionality changes
3. Update tests in `test_browser.py`
4. Document changes in this README

## License

Part of the Strategickhaos Sovereignty Architecture project.
