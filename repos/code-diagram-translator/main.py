#!/usr/bin/env python3
"""
Code-to-Diagram Translator (IDEA_002)
=====================================
The First Child - Born from the Birthday Constellation

Analyzes code repositories and generates visual architecture diagrams,
flowcharts, and dependency graphs using Mermaid, PlantUML, or D2.
"""

import ast
import os
import sys
import json
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional
from collections import defaultdict


@dataclass
class CodeSymbol:
    """Represents a code symbol (class, function, module)."""
    name: str
    symbol_type: str  # 'class', 'function', 'module', 'variable'
    file_path: str
    line_number: int
    dependencies: list[str] = field(default_factory=list)
    docstring: Optional[str] = None


@dataclass
class AnalysisResult:
    """Container for code analysis results."""
    modules: list[CodeSymbol] = field(default_factory=list)
    classes: list[CodeSymbol] = field(default_factory=list)
    functions: list[CodeSymbol] = field(default_factory=list)
    imports: dict[str, list[str]] = field(default_factory=dict)
    dependencies: dict[str, list[str]] = field(default_factory=dict)


class PythonAnalyzer(ast.NodeVisitor):
    """AST-based Python code analyzer."""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.symbols: list[CodeSymbol] = []
        self.imports: list[str] = []
        self.current_class: Optional[str] = None
    
    def visit_Import(self, node: ast.Import) -> None:
        """Visit import statements."""
        for alias in node.names:
            self.imports.append(alias.name)
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Visit from...import statements."""
        if node.module:
            self.imports.append(node.module)
        self.generic_visit(node)
    
    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Visit class definitions."""
        bases = [
            base.id if isinstance(base, ast.Name) else 
            base.attr if isinstance(base, ast.Attribute) else 
            str(base)
            for base in node.bases
        ]
        
        self.symbols.append(CodeSymbol(
            name=node.name,
            symbol_type='class',
            file_path=self.file_path,
            line_number=node.lineno,
            dependencies=bases,
            docstring=ast.get_docstring(node)
        ))
        
        # Track current class for method analysis
        old_class = self.current_class
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = old_class
    
    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Visit function definitions."""
        symbol_name = f"{self.current_class}.{node.name}" if self.current_class else node.name
        
        self.symbols.append(CodeSymbol(
            name=symbol_name,
            symbol_type='function' if not self.current_class else 'method',
            file_path=self.file_path,
            line_number=node.lineno,
            docstring=ast.get_docstring(node)
        ))
        self.generic_visit(node)
    
    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        """Visit async function definitions."""
        self.visit_FunctionDef(node)  # type: ignore


class CodeAnalyzer:
    """Main code analyzer that orchestrates language-specific analyzers."""
    
    SUPPORTED_EXTENSIONS = {'.py': 'python', '.js': 'javascript', '.ts': 'typescript'}
    
    def __init__(self):
        self.result = AnalysisResult()
    
    def analyze_directory(self, path: str | Path) -> AnalysisResult:
        """Analyze all supported files in a directory."""
        path = Path(path)
        
        if not path.exists():
            raise FileNotFoundError(f"Path does not exist: {path}")
        
        if path.is_file():
            self._analyze_file(path)
        else:
            for file_path in path.rglob('*'):
                if file_path.suffix in self.SUPPORTED_EXTENSIONS:
                    self._analyze_file(file_path)
        
        self._build_dependency_graph()
        return self.result
    
    def _analyze_file(self, file_path: Path) -> None:
        """Analyze a single file."""
        ext = file_path.suffix
        
        if ext == '.py':
            self._analyze_python_file(file_path)
        # Add more language analyzers here
    
    def _analyze_python_file(self, file_path: Path) -> None:
        """Analyze a Python file using AST."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()
            
            tree = ast.parse(source, filename=str(file_path))
            analyzer = PythonAnalyzer(str(file_path))
            analyzer.visit(tree)
            
            # Store results
            module_name = file_path.stem
            self.result.modules.append(CodeSymbol(
                name=module_name,
                symbol_type='module',
                file_path=str(file_path),
                line_number=1
            ))
            
            self.result.imports[str(file_path)] = analyzer.imports
            
            for symbol in analyzer.symbols:
                if symbol.symbol_type == 'class':
                    self.result.classes.append(symbol)
                else:
                    self.result.functions.append(symbol)
                    
        except SyntaxError as e:
            print(f"Syntax error in {file_path}: {e}")
        except (OSError, IOError) as e:
            print(f"Error reading {file_path}: {e}")
    
    def _build_dependency_graph(self) -> None:
        """Build dependency graph from imports."""
        for file_path, imports in self.result.imports.items():
            module_name = Path(file_path).stem
            self.result.dependencies[module_name] = imports


