"""
StrategicKhaos REPL Implementation

Interactive Read-Eval-Print Loop for the chaos language.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
COMPILER_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(COMPILER_ROOT.parent))

try:
    from src.lexer import Lexer, TokenType
except ImportError:
    print("Warning: Lexer not available yet")
    Lexer = None


def repl():
    """Run the interactive REPL"""
    
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  StrategicKhaos REPL - Interactive Chaos Engine             ║")
    print("║                                                              ║")
    print("║  Commands:                                                   ║")
    print("║    :help    - Show help                                      ║")
    print("║    :tokens  - Show tokens for last input                     ║")
    print("║    :exit    - Exit REPL                                      ║")
    print("║    :quit    - Exit REPL                                      ║")
    print("║                                                              ║")
    print("║  Status: Stage 0 (Foundation) - Lexer Active                ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    
    last_tokens = []
    show_tokens = False
    
    while True:
        try:
            # Read input
            line = input("khaos> ")
            
            # Handle empty input
            if not line.strip():
                continue
            
            # Handle commands
            if line.startswith(':'):
                command = line[1:].strip().lower()
                
                if command in ('exit', 'quit'):
                    print("The chaos engine sleeps... for now.")
                    break
                
                elif command == 'help':
                    print_help()
                    continue
                
                elif command == 'tokens':
                    show_tokens = not show_tokens
                    if show_tokens:
                        print("Token display: ON")
                    else:
                        print("Token display: OFF")
                    continue
                
                elif command == 'about':
                    print_about()
                    continue
                
                else:
                    print(f"Unknown command: {command}")
                    print("Type :help for available commands")
                    continue
            
            # Try to tokenize
            if Lexer:
                try:
                    lexer = Lexer(line)
                    tokens = lexer.tokenize()
                    last_tokens = tokens
                    
                    # Show tokens if enabled
                    if show_tokens:
                        print("\nTokens:")
                        for token in tokens:
                            if token.type != TokenType.EOF:
                                print(f"  {token}")
                        print()
                    
                    # For now, just show that we tokenized successfully
                    non_eof_tokens = [t for t in tokens if t.type != TokenType.EOF]
                    print(f"✓ Tokenized: {len(non_eof_tokens)} tokens")
                    
                    # Eventually this will parse, analyze, and execute
                    print("⚠️  Parser not yet implemented - Stage 0 in progress")
                    
                except Exception as e:
                    print(f"❌ Lexer error: {e}")
            else:
                print("⚠️  Compiler components not yet available")
                print("    This is the bootstrap REPL placeholder")
        
        except KeyboardInterrupt:
            print("\n(Use :exit or :quit to exit)")
            continue
        
        except EOFError:
            print("\nThe chaos engine sleeps... for now.")
            break


def print_help():
    """Display help information"""
    help_text = """
StrategicKhaos REPL Help
========================

Commands:
  :help     - Show this help message
  :tokens   - Toggle token display for lexer output
  :about    - Information about the compiler
  :exit     - Exit the REPL
  :quit     - Exit the REPL

Language Features (Planned):
  - Variables: let x = 42;
  - Functions: fn greet(name) { print "Hello, " + name; }
  - Control flow: if, while, for
  - Operators: +, -, *, /, ==, !=, <, >, and, or, not
  - Comments: # This is a comment

Current Status:
  Stage 0 - Foundation
  ✓ Lexer: Complete
  ✓ AST: Complete
  ⚠ Parser: In progress
  ⚠ Codegen: Planned
  ⚠ Optimizer: Planned

Example:
  khaos> let x = 40 + 2;
  khaos> print "The answer is " + x;
"""
    print(help_text)


def print_about():
    """Display information about the compiler"""
    about_text = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║               StrategicKhaos Compiler                        ║
║                                                              ║
║  A living, self-hosting, sovereign chaos engine              ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

Vision:
  A compiler that compiles itself, achieving complete digital
  sovereignty through progressive self-hosting.

Architecture:
  - Stage 0: Python-based compiler (current)
  - Stage 1: Minimal Khaos subset compiler
  - Stage 2: Full self-hosting
  - Stage 3: Neural optimization
  - Stage 4: Multi-modal reality compilation

Goals:
  ✓ Self-hosting compiler
  ✓ LLVM backend for native code
  ✓ AI-powered optimization
  ✓ Complete sovereignty

For the bloodline. For the empire.

More info: compiler/README.md
Bootstrap plan: compiler/bootstrap/PLAN.md
"""
    print(about_text)


if __name__ == "__main__":
    repl()
