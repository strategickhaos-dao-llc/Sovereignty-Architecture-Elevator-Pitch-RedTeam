# 🔥 Ingot Forge Architecture

The **Ingot Forge** is a modular architecture pattern for the Sovereignty Architecture ecosystem. It provides a standardized way to create, manage, and deploy self-contained functional modules called "ingots."

## 🏛️ Overview

An **ingot** is a self-contained, reusable module that:
- Encapsulates specific functionality
- Has a well-defined interface
- Can be loaded/unloaded independently
- Follows a consistent structure

The **smelter** is the loader/manager that:
- Discovers and lists available ingots
- Validates ingot structure
- Loads and initializes ingots
- Runs ingot CLI commands and tests

## 📁 Directory Structure

```
Sovereignty-Architecture/
├── ingots/                          # 🆕 Ingot modules directory
│   ├── example_ingot/               # Example/template ingot
│   │   ├── manifest.yaml            # Metadata and configuration
│   │   ├── README.md                # Documentation
│   │   ├── src/                     # Source code
│   │   │   ├── init.sh              # Initialization script
│   │   │   └── cli.sh               # CLI entry point
│   │   └── tests/                   # Test files
│   │       └── test_example.sh      # Test script
│   │
│   └── your_ingot/                  # Your custom ingot
│       ├── manifest.yaml
│       ├── README.md
│       ├── src/
│       └── tests/
│
├── scripts/
│   └── smelter.sh                   # 🆕 Ingot loader/manager
│
├── INGOT_FORGE.md                   # 🆕 This documentation
└── ...
```

## 🚀 Quick Start

### List Available Ingots

```bash
./scripts/smelter.sh list
```

### Load an Ingot

```bash
./scripts/smelter.sh load example_ingot
```

### Run Ingot Commands

```bash
./scripts/smelter.sh run example_ingot demo
./scripts/smelter.sh run example_ingot help
./scripts/smelter.sh run example_ingot version
```

### Test an Ingot

```bash
./scripts/smelter.sh test example_ingot
```

### Validate Ingot Structure

```bash
./scripts/smelter.sh validate example_ingot
```

### View Ingot Information

```bash
./scripts/smelter.sh info example_ingot
```

## 📝 Creating a New Ingot

### 1. Create Directory Structure

```bash
mkdir -p ingots/my_ingot/src ingots/my_ingot/tests
```

### 2. Create manifest.yaml

The manifest is the heart of your ingot. It defines metadata, dependencies, and entry points.

```yaml
# ingots/my_ingot/manifest.yaml

name: my_ingot
version: "1.0.0"
description: |
  A brief description of what this ingot does.

author:
  name: Your Name
  contact: your@email.com

# Dependencies on other ingots
dependencies:
  ingots:
    - name: another_ingot
      version: ">=1.0.0"
  external:
    - name: some-npm-package
      version: "^4.0.0"
      ecosystem: npm

# Entry points
entry_points:
  cli:
    - name: my-command
      script: src/cli.sh
      description: Main CLI command
  hooks:
    - event: on_load
      handler: src/init.sh
      description: Initialization hook

# Categorization
tags:
  - utility
  - automation

# Environment variables
environment:
  required:
    - name: MY_INGOT_API_KEY
      description: API key for external service
  optional:
    - name: MY_INGOT_DEBUG
      description: Enable debug mode
      default: "false"

license: MIT
```

### 3. Create README.md

Document your ingot's purpose, usage, and configuration.

```markdown
# My Ingot

Description of what this ingot does.

## Usage

./scripts/smelter.sh run my_ingot command

## Configuration

| Variable | Description | Required |
|----------|-------------|----------|
| MY_INGOT_API_KEY | API key | Yes |

## License

MIT
```

### 4. Create Source Files

**src/init.sh** - Called when the ingot is loaded:

```bash
#!/usr/bin/env bash
set -euo pipefail

echo "Initializing my_ingot..."
# Your initialization logic here
echo "my_ingot initialized"
```

