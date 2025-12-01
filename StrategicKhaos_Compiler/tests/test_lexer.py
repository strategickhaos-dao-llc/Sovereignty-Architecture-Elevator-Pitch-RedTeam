#!/usr/bin/env python3
"""
Test suite for StrategicKhaos Compiler Lexer
Stage 0 Bootstrap - Grammar and Lexical Analysis
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.lexer import Lexer, Token, LexerError
from src.token import TokenType

def test_simple_tokens():
    """Test basic single-character tokens"""
    source = "(){},.;+-*/"
    lexer = Lexer(source)
    tokens = lexer.scan_tokens()
    
    expected = [
        TokenType.LEFT_PAREN,
        TokenType.RIGHT_PAREN,
        TokenType.LEFT_BRACE,
        TokenType.RIGHT_BRACE,
        TokenType.COMMA,
        TokenType.DOT,
        TokenType.SEMICOLON,
        TokenType.PLUS,
        TokenType.MINUS,
        TokenType.STAR,
        TokenType.SLASH,
        TokenType.EOF
    ]
    
    assert len(tokens) == len(expected)
    for i, token in enumerate(tokens):
        assert token.type == expected[i], f"Expected {expected[i]}, got {token.type}"
    print("✓ test_simple_tokens passed")

def test_two_char_tokens():
    """Test two-character operators"""
    source = "!= == <= >= -> =>"
    lexer = Lexer(source)
    tokens = lexer.scan_tokens()
    
    expected = [
        TokenType.BANG_EQUAL,
        TokenType.EQUAL_EQUAL,
        TokenType.LESS_EQUAL,
        TokenType.GREATER_EQUAL,
        TokenType.ARROW,
        TokenType.FAT_ARROW,
        TokenType.EOF
    ]
    
    assert len(tokens) == len(expected)
    for i, token in enumerate(tokens):
        assert token.type == expected[i], f"Expected {expected[i]}, got {token.type}"
    print("✓ test_two_char_tokens passed")

def test_chaos_operator():
    """Test the chaos knife-flip operator"""
    source = "≫"
    lexer = Lexer(source)
    tokens = lexer.scan_tokens()
    
    assert len(tokens) == 2  # CHAOS + EOF
    assert tokens[0].type == TokenType.CHAOS
    print("✓ test_chaos_operator passed")

def test_keywords():
    """Test keyword recognition"""
    source = "let mut fn return if else while for print show"
    lexer = Lexer(source)
    tokens = lexer.scan_tokens()
    
    expected = [
        TokenType.LET,
        TokenType.MUT,
        TokenType.FN,
        TokenType.RETURN,
        TokenType.IF,
        TokenType.ELSE,
        TokenType.WHILE,
        TokenType.FOR,
        TokenType.PRINT,
        TokenType.SHOW,
        TokenType.EOF
    ]
    
    assert len(tokens) == len(expected)
    for i, token in enumerate(tokens):
        assert token.type == expected[i], f"Expected {expected[i]}, got {token.type}"
    print("✓ test_keywords passed")

def test_string_literals():
    """Test string parsing"""
    source = '"Welcome to the chaos realm"'
    lexer = Lexer(source)
    tokens = lexer.scan_tokens()
    
    assert len(tokens) == 2  # STRING + EOF
    assert tokens[0].type == TokenType.STRING
    assert tokens[0].literal == "Welcome to the chaos realm"
    print("✓ test_string_literals passed")

def test_number_literals():
    """Test number parsing"""
    source = "42 3.14159"
    lexer = Lexer(source)
    tokens = lexer.scan_tokens()
    
    assert len(tokens) == 3  # NUMBER + NUMBER + EOF
    assert tokens[0].type == TokenType.NUMBER
    assert tokens[0].literal == 42.0
    assert tokens[1].type == TokenType.NUMBER
    assert tokens[1].literal == 3.14159
    print("✓ test_number_literals passed")

def test_identifiers():
    """Test identifier parsing"""
    source = "x foo_bar _private myVar123"
    lexer = Lexer(source)
    tokens = lexer.scan_tokens()
    
    assert len(tokens) == 5  # 4 IDENTIFIER + EOF
    for i in range(4):
        assert tokens[i].type == TokenType.IDENTIFIER
    print("✓ test_identifiers passed")

def test_hello_khaos():
    """Test the hello.khaos example file"""
    hello_khaos_path = os.path.join(os.path.dirname(__file__), '..', 'examples', 'hello.khaos')
    with open(hello_khaos_path, 'r', encoding='utf-8') as f:
        source = f.read()
    
    lexer = Lexer(source)
    tokens = lexer.scan_tokens()
    
    # Expected token sequence for hello.khaos
    # print "Welcome to the chaos realm";
    # let x = 40 + 2;
    # show x;
    # ≫ "The empire has grammar now" ≫
    
    expected_types = [
        TokenType.PRINT,
        TokenType.STRING,
        TokenType.SEMICOLON,
        TokenType.LET,
        TokenType.IDENTIFIER,  # x
        TokenType.EQUAL,
        TokenType.NUMBER,      # 40
        TokenType.PLUS,
        TokenType.NUMBER,      # 2
        TokenType.SEMICOLON,
        TokenType.SHOW,
        TokenType.IDENTIFIER,  # x
        TokenType.SEMICOLON,
        TokenType.CHAOS,       # ≫
        TokenType.STRING,
        TokenType.CHAOS,       # ≫
        TokenType.EOF
    ]
    
    assert len(tokens) == len(expected_types), f"Expected {len(expected_types)} tokens, got {len(tokens)}"
    
    for i, (token, expected_type) in enumerate(zip(tokens, expected_types)):
        assert token.type == expected_type, f"Token {i}: Expected {expected_type}, got {token.type}"
    
    print("✓ test_hello_khaos passed")

def test_comments():
    """Test comment handling"""
    source = """// This is a comment
