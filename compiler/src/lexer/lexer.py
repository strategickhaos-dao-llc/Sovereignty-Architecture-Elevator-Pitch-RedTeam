"""
StrategicKhaos Lexer Implementation

Tokenizes StrategicKhaos source code into a stream of tokens.
"""

from typing import List, Optional
from .token_types import Token, TokenType, KEYWORDS


class LexerError(Exception):
    """Exception raised for lexer errors"""
    pass


class Lexer:
    """Lexical analyzer for StrategicKhaos language"""
    
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
    
    def current_char(self) -> Optional[str]:
        """Get the current character without advancing"""
        if self.pos >= len(self.source):
            return None
        return self.source[self.pos]
    
    def peek_char(self, offset: int = 1) -> Optional[str]:
        """Peek at a character ahead without advancing"""
        pos = self.pos + offset
        if pos >= len(self.source):
            return None
        return self.source[pos]
    
    def advance(self) -> Optional[str]:
        """Move to the next character and return current"""
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
        """Skip whitespace characters except newlines"""
        while self.current_char() and self.current_char() in ' \t\r':
            self.advance()
    
    def skip_comment(self):
        """Skip a comment line"""
        if self.current_char() == '#':
            while self.current_char() and self.current_char() != '\n':
                self.advance()
    
    def read_number(self) -> Token:
        """Read a number (integer or float)"""
        start_line = self.line
        start_column = self.column
        num_str = ''
        has_dot = False
        
        char = self.current_char()
        while char and (char.isdigit() or char == '.'):
            if char == '.':
                if has_dot:
                    break  # Second dot, stop here
                has_dot = True
                # Check if next char is a digit (to distinguish from method call)
                next_char = self.peek_char()
                if not next_char or not next_char.isdigit():
                    break
            
            num_str += char
            self.advance()
            char = self.current_char()
        
        if has_dot:
            return Token(TokenType.FLOAT, float(num_str), start_line, start_column)
        else:
            return Token(TokenType.INTEGER, int(num_str), start_line, start_column)
    
    def read_string(self, quote_char: str) -> Token:
        """Read a string literal"""
        start_line = self.line
        start_column = self.column
        self.advance()  # Skip opening quote
        
        string_val = ''
        while self.current_char() and self.current_char() != quote_char:
            if self.current_char() == '\\':
                self.advance()
                # Handle escape sequences
                escape_char = self.current_char()
                if escape_char == 'n':
                    string_val += '\n'
                elif escape_char == 't':
                    string_val += '\t'
                elif escape_char == 'r':
                    string_val += '\r'
                elif escape_char == '\\':
                    string_val += '\\'
                elif escape_char == quote_char:
                    string_val += quote_char
                else:
                    string_val += escape_char
                self.advance()
            else:
                string_val += self.current_char()
                self.advance()
        
        if not self.current_char():
            raise LexerError(f"Unterminated string at line {start_line}, column {start_column}")
        
        self.advance()  # Skip closing quote
        return Token(TokenType.STRING, string_val, start_line, start_column)
    
    def read_identifier(self) -> Token:
        """Read an identifier or keyword"""
        start_line = self.line
        start_column = self.column
        identifier = ''
        
        while self.current_char() and (self.current_char().isalnum() or self.current_char() == '_'):
            identifier += self.current_char()
            self.advance()
        
        # Check if it's a keyword
        token_type = KEYWORDS.get(identifier, TokenType.IDENTIFIER)
        
        # For boolean keywords, set appropriate value
        if token_type == TokenType.TRUE:
            return Token(token_type, True, start_line, start_column)
        elif token_type == TokenType.FALSE:
            return Token(token_type, False, start_line, start_column)
        
        return Token(token_type, identifier, start_line, start_column)
    
    def tokenize(self) -> List[Token]:
        """Tokenize the entire source code"""
        while self.pos < len(self.source):
            self.skip_whitespace()
            
            char = self.current_char()
            if not char:
                break
            
            # Skip comments
            if char == '#':
                self.skip_comment()
                continue
            
            # Newlines (significant in some contexts)
            if char == '\n':
                # For now, skip newlines (we use semicolons for statement separation)
                self.advance()
                continue
            
            # Numbers
            if char.isdigit():
                self.tokens.append(self.read_number())
                continue
            
            # Strings
            if char in ('"', "'"):
                self.tokens.append(self.read_string(char))
                continue
            
            # Identifiers and keywords
            if char.isalpha() or char == '_':
                self.tokens.append(self.read_identifier())
                continue
            
            # Operators and punctuation
            line = self.line
            column = self.column
            
            # Two-character operators
            if char == '=' and self.peek_char() == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.EQUAL, '==', line, column))
                continue
            
            if char == '!' and self.peek_char() == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.NOT_EQUAL, '!=', line, column))
                continue
            
            if char == '<' and self.peek_char() == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.LESS_EQUAL, '<=', line, column))
                continue
            
            if char == '>' and self.peek_char() == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.GREATER_EQUAL, '>=', line, column))
                continue
            
            if char == '+' and self.peek_char() == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.PLUS_ASSIGN, '+=', line, column))
                continue
            
            if char == '-' and self.peek_char() == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.MINUS_ASSIGN, '-=', line, column))
                continue
            
            if char == '-' and self.peek_char() == '>':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.ARROW, '->', line, column))
                continue
            
            if char == '*' and self.peek_char() == '*':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.POWER, '**', line, column))
                continue
            
            # Single-character operators
            single_char_tokens = {
                '+': TokenType.PLUS,
                '-': TokenType.MINUS,
                '*': TokenType.MULTIPLY,
                '/': TokenType.DIVIDE,
                '%': TokenType.MODULO,
                '=': TokenType.ASSIGN,
                '<': TokenType.LESS,
                '>': TokenType.GREATER,
                '(': TokenType.LPAREN,
                ')': TokenType.RPAREN,
                '{': TokenType.LBRACE,
                '}': TokenType.RBRACE,
                '[': TokenType.LBRACKET,
                ']': TokenType.RBRACKET,
                ';': TokenType.SEMICOLON,
                ':': TokenType.COLON,
                ',': TokenType.COMMA,
                '.': TokenType.DOT,
                '@': TokenType.AT,
            }
            
            if char in single_char_tokens:
                self.advance()
                self.tokens.append(Token(single_char_tokens[char], char, line, column))
                continue
            
            # Unknown character
            raise LexerError(f"Unknown character '{char}' at line {line}, column {column}")
        
        # Add EOF token
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens
