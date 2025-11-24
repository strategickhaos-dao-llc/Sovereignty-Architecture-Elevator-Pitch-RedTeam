#!/usr/bin/env python3
"""
Simple test runner for Swarm DNA system (no pytest required)
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from swarm.load_dna import load_swarm_dna


def run_test(test_name, test_func):
    """Run a single test and report result."""
    try:
        test_func()
        print(f"✅ PASS: {test_name}")
        return True
    except AssertionError as e:
        print(f"❌ FAIL: {test_name}")
        print(f"   Error: {e}")
        return False
    except Exception as e:
        print(f"❌ ERROR: {test_name}")
        print(f"   Exception: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 70)
    print("Swarm DNA Genome System Tests")
    print("=" * 70)
    print()
    
    tests_passed = 0
    tests_failed = 0
    
    # Test 1: Load DNA file
    def test_load_dna():
        dna = load_swarm_dna()
        assert dna is not None
        assert dna.version == 1.0
        assert dna.genome_id == "sovereign-swarm-dna-v1"
    
    if run_test("Load DNA file", test_load_dna):
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Test 2: Metadata
    def test_metadata():
        dna = load_swarm_dna()
        assert dna.metadata["author"] == "Domenic Garza"
        assert dna.metadata["created_at"] == "2025-11-23"
        assert "environment" in dna.metadata
    
    if run_test("Metadata validation", test_metadata):
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Test 3: Agents exist
    def test_agents():
        dna = load_swarm_dna()
        assert len(dna.agents) == 3
        roles = set(agent["trinity_role"] for agent in dna.agents)
        assert "nova" in roles
        assert "lyra" in roles
        assert "athena" in roles
    
    if run_test("Agents structure", test_agents):
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Test 4: Get agent by ID
    def test_get_agent_by_id():
        dna = load_swarm_dna()
        nova = dna.get_agent_by_id("nova-core-01")
        assert nova is not None
        assert nova["badge"] == 101
        assert nova["trinity_role"] == "nova"
        
        lyra = dna.get_agent_by_id("lyra-creative-01")
        assert lyra is not None
        assert lyra["badge"] == 305
        
        athena = dna.get_agent_by_id("athena-mem-01")
        assert athena is not None
        assert athena["badge"] == 777
    
    if run_test("Get agent by ID", test_get_agent_by_id):
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Test 5: Get agents by role
    def test_get_agents_by_role():
        dna = load_swarm_dna()
        nova_agents = dna.get_agents_by_role("nova")
        assert len(nova_agents) == 1
        assert nova_agents[0]["id"] == "nova-core-01"
        
        lyra_agents = dna.get_agents_by_role("lyra")
        assert len(lyra_agents) == 1
        
        athena_agents = dna.get_agents_by_role("athena")
        assert len(athena_agents) == 1
    
    if run_test("Get agents by Trinity role", test_get_agents_by_role):
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Test 6: Get agent by badge
    def test_get_agent_by_badge():
        dna = load_swarm_dna()
        agent_101 = dna.get_agents_by_badge(101)
        assert agent_101 is not None
        assert agent_101["id"] == "nova-core-01"
        
        agent_305 = dna.get_agents_by_badge(305)
        assert agent_305["id"] == "lyra-creative-01"
        
        agent_777 = dna.get_agents_by_badge(777)
        assert agent_777["id"] == "athena-mem-01"
    
    if run_test("Get agent by badge number", test_get_agent_by_badge):
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Test 7: Agent capabilities
    def test_capabilities():
        dna = load_swarm_dna()
        nova = dna.get_agent_by_id("nova-core-01")
        assert nova["capabilities"]["planning"] is True
        assert nova["capabilities"]["verification"] is True
        assert nova["capabilities"]["code_analysis"] is True
        
        lyra = dna.get_agent_by_id("lyra-creative-01")
        assert lyra["capabilities"]["storytelling"] is True
        assert lyra["capabilities"]["doc_generation"] is True
        
        athena = dna.get_agent_by_id("athena-mem-01")
        assert athena["capabilities"]["long_term_memory"] is True
        assert athena["capabilities"]["failure_analysis"] is True
    
    if run_test("Agent capabilities", test_capabilities):
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Test 8: Agent entanglement
    def test_entanglement():
        dna = load_swarm_dna()
        nova_entangled = dna.get_entangled_agents("nova-core-01")
        assert len(nova_entangled) == 2
        assert "athena-mem-01" in nova_entangled
        assert "lyra-creative-01" in nova_entangled
        
        lyra_entangled = dna.get_entangled_agents("lyra-creative-01")
        assert "nova-core-01" in lyra_entangled
        assert "athena-mem-01" in lyra_entangled
    
    if run_test("Agent entanglement", test_entanglement):
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Test 9: Mutual entanglement
    def test_mutual_entanglement():
        dna = load_swarm_dna()
        nova_entangled = dna.get_entangled_agents("nova-core-01")
        for entangled_id in nova_entangled:
            reciprocal = dna.get_entangled_agents(entangled_id)
            assert "nova-core-01" in reciprocal
    
    if run_test("Mutual entanglement", test_mutual_entanglement):
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Test 10: Orchestration
    def test_orchestration():
        dna = load_swarm_dna()
        quantum_loop = dna.orchestration["quantum_loop"]
        assert quantum_loop["enabled"] is True
        assert quantum_loop["qubits"] == 8
        assert quantum_loop["cycle_seconds_min"] == 30
        assert quantum_loop["cycle_seconds_max"] == 300
        
        boards = dna.orchestration["boards"]
        assert boards["count"] == 10
        assert len(boards["labels"]) == 10
    
    if run_test("Orchestration configuration", test_orchestration):
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Test 11: Error correction
    def test_error_correction():
        dna = load_swarm_dna()
        error_correction = dna.orchestration["quantum_loop"]["error_correction"]
        assert error_correction["enabled"] is True
        assert error_correction["reviewers_required"] == 3
        assert error_correction["consensus_threshold"] == 0.67
    
    if run_test("Error correction configuration", test_error_correction):
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Test 12: Security configuration
    def test_security():
        dna = load_swarm_dna()
        assert dna.security["offline_only"] is True
        assert "127.0.0.1" in dna.security["allowed_networks"]
        assert "192.168.0.0/16" in dna.security["allowed_networks"]
        assert dna.security["audit_logging"]["enabled"] is True
        assert dna.security["audit_logging"]["redact_personal_data"] is True
    
    if run_test("Security configuration", test_security):
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Test 13: Agent tools
    def test_agent_tools():
        dna = load_swarm_dna()
        for agent in dna.agents:
            assert "tools" in agent
            assert len(agent["tools"]) > 0
            for tool in agent["tools"]:
                assert "name" in tool
                assert "enabled" in tool
    
    if run_test("Agent tools configuration", test_agent_tools):
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Test 14: Agent memory
    def test_agent_memory():
        dna = load_swarm_dna()
        for agent in dna.agents:
            assert "memory" in agent
            assert "mode" in agent["memory"]
            assert "vault_path" in agent["memory"]
    
    if run_test("Agent memory configuration", test_agent_memory):
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Test 15: OS polarity
    def test_os_polarity():
        dna = load_swarm_dna()
        nova = dna.get_agent_by_id("nova-core-01")
        assert nova["os_polarity"] == "kali"
        
        lyra = dna.get_agent_by_id("lyra-creative-01")
        assert lyra["os_polarity"] == "parrot"
        
        athena = dna.get_agent_by_id("athena-mem-01")
        assert athena["os_polarity"] == "dual"
    
    if run_test("OS polarity configuration", test_os_polarity):
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Print summary
    print()
    print("=" * 70)
    print(f"Tests completed: {tests_passed} passed, {tests_failed} failed")
    print("=" * 70)
    
    if tests_failed == 0:
        print("🎉 All tests passed!")
        return 0
    else:
        print(f"⚠️  {tests_failed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