**src/cli.sh** - CLI entry point:

```bash
#!/usr/bin/env bash
set -euo pipefail

case "${1:-help}" in
    help)
        echo "Usage: my_ingot <command>"
        ;;
    version)
        echo "my_ingot v1.0.0"
        ;;
    *)
        echo "Unknown command: $1"
        exit 1
        ;;
esac
```

### 5. Create Tests

**tests/test_my_ingot.sh**:

```bash
#!/usr/bin/env bash
set -euo pipefail

# Test that CLI works
./ingots/my_ingot/src/cli.sh help > /dev/null
echo "✓ CLI help works"

echo "All tests passed!"
```

### 6. Validate and Load

```bash
./scripts/smelter.sh validate my_ingot
./scripts/smelter.sh load my_ingot
./scripts/smelter.sh test my_ingot
```

## 🔐 Security Best Practices

### Environment Variables

- **Never** commit real secrets to manifest.yaml or source code
- Use `.env` files for local development (already in `.gitignore`)
- Use environment variables for sensitive configuration
- Document required environment variables in manifest.yaml

### Secrets in Ingots

```yaml
# manifest.yaml - DO THIS
environment:
  required:
    - name: MY_API_KEY
      description: API key (set via environment)

# DON'T DO THIS
# api_key: sk-real-secret-key-abc123
```

### Per-Ingot .env Files

Each ingot can have its own `.env.example`:

```bash
# ingots/my_ingot/.env.example
MY_INGOT_API_KEY=your_api_key_here
MY_INGOT_DEBUG=false
```

Add ingot-specific .env to `.gitignore`:

```gitignore
ingots/*/.env
```

## 🔧 Advanced Usage

### Using Ingots as Submodules

For large or reusable ingots, consider using git submodules:

```bash
# Add an ingot as a submodule
git submodule add https://github.com/org/useful-ingot.git ingots/useful-ingot

# Update submodule
git submodule update --remote ingots/useful-ingot
```

### Ingot Dependencies

Ingots can depend on other ingots. The smelter will eventually support automatic dependency resolution:

```yaml
# manifest.yaml
dependencies:
  ingots:
    - name: base_utilities
      version: ">=1.0.0"
    - name: logging_ingot
      version: "^2.0.0"
```

### Custom Entry Points

Beyond `init.sh` and `cli.sh`, you can define custom entry points:

```yaml
entry_points:
  cli:
    - name: backup
      script: src/backup.sh
    - name: restore
      script: src/restore.sh
  hooks:
    - event: on_load
      handler: src/init.sh
    - event: on_unload
      handler: src/cleanup.sh
    - event: on_deploy
      handler: src/deploy-hook.sh
```

## 📊 Ingot Lifecycle

```
┌─────────────┐
│  CREATED    │  Directory exists with manifest
└─────┬───────┘
      │ smelter.sh validate
      ▼
┌─────────────┐
│  VALIDATED  │  Structure verified
└─────┬───────┘
      │ smelter.sh load
      ▼
┌─────────────┐
│   LOADED    │  init.sh executed
└─────┬───────┘
      │ smelter.sh run
      ▼
┌─────────────┐
│  RUNNING    │  CLI commands available
└─────────────┘
```

## 🤝 Contributing Ingots

When contributing new ingots to the Sovereignty Architecture:

1. Follow the standard structure (manifest.yaml, README.md, src/, tests/)
2. Include comprehensive tests
3. Document all environment variables
4. Never commit secrets
5. Tag appropriately for discoverability
6. Include usage examples in README.md

## 📚 Additional Resources

- [Main README](README.md) - Project overview
- [Security Guidelines](SECURITY.md) - Security best practices
- [Community Guidelines](COMMUNITY.md) - Contribution guidelines

---

**Built with 🔥 by the Strategickhaos Swarm Intelligence collective**

*"Each ingot is a spark. Together, they forge sovereignty."*
