"""
Core modules for the Sovereign Mind Kernel
"""

from .dom_kernel import (
    DomKernel,
    Polarity,
    Phase,
    Board,
    initialize_swarm,
    get_swarm_metrics
)

from .obsidian_graph import (
    Vault,
    get_vault,
    init_vault,
    current_vault
)

from .tools import (
    duckduckgo_search,
    run_terminal,
    get_system_metrics,
    vector_distance,
    normalize_vector
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
    'current_vault',
    'duckduckgo_search',
    'run_terminal',
    'get_system_metrics',
    'vector_distance',
    'normalize_vector',
]
