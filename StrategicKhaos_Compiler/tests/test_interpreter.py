"""
Tests for the StrategicKhaos interpreter.
"""

import pytest
from src.lexer import Lexer
from src.parser import Parser
from src.vm import Interpreter


def eval_code(source: str):
    """Helper to evaluate StrategicKhaos code."""
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    expressions = parser.parse()
    interpreter = Interpreter()
    return interpreter.run(expressions)


def test_interpreter_number():
    """Test evaluating a number literal."""
    result = eval_code("42")
    assert result == 42


def test_interpreter_string():
    """Test evaluating a string literal."""
    result = eval_code('"Hello"')
    assert result == "Hello"


def test_interpreter_addition():
    """Test addition."""
    result = eval_code("(+ 2 3)")
    assert result == 5


def test_interpreter_subtraction():
    """Test subtraction."""
    result = eval_code("(- 5 3)")
    assert result == 2


def test_interpreter_multiplication():
    """Test multiplication."""
    result = eval_code("(* 6 7)")
    assert result == 42


def test_interpreter_division():
    """Test division."""
    result = eval_code("(/ 10 2)")
    assert result == 5


def test_interpreter_nested_arithmetic():
    """Test nested arithmetic expressions."""
    result = eval_code("(+ (* 2 3) 4)")
    assert result == 10


def test_interpreter_multiple_args():
    """Test functions with multiple arguments."""
    result = eval_code("(+ 1 2 3 4)")
    assert result == 10


def test_interpreter_print(capsys):
    """Test print function."""
    eval_code('(print "Hello, World!")')
    captured = capsys.readouterr()
    assert "Hello, World!" in captured.out


def test_interpreter_print_number(capsys):
    """Test printing a number."""
    eval_code('(print 42)')
    captured = capsys.readouterr()
    assert "42" in captured.out
