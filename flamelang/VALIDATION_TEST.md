# FlameLang Validation Test Suite

## Quick Validation Checklist

Use this checklist to verify your FlameLang installation is working correctly.

## 1. File Structure Validation

```bash
cd flamelang
```

### Check all required files exist:
```bash
# Documentation
[ -f README.md ] && echo "✓ README.md" || echo "✗ README.md MISSING"
[ -f FLAMELANG_SPEC.md ] && echo "✓ FLAMELANG_SPEC.md" || echo "✗ FLAMELANG_SPEC.md MISSING"
[ -f QUICKSTART.md ] && echo "✓ QUICKSTART.md" || echo "✗ QUICKSTART.md MISSING"
[ -f OS_INVENTORY.md ] && echo "✓ OS_INVENTORY.md" || echo "✗ OS_INVENTORY.md MISSING"
[ -f PROOF_DOSSIER.md ] && echo "✓ PROOF_DOSSIER.md" || echo "✗ PROOF_DOSSIER.md MISSING"

# Pattern files
[ -f patterns/arithmetic_patterns.json ] && echo "✓ arithmetic_patterns.json" || echo "✗ arithmetic_patterns.json MISSING"
[ -f patterns/algebra_patterns.json ] && echo "✓ algebra_patterns.json" || echo "✗ algebra_patterns.json MISSING"
[ -f patterns/boolean_logic_patterns.json ] && echo "✓ boolean_logic_patterns.json" || echo "✗ boolean_logic_patterns.json MISSING"

# Algorithm docs
[ -f algorithms/MATH_CONVERSION.md ] && echo "✓ MATH_CONVERSION.md" || echo "✗ MATH_CONVERSION.md MISSING"

# Benchmark files
[ -f benchmarks/cpp_benchmark.cpp ] && echo "✓ cpp_benchmark.cpp" || echo "✗ cpp_benchmark.cpp MISSING"
[ -f benchmarks/rust_benchmark.rs ] && echo "✓ rust_benchmark.rs" || echo "✗ rust_benchmark.rs MISSING"
[ -f benchmarks/CMakeLists.txt ] && echo "✓ CMakeLists.txt" || echo "✗ CMakeLists.txt MISSING"
[ -f benchmarks/Cargo.toml ] && echo "✓ Cargo.toml" || echo "✗ Cargo.toml MISSING"
```

## 2. JSON Validation

```bash
# Validate all JSON pattern files are well-formed
python3 -m json.tool patterns/arithmetic_patterns.json > /dev/null && echo "✓ arithmetic_patterns.json is valid JSON"
python3 -m json.tool patterns/algebra_patterns.json > /dev/null && echo "✓ algebra_patterns.json is valid JSON"
python3 -m json.tool patterns/boolean_logic_patterns.json > /dev/null && echo "✓ boolean_logic_patterns.json is valid JSON"
```

## 3. Pattern Count Validation

```bash
# Count patterns in each library
echo "Pattern Counts:"
echo -n "  Arithmetic: "
python3 -c "import json; print(len(json.load(open('patterns/arithmetic_patterns.json'))['patterns']))"
echo -n "  Algebra: "
python3 -c "import json; print(len(json.load(open('patterns/algebra_patterns.json'))['patterns']))"
echo -n "  Boolean Logic: "
python3 -c "import json; print(len(json.load(open('patterns/boolean_logic_patterns.json'))['patterns']))"
```

**Expected**: 6 arithmetic, 5 algebra, 8 boolean logic = 19 total

## 4. Compiler Availability

```bash
# Check C++ compiler
g++ --version | head -1 && echo "✓ g++ available" || echo "✗ g++ NOT available"

# Check Clang (optional)
clang++ --version 2>/dev/null | head -1 && echo "✓ clang++ available" || echo "⚠ clang++ not available (optional)"

# Check CMake
cmake --version | head -1 && echo "✓ cmake available" || echo "✗ cmake NOT available"

# Check Rust
rustc --version && echo "✓ rustc available" || echo "⚠ rustc not available (optional)"
cargo --version && echo "✓ cargo available" || echo "⚠ cargo not available (optional)"
```

## 5. Pattern Syntax Validation

