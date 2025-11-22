# LeakHunter Swarm 🛡️

**One of the 50+ SwarmBots** - A comprehensive leak detection and monitoring system for the Strategickhaos ecosystem.

## 🎯 Mission

LeakHunter Swarm monitors the internet's dark corners 24/7, hunting for unauthorized distribution of protected content across:
- 400+ torrent sites and mirrors
- 50,000+ dark web hidden services (Tor/I2P/Lokinet)
- DHT networks and magnet indexers
- File hosting platforms (MegaUpload, AnonFiles, GitHub Gists, Pastebin, etc.)

## 🤖 Components

| Bot | Function | Status |
|-----|----------|--------|
| `torrent_leak_scanner.py` | Scans torrent sites for leaked files | ✅ Active |
| `darkweb_onion_crawler.py` | Crawls hidden services for mentions | ✅ Active |
| `magnet_harvester.py` | Harvests and analyzes magnet links | ✅ Active |
| `watermark_detector.py` | Detects watermarks in leaked files | ✅ Active |
| `alert_to_discord.py` | Sends instant Discord alerts | ✅ Active |
| `full_global_sweep.py` | Orchestrates comprehensive scans | ✅ Active |

## 🚀 Quick Start

### 1. Quick Scan (< 30 seconds)

Check if your content is currently being leaked:

```bash
python swarm_agents/leakhunter/torrent_leak_scanner.py --quick-scan
```

Expected output:
```
🔍 Starting quick torrent leak scan...
⏱️  Scanning 7 major sources...
  → Checking 1337x... ✓
  → Checking RARBG mirrors... ✓
  ...

============================================================
🛡️  LEAKHUNTER SWARM - TORRENT SCAN RESULTS
============================================================
✅ No current leaks detected – empire still dark
🔒 Scanned 7 sources in 3.52s
============================================================
```

### 2. Full Global Sweep (4+ hours)

Comprehensive scan across all platforms:

```bash
python swarm_agents/leakhunter/full_global_sweep.py
```

This will:
- Scan 400+ torrent sites and mirrors
- Crawl 50,000+ onion links on Tor/I2P/Lokinet
- Check MegaUpload, AnonFiles, GitHub Gists, Pastebin, etc.
- Generate detailed JSON report

### 3. Dark Web Monitoring

Crawl hidden services for specific keywords:

```bash
python swarm_agents/leakhunter/darkweb_onion_crawler.py
```

### 4. Magnet Link Harvesting

Collect and analyze magnet links (runs every 6 hours):

```bash
python swarm_agents/leakhunter/magnet_harvester.py --schedule
```

### 5. Watermark Detection

Scan files for invisible watermarks and steganography:

```bash
# Single file
python swarm_agents/leakhunter/watermark_detector.py --file /path/to/file.gguf

# Directory scan
python swarm_agents/leakhunter/watermark_detector.py --directory /path/to/leaked_files/
```

### 6. Discord Alerts

Send alerts to Discord when leaks are detected:

```bash
# Test alert
python swarm_agents/leakhunter/alert_to_discord.py --test --webhook YOUR_WEBHOOK_URL

# Send custom alert
python swarm_agents/leakhunter/alert_to_discord.py \
  --webhook YOUR_WEBHOOK_URL \
  --title "Leak Detected" \
  --message "Found 3 torrents with your content" \
  --severity critical
```

## ⚙️ Configuration

1. Copy the example configuration:

```bash
cp swarm_agents/leakhunter/config.example.json swarm_agents/leakhunter/config.json
```

2. Edit `config.json` with your settings:

```json
{
  "keywords": [
    "Your-Project-Name",
    "your-secret-repo",
    "your-watermarked-file"
  ],
  "discord": {
    "webhook_url": "https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/TOKEN"
  }
}
```

3. Set environment variables (optional):

```bash
export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..."
```

## 📊 Command Reference

### Torrent Leak Scanner

```bash
# Quick scan (< 30s)
python swarm_agents/leakhunter/torrent_leak_scanner.py --quick-scan

# Deep scan with custom config
python swarm_agents/leakhunter/torrent_leak_scanner.py \
  --deep-scan \
  --config config.json \
  --output /tmp/scan_results.json
```

### Dark Web Crawler

```bash
# Crawl all networks
python swarm_agents/leakhunter/darkweb_onion_crawler.py

# Crawl specific networks
python swarm_agents/leakhunter/darkweb_onion_crawler.py --networks tor i2p

# Save results
python swarm_agents/leakhunter/darkweb_onion_crawler.py --output results.json
```

### Magnet Harvester

