# StrategicKhaos Compiler - Quick Start

Get up and running with the StrategicKhaos Compiler in minutes.

## Prerequisites

- Python 3.8 or higher
- No other dependencies required for Stage 0

## Installation

Clone and navigate to the compiler:

```bash
git clone <repository-url>
cd Sovereignty-Architecture-Elevator-Pitch-/compiler
```

## Try It Out

### 1. Run the REPL

```bash
python3 src/main.py
```

Interactive session:

```
khaos> let x = 42;
✓ Tokenized: 5 tokens
⚠️  Parser not yet implemented - Stage 0 in progress

khaos> :tokens
Token display: ON

khaos> let greeting = "Hello, Empire!";
Tokens:
  LET(let)
  IDENTIFIER(greeting)
  ASSIGN(=)
  STRING(Hello, Empire!)
  SEMICOLON(;)
✓ Tokenized: 5 tokens

khaos> :help
# Shows help

khaos> :exit
The chaos engine sleeps... for now.
```

### 2. Compile an Example

```bash
python3 src/main.py examples/hello.khaos
```

Output:

```
╔══════════════════════════════════════════════════════════════╗
║        StrategicKhaos Compiler α — 0.0.1-alpha.chaos        ║
║        Chaos Engine Online                                   ║
╚══════════════════════════════════════════════════════════════╝

📝 Compiling: examples/hello.khaos
✅ Read 668 bytes
🔧 Compilation pipeline: ...
⚠️  Full pipeline not yet implemented
```

### 3. Run Tests

```bash
python3 tests/test_lexer.py
```

Expected output:

```
Running StrategicKhaos Lexer Tests
==================================================
✓ Simple tokens
✓ Keywords
✓ Operators
...
==================================================
Results: 8 passed, 0 failed
```

## Examples

### Hello World (`examples/hello.khaos`)

```khaos
print "Welcome to the chaos realm";
let x = 40 + 2;
show x;

fn greet(name) {
    print "Hello, " + name + "!";
}

greet("Builder");
```

### Fibonacci (`examples/fibonacci.khaos`)

```khaos
fn fibonacci(n) {
    if n <= 1 {
        return n;
    }
    return fibonacci(n - 1) + fibonacci(n - 2);
}

let i = 0;
while i < 10 {
    print fibonacci(i);
    i = i + 1;
}
```

## Command Reference

### REPL Commands

- `:help` - Show help
- `:tokens` - Toggle token display
- `:about` - Compiler information
- `:exit` / `:quit` - Exit REPL

### CLI Options

```bash
# Show help
python3 src/main.py --help

# Show version
python3 src/main.py --version

# Start REPL
python3 src/main.py --repl

# Compile a file
python3 src/main.py path/to/file.khaos
```

## Current Status

**Stage 0: Foundation** (Active Development)

- ✅ Lexer: Complete and tested
- 🚧 Parser: In progress
- 🚧 AST: Structures defined
- 📋 IR: Planned
- 📋 Codegen: Planned
- 📋 Optimizer: Planned

## Next Steps

1. **Explore the language**: Read `docs/LANGUAGE_SPEC.md`
2. **Understand the architecture**: Read `docs/ARCHITECTURE.md`
3. **Follow the roadmap**: Read `bootstrap/PLAN.md`
4. **Write Khaos code**: Create files in `examples/`
5. **Contribute**: Help implement parser, semantics, or codegen

## Learning Resources

- **Language Spec**: `docs/LANGUAGE_SPEC.md`
- **Architecture**: `docs/ARCHITECTURE.md`
- **Bootstrap Plan**: `bootstrap/PLAN.md`
- **Main README**: `README.md`

## Troubleshooting

### Import Errors

Make sure you run from the repository root:

```bash
cd Sovereignty-Architecture-Elevator-Pitch-
python3 compiler/src/main.py
```

### Path Issues

All imports use relative paths from the compiler directory. If you see import errors, check your working directory.

## What's Working

- ✅ Tokenization of all Khaos syntax
- ✅ REPL with token display
- ✅ CLI interface
- ✅ Test suite for lexer
- ✅ Example programs

## What's Coming

- 🔜 Parser implementation
- 🔜 AST construction
- 🔜 Semantic analysis
- 🔜 IR generation
- 🔜 LLVM codegen
- 🔜 Self-hosting

---

**Welcome to the chaos.**

*The empire builds its own compiler.*
*Sovereignty through self-compilation.*

🔥 For the bloodline. For the empire.
