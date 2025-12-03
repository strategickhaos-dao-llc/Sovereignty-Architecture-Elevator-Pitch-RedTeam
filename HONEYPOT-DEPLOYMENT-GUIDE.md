# 🔥 Honeypot System - Quick Deployment Guide

This guide helps you quickly deploy the honeypot security system for leak detection and OpSec.

## Prerequisites

- Docker and Docker Compose installed
- Access to a server (can be local, VPS, or behind Tailscale/Cloudflare)
- Basic understanding of networking and security

## Quick Start (5 minutes)

### 1. Clone and Navigate

```bash
git clone https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-.git
cd Sovereignty-Architecture-Elevator-Pitch-
```

### 2. Build Lab Packages

```bash
# Build both real and honeypot versions
./scripts/build-lab-packages.sh

# Packages are created in invite-html/
# - real-lab.zip (105KB)
# - honeypot-lab.zip (9.3KB)
# - checksums.txt
```

### 3. Configure Environment

```bash
# Copy example config
cp .env.honeypot.example .env.honeypot

# Edit configuration
nano .env.honeypot

# Set your tracking URL
BEACON_URL=https://your-tracking-server.com/leaker

# Optional: Set WebUI URL
WEBUI_URL=http://your-tailscale-ip:3000
```

### 4. Deploy System

```bash
# Start all services
./start-honeypot.sh

# Or manually:
docker compose -f docker-compose-honeypot.yml up -d
```

### 5. Access Landing Page

**Local Access:**
```
http://localhost:8080
```

**Public Access (with Cloudflare/Tailscale):**
```
https://your-domain.com
```

## System Architecture

```
┌─────────────────────────────────────────────────────┐
│                  Invite Gate (Nginx)                 │
│  - Serves landing page                               │
│  - Logs all access to shared volume                  │
│  - Serves lab packages when available                │
└────────────────┬────────────────────────────────────┘
                 │
                 │ Shared nginx_logs volume
                 │
┌────────────────┴────────────────────────────────────┐
│             Visitor Logger (Python)                  │
│  - Monitors nginx access logs                        │
│  - Detects suspicious activity                       │
│  - Writes events to honeypot_events.log              │
└──────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────┐
│             Honeypot Git Server                       │
│  - Serves watermarked Git repositories               │
│  - Accessible via SSH on port 2222                   │
└──────────────────────────────────────────────────────┘
```

## Event Types Tracked

The visitor logger detects and logs these events:

1. **REAL_LAB_DOWNLOAD** - Someone downloaded real-lab.zip
2. **HONEYPOT_DOWNLOAD** - Someone downloaded honeypot-lab.zip  
3. **SUSPICIOUS_ACCESS** - Unusual access patterns (bots, curl, wget)
4. **BEACON_ACTIVATION** - Honeypot lab deployed somewhere (beacon phoned home)

## Monitoring

### View Real-time Logs

```bash
# Watch visitor logger
docker logs -f snoop-detector

# View events
cat logs/honeypot_events.log

# With jq formatting
jq -r '. | "\(.timestamp) - \(.event_type) - \(.data.ip)"' logs/honeypot_events.log
```

### Check System Status

```bash
docker compose -f docker-compose-honeypot.yml ps
```

### View Recent Events

```bash
# Last 10 events
tail -10 logs/honeypot_events.log | jq

# Filter by type
jq 'select(.event_type == "HONEYPOT_DOWNLOAD")' logs/honeypot_events.log
```

## Distribution Strategy

### Option 1: Direct Link (Simple)

1. Send trusted people: `https://your-domain.com`
2. They download `real-lab.zip`
3. Monitor logs to see who accessed

### Option 2: Unique Packages (Advanced)

1. Create 10 unique honeypot packages (each with different watermark)
2. Give each person their specific version
3. If leaked, watermark reveals who shared it

```bash
# Create unique package for person
RECIPIENT="john@example.com" ./scripts/build-lab-packages.sh
```

### Option 3: Token-Based Access

1. Uncomment token check in `nginx-conf/default.conf`
2. Generate unique tokens per person
3. Send personalized URLs: `https://your-domain.com/?token=abc123...`

## Security Best Practices

### Enable Basic Authentication

```bash
# Create password file
docker run --rm nginx:alpine \
    htpasswd -cb /tmp/.htpasswd username password

# Copy to nginx-conf
cp /tmp/.htpasswd nginx-conf/.htpasswd

# Uncomment auth_basic lines in nginx-conf/default.conf
```

### Enable Secret Token

Edit `nginx-conf/default.conf`:

```nginx
location = / {
    if ($arg_token != "YOUR_SECRET_TOKEN") {
        return 403;
    }
    try_files $uri $uri/ =404;
}
```

### Rate Limiting

