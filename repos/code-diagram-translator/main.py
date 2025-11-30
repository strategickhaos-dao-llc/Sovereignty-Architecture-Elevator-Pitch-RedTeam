#!/usr/bin/env python3
"""
Code-to-Diagram Translator
IDEA_002 - StrategicKhaos DAO LLC

Tool that ingests source code and generates living architecture diagrams
that update automatically as the codebase evolves.

Video Module: Q034
Department: infra_cloud
"""

import argparse
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class DiagramConfig:
    """Configuration for diagram generation."""
    input_path: str
    output_format: str = "mermaid"
    output_path: str = "./output"
    include_private: bool = False
    max_depth: int = 5


class CodeParser:
    """Parse source code to extract structural information."""
    
    def __init__(self, config: DiagramConfig):
        self.config = config
        self.modules: list[dict] = []
        self.relationships: list[dict] = []
    
    def parse(self, path: str) -> None:
        """Parse source code at the given path."""
        source_path = Path(path)
        if not source_path.exists():
            print(f"Warning: Path {path} does not exist")
            return
        
        if source_path.is_file():
            self._parse_file(source_path)
        elif source_path.is_dir():
            self._parse_directory(source_path)
    
    def _parse_file(self, file_path: Path) -> None:
        """Parse a single file."""
        # Placeholder for actual parsing logic
        self.modules.append({
            "name": file_path.stem,
            "type": "module",
            "path": str(file_path)
        })
    
    def _parse_directory(self, dir_path: Path, depth: int = 0) -> None:
        """Recursively parse a directory."""
        if depth >= self.config.max_depth:
            return
        
        for item in dir_path.iterdir():
            if item.name.startswith('.'):
                continue
            if item.is_file() and item.suffix in ('.py', '.js', '.ts', '.java', '.go'):
                self._parse_file(item)
            elif item.is_dir():
                self._parse_directory(item, depth + 1)


class DiagramGenerator:
    """Generate diagrams from parsed code structure."""
    
    def __init__(self, parser: CodeParser):
        self.parser = parser
    
    def generate(self, format_type: str = "mermaid") -> str:
        """Generate diagram in the specified format."""
        if format_type == "mermaid":
            return self._generate_mermaid()
        elif format_type == "dot":
            return self._generate_dot()
        elif format_type == "plantuml":
            return self._generate_plantuml()
        else:
            raise ValueError(f"Unsupported format: {format_type}")
    
    def _generate_mermaid(self) -> str:
        """Generate Mermaid diagram."""
        lines = ["graph TD"]
        
        for module in self.parser.modules:
            node_id = module["name"].replace("-", "_").replace(".", "_")
            lines.append(f"    {node_id}[{module['name']}]")
        
        for rel in self.parser.relationships:
            lines.append(f"    {rel['from']} --> {rel['to']}")
        
        return "\n".join(lines)
    
    def _generate_dot(self) -> str:
        """Generate DOT/Graphviz diagram."""
        lines = ["digraph CodeStructure {"]
        lines.append("    rankdir=TB;")
        
        for module in self.parser.modules:
            node_id = module["name"].replace("-", "_").replace(".", "_")
            lines.append(f'    {node_id} [label="{module["name"]}"];')
        
        for rel in self.parser.relationships:
            lines.append(f"    {rel['from']} -> {rel['to']};")
        
        lines.append("}")
        return "\n".join(lines)
    
    def _generate_plantuml(self) -> str:
        """Generate PlantUML diagram."""
        lines = ["@startuml"]
        
        for module in self.parser.modules:
            lines.append(f"component [{module['name']}]")
        
        for rel in self.parser.relationships:
            lines.append(f"[{rel['from']}] --> [{rel['to']}]")
        
        lines.append("@enduml")
        return "\n".join(lines)


def main():
    """Main entry point for the Code-to-Diagram Translator."""
    parser = argparse.ArgumentParser(
        description="Code-to-Diagram Translator - Generate architecture diagrams from source code",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py ./src --format mermaid
  python main.py ./project --format dot --output ./diagrams
  python main.py . --max-depth 3 --include-private
        """
    )
    
    parser.add_argument(
        "input_path",
        nargs="?",
        default=".",
        help="Path to source code (default: current directory)"
    )
    parser.add_argument(
        "--format", "-f",
        choices=["mermaid", "dot", "plantuml"],
        default=os.environ.get("OUTPUT_FORMAT", "mermaid"),
        help="Output format (default: mermaid)"
    )
    parser.add_argument(
        "--output", "-o",
        default="./output",
        help="Output directory (default: ./output)"
    )
    parser.add_argument(
        "--max-depth", "-d",
        type=int,
        default=5,
        help="Maximum directory depth to traverse (default: 5)"
    )
    parser.add_argument(
        "--include-private",
        action="store_true",
        help="Include private/internal modules"
    )
    parser.add_argument(
        "--version", "-v",
        action="version",
        version="Code-to-Diagram Translator v0.1.0 (IDEA_002)"
    )
    
    args = parser.parse_args()
    
    # Create configuration
    config = DiagramConfig(
        input_path=args.input_path,
        output_format=args.format,
        output_path=args.output,
        include_private=args.include_private,
        max_depth=args.max_depth
    )
    
    print(f"Code-to-Diagram Translator (IDEA_002)")
    print(f"=====================================")
    print(f"Input Path: {config.input_path}")
    print(f"Output Format: {config.output_format}")
    print(f"Output Path: {config.output_path}")
    print()
    
    # Parse source code
    code_parser = CodeParser(config)
    code_parser.parse(config.input_path)
    
    print(f"Found {len(code_parser.modules)} modules")
    print()
    
    # Generate diagram
    generator = DiagramGenerator(code_parser)
    diagram = generator.generate(config.output_format)
    
    # Output result
    output_dir = Path(config.output_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    ext_map = {"mermaid": "md", "dot": "dot", "plantuml": "puml"}
    output_file = output_dir / f"architecture.{ext_map.get(config.output_format, 'txt')}"
    
    with open(output_file, "w") as f:
        if config.output_format == "mermaid":
            f.write("```mermaid\n")
            f.write(diagram)
            f.write("\n```\n")
        else:
            f.write(diagram)
    
    print(f"Diagram generated: {output_file}")
    print()
    print("Generated Output:")
    print("-" * 40)
    print(diagram)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
