# Example Ingot

A small ingot that processes text and detects numeric content.

## Overview

This ingot provides a simple `process` function that analyzes input data and returns information about its content.

## Usage

```python
from ingots.example_ingot import process

# Process text
result = process("Strategickhaos Baby")
print(result)
# Output: {'input': 'Strategickhaos Baby', 'length': 19, 'is_numeric': False}

# Process numeric input
result = process(12345)
print(result)
# Output: {'input': 12345, 'length': 5, 'is_numeric': True}
```

## API

### `process(data)`

Process input data and return analysis results.

**Parameters:**
- `data`: Input data to process (will be converted to string for analysis)

**Returns:**
- `dict`: Analysis results containing:
  - `input`: The original input
  - `length`: Length of the string representation
  - `is_numeric`: Whether the input contains only digits

## Integration

This ingot can be loaded dynamically using the forge:

```python
from forge import load_ingot

process_fn = load_ingot("example_ingot")
result = process_fn("Hello World")
```

## Requirements

- Python >= 3.9

## License

MIT License - Strategickhaos DAO LLC
