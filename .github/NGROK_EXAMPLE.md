# ngrok Usage Example for Sovereignty Architecture

This example demonstrates a complete workflow for setting up ngrok tunnels and testing GitHub webhooks locally.

## 📋 Prerequisites

- ngrok installed and configured (see [NGROK_SETUP.md](../NGROK_SETUP.md))
- Docker and Docker Compose installed
- GitHub repository with webhook access

## 🎯 Step-by-Step Tutorial

### 1. Configure Your ngrok Authtoken

First, get your authtoken from https://dashboard.ngrok.com/get-started/your-authtoken

```bash
# Edit ngrok.yml and replace YOUR_NGROK_AUTHTOKEN with your actual token
nano ngrok.yml

# Or use sed to replace it
sed -i 's/YOUR_NGROK_AUTHTOKEN/your_actual_token_here/g' ngrok.yml
```

### 2. Start Local Services

Start your local development environment:

```bash
# Start all services with Docker Compose
docker-compose up -d

# Verify services are running
docker-compose ps

# Check service health
curl http://localhost:8080/health  # Event Gateway
curl http://localhost:3000/health  # Discord Bot
curl http://localhost:8000/health  # Refinory
```

### 3. Start ngrok Tunnels

```bash
# Linux/macOS
./scripts/start-ngrok.sh

# Windows (PowerShell)
.\scripts\start-ngrok.ps1

# You should see output like:
# ═══════════════════════════════════════════════════════════
# 🌐 Tunnel URLs:
# ═══════════════════════════════════════════════════════════
#
#   event-gateway        https://abc123.ngrok.io
#   discord-bot          https://def456.ngrok.io
#   refinory             https://ghi789.ngrok.io
```

### 4. Get Your Tunnel URL

Open the ngrok web interface to see your tunnel URLs:

```bash
# Open web interface
open http://localhost:4040  # macOS
# OR: start http://localhost:4040  # Windows
# OR: xdg-open http://localhost:4040  # Linux

# Or get URLs via API
curl http://localhost:4040/api/tunnels | jq -r '.tunnels[] | select(.name=="event-gateway") | .public_url'
```

Example output:
```
https://f3e8-203-0-113-42.ngrok.io
```

### 5. Configure GitHub Webhook

1. Go to your GitHub repository
2. Click **Settings** → **Webhooks** → **Add webhook**
3. Fill in the webhook details:

```
Payload URL: https://YOUR-TUNNEL-URL.ngrok.io/webhook
Content type: application/json
Secret: your_webhook_secret (from .env file)

Events:
☑ Pull requests
☑ Pushes
☑ Issues
☑ Issue comments
```

4. Click **Add webhook**

### 6. Test the Webhook

#### Option A: Trigger a Real Event

```bash
# Create a test file and push
echo "test" > test-webhook.txt
git add test-webhook.txt
git commit -m "Test webhook"
git push origin main
```

#### Option B: Send Manual Test

From GitHub webhook settings, click **Recent Deliveries** and **Redeliver** a past event.

#### Option C: Use curl

```bash
# Set your webhook secret
SECRET="your_webhook_secret"

# Create a test payload
PAYLOAD='{"action":"opened","pull_request":{"number":123,"title":"Test PR"}}'

# Generate HMAC signature
SIGNATURE=$(echo -n "$PAYLOAD" | openssl dgst -sha256 -hmac "$SECRET" | sed 's/^.* //')

# Send the webhook
curl -X POST https://YOUR-TUNNEL-URL.ngrok.io/webhook \
  -H "Content-Type: application/json" \
  -H "X-GitHub-Event: pull_request" \
  -H "X-Hub-Signature-256: sha256=$SIGNATURE" \
  -H "X-GitHub-Delivery: test-$(date +%s)" \
  -d "$PAYLOAD"
```

### 7. Inspect the Request

Open http://localhost:4040 and you'll see:

```
Status: 200 OK
Duration: 45ms

Request Headers:
  Content-Type: application/json
  X-GitHub-Event: pull_request
  X-Hub-Signature-256: sha256=...
  
Request Body:
  {"action":"opened","pull_request":...}

Response Headers:
  Content-Type: application/json
  
Response Body:
  {"status":"success","message":"Webhook received"}
```

### 8. Debug with Logs

Check your local service logs:

```bash
# View event gateway logs
docker-compose logs -f event-gateway

# Should show something like:
# event-gateway | 2025-11-19 17:00:00 INFO  [webhook] GitHub webhook received
# event-gateway | 2025-11-19 17:00:00 INFO  [webhook] Event: pull_request
# event-gateway | 2025-11-19 17:00:00 INFO  [webhook] Action: opened
# event-gateway | 2025-11-19 17:00:00 INFO  [discord] Sending notification to #prs
```

### 9. Test Webhook Signature Validation

Test with an invalid signature to ensure security:

```bash
# Send webhook with wrong signature
curl -X POST https://YOUR-TUNNEL-URL.ngrok.io/webhook \
  -H "Content-Type: application/json" \
  -H "X-GitHub-Event: ping" \
  -H "X-Hub-Signature-256: sha256=invalid_signature" \
  -d '{"test":"data"}'

# Should return 401 Unauthorized
```

### 10. Use Replay Feature for Testing

1. Go to http://localhost:4040
2. Find a previous webhook request
3. Click **Replay** to send it again
4. Modify the request body or headers if needed
5. Test different scenarios quickly

## 🔄 Complete Development Workflow

```bash
# 1. Start everything
docker-compose up -d && ./scripts/start-ngrok.sh

# 2. Make code changes
vim src/event-gateway.ts

# 3. Restart the service
docker-compose restart event-gateway

# 4. Test immediately with replay in ngrok UI
# (No need to trigger real GitHub events!)

# 5. View logs
docker-compose logs -f event-gateway

# 6. Iterate quickly!
```

## 📊 Monitoring Your Tunnels

### Check Tunnel Status

```bash
# List all active tunnels
curl http://localhost:4040/api/tunnels | jq '.tunnels[] | {name, public_url, config}'

# Get tunnel metrics
curl http://localhost:4040/api/tunnels/event-gateway | jq '.metrics'
```

### View Request History

```bash
# List recent requests
curl http://localhost:4040/api/requests | jq '.requests[] | {uri, method, status, duration}'

# Get specific request details
REQUEST_ID=$(curl -s http://localhost:4040/api/requests | jq -r '.requests[0].id')
curl http://localhost:4040/api/requests/http/$REQUEST_ID | jq
```

### Monitor in Real-Time

```bash
# Watch for new requests
watch -n 2 'curl -s http://localhost:4040/api/requests | jq ".requests[-5:] | .[] | {uri, method, status}"'
```

## 🐛 Troubleshooting Common Issues

### Issue: Webhook not received

```bash
# 1. Check if ngrok tunnel is running
curl http://localhost:4040/api/tunnels

# 2. Check if local service is accessible
curl http://localhost:8080/health

# 3. Check Docker container logs
docker-compose logs event-gateway

# 4. Verify webhook URL in GitHub settings
# Make sure it matches your ngrok tunnel URL
```

### Issue: Signature validation failing

```bash
# 1. Check your webhook secret
echo $GITHUB_WEBHOOK_SECRET

# 2. Verify it matches in GitHub webhook settings

# 3. Test with known good signature
# See step 6 above for signature generation
```

### Issue: Tunnel connection lost

```bash
# 1. Restart ngrok
# Press Ctrl+C to stop
./scripts/start-ngrok.sh

# 2. Update GitHub webhook URL with new tunnel URL
# (Free tier tunnels get new URLs on restart)
```

## 💡 Pro Tips

1. **Save time with replay**: Use ngrok's replay feature instead of triggering real GitHub events
2. **Test edge cases**: Modify replayed requests to test error conditions
3. **Monitor latency**: Check request duration in ngrok UI to optimize performance
4. **Use filters**: Click status codes in ngrok UI to filter by success/error
5. **Export requests**: Right-click requests in ngrok UI to copy as curl commands

## 🎓 Next Steps

- [ ] Set up Discord bot local testing
- [ ] Test refinory AI processing locally
- [ ] Add custom webhook endpoints
- [ ] Test with multiple repositories
- [ ] Set up staging environment with persistent ngrok domain

## 📚 Additional Resources

- [ngrok Web Interface](http://localhost:4040)
- [ngrok API Documentation](https://ngrok.com/docs/api)
- [GitHub Webhooks Documentation](https://docs.github.com/en/webhooks)
- [Sovereignty Architecture README](../README.md)
- [Complete ngrok Setup Guide](../NGROK_SETUP.md)

---

**Happy local testing! 🚀**
