#!/usr/bin/env python3
"""
Quick demo script to show the StrategicKhaos Compiler in action
"""

import sys
from pathlib import Path

# Add compiler src to path
COMPILER_ROOT = Path(__file__).parent / "src"
sys.path.insert(0, str(COMPILER_ROOT.parent))

from src.lexer import Lexer, TokenType
from src import __version__

def demo_lexer():
    """Demonstrate the lexer with various code examples"""
    
    print("=" * 70)
    print("  StrategicKhaos Compiler Demo")
    print(f"  Version: {__version__}")
    print("=" * 70)
    print()
    
    examples = [
        ("Variable Declaration", "let x = 42;"),
        ("Function Definition", "fn greet(name) { print name; }"),
        ("Conditional", "if x > 10 { print \"big\"; }"),
        ("Arithmetic", "let result = (10 + 20) * 3 - 5;"),
        ("Boolean Logic", "let flag = true and not false;"),
        ("String", 'print "Hello, Empire!";'),
    ]
    
    for title, code in examples:
        print(f"📌 {title}")
        print(f"   Code: {code}")
        
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        # Filter out EOF for cleaner display
        tokens_display = [t for t in tokens if t.type != TokenType.EOF]
        
        print(f"   Tokens ({len(tokens_display)}):")
        for token in tokens_display:
            print(f"      • {token.type.name:15} → {repr(token.value)}")
        print()
    
    print("=" * 70)
    print("✅ Lexer Demo Complete!")
    print("=" * 70)
    print()
    print("Next Steps:")
    print("  • Run REPL: python3 compiler/src/main.py")
    print("  • Compile: python3 compiler/src/main.py compiler/examples/hello.khaos")
    print("  • Test: python3 compiler/tests/test_lexer.py")
    print("  • Read: compiler/README.md")
    print()


if __name__ == "__main__":
    demo_lexer()
