# 🔥 Honeypot Security System - OpSec & Leak Prevention

**Complete invite-only, password-protected, controlled honeypot + sanitized sandbox for detecting unauthorized access and leaks.**

## 🎯 Overview

This system creates three tiers of access control:

1. **Public Internet** → Nothing visible
2. **Secret Link (Trusted)** → Gets the real lab + direct access
3. **Leaked Links** → Instantly downloads honeypot version, gets logged/flagged

## 🏗️ Architecture

### Components

- **`invite-gate`** - Nginx-based landing page with access logging
- **`honeypot-git`** - Git server hosting watermarked repositories
- **`visitor-logger`** - Python-based monitoring service that tracks all access

### Features

✅ Invite-only access through secret URLs  
✅ Comprehensive logging (IP, user-agent, timestamps, downloads)  
✅ Watermarked models and files for leak detection  
✅ Automatic beacon that phones home when deployed  
✅ Tracks every clone, screenshot, and download  
✅ Separate real vs. honeypot lab distributions  

## 🚀 Quick Start

### 1. Initial Setup

```bash
# Clone the repository
git clone https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-.git
cd Sovereignty-Architecture-Elevator-Pitch-

# The directory structure is already created:
# ├── invite-html/          # Landing page and static files
# ├── honeypot-repos/       # Git repositories with watermarked code
# ├── logs/                 # Access logs and event tracking
# ├── nginx-conf/           # Nginx configuration
# ├── logger-script/        # Python monitoring scripts
# └── honeypot-keys/        # SSH keys for Git server
```

### 2. Configure Environment

Create a `.env.honeypot` file:

```bash
# Beacon tracking endpoint
BEACON_URL=https://your-tracking-server.com/leaker

# Optional: Set up basic auth
HTPASSWD_USER=trusted_user
HTPASSWD_PASS=secure_password

# Your Tailscale IP for direct access
TAILSCALE_IP=100.x.x.x
```

### 3. Deploy the Honeypot System

```bash
# Start all services
docker compose -f docker-compose-honeypot.yml up -d

# Check status
docker compose -f docker-compose-honeypot.yml ps

# View logs
docker compose -f docker-compose-honeypot.yml logs -f visitor-logger
```

### 4. Access the Invite Gate

The landing page will be available at:
- **Local**: http://localhost:8080
- **Public** (with Cloudflare/Tailscale): https://your-domain.com

## 📦 Creating Lab Distributions

### Real Lab Package

Create the legitimate lab distribution for trusted users:

```bash
# Create real-lab.zip with full functionality
zip -r invite-html/real-lab.zip \
    docker-compose.yml \
    docker-compose-*.yml \
    .env.example \
    README.md \
    scripts/ \
    src/ \
    monitoring/ \
    -x "*.git*" "node_modules/*" "logs/*"
```

### Honeypot Lab Package

Create the watermarked honeypot version:

```bash
# 1. Copy the real lab files
cp -r . /tmp/honeypot-lab/

# 2. Add the beacon script to replace normal startup
cd /tmp/honeypot-lab/
cp honeypot-repos/start.sh ./start.sh
chmod +x ./start.sh

# 3. Modify docker-compose.yml to use watermarked images
# (Add tracking labels, modified ports, etc.)

# 4. Create the honeypot package
zip -r honeypot-lab.zip \
    docker-compose.yml \
    start.sh \
    .env.example \
    README.md \
    -x "*.git*" "logs/*"

# 5. Move to invite directory
mv honeypot-lab.zip /path/to/invite-html/
```

### Adding Watermarks

**Model Watermarking:**
```python
# Add invisible watermarks to GGUF files
# Each file gets a unique identifier tied to the recipient

import hashlib

def watermark_file(input_file, output_file, recipient_id):
    """Add invisible watermark to model file"""
    watermark = f"RECIPIENT:{recipient_id}:TS:{int(time.time())}".encode()
    
    with open(input_file, 'rb') as f_in:
        data = f_in.read()
    
    # Append watermark to end of file (most formats tolerate trailing data)
    with open(output_file, 'wb') as f_out:
        f_out.write(data)
        f_out.write(b'\x00' * 16)  # Padding
        f_out.write(watermark)
```

