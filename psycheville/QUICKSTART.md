# PsycheVille Quick Start Guide

Get PsycheVille up and running in **under 5 minutes**.

## What You'll Get

✅ Self-observing infrastructure that monitors your tool usage  
✅ Automated daily reflection reports in Obsidian-compatible markdown  
✅ Insights into which tools you use, what's failing, and what needs improvement

## Prerequisites

- Docker and Docker Compose installed
- Git repository cloned locally

## Step 1: Deploy PsycheVille (2 minutes)

```bash
# Navigate to repository
cd /path/to/Sovereignty-Architecture-Elevator-Pitch-

# Option A: Quick deploy (recommended)
./psycheville/deploy-psycheville.sh deploy --with-samples

# Option B: Manual deploy
docker-compose -f docker-compose.psycheville.yml up -d
```

That's it! PsycheVille is now running.

## Step 2: Verify It's Working (1 minute)

```bash
# Check service status
./psycheville/deploy-psycheville.sh status

# Or manually check
docker-compose -f docker-compose.psycheville.yml ps

# View worker logs
docker-compose -f docker-compose.psycheville.yml logs psycheville-worker
```

You should see output like:
```
PsycheVille Reflection Worker initialized
Running initial reflection on startup...
Processing department: Tools_Refinery
Report saved to .../reflection_2024-11-21_120000.md
```

## Step 3: Check Your First Report (1 minute)

```bash
# List generated reports
ls -la psycheville/obsidian_vault/PsycheVille/Departments/Tools_Refinery/

# View the latest report
cat psycheville/obsidian_vault/PsycheVille/Departments/Tools_Refinery/reflection_*.md
```

You should see a report like:

```markdown
# PsycheVille Daily Reflection - 2024-11-21

## Department: Tools_Refinery

### Observations
Total observations: 22

Pattern breakdown:
- `tool_invoked`: 15 times
- `tool_created`: 4 times
- `tool_failed`: 3 times

### Key Insights
- Tools were invoked 15 times
- Most used tools: deploy-script (4x), test-runner (3x)
- 4 new tools were created
- ⚠️ 3 tool failures detected

### Recommendations
- Consider documenting new tools for team visibility
- Investigate failing tools and improve error handling
```

## Step 4: Generate More Test Data (Optional)

```bash
# Generate additional sample logs
python3 psycheville/test_logging.py

# Wait 60 seconds for PsycheVille to process (or restart worker)
docker-compose -f docker-compose.psycheville.yml restart psycheville-worker

# Check for new report
ls -lht psycheville/obsidian_vault/PsycheVille/Departments/Tools_Refinery/
```

## Step 5: Integrate Your Tools (5 minutes)

Add PsycheVille logging to your existing tools:

### Python Integration

```python
# Add to your Python scripts
from psycheville.psycheville_logger import PsycheVilleLogger

pv = PsycheVilleLogger()

# Log tool events
pv.tool_created('my-tool', creator='your-name')
pv.tool_invoked('my-tool', parameters={'arg': 'value'})
pv.tool_invoked('my-tool', result='success')
```

### Shell Script Integration

```bash
# Add to your shell scripts
LOG_FILE="psycheville/logs/tools_refinery/tools.log"
TOOL_NAME="my-script"

echo "{\"pattern\":\"tool_invoked\",\"tool_name\":\"$TOOL_NAME\",\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}" >> "$LOG_FILE"
```

See [INTEGRATION_EXAMPLE.md](INTEGRATION_EXAMPLE.md) for detailed examples.

---

## Daily Usage

### Morning Routine

```bash
# Check yesterday's reflection
cat psycheville/obsidian_vault/PsycheVille/Departments/Tools_Refinery/reflection_$(date +%Y-%m-%d)*.md

# Or use your favorite markdown viewer
open psycheville/obsidian_vault/PsycheVille/Departments/Tools_Refinery/
```

### Viewing Reports

**Option 1: Command Line**
```bash
cat psycheville/obsidian_vault/PsycheVille/Departments/Tools_Refinery/reflection_*.md
```

**Option 2: Obsidian**
1. Open Obsidian
2. Open vault: `psycheville/obsidian_vault/PsycheVille`
3. Browse to Departments → Tools_Refinery
4. View reflection files

