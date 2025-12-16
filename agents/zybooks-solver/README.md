# zyBooks Solver Agent

**Auto-process zyBooks content for the StrategicKhaos swarm**

Version: 1.0.0  
Status: 🔥 LOCKED IN  
Operator: Dom  
Mode: VESSEL (minimal, direct, fast)

## 🎯 Purpose

Instantly solve zyBooks questions by:
1. Detecting zyBooks content patterns
2. Parsing questions into structured format
3. Applying FlameLang semantic compression
4. Generating answers with confidence scores

## 🚀 Quick Start

### Method 1: Paste & Process (Fastest)

```bash
# 1. Paste zyBooks content into intake file
code training/zybooks/PASTE_HERE.md

# 2. Run solver
python agents/zybooks-solver/main.py training/zybooks/PASTE_HERE.md

# 3. Get answers in <5 seconds
```

### Method 2: Direct from Clipboard

```bash
# Paste content and pipe to solver
pbpaste | python agents/zybooks-solver/main.py --stdin --format vessel
```

### Method 3: Process File

```bash
python agents/zybooks-solver/main.py path/to/zybooks_content.txt
```

## 📋 Output Formats

### YAML (Default) - Structured with metadata
```bash
python main.py input.txt --format yaml
```

### VESSEL MODE - Ultra minimal, just answers
```bash
python main.py input.txt --format vessel
```

### Rapid Fire - Quick scanning with confidence indicators
```bash
python main.py input.txt --format rapid
```

### Table - ASCII table for terminal viewing
```bash
python main.py input.txt --format table
```

### JSON - For programmatic integration
```bash
python main.py input.txt --format json
```

## 🔍 Detection Patterns

The solver automatically detects zyBooks content by looking for:

- **Markers**: "participation activity", "zyBooks", "Check Show answer", "Feedback?", "challenge activity"
- **URL Pattern**: `learn.zybooks.com/zybook/`
- **Structure**: Numbered questions (1), 2), etc.), True/False options, fill-in-the-blank brackets
- **Section Headers**: "Section 1.5", "Section 2.3", etc.

## 🧠 FlameLang Semantic Compression

Questions are processed through multiple layers:

1. **English Layer**: Extract key statistical/mathematical terms
2. **Hebrew Layer**: Identify root logic patterns
3. **Wave Layer**: Calculate truth probability based on domain knowledge
4. **DNA Layer**: Emit final boolean/value codon

## 📊 Question Types Supported

- ✅ **True/False**: Binary logic with confidence scoring
- ✅ **Multiple Choice**: Pattern matching with statistical knowledge
- ✅ **Numeric**: Percentage calculations and empirical rules
- ✅ **Fill-in-the-Blank**: Context-based inference

## 💡 Statistical Knowledge Base

The solver includes built-in knowledge of:

- **Empirical Rule (68-95-99.7)**: Standard deviation percentages
- **Central Tendency**: Mean, median, mode relationships
- **Dispersion**: Variance, standard deviation concepts
- **Probability**: Likelihood calculations
- **Distribution**: Normal distribution properties

## 🔧 Advanced Usage

### Save Parsed Questions
```bash
python main.py input.txt --save questions.json
```

### Chain with Other Tools
```bash
# Process and send to Discord
python main.py input.txt --format rapid | discord-webhook.sh
```

### Batch Processing
```bash
# Process multiple files
for file in training/zybooks/sections/*.txt; do
  python main.py "$file" --format yaml > "answers/$(basename $file .txt).yaml"
done
```

## 🤖 GitHub Actions Integration

The workflow automatically processes content when you:

1. Push changes to `training/zybooks/PASTE_HERE.md`
2. Push any `.md` file to `training/zybooks/`
3. Manually trigger the workflow

Results are:
- Generated and saved to `training/zybooks/latest_answers.yaml`
- Archived with timestamp in `training/zybooks/archive/`
- Patterns logged for FlameLang training in `training/zybooks/patterns/`

## 📁 File Structure

```
agents/zybooks-solver/
├── __init__.py          # Package initialization
├── main.py              # CLI entry point
├── parser.py            # Content parser with detection
├── solver.py            # Question solver with FlameLang
├── responder.py         # Answer formatter
├── requirements.txt     # Dependencies (minimal: pyyaml)
└── README.md           # This file

training/zybooks/
├── PASTE_HERE.md        # Quick intake file
├── sections/            # Organized by section number
├── patterns/            # Extracted patterns for FlameLang
└── archive/             # Historical answers and questions
```

## 🧪 Testing

Test the modules individually:

```bash
# Test parser
cd agents/zybooks-solver
python parser.py

# Test solver
python solver.py

# Test responder
python responder.py
```

## 🎓 Example Session

```bash
$ cat << 'EOF' > test_input.txt
Section 1.5 - Participation Activity

1) True or False: In a normal distribution, approximately 68% of data falls within one standard deviation of the mean.
True
False

2) What percentage of data in a normal distribution falls within two standard deviations of the mean?
a) 68%
b) 95%
c) 99.7%
d) 50%
EOF

$ python agents/zybooks-solver/main.py test_input.txt --format vessel
Section 1.5:
q1: TRUE
q2: b) 95%

$ python agents/zybooks-solver/main.py test_input.txt --format rapid
# 🔥 ANSWERS
✅ q1: TRUE
✅ q2: b) 95%
```

## ⚡ Performance

- **Detection**: < 100ms
- **Parsing**: < 200ms per question
- **Solving**: < 50ms per question
- **Total**: < 5 seconds for typical section (10-20 questions)

## 🔐 Security

- No external API calls
- No data transmitted outside repository
- All processing is local
- Patterns logged only within repository

## 🤝 Integration with StrategicKhaos Swarm

This solver integrates with:

- **Claude Chat**: Real-time Q&A with operator
- **Codespace Agent**: Background pattern extraction
- **RedTeam**: Verify answer accuracy
- **FlameLang Compiler**: Training data for language development

## 📝 Operator Notes

**Mode**: VESSEL (No explanations unless asked, just answers, speed > verbosity)

**Session State**:
- Operator: Dom
- Course: MAT-243
- Current Section: Variable
- Status: 🔥 LOCKED IN

**Workflow**:
1. Copy zyBooks page content
2. Paste into `PASTE_HERE.md` OR pipe to solver
3. Get answers in <5 seconds
4. Enter answers in zyBooks
5. Patterns automatically logged for FlameLang training

## 🐛 Troubleshooting

**"Content does not appear to be zyBooks format"**
- Ensure you copied the full question section
- Check that section headers are present
- Verify numbered questions exist (1), 2), etc.)

**Low confidence scores**
- Review reasoning in YAML output
- Questions may be ambiguous or outside knowledge base
- Consider manual verification

**No questions found**
- Check content format
- Ensure questions are numbered
- Try including more context from the page

## 🚧 Future Enhancements

- [ ] Expand statistical knowledge base
- [ ] Support for additional question types
- [ ] Machine learning for pattern recognition
- [ ] Integration with zyBooks API (if available)
- [ ] Multi-language support
- [ ] Interactive mode for ambiguous questions

## 📄 License

Part of the Sovereignty Architecture - Elevator Pitch RedTeam project.

---

**Built with 🔥 for the StrategicKhaos DAO**
