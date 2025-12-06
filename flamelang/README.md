# 🔥 FlameLang - Sovereign Symbolic Language

**A glyph-based programming language with physics simulations and sovereignty enforcement.**

## What is FlameLang?

FlameLang is a unique programming language that combines:
- 🎨 **Visual Programming** - Use Unicode glyphs (⚡, 🔥, 🌊) as syntax
- 🔬 **Physics Simulations** - Black holes, ocean eddies, photon spheres
- 🛡️ **Digital Sovereignty** - Network blocking, telemetry control, process monitoring
- 🐍 **Python Integration** - Full Python API for extension

## Quick Start

### Installation

```bash
./install.sh
```

Or with make:
```bash
make install
```

### Your First Program

```flamelang
# Create a black hole simulation
sim BH1 M=1.989e30 r=1e7

# Variables
coherence = 0.95

# Glyph pipeline
⚡ -> [BH1] |> 🔥
```

Save as `hello.fl` and run:
```bash
flamelang compile hello.fl
```

### Start the REPL

```bash
flamelang repl
```

```
🔥> sim BH1 M=1.989e30 r=1e7
✓ BH1: Schwarzschild radius = 2.95 km, g_tt = -0.999705

🔥> .glyphs
Core Glyphs:
  ⚡  Execute      @ 528Hz
  🔥  Transform    @ 741Hz
  🌊  Flow         @ 432Hz
  ...
```

## Features

### Glyph-Based Syntax

Use visual symbols as code:
```flamelang
⚡ -> [OC1] |> 🔥    # Execute -> Ocean -> Transform
🛡️ -> 🔒            # Boundary Harden -> Encrypt
```

### Physics Engine

Simulate real physics:
```flamelang
sim BH1 M=1.989e30 r=1e7    # Black hole (solar mass)
sim OC1 coherence=0.95       # Ocean eddy
sim PS1 M=1.989e30          # Photon sphere
```

### Built-in Constants

Physics constants ready to use:
- `pi` - 3.14159...
- `e` - 2.71828...
- `phi` - 1.61803... (golden ratio)
- `c` - 299792458 m/s (speed of light)
- `G` - 6.67430e-11 (gravitational constant)
- `alpha` - 1/137 (fine-structure constant)

### Sovereignty System

Secure by default:
- ✅ Network: BLOCKED
- ✅ Telemetry: BLOCKED
- ✅ Coherence: MONITORED
- ✅ Audit: ACTIVE

## Documentation

- 📖 **[QUICKSTART.md](QUICKSTART.md)** - Get started in 5 minutes
- 📋 **[QUICKREFERENCE.md](QUICKREFERENCE.md)** - Complete syntax reference
- 🏗️ **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design and internals

## Examples

### Black Hole Simulation

```flamelang
# Solar mass black hole
sim BH1 M=1.989e30 r=1e7

# Output: Schwarzschild radius = 2.95 km
```

### Glyph Pipeline

```flamelang
# Execute operation on ocean eddy, then transform
⚡ -> [OC1] |> 🔥
```

### Security Operations

```flamelang
# Sovereignty protocol
🛡️ -> 🔒    # Harden boundaries, then encrypt
```

## Testing

Run the test suite:
```bash
python3 tests/test_all.py
```

All tests should pass:
```
Testing Lexer... ✓
Testing Glyph Registry... ✓
Testing Physics Engine... ✓
Testing Sovereignty System... ✓
Testing Interpreter... ✓
Testing Integration... ✓

Results: 6/6 passed
🔥 All tests passed!
```

## Python API

Use FlameLang from Python:

```python
from core.repl import Interpreter

# Create interpreter
interp = Interpreter()

# Execute FlameLang code
interp.execute("sim BH1 M=1.989e30 r=1e7")
interp.execute("x = 42")

# Access results
print(interp.variables['x'])  # 42
```

### Glyph Registry

```python
from glyphs.registry import REGISTRY

# Get a glyph
execute = REGISTRY.get('⚡')
print(execute.name)       # Execute
print(execute.frequency)  # 528

# List by category
physics_glyphs = REGISTRY.by_category('physics')
```

### Physics Engine

```python
from physics.engine import ENGINE

# Schwarzschild calculation
result = ENGINE.compute_schwarzschild(M=1.989e30, r=1e7)
print(f"r_s = {result['r_s']/1000:.2f} km")

# Run simulation
bh = ENGINE.simulate_black_hole('BH1', M=1.989e30, r=1e7)
```

### Sovereignty System

```python
from security.sovereignty import SOVEREIGNTY

# Initialize
SOVEREIGNTY.initialize_sovereign_environment()

# Check status
status = SOVEREIGNTY.get_status()
print(f"Coherence: {status['coherence']:.2%}")

# Security operations
SOVEREIGNTY.harden_boundary()
encrypted = SOVEREIGNTY.encrypt("secret data")
```

## Commands

```bash
flamelang repl              # Start interactive REPL
flamelang compile file.fl   # Run a script
flamelang info              # System information
flamelang export-glyphs     # Export glyph table
```

## REPL Meta Commands

```
.help      Show help
.glyphs    List all glyphs
.physics   Show physics status
.vars      Show variables
.exit      Exit REPL
```

## Requirements

- Python 3.8+
- numpy ≥1.21
- scipy ≥1.7
- sympy ≥1.9
- psutil ≥5.8

## Development

### Run Demo

```bash
python3 demo.py
```

### Clean Build

```bash
make clean
```

### Export Glyphs

```bash
flamelang export-glyphs glyphs.csv
```

## Project Structure

```
flamelang/
├── core/         # Lexer, parser, interpreter
├── glyphs/       # Glyph registry
├── physics/      # Physics engine
├── security/     # Sovereignty system
├── examples/     # Example programs
├── tests/        # Test suite
└── docs/         # Documentation
```

## Philosophy

FlameLang embodies **sovereign computing**:
1. **Control** - You control your environment
2. **Privacy** - No telemetry, no tracking
3. **Transparency** - Open source, auditable
4. **Power** - Real physics, real simulations

## License

MIT License / StrategicKhaos DAO LLC

## Version

FlameLang v0.1.0
Released: December 6, 2025

## Support

- 📧 Issues: GitHub Issues
- 📖 Docs: See QUICKSTART.md and ARCHITECTURE.md
- 🌐 Website: Coming soon

---

🔥 **Stay Sovereign. Compute Freely.** 🔥

StrategicKhaos DAO LLC © 2025
