# StrategicKhaos Compiler Tests

Test suite for the StrategicKhaos compiler.

## Running Tests

### Run All Tests

```bash
python3 compiler/tests/test_lexer.py
```

### Run with pytest (if available)

```bash
pytest compiler/tests/
```

## Test Coverage

### Lexer Tests (`test_lexer.py`)

- ✓ Simple token recognition
- ✓ Keyword identification
- ✓ Operator parsing
- ✓ String literals (single and double quotes)
- ✓ Number parsing (integers and floats)
- ✓ Comment handling
- ✓ Complex expressions
- ✓ Function definitions

### Parser Tests (Planned)

- AST construction
- Expression precedence
- Statement parsing
- Error recovery

### Semantic Tests (Planned)

- Type checking
- Scope analysis
- Undefined variable detection

### Codegen Tests (Planned)

- LLVM IR generation
- Bytecode generation

### Integration Tests (Planned)

- End-to-end compilation
- Example program execution
- Self-compilation (Stage 2+)

## Adding New Tests

1. Create test file: `test_<component>.py`
2. Import component to test
3. Write test functions (prefix with `test_`)
4. Run tests

Example:

```python
from src.lexer import Lexer, TokenType

def test_my_feature():
    source = "let x = 42;"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    assert tokens[0].type == TokenType.LET
    # More assertions...
```

---

*Testing is sovereignty validation.*
