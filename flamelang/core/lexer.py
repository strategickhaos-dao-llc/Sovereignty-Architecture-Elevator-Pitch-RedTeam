"""
FlameLang Lexer
Tokenizes FlameLang source code with frequency metadata
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional
from .glyph_registry import GlyphRegistry


class TokenType(Enum):
    """Token types for FlameLang"""
    # Literals
    NUMBER = auto()
    STRING = auto()
    IDENTIFIER = auto()
    
    # Glyphs
    GLYPH = auto()
    
    # Keywords
    LET = auto()
    CONST = auto()
    FUNCTION = auto()
    RETURN = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    
    # Physics operations
    SCHWARZSCHILD = auto()
    GEODESIC = auto()
    TENSOR = auto()
    EDDY = auto()
    
    # Sovereignty operations
    ISOLATE = auto()
    MONITOR = auto()
    HARDEN = auto()
    AUDIT = auto()
    
    # Operators
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    ASSIGN = auto()
    EQUALS = auto()
    LESS_THAN = auto()
    GREATER_THAN = auto()
    
    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    COMMA = auto()
    SEMICOLON = auto()
    COLON = auto()
    DOT = auto()
    ARROW = auto()
    
    # Special
    NEWLINE = auto()
    EOF = auto()
    COMMENT = auto()


@dataclass
class Token:
    """Represents a single token with frequency metadata"""
    type: TokenType
    value: any
    line: int
    column: int
    frequency: Optional[int] = None  # Frequency metadata from glyph
    
    def __repr__(self):
        freq_str = f", {self.frequency}Hz" if self.frequency else ""
        return f"Token({self.type.name}, {self.value!r}, {self.line}:{self.column}{freq_str})"


class Lexer:
    """
    Lexical analyzer for FlameLang
    Tokenizes source code and attaches frequency metadata to glyphs
    """
    
    KEYWORDS = {
        'let': TokenType.LET,
        'const': TokenType.CONST,
        'function': TokenType.FUNCTION,
        'fn': TokenType.FUNCTION,
        'return': TokenType.RETURN,
        'if': TokenType.IF,
        'else': TokenType.ELSE,
        'while': TokenType.WHILE,
        'for': TokenType.FOR,
        # Physics operations
        'schwarzschild': TokenType.SCHWARZSCHILD,
        'geodesic': TokenType.GEODESIC,
        'tensor': TokenType.TENSOR,
        'eddy': TokenType.EDDY,
        # Sovereignty operations
        'isolate': TokenType.ISOLATE,
        'monitor': TokenType.MONITOR,
        'harden': TokenType.HARDEN,
        'audit': TokenType.AUDIT,
    }
    
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
        self.glyph_registry = GlyphRegistry()
    
    def current_char(self) -> Optional[str]:
        """Get the current character"""
        if self.position >= len(self.source):
            return None
        return self.source[self.position]
    
    def peek_char(self, offset: int = 1) -> Optional[str]:
        """Peek ahead at a character"""
        pos = self.position + offset
        if pos >= len(self.source):
            return None
        return self.source[pos]
    
    def advance(self):
        """Move to the next character"""
        if self.position < len(self.source):
            if self.source[self.position] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.position += 1
    
    def skip_whitespace(self):
        """Skip whitespace except newlines"""
        while self.current_char() in ' \t\r':
            self.advance()
    
    def skip_comment(self):
        """Skip single-line comments"""
        if self.current_char() == '#':
            while self.current_char() and self.current_char() != '\n':
                self.advance()
    
    def read_number(self) -> Token:
        """Read a number (integer or float)"""
        start_col = self.column
        num_str = ''
        has_dot = False
        
        while self.current_char() and (self.current_char().isdigit() or self.current_char() == '.'):
            if self.current_char() == '.':
                if has_dot:
                    break
                has_dot = True
            num_str += self.current_char()
            self.advance()
        
        value = float(num_str) if has_dot else int(num_str)
        return Token(TokenType.NUMBER, value, self.line, start_col)
    
    def read_string(self, quote_char: str) -> Token:
        """Read a string literal"""
        start_col = self.column
        self.advance()  # Skip opening quote
        string_value = ''
        
        while self.current_char() and self.current_char() != quote_char:
            if self.current_char() == '\\':
                self.advance()
                # Handle escape sequences
                escape_char = self.current_char()
                if escape_char == 'n':
                    string_value += '\n'
                elif escape_char == 't':
                    string_value += '\t'
                elif escape_char == '\\':
                    string_value += '\\'
                elif escape_char == quote_char:
                    string_value += quote_char
                else:
                    string_value += escape_char
                self.advance()
            else:
                string_value += self.current_char()
                self.advance()
        
        self.advance()  # Skip closing quote
        return Token(TokenType.STRING, string_value, self.line, start_col)
    
    def read_identifier(self) -> Token:
        """Read an identifier or keyword"""
        start_col = self.column
        identifier = ''
        
        while self.current_char() and (self.current_char().isalnum() or self.current_char() == '_'):
            identifier += self.current_char()
            self.advance()
        
        # Check if it's a keyword
        token_type = self.KEYWORDS.get(identifier, TokenType.IDENTIFIER)
        return Token(token_type, identifier, self.line, start_col)
    
    def read_glyph(self) -> Token:
        """Read a glyph and attach frequency metadata"""
        start_col = self.column
        glyph_char = self.current_char()
        self.advance()
        
        # Look up glyph in registry
        glyph = self.glyph_registry.lookup(glyph_char)
        frequency = glyph.frequency if glyph else None
        
        return Token(TokenType.GLYPH, glyph_char, self.line, start_col, frequency)
    
    def tokenize(self) -> List[Token]:
        """Tokenize the entire source code"""
        self.tokens = []
        
        while self.current_char():
            self.skip_whitespace()
            
            if not self.current_char():
                break
            
            # Comments
            if self.current_char() == '#':
                self.skip_comment()
                continue
            
            # Newlines
            if self.current_char() == '\n':
                self.tokens.append(Token(TokenType.NEWLINE, '\n', self.line, self.column))
                self.advance()
                continue
            
            # Numbers
            if self.current_char().isdigit():
                self.tokens.append(self.read_number())
                continue
            
            # Strings
            if self.current_char() in '"\'':
                quote = self.current_char()
                self.tokens.append(self.read_string(quote))
                continue
            
            # Identifiers and keywords
            if self.current_char().isalpha() or self.current_char() == '_':
                self.tokens.append(self.read_identifier())
                continue
            
            # Check for glyphs (Unicode symbols)
            if ord(self.current_char()) > 127:
                self.tokens.append(self.read_glyph())
                continue
            
            # Operators and delimiters
            char = self.current_char()
            col = self.column
            
            if char == '+':
                self.tokens.append(Token(TokenType.PLUS, '+', self.line, col))
                self.advance()
            elif char == '-':
                if self.peek_char() == '>':
                    self.tokens.append(Token(TokenType.ARROW, '->', self.line, col))
                    self.advance()
                    self.advance()
                else:
                    self.tokens.append(Token(TokenType.MINUS, '-', self.line, col))
                    self.advance()
            elif char == '*':
                self.tokens.append(Token(TokenType.MULTIPLY, '*', self.line, col))
                self.advance()
            elif char == '/':
                self.tokens.append(Token(TokenType.DIVIDE, '/', self.line, col))
                self.advance()
            elif char == '=':
                if self.peek_char() == '=':
                    self.tokens.append(Token(TokenType.EQUALS, '==', self.line, col))
                    self.advance()
                    self.advance()
                else:
                    self.tokens.append(Token(TokenType.ASSIGN, '=', self.line, col))
                    self.advance()
            elif char == '<':
                self.tokens.append(Token(TokenType.LESS_THAN, '<', self.line, col))
                self.advance()
            elif char == '>':
                self.tokens.append(Token(TokenType.GREATER_THAN, '>', self.line, col))
                self.advance()
            elif char == '(':
                self.tokens.append(Token(TokenType.LPAREN, '(', self.line, col))
                self.advance()
            elif char == ')':
                self.tokens.append(Token(TokenType.RPAREN, ')', self.line, col))
                self.advance()
            elif char == '{':
                self.tokens.append(Token(TokenType.LBRACE, '{', self.line, col))
                self.advance()
            elif char == '}':
                self.tokens.append(Token(TokenType.RBRACE, '}', self.line, col))
                self.advance()
            elif char == '[':
                self.tokens.append(Token(TokenType.LBRACKET, '[', self.line, col))
                self.advance()
            elif char == ']':
                self.tokens.append(Token(TokenType.RBRACKET, ']', self.line, col))
                self.advance()
            elif char == ',':
                self.tokens.append(Token(TokenType.COMMA, ',', self.line, col))
                self.advance()
            elif char == ';':
                self.tokens.append(Token(TokenType.SEMICOLON, ';', self.line, col))
                self.advance()
            elif char == ':':
                self.tokens.append(Token(TokenType.COLON, ':', self.line, col))
                self.advance()
            elif char == '.':
                self.tokens.append(Token(TokenType.DOT, '.', self.line, col))
                self.advance()
            else:
                # Unknown character
                self.advance()
        
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens
