#!/usr/bin/env python3
"""
Tests for Swarm DNA Genome System

Validates the loading, parsing, and access of the YAML DNA genome.
"""

import pytest
import yaml
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from swarm.load_dna import load_swarm_dna, SwarmDNA


class TestSwarmDNALoading:
    """Test DNA file loading and parsing."""
    
    def test_load_dna_file_exists(self):
        """Test that the DNA file can be loaded."""
        dna = load_swarm_dna()
        assert dna is not None
        assert isinstance(dna, SwarmDNA)
    
    def test_dna_version(self):
        """Test that DNA has correct version."""
        dna = load_swarm_dna()
        assert dna.version == 1.0
    
    def test_dna_genome_id(self):
        """Test that genome ID is set."""
        dna = load_swarm_dna()
        assert dna.genome_id == "sovereign-swarm-dna-v1"
    
    def test_dna_description(self):
        """Test that description exists."""
        dna = load_swarm_dna()
        assert dna.description is not None
        assert len(dna.description) > 0
        assert "YAML DNA genome" in dna.description


class TestSwarmDNAMetadata:
    """Test DNA metadata section."""
    
    def test_metadata_author(self):
        """Test that metadata contains author."""
        dna = load_swarm_dna()
        assert "author" in dna.metadata
        assert dna.metadata["author"] == "Domenic Garza"
    
    def test_metadata_created_at(self):
        """Test that metadata contains creation date."""
        dna = load_swarm_dna()
        assert "created_at" in dna.metadata
        assert dna.metadata["created_at"] == "2025-11-23"
    
    def test_metadata_environment(self):
        """Test that environment settings exist."""
        dna = load_swarm_dna()
        assert "environment" in dna.metadata
        env = dna.metadata["environment"]
        assert "primary_vault" in env
        assert "primary_repo" in env
        assert "default_search_engine" in env


class TestSwarmDNADefaults:
    """Test DNA defaults section."""
    
    def test_defaults_exist(self):
        """Test that defaults are defined."""
        dna = load_swarm_dna()
        assert dna.defaults is not None
        assert isinstance(dna.defaults, dict)
    
    def test_default_model(self):
        """Test default model configuration."""
        dna = load_swarm_dna()
        assert "model" in dna.defaults
        assert dna.defaults["model"] == "llama3.1:70b-local"
    
    def test_default_tools(self):
        """Test default tools configuration."""
        dna = load_swarm_dna()
        assert "tools" in dna.defaults
        tools = dna.defaults["tools"]
        assert len(tools) > 0
        
        # Check for terminal tool
        terminal_tool = next((t for t in tools if t["name"] == "terminal"), None)
        assert terminal_tool is not None
        assert terminal_tool["enabled"] is True


class TestSwarmDNAAgents:
    """Test DNA agents section."""
    
    def test_agents_exist(self):
        """Test that agents are defined."""
        dna = load_swarm_dna()
        assert len(dna.agents) > 0
    
    def test_trinity_agents_present(self):
        """Test that all Trinity roles are represented."""
        dna = load_swarm_dna()
        roles = set(agent["trinity_role"] for agent in dna.agents)
        assert "nova" in roles
        assert "lyra" in roles
        assert "athena" in roles
    
    def test_agent_structure(self):
        """Test that agents have required fields."""
        dna = load_swarm_dna()
        required_fields = ["id", "badge", "display_name", "trinity_role", 
                          "os_polarity", "purpose", "model"]
        
        for agent in dna.agents:
            for field in required_fields:
                assert field in agent, f"Agent {agent.get('id')} missing field: {field}"
    
    def test_get_agent_by_id(self):
        """Test retrieving agent by ID."""
        dna = load_swarm_dna()
        
        # Test Nova agent
        nova = dna.get_agent_by_id("nova-core-01")
        assert nova is not None
        assert nova["badge"] == 101
        assert nova["trinity_role"] == "nova"
        assert nova["os_polarity"] == "kali"
        
        # Test Lyra agent
        lyra = dna.get_agent_by_id("lyra-creative-01")
        assert lyra is not None
        assert lyra["badge"] == 305
        assert lyra["trinity_role"] == "lyra"
        
        # Test Athena agent
        athena = dna.get_agent_by_id("athena-mem-01")
        assert athena is not None
        assert athena["badge"] == 777
        assert athena["trinity_role"] == "athena"
    
    def test_get_agents_by_role(self):
        """Test retrieving agents by Trinity role."""
        dna = load_swarm_dna()
        
        nova_agents = dna.get_agents_by_role("nova")
        assert len(nova_agents) >= 1
        assert all(agent["trinity_role"] == "nova" for agent in nova_agents)
        
        lyra_agents = dna.get_agents_by_role("lyra")
        assert len(lyra_agents) >= 1
        assert all(agent["trinity_role"] == "lyra" for agent in lyra_agents)
        
        athena_agents = dna.get_agents_by_role("athena")
        assert len(athena_agents) >= 1
        assert all(agent["trinity_role"] == "athena" for agent in athena_agents)
    
    def test_get_agent_by_badge(self):
        """Test retrieving agent by badge number."""
        dna = load_swarm_dna()
        
        agent_101 = dna.get_agents_by_badge(101)
        assert agent_101 is not None
        assert agent_101["id"] == "nova-core-01"
        
        agent_305 = dna.get_agents_by_badge(305)
        assert agent_305 is not None
        assert agent_305["id"] == "lyra-creative-01"
        
        agent_777 = dna.get_agents_by_badge(777)
        assert agent_777 is not None
        assert agent_777["id"] == "athena-mem-01"
    
    def test_agent_capabilities(self):
        """Test that agents have capabilities defined."""
        dna = load_swarm_dna()
        
        nova = dna.get_agent_by_id("nova-core-01")
        assert "capabilities" in nova
        assert nova["capabilities"]["planning"] is True
        assert nova["capabilities"]["verification"] is True
        assert nova["capabilities"]["code_analysis"] is True
        
        lyra = dna.get_agent_by_id("lyra-creative-01")
        assert "capabilities" in lyra
        assert lyra["capabilities"]["storytelling"] is True
        assert lyra["capabilities"]["doc_generation"] is True
        
        athena = dna.get_agent_by_id("athena-mem-01")
        assert "capabilities" in athena
        assert athena["capabilities"]["long_term_memory"] is True
        assert athena["capabilities"]["failure_analysis"] is True
    
    def test_agent_tools(self):
        """Test that agents have tools configured."""
        dna = load_swarm_dna()
        
        for agent in dna.agents:
            assert "tools" in agent
            assert len(agent["tools"]) > 0
            
            # Each tool should have name and enabled status
            for tool in agent["tools"]:
                assert "name" in tool
                assert "enabled" in tool
    
    def test_agent_memory(self):
        """Test that agents have memory configuration."""
        dna = load_swarm_dna()
        
        for agent in dna.agents:
            assert "memory" in agent
            memory = agent["memory"]
            assert "mode" in memory
            assert "vault_path" in memory


class TestSwarmDNAConnections:
    """Test agent entanglement/connections."""
    
    def test_entangled_agents(self):
        """Test that agents have entanglement connections."""
        dna = load_swarm_dna()
        
        nova_entangled = dna.get_entangled_agents("nova-core-01")
        assert len(nova_entangled) > 0
        assert "athena-mem-01" in nova_entangled
        assert "lyra-creative-01" in nova_entangled
        
        lyra_entangled = dna.get_entangled_agents("lyra-creative-01")
        assert len(lyra_entangled) > 0
        assert "nova-core-01" in lyra_entangled
        assert "athena-mem-01" in lyra_entangled
        
        athena_entangled = dna.get_entangled_agents("athena-mem-01")
        assert len(athena_entangled) > 0
        assert "nova-core-01" in athena_entangled
        assert "lyra-creative-01" in athena_entangled
    
    def test_mutual_entanglement(self):
        """Test that entanglement is mutual between agents."""
        dna = load_swarm_dna()
        
        # If Nova is entangled with Lyra, Lyra should be entangled with Nova
        nova_entangled = dna.get_entangled_agents("nova-core-01")
        
        for entangled_id in nova_entangled:
            reciprocal_entangled = dna.get_entangled_agents(entangled_id)
            assert "nova-core-01" in reciprocal_entangled, \
                f"Agent {entangled_id} should be mutually entangled with nova-core-01"