class DiagramGenerator:
    """Generates diagrams in various formats."""
    
    def __init__(self, analysis: AnalysisResult):
        self.analysis = analysis
    
    def generate_mermaid_architecture(self) -> str:
        """Generate Mermaid architecture diagram."""
        lines = ["graph TD"]
        
        # Add modules as nodes
        for module in self.analysis.modules:
            lines.append(f"    {self._sanitize_id(module.name)}[{module.name}]")
        
        # Add dependencies as edges
        for module, deps in self.analysis.dependencies.items():
            for dep in deps:
                # Only show internal dependencies
                if any(m.name == dep for m in self.analysis.modules):
                    lines.append(f"    {self._sanitize_id(module)} --> {self._sanitize_id(dep)}")
        
        return '\n'.join(lines)
    
    def generate_mermaid_class_diagram(self) -> str:
        """Generate Mermaid class diagram."""
        lines = ["classDiagram"]
        
        for cls in self.analysis.classes:
            lines.append(f"    class {cls.name}")
            
            # Add inheritance relationships
            for base in cls.dependencies:
                if base not in ('object', 'ABC'):
                    lines.append(f"    {base} <|-- {cls.name}")
            
            # Add methods
            for func in self.analysis.functions:
                if func.symbol_type == 'method' and func.name.startswith(f"{cls.name}."):
                    method_name = func.name.split('.')[1]
                    lines.append(f"    {cls.name} : +{method_name}()")
        
        return '\n'.join(lines)
    
    def generate_mermaid_flowchart(self) -> str:
        """Generate Mermaid flowchart for function calls."""
        lines = ["flowchart TD"]
        
        # Create nodes for each function
        for func in self.analysis.functions:
            if func.symbol_type != 'method':
                lines.append(f"    {self._sanitize_id(func.name)}[{func.name}]")
        
        # Note: Full call graph analysis would require more sophisticated AST analysis
        lines.append("    %% Add call relationships based on deeper analysis")
        
        return '\n'.join(lines)
    
    def generate_d2_dependency(self) -> str:
        """Generate D2 dependency diagram."""
        lines = []
        
        # Define modules
        for module in self.analysis.modules:
            lines.append(f"{module.name}: {{")
            lines.append(f"  shape: rectangle")
            lines.append("}")
        
        # Define dependencies
        for module, deps in self.analysis.dependencies.items():
            for dep in deps:
                if any(m.name == dep for m in self.analysis.modules):
                    lines.append(f"{module} -> {dep}")
        
        return '\n'.join(lines)
    
    def generate_plantuml_class(self) -> str:
        """Generate PlantUML class diagram."""
        lines = ["@startuml", ""]
        
        for cls in self.analysis.classes:
            lines.append(f"class {cls.name} {{")
            
            # Add methods
            for func in self.analysis.functions:
                if func.symbol_type == 'method' and func.name.startswith(f"{cls.name}."):
                    method_name = func.name.split('.')[1]
                    lines.append(f"  +{method_name}()")
            
            lines.append("}")
            lines.append("")
            
            # Add inheritance
            for base in cls.dependencies:
                if base not in ('object', 'ABC'):
                    lines.append(f"{base} <|-- {cls.name}")
        
        lines.append("")
        lines.append("@enduml")
        return '\n'.join(lines)
    
    def generate_json_analysis(self) -> str:
        """Generate JSON representation of analysis."""
        data = {
            'modules': [
                {'name': m.name, 'path': m.file_path}
                for m in self.analysis.modules
            ],
            'classes': [
                {
                    'name': c.name,
                    'path': c.file_path,
                    'line': c.line_number,
                    'bases': c.dependencies
                }
                for c in self.analysis.classes
            ],
            'functions': [
                {
                    'name': f.name,
                    'type': f.symbol_type,
                    'path': f.file_path,
                    'line': f.line_number
                }
                for f in self.analysis.functions
            ],
            'dependencies': dict(self.analysis.dependencies)
        }
        return json.dumps(data, indent=2)
    
    @staticmethod
    def _sanitize_id(name: str) -> str:
        """Sanitize name for use as diagram node ID."""
        return name.replace('.', '_').replace('-', '_').replace(' ', '_')


