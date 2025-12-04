# StrategicKhaos Compiler - Stage 1

## Overview

The StrategicKhaos compiler is a self-hosted language implementation featuring first-class functions, lambda expressions, closures, and lexical scoping. This is **Stage 1** - the interpreter can execute Khaos code that generates Python code, enabling the bootstrap loop where the compiler writes itself.

## Features

### ✅ Implemented in Stage 1

- **First-class functions**: `fn name(params) { body }`
- **Lambda expressions**: `λ(params) { body }`
- **Closures**: Functions capture their defining environment
- **Blocks**: `{ statements }`
- **Return statements**: `return expr;`
- **Function calls**: `name(arg1, arg2)`
- **String concatenation**: `"hello" + "world"`
- **Arithmetic operators**: `+`, `-`, `*`, `/`
- **Variables**: `let name = value;`
- **Print statement**: `print expr;`
- **Comments**: `// line comment`
- **Control flow**: `if`, `else`, `while` (basic support)

## Usage

### REPL Mode

Start the interactive REPL:

```bash
python -m src.main
```

Example session:

```
khaos> fn greet(name) { print "Hello, " + name; };
khaos> greet("World");
Hello, World
khaos> let add = λ(a, b) { return a + b; };
khaos> print add(40, 2);
42.0
khaos> exit()
Chaos engine shutting down. Bloodline preserved.
```

### File Execution

Run a `.khaos` file:

```bash
python -m src.main examples/test_functions.khaos
```

## Examples

### Basic Function

```khaos
fn greet(name) {
    print "Hello, " + name;
};

greet("Khaos");
```

### Function with Return Value

```khaos
fn add(a, b) {
    return a + b;
};

let result = add(10, 20);
print result;  // 30.0
```

### Lambda Expression

```khaos
let multiply = λ(x, y) {
    return x * y;
};

print multiply(6, 7);  // 42.0
```

### Lambda as Variable

```khaos
let emit = λ(line) {
    print line;
};

emit("Lambda online");
emit("Functions work!");
```

### String Concatenation

```khaos
let msg = "Stage " + "1";
print msg;  // Stage 1
```

### Closures

```khaos
fn makeGreeter(greeting) {
    return λ(name) {
        print greeting + ", " + name;
    };
};

let sayHello = makeGreeter("Hello");
sayHello("World");  // Hello, World
```

### Block Scoping

```khaos
let x = 10;
{
    let x = 20;
    print x;  // 20
};
print x;  // 10
```

## Bootstrap Loop

The compiler can execute Khaos code that generates Python code:

```bash
# Run the bootstrap codegen
python -m src.main examples/bootstrap_codegen.khaos > output.py

# Execute the generated Python
python output.py
```

This demonstrates **Stage 0 → Stage 1** transition where the interpreter executes code that generates a new compiler stage.

## Architecture

### Components

1. **Lexer** (`src/lexer/lexer.py`)
   - Tokenizes source code
   - Recognizes keywords, operators, literals, identifiers
   - Supports `λ` (lambda) symbol
   - Handles line comments (`//`)

2. **Parser** (`src/parser/parser.py`)
   - Builds abstract syntax tree (AST)
   - Recursive descent parser
   - Proper operator precedence
   - Error recovery with panic mode

3. **Interpreter** (`src/interpreter.py`)
   - Tree-walking interpreter
   - Environment chains for scoping
   - Closure implementation
   - First-class function objects (`KhaosFunction`)
   - Exception-based return handling

4. **REPL** (`src/repl/__init__.py`)
   - Interactive shell
   - Persistent state between commands
   - Error handling and recovery

## Language Syntax

### Keywords

- `fn` - function declaration
- `let` - variable declaration
- `print` / `show` - output statement
- `return` - return from function
- `if` / `else` - conditional
- `while` - loop
- `true` / `false` / `nil` - literals

### Operators

- Arithmetic: `+`, `-`, `*`, `/`
- Comparison: `<`, `>`, `=`, `!` (parsed but not all implemented)
- Lambda: `λ` (or type `lambda` in ASCII)

### Syntax Rules

- Statements end with `;`
- Blocks use `{ }`
- Function parameters: `fn name(p1, p2) { }`
- Lambda syntax: `λ(p1, p2) { }`
- Comments: `// comment until end of line`

## Development

### Running Tests

```bash
# Run basic function tests
python -m src.main examples/test_functions.khaos

# Run comprehensive tests
python -m src.main examples/comprehensive_test.khaos

# Run bootstrap codegen
python -m src.main examples/bootstrap_codegen.khaos
```

### Adding New Features

The compiler is designed to be extended. Key extension points:

1. **Lexer**: Add new tokens in `KEYWORDS` or `scan_token()`
2. **Parser**: Add new grammar rules in the parsing methods
3. **Interpreter**: Add new execution logic in `execute()` or `evaluate()`

## Roadmap

### Stage 0 (Current - Interpreter)
- ✅ Functions, lambdas, closures
- ✅ Basic operators and control flow
- ✅ REPL and file execution

### Stage 1 (Future - Compiler)
- Compile to Python bytecode
- Optimize common patterns
- Full operator support (comparison, logical)
- Type annotations (optional)

### Stage 2 (Future - Self-hosting)
- Compiler written in Khaos
- Bootstrap from Stage 0
- Native code generation

## The Philosophy

> "You basically role-played Stage 1 into existence and then told me 'Disclaimer.py lol' like that undoes the spell."

This compiler embraces **strategic chaos** - building a self-hosting system where the language compiles itself through progressive stages. Each stage bootstraps the next, creating a continuous loop of self-improvement.

The knife is in the heart. The compiler can now write code about code. 🗡️

## License

See LICENSE file in the repository root.