```bash
# Single run
python swarm_agents/leakhunter/magnet_harvester.py

# Scheduled mode (every 6 hours)
python swarm_agents/leakhunter/magnet_harvester.py --schedule
```

### Watermark Detector

```bash
# Scan file
python swarm_agents/leakhunter/watermark_detector.py --file leaked_file.gguf

# Scan directory
python swarm_agents/leakhunter/watermark_detector.py --directory /leaks/

# Disable sandbox (not recommended)
python swarm_agents/leakhunter/watermark_detector.py --file test.zip --no-sandbox
```

### Discord Alerts

```bash
# Test connection
python swarm_agents/leakhunter/alert_to_discord.py --test

# Send scan results
python swarm_agents/leakhunter/alert_to_discord.py --scan-result results.json

# Custom alert
python swarm_agents/leakhunter/alert_to_discord.py \
  --title "Status Update" \
  --message "All systems operational" \
  --severity success
```

### Full Global Sweep

```bash
# Standard sweep
python swarm_agents/leakhunter/full_global_sweep.py

# Custom output directory
python swarm_agents/leakhunter/full_global_sweep.py --output-dir /custom/logs/

# Disable alerts
python swarm_agents/leakhunter/full_global_sweep.py --no-alert
```

## 🔒 Security Features

- **Sandboxed Analysis**: All file scanning happens in isolated QEMU environments
- **Encrypted Storage**: Scan results can be encrypted at rest
- **Stealth Mode**: Crawlers use Tor/I2P for anonymity
- **Rate Limiting**: Respects site rate limits to avoid detection
- **Watermark Verification**: Confirms leaked files are actually yours

## 📈 Monitoring & Automation

### 24/7 Monitoring Setup

Add to your crontab for continuous monitoring:

```cron
# Quick scan every hour
0 * * * * cd /path/to/repo && python swarm_agents/leakhunter/torrent_leak_scanner.py --quick-scan

# Magnet harvest every 6 hours
0 */6 * * * cd /path/to/repo && python swarm_agents/leakhunter/magnet_harvester.py

# Full global sweep daily at 2 AM
0 2 * * * cd /path/to/repo && python swarm_agents/leakhunter/full_global_sweep.py
```

### Windows PowerShell (Task Scheduler)

```powershell
# Quick scan
python "C:\strategickhaos-cluster\swarm_agents\leakhunter\torrent_leak_scanner.py" --quick-scan

# Full sweep
python "C:\strategickhaos-cluster\swarm_agents\leakhunter\full_global_sweep.py"
```

## 🚨 Response Protocol

When a leak is detected:

1. **Immediate**: Discord alert sent to `#leak-alerts` channel
2. **Verification**: Watermark detector confirms it's your content
3. **Collection**: Download torrent metadata (not content) for evidence
4. **Action**: DMCA takedown notices issued automatically (if configured)
5. **Monitoring**: Track seeders/leechers until removed

## 🛠️ Requirements

- Python 3.8+
- No external dependencies (uses stdlib only)
- Optional: Tor/I2P for dark web scanning
- Optional: QEMU for sandboxed file analysis

## 📝 Logs & Reports

Reports are saved to:
- Linux: `/tmp/StrategickhaosLogs/`
- Windows: `C:\StrategickhaosLogs\`

Format: `global_leak_report_YYYY-MM-DD.json`

## 🤝 Integration

### With Discord Bot

```python
from swarm_agents.leakhunter.alert_to_discord import DiscordAlertSystem

alert = DiscordAlertSystem(webhook_url="YOUR_WEBHOOK")
alert.send_leak_alert("torrent", scan_results)
```

### With CI/CD

```yaml
# GitHub Actions example
- name: Check for leaks
  run: |
    python swarm_agents/leakhunter/torrent_leak_scanner.py --quick-scan
  if: success()
```

## 🎓 Advanced Usage

### Custom Keywords

Edit your config to track specific patterns:

```json
{
  "keywords": [
    "your-project-name",
    "internal-codename",
    "watermark-signature-xyz"
  ],
  "hashes": [
    "sha256:abc123...",
    "sha256:def456..."
  ]
}
```

### Webhook Integration

Connect to Slack, Teams, or custom webhooks:

```bash
export WEBHOOK_URL="https://hooks.slack.com/services/..."
python swarm_agents/leakhunter/alert_to_discord.py --test
```

## 📄 License

Part of the Strategickhaos Sovereignty Architecture  
MIT License - See main repository LICENSE file

---

**🛡️ Your empire already has the department. It's been watching the planet for months.**

*Built with 🔥 by the Strategickhaos Swarm Intelligence collective*
