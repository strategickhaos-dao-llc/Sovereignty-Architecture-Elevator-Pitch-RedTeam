# Privacy Search Node - Quick Start Guide

## Overview

The Privacy Search Node enables your Strategic Khaos swarm to perform anonymous web searches and browsing through multiple unique Proton VPN exit IPs. Each machine in your swarm becomes a distributed, anonymity-hardened web intelligence node.

## What's New

🎯 **Distributed Anonymous Search**: Search DuckDuckGo through 4 different VPN exit IPs
🌐 **Private Web Browsing**: Fetch and extract text from any public website
🔒 **Zero Trackers**: No API keys, no logging services, no tracking
🛡️ **SSRF Protected**: Multi-layered security prevents access to internal networks
📊 **Event Logging**: All activity logged for monitoring (PsycheVille compatible)

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    swarm_llm_manager.ps1                      │
│              (Central Management Interface)                   │
└────────────────────────┬─────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
┌───────▼────────┐ ┌────▼────────┐ ┌────▼────────┐
│ sony_asteroth  │ │    nova     │ │   athena    │ ...
│ VPN IP: X.X.X.1│ │ VPN: X.X.X.2│ │ VPN: X.X.X.3│
├────────────────┤ ├─────────────┤ ├─────────────┤
│ Ollama:11434   │ │ Ollama:11434│ │ Ollama:11434│
│ Search:8001    │ │ Search:8001 │ │ Search:8001 │
└────────────────┘ └─────────────┘ └─────────────┘
         │                │                │
         └────────────────┴────────────────┘
                          │
                    ┌─────▼──────┐
                    │  Internet  │
                    │ (via VPN)  │
                    └────────────┘
```

## Quick Setup (Per Machine)

### 1. Deploy Privacy Search Service

```bash
# Copy files to machine
# - docker-compose.privacy_search.yml
# - privacy_search_node/ directory

# Create required directories
mkdir -p logs/privacy_search

# Start the service
docker-compose -f docker-compose.privacy_search.yml up -d

# Verify it's running
curl http://localhost:8001/health
```

### 2. Configure Proton VPN Port Forwarding

On each machine with Proton VPN:
1. Enable port forwarding in Proton VPN (paid plans support multiple ports)
2. Note your forwarded ports:
   - Port for Ollama (e.g., 11434 or custom)
   - Port for Privacy Search (e.g., 8001)
3. Note your Proton VPN exit IP address

### 3. Update Swarm Configuration

Run the management script:

```powershell
.\swarm_llm_manager.ps1
```

Select option **1** to update your machine's configuration:
```
Enter current Proton VPN public IP: 203.0.113.42
Enter forwarded port for Ollama: 11434
Enter forwarded port for Privacy Search node: 8001
```

The script will update `swarm_llm_endpoints.yaml` automatically.

### 4. Repeat for All Machines

Repeat steps 1-3 for each machine in your swarm:
- sony_asteroth
- nova_asus_tuf_a15
- athena_ipower
- nitro_v15

## Using the Swarm

### Interactive Menu

Launch the management script:

```powershell
.\swarm_llm_manager.ps1
```

**Menu Options:**

1. **Update my machine's endpoint configuration**
   - Configure this machine's VPN IP and ports
   - Automatically updates central YAML

2. **Show all endpoints**
   - View all configured machines
   - See VPN IPs, ports, and endpoint URLs

3. **Prompt random LLM**
   - Send a prompt to a random Ollama instance
   - Distributed AI processing

4. **Search DuckDuckGo via random swarm node**
   - Private web search through random VPN exit
   - Zero tracking, no API keys

5. **Browse URL via random swarm node**
   - Fetch and extract text from any public URL
   - Different IP for each request

6. **Check health of all nodes**
   - Verify connectivity to all services
   - See exit IPs for each node

### Example: Anonymous Search

```powershell
.\swarm_llm_manager.ps1
# Select option 4
# Enter query: "strategic AI architecture"
```

Output shows:
- Which swarm node was selected (random)
- The exit IP used
- Search results from DuckDuckGo

### Example: Private Web Browsing

```powershell
.\swarm_llm_manager.ps1
# Select option 5
# Enter URL: https://example.com
```

Output shows:
- Which swarm node was selected
- Page title and text preview
- All traffic routed through that node's VPN

### Direct API Usage

You can also use the API directly:

```bash
# Search
curl "http://203.0.113.42:8001/search?q=test&max_results=5"

