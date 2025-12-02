# LeakHunter Swarm - Deployment Guide

This guide covers deploying LeakHunter Swarm for 24/7 leak monitoring.

## 🚀 Quick Deployment

### Windows (Nitro Lyra Node)

1. **PowerShell Quick Scan**
   ```powershell
   cd C:\strategickhaos-cluster
   python swarm_agents\leakhunter\torrent_leak_scanner.py --quick-scan
   ```

2. **Using PowerShell Launcher**
   ```powershell
   .\swarm_agents\leakhunter\leakhunter.ps1 quick-scan
   ```

### Linux/Unix/macOS

1. **Direct Command**
   ```bash
   python3 swarm_agents/leakhunter/torrent_leak_scanner.py --quick-scan
   ```

2. **Using Shell Launcher**
   ```bash
   ./swarm_agents/leakhunter/leakhunter.sh quick-scan
   ```

## 🔧 Configuration

### 1. Create Configuration File

```bash
# Copy example config
cp swarm_agents/leakhunter/config.example.json swarm_agents/leakhunter/config.json

# Edit with your settings
nano swarm_agents/leakhunter/config.json  # or your preferred editor
```

### 2. Configure Discord Webhooks

Get your Discord webhook URL:
1. Go to your Discord server
2. Navigate to Server Settings → Integrations → Webhooks
3. Create a new webhook for your `#leak-alerts` channel
4. Copy the webhook URL

Add to config:
```json
{
  "discord": {
    "webhook_url": "https://discord.com/api/webhooks/YOUR_ID/YOUR_TOKEN",
    "alert_role": "@here",
    "leak_alerts_channel": "leak-alerts"
  }
}
```

Or set environment variable:
```bash
export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..."
```

### 3. Add Your Keywords

Edit config.json:
```json
{
  "keywords": [
    "YourProjectName",
    "your-repo-name",
    "your-secret-codename"
  ],
  "folder_patterns": [
    "your-folder-structure",
    "sensitive-directory"
  ]
}
```

## 📅 Automated Monitoring

### Linux/Unix - Cron Jobs

Edit crontab:
```bash
crontab -e
```

Add these lines:
```cron
# Quick scan every hour
0 * * * * cd /path/to/repo && python3 swarm_agents/leakhunter/torrent_leak_scanner.py --quick-scan --config swarm_agents/leakhunter/config.json

# Magnet harvest every 6 hours
0 */6 * * * cd /path/to/repo && python3 swarm_agents/leakhunter/magnet_harvester.py --config swarm_agents/leakhunter/config.json

# Dark web crawl every 12 hours
0 */12 * * * cd /path/to/repo && python3 swarm_agents/leakhunter/darkweb_onion_crawler.py --config swarm_agents/leakhunter/config.json

# Full global sweep weekly (Sunday 2 AM)
0 2 * * 0 cd /path/to/repo && python3 swarm_agents/leakhunter/full_global_sweep.py --config swarm_agents/leakhunter/config.json
```

### Windows - Task Scheduler

Create scheduled tasks using PowerShell:

```powershell
# Quick scan every hour
$action = New-ScheduledTaskAction -Execute "python3" -Argument "swarm_agents\leakhunter\torrent_leak_scanner.py --quick-scan"
$trigger = New-ScheduledTaskTrigger -Once -At 12am -RepetitionInterval (New-TimeSpan -Hours 1)
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "LeakHunter-QuickScan" -Description "LeakHunter quick scan every hour"

# Full global sweep weekly
$action = New-ScheduledTaskAction -Execute "python3" -Argument "swarm_agents\leakhunter\full_global_sweep.py"
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At 2am
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "LeakHunter-GlobalSweep" -Description "LeakHunter weekly global sweep"
```

## 🐳 Docker Deployment

### Dockerfile

Create `Dockerfile.leakhunter`:
```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Copy LeakHunter files
COPY swarm_agents/leakhunter/ /app/

# Create config volume mount point
VOLUME ["/config", "/logs"]

# Default command (can be overridden)
CMD ["python3", "torrent_leak_scanner.py", "--quick-scan", "--config", "/config/config.json"]
```

### Build and Run

