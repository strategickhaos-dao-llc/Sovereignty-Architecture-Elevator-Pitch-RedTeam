# 🔥 FlameLang ZyBooks Solver - Quick Reference

## One-Minute Setup

1. **Copy the solver**:
   ```bash
   cat flamelang-zybooks-solver.yaml
   ```

2. **Paste to Claude** (entire YAML file)

3. **Ask your question**:
   ```
   A bar chart excels at showing precise values. True or False?
   ```

4. **Get instant answer**:
   ```yaml
   answer: FALSE
   confidence: 0.95
   reason: "bars show relative comparison, not precision"
   ```

## Common Patterns - Instant Cheat Sheet

### Bar Chart Rules

| Question Pattern | Answer | Why |
|-----------------|--------|-----|
| "bar chart + precise values" | FALSE | Bars show comparison, not precision |
| "bar chart + relative values" | TRUE | Visual comparison is the core purpose |
| "more gridlines = better" | FALSE | Clutter reduces readability |
| "data label = category name" | FALSE | Data labels show numeric values |

### Orientation Rules

| Question Pattern | Answer | Why |
|-----------------|--------|-----|
| "horizontal + long labels" | TRUE | No text rotation needed |
| "horizontal + many categories" | TRUE | Vertical scroll better than horizontal |
| "horizontal + negative values" | FALSE | Vertical is intuitive: down = negative |
| "horizontal + height/buildings" | FALSE | Literal mapping: height shows height |

### Trend Analysis

| Question Pattern | Answer | Why |
|-----------------|--------|-----|
| "gap narrowing over time" | Decreased | Visual convergence |
| "gap widening over time" | Increased | Visual divergence |
| "total rising" | Increased | Sum accumulation |
| "percentage rising in stacked" | Increase | Proportion growth |

## Question Types

The solver automatically detects:

- **Boolean** → True/False answers
- **Comparison** → More/fewer/same
- **Trend** → Increased/decreased/same
- **Percentage** → Numeric percentage
- **Prediction** → Forecast value

## Confidence Levels

- **0.9+** (High) → Direct rule match, no ambiguity
- **0.7-0.9** (Medium) → Requires chart interpretation
- **<0.7** (Low) → Prediction or subjective

## Usage Tips

✅ **DO**:
- Copy the full YAML to Claude
- Paste the exact question text
- Trust the pattern rules
- Use the confidence score

❌ **DON'T**:
- Edit the YAML unless extending
- Paraphrase questions
- Second-guess high confidence answers
- Skip the reasoning field

## Quick Test

Try this test question:

```
Horizontal bar charts are preferable when category labels are long. True or False?
```

Expected:
```yaml
answer: TRUE
confidence: 0.95
reason: "no rotation needed"
```

## File Structure

```
flamelang-zybooks-solver.yaml     ← Main solver specification
FLAMELANG_ZYBOOKS_SOLVER.md       ← Full documentation
flamelang-examples.yaml           ← Test cases and examples
flamelang-quick-reference.md      ← This file
```

## Extending the Solver

To add a new pattern:

```yaml
# In layer_3_rules, add to appropriate section:
your_new_rule:
  - pattern: "describe the pattern"
    answer: YOUR_ANSWER
    reason: "one line explanation"
```

## Support

- **Full Docs**: See `FLAMELANG_ZYBOOKS_SOLVER.md`
- **Test Cases**: See `flamelang-examples.yaml`
- **Questions**: Open an issue on GitHub

---

**Built with 🔥 by Strategickhaos DAO LLC**

*Speed > Verbosity. Trust the patterns.*
