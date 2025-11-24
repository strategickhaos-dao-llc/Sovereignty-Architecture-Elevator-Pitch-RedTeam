#!/usr/bin/env python3
"""
Sovereign Swarm DNA Loader
Loads, validates, and provides access to the swarm genome configuration
"""

import yaml
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum


class TrinityRole(Enum):
    """Trinity architecture roles"""
    THESIS = "thesis"
    ANTITHESIS = "antithesis"
    SYNTHESIS = "synthesis"


class OSPolarity(Enum):
    """Operating system polarities"""
    LINUX = "linux"
    DARWIN = "darwin"
    WINDOWS = "windows"
    NEUTRAL = "neutral"


@dataclass
class Agent:
    """Agent configuration"""
    name: str
    type: str
    trinity_role: str
    os_polarity: str
    primary_functions: List[str]
    tools: List[str]
    security_clearance: str
    autonomy_level: int
    
    def __post_init__(self):
        """Validate agent configuration"""
        if self.autonomy_level < 1 or self.autonomy_level > 5:
            raise ValueError(f"Autonomy level must be 1-5, got {self.autonomy_level}")
        
        valid_clearances = ["low", "medium", "high", "critical"]
        if self.security_clearance not in valid_clearances:
            raise ValueError(f"Invalid security clearance: {self.security_clearance}")


@dataclass
class SwarmDNA:
    """Complete swarm DNA configuration"""
    metadata: Dict[str, Any]
    trinity: Dict[str, Any]
    agents: List[Agent]
    orchestration: Dict[str, Any]
    security: Dict[str, Any]
    resources: Dict[str, Any]
    observability: Dict[str, Any]
    integrations: Dict[str, Any]
    governance: Dict[str, Any]
    swarm_behavior: Dict[str, Any]
    
    def get_agents_by_role(self, role: str) -> List[Agent]:
        """Get all agents with a specific trinity role"""
        return [agent for agent in self.agents if agent.trinity_role == role]
    
    def get_agent_by_name(self, name: str) -> Optional[Agent]:
        """Get a specific agent by name"""
        for agent in self.agents:
            if agent.name == name:
                return agent
        return None
    
    def get_agents_by_clearance(self, min_clearance: str) -> List[Agent]:
        """Get agents with at least the specified security clearance"""
        clearance_hierarchy = {"low": 0, "medium": 1, "high": 2, "critical": 3}
        min_level = clearance_hierarchy.get(min_clearance, 0)
        
        return [
            agent for agent in self.agents
            if clearance_hierarchy.get(agent.security_clearance, 0) >= min_level
        ]