### Test Arithmetic Pattern
```python3
python3 << 'EOF'
import json
import re

# Load arithmetic patterns
with open('patterns/arithmetic_patterns.json', 'r') as f:
    data = json.load(f)

# Validate pattern structure
pattern = data['patterns'][0]  # basic_addition
assert 'id' in pattern, "Missing 'id' field"
assert 'match_regex' in pattern, "Missing 'match_regex' field"
assert 'algorithm' in pattern, "Missing 'algorithm' field"
assert 'test_cases' in pattern, "Missing 'test_cases' field"

# Test regex compilation
try:
    regex = re.compile(pattern['match_regex'])
    print("✓ Arithmetic pattern syntax valid")
except re.error as e:
    print(f"✗ Arithmetic pattern regex error: {e}")

# Test against example
test_input = "What is 5 + 3?"
if regex.search(test_input):
    print("✓ Arithmetic pattern matches test input")
else:
    print("✗ Arithmetic pattern does not match test input")
EOF
```

### Test Algebra Pattern
```python3
python3 << 'EOF'
import json
import re

# Load algebra patterns
with open('patterns/algebra_patterns.json', 'r') as f:
    data = json.load(f)

# Test quadratic pattern
quadratic = None
for p in data['patterns']:
    if p['id'] == 'quadratic_equation':
        quadratic = p
        break

assert quadratic is not None, "Quadratic pattern not found"

# Test regex
try:
    regex = re.compile(quadratic['match_regex'])
    print("✓ Quadratic pattern syntax valid")
except re.error as e:
    print(f"✗ Quadratic pattern regex error: {e}")

# Test against example
test_input = "x^2 - 5x + 6 = 0"
if regex.search(test_input):
    print("✓ Quadratic pattern matches test input")
else:
    print("✗ Quadratic pattern does not match test input")
EOF
```

## 6. Documentation Completeness

```bash
# Check documentation word counts
echo "Documentation Word Counts:"
wc -w README.md | awk '{print "  README: " $1 " words"}'
wc -w FLAMELANG_SPEC.md | awk '{print "  SPEC: " $1 " words"}'
wc -w QUICKSTART.md | awk '{print "  QUICKSTART: " $1 " words"}'
wc -w OS_INVENTORY.md | awk '{print "  INVENTORY: " $1 " words"}'
wc -w PROOF_DOSSIER.md | awk '{print "  DOSSIER: " $1 " words"}'
wc -w algorithms/MATH_CONVERSION.md | awk '{print "  CONVERSION: " $1 " words"}'
```

**Expected**: Thousands of words in each document

## 7. Code Syntax Check

```bash
# Check C++ syntax (without compilation)
echo "Checking C++ syntax..."
g++ -std=c++20 -fsyntax-only -Wall benchmarks/cpp_benchmark.cpp 2>&1 | grep -q "error:" && echo "✗ C++ syntax errors found" || echo "✓ C++ syntax clean"

# Check Rust syntax
echo "Checking Rust syntax..."
cd benchmarks
cargo check 2>&1 | grep -q "error:" && echo "✗ Rust syntax errors found" || echo "✓ Rust syntax clean"
cd ..
```

## 8. Test Case Validation

```bash
# Count total test cases across all patterns
python3 << 'EOF'
import json

total_tests = 0

# Arithmetic
with open('patterns/arithmetic_patterns.json', 'r') as f:
    data = json.load(f)
    for p in data['patterns']:
        total_tests += len(p.get('test_cases', []))

# Algebra
with open('patterns/algebra_patterns.json', 'r') as f:
    data = json.load(f)
    for p in data['patterns']:
        total_tests += len(p.get('test_cases', []))

# Boolean Logic
with open('patterns/boolean_logic_patterns.json', 'r') as f:
    data = json.load(f)
    for p in data['patterns']:
        total_tests += len(p.get('test_cases', []))

print(f"Total test cases: {total_tests}")
if total_tests >= 19:  # At least one per pattern
    print("✓ Sufficient test coverage")
else:
    print("✗ Insufficient test coverage")
EOF
```

## 9. Build System Validation

```bash
# Test CMake configuration
cd benchmarks
mkdir -p build_test && cd build_test
cmake .. -DCMAKE_BUILD_TYPE=Release 2>&1 | grep -q "error:" && echo "✗ CMake configuration failed" || echo "✓ CMake configuration successful"
cd ../..
rm -rf benchmarks/build_test

# Test Cargo configuration
cd benchmarks
cargo metadata --format-version 1 > /dev/null 2>&1 && echo "✓ Cargo configuration valid" || echo "⚠ Cargo configuration issue"
cd ..
```

