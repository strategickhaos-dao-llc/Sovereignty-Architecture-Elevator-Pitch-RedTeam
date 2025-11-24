#!/usr/bin/env python3
"""
Model Lineage Reconstructor for Swarm DNA Architecture

Analyzes model metadata and reconstructs their ancestry, relationships,
and dependency trees. This enables Dom's "unification instinct" - seeing
everything as a graph of relationships.

Built for Strategickhaos Swarm Intelligence
"""

import os
import sys
import yaml
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
from datetime import datetime
from collections import defaultdict


class ModelLineage:
    """Reconstruct and analyze model lineage and relationships"""
    
    def __init__(self, metadata_file: Optional[str] = None):
        self.models = []
        self.lineage_graph = defaultdict(list)
        self.families = defaultdict(list)
        
        if metadata_file:
            self.load_metadata(metadata_file)
            
    def load_metadata(self, metadata_file: str):
        """Load model metadata from YAML file"""
        with open(metadata_file, 'r') as f:
            data = yaml.safe_load(f)
            
        if 'models' in data:
            self.models = data['models']
        else:
            self.models = [data]
            
    def extract_model_info(self, model: Dict) -> Dict[str, Any]:
        """Extract key information from model metadata"""
        info = {
            'name': model.get('file_info', {}).get('name', 'unknown'),
            'size_bytes': model.get('file_info', {}).get('size_bytes', 0),
            'modified': model.get('file_info', {}).get('modified', ''),
        }
        
        # Extract model-specific metadata
        metadata = model.get('metadata', {})
        
        # Common GGUF metadata fields
        info['architecture'] = metadata.get('general.architecture', 'unknown')
        info['model_name'] = metadata.get('general.name', info['name'])
        info['base_model'] = metadata.get('general.base_model', None)
        info['quantization'] = metadata.get('general.quantization_version', None)
        info['file_type'] = metadata.get('general.file_type', None)
        
        # Extract family/lineage hints from name
        info['family'] = self._extract_family(info['model_name'])
        info['version'] = self._extract_version(info['model_name'])
        
        return info
        
    def _extract_family(self, name: str) -> str:
        """Extract model family from name (e.g., llama, mistral, qwen)"""
        name_lower = name.lower()
        
        families = [
            'llama', 'mistral', 'qwen', 'phi', 'gemma', 'falcon',
            'mpt', 'gpt', 'opt', 'bloom', 'stablelm', 'vicuna',
            'alpaca', 'wizardlm', 'orca', 'codellama'
        ]
        
        for family in families:
            if family in name_lower:
                return family
                
        return 'unknown'
        
    def _extract_version(self, name: str) -> Optional[str]:
        """Extract version from model name"""
        import re
        
        # Look for version patterns like v1, v2.0, 3.5, etc.
        patterns = [
            r'v(\d+\.?\d*)',  # v1, v2.0
            r'-(\d+\.?\d*)',  # -3.5
            r':(\d+\.?\d*)',  # :7b
        ]
        
        for pattern in patterns:
            match = re.search(pattern, name)
            if match:
                return match.group(1)
                
        return None
        
    def build_lineage_graph(self) -> Dict[str, Any]:
        """Build a lineage graph showing model relationships"""
        graph = {
            'families': defaultdict(list),
            'lineage': [],
            'quantization_variants': defaultdict(list),
        }
        
        for model in self.models:
            info = self.extract_model_info(model)
            
            # Group by family
            graph['families'][info['family']].append(info)
            
            # Track base model relationships
            if info['base_model']:
                graph['lineage'].append({
                    'model': info['model_name'],
                    'base': info['base_model'],
                    'relationship': 'derived_from',
                })
                
            # Group quantization variants
            if info['quantization']:
                base_name = info['model_name'].split('-q')[0]  # Remove quantization suffix
                graph['quantization_variants'][base_name].append({
                    'name': info['model_name'],
                    'quantization': info['quantization'],
                    'size': info['size_bytes'],
                })
                
        # Convert defaultdicts to regular dicts for YAML serialization
        return {
            'families': dict(graph['families']),
            'lineage': graph['lineage'],
            'quantization_variants': dict(graph['quantization_variants']),
        }
        
    def generate_lineage_report(self) -> Dict[str, Any]:
        """Generate a comprehensive lineage report"""
        graph = self.build_lineage_graph()
        
        # Statistics
        stats = {
            'total_models': len(self.models),
            'families_count': len(graph['families']),
            'families': list(graph['families'].keys()),
            'largest_family': max(
                graph['families'].items(),
                key=lambda x: len(x[1]),
                default=('none', [])
            )[0] if graph['families'] else 'none',
        }
        
        # Calculate total storage
        total_size = sum(
            model.get('file_info', {}).get('size_bytes', 0)
            for model in self.models
        )
        stats['total_size_gb'] = round(total_size / (1024**3), 2)
        
        return {
            'swarm_dna_component': 'model_lineage_graph',
            'generated': datetime.now().isoformat(),
            'statistics': stats,
            'lineage_graph': graph,
            'philosophical_note': (
                "Everything belongs in a graph of relationships. "
                "This is Dom's unification instinct made manifest."
            ),
        }
        
    def generate_dot_graph(self) -> str:
        """Generate GraphViz DOT format for visualization"""
        graph = self.build_lineage_graph()
        
        dot = ['digraph ModelLineage {']
        dot.append('  rankdir=LR;')
        dot.append('  node [shape=box, style=rounded];')
        dot.append('')
        
        # Group by families with subgraphs
        for family, models in graph['families'].items():
            dot.append(f'  subgraph cluster_{family} {{')
            dot.append(f'    label="{family.title()} Family";')
            dot.append('    style=filled;')
            dot.append('    color=lightgrey;')
            
            for model in models:
                node_id = model['model_name'].replace('-', '_').replace('.', '_')
                label = f"{model['model_name']}\\n{round(model['size_bytes']/(1024**3), 1)}GB"
                dot.append(f'    {node_id} [label="{label}"];')
                
            dot.append('  }')
            dot.append('')
            
        # Add lineage edges
        for lineage in graph['lineage']:
            src = lineage['base'].replace('-', '_').replace('.', '_')
            dst = lineage['model'].replace('-', '_').replace('.', '_')
            dot.append(f'  {src} -> {dst} [label="derived"];')
            
        dot.append('}')
        return '\n'.join(dot)


