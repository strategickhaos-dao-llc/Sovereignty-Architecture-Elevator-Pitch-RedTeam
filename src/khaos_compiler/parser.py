"""
StrategicKhaos Parser - Stage 0
Parses tokens into an Abstract Syntax Tree (AST)
"""

from dataclasses import dataclass
from typing import List, Optional, Any
from .lexer import Token, TokenType


# AST Node types
@dataclass
class ASTNode:
    pass


@dataclass
class Program(ASTNode):
    statements: List[ASTNode]


@dataclass
class PrintStatement(ASTNode):
    expression: ASTNode


@dataclass
class LetStatement(ASTNode):
    name: str
    value: ASTNode


@dataclass
class StringLiteral(ASTNode):
    value: str


@dataclass
class NumberLiteral(ASTNode):
    value: float


@dataclass
class Identifier(ASTNode):
    name: str


@dataclass
class BinaryOp(ASTNode):
    left: ASTNode
    operator: str
    right: ASTNode


@dataclass
class Lambda(ASTNode):
    params: List[str]
    body: ASTNode


@dataclass
class FunctionCall(ASTNode):
    function: ASTNode
    arguments: List[ASTNode]


@dataclass
class Block(ASTNode):
    statements: List[ASTNode]


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
    
    def error(self, msg: str):
        if self.pos < len(self.tokens):
            token = self.tokens[self.pos]
            raise SyntaxError(f"Parser error at line {token.line}, column {token.column}: {msg}")
        else:
            raise SyntaxError(f"Parser error at end of file: {msg}")
    
    def peek(self, offset: int = 0) -> Optional[Token]:
        pos = self.pos + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return None
    
    def advance(self) -> Token:
        token = self.tokens[self.pos]
        self.pos += 1
        return token
    
    def expect(self, token_type: TokenType) -> Token:
        token = self.peek()
        if not token or token.type != token_type:
            self.error(f"Expected {token_type}, got {token.type if token else 'EOF'}")
        return self.advance()
    
    def skip_newlines(self):
        while self.peek() and self.peek().type == TokenType.NEWLINE:
            self.advance()
    
    def parse(self) -> Program:
        statements = []
        
        while self.peek() and self.peek().type != TokenType.EOF:
            self.skip_newlines()
            if self.peek() and self.peek().type != TokenType.EOF:
                stmt = self.parse_statement()
                if stmt:
                    statements.append(stmt)
            self.skip_newlines()
        
        return Program(statements)
    
    def parse_statement(self) -> Optional[ASTNode]:
        self.skip_newlines()
        token = self.peek()
        
        if not token or token.type == TokenType.EOF:
            return None
        
        if token.type == TokenType.PRINT:
            return self.parse_print()
        elif token.type == TokenType.LET:
            return self.parse_let()
        else:
            # Expression statement
            expr = self.parse_expression()
            self.skip_newlines()
            # Optional semicolon
            if self.peek() and self.peek().type == TokenType.SEMICOLON:
                self.advance()
            return expr
    
    def parse_print(self) -> PrintStatement:
        self.expect(TokenType.PRINT)
        expr = self.parse_expression()
        self.skip_newlines()
        # Optional semicolon
        if self.peek() and self.peek().type == TokenType.SEMICOLON:
            self.advance()
        return PrintStatement(expr)
    
    def parse_let(self) -> LetStatement:
        self.expect(TokenType.LET)
        name_token = self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.EQUALS)
        value = self.parse_expression()
        self.skip_newlines()
        # Optional semicolon
        if self.peek() and self.peek().type == TokenType.SEMICOLON:
            self.advance()
        return LetStatement(name_token.value, value)
    
    def parse_expression(self) -> ASTNode:
        return self.parse_additive()
    
    def parse_additive(self) -> ASTNode:
        left = self.parse_primary()
        
        while self.peek() and self.peek().type == TokenType.PLUS:
            op = self.advance()
            right = self.parse_primary()
            left = BinaryOp(left, op.value, right)
        
        return left
    
    def parse_primary(self) -> ASTNode:
        token = self.peek()
        
        if not token:
            self.error("Unexpected end of input")
        
        # String literal
        if token.type == TokenType.STRING:
            self.advance()
            return StringLiteral(token.value)
        
        # Number literal
        if token.type == TokenType.NUMBER:
            self.advance()
            return NumberLiteral(float(token.value))
        
        # Lambda
        if token.type == TokenType.LAMBDA:
            return self.parse_lambda()
        
        # Identifier or function call
        if token.type == TokenType.IDENTIFIER:
            self.advance()
            identifier = Identifier(token.value)
            
            # Check for function call
            if self.peek() and self.peek().type == TokenType.LPAREN:
                return self.parse_function_call(identifier)
            
            return identifier
        
        # Parenthesized expression
        if token.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr
        
        self.error(f"Unexpected token: {token.type}")
    
    def parse_lambda(self) -> Lambda:
        self.expect(TokenType.LAMBDA)
        self.expect(TokenType.LPAREN)
        
        # Parse parameters
        params = []
        if self.peek() and self.peek().type == TokenType.IDENTIFIER:
            params.append(self.advance().value)
            
            # Handle comma-separated parameters
            while self.peek() and self.peek().type == TokenType.COMMA:
                self.advance()  # consume comma
                if self.peek() and self.peek().type == TokenType.IDENTIFIER:
                    params.append(self.advance().value)
        
        self.expect(TokenType.RPAREN)
        
        # Parse body
        if self.peek() and self.peek().type == TokenType.LBRACE:
            self.advance()
            self.skip_newlines()
            
            # Parse statements in body
            statements = []
            while self.peek() and self.peek().type != TokenType.RBRACE:
                stmt = self.parse_statement()
                if stmt:
                    statements.append(stmt)
                self.skip_newlines()
            
            self.expect(TokenType.RBRACE)
            body = Block(statements)
        else:
            # Single expression body
            body = self.parse_expression()
        
        return Lambda(params, body)
    
    def parse_function_call(self, function: ASTNode) -> FunctionCall:
        self.expect(TokenType.LPAREN)
        
        arguments = []
        if self.peek() and self.peek().type != TokenType.RPAREN:
            arguments.append(self.parse_expression())
            
            # Handle comma-separated arguments
            while self.peek() and self.peek().type == TokenType.COMMA:
                self.advance()  # consume comma
                arguments.append(self.parse_expression())
        
        self.expect(TokenType.RPAREN)
        
        return FunctionCall(function, arguments)
