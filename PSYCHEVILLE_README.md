# PsycheVille: Self-Observing Infrastructure Architecture

**Zero-cost observability with AI-powered insights**

## 🎯 Quick Start (5 Minutes)

```bash
# 1. Run the quick start script
./psycheville-quickstart.sh

# 2. Generate sample logs (optional)
python3 psycheville_sample_logger.py --log-dir ~/.psycheville/logs --events 100

# 3. Run reflection worker
python3 psycheville_reflection_worker.py

# 4. Check your Obsidian vault
ls ~/Obsidian/PsycheVille/Daily\ Reports/
```

## 📚 What Is PsycheVille?

PsycheVille is a self-observing infrastructure system that provides:

- 📊 **Distributed Logging** - JSONL format per department
- 🤖 **AI-Powered Analytics** - LLM-driven insights using Ollama
- 📝 **Automated Reporting** - Daily/weekly Obsidian notes
- 🔍 **Pattern Detection** - Anomaly identification and trend analysis
- 💰 **Zero Cost** - $0/year vs $50k-500k/year for enterprise tools

## 🏗️ Architecture

```
Departments → JSONL Logs → Reflection Worker → LLM Analysis → Obsidian Notes
```

### Components

1. **Department Logs** (`/var/log/psycheville/*.jsonl`)
   - Tools Refinery
   - Sovereign AI Lab
   - RF Sensor Lab
   - Quantum Emulation Lab
   - Cloud OS Development
   - Valoryield Engine

2. **Reflection Worker** (`psycheville_reflection_worker.py`)
   - Collects events from all departments
   - Calculates metrics and detects anomalies
   - Queries Ollama LLM for insights
   - Generates Obsidian markdown reports

3. **Configuration** (`psycheville.yaml`)
   - Department definitions
   - Metric thresholds
   - LLM settings
   - Output preferences

4. **Output** (Obsidian vault)
   - Daily department reports
   - Weekly synthesis
   - Dashboard overview

## 📦 Installation

### Requirements

- Python 3.8+
- PyYAML (`pip install pyyaml`)
- Ollama (optional, for AI analysis)
- Docker (optional, for containerized deployment)

### Setup

```bash
# Install Python dependencies
pip install pyyaml

# Create log directories
sudo mkdir -p /var/log/psycheville
sudo chown $USER:$USER /var/log/psycheville

# Create Obsidian vault
mkdir -p ~/Obsidian/PsycheVille/{Daily\ Reports,Weekly\ Synthesis}

# Optional: Install Ollama for AI analysis
# Visit https://ollama.ai/ for installation instructions
ollama pull llama3:latest
```

## 🚀 Usage

### Manual Execution

```bash
# Run once
python3 psycheville_reflection_worker.py

# With custom config
python3 psycheville_reflection_worker.py --config /path/to/config.yaml

# Verbose mode
python3 psycheville_reflection_worker.py --verbose
```

### Docker Deployment

```bash
# Start scheduled reflection (hourly)
docker-compose -f docker-compose.psycheville.yml up -d

# View logs
docker-compose -f docker-compose.psycheville.yml logs -f

# Stop services
docker-compose -f docker-compose.psycheville.yml down
```

### Generate Sample Data

```bash
# Generate 100 events per department
python3 psycheville_sample_logger.py

# Custom log directory
python3 psycheville_sample_logger.py --log-dir ~/.psycheville/logs --events 200
```

## 📊 Example Output

### Daily Report

```markdown
# Tools Refinery Daily Report
**Date:** 2025-11-21

## 📊 Metrics Summary
- **Total Events:** 1,247
- **Error Rate:** 0.8%
- **Avg Response Time:** 67ms

### Event Breakdown
- **endpoint_called:** 1,120 (89.8%)
- **error:** 10 (0.8%)
- **health_check:** 117 (9.4%)

## 🤖 AI Analysis

### Key Insights
1. High usage pattern detected on /api/v1/tools/list endpoint
2. 41 unused endpoints identified
3. Response time spike during 2-4 PM window

### Recommendations
- [ ] Implement WebSocket updates for real-time data
- [ ] Archive unused endpoints
- [ ] Optimize batch processing schedule
```

## ⚙️ Configuration

Edit `psycheville.yaml` to customize:

```yaml
psycheville:
  departments:
    your_department:
      name: "Your Department"
      log_file: "/var/log/psycheville/your_department.jsonl"
      metrics:
        - custom_metric_1
        - custom_metric_2
      thresholds:
        max_error_rate_percent: 1.0
  
  reflection_worker:
    schedule: "0 * * * *"  # Hourly
    llm_model: "llama3:latest"
    output_dir: "/home/user/Obsidian/PsycheVille"
```

## 🔧 Integration

### Logging to PsycheVille

From your application:

```python
import json
from datetime import datetime

def log_event(department: str, event_type: str, metadata: dict):
    with open(f'/var/log/psycheville/{department}.jsonl', 'a') as f:
        event = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'department': department,
            'event_type': event_type,
            'metadata': metadata
        }
        f.write(json.dumps(event) + '\n')

# Usage
log_event('tools_refinery', 'endpoint_called', {
    'endpoint': '/api/v1/tools/list',
    'response_time_ms': 45
})
```

### Bash Logging

```bash
#!/bin/bash
DEPARTMENT="cloud_os"
LOG_FILE="/var/log/psycheville/${DEPARTMENT}.jsonl"

log_event() {
    local event_type="$1"
    local metadata="$2"
    
    echo "{\"timestamp\": \"$(date -u +"%Y-%m-%dT%H:%M:%SZ")\", \"department\": \"${DEPARTMENT}\", \"event_type\": \"${event_type}\", \"metadata\": ${metadata}}" >> "$LOG_FILE"
}

# Usage
log_event "container_start" '{"container": "api-server", "status": "success"}'
```

## 📈 Cost Comparison

| Feature | Enterprise Tools | PsycheVille |
|---------|-----------------|-------------|
| **Annual Cost** | $50k - $500k | $0 |
| **Per-User** | $100-200/mo | $0 |
| **Data Ingestion** | $0.10-0.25/GB | $0 |
| **AI Insights** | $$$$$ | Free (Ollama) |
| **Vendor Lock-in** | High | Zero |

**Total Savings: 1,000× - ∞×**

## 🎓 Learn More

- **Full Documentation**: [PSYCHEVILLE_COMPARATIVE_ANALYSIS.md](PSYCHEVILLE_COMPARATIVE_ANALYSIS.md)
- **Main Repository**: [README.md](README.md)

## 🤝 Contributing

PsycheVille is part of the Sovereignty Architecture project. Contributions welcome!

1. Add new department templates
2. Improve LLM prompts
3. Create custom metrics
4. Add alerting integrations
5. Build visualization dashboards

## 📄 License

MIT License - See [LICENSE](LICENSE)

---

**Built with 🔥 by the Strategickhaos Swarm Intelligence collective**

*"Zero-cost observability, infinite insights, full sovereignty."* 🚀
