"""
Tests for the StrategicKhaos Lexer
"""

import sys
from pathlib import Path

# Add compiler src to path
COMPILER_ROOT = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(COMPILER_ROOT.parent))

from src.lexer import Lexer, TokenType, Token


def test_simple_tokens():
    """Test basic token recognition"""
    source = "let x = 42;"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    assert len(tokens) == 6  # let, x, =, 42, ;, EOF
    assert tokens[0].type == TokenType.LET
    assert tokens[1].type == TokenType.IDENTIFIER
    assert tokens[1].value == "x"
    assert tokens[2].type == TokenType.ASSIGN
    assert tokens[3].type == TokenType.INTEGER
    assert tokens[3].value == 42
    assert tokens[4].type == TokenType.SEMICOLON
    assert tokens[5].type == TokenType.EOF


def test_keywords():
    """Test keyword recognition"""
    source = "fn if else while for return print show"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    expected = [
        TokenType.FN,
        TokenType.IF,
        TokenType.ELSE,
        TokenType.WHILE,
        TokenType.FOR,
        TokenType.RETURN,
        TokenType.PRINT,
        TokenType.SHOW,
        TokenType.EOF
    ]
    
    for i, expected_type in enumerate(expected):
        assert tokens[i].type == expected_type


def test_operators():
    """Test operator recognition"""
    source = "+ - * / % ** == != < <= > >= and or not"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    expected = [
        TokenType.PLUS,
        TokenType.MINUS,
        TokenType.MULTIPLY,
        TokenType.DIVIDE,
        TokenType.MODULO,
        TokenType.POWER,
        TokenType.EQUAL,
        TokenType.NOT_EQUAL,
        TokenType.LESS,
        TokenType.LESS_EQUAL,
        TokenType.GREATER,
        TokenType.GREATER_EQUAL,
        TokenType.AND,
        TokenType.OR,
        TokenType.NOT,
        TokenType.EOF
    ]
    
    for i, expected_type in enumerate(expected):
        assert tokens[i].type == expected_type


def test_strings():
    """Test string literal parsing"""
    source = '"Hello, world!" \'Single quotes\''
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    assert tokens[0].type == TokenType.STRING
    assert tokens[0].value == "Hello, world!"
    assert tokens[1].type == TokenType.STRING
    assert tokens[1].value == "Single quotes"


def test_numbers():
    """Test number parsing"""
    source = "42 3.14 0 -17"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    assert tokens[0].type == TokenType.INTEGER
    assert tokens[0].value == 42
    assert tokens[1].type == TokenType.FLOAT
    assert tokens[1].value == 3.14
    assert tokens[2].type == TokenType.INTEGER
    assert tokens[2].value == 0
    # -17 is parsed as MINUS followed by INTEGER
    assert tokens[3].type == TokenType.MINUS
    assert tokens[4].type == TokenType.INTEGER
    assert tokens[4].value == 17


def test_comments():
    """Test comment handling"""
    source = """
    let x = 10; # This is a comment
    # Another comment
    let y = 20;
    """
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    # Comments should be ignored
    token_types = [t.type for t in tokens if t.type != TokenType.EOF]
    assert TokenType.COMMENT not in token_types
    
    # Should have: let, x, =, 10, ;, let, y, =, 20, ;
    non_eof = [t for t in tokens if t.type != TokenType.EOF]
    assert len(non_eof) == 10


def test_complex_expression():
    """Test a more complex expression"""
    source = "let result = (a + b) * 2 - c / 3;"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    expected_types = [
        TokenType.LET,
        TokenType.IDENTIFIER,  # result
        TokenType.ASSIGN,
        TokenType.LPAREN,
        TokenType.IDENTIFIER,  # a
        TokenType.PLUS,
        TokenType.IDENTIFIER,  # b
        TokenType.RPAREN,
        TokenType.MULTIPLY,
        TokenType.INTEGER,     # 2
        TokenType.MINUS,
        TokenType.IDENTIFIER,  # c
        TokenType.DIVIDE,
        TokenType.INTEGER,     # 3
        TokenType.SEMICOLON,
        TokenType.EOF
    ]
    
    for i, expected_type in enumerate(expected_types):
        assert tokens[i].type == expected_type


def test_function_definition():
    """Test lexing a function definition"""
    source = """
    fn greet(name) {
        print "Hello, " + name;
    }
    """
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    # Check key tokens
    assert tokens[0].type == TokenType.FN
    assert tokens[1].type == TokenType.IDENTIFIER  # greet
    assert tokens[1].value == "greet"
    assert tokens[2].type == TokenType.LPAREN
    assert tokens[3].type == TokenType.IDENTIFIER  # name
    assert tokens[4].type == TokenType.RPAREN
    assert tokens[5].type == TokenType.LBRACE


def run_tests():
    """Run all lexer tests"""
    tests = [
        ("Simple tokens", test_simple_tokens),
        ("Keywords", test_keywords),
        ("Operators", test_operators),
        ("Strings", test_strings),
        ("Numbers", test_numbers),
        ("Comments", test_comments),
        ("Complex expression", test_complex_expression),
        ("Function definition", test_function_definition),
    ]
    
    passed = 0
    failed = 0
    
    print("Running StrategicKhaos Lexer Tests")
    print("=" * 50)
    
    for name, test_func in tests:
        try:
            test_func()
            print(f"✓ {name}")
            passed += 1
        except AssertionError as e:
            print(f"✗ {name}: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {name}: Unexpected error - {e}")
            failed += 1
    
    print("=" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    
    return failed == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