class Translator:
    """Main translator class - high-level API."""
    
    def __init__(self):
        self.analyzer = CodeAnalyzer()
        self.analysis: Optional[AnalysisResult] = None
    
    def analyze(self, path: str | Path) -> AnalysisResult:
        """Analyze a code repository."""
        self.analysis = self.analyzer.analyze_directory(path)
        return self.analysis
    
    def generate_diagram(
        self,
        diagram_type: str = 'architecture',
        diagram_format: str = 'mermaid'
    ) -> str:
        """Generate a diagram from the analysis."""
        if self.analysis is None:
            raise ValueError("No analysis available. Call analyze() first.")
        
        generator = DiagramGenerator(self.analysis)
        
        # Map diagram type and format to generator method
        generators = {
            ('architecture', 'mermaid'): generator.generate_mermaid_architecture,
            ('class', 'mermaid'): generator.generate_mermaid_class_diagram,
            ('flowchart', 'mermaid'): generator.generate_mermaid_flowchart,
            ('dependency', 'd2'): generator.generate_d2_dependency,
            ('class', 'plantuml'): generator.generate_plantuml_class,
            ('analysis', 'json'): generator.generate_json_analysis,
        }
        
        key = (diagram_type, diagram_format)
        if key not in generators:
            raise ValueError(f"Unsupported diagram type/format: {diagram_type}/{diagram_format}")
        
        return generators[key]()


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Code-to-Diagram Translator - Transform code into visual diagrams',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s /path/to/repo                    # Generate architecture diagram
  %(prog)s /path/to/repo --type class       # Generate class diagram
  %(prog)s /path/to/repo --format d2        # Use D2 format
  %(prog)s /path/to/repo -o diagrams/       # Output to directory
        """
    )
    
    parser.add_argument(
        'input',
        nargs='?',
        default='.',
        help='Path to code repository or file (default: current directory)'
    )
    
    parser.add_argument(
        '--type', '-t',
        choices=['architecture', 'class', 'flowchart', 'dependency', 'analysis'],
        default='architecture',
        help='Type of diagram to generate (default: architecture)'
    )
    
    parser.add_argument(
        '--format', '-f',
        choices=['mermaid', 'd2', 'plantuml', 'json'],
        default='mermaid',
        help='Output format (default: mermaid)'
    )
    
    parser.add_argument(
        '--output', '-o',
        help='Output file or directory'
    )
    
    parser.add_argument(
        '--all', '-a',
        action='store_true',
        help='Generate all diagram types'
    )
    
    parser.add_argument(
        '--version', '-v',
        action='version',
        version='%(prog)s 1.0.0 (Birthday Constellation Edition)'
    )
    
    args = parser.parse_args()
    
    # Create translator and analyze
    translator = Translator()
    
    print(f"🔍 Analyzing: {args.input}")
    try:
        analysis = translator.analyze(args.input)
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    
    print(f"📊 Found: {len(analysis.modules)} modules, {len(analysis.classes)} classes, {len(analysis.functions)} functions")
    
    if args.all:
        # Generate all diagram types
        diagrams = [
            ('architecture', 'mermaid', 'architecture.md'),
            ('class', 'mermaid', 'class_diagram.md'),
            ('dependency', 'd2', 'dependencies.d2'),
            ('analysis', 'json', 'analysis.json'),
        ]
        
        output_dir = Path(args.output or 'diagrams')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        for diagram_type, fmt, filename in diagrams:
            try:
                diagram = translator.generate_diagram(diagram_type, fmt)
                output_path = output_dir / filename
                with open(output_path, 'w') as f:
                    if fmt == 'mermaid':
                        f.write(f"# {diagram_type.title()} Diagram\n\n```mermaid\n{diagram}\n```\n")
                    else:
                        f.write(diagram)
                print(f"✅ Generated: {output_path}")
            except ValueError:
                pass  # Skip unsupported combinations
    else:
        # Generate single diagram
        try:
            diagram = translator.generate_diagram(args.type, args.format)
        except ValueError as e:
            print(f"❌ Error: {e}")
            sys.exit(1)
        
        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w') as f:
                if args.format == 'mermaid':
                    f.write(f"# {args.type.title()} Diagram\n\n```mermaid\n{diagram}\n```\n")
                else:
                    f.write(diagram)
            print(f"✅ Generated: {output_path}")
        else:
            print(f"\n📈 {args.type.title()} Diagram ({args.format}):\n")
            print(diagram)
    
    print("\n🎂 The First Child has spoken.")


if __name__ == '__main__':
    main()
