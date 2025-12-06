# 🔥 FlameLang Quick Reference Card

## Installation
```bash
cd flamelang && ./install.sh
# or
make install
```

## Commands
```bash
flamelang repl              # Interactive shell
flamelang compile file.fl   # Run script
flamelang info              # System info
flamelang export-glyphs     # Export glyph table
```

## REPL Meta Commands
```
.help      Show help
.glyphs    List glyphs
.physics   Physics status
.vars      Show variables
.exit      Exit REPL
```

## Syntax

### Simulations
```flamelang
sim BH1 M=1.989e30 r=1e7    # Black hole
sim OC1                      # Ocean eddy
sim PS1                      # Photon sphere
```

### Glyph Composition
```flamelang
⚡ -> [OC1] |> 🔥           # Execute -> Ocean -> Transform
[BH1] <> [PS1]             # Compose operations
```

### Variables
```flamelang
x = 42
coherence = 0.95
mass = 1.989e30
```

## Built-in Constants
```
pi      3.14159...
e       2.71828...
phi     1.61803... (golden ratio)
c       299792458 m/s
G       6.67430e-11 m³/kg·s²
alpha   1/137 (fine-structure)
```

## Core Glyphs (@Frequency)
```
⚡  Execute      (528Hz)
🔥  Transform    (741Hz)
🌊  Flow         (432Hz)
⚛️  Compose      (963Hz)
🎯  Target       (639Hz)
🔮  Synthesize   (852Hz)
```

## Physics Glyphs
```
BH1  Schwarzschild    (137Hz)
OC1  Ocean Coherence  (432Hz)
PS1  Photon Sphere    (528Hz)
GR1  Geodesic         (963Hz)
ED1  Eddy Coherence   (285Hz)
MT1  Metric Compute   (741Hz)
```

## Security Glyphs
```
🛡️  Boundary Harden  (174Hz)
🔒  Encrypt          (396Hz)
👁️  Audit            (417Hz)
⚔️  Defend           (639Hz)
🌐  Sovereignty      (852Hz)
```

## Operators
```
=   Assignment
->  Arrow (sequence)
|>  Pipe
<>  Compose
```

## Physics Formulas

### Schwarzschild Radius
```
r_s = 2GM/c²
```

### Strain Tensor
```
E_λ = (1/2)(C - λ²I)
```

### Lorentzian Metric
```
g_λ(u,u) = ⟨u, E_λ u⟩
```

## Python API

### Glyph Registry
```python
from glyphs.registry import REGISTRY
glyph = REGISTRY.get("BH1")
physics = REGISTRY.by_category("physics")
```

### Physics Engine
```python
from physics.engine import ENGINE
results = ENGINE.compute_schwarzschild(M, r)
```

### Sovereignty
```python
from security.sovereignty import SOVEREIGNTY
SOVEREIGNTY.initialize_sovereign_environment()
coherence = SOVEREIGNTY.coherence.check_process_coherence()
```

### Interpreter
```python
from core.repl import Interpreter
interp = Interpreter()
result = interp.execute("sim BH1 M=1e30 r=1e7")
```

## File Structure
```
flamelang/
├── core/         Compiler
├── glyphs/       Registry
├── physics/      Engine
├── security/     Sovereignty
├── examples/     Demos
└── tests/        Tests
```

## Testing
```bash
python3 tests/test_all.py
# Should show: 6/6 passed
```

## Example Program
```flamelang
# Black hole simulation
sim BH1 M=1.989e30 r=1e7

# Variables
coherence = 0.95
lambda_param = 1.0

# Glyph pipeline
⚡ -> [OC1] |> 🔥

# Sovereignty
🛡️ -> 🔒
```

## Common Tasks

### Export Glyph Table
```bash
flamelang export-glyphs glyphs.csv
```

### Run Demo
```bash
python3 demo.py
```

### Clean Build
```bash
make clean
```

### Development Install
```bash
make install-dev
```

## Troubleshooting

### Import Errors
```bash
export PYTHONPATH=/path/to/flamelang:$PYTHONPATH
```

### Network Blocked
This is normal - FlameLang blocks network by default.
Enable with: `flamelang --enable-network repl`

### Glyph Not Displaying
Use binding syntax: `[⚡]` instead of `⚡`

## Quick Physics

### Solar Mass BH
```
M = 1.989e30 kg
r_s = 2.95 km
```

### Earth at 1AU
```
r = 1.496e11 m
g_tt ≈ -1 (negligible)
```

### Event Horizon Test
```
r = r_s → g_tt = 0
r → ∞ → g_tt = -1
```

## Sovereignty Status

**Default State:**
- Network: OFF ❌
- Telemetry: BLOCKED ❌
- Coherence: MONITORED ✓
- Audit: ACTIVE ✓

**Enable Network (not recommended):**
```bash
flamelang --enable-network repl
```

## Dependencies
```
numpy    ≥1.21
sympy    ≥1.9
scipy    ≥1.7
psutil   ≥5.8
```

## Support Files
```
README.md        Full docs
QUICKSTART.md    5-min guide
ARCHITECTURE.md  System design
examples/demo.fl Sample code
```

## Version Info
```
FlameLang v0.1.0
Released: Dec 6, 2025
Platform: Python 3.8+
License: MIT / StrategicKhaos DAO
```

---

## 🔥 Quick Debug 🔥

**Lexer Test:**
```bash
cd flamelang
PYTHONPATH=. python3 core/lexer.py
```

**Physics Test:**
```bash
PYTHONPATH=. python3 physics/engine.py
```

**Sovereignty Test:**
```bash
PYTHONPATH=. python3 security/sovereignty.py
```

**All Tests:**
```bash
PYTHONPATH=. python3 tests/test_all.py
```

---

🔥 **Stay Sovereign. Compute Freely.** 🔥

StrategicKhaos DAO LLC © 2025
