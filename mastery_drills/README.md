# Mastery Drills - Data Analysis Exercises

This directory contains structured data analysis exercises designed to build pattern recognition and compiler-level thinking.

## Available Drills

### Section 1.5.8: Preterm Births Analysis

**File:** `preterm_births_1_5_8.yaml`

**Difficulty:** Intermediate  
**Bloom Level:** Analyzing  
**Estimated Time:** 15 minutes

**Concepts Covered:**
- Stacked bar chart decomposition
- Statistical aggregation patterns
- Delta/gradient calculations
- Extremum finding (MAX operations)

**Answer Key:**
- Q1: `10.40%` — Total preterm rate (early 3.20% + late 7.20%)
- Q2: `0.22%` — Increase in preterm rate (9.85% - 9.63%)
- Q3: `Over 40` — Age group with highest late preterm rate (10.37%)

**FlameLang Pattern:** Stacked Bar Decomposition
- **SUM** → accumulator pattern
- **DIFF** → gradient/derivative
- **MAX** → comparator tree

## Pattern Philosophy

> "The grade is temporary, the patterns are permanent."

These exercises focus on recognizing the fundamental reduction operations that underlie all data analysis:

1. **SUM/Aggregation** - Accumulator patterns that combine multiple values
2. **DIFF/Delta** - Derivative patterns that measure change
3. **MAX/MIN/Extremum** - Comparison patterns that find optimal values

Understanding these three operations at a compiler level unlocks the ability to reason about any statistical analysis or data transformation pipeline.

## Usage

### View Exercise

```bash
cat mastery_drills/preterm_births_1_5_8.yaml
```

### Validate YAML

```bash
python3 -c "import yaml; print(yaml.safe_load(open('mastery_drills/preterm_births_1_5_8.yaml')))"
```

### Parse Answers

```bash
python3 -c "
import yaml
data = yaml.safe_load(open('mastery_drills/preterm_births_1_5_8.yaml'))
print('Answers:')
for q, answer in data['answers'].items():
    print(f'  {q}: {answer}')
"
```

## Integration with Mastery System

This directory complements the shell-based mastery drills in `mastery-drills.sh`. While the shell drills focus on operational CLI mastery, these YAML-based exercises focus on analytical thinking and pattern recognition.

## Contributing

When adding new drills:
1. Follow the established YAML structure
2. Include detailed explanations for each answer
3. Map questions to fundamental operations (SUM, DIFF, MAX, etc.)
4. Add compiler/pattern insights
5. Validate YAML syntax before committing

## Fire 🔥

> **10.40% → 0.22% → Over 40**

You're not getting F+, you're getting compiler knowledge.
