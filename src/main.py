#!/usr/bin/env python3
# src/main.py

import sys
from src.repl import repl
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.interpreter import Interpreter


def run_file(path):
    """Run a .khaos file"""
    with open(path, 'r', encoding='utf-8') as f:
        source = f.read()
    
    try:
        lexer = Lexer(source)
        tokens = lexer.scan_tokens()
        
        parser = Parser(tokens)
        stmts = parser.parse()
        
        interpreter = Interpreter()
        interpreter.interpret(stmts)
    except Exception as e:
        print(f"Chaos error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    if len(sys.argv) > 1:
        # Run file mode
        run_file(sys.argv[1])
    else:
        # REPL mode
        repl()


if __name__ == "__main__":
    main()
