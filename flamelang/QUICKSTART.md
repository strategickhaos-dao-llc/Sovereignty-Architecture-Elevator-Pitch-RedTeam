# 🔥 FlameLang Quick Start Guide

Get up and running with FlameLang in 5 minutes!

## Step 1: Install (30 seconds)

```bash
cd flamelang
./install.sh
```

Or if you prefer make:
```bash
make install
```

This will:
- Install Python dependencies (numpy, scipy, sympy, psutil)
- Create a `flamelang` command in your PATH

## Step 2: Verify Installation (30 seconds)

```bash
flamelang info
```

You should see:
```
🔥 FlameLang v0.1.0
============================================================
Platform: Python 3.8+
License: MIT / StrategicKhaos DAO
...
```

## Step 3: Run the Demo (1 minute)

```bash
cd flamelang
python3 demo.py
```

This demonstrates:
- Sovereignty system initialization
- Glyph registry
- Physics simulations
- Interpreter execution
- Security features

## Step 4: Try the REPL (2 minutes)

```bash
flamelang repl
```

Try these commands:

```flamelang
# Create a black hole simulation
sim BH1 M=1.989e30 r=1e7

# Set variables
coherence = 0.95

# Run a glyph pipeline
⚡ -> [BH1] |> 🔥

# List all glyphs
.glyphs

# Show variables
.vars

# Exit
.exit
```

## Step 5: Run a Script (1 minute)

Create a file `my_program.fl`:

```flamelang
# My first FlameLang program
sim BH1 M=1.989e30 r=1e7
coherence = 0.95
⚡ -> [BH1] |> 🔥
```

Run it:
```bash
flamelang compile my_program.fl
```

## Next Steps

### Export Glyph Table
```bash
flamelang export-glyphs my_glyphs.csv
```

### Run Tests
```bash
cd flamelang/tests
python3 test_all.py
```

### Learn More
- Read `QUICKREFERENCE.md` for complete syntax reference
- Read `ARCHITECTURE.md` for system design
- Explore `examples/demo.fl` for more examples

## Troubleshooting

### "Module not found" errors
```bash
export PYTHONPATH=/path/to/flamelang:$PYTHONPATH
```

### "flamelang command not found"
Add flamelang directory to your PATH:
```bash
export PATH="/path/to/flamelang:$PATH"
```

### Glyphs not rendering
Make sure your terminal supports Unicode/UTF-8:
```bash
export LANG=en_US.UTF-8
```

## Common Commands Cheat Sheet

```bash
# Start REPL
flamelang repl

# Run script
flamelang compile file.fl

# System info
flamelang info

# Export glyphs
flamelang export-glyphs

# Enable network (not recommended)
flamelang --enable-network repl
```

## REPL Meta Commands

```
.help      Show help
.glyphs    List all glyphs
.physics   Show physics status
.vars      Show all variables
.exit      Exit REPL
```

## Core Concepts

### Simulations
Create physics simulations with the `sim` keyword:
```flamelang
sim BH1 M=1.989e30 r=1e7    # Black hole
sim OC1                      # Ocean eddy
sim PS1 M=1.989e30          # Photon sphere
```

### Variables
Assign values to variables:
```flamelang
x = 42
mass = 1.989e30
coherence = 0.95
```

### Glyph Pipelines
Chain operations using glyphs:
```flamelang
⚡ -> [BH1] |> 🔥           # Execute -> Reference -> Transform
```

### Built-in Constants
Use physics constants directly:
```flamelang
# Available: pi, e, phi, c, G, alpha
```

## Sovereignty Features

By default, FlameLang:
- ✅ Blocks network access
- ✅ Blocks telemetry
- ✅ Monitors process coherence
- ✅ Maintains audit log

This ensures **sovereign computing** - you control your environment.

## 🔥 You're Ready!

You now know enough to start using FlameLang!

For more details, see:
- `QUICKREFERENCE.md` - Complete syntax reference
- `ARCHITECTURE.md` - System architecture
- `examples/` - More example programs

**Stay Sovereign. Compute Freely.** 🔥
