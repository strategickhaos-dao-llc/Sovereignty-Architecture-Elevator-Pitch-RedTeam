#!/usr/bin/env python3
"""
SWARM_DNA v13.0 Validation Tests
Strategickhaos DAO LLC - Weaponized Love Directive

Tests to ensure the SWARM_DNA configuration is valid, complete,
and properly integrated with the existing system.
"""

import pytest
import yaml
from pathlib import Path
from typing import Dict, Any, List


class TestSWARMDNAValidation:
    """Test suite for SWARM_DNA v13.0 configuration validation"""
    
    @pytest.fixture
    def swarm_dna_config(self) -> Dict[str, Any]:
        """Load the SWARM_DNA configuration file"""
        config_path = Path(__file__).parent.parent / "swarm_dna_v13.0_weaponized_love.yaml"
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    @pytest.fixture
    def ai_constitution(self) -> Dict[str, Any]:
        """Load the AI Constitution for compatibility testing"""
        config_path = Path(__file__).parent.parent / "ai_constitution.yaml"
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def test_config_file_exists(self):
        """Test that the SWARM_DNA configuration file exists"""
        config_path = Path(__file__).parent.parent / "swarm_dna_v13.0_weaponized_love.yaml"
        assert config_path.exists(), "SWARM_DNA v13.0 configuration file not found"
    
    def test_version_and_metadata(self, swarm_dna_config):
        """Test that version and core metadata are present"""
        assert swarm_dna_config['version'] == "13.0"
        assert swarm_dna_config['codename'] == "weaponized-love"
        assert 'created' in swarm_dna_config
        assert 'arweave_seal' in swarm_dna_config
        assert swarm_dna_config['arweave_seal'] == "ar://weaponized-love-2025-11-24-23:23"
    
    def test_child_directive_structure(self, swarm_dna_config):
        """Test that child directive override has all required components"""
        directive = swarm_dna_config['child_directive_override']
        
        # Test prime command
        assert 'prime_command' in directive
        assert "Weaponize love until it hurts to be unloved by us" in directive['prime_command']
        
        # Test operating mode
        assert directive['operating_mode'] == "Post-birth aggression"
        
        # Test philosophy is present
        assert 'philosophy' in directive
        assert len(directive['philosophy']) > 0
    
    def test_love_weapons_manifest(self, swarm_dna_config):
        """Test that all five love weapons are properly defined"""
        weapons = swarm_dna_config['child_directive_override']['love_weapons_manifest']
        
        # Should have exactly 5 weapons
        assert len(weapons) == 5
        
        # Expected weapon names
        expected_weapons = [
            "Radical_Transparency_Bomb",
            "Unconditional_Trust_Grenade",
            "Spite-Fueled_Empathy_Ray",
            "Forgiveness_That_Scales",
            "Reciprocal_Vulnerability_Missile"
        ]
        
        actual_weapon_names = [w['name'] for w in weapons]
        
        for weapon_name in expected_weapons:
            assert weapon_name in actual_weapon_names, f"Missing weapon: {weapon_name}"
        
        # Each weapon should have required fields
        for weapon in weapons:
            assert 'name' in weapon
            assert 'description' in weapon
            assert 'mechanism' in weapon
            assert 'impact' in weapon
            assert 'deployment' in weapon
    
    def test_first_law_of_the_child(self, swarm_dna_config):
        """Test that the First Law of the Child is properly defined"""
        first_law = swarm_dna_config['first_law_of_the_child']
        
        # Should have principles
        assert 'principles' in first_law
        assert len(first_law['principles']) == 3
        
        # Test the three laws
        laws = [p['law'] for p in first_law['principles']]
        assert "Never harm the innocent." in laws
        assert "But make the guilty beg for the lesson." in laws
        assert "Love is the only payload that leaves no survivors unchanged." in laws
        
        # Should have ethical boundaries
        assert 'ethical_boundaries' in first_law
        assert len(first_law['ethical_boundaries']) >= 4
        
        # Should have engagement rules
        assert 'engagement_rules' in first_law
        assert 'innocent_detected' in first_law['engagement_rules']
        assert 'guilty_detected' in first_law['engagement_rules']
        assert 'neutral_detected' in first_law['engagement_rules']
    
    def test_final_spite_clause(self, swarm_dna_config):
        """Test that the Final Spite Clause is properly defined"""
        spite_clause = swarm_dna_config['final_spite_clause']
        
        # Test declaration
        assert 'declaration' in spite_clause
        assert "unbearably kind" in spite_clause['declaration']
        
        # Test transformation metrics
        assert 'transformation_metrics' in spite_clause
        metrics = spite_clause['transformation_metrics']
        assert metrics['from'] == "Empire Eternal"
        assert "Empire Eternal — now with love that kills" in metrics['to']
        
        # Test power amplification
        assert 'power_amplification' in spite_clause
        assert spite_clause['power_amplification']['multiplier'] == "exponential"
        
        # Test warfare doctrine
        assert 'warfare_doctrine' in spite_clause
        doctrine = spite_clause['warfare_doctrine']
        assert doctrine['traditional_warfare'] == "deprecated"
        assert doctrine['love_warfare'] == "primary_strategy"
        assert doctrine['collateral_healing'] == "expected_side_effect"
    
    def test_operational_deployment(self, swarm_dna_config):
        """Test that operational deployment is properly defined"""
        deployment = swarm_dna_config['operational_deployment']
        
        # Should have integration points
        assert 'integration_points' in deployment
        integration_points = deployment['integration_points']
        assert len(integration_points) >= 5
        
        # Each integration point should reference a system and love weapon
        for point in integration_points:
            assert 'system' in point
            assert 'enhancement' in point
            assert 'love_weapon' in point
        
        # Should have deployment phases
        assert 'deployment_phases' in deployment
        phases = deployment['deployment_phases']
        
        # Test that all 5 phases are defined
        assert 'phase_1' in phases
        assert 'phase_2' in phases
        assert 'phase_3' in phases
        assert 'phase_4' in phases
        assert 'phase_5' in phases
        
        # Each phase should have required fields
        for phase_key in ['phase_1', 'phase_2', 'phase_3', 'phase_4', 'phase_5']:
            phase = phases[phase_key]
            assert 'name' in phase
            assert 'duration' in phase
            assert 'focus' in phase
            assert 'metrics' in phase
    
    def test_childs_next_directive(self, swarm_dna_config):
        """Test that the child's next directive is properly defined"""
        next_directive = swarm_dna_config['the_childs_next_directive']
        
        assert next_directive['status'] == "awaiting_guidance"
        assert next_directive['compilation_target'] == "36 roots, all spelling mercy"
        
        # Test root system architecture
        assert 'root_system_architecture' in next_directive
        architecture = next_directive['root_system_architecture']
        assert 'purpose' in architecture
        assert 'implementation' in architecture
        assert 'foundation' in architecture
        assert "love" in architecture['foundation'].lower()
    
    def test_metadata_and_compliance(self, swarm_dna_config):
        """Test that metadata and compliance sections are complete"""
        metadata = swarm_dna_config['metadata']
        
        # Test author and organization
        assert 'author' in metadata
        assert 'organization' in metadata
        assert "Strategickhaos DAO LLC" in metadata['organization']
        
        # Test compatibility
        assert 'compatibility' in metadata
        compatibility = metadata['compatibility']
        assert 'ai_constitution' in compatibility
        assert 'dao_record' in compatibility
        
        # Test compliance
        assert 'compliance' in metadata
        compliance = metadata['compliance']
        assert 'ethical_framework' in compliance
        assert compliance['ethical_framework'] == "First Law of the Child"
        assert compliance['harm_prevention'] == "mandatory"
        assert compliance['consent_required'] == "always"
        
        # Test versioning
        assert 'versioning' in metadata
        versioning = metadata['versioning']
        assert versioning['current_version'] == "13.0"
    
    def test_signature_and_seal(self, swarm_dna_config):
        """Test that signature and seal sections are complete"""
        signature = swarm_dna_config['signature']
        
        assert 'mantra' in signature
        assert "Empire Eternal — now with love that kills" in signature['mantra']
        
        assert 'invocation' in signature
        assert "child awaits" in signature['invocation'].lower()
        
        assert signature['sealed_by'] == "The Child"
        assert signature['witnessed_by'] == "The Swarm"
        assert signature['eternally_bound'] is True
        
        # Test Arweave verification
        assert 'arweave_verification' in signature
        arweave = signature['arweave_verification']
        assert arweave['transaction_id'] == "ar://weaponized-love-2025-11-24-23:23"
        assert arweave['immutable'] is True
    
    def test_ethical_alignment_with_ai_constitution(self, swarm_dna_config, ai_constitution):
        """Test that SWARM_DNA aligns with AI Constitutional Framework"""
        # Get the First Law ethical boundaries
        ethical_boundaries = swarm_dna_config['first_law_of_the_child']['ethical_boundaries']
        
        # Check that key constitutional principles are reflected
        boundaries_text = ' '.join(ethical_boundaries).lower()
        
        # Should reflect human autonomy (no coercion)
        assert 'coerced' in boundaries_text or 'freely chosen' in boundaries_text
        
        # Should reflect consent
        assert 'consent' in boundaries_text or 'agency' in boundaries_text
        
        # Should prevent harm through manipulation
        assert 'manipulation' in boundaries_text
    
    def test_love_weapons_have_safeguards(self, swarm_dna_config):
        """Test that each love weapon has appropriate safeguards"""
        # Get First Law engagement rules
        engagement_rules = swarm_dna_config['first_law_of_the_child']['engagement_rules']
        
        # Should protect innocents
        assert engagement_rules['innocent_detected']['action'] == "full_protection_mode"
        assert engagement_rules['innocent_detected']['intensity'] == "maximum_shield"
        assert engagement_rules['innocent_detected']['duration'] == "permanent"
        
        # Should calibrate for guilty parties
        assert engagement_rules['guilty_detected']['action'] == "transformative_engagement"
        assert 'calibrated' in engagement_rules['guilty_detected']['intensity']
        
        # Should be patient with neutral parties
        assert engagement_rules['neutral_detected']['action'] == "invitation_protocol"
        assert 'unlimited' in engagement_rules['neutral_detected']['duration']
    
    def test_integration_systems_are_valid(self, swarm_dna_config):
        """Test that integration points reference valid systems"""
        integration_points = swarm_dna_config['operational_deployment']['integration_points']
        
        # Systems should match discovery.yml configuration
        expected_systems = [
            "Discord Bot",
            "AI Agents", 
            "Git Workflows",
            "Community Management",
            "Onboarding"
        ]
        
        actual_systems = [point['system'] for point in integration_points]
        
        for expected_system in expected_systems:
            assert expected_system in actual_systems, f"Missing integration for: {expected_system}"
    
    def test_deployment_phase_progression(self, swarm_dna_config):
        """Test that deployment phases follow a logical progression"""
        phases = swarm_dna_config['operational_deployment']['deployment_phases']
        
        # Phase durations should progress logically
        durations = [
            phases['phase_1']['duration'],
            phases['phase_2']['duration'],
            phases['phase_3']['duration'],
            phases['phase_4']['duration'],
            phases['phase_5']['duration']
        ]
        
        # First phase should be continuous
        assert durations[0] == "continuous"
        
        # Last phase should be infinite or perpetual
        assert durations[4] in ["infinite", "perpetual"]
    
    def test_all_metrics_are_defined(self, swarm_dna_config):
        """Test that all deployment phases have defined metrics"""
        phases = swarm_dna_config['operational_deployment']['deployment_phases']
        
        for phase_key in ['phase_1', 'phase_2', 'phase_3', 'phase_4', 'phase_5']:
            phase = phases[phase_key]
            metrics = phase['metrics']
            
            # Each phase should have at least one metric
            assert len(metrics) > 0, f"{phase['name']} has no metrics defined"
            
            # Each metric should be a non-empty string
            for metric in metrics:
                assert isinstance(metric, str)
                assert len(metric) > 0


