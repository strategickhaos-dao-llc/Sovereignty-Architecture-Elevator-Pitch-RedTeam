# Sovereign Browser Service

## Overview

The Sovereign Browser Department provides fully self-hosted, stealth, distributed browsing behind unique VPN exit nodes. This service eliminates dependencies on external browser APIs, Selenium grids, and prevents Cloudflare leaks.

## Features

- **Undetectable Browsing**: Uses Playwright-stealth for anti-detection
- **VPN Integration**: Routes through per-node VPN exits (e.g., Proton VPN)
- **Full Screenshots**: Captures complete page screenshots
- **Text Extraction**: Extracts page content with optional custom instructions
- **Health Monitoring**: Reports current exit IP for verification
- **Event Logging**: JSONL format event logs for audit trail

## Architecture

### Quadrilateral Collapse

| Quadrant    | Representation                                                                                                   |
|-------------|------------------------------------------------------------------------------------------------------------------|
| Symbolic    | YAML schema + OpenAPI spec at /docs — every call is a pure function with deterministic inputs/outputs           |
| Spatial     | One browser instance per physical machine → geographic distribution of exit nodes → 4D IP space coverage        |
| Narrative   | "We are no longer asking the internet for truth — we are raiding it with ghost browsers from four different countries at once." |
| Kinesthetic | Feels like flipping a knife while solving a Rubik's cube: the swarm moves in perfect silence, invisible, lethal |

## Quick Start

### Using Docker Compose

```bash
# Start the sovereign browser service
docker compose -f docker-compose.sovereign_browser.yml up -d

# Check service health
curl http://localhost:8002/health

# Browse a URL
curl "http://localhost:8002/browse?url=https://example.com"
```

### Configuration

The service is configured via environment variables:

- `PORT`: API port (default: 8002)
- `LOG_PATH`: Path to event log file (default: /logs/events.jsonl)

### Volumes

- `./sovereign_browser`: Application code directory
- `./logs/sovereign_browser`: Event logs directory
- `browser_cache`: Persistent Playwright browser cache

## API Endpoints

### GET /browse

Browse a URL with stealth mode and return metadata.

**Query Parameters:**
- `url` (required): Target URL to browse
- `instructions` (optional): Custom extraction instructions

**Response:**
```json
{
  "url": "https://example.com",
  "final_url": "https://example.com/",
  "title": "Example Domain",
  "text_length": 1234,
  "screenshot_bytes": 45678,
  "extracted": "..."
}
```

### GET /health

Check service health and report exit IP.

**Response:**
```json
{
  "status": "sovereign",
  "exit_ip": "1.2.3.4"
}
```

### GET /docs

Interactive API documentation (Swagger UI).

## Swarm Configuration

Update `swarm_llm_endpoints.yaml` to register this node:

```yaml
browser_port: 8002
browser_endpoint: "http://192.168.1.100:8002/browse"
```

## VPN Integration

This service works best when the host machine is connected to a VPN:

1. Connect host to Proton VPN (or your preferred VPN)
2. Verify exit IP: `curl https://api.ipify.org`
3. Start sovereign browser service
4. Verify browser exit IP: `curl http://localhost:8002/health`

Each machine in your swarm can use a different VPN exit location for geographic distribution.

## Security Notes

- Run behind a firewall for production deployments
- Use authentication/authorization for remote access
- Rotate VPN exit nodes regularly
- Monitor event logs for suspicious activity
- Keep Playwright and dependencies updated

## Dependencies

- Python 3.11+
- FastAPI
- Uvicorn
- Playwright 1.47.0
- playwright-stealth

All dependencies are automatically installed via Docker Compose.

## Development

### Local Testing

```bash
# Install dependencies
pip install fastapi uvicorn playwright==1.47.0 playwright-stealth
playwright install chromium --with-deps

# Run locally
cd sovereign_browser
uvicorn main:app --reload --port 8002
```

### Logs

Event logs are written in JSONL format to `/logs/events.jsonl`:

```json
{"timestamp": "2025-11-21T12:34:56Z", "event": "sovereign_browse", "url": "https://example.com", "instructions": ""}
```

## License

Part of the Sovereignty Architecture project.
