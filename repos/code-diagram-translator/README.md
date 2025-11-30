# Code-to-Diagram Translator

> **IDEA_002** | Category: devtools | Maturity: concept

Tool that ingests source code and generates living architecture diagrams that update automatically as the codebase evolves.

## Overview

The Code-to-Diagram Translator is a DevOps tool that automatically analyzes source code repositories and generates visual architecture diagrams. These diagrams stay in sync with the codebase as it evolves, providing always-up-to-date documentation.

## Features

- **Multi-Language Support**: Parse Python, JavaScript/TypeScript, Java, Go, and more
- **Diagram Formats**: Generate Mermaid, PlantUML, DOT (Graphviz), and SVG outputs
- **CI/CD Integration**: Auto-update diagrams on every commit via GitHub Actions
- **Dependency Mapping**: Visualize module dependencies and data flows
- **API Documentation**: Extract and visualize REST/GraphQL endpoints

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python main.py --repo ./path/to/code --output ./diagrams

# Using Docker
docker build -t svc-code-diagram .
docker run -v $(pwd):/app/repo svc-code-diagram --repo /app/repo
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `IDEA_ID` | Unique idea identifier | `IDEA_002` |
| `NAMESPACE` | Kubernetes namespace | `ns-infra` |
| `OUTPUT_FORMAT` | Diagram format (mermaid/plantuml/dot) | `mermaid` |
| `WATCH_MODE` | Enable file watching | `false` |

## Kubernetes Deployment

```bash
kubectl apply -f k8s/deployment.yaml
```

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Source Code   │────▶│   Parser Engine  │────▶│  Diagram Gen    │
│   Repository    │     │   (AST Analysis) │     │  (Mermaid/SVG)  │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                                │
                                ▼
                        ┌──────────────────┐
                        │  Dependency Map  │
                        │  (Graph DB)      │
                        └──────────────────┘
```

## Integration with StrategicKhaos

This service integrates with:
- **svc-claude-prime**: For verification and code review
- **ideas_catalog.yaml**: Registered as IDEA_002
- **docker-compose.board.yml**: Part of the board orchestration layer

## Video Module

Tied to **Q034** in the 100-question Bloom's taxonomy curriculum.

## License

MIT License - StrategicKhaos DAO LLC

---

*Part of the StrategicKhaos Sovereignty Architecture*
