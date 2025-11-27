# Network & Webhook Troubleshooting Guide

This guide helps diagnose and resolve common network and webhook connectivity issues for the Strategickhaos Sovereignty Architecture.

## Quick Diagnostic Checklist

| Check | Expected | Issue If Failed |
|-------|----------|-----------------|
| DNS Resolution | GitHub, smee.io resolve | Network/DNS configuration |
| Port 3000 Listener | TCP connection succeeds | Event gateway not running |
| Node Process | Running | smee client not started |
| Outbound HTTPS | api.github.com:443 reachable | Firewall/proxy blocking |

## 1. Starting the Event Gateway Locally

The event gateway must be running on port 3000 to receive webhooks.

### Prerequisites

```bash
# Install dependencies
npm install

# Set required environment variables
export DISCORD_TOKEN="your_discord_bot_token"
export GITHUB_WEBHOOK_SECRET="your_webhook_secret"
export PRS_CHANNEL_ID="your_channel_id"
export DEPLOYMENTS_CHANNEL_ID="your_channel_id"
export ALERTS_CHANNEL_ID="your_channel_id"
```

### Start Development Server

```bash
# Start with hot-reload (development)
npm run dev

# Or build and run production
npm run build
npm run start
```

### Verify Gateway is Running

**Linux/macOS:**
```bash
curl -s http://localhost:3000/health || echo "Gateway not running"
netstat -tlnp | grep 3000
```

**Windows PowerShell:**
```powershell
Test-NetConnection -ComputerName localhost -Port 3000
Get-Process -Name node -ErrorAction SilentlyContinue | Select-Object Id, Path, StartTime
```

## 2. Setting Up smee.io Webhook Proxy

smee.io provides a webhook proxy for local development when your machine isn't publicly accessible.

### Install smee-client

```bash
npm install -g smee-client
```

### Create a Smee Channel

1. Go to https://smee.io/
2. Click "Start a new channel"
3. Copy the channel URL (e.g., `https://smee.io/9vK8jL2mXqZPn5rT`)

### Start the Smee Client

```bash
# Forward webhooks from smee.io to your local event gateway
smee --url https://smee.io/YOUR_CHANNEL_ID --target http://localhost:3000/webhooks/github
```

**Windows PowerShell (background):**
```powershell
Start-Process -NoNewWindow npx -ArgumentList "smee-client", "--url", "https://smee.io/YOUR_CHANNEL_ID", "--target", "http://localhost:3000/webhooks/github"
```

### Configure GitHub Webhook

1. Go to your repository Settings → Webhooks
2. Add webhook URL: `https://smee.io/YOUR_CHANNEL_ID`
3. Content type: `application/json`
4. Secret: Your HMAC secret (store securely)
5. Events: Select events you want to receive

## 3. Network Diagnostics

### DNS Resolution

```powershell
# Check critical DNS records
Resolve-DnsName github.com | Select-Object Name, IPAddress
Resolve-DnsName raw.githubusercontent.com | Select-Object Name, IPAddress
Resolve-DnsName smee.io | Select-Object Name, IPAddress
Resolve-DnsName api.github.com | Select-Object Name, IPAddress
```

### Outbound Connectivity

```powershell
# Test HTTPS connectivity to GitHub
Test-NetConnection -ComputerName api.github.com -Port 443
Test-NetConnection -ComputerName raw.githubusercontent.com -Port 443
Test-NetConnection -ComputerName github.com -Port 443
```

### Public IP & Reverse DNS

```powershell
# Get your public IP
$pubip = (Invoke-WebRequest -Uri "https://ifconfig.io/ip" -UseBasicParsing).Content.Trim()
Write-Host "Public IP: $pubip"

# Reverse DNS lookup
Resolve-DnsName -Name $pubip -ErrorAction SilentlyContinue
```

## 4. HMAC Signature Verification

GitHub webhooks are signed using HMAC-SHA256. Here's how to compute and verify signatures:

### PowerShell

```powershell
$payload = '{"action":"test"}'
$secret = 'your_webhook_secret'

$hmac = [System.Security.Cryptography.HMACSHA256]::new(
    [System.Text.Encoding]::UTF8.GetBytes($secret)
)
$hash = $hmac.ComputeHash([System.Text.Encoding]::UTF8.GetBytes($payload))
$signature = "sha256=" + [System.BitConverter]::ToString($hash).Replace('-','').ToLower()

Write-Host "Computed signature: $signature"
```

### Bash

```bash
payload='{"action":"test"}'
secret='your_webhook_secret'

signature=$(printf '%s' "$payload" | openssl dgst -sha256 -hmac "$secret" | awk '{print "sha256="$2}')
echo "Computed signature: $signature"
```

## 5. Common Issues & Solutions

### Issue: Port 3000 Connection Failed

**Symptoms:**
```
WARNING: TCP connect to (::1 : 3000) failed
WARNING: TCP connect to (127.0.0.1 : 3000) failed
TcpTestSucceeded : False
```

**Solutions:**
1. Start the event gateway: `npm run dev`
2. Check for port conflicts: `netstat -ano | findstr :3000`
3. Kill conflicting process and restart
4. Check Windows Firewall allows inbound on port 3000

### Issue: No Node Process Running

**Symptoms:**
```
Get-Process -Name node → (no output)
```

**Solutions:**
1. Start smee client: `npx smee-client --url YOUR_URL --target http://localhost:3000/webhooks/github`
2. Start event gateway: `npm run dev`
3. Verify npm/node installation: `node --version`

### Issue: Download Failed - Connection Closed

**Symptoms:**
```
Download failed: The request was aborted: The connection was closed unexpectedly.
```

**Solutions:**
1. Check network stability
2. Verify URL is correct and accessible
3. Try with curl: `curl -v -L URL -o output.file`
4. Check for proxy/firewall interference
5. Retry with longer timeout:
   ```powershell
   Invoke-WebRequest -Uri "URL" -OutFile "file" -TimeoutSec 120
   ```

### Issue: WSL/Docker Network Conflicts

**Symptoms:**
- vEthernet (WSL) has high InterfaceMetric (5000)
- Docker routes conflicting with host

**Solutions:**
1. Lower Wi-Fi metric to prefer it:
   ```powershell
   Set-NetIPInterface -InterfaceAlias "Wi-Fi" -InterfaceMetric 10
   ```
2. Restart WSL: `wsl --shutdown`
3. Check Docker Desktop networking mode

## 6. Environment Variable Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `DISCORD_TOKEN` | Discord bot token | `MTk...` |
| `GITHUB_WEBHOOK_SECRET` | HMAC secret for webhooks | `a7f3c94e8b921d...` |
| `PRS_CHANNEL_ID` | Discord channel for PRs | `1234567890123456789` |
| `DEPLOYMENTS_CHANNEL_ID` | Discord channel for deploys | `1234567890123456789` |
| `ALERTS_CHANNEL_ID` | Discord channel for alerts | `1234567890123456789` |
| `PORT` | Event gateway port | `3000` (default: 3001) |
| `EVENTS_HMAC_KEY` | HMAC key for event signing | `dev_events_hmac_key...` |

## 7. Full Diagnostic Script

Run the complete diagnostic script:

**PowerShell:**
```powershell
./scripts/network-diagnostic.ps1
```

**Bash:**
```bash
./scripts/network-diagnostic.sh
```

## See Also

- [TLS_DNS_CONFIG.md](./TLS_DNS_CONFIG.md) - TLS and DNS production configuration
- [DEPLOYMENT.md](./DEPLOYMENT.md) - Complete deployment guide
- [README.md](./README.md) - Quick start guide