Already included in nginx config:
- 10 requests per minute per IP
- Burst allowance of 5 requests

## Forensics & Investigation

### When Beacon Triggers

```bash
# Find all BEACON_ACTIVATION events
jq 'select(.event_type == "BEACON_ACTIVATION")' logs/honeypot_events.log

# Extract IPs
jq -r 'select(.event_type == "BEACON_ACTIVATION") | .data.ip' logs/honeypot_events.log
```

### Identify Leak Source

```bash
# List all downloads with timestamps
jq 'select(.event_type == "REAL_LAB_DOWNLOAD")' logs/honeypot_events.log \
    | jq -r '[.timestamp, .data.ip, .data.user_agent] | @csv'

# Cross-reference with beacon
# If IP X downloaded at time T and beacon from IP Y at time T+5min,
# likely that person X leaked to person Y
```

### Extract Watermark from Recovered File

```bash
# If you get a copy of leaked files back
grep -r "HONEYPOT_" suspected-lab/
cat suspected-lab/.pkg_id
```

## Troubleshooting

### Containers Won't Start

```bash
# Check logs
docker compose -f docker-compose-honeypot.yml logs

# Verify ports not in use
netstat -tlnp | grep -E '(8080|2222)'
```

### Logger Not Detecting Events

```bash
# Verify log file exists
docker exec invite-only-gate ls -la /var/log/nginx/

# Check if logger can read it
docker exec snoop-detector cat /var/log/nginx/honeypot_access.log

# Restart logger
docker compose -f docker-compose-honeypot.yml restart visitor-logger
```

### Files Not Downloading (404)

```bash
# Verify packages exist
ls -lh invite-html/*.zip

# Should see:
# real-lab.zip
# honeypot-lab.zip

# Rebuild if missing
./scripts/build-lab-packages.sh
```

## Advanced Configuration

### Alert Integration

Add to `logger-script/log_watcher.py`:

```python
import requests

def send_discord_alert(event_type, data):
    webhook_url = "https://discord.com/api/webhooks/YOUR_WEBHOOK"
    requests.post(webhook_url, json={
        "content": f"🚨 {event_type}: {data['ip']}"
    })
```

### Geo-Blocking

Add to `nginx-conf/default.conf`:

```nginx
geo $blocked_country {
    default 1;
    US 0;  # Allow US
    CA 0;  # Allow Canada
}

server {
    if ($blocked_country) {
        return 403;
    }
    # ...
}
```

### Custom Watermarks

Edit `scripts/build-lab-packages.sh`:

```bash
# Add custom identifier
echo "DIST_ID: ${CUSTOM_ID}" > "${HONEYPOT_DIR}/.tracking"
```

## Maintenance

### Log Rotation

```bash
# Add to crontab
0 0 * * * cd /path/to/repo && docker exec snoop-detector \
    sh -c 'mv /logs/honeypot_events.log /logs/honeypot_events.$(date +\%Y\%m\%d).log'
```

### Update Packages

```bash
# After code changes
./scripts/build-lab-packages.sh

# Restart to pick up new files
docker compose -f docker-compose-honeypot.yml restart invite-gate
```

### Backup Logs

```bash
# Export logs
docker cp snoop-detector:/logs ./backup-logs-$(date +%Y%m%d)

# Or use volumes
docker run --rm -v sovereignty-architecture-elevator-pitch-_honeypot_logs:/logs \
    -v $(pwd):/backup alpine tar czf /backup/logs-backup.tar.gz /logs
```

## Stopping the System

```bash
# Stop all containers
./start-honeypot.sh
# Choose option 2 (Stop)

# Or manually
docker compose -f docker-compose-honeypot.yml down

# Remove all data
docker compose -f docker-compose-honeypot.yml down -v
```

## Security Considerations

⚠️ **Important:**
- This is a detection tool, not a defense tool
- Always comply with applicable laws
- Inform users about monitoring in ToS
- Protect the tracking data
- Don't use for entrapment

## Support

For detailed documentation, see:
- [README-HONEYPOT.md](README-HONEYPOT.md) - Complete documentation
- [SECURITY.md](SECURITY.md) - Security policy
- [VAULT_SECURITY_PLAYBOOK.md](VAULT_SECURITY_PLAYBOOK.md) - Advanced security

## Quick Reference Commands

```bash
# Start system
./start-honeypot.sh

# View logs
docker logs -f snoop-detector

# Check events
tail -f logs/honeypot_events.log | jq

# Build packages
./scripts/build-lab-packages.sh

# Stop system
docker compose -f docker-compose-honeypot.yml down

# Full cleanup
docker compose -f docker-compose-honeypot.yml down -v
```

---

**Built with 🔥 by the Strategickhaos Security Team**

*"Every access logged. Every leak traced. Zero tolerance for unauthorized distribution."*
