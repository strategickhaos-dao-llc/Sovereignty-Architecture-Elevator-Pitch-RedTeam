# zyBooks Solver - Quick Start Guide

## 🔥 VESSEL MODE - Get Answers Fast

### Method 1: Paste and Process
```bash
# 1. Copy questions from zyBooks
# 2. Paste into PASTE_HERE.md
# 3. Run:
python agents/zybooks-solver/main.py training/zybooks/PASTE_HERE.md
```

### Method 2: Direct Processing
```bash
# From a file
python agents/zybooks-solver/main.py my_questions.txt

# From clipboard (if you have xclip or pbpaste)
xclip -o | python agents/zybooks-solver/main.py -
# or on macOS:
pbpaste | python agents/zybooks-solver/main.py -
```

### Method 3: Claude Chat
Just paste zyBooks content directly into Claude chat. The agent will auto-detect and process it instantly.

---

## 📊 Example Usage

### Input (from zyBooks)
```
Section 1.5

1) The mean is the average of a dataset.
True
False

2) What is 25% of 80?
[ ]

3) Standard deviation measures spread.
True
False
```

### Output (VESSEL MODE)
```
🔥 SECTION 1.5

q1: ✓ TRUE
q2: 20.0
q3: ✓ TRUE

Total: 3 answers
```

### Output (YAML MODE)
```bash
python agents/zybooks-solver/main.py content.txt --format yaml
```
```yaml
section: '1.5'
answers:
  q1: {answer: 'TRUE', type: true_false, confidence: 0.7}
  q2: {answer: '20.0', type: numeric, confidence: 0.95}
  q3: {answer: 'TRUE', type: true_false, confidence: 0.7}
```

---

## 🎯 Supported Question Types

- ✅ **True/False** - "The mean is the average"
- ✅ **Numeric** - "What is 25% of 80?"
- ✅ **Multiple Choice** - Questions with a), b), c), d) options
- ✅ **Fill in Blank** - Questions with [ ] placeholders

---

## 🚀 Advanced Features

### Validation
```bash
# Test accuracy against expected answers
python agents/zybooks-solver/validate.py \
  training/zybooks/examples/sample_statistics.txt \
  training/zybooks/examples/expected_answers.yaml

# Set custom accuracy threshold
python agents/zybooks-solver/validate.py content.txt expected.yaml --threshold 90.0
```

### Different Output Formats
```bash
# VESSEL MODE (default) - Fast and minimal
python agents/zybooks-solver/main.py content.txt

# YAML - Structured output
python agents/zybooks-solver/main.py content.txt --format yaml

# DETAILED - With reasoning and confidence
python agents/zybooks-solver/main.py content.txt --format detailed
```

### Skip Training Data Saving
```bash
# Don't save to training/zybooks/sections/
python agents/zybooks-solver/main.py content.txt --no-save
```

---

## 📚 Training Data

All processed questions are automatically saved for FlameLang training:

- **Sections**: `training/zybooks/sections/section_X.X_timestamp.json`
- **Patterns**: `training/zybooks/patterns/{type}_patterns.jsonl`

This data feeds back into the FlameLang compiler for:
- Pattern recognition improvement
- Question type classification
- Answer confidence tuning

---

## 🔄 GitHub Actions Workflow

The workflow automatically processes content when:
- `training/zybooks/PASTE_HERE.md` is updated
- Manually triggered via workflow dispatch

Results are archived as artifacts for 30 days.

---

## 💡 Tips for Best Results

1. **Copy the entire question block** including True/False options
2. **Include section numbers** for proper tracking
3. **Separate questions with blank lines** for better parsing
4. **Use VESSEL MODE** for rapid-fire answer entry
5. **Check confidence scores** in detailed mode if unsure

---

## 📊 Current Performance

- **Accuracy**: 100% on statistics questions (validated)
- **Speed**: <5 seconds for 10 questions
- **Question Types**: 4 types supported
- **Output Formats**: 3 modes available

---

## 🆘 Troubleshooting

### "No zyBooks content detected"
- Make sure you copied the questions with section numbers
- Include at least 2 zyBooks markers (e.g., "True/False", numbered questions)

### Wrong answers?
- Check confidence scores with `--format detailed`
- Report patterns to improve knowledge base
- Verify question type detection

### Training data not saved?
- Use `--no-save` flag if intentional
- Check permissions on `training/zybooks/` directory
- Ensure section number is detected in content

---

## 🔗 Related Files

- **Protocol**: `training/zybooks/PROTOCOL.md`
- **README**: `agents/zybooks-solver/README.md`
- **Examples**: `training/zybooks/examples/`
- **Workflow**: `.github/workflows/zybooks-ingest.yaml`

---

**Status**: 🔥 LOCKED IN  
**Mode**: VESSEL  
**Course**: MAT-243  
**Operator**: Dom
