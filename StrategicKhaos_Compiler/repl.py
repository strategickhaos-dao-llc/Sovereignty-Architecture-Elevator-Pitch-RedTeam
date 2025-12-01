#!/usr/bin/env python3
"""
StrategicKhaos Compiler REPL (Stage 0)
Read-Eval-Print Loop for tokenization and lexical analysis

Usage:
    python repl.py                  # Interactive mode
    python repl.py examples/hello.khaos  # Run a file
"""

import sys
import os
from src.lexer import Lexer
from src.token import TokenType

def run_file(filepath):
    """Run a .khaos file through the lexer"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
        run(source, filepath)
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

def run(source, filename="<stdin>"):
    """Tokenize and display source code"""
    lexer = Lexer(source)
    tokens = lexer.scan_tokens()
    
    # Display any errors
    if lexer.errors:
        print(f"\n=== Lexer Errors in {filename} ===\n")
        for error in lexer.errors:
            print(f"  {error}")
        print()
    
    print(f"\n=== Tokenization Results for {filename} ===\n")
    print(f"{'Line':<6} {'Type':<20} {'Lexeme':<20} {'Literal':<20}")
    print("-" * 70)
    
    for token in tokens:
        type_name = token.type.name
        lexeme = repr(token.lexeme) if token.lexeme else '""'
        literal = repr(token.literal) if token.literal is not None else ''
        print(f"{token.line:<6} {type_name:<20} {lexeme:<20} {literal:<20}")
    
    print(f"\nTotal tokens: {len(tokens)}")

def run_repl():
    """Interactive REPL mode"""
    print("╔═══════════════════════════════════════════════════════════════╗")
    print("║   StrategicKhaos Compiler REPL - Stage 0: Grammar Bootstrap   ║")
    print("║                                                               ║")
    print("║   The empire has a heartbeat. Now it speaks.                 ║")
    print("╚═══════════════════════════════════════════════════════════════╝")
    print("\nCommands:")
    print("  :quit or :q    - Exit REPL")
    print("  :file <path>   - Load and tokenize a file")
    print("  :help          - Show this help")
    print("\nEnter StrategicKhaos code to tokenize (end with empty line):\n")
    
    line_buffer = []
    
    while True:
        try:
            if not line_buffer:
                prompt = "khaos> "
            else:
                prompt = "    ... "
            
            line = input(prompt)
            
            # Handle commands
            if line.startswith(':'):
                cmd = line.split()
                if cmd[0] in [':quit', ':q']:
                    print("\n≫ The empire sleeps. Until next time... ≫")
                    break
                elif cmd[0] == ':help':
                    print("\nCommands:")
                    print("  :quit or :q    - Exit REPL")
                    print("  :file <path>   - Load and tokenize a file")
                    print("  :help          - Show this help")
                    print()
                    continue
                elif cmd[0] == ':file':
                    if len(cmd) < 2:
                        print("Usage: :file <path>")
                    else:
                        run_file(cmd[1])
                    continue
                else:
                    print(f"Unknown command: {cmd[0]}")
                    continue
            
            # Empty line processes the buffer
            if line == "" and line_buffer:
                source = '\n'.join(line_buffer)
                run(source)
                line_buffer = []
            elif line:
                line_buffer.append(line)
                
        except EOFError:
            print("\n\n≫ The empire sleeps. Until next time... ≫")
            break
        except KeyboardInterrupt:
            print("\n\n≫ Interrupted. The empire sleeps. ≫")
            break

def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        # File mode
        run_file(sys.argv[1])
    else:
        # REPL mode
        run_repl()

if __name__ == "__main__":
    main()
