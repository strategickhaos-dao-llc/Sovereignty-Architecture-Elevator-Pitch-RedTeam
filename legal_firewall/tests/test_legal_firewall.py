#!/usr/bin/env python3
"""
Tests for Legal-Firewall Generator Module
Strategickhaos DAO LLC - LB-GSE Methodology
"""

import os
import sys
import tempfile
import json
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from legal_firewall_generator import (
    LegalFirewallGenerator,
    RequiredComponent,
    LegalRequirement,
    AnalysisResult,
    generate_required_components,
)
from component_templates import (
    ComponentTemplateEngine,
    ComponentSpec,
    COMPONENT_TEMPLATES,
)
from auto_pr_creator import AutoPRCreator


class TestLegalFirewallGenerator:
    """Tests for the LegalFirewallGenerator class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.generator = LegalFirewallGenerator()
        self.sample_contract = {
            "version": "1.0",
            "legal_primitives": {
                "fiduciary_duties": {
                    "duty_of_care": {
                        "description": "Exercise reasonable care",
                        "requirements": [
                            {
                                "id": "risk_assessment",
                                "description": "Evaluate risks before executing proposals",
                                "constraint_type": "mandatory",
                                "enforcement": "risk_scoring_agent"
                            }
                        ]
                    }
                },
                "charitable_constraints": {
                    "irrevocable_percentage": {
                        "description": "Maintain charitable percentage",
                        "percentage": 10,
                        "requirements": [
                            {
                                "id": "percentage_validator",
                                "description": "Validate charitable percentage",
                                "constraint_type": "mandatory",
                                "enforcement": "manifest_compliance_checker"
                            }
                        ]
                    }
                }
            },
            "component_registry": {
                "implemented": ["audit_log_basic"],
                "planned": ["risk_scoring_agent"]
            },
            "capability_mappings": {
                "risk_scoring_agent": {
                    "component": "risk_assessment_agent",
                    "priority": "high",
                    "estimated_effort": "high"
                },
                "manifest_compliance_checker": {
                    "component": "percentage_validator",
                    "priority": "high",
                    "estimated_effort": "low"
                }
            }
        }
    
    def test_load_contract_from_string(self):
        """Test loading a contract from YAML string."""
        import yaml
        yaml_content = yaml.dump(self.sample_contract)
        
        result = self.generator.load_contract_from_string(yaml_content)
        
        assert result is not None
        assert "legal_primitives" in result
        assert "fiduciary_duties" in result["legal_primitives"]
    
    def test_component_exists(self):
        """Test checking if a component exists."""
        self.generator.component_registry = {"test_component": {"status": "implemented"}}
        
        assert self.generator.component_exists("test_component") is True
        assert self.generator.component_exists("nonexistent") is False
    
    def test_register_component(self):
        """Test registering a new component."""
        self.generator.register_component("new_component", {"version": "1.0"})
        
        assert "new_component" in self.generator.component_registry
        assert self.generator.component_registry["new_component"]["version"] == "1.0"
    
    def test_generate_required_components(self):
        """Test generating required components from contract."""
        import yaml
        yaml_content = yaml.dump(self.sample_contract)
        self.generator.load_contract_from_string(yaml_content)
        
        required = self.generator.generate_required_components()
        
        assert len(required) > 0
        assert all(isinstance(comp, RequiredComponent) for comp in required)
        
        # Check that implemented components are not in required list
        component_names = [comp.name for comp in required]
        assert "audit_log_basic" not in component_names
    
    def test_analyze_contract(self):
        """Test comprehensive contract analysis."""
        import yaml
        yaml_content = yaml.dump(self.sample_contract)
        self.generator.load_contract_from_string(yaml_content)
        
        analysis = self.generator.analyze_contract()
        
        assert isinstance(analysis, AnalysisResult)
        assert analysis.total_requirements >= 0
        assert 0 <= analysis.compliance_score <= 1
    
    def test_prioritize_components(self):
        """Test component prioritization."""
        components = [
            RequiredComponent("c1", "comp1", "desc", "legal", "mandatory", "enf", "low", "low"),
            RequiredComponent("c2", "comp2", "desc", "legal", "mandatory", "enf", "critical", "high"),
            RequiredComponent("c3", "comp3", "desc", "legal", "recommended", "enf", "high", "medium"),
        ]
        
        prioritized = self.generator.prioritize_components(components)
        
        # Critical should be first
        assert prioritized[0].priority == "critical"
        # High mandatory should be before low
        assert prioritized[1].priority == "high"
    
    def test_generate_development_roadmap(self):
        """Test roadmap generation."""
        import yaml
        yaml_content = yaml.dump(self.sample_contract)
        self.generator.load_contract_from_string(yaml_content)
        
        roadmap = self.generator.generate_development_roadmap()
        
        assert "phase_1_critical" in roadmap
        assert "phase_2_high" in roadmap
        assert "phase_3_medium" in roadmap
        assert "phase_4_low" in roadmap
    
    def test_validate_action_allowed(self):
        """Test action validation for allowed actions."""
        import yaml
        yaml_content = yaml.dump(self.sample_contract)
        self.generator.load_contract_from_string(yaml_content)
        
        is_allowed, reasons = self.generator.validate_action(
            "vote_proposal",
            {"proposal_id": "123"}
        )
        
        # Generic action should be allowed
        assert is_allowed is True
    
    def test_validate_action_blocked(self):
        """Test action validation for blocked actions."""
        import yaml
        yaml_content = yaml.dump(self.sample_contract)
        self.generator.load_contract_from_string(yaml_content)
        
        # Add liability boundaries to contract
        self.generator.contract["legal_primitives"]["liability_boundaries"] = {
            "member_liability": {"requirements": []}
        }
        
        is_allowed, reasons = self.generator.validate_action(
            "external_contract",
            {}
        )
        
        assert is_allowed is False
        assert len(reasons) > 0


class TestComponentTemplateEngine:
    """Tests for the ComponentTemplateEngine class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.engine = ComponentTemplateEngine()
    
    def test_get_template_exists(self):
        """Test getting an existing template."""
        template = self.engine.get_template("immutable_event_logger")
        
        assert template is not None
        assert "description" in template
        assert "interfaces" in template
    
    def test_get_template_not_exists(self):
        """Test getting a non-existent template."""
        template = self.engine.get_template("nonexistent_template")
        
        assert template is None
    
    def test_generate_spec(self):
        """Test generating a component specification."""
        spec = self.engine.generate_spec(
            component_name="immutable_event_logger",
            legal_basis="Wyoming DAO LLC audit requirement",
            priority="high",
            estimated_effort="medium"
        )
        
        assert spec is not None
        assert isinstance(spec, ComponentSpec)
        assert spec.name == "immutable_event_logger"
        assert spec.priority == "high"
        assert len(spec.interfaces) > 0
    
    def test_generate_spec_unknown_component(self):
        """Test generating spec for unknown component returns None."""
        spec = self.engine.generate_spec(
            component_name="unknown_component",
            legal_basis="Test legal basis"
        )
        
        assert spec is None
    
    def test_generate_specs_for_requirements(self):
        """Test generating specs for multiple requirements."""
        requirements = [
            RequiredComponent(
                "id1", "immutable_event_logger", "Audit log",
                "Legal req", "mandatory", "append_only_log", "high", "medium"
            ),
            RequiredComponent(
                "id2", "percentage_validator", "Validate percentage",
                "Legal req", "mandatory", "manifest_checker", "high", "low"
            ),
        ]
        
        specs = self.engine.generate_specs_for_requirements(requirements)
        
        assert len(specs) == 2
        assert all(isinstance(spec, ComponentSpec) for spec in specs)
    
    def test_export_spec_to_yaml(self):
        """Test exporting spec to YAML format."""
        spec = ComponentSpec(
            name="test_component",
            description="Test description",
            legal_basis="Test legal basis",
            interfaces=["method1() -> str"],
            dependencies=["dep1"],
            security_requirements=["req1"],
            compliance_tags=["tag1"],
            estimated_effort="medium",
            priority="high"
        )
        
        yaml_content = self.engine.export_spec_to_yaml(spec)
        
        assert "test_component" in yaml_content
        assert "Test description" in yaml_content
    
    def test_export_spec_to_markdown(self):
        """Test exporting spec to Markdown format."""
        spec = ComponentSpec(
            name="test_component",
            description="Test description",
            legal_basis="Test legal basis",
            interfaces=["method1() -> str"],
            dependencies=["dep1"],
            security_requirements=["req1"],
            compliance_tags=["tag1"],
            estimated_effort="medium",
            priority="high"
        )
        
        md_content = self.engine.export_spec_to_markdown(spec)
        
        assert "# Component Specification: test_component" in md_content
        assert "Test description" in md_content
        assert "## Security Requirements" in md_content


