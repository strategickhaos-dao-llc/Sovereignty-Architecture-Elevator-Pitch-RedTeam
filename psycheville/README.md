# PsycheVille - Self-Observing Infrastructure

**PsycheVille** is an automated reflection and self-observation system for the Sovereignty Architecture. It monitors tool usage, infrastructure events, and AI agent interactions to generate daily insights and recommendations.

## 🎯 Purpose

PsycheVille answers the question: **"How am I actually using my systems?"**

Instead of manually reviewing logs and metrics, PsycheVille:
- Monitors your Tools Refinery usage patterns
- Detects trends in infrastructure behavior
- Generates automated reflection reports in Obsidian
- Provides actionable insights for system improvements

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Sovereignty Architecture base stack running (optional, but recommended)

### Deploy PsycheVille

```bash
# 1. Ensure the psycheville directory exists with required structure
cd /path/to/Sovereignty-Architecture-Elevator-Pitch-
ls psycheville/

# 2. Start PsycheVille services
docker-compose -f docker-compose.psycheville.yml up -d

# 3. Check logs to verify it's running
docker-compose -f docker-compose.psycheville.yml logs -f psycheville-worker

# 4. Check for generated reports
ls -la psycheville/obsidian_vault/PsycheVille/Departments/Tools_Refinery/
```

### First Reflection

PsycheVille will generate an initial reflection report on startup. Check:

```bash
cat psycheville/obsidian_vault/PsycheVille/Departments/Tools_Refinery/reflection_*.md
```

## 📁 Directory Structure

```
psycheville/
├── psycheville.yaml              # Configuration
├── reflection_worker.py          # Main worker script
├── logs/                         # Log files to monitor
│   └── tools_refinery/          # Tools Refinery logs
└── obsidian_vault/              # Generated reports
    └── PsycheVille/
        └── Departments/
            ├── Tools_Refinery/   # Tool usage reflections
            ├── Infrastructure/   # Infrastructure reflections
            └── AI_Agents/        # AI agent reflections
```

## ⚙️ Configuration

Edit `psycheville/psycheville.yaml` to customize:

### Departments

Define what to observe:

```yaml
departments:
  Tools_Refinery:
    log_path: "/app/logs/tools_refinery"
    observation_patterns:
      - pattern: "tool_created"
        extract: ["tool_name", "timestamp", "creator"]
      - pattern: "tool_invoked"
        extract: ["tool_name", "timestamp", "parameters"]
```

### Reflection Cadence

Control when reports are generated:

```yaml
reflection:
  daily:
    enabled: true
    time: "06:00"  # UTC
  weekly:
    enabled: true
    day: "Sunday"
    time: "08:00"
```

## 🔧 Integration with Tools Refinery

To enable PsycheVille monitoring, add logging to your tool creation/usage:

### Example: Python Tool

```python
import logging
import json
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename='psycheville/logs/tools_refinery/tools.log',
    level=logging.INFO,
    format='%(message)s'
)
logger = logging.getLogger('tools_refinery')

def log_tool_event(event_type, tool_name, **kwargs):
    """Log tool events for PsycheVille monitoring"""
    event = {
        'pattern': event_type,
        'tool_name': tool_name,
        'timestamp': datetime.now().isoformat(),
        **kwargs
    }
    logger.info(json.dumps(event))

# Usage examples
log_tool_event('tool_created', 'my_awesome_tool', creator='user123')
log_tool_event('tool_invoked', 'my_awesome_tool', parameters={'arg1': 'value1'})
log_tool_event('tool_failed', 'my_awesome_tool', error='Connection timeout')
```

### Example: Shell Script

```bash
#!/bin/bash
LOG_FILE="psycheville/logs/tools_refinery/tools.log"

log_tool_event() {
    local pattern=$1
    local tool_name=$2
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    echo "pattern:$pattern tool_name:$tool_name timestamp:$timestamp" >> "$LOG_FILE"
}

# Usage
log_tool_event "tool_created" "backup-script"
log_tool_event "tool_invoked" "backup-script"
```

## 📊 Reading Reports

Reports are generated in Markdown format and saved to:

```
psycheville/obsidian_vault/PsycheVille/Departments/{DepartmentName}/
```

Each report includes:
- **Observations**: Raw data summary
- **Patterns Detected**: Usage trends
- **Key Insights**: Analysis of behavior
- **Recommendations**: Actionable suggestions

### Example Report

