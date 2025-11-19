# ngrok Setup Guide for Sovereignty Architecture

## 🎯 Purpose

This guide helps you set up ngrok tunnels for **local development and webhook testing** of the Sovereignty Architecture. ngrok allows you to:

- ✅ Test GitHub webhooks locally without deploying to production
- ✅ Receive Discord interactions during development
- ✅ Debug webhook payloads in real-time
- ✅ Expose local services for integration testing

## 📦 Installation

### macOS (Homebrew)
```bash
brew install ngrok/ngrok/ngrok
```

### Linux (Debian/Ubuntu)
```bash
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | \
  sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null

echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | \
  sudo tee /etc/apt/sources.list.d/ngrok.list

sudo apt update && sudo apt install ngrok
```

### Windows (Chocolatey)
```powershell
choco install ngrok
```

### Manual Installation
1. Download from: https://ngrok.com/download
2. Extract the executable to a directory in your PATH
3. Verify installation: `ngrok version`

## 🔐 Configuration

### 1. Get Your ngrok Authtoken

1. Sign up for a free account at https://ngrok.com
2. Navigate to https://dashboard.ngrok.com/get-started/your-authtoken
3. Copy your authtoken

### 2. Configure ngrok.yml

Edit `ngrok.yml` in the repository root and replace `YOUR_NGROK_AUTHTOKEN` with your actual token:

```yaml
authtoken: your_actual_authtoken_here
```

### 3. (Optional) Customize Subdomains

Free ngrok accounts get random subdomains. For custom subdomains, you'll need a paid plan. Edit `ngrok.yml`:

```yaml
tunnels:
  event-gateway:
    subdomain: your-custom-name  # Requires paid plan
```

Or remove the `subdomain` line to use auto-generated URLs (free tier).

## 🚀 Quick Start

### Start All Tunnels

```bash
./scripts/start-ngrok.sh
```

This script will:
1. ✅ Check if ngrok is installed
2. ✅ Validate your configuration
3. ✅ Start all configured tunnels
4. ✅ Display tunnel URLs
5. ✅ Open web inspection interface

### Manual Start

```bash
ngrok start --all --config=ngrok.yml
```

### Start Individual Tunnels

```bash
# Just the event gateway
ngrok start event-gateway --config=ngrok.yml

# Multiple specific tunnels
ngrok start event-gateway discord-bot --config=ngrok.yml
```

## 🔌 Tunnel Configuration

The default configuration includes three tunnels:

### 1. Event Gateway (Port 8080)
- **Purpose**: Receives GitHub webhook events
- **Local**: http://localhost:8080
- **Public**: https://your-tunnel.ngrok.io
- **Usage**: Configure as GitHub webhook URL

### 2. Discord Bot (Port 3000)
- **Purpose**: Discord bot API endpoint
- **Local**: http://localhost:3000
- **Public**: https://your-tunnel.ngrok.io
- **Usage**: Discord interaction endpoints

### 3. Refinory Service (Port 8000)
- **Purpose**: AI processing and refinement
- **Local**: http://localhost:8000
- **Public**: https://your-tunnel.ngrok.io
- **Usage**: External API calls to refinory

## 🔍 Web Inspection Interface

ngrok provides a web interface for inspecting requests:

1. Open http://localhost:4040 in your browser
2. View all HTTP requests and responses
3. Replay requests for debugging
4. Inspect headers, bodies, and timing

## 🛠️ GitHub Webhook Setup

### 1. Get Your Tunnel URL

After starting ngrok, copy the event-gateway tunnel URL from the output or web interface.

### 2. Configure GitHub Webhook

1. Go to your GitHub repository settings
2. Navigate to **Settings → Webhooks → Add webhook**
3. Set **Payload URL**: `https://your-tunnel.ngrok.io/webhook`
4. Set **Content type**: `application/json`
5. Set **Secret**: Your webhook secret from `.env`
6. Select events to trigger (e.g., Pull requests, Pushes)
7. Click **Add webhook**

### 3. Test the Webhook

1. Create a test event (e.g., open a PR or push a commit)
2. Check ngrok web interface at http://localhost:4040
3. View the webhook payload and your service's response
4. Check your local service logs for processing details

## 🐛 Troubleshooting

### ngrok Command Not Found

**Problem**: `bash: ngrok: command not found`

