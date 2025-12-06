#!/usr/bin/env python3
"""
Swarm DNA CLI - Master Tool for Swarm DNA Operations

A unified command-line interface for all Swarm DNA tools:
- Parse GGUF model blobs
- Reconstruct model lineage
- Compile lore to configs
- Generate IDE projects

This is the gateway to Dom's unified cognitive architecture.

Built for Strategickhaos Swarm Intelligence
"""

import sys
import argparse
from pathlib import Path


def print_banner():
    """Print the Swarm DNA banner"""
    banner = """
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║              🧬 SWARM DNA ARCHITECTURE TOOLKIT 🧬                ║
║                                                                   ║
║           Child of the Black Hole - Version 12.0                 ║
║           Strategickhaos Swarm Intelligence                       ║
║                                                                   ║
║   "Everything belongs in a graph of relationships"               ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
    """
    print(banner)


def cmd_parse_blobs(args):
    """Parse model blobs and extract metadata"""
    # Note: Using direct imports (not relative) because this is designed to run as a standalone script
    from gguf_parser import parse_blob_directory
    import yaml
    
    print(f"🔍 Parsing blobs in: {args.blob_dir}")
    result = parse_blob_directory(args.blob_dir)
    
    if args.output:
        with open(args.output, 'w') as f:
            yaml.dump(result, f, default_flow_style=False, sort_keys=False)
        print(f"✅ Metadata saved to: {args.output}")
    else:
        print(yaml.dump(result, default_flow_style=False, sort_keys=False))
        

def cmd_lineage(args):
    """Reconstruct model lineage"""
    from model_lineage import ModelLineage
    import yaml
    
    print(f"🧬 Building lineage from: {args.metadata_file}")
    lineage = ModelLineage(args.metadata_file)
    report = lineage.generate_lineage_report()
    
    if args.output:
        with open(args.output, 'w') as f:
            yaml.dump(report, f, default_flow_style=False, sort_keys=False)
        print(f"✅ Lineage report saved to: {args.output}")
        
    if args.dot:
        dot_graph = lineage.generate_dot_graph()
        with open(args.dot, 'w') as f:
            f.write(dot_graph)
        print(f"📊 DOT graph saved to: {args.dot}")
        print(f"    Generate PNG: dot -Tpng {args.dot} -o lineage.png")
        
    if not args.output and not args.dot:
        print(yaml.dump(report, default_flow_style=False, sort_keys=False))


def cmd_compile(args):
    """Compile Swarm DNA to operational configs"""
    from swarm_dna_compiler import SwarmDNACompiler
    
    print(f"🧬 Compiling Swarm DNA: {args.swarm_dna}")
    compiler = SwarmDNACompiler(args.swarm_dna)
    results = compiler.compile_all(args.output_dir)
    
    print("\n✅ Compilation complete!")
    print("\nGenerated configurations:")
    for config_type, path in results.items():
        print(f"  • {config_type:20s} → {path}")


def cmd_make_project(args):
    """Generate IDE project for blob directory"""
    from blob_project_generator import BlobProjectGenerator
    
    print(f"🏗️  Generating IDE project for: {args.blob_dir}")
    generator = BlobProjectGenerator(args.blob_dir, args.name)
    results = generator.generate_all()
    
    print("\n✅ Project generation complete!")
    print("\nGenerated files:")
    for path in results:
        print(f"  • {path}")


