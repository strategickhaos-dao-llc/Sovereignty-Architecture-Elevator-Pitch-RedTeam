# Sovereign Research Browser Node

**A legally compliant research browser for public documentation sites**

## Overview

The Sovereign Research Browser Node is a FastAPI-based web automation service that provides safe, legally compliant access to public documentation and research resources. Built on Playwright, it's designed for the Strategickhaos ecosystem with strict domain whitelisting and comprehensive audit logging.

## Legal Compliance

This implementation is designed to be 100% compliant with US computer fraud and abuse laws based on 30+ key court cases up to November 2025:

### Key Legal Principles

1. **Van Buren v. United States (2021)** - Supreme Court ruling that narrowed CFAA: violating Terms of Service alone does NOT constitute "exceeding authorized access"
2. **hiQ Labs v. LinkedIn (2019 & 2022)** - 9th Circuit ruled that scraping public profiles is legal; CFAA doesn't apply to public data
3. **X Corp v. Bright Data (2024)** - Copyright preemption; selling scraped public data is legal
4. **Meta v. Bright Data (2024)** - No CFAA violation for scraping public data

### What Makes This Legal

✅ **Only accesses truly public pages** (no login required)  
✅ **Respects domain whitelist** (explicit opt-in for research domains)  
✅ **No stealth tactics** (clean Playwright usage, no evasion libraries)  
✅ **Comprehensive logging** (PsycheVille event logs for accountability)  
✅ **Rate limiting friendly** (reasonable timeouts and delays)  
✅ **Research-focused** (explicitly for documentation and open-source resources)

### What Would Be Illegal

❌ Accessing pages behind login/authentication  
❌ Ignoring robots.txt + cease-and-desist letters  
❌ Copying copyrighted content for commercial use  
❌ Overloading servers (trespass to chattels)  
❌ Using stealth to evade detection systems

## Features

- **Domain Whitelist**: Only pre-approved research domains allowed
- **FastAPI REST API**: Clean, documented endpoints
- **Playwright Browser**: Headless Chromium automation
- **PsycheVille Logging**: All requests logged to `/logs/events.jsonl`
- **Health Checks**: Kubernetes-ready health and readiness endpoints
- **Docker Ready**: Full containerization support

## Allowed Research Domains

By default, the browser allows access to:

- `docs.python.org` - Python documentation
- `developer.mozilla.org` - MDN Web Docs
- `pypi.org` - Python Package Index
- `github.com` - Open source code
- `wikipedia.org` - Public encyclopedia
- `arxiv.org` - Academic papers
- `rfc-editor.org` - Internet standards
- `ietf.org` - Internet Engineering Task Force
- `nginx.com` - Nginx documentation
- `cloudflare.com` - Cloudflare documentation
- `proton.me` - Proton documentation
- `tailscale.com` - Tailscale documentation

You can expand this list by editing the `ALLOWED_DOMAINS` list in `main.py`.

## API Endpoints

### `GET /browse`

Browse a URL and extract content.

**Parameters:**
- `url` (query, required): URL to browse (must be in allowed domains)

**Response:**
```json
{
  "url": "https://docs.python.org/3/library/asyncio.html",
  "title": "asyncio — Asynchronous I/O — Python 3.x documentation",
  "text_preview": "asyncio is a library to write concurrent code...",
  "allowed": true
}
```

**Errors:**
- `403 Forbidden`: Domain not in allowed list
- `500 Internal Server Error`: Browser error or timeout

### `GET /health`

Health check endpoint for monitoring.

**Response:**
```json
{
  "status": "sovereign_research_node",
  "node": "hostname",
  "allowed_domains_count": 12
}
```

### `GET /domains`

List all allowed research domains.

**Response:**
```json
{
  "allowed_domains": ["arxiv.org", "cloudflare.com", ...],
  "count": 12
}
```

## Running Locally

### Prerequisites

- Python 3.11+
- pip

### Installation

```bash
# Navigate to sovereign_browser directory
cd sovereign_browser

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Create logs directory
mkdir -p /logs  # or set LOGS_DIR=/tmp/logs

# Run the server
python main.py
```

The server will start on `http://localhost:8086`.

### Testing

