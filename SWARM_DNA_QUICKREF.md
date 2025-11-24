# 🧬 Swarm DNA Quick Reference Card

One-page reference for all Swarm DNA operations.

## Installation

```bash
# Install dependencies
pip install pyyaml

# Make scripts executable
chmod +x tools/swarm-dna/*.py
```

## Common Commands

### 🎬 Run Demo
```bash
./demo-swarm-dna.sh
```

### 🔍 Parse Model Blobs
```bash
# Parse directory
./tools/swarm-dna/gguf_parser.py ~/.ollama/models/blob/ metadata.yaml

# View without saving
./tools/swarm-dna/gguf_parser.py ~/.ollama/models/blob/
```

### 🧬 Build Model Lineage
```bash
# Generate lineage report
./tools/swarm-dna/model_lineage.py metadata.yaml lineage.yaml

# With visualization
./tools/swarm-dna/model_lineage.py metadata.yaml lineage.yaml --dot lineage.dot
dot -Tpng lineage.dot -o lineage.png
```

### ⚙️ Compile Swarm DNA
```bash
# Compile to all formats
./tools/swarm-dna/swarm_dna_compiler.py SWARM_DNA.yaml compiled/

# Output: docker-compose, kubernetes, github-actions, prometheus, discovery
```

### 🏗️ Generate IDE Project
```bash
# Basic
./tools/swarm-dna/blob_project_generator.py ~/.ollama/models/blob/

# With custom name
./tools/swarm-dna/blob_project_generator.py ~/models/ "My Models"
```

### 🚀 Full Pipeline
```bash
# Everything at once
./tools/swarm-dna/swarm_cli.py full-pipeline ~/.ollama/models/blob/ \
    --swarm-dna SWARM_DNA.yaml \
    -o swarm-output/
```

## Using the CLI

### Parse
```bash
./tools/swarm-dna/swarm_cli.py parse <blob_dir> [-o output.yaml]
```

### Lineage
```bash
./tools/swarm-dna/swarm_cli.py lineage <metadata.yaml> [-o lineage.yaml] [--dot graph.dot]
```

### Compile
```bash
./tools/swarm-dna/swarm_cli.py compile <SWARM_DNA.yaml> [-o output_dir]
```

### Make Project
```bash
./tools/swarm-dna/swarm_cli.py make-project <blob_dir> [--name "Project Name"]
```

### Full Pipeline
```bash
./tools/swarm-dna/swarm_cli.py full-pipeline <blob_dir> \
    [--swarm-dna SWARM_DNA.yaml] \
    [-o output_dir]
```

## File Locations

```
Repository Root/
├── SWARM_DNA.yaml              # Core identity manifest
├── SWARM_DNA_GUIDE.md          # Complete guide
├── SWARM_DNA_QUICKREF.md       # This file
├── demo-swarm-dna.sh           # Demo script
├── tools/swarm-dna/
│   ├── README.md               # Tool documentation
│   ├── gguf_parser.py          # Model parser
│   ├── model_lineage.py        # Lineage builder
│   ├── swarm_dna_compiler.py   # Config compiler
│   ├── blob_project_generator.py  # IDE project gen
│   ├── swarm_cli.py            # Master CLI
│   └── requirements.txt        # Dependencies
└── templates/swarm-project/
    ├── example-workflow.yml    # GitHub Actions example
    └── example-swarm-dna-minimal.yaml  # Minimal template
```

## Deployment

### Docker Compose
```bash
# Compile and deploy
./tools/swarm-dna/swarm_dna_compiler.py SWARM_DNA.yaml configs/
docker-compose -f configs/docker-compose.swarm.yml up -d

# Stop
docker-compose -f configs/docker-compose.swarm.yml down
```

### Kubernetes
```bash
# Compile and deploy
./tools/swarm-dna/swarm_dna_compiler.py SWARM_DNA.yaml configs/
kubectl apply -f configs/kubernetes-swarm.yaml

# Check status
kubectl get all -n swarm-dna

# Delete
kubectl delete -f configs/kubernetes-swarm.yaml
```

### GitHub Actions
```bash
# Copy workflow to your repo
cp configs/swarm-dna-workflow.yml .github/workflows/

# Commit and push
git add .github/workflows/swarm-dna-workflow.yml
git commit -m "Add Swarm DNA workflow"
git push
```

## IDE Integration

### VS Code
```bash
# Generate project
./tools/swarm-dna/blob_project_generator.py ~/.ollama/models/blob/

# Open in VS Code
code ~/.ollama/models/blob/

# Run task (Ctrl+Shift+B)
# → Select: "Scan Model Blobs"
```

### IntelliJ IDEA
```bash
# Generate project
./tools/swarm-dna/blob_project_generator.py ~/.ollama/models/blob/

# Open in IDEA
# File → Open → Select: ~/.ollama/models/blob/

# Run → Parse GGUF Metadata
```

## Python API

```python
# Parse blobs
from tools.swarm_dna.gguf_parser import GGUFParser, parse_blob_directory
result = parse_blob_directory('~/.ollama/models/blob/')

# Build lineage
from tools.swarm_dna.model_lineage import ModelLineage
lineage = ModelLineage('metadata.yaml')
report = lineage.generate_lineage_report()

# Compile Swarm DNA
from tools.swarm_dna.swarm_dna_compiler import SwarmDNACompiler
compiler = SwarmDNACompiler('SWARM_DNA.yaml')
results = compiler.compile_all('output/')

# Generate IDE project
from tools.swarm_dna.blob_project_generator import BlobProjectGenerator
gen = BlobProjectGenerator('~/.ollama/models/blob/')
gen.generate_all()
```

## Troubleshooting

### PyYAML not found
```bash
pip install pyyaml
```

### Permission denied
```bash
chmod +x tools/swarm-dna/*.py
```

### GraphViz not installed
```bash
# Ubuntu/Debian
sudo apt install graphviz

# macOS
brew install graphviz
```

### No models found
```bash
# Check path
ls ~/.ollama/models/blob/

# Or use test directory
mkdir -p ~/test-models
./tools/swarm-dna/blob_project_generator.py ~/test-models/
```

## Key Concepts

- **SWARM_DNA.yaml** = Narrative + Technical reality unified
- **Lore → Config** = Mythological YAML becomes operational configs
- **Blobs → Projects** = Binary files get IDE integration
- **Everything is a graph** = Models, configs, lore - all relationships
- **Peak Dom** = Reverse-engineering oracle meets mythopoetic firmware

## Getting Help

```bash
# CLI help
./tools/swarm-dna/swarm_cli.py --help
./tools/swarm-dna/swarm_cli.py <command> --help

# Documentation
cat SWARM_DNA_GUIDE.md
cat tools/swarm-dna/README.md

# Demo
./demo-swarm-dna.sh
```

## Links

- **GitHub**: https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-
- **Main README**: [README.md](README.md)
- **Complete Guide**: [SWARM_DNA_GUIDE.md](SWARM_DNA_GUIDE.md)
- **Tool Docs**: [tools/swarm-dna/README.md](tools/swarm-dna/README.md)

---

🧬 **Swarm DNA v12.0** - Child of the Black Hole - EIN 39-2923503 - Empire Eternal

Built with 🔥 by the Strategickhaos Swarm Intelligence collective

*"This is peak Dom. This is EXACTLY how a sovereign AI architect thinks."*
