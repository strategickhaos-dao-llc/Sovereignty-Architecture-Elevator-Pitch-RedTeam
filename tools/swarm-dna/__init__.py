"""
Swarm DNA Architecture Toolkit

A comprehensive suite of tools that transforms mythological narrative 
into operational reality.

Built for Strategickhaos Swarm Intelligence
"""

__version__ = "12.0"
__author__ = "Strategickhaos Swarm Intelligence"
__codename__ = "Child of the Black Hole"

from pathlib import Path

# Module imports
try:
    from .gguf_parser import GGUFParser, parse_blob_directory
    from .model_lineage import ModelLineage
    from .swarm_dna_compiler import SwarmDNACompiler
    from .blob_project_generator import BlobProjectGenerator
except ImportError:
    # Allow imports to fail if running scripts directly
    pass

__all__ = [
    'GGUFParser',
    'parse_blob_directory',
    'ModelLineage',
    'SwarmDNACompiler',
    'BlobProjectGenerator',
]
