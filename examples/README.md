# FlameLang Examples

This directory contains examples and demonstrations for the FlameLang ZyBooks Solver (INV-083).

## Files

### `flamelang_demo.py`
Interactive demonstration of the FlameLang knowledge compiler.

**Run Demo Mode:**
```bash
python3 examples/flamelang_demo.py
```

This will run through 3 example questions and show:
- Question type classification
- Pattern matching
- Answer with confidence score and reasoning

**Run Interactive Mode:**
```bash
python3 examples/flamelang_demo.py --interactive
```

This allows you to enter your own zyBooks questions and get immediate answers.

### `flamelang_test_suite.py`
Comprehensive test suite that validates all components of the FlameLang YAML artifact.

**Run Tests:**
```bash
python3 examples/flamelang_test_suite.py
```

Tests include:
- YAML structure validation
- Meta information completeness
- Layer 1: Question classification
- Layer 2: Semantic roots
- Layer 3: Pattern rules
- Layer 4: Confidence scoring
- Layer 5: Output encoding
- Example execution
- Architecture analogy
- Deployment instructions

All tests must pass for the artifact to be valid.

## Example Usage

### Command Line Demo

```bash
$ python3 examples/flamelang_demo.py
================================================================================
🔥 FLAMELANG ZYBOOKS SOLVER v1.0 - DEMONSTRATION
================================================================================

────────────────────────────────────────────────────────────────────────────────
Question 1:
  A bar chart excels at showing precise values. True or False?

📊 Question Type: type_boolean
🔤 Semantic Analysis: Processing...
✓ Pattern Matched: bar chart + precise values

📝 ANSWER:
  answer: False
  confidence: 0.95
  reason: "bars show relative comparison, not precision"
```

### Interactive Mode

```bash
$ python3 examples/flamelang_demo.py --interactive
================================================================================
🔥 FLAMELANG ZYBOOKS SOLVER v1.0 - INTERACTIVE MODE
================================================================================

Enter questions (or 'quit' to exit):

❓ Question: Horizontal bar charts are better for showing building heights. True or False?

📊 Question Type: type_boolean
🔤 Semantic Analysis: Processing...
✓ Pattern Matched: horizontal + height/floors/buildings

📝 ANSWER:
  answer: False
  confidence: 0.95
  reason: "literal mapping: height shows height"
```

### Test Suite

```bash
$ python3 examples/flamelang_test_suite.py
================================================================================
🔥 FLAMELANG ZYBOOKS SOLVER - COMPREHENSIVE TEST SUITE
================================================================================

────────────────────────────────────────────────────────────────────────────────
TEST: YAML Structure
────────────────────────────────────────────────────────────────────────────────
Testing YAML structure...
  ✓ meta
  ✓ layer_1_classification
  ✓ layer_2_roots
  ✓ layer_3_rules
  ✓ layer_4_confidence
  ✓ layer_5_output
  ✓ All required layers present

...

================================================================================
TEST RESULTS: 10 passed, 0 failed
================================================================================
✓ ALL TESTS PASSED
```

## Pattern Rules

The FlameLang solver uses pattern matching to answer questions. Here are the current patterns:

### Bar Chart Rules
- ❌ **Precise values**: Bars show relative comparison, not precision
- ✅ **Relative values**: Visual comparison is core purpose
- ❌ **More gridlines**: Clutter reduces readability
- ❌ **Data label = category name**: Data label = numeric value on bar

### Orientation Rules
- ✅ **Horizontal + long labels**: No rotation needed
- ✅ **Horizontal + many categories**: Better scrolling
- ❌ **Horizontal + negative values**: Vertical is intuitive (down = negative)
- ❌ **Horizontal + height data**: Literal mapping (height shows height)

### Trend Rules
- Gap narrowing → **Decreased**
- Gap widening → **Increased**
- Total rising → **Increased**
- Percentage rising → **Increased**

## Extending Patterns

To add new pattern rules:

1. Edit `flamelang_zybooks_solver_v1.yaml`
2. Add new pattern to appropriate rule category
3. Include: `pattern`, `answer`, `reason`
4. Run test suite to validate
5. Test with demo script

Example:
```yaml
layer_3_rules:
  bar_chart_rules:
    - pattern: "your + pattern + here"
      answer: true
      reason: "explanation of why this is true"
```

## Requirements

- Python 3.6+
- PyYAML (installed: `pip install pyyaml`)

## Related Files

- `../flamelang_zybooks_solver_v1.yaml` - The main artifact (pattern rules)
- `../FLAMELANG_KNOWLEDGE_COMPILER.md` - Full documentation
- `../README.md` - Main project README

## Support

For issues or questions:
- GitHub Issues: [Sovereignty-Architecture-Elevator-Pitch-RedTeam](https://github.com/strategickhaos-dao-llc/Sovereignty-Architecture-Elevator-Pitch-RedTeam/issues)
- Operator: Domenic Garza (Me10101)
- Organization: Strategickhaos DAO LLC

---

**Built with 🔥 by Strategickhaos DAO LLC**

*Empowering educational sovereignty through knowledge compilation*