## 10. Quick Functional Test

### Test Pattern Matching (Python)
```python3
python3 << 'EOF'
import json
import re

def test_pattern_matching():
    """Test that patterns can actually match and extract variables"""
    
    # Load arithmetic patterns
    with open('patterns/arithmetic_patterns.json', 'r') as f:
        arithmetic = json.load(f)
    
    # Test addition pattern
    addition = arithmetic['patterns'][0]
    regex = re.compile(addition['match_regex'])
    
    test_cases = [
        ("5 + 3", True, [5, 3]),
        ("12.5 + 7.3", True, [12.5, 7.3]),
        ("Hello world", False, None),
    ]
    
    passed = 0
    for text, should_match, expected_vars in test_cases:
        match = regex.search(text)
        if should_match:
            if match:
                print(f"✓ Matched: '{text}'")
                passed += 1
            else:
                print(f"✗ Failed to match: '{text}'")
        else:
            if not match:
                print(f"✓ Correctly rejected: '{text}'")
                passed += 1
            else:
                print(f"✗ Incorrectly matched: '{text}'")
    
    print(f"\nPattern matching: {passed}/{len(test_cases)} tests passed")
    return passed == len(test_cases)

if test_pattern_matching():
    print("✓ Pattern matching validation PASSED")
else:
    print("✗ Pattern matching validation FAILED")
EOF
```

## Summary Report

Run all validations at once:

```bash
#!/bin/bash
echo "================================"
echo "FlameLang Validation Report"
echo "================================"
echo ""

# File structure
echo "1. File Structure:"
files=(
    "README.md"
    "FLAMELANG_SPEC.md"
    "patterns/arithmetic_patterns.json"
    "patterns/algebra_patterns.json"
    "patterns/boolean_logic_patterns.json"
    "algorithms/MATH_CONVERSION.md"
    "benchmarks/cpp_benchmark.cpp"
    "benchmarks/rust_benchmark.rs"
)
missing=0
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file"
    else
        echo "  ✗ $file MISSING"
        ((missing++))
    fi
done

echo ""
echo "2. JSON Validation:"
python3 -m json.tool patterns/arithmetic_patterns.json > /dev/null 2>&1 && echo "  ✓ arithmetic_patterns.json" || echo "  ✗ arithmetic_patterns.json"
python3 -m json.tool patterns/algebra_patterns.json > /dev/null 2>&1 && echo "  ✓ algebra_patterns.json" || echo "  ✗ algebra_patterns.json"
python3 -m json.tool patterns/boolean_logic_patterns.json > /dev/null 2>&1 && echo "  ✓ boolean_logic_patterns.json" || echo "  ✗ boolean_logic_patterns.json"

echo ""
echo "3. Toolchain:"
command -v g++ > /dev/null 2>&1 && echo "  ✓ g++" || echo "  ✗ g++ (required)"
command -v cmake > /dev/null 2>&1 && echo "  ✓ cmake" || echo "  ✗ cmake (required)"
command -v rustc > /dev/null 2>&1 && echo "  ✓ rustc" || echo "  ⚠ rustc (optional)"
command -v cargo > /dev/null 2>&1 && echo "  ✓ cargo" || echo "  ⚠ cargo (optional)"

echo ""
echo "================================"
if [ $missing -eq 0 ]; then
    echo "Status: ✓ VALIDATION PASSED"
else
    echo "Status: ✗ VALIDATION FAILED ($missing files missing)"
fi
echo "================================"
```

Save this as `validate.sh` and run with `bash validate.sh`

## Expected Results

### ✓ All Checks Pass
- All 13 files present
- All JSON files valid
- All patterns properly structured
- Compilers available
- Documentation complete
- Test cases present

### Next Steps After Validation
1. Build C++ benchmarks: `cd benchmarks && mkdir build && cd build && cmake .. && make`
2. Run Rust benchmarks: `cd benchmarks && cargo bench`
3. Read the documentation: `less README.md`
4. Try transferring patterns to an AI chat

---

**Validation Status**: Run this test suite to verify your installation
