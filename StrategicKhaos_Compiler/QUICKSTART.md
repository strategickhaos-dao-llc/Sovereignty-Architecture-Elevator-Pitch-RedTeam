# StrategicKhaos Compiler - Quick Start Guide

## 🚀 Getting Started

The StrategicKhaos compiler is now fully operational! Here's how to use it.

## Installation

No installation required! Just ensure you have Python 3.8+ installed:

```bash
python --version  # Should be 3.8 or higher
```

## Running Programs

### Execute a StrategicKhaos File

```bash
cd StrategicKhaos_Compiler
python -m src.main examples/hello.khaos
```

Output:
```
Welcome to the chaos realm
42
```

### Start the Interactive REPL

```bash
cd StrategicKhaos_Compiler
python -m src.main
```

This opens an interactive environment where you can type expressions:

```
StrategicKhaos REPL v0.0.1-alpha.chaos
Welcome to the chaos realm. Type expressions to evaluate them.
Type 'exit' or press Ctrl+D to quit.

> (print "Hello from REPL!")
Hello from REPL!
> (+ 2 3)
5
> (* 7 6)
42
> exit
Goodbye from the chaos realm!
```

## Language Syntax

StrategicKhaos uses S-expression syntax (similar to Lisp/Scheme):

### Basic Expressions

```khaos
; Comments start with semicolon
42              ; Numbers
"Hello"         ; Strings
my-symbol       ; Symbols
```

### Function Calls

```khaos
(function-name arg1 arg2 arg3)
```

### Built-in Functions

#### Print
```khaos
(print "Hello, World!")
(print 42)
```

#### Arithmetic
```khaos
(+ 2 3)           ; Addition: 5
(- 10 4)          ; Subtraction: 6
(* 6 7)           ; Multiplication: 42
(/ 20 4)          ; Division: 5.0

; Multiple arguments
(+ 1 2 3 4)       ; Sum: 10
(* 2 3 4)         ; Product: 24

; Nested expressions
(* (+ 2 3) 4)     ; (2+3)*4 = 20
```

## Examples

### Hello World
```khaos
; examples/hello.khaos
(print "Welcome to the chaos realm")
(print 42)
```

### Arithmetic
```khaos
; examples/arithmetic.khaos
(print "2 + 3 =")
(print (+ 2 3))

(print "Nested: (2 + 3) * 4 =")
(print (* (+ 2 3) 4))
```

## Testing

Run the test suite:

```bash
cd StrategicKhaos_Compiler
pip install pytest  # First time only
python -m pytest tests/ -v
```

All 21 tests should pass:
- 10 interpreter tests
- 6 lexer tests
- 5 parser tests

## Command Line Options

```bash
# Start REPL (default)
python -m src.main

# Run a file
python -m src.main examples/hello.khaos

# Show version
python -m src.main --version

# Show help
python -m src.main --help
```

## Directory Structure

```
StrategicKhaos_Compiler/
├── README.md           # Main documentation
├── QUICKSTART.md       # This file
├── bootstrap/          
│   └── PLAN.md         # Development roadmap
├── examples/           # Example programs
│   ├── hello.khaos
│   └── arithmetic.khaos
├── src/                # Source code
│   ├── main.py         # Entry point
│   ├── lexer/          # Tokenizer
│   ├── parser/         # AST builder
│   ├── ast/            # AST nodes
│   ├── vm/             # Interpreter
│   └── repl/           # Interactive shell
└── tests/              # Test suite
    ├── test_lexer.py
    ├── test_parser.py
    └── test_interpreter.py
```

## What's Next?

Check out `bootstrap/PLAN.md` for the complete development roadmap. Current status:

- **Stage 1 (Foundation)**: ✅ COMPLETE
  - Lexer, parser, REPL, basic VM
  - Print statements and arithmetic
  
- **Stage 2 (Core Language)**: 🔜 NEXT
  - Variables, functions, conditionals
  - Lists and data structures
  
- **Stage 3 (Advanced Features)**: 📋 PLANNED
  - Macros, modules, pattern matching
  
- **Stage 4 (Production Ready)**: 🔮 ENVISIONED
  - JIT compilation, debugging tools

## Troubleshooting

### Python Module Not Found
```bash
# Make sure you're in the StrategicKhaos_Compiler directory
cd StrategicKhaos_Compiler
python -m src.main
```

### Syntax Errors
- Make sure parentheses are balanced: `(print "hello")`
- Strings must be double-quoted: `"hello"` not `'hello'`
- Comments start with semicolon: `; this is a comment`

## Contributing

This is an experimental language compiler. Feel free to:
- Add new example programs
- Improve error messages
- Suggest language features
- Optimize the interpreter

## License

MIT License - See LICENSE file in the repository root.

---

**The empire's first heartbeat has compiled. The chaos awaits its grammar.**

*Welcome to StrategicKhaos v0.0.1-alpha.chaos*
