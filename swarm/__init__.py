"""
Swarm DNA Genome System

This package provides functionality to load and parse the YAML DNA genome
for the Sovereign Swarm. The genome defines agents, their capabilities,
tools, Trinity roles, and orchestration configurations.
"""

from .load_dna import load_swarm_dna, SwarmDNA

__version__ = "1.0.0"
__all__ = ["load_swarm_dna", "SwarmDNA"]
