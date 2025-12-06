"""
KHAOS ENGINE - Kubernetes-Harmonized Autonomous Operating System
for Sovereign Enterprises

Strategickhaos DAO LLC / Valoryield Engine
A sovereign resource governance platform replacing vendor lock-in 
with policy-based autonomy.

Architecture Layers:
- Layer 1: Sensory Cortex (Data Collection)
- Layer 2: Autonomic Nervous System (Automated Response)
- Layer 3: Prefrontal Cortex (Strategic Planning)
- Layer 4: Sovereignty Interface (Zero Vendor Lock-in)
- Layer 5: Legion Coordination (Multi-AI Orchestration)
"""

__version__ = "0.1.0"
__author__ = "Strategickhaos DAO LLC"
__license__ = "MIT"

from .core.resource_arbiter import KhaosArbiter, ProcessProfile

__all__ = ["KhaosArbiter", "ProcessProfile", "__version__"]
