# Mathematical Expression to FlameLang Algorithm Conversion

## Overview
This document provides comprehensive rules for converting mathematical expressions, equations, and logical statements into FlameLang algorithms. This is the core capability that enables automated question solving.

## Conversion Philosophy

**Principle**: Every mathematical operation has a direct FlameLang equivalent that can be:
1. Pattern matched from natural language
2. Executed algorithmically
3. Validated for correctness
4. Transferred between AI instances

---

## 1. Arithmetic Conversions

### 1.1 Basic Operations

#### Addition
```
Mathematical Notation: a + b
FlameLang Algorithm: add(a, b)
Implementation: return a + b

Example:
  Math: "5 + 3"
  FlameLang: eval(add(5, 3))
  Result: 8
```

#### Subtraction
```
Mathematical Notation: a - b
FlameLang Algorithm: sub(a, b)
Implementation: return a - b

Example:
  Math: "10 - 4"
  FlameLang: eval(sub(10, 4))
  Result: 6
```

#### Multiplication
```
Mathematical Notation: a × b (or a * b)
FlameLang Algorithm: mul(a, b)
Implementation: return a * b

Example:
  Math: "6 × 7"
  FlameLang: eval(mul(6, 7))
  Result: 42
```

#### Division
```
Mathematical Notation: a ÷ b (or a / b)
FlameLang Algorithm: div(a, b)
Implementation: 
  if b == 0: error("division by zero")
  return a / b

Example:
  Math: "20 ÷ 4"
  FlameLang: eval(div(20, 4))
  Result: 5
```

### 1.2 Order of Operations (PEMDAS/BODMAS)

```
Mathematical: 2 + 3 × 4
Parse Tree:
    +
   / \
  2   ×
     / \
    3   4

FlameLang Algorithm:
  step1: mul(3, 4) -> 12
  step2: add(2, 12) -> 14
  
Compact Form: eval(add(2, mul(3, 4)))
```

#### Complex Expression Example
```
Mathematical: (2 + 3) × (4 - 1)
Parse Tree:
       ×
      / \
     +   -
    / \ / \
   2  3 4  1

FlameLang Algorithm:
  step1: add(2, 3) -> 5
  step2: sub(4, 1) -> 3
  step3: mul(5, 3) -> 15

Compact Form: eval(mul(add(2, 3), sub(4, 1)))
```

### 1.3 Percentage Operations

```
Mathematical: "What is P% of N?"
Formula: (P / 100) × N
FlameLang Algorithm: mul(N, div(P, 100))

Example:
  Math: "25% of 80"
  FlameLang: eval(mul(80, div(25, 100)))
  Result: 20
```

### 1.4 Exponentiation

```
Mathematical: a^b
FlameLang Algorithm: pow(a, b)
Implementation: return a ** b

Example:
  Math: "2^3"
  FlameLang: eval(pow(2, 3))
  Result: 8
```

---

## 2. Algebraic Conversions

### 2.1 Linear Equations

#### Standard Form: ax + b = c
```
Mathematical: 2x + 3 = 7
Goal: Solve for x

Algebraic Steps:
  1. 2x + 3 = 7
  2. 2x = 7 - 3
  3. 2x = 4
  4. x = 4 / 2
  5. x = 2

FlameLang Algorithm:
  solve_linear(a, b, c):
    if a == 0: error("not linear")
    return (c - b) / a

Example:
  Math: "2x + 3 = 7"
  FlameLang: solve_linear(2, 3, 7)
  Result: 2
```

### 2.2 Quadratic Equations

#### Standard Form: ax² + bx + c = 0
```
Mathematical: x² - 5x + 6 = 0
Goal: Solve for x

Algebraic Formula: x = (-b ± √(b² - 4ac)) / 2a

FlameLang Algorithm:
  solve_quadratic(a, b, c):
    D = discriminant(a, b, c)
    if D < 0: return "no real solutions"
    sqrt_D = sqrt(D)
    x1 = (-b + sqrt_D) / (2 * a)
    x2 = (-b - sqrt_D) / (2 * a)
    return [x1, x2]
  
  discriminant(a, b, c):
    return b * b - 4 * a * c

Example:
  Math: "x² - 5x + 6 = 0"
  FlameLang: solve_quadratic(1, -5, 6)
  Result: [2, 3]
```

### 2.3 Systems of Equations

#### 2x2 System
```
Mathematical:
  Equation 1: a1*x + b1*y = c1
  Equation 2: a2*x + b2*y = c2

Method: Cramer's Rule
  D = a1*b2 - a2*b1
  Dx = c1*b2 - c2*b1
  Dy = a1*c2 - a2*c1
  x = Dx / D
  y = Dy / D

FlameLang Algorithm:
  solve_system_2x2(a1, b1, c1, a2, b2, c2):
    D = sub(mul(a1, b2), mul(a2, b1))
    if D == 0: error("no unique solution")
    Dx = sub(mul(c1, b2), mul(c2, b1))
    Dy = sub(mul(a1, c2), mul(a2, c1))
    x = div(Dx, D)
    y = div(Dy, D)
    return {x: x, y: y}

Example:
  Math: "2x + y = 5 and x - y = 1"
  FlameLang: solve_system_2x2(2, 1, 5, 1, -1, 1)
  Result: {x: 2, y: 1}
```

