from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.interpreter import Interpreter

def repl():
    interpreter = Interpreter()
    print("StrategicKhaos α — chaos engine online")
    print("Type 'exit()' or Ctrl+C to quit\n")

    while True:
        try:
            source = input("khaos> ")
            if source.strip() in ["exit()", "quit()"]:
                print("Chaos engine shutting down. Bloodline preserved.")
                break

            lexer = Lexer(source)
            tokens = lexer.scan_tokens()

            parser = Parser(tokens)
            stmts = parser.parse()

            if stmts:
                interpreter.interpret(stmts)

        except Exception as e:
            print(f"Chaos error: {e}")
