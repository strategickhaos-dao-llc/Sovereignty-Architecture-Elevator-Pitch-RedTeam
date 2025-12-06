#!/usr/bin/env python3
"""FlameLang Lexer - Tokenizes FlameLang source code."""

import re
from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional

class TokenType(Enum):
    # Literals
    NUMBER = auto()
    IDENTIFIER = auto()
    GLYPH = auto()
    
    # Keywords
    SIM = auto()
    
    # Operators
    EQUALS = auto()
    ARROW = auto()        # ->
    PIPE = auto()         # |>
    COMPOSE = auto()      # <>
    
    # Delimiters
    LBRACKET = auto()
    RBRACKET = auto()
    
    # Special
    NEWLINE = auto()
    EOF = auto()

@dataclass
class Token:
    type: TokenType
    value: any
    line: int
    column: int

class Lexer:
    """Tokenizes FlameLang source code."""
    
    # Core glyphs with their frequencies
    GLYPHS = {
        '⚡': ('Execute', 528),
        '🔥': ('Transform', 741),
        '🌊': ('Flow', 432),
        '⚛️': ('Compose', 963),
        '🎯': ('Target', 639),
        '🔮': ('Synthesize', 852),
        '🛡️': ('Boundary_Harden', 174),
        '🔒': ('Encrypt', 396),
        '👁️': ('Audit', 417),
        '⚔️': ('Defend', 639),
        '🌐': ('Sovereignty', 852),
    }
    
    KEYWORDS = {'sim'}
    
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
    
    def error(self, msg: str):
        raise SyntaxError(f"Lexer error at line {self.line}, col {self.column}: {msg}")
    
    def peek(self, offset: int = 0) -> Optional[str]:
        """Look ahead in the source without consuming."""
        pos = self.pos + offset
        if pos < len(self.source):
            return self.source[pos]
        return None
    
    def advance(self) -> Optional[str]:
        """Consume and return the current character."""
        if self.pos >= len(self.source):
            return None
        char = self.source[self.pos]
        self.pos += 1
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return char
    
    def skip_whitespace(self):
        """Skip spaces and tabs (but not newlines)."""
        while self.peek() and self.peek() in ' \t':
            self.advance()
    
    def skip_comment(self):
        """Skip comment lines starting with #."""
        if self.peek() == '#':
            while self.peek() and self.peek() != '\n':
                self.advance()
    
    def read_number(self) -> Token:
        """Read a number (int or float, including scientific notation)."""
        start_line = self.line
        start_col = self.column
        num_str = ''
        
        # Read digits before decimal point
        while self.peek() and (self.peek().isdigit() or self.peek() == '.'):
            num_str += self.advance()
        
        # Handle scientific notation
        if self.peek() and self.peek() in 'eE':
            num_str += self.advance()
            if self.peek() and self.peek() in '+-':
                num_str += self.advance()
            while self.peek() and self.peek().isdigit():
                num_str += self.advance()
        
        value = float(num_str) if '.' in num_str or 'e' in num_str or 'E' in num_str else int(num_str)
        return Token(TokenType.NUMBER, value, start_line, start_col)
    
    def read_identifier(self) -> Token:
        """Read an identifier or keyword."""
        start_line = self.line
        start_col = self.column
        ident = ''
        
        while self.peek() and (self.peek().isalnum() or self.peek() == '_'):
            ident += self.advance()
        
        # Check if it's a keyword
        if ident in self.KEYWORDS:
            return Token(TokenType.SIM if ident == 'sim' else TokenType.IDENTIFIER, ident, start_line, start_col)
        
        return Token(TokenType.IDENTIFIER, ident, start_line, start_col)
    
    def tokenize(self) -> List[Token]:
        """Tokenize the entire source code."""
        while self.pos < len(self.source):
            self.skip_whitespace()
            
            if self.pos >= len(self.source):
                break
            
            # Skip comments
            if self.peek() == '#':
                self.skip_comment()
                continue
            
            char = self.peek()
            start_line = self.line
            start_col = self.column
            
            # Newline
            if char == '\n':
                self.advance()
                self.tokens.append(Token(TokenType.NEWLINE, '\n', start_line, start_col))
            
            # Numbers
            elif char.isdigit():
                self.tokens.append(self.read_number())
            
            # Identifiers and keywords
            elif char.isalpha() or char == '_':
                self.tokens.append(self.read_identifier())
            
            # Operators and delimiters
            elif char == '=':
                self.advance()
                self.tokens.append(Token(TokenType.EQUALS, '=', start_line, start_col))
            
            elif char == '-':
                self.advance()
                if self.peek() == '>':
                    self.advance()
                    self.tokens.append(Token(TokenType.ARROW, '->', start_line, start_col))
                else:
                    self.error(f"Unexpected character: {char}")
            
            elif char == '|':
                self.advance()
                if self.peek() == '>':
                    self.advance()
                    self.tokens.append(Token(TokenType.PIPE, '|>', start_line, start_col))
                else:
                    self.error(f"Unexpected character: {char}")
            
            elif char == '<':
                self.advance()
                if self.peek() == '>':
                    self.advance()
                    self.tokens.append(Token(TokenType.COMPOSE, '<>', start_line, start_col))
                else:
                    self.error(f"Unexpected character: {char}")
            
            elif char == '[':
                self.advance()
                self.tokens.append(Token(TokenType.LBRACKET, '[', start_line, start_col))
            
            elif char == ']':
                self.advance()
                self.tokens.append(Token(TokenType.RBRACKET, ']', start_line, start_col))
            
            # Glyphs (multi-byte Unicode characters)
            else:
                # Try to match a glyph (may be multi-codepoint)
                glyph = self.advance()
                
                # Check if next char is a variation selector or other combining character
                while self.peek() and ord(self.peek()) in [0xFE0F, 0xFE0E]:
                    glyph += self.advance()
                
                # Check if this is a registered glyph
                if glyph in self.GLYPHS:
                    self.tokens.append(Token(TokenType.GLYPH, glyph, start_line, start_col))
                else:
                    self.error(f"Unexpected character: {glyph}")
        
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens

def main():
    """Test the lexer."""
    test_code = """
# Black hole simulation
sim BH1 M=1.989e30 r=1e7

# Variables
coherence = 0.95
lambda_param = 1.0

# Glyph pipeline
⚡ -> [OC1] |> 🔥

# Sovereignty
🛡️ -> 🔒
"""
    
    lexer = Lexer(test_code)
    tokens = lexer.tokenize()
    
    print("Tokens:")
    for token in tokens:
        if token.type != TokenType.NEWLINE and token.type != TokenType.EOF:
            print(f"  {token.type.name:15} {repr(token.value):20} @ {token.line}:{token.column}")

if __name__ == '__main__':
    main()