**Solution**:
```bash
# Verify installation
which ngrok

# If not found, reinstall or add to PATH
export PATH=$PATH:/path/to/ngrok
```

### Invalid Authtoken

**Problem**: `ERROR: authentication failed: Your authtoken is not valid`

**Solution**:
1. Verify you've updated `ngrok.yml` with your actual token
2. Check for extra spaces or quotes around the token
3. Get a fresh token from https://dashboard.ngrok.com

### Tunnel Connection Failed

**Problem**: `ERROR: failed to connect to ngrok.com`

**Solution**:
1. Check your internet connection
2. Verify firewall isn't blocking ngrok
3. Try different region in `ngrok.yml`: `region: eu` or `region: us`

### Port Already in Use

**Problem**: `ERROR: bind: address already in use`

**Solution**:
```bash
# Find what's using the port
lsof -i :8080

# Kill the process or change port in ngrok.yml
```

### Webhook Not Received

**Problem**: GitHub webhook shows delivery but no logs in local service

**Solution**:
1. Verify your local service is running: `curl http://localhost:8080/health`
2. Check ngrok web interface for received requests
3. Verify webhook secret matches between GitHub and your `.env`
4. Check ngrok tunnel status: `curl http://localhost:4040/api/tunnels`

### Subdomain Not Available

**Problem**: `ERROR: the subdomain is not available`

**Solution**:
1. Free accounts can't use custom subdomains - remove `subdomain:` line
2. Or upgrade to a paid ngrok plan
3. Use the auto-generated random subdomain

## 💡 Best Practices

### Security

1. **Never commit your authtoken** - It's already in `.gitignore`
2. **Use webhook secrets** - Always verify HMAC signatures
3. **Monitor the inspection interface** - Watch for unexpected requests
4. **Rotate authtokens periodically** - Generate new tokens in ngrok dashboard

### Development Workflow

1. **Start local services first**
   ```bash
   docker-compose up -d
   ```

2. **Then start ngrok**
   ```bash
   ./scripts/start-ngrok.sh
   ```

3. **Configure webhooks** with the ngrok URLs

4. **Use replay feature** in web interface to test edge cases

### Performance

1. **Choose closest region** - Edit `region:` in `ngrok.yml`
2. **Use compression** - ngrok automatically compresses HTTP
3. **Monitor latency** - Check inspection interface for timing
4. **Free tier limits** - 40 connections/minute, check usage

## 🔗 Integration with Services

### Docker Compose

If using Docker Compose for local development:

```yaml
# docker-compose.yml
services:
  event-gateway:
    ports:
      - "8080:8080"  # Match ngrok tunnel port
```

### Environment Variables

Update your `.env` file with ngrok URLs:

```bash
# .env
WEBHOOK_URL=https://your-tunnel.ngrok.io/webhook
PUBLIC_URL=https://your-tunnel.ngrok.io
```

### Testing Script

Quick test to verify tunnel is working:

```bash
# Test event gateway tunnel
curl -X POST https://your-tunnel.ngrok.io/health

# Check from ngrok web interface
open http://localhost:4040
```

## 📚 Additional Resources

- **ngrok Documentation**: https://ngrok.com/docs
- **ngrok Dashboard**: https://dashboard.ngrok.com
- **ngrok Pricing**: https://ngrok.com/pricing
- **GitHub Webhooks**: https://docs.github.com/en/webhooks
- **Discord Interactions**: https://discord.com/developers/docs/interactions/receiving-and-responding

## 🆘 Support

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review logs: `tail -f logs/ngrok.log`
3. Visit ngrok web interface: http://localhost:4040
4. Check repository issues: [GitHub Issues](https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-/issues)
5. Join our Discord: [Strategickhaos Discord](https://discord.gg/strategickhaos)

## 🎓 Learning Path

### Beginner
1. ✅ Install ngrok
2. ✅ Configure authtoken
3. ✅ Start a single tunnel
4. ✅ View requests in web interface

### Intermediate
1. ✅ Configure multiple tunnels
2. ✅ Set up GitHub webhooks
3. ✅ Test webhook payloads
4. ✅ Debug with replay feature

### Advanced
1. ✅ Custom domains (paid plan)
2. ✅ TLS termination
3. ✅ IP restrictions
4. ✅ Custom headers and auth

---

**Built with 🔥 by the Strategickhaos Swarm Intelligence collective**

*Making sovereign architecture accessible for local development*
