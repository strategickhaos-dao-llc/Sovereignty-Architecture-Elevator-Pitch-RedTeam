# Code-to-Diagram Translator

> **IDEA_002** | Category: devtools | Department: infra_cloud

## Overview

Tool that ingests source code and generates living architecture diagrams
that update automatically as the codebase evolves.

## Purpose

The Code-to-Diagram Translator is designed to bridge the gap between code
and visual documentation. It automatically parses source code to extract:

- Class hierarchies and relationships
- Module dependencies and imports
- Service communication patterns
- Data flow between components

## Features

- **Automatic Parsing**: Supports multiple programming languages
- **Living Diagrams**: Diagrams update as code changes
- **Multiple Output Formats**: Mermaid, PlantUML, DOT, SVG
- **CI/CD Integration**: Generate diagrams on every commit
- **Customizable Themes**: Match your documentation style

## Video Module

This project is tied to **Q034** in the 100 Bloom's Questions framework.

## Quick Start

```bash
# Build the container
docker build -t strategickhaos/code-diagram-translator:dev .

# Run the translator
docker run -v $(pwd)/your-code:/input strategickhaos/code-diagram-translator:dev
```

## Usage

```python
from code_diagram_translator import Translator

# Initialize the translator
translator = Translator()

# Parse a codebase
translator.parse("./src")

# Generate diagram
diagram = translator.generate(format="mermaid")
print(diagram)
```

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                 Code-to-Diagram Translator              │
├─────────────────────────────────────────────────────────┤
│  ┌─────────┐   ┌──────────┐   ┌───────────────────────┐ │
│  │ Parser  │──▶│ Analyzer │──▶│ Diagram Generator     │ │
│  └─────────┘   └──────────┘   └───────────────────────┘ │
│       ▲                               │                 │
│       │                               ▼                 │
│  ┌─────────┐                   ┌───────────────────────┐│
│  │ Source  │                   │ Output (Mermaid/DOT)  ││
│  │  Code   │                   └───────────────────────┘│
│  └─────────┘                                            │
└─────────────────────────────────────────────────────────┘
```

## Configuration

Create a `diagram-config.yaml` in your project root:

```yaml
code_diagram_translator:
  input_paths:
    - ./src
    - ./lib
  output_format: mermaid
  include_private: false
  max_depth: 5
  themes:
    default: dark
```

## Integration with StrategicKhaos

This service is overseen by **svc-claude-prime** (Governance Verification Node)
and integrates with the KnowledgePod demonstration pipeline.

## Development Status

**Maturity Level**: concept

## Contributing

See the main repository [CONTRIBUTORS.md](../../CONTRIBUTORS.md) for guidelines.

## License

Part of the StrategicKhaos DAO LLC ecosystem.