```bash
# Test health endpoint
curl http://localhost:8086/health

# Test allowed domains list
curl http://localhost:8086/domains

# Test browsing (should succeed)
curl "http://localhost:8086/browse?url=https://docs.python.org/3/"

# Test blocked domain (should fail with 403)
curl "http://localhost:8086/browse?url=https://example.com/"
```

## Running with Docker

### Build the image

```bash
docker build -f Dockerfile.sovereign_browser -t sovereign-browser:latest .
```

### Run the container

```bash
docker run -d \
  --name sovereign-browser \
  -p 8086:8086 \
  -v /var/sovereign_browser/logs:/logs \
  -e SOVEREIGN_BROWSER_PORT=8086 \
  sovereign-browser:latest
```

### Using Docker Compose

The service is already integrated into the main `docker-compose.yml`:

```bash
# Start all services including sovereign browser
docker-compose up -d

# Start only the browser service
docker-compose up -d sovereign-browser

# View logs
docker-compose logs -f sovereign-browser

# Stop the service
docker-compose down
```

## Configuration

### Environment Variables

- `SOVEREIGN_BROWSER_PORT`: Port to listen on (default: 8086)
- `LOGS_DIR`: Directory for event logs (default: /logs)

### Adding New Domains

To add new research domains to the whitelist, edit `main.py`:

```python
ALLOWED_DOMAINS = [
    "docs.python.org",
    "developer.mozilla.org",
    # ... existing domains ...
    "your-research-domain.com",  # Add your domain here
]
```

**Important**: Only add domains that:
1. Provide public, freely accessible documentation
2. Don't require authentication
3. Allow automated access (check their robots.txt and ToS)
4. Are used for legitimate research purposes

## PsycheVille Event Logging

All browser requests are logged to `/logs/events.jsonl` in JSONL (JSON Lines) format:

```json
{"timestamp": "2025-11-22T00:18:21.810Z", "event": "research_browse_success", "url": "https://docs.python.org/3/", "title": "Python Documentation"}
{"timestamp": "2025-11-22T00:18:22.123Z", "event": "research_browse_blocked", "url": "https://blocked-site.com/", "domain": "blocked-site.com", "reason": "not_in_allowlist"}
```

Event types:
- `research_browse_success`: Successful page load
- `research_browse_blocked`: Domain not in allowlist
- `research_browse_error`: Browser error or timeout

## Architecture Integration

The Sovereign Browser integrates with the Strategickhaos ecosystem:

```
┌─────────────────────────────────────────────────────────┐
│                 Strategickhaos Stack                    │
├─────────────────────────────────────────────────────────┤
│  Discord Bot  │  Event Gateway  │  Refinory AI          │
├─────────────────────────────────────────────────────────┤
│             Sovereign Research Browser                  │
│         (Port 8086, /browse, /health, /domains)        │
├─────────────────────────────────────────────────────────┤
│    Prometheus    │     Grafana     │    PostgreSQL      │
└─────────────────────────────────────────────────────────┘
```

## Monitoring

The service exposes metrics compatible with the existing Prometheus/Grafana stack:

- HTTP request counts
- Response times
- Success/failure rates
- Domain blocking events

Health check available at `/health` for Kubernetes liveness/readiness probes.

## Security Best Practices

1. **Always run with domain whitelist** - Never disable the allowed domains check
2. **Keep Playwright updated** - Security patches for browser automation
3. **Monitor logs** - Watch for suspicious patterns or abuse attempts
4. **Rate limiting** - Consider adding rate limits for production use
5. **Network isolation** - Run in isolated network namespace if possible

## Troubleshooting

### Browser not starting

```bash
# Reinstall Playwright browsers
playwright install --with-deps chromium
```

### Permission errors on /logs

```bash
# Ensure logs directory is writable
mkdir -p /var/sovereign_browser/logs
chmod 777 /var/sovereign_browser/logs
```

### Domain blocking issues

Check that the domain is in the `ALLOWED_DOMAINS` list and matches exactly (case-insensitive).

## License

MIT License - see root LICENSE file

## Contributing

When adding features:
1. Maintain legal compliance (no stealth, no login bypass)
2. Keep domain whitelist explicit
3. Add appropriate logging for audit trails
4. Update tests and documentation

---

**Built with 🔥 by the Strategickhaos Swarm Intelligence collective**

*"Sovereign, legal, and transparent research browsing for the distributed web"*
