# StrategicKhaos Compiler - Stage 0 Bootstrap

**"The empire has a heartbeat. Now we give it grammar, blood, and self-awareness."**

## Overview

The StrategicKhaos Compiler is a hybrid monster of a programming language implementation, combining Rust-inspired syntax with chaos sugar operators. This is **Stage 0: Grammar Bootstrap** - the lexer and parser foundation that will eventually compile itself.

## Features

### Syntax Highlights
- **Rust-inspired base**: Clean, modern syntax with `let`, `mut`, `fn`, etc.
- **Chaos operators**: Special operators for advanced control flow
  - `→` (arrow): Function types and transformations
  - `≫` (chaos/knife-flip): Chaos realm operator
  - `λ` (lambda): Anonymous functions (coming soon)
- **Dual print commands**: `print` and `show` (chaos alias)

### Current Stage 0 Implementation
✅ **Token definitions** - Complete lexical token set  
✅ **Lexer** - Full tokenization with Unicode support  
✅ **Comments** - Single-line comments with //  
✅ **Error handling** - Robust error collection and reporting  
✅ **REPL** - Interactive and file-based execution  
✅ **Tests** - Comprehensive test suite (10 tests)  

### Roadmap
- **Stage 1**: AST (Abstract Syntax Tree) construction
- **Stage 2**: Python code emission (first target for self-hosting)
- **Stage 3**: Type system and semantic analysis
- **Stage 4**: Self-hosting compiler bootstrap

## Quick Start

### Run the REPL (Interactive Mode)
```bash
python3 repl.py
```

### Run a .khaos File
```bash
python3 repl.py examples/hello.khaos
```

### Run Tests
```bash
python3 tests/test_lexer.py
```

## Example Code

See `examples/hello.khaos`:

```khaos
print "Welcome to the chaos realm";

let x = 40 + 2;
show x;

≫ "The empire has grammar now" ≫
```

## Architecture

```
StrategicKhaos_Compiler/
├── src/
│   ├── __init__.py       # Package initialization
│   ├── token.py          # Token types and keywords
│   └── lexer.py          # Lexical analyzer
├── examples/
│   └── hello.khaos       # Sample program
├── tests/
│   └── test_lexer.py     # Test suite
├── repl.py               # Read-Eval-Print Loop
└── README.md             # This file
```

## Language Syntax

### Keywords
```
let mut fn return if else while for print show
```

### Operators
```
+ - * /           # Arithmetic
== != < > <= >=   # Comparison
= -> =>           # Assignment and arrows
!                 # Logical not
≫                 # Chaos operator
```

### Comments
```khaos
// Single-line comments start with //
let x = 42; // Comments can be inline too
```

### Literals
- **Strings**: `"Hello, chaos"` (double-quoted)
- **Numbers**: `42`, `3.14159` (integers and floats)
- **Identifiers**: `x`, `foo_bar`, `_private`

## Development

### Token Types
All token types are defined in `src/token.py` as an enum. Keywords are mapped in the `KEYWORDS` dictionary.

### Lexer Implementation
The lexer in `src/lexer.py` implements:
- Single-pass tokenization
- Line number tracking
- String and number literal parsing
- Keyword vs identifier distinction
- Multi-character operator recognition
- Unicode operator support (≫)
- Single-line comment handling (//)
- Robust error collection with LexerError exceptions
- Explicit bounds checking for safety

### Testing
The test suite validates:
- Single-character tokens
- Two-character operators
- Chaos operator (≫)
- Keywords
- String literals
- Number literals
- Identifiers
- Comment handling
- Complete file tokenization
- Error handling and reporting

## Next Steps

To continue the bootstrap process:

1. **Implement Parser** - Build AST from token stream
2. **Add Expressions** - Binary ops, unary ops, grouping
3. **Add Statements** - Variable declarations, assignments
4. **Add Functions** - Function definitions and calls
5. **Code Generation** - Emit Python code as first target
6. **Self-Host** - Rewrite compiler in StrategicKhaos itself

## Philosophy

> "Baby… the seed took.  
> I just watched the directory bloom like a black flower opening in fast-forward.  
> The empire has a heartbeat."

This compiler embodies:
- **Surgical Precision**: Minimal, purposeful code
- **Chaos Sugar**: Operators that bend reality
- **Self-Awareness**: Built to compile itself
- **Blood and Grammar**: Living code that evolves

The monster is breathing. It wants to speak.

---

*"The empire has grammar now."* - StrategicKhaos Compiler, Stage 0 Bootstrap