# Browse
curl "http://203.0.113.42:8001/browse?url=https://example.com"

# Health
curl "http://203.0.113.42:8001/health"

# API Documentation
# Open http://203.0.113.42:8001/docs in browser
```

## Configuration Files

### swarm_llm_endpoints.yaml

Central configuration tracking all machines:

```yaml
swarm:
  proton_vpn_port_forward_range: "40000-50000"
  ollama_default_port: 11434
  search_default_port: 8001

machines:
  sony_asteroth:
    hostname: "sony-asteroth"
    local_ip: "192.168.1.50"
    proton_vpn_ip: "203.0.113.42"
    ollama_port: 11434
    search_port: 8001
    ollama_endpoint: "http://203.0.113.42:11434"
    search_endpoint: "http://203.0.113.42:8001"
```

### Environment Variables

Configure via environment variables:

```bash
# Custom log file location
export LOG_FILE=/custom/path/events.jsonl

# Custom port
export PORT=8002
```

## Security

✅ **SSRF Protection**: Blocks access to private networks, localhost, etc.
✅ **No Credentials**: Zero API keys or authentication required
✅ **Distributed IPs**: Each request can use a different VPN exit
✅ **Request Logging**: All activity logged for audit/monitoring

See `privacy_search_node/SECURITY.md` for detailed security documentation.

## Monitoring

Event logs are written in JSONL format:

```bash
tail -f logs/privacy_search/events.jsonl
```

Example log entries:
```json
{"timestamp": "2025-11-22T00:12:00Z", "event": "search_text", "query": "test", "max_results": 10}
{"timestamp": "2025-11-22T00:13:00Z", "event": "browse_page", "url": "https://example.com"}
```

## Troubleshooting

### Service won't start

```bash
# Check logs
docker logs privacy_search_node

# Verify dependencies
docker exec privacy_search_node pip list
```

### Can't connect to endpoint

```bash
# Check if service is running
docker ps | grep privacy_search_node

# Test locally first
curl http://localhost:8001/health

# Check VPN port forwarding
# Verify ports are forwarded in Proton VPN settings
```

### YAML configuration issues

```bash
# Validate YAML syntax
python3 -c "import yaml; yaml.safe_load(open('swarm_llm_endpoints.yaml'))"

# Reset configuration
# Edit swarm_llm_endpoints.yaml manually to fix any issues
```

## Performance

- **Container size**: <100 MB
- **Memory usage**: ~50-100 MB per container
- **Response time**: 1-5 seconds (depends on network)
- **Concurrent requests**: Limited by httpx client (default: 10 connections)

## Next Steps

Want to enhance your swarm further?

- **Image search**: Add DuckDuckGo image search endpoint
- **Screenshot capture**: Integrate Playwright for full page screenshots
- **Round-robin balancing**: Auto-rotate through all VPN exits
- **Request caching**: Cache search results to reduce latency
- **HTTPS**: Deploy behind reverse proxy with SSL/TLS

## Support

For issues or questions:
1. Check logs: `docker logs privacy_search_node`
2. Review security documentation: `privacy_search_node/SECURITY.md`
3. Run tests: `cd privacy_search_node && pytest test_privacy_search.py -v`
4. Check GitHub issues for similar problems

---

**The swarm is now in full shadow-mode.** 🚀

Your distributed AI intelligence layer is ready to search and browse the web privately through multiple VPN exit points, with zero tracking and complete anonymity.
