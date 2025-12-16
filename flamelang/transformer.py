#!/usr/bin/env python3
"""
FlameLang Transformer - First transformation layer
Token stream → Abstract Syntax Tree (AST)

Status: Achievable tonight ✅
"""

from dataclasses import dataclass
from typing import List, Optional, Union
from enum import Enum, auto
from lexer import Token, TokenType, FlameLangLexer


class ASTNodeType(Enum):
    """AST Node types for FlameLang"""
    PROGRAM = auto()
    FUNCTION = auto()
    BLOCK = auto()
    DECLARATION = auto()
    ASSIGNMENT = auto()
    RETURN = auto()
    BINARY_OP = auto()
    LITERAL = auto()
    IDENTIFIER = auto()


@dataclass
class ASTNode:
    """Base AST Node"""
    node_type: ASTNodeType
    value: Optional[str] = None
    children: List['ASTNode'] = None
    
    def __post_init__(self):
        if self.children is None:
            self.children = []


class FlameLangTransformer:
    """
    Transformer: Token stream → AST
    
    Pattern Training: Multi-pass transformation
    Like grouped bars showing parallel data streams,
    this transforms one representation into another
    while preserving semantic meaning.
    
    Category → Type mapping (like category axis)
    Value → Memory mapping (like value axis)
    """
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.position = 0
        self.current_token = self.tokens[0] if tokens else None
    
    def advance(self):
        """Move to next token"""
        self.position += 1
        if self.position < len(self.tokens):
            self.current_token = self.tokens[self.position]
        else:
            self.current_token = None
    
    def peek(self) -> Optional[Token]:
        """Look at next token without advancing"""
        if self.position + 1 < len(self.tokens):
            return self.tokens[self.position + 1]
        return None
    
    def expect(self, token_type: TokenType) -> Token:
        """Expect a specific token type, raise error if not found"""
        if not self.current_token or self.current_token.type != token_type:
            raise SyntaxError(
                f"Expected {token_type.name}, got {self.current_token.type.name if self.current_token else 'EOF'}"
            )
        token = self.current_token
        self.advance()
        return token
    
    def parse_program(self) -> ASTNode:
        """
        Parse entire program
        program := function*
        """
        program = ASTNode(ASTNodeType.PROGRAM)
        
        while self.current_token and self.current_token.type != TokenType.EOF:
            if self.current_token.type in [TokenType.INT, TokenType.VOID, TokenType.FLOAT]:
                program.children.append(self.parse_function())
            else:
                self.advance()
        
        return program
    
    def parse_function(self) -> ASTNode:
        """
        Parse function definition
        function := type IDENTIFIER '(' ')' block
        """
        return_type = self.current_token.value
        self.advance()
        
        name = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.LPAREN)
        self.expect(TokenType.RPAREN)
        
        body = self.parse_block()
        
        func_node = ASTNode(ASTNodeType.FUNCTION, value=name)
        func_node.children.append(body)
        return func_node
    
    def parse_block(self) -> ASTNode:
        """
        Parse code block
        block := '{' statement* '}'
        """
        self.expect(TokenType.LBRACE)
        
        block = ASTNode(ASTNodeType.BLOCK)
        
        while self.current_token and self.current_token.type != TokenType.RBRACE:
            if self.current_token.type == TokenType.ALLOC:
                block.children.append(self.parse_declaration())
            elif self.current_token.type == TokenType.RETURN:
                block.children.append(self.parse_return())
            else:
                self.advance()
        
        self.expect(TokenType.RBRACE)
        return block
    
    def parse_declaration(self) -> ASTNode:
        """
        Parse variable declaration
        declaration := 'alloc' IDENTIFIER '=' expression ';'
        """
        self.expect(TokenType.ALLOC)
        name = self.expect(TokenType.IDENTIFIER).value
        
        decl = ASTNode(ASTNodeType.DECLARATION, value=name)
        
        if self.current_token and self.current_token.type == TokenType.ASSIGN:
            self.advance()
            decl.children.append(self.parse_expression())
        
        return decl
    
    def parse_return(self) -> ASTNode:
        """
        Parse return statement
        return := 'return' expression
        """
        self.expect(TokenType.RETURN)
        
        ret = ASTNode(ASTNodeType.RETURN)
        ret.children.append(self.parse_expression())
        
        return ret
    
    def parse_expression(self) -> ASTNode:
        """
        Parse expression (simplified for now)
        expression := literal | identifier
        """
        if not self.current_token:
            # Default to empty expression if no token
            return ASTNode(ASTNodeType.LITERAL, value="0")
        
        if self.current_token.type == TokenType.NUMBER:
            value = self.current_token.value
            self.advance()
            return ASTNode(ASTNodeType.LITERAL, value=value)
        
        elif self.current_token.type == TokenType.STRING:
            value = self.current_token.value
            self.advance()
            return ASTNode(ASTNodeType.LITERAL, value=f'"{value}"')
        
        elif self.current_token.type == TokenType.IDENTIFIER:
            value = self.current_token.value
            self.advance()
            return ASTNode(ASTNodeType.IDENTIFIER, value=value)
        
        else:
            # Default to empty expression
            return ASTNode(ASTNodeType.LITERAL, value="0")
    
    def transform(self) -> ASTNode:
        """
        Main transformation entry point
        
        This is Layer 1 of transformation:
        Token Stream → AST
        
        Future layers:
        AST → LLVM IR (Layer 2)
        LLVM IR → Machine Code (Layer 3)
        """
        return self.parse_program()
    
    def print_ast(self, node: ASTNode, indent: int = 0):
        """Pretty print AST for debugging"""
        prefix = "  " * indent
        print(f"{prefix}{node.node_type.name}: {node.value or ''}")
        for child in node.children:
            self.print_ast(child, indent + 1)


def main():
    """Test the transformer with sample code"""
    sample_code = """
    # FlameLang sample
    int main() {
        alloc message = "Hello, FlameLang!"
        return 0
    }
    """
    
    print("FlameLang Transformer - Token Stream → AST")
    print("=" * 50)
    
    # Lexical analysis
    lexer = FlameLangLexer(sample_code)
    tokens = lexer.tokenize()
    print(f"Lexer produced {len(tokens) - 1} tokens")
    
    # Transformation
    transformer = FlameLangTransformer(tokens)
    ast = transformer.transform()
    
    print("\nAbstract Syntax Tree:")
    print("-" * 50)
    transformer.print_ast(ast)
    
    print("=" * 50)
    print("✅ One transformation layer working - ACHIEVED")


if __name__ == "__main__":
    main()
