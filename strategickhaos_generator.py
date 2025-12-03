#!/usr/bin/env python3
"""
Strategickhaos Generator - Dialectical Engine for OS Feature Generation
Strategickhaos DAO LLC - Multi-AI Collaboration Framework

This tool loads YAML configuration and generates prompts dynamically by:
1. Parsing the YAML structure with mappings and dialectical core
2. Dialectically processing input contradictions
3. Selecting relevant analogies based on keyword matching
4. Outputting generated prompts, OS methodology snippets, and CSV exports

Usage:
    python strategickhaos_generator.py <yaml_path> [contradiction1] [contradiction2] ...

Example:
    python strategickhaos_generator.py strategickhaos.yaml "stability vs mutation" "order vs chaos"
"""

import csv
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml


class StrategickhaosGenerator:
    """Generator for dialectical OS features and multi-AI collaboration prompts."""

    def __init__(self, yaml_path: str):
        """Initialize the generator with a YAML configuration file.

        Args:
            yaml_path: Path to the strategickhaos.yaml configuration file.

        Raises:
            FileNotFoundError: If the YAML file doesn't exist.
            yaml.YAMLError: If the YAML file is malformed.
        """
        with open(yaml_path, "r", encoding="utf-8") as file:
            self.config = yaml.safe_load(file)

        self.mappings = self.config.get("mappings_integration", {}).get(
            "strong_analogies_pool", []
        )
        self.dialectical_core = self.config.get("dialectical_core", {})
        self.prompt_templates = self.config.get("prompt_templates", {})
        self.resolution_patterns = self.dialectical_core.get("resolution_patterns", {})

    def select_analogies(self, contradiction: str, max_results: int = 5) -> List[str]:
        """Select relevant analogies based on keyword matching.

        Args:
            contradiction: The contradiction string to match against.
            max_results: Maximum number of analogies to return.

        Returns:
            List of relevant analogies, or fallback to first 3 if no match.
        """
        contradiction_words = set(contradiction.lower().split())
        scored_analogies: List[Tuple[str, int]] = []

        for analogy in self.mappings:
            analogy_lower = analogy.lower()
            score = sum(1 for word in contradiction_words if word in analogy_lower)
            if score > 0:
                scored_analogies.append((analogy, score))

        # Sort by score descending and return top matches
        scored_analogies.sort(key=lambda x: x[1], reverse=True)
        selected = [a[0] for a in scored_analogies[:max_results]]

        # Fallback to first 3 analogies if no matches
        return selected if selected else self.mappings[:3]

    def _find_resolution_pattern(self, contradiction: str) -> Optional[Dict[str, Any]]:
        """Find a matching resolution pattern for the contradiction.

        Args:
            contradiction: The contradiction string.

        Returns:
            The matching resolution pattern dict, or None if not found.
        """
        contradiction_lower = contradiction.lower().replace(" ", "_")

        for pattern_key, pattern_value in self.resolution_patterns.items():
            if pattern_key in contradiction_lower:
                return pattern_value
            # Also check for reversed order (e.g., "mutation vs stability")
            parts = contradiction_lower.split("_vs_")
            if len(parts) == 2:
                reversed_key = f"{parts[1]}_vs_{parts[0]}"
                if reversed_key == pattern_key:
                    return pattern_value

        return None

    def generate_synthesis(self, contradiction: str) -> str:
        """Generate a dialectical synthesis for a given contradiction.

        Args:
            contradiction: The contradiction to resolve (e.g., "stability vs mutation").

        Returns:
            A formatted synthesis string with thesis, antithesis, and resolution.
        """
        thesis = self.dialectical_core.get("thesis", "Order and structure")
        antithesis = self.dialectical_core.get("antithesis", "Chaos and adaptation")
        selected_analogies = self.select_analogies(contradiction)

        synthesis = f"Thesis: {thesis}\n"
        synthesis += f"Antithesis: {antithesis}\n"
        synthesis += f"Contradiction: {contradiction}\n"
        synthesis += "Selected Analogies: " + ", ".join(selected_analogies) + "\n"
        synthesis += "Synthesis: "

        # Check for predefined resolution patterns
        pattern = self._find_resolution_pattern(contradiction)
        if pattern:
            synthesis += pattern.get(
                "synthesis", "Dialectically birthed feature from contradiction resolution."
            )
            if pattern.get("os_feature"):
                synthesis += f"\nOS Feature: {pattern['os_feature']}"
        else:
            # Generate generic synthesis based on keywords
            synthesis += self._generate_generic_synthesis(contradiction, selected_analogies)

        return synthesis

    def _generate_generic_synthesis(
        self, contradiction: str, analogies: List[str]
    ) -> str:
        """Generate a generic synthesis when no predefined pattern exists.

        Args:
            contradiction: The contradiction string.
            analogies: List of selected analogies.

        Returns:
            A generic synthesis string.
        """
        # Extract key concepts from analogies
        analogy_concepts = []
        for analogy in analogies[:2]:
            if "=" in analogy:
                concept = analogy.split("=")[0].strip()
                analogy_concepts.append(concept)

        concepts_str = " and ".join(analogy_concepts) if analogy_concepts else "system components"

        return (
            f"Generic Feature - Dialectically birthed component using {concepts_str} "
            f"strategies for resilient processes. This contradiction ({contradiction}) "
            "resolves through emergent behavior that balances both elements."
        )

    def generate_prompt(
        self, contradiction: str, feature: str = "Kernel", template_key: str = "feature_generation_prompt"
    ) -> str:
        """Generate a prompt from templates using the contradiction.

        Args:
            contradiction: The contradiction to incorporate into the prompt.
            feature: The feature type to generate (default: "Kernel").
            template_key: The template key to use from prompt_templates.

        Returns:
            A formatted prompt string.
        """
        template = self.prompt_templates.get(template_key, "")
        if not template:
            return f"No template found for key: {template_key}"

        selected_analogies = self.select_analogies(contradiction)

        # Replace placeholders manually to handle mixed placeholder styles
        prompt = template.replace("{contradiction_example}", contradiction)
        prompt = prompt.replace("{selected_analogies}", ", ".join(selected_analogies))
        prompt = prompt.replace("{feature}", feature)

        return prompt

    def simulate_os_birth(self, contradictions: List[str]) -> Dict[str, str]:
        """Simulate the birth of OS features from contradictions.

        Args:
            contradictions: List of contradiction strings.

        Returns:
            A dictionary mapping feature names to their synthesis descriptions.
        """
        os_blueprint: Dict[str, str] = {}

        for contradiction in contradictions:
            # Extract feature name from contradiction (expects "X vs Y" format)
            parts = contradiction.split(" vs ")
            if len(parts) >= 2:
                feature_name = parts[0].strip().capitalize() + " Module"
            else:
                # Fallback for non-standard formats
                feature_name = contradiction.strip().capitalize() + " Module"

            os_blueprint[feature_name] = self.generate_synthesis(contradiction)

        return os_blueprint

    def export_analogies_csv(self, output_path: str = "analogies.csv") -> str:
        """Export strong analogies to a CSV file.

        Args:
            output_path: Path for the CSV output file.

        Returns:
            Path to the created CSV file.
        """
        with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Analogy", "Description"])

            for analogy in self.mappings:
                if ":" in analogy:
                    parts = analogy.split(":", 1)
                    writer.writerow([parts[0].strip(), parts[1].strip()])
                else:
                    writer.writerow([analogy, ""])

        return output_path

    def export_blueprint_json(
        self, contradictions: List[str], output_path: str = "os_blueprint.json"
    ) -> str:
        """Export the OS blueprint to a JSON file.

        Args:
            contradictions: List of contradictions to process.
            output_path: Path for the JSON output file.

        Returns:
            Path to the created JSON file.
        """
        blueprint = self.simulate_os_birth(contradictions)
        config_blueprint = self.config.get("os_blueprint", {})

        export_data = {
            "framework_name": self.config.get("framework_name", "Strategickhaos Engine"),
            "version": config_blueprint.get("version", "0.1.0"),
            "generated_features": blueprint,
            "core_modules": config_blueprint.get("core_modules", []),
            "dialectical_core": {
                "thesis": self.dialectical_core.get("thesis"),
                "antithesis": self.dialectical_core.get("antithesis"),
                "synthesis_principle": self.dialectical_core.get("synthesis_principle"),
            },
        }

        with open(output_path, "w", encoding="utf-8") as jsonfile:
            json.dump(export_data, jsonfile, indent=2)

        return output_path

    def list_available_templates(self) -> List[str]:
        """List all available prompt templates.

        Returns:
            List of template key names.
        """
        return list(self.prompt_templates.keys())


