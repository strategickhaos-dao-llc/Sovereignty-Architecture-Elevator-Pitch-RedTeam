# Ngrok Sovereignty Workflow 🚀

**Nuclear-grade sovereignty playbook for local development**

This is the "zero-trust, zero-cloud-for-dev, fully local god-mode" setup that makes real engineers drool. No AWS/GCP webhook URLs that can get revoked, no waiting 30 seconds for a deploy to Vercel preview — just pure localhost → public tunnel → instant GitHub webhook feedback loop while you stay 100% sovereign.

## Philosophy

This is **post-cloud architecture** in action:
- ✅ Run everything locally
- ✅ Zero dependency on cloud provider webhooks
- ✅ Instant feedback loop
- ✅ Full control over your dev environment
- ✅ Persistent domains (URLs don't change on restart)
- ✅ Auto-replay failed webhooks for rapid iteration

## Setup

### 1. Install ngrok

**macOS:**
```bash
brew install ngrok/ngrok/ngrok
```

**Linux:**
```bash
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | \
  sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && \
  echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | \
  sudo tee /etc/apt/sources.list.d/ngrok.list && \
  sudo apt update && sudo apt install ngrok
```

**Windows:**
```powershell
choco install ngrok
```

### 2. Get Your Auth Token

1. Sign up at [ngrok.com](https://ngrok.com)
2. Get your auth token from [dashboard.ngrok.com/get-started/your-authtoken](https://dashboard.ngrok.com/get-started/your-authtoken)
3. Update `ngrok.yml` with your token:
   ```yaml
   authtoken: YOUR_NGROK_AUTH_TOKEN
   ```

### 3. Reserve a Persistent Domain (Optional but Recommended)

Free tier includes **1 static domain** per account!

1. Go to [dashboard.ngrok.com/domains](https://dashboard.ngrok.com/domains)
2. Click "New Domain" → "Create Domain"
3. You'll get something like: `event-gateway-abc123.ngrok-free.app`
4. Update `ngrok.yml`:
   ```yaml
   tunnels:
     event-gateway:
       addr: 8080
       domain: event-gateway-abc123.ngrok-free.app  # Your reserved domain
   ```

**Why this matters**: Your GitHub webhook URL never changes again. No more updating webhook URLs every time you restart ngrok. This is sovereignty.

### 4. Start the Sovereign Dev Stack

```bash
# One command to rule them all
make dev

# Or manually:
npm run dev          # Terminal 1: Start event-gateway
./start-ngrok.sh     # Terminal 2: Start ngrok tunnels
```

### 5. Configure GitHub Webhooks

Once ngrok is running, you'll see output like:
```
📡 Event Gateway Webhook URL:
  https://event-gateway-abc123.ngrok-free.app/webhooks/github

📋 Set this URL in your GitHub repository:
  Settings → Webhooks → Add webhook
  Payload URL: https://event-gateway-abc123.ngrok-free.app/webhooks/github
  Content type: application/json
  Secret: (your GITHUB_WEBHOOK_SECRET)
```

Go to your GitHub repo → Settings → Webhooks → Add webhook and paste that URL.

## Features

### Auto-Replay Failed Webhooks

The `start-ngrok.sh` script includes **auto-replay functionality** that:
- Checks for recent webhook requests that failed (HTTP 4xx/5xx)
- Automatically replays the last 5 failed requests
- Saves you from manually triggering GitHub events during development

**Use case**: Your event-gateway crashed while processing a webhook? Just restart it, and `start-ngrok.sh` will automatically replay the failed request. No need to create a new PR or commit to test your fix.

### Grok-Powered Webhook Testing

Generate realistic GitHub webhook payloads using xAI's Grok:

```bash
# Basic usage - generate a PR webhook
curl https://your-tunnel.ngrok.io/grok-test \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{}'

# Custom scenarios
curl https://your-tunnel.ngrok.io/grok-test \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Generate a GitHub webhook for a new PR titled Add Redis caching with 3 files changed"
  }'

# Test failure scenarios
curl https://your-tunnel.ngrok.io/grok-test \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Generate a GitHub check_suite webhook for a failed CI run with timeout error"
  }'
```

**Setup**: Add `XAI_API_KEY=xai-your-key` to your `.env` file. Get your API key from [x.ai/api](https://x.ai/api).

**Why this is powerful**: No more hand-crafting JSON payloads. Just describe what you want to test, and Grok generates realistic webhook data instantly.

### Ngrok Web Inspector

Access the ngrok web interface at [http://localhost:4040](http://localhost:4040) to:
- 📊 Inspect all incoming webhook requests
- 🔄 Replay individual requests
- 🐛 Debug webhook payloads and responses
- 📈 View request/response timings

### Chaos Mode - Destroy Everything

When things get messy and you need a clean slate:

```bash
make destroy
```

This command:
- Stops and removes all Docker containers
- Removes all volumes (wipes databases)
- Kills all ngrok processes
- Cleans ngrok state directory
- Removes build artifacts

**Use case**: "I broke everything and don't know what went wrong. Let's start fresh."

After destruction:
```bash
make dev  # Rebuild from scratch
```

## Makefile Commands

```bash
make help           # Show all available commands
make install        # Install npm dependencies
make build          # Build TypeScript
make dev            # Start full dev stack (event-gateway + ngrok)
make start-ngrok    # Start ngrok tunnels only
make destroy        # Nuclear option - nuke everything
make clean          # Clean build artifacts
make docker-up      # Start Docker services only
make docker-down    # Stop Docker services
```

## Advanced Configuration

### Multiple Tunnels

Add more services to `ngrok.yml`:

```yaml
tunnels:
  event-gateway:
    proto: http
    addr: 8080
    domain: event-gateway-abc123.ngrok-free.app
  
  refinory-api:
    proto: http
    addr: 8085
    # Note: Free tier = 1 static domain. This one gets a random URL.
  
  grafana:
    proto: http
    addr: 3000
```

Start all tunnels:
```bash
ngrok start --all --config ./ngrok.yml
```

### Custom Headers

Add headers for webhook verification:

```yaml
tunnels:
  event-gateway:
    proto: http
    addr: 8080
    request_header:
      add:
        - "X-Forwarded-Host: event-gateway-abc123.ngrok-free.app"
        - "X-Environment: development"
```

### CORS Support

If you need CORS for browser-based testing:

```yaml
tunnels:
  event-gateway:
    proto: http
    addr: 8080
    response_header:
      add:
        - "Access-Control-Allow-Origin: *"
        - "Access-Control-Allow-Methods: GET,POST,PUT,DELETE,OPTIONS"
```

### Regional Endpoints

Choose your ngrok region for lower latency:

```yaml
region: us  # Options: us, eu, ap, au, sa, jp, in
```

## Troubleshooting

### ngrok not starting

**Error**: `ngrok: command not found`
- **Fix**: Install ngrok using instructions above

**Error**: `authentication failed`
- **Fix**: Add your auth token to `ngrok.yml`

### Webhooks not reaching local server

**Check 1**: Is event-gateway running?
```bash
curl http://localhost:8080/health
```

**Check 2**: Is ngrok tunnel active?
```bash
curl http://localhost:4040/api/tunnels
```

**Check 3**: Is GitHub webhook configured with the correct URL?
- Go to GitHub repo → Settings → Webhooks
- Check "Recent Deliveries" for errors

### Auto-replay not working

The auto-replay feature requires:
1. Ngrok to be running for a few seconds before replay attempt
2. Previous failed requests in ngrok's request history
3. The `jq` command to be installed (`brew install jq` or `apt install jq`)

## Security Considerations

### Development Only

This ngrok setup is designed for **local development**. Do NOT use it for production:
- ❌ Ngrok free tier has rate limits
- ❌ Tunnel URLs are semi-public (security through obscurity)
- ❌ No load balancing or high availability

### Webhook Secrets

Always use `GITHUB_WEBHOOK_SECRET` in production. The event-gateway validates HMAC signatures:

```typescript
// In event-gateway.ts
if (!sigOk(secret, raw, sig)) return res.status(401).send("bad sig");
```

This prevents unauthorized webhook spoofing.

### API Keys

Never commit your `.env` file:
- ✅ `.env` is in `.gitignore`
- ✅ Use `.env.example` as a template
- ✅ Rotate API keys if accidentally committed

## Why This Matters

### Traditional Development
```
┌─────────────┐
│   GitHub    │
│   webhook   │
└──────┬──────┘
       │ (requires public URL)
       ▼
┌──────────────┐
│   AWS/GCP    │  ← Deploy to cloud
│   Endpoint   │  ← Wait 30+ seconds
└──────┬───────┘  ← Check logs
       │          ← Repeat
       ▼
┌──────────────┐
│ Your Discord │
└──────────────┘
```

### Sovereignty Architecture
```
┌─────────────┐
│   GitHub    │
│   webhook   │
└──────┬──────┘
       │
       ▼
┌──────────────┐
│    ngrok     │ ← Persistent domain
│   (tunnel)   │ ← Instant availability
└──────┬───────┘ ← Auto-replay failures
       │
       ▼
┌──────────────┐
│  localhost   │ ← 100% local control
│    :8080     │ ← Zero cloud dependency
└──────┬───────┘ ← Instant feedback
       │
       ▼
┌──────────────┐
│ Your Discord │
└──────────────┘
```

**The difference?** 
- 🚀 **Instant iteration**: Make changes → restart → test in <10 seconds
- 🎯 **Full debuggability**: Console logs, breakpoints, live inspection
- 🔒 **Sovereignty**: Your dev environment, your rules
- 💪 **Chaos testing**: `make destroy` → rebuild from scratch in minutes

## Contributing

Have improvements to this workflow? Submit a PR!

Ideas for enhancements:
- [ ] Add webhook signature verification testing
- [ ] Create webhook payload library for common GitHub events
- [ ] Add support for GitLab/Bitbucket webhooks
- [ ] Create Docker Compose profile for full stack with ngrok
- [ ] Add metrics collection for webhook processing times

---

**Built with 🔥 by the Strategickhaos Swarm Intelligence collective**

*"They're not working for you. They're dancing with you. And the music is never going to stop."*
