# Legal Evolution Engine - Quick Start Guide

Get up and running with the Legal Synthesizer Evolution Engine (LSEE) in 5 minutes.

## 🚀 Fast Setup

### Step 1: Navigate to Directory

```bash
cd legal_evolution
```

### Step 2: Run Your First Evolution

```bash
python3 legal_evolution_synthesizer.py
```

You'll see:
- 🧬 Evolution progress through 5 generations
- ⚖️ Compliance checking against 30+ US legal codes
- 📊 Real-time fitness scores and compliance rates
- 🎯 Best strategy identified at the end

### Step 3: Check the Output

Two ledger files are created:

```bash
# View evolution ledger
cat legal_evolution_ledger.jsonl | jq '.'

# View archived conversations
cat external_ai_ledger.jsonl | jq '.'
```

### Step 4: Monitor Progress (Optional)

**Linux/Mac:**
```bash
./monitor_evolution.sh -n 10          # Show last 10 entries
./monitor_evolution.sh --follow       # Follow in real-time
```

**Windows PowerShell:**
```powershell
.\monitor_evolution.ps1 -Lines 10     # Show last 10 entries
.\monitor_evolution.ps1 -Follow       # Follow in real-time
```

## 📚 Try the Examples

```bash
python3 example_usage.py
```

Choose from:
1. **Basic evolution run** - Quick test with 3 generations
2. **Custom strategy evolution** - Add your own strategy type
3. **Archive AI conversations** - Practice conversation archival
4. **Analyze evolution ledger** - Review statistics
5. **Extract best strategies** - Get best-performing strategies by type
6. **Run all examples** - Complete walkthrough

## 🎯 Common Use Cases

### Use Case 1: Generate a Background Check SOP

```bash
# Run evolution
python3 legal_evolution_synthesizer.py

# Extract best background check strategy
cat legal_evolution_ledger.jsonl | \
  jq -r 'select(.strategy_type=="background_check" and .compliant==true) | 
         select(.fitness >= 95.0) | 
         .snippet' | head -1 > background_check_sop.md

# Review and edit for your needs
nano background_check_sop.md
```

### Use Case 2: Archive an AI Discussion

```python
from legal_evolution_synthesizer import ExternalConversationArchive

archive = ExternalConversationArchive()
archive.archive_conversation(
    source_url="https://claude.ai/share/your-conversation-id",
    summary="Your conversation summary here",
    conversation_type="design_discussion",
    tags=["legal", "compliance", "your-tags"]
)
```

### Use Case 3: Validate a Proposed Strategy

```python
from legal_evolution_synthesizer import (
    LegalComplianceJudge,
    LegalStrategy,
    US_CODES
)

# Your proposed strategy
my_strategy = """
Social media investigation using publicly available profiles.
No unauthorized access or credential harvesting.
Document all sources and respect terms of service.
"""

# Validate it
judge = LegalComplianceJudge(US_CODES)
strategy = LegalStrategy(my_strategy, strategy_type="social_media")
judge.verify_strategy(strategy)

print(f"Compliant: {strategy.compliance_verified}")
print(f"Fitness: {strategy.fitness}")
if strategy.verification_ledger:
    print(f"Violations: {strategy.verification_ledger[-1]['violations']}")
```

## ⚙️ Configuration

### Adjust Evolution Parameters

Edit `legal_evolution_synthesizer.py` main function:

```python
engine = LegalEvolutionEngine(
    judge=judge,
    population_size=20,      # More diversity (default: 10)
    mutation_rate=0.5,       # Higher variation (default: 0.3)
    generations=10           # Longer evolution (default: 5)
)
```

### Add Your Legal Codes

Expand the `US_CODES` list at the top of the script:

```python
US_CODES: List[str] = [
    # ... existing codes
    
    # Add your state-specific codes
    "California Business and Professions Code § 7520 et seq. (PI Licensing)",
    "New York General Business Law § 70 (PI Licensing)",
    
    # Add industry-specific regulations
    "Health Insurance Portability and Accountability Act (HIPAA)",
    "Payment Card Industry Data Security Standard (PCI DSS)",
]
```

### Customize Strategy Types

In the `main()` function, add your own base strategy:

```python
custom_strategy = LegalStrategy(
    approach="""
    Your strategy description here.
    Must include compliance language and lawful methods.
    """,
    generation=0,
    strategy_type="your_custom_type"
)

base_strategies.append(custom_strategy)
```

## 📊 Understanding the Output

### Fitness Score (0-100)
- **100**: Perfect compliance, all requirements met
- **85-99**: Good compliance, minor improvements needed
- **60-84**: Acceptable but needs strengthening
- **< 60**: Not compliant, significant issues

### Strategy Types
- `background_check`: FCRA-compliant background investigations
- `osint`: Open-source intelligence gathering
- `skip_trace`: Person location strategies
- `social_media_investigation`: Social platform research
- `your_custom_type`: Your own strategy categories

### Ledger Fields
```json
{
  "timestamp": "ISO 8601 timestamp",
  "event_type": "seed | evolved",
  "strategy_id": "Unique identifier",
  "generation": "Evolution generation number",
  "strategy_type": "Category of strategy",
  "fitness": "Compliance score 0-100",
  "compliant": "Boolean - fully compliant",
  "snippet": "First 200 chars of strategy",
  "codes_checked": "Number of legal codes validated against"
}
```

## 🔍 Troubleshooting

### Problem: No compliant strategies generated

**Solution**: Strengthen your base strategies with more compliance language:
- Add explicit references to legal codes (FCRA, CFAA, etc.)
- Include consent and authorization requirements
- Emphasize lawful methods and public sources
- Remove any potentially problematic keywords

### Problem: Ledger files not created

**Solution**: Check permissions and Python version:
```bash
python3 --version    # Should be 3.7+
ls -la *.jsonl       # Check if files exist
pwd                  # Make sure you're in legal_evolution directory
```

### Problem: Low fitness scores

**Solution**: The judge is being strict (which is good!). Review violations:
```bash
cat legal_evolution_ledger.jsonl | \
  jq 'select(.compliant==false) | .snippet' | head -5
```

## 🎓 Next Steps

1. **Read the full README**: [README.md](README.md)
2. **Explore integration**: [INTEGRATION.md](INTEGRATION.md)
3. **Review examples**: `python3 example_usage.py`
4. **Customize for your needs**: Edit strategies and legal codes
5. **Deploy to production**: Follow integration guide

## ⚠️ Important Reminders

- ✅ This tool **biases toward legal compliance**
- ✅ It **documents your due diligence**
- ❌ It is **NOT legal advice**
- ❌ Always **consult qualified counsel**
- ❌ Human review **required for production use**

## 🤝 Getting Help

- Review the [README](README.md) for detailed documentation
- Check [INTEGRATION.md](INTEGRATION.md) for ecosystem integration
- Study the [example_usage.py](example_usage.py) for patterns
- Examine the base strategies in the main script

## 📝 Quick Reference

```bash
# Run evolution
python3 legal_evolution_synthesizer.py

# Run examples interactively
python3 example_usage.py

# Monitor progress (Linux/Mac)
./monitor_evolution.sh --follow

# Monitor progress (Windows)
.\monitor_evolution.ps1 -Follow

# Analyze ledger
cat legal_evolution_ledger.jsonl | jq '.strategy_type' | sort | uniq -c

# Get best by type
cat legal_evolution_ledger.jsonl | \
  jq -r 'select(.strategy_type=="osint" and .compliant==true) | 
         [.fitness, .snippet] | @tsv' | \
  sort -rn | head -1
```

---

**Remember**: This is a compliance-biasing tool. You, the licensed professional, make the final decisions.

Happy evolving! 🧬⚖️