def main():
    """CLI interface for model lineage reconstruction"""
    if len(sys.argv) < 2:
        print("Usage: model_lineage.py <metadata.yaml> [output.yaml] [--dot graph.dot]")
        print()
        print("Examples:")
        print("  model_lineage.py model_metadata.yaml")
        print("  model_lineage.py model_metadata.yaml lineage.yaml")
        print("  model_lineage.py model_metadata.yaml lineage.yaml --dot lineage.dot")
        sys.exit(1)
        
    metadata_file = sys.argv[1]
    output_file = None
    dot_file = None
    
    # Parse arguments
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == '--dot' and i + 1 < len(sys.argv):
            dot_file = sys.argv[i + 1]
            i += 2
        else:
            output_file = sys.argv[i]
            i += 1
            
    print(f"🧬 Reconstructing model lineage from: {metadata_file}")
    
    lineage = ModelLineage(metadata_file)
    report = lineage.generate_lineage_report()
    
    stats = report['statistics']
    print(f"📊 Found {stats['total_models']} models across {stats['families_count']} families")
    print(f"💾 Total storage: {stats['total_size_gb']} GB")
    print(f"🏆 Largest family: {stats['largest_family']}")
    
    if output_file:
        with open(output_file, 'w') as f:
            yaml.dump(report, f, default_flow_style=False, sort_keys=False)
        print(f"✅ Lineage report written to: {output_file}")
        
    if dot_file:
        dot_graph = lineage.generate_dot_graph()
        with open(dot_file, 'w') as f:
            f.write(dot_graph)
        print(f"📊 DOT graph written to: {dot_file}")
        print(f"    Generate visualization: dot -Tpng {dot_file} -o lineage.png")
        
    if not output_file and not dot_file:
        print("\n" + "="*60)
        print(yaml.dump(report, default_flow_style=False, sort_keys=False))


if __name__ == '__main__':
    main()
