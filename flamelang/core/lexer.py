"""
FlameLang Lexer
Tokenization for glyph-based syntax
"""
from enum import Enum, auto
from typing import List, Optional
from dataclasses import dataclass


class TokenType(Enum):
    """Token types for FlameLang"""
    # Literals
    NUMBER = auto()
    STRING = auto()
    IDENTIFIER = auto()
    
    # Glyphs
    GLYPH = auto()
    
    # Keywords
    SIM = auto()      # Simulation
    CONST = auto()    # Constant
    
    # Operators
    ARROW = auto()         # ->
    PIPE = auto()          # |>
    COMPOSE = auto()       # <>
    
    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    EQUALS = auto()
    
    # Special
    NEWLINE = auto()
    EOF = auto()
    COMMENT = auto()


@dataclass
class Token:
    """Token representation"""
    type: TokenType
    value: str
    line: int
    column: int
    
    def __repr__(self):
        return f"Token({self.type.name}, {self.value!r}, {self.line}:{self.column})"


class Lexer:
    """
    Lexer for FlameLang
    Tokenizes glyph-based source code
    """
    
    # Recognized glyphs
    GLYPHS = {
        '⚡', '🔥', '🌊', '⚛️', '🎯', '🔮',
        '🛡️', '🔒', '👁️', '⚔️', '🌐',
    }
    
    # Physics symbols (text-based glyphs)
    PHYSICS_GLYPHS = {
        'BH1', 'OC1', 'PS1', 'GR1', 'ED1', 'MT1',
    }
    
    KEYWORDS = {
        'sim': TokenType.SIM,
        'const': TokenType.CONST,
    }
    
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        
    def current_char(self) -> Optional[str]:
        """Get current character"""
        if self.pos >= len(self.source):
            return None
        return self.source[self.pos]
    
    def peek_char(self, offset: int = 1) -> Optional[str]:
        """Peek at character ahead"""
        pos = self.pos + offset
        if pos >= len(self.source):
            return None
        return self.source[pos]
    
    def advance(self) -> None:
        """Move to next character"""
        if self.pos < len(self.source):
            if self.source[self.pos] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.pos += 1
    
    def skip_whitespace(self) -> None:
        """Skip whitespace characters (except newlines)"""
        while self.current_char() and self.current_char() in ' \t\r':
            self.advance()
    
    def read_number(self) -> Token:
        """Read a number token"""
        start_col = self.column
        num_str = ''
        
        while self.current_char() and (self.current_char().isdigit() or self.current_char() in '.e+-'):
            num_str += self.current_char()
            self.advance()
        
        return Token(TokenType.NUMBER, num_str, self.line, start_col)
    
    def read_identifier(self) -> Token:
        """Read an identifier or keyword"""
        start_col = self.column
        ident = ''
        
        while self.current_char() and (self.current_char().isalnum() or self.current_char() in '_'):
            ident += self.current_char()
            self.advance()
        
        # Check if it's a keyword or physics glyph
        if ident in self.KEYWORDS:
            return Token(self.KEYWORDS[ident], ident, self.line, start_col)
        elif ident in self.PHYSICS_GLYPHS:
            return Token(TokenType.GLYPH, ident, self.line, start_col)
        else:
            return Token(TokenType.IDENTIFIER, ident, self.line, start_col)
    
    def read_string(self) -> Token:
        """Read a string token"""
        start_col = self.column
        quote = self.current_char()
        self.advance()  # Skip opening quote
        
        string = ''
        while self.current_char() and self.current_char() != quote:
            string += self.current_char()
            self.advance()
        
        if self.current_char() == quote:
            self.advance()  # Skip closing quote
        
        return Token(TokenType.STRING, string, self.line, start_col)
    
    def read_comment(self) -> Token:
        """Read a comment"""
        start_col = self.column
        comment = ''
        
        while self.current_char() and self.current_char() != '\n':
            comment += self.current_char()
            self.advance()
        
        return Token(TokenType.COMMENT, comment, self.line, start_col)
    
    def tokenize(self) -> List[Token]:
        """Tokenize the entire source"""
        tokens = []
        
        while self.current_char():
            self.skip_whitespace()
            
            if not self.current_char():
                break
            
            ch = self.current_char()
            
            # Comments
            if ch == '#':
                tokens.append(self.read_comment())
                continue
            
            # Newlines
            if ch == '\n':
                tokens.append(Token(TokenType.NEWLINE, '\n', self.line, self.column))
                self.advance()
                continue
            
            # Numbers
            if ch.isdigit():
                tokens.append(self.read_number())
                continue
            
            # Strings
            if ch in '"\'':
                tokens.append(self.read_string())
                continue
            
            # Identifiers and keywords
            if ch.isalpha() or ch == '_':
                tokens.append(self.read_identifier())
                continue
            
            # Glyphs
            if ch in self.GLYPHS:
                tokens.append(Token(TokenType.GLYPH, ch, self.line, self.column))
                self.advance()
                continue
            
            # Operators
            if ch == '-' and self.peek_char() == '>':
                tokens.append(Token(TokenType.ARROW, '->', self.line, self.column))
                self.advance()
                self.advance()
                continue
            
            if ch == '|' and self.peek_char() == '>':
                tokens.append(Token(TokenType.PIPE, '|>', self.line, self.column))
                self.advance()
                self.advance()
                continue
            
            if ch == '<' and self.peek_char() == '>':
                tokens.append(Token(TokenType.COMPOSE, '<>', self.line, self.column))
                self.advance()
                self.advance()
                continue
            
            # Delimiters
            if ch == '(':
                tokens.append(Token(TokenType.LPAREN, '(', self.line, self.column))
                self.advance()
                continue
            
            if ch == ')':
                tokens.append(Token(TokenType.RPAREN, ')', self.line, self.column))
                self.advance()
                continue
            
            if ch == '[':
                tokens.append(Token(TokenType.LBRACKET, '[', self.line, self.column))
                self.advance()
                continue
            
            if ch == ']':
                tokens.append(Token(TokenType.RBRACKET, ']', self.line, self.column))
                self.advance()
                continue
            
            if ch == '=':
                tokens.append(Token(TokenType.EQUALS, '=', self.line, self.column))
                self.advance()
                continue
            
            # Unknown character - skip it
            self.advance()
        
        tokens.append(Token(TokenType.EOF, '', self.line, self.column))
        self.tokens = tokens
        return tokens
