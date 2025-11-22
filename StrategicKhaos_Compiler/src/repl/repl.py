"""
REPL (Read-Eval-Print Loop) implementation for StrategicKhaos.
"""

import sys
from ..lexer import Lexer, TokenType
from ..parser import Parser, ParserError
from ..vm import Interpreter, InterpreterError
from .. import get_version


def repl():
    """
    Start the StrategicKhaos REPL.
    
    Provides an interactive environment for evaluating StrategicKhaos expressions.
    """
    interpreter = Interpreter()
    
    print(f"StrategicKhaos REPL v{get_version()}")
    print("Welcome to the chaos realm. Type expressions to evaluate them.")
    print("Type 'exit' or press Ctrl+D to quit.")
    print()
    
    while True:
        try:
            # Read input
            try:
                line = input("> ")
            except EOFError:
                print("\nGoodbye from the chaos realm!")
                break
            
            # Check for exit command
            if line.strip().lower() in ['exit', 'quit']:
                print("Goodbye from the chaos realm!")
                break
            
            # Skip empty lines
            if not line.strip():
                continue
            
            # Lex, parse, and evaluate
            try:
                # Tokenize
                lexer = Lexer(line)
                tokens = lexer.tokenize()
                
                # Filter out EOF token for inspection
                non_eof_tokens = [t for t in tokens if t.type != TokenType.EOF]
                
                if not non_eof_tokens:
                    continue
                
                # Parse
                parser = Parser(tokens)
                expressions = parser.parse()
                
                # Evaluate each expression
                for expr in expressions:
                    result = interpreter.eval(expr)
                    
                    # Print result if not None
                    if result is not None:
                        print(result)
            
            except (ParserError, InterpreterError) as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")
        
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt")
            continue


def run_file(filename: str):
    """
    Execute a StrategicKhaos source file.
    
    Args:
        filename: Path to the source file
    """
    try:
        # Read the file
        with open(filename, 'r') as f:
            source = f.read()
        
        # Lex
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        # Parse
        parser = Parser(tokens)
        expressions = parser.parse()
        
        # Execute
        interpreter = Interpreter()
        interpreter.run(expressions)
    
    except FileNotFoundError:
        print(f"Error: File not found: {filename}")
        sys.exit(1)
    except (ParserError, InterpreterError) as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)
