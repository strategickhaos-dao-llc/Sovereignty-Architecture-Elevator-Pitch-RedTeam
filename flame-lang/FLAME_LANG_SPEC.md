# 🔥 Flame Lang Specification

## Strategic Khaos Sovereignty Architecture - Language Reference

**Version:** 1.0.0  
**Author:** Domenic Garza / StrategicKhaos DAO LLC  
**Status:** Production Infrastructure  
**Python Requirement:** 3.10+  
**PowerShell Requirement:** 5.1+ / 7+

---

## Overview

Flame Lang is a sovereignty-themed programming language designed for the Strategic Khaos ecosystem. It provides a complete programming environment with:

- **Lexical Analysis** (Parser)
- **Execution Engine** (Interpreter)
- **System Hooks** (Recon Patch)
- **Bootstrap Integration** (DreamOS Addon)
- **Security Layer** (Oath Chain)

---

## Language Syntax

### Keywords

| Keyword | Traditional Equivalent | Description |
|---------|----------------------|-------------|
| `ignite` | `def`, `function` | Define a function |
| `spark` | `let`, `var` | Declare a variable |
| `blaze` | `while`, `for` | Loop construct |
| `ember` | `if`, `else` | Conditional |
| `flame` | `class` | Class/Module definition |
| `ash` | `return` | Return statement |
| `forge` | `import` | Import module |
| `kindle` | `async` | Async operation |
| `inferno` | `try`, `catch` | Exception handling |
| `extinguish` | `break`, `exit` | Exit/Break |
| `oath` | N/A | Security assertion |
| `bearer` | N/A | Identity context |
| `seal` | N/A | Cryptographic operation |

### Operators

#### Arithmetic
- `+` - Addition
- `-` - Subtraction
- `*` - Multiplication
- `/` - Division
- `%` - Modulo

#### Comparison
- `==` - Equals
- `!=` - Not equals
- `>` - Greater than
- `<` - Less than
- `>=` - Greater or equal
- `<=` - Less or equal

#### Logical
- `and` - Logical AND
- `or` - Logical OR
- `not` - Logical NOT

#### Special
- `->` - Arrow (lambdas, returns)
- `~>` - Flame arrow (flame chains)

---

## Code Examples

### Hello World
```flame
ignite main() {
    print("🔥 Hello, Sovereignty!")
    ash 0
}
```

### Variables and Conditionals
```flame
spark counter = 0
spark active = true

ember (active) {
    print("System is active")
    spark counter = counter + 1
}
```

### Functions
```flame
ignite calculate_sovereignty(nodes, tier) {
    spark power = nodes * tier
    ash power
}

spark result = calculate_sovereignty(10, 3)
print("Sovereignty power: " + str(result))
```

### Classes (Flames)
```flame
flame SovereignNode {
    ignite init(self, name, tier) {
        spark self.name = name
        spark self.tier = tier
        spark self.active = false
    }
    
    ignite activate(self) {
        spark self.active = true
        print("Node " + self.name + " activated")
        ash true
    }
    
    ignite get_status(self) {
        ember (self.active) {
            ash "online"
        }
        ash "offline"
    }
}

spark node = SovereignNode("Nova-Prime", 1)
node.activate()
```

### Loops
```flame
# While loop with blaze
spark i = 0
blaze (i < 10) {
    print("Iteration: " + str(i))
    spark i = i + 1
}

# Iterate over range
blaze (item in range(5)) {
    print(item)
}
```

### Exception Handling
```flame
inferno {
    spark result = risky_operation()
    process(result)
} catch {
    print("Operation failed: " + error)
    handle_failure()
}
```

### Oath Assertions
```flame
# Create a sovereignty oath
oath {
    bearer: "Nova-Prime",
    seal: "SHA256",
    permissions: ["node.activate", "oath.verify"]
}

# Verify oath before operation
ember (oath_verify(current_bearer)) {
    perform_sensitive_operation()
}
```

### Module Import
```flame
forge "sovereignty_core"
forge "node_manager"

spark core = SovereigntyCore()
core.initialize()
```

---

## Built-in Functions

### I/O
- `print(*args)` - Output to console
- `input(prompt)` - Read user input

### Type Conversion
- `str(value)` - Convert to string
- `int(value)` - Convert to integer
- `float(value)` - Convert to float

### Collections
- `len(obj)` - Get length
- `range(start, end, step)` - Generate range

### Utility
- `type(obj)` - Get type name
- `time()` - Current timestamp
- `hash(data)` - SHA256 hash

