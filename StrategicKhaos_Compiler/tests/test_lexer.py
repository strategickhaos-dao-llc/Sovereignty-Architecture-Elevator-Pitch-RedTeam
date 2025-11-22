"""
Tests for the StrategicKhaos lexer.
"""

import pytest
from src.lexer import Lexer, TokenType


def test_lexer_simple_expression():
    """Test lexing a simple expression."""
    source = "(print 42)"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    assert len(tokens) == 5  # LPAREN, SYMBOL, NUMBER, RPAREN, EOF
    assert tokens[0].type == TokenType.LPAREN
    assert tokens[1].type == TokenType.SYMBOL
    assert tokens[1].value == "print"
    assert tokens[2].type == TokenType.NUMBER
    assert tokens[2].value == 42
    assert tokens[3].type == TokenType.RPAREN
    assert tokens[4].type == TokenType.EOF


def test_lexer_string_literal():
    """Test lexing string literals."""
    source = '(print "Hello, World!")'
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    assert tokens[2].type == TokenType.STRING
    assert tokens[2].value == "Hello, World!"


def test_lexer_float():
    """Test lexing floating point numbers."""
    source = "(print 3.14)"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    assert tokens[2].type == TokenType.NUMBER
    assert tokens[2].value == 3.14


def test_lexer_arithmetic():
    """Test lexing arithmetic expressions."""
    source = "(+ 2 3)"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    assert tokens[1].type == TokenType.SYMBOL
    assert tokens[1].value == "+"
    assert tokens[2].value == 2
    assert tokens[3].value == 3


def test_lexer_comment():
    """Test that comments are skipped."""
    source = "; This is a comment\n(print 42)"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    # Comment should be skipped
    assert tokens[0].type == TokenType.LPAREN


def test_lexer_nested_expression():
    """Test lexing nested expressions."""
    source = "(+ (* 2 3) 4)"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    assert len(tokens) == 10  # LPAREN + * LPAREN * 2 3 RPAREN 4 RPAREN EOF
    assert tokens[0].type == TokenType.LPAREN
    assert tokens[1].type == TokenType.SYMBOL
    assert tokens[1].value == "+"
    assert tokens[2].type == TokenType.LPAREN
