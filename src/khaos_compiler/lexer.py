"""
StrategicKhaos Lexer - Stage 0
Tokenizes StrategicKhaos source code
"""

import re
from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional


class TokenType(Enum):
    # Literals
    STRING = auto()
    NUMBER = auto()
    IDENTIFIER = auto()
    
    # Keywords
    LET = auto()
    PRINT = auto()
    LAMBDA = auto()
    
    # Operators
    PLUS = auto()
    EQUALS = auto()
    
    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    SEMICOLON = auto()
    COMMA = auto()
    
    # Special
    COMMENT = auto()
    EOF = auto()
    NEWLINE = auto()


@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
    
    def error(self, msg: str):
        raise SyntaxError(f"Lexer error at line {self.line}, column {self.column}: {msg}")
    
    def peek(self, offset: int = 0) -> Optional[str]:
        pos = self.pos + offset
        if pos < len(self.source):
            return self.source[pos]
        return None
    
    def advance(self) -> Optional[str]:
        if self.pos < len(self.source):
            char = self.source[self.pos]
            self.pos += 1
            if char == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            return char
        return None
    
    def skip_whitespace(self):
        while self.peek() and self.peek() in ' \t\r':
            self.advance()
    
    def skip_comment(self):
        if self.peek() == '-' and self.peek(1) == '-':
            while self.peek() and self.peek() != '\n':
                self.advance()
    
    def read_string(self) -> str:
        quote = self.advance()  # consume opening quote
        value = ""
        while self.peek() and self.peek() != quote:
            char = self.advance()
            if char == '\\' and self.peek():
                next_char = self.advance()
                if next_char == 'n':
                    value += '\n'
                elif next_char == 't':
                    value += '\t'
                elif next_char == '\\':
                    value += '\\'
                elif next_char == quote:
                    value += quote
                else:
                    value += next_char
            else:
                value += char
        
        if not self.peek():
            self.error("Unterminated string")
        
        self.advance()  # consume closing quote
        return value
    
    def read_number(self) -> str:
        value = ""
        while self.peek() and (self.peek().isdigit() or self.peek() == '.'):
            value += self.advance()
        return value
    
    def read_identifier(self) -> str:
        value = ""
        while self.peek() and (self.peek().isalnum() or self.peek() == '_'):
            value += self.advance()
        return value
    
    def tokenize(self) -> List[Token]:
        keywords = {
            'let': TokenType.LET,
            'print': TokenType.PRINT,
            'λ': TokenType.LAMBDA,
        }
        
        while self.pos < len(self.source):
            self.skip_whitespace()
            
            if not self.peek():
                break
            
            # Skip comments
            if self.peek() == '-' and self.peek(1) == '-':
                self.skip_comment()
                continue
            
            # Newlines
            if self.peek() == '\n':
                token = Token(TokenType.NEWLINE, '\n', self.line, self.column)
                self.tokens.append(token)
                self.advance()
                continue
            
            # Strings
            if self.peek() in '"\'':
                start_line, start_col = self.line, self.column
                value = self.read_string()
                token = Token(TokenType.STRING, value, start_line, start_col)
                self.tokens.append(token)
                continue
            
            # Numbers
            if self.peek().isdigit():
                start_line, start_col = self.line, self.column
                value = self.read_number()
                token = Token(TokenType.NUMBER, value, start_line, start_col)
                self.tokens.append(token)
                continue
            
            # Identifiers and keywords
            if self.peek().isalpha() or self.peek() == '_' or self.peek() == 'λ':
                start_line, start_col = self.line, self.column
                value = self.read_identifier()
                token_type = keywords.get(value, TokenType.IDENTIFIER)
                token = Token(token_type, value, start_line, start_col)
                self.tokens.append(token)
                continue
            
            # Operators and delimiters
            char = self.peek()
            start_line, start_col = self.line, self.column
            
            if char == '+':
                self.advance()
                self.tokens.append(Token(TokenType.PLUS, '+', start_line, start_col))
            elif char == '=':
                self.advance()
                self.tokens.append(Token(TokenType.EQUALS, '=', start_line, start_col))
            elif char == '(':
                self.advance()
                self.tokens.append(Token(TokenType.LPAREN, '(', start_line, start_col))
            elif char == ')':
                self.advance()
                self.tokens.append(Token(TokenType.RPAREN, ')', start_line, start_col))
            elif char == '{':
                self.advance()
                self.tokens.append(Token(TokenType.LBRACE, '{', start_line, start_col))
            elif char == '}':
                self.advance()
                self.tokens.append(Token(TokenType.RBRACE, '}', start_line, start_col))
            elif char == ';':
                self.advance()
                self.tokens.append(Token(TokenType.SEMICOLON, ';', start_line, start_col))
            elif char == ',':
                self.advance()
                self.tokens.append(Token(TokenType.COMMA, ',', start_line, start_col))
            else:
                self.error(f"Unexpected character: '{char}'")
        
        self.tokens.append(Token(TokenType.EOF, '', self.line, self.column))
        return self.tokens
