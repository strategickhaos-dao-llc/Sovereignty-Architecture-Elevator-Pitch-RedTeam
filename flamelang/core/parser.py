"""
FlameLang Parser
Builds Abstract Syntax Tree (AST) from tokens
"""

from dataclasses import dataclass
from typing import List, Optional, Any
from .lexer import Token, TokenType


# AST Node Types
@dataclass
class ASTNode:
    """Base class for all AST nodes"""
    pass


@dataclass
class NumberNode(ASTNode):
    """Represents a numeric literal"""
    value: float | int


@dataclass
class StringNode(ASTNode):
    """Represents a string literal"""
    value: str


@dataclass
class IdentifierNode(ASTNode):
    """Represents an identifier"""
    name: str


@dataclass
class GlyphNode(ASTNode):
    """Represents a glyph with frequency metadata"""
    symbol: str
    frequency: Optional[int]


@dataclass
class BinaryOpNode(ASTNode):
    """Represents a binary operation"""
    left: ASTNode
    operator: str
    right: ASTNode


@dataclass
class UnaryOpNode(ASTNode):
    """Represents a unary operation"""
    operator: str
    operand: ASTNode


@dataclass
class AssignmentNode(ASTNode):
    """Represents variable assignment"""
    name: str
    value: ASTNode


@dataclass
class FunctionCallNode(ASTNode):
    """Represents a function call"""
    name: str
    arguments: List[ASTNode]


@dataclass
class PhysicsOpNode(ASTNode):
    """Represents a physics operation (schwarzschild, geodesic, etc.)"""
    operation: str
    arguments: List[ASTNode]


@dataclass
class SovereigntyOpNode(ASTNode):
    """Represents a sovereignty operation (isolate, monitor, etc.)"""
    operation: str
    arguments: List[ASTNode]


@dataclass
class ProgramNode(ASTNode):
    """Represents the entire program"""
    statements: List[ASTNode]


class Parser:
    """
    Recursive descent parser for FlameLang
    Builds an Abstract Syntax Tree from tokens
    """
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.position = 0
    
    def current_token(self) -> Optional[Token]:
        """Get the current token"""
        if self.position >= len(self.tokens):
            return None
        return self.tokens[self.position]
    
    def peek_token(self, offset: int = 1) -> Optional[Token]:
        """Peek ahead at a token"""
        pos = self.position + offset
        if pos >= len(self.tokens):
            return None
        return self.tokens[pos]
    
    def advance(self):
        """Move to the next token"""
        self.position += 1
    
    def expect(self, token_type: TokenType) -> Token:
        """Expect a specific token type and consume it"""
        token = self.current_token()
        if not token or token.type != token_type:
            raise SyntaxError(f"Expected {token_type}, got {token.type if token else 'EOF'}")
        self.advance()
        return token
    
    def skip_newlines(self):
        """Skip any newline tokens"""
        while self.current_token() and self.current_token().type == TokenType.NEWLINE:
            self.advance()
    
    def parse(self) -> ProgramNode:
        """Parse the entire program"""
        statements = []
        
        while self.current_token() and self.current_token().type != TokenType.EOF:
            self.skip_newlines()
            if self.current_token() and self.current_token().type != TokenType.EOF:
                stmt = self.parse_statement()
                if stmt:
                    statements.append(stmt)
            self.skip_newlines()
        
        return ProgramNode(statements)
    
    def parse_statement(self) -> Optional[ASTNode]:
        """Parse a single statement"""
        token = self.current_token()
        
        if not token:
            return None
        
        # Variable assignment (let x = ...)
        if token.type in (TokenType.LET, TokenType.CONST):
            self.advance()
            name_token = self.expect(TokenType.IDENTIFIER)
            self.expect(TokenType.ASSIGN)
            value = self.parse_expression()
            return AssignmentNode(name_token.value, value)
        
        # Physics operations
        if token.type in (TokenType.SCHWARZSCHILD, TokenType.GEODESIC, 
                         TokenType.TENSOR, TokenType.EDDY):
            operation = token.value
            self.advance()
            args = self.parse_function_args()
            return PhysicsOpNode(operation, args)
        
        # Sovereignty operations
        if token.type in (TokenType.ISOLATE, TokenType.MONITOR, 
                         TokenType.HARDEN, TokenType.AUDIT):
            operation = token.value
            self.advance()
            args = self.parse_function_args()
            return SovereigntyOpNode(operation, args)
        
        # Expression statement
        return self.parse_expression()
    
    def parse_expression(self) -> ASTNode:
        """Parse an expression"""
        return self.parse_additive()
    
    def parse_additive(self) -> ASTNode:
        """Parse addition and subtraction"""
        left = self.parse_multiplicative()
        
        while self.current_token() and self.current_token().type in (TokenType.PLUS, TokenType.MINUS):
            op_token = self.current_token()
            self.advance()
            right = self.parse_multiplicative()
            left = BinaryOpNode(left, op_token.value, right)
        
        return left
    
    def parse_multiplicative(self) -> ASTNode:
        """Parse multiplication and division"""
        left = self.parse_unary()
        
        while self.current_token() and self.current_token().type in (TokenType.MULTIPLY, TokenType.DIVIDE):
            op_token = self.current_token()
            self.advance()
            right = self.parse_unary()
            left = BinaryOpNode(left, op_token.value, right)
        
        return left
    
    def parse_unary(self) -> ASTNode:
        """Parse unary operations"""
        if self.current_token() and self.current_token().type in (TokenType.PLUS, TokenType.MINUS):
            op_token = self.current_token()
            self.advance()
            operand = self.parse_unary()
            return UnaryOpNode(op_token.value, operand)
        
        return self.parse_primary()
    
    def parse_primary(self) -> ASTNode:
        """Parse primary expressions"""
        token = self.current_token()
        
        if not token:
            raise SyntaxError("Unexpected end of input")
        
        # Numbers
        if token.type == TokenType.NUMBER:
            self.advance()
            return NumberNode(token.value)
        
        # Strings
        if token.type == TokenType.STRING:
            self.advance()
            return StringNode(token.value)
        
        # Glyphs
        if token.type == TokenType.GLYPH:
            self.advance()
            return GlyphNode(token.value, token.frequency)
        
        # Identifiers (variables or function calls)
        if token.type == TokenType.IDENTIFIER:
            name = token.value
            self.advance()
            
            # Check for function call
            if self.current_token() and self.current_token().type == TokenType.LPAREN:
                args = self.parse_function_args()
                return FunctionCallNode(name, args)
            
            return IdentifierNode(name)
        
        # Parenthesized expressions
        if token.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr
        
        raise SyntaxError(f"Unexpected token: {token}")
    
    def parse_function_args(self) -> List[ASTNode]:
        """Parse function arguments"""
        args = []
        
        self.expect(TokenType.LPAREN)
        
        while self.current_token() and self.current_token().type != TokenType.RPAREN:
            args.append(self.parse_expression())
            
            if self.current_token() and self.current_token().type == TokenType.COMMA:
                self.advance()
        
        self.expect(TokenType.RPAREN)
        return args