class TestAutoPRCreator:
    """Tests for the AutoPRCreator class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.pr_creator = AutoPRCreator(self.temp_dir)
    
    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_ensure_output_dir(self):
        """Test output directory creation."""
        self.pr_creator.ensure_output_dir()
        
        assert (Path(self.temp_dir) / "specs").exists()
        assert (Path(self.temp_dir) / "scaffolds").exists()
        assert (Path(self.temp_dir) / "issues").exists()
    
    def test_generate_component_scaffold(self):
        """Test scaffold generation."""
        spec = ComponentSpec(
            name="test_component",
            description="Test description",
            legal_basis="Test legal basis",
            interfaces=["method1(arg: str) -> str"],
            dependencies=["json"],
            security_requirements=["Security req"],
            compliance_tags=["tag1"],
            estimated_effort="medium",
            priority="high"
        )
        
        filepath = self.pr_creator.generate_component_scaffold(spec)
        
        assert os.path.exists(filepath)
        with open(filepath, 'r') as f:
            content = f.read()
        assert "class TestComponent" in content
        assert "def method1" in content
    
    def test_generate_spec_files(self):
        """Test spec file generation."""
        spec = ComponentSpec(
            name="test_component",
            description="Test description",
            legal_basis="Test legal basis",
            interfaces=["method1() -> str"],
            dependencies=[],
            security_requirements=["req1"],
            compliance_tags=["tag1"],
            estimated_effort="medium",
            priority="high"
        )
        
        yaml_path, md_path = self.pr_creator.generate_spec_files(spec)
        
        assert os.path.exists(yaml_path)
        assert os.path.exists(md_path)
        assert yaml_path.endswith(".yaml")
        assert md_path.endswith(".md")
    
    def test_generate_issue_template(self):
        """Test issue template generation."""
        spec = ComponentSpec(
            name="test_component",
            description="Test description",
            legal_basis="Test legal basis",
            interfaces=["method1() -> str"],
            dependencies=[],
            security_requirements=["req1"],
            compliance_tags=["tag1"],
            estimated_effort="medium",
            priority="high"
        )
        
        filepath = self.pr_creator.generate_issue_template(spec)
        
        assert os.path.exists(filepath)
        with open(filepath, 'r') as f:
            content = f.read()
        assert "test_component" in content
        assert "Legal Basis" in content
    
    def test_generate_pr_description(self):
        """Test PR description generation."""
        specs = [
            ComponentSpec(
                name="comp1",
                description="Component 1",
                legal_basis="Legal basis 1",
                interfaces=["method1() -> str"],
                dependencies=[],
                security_requirements=["req1"],
                compliance_tags=["tag1"],
                estimated_effort="medium",
                priority="high"
            ),
        ]
        
        pr_desc = self.pr_creator.generate_pr_description(specs)
        
        assert "comp1" in pr_desc
        assert "Legal-Firewall" in pr_desc
        assert "LB-GSE" in pr_desc
    
    def test_generate_all_for_components(self):
        """Test generating all artifacts."""
        required = [
            RequiredComponent(
                "id1", "immutable_event_logger", "Audit log",
                "Legal req", "mandatory", "append_only_log", "high", "medium"
            ),
        ]
        
        results = self.pr_creator.generate_all_for_components(required)
        
        assert "scaffolds" in results
        assert "specs_yaml" in results
        assert "specs_md" in results
        assert "issues" in results
        assert "pr_description" in results
        assert len(results["scaffolds"]) > 0


class TestGenerateRequiredComponentsFunction:
    """Tests for the standalone generate_required_components function."""
    
    def test_basic_usage(self):
        """Test basic function usage."""
        contract = {
            "legal_primitives": {
                "test_category": {
                    "test_requirement": {
                        "requirements": [
                            {
                                "id": "test_id",
                                "description": "Test description",
                                "constraint_type": "mandatory",
                                "enforcement": "test_enforcement"
                            }
                        ]
                    }
                }
            },
            "component_registry": {
                "implemented": []
            },
            "capability_mappings": {
                "test_enforcement": {
                    "component": "test_component"
                }
            }
        }
        
        needed = generate_required_components(contract)
        
        assert "test_component" in needed
    
    def test_empty_contract(self):
        """Test with empty contract."""
        contract = {"legal_primitives": {}}
        
        needed = generate_required_components(contract)
        
        assert needed == []


def run_tests():
    """Run all tests and report results."""
    import traceback
    
    test_classes = [
        TestLegalFirewallGenerator,
        TestComponentTemplateEngine,
        TestAutoPRCreator,
        TestGenerateRequiredComponentsFunction,
    ]
    
    total_tests = 0
    passed_tests = 0
    failed_tests = []
    
    for test_class in test_classes:
        print(f"\n{'='*60}")
        print(f"Running {test_class.__name__}")
        print('='*60)
        
        instance = test_class()
        
        for method_name in dir(instance):
            if method_name.startswith("test_"):
                total_tests += 1
                
                # Setup
                if hasattr(instance, 'setup_method'):
                    try:
                        instance.setup_method()
                    except Exception as e:
                        print(f"  ❌ {method_name} - Setup failed: {e}")
                        failed_tests.append((test_class.__name__, method_name, str(e)))
                        continue
                
                # Run test
                try:
                    method = getattr(instance, method_name)
                    method()
                    print(f"  ✅ {method_name}")
                    passed_tests += 1
                except AssertionError as e:
                    print(f"  ❌ {method_name} - Assertion failed: {e}")
                    failed_tests.append((test_class.__name__, method_name, str(e)))
                except Exception as e:
                    print(f"  ❌ {method_name} - Error: {e}")
                    traceback.print_exc()
                    failed_tests.append((test_class.__name__, method_name, str(e)))
                
                # Teardown
                if hasattr(instance, 'teardown_method'):
                    try:
                        instance.teardown_method()
                    except Exception:
                        pass
    
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print('='*60)
    print(f"Total tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {len(failed_tests)}")
    
    if failed_tests:
        print("\nFailed tests:")
        for class_name, method_name, error in failed_tests:
            print(f"  - {class_name}.{method_name}: {error}")
    
    return len(failed_tests) == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
