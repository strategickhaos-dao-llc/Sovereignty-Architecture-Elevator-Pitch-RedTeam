# zyBooks Solver Agent

**Automated zyBooks content processing for rapid answer generation**

## Overview

The zyBooks Solver is an intelligent agent that:
1. 🔍 **Detects** zyBooks content patterns
2. 📝 **Parses** questions into structured format
3. 🧠 **Solves** using statistical reasoning and FlameLang compression
4. 🚀 **Responds** in VESSEL MODE (minimal, direct, fast)

## Quick Start

### Method 1: File-Based
```bash
# Paste content into intake file
nano /path/to/training/zybooks/PASTE_HERE.md

# Process it
python agents/zybooks-solver/main.py training/zybooks/PASTE_HERE.md
```

### Method 2: Direct Processing
```bash
# From file
python agents/zybooks-solver/main.py my_questions.txt

# From stdin
cat questions.txt | python agents/zybooks-solver/main.py -
```

### Method 3: Claude Chat
Just paste zyBooks content directly into Claude chat. The agent auto-detects and processes it.

## Output Formats

### VESSEL MODE (Default) - Fast & Minimal
```
🔥 SECTION 1.5

q1: ✓ TRUE
q2: 20
q3: (b)

Total: 3 answers
```

### YAML Format
```bash
python main.py content.txt --format yaml
```
```yaml
section: "1.5"
answers:
  q1: {answer: TRUE, type: true_false, confidence: 0.85}
  q2: {answer: "20", type: numeric, confidence: 0.95}
```

### Detailed Format (Debug)
```bash
python main.py content.txt --format detailed
```
```
=== SECTION 1.5 ===

q1: TRUE
  Type: true_false
  Confidence: 85.00%
  Reasoning: Pattern match: 2 true indicators
```

## Supported Question Types

- ✅ **True/False** - Binary logic questions
- ✅ **Numeric** - Mathematical calculations (percentages, arithmetic)
- ✅ **Multiple Choice** - Options a, b, c, d
- ✅ **Fill in Blank** - Term identification

## Architecture

```
agents/zybooks-solver/
├── __init__.py      # Package exports
├── parser.py        # Content parsing & question extraction
├── solver.py        # Answer generation with FlameLang logic
├── responder.py     # Output formatting (VESSEL/YAML/Detailed)
└── main.py          # CLI entry point
```

### Pipeline Flow

```
Raw Text → Parser → Questions → Solver → Answers → Responder → Output
           ↓                                                      ↓
      Detect type                                          Format choice
      Extract text                                         (VESSEL/YAML)
      Structure data
```

## Detection Patterns

The parser automatically detects zyBooks content using:

- **Markers**: "participation activity", "zyBooks", "Check Show answer"
- **URL Pattern**: `learn.zybooks.com/zybook/`
- **Structure**: Numbered questions `1)`, True/False options, brackets `[ ]`

## FlameLang Integration

The solver applies FlameLang semantic compression layers:

1. **English**: Extract key statistical terms
2. **Hebrew**: Find root logic patterns
3. **Wave**: Calculate truth probability
4. **DNA**: Emit boolean/value codon

## Training Data

All processed questions are automatically saved to:
- `training/zybooks/sections/` - By section number with timestamp
- `training/zybooks/patterns/` - By question type (JSONL format)

This data feeds back into FlameLang compiler training.

## Dependencies

- Python 3.8+
- PyYAML (for YAML output)

```bash
pip install pyyaml
```

## Examples

### Example 1: Statistics Questions
```
Section 1.5

1) The mean is the average of a dataset.
True
False

2) What is 25% of 80?
[ ]
```

**Output (VESSEL MODE)**:
```
🔥 SECTION 1.5

q1: ✓ TRUE
q2: 20

Total: 2 answers
```

### Example 2: Multiple Choice
```
Section 2.1

1) Standard deviation measures:
a) Central tendency
b) Spread of data
c) Mode only
d) Sample size
```

**Output**:
```
🔥 SECTION 2.1

q1: (b)

Total: 1 answers
```

## Testing

Run individual modules:
```bash
# Test parser
python parser.py

# Test solver
python solver.py

# Test responder
python responder.py

# Test full pipeline
python main.py --help
```

## Integration with GitHub Actions

The workflow `.github/workflows/zybooks-ingest.yaml` automatically processes content when:
- `training/zybooks/PASTE_HERE.md` is updated
- Manually triggered via workflow dispatch

Results are archived as artifacts for 30 days.

## VESSEL MODE Philosophy

**VESSEL MODE** prioritizes:
- ⚡ **Speed** - Answers in <5 seconds
- 🎯 **Directness** - Just the answers, no fluff
- 🔥 **Efficiency** - Operator is locked in, don't break flow

When operator is in VESSEL MODE:
- ❌ No explanations unless asked
- ❌ No verbose output
- ✅ Just answers
- ✅ Clear symbols (✓/✗)
- ✅ Rapid-fire format

## Contributing

This agent is part of the StrategicKhaos swarm intelligence system. Improvements welcome:
- Better pattern detection
- More question types
- Enhanced statistical reasoning
- FlameLang operator mappings

## License

Part of the Sovereignty Architecture - Strategickhaos DAO LLC

---

**Status**: 🔥 LOCKED IN  
**Version**: 1.0.0  
**Operator**: Dom  
**Course**: MAT-243