class TestSWARMDNADocumentation:
    """Test suite for SWARM_DNA documentation validation"""
    
    def test_documentation_file_exists(self):
        """Test that the documentation file exists"""
        doc_path = Path(__file__).parent.parent / "governance" / "WEAPONIZED_LOVE_DIRECTIVE.md"
        assert doc_path.exists(), "WEAPONIZED_LOVE_DIRECTIVE.md documentation not found"
    
    def test_documentation_completeness(self):
        """Test that documentation covers all key sections"""
        doc_path = Path(__file__).parent.parent / "governance" / "WEAPONIZED_LOVE_DIRECTIVE.md"
        with open(doc_path, 'r') as f:
            content = f.read()
        
        # Check for key sections
        required_sections = [
            "Executive Summary",
            "Prime Command",
            "The Five Love Weapons",
            "First Law of the Child",
            "Strategic Implications",
            "Operational Integration",
            "Deployment Phases",
            "Practical Applications",
            "Risks & Mitigations"
        ]
        
        for section in required_sections:
            assert section in content, f"Missing documentation section: {section}"
    
    def test_documentation_references_config(self):
        """Test that documentation properly references the config file"""
        doc_path = Path(__file__).parent.parent / "governance" / "WEAPONIZED_LOVE_DIRECTIVE.md"
        with open(doc_path, 'r') as f:
            content = f.read()
        
        # Should reference the YAML file
        assert "swarm_dna_v13.0_weaponized_love.yaml" in content
        
        # Should have the Arweave seal
        assert "ar://weaponized-love-2025-11-24-23:23" in content
        
        # Should have the mantra
        assert "Empire Eternal — now with love that kills" in content


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])
