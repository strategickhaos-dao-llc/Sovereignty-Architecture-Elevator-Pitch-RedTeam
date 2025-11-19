# ngrok Integration Architecture

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                          GitHub / Discord                            │
│                                                                       │
│  ┌──────────────┐              ┌──────────────┐                     │
│  │   GitHub     │              │   Discord    │                     │
│  │  Webhooks    │              │    Events    │                     │
│  └──────┬───────┘              └──────┬───────┘                     │
└─────────┼──────────────────────────────┼─────────────────────────────┘
          │                              │
          │ HTTPS                        │ HTTPS
          │                              │
┌─────────▼──────────────────────────────▼─────────────────────────────┐
│                        ngrok Cloud Service                            │
│                                                                       │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │  Secure Tunnel (TLS)                                           │ │
│  │  • Public URLs: https://*.ngrok.io                             │ │
│  │  • Request/Response forwarding                                 │ │
│  │  • Traffic inspection                                          │ │
│  └────────────────────────────────────────────────────────────────┘ │
└───────────────────────────────────┬───────────────────────────────────┘
                                    │
                                    │ Encrypted Tunnel
                                    │
┌───────────────────────────────────▼───────────────────────────────────┐
│                     Your Local Machine (localhost)                    │
│                                                                       │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │                    ngrok Agent (Port 4040)                      │ │
│  │                                                                 │ │
│  │  Web UI: http://localhost:4040                                 │ │
│  │  • Request inspection                                          │ │
│  │  • Tunnel status                                               │ │
│  │  • Replay requests                                             │ │
│  └───┬────────────────┬────────────────────┬───────────────────────┘ │
│      │                │                    │                         │
│      │ :8080          │ :3000              │ :8000                   │
│      │                │                    │                         │
│  ┌───▼──────────┐  ┌──▼──────────┐  ┌─────▼────────────┐           │
│  │   Event      │  │   Discord   │  │    Refinory      │           │
│  │   Gateway    │  │     Bot     │  │    Service       │           │
│  │              │  │             │  │                  │           │
│  │  • Webhook   │  │  • Commands │  │  • AI Process    │           │
│  │    Handler   │  │  • Events   │  │  • Refinement    │           │
│  └──────────────┘  └─────────────┘  └──────────────────┘           │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

## Data Flow

### Inbound Webhook Flow

```
1. GitHub Event Occurs
   └─> GitHub sends webhook to: https://xyz.ngrok.io/webhook

2. ngrok Cloud Receives Request
   └─> Validates tunnel connection
   └─> Records request in inspection interface
   └─> Forwards to local ngrok agent

3. Local ngrok Agent Receives Request
   └─> Forwards to: http://localhost:8080/webhook
   └─> Available for inspection at: http://localhost:4040

4. Event Gateway Processes Request
   └─> Validates HMAC signature
   └─> Parses GitHub event
   └─> Sends notification to Discord
   └─> Returns response

5. Response Flows Back
   └─> localhost:8080 → ngrok agent → ngrok cloud → GitHub
```

### Development Workflow

```
┌──────────────────────────────────────────────────────────────┐
│                    Developer Workflow                         │
└──────────────────────────────────────────────────────────────┘

1. Start Local Services
   $ docker-compose up -d
   
2. Start ngrok Tunnels  
   $ ./scripts/start-ngrok.sh
   
3. Get Tunnel URL
   $ curl http://localhost:4040/api/tunnels
   
4. Configure GitHub Webhook
   → GitHub Settings → Webhooks → Add webhook
   → Payload URL: https://your-tunnel.ngrok.io/webhook
   
5. Test with Real Event
   → Create PR or push commit
   
6. Inspect in ngrok UI
   → Open http://localhost:4040
   → View request/response
   → Replay for testing
   
7. Make Code Changes
   → Edit source files
   → Restart service
   
8. Test Again
   → Replay request in ngrok UI
   → No need to trigger real event!
```

## Security Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Security Layers                           │
└─────────────────────────────────────────────────────────────┘

1. Transport Security (TLS)
   ┌─────────────────────────────────────────┐
   │  • End-to-end TLS encryption            │
   │  • Certificate validation               │
   │  • ngrok-managed certificates           │
   └─────────────────────────────────────────┘

2. Tunnel Security
   ┌─────────────────────────────────────────┐
   │  • Authtoken authentication             │
   │  • Encrypted tunnel connection          │
   │  • No inbound firewall rules needed     │
   └─────────────────────────────────────────┘

3. Application Security
   ┌─────────────────────────────────────────┐
   │  • HMAC signature verification          │
   │  • Request validation                   │
   │  • Content filtering                    │
   └─────────────────────────────────────────┘

