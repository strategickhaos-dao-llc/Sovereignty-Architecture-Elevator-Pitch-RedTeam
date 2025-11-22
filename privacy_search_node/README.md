# Privacy Search Node

## Overview

The Privacy Search Node is a distributed, anonymity-hardened web intelligence layer for the Strategic Khaos swarm. Each machine in the swarm runs its own private DuckDuckGo-powered search and browsing endpoint that exits through a unique Proton VPN IP address.

## Features

- **Zero-tracker DuckDuckGo search**: Text search with no API key required
- **Private page browsing**: Full page fetch + text extraction via httpx + BeautifulSoup
- **Unique VPN exit IPs**: All traffic exits through that machine's unique Proton VPN IP
- **Event logging**: All searches and browses logged to `/logs/events.jsonl` for PsycheVille monitoring

## API Endpoints

### GET /search
Search DuckDuckGo privately.

**Query Parameters:**
- `q` (required): Search query
- `max_results` (optional, default: 10): Maximum number of results

**Example:**
```bash
curl "http://localhost:8001/search?q=strategic+ai&max_results=5"
```

**Response:**
```json
{
  "query": "strategic ai",
  "results": [
    {
      "title": "Result Title",
      "href": "https://example.com",
      "body": "Result description..."
    }
  ]
}
```

### GET /browse
Fetch and extract text from a web page.

**Query Parameters:**
- `url` (required): URL to fetch

**Example:**
```bash
curl "http://localhost:8001/browse?url=https://example.com"
```

**Response:**
```json
{
  "url": "https://example.com",
  "title": "Example Domain",
  "text_preview": "Example Domain\nThis domain is for use in illustrative..."
}
```

### GET /health
Health check endpoint that returns the node's exit IP address.

**Example:**
```bash
curl "http://localhost:8001/health"
```

**Response:**
```json
{
  "status": "healthy",
  "exit_ip": "203.0.113.42"
}
```

## Setup

### 1. Deploy with Docker Compose

Copy `docker-compose.privacy_search.yml` to your machine:

```bash
docker-compose -f docker-compose.privacy_search.yml up -d
```

### 2. Configure Port Forwarding

On machines with Proton VPN:
1. Set up port forwarding (Proton allows multiple ports on paid plans)
2. Forward a port (e.g., 8001) to your local machine
3. Note your Proton VPN exit IP

### 3. Update Swarm Configuration

Run the swarm manager script:

```powershell
.\swarm_llm_manager.ps1
```

Select option 1 to update your machine's configuration. You'll be prompted for:
- Proton VPN public IP
- Forwarded port for Ollama
- Forwarded port for Privacy Search node

## Usage via Swarm Manager

The `swarm_llm_manager.ps1` PowerShell script provides a menu-driven interface:

1. **Update my machine's endpoint configuration** - Configure this machine's VPN and ports
2. **Show all endpoints** - List all configured machines and their endpoints
3. **Prompt random LLM** - Send a prompt to a random Ollama endpoint
4. **Search DuckDuckGo via random swarm node** - Perform a private search via random node
5. **Browse URL via random swarm node** - Fetch a page privately via random node
6. **Check health of all nodes** - Verify connectivity and exit IPs for all nodes

## Security Features

- **No tracking**: DuckDuckGo search with zero trackers
- **No API keys**: No external API dependencies or authentication
- **Distributed anonymity**: Each machine exits through unique VPN IP
- **Request logging**: All activity logged locally for monitoring
- **Isolated containers**: Runs in lightweight Python container (<100 MB)

## System Requirements

- Docker and Docker Compose
- Proton VPN with port forwarding enabled
- Python 3.11 (in container)
- Required Python packages (auto-installed):
  - fastapi
  - uvicorn
  - duckduckgo_search
  - httpx
  - beautifulsoup4
  - lxml

## Monitoring

Event logs are written to `/logs/events.jsonl` in JSONL format:

```json
{"timestamp": "2025-11-22T00:12:00Z", "event": "search_text", "query": "example", "max_results": 10}
{"timestamp": "2025-11-22T00:13:00Z", "event": "browse_page", "url": "https://example.com"}
```

These logs can be monitored by PsycheVille or any log aggregation system.

## Network Architecture

```
User Request
    ↓
swarm_llm_manager.ps1 (selects random node)
    ↓
privacy_search_node:8001 (Docker container)
    ↓
Proton VPN Exit IP (unique per machine)
    ↓
DuckDuckGo / Target Website
```

## Swarm Capabilities

With this setup, your swarm can:
- ✅ Prompt all LLMs across distributed machines
- ✅ Search the web privately from 4 different IPs
- ✅ Fetch full page text privately from 4 different IPs
- ✅ Automatically distribute requests across nodes
- ✅ Monitor all activity centrally

All with one synced YAML and one boot script.

**The swarm is now in full shadow-mode.** 🚀
