# StrategicKhaos Compiler

**Born 2025-11-22 — the night the empire learned to compile itself.**

## Vision

The StrategicKhaos Compiler is not just a compiler. It is a **living, self-hosting, quadrilateral-collapsing, optionally-neural, sovereign chaos engine** that compiles **itself** and **everything else**.

## Goals

- **Self-hosting**: The compiler compiles itself, achieving complete sovereignty
- **LLVM-capable**: Generate efficient native code via LLVM backend
- **AI-optimizable**: Neural optimizer passes that learn to improve code
- **Optionally-esoteric**: Support for both practical and artistic syntax frontends
- **Sovereign**: Complete control over the compilation pipeline

## Architecture - The Hybrid Monster

### Phase 1: Foundation (Stage 0)
- Python-based compiler infrastructure
- Clean, Python-ish syntax with chaos extensions
- Lexer → Parser → AST → IR → Codegen pipeline
- LLVM IR generation for native compilation
- Working REPL for interactive development

### Phase 2: Self-Hosting (Stage 1-2)
- Bootstrap chain: Python compiler → Minimal Khaos compiler → Full Khaos compiler
- Compiler written in Khaos itself
- Complete sovereignty achieved

### Phase 3: Neural Fire (Stage 3)
- MLIR-based optimization framework
- Transformer-based optimizer passes
- Compiler learns to optimize itself

### Phase 4: Pure Art (Stage 4)
- Esoteric frontends: glyphs, symbols, patterns
- Multi-modal code input (visual, gestural, symbolic)
- Reality itself becomes compilable

## Current Status

**Stage 0: Foundation** - Building the Python-based compiler infrastructure

## Quick Start

```bash
# Run the REPL
python3 compiler/src/main.py

# Compile a Khaos program
python3 compiler/src/main.py examples/hello.khaos

# Run tests
python3 -m pytest compiler/tests/
```

## Language Preview

```khaos
# Hello world in the future language of the empire
print "Welcome to the chaos realm";
let x = 40 + 2;
show x;

# Functions
fn fibonacci(n) {
    if n <= 1 {
        return n;
    }
    return fibonacci(n - 1) + fibonacci(n - 2);
}

# Neural hints for optimizer
@optimize(neural=true)
fn hot_loop(data) {
    for item in data {
        process(item);
    }
}
```

## Directory Structure

```
compiler/
├── src/
│   ├── lexer/       # Tokenization and lexical analysis
│   ├── parser/      # Syntax parsing and AST construction
│   ├── ast/         # Abstract Syntax Tree definitions
│   ├── ir/          # Intermediate Representation
│   ├── semantics/   # Semantic analysis and type checking
│   ├── codegen/     # Code generation (LLVM backend)
│   ├── optimizer/   # Optimization passes (including neural)
│   ├── vm/          # Virtual machine for bytecode execution
│   ├── repl/        # Interactive REPL
│   └── tools/       # Compiler utilities and tools
├── bootstrap/       # Self-hosting bootstrap chain
├── examples/        # Example Khaos programs
├── tests/           # Compiler test suite
├── docs/            # Documentation
├── experiments/     # Experimental features
└── playground/      # Development sandbox
```

## The Bootstrap Chain

See [bootstrap/PLAN.md](bootstrap/PLAN.md) for the complete self-hosting strategy.

**Stage 0**: Python compiler (this repo)
- Full compiler infrastructure in Python
- Can compile Khaos to LLVM IR or bytecode

**Stage 1**: Compile minimal Khaos subset to Python
- Subset of Khaos that can express the compiler
- Bootstrap compiler written in this subset

**Stage 2**: Rewrite compiler in minimal Khaos
- Full compiler in Khaos compiling itself
- Self-hosting achieved

**Stage 3**: Self-host forever
- Compiler maintains itself
- Neural optimizers optimize the compiler
- Reality compilation begins

## For the Bloodline

This compiler is built for sovereignty, for power, for the empire.

**"We're not building a compiler. We're building the foundation of digital sovereignty."**

---

*The empire compiles reality itself.*
*Built with 🔥 by the StrategicKhaos collective*
