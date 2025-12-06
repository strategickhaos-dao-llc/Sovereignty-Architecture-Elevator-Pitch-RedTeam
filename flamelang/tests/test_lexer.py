"""
Tests for Lexer
"""

import unittest
from flamelang.core.lexer import Lexer, TokenType


class TestLexer(unittest.TestCase):
    
    def test_tokenize_numbers(self):
        """Test tokenizing numbers"""
        lexer = Lexer("42 3.14 0.5")
        tokens = lexer.tokenize()
        
        self.assertEqual(tokens[0].type, TokenType.NUMBER)
        self.assertEqual(tokens[0].value, 42)
        
        self.assertEqual(tokens[1].type, TokenType.NUMBER)
        self.assertEqual(tokens[1].value, 3.14)
        
        self.assertEqual(tokens[2].type, TokenType.NUMBER)
        self.assertEqual(tokens[2].value, 0.5)
    
    def test_tokenize_strings(self):
        """Test tokenizing strings"""
        lexer = Lexer('"hello" \'world\'')
        tokens = lexer.tokenize()
        
        self.assertEqual(tokens[0].type, TokenType.STRING)
        self.assertEqual(tokens[0].value, "hello")
        
        self.assertEqual(tokens[1].type, TokenType.STRING)
        self.assertEqual(tokens[1].value, "world")
    
    def test_tokenize_identifiers(self):
        """Test tokenizing identifiers"""
        lexer = Lexer("let x = 42")
        tokens = lexer.tokenize()
        
        self.assertEqual(tokens[0].type, TokenType.LET)
        self.assertEqual(tokens[1].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[1].value, "x")
        self.assertEqual(tokens[2].type, TokenType.ASSIGN)
        self.assertEqual(tokens[3].type, TokenType.NUMBER)
    
    def test_tokenize_glyphs(self):
        """Test tokenizing glyphs with frequency metadata"""
        lexer = Lexer("🔥 ⚔")
        tokens = lexer.tokenize()
        
        self.assertEqual(tokens[0].type, TokenType.GLYPH)
        self.assertEqual(tokens[0].value, "🔥")
        self.assertEqual(tokens[0].frequency, 741)  # Transform frequency
        
        self.assertEqual(tokens[1].type, TokenType.GLYPH)
        self.assertEqual(tokens[1].value, "⚔")
        self.assertEqual(tokens[1].frequency, 174)  # Defense frequency
    
    def test_tokenize_operators(self):
        """Test tokenizing operators"""
        lexer = Lexer("+ - * / == < >")
        tokens = lexer.tokenize()
        
        self.assertEqual(tokens[0].type, TokenType.PLUS)
        self.assertEqual(tokens[1].type, TokenType.MINUS)
        self.assertEqual(tokens[2].type, TokenType.MULTIPLY)
        self.assertEqual(tokens[3].type, TokenType.DIVIDE)
        self.assertEqual(tokens[4].type, TokenType.EQUALS)
        self.assertEqual(tokens[5].type, TokenType.LESS_THAN)
        self.assertEqual(tokens[6].type, TokenType.GREATER_THAN)
    
    def test_tokenize_physics_operations(self):
        """Test tokenizing physics operation keywords"""
        lexer = Lexer("schwarzschild geodesic tensor eddy")
        tokens = lexer.tokenize()
        
        self.assertEqual(tokens[0].type, TokenType.SCHWARZSCHILD)
        self.assertEqual(tokens[1].type, TokenType.GEODESIC)
        self.assertEqual(tokens[2].type, TokenType.TENSOR)
        self.assertEqual(tokens[3].type, TokenType.EDDY)
    
    def test_tokenize_sovereignty_operations(self):
        """Test tokenizing sovereignty operation keywords"""
        lexer = Lexer("isolate monitor harden audit")
        tokens = lexer.tokenize()
        
        self.assertEqual(tokens[0].type, TokenType.ISOLATE)
        self.assertEqual(tokens[1].type, TokenType.MONITOR)
        self.assertEqual(tokens[2].type, TokenType.HARDEN)
        self.assertEqual(tokens[3].type, TokenType.AUDIT)
    
    def test_tokenize_comments(self):
        """Test that comments are properly skipped"""
        lexer = Lexer("let x = 42 # this is a comment\nlet y = 10")
        tokens = lexer.tokenize()
        
        # Should have: let, x, =, 42, newline, let, y, =, 10, EOF
        self.assertEqual(tokens[0].type, TokenType.LET)
        self.assertEqual(tokens[1].value, "x")
        self.assertEqual(tokens[4].type, TokenType.NEWLINE)
        self.assertEqual(tokens[5].type, TokenType.LET)
        self.assertEqual(tokens[6].value, "y")
    
    def test_tokenize_function_call(self):
        """Test tokenizing function calls"""
        lexer = Lexer("print(42)")
        tokens = lexer.tokenize()
        
        self.assertEqual(tokens[0].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[0].value, "print")
        self.assertEqual(tokens[1].type, TokenType.LPAREN)
        self.assertEqual(tokens[2].type, TokenType.NUMBER)
        self.assertEqual(tokens[3].type, TokenType.RPAREN)


if __name__ == '__main__':
    unittest.main()
