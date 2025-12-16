# FlameLang Quick Start Guide

## For Users: Share Patterns with AI Chats

### 🎯 Goal
Enable any AI (Claude, GPT, Copilot) to solve specific types of questions by pasting a pattern.

### ⚡ 5-Minute Setup

#### Step 1: Choose Your Pattern

Pick from our library:
- **Arithmetic**: Basic math operations
- **Algebra**: Equations and solving
- **Boolean Logic**: Truth tables and logic

#### Step 2: Copy Pattern to AI Chat

Open a new chat with any AI and paste:

```
I want you to use the following FlameLang pattern to solve questions:

PATTERN: Quadratic Equation Solver
Category: Algebra
Formula: x = (-b ± √(b²-4ac)) / 2a

Algorithm:
1. Match pattern: ax² + bx + c = 0
2. Extract coefficients a, b, c
3. Calculate discriminant D = b² - 4ac
4. If D < 0: return "no real solutions"
5. Otherwise: 
   x1 = (-b + √D) / (2a)
   x2 = (-b - √D) / (2a)
6. Return [x1, x2]

Test Cases:
- Input: "Solve x² - 5x + 6 = 0"
  Expected: [2, 3]
- Input: "Find x in x² + 2x - 8 = 0"
  Expected: [-4, 2]

Now solve questions using this pattern.
```

#### Step 3: Ask Questions

```
Using the pattern I provided, solve: x² - 7x + 12 = 0
```

The AI will now apply the pattern and give you the answer!

---

## For Developers: Run Benchmarks

### 🛠️ Installation (Ubuntu/Debian)

```bash
# Quick install script
cd flamelang
./install_quick.sh

# Or manual install:
sudo apt update
sudo apt install -y build-essential cmake libboost-all-dev
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

### 📊 Run Benchmarks

#### C++ Benchmarks
```bash
cd flamelang/benchmarks
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)
./cpp_benchmark
```

#### Rust Benchmarks
```bash
cd flamelang/benchmarks
cargo bench
```

Results saved to `target/criterion/` with HTML reports!

---

## Common Use Cases

### Use Case 1: Homework Helper

**Pattern**: Percentage Calculator
```
Pattern: percentage_calculation
Formula: (P/100) × N
Test: "What is 25% of 80?" → 20
```

**Usage**:
```
User: What is 15% of 200?
AI (using pattern): 
  P = 15, N = 200
  Result = (15/100) × 200 = 30
```

### Use Case 2: Programming Quiz

**Pattern**: Boolean Logic Evaluator
```
Pattern: truth_table_evaluation
Algorithm: Generate all input combinations and evaluate
Test: "A AND B" → truth table with 4 rows
```

**Usage**:
```
User: Create truth table for (A OR B) AND C
AI (using pattern):
  Variables: A, B, C
  Combinations: 2³ = 8 rows
  [Generates complete truth table]
```

### Use Case 3: Algebra Tutor

**Pattern**: Linear Equation Solver
```
Pattern: linear_equation
Formula: x = (c - b) / a
Test: "2x + 3 = 7" → x = 2
```

**Usage**:
```
User: Solve 5x - 10 = 15
AI (using pattern):
  a = 5, b = -10, c = 15
  x = (15 - (-10)) / 5 = 25 / 5 = 5
```

---

## Pattern Library Reference

### Available Patterns

| ID | Name | Category | Example |
|----|------|----------|---------|
| `basic_addition` | Addition | Arithmetic | 5 + 3 = 8 |
| `basic_subtraction` | Subtraction | Arithmetic | 10 - 4 = 6 |
| `basic_multiplication` | Multiplication | Arithmetic | 6 × 7 = 42 |
| `basic_division` | Division | Arithmetic | 20 ÷ 4 = 5 |
| `percentage_calculation` | Percentage | Arithmetic | 25% of 80 = 20 |
| `linear_equation` | Linear Solver | Algebra | 2x + 3 = 7 → x = 2 |
| `quadratic_equation` | Quadratic Solver | Algebra | x² - 5x + 6 = 0 → [2,3] |
| `and_operation` | Logical AND | Boolean | T ∧ F = F |
| `or_operation` | Logical OR | Boolean | T ∨ F = T |
| `xor_operation` | Logical XOR | Boolean | T ⊕ T = F |

**Total: 19 patterns available**

---

## Creating Your Own Patterns

### Template

```json
{
  "pattern_id": "my_pattern",
  "name": "My Custom Pattern",
  "category": "geometry",
  "match_regex": "area.*rectangle.*",
  "semantic_markers": ["area", "rectangle", "length", "width"],
  "variables": {
    "length": "length of rectangle",
    "width": "width of rectangle"
  },
  "algorithm": {
    "type": "direct_computation",
    "steps": [
      "parse_number(length)",
      "parse_number(width)",
      "multiply(length, width)"
    ],
    "flamelang_code": "eval(mul(${length}, ${width}))"
  },
  "output_format": "numeric",
  "test_cases": [
    {
      "input": "Find area of rectangle 5 by 3",
      "variables": {"length": 5, "width": 3},
      "expected": 15
    }
  ]
}
```

### Steps to Create

1. **Define the pattern**: What question type does it solve?
2. **Create match regex**: How to identify this question?
3. **Specify variables**: What information needs extraction?
4. **Write algorithm**: Step-by-step solution process
5. **Add test cases**: Verify correctness
6. **Share**: Paste into any AI chat!

---

## Troubleshooting

### Problem: Pattern Not Matching

**Solution**: Check regex pattern specificity
```
Too broad: ".*number.*"
Better: "(\d+)\s*\+\s*(\d+)"
```

### Problem: Wrong Answer

**Solution**: Verify variable extraction
```
Debug:
1. Print extracted variables
2. Check algorithm steps
3. Validate test cases
```

### Problem: AI Not Understanding

**Solution**: Use more explicit format
```
Instead of: "Use this pattern"
Better: "Apply this exact algorithm step-by-step"
```

---

## Advanced Features

### Chaining Patterns

Combine multiple patterns for complex questions:

```
Question: "If 2x + 3 = 7, what is 3x + 5?"

