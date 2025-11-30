# Legal Synthesizer Evolution Engine (LSEE)

An evolutionary algorithm system that generates and refines legal compliance strategies for private investigation, OSINT, and background check operations.

## 🎯 Purpose

The LSEE uses genetic algorithms to:
- **Evolve strategies** across generations using crossover and mutation
- **Validate compliance** against 30+ US legal codes (FCRA, CFAA, SCA, etc.)
- **Maintain audit trails** in JSONL ledgers for every generation
- **Archive external AI discussions** for compliance documentation

## 🚀 Quick Start

```bash
cd legal_evolution
python3 legal_evolution_synthesizer.py
```

This will:
1. Initialize population with base strategies (background checks, OSINT, skip tracing)
2. Evolve strategies over 5 generations
3. Validate each strategy against US legal codes
4. Generate `legal_evolution_ledger.jsonl` with full audit trail
5. Archive the Claude AI conversation in `external_ai_ledger.jsonl`

## 📊 Output

### Strategy Evolution Ledger (`legal_evolution_ledger.jsonl`)

Each line is a JSON entry documenting:
```json
{
  "timestamp": "2025-11-21T03:06:35Z",
  "event_type": "evolved",
  "strategy_id": "strategy_1732158395.123_4567",
  "generation": 3,
  "strategy_type": "osint",
  "fitness": 87.5,
  "compliant": true,
  "snippet": "OSINT collection limited to publicly available...",
  "codes_checked": 30
}
```

### External AI Archive (`external_ai_ledger.jsonl`)

Archives external discussions for audit trail:
```json
{
  "timestamp": "2025-11-21T03:06:35Z",
  "type": "design_discussion",
  "source": "https://claude.ai/share/777c7e93-fb67-4026-8370-1b1588c5df56",
  "summary": "Design of meta-evolution and legal synthesizer engine.",
  "tags": ["legal", "evolution", "compliance"],
  "archived_by": "legal_evolution_system"
}
```

## 📋 Features

### Strategy Types

- **`background_check`**: FCRA-compliant background investigation procedures
- **`osint`**: Open-source intelligence gathering methods
- **`skip_trace`**: Person location strategies

### Compliance Validation

The system checks strategies against:
- **30+ US legal codes** including FCRA, CFAA, Wiretap Act, SCA
- **Prohibited keywords** (unauthorized access, hacking, pretexting, etc.)
- **Required compliance phrases** (lawful, authorized, consent, public record)
- **Strategy-specific rules** (e.g., OSINT must emphasize public sources)

### Evolutionary Operations

1. **Selection**: Tournament selection favoring compliant strategies
2. **Crossover**: Combine sentences from two parent strategies
3. **Mutation**: Add compliance-focused improvements
4. **Elitism**: Preserve top 20% of compliant strategies

## 🔧 Configuration

Edit the script to customize:

```python
# Population and evolution parameters
engine = LegalEvolutionEngine(
    judge=judge,
    population_size=10,      # Number of strategies per generation
    mutation_rate=0.3,       # Probability of mutation (0.0-1.0)
    generations=5            # Number of evolution cycles
)
```

### Adding Legal Codes

Expand the `US_CODES` list near the top of the script:

```python
US_CODES: List[str] = [
    "15 U.S.C. § 1681 et seq. (FCRA)",
    "18 U.S.C. § 2510 et seq. (Wiretap Act)",
    # Add your codes here
]
```

## 📈 Monitoring Progress

### PowerShell (Windows)
```powershell
Get-Content .\legal_evolution_ledger.jsonl -Wait |
  ForEach-Object { $_ | ConvertFrom-Json } |
  Select-Object generation, population_size, fitness, compliant
```

### Bash (Linux/Mac)
```bash
tail -f legal_evolution_ledger.jsonl | jq '{generation, fitness, compliant, strategy_type}'
```

## 🔍 Use Cases

### 1. Generate SOPs
Export best strategies to your Obsidian/Markdown vault:
```
Background_Check_Procedure_LSEE_Gen5.md
OSINT_Procedure_LSEE_Gen5.md
```

### 2. Compliance Documentation
Reference ledger entries to demonstrate due diligence:
```
"Strategy validated against 30 legal codes on 2025-11-21"
```

### 3. Archive AI Discussions
```python
archive = ExternalConversationArchive()
archive.archive_conversation(
    source_url="https://claude.ai/share/xxx",
    summary="Discussion of compliance strategies",
    tags=["legal", "compliance"]
)
```

### 4. Training Data
Extract annotated prompt/response pairs for:
- Agent training
- Legal compliance syntheses
- Chain-of-custody documentation

## ⚠️ Important Disclaimers

### This is NOT Legal Advice

- The LSEE uses **heuristic pattern matching**, not legal analysis
- It is a **compliance-biasing tool**, not a legal authority
- It **strongly biases toward conservative, lawful strategies**
- It **documents due diligence** in machine-readable format

### Human Review Required

**Always** have a licensed professional review:
- Generated strategies before operational use
- Legal compliance for your specific jurisdiction
- High-stakes or novel investigation scenarios

### Proper Use

Treat LSEE as:
> "A compliance-obsessed junior analyst that drafts SOPs and flags risk.
> You, the licensed human, sign off."

## 🚀 Next Steps

### After First Run

1. **Review Output**: Check `legal_evolution_ledger.jsonl` for best strategies
2. **Export SOPs**: Copy best strategies to your documentation system
3. **Add Legal Codes**: Expand `US_CODES` with jurisdiction-specific regulations
4. **Customize**: Adjust mutation rate, population size, generations

### Future Enhancements

1. **Effectiveness Judge**: Add second scoring dimension for practical utility
2. **Dashboard**: Visualize evolution progress and best-per-type strategies
3. **Agent Integration**: Hook into worker agents for real-time strategy retrieval
4. **Multi-jurisdictional**: Add state-specific legal code validation

## 📚 References

- [Fair Credit Reporting Act (FCRA)](https://www.ftc.gov/legal-library/browse/statutes/fair-credit-reporting-act)
- [Computer Fraud and Abuse Act (CFAA)](https://www.law.cornell.edu/uscode/text/18/1030)
- [Stored Communications Act (SCA)](https://www.law.cornell.edu/uscode/text/18/part-I/chapter-121)

## 📝 License

Part of the Strategickhaos Sovereignty Architecture ecosystem.

## 🤝 Contributing

This is an evolving system. Contributions welcome for:
- Additional legal codes
- Improved compliance heuristics
- Integration with other sovereignty tools
- Documentation improvements

---

**Remember**: This tool helps you *stay legal*, but it doesn't *make you legal*.
Always consult qualified counsel for your specific use case.
