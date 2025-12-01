# RDKit Tutorials Environment Setup Guide

**Complete cheminformatics setup for molecular visualization, drug discovery, and computational chemistry workflows.**

## 🧪 Overview

This guide provides instructions for setting up an RDKit tutorials environment. RDKit is the leading open-source cheminformatics library, used extensively in drug discovery, molecular modeling, and chemical informatics.

## 🚀 Quick Start

### Option 1: Clone RDKit Official Tutorials

The official RDKit tutorials repository is safe and maintained by the RDKit core team:

```bash
# 1. Clone the repo
git clone https://github.com/rdkit/rdkit-tutorials.git
cd rdkit-tutorials

# 2. Create the conda env (environment.yml is rock-solid)
conda env create -f environment.yml
# Alternative: use mamba for 5-10× faster installation
# mamba env create -f environment.yml

# 3. Activate it
conda activate rdkit-tutorial

# 4. Launch JupyterLab
jupyter lab
```

### Option 2: Use Our Custom Environment

If you prefer a standalone environment without cloning the tutorials:

```bash
# 1. Create environment from our configuration
conda env create -f rdkit-environment.yml
# Or with mamba (faster):
# mamba env create -f rdkit-environment.yml

# 2. Activate the environment
conda activate rdkit-tutorial

# 3. Launch JupyterLab
jupyter lab
```

## 📦 What's Included

The environment provides:

| Component | Description |
|-----------|-------------|
| **RDKit** | Core cheminformatics library (2024.03.x or later) |
| **JupyterLab** | Interactive notebook environment |
| **nglview** | 3D molecular visualization |
| **py3Dmol** | Alternative 3D visualization |
| **mols2grid** | 2D molecule grid display |
| **NumPy/Pandas** | Data manipulation |
| **Matplotlib** | Plotting and visualization |
| **scikit-learn** | Machine learning tools |
| **OpenBabel** | File format conversion |

## 🔧 Platform-Specific Notes

### macOS (Apple Silicon M1/M2/M3)

Everything works perfectly with recent miniforge-arm64:

```bash
# Install miniforge for ARM64
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-arm64.sh"
bash Miniforge3-MacOSX-arm64.sh

# Then proceed with environment creation
mamba env create -f rdkit-environment.yml
```

### Windows

If nglview visualizations are broken (rare with recent versions):

```bash
# Fix nglview widget extension
jupyter labextension install nglview-js-widgets
```

### Linux

Standard installation works without issues:

```bash
conda env create -f rdkit-environment.yml
conda activate rdkit-tutorial
jupyter lab
```

## ⚡ Pro Tips

1. **Use mamba instead of conda** - It's 5-10× faster for solving dependencies:
   ```bash
   conda install -n base -c conda-forge mamba
   mamba env create -f rdkit-environment.yml
   ```

2. **Use pixi** - Modern alternative to conda (still experimental):
   ```bash
   pixi init
   pixi add rdkit jupyterlab nglview py3dmol ipywidgets numpy pandas matplotlib
   pixi run jupyter lab
   ```

3. **Update existing environment**:
   ```bash
   conda env update -f rdkit-environment.yml --prune
   ```

4. **Remove environment**:
   ```bash
   conda deactivate
   conda env remove -n rdkit-tutorial
   ```

## 🎯 Recommended Notebooks to Start

Once inside the environment, try these notebooks:

1. **Getting Started** - Basic RDKit operations
2. **Molecular Descriptors** - Calculate chemical properties
3. **Fingerprints** - Molecular fingerprint generation
4. **Substructure Search** - Pattern matching in molecules
5. **3D Conformers** - Generate 3D molecular structures

## 🔗 Resources

- [RDKit Documentation](https://www.rdkit.org/docs/)
- [RDKit Tutorials Repository](https://github.com/rdkit/rdkit-tutorials)
- [RDKit Cookbook](https://www.rdkit.org/docs/Cookbook.html)
- [RDKit Blog](https://greglandrum.github.io/rdkit-blog/)

## 🧬 Integration with Sovereignty Architecture

This cheminformatics environment integrates with the broader Sovereignty Architecture for:

- **Molecular property prediction** using LLM agents
- **Drug discovery workflows** with automated pipelines
- **Chemical data management** in vector databases
- **Computational chemistry** integration with quantum simulation tools

For advanced integration examples, see the agent configurations in `.github/agents/`.

---

*Part of the Strategickhaos Sovereignty Architecture - Empowering sovereign digital infrastructure*
