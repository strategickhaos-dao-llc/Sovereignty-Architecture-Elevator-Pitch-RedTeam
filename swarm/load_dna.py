#!/usr/bin/env python3
"""
Swarm DNA Loader

Loads and parses the YAML DNA genome for the Sovereign Swarm.
The genome defines agents, capabilities, tools, Trinity roles, and orchestration.
"""

import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any


class SwarmDNA:
    """
    Represents the parsed DNA genome of the swarm.
    
    Provides convenient access to genome components:
    - metadata
    - defaults
    - agents
    - orchestration
    - security
    """
    
    def __init__(self, dna_dict: Dict[str, Any]):
        """Initialize SwarmDNA from parsed YAML dictionary."""
        self._dna = dna_dict
        self.version = dna_dict.get("version")
        self.genome_id = dna_dict.get("genome_id")
        self.description = dna_dict.get("description")
        self.metadata = dna_dict.get("metadata", {})
        self.defaults = dna_dict.get("defaults", {})
        self.agents = dna_dict.get("agents", [])
        self.orchestration = dna_dict.get("orchestration", {})
        self.security = dna_dict.get("security", {})
    
    def get_agent_by_id(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """
        Get agent configuration by ID.
        
        Args:
            agent_id: The agent ID (e.g., "nova-core-01")
            
        Returns:
            Agent configuration dict or None if not found
        """
        for agent in self.agents:
            if agent.get("id") == agent_id:
                return agent
        return None
    
    def get_agents_by_role(self, trinity_role: str) -> List[Dict[str, Any]]:
        """
        Get all agents with a specific Trinity role.
        
        Args:
            trinity_role: Trinity role (nova, lyra, or athena)
            
        Returns:
            List of agent configuration dicts
        """
        return [
            agent for agent in self.agents
            if agent.get("trinity_role") == trinity_role
        ]
    
    def get_agents_by_badge(self, badge: int) -> Optional[Dict[str, Any]]:
        """
        Get agent by badge number.
        
        Args:
            badge: Badge number
            
        Returns:
            Agent configuration dict or None if not found
        """
        for agent in self.agents:
            if agent.get("badge") == badge:
                return agent
        return None
    
    def get_entangled_agents(self, agent_id: str) -> List[str]:
        """
        Get list of agent IDs entangled with the specified agent.
        
        Args:
            agent_id: The agent ID
            
        Returns:
            List of entangled agent IDs
        """
        agent = self.get_agent_by_id(agent_id)
        if agent and "connections" in agent:
            return agent["connections"].get("entangled_with", [])
        return []
    
    def to_dict(self) -> Dict[str, Any]:
        """Return the raw DNA dictionary."""
        return self._dna
    
    def __repr__(self) -> str:
        return f"SwarmDNA(genome_id='{self.genome_id}', version={self.version}, agents={len(self.agents)})"


def load_swarm_dna(path: str = "config/swarm_dna.yaml") -> SwarmDNA:
    """
    Load the swarm DNA genome from a YAML file.
    
    Args:
        path: Path to the swarm_dna.yaml file (relative or absolute)
        
    Returns:
        SwarmDNA object with parsed genome data
        
    Raises:
        FileNotFoundError: If the DNA file doesn't exist
        yaml.YAMLError: If the YAML is malformed
    """
    dna_path = Path(path)
    
    # Try absolute path first, then relative to current directory
    if not dna_path.exists():
        # Try relative to this module's location
        module_dir = Path(__file__).parent.parent
        dna_path = module_dir / path
    
    if not dna_path.exists():
        raise FileNotFoundError(f"Swarm DNA not found at: {path}")
    
    with dna_path.open("r", encoding="utf-8") as f:
        dna_dict = yaml.safe_load(f)
    
    return SwarmDNA(dna_dict)


if __name__ == "__main__":
    # Example usage
    try:
        dna = load_swarm_dna()
        print(f"Loaded genome: {dna.genome_id} (version {dna.version})")
        print(f"Description: {dna.description.strip()}")
        print(f"\nMetadata:")
        print(f"  Author: {dna.metadata.get('author')}")
        print(f"  Created: {dna.metadata.get('created_at')}")
        print(f"\nAgents:")
        for agent in dna.agents:
            print(f"  - {agent['id']} [{agent['trinity_role']}] badge={agent['badge']}")
            print(f"    Display: {agent['display_name']}")
            print(f"    OS: {agent['os_polarity']}")
            print(f"    Model: {agent['model']}")
            
            # Show capabilities
            capabilities = agent.get('capabilities', {})
            enabled_caps = [k for k, v in capabilities.items() if v]
            if enabled_caps:
                print(f"    Capabilities: {', '.join(enabled_caps)}")
            
            # Show entanglements
            entangled = dna.get_entangled_agents(agent['id'])
            if entangled:
                print(f"    Entangled with: {', '.join(entangled)}")
            print()
        
        print(f"Orchestration:")
        quantum_loop = dna.orchestration.get('quantum_loop', {})
        print(f"  Quantum Loop: {'enabled' if quantum_loop.get('enabled') else 'disabled'}")
        print(f"  Qubits: {quantum_loop.get('qubits')}")
        print(f"  Cycle time: {quantum_loop.get('cycle_seconds_min')}-{quantum_loop.get('cycle_seconds_max')}s")
        
        boards = dna.orchestration.get('boards', {})
        print(f"  Boards: {boards.get('count')}")
        print(f"  Board labels: {', '.join(boards.get('labels', []))}")
        
        print(f"\nSecurity:")
        print(f"  Offline only: {dna.security.get('offline_only')}")
        print(f"  Allowed networks: {', '.join(dna.security.get('allowed_networks', []))}")
        print(f"  Audit logging: {'enabled' if dna.security.get('audit_logging', {}).get('enabled') else 'disabled'}")
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("\nMake sure swarm_dna.yaml exists in the config/ directory")
    except Exception as e:
        print(f"Error loading DNA: {e}")
