"""
Lexer implementation for StrategicKhaos.
Converts source code into a stream of tokens.
"""

from typing import List, Optional
from .tokens import Token, TokenType


class LexerError(Exception):
    """Exception raised for lexer errors."""
    def __init__(self, message: str, line: int, column: int):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"Lexer error at {line}:{column}: {message}")


class Lexer:
    """
    Tokenizer for StrategicKhaos source code.
    
    Supports:
    - S-expressions (parentheses)
    - Numbers (integers and floats)
    - Strings (double-quoted)
    - Symbols (identifiers and operators)
    - Comments (semicolon to end of line)
    """
    
    def __init__(self, source: str):
        """
        Initialize the lexer with source code.
        
        Args:
            source: The source code string to tokenize
        """
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
    
    def current_char(self) -> Optional[str]:
        """Return the current character or None if at end."""
        if self.pos >= len(self.source):
            return None
        return self.source[self.pos]
    
    def peek_char(self, offset: int = 1) -> Optional[str]:
        """Look ahead at a character without consuming it."""
        pos = self.pos + offset
        if pos >= len(self.source):
            return None
        return self.source[pos]
    
    def advance(self) -> Optional[str]:
        """Move to the next character and return it."""
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
        """Skip whitespace characters except newlines."""
        while self.current_char() and self.current_char() in ' \t\r':
            self.advance()
    
    def skip_comment(self):
        """Skip a comment (from ; to end of line)."""
        if self.current_char() == ';':
            while self.current_char() and self.current_char() != '\n':
                self.advance()
    
    def read_number(self) -> Token:
        """Read a number (integer or float)."""
        start_line = self.line
        start_column = self.column
        num_str = ''
        has_dot = False
        
        while self.current_char() and (self.current_char().isdigit() or self.current_char() == '.'):
            if self.current_char() == '.':
                if has_dot:
                    raise LexerError("Invalid number: multiple decimal points", self.line, self.column)
                has_dot = True
            num_str += self.current_char()
            self.advance()
        
        try:
            value = float(num_str) if has_dot else int(num_str)
            return Token(TokenType.NUMBER, value, start_line, start_column)
        except ValueError:
            raise LexerError(f"Invalid number: {num_str}", start_line, start_column)
    
    def read_string(self) -> Token:
        """Read a string literal (double-quoted)."""
        start_line = self.line
        start_column = self.column
        
        # Skip opening quote
        self.advance()
        
        string_value = ''
        while self.current_char() and self.current_char() != '"':
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
                elif escape_char == '"':
                    string_value += '"'
                else:
                    string_value += escape_char
                self.advance()
            else:
                string_value += self.current_char()
                self.advance()
        
        if not self.current_char():
            raise LexerError("Unterminated string", start_line, start_column)
        
        # Skip closing quote
        self.advance()
        
        return Token(TokenType.STRING, string_value, start_line, start_column)
    
    def read_symbol(self) -> Token:
        """Read a symbol (identifier or operator)."""
        start_line = self.line
        start_column = self.column
        symbol_str = ''
        
        # Symbols can contain letters, digits, and special characters
        # but cannot start with a digit
        valid_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-*/=<>!?_')
        
        while self.current_char() and self.current_char() in valid_chars:
            symbol_str += self.current_char()
            self.advance()
        
        return Token(TokenType.SYMBOL, symbol_str, start_line, start_column)
    
    def tokenize(self) -> List[Token]:
        """
        Tokenize the entire source code.
        
        Returns:
            List of tokens
        
        Raises:
            LexerError: If an invalid character or construct is encountered
        """
        self.tokens = []
        
        while self.current_char():
            # Skip whitespace
            if self.current_char() in ' \t\r':
                self.skip_whitespace()
                continue
            
            # Handle newlines
            if self.current_char() == '\n':
                self.advance()
                continue
            
            # Handle comments
            if self.current_char() == ';':
                self.skip_comment()
                continue
            
            # Handle left parenthesis
            if self.current_char() == '(':
                token = Token(TokenType.LPAREN, '(', self.line, self.column)
                self.tokens.append(token)
                self.advance()
                continue
            
            # Handle right parenthesis
            if self.current_char() == ')':
                token = Token(TokenType.RPAREN, ')', self.line, self.column)
                self.tokens.append(token)
                self.advance()
                continue
            
            # Handle numbers
            if self.current_char().isdigit():
                self.tokens.append(self.read_number())
                continue
            
            # Handle strings
            if self.current_char() == '"':
                self.tokens.append(self.read_string())
                continue
            
            # Handle symbols
            if self.current_char().isalpha() or self.current_char() in '+-*/=<>!?_':
                self.tokens.append(self.read_symbol())
                continue
            
            # Unknown character
            raise LexerError(f"Unexpected character: {self.current_char()!r}", self.line, self.column)
        
        # Add EOF token
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        
        return self.tokens
