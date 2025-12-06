#!/usr/bin/env python3
"""
FlameLang CLI
Command-line interface for FlameLang compiler and interpreter
"""

import sys
import argparse
from pathlib import Path
from typing import Optional

from .core.lexer import Lexer
from .core.parser import Parser
from .core.interpreter import Interpreter
from .repl import REPL


def compile_file(filepath: str, verbose: bool = False) -> int:
    """
    Compile and execute a FlameLang file
    
    Args:
        filepath: Path to .fl file
        verbose: Print verbose output
        
    Returns:
        Exit code
    """
    try:
        # Read source file
        path = Path(filepath)
        if not path.exists():
            print(f"Error: File '{filepath}' not found", file=sys.stderr)
            return 1
        
        if path.suffix not in ['.fl', '.flame']:
            print(f"Warning: Expected .fl or .flame extension", file=sys.stderr)
        
        source = path.read_text()
        
        if verbose:
            print(f"🔥 Compiling: {filepath}")
            print(f"Source length: {len(source)} characters")
        
        # Lexical analysis
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        if verbose:
            print(f"Tokens generated: {len(tokens)}")
            print("Token stream:")
            for token in tokens[:10]:  # Show first 10 tokens
                print(f"  {token}")
            if len(tokens) > 10:
                print(f"  ... and {len(tokens) - 10} more")
        
        # Syntax analysis
        parser = Parser(tokens)
        ast = parser.parse()
        
        if verbose:
            print(f"AST generated with {len(ast.statements)} statements")
        
        # Execution
        interpreter = Interpreter()
        result = interpreter.interpret(ast)
        
        if verbose:
            print(f"Execution completed")
            if result is not None:
                print(f"Result: {result}")
        
        return 0
        
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except SyntaxError as e:
        print(f"Syntax Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Runtime Error: {e}", file=sys.stderr)
        if verbose:
            import traceback
            traceback.print_exc()
        return 1


def run_repl():
    """Run interactive REPL"""
    repl = REPL()
    repl.run()
    return 0


def show_version():
    """Show version information"""
    from . import __version__
    print(f"🔥 FlameLang v{__version__}")
    print("Sovereign Computing Platform")
    print("Copyright © 2025 Strategickhaos DAO LLC")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        prog='flamelang',
        description='🔥 FlameLang - Sovereign Computing Platform',
        epilog='Examples:\n'
               '  flamelang repl              # Start interactive REPL\n'
               '  flamelang compile script.fl # Compile and run a file\n'
               '  flamelang --version         # Show version\n',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--version', '-v',
        action='store_true',
        help='Show version information'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # REPL command
    repl_parser = subparsers.add_parser('repl', help='Start interactive REPL')
    
    # Compile command
    compile_parser = subparsers.add_parser('compile', help='Compile and execute a file')
    compile_parser.add_argument('file', help='FlameLang source file (.fl)')
    
    # Run command (alias for compile)
    run_parser = subparsers.add_parser('run', help='Run a FlameLang file (alias for compile)')
    run_parser.add_argument('file', help='FlameLang source file (.fl)')
    
    args = parser.parse_args()
    
    # Show version
    if args.version:
        show_version()
        return 0
    
    # No command - show help
    if not args.command:
        parser.print_help()
        return 0
    
    # Execute command
    if args.command == 'repl':
        return run_repl()
    
    elif args.command in ['compile', 'run']:
        return compile_file(args.file, verbose=args.verbose)
    
    else:
        parser.print_help()
        return 1


if __name__ == '__main__':
    sys.exit(main())