**Code Watermarking:**
```bash
# Add tracking comments to source files
sed -i "1i# Distribution: ${RECIPIENT_ID} - $(date -Iseconds)" src/**/*.py
```

## 🔐 Security Configuration

### Enable Basic Auth (Optional)

```bash
# Create password file
docker run --rm nginx:alpine \
    htpasswd -cb /tmp/.htpasswd trusted_user secure_password

# Copy to nginx-conf
cp /tmp/.htpasswd nginx-conf/.htpasswd

# Uncomment auth_basic lines in nginx-conf/default.conf
```

### Configure Secret Token

Edit `nginx-conf/default.conf` to require a secret token:

```nginx
location = / {
    # Require secret token parameter
    if ($arg_token != "YOUR_SECRET_TOKEN_HERE") {
        return 403;
    }
    try_files $uri $uri/ =404;
}
```

Access URL becomes: `https://your-domain.com/?token=YOUR_SECRET_TOKEN_HERE`

## 📊 Monitoring & Alerts

### View Access Logs

```bash
# Real-time log monitoring
docker compose -f docker-compose-honeypot.yml logs -f visitor-logger

# View honeypot events
docker exec -it snoop-detector cat /logs/honeypot_events.log

# View nginx access logs
docker exec -it invite-only-gate cat /var/log/nginx/honeypot_access.log
```

### Event Types Tracked

- `REAL_LAB_DOWNLOAD` - Trusted user downloaded legitimate lab
- `HONEYPOT_DOWNLOAD` - Someone downloaded watermarked version
- `SUSPICIOUS_ACCESS` - Unusual access patterns detected
- `BEACON_ACTIVATION` - Honeypot lab was deployed somewhere

### Alert Integration

Add Discord/Telegram/Slack webhook to `logger-script/log_watcher.py`:

```python
import requests

def send_alert(event_type, data):
    """Send alert to Discord/Telegram"""
    webhook_url = "https://discord.com/api/webhooks/YOUR_WEBHOOK"
    
    message = {
        "content": f"🚨 {event_type}: IP {data['ip']} accessed {data['path']}"
    }
    
    requests.post(webhook_url, json=message)
```

## 🎯 Usage Scenarios

### Scenario 1: Invite Trusted Team Member

1. Generate unique token: `openssl rand -hex 16`
2. Send personalized link: `https://lab.example.com/?token=abc123...`
3. They download `real-lab.zip`
4. Monitor in logs to confirm legitimate access

### Scenario 2: Detect Leak