def cmd_full_pipeline(args):
    """Run the full Swarm DNA pipeline"""
    print("🚀 Running full Swarm DNA pipeline...")
    print()
    
    # Step 1: Parse blobs
    print("Step 1/4: Parsing model blobs...")
    from gguf_parser import parse_blob_directory
    import yaml
    
    metadata_file = Path(args.output_dir) / 'model_metadata.yaml'
    result = parse_blob_directory(args.blob_dir)
    
    Path(args.output_dir).mkdir(exist_ok=True)
    with open(metadata_file, 'w') as f:
        yaml.dump(result, f, default_flow_style=False, sort_keys=False)
    print(f"   ✅ Metadata: {metadata_file}")
    
    # Step 2: Build lineage
    print("\nStep 2/4: Reconstructing model lineage...")
    from model_lineage import ModelLineage
    
    lineage_file = Path(args.output_dir) / 'lineage.yaml'
    dot_file = Path(args.output_dir) / 'lineage.dot'
    
    lineage = ModelLineage(str(metadata_file))
    report = lineage.generate_lineage_report()
    
    with open(lineage_file, 'w') as f:
        yaml.dump(report, f, default_flow_style=False, sort_keys=False)
    print(f"   ✅ Lineage: {lineage_file}")
    
    dot_graph = lineage.generate_dot_graph()
    with open(dot_file, 'w') as f:
        f.write(dot_graph)
    print(f"   ✅ Graph: {dot_file}")
    
    # Step 3: Compile Swarm DNA
    if args.swarm_dna:
        print("\nStep 3/4: Compiling Swarm DNA...")
        from swarm_dna_compiler import SwarmDNACompiler
        
        compiler = SwarmDNACompiler(args.swarm_dna)
        configs = compiler.compile_all(args.output_dir)
        print(f"   ✅ Configs: {len(configs)} files generated")
    else:
        print("\nStep 3/4: Skipped (no SWARM_DNA.yaml specified)")
    
    # Step 4: Generate IDE project
    print("\nStep 4/4: Generating IDE project...")
    from blob_project_generator import BlobProjectGenerator
    
    generator = BlobProjectGenerator(args.blob_dir)
    results = generator.generate_all()
    print(f"   ✅ IDE project: {len(results)} files generated")
    
    print("\n" + "="*60)
    print("🎉 Full pipeline complete!")
    print(f"📦 All outputs in: {args.output_dir}")
    print()
    print("Next steps:")
    print("  1. Open blob directory in your IDE")
    print("  2. View model_metadata.yaml and lineage.yaml")
    print("  3. Generate visualization: dot -Tpng lineage.dot -o lineage.png")
    print()
    print("🔥 Lore → Reality transformation complete.")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Swarm DNA Architecture Toolkit',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Parse model blobs
  swarm-cli parse ~/.ollama/models/blob/ -o metadata.yaml
  
  # Build lineage graph
  swarm-cli lineage metadata.yaml -o lineage.yaml --dot lineage.dot
  
  # Compile Swarm DNA to configs
  swarm-cli compile SWARM_DNA.yaml -o compiled/
  
  # Generate IDE project
  swarm-cli make-project ~/.ollama/models/blob/ --name "My Models"
  
  # Run full pipeline
  swarm-cli full-pipeline ~/.ollama/models/blob/ --swarm-dna SWARM_DNA.yaml

Built with 🔥 by Strategickhaos Swarm Intelligence
        """
    )
    
    parser.add_argument('--version', action='version', version='Swarm DNA v12.0')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Parse blobs command
    parse_parser = subparsers.add_parser('parse', help='Parse model blobs')
    parse_parser.add_argument('blob_dir', help='Directory containing model blobs')
    parse_parser.add_argument('-o', '--output', help='Output YAML file')
    
    # Lineage command
    lineage_parser = subparsers.add_parser('lineage', help='Reconstruct model lineage')
    lineage_parser.add_argument('metadata_file', help='Model metadata YAML file')
    lineage_parser.add_argument('-o', '--output', help='Output lineage YAML file')
    lineage_parser.add_argument('--dot', help='Output DOT graph file')
    
    # Compile command
    compile_parser = subparsers.add_parser('compile', help='Compile Swarm DNA to configs')
    compile_parser.add_argument('swarm_dna', help='SWARM_DNA.yaml file')
    compile_parser.add_argument('-o', '--output-dir', default='compiled', 
                               help='Output directory')
    
    # Make project command
    project_parser = subparsers.add_parser('make-project', 
                                           help='Generate IDE project')
    project_parser.add_argument('blob_dir', help='Blob directory')
    project_parser.add_argument('--name', default='Swarm Models',
                               help='Project name')
    
    # Full pipeline command
    pipeline_parser = subparsers.add_parser('full-pipeline',
                                           help='Run complete pipeline')
    pipeline_parser.add_argument('blob_dir', help='Blob directory')
    pipeline_parser.add_argument('--swarm-dna', help='SWARM_DNA.yaml file')
    pipeline_parser.add_argument('-o', '--output-dir', default='swarm-output',
                                help='Output directory')
    
    args = parser.parse_args()
    
    if not args.command:
        print_banner()
        parser.print_help()
        return
        
    # Execute command
    print_banner()
    
    if args.command == 'parse':
        cmd_parse_blobs(args)
    elif args.command == 'lineage':
        cmd_lineage(args)
    elif args.command == 'compile':
        cmd_compile(args)
    elif args.command == 'make-project':
        cmd_make_project(args)
    elif args.command == 'full-pipeline':
        cmd_full_pipeline(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