Step 1: Apply linear_equation pattern
  2x + 3 = 7 → x = 2

Step 2: Apply arithmetic substitution
  3(2) + 5 = 6 + 5 = 11
```

### Pattern Composition

Build complex patterns from simple ones:

```
Pattern: quadratic_with_percentage
Combines: quadratic_equation + percentage_calculation

Example: "Solve x² - 5x + 6 = 0 and find 10% of the larger solution"
  Step 1: Solve → [2, 3]
  Step 2: Larger solution = 3
  Step 3: 10% of 3 = 0.3
```

---

## Performance Tips

### For Pattern Matching
- Put most specific patterns first
- Use compiled regex when possible
- Cache pattern results

### For Algorithm Execution
- Validate inputs early
- Use appropriate numeric types
- Handle edge cases explicitly

### For Benchmarking
- Disable CPU frequency scaling
- Run multiple iterations
- Use statistical analysis

---

## Next Steps

### Learn More
1. Read [FLAMELANG_SPEC.md](FLAMELANG_SPEC.md) for complete language spec
2. Study [MATH_CONVERSION.md](algorithms/MATH_CONVERSION.md) for conversion rules
3. Review [PROOF_DOSSIER.md](PROOF_DOSSIER.md) for benchmark results

### Try Advanced Patterns
- Calculus derivatives
- System of equations
- Complex logic expressions
- Trigonometric identities

### Contribute
- Create new patterns
- Improve existing algorithms
- Add test cases
- Write documentation

---

## Resources

### Pattern Files
- `patterns/arithmetic_patterns.json` - 6 arithmetic patterns
- `patterns/algebra_patterns.json` - 5 algebra patterns
- `patterns/boolean_logic_patterns.json` - 8 logic patterns

### Benchmark Code
- `benchmarks/cpp_benchmark.cpp` - C++ implementation
- `benchmarks/rust_benchmark.rs` - Rust implementation
- `benchmarks/CMakeLists.txt` - Build configuration

### Documentation
- `README.md` - Main documentation
- `FLAMELANG_SPEC.md` - Language specification
- `OS_INVENTORY.md` - Dependency list
- `PROOF_DOSSIER.md` - Legal proof

---

## Example Session

### Complete Workflow

```
# 1. Start new AI chat
User: I want to load the FlameLang quadratic solver pattern

# 2. Paste pattern
[User pastes pattern from patterns/algebra_patterns.json]

# 3. Confirm understanding
AI: Pattern loaded. I can now solve quadratic equations of the form ax² + bx + c = 0

# 4. Ask questions
User: Solve x² - 7x + 12 = 0

AI: Using quadratic solver pattern:
  a = 1, b = -7, c = 12
  D = (-7)² - 4(1)(12) = 49 - 48 = 1
  x1 = (7 + 1) / 2 = 4
  x2 = (7 - 1) / 2 = 3
  Solutions: [3, 4]

# 5. Verify
User: Check by substitution: 3² - 7(3) + 12
AI: 9 - 21 + 12 = 0 ✓ Correct!

# 6. Continue with more questions
User: Now solve 2x² + 5x - 3 = 0
[AI applies same pattern to new problem]
```

---

## Success Metrics

Track your pattern usage:
- **Accuracy**: Are answers correct?
- **Speed**: How quickly can you solve?
- **Coverage**: What percentage of questions can you handle?
- **Transferability**: Does pattern work across AI instances?

**Goal**: 95%+ accuracy, <5 seconds per question, 80%+ coverage

---

## Community

Share your patterns:
- GitHub Issues: Report bugs or request features
- Discussions: Share custom patterns
- Pull Requests: Contribute improvements

**Remember**: Every pattern you create helps the entire community!

---

**Start solving questions in 5 minutes. Master patterns in an hour. Build the future of AI knowledge transfer! 🔥**