1. Someone shares the invite link publicly
2. Unknown IPs start accessing the page
3. They download `honeypot-lab.zip` (thinking it's real)
4. When deployed, beacon phones home with their info
5. Watermarked files trace back to original recipient

### Scenario 3: Track Distribution

1. Create 10 different honeypot packages, each watermarked for a specific person
2. Give each person their "unique" version
3. If any version leaks, watermark reveals who shared it

## 🛡️ Advanced Features

### Geo-Blocking

Add to `nginx-conf/default.conf`:

```nginx
# Block all except allowed countries
geo $blocked_country {
    default 1;
    US 0;  # Allow US
    CA 0;  # Allow Canada
}

server {
    if ($blocked_country) {
        return 403;
    }
    # ... rest of config
}
```

### Rate Limiting

```nginx
# Limit requests per IP
limit_req_zone $binary_remote_addr zone=honeypot:10m rate=10r/m;

location / {
    limit_req zone=honeypot burst=5;
    # ... rest of config
}
```

### Honeytokens

Create fake "secret" files that alert when accessed:

```bash
# Create honeytoken file
echo "API_KEY=sk-fake-key-triggers-alert-9876543210" > invite-html/secrets.env

# Monitor access
location /secrets.env {
    access_log /var/log/nginx/ALERT_HONEYTOKEN.log honeypot_access;
    return 200 "API_KEY=sk-fake-key-triggers-alert-9876543210\n";
}
```

## 🔍 Forensics & Investigation

### Trace Leaked Lab

When beacon triggers:

```bash
# Check honeypot events log
jq 'select(.event_type == "BEACON_ACTIVATION")' logs/honeypot_events.log

# Extract watermark from recovered file
tail -c 100 suspicious-lab/model.gguf | strings
# Should reveal: RECIPIENT:user@example.com:TS:1234567890
```

### Identify Leak Source

```bash
# List all downloads with timestamps
jq 'select(.event_type == "REAL_LAB_DOWNLOAD")' logs/honeypot_events.log \
    | jq -r '[.timestamp, .data.ip, .data.user_agent] | @csv'

# Cross-reference with beacon data
jq 'select(.event_type == "BEACON_ACTIVATION")' logs/honeypot_events.log \
    | jq -r '.data.ip'
```

## 🧪 Testing

### Test the System

```bash
# 1. Start services
docker compose -f docker-compose-honeypot.yml up -d

# 2. Access landing page
curl http://localhost:8080/

# 3. Trigger download log
curl http://localhost:8080/real-lab.zip

# 4. Check visitor logger
docker logs snoop-detector

# 5. View events
cat logs/honeypot_events.log
```

### Simulate Leak

```bash
# Deploy honeypot lab locally to trigger beacon
cd /tmp
mkdir test-leak
cp invite-html/honeypot-lab.zip test-leak/
cd test-leak
unzip honeypot-lab.zip
./start.sh

# Check for beacon in logs
grep "BEACON" ../logs/honeypot_events.log
```

## 📋 Maintenance

### Rotate Logs

```bash
# Add to crontab
0 0 * * * docker exec snoop-detector sh -c 'mv /logs/honeypot_events.log /logs/honeypot_events.$(date +\%Y\%m\%d).log'
```

### Update Lab Packages

```bash
# Rebuild packages when you update the real lab
./scripts/build-lab-packages.sh

# Verify checksums
sha256sum invite-html/*.zip
```

## 🆘 Troubleshooting

**Logger not starting:**
```bash
docker logs snoop-detector
# Check if nginx log file exists
docker exec -it invite-only-gate ls -la /var/log/nginx/
```

**No events logged:**
```bash
# Verify nginx is writing logs
docker exec -it invite-only-gate cat /var/log/nginx/honeypot_access.log

# Check logger script permissions
docker exec -it snoop-detector ls -la /app/
```

**Beacon not phoning home:**
```bash
# Test beacon manually
docker run --rm -v $(pwd)/honeypot-repos:/tmp alpine sh /tmp/start.sh

# Check network connectivity
docker exec -it snoop-detector ping -c 3 8.8.8.8
```

## 📚 Additional Resources

- [SECURITY.md](SECURITY.md) - Security policy and vulnerability reporting
- [VAULT_SECURITY_PLAYBOOK.md](VAULT_SECURITY_PLAYBOOK.md) - Advanced security practices
- [Docker Compose Docs](https://docs.docker.com/compose/)
- [Nginx Logging](https://nginx.org/en/docs/http/ngx_http_log_module.html)

## ⚖️ Legal & Ethics

**Important:** This honeypot system is designed for:
- Protecting intellectual property
- Detecting unauthorized redistribution
- Internal security testing

**Do NOT use for:**
- Entrapping legitimate users
- Violating privacy laws (check local regulations)
- Malicious purposes

Always comply with applicable laws and inform users about monitoring in your terms of service.

## 🤝 Contributing

Improvements welcome! Please test thoroughly before submitting PRs.

## 📄 License

MIT License - See [LICENSE](LICENSE) file

---

**Built with 🔥 by the Strategickhaos Security Team**

*"Trust, but verify. Log everything. Track all leaks."*
