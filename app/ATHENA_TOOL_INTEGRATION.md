# Athena Tool Integration - Sovereign Research Browser

## Overview

The Sovereign Research Browser is a polite, robots.txt-respecting research browser that provides access to 100+ whitelisted domains for research purposes only.

## Tool Endpoint

**Base URL:** `http://sovereign-browser:8000/browse`

**Method:** `GET`

**Query Parameters:**
- `url` (required): HTTPS URL on an allowed domain for research-only retrieval

## Tool Schema (OpenAI-style JSON)

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

## Response Format

```json
{
  "url": "https://example.com/page",
  "title": "Page Title",
  "text_preview": "First ~10k characters of page content...",
  "research_allowed": true,
  "rate_limited": false,
  "robots_compliant": true,
  "status_code": 200,
  "content_type": "text/html; charset=utf-8"
}
```

## Error Semantics

- **403 Forbidden**: Domain or path not allowed (whitelist / robots.txt)
- **429 Too Many Requests**: Rate limited (back off on that domain)
- **500 Internal Server Error**: Server error

## Internal Calling Contract

### Intent
Only for reading public pages on whitelisted domains for research, not automation or scraping.

### Error Handling

- **403** → Domain or path not allowed (whitelist / robots.txt)
- **429** → Back off on that domain (respect rate_limit_seconds)

### Response Usage

- Treat `text_preview` as a summary input to LLM
- If an agent needs more than ~10k chars, it should plan multiple calls or a follow-up tool

## Agent Prompt Template

Add this to Athena's planner prompt:

```
When you need to read a public webpage on a research domain (docs, standards, academic pages), 
call sovereign_research_browse. Do not use it for login pages, forms, or anything that looks 
non-public. Respect 403/429 as hard boundaries.
```

## Features

1. **Domain Whitelist Enforcement**: Only 100+ approved research domains are accessible
2. **robots.txt Compliance**: Automatically checks and respects robots.txt rules
3. **Rate Limiting**: 12 requests per minute per domain (configurable)
4. **Structured Psyche Logging**: All requests are logged with structured data
5. **Polite User Agent**: Identifies itself properly and provides contact information

## Whitelisted Domain Categories

- Core reference & documentation (MDN, Python docs, GitHub, etc.)
- Open standards / RFCs (IETF, W3C, ECMA, etc.)
- Open data & government (NASA, Census, NOAA, etc.)
- International organizations (WHO, UN, World Bank, etc.)
- Academic search & preprints (arXiv, PubMed, Semantic Scholar, etc.)
- Major scientific publishers (Nature, Science, IEEE, ACM, etc.)
- Math / CS learning (Khan Academy, MIT OCW, Coursera, etc.)
- Security / CVE / standards (NIST, CVE MITRE, OWASP, etc.)
- Open knowledge & encyclopedias (Wikipedia, Wikidata, etc.)
- ML & AI docs (PyTorch, TensorFlow, Hugging Face, etc.)
- Cloud provider documentation (AWS, GCP, Azure, etc.)
- Tech docs / tooling (Linux, Debian, Ubuntu, Prometheus, etc.)
- Economics / statistics / markets (BLS, Federal Reserve, etc.)
- Misc reference & safe utilities (Stack Overflow, Archive.org, etc.)

## Example Usage

### Python (httpx)

```python
import httpx

async with httpx.AsyncClient() as client:
    response = await client.get(
        "http://sovereign-browser:8000/browse",
        params={"url": "https://arxiv.org/abs/2103.00020"}
    )
    data = response.json()
    print(f"Title: {data['title']}")
    print(f"Preview: {data['text_preview'][:200]}")
```

### cURL

```bash
curl "http://sovereign-browser:8000/browse?url=https%3A%2F%2Farxiv.org%2Fabs%2F2103.00020"
```

## Rate Limiting

Each domain has a rate limit of 12 requests per minute by default. When rate limited, the response will include:

```json
{
  "url": "...",
  "research_allowed": true,
  "rate_limited": true,
  "robots_compliant": true,
  "error": "Rate limited. Retry after 30.5 seconds"
}
```

## Extending the Whitelist

To add or modify allowed domains, edit `/app/allowed_domains.yaml`:

```yaml
allowed_domains:
  - "newdomain.com"
  - "research.example.org"
  # ... more domains
```

For per-domain configuration (rate limits, priorities), the YAML can be extended:

```yaml
allowed_domains:
  - domain: "arxiv.org"
    intent: "primary_research"
    max_requests_per_minute: 12
  - domain: "bloomberg.com"
    intent: "news_meta_only"
    max_requests_per_minute: 2
```

## Security Considerations

1. **Whitelist Only**: The browser will ONLY access domains in the whitelist
2. **robots.txt Compliance**: Respects website operator preferences
3. **Rate Limiting**: Prevents abuse and excessive load
4. **Audit Trail**: All requests are logged for transparency
5. **No Authentication**: Does not handle login pages or authenticated content
6. **Research Only**: Intended for reading public research content, not automation

## Future Enhancements

Potential future features:

1. `/screenshot` endpoint for visual diffing
2. `user_agent` and `purpose` fields in psyche_log
3. Per-domain priority and rate limit customization
4. Content caching for frequently accessed pages
5. PDF and document parsing
6. Link extraction and crawling capabilities (with strict whitelist enforcement)