```markdown
# PsycheVille Daily Reflection - 2024-11-21

## Department: Tools_Refinery

### Observations
Total observations: 47

Pattern breakdown:
- `tool_invoked`: 32 times
- `tool_created`: 10 times
- `tool_failed`: 5 times

### Patterns Detected
- tool_invoked: 32
- tool_created: 10
- tool_failed: 5

### Key Insights
- Tools were invoked 32 times
- Most used tools: deploy-script (12x), test-runner (8x), linter (7x)
- 10 new tools were created
- ⚠️ 5 tool failures detected

### Recommendations
- Consider documenting new tools for team visibility
- Investigate failing tools and improve error handling

---
*Generated by PsycheVille Self-Observation System*
```

## 🎯 Use Cases

### 1. Understanding Tool Usage
**Question**: "Which tools am I actually using?"
**Answer**: Check daily reflections for usage patterns and frequency

### 2. Identifying Problems
**Question**: "Why are things breaking?"
**Answer**: Review failure patterns and error trends

### 3. Optimizing Workflows
**Question**: "What should I focus on improving?"
**Answer**: Follow recommendations based on usage patterns

### 4. Tracking Evolution
**Question**: "How has my system evolved?"
**Answer**: Compare reports over time to see growth trends

## 🔍 Monitoring

Check PsycheVille health:

```bash
# View worker logs
docker-compose -f docker-compose.psycheville.yml logs -f psycheville-worker

# Check if worker is running
docker ps | grep psycheville-worker

# View recent reports
ls -lt psycheville/obsidian_vault/PsycheVille/Departments/*/

# Check metrics (if enabled)
curl http://localhost:9091/metrics
```

## 🛠️ Troubleshooting

### No Reports Generated

**Problem**: No reflection files appear after deployment

**Solutions**:
1. Check worker logs: `docker-compose -f docker-compose.psycheville.yml logs psycheville-worker`
2. Verify log directory exists: `ls -la psycheville/logs/tools_refinery/`
3. Ensure configuration is valid: `cat psycheville/psycheville.yaml`

### Worker Crashes

**Problem**: PsycheVille worker keeps restarting

**Solutions**:
1. Check Python dependencies: `docker-compose -f docker-compose.psycheville.yml exec psycheville-worker pip list`
2. Verify configuration syntax: `python3 -c "import yaml; yaml.safe_load(open('psycheville/psycheville.yaml'))"`
3. Check permissions on volumes: `ls -la psycheville/`

### Empty Reports

**Problem**: Reports are generated but contain no data

**Solutions**:
1. Verify logs exist: `ls -la psycheville/logs/tools_refinery/*.log`
2. Check log format matches patterns in configuration
3. Add test log entries manually to verify parsing

## 🚀 Advanced Usage

### Custom Departments

Add new observation categories:

```yaml
departments:
  Custom_Service:
    description: "Monitor my custom service"
    log_path: "/app/logs/custom"
    observation_patterns:
      - pattern: "my_event"
        extract: ["field1", "field2"]
    reflection_questions:
      - "What is happening with my service?"
```

### Discord Notifications

Enable Discord integration for insights:

```yaml
integrations:
  discord:
    enabled: true
    webhook_url: "https://discord.com/api/webhooks/YOUR_WEBHOOK"
    notify_on_insights: true
```

### Custom Report Templates

Modify report format in `psycheville.yaml`:

```yaml
reports:
  template: |
    # Custom Report - {{date}}
    
    Department: {{department}}
    
    ## Summary
    {{insights}}
    
    ## Actions
    {{recommendations}}
```

## 📈 Metrics

PsycheVille exposes metrics via Prometheus Pushgateway on port 9091:

- `psycheville_observations_total` - Total observations processed
- `psycheville_reports_generated_total` - Total reports generated
- `psycheville_patterns_detected` - Patterns detected by type

## 🤝 Contributing

To add new observation patterns or departments:

1. Edit `psycheville/psycheville.yaml`
2. Restart the worker: `docker-compose -f docker-compose.psycheville.yml restart`
3. Check logs for confirmation

## 📚 Related Documentation

- [Sovereignty Architecture README](../README.md)
- [Tools Refinery Documentation](../refinory/README.md)
- [Monitoring Stack Setup](../monitoring/README.md)

---

**Built with 🔥 by the Strategickhaos Swarm Intelligence collective**

*"Know thyself - through automated self-observation"*