class DNALoader:
    """Loads and validates swarm DNA configuration"""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize DNA loader with optional custom config path"""
        if config_path is None:
            # Default to config/swarm_dna.yaml relative to project root
            project_root = Path(__file__).parent.parent
            config_path = project_root / "config" / "swarm_dna.yaml"
        
        self.config_path = Path(config_path)
        self.dna: Optional[SwarmDNA] = None
    
    def load(self) -> SwarmDNA:
        """Load and parse the DNA configuration"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"DNA configuration not found: {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            raw_config = yaml.safe_load(f)
        
        # Validate required sections
        required_sections = [
            'metadata', 'trinity', 'agents', 'orchestration',
            'security', 'resources', 'observability', 'integrations',
            'governance', 'swarm_behavior'
        ]
        
        for section in required_sections:
            if section not in raw_config:
                raise ValueError(f"Missing required section in DNA: {section}")
        
        # Parse agents
        agents = []
        for agent_data in raw_config['agents']:
            agent = Agent(
                name=agent_data['name'],
                type=agent_data['type'],
                trinity_role=agent_data['trinity_role'],
                os_polarity=agent_data['os_polarity'],
                primary_functions=agent_data['primary_functions'],
                tools=agent_data['tools'],
                security_clearance=agent_data['security_clearance'],
                autonomy_level=agent_data['autonomy_level']
            )
            agents.append(agent)
        
        # Create SwarmDNA object
        self.dna = SwarmDNA(
            metadata=raw_config['metadata'],
            trinity=raw_config['trinity'],
            agents=agents,
            orchestration=raw_config['orchestration'],
            security=raw_config['security'],
            resources=raw_config['resources'],
            observability=raw_config['observability'],
            integrations=raw_config['integrations'],
            governance=raw_config['governance'],
            swarm_behavior=raw_config['swarm_behavior']
        )
        
        return self.dna
    
    def validate(self) -> bool:
        """Validate the loaded DNA configuration"""
        if self.dna is None:
            raise RuntimeError("DNA not loaded. Call load() first.")
        
        # Validate trinity structure
        trinity_roles = ['thesis', 'antithesis', 'synthesis']
        for role in trinity_roles:
            if role not in self.dna.trinity:
                raise ValueError(f"Missing trinity role: {role}")
        
        # Validate agents have all trinity roles represented
        agent_roles = set(agent.trinity_role for agent in self.dna.agents)
        for role in trinity_roles:
            if role not in agent_roles:
                print(f"Warning: No agents with trinity role '{role}'")
        
        # Validate orchestration workflow
        workflow = self.dna.orchestration.get('workflow', [])
        if not workflow:
            raise ValueError("Orchestration workflow is empty")
        
        # Validate security configuration
        if not self.dna.security.get('encryption', {}).get('at_rest'):
            print("Warning: Encryption at rest is disabled")
        
        if not self.dna.security.get('audit', {}).get('enabled'):
            print("Warning: Security auditing is disabled")
        
        return True
    
    def get_dna(self) -> SwarmDNA:
        """Get the loaded DNA configuration"""
        if self.dna is None:
            raise RuntimeError("DNA not loaded. Call load() first.")
        return self.dna
    
    def reload(self) -> SwarmDNA:
        """Reload the DNA configuration from disk"""
        return self.load()
    
    def get_config_value(self, path: str, default: Any = None) -> Any:
        """
        Get a configuration value using dot notation path.
        Example: get_config_value('security.encryption.algorithm')
        """
        if self.dna is None:
            raise RuntimeError("DNA not loaded. Call load() first.")
        
        # Convert SwarmDNA to dict for path traversal
        config_dict = {
            'metadata': self.dna.metadata,
            'trinity': self.dna.trinity,
            'agents': [vars(agent) for agent in self.dna.agents],
            'orchestration': self.dna.orchestration,
            'security': self.dna.security,
            'resources': self.dna.resources,
            'observability': self.dna.observability,
            'integrations': self.dna.integrations,
            'governance': self.dna.governance,
            'swarm_behavior': self.dna.swarm_behavior
        }
        
        parts = path.split('.')
        current = config_dict
        
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return default
        
        return current
    
    def get_integration_config(self, integration_name: str) -> Optional[Dict[str, Any]]:
        """Get configuration for a specific integration"""
        if self.dna is None:
            raise RuntimeError("DNA not loaded. Call load() first.")
        
        return self.dna.integrations.get(integration_name)
    
    def is_integration_enabled(self, integration_name: str) -> bool:
        """Check if an integration is enabled"""
        config = self.get_integration_config(integration_name)
        if config is None:
            return False
        return config.get('enabled', False)


def load_swarm_dna(config_path: Optional[str] = None) -> SwarmDNA:
    """
    Convenience function to load and validate swarm DNA.
    
    Args:
        config_path: Optional path to DNA configuration file
        
    Returns:
        SwarmDNA object with loaded configuration
        
    Raises:
        FileNotFoundError: If configuration file not found
        ValueError: If configuration is invalid
    """
    loader = DNALoader(config_path)
    dna = loader.load()
    loader.validate()
    return dna


if __name__ == "__main__":
    """Test DNA loading"""
    try:
        print("🧬 Loading Swarm DNA...")
        dna = load_swarm_dna()
        
        print(f"✅ DNA loaded successfully")
        print(f"   Version: {dna.metadata['version']}")
        print(f"   Agents: {len(dna.agents)}")
        
        print("\n📊 Trinity Distribution:")
        for role in ['thesis', 'antithesis', 'synthesis']:
            agents = dna.get_agents_by_role(role)
            print(f"   {role}: {len(agents)} agents - {[a.name for a in agents]}")
        
        print("\n🔒 Security Clearance Distribution:")
        for clearance in ['low', 'medium', 'high', 'critical']:
            agents = dna.get_agents_by_clearance(clearance)
            print(f"   {clearance}+: {len(agents)} agents")
        
        print("\n🔗 Enabled Integrations:")
        for integration in ['github', 'discord', 'vector_db', 'ci_cd']:
            if dna.integrations.get(integration, {}).get('enabled'):
                print(f"   ✅ {integration}")
            else:
                print(f"   ❌ {integration}")
        
        print("\n✨ Swarm DNA validation complete")
        
    except Exception as e:
        print(f"❌ Error loading DNA: {e}")
        import traceback
        traceback.print_exc()
