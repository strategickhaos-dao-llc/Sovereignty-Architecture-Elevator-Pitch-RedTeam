#!/usr/bin/env python3
"""
Strategickhaos OS Prompt Engineering Loader
Loads YAML configuration and generates dynamic prompts for OS simulation/design.

Usage:
    python strategickhaos_os_loader.py --generate-prompts
    python strategickhaos_os_loader.py --run-execution-flow
    python strategickhaos_os_loader.py --export-blueprint
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("Error: PyYAML not installed. Install with: pip install pyyaml")
    sys.exit(1)


class StrategickhaosOSLoader:
    """Loader and processor for Strategickhaos OS prompt engineering YAML."""

    def __init__(self, yaml_path: str = "strategickhaos_os_prompt_engineering.yaml"):
        self.yaml_path = Path(yaml_path)
        self.config: dict[str, Any] = {}
        self._execution_results: dict[str, Any] | None = None
        self._load_yaml()

    def _load_yaml(self) -> None:
        """Load and parse the YAML configuration file."""
        if not self.yaml_path.exists():
            raise FileNotFoundError(f"YAML file not found: {self.yaml_path}")

        with open(self.yaml_path, encoding="utf-8") as f:
            self.config = yaml.safe_load(f)

        print(f"✅ Loaded Strategickhaos OS configuration from {self.yaml_path}")

    def get_metadata(self) -> dict[str, Any]:
        """Return OS metadata."""
        return self.config.get("metadata", {})

    def get_dialectical_core(self) -> dict[str, Any]:
        """Return dialectical core configuration (thesis, antithesis, synthesis)."""
        return self.config.get("dialectical_core", {})

    def get_mappings(self) -> dict[str, Any]:
        """Return all mappings integration configuration."""
        return self.config.get("mappings_integration", {})

    def get_prompt_templates(self) -> dict[str, str]:
        """Return all prompt templates."""
        return self.config.get("prompt_templates", {})

    def generate_prompt(self, template_name: str, **kwargs: Any) -> str:
        """
        Generate a prompt from a template with placeholder substitution.

        Args:
            template_name: Name of the template (base_system_prompt, feature_generation_prompt, etc.)
            **kwargs: Values to substitute for placeholders in the template

        Returns:
            Generated prompt string with placeholders filled

        Raises:
            ValueError: If template is not found or required placeholders are missing
        """
        templates = self.get_prompt_templates()
        if template_name not in templates:
            raise ValueError(f"Template '{template_name}' not found. Available: {list(templates.keys())}")

        template = templates[template_name]

        # Convert list values to comma-separated strings
        formatted_kwargs = {}
        for key, value in kwargs.items():
            if isinstance(value, list):
                formatted_kwargs[key] = ", ".join(str(v) for v in value)
            else:
                formatted_kwargs[key] = str(value)

        # Find all placeholders in the template
        placeholders = set(re.findall(r"\{(\w+)\}", template))

        # Check for missing required placeholders
        missing = placeholders - set(formatted_kwargs.keys())
        if missing:
            print(f"Warning: Unsubstituted placeholders in template '{template_name}': {missing}")

        # Substitute placeholders
        for key, value in formatted_kwargs.items():
            placeholder = "{" + key + "}"
            template = template.replace(placeholder, value)

        return template

    def generate_base_system_prompt(self, feature: str = "kernel") -> str:
        """Generate the base system prompt for OS architecture."""
        metadata = self.get_metadata()
        dialectical = self.get_dialectical_core()

        mappings = [m for m in metadata.get("combined_mappings", [])]
        mappings_str = "; ".join(str(m) for m in mappings)

        return self.generate_prompt(
            "base_system_prompt",
            mappings=mappings_str,
            thesis=dialectical.get("thesis", "Order"),
            antithesis=dialectical.get("antithesis", "Chaos"),
            feature=feature,
        )

    def generate_feature_prompt(self, contradiction: str, analogies: list[str] | None = None) -> str:
        """Generate a feature generation prompt for a specific contradiction."""
        if analogies is None:
            mappings = self.get_mappings()
            analogies = [str(a) for a in mappings.get("strong_analogies_pool", [])[:3]]

        return self.generate_prompt(
            "feature_generation_prompt",
            contradiction_example=contradiction,
            selected_analogies=analogies,
        )

    def run_execution_flow(self, use_cache: bool = True) -> dict[str, Any]:
        """
        Execute the dialectical OS creation flow.

        Args:
            use_cache: If True, return cached results if available

        Returns:
            Dictionary containing generated prompts and OS blueprint
        """
        # Return cached results if available and caching is enabled
        if use_cache and self._execution_results is not None:
            return self._execution_results

        print("\n🚀 Running Strategickhaos OS Execution Flow...")

        execution_flow = self.config.get("execution_flow", {})
        dialectical = self.get_dialectical_core()
        methodology = self.config.get("os_methodology", {})

        results = {
            "timestamp": datetime.now().isoformat(),
            "os_name": self.get_metadata().get("os_name", "Strategickhaos OS"),
            "phases": [],
            "generated_prompts": [],
            "blueprint": {},
        }

        # Phase 1: Init - Load metadata and mappings
        print("📋 Phase 1: Initializing metadata and mappings...")
        results["phases"].append({
            "name": "init",
            "status": "complete",
            "action": execution_flow.get("init", "Load metadata and mappings"),
        })

        # Phase 2: Loop - Process contradictions
        print("🔄 Phase 2: Processing contradictions dialectically...")
        synthesis_rules = dialectical.get("synthesis_rules", [])
        contradictions = [
            "stability vs. entropy",
            "order vs. chaos",
            "DNA fidelity vs. mutation",
        ]

        for contradiction in contradictions:
            prompt = self.generate_feature_prompt(contradiction)
            results["generated_prompts"].append({
                "contradiction": contradiction,
                "prompt": prompt,
                "synthesis_rules_applied": [str(r) for r in synthesis_rules],
            })
            print(f"   ✓ Generated prompt for: {contradiction}")

        results["phases"].append({
            "name": "loop",
            "status": "complete",
            "contradictions_processed": len(contradictions),
        })

        # Phase 3: End - Export blueprint
        print("📦 Phase 3: Generating OS blueprint...")
        results["blueprint"] = {
            "core_components": methodology.get("core_components", []),
            "birth_process": methodology.get("birth_process", []),
            "windows_like_elements": methodology.get("windows_like_elements", []),
            "emergent_properties": self.get_mappings().get("emergent_properties", []),
        }

        results["phases"].append({
            "name": "end",
            "status": "complete",
            "action": execution_flow.get("end", "Export as OS blueprint"),
        })

        print("✅ Execution flow complete!")

        # Cache the results
        self._execution_results = results
        return results

    def export_blueprint(self, output_format: str = "markdown") -> str:
        """
        Export the OS blueprint in the specified format.

        Args:
            output_format: Output format (markdown or json)

        Returns:
            Blueprint string in the requested format
        """
        results = self.run_execution_flow()

        if output_format == "json":
            return json.dumps(results, indent=2)

        # Generate Markdown blueprint
        metadata = self.get_metadata()
        dialectical = self.get_dialectical_core()
        blueprint = results["blueprint"]

        markdown = f"""# {metadata.get('os_name', 'Strategickhaos OS')} Blueprint