### 2.4 Polynomial Operations

#### Factorization
```
Mathematical: x² + 5x + 6
Goal: Factor as (x + a)(x + b)

Method: Find two numbers that multiply to c and add to b
  For x² + 5x + 6:
  Need: m * n = 6 and m + n = 5
  Answer: m = 2, n = 3
  Result: (x + 2)(x + 3)

FlameLang Algorithm:
  factorize_quadratic(a, b, c):
    if a != 1: return "use general method"
    factors = find_factor_pairs(c)
    for [m, n] in factors:
      if m + n == b:
        return format("(x + {})(x + {})", m, n)
    return "cannot factor"

Example:
  Math: "Factor x² + 5x + 6"
  FlameLang: factorize_quadratic(1, 5, 6)
  Result: "(x + 2)(x + 3)"
```

### 2.5 Exponential and Logarithmic

#### Exponential Equations
```
Mathematical: b^x = N
Goal: Solve for x

Method: Apply logarithm
  x = log_b(N)

FlameLang Algorithm:
  solve_exponential(base, result):
    if base <= 0 or base == 1: error("invalid base")
    if result <= 0: error("invalid result")
    return log(result) / log(base)

Example:
  Math: "2^x = 8"
  FlameLang: solve_exponential(2, 8)
  Result: 3
```

---

## 3. Calculus Conversions

### 3.1 Derivatives

#### Power Rule: d/dx(x^n) = n*x^(n-1)
```
Mathematical: d/dx(x³)
FlameLang Algorithm:
  derivative_power(n):
    return format("{}*x^{}", n, n-1)

Example:
  Math: "d/dx(x³)"
  FlameLang: derivative_power(3)
  Result: "3*x^2"
```

#### Product Rule: d/dx(f*g) = f'*g + f*g'
```
Mathematical: d/dx(x² * sin(x))
FlameLang Algorithm:
  derivative_product(f, g, f_prime, g_prime):
    return add(mul(f_prime, g), mul(f, g_prime))

Example representation:
  f = x^2, f' = 2x
  g = sin(x), g' = cos(x)
  Result: 2x*sin(x) + x²*cos(x)
```

### 3.2 Integrals

#### Power Rule: ∫x^n dx = x^(n+1)/(n+1) + C
```
Mathematical: ∫x² dx
FlameLang Algorithm:
  integral_power(n):
    if n == -1: return "ln|x| + C"
    return format("x^{}/({})+C", n+1, n+1)

Example:
  Math: "∫x² dx"
  FlameLang: integral_power(2)
  Result: "x^3/3 + C"
```

---

## 4. Boolean Logic Conversions

### 4.1 Basic Operations

#### AND (Conjunction)
```
Mathematical: A ∧ B
Truth Table:
  A | B | A∧B
  T | T | T
  T | F | F
  F | T | F
  F | F | F

FlameLang Algorithm: and(A, B)
Implementation: return A && B
```

#### OR (Disjunction)
```
Mathematical: A ∨ B
Truth Table:
  A | B | A∨B
  T | T | T
  T | F | T
  F | T | T
  F | F | F

FlameLang Algorithm: or(A, B)
Implementation: return A || B
```

#### NOT (Negation)
```
Mathematical: ¬A
Truth Table:
  A | ¬A
  T | F
  F | T

FlameLang Algorithm: not(A)
Implementation: return !A
```

#### XOR (Exclusive OR)
```
Mathematical: A ⊕ B
Truth Table:
  A | B | A⊕B
  T | T | F
  T | F | T
  F | T | T
  F | F | F

FlameLang Algorithm: xor(A, B)
Implementation: return A != B
```

### 4.2 Complex Logic Expressions

#### De Morgan's Laws
```
Mathematical: ¬(A ∧ B) = (¬A) ∨ (¬B)
FlameLang Algorithm:
  demorgan_and(A, B):
    return or(not(A), not(B))

Mathematical: ¬(A ∨ B) = (¬A) ∧ (¬B)
FlameLang Algorithm:
  demorgan_or(A, B):
    return and(not(A), not(B))
```

#### Implication
```
Mathematical: A → B (if A then B)
Equivalent: ¬A ∨ B

FlameLang Algorithm:
  implies(A, B):
    return or(not(A), B)

Truth Table:
  A | B | A→B
  T | T | T
  T | F | F
  F | T | T
  F | F | T
```

### 4.3 Logic Simplification

```
Identity Laws:
  A ∧ T = A  =>  and(A, true) => A
  A ∨ F = A  =>  or(A, false) => A

Domination Laws:
  A ∧ F = F  =>  and(A, false) => false
  A ∨ T = T  =>  or(A, true) => true

Idempotent Laws:
  A ∧ A = A  =>  and(A, A) => A
  A ∨ A = A  =>  or(A, A) => A

Double Negation:
  ¬(¬A) = A  =>  not(not(A)) => A
```

