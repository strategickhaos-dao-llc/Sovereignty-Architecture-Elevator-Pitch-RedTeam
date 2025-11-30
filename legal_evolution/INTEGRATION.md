# Legal Evolution Engine Integration Guide

This document describes how to integrate the Legal Synthesizer Evolution Engine (LSEE) with the broader Strategickhaos Sovereignty Architecture ecosystem.

## 🔗 Integration Points

### 1. Obsidian Vault / Knowledge Base

#### SOP Export Workflow

1. Run LSEE to generate evolved strategies:
   ```bash
   cd legal_evolution
   python3 legal_evolution_synthesizer.py
   ```

2. Extract best strategies by type:
   ```bash
   python3 example_usage.py
   # Choose option 5
   ```

3. Export to your Obsidian vault:
   ```bash
   # Example for background checks
   cat legal_evolution_ledger.jsonl | \
     jq -r 'select(.strategy_type=="background_check" and .compliant==true) | 
            select(.fitness == (map(select(.strategy_type=="background_check" and .compliant==true).fitness) | max)) | 
            .snippet' > ~/vault/SOPs/Background_Check_LSEE_GenX.md
   ```

#### Audit Trail Documentation

Add to your investigation ledger:
```markdown
## Compliance Validation

Strategy: Background Check Procedure v2.0
Generated: 2025-11-21T03:06:35Z
Evolution: Generation 5
Fitness Score: 100.0
Legal Codes Checked: 30
Ledger Reference: legal_evolution_ledger.jsonl:strategy_1763694746.125102_4137

✅ Validated against FCRA, CFAA, SCA, Wiretap Act, and 26 additional statutes.
```

### 2. Discord Command Integration

Create a Discord bot command to archive AI conversations:

```python
# In your discord_commands.py
from legal_evolution.legal_evolution_synthesizer import ExternalConversationArchive

@bot.command(name='archive_ai')
async def archive_conversation(ctx, url: str, *, summary: str):
    """Archive an external AI conversation for compliance tracking."""
    archive = ExternalConversationArchive()
    archive.archive_conversation(
        source_url=url,
        summary=summary,
        conversation_type="operational_discussion",
        tags=["discord", "archived"]
    )
    await ctx.send(f"✅ Archived conversation: {url}")
```

Usage:
```
/archive_ai https://claude.ai/share/abc123 Discussed OSINT workflow improvements
```

### 3. GitHub Actions / CI/CD

#### Pre-deployment Compliance Check

Add to `.github/workflows/compliance-check.yml`:

```yaml
name: Legal Compliance Check

on:
  pull_request:
    paths:
      - 'legal/**'
      - 'legal_evolution/**'

jobs:
  compliance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run LSEE Validation
        run: |
          cd legal_evolution
          python3 legal_evolution_synthesizer.py
          
      - name: Check Compliance Rate
        run: |
          COMPLIANT=$(jq -r 'select(.compliant==true) | .compliant' legal_evolution_ledger.jsonl | wc -l)
          TOTAL=$(wc -l < legal_evolution_ledger.jsonl)
          RATE=$(echo "scale=2; $COMPLIANT / $TOTAL * 100" | bc)
          echo "Compliance Rate: $RATE%"
          
          if (( $(echo "$RATE < 80" | bc -l) )); then
            echo "❌ Compliance rate below 80%"
            exit 1
          fi
```

### 4. Agent Workflow Integration

#### Strategy Retrieval for Autonomous Agents

```python
# worker_agent.py
import json
from pathlib import Path

class LegalStrategyRetriever:
    """Retrieve best legal strategies for agent operations."""
    
    def __init__(self, ledger_path: Path = Path("legal_evolution/legal_evolution_ledger.jsonl")):
        self.ledger_path = ledger_path
        self._cache = {}
        self._load_best_strategies()
    
    def _load_best_strategies(self):
        """Load best strategies by type from ledger."""
        if not self.ledger_path.exists():
            return
        
        strategies_by_type = {}
        with open(self.ledger_path, 'r') as f:
            for line in f:
                entry = json.loads(line)
                if not entry.get('compliant', False):
                    continue
                
                stype = entry.get('strategy_type', 'unknown')
                if stype not in strategies_by_type or \
                   entry.get('fitness', 0) > strategies_by_type[stype].get('fitness', 0):
                    strategies_by_type[stype] = entry
        
        self._cache = strategies_by_type
    
    def get_strategy(self, strategy_type: str) -> dict:
        """Get best strategy for a given type."""
        return self._cache.get(strategy_type, {})
    
    def get_guidance(self, task_type: str) -> str:
        """Get compliance guidance for a task."""
        strategy = self.get_strategy(task_type)
        if not strategy:
            return "No guidance available. Consult licensed professional."
        
        return f"""
Strategy: {task_type.title()}
Fitness: {strategy.get('fitness', 0):.2f}/100.0
Generation: {strategy.get('generation', 0)}

Guidance:
{strategy.get('snippet', 'N/A')}

⚠️  This is heuristic guidance only. Verify with qualified counsel.
"""

# Usage in agent
def osint_task(agent):
    retriever = LegalStrategyRetriever()
    guidance = retriever.get_guidance('osint')
    
    agent.log(f"Legal Guidance:\n{guidance}")
    
    # Agent proceeds with task using guidance constraints
    agent.execute_with_constraints(guidance)
```

### 5. Refinory Integration

The LSEE can feed strategies to the Refinory orchestrator:

```python
# In refinory/orchestrator.py
from legal_evolution.legal_evolution_synthesizer import (
    LegalEvolutionEngine,
    LegalComplianceJudge,
    US_CODES
)

class RefinoryOrchestrator:
    def __init__(self):
        self.legal_judge = LegalComplianceJudge(US_CODES)
        # ... other init
    
    def validate_operation(self, operation_description: str, op_type: str):
        """Validate an operation against legal constraints."""
        from legal_evolution.legal_evolution_synthesizer import LegalStrategy
        
        strategy = LegalStrategy(
            approach=operation_description,
            strategy_type=op_type
        )
        
        self.legal_judge.verify_strategy(strategy)
        
        if not strategy.compliance_verified:
            violations = strategy.verification_ledger[-1].get('violations', [])
            raise ValueError(f"Operation fails compliance: {violations}")
        
        return strategy.fitness
```

### 6. Monitoring Dashboard

Create a simple web dashboard to visualize LSEE metrics:

```python
# dashboard.py
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import json
from pathlib import Path

app = FastAPI()

@app.get("/legal/dashboard")
def legal_dashboard():
    ledger = Path("legal_evolution/legal_evolution_ledger.jsonl")
    
    strategies = []
    with open(ledger, 'r') as f:
        for line in f:
            strategies.append(json.loads(line))
    
    # Calculate metrics
    by_type = {}
    for s in strategies:
        stype = s.get('strategy_type', 'unknown')
        if stype not in by_type:
            by_type[stype] = {'count': 0, 'compliant': 0, 'fitness_sum': 0}
        
        by_type[stype]['count'] += 1
        if s.get('compliant', False):
            by_type[stype]['compliant'] += 1
        by_type[stype]['fitness_sum'] += s.get('fitness', 0)
    
    html = "<h1>Legal Evolution Dashboard</h1>"
    for stype, metrics in by_type.items():
        avg_fitness = metrics['fitness_sum'] / metrics['count']
        compliance_rate = metrics['compliant'] / metrics['count'] * 100
        
        html += f"""
        <div style="border: 1px solid #ccc; margin: 10px; padding: 10px;">
            <h2>{stype.replace('_', ' ').title()}</h2>
            <p>Strategies: {metrics['count']}</p>
            <p>Compliance Rate: {compliance_rate:.1f}%</p>
            <p>Avg Fitness: {avg_fitness:.2f}</p>
        </div>
        """
    
    return HTMLResponse(content=html)
```

### 7. External AI Conversation Workflows

#### Automated Archival from Browser

Create a browser bookmarklet for one-click archival:

```javascript
javascript:(function(){
  const url = window.location.href;
  const summary = prompt('Enter conversation summary:');
  
  if (summary) {
    fetch('http://your-server/api/archive_ai', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({url, summary})
    }).then(r => alert('✅ Archived!'));
  }
})();
```

#### Slack Integration

```python
# slack_bot.py
@app.command("/archive_ai")
def archive_ai_conversation(ack, command, client):
    ack()
    
    # Parse command: /archive_ai <url> <summary>
    parts = command['text'].split(' ', 1)
    url = parts[0]
    summary = parts[1] if len(parts) > 1 else "No summary provided"
    
    archive = ExternalConversationArchive()
    archive.archive_conversation(
        source_url=url,
        summary=summary,
        conversation_type="slack_discussion",
        tags=["slack", command['channel_id']]
    )
    
    client.chat_postMessage(
        channel=command['channel_id'],
        text=f"✅ Archived: {url}"
    )
```

## 📊 Metrics & Reporting

### Weekly Compliance Report

```bash
#!/bin/bash
# weekly_compliance_report.sh

cd legal_evolution

echo "# Weekly Legal Compliance Report"
echo "Generated: $(date)"
echo ""

# Total strategies evolved
TOTAL=$(wc -l < legal_evolution_ledger.jsonl)
echo "Total Strategies Evaluated: $TOTAL"

# Compliance rate
COMPLIANT=$(jq -r 'select(.compliant==true) | .compliant' legal_evolution_ledger.jsonl | wc -l)
RATE=$(echo "scale=1; $COMPLIANT / $TOTAL * 100" | bc)
echo "Compliance Rate: $RATE%"

# Average fitness by type
echo ""
echo "## Average Fitness by Type"
jq -r '.strategy_type' legal_evolution_ledger.jsonl | sort | uniq | while read TYPE; do
    AVG=$(jq -r "select(.strategy_type==\"$TYPE\") | .fitness" legal_evolution_ledger.jsonl | \
          awk '{sum+=$1; count++} END {print sum/count}')
    echo "  $TYPE: $AVG"
done

# External conversations archived
ARCHIVED=$(wc -l < external_ai_ledger.jsonl)
echo ""
echo "External Conversations Archived: $ARCHIVED"
```

## 🔒 Security Considerations

1. **Ledger Protection**: Store ledgers in secure, access-controlled locations
2. **Encryption**: Consider encrypting sensitive strategy snippets in ledgers
3. **Access Control**: Restrict who can run evolution and view strategies
4. **Audit Trail**: Maintain immutable audit logs of all LSEE runs
5. **Version Control**: Track changes to US_CODES and base strategies

## 🚀 Deployment Checklist

- [ ] Set up legal_evolution directory in production
- [ ] Configure cron job for periodic evolution runs
- [ ] Integrate with Discord/Slack for notifications
- [ ] Set up dashboard for monitoring compliance metrics
- [ ] Create backup strategy for ledger files
- [ ] Document SOP export workflow for team
- [ ] Train operators on LSEE usage and limitations
- [ ] Establish legal review process for generated strategies

## 📚 References

- [Main LSEE README](README.md)
- [Sovereignty Architecture README](../README.md)
- [Refinory Documentation](../refinory/README.md)
- [Discord Integration Guide](../GITLENS_INTEGRATION.md)

---

**Remember**: LSEE is a compliance-biasing tool, not a legal authority. Always consult qualified counsel for your specific use cases.
