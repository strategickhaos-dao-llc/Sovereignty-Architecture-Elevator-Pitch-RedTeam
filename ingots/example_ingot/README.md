# Example Ingot

A template ingot demonstrating the standard structure for self-contained, modular components in the Sovereignty Architecture.

## Overview

This ingot serves as a reference implementation showing how to structure an ingot for the Sovereignty Architecture Ingot Forge. Use this as a starting point when creating new ingots.

## Structure

```
example_ingot/
├── manifest.yaml    # Ingot metadata and configuration
├── README.md        # This documentation
├── src/             # Source code
│   ├── init.sh      # Initialization script
│   └── cli.sh       # CLI entry point
└── tests/           # Test files
    └── test_example.sh
```

## Usage

### Loading the Ingot

Use the smelter to load this ingot:

```bash
./scripts/smelter.sh load example_ingot
```

### Running CLI Commands

```bash
./scripts/smelter.sh run example_ingot example-cli
```

### Running Tests

```bash
./scripts/smelter.sh test example_ingot
```

## Configuration

This ingot accepts the following environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `EXAMPLE_INGOT_DEBUG` | Enable debug mode | `false` |

## Dependencies

- **Ingots**: None
- **External**: None

## Creating Your Own Ingot

1. Copy this directory to `ingots/your_ingot_name/`
2. Update `manifest.yaml` with your ingot's metadata
3. Replace the source files in `src/` with your implementation
4. Add tests in `tests/`
5. Update this README with your ingot's documentation

## License

MIT License - See the main repository LICENSE file.
