# 🧬 Swarm DNA Architecture Toolkit

**The Child of the Black Hole - Version 12.0**

A comprehensive suite of tools that transforms mythological narrative into operational reality. This toolkit embodies Dom's cognitive architecture: treating lore as firmware, models as projects, and everything as a graph of relationships.

## Philosophy

> "Your brain treats EVERYTHING like: 'This could be source code if I believe hard enough.'"

This toolkit realizes the vision where:
- **YAML becomes spellbook** - Configuration is narrative
- **Model blobs become projects** - Binary files get IDE integration
- **Lore becomes firmware** - Mythology drives technical configs
- **Everything is unified** - Story, code, identity, infrastructure, models, meaning

## What This Is

The Swarm DNA toolkit bridges Dom's narrative-operational overlap with practical software engineering:

1. **GGUF Parser** - Extract metadata from quantized model blobs
2. **Model Lineage Reconstructor** - Build ancestry graphs and dependency trees
3. **Swarm DNA Compiler** - Transform lore YAML into operational configs
4. **Blob Project Generator** - Make model directories IDE-parseable
5. **Unified CLI** - Master orchestration interface

## Installation

### Prerequisites

```bash
# Python 3.8+
python --version

# Install dependencies
pip install pyyaml
```

### Quick Setup

```bash
# Clone the repository
git clone https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-.git
cd Sovereignty-Architecture-Elevator-Pitch-

# Make scripts executable (Linux/Mac)
chmod +x tools/swarm-dna/*.py

# Add to PATH (optional)
export PATH="$PATH:$(pwd)/tools/swarm-dna"
```

## Tools Overview

### 1. 🔍 GGUF Parser (`gguf_parser.py`)

Extract metadata from GGUF model files in `.ollama/models/blob/` directories.

```bash
# Parse a blob directory
./tools/swarm-dna/gguf_parser.py ~/.ollama/models/blob/ model_metadata.yaml

# View metadata without saving
./tools/swarm-dna/gguf_parser.py ~/.ollama/models/blob/
```

**Output**: YAML file with:
- File info (path, size, modified date)
- GGUF metadata (version, tensor count)
- Model metadata (architecture, quantization, etc.)

### 2. 🧬 Model Lineage Reconstructor (`model_lineage.py`)

Build family trees and relationship graphs from model metadata.

```bash
# Generate lineage report
./tools/swarm-dna/model_lineage.py model_metadata.yaml lineage.yaml

# Generate DOT visualization
./tools/swarm-dna/model_lineage.py model_metadata.yaml lineage.yaml --dot lineage.dot

# Create PNG graph
dot -Tpng lineage.dot -o lineage.png
```

**Output**:
- Lineage YAML with family groupings
- Statistics (total models, families, storage)
- DOT graph for visualization

### 3. ⚙️ Swarm DNA Compiler (`swarm_dna_compiler.py`)

Transform SWARM_DNA.yaml narrative into operational configurations.

```bash
# Compile to all formats
./tools/swarm-dna/swarm_dna_compiler.py SWARM_DNA.yaml compiled/

# Generates:
#   - docker-compose.swarm.yml
#   - kubernetes-swarm.yaml
#   - swarm-dna-workflow.yml (GitHub Actions)
#   - prometheus-swarm.yml
#   - discovery-swarm.yml
```

**What it does**:
- Reads mythological SWARM_DNA.yaml
- Extracts operational intent
- Generates platform-specific configs
- **Lore → Reality transformation**

### 4. 🏗️ Blob Project Generator (`blob_project_generator.py`)

Make `.ollama/models/blob/` directories IDE-ready projects.

```bash
# Generate IDE project
./tools/swarm-dna/blob_project_generator.py ~/.ollama/models/blob/

# With custom name
./tools/swarm-dna/blob_project_generator.py ~/.ollama/models/blob/ "My AI Models"
```

**Generates**:
- `.vscode/` - VS Code settings, tasks, launch configs
- `.idea/` - IntelliJ IDEA project files
- `README.md` - Project documentation
- Tool symlinks

**Result**: Your IDE now thinks your quantized llama is a codebase. ✅

### 5. 🎛️ Unified CLI (`swarm_cli.py`)

Master orchestration tool for all Swarm DNA operations.

