# ngrok Quick Reference

## 🚀 Quick Commands

```bash
# Start all tunnels (recommended)
./scripts/start-ngrok.sh

# Start with config file
ngrok start --all --config=ngrok.yml

# Start specific tunnel
ngrok start event-gateway --config=ngrok.yml

# Start HTTP tunnel on port 8080 (simple)
ngrok http 8080

# Web inspection interface
open http://localhost:4040
```

## 🔍 Inspection API

```bash
# List all tunnels
curl http://localhost:4040/api/tunnels | jq

# Get specific tunnel info
curl http://localhost:4040/api/tunnels/event-gateway | jq

# List captured requests
curl http://localhost:4040/api/requests | jq
```

## 🛠️ Testing Webhooks

```bash
# Test event gateway health
curl -X POST https://your-tunnel.ngrok.io/health

# Send test webhook
curl -X POST https://your-tunnel.ngrok.io/webhook \
  -H "Content-Type: application/json" \
  -H "X-GitHub-Event: ping" \
  -d '{"zen":"Keep it logically awesome"}'

# Test with HMAC signature
SECRET="your_webhook_secret"
PAYLOAD='{"test":"data"}'
SIGNATURE=$(echo -n "$PAYLOAD" | openssl dgst -sha256 -hmac "$SECRET" | sed 's/^.* //')
curl -X POST https://your-tunnel.ngrok.io/webhook \
  -H "Content-Type: application/json" \
  -H "X-Hub-Signature-256: sha256=$SIGNATURE" \
  -d "$PAYLOAD"
```

## 📊 Monitoring

```bash
# Watch ngrok logs
tail -f logs/ngrok.log

# Check tunnel status
curl http://localhost:4040/api/tunnels | jq '.tunnels[] | {name, public_url, config}'

# Monitor requests in real-time
watch -n 2 'curl -s http://localhost:4040/api/requests | jq ".requests[-5:] | .[] | {uri, method, status}"'
```

## 🐛 Debugging

```bash
# Replay last request
REQUEST_ID=$(curl -s http://localhost:4040/api/requests | jq -r '.requests[-1].id')
curl -X POST http://localhost:4040/api/requests/http/$REQUEST_ID/replay

# Clear request history
curl -X DELETE http://localhost:4040/api/requests/http

# Check ngrok status
curl http://localhost:4040/status
```

## ⚙️ Configuration Snippets

### Basic HTTP Tunnel
```yaml
tunnels:
  myservice:
    proto: http
    addr: 8080
```

### With Authentication
```yaml
tunnels:
  myservice:
    proto: http
    addr: 8080
    auth: "user:password"
```

### With IP Restrictions (Paid)
```yaml
tunnels:
  myservice:
    proto: http
    addr: 8080
    ip_restriction:
      allow_cidrs:
        - "1.2.3.4/32"
        - "10.0.0.0/8"
```

### With Request/Response Headers
```yaml
tunnels:
  myservice:
    proto: http
    addr: 8080
    request_headers:
      add:
        - "X-Custom-Header: value"
    response_headers:
      add:
        - "X-Response-Header: value"
```

## 🔐 Security

```bash
# Generate webhook secret
openssl rand -hex 32

# Test HMAC signature verification
echo -n 'payload' | openssl dgst -sha256 -hmac 'secret'

# Check certificate info
curl -vI https://your-tunnel.ngrok.io 2>&1 | grep -A 10 "Server certificate"
```

## 💡 Pro Tips

1. **Use the web interface**: http://localhost:4040 is your best friend
2. **Save useful requests**: Use the replay feature for testing edge cases
3. **Filter by status**: Click status codes in web UI to filter requests
4. **Use regions wisely**: Set closest region in config for better latency
5. **Check limits**: Free tier has 40 connections/min limit
6. **Keep logs**: ngrok logs are useful for debugging later

## 🔗 Useful Links

- [ngrok Dashboard](https://dashboard.ngrok.com)
- [ngrok Documentation](https://ngrok.com/docs)
- [API Reference](https://ngrok.com/docs/api)
- [GitHub Integration Guide](https://ngrok.com/docs/integrations/github/)
