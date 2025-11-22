"""
AST node definitions for StrategicKhaos.
"""

from abc import ABC, abstractmethod
from typing import Any, List
from dataclasses import dataclass


class ASTNode(ABC):
    """Base class for all AST nodes."""
    
    @abstractmethod
    def __repr__(self):
        pass


@dataclass
class NumberNode(ASTNode):
    """Represents a numeric literal."""
    value: float
    
    def __repr__(self):
        return f'NumberNode({self.value})'


@dataclass
class StringNode(ASTNode):
    """Represents a string literal."""
    value: str
    
    def __repr__(self):
        return f'StringNode({self.value!r})'


@dataclass
class SymbolNode(ASTNode):
    """Represents a symbol (identifier or operator)."""
    name: str
    
    def __repr__(self):
        return f'SymbolNode({self.name!r})'


@dataclass
class ListNode(ASTNode):
    """Represents a list (S-expression)."""
    elements: List[ASTNode]
    
    def __repr__(self):
        elements_repr = ', '.join(repr(e) for e in self.elements)
        return f'ListNode([{elements_repr}])'
    
    def is_call(self) -> bool:
        """Check if this list represents a function call."""
        return len(self.elements) > 0 and isinstance(self.elements[0], SymbolNode)
    
    def get_function_name(self) -> str:
        """Get the function name if this is a function call."""
        if self.is_call():
            return self.elements[0].name
        return None
    
    def get_arguments(self) -> List[ASTNode]:
        """Get the arguments if this is a function call."""
        if self.is_call():
            return self.elements[1:]
        return []