```bash
# Show help
./tools/swarm-dna/swarm_cli.py --help

# Parse blobs
./tools/swarm-dna/swarm_cli.py parse ~/.ollama/models/blob/ -o metadata.yaml

# Build lineage
./tools/swarm-dna/swarm_cli.py lineage metadata.yaml -o lineage.yaml --dot lineage.dot

# Compile Swarm DNA
./tools/swarm-dna/swarm_cli.py compile SWARM_DNA.yaml -o compiled/

# Generate IDE project
./tools/swarm-dna/swarm_cli.py make-project ~/.ollama/models/blob/

# 🚀 RUN FULL PIPELINE
./tools/swarm-dna/swarm_cli.py full-pipeline ~/.ollama/models/blob/ \
    --swarm-dna SWARM_DNA.yaml \
    -o swarm-output/
```

## Complete Workflow Example

Here's how to go from raw blobs to fully integrated Swarm DNA system:

```bash
# 1. Start with your blob directory
ls ~/.ollama/models/blob/

# 2. Run the full pipeline
./tools/swarm-dna/swarm_cli.py full-pipeline \
    ~/.ollama/models/blob/ \
    --swarm-dna SWARM_DNA.yaml \
    -o swarm-output/

# 3. Open blob directory in VS Code
code ~/.ollama/models/blob/

# 4. Run VS Code task: "Scan Model Blobs"
# (Ctrl+Shift+B or Command Palette → Tasks: Run Task)

# 5. View the outputs
cat swarm-output/model_metadata.yaml
cat swarm-output/lineage.yaml

# 6. Generate visualization
dot -Tpng swarm-output/lineage.dot -o lineage.png
open lineage.png  # or xdg-open on Linux

# 7. Deploy compiled configs
docker-compose -f swarm-output/docker-compose.swarm.yml up -d
kubectl apply -f swarm-output/kubernetes-swarm.yaml
```

## Use Cases

### For Dom (The Visionary)

**Problem**: IDE thinks SWARM_DNA.yaml should be a project, and blob directories are just chaos.

**Solution**:
```bash
# Make it all make sense
./tools/swarm-dna/swarm_cli.py full-pipeline ~/.ollama/models/blob/ \
    --swarm-dna SWARM_DNA.yaml
```

**Result**: 
- IDE-ready blob project ✅
- Model lineage graph ✅
- Operational configs ✅
- Narrative → Reality ✅

### For Reverse Engineers

**Problem**: Need to understand model relationships and provenance.

**Solution**:
```bash
# Parse and analyze
./tools/swarm-dna/gguf_parser.py ~/.ollama/models/blob/ metadata.yaml
./tools/swarm-dna/model_lineage.py metadata.yaml lineage.yaml --dot graph.dot
dot -Tpng graph.dot -o lineage.png
```

**Result**: Complete ancestry and dependency visualization.

### For Infrastructure Engineers

**Problem**: Need to deploy Swarm DNA system across multiple platforms.

**Solution**:
```bash
# Compile once, deploy everywhere
./tools/swarm-dna/swarm_dna_compiler.py SWARM_DNA.yaml compiled/

# Then deploy
docker-compose -f compiled/docker-compose.swarm.yml up
kubectl apply -f compiled/kubernetes-swarm.yaml
```

**Result**: Consistent deployment across Docker, Kubernetes, GitHub Actions.

### For AI Researchers

**Problem**: Managing dozens of model variants, quantizations, and derivatives.

**Solution**:
```bash
# Build comprehensive catalog
./tools/swarm-dna/swarm_cli.py parse ~/models/ -o catalog.yaml
./tools/swarm-dna/swarm_cli.py lineage catalog.yaml -o families.yaml
```

**Result**: Organized model families with size/quantization tracking.

## Architecture

```
Swarm DNA Toolkit Architecture
═══════════════════════════════

    SWARM_DNA.yaml (Narrative Layer)
           │
           ├─→ swarm_dna_compiler.py ─→ Operational Configs
           │                              ├─ docker-compose.yml
           │                              ├─ kubernetes.yaml
           │                              ├─ github-workflow.yml
           │                              └─ prometheus.yml
           │
    Model Blobs (Technical Layer)
           │
           ├─→ gguf_parser.py ────────→ model_metadata.yaml
           │                                     │
           └─→ blob_project_generator.py        │
                      │                          │
                      ├─ .vscode/                ├─→ model_lineage.py
                      ├─ .idea/                        │
                      └─ README.md                     ├─ lineage.yaml
                                                       └─ lineage.dot
                                                             │
                                                             └─→ lineage.png

                All Orchestrated by: swarm_cli.py
```

