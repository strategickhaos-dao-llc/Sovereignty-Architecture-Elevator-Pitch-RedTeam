#!/usr/bin/env python3
"""
Code-to-Diagram Translator (IDEA_002)

Ingests source code and generates living architecture diagrams
that update automatically as the codebase evolves.

Part of StrategicKhaos DAO LLC / Valoryield Engine
"""

import argparse
import ast
import os
import sys
from pathlib import Path
from typing import Optional


class CodeDiagramTranslator:
    """Translates source code into architecture diagrams."""

    SUPPORTED_EXTENSIONS = {".py", ".js", ".ts", ".java", ".go"}

    def __init__(self, repo_path: str, output_format: str = "mermaid"):
        self.repo_path = Path(repo_path)
        self.output_format = output_format
        self.dependencies: dict[str, list[str]] = {}

    def scan_repository(self) -> dict[str, list[str]]:
        """Scan repository for source files and extract dependencies."""
        for root, _dirs, files in os.walk(self.repo_path):
            for file in files:
                ext = Path(file).suffix
                if ext in self.SUPPORTED_EXTENSIONS:
                    filepath = Path(root) / file
                    self._analyze_file(filepath)
        return self.dependencies

    def _analyze_file(self, filepath: Path) -> None:
        """Analyze a single file for imports/dependencies."""
        if filepath.suffix == ".py":
            self._analyze_python(filepath)
        # Additional language support can be added here

    def _analyze_python(self, filepath: Path) -> None:
        """Extract imports from Python files using AST."""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read(), filename=str(filepath))

            module_name = filepath.stem
            imports: list[str] = []

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)

            self.dependencies[module_name] = imports
        except (SyntaxError, UnicodeDecodeError) as e:
            print(f"Warning: Could not parse {filepath}: {e}", file=sys.stderr)

    def generate_mermaid(self) -> str:
        """Generate Mermaid diagram from dependencies."""
        lines = ["graph TD"]

        for module, deps in self.dependencies.items():
            safe_module = module.replace("-", "_")
            for dep in deps:
                safe_dep = dep.replace(".", "_").replace("-", "_")
                lines.append(f"    {safe_module} --> {safe_dep}")

        if len(lines) == 1:
            lines.append("    No_Dependencies[No dependencies found]")

        return "\n".join(lines)

    def generate_plantuml(self) -> str:
        """Generate PlantUML diagram from dependencies."""
        lines = ["@startuml", "!theme plain"]

        for module, deps in self.dependencies.items():
            for dep in deps:
                lines.append(f'"{module}" --> "{dep}"')

        lines.append("@enduml")
        return "\n".join(lines)

    def generate_dot(self) -> str:
        """Generate DOT (Graphviz) diagram from dependencies."""
        lines = ["digraph G {", "    rankdir=TB;"]

        for module, deps in self.dependencies.items():
            safe_module = module.replace("-", "_")
            for dep in deps:
                safe_dep = dep.replace(".", "_").replace("-", "_")
                lines.append(f'    "{safe_module}" -> "{safe_dep}";')

        lines.append("}")
        return "\n".join(lines)

    def generate(self) -> str:
        """Generate diagram in the configured format."""
        self.scan_repository()

        generators = {
            "mermaid": self.generate_mermaid,
            "plantuml": self.generate_plantuml,
            "dot": self.generate_dot,
        }

        generator = generators.get(self.output_format)
        if not generator:
            raise ValueError(f"Unsupported format: {self.output_format}")

        return generator()


def main(argv: Optional[list[str]] = None) -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Code-to-Diagram Translator (IDEA_002)"
    )
    parser.add_argument(
        "--repo",
        type=str,
        default=".",
        help="Path to repository to analyze (default: current directory)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output file path (default: stdout)",
    )
    parser.add_argument(
        "--format",
        type=str,
        choices=["mermaid", "plantuml", "dot"],
        default=os.getenv("OUTPUT_FORMAT", "mermaid"),
        help="Output format (default: mermaid)",
    )

    args = parser.parse_args(argv)

    translator = CodeDiagramTranslator(args.repo, args.format)
    diagram = translator.generate()

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(diagram)
        print(f"Diagram written to {args.output}")
    else:
        print(diagram)

    return 0


if __name__ == "__main__":
    sys.exit(main())
