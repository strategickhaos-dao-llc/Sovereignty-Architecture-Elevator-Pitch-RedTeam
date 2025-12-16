# 🔥 FlameLang Quick Start Guide

## What is This?

A **semantic pattern compiler** that runs on any LLM to solve zyBooks questions for MAT-243 Applied Statistics.

## 5-Minute Setup

### Step 1: Copy the Pattern Rules

```bash
# Copy the YAML file content
cat flamelang_zybooks_solver_v1.yaml | pbcopy
```

### Step 2: Paste to Your LLM

Open any of these LLM platforms:
- [Claude](https://claude.ai)
- [ChatGPT](https://chat.openai.com)
- [Grok](https://x.com)
- [Gemini](https://gemini.google.com)

Paste the entire YAML file into a new conversation.

### Step 3: Ask Questions

Just paste your zyBooks question:

```
❓ A bar chart excels at showing precise values. True or False?

📝 ANSWER:
answer: false
confidence: 0.95
reason: "bars show relative comparison, not precision"
```

## Demo Mode (Local)

```bash
# Run demonstration with 3 example questions
python3 examples/flamelang_demo.py

# Interactive mode for custom questions
python3 examples/flamelang_demo.py --interactive
```

## Pattern Rules Coverage

### ✅ Currently Supported

**Bar Charts:**
- Precise vs relative values
- Gridline effectiveness
- Data label identification

**Orientation:**
- Long labels → Horizontal
- Many categories → Horizontal
- Negative values → Vertical
- Height data → Vertical

**Trends:**
- Gap analysis (narrowing/widening)
- Total changes
- Percentage changes

### 🚧 Coming Soon

- Hypothesis testing
- Confidence intervals
- P-values
- Distribution identification
- Probability calculations

## Output Format

Every answer includes:
- **answer**: true/false or specific value
- **confidence**: 0.0-1.0 score
- **reason**: One-line explanation

Example:
```yaml
answer: false
confidence: 0.95
reason: "bars show relative comparison, not precision"
```

## Platform-Specific Tips

### Claude
- Best for: Complex reasoning
- Context: Paste YAML once per session
- Speed: Fast responses

### ChatGPT
- Best for: Quick answers
- Context: Paste YAML once per session
- Speed: Very fast responses

### Grok
- Best for: Real-time learning
- Context: Paste YAML once per session
- Speed: Fast responses

### Local LLMs
- Best for: Privacy
- Context: Include YAML in system prompt
- Speed: Depends on hardware

## Parallel Processing

Solve multiple questions simultaneously:

1. **Open 3 browser windows** (Claude, GPT, Grok)
2. **Paste YAML** to each
3. **Ask different questions** in each window
4. **Aggregate results**

This is 3x faster than sequential processing.

## Confidence Levels

- **0.9-1.0**: High confidence - Direct pattern match
- **0.7-0.9**: Medium confidence - Requires interpretation
- **0.0-0.7**: Low confidence - Prediction or subjective

Trust high confidence answers. Review medium/low confidence answers.

## Troubleshooting

### "Pattern not found"
- Question type not yet supported
- Add pattern rule to YAML
- Run test suite to validate

### "Wrong answer"
- Check question wording
- Verify pattern matching logic
- Submit issue on GitHub

### "YAML parse error"
- Copy entire file including headers
- Don't modify structure
- Validate with: `python3 -c "import yaml; yaml.safe_load(open('flamelang_zybooks_solver_v1.yaml'))"`

## Adding New Patterns

1. **Edit YAML** - Add rule to `layer_3_rules`
2. **Test** - Run `python3 examples/flamelang_test_suite.py`
3. **Demo** - Try in `flamelang_demo.py --interactive`
4. **Deploy** - Copy to LLMs

Example pattern:
```yaml
layer_3_rules:
  bar_chart_rules:
    - pattern: "stacked + percentage"
      answer: true
      reason: "stacked charts show proportions"
```

## Academic Integrity

### ✅ Good Use
- Understanding concepts
- Verifying your reasoning
- Learning pattern recognition
- Studying efficiently

### ❌ Bad Use
- Submitting without understanding
- Bypassing learning process
- Violating academic policies

**Your responsibility:** Follow your institution's policies.

## Files

- `flamelang_zybooks_solver_v1.yaml` - Main artifact (15KB)
- `FLAMELANG_KNOWLEDGE_COMPILER.md` - Full documentation (8KB)
- `examples/flamelang_demo.py` - Demo script (6KB)
- `examples/flamelang_test_suite.py` - Test suite (10KB)
- `examples/README.md` - Examples guide (5KB)
- `FLAMELANG_QUICK_START.md` - This file

## Test Suite

Validate everything works:

```bash
python3 examples/flamelang_test_suite.py
```

Should output:
```
TEST RESULTS: 10 passed, 0 failed
✓ ALL TESTS PASSED
```

## Advanced Usage

### Batch Processing

```python
from flamelang_demo import solve_question

questions = [
    "Question 1 text...",
    "Question 2 text...",
    "Question 3 text..."
]

for q in questions:
    result = solve_question(q)
    print(f"{result['answer']}: {result['reason']}")
```

### Custom Confidence Threshold

Only accept high-confidence answers:

```python
result = solve_question(question)
if result['confidence'] >= 0.9:
    print(f"Answer: {result['answer']}")
else:
    print("Manual review needed")
```

### Integration with Study Tools

Use with Anki, Quizlet, or other spaced repetition systems.

## Support

- **Issues**: [GitHub Issues](https://github.com/strategickhaos-dao-llc/Sovereignty-Architecture-Elevator-Pitch-RedTeam/issues)
- **Docs**: [FLAMELANG_KNOWLEDGE_COMPILER.md](FLAMELANG_KNOWLEDGE_COMPILER.md)
- **Contact**: Domenic Garza (Me10101)
- **Org**: Strategickhaos DAO LLC

## Version

- **Artifact**: INV-083
- **Version**: 1.0
- **Released**: 2025-12-16
- **Course**: MAT-243 Applied Statistics for STEM

## License

MIT License - See [LICENSE](LICENSE) file

---

**Built with 🔥 by Strategickhaos DAO LLC**

*"This is literally what compilers do — pattern → transform → output."*

*Start solving zyBooks questions in under 5 minutes.*
