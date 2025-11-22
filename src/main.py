#!/usr/bin/env python3
"""
StrategicKhaos Compiler - Stage 0
Main entry point for the compiler
"""

import sys
import argparse
from pathlib import Path

# Add src to path to allow imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.khaos_compiler.lexer import Lexer
from src.khaos_compiler.parser import Parser
from src.khaos_compiler.interpreter import Interpreter
from src.khaos_compiler.codegen import PythonCodeGenerator


def compile_file(input_path: str, output_path: str = None):
    """Compile a StrategicKhaos file to Python"""
    
    # Read source file
    with open(input_path, 'r') as f:
        source = f.read()
    
    # Lex
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    # Parse
    parser = Parser(tokens)
    ast = parser.parse()
    
    # Generate Python code
    codegen = PythonCodeGenerator()
    python_code = codegen.generate(ast)
    
    # Output
    if output_path:
        with open(output_path, 'w') as f:
            f.write(python_code)
        print(f"Compiled {input_path} -> {output_path}")
    else:
        print(python_code)
    
    return python_code


def interpret_file(input_path: str):
    """Interpret and execute a StrategicKhaos file"""
    
    # Read source file
    with open(input_path, 'r') as f:
        source = f.read()
    
    # Lex
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    # Parse
    parser = Parser(tokens)
    ast = parser.parse()
    
    # Interpret
    interpreter = Interpreter()
    interpreter.interpret(ast)
    
    return interpreter


def main():
    parser = argparse.ArgumentParser(
        description='StrategicKhaos Compiler - Stage 0',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m src.main --compile examples/bootstrap_codegen.khaos
  python -m src.main --run examples/bootstrap_codegen.khaos
  python -m src.main --compile input.khaos -o output.py
        """
    )
    
    parser.add_argument('input', help='Input .khaos file')
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--compile', action='store_true',
                      help='Compile to Python code')
    group.add_argument('--run', action='store_true',
                      help='Interpret and execute')
    
    parser.add_argument('-o', '--output',
                       help='Output file (for --compile)')
    
    args = parser.parse_args()
    
    try:
        if args.compile:
            compile_file(args.input, args.output)
        elif args.run:
            interpret_file(args.input)
    except FileNotFoundError as e:
        print(f"Error: File not found: {e}", file=sys.stderr)
        sys.exit(1)
    except (SyntaxError, RuntimeError, NameError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