def main() -> int:
    """Main entry point for the Strategickhaos Generator.

    Returns:
        Exit code (0 for success, 1 for failure).
    """
    if len(sys.argv) < 2:
        print("Usage: python strategickhaos_generator.py <yaml_path> [contradiction1] [contradiction2]...")
        print("\nExample:")
        print('  python strategickhaos_generator.py strategickhaos.yaml "stability vs mutation" "order vs chaos"')
        print("\nThis tool generates dialectical prompts and OS features from contradictions.")
        return 1

    yaml_path = sys.argv[1]
    contradictions = sys.argv[2:] if len(sys.argv) > 2 else ["stability vs mutation", "order vs chaos"]

    try:
        generator = StrategickhaosGenerator(yaml_path)
    except FileNotFoundError:
        print(f"Error: YAML file not found: {yaml_path}")
        return 1
    except yaml.YAMLError as e:
        print(f"Error: Invalid YAML file: {e}")
        return 1

    print("=" * 60)
    print("STRATEGICKHAOS DIALECTICAL ENGINE")
    print("=" * 60)

    # Display available templates
    print("\nAvailable Prompt Templates:")
    for template in generator.list_available_templates():
        print(f"  - {template}")

    # Generate prompts for each contradiction
    print("\n" + "=" * 60)
    print("GENERATED PROMPTS AND SYNTHESES")
    print("=" * 60)

    for contradiction in contradictions:
        print(f"\n--- Contradiction: '{contradiction}' ---")
        print("\nPrompt:")
        print(generator.generate_prompt(contradiction))

    # Generate OS Blueprint
    print("\n" + "=" * 60)
    print("STRATEGICKHAOS OS BLUEPRINT")
    print("=" * 60)

    blueprint = generator.simulate_os_birth(contradictions)
    for feature, desc in blueprint.items():
        print(f"\n{feature}:")
        print("-" * 40)
        print(desc)

    # Export to CSV
    csv_path = generator.export_analogies_csv()
    print(f"\n✅ Exported strong analogies to {csv_path}")

    # Export to JSON
    json_path = generator.export_blueprint_json(contradictions)
    print(f"✅ Exported OS blueprint to {json_path}")

    print("\n" + "=" * 60)
    print("GENERATION COMPLETE")
    print("=" * 60)
    print(f"Contradictions processed: {len(contradictions)}")
    print(f"Analogies available: {len(generator.mappings)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
