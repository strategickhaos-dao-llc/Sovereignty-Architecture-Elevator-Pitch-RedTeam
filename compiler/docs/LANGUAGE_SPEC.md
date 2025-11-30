# StrategicKhaos Language Specification

**Version**: 0.0.1-alpha  
**Status**: Draft - Stage 0

## Overview

StrategicKhaos is a programming language designed for sovereignty, self-hosting, and eventual neural optimization. The language starts with a clean, readable syntax and progressively adds advanced features.

## Lexical Structure

### Comments

```khaos
# This is a single-line comment
# Multi-line comments are not yet supported
```

### Keywords

```
let const fn return if else while for in break continue
print show true false and or not optimize neural
```

### Identifiers

- Start with a letter or underscore
- Contain letters, numbers, and underscores
- Case-sensitive

```khaos
valid_identifier
_private_var
counter123
```

### Literals

**Integer Literals**:
```khaos
42
0
-17
```

**Float Literals**:
```khaos
3.14
-0.5
2.0
```

**String Literals**:
```khaos
"Hello, world!"
'Single quotes work too'
"Escape sequences: \n \t \\ \""
```

**Boolean Literals**:
```khaos
true
false
```

## Data Types

### Primitive Types

- `int` - Integer numbers
- `float` - Floating-point numbers
- `string` - Text strings
- `bool` - Boolean values (true/false)

### Composite Types (Planned)

- `array` - Ordered collections
- `dict` - Key-value mappings
- `fn` - Function type

## Variables

### Declaration

```khaos
let x = 42;              # Mutable variable
const PI = 3.14159;      # Immutable constant
```

### Assignment

```khaos
x = 100;                 # Simple assignment
x += 5;                  # Compound assignment
x -= 3;
```

## Operators

### Arithmetic

```khaos
+ - * / %                # Basic arithmetic
**                       # Power/exponentiation
```

### Comparison

```khaos
== !=                    # Equality
< <= > >=                # Relational
```

### Logical

```khaos
and or not               # Boolean logic
```

### Precedence (highest to lowest)

1. `**` (power)
2. `* / %` (multiplication, division, modulo)
3. `+ -` (addition, subtraction)
4. `< <= > >=` (comparison)
5. `== !=` (equality)
6. `not` (logical not)
7. `and` (logical and)
8. `or` (logical or)

## Control Flow

### If Statements

```khaos
if condition {
    # then block
} else {
    # else block
}

# Without else
if x > 0 {
    print "positive";
}
```

### While Loops

```khaos
while condition {
    # loop body
}

# Example
let i = 0;
while i < 10 {
    print i;
    i += 1;
}
```

### For Loops (Planned)

```khaos
for item in collection {
    print item;
}
```

### Break and Continue

```khaos
while true {
    if should_exit {
        break;      # Exit loop
    }
    if should_skip {
        continue;   # Skip to next iteration
    }
}
```

## Functions

### Declaration

```khaos
fn function_name(param1, param2) {
    # function body
    return result;
}
```

### Calling

```khaos
let result = function_name(arg1, arg2);
```

### Examples

```khaos
fn add(a, b) {
    return a + b;
}

fn greet(name) {
    print "Hello, " + name + "!";
    # Implicit return for void functions
}

# Recursive functions
fn factorial(n) {
    if n <= 1 {
        return 1;
    }
    return n * factorial(n - 1);
}
```

## I/O Operations

### Print Statement

```khaos
print expression;        # Print with newline
show expression;         # Alternative syntax
```

String concatenation:
```khaos
print "Value: " + x;
```

## Advanced Features (Planned)

### Decorators

```khaos
@optimize(neural=true)
fn hot_function(data) {
    # This function will be optimized using neural algorithms
}
```

### Arrays (Planned)

```khaos
let arr = [1, 2, 3, 4, 5];
let first = arr[0];
```

### Dictionaries (Planned)

```khaos
let person = {
    "name": "Builder",
    "power": 9001
};
```

## Grammar (EBNF-style)

```ebnf
program = statement* ;

statement = variable_declaration
          | function_declaration
          | if_statement
          | while_statement
          | return_statement
          | print_statement
          | expression_statement
          | break_statement
          | continue_statement
          ;

variable_declaration = ("let" | "const") IDENTIFIER "=" expression ";" ;

function_declaration = "fn" IDENTIFIER "(" parameters? ")" block ;

parameters = IDENTIFIER ("," IDENTIFIER)* ;

if_statement = "if" expression block ("else" block)? ;

while_statement = "while" expression block ;

return_statement = "return" expression? ";" ;

print_statement = ("print" | "show") expression ";" ;

expression_statement = expression ";" ;

block = "{" statement* "}" ;

expression = assignment ;

assignment = logical_or (("=" | "+=" | "-=") assignment)? ;

logical_or = logical_and ("or" logical_and)* ;

logical_and = equality ("and" equality)* ;

equality = comparison (("==" | "!=") comparison)* ;

comparison = term (("<" | "<=" | ">" | ">=") term)* ;

term = factor (("+" | "-") factor)* ;

factor = power (("*" | "/" | "%") power)* ;

power = unary ("**" unary)* ;

unary = ("not" | "-") unary | call ;

call = primary ("(" arguments? ")" | "[" expression "]")* ;

arguments = expression ("," expression)* ;

primary = INTEGER | FLOAT | STRING | BOOLEAN
        | IDENTIFIER
        | "(" expression ")"
        ;
```

## Stage Roadmap

### Stage 0: Foundation (Current)
- ✓ Basic lexer
- ⚠ Parser (in progress)
- ⚠ AST
- ⚠ Simple interpreter/VM
- ⚠ LLVM codegen

### Stage 1: Minimal Subset
- Define minimal compilable subset
- Bootstrap compiler in minimal Khaos

### Stage 2: Self-Hosting
- Full compiler in Khaos
- Compile itself

### Stage 3: Neural Optimization
- MLIR backend
- Transformer-based optimizer
- Self-learning optimization

### Stage 4: Multi-Modal
- Esoteric frontends
- Visual/gestural input
- Reality compilation

---

*This specification evolves with the language.*  
*Sovereignty through self-definition.*