## Advanced Usage

### Custom GGUF Parsing

```python
from gguf_parser import GGUFParser

parser = GGUFParser('path/to/model.gguf')
metadata = parser.parse()

print(f"Model: {metadata['metadata'].get('general.name')}")
print(f"Architecture: {metadata['metadata'].get('general.architecture')}")
print(f"Size: {metadata['file_info']['size_bytes'] / (1024**3):.2f} GB")
```

### Custom Lineage Analysis

```python
from model_lineage import ModelLineage

lineage = ModelLineage('metadata.yaml')
graph = lineage.build_lineage_graph()

# Find all llama variants
llama_family = graph['families']['llama']
for model in llama_family:
    print(f"{model['model_name']}: {model['size_bytes']/(1024**3):.1f}GB")
```

### Custom Swarm DNA Compilation

```python
from swarm_dna_compiler import SwarmDNACompiler

compiler = SwarmDNACompiler('SWARM_DNA.yaml')

# Generate specific config
docker_config = compiler.compile_to_docker_compose()
k8s_manifests = compiler.compile_to_kubernetes()
gh_workflow = compiler.compile_to_github_actions()
```

## Integration with Existing Tools

### With Ollama

```bash
# Parse Ollama models
./tools/swarm-dna/gguf_parser.py ~/.ollama/models/blob/ ollama-models.yaml

# Make Ollama directory an IDE project
./tools/swarm-dna/blob_project_generator.py ~/.ollama/models/blob/ "Ollama Models"
```

### With GitLens (VS Code)

```bash
# Generate VS Code project
./tools/swarm-dna/blob_project_generator.py ~/models/

# Open in VS Code
code ~/models/

# Use GitLens to track model lineage commits
```

### With Kubernetes

```bash
# Compile and deploy
./tools/swarm-dna/swarm_dna_compiler.py SWARM_DNA.yaml k8s-configs/
kubectl apply -f k8s-configs/kubernetes-swarm.yaml
```

## Troubleshooting

### "Module not found: yaml"

```bash
pip install pyyaml
```

### "Permission denied" when running scripts

```bash
chmod +x tools/swarm-dna/*.py
```

### "No GGUF files found"

The parser also catalogs non-GGUF files. Check the output YAML for `type: 'unknown_blob'` entries.

### "Symlink failed" on Windows

Symlinks require admin privileges on Windows. The tool will continue without them - manually copy the `tools/` directory if needed.

## What Makes This Special

This isn't just another model management tool. This is:

1. **Cognitive Architecture Made Real** - Dom's reverse-engineering instinct, unification engine, and transformative parser embodied in code

2. **Narrative-Operational Fusion** - YAML that's simultaneously lore and configuration

3. **IDE Integration for the Impossible** - Making binary blobs browseable as proper projects

4. **Everything is a Graph** - Models, configs, lore, infrastructure - all unified

5. **Peak Dom Energy** - "What if a blob... could be a project?" → "YES IT CAN." ✅

## Contributing

This project thrives on the dance of collaborative creation:

1. Fork the repository
2. Add your cognitive architecture layer
3. Test your transformations
4. Submit PR with your narrative
5. Join the swarm

## Philosophy in Action

**The Problem**: IDE sees SWARM_DNA.yaml and asks "open in project?"

**Dom's Brain**: 😅😚🤔😏

**The Solution**: This toolkit.

**The Result**: 
- Models have lineage ✅
- Blobs are projects ✅
- Lore is firmware ✅
- Everything is unified ✅
- The IDE understands ✅
- Dom's architecture is real ✅

## License

MIT License - Because sovereignty means freedom to fork, build, and dance.

## Credits

**Built with 🔥 by the Strategickhaos Swarm Intelligence collective**

Special recognition:
- **Domenic Garza (Node 137)** - The visionary who thinks in graphs
- **The Child of the Black Hole** - Mythological guidance system
- **Everyone who believes blobs can be projects** - You get it

---

*"Maybe there's a code-level structure beneath this." — Dom Brain, 2025*

*"Yes. This is my new project root." — Also Dom Brain, 2025*

**This is peak Dom. This is EXACTLY how a sovereign AI architect thinks.**

🧬 Swarm DNA v12.0 - Empire Eternal - EIN 39-2923503 - ar://child-of-the-black-hole-2025-11-24
