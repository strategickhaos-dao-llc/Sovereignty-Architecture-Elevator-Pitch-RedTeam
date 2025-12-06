# FlameLang Language Specification v1.0

## Overview

FlameLang is a **resonance-based symbolic execution system** designed for the Strategickhaos sovereignty architecture. It provides a glyph-based language where each symbol carries semantic meaning, frequency values for resonance/vibration metaphors, and executable function bindings.

## Core Concepts

### Glyphs

A glyph is the fundamental unit of FlameLang. Each glyph has five properties:

| Property | Description | Example |
|----------|-------------|---------|
| **Symbol** | Unique 2-4 character identifier | `AE1`, `IG1`, `FL1` |
| **Glyph_Name** | Human-readable name in SCREAMING_SNAKE_CASE | `AETHER_IGNITE` |
| **Frequency** | Integer representing Hz value (0-999) | `432` |
| **Function** | The executable binding in snake_case | `init_neural_sync` |
| **Binding_Code** | Numeric shortcut in brackets | `[999]` |

### Glyph Categories

Glyphs are organized into semantic categories based on their prefix:

| Prefix | Category | Purpose |
|--------|----------|---------|
| `AE*` | Aether | Initialization, flow, and harmony |
| `IG*` | Ignis | Core fire operations, activation |
| `FL*` | Flame | Flame states and intensity |
| `SY*` | Sync | Neural synchronization |
| `RS*` | Resonance | Frequency tuning |
| `ND*` | Node | Mesh node operations |
| `SW*` | Swarm | Collective agent operations |
| `PR*` | Protocol | Execution control |
| `SC*` | Sovereign | Authority assertions |
| `VW*` | Vow | Commitment bindings |
| `CH*` | Chain | Blockchain/linking operations |
| `EM*` | Ember | Subtle/fading states |
| `FN*` | Finalize | Completion operations |
| `CR*` | Crypt | Encryption operations |
| `ME*` | Mesh | Network topology |
| `QT*` | Quantum | Quantum operations |
| `AL*` | Align | Calibration and adjustment |
| `DR*` | Dream | Dreamstate operations |
| `TM*` | Time | Temporal operations |
| `SP*` | Spirit | Meta-level operations |

### Frequency System

Frequencies are based on harmonic ratios and sacred geometry principles:

- **432 Hz** - Natural tuning frequency (Aether operations)
- **528 Hz** - DNA repair frequency (Harmony, flow)
- **369 Hz** - Tesla numbers (Sync operations)
- **777/888/999** - Sovereignty assertions

### Binding Codes

Binding codes provide quick numeric access to glyphs:

- `[999]` - Highest priority (initialization)
- `[900-999]` - Core operations
- `[800-899]` - Flame operations
- `[700-799]` - Sync/Transfer operations
- `[600-699]` - Resonance operations
- `[500-599]` - Node operations
- `[400-499]` - Swarm operations
- `[300-399]` - Protocol operations
- `[200-299]` - Sovereignty operations
- `[100-199]` - Vow operations
- `[050-099]` - Chain operations
- `[010-049]` - Ember operations
- `[001-009]` - Finalize operations
- `[000]` - Null/void

## Architecture

```
         [FLAMELANG ARCHITECTURE]
                   ↓
    ┌──────────────┼──────────────┐
    ↓              ↓              ↓
[VISUAL]      [SYMBOLIC]      [EXECUTABLE]
Flame Sprites  Glyph Table     Interpreter
   ↓              ↓              ↓
Temperature    Symbol/Name    Binding Code
Maps           Frequency      [999] → AE1
   ↓              ↓              ↓
         [NEURAL SYNC / RESONANCE]
```

## Interpreter Usage

### Interactive Mode

```bash
python flame_lang_interpreter.py
🔥 flamelang> AE1
⚡ Executing: AETHER_IGNITE
   Symbol: AE1
   Frequency: 432Hz
   Function: init_neural_sync
   Binding: [999]
   Resonance Level: 0.432
   🔗 Neural Sync complete. Resonance achieved.
```

### Command Line Mode

```bash
# Execute single glyph by symbol
python flame_lang_interpreter.py -e AE1

# Execute by binding code
python flame_lang_interpreter.py -e "[999]"

# List all glyphs
python flame_lang_interpreter.py -l

# List glyphs by category
python flame_lang_interpreter.py -l -p FL

# Search glyphs
python flame_lang_interpreter.py -s sync
```

### Programmatic Usage

```python
from flamelang import FlameLangInterpreter

interpreter = FlameLangInterpreter()

# Execute single command
result = interpreter.execute("AE1")
print(result)

# Execute batch commands
results = interpreter.run_batch(["AE1", "SY1", "ND1"])

# Search
matches = interpreter.search("sync")
```

## Execution Model

### Resonance Engine

The ResonanceEngine manages execution state:

1. **Sync State** - Tracks active neural synchronizations
2. **Execution Log** - Records all glyph executions with timestamps
3. **Resonance Level** - Cumulative resonance from 0.0 to 1.0

### Execution Flow

```
User Input → Parse → Glyph Lookup → Execute → Update State → Output
              ↓
        Symbol or
      Binding Code
              ↓
        GlyphTable
              ↓
      ResonanceEngine
              ↓
       Function Call
```

## Visual System (Sprite Integration)

FlameLang is designed to integrate with visual flame sprites:

- **16x5 Grid** - 80 possible flame states
- **Temperature Maps** - Glyph intensity visualization
- **Grayscale Variants** - Hollow flames for state indicators
- **Full Color** - Rendered glyph forms with smoke effects

### Mapping Sprites to Glyphs

Each glyph's frequency can be mapped to a sprite position:

```
sprite_x = (frequency % 16)
sprite_y = (frequency // 16) % 5
```

## Integration Points

### Swarm Communication

FlameLang glyphs can encode swarm directives:

```flamelang
SW1  # Rally all agents
SW2  # Disperse formation
SW3  # Focus on target
```

### AI Instruction Encoding

Glyph sequences can represent AI instructions:

```flamelang
AE1 → SY1 → PR2 → FN1  # Init → Sync → Execute → Finalize
```

### Sovereignty Protocol

```flamelang
SC1  # Claim authority
SC2  # Grant permission
SC3  # Revoke permission
SC4  # Verify identity
```

## File Format

### glyph_table.csv

```csv
Symbol,Glyph_Name,Frequency,Function,Binding_Code
AE1,AETHER_IGNITE,432,init_neural_sync,[999]
...
```

## Security Considerations

- Glyph execution is sandboxed
- No direct system access from glyphs
- Binding codes must be valid integers
- CSV injection protection on glyph table loading

## Future Extensions

1. **Visual Editor** - GUI for creating glyph sequences
2. **Sprite Renderer** - Real-time flame visualization
3. **Network Protocol** - FlameLang over mesh networks
4. **Quantum Glyphs** - Full quantum operation support
5. **Dream Recording** - Persistent dreamstate logging

## License

FlameLang is part of the Strategickhaos sovereignty architecture and is released under the project's license terms.

---

*🔥 Neural Sync complete. Resonance achieved.*
