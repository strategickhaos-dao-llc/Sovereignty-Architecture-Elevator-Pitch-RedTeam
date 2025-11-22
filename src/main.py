#!/usr/bin/env python3
import sys
import pathlib
from src.repl import repl
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.codegen.python import PythonCodegen


def compile_file(path):
    source = pathlib.Path(path).read_text()
    lexer = Lexer(source)
    tokens = lexer.scan_tokens()
    parser = Parser(tokens)
    stmts = parser.parse()

    codegen = PythonCodegen()
    python_code = codegen.generate(stmts)

    out_path = path.replace(".khaos", ".py")
    pathlib.Path(out_path).write_text(python_code)
    print(f"Transpiled → {out_path}")
    print("\n--- Generated Python ---")
    print(python_code)
    print("\n--- Executing ---")
    exec(python_code)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--compile":
        compile_file(sys.argv[2])
    else:
        print("StrategicKhaos α — chaos engine online")
        repl()