**Option 3: Any Markdown Viewer**
```bash
# VSCode
code psycheville/obsidian_vault/PsycheVille/

# Typora, Marked, etc.
open psycheville/obsidian_vault/PsycheVille/Departments/
```

---

## Configuration

### Change Reflection Schedule

Edit `psycheville/psycheville.yaml`:

```yaml
reflection:
  daily:
    enabled: true
    time: "06:00"  # Change to your preferred time (UTC)
  weekly:
    enabled: true
    day: "Sunday"
    time: "08:00"
```

Restart PsycheVille:
```bash
docker-compose -f docker-compose.psycheville.yml restart
```

### Add Custom Departments

Edit `psycheville/psycheville.yaml` and add a new department:

```yaml
departments:
  My_Custom_Department:
    description: "Custom monitoring"
    log_path: "/app/logs/custom"
    obsidian_path: "/app/obsidian_vault/PsycheVille/Departments/My_Custom"
    observation_patterns:
      - pattern: "my_event"
        extract: ["field1", "field2"]
```

---

## Troubleshooting

### No Reports Generated

**Check worker logs:**
```bash
docker-compose -f docker-compose.psycheville.yml logs psycheville-worker
```

**Common issues:**
- No log files → Run `python3 psycheville/test_logging.py` to generate samples
- Wrong paths → Check `psycheville/psycheville.yaml` configuration
- Service not running → Run `./psycheville/deploy-psycheville.sh deploy`

### Service Won't Start

**Check Docker:**
```bash
docker ps -a | grep psycheville
docker-compose -f docker-compose.psycheville.yml logs
```

**Common issues:**
- Network doesn't exist → Run `docker network create strategickhaos_network`
- Port conflicts → Check if port 9091 is available
- Permission issues → Run `chmod +x psycheville/*.sh`

### Logs Not Being Parsed

**Verify log format:**
```bash
# Check if logs are valid JSON
cat psycheville/logs/tools_refinery/tools.log | python3 -m json.tool
```

**Common issues:**
- Invalid JSON → Use the PsycheVilleLogger class for proper formatting
- Wrong pattern names → Check patterns in `psycheville/psycheville.yaml`

---

## Commands Reference

### Deployment
```bash
./psycheville/deploy-psycheville.sh deploy          # Deploy PsycheVille
./psycheville/deploy-psycheville.sh deploy --with-samples  # Deploy with test data
./psycheville/deploy-psycheville.sh status          # Check status
./psycheville/deploy-psycheville.sh stop            # Stop services
./psycheville/deploy-psycheville.sh logs            # View logs
```

### Docker Compose
```bash
docker-compose -f docker-compose.psycheville.yml up -d      # Start
docker-compose -f docker-compose.psycheville.yml down       # Stop
docker-compose -f docker-compose.psycheville.yml ps         # Status
docker-compose -f docker-compose.psycheville.yml logs -f    # Follow logs
docker-compose -f docker-compose.psycheville.yml restart    # Restart
```

### Testing
```bash
python3 psycheville/test_logging.py                         # Generate sample logs
python3 psycheville/test_reflection_standalone.py           # Test reflection system
```

---

## Next Steps

1. **Review Reports**: Check generated reports each morning
2. **Integrate Tools**: Add PsycheVille logging to your most-used tools
3. **Customize Config**: Adjust reflection schedule and patterns
4. **Add Departments**: Create custom departments for different monitoring needs
5. **Share Insights**: Use reflection reports to guide improvements

---

## Resources

- **Full Documentation**: [README.md](README.md)
- **Integration Examples**: [INTEGRATION_EXAMPLE.md](INTEGRATION_EXAMPLE.md)
- **Configuration Reference**: [psycheville.yaml](psycheville.yaml)
- **Main Repository**: [Sovereignty Architecture](../README.md)

---

## Support

Having issues? Check:
1. Docker logs: `docker-compose -f docker-compose.psycheville.yml logs`
2. Worker status: `./psycheville/deploy-psycheville.sh status`
3. Log files: `ls -la psycheville/logs/tools_refinery/`
4. Generated reports: `ls -la psycheville/obsidian_vault/PsycheVille/Departments/*/`

---

**Built with 🔥 by the Strategickhaos Swarm Intelligence collective**

*"Know thyself - through automated self-observation"*

**Deployment time: ~2 minutes**  
**First insights: Immediate**  
**Ongoing value: Daily**
