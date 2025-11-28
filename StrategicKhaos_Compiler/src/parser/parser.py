"""
Parser implementation for StrategicKhaos.
Converts a stream of tokens into an Abstract Syntax Tree.
"""

from typing import List, Optional
from ..lexer.tokens import Token, TokenType
from ..ast.nodes import ASTNode, NumberNode, StringNode, SymbolNode, ListNode


class ParserError(Exception):
    """Exception raised for parser errors."""
    def __init__(self, message: str, token: Optional[Token] = None):
        self.message = message
        self.token = token
        if token:
            super().__init__(f"Parser error at {token.line}:{token.column}: {message}")
        else:
            super().__init__(f"Parser error: {message}")


class Parser:
    """
    Parser for StrategicKhaos language.
    
    Parses S-expressions into an Abstract Syntax Tree.
    """
    
    def __init__(self, tokens: List[Token]):
        """
        Initialize the parser with a list of tokens.
        
        Args:
            tokens: List of tokens from the lexer
        """
        self.tokens = tokens
        self.pos = 0
    
    def current_token(self) -> Optional[Token]:
        """Return the current token or None if at end."""
        if self.pos >= len(self.tokens):
            return None
        return self.tokens[self.pos]
    
    def peek_token(self, offset: int = 1) -> Optional[Token]:
        """Look ahead at a token without consuming it."""
        pos = self.pos + offset
        if pos >= len(self.tokens):
            return None
        return self.tokens[pos]
    
    def advance(self) -> Optional[Token]:
        """Move to the next token and return it."""
        token = self.current_token()
        self.pos += 1
        return token
    
    def expect(self, token_type: TokenType) -> Token:
        """
        Expect a specific token type and consume it.
        
        Args:
            token_type: The expected token type
        
        Returns:
            The consumed token
        
        Raises:
            ParserError: If the current token doesn't match
        """
        token = self.current_token()
        if not token or token.type != token_type:
            expected = token_type.name
            actual = token.type.name if token else "EOF"
            raise ParserError(f"Expected {expected}, got {actual}", token)
        return self.advance()
    
    def parse_atom(self) -> ASTNode:
        """
        Parse an atomic expression (number, string, or symbol).
        
        Returns:
            An ASTNode representing the atom
        
        Raises:
            ParserError: If an unexpected token is encountered
        """
        token = self.current_token()
        
        if not token or token.type == TokenType.EOF:
            raise ParserError("Unexpected end of input")
        
        if token.type == TokenType.NUMBER:
            self.advance()
            return NumberNode(token.value)
        
        if token.type == TokenType.STRING:
            self.advance()
            return StringNode(token.value)
        
        if token.type == TokenType.SYMBOL:
            self.advance()
            return SymbolNode(token.value)
        
        raise ParserError(f"Unexpected token: {token.type.name}", token)
    
    def parse_list(self) -> ListNode:
        """
        Parse a list (S-expression).
        
        Returns:
            A ListNode containing the parsed elements
        
        Raises:
            ParserError: If the list is malformed
        """
        # Expect opening parenthesis
        self.expect(TokenType.LPAREN)
        
        elements = []
        
        # Parse elements until we hit closing parenthesis
        while self.current_token() and self.current_token().type != TokenType.RPAREN:
            elements.append(self.parse_expression())
        
        # Expect closing parenthesis
        self.expect(TokenType.RPAREN)
        
        return ListNode(elements)
    
    def parse_expression(self) -> ASTNode:
        """
        Parse an expression (atom or list).
        
        Returns:
            An ASTNode representing the expression
        
        Raises:
            ParserError: If the expression is malformed
        """
        token = self.current_token()
        
        if not token or token.type == TokenType.EOF:
            raise ParserError("Unexpected end of input")
        
        if token.type == TokenType.LPAREN:
            return self.parse_list()
        else:
            return self.parse_atom()
    
    def parse(self) -> List[ASTNode]:
        """
        Parse all expressions in the token stream.
        
        Returns:
            A list of ASTNodes representing the program
        
        Raises:
            ParserError: If the input is malformed
        """
        expressions = []
        
        while self.current_token() and self.current_token().type != TokenType.EOF:
            expressions.append(self.parse_expression())
        
        return expressions
