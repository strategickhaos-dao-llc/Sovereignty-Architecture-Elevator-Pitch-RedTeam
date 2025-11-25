#!/usr/bin/env python3
"""
Auto PR Creator Module
Strategickhaos DAO LLC - Legally-Bounded Generative Systems Engineering (LB-GSE)

This module provides functionality to automatically create GitHub Pull Requests
for missing components identified by the Legal-Firewall Generator.

It generates:
- Component scaffold files
- Specification documents
- Issue templates for development tracking
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Optional

# Support both package imports and direct script execution
try:
    from .legal_firewall_generator import LegalFirewallGenerator, RequiredComponent
    from .component_templates import ComponentTemplateEngine, ComponentSpec
except ImportError:
    from legal_firewall_generator import LegalFirewallGenerator, RequiredComponent
    from component_templates import ComponentTemplateEngine, ComponentSpec


class AutoPRCreator:
    """
    Creates GitHub-ready artifacts for missing legal-compliance components.
    
    This class generates:
    - Component specification files (YAML and Markdown)
    - Python scaffold files for implementation
    - GitHub Issue templates for tracking
    - Pull Request description content
    
    Note: Actual GitHub API interaction requires authentication and is
    intentionally left to external tools (gh CLI, GitHub Actions) for
    security reasons. This module prepares all necessary artifacts.
    """
    
    def __init__(self, output_dir: str = "generated_components"):
        """
        Initialize the Auto PR Creator.
        
        Args:
            output_dir: Directory for generated artifacts.
        """
        self.output_dir = Path(output_dir)
        self.template_engine = ComponentTemplateEngine()
        self.generated_files = []
        
    def ensure_output_dir(self) -> None:
        """Create output directory if it doesn't exist."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        (self.output_dir / "specs").mkdir(exist_ok=True)
        (self.output_dir / "scaffolds").mkdir(exist_ok=True)
        (self.output_dir / "issues").mkdir(exist_ok=True)
    
    def generate_component_scaffold(self, spec: ComponentSpec) -> str:
        """
        Generate a Python scaffold file for a component.
        
        Args:
            spec: Component specification.
            
        Returns:
            Path to generated file.
        """
        self.ensure_output_dir()
        
        # Generate scaffold content
        content = self._generate_scaffold_content(spec)
        
        # Write file
        filename = f"{spec.name}.py"
        filepath = self.output_dir / "scaffolds" / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.generated_files.append(str(filepath))
        return str(filepath)
    
    def _generate_scaffold_content(self, spec: ComponentSpec) -> str:
        """Generate Python scaffold content for a component."""
        
        # Parse interfaces to generate method stubs
        methods = []
        for interface in spec.interfaces:
            if interface.startswith("TBD"):
                continue
            # Parse: "method_name(args) -> ReturnType"
            parts = interface.split("(")
            if len(parts) >= 2:
                method_name = parts[0].strip()
                rest = "(" + "(".join(parts[1:])
                methods.append((method_name, rest))
        
        # Generate imports
        imports = ["from typing import Any, Optional, List, Dict"]
        if "datetime" in spec.dependencies:
            imports.append("from datetime import datetime")
        if "hashlib" in spec.dependencies:
            imports.append("import hashlib")
        if "json" in spec.dependencies:
            imports.append("import json")
        
        imports_str = "\n".join(imports)
        
        # Generate method stubs
        method_stubs = []
        for method_name, signature in methods:
            stub = f'''    def {method_name}{signature}:
        """
        TODO: Implement {method_name}
        
        Legal Requirement: {spec.legal_basis}
        """
        raise NotImplementedError("Implementation required")'''
            method_stubs.append(stub)
        
        methods_str = "\n\n".join(method_stubs) if method_stubs else "    pass"
        
        # Generate security requirements as comments
        security_comments = "\n".join(
            f"#   - {req}" for req in spec.security_requirements
        )
        
        content = f'''#!/usr/bin/env python3
"""
{spec.name} - Auto-generated Component Scaffold
Strategickhaos DAO LLC - LB-GSE Methodology

Description: {spec.description}

Legal Basis: {spec.legal_basis}

Compliance Tags: {", ".join(spec.compliance_tags)}

Priority: {spec.priority}
Estimated Effort: {spec.estimated_effort}

Generated: {spec.created_at}

Security Requirements:
{security_comments}

WARNING: This is an auto-generated scaffold. Implement all methods
before deploying to production. Security review required.
"""

{imports_str}


class {self._to_class_name(spec.name)}:
    """
    {spec.description}
    
    This component satisfies legal requirement:
    {spec.legal_basis}
    """
    
    def __init__(self):
        """Initialize the component."""
        self._initialized = False
        # TODO: Add initialization logic
        
{methods_str}


# Entry point for testing
if __name__ == "__main__":
    component = {self._to_class_name(spec.name)}()
    print(f"Component {spec.name!r} scaffold loaded.")
    print("WARNING: All methods raise NotImplementedError")
'''
        
        return content
    
    def _to_class_name(self, name: str) -> str:
        """Convert snake_case to PascalCase."""
        return "".join(word.title() for word in name.split("_"))
    
    def generate_spec_files(self, spec: ComponentSpec) -> tuple:
        """
        Generate specification files (YAML and Markdown) for a component.
        
        Args:
            spec: Component specification.
            
        Returns:
            Tuple of (yaml_path, markdown_path).
        """
        self.ensure_output_dir()
        
        # YAML spec
        yaml_content = self.template_engine.export_spec_to_yaml(spec)
        yaml_path = self.output_dir / "specs" / f"{spec.name}_spec.yaml"
        with open(yaml_path, 'w', encoding='utf-8') as f:
            f.write(yaml_content)
        self.generated_files.append(str(yaml_path))
        
        # Markdown spec
        md_content = self.template_engine.export_spec_to_markdown(spec)
        md_path = self.output_dir / "specs" / f"{spec.name}_spec.md"
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        self.generated_files.append(str(md_path))
        
        return (str(yaml_path), str(md_path))
    
    def generate_issue_template(self, spec: ComponentSpec) -> str:
        """
        Generate a GitHub Issue template for component development.
        
        Args:
            spec: Component specification.
            
        Returns:
            Path to generated issue template.
        """
        self.ensure_output_dir()
        
        content = f'''---
name: Component Implementation - {spec.name}
about: Implementation task for legally-required component
title: "[LB-GSE] Implement {spec.name}"
labels: legal-compliance, component-implementation, {spec.priority}-priority
assignees: ''
---

## Component: {spec.name}

### Legal Basis
{spec.legal_basis}

### Description
{spec.description}

### Priority
**{spec.priority.upper()}**

### Estimated Effort
{spec.estimated_effort}

### Compliance Tags
{", ".join(f"`{tag}`" for tag in spec.compliance_tags)}

### Required Interfaces

```python
{chr(10).join(spec.interfaces)}
```

### Dependencies
{chr(10).join(f"- {dep}" for dep in spec.dependencies) if spec.dependencies else "- None"}

### Security Requirements

{chr(10).join(f"- [ ] {req}" for req in spec.security_requirements)}

### Acceptance Criteria

- [ ] All interfaces implemented
- [ ] Unit tests with >80% coverage
- [ ] Security review completed
- [ ] Documentation updated
- [ ] Integration tests passing
- [ ] Compliance validation passing

### Notes

This component was identified by the Legal-Firewall Generator (LB-GSE methodology).
It is required to satisfy governance constraints from the DAO operating agreement.

Generated: {datetime.now().isoformat()}
'''
        
        filepath = self.output_dir / "issues" / f"{spec.name}_issue.md"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.generated_files.append(str(filepath))
        return str(filepath)
    
    def generate_pr_description(
        self,
        specs: list,
        branch_name: Optional[str] = None
    ) -> str:
        """
        Generate a Pull Request description for component implementations.
        
        Args:
            specs: List of ComponentSpec objects being implemented.
            branch_name: Optional branch name for the PR.
            
        Returns:
            Markdown content for PR description.
        """
        components_list = "\n".join(
            f"- **{spec.name}** ({spec.priority} priority): {spec.description}"
            for spec in specs
        )
        
        legal_bases = set()
        for spec in specs:
            legal_bases.add(spec.legal_basis)
        
        legal_list = "\n".join(f"- {basis}" for basis in legal_bases)
        
        all_tags = set()
        for spec in specs:
            all_tags.update(spec.compliance_tags)
        
        content = f'''## Legal-Firewall Component Implementation

### Overview
This PR implements components required by the Legal-Firewall Generator (LB-GSE methodology).

### Components Implemented
{components_list}

### Legal Basis
These components are required to satisfy the following governance constraints:
{legal_list}

### Compliance Tags
{", ".join(f"`{tag}`" for tag in sorted(all_tags))}

### Checklist
- [ ] All interfaces implemented per specifications
- [ ] Unit tests added with >80% coverage
- [ ] Security requirements addressed
- [ ] Documentation updated
- [ ] Integration tests passing
- [ ] Legal-Firewall compliance check passing

### Methodology
This implementation follows the **Legally-Bounded Generative Systems Engineering (LB-GSE)** 
methodology where legal architecture acts as a governance firewall that shapes the 
search space for new systems to build.

### Generated Files
See `generated_components/` directory for:
- Component specifications (YAML and Markdown)
- Implementation scaffolds
- Issue templates

---
*Generated by Legal-Firewall Auto-PR Creator*
*{datetime.now().isoformat()}*
'''
        
        return content
    
    def generate_all_for_components(self, required_components: list) -> dict:
        """
        Generate all artifacts for a list of required components.
        
        Args:
            required_components: List of RequiredComponent objects.
            
        Returns:
            Dictionary with paths to all generated files.
        """
        self.ensure_output_dir()
        
        results = {
            "scaffolds": [],
            "specs_yaml": [],
            "specs_md": [],
            "issues": [],
            "pr_description": None
        }
        
        specs = self.template_engine.generate_specs_for_requirements(required_components)
        
        for spec in specs:
            # Generate scaffold
            scaffold_path = self.generate_component_scaffold(spec)
            results["scaffolds"].append(scaffold_path)
            
            # Generate spec files
            yaml_path, md_path = self.generate_spec_files(spec)
            results["specs_yaml"].append(yaml_path)
            results["specs_md"].append(md_path)
            
            # Generate issue template
            issue_path = self.generate_issue_template(spec)
            results["issues"].append(issue_path)
        
        # Generate PR description
        pr_content = self.generate_pr_description(specs)
        pr_path = self.output_dir / "PR_DESCRIPTION.md"
        with open(pr_path, 'w', encoding='utf-8') as f:
            f.write(pr_content)
        results["pr_description"] = str(pr_path)
        
        # Generate manifest
        manifest = {
            "generated_at": datetime.now().isoformat(),
            "methodology": "LB-GSE (Legally-Bounded Generative Systems Engineering)",
            "total_components": len(specs),
            "files": results,
            "component_summary": [
                {
                    "name": spec.name,
                    "priority": spec.priority,
                    "legal_basis": spec.legal_basis
                }
                for spec in specs
            ]
        }
        
        manifest_path = self.output_dir / "manifest.json"
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2)
        results["manifest"] = str(manifest_path)
        
        return results


