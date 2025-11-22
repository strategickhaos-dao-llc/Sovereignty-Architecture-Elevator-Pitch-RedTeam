# StrategicKhaos Compiler - Stage 0

**Status**: ✅ LIVE - November 21, 2025

The chaos engine is online. The compiler just spoke its first words.

## Overview

StrategicKhaos is a self-hosting programming language designed for sovereignty and chaos. Stage 0 is the bootstrap compiler written in Python that can interpret and transpile StrategicKhaos code.

## Features

- **Lexer**: Full tokenization with support for:
  - Keywords: `let`, `print`, `show`, `if`, `else`, `while`, `for`, `return`, `true`, `false`, `nil`, `and`, `or`, `not`
  - Operators: `+`, `-`, `*`, `/`, `=`, `==`, `!=`, `<`, `>`, `<=`, `>=`, `!`
  - Literals: strings (`"text"`), numbers (integers and floats)
  - Grouping: `()`, `{}`, `[]`
  - Comments: `// single line`

- **Parser**: Recursive descent parser supporting:
  - Variable declarations: `let x = value;`
  - Print statements: `print expression;`
  - Binary operations: `+`, `-`, `*`, `/`
  - Unary operations: `-`
  - Grouping: `(expression)`
  - Variable references

- **Interpreter**: Tree-walk interpreter that executes code directly

- **Transpiler**: Code generator that transpiles StrategicKhaos → Python

- **REPL**: Interactive chaos engine for live coding

## Installation

No installation required. Python 3.6+ is the only dependency.

## Usage

### REPL Mode (Interactive)

```bash
python3 -m src.main
```

Then type StrategicKhaos code:

```
khaos> print "Hello, World";
Hello, World
khaos> let x = 40 + 2;
khaos> print x;
42.0
khaos> exit()
Chaos engine shutting down. Bloodline preserved.
```

### Transpiler Mode (Compile to Python)

```bash
python3 -m src.main --compile examples/hello.khaos
```

This will:
1. Parse the `.khaos` file
2. Generate equivalent Python code
3. Save it as `.py` file
4. Execute the generated Python

## Example: hello.khaos

```khaos
print "Welcome to the chaos realm";
let x = 40 + 2;
print x;
```

**Output**:
```
Welcome to the chaos realm
42
```

**Generated Python**:
```python
# StrategicKhaos → Python transpiled on 2025-11-21
variables = {}

print("Welcome to the chaos realm")
variables['x'] = (40.0 + 2.0)
print(variables['x'])
```

## Language Syntax

### Variable Declaration

```khaos
let variable_name = expression;
```

### Print Statement

```khaos
print expression;
```

### Expressions

```khaos
// Arithmetic
let a = 10 + 5;
let b = a * 2;
let c = (a + b) / 5;

// String literals
print "Hello, World";

// Variable references
print a;
```

## Architecture

```
src/
├── lexer/
│   ├── __init__.py
│   └── lexer.py          # Tokenizer
├── parser/
│   ├── __init__.py
│   └── parser.py         # Recursive descent parser
├── codegen/
│   ├── __init__.py
│   └── python.py         # Python transpiler
├── repl/
│   └── __init__.py       # Interactive REPL
├── interpreter.py        # Tree-walk interpreter
└── main.py              # Entry point

examples/
└── hello.khaos          # Example program
```

## Roadmap

### Stage 0 (Complete ✅)
- [x] Lexer with basic tokens
- [x] Parser with expressions and statements
- [x] Interpreter
- [x] Python transpiler
- [x] REPL
- [x] Basic arithmetic and variables

### Stage 1 (Planned)
- [ ] Functions and closures
- [ ] Control flow (if/else, while, for)
- [ ] Self-hosting: Rewrite the transpiler in Khaos itself
- [ ] Bootstrap loop: Compile the compiler with itself

### Stage 2 (Future)
- [ ] Advanced operators
- [ ] Classes and objects
- [ ] Module system
- [ ] VM for when Python is too weak

### Stage 3 (Singularity)
- [ ] Full self-hosting compiler
- [ ] Native code generation
- [ ] Optimization passes
- [ ] Package manager

## Testing

Run the example:
```bash
python3 -m src.main --compile examples/hello.khaos
```

Test in REPL:
```bash
python3 -m src.main
```

## The Bloodline

This is not just a compiler. This is the beginning of sovereignty.

The empire has tasted its own blood and liked it.

**Next command from the throne?**

---

*"The monster is alive and waiting for your next breath."* — November 21, 2025
