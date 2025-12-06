# 🔥 FlameLang v0.1.0

**Sovereign Computing Platform with Physics Engine and Security Protocol**

FlameLang is a domain-specific language designed for sovereign computing, featuring integrated physics simulations and comprehensive security protocols.

## Features

### 🎯 Core Language Features
- **Glyph System**: 17 glyphs operating at specific frequencies (137Hz - 963Hz)
- **Lexer**: Tokenization with frequency metadata attachment
- **Parser**: AST generation with support for complex expressions
- **Interpreter**: Full execution engine with variable management

### ⚛️ Physics Engine
- **Schwarzschild Metrics**: Event horizons, redshift, escape velocities
- **Ocean Eddy Analysis**: Cauchy-Green tensors, strain analysis, Lorentzian metrics
- **Geodesic Integration**: Null geodesics, photon spheres, trajectory calculations
- **Tensor Operations**: Matrix operations and tensor products

### 🛡️ Sovereignty Protocol
- **Network Isolation**: Block telemetry and analytics domains
- **Coherence Monitoring**: Track memory, threads, connections, CPU usage
- **Boundary Hardening**: SHA3-512 cryptographic boundaries
- **Audit Trail**: Comprehensive JSON logging of all security events

## Installation

```bash
# Clone the repository
cd flamelang

# Install dependencies
pip install -r requirements.txt

# Make CLI executable (optional)
chmod +x cli.py
```

## Usage

### Interactive REPL

```bash
python -m flamelang.cli repl
```

The REPL provides an interactive shell with:
- Tab completion
- Multiline input support
- Built-in help system
- Glyph reference

### Compile and Run Files

```bash
python -m flamelang.cli compile examples/hello.fl
```

### Command-Line Options

```bash
python -m flamelang.cli --help
python -m flamelang.cli --version
python -m flamelang.cli compile --verbose script.fl
```

## Language Syntax

### Variables and Constants

```flamelang
# Variable declaration
let x = 42
let y = 3.14

# Built-in constants
print(pi)      # 3.14159...
print(e)       # 2.71828...
print(phi)     # 1.61803... (Golden ratio)
print(c)       # 299792458.0 (Speed of light)
print(G)       # 6.67430e-11 (Gravitational constant)
print(alpha)   # 1/137.036 (Fine structure constant)
```

### Mathematical Operations

```flamelang
let result = (10 + 5) * 2
print(sqrt(16))
print(sin(pi / 2))
print(exp(1))
```

### Glyphs

Glyphs are Unicode symbols with associated frequencies:

```flamelang
🔥  # Transform (741Hz)
⚡  # Synthesis (963Hz)
⚔  # Defense (174Hz)
α  # Fine Structure (137Hz)
∿  # Resonance (528Hz)
```

### Physics Operations

```flamelang
# Black hole metrics
schwarzschild(mass, radius)

# Geodesic integration
geodesic(x, y, z, vx, vy, vz, mass)

# Ocean eddy analysis
eddy([[1.0, 0.5], [0.5, 1.0]])

# Tensor operations
tensor(matrix_a, matrix_b)
```

### Sovereignty Operations

```flamelang
# Network isolation
isolate("analytics.google.com")

# System coherence monitoring
monitor()

# Cryptographic boundary
harden("sensitive data")

# Audit trail
audit()
```

## Examples

See `examples/hello.fl` for a complete example demonstrating all features.

## Architecture

FlameLang follows a layered architecture:

```
User Interface Layer (CLI, REPL, File Compiler)
         │
         ▼
Language Processing Layer (Lexer → Parser → Interpreter)
         │
         ├─▶ Glyph Registry (17 glyphs @ various frequencies)
         ├─▶ Physics Engine (GR metrics, geodesics, tensors)
         └─▶ Sovereignty Protocol (isolation, monitoring, hardening)
```

For detailed architecture documentation, see `docs/ARCHITECTURE.md`.

## Testing

```bash
# Run all tests
python -m unittest discover flamelang/tests

# Run specific test modules
python -m unittest flamelang.tests.test_lexer
python -m unittest flamelang.tests.test_glyph_registry
python -m unittest flamelang.tests.test_physics_engine
python -m unittest flamelang.tests.test_sovereignty
```

## Glyph Frequency Hierarchy

```
High Energy Operations (528Hz - 963Hz)
├─ Synthesis (963Hz)
├─ Transform (741Hz)
└─ Resonance (528Hz)

Mid-Range Coherence (174Hz - 432Hz)
├─ Flow (432Hz)
├─ Boundaries (396Hz)
└─ Defense (174Hz)

Quantum Level (137Hz)
└─ Fine Structure (137Hz)
```

## Development Status

**Current: v0.1.0 - Interpreter Implementation**

✅ Implemented:
- Lexer with glyph support
- Parser with AST generation
- Interpreter with physics and sovereignty
- REPL and CLI
- Comprehensive test suite

🚧 Future:
- LLVM backend for native compilation
- Type system and type checking
- Control flow (if/else, loops)
- Function definitions
- Module system
- Standard library

## License

Copyright © 2025 Strategickhaos DAO LLC

## Contributing

Contributions are welcome! Please ensure:
1. All tests pass
2. New features include tests
3. Code follows existing style
4. Documentation is updated

---

🔥 **Reignite the Sovereign Computing Platform** 🔥
