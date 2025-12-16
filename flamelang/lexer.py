#!/usr/bin/env python3
"""
FlameLang Lexer - Layer 5 DNA Implementation
Parsing FlameLang glyphs into tokens

Concept: 64 codons → 64 opcodes
Status: Achievable tonight ✅
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional


class TokenType(Enum):
    """Token types for FlameLang - inspired by 64 codon system"""
    
    # Structural
    GLYPH = auto()          # FlameLang glyph symbol
    IDENTIFIER = auto()     # Variable/function names
    NUMBER = auto()         # Numeric literals
    STRING = auto()         # String literals
    
    # Operators (first 16 codons)
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    ASSIGN = auto()
    
    # Control flow (next 16 codons)
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    RETURN = auto()
    
    # Memory operations (next 16 codons)
    ALLOC = auto()
    FREE = auto()
    LOAD = auto()
    STORE = auto()
    
    # Type system (next 16 codons)
    INT = auto()
    FLOAT = auto()
    BOOL = auto()
    VOID = auto()
    
    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    SEMICOLON = auto()
    COMMA = auto()
    
    # Special
    EOF = auto()
    UNKNOWN = auto()


@dataclass
class Token:
    """A lexical token from FlameLang source"""
    type: TokenType
    value: str
    line: int
    column: int


class FlameLangLexer:
    """
    Lexer for FlameLang - parsing glyphs into tokens
    
    Pattern Training: This lexer applies the same categorical logic
    as grouped bar charts:
    - Category axis = Token types (discrete classification)
    - Value axis = Position in source (quantitative measure)
    - Grouped bars = Token sequences (parallel streams)
    """
    
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
        
        # Keywords mapping
        self.keywords = {
            'if': TokenType.IF,
            'else': TokenType.ELSE,
            'while': TokenType.WHILE,
            'for': TokenType.FOR,
            'return': TokenType.RETURN,
            'alloc': TokenType.ALLOC,
            'free': TokenType.FREE,
            'load': TokenType.LOAD,
            'store': TokenType.STORE,
            'int': TokenType.INT,
            'float': TokenType.FLOAT,
            'bool': TokenType.BOOL,
            'void': TokenType.VOID,
        }
        
        # Operator mapping
        self.operators = {
            '+': TokenType.PLUS,
            '-': TokenType.MINUS,
            '*': TokenType.MULTIPLY,
            '/': TokenType.DIVIDE,
            '=': TokenType.ASSIGN,
            '(': TokenType.LPAREN,
            ')': TokenType.RPAREN,
            '{': TokenType.LBRACE,
            '}': TokenType.RBRACE,
            ';': TokenType.SEMICOLON,
            ',': TokenType.COMMA,
        }
    
    def current_char(self) -> Optional[str]:
        """Get current character or None if at end"""
        if self.position >= len(self.source):
            return None
        return self.source[self.position]
    
    def peek_char(self) -> Optional[str]:
        """Peek at next character without advancing"""
        if self.position + 1 >= len(self.source):
            return None
        return self.source[self.position + 1]
    
    def advance(self):
        """Move to next character"""
        if self.current_char() == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        self.position += 1
    
    def skip_whitespace(self):
        """Skip whitespace characters"""
        while self.current_char() and self.current_char().isspace():
            self.advance()
    
    def skip_comment(self):
        """Skip single-line comments starting with #"""
        if self.current_char() == '#':
            while self.current_char() and self.current_char() != '\n':
                self.advance()
    
    def read_number(self) -> Token:
        """Read numeric literal"""
        start_line = self.line
        start_col = self.column
        num_str = ''
        
        while self.current_char() and (self.current_char().isdigit() or self.current_char() == '.'):
            num_str += self.current_char()
            self.advance()
        
        return Token(TokenType.NUMBER, num_str, start_line, start_col)
    
    def read_identifier(self) -> Token:
        """Read identifier or keyword"""
        start_line = self.line
        start_col = self.column
        ident_str = ''
        
        while self.current_char() and (self.current_char().isalnum() or self.current_char() == '_'):
            ident_str += self.current_char()
            self.advance()
        
        # Check if it's a keyword
        token_type = self.keywords.get(ident_str, TokenType.IDENTIFIER)
        return Token(token_type, ident_str, start_line, start_col)
    
    def read_string(self) -> Token:
        """Read string literal"""
        start_line = self.line
        start_col = self.column
        string_val = ''
        
        # Skip opening quote
        self.advance()
        
        while self.current_char() and self.current_char() != '"':
            if self.current_char() == '\\':
                self.advance()
                if self.current_char():
                    string_val += self.current_char()
                    self.advance()
            else:
                string_val += self.current_char()
                self.advance()
        
        # Skip closing quote
        if self.current_char() == '"':
            self.advance()
        
        return Token(TokenType.STRING, string_val, start_line, start_col)
    
    def tokenize(self) -> List[Token]:
        """
        Tokenize the entire source
        
        Multi-pass transformation (like grouped bars):
        Pass 1: Character stream → Token stream
        Future: Pass 2: Token stream → AST
        Future: Pass 3: AST → LLVM IR
        """
        while self.current_char():
            self.skip_whitespace()
            
            if not self.current_char():
                break
            
            # Skip comments
            if self.current_char() == '#':
                self.skip_comment()
                continue
            
            # Numbers
            if self.current_char().isdigit():
                self.tokens.append(self.read_number())
                continue
            
            # Identifiers and keywords
            if self.current_char().isalpha() or self.current_char() == '_':
                self.tokens.append(self.read_identifier())
                continue
            
            # Strings
            if self.current_char() == '"':
                self.tokens.append(self.read_string())
                continue
            
            # Operators and delimiters
            char = self.current_char()
            if char in self.operators:
                token_type = self.operators[char]
                self.tokens.append(Token(token_type, char, self.line, self.column))
                self.advance()
                continue
            
            # Unknown character
            self.tokens.append(Token(TokenType.UNKNOWN, char, self.line, self.column))
            self.advance()
        
        # Add EOF token
        self.tokens.append(Token(TokenType.EOF, '', self.line, self.column))
        return self.tokens


def main():
    """Test the lexer with sample FlameLang code"""
    sample_code = """
    # FlameLang sample - Hello World
    int main() {
        alloc message = "Hello, FlameLang!"
        return 0
    }
    """
    
    lexer = FlameLangLexer(sample_code)
    tokens = lexer.tokenize()
    
    print("FlameLang Lexer - Token Stream:")
    print("=" * 50)
    for token in tokens:
        if token.type != TokenType.EOF:
            print(f"{token.type.name:12} | {token.value:20} | Line {token.line}, Col {token.column}")
    print("=" * 50)
    print(f"Total tokens: {len(tokens) - 1}")  # Exclude EOF
    print("\n✅ Lexer parsing FlameLang glyphs - ACHIEVED")


if __name__ == "__main__":
    main()
