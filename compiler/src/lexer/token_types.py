"""
Token Types for StrategicKhaos Language

Defines all token types recognized by the lexer.
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import Any, Optional


class TokenType(Enum):
    """All token types in the StrategicKhaos language"""
    
    # Literals
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()
    TRUE = auto()
    FALSE = auto()
    
    # Identifiers and Keywords
    IDENTIFIER = auto()
    
    # Keywords
    LET = auto()
    CONST = auto()
    FN = auto()
    RETURN = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    IN = auto()
    BREAK = auto()
    CONTINUE = auto()
    PRINT = auto()
    SHOW = auto()
    
    # Neural optimization hints
    OPTIMIZE = auto()
    NEURAL = auto()
    
    # Operators
    PLUS = auto()          # +
    MINUS = auto()         # -
    MULTIPLY = auto()      # *
    DIVIDE = auto()        # /
    MODULO = auto()        # %
    POWER = auto()         # **
    
    # Comparison
    EQUAL = auto()         # ==
    NOT_EQUAL = auto()     # !=
    LESS = auto()          # <
    LESS_EQUAL = auto()    # <=
    GREATER = auto()       # >
    GREATER_EQUAL = auto() # >=
    
    # Logical
    AND = auto()           # and
    OR = auto()            # or
    NOT = auto()           # not
    
    # Assignment
    ASSIGN = auto()        # =
    PLUS_ASSIGN = auto()   # +=
    MINUS_ASSIGN = auto()  # -=
    
    # Delimiters
    LPAREN = auto()        # (
    RPAREN = auto()        # )
    LBRACE = auto()        # {
    RBRACE = auto()        # }
    LBRACKET = auto()      # [
    RBRACKET = auto()      # ]
    
    # Punctuation
    SEMICOLON = auto()     # ;
    COLON = auto()         # :
    COMMA = auto()         # ,
    DOT = auto()           # .
    ARROW = auto()         # ->
    AT = auto()            # @
    
    # Special
    NEWLINE = auto()
    EOF = auto()
    COMMENT = auto()


@dataclass
class Token:
    """A single token from the source code"""
    
    type: TokenType
    value: Any
    line: int
    column: int
    
    def __repr__(self):
        return f"Token({self.type.name}, {repr(self.value)}, {self.line}:{self.column})"
    
    def __str__(self):
        if self.value is not None:
            return f"{self.type.name}({self.value})"
        return self.type.name


# Keywords mapping
KEYWORDS = {
    'let': TokenType.LET,
    'const': TokenType.CONST,
    'fn': TokenType.FN,
    'return': TokenType.RETURN,
    'if': TokenType.IF,
    'else': TokenType.ELSE,
    'while': TokenType.WHILE,
    'for': TokenType.FOR,
    'in': TokenType.IN,
    'break': TokenType.BREAK,
    'continue': TokenType.CONTINUE,
    'print': TokenType.PRINT,
    'show': TokenType.SHOW,
    'true': TokenType.TRUE,
    'false': TokenType.FALSE,
    'and': TokenType.AND,
    'or': TokenType.OR,
    'not': TokenType.NOT,
    'optimize': TokenType.OPTIMIZE,
    'neural': TokenType.NEURAL,
}
