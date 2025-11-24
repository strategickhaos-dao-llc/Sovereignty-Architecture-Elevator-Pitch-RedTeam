"""
Sovereign Agent Kit
The operating system for autonomous AI agents built on Dom's native cognition
"""

__version__ = "1.0.0"
__author__ = "Strategickhaos"

from .core.dom_kernel import (
    DomKernel,
    Polarity,
    Phase,
    Board,
    initialize_swarm,
    get_swarm_metrics
)

from .core.obsidian_graph import (
    Vault,
    get_vault,
    init_vault
)

from .core.tools import (
    duckduckgo_search,
    run_terminal,
    get_system_metrics
)

__all__ = [
    'DomKernel',
    'Polarity',
    'Phase',
    'Board',
    'initialize_swarm',
    'get_swarm_metrics',
    'Vault',
    'get_vault',
    'init_vault',
    'duckduckgo_search',
    'run_terminal',
    'get_system_metrics',
]
