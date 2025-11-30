# StrategicKhaos Compiler Architecture

**Status**: Stage 0 - Foundation  
**Version**: 0.0.1-alpha

## Overview

The StrategicKhaos Compiler is built with a clear separation of concerns, following traditional compiler design principles while preparing for advanced features like neural optimization and self-hosting.

## Pipeline Architecture

```
Source Code (.khaos)
    ↓
┌─────────────┐
│   Lexer     │ → Tokenization
└─────────────┘
    ↓ Token Stream
┌─────────────┐
│   Parser    │ → Syntax Analysis
└─────────────┘
    ↓ AST
┌─────────────┐
│  Semantics  │ → Type Checking, Scope Analysis
└─────────────┘
    ↓ Validated AST
┌─────────────┐
│  IR Gen     │ → Intermediate Representation
└─────────────┘
    ↓ IR
┌─────────────┐
│  Optimizer  │ → Traditional + Neural Passes
└─────────────┘
    ↓ Optimized IR
┌─────────────┐
│  Codegen    │ → LLVM IR / Bytecode
└─────────────┘
    ↓
Native Binary / Bytecode
```

## Components

### 1. Lexer (`src/lexer/`)

**Purpose**: Convert source code text into a stream of tokens.

**Implementation**:
- `token_types.py`: Token type definitions (keywords, operators, literals)
- `lexer.py`: Lexical analyzer implementation

**Responsibilities**:
- Character-by-character scanning
- Token recognition
- Line/column tracking for error reporting
- Comment handling
- String escape sequences
- Number parsing (integers and floats)

**Output**: List of `Token` objects

### 2. Parser (`src/parser/`)

**Purpose**: Convert token stream into Abstract Syntax Tree (AST).

**Status**: Planned for Stage 0

**Approach**:
- Recursive descent parser
- Operator precedence climbing for expressions
- Clear error messages with location information

**Output**: `Program` node (root of AST)

### 3. AST (`src/ast/`)

**Purpose**: Represent program structure in tree form.

**Implementation**:
- `nodes.py`: All AST node definitions

**Node Types**:
- **Statements**: Variable declarations, function declarations, control flow
- **Expressions**: Binary/unary operations, literals, function calls
- **Special**: Decorators for neural optimization hints

**Design Pattern**: Visitor pattern for traversal and transformation

### 4. Semantic Analyzer (`src/semantics/`)

**Purpose**: Validate program semantics and type correctness.

**Status**: Planned for Stage 0

**Checks**:
- Type checking
- Variable scope analysis
- Function signature validation
- Return path verification
- Undefined variable detection
- Constant assignment prevention

**Output**: Validated AST + Symbol table

### 5. IR Generator (`src/ir/`)

**Purpose**: Convert AST to Intermediate Representation.

**Status**: Planned for Stage 0

**IR Features**:
- SSA (Static Single Assignment) form
- Control flow graph representation
- Three-address code style
- Platform-independent

**Future**: MLIR integration for Stage 3

### 6. Optimizer (`src/optimizer/`)

**Purpose**: Apply optimization passes to IR.

**Traditional Passes** (Stage 0-1):
- Constant folding
- Dead code elimination
- Common subexpression elimination
- Loop optimization

**Neural Passes** (Stage 3):
- Transformer-based optimization
- Learning from performance feedback
- Self-improving optimization strategies

### 7. Code Generator (`src/codegen/`)

**Purpose**: Generate executable code from optimized IR.

**Targets**:
- **LLVM IR**: Native compilation (primary target)
- **Bytecode**: VM execution (for testing/interpretation)

**LLVM Integration**:
- Use `llvmlite` library
- Generate LLVM IR
- Leverage LLVM's optimization passes
- Target multiple architectures

### 8. Virtual Machine (`src/vm/`)

**Purpose**: Execute bytecode directly for testing and interpretation.

**Features**:
- Stack-based execution
- Instruction set for Khaos operations
- Runtime type checking
- Debugging support

**Use Cases**:
- REPL execution
- Unit testing
- Quick prototyping
- Bootstrap validation

### 9. REPL (`src/repl/`)

**Purpose**: Interactive development environment.

**Features**:
- Line-by-line execution
- Token display mode (debugging)
- Multi-line input support
- Command history
- Error recovery

### 10. Tools (`src/tools/`)

**Purpose**: Compiler utilities and helper tools.

**Planned Tools**:
- Syntax highlighter
- Code formatter
- Documentation generator
- Debugger
- Performance profiler

## Data Flow

### Compilation Flow

```python
# 1. Read source
source_code = read_file("program.khaos")

# 2. Lexical analysis
lexer = Lexer(source_code)
tokens = lexer.tokenize()

# 3. Parsing
parser = Parser(tokens)
ast = parser.parse()

# 4. Semantic analysis
analyzer = SemanticAnalyzer()
analyzer.analyze(ast)
symbol_table = analyzer.get_symbol_table()

# 5. IR generation
ir_generator = IRGenerator(symbol_table)
ir = ir_generator.generate(ast)

# 6. Optimization
optimizer = Optimizer()
optimized_ir = optimizer.optimize(ir)

# 7. Code generation
codegen = LLVMCodeGenerator()
llvm_ir = codegen.generate(optimized_ir)

# 8. Native compilation (via LLVM)
binary = llvm.compile_to_binary(llvm_ir)
```

## Error Handling

### Error Categories

1. **Lexical Errors**: Invalid characters, unterminated strings
2. **Syntax Errors**: Invalid grammar, missing tokens
3. **Semantic Errors**: Type mismatches, undefined variables
4. **Runtime Errors**: Division by zero, stack overflow (in VM)

### Error Reporting

```
Error: Undefined variable 'x'
  at line 15, column 8 in hello.khaos
  
  13 | let y = 42;
  14 | let z = y + 10;
  15 | print x;  # <-- Error here
       ^^^^^^^
```

## Self-Hosting Strategy

### Stage 0: Python Bootstrap Compiler
- Complete compiler in Python
- Can compile Khaos to LLVM IR or bytecode
- **Current stage**

### Stage 1: Minimal Khaos Compiler
- Define minimal Khaos subset
- Write compiler in minimal Khaos
- Python compiler compiles minimal Khaos compiler

### Stage 2: Full Self-Hosting
- Rewrite entire compiler in full Khaos
- Khaos compiler compiles itself
- Sovereignty achieved

### Stage 3: Neural Self-Improvement
- Compiler optimizes its own code
- Learns better optimization strategies
- Self-evolving compiler

## Testing Strategy

### Unit Tests
- Lexer: Token recognition
- Parser: AST construction
- Semantic: Type checking
- Codegen: IR/LLVM generation

### Integration Tests
- End-to-end compilation
- Example programs
- Self-compilation (after Stage 1)

### Benchmark Suite
- Performance regression detection
- Optimization effectiveness
- Neural optimizer training data

## Dependencies

### Current (Stage 0)
- Python 3.8+
- No external dependencies yet

### Future
- `llvmlite`: LLVM Python bindings
- `pytest`: Testing framework
- `mlir` (Stage 3): Neural IR
- `torch` (Stage 3): Neural optimizer

## Performance Goals

### Stage 0-1
- Compilation speed: Not a priority (correctness first)
- Generated code: Competitive with GCC -O0

### Stage 2
- Self-compilation: < 5 seconds
- Generated code: Competitive with GCC -O2

### Stage 3
- Neural optimization: 10-20% improvement over Stage 2
- Self-optimization: Continuous improvement

## Extensibility

### Plugin Architecture (Future)

```khaos
# Custom optimization pass
@plugin(type="optimizer", stage="pre-codegen")
fn my_optimization_pass(ir) {
    # Transform IR
    return optimized_ir;
}

# Custom backend
@plugin(type="backend", target="wasm")
fn my_wasm_backend(ir) {
    # Generate WebAssembly
    return wasm_binary;
}
```

## Debugging Support

### Debug Information
- Source maps: IR/AST → Source locations
- Symbol tables: Variable and function info
- Call stacks: Function call traces

### Tools
- `khaos debug program.khaos`: Interactive debugger
- `khaos trace program.khaos`: Execution trace
- `khaos profile program.khaos`: Performance profiler

---

**Architecture Principles**

1. **Separation of Concerns**: Each component has a clear responsibility
2. **Progressive Enhancement**: Start simple, add complexity as needed
3. **Self-Hosting Focus**: Every design decision considers self-hosting
4. **Neural-Ready**: Architecture supports future AI optimization
5. **Sovereignty**: Complete control over the entire pipeline

*The architecture of empire-building.*