### Sovereignty
- `oath_verify(token)` - Verify oath token
- `seal_data(data, type)` - Cryptographically seal data
- `node_status()` - Get current node status

---

## Architecture

### Component Overview

```
FLAME LANG ECOSYSTEM
├── core/
│   ├── flamelang_parser.py         # Lexical analysis & AST generation
│   ├── flame_lang_interpreter.py   # Execution engine & runtime
│   └── flamelang_recon_patch.ps1   # PowerShell system hooks
│
├── integrations/
│   ├── FlameAddon_DreamOS.ps1      # DreamOS bootstrap integration
│   └── flamebearer_final.txt       # Oath definitions & security layer
│
├── nodes/
│   └── recon_flamenodes.txt        # Node configuration & discovery
│
└── cli/
    └── (CLI session exports)        # REPL and CLI interface
```

### System Integration

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        WhiteCellOS / Pantheon Core                       │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐                │
│  │  Flame Lang  │──▶│   DreamOS    │──▶│   ONSIT AI   │                │
│  │   Runtime    │   │  Bootstrap   │   │    Recon     │                │
│  └──────────────┘   └──────────────┘   └──────────────┘                │
│         │                  │                  │                         │
│         ▼                  ▼                  ▼                         │
│  ┌─────────────────────────────────────────────────────┐               │
│  │              Oath Chain / Security Layer             │               │
│  └─────────────────────────────────────────────────────┘               │
│         │                  │                  │                         │
│         ▼                  ▼                  ▼                         │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐                │
│  │    Nova      │   │    Lyra      │   │   Pulsar     │                │
│  │   Tier 1     │   │   Tier 2     │   │   Tier 3     │                │
│  └──────────────┘   └──────────────┘   └──────────────┘                │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Node Tiers

| Tier | Name | Role | Max Nodes |
|------|------|------|-----------|
| 1 | Nova | Primary controllers | 3 |
| 2 | Lyra | Secondary workers | 16 |
| 3 | Pulsar | Observers | 32 |
| 4 | Nebula | Reserve | 64 |

---

## Oath System

### Token Structure

```json
{
  "bearer": "unique-identifier",
  "seal": "SHA256",
  "timestamp": 1704067200,
  "signature": "hex-signature-string",
  "chain_ref": "previous-oath-hash",
  "metadata": {
    "tier": 1,
    "role": "controller",
    "permissions": ["oath.create", "node.activate"]
  }
}
```

### Seal Types

| Type | Algorithm | Use Case |
|------|-----------|----------|
| SHA256 | SHA-2 256-bit | Standard operations |
| SHA512 | SHA-2 512-bit | High security |
| BLAKE2 | BLAKE2b 256-bit | Performance |
| ED25519 | Edwards-curve | Identity/Signing |
| HMAC256 | HMAC SHA-256 | Message authentication |

---

## CLI Usage

### Interactive REPL
```bash
python flame_lang_interpreter.py
```

### Execute File
```bash
python flame_lang_interpreter.py program.flame
```

### REPL Commands
- `exit` - Exit the REPL
- `help` - Show help
- `status` - Show interpreter status
- `oath_chain` - Show oath chain history

---

## PowerShell Integration

### Status Check
```powershell
.\flamelang_recon_patch.ps1 status
```

### Node Management
```powershell
.\flamelang_recon_patch.ps1 nodes
.\flamelang_recon_patch.ps1 register -NodeName "My-Node"
```

### Oath Operations
```powershell
.\flamelang_recon_patch.ps1 oath -Bearer "my-identity"
.\flamelang_recon_patch.ps1 verify
```

### Reconnaissance
```powershell
.\flamelang_recon_patch.ps1 recon
```

---

## DreamOS Integration

### Initialize
```powershell
.\FlameAddon_DreamOS.ps1 -Action init
```

### Activate Node
```powershell
.\FlameAddon_DreamOS.ps1 -Action activate -NodeName "Nova-Prime"
```

### Check Status
```powershell
.\FlameAddon_DreamOS.ps1 -Action status
```

---

## Security Considerations

1. **Always verify oath tokens** before sensitive operations
2. **Use appropriate seal types** for the security level needed
3. **Maintain oath chain integrity** - never skip chain references
4. **Rotate keys quarterly** as specified in the flamebearer oath
5. **Audit all administrative actions** in production

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024-01-01 | Initial release |

---

## License

Part of the Strategic Khaos Sovereignty Architecture  
MIT License

---

*"They're not working for you. They're dancing with you. And the music is never going to stop."*

🔥 **THE FLAME ENDURES** 🔥