4. Access Control (Paid Features)
   ┌─────────────────────────────────────────┐
   │  • IP whitelisting                      │
   │  • Basic authentication                 │
   │  • OAuth protection                     │
   └─────────────────────────────────────────┘
```

## Tunnel Configuration

### Multi-Service Setup

```yaml
# ngrok.yml configuration

version: "2"
authtoken: YOUR_AUTHTOKEN

# Multiple tunnels for different services
tunnels:
  event-gateway:      # GitHub webhooks
    proto: http
    addr: 8080
    bind_tls: true
    
  discord-bot:        # Discord interactions
    proto: http
    addr: 3000
    bind_tls: true
    
  refinory:           # AI processing
    proto: http
    addr: 8000
    bind_tls: true
```

### Single Command Startup

```bash
# Start all tunnels at once
ngrok start --all --config=ngrok.yml

# Or use our helper script
./scripts/start-ngrok.sh
```

## Inspection Interface

### Web UI Features

```
http://localhost:4040
├── Status          : Tunnel status and URLs
├── Requests        : All captured HTTP requests/responses
│   ├── Filter      : By status code, method, path
│   ├── Search      : Find specific requests
│   ├── Details     : Headers, body, timing
│   └── Replay      : Resend requests for testing
├── Metrics         : Connection stats and usage
└── Tunnels         : Active tunnel configuration
```

### API Access

```bash
# List tunnels
GET http://localhost:4040/api/tunnels

# Get tunnel details
GET http://localhost:4040/api/tunnels/event-gateway

# List requests
GET http://localhost:4040/api/requests

# Replay request
POST http://localhost:4040/api/requests/http/{id}/replay
```

## Integration Points

### With Docker Compose

```yaml
# docker-compose.yml
services:
  event-gateway:
    ports:
      - "8080:8080"  # ← ngrok forwards here
    environment:
      - WEBHOOK_SECRET=${WEBHOOK_SECRET}
      - DISCORD_TOKEN=${DISCORD_TOKEN}
```

### With GitHub

```
Repository Settings → Webhooks
├── Payload URL     : https://your-tunnel.ngrok.io/webhook
├── Content type    : application/json
├── Secret          : ${WEBHOOK_SECRET}
└── Events          : Pull requests, Pushes, etc.
```

### With Discord

```
Discord Developer Portal → Applications
├── Bot Token       : ${DISCORD_BOT_TOKEN}
├── Intents         : Message Content, Guild Messages
└── OAuth2 URL      : https://your-tunnel.ngrok.io/discord/callback
```

## Performance Considerations

### Latency

```
GitHub → ngrok Cloud → Your Machine → Response
   ↓         ↓              ↓
 ~50ms    ~100ms         ~10ms
═══════════════════════════════════
Total Round Trip: ~160ms
```

### Throughput

```
Free Tier Limits:
├── Connections/min  : 40
├── Bandwidth        : 1GB/month
├── Tunnel Count     : 1 at a time (multiple with start --all)
└── Region           : Closest data center

Paid Tier:
├── Connections/min  : Unlimited
├── Bandwidth        : Unlimited
├── Custom domains   : Yes
└── Reserved URLs    : Yes
```

## Best Practices

1. **Start ngrok after local services**
   ```bash
   docker-compose up -d && ./scripts/start-ngrok.sh
   ```

2. **Use the web interface for debugging**
   ```bash
   open http://localhost:4040
   ```

3. **Replay requests for rapid iteration**
   - No need to trigger real GitHub events
   - Modify request body to test edge cases

4. **Monitor for rate limits**
   - Free tier: 40 connections/minute
   - Check usage in web interface

5. **Secure your webhook secret**
   - Store in `.env` file (already in `.gitignore`)
   - Use strong random values

6. **Use closest region for best performance**
   ```yaml
   region: us  # or eu, ap, au, sa, jp, in
   ```

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Tunnel not connecting | Firewall/proxy blocking | Check network settings |
| 401 Unauthorized | Invalid authtoken | Update ngrok.yml |
| Webhook not received | Service not running | Check `docker-compose ps` |
| Wrong tunnel URL | Restart changed URL | Update GitHub webhook |
| Rate limited | Too many requests | Upgrade or reduce frequency |

### Debug Commands

```bash
# Check tunnel status
curl http://localhost:4040/api/tunnels | jq

# Test local service
curl http://localhost:8080/health

# Check Docker containers
docker-compose ps

# View service logs
docker-compose logs -f event-gateway

# Monitor ngrok logs
tail -f logs/ngrok.log
```

---

**For more details, see:**
- [NGROK_SETUP.md](../NGROK_SETUP.md) - Complete setup guide
- [NGROK_QUICKREF.md](NGROK_QUICKREF.md) - Command reference
- [NGROK_EXAMPLE.md](NGROK_EXAMPLE.md) - Step-by-step tutorial