```bash
# Build image
docker build -f Dockerfile.leakhunter -t leakhunter:latest .

# Run quick scan
docker run --rm \
  -v $(pwd)/swarm_agents/leakhunter/config.json:/config/config.json \
  leakhunter:latest

# Run scheduled magnet harvester
docker run -d --name leakhunter-magnet \
  -v $(pwd)/swarm_agents/leakhunter/config.json:/config/config.json \
  leakhunter:latest \
  python3 magnet_harvester.py --schedule --config /config/config.json
```

## 🔄 Kubernetes Deployment

### CronJob Example

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: leakhunter-quick-scan
  namespace: security
spec:
  schedule: "0 * * * *"  # Every hour
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: leakhunter
            image: leakhunter:latest
            command:
            - python3
            - torrent_leak_scanner.py
            - --quick-scan
            - --config
            - /config/config.json
            volumeMounts:
            - name: config
              mountPath: /config
            env:
            - name: DISCORD_WEBHOOK_URL
              valueFrom:
                secretKeyRef:
                  name: leakhunter-secrets
                  key: webhook-url
          volumes:
          - name: config
            configMap:
              name: leakhunter-config
          restartPolicy: OnFailure
```

## 📊 Monitoring Dashboard

### Prometheus Metrics (Future Enhancement)

```python
# Add to each scanner for metrics export
from prometheus_client import Counter, Histogram

scans_total = Counter('leakhunter_scans_total', 'Total scans performed')
leaks_found = Counter('leakhunter_leaks_found', 'Total leaks detected')
scan_duration = Histogram('leakhunter_scan_duration_seconds', 'Scan duration')
```

## 🚨 Alert Configuration

### Alert Levels

Configure different alert severities:

```json
{
  "alerts": {
    "critical": {
      "channels": ["#leak-alerts", "#security-ops"],
      "mention": "@security-team"
    },
    "warning": {
      "channels": ["#leak-alerts"],
      "mention": "@here"
    },
    "info": {
      "channels": ["#leak-alerts"],
      "mention": null
    }
  }
}
```

## 🔐 Security Recommendations

1. **Config File**: Store config.json outside the repository with proper permissions
   ```bash
   chmod 600 swarm_agents/leakhunter/config.json
   ```

2. **Webhook Security**: Use environment variables instead of hardcoding
   ```bash
   export DISCORD_WEBHOOK_URL="..."
   unset HISTFILE  # Prevent webhook from being saved in history
   ```

3. **Log Rotation**: Implement log rotation for report directories
   ```bash
   # Add to logrotate.d
   /tmp/StrategickhaosLogs/*.json {
       weekly
       rotate 12
       compress
       missingok
       notifempty
   }
   ```

4. **Network Security**: If running on a server, restrict outbound connections to only necessary services

## 📈 Performance Tuning

### For High-Volume Monitoring

Adjust scan frequencies based on your threat model:

```json
{
  "scan_settings": {
    "torrent": {
      "quick_scan_interval_minutes": 30,
      "deep_scan_interval_hours": 24
    },
    "darkweb": {
      "crawl_interval_hours": 12,
      "max_concurrent_requests": 10
    },
    "magnet": {
      "check_interval_hours": 3,
      "batch_size": 100
    }
  }
}
```

## 🆘 Troubleshooting

### Common Issues

**1. Python not found**
```bash
# Check Python installation
which python3
python3 --version

# Should be Python 3.8+
```

**2. Discord webhook not working**
```bash
# Test webhook manually
curl -X POST "$DISCORD_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{"content":"Test message"}'
```

**3. Permission denied errors**
```bash
# Make scripts executable
chmod +x swarm_agents/leakhunter/*.py
chmod +x swarm_agents/leakhunter/*.sh
```

**4. Module import errors**
```bash
# All modules use only Python stdlib - no pip install needed
# Just ensure Python 3.8+ is installed
```

## 📞 Support

- **Documentation**: See [README.md](README.md)
- **Issues**: Report on GitHub Issues
- **Discord**: Join #security-ops channel

---

**🛡️ Your empire's watchers are now deployed and vigilant.**

*Built with 🔥 by the Strategickhaos Swarm Intelligence collective*
