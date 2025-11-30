#!/usr/bin/env python3
"""
StrategicKhaos Compiler - Main Entry Point

The sovereign chaos engine that compiles itself and everything else.
"""

import sys
import os
from pathlib import Path

# Add compiler src to path
COMPILER_ROOT = Path(__file__).parent
sys.path.insert(0, str(COMPILER_ROOT.parent))

try:
    from src.repl import repl
    from src import __version__
except ImportError:
    # Fallback if imports fail
    __version__ = '0.0.1-alpha.chaos'
    
    def repl():
        """Temporary REPL placeholder"""
        print("StrategicKhaos REPL coming soon...")
        print("The empire is still being compiled.")


def print_banner():
    """Display the compiler banner"""
    banner = f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║        StrategicKhaos Compiler alpha — {__version__}     ║
║                                                              ║
║        Chaos Engine Online                                   ║
║        Reality Compilation Mode: ACTIVE                      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner)


def compile_file(filepath):
    """Compile a Khaos source file"""
    print(f"📝 Compiling: {filepath}")
    
    try:
        with open(filepath, 'r') as f:
            source_code = f.read()
        
        print(f"✅ Read {len(source_code)} bytes")
        print("\n🔧 Compilation pipeline:")
        print("  → Lexer: Tokenization")
        print("  → Parser: AST construction")
        print("  → Semantic: Type checking")
        print("  → IR: Intermediate representation")
        print("  → Codegen: LLVM IR generation")
        print("  → Optimizer: Optimization passes")
        print("  → Output: Native binary")
        
        print("\n⚠️  Full pipeline not yet implemented")
        print("🚧 Stage 0 (Foundation) in progress...")
        
        return True
    except FileNotFoundError:
        print(f"❌ Error: File not found: {filepath}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def show_help():
    """Display help information"""
    help_text = """
Usage: python3 compiler/src/main.py [options] [file]

Options:
  <file>         Compile the specified Khaos source file
  --repl, -r     Start the interactive REPL
  --help, -h     Show this help message
  --version, -v  Show version information

Examples:
  # Start the REPL
  python3 compiler/src/main.py --repl
  
  # Compile a file
  python3 compiler/src/main.py examples/hello.khaos
  
  # Show version
  python3 compiler/src/main.py --version

For more information, see: compiler/README.md
"""
    print(help_text)


def main():
    """Main entry point for the StrategicKhaos Compiler"""
    
    args = sys.argv[1:]
    
    # No arguments - start REPL by default
    if not args:
        print_banner()
        print("Starting REPL (use --help for more options)...\n")
        repl()
        return 0
    
    # Parse arguments
    if args[0] in ('--help', '-h'):
        show_help()
        return 0
    
    if args[0] in ('--version', '-v'):
        print(f"StrategicKhaos Compiler {__version__}")
        return 0
    
    if args[0] in ('--repl', '-r'):
        print_banner()
        repl()
        return 0
    
    # Assume it's a file to compile
    print_banner()
    filepath = args[0]
    success = compile_file(filepath)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