let x = 42; // inline comment
// Another comment
show x;"""
    lexer = Lexer(source)
    tokens = lexer.scan_tokens()
    
    # Should only have: LET, IDENTIFIER, EQUAL, NUMBER, SEMICOLON, SHOW, IDENTIFIER, SEMICOLON, EOF
    expected_types = [
        TokenType.LET,
        TokenType.IDENTIFIER,
        TokenType.EQUAL,
        TokenType.NUMBER,
        TokenType.SEMICOLON,
        TokenType.SHOW,
        TokenType.IDENTIFIER,
        TokenType.SEMICOLON,
        TokenType.EOF
    ]
    
    assert len(tokens) == len(expected_types), f"Expected {len(expected_types)} tokens, got {len(tokens)}"
    for i, (token, expected_type) in enumerate(zip(tokens, expected_types)):
        assert token.type == expected_type, f"Token {i}: Expected {expected_type}, got {token.type}"
    
    print("✓ test_comments passed")

def test_error_handling():
    """Test lexer error handling"""
    # Test unterminated string
    source = '"unterminated string'
    lexer = Lexer(source)
    tokens = lexer.scan_tokens()
    assert len(lexer.errors) > 0, "Should have errors for unterminated string"
    
    # Test unexpected character
    source = '@#$'
    lexer = Lexer(source)
    tokens = lexer.scan_tokens()
    assert len(lexer.errors) > 0, "Should have errors for unexpected characters"
    
    print("✓ test_error_handling passed")

def run_all_tests():
    """Run all lexer tests"""
    print("\n=== Running StrategicKhaos Compiler Lexer Tests ===\n")
    
    test_simple_tokens()
    test_two_char_tokens()
    test_chaos_operator()
    test_keywords()
    test_string_literals()
    test_number_literals()
    test_identifiers()
    test_comments()
    test_hello_khaos()
    test_error_handling()
    
    print("\n=== All tests passed! The empire has grammar. ===\n")

if __name__ == "__main__":
    run_all_tests()
