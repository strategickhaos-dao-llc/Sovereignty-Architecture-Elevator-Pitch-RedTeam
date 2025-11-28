"""
Token definitions for StrategicKhaos lexer.
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import Any, Optional


class TokenType(Enum):
    """Token types for the StrategicKhaos language."""
    # Structural
    LPAREN = auto()      # (
    RPAREN = auto()      # )
    
    # Literals
    NUMBER = auto()      # 42, 3.14
    STRING = auto()      # "hello"
    SYMBOL = auto()      # print, +, define
    
    # Special
    COMMENT = auto()     # ; comment
    EOF = auto()         # End of file
    NEWLINE = auto()     # \n
    
    def __repr__(self):
        return f'TokenType.{self.name}'


@dataclass
class Token:
    """
    Represents a token in the source code.
    
    Attributes:
        type: The type of token
        value: The actual value of the token
        line: Line number (1-indexed)
        column: Column number (1-indexed)
    """
    type: TokenType
    value: Any
    line: int
    column: int
    
    def __repr__(self):
        if self.value is not None:
            return f'Token({self.type.name}, {self.value!r}, {self.line}:{self.column})'
        return f'Token({self.type.name}, {self.line}:{self.column})'
    
    def __str__(self):
        return self.__repr__()