class TestSwarmDNAOrchestration:
    """Test orchestration configuration."""
    
    def test_orchestration_exists(self):
        """Test that orchestration config exists."""
        dna = load_swarm_dna()
        assert dna.orchestration is not None
        assert isinstance(dna.orchestration, dict)
    
    def test_quantum_loop_config(self):
        """Test quantum loop configuration."""
        dna = load_swarm_dna()
        assert "quantum_loop" in dna.orchestration
        
        quantum_loop = dna.orchestration["quantum_loop"]
        assert quantum_loop["enabled"] is True
        assert quantum_loop["qubits"] == 8
        assert quantum_loop["cycle_seconds_min"] == 30
        assert quantum_loop["cycle_seconds_max"] == 300
    
    def test_error_correction_config(self):
        """Test error correction configuration."""
        dna = load_swarm_dna()
        quantum_loop = dna.orchestration["quantum_loop"]
        
        assert "error_correction" in quantum_loop
        error_correction = quantum_loop["error_correction"]
        assert error_correction["enabled"] is True
        assert error_correction["reviewers_required"] == 3
        assert error_correction["consensus_threshold"] == 0.67
    
    def test_boards_config(self):
        """Test boards configuration."""
        dna = load_swarm_dna()
        assert "boards" in dna.orchestration
        
        boards = dna.orchestration["boards"]
        assert boards["count"] == 10
        assert len(boards["labels"]) == 10
        
        # Check for specific board labels
        expected_labels = [
            "planning", "counter-planning", "threat-mapping",
            "self-modeling", "opponent-modeling", "constraints",
            "pattern-memory", "fractal-projection", "harmonic-sequencing",
            "final-synthesis"
        ]
        
        for label in expected_labels:
            assert label in boards["labels"]


class TestSwarmDNASecurity:
    """Test security configuration."""
    
    def test_security_exists(self):
        """Test that security config exists."""
        dna = load_swarm_dna()
        assert dna.security is not None
        assert isinstance(dna.security, dict)
    
    def test_offline_mode(self):
        """Test offline mode configuration."""
        dna = load_swarm_dna()
        assert "offline_only" in dna.security
        assert dna.security["offline_only"] is True
    
    def test_allowed_networks(self):
        """Test allowed networks configuration."""
        dna = load_swarm_dna()
        assert "allowed_networks" in dna.security
        
        allowed_networks = dna.security["allowed_networks"]
        assert "127.0.0.1" in allowed_networks
        assert "192.168.0.0/16" in allowed_networks
    
    def test_audit_logging(self):
        """Test audit logging configuration."""
        dna = load_swarm_dna()
        assert "audit_logging" in dna.security
        
        audit_logging = dna.security["audit_logging"]
        assert audit_logging["enabled"] is True
        assert "log_path" in audit_logging
        assert audit_logging["redact_personal_data"] is True


class TestSwarmDNAMethods:
    """Test SwarmDNA helper methods."""
    
    def test_to_dict(self):
        """Test converting DNA back to dict."""
        dna = load_swarm_dna()
        dna_dict = dna.to_dict()
        
        assert isinstance(dna_dict, dict)
        assert "version" in dna_dict
        assert "genome_id" in dna_dict
        assert "agents" in dna_dict
    
    def test_repr(self):
        """Test string representation."""
        dna = load_swarm_dna()
        repr_str = repr(dna)
        
        assert "SwarmDNA" in repr_str
        assert "sovereign-swarm-dna-v1" in repr_str
        assert "version=1.0" in repr_str


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])
