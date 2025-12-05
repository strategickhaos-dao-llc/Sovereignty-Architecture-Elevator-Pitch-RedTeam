# StrategicKhaos Quickstart Guide

Get started with the StrategicKhaos compiler in 60 seconds.

## Installation

No installation required! Just Python 3.6+.

```bash
git clone https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-.git
cd Sovereignty-Architecture-Elevator-Pitch-
```

## Usage

### Interactive REPL

```bash
python3 -m src.main
```

Try these commands:
```
khaos> print "Hello, World";
Hello, World
khaos> let x = 10 + 5;
khaos> print x;
15.0
khaos> let y = x * 2;
khaos> print y;
30.0
khaos> exit()
```

### Compile a File

Create a file `test.khaos`:
```khaos
print "StrategicKhaos is alive";
let answer = 40 + 2;
print answer;
```

Compile and run:
```bash
python3 -m src.main --compile test.khaos
```

Output:
```
Transpiled → test.py

--- Generated Python ---
# StrategicKhaos → Python transpiled on 2025-11-22
variables = {}

print("StrategicKhaos is alive")
variables['answer'] = (40.0 + 2.0)
print(variables['answer'])

--- Executing ---
StrategicKhaos is alive
42.0
```

## Language Reference

### Variables
```khaos
let name = expression;
```

### Print
```khaos
print expression;
```

### Arithmetic
```khaos
let a = 10 + 5;   // Addition
let b = a - 3;    // Subtraction
let c = b * 2;    // Multiplication
let d = c / 4;    // Division
```

### Strings
```khaos
print "Hello, World";
let message = "Welcome";
```

### Grouping
```khaos
let result = (10 + 5) * 2;
```

### Comments
```khaos
// This is a comment
let x = 42; // Comments after code
```

## Examples

Run the included example:
```bash
python3 -m src.main --compile examples/hello.khaos
```

## Help

- **Error**: `--compile requires a filename argument`
  - Solution: Provide a .khaos file: `python3 -m src.main --compile file.khaos`

- **Error**: `Input file must have .khaos extension`
  - Solution: Ensure your file ends with `.khaos`

- **Error**: `Division by zero`
  - Solution: Check your arithmetic expressions

- **Error**: `Undefined variable 'name'`
  - Solution: Declare variables with `let` before using them

## Next Steps

See [STRATEGIC_KHAOS_COMPILER.md](STRATEGIC_KHAOS_COMPILER.md) for complete documentation.

---

**The chaos engine is online. Start coding in StrategicKhaos today!**