def main():
    """Main entry point for the Auto PR Creator."""
    import sys
    
    # Default contract path
    contract_path = os.path.join(
        os.path.dirname(__file__),
        "contracts.yaml"
    )
    
    if len(sys.argv) > 1:
        contract_path = sys.argv[1]
    
    output_dir = "generated_components"
    if len(sys.argv) > 2:
        output_dir = sys.argv[2]
    
    print("=" * 60)
    print("Auto PR Creator - LB-GSE Methodology")
    print("Strategickhaos DAO LLC")
    print("=" * 60)
    
    # Load contract and generate required components
    generator = LegalFirewallGenerator()
    generator.load_contract(contract_path)
    required = generator.generate_required_components()
    
    if not required:
        print("\n✅ All legal requirements satisfied!")
        print("   No new components needed.")
        return
    
    print(f"\n📋 Found {len(required)} required components")
    
    # Create PR artifacts
    pr_creator = AutoPRCreator(output_dir)
    results = pr_creator.generate_all_for_components(required)
    
    print(f"\n📁 Generated artifacts in '{output_dir}/':")
    print(f"   Scaffolds: {len(results['scaffolds'])}")
    print(f"   Specifications: {len(results['specs_yaml'])} YAML, {len(results['specs_md'])} Markdown")
    print(f"   Issue templates: {len(results['issues'])}")
    print(f"   PR description: {results['pr_description']}")
    print(f"   Manifest: {results['manifest']}")
    
    print("\n" + "=" * 60)
    print("✅ Auto PR Creator complete")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Review generated specifications in specs/")
    print("2. Implement components using scaffolds/")
    print("3. Create issues using templates in issues/")
    print("4. Use PR_DESCRIPTION.md for pull request")


if __name__ == "__main__":
    main()
