"""
Tests for the StrategicKhaos parser.
"""

import pytest
from src.lexer import Lexer
from src.parser import Parser
from src.ast import NumberNode, StringNode, SymbolNode, ListNode


def test_parser_number():
    """Test parsing a number literal."""
    source = "42"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    expressions = parser.parse()
    
    assert len(expressions) == 1
    assert isinstance(expressions[0], NumberNode)
    assert expressions[0].value == 42


def test_parser_string():
    """Test parsing a string literal."""
    source = '"Hello"'
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    expressions = parser.parse()
    
    assert len(expressions) == 1
    assert isinstance(expressions[0], StringNode)
    assert expressions[0].value == "Hello"


def test_parser_symbol():
    """Test parsing a symbol."""
    source = "print"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    expressions = parser.parse()
    
    assert len(expressions) == 1
    assert isinstance(expressions[0], SymbolNode)
    assert expressions[0].name == "print"


def test_parser_simple_list():
    """Test parsing a simple list."""
    source = "(print 42)"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    expressions = parser.parse()
    
    assert len(expressions) == 1
    assert isinstance(expressions[0], ListNode)
    assert len(expressions[0].elements) == 2
    assert isinstance(expressions[0].elements[0], SymbolNode)
    assert expressions[0].elements[0].name == "print"
    assert isinstance(expressions[0].elements[1], NumberNode)
    assert expressions[0].elements[1].value == 42


def test_parser_nested_list():
    """Test parsing nested lists."""
    source = "(+ (* 2 3) 4)"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    expressions = parser.parse()
    
    assert len(expressions) == 1
    outer_list = expressions[0]
    assert isinstance(outer_list, ListNode)
    assert len(outer_list.elements) == 3
    
    # Check the nested list
    inner_list = outer_list.elements[1]
    assert isinstance(inner_list, ListNode)
    assert len(inner_list.elements) == 3