---

## 5. Pattern Recognition to Algorithm Mapping

### 5.1 Question Type Detection

```
FlameLang Decision Tree:

1. Parse question text
2. Check for mathematical operators
   - If contains +, -, *, /: ARITHMETIC
   - If contains x, =, equation format: ALGEBRA
   - If contains AND, OR, NOT, TRUE/FALSE: BOOLEAN_LOGIC
   - If contains derivative, integral: CALCULUS
3. Within category, match specific pattern
4. Extract variables
5. Apply algorithm
6. Return result
```

### 5.2 Variable Extraction

```
Pattern: "What is 5 + 3?"
Regex: (\d+)\s*\+\s*(\d+)
Extract: [5, 3]
Algorithm: add(5, 3)
Result: 8

Pattern: "Solve 2x + 3 = 7"
Regex: (\d+)x\s*\+\s*(\d+)\s*=\s*(\d+)
Extract: [2, 3, 7]
Algorithm: solve_linear(2, 3, 7)
Result: 2
```

---

## 6. Transferable Algorithm Templates

### 6.1 Generic Solver Template

```json
{
  "pattern_id": "<unique_id>",
  "category": "<arithmetic|algebra|calculus|boolean>",
  "match_pattern": "<regex_or_semantic>",
  "variables": ["<var1>", "<var2>", "..."],
  "algorithm": {
    "steps": [
      "step1: extract_variables()",
      "step2: validate_input()",
      "step3: apply_formula()",
      "step4: validate_output()"
    ],
    "formula": "<mathematical_formula>",
    "flamelang_code": "<executable_code>"
  },
  "test_cases": [
    {
      "input": "<example_question>",
      "expected": "<expected_result>"
    }
  ]
}
```

### 6.2 Copy-Paste Ready Patterns

For sharing between AI chats, use this format:

```
FLAMELANG PATTERN: QUADRATIC_SOLVER
================================
Category: Algebra
Pattern: x^2 coefficient equation
Formula: x = (-b ± √(b²-4ac)) / 2a

Algorithm:
1. Extract a, b, c from ax² + bx + c = 0
2. Calculate D = b² - 4ac
3. If D < 0: return "no real solutions"
4. x1 = (-b + √D) / 2a
5. x2 = (-b - √D) / 2a
6. Return [x1, x2]

Test: x² - 5x + 6 = 0 → [2, 3] ✓

Paste this into any AI chat to enable quadratic solving!
================================
```

---

## 7. Implementation Best Practices

### 7.1 Error Handling

```
Always validate:
- Division by zero
- Negative discriminants
- Invalid input formats
- Out of range values

Example FlameLang:
  algorithm safe_divide(a, b):
    validate b != 0, "Division by zero"
    return a / b
```

### 7.2 Numerical Precision

```
Use appropriate precision:
- Integer operations: exact
- Floating point: be aware of rounding
- Symbolic: maintain exact forms when possible

Example:
  1/3 + 1/3 + 1/3 should equal 1 exactly
  Use rational arithmetic: add(frac(1,3), frac(1,3), frac(1,3))
```

### 7.3 Performance Optimization

```
Cache common calculations:
- Factorials
- Powers of 2
- Trigonometric values
- Common quadratic solutions

Optimize regex patterns:
- Most specific patterns first
- Compile once, use many times
```

---

## 8. Usage Examples

### Example 1: Arithmetic
```
Input: "Calculate 15 + 27"
Pattern Match: arithmetic_addition
Variables: {operand1: 15, operand2: 27}
Algorithm: eval(add(15, 27))
Output: 42
```

### Example 2: Quadratic
```
Input: "Solve x² + 2x - 8 = 0"
Pattern Match: quadratic_equation
Variables: {a: 1, b: 2, c: -8}
Algorithm: solve_quadratic(1, 2, -8)
Calculation:
  D = 4 - 4(1)(-8) = 4 + 32 = 36
  x1 = (-2 + 6) / 2 = 2
  x2 = (-2 - 6) / 2 = -4
Output: [2, -4]
```

### Example 3: Boolean Logic
```
Input: "Simplify NOT(A AND B)"
Pattern Match: demorgan_simplification
Variables: {expression: "¬(A ∧ B)"}
Algorithm: apply_demorgan(expression)
Transformation: ¬(A ∧ B) → (¬A) ∨ (¬B)
Output: "(NOT A) OR (NOT B)"
```

---

## Conclusion

This conversion system enables:
1. **Systematic** translation of math to algorithms
2. **Transferable** patterns between AI instances
3. **Verifiable** correctness through test cases
4. **Scalable** addition of new patterns
5. **Production-ready** implementation

Copy any pattern from this document into another AI chat, and it will immediately understand how to solve that category of problems!

---

**Version**: 1.0.0  
**Last Updated**: 2025-12-16  
**Status**: Production Ready
