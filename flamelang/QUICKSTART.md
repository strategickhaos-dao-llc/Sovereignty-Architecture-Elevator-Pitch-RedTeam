# 🔥 FlameLang Quick Start Guide

Get started with FlameLang in 5 minutes.

## Installation (1 minute)

```bash
cd flamelang
./install.sh
```

That's it! The installer will:
1. Check Python 3.8+ is installed
2. Install dependencies (numpy, sympy, scipy, psutil)
3. Make flamelang executable
4. Run tests to verify installation

## Your First FlameLang Program (2 minutes)

### Start the REPL

```bash
./flamelang repl
```

You'll see:

```
╔══════════════════════════════════════════════════════════════╗
║          🔥 FlameLang v0.1.0 - Sovereign REPL 🔥            ║
║                                                              ║
║  Glyph-based programming with physics simulation            ║
║  Type 'help' for commands, 'exit' to quit                   ║
║                                                              ║
║  Sovereignty: ACTIVE | Network: ISOLATED | Freq: 137Hz      ║
╚══════════════════════════════════════════════════════════════╝

🔥>
```

### Try These Commands

```flamelang
# 1. Simulate a black hole
sim BH1 M=1.989e30 r=1e7

# 2. Use physical constants
c
G
alpha

# 3. List all glyphs
glyphs

# 4. Check sovereignty status
status

# 5. Exit
exit
```

## Run the Demo (1 minute)

```bash
python3 demo.py
```

This interactive demo showcases:
- Glyph registry (17 glyphs)
- Black hole physics simulation
- Sovereignty protocol
- Compiler execution
- Physical constants

## Run Example Programs (1 minute)

```bash
./flamelang run examples/demo.fl
```

This executes 10 example programs showing various FlameLang features.

## Next Steps

- Read full documentation: `cat README.md`
- Explore examples: `cat examples/demo.fl`
- Run tests: `make test` or `python3 tests/test_all.py`
- Write your own `.fl` files and run them with `./flamelang run yourfile.fl`

## Quick Reference

### REPL Commands
- `help` - Show help
- `glyphs` - List glyphs
- `constants` - List constants
- `status` - Sovereignty status
- `exit` - Quit

### Simulations
```flamelang
sim BH1 M=<mass> r=<radius>  # Black hole
sim PS1 M=<mass>             # Photon sphere
sim OC1                      # Ocean eddy
```

### Glyphs
- Core: ⚡🔥🌊⚛️🎯🔮
- Physics: BH1, OC1, PS1, GR1, ED1, MT1
- Security: 🛡️🔒👁️⚔️🌐

### Constants
- `c` - Speed of light
- `G` - Gravitational constant
- `alpha` - Fine-structure constant
- `pi`, `e`, `phi` - Math constants

## Troubleshooting

### Python Version Error
Make sure you have Python 3.8+:
```bash
python3 --version
```

### Dependency Errors
Manually install dependencies:
```bash
pip3 install numpy sympy scipy psutil
```

### Permission Denied
Make scripts executable:
```bash
chmod +x flamelang install.sh demo.py
```

## 🔥 That's It!

You're now ready to explore FlameLang. Happy coding!

For more details, see the full README.md.

🔥 Stay sovereign. 🔥
