# ═══════════════════════════════════════════════════════════════════
# 🔥 ZYBOOKS INGESTION PROTOCOL
# ═══════════════════════════════════════════════════════════════════

**Repository**: `strategickhaos-dao-llc/Sovereignty-Architecture-Elevator-Pitch-RedTeam`  
**Version**: 1.0.0  
**Purpose**: Auto-process zyBooks content pasted by operator

---

## Protocol Overview

This protocol enables rapid processing of zyBooks educational content through:
1. **Pattern Detection** - Automatically identify zyBooks content
2. **Question Parsing** - Extract structured questions from text
3. **Answer Generation** - Apply FlameLang semantic compression and statistical reasoning
4. **Rapid Response** - Return answers in VESSEL MODE (minimal, direct, fast)

---

## Detection Patterns

### Content Markers
The system detects zyBooks content by looking for these markers:
- `participation activity`
- `zyBooks`
- `Check Show answer`
- `Feedback?`
- `challenge activity`
- `Section 1.`
- `True\nFalse`

### URL Pattern
- `learn.zybooks.com/zybook/`

### Content Structure
- **Numbered questions**: `^\d+\)`
- **True/False**: `(True|False)`
- **Fill blank**: `\[\s*\]`
- **Percentage**: `\s*%\s*`

---

## Agent Instructions

### Step 1: Parse
**Action**: Extract question blocks  
**Output**: `questions.json`  
**Format**:
```json
{
  "questions": [
    {
      "id": "q1",
      "type": "true_false",
      "text": "question text",
      "options": null,
      "section": "1.5"
    }
  ]
}
```

### Step 2: Analyze
**Action**: Apply FlameLang semantic compression  
**Layers**:
- **English**: Extract key terms
- **Hebrew**: Find root logic pattern
- **Wave**: Calculate truth probability
- **DNA**: Emit boolean/value codon

### Step 3: Solve
**Action**: Generate answer key  
**Output**: `answers.yaml`  
**Format**:
```yaml
section: "1.5"
answers:
  q1:
    answer: TRUE
    type: true_false
    confidence: 0.85
```

### Step 4: Respond
**Action**: Return rapid-fire format to operator  
**Style**: VESSEL MODE - minimal, direct, fast

---

## Usage Methods

### Method 1: File-Based Processing
```bash
# Paste content into PASTE_HERE.md
# Then run:
python agents/zybooks-solver/main.py training/zybooks/PASTE_HERE.md
```

### Method 2: Direct CLI
```bash
# Process from stdin
cat content.txt | python agents/zybooks-solver/main.py -
```

### Method 3: Claude Chat
Simply paste zyBooks content into Claude chat. The agent will:
1. Auto-detect zyBooks format
2. Parse questions
3. Generate answers
4. Return in VESSEL MODE

---

## Output Formats

### VESSEL MODE (Default)
```
🔥 SECTION 1.5

q1: ✓ TRUE
q2: 20
q3: (b)

Total: 3 answers
```

### YAML Format
```yaml
section: "1.5"
answers:
  q1: {answer: TRUE, type: true_false, confidence: 0.85}
  q2: {answer: "20", type: numeric, confidence: 0.95}
  q3: {answer: b, type: multiple_choice, confidence: 0.70}
```

### Detailed Format (Debug)
```
=== SECTION 1.5 ===

q1: TRUE
  Type: true_false
  Confidence: 85.00%
  Reasoning: Pattern match: 2 true indicators

q2: 20
  Type: numeric
  Confidence: 95.00%
  Reasoning: 25% of 80
```

---

## File Structure

```
training/zybooks/
├── PASTE_HERE.md           # Operator intake file
├── PROTOCOL.md             # This file
├── sections/               # Processed sections archive
│   ├── section_1.5.json
│   └── section_2.1.json
└── patterns/               # Extracted patterns for training
    ├── true_false.json
    └── numeric.json

agents/zybooks-solver/
├── __init__.py             # Package initialization
├── parser.py               # Content parser
├── solver.py               # Answer generation
├── responder.py            # Output formatting
└── main.py                 # CLI entry point
```

---

## Integration with Main Claude Chat

### Operator Flow
1. Copy zyBooks page content
2. Paste into codespace `PASTE_HERE.md` OR into Claude chat
3. Agent/Claude detects zyBooks format
4. Returns answer key in <5 seconds
5. Operator enters answers
6. Patterns logged for FlameLang training

### Parallel Execution
- **Claude**: Real-time Q&A with operator
- **Codespace Agent**: Background pattern extraction
- **RedTeam**: Verify answer accuracy

---

## Current Session State

- **Operator**: Dom
- **Mode**: VESSEL 🔥
- **Course**: MAT-243
- **Current Section**: 1.5
- **Points Earned**: 13
- **Status**: LOCKED IN

---

## FlameLang Training

All processed questions are logged to:
- `/training/zybooks/sections/` - By section number
- `/training/zybooks/patterns/` - By question type

These logs feed the FlameLang compiler for:
- Transformation rule extraction
- Question type → FlameLang operator mapping
- Pattern recognition improvement

---

## Quick Start Commands

```bash
# Create structure (if not exists)
mkdir -p training/zybooks/sections agents/zybooks-solver

# Create intake file
touch training/zybooks/PASTE_HERE.md

# Watch for changes (optional)
watch -n 1 'if [ -s training/zybooks/PASTE_HERE.md ]; then python agents/zybooks-solver/main.py training/zybooks/PASTE_HERE.md; fi'
```

---

## GitHub Workflow

The workflow `.github/workflows/zybooks-ingest.yaml` can be configured to:
- Auto-process on file changes
- Store results in GitHub artifacts
- Trigger notifications to Discord
- Update progress tracking

---

**END OF PROTOCOL**