**Generated:** {results['timestamp']}
**Philosophy:** {metadata.get('core_philosophy', 'N/A')}

## Dialectical Foundation

- **Thesis:** {dialectical.get('thesis', 'N/A')}
- **Antithesis:** {dialectical.get('antithesis', 'N/A')}

### Synthesis Rules
"""
        for rule in dialectical.get("synthesis_rules", []):
            markdown += f"- {rule}\n"

        markdown += """
## Core Components
"""
        for component in blueprint.get("core_components", []):
            markdown += f"- {component}\n"

        markdown += """
## Birth Process
"""
        for step in blueprint.get("birth_process", []):
            markdown += f"1. {step}\n"

        markdown += """
## Windows-Like Elements (Chaotic)
"""
        for element in blueprint.get("windows_like_elements", []):
            markdown += f"- {element}\n"

        markdown += """
## Emergent Properties
"""
        for prop in blueprint.get("emergent_properties", []):
            markdown += f"- {prop}\n"

        markdown += """
## Generated Prompts

"""
        for i, prompt_data in enumerate(results["generated_prompts"], 1):
            markdown += f"""### Prompt {i}: {prompt_data['contradiction']}

```
{prompt_data['prompt']}
```

"""

        markdown += """---
*Built with the Strategickhaos OS Prompt Engineering Framework*
*Transform contradictions into creation through dialectical synthesis*
"""

        return markdown


def main() -> None:
    """Main entry point for the Strategickhaos OS loader."""
    parser = argparse.ArgumentParser(
        description="Strategickhaos OS Prompt Engineering Loader",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python strategickhaos_os_loader.py --generate-prompts
    python strategickhaos_os_loader.py --run-execution-flow
    python strategickhaos_os_loader.py --export-blueprint --format markdown
    python strategickhaos_os_loader.py --export-blueprint --format json
        """,
    )

    parser.add_argument(
        "--yaml-path",
        default="strategickhaos_os_prompt_engineering.yaml",
        help="Path to the YAML configuration file",
    )
    parser.add_argument(
        "--generate-prompts",
        action="store_true",
        help="Generate and display all prompt templates",
    )
    parser.add_argument(
        "--run-execution-flow",
        action="store_true",
        help="Run the full execution flow to generate OS features",
    )
    parser.add_argument(
        "--export-blueprint",
        action="store_true",
        help="Export the complete OS blueprint",
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format for blueprint export",
    )
    parser.add_argument(
        "--output",
        help="Output file path (defaults to stdout)",
    )

    args = parser.parse_args()

    # Default to showing help if no action specified
    if not any([args.generate_prompts, args.run_execution_flow, args.export_blueprint]):
        parser.print_help()
        return

    try:
        loader = StrategickhaosOSLoader(args.yaml_path)

        if args.generate_prompts:
            print("\n📝 Generated Prompts:\n")

            print("=" * 60)
            print("BASE SYSTEM PROMPT (for kernel feature):")
            print("=" * 60)
            print(loader.generate_base_system_prompt("kernel"))

            print("\n" + "=" * 60)
            print("FEATURE GENERATION PROMPT:")
            print("=" * 60)
            print(loader.generate_feature_prompt("stability vs. chaos"))

        if args.run_execution_flow:
            results = loader.run_execution_flow()
            print("\n📊 Execution Results:")
            print(json.dumps(results, indent=2))

        if args.export_blueprint:
            blueprint = loader.export_blueprint(args.format)

            if args.output:
                output_path = Path(args.output)
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(blueprint)
                print(f"✅ Blueprint exported to: {output_path}")
            else:
                print(blueprint)

    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"❌ YAML parsing error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
