#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  FLAME LANG PARSER - WhiteCellOS / Pantheon Core Integration                ║
║  Lexical Analysis and AST Generation for Flame Language                      ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Part of the Strategic Khaos Sovereignty Architecture                        ║
║  Author: Domenic Garza / StrategicKhaos DAO LLC                             ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import re
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any


class TokenType(Enum):
    """Token types for Flame Lang lexical analysis."""
    # Literals
    NUMBER = auto()
    STRING = auto()
    IDENTIFIER = auto()
    BOOLEAN = auto()
    
    # Sovereignty Keywords
    IGNITE = auto()      # Function definition
    SPARK = auto()       # Variable declaration
    BLAZE = auto()       # Loop construct
    EMBER = auto()       # Conditional
    FLAME = auto()       # Class/Module definition
    ASH = auto()         # Return statement
    FORGE = auto()       # Import/Module load
    KINDLE = auto()      # Async operation
    INFERNO = auto()     # Exception/Error handling
    EXTINGUISH = auto()  # Exit/Break
    
    # Oath/Sovereignty
    OATH = auto()        # Security assertion
    BEARER = auto()      # Identity/Auth context
    SEAL = auto()        # Cryptographic operation
    
    # Operators
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MODULO = auto()
    ASSIGN = auto()
    EQUALS = auto()
    NOT_EQUALS = auto()
    GREATER = auto()
    LESS = auto()
    GREATER_EQ = auto()
    LESS_EQ = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    ARROW = auto()       # -> for lambdas/returns
    FLAME_ARROW = auto() # ~> for flame chains
    
    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    COMMA = auto()
    COLON = auto()
    SEMICOLON = auto()
    DOT = auto()
    
    # Special
    COMMENT = auto()
    WHITESPACE = auto()
    NEWLINE = auto()
    EOF = auto()


@dataclass
class Token:
    """Represents a lexical token."""
    type: TokenType
    value: Any
    line: int
    column: int


@dataclass
class ASTNode:
    """Base AST node."""
    node_type: str
    children: list = field(default_factory=list)
    value: Any = None
    line: int = 0
    column: int = 0


class FlameLangLexer:
    """
    Lexical analyzer for Flame Lang.
    
    Flame Lang uses sovereignty-themed keywords to represent programming constructs:
    - ignite: Define functions (like def/function)
    - spark: Declare variables (like let/var)
    - blaze: Loop constructs (like for/while)
    - ember: Conditionals (like if/else)
    - flame: Class/module definitions
    - ash: Return statements
    - forge: Import/require modules
    - kindle: Async operations
    - inferno: Exception handling
    """
    
    KEYWORDS = {
        'ignite': TokenType.IGNITE,
        'spark': TokenType.SPARK,
        'blaze': TokenType.BLAZE,
        'ember': TokenType.EMBER,
        'flame': TokenType.FLAME,
        'ash': TokenType.ASH,
        'forge': TokenType.FORGE,
        'kindle': TokenType.KINDLE,
        'inferno': TokenType.INFERNO,
        'extinguish': TokenType.EXTINGUISH,
        'oath': TokenType.OATH,
        'bearer': TokenType.BEARER,
        'seal': TokenType.SEAL,
        'true': TokenType.BOOLEAN,
        'false': TokenType.BOOLEAN,
        'and': TokenType.AND,
        'or': TokenType.OR,
        'not': TokenType.NOT,
    }
    
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: list[Token] = []
    
    def peek(self, offset: int = 0) -> str | None:
        """Peek at character at current position + offset."""
        idx = self.pos + offset
        if idx < len(self.source):
            return self.source[idx]
        return None
    
    def advance(self) -> str | None:
        """Advance position and return current character."""
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
        """Skip whitespace characters."""
        while self.peek() and self.peek() in ' \t\r':
            self.advance()
    
    def skip_comment(self):
        """Skip single-line comments (# or //)."""
        while self.peek() and self.peek() != '\n':
            self.advance()
    
    def read_string(self, quote: str) -> Token:
        """Read a string literal."""
        start_line, start_col = self.line, self.column
        self.advance()  # Skip opening quote
        value = ""
        while self.peek() and self.peek() != quote:
            if self.peek() == '\\' and self.peek(1):
                self.advance()
                escaped = self.advance()
                if escaped == 'n':
                    value += '\n'
                elif escaped == 't':
                    value += '\t'
                elif escaped == '\\':
                    value += '\\'
                elif escaped == quote:
                    value += quote
                else:
                    value += escaped
            else:
                value += self.advance()
        self.advance()  # Skip closing quote
        return Token(TokenType.STRING, value, start_line, start_col)
    
    def read_number(self) -> Token:
        """Read a numeric literal."""
        start_line, start_col = self.line, self.column
        value = ""
        while self.peek() and (self.peek().isdigit() or self.peek() == '.'):
            value += self.advance()
        if '.' in value:
            return Token(TokenType.NUMBER, float(value), start_line, start_col)
        return Token(TokenType.NUMBER, int(value), start_line, start_col)
    
    def read_identifier(self) -> Token:
        """Read an identifier or keyword."""
        start_line, start_col = self.line, self.column
        value = ""
        while self.peek() and (self.peek().isalnum() or self.peek() == '_'):
            value += self.advance()
        token_type = self.KEYWORDS.get(value.lower(), TokenType.IDENTIFIER)
        if token_type == TokenType.BOOLEAN:
            return Token(token_type, value.lower() == 'true', start_line, start_col)
        return Token(token_type, value, start_line, start_col)
    
    def tokenize(self) -> list[Token]:
        """Tokenize the source code."""
        while self.pos < len(self.source):
            char = self.peek()
            
            # Whitespace
            if char in ' \t\r':
                self.skip_whitespace()
                continue
            
            # Newline
            if char == '\n':
                self.tokens.append(Token(TokenType.NEWLINE, '\n', self.line, self.column))
                self.advance()
                continue
            
            # Comments
            if char == '#' or (char == '/' and self.peek(1) == '/'):
                self.skip_comment()
                continue
            
            # Multi-line comments /* */
            if char == '/' and self.peek(1) == '*':
                self.advance()
                self.advance()
                while self.peek() and not (self.peek() == '*' and self.peek(1) == '/'):
                    self.advance()
                self.advance()  # Skip *
                self.advance()  # Skip /
                continue
            
            # String literals
            if char in '"\'':
                self.tokens.append(self.read_string(char))
                continue
            
            # Numbers
            if char.isdigit():
                self.tokens.append(self.read_number())
                continue
            
            # Identifiers and keywords
            if char.isalpha() or char == '_':
                self.tokens.append(self.read_identifier())
                continue
            
            # Operators and delimiters
            start_line, start_col = self.line, self.column
            
            if char == '~' and self.peek(1) == '>':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.FLAME_ARROW, '~>', start_line, start_col))
            elif char == '-' and self.peek(1) == '>':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.ARROW, '->', start_line, start_col))
            elif char == '=' and self.peek(1) == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.EQUALS, '==', start_line, start_col))
            elif char == '!' and self.peek(1) == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.NOT_EQUALS, '!=', start_line, start_col))
            elif char == '>' and self.peek(1) == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.GREATER_EQ, '>=', start_line, start_col))
            elif char == '<' and self.peek(1) == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.LESS_EQ, '<=', start_line, start_col))
            elif char == '+':
                self.advance()
                self.tokens.append(Token(TokenType.PLUS, '+', start_line, start_col))
            elif char == '-':
                self.advance()
                self.tokens.append(Token(TokenType.MINUS, '-', start_line, start_col))
            elif char == '*':
                self.advance()
                self.tokens.append(Token(TokenType.MULTIPLY, '*', start_line, start_col))
            elif char == '/':
                self.advance()
                self.tokens.append(Token(TokenType.DIVIDE, '/', start_line, start_col))
            elif char == '%':
                self.advance()
                self.tokens.append(Token(TokenType.MODULO, '%', start_line, start_col))
            elif char == '=':
                self.advance()
                self.tokens.append(Token(TokenType.ASSIGN, '=', start_line, start_col))
            elif char == '>':
                self.advance()
                self.tokens.append(Token(TokenType.GREATER, '>', start_line, start_col))
            elif char == '<':
                self.advance()
                self.tokens.append(Token(TokenType.LESS, '<', start_line, start_col))
            elif char == '(':
                self.advance()
                self.tokens.append(Token(TokenType.LPAREN, '(', start_line, start_col))
            elif char == ')':
                self.advance()
                self.tokens.append(Token(TokenType.RPAREN, ')', start_line, start_col))
            elif char == '{':
                self.advance()
                self.tokens.append(Token(TokenType.LBRACE, '{', start_line, start_col))
            elif char == '}':
                self.advance()
                self.tokens.append(Token(TokenType.RBRACE, '}', start_line, start_col))
            elif char == '[':
                self.advance()
                self.tokens.append(Token(TokenType.LBRACKET, '[', start_line, start_col))
            elif char == ']':
                self.advance()
                self.tokens.append(Token(TokenType.RBRACKET, ']', start_line, start_col))
            elif char == ',':
                self.advance()
                self.tokens.append(Token(TokenType.COMMA, ',', start_line, start_col))
            elif char == ':':
                self.advance()
                self.tokens.append(Token(TokenType.COLON, ':', start_line, start_col))
            elif char == ';':
                self.advance()
                self.tokens.append(Token(TokenType.SEMICOLON, ';', start_line, start_col))
            elif char == '.':
                self.advance()
                self.tokens.append(Token(TokenType.DOT, '.', start_line, start_col))
            else:
                # Unknown character - skip
                self.advance()
        
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens


class FlameLangParser:
    """
    Parser for Flame Lang - generates Abstract Syntax Tree from tokens.
    """
    
    def __init__(self, tokens: list[Token]):
        self.tokens = [t for t in tokens if t.type not in (TokenType.WHITESPACE, TokenType.COMMENT)]
        self.pos = 0
    
    def current_token(self) -> Token | None:
        """Get current token."""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None
    
    def peek(self, offset: int = 0) -> Token | None:
        """Peek at token at current position + offset."""
        idx = self.pos + offset
        if idx < len(self.tokens):
            return self.tokens[idx]
        return None
    
    def advance(self) -> Token | None:
        """Advance and return current token."""
        token = self.current_token()
        self.pos += 1
        return token
    
    def skip_newlines(self):
        """Skip newline tokens."""
        while self.current_token() and self.current_token().type == TokenType.NEWLINE:
            self.advance()
    
    def expect(self, token_type: TokenType) -> Token:
        """Expect a specific token type."""
        token = self.current_token()
        if token is None or token.type != token_type:
            raise SyntaxError(f"Expected {token_type}, got {token.type if token else 'EOF'}")
        return self.advance()
    
    def parse(self) -> ASTNode:
        """Parse the token stream into an AST."""
        return self.parse_program()
    
    def parse_program(self) -> ASTNode:
        """Parse the entire program."""
        node = ASTNode('program')
        self.skip_newlines()
        while self.current_token() and self.current_token().type != TokenType.EOF:
            stmt = self.parse_statement()
            if stmt:
                node.children.append(stmt)
            self.skip_newlines()
        return node
    
    def parse_statement(self) -> ASTNode | None:
        """Parse a single statement."""
        token = self.current_token()
        if not token:
            return None
        
        if token.type == TokenType.IGNITE:
            return self.parse_function_def()
        elif token.type == TokenType.SPARK:
            return self.parse_variable_decl()
        elif token.type == TokenType.EMBER:
            return self.parse_conditional()
        elif token.type == TokenType.BLAZE:
            return self.parse_loop()
        elif token.type == TokenType.FLAME:
            return self.parse_class_def()
        elif token.type == TokenType.ASH:
            return self.parse_return()
        elif token.type == TokenType.FORGE:
            return self.parse_import()
        elif token.type == TokenType.OATH:
            return self.parse_oath()
        elif token.type == TokenType.INFERNO:
            return self.parse_exception()
        elif token.type == TokenType.NEWLINE:
            self.advance()
            return None
        else:
            return self.parse_expression()
    
    def parse_function_def(self) -> ASTNode:
        """Parse function definition: ignite name(params) { body }"""
        token = self.advance()  # consume 'ignite'
        name = self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.LPAREN)
        
        params = []
        while self.current_token() and self.current_token().type != TokenType.RPAREN:
            param = self.expect(TokenType.IDENTIFIER)
            params.append(param.value)
            if self.current_token() and self.current_token().type == TokenType.COMMA:
                self.advance()
        
        self.expect(TokenType.RPAREN)
        self.skip_newlines()
        self.expect(TokenType.LBRACE)
        
        body = self.parse_block()
        self.expect(TokenType.RBRACE)
        
        node = ASTNode('function_def', value={'name': name.value, 'params': params})
        node.children = [body]
        node.line = token.line
        node.column = token.column
        return node
    
    def parse_variable_decl(self) -> ASTNode:
        """Parse variable declaration: spark name = value or spark self.name = value"""
        token = self.advance()  # consume 'spark'
        name = self.expect(TokenType.IDENTIFIER)
        
        # Handle compound identifiers like self.name
        full_name = name.value
        while self.current_token() and self.current_token().type == TokenType.DOT:
            self.advance()  # consume '.'
            next_part = self.expect(TokenType.IDENTIFIER)
            full_name += '.' + next_part.value
        
        self.expect(TokenType.ASSIGN)
        value = self.parse_expression()
        
        node = ASTNode('variable_decl', value=full_name)
        node.children = [value]
        node.line = token.line
        node.column = token.column
        return node
    
    def parse_conditional(self) -> ASTNode:
        """Parse conditional: ember (condition) { body } [else { body }]"""
        token = self.advance()  # consume 'ember'
        self.expect(TokenType.LPAREN)
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN)
        self.skip_newlines()
        self.expect(TokenType.LBRACE)
        then_body = self.parse_block()
        self.expect(TokenType.RBRACE)
        
        node = ASTNode('conditional')
        node.children = [condition, then_body]
        node.line = token.line
        node.column = token.column
        
        # Check for else branch
        self.skip_newlines()
        if self.current_token() and self.current_token().value == 'else':
            self.advance()
            self.skip_newlines()
            self.expect(TokenType.LBRACE)
            else_body = self.parse_block()
            self.expect(TokenType.RBRACE)
            node.children.append(else_body)
        
        return node
    
    def parse_loop(self) -> ASTNode:
        """Parse loop: blaze (condition) { body }"""
        token = self.advance()  # consume 'blaze'
        self.expect(TokenType.LPAREN)
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN)
        self.skip_newlines()
        self.expect(TokenType.LBRACE)
        body = self.parse_block()
        self.expect(TokenType.RBRACE)
        
        node = ASTNode('loop')
        node.children = [condition, body]
        node.line = token.line
        node.column = token.column
        return node
    
    def parse_class_def(self) -> ASTNode:
        """Parse class definition: flame ClassName { body }"""
        token = self.advance()  # consume 'flame'
        name = self.expect(TokenType.IDENTIFIER)
        self.skip_newlines()
        self.expect(TokenType.LBRACE)
        body = self.parse_block()
        self.expect(TokenType.RBRACE)
        
        node = ASTNode('class_def', value=name.value)
        node.children = [body]
        node.line = token.line
        node.column = token.column
        return node
    
    def parse_return(self) -> ASTNode:
        """Parse return statement: ash value"""
        token = self.advance()  # consume 'ash'
        value = None
        if self.current_token() and self.current_token().type not in (TokenType.NEWLINE, TokenType.RBRACE, TokenType.EOF):
            value = self.parse_expression()
        
        node = ASTNode('return')
        if value:
            node.children = [value]
        node.line = token.line
        node.column = token.column
        return node
    
    def parse_import(self) -> ASTNode:
        """Parse import: forge 'module_name'"""
        token = self.advance()  # consume 'forge'
        module = self.expect(TokenType.STRING)
        
        node = ASTNode('import', value=module.value)
        node.line = token.line
        node.column = token.column
        return node
    
    def parse_oath(self) -> ASTNode:
        """Parse oath assertion: oath { bearer: ..., seal: ... }"""
        token = self.advance()  # consume 'oath'
        self.skip_newlines()
        self.expect(TokenType.LBRACE)
        
        oath_data = {}
        while self.current_token() and self.current_token().type != TokenType.RBRACE:
            self.skip_newlines()
            if self.current_token().type == TokenType.RBRACE:
                break
            # Accept both IDENTIFIER and keywords (like bearer, seal) as keys
            key_token = self.current_token()
            if key_token.type == TokenType.IDENTIFIER:
                key = self.advance()
            elif key_token.type in (TokenType.BEARER, TokenType.SEAL):
                key = self.advance()
            else:
                raise SyntaxError(f"Expected identifier or keyword as key, got {key_token.type}")
            
            self.expect(TokenType.COLON)
            value = self.parse_expression()
            oath_data[key.value if hasattr(key, 'value') and isinstance(key.value, str) else str(key.type).split('.')[-1].lower()] = value
            self.skip_newlines()
            if self.current_token() and self.current_token().type == TokenType.COMMA:
                self.advance()
        
        self.expect(TokenType.RBRACE)
        
        node = ASTNode('oath', value=oath_data)
        node.line = token.line
        node.column = token.column
        return node
    
    def parse_exception(self) -> ASTNode:
        """Parse exception handling: inferno { try } catch { handler }"""
        token = self.advance()  # consume 'inferno'
        self.skip_newlines()
        self.expect(TokenType.LBRACE)
        try_body = self.parse_block()
        self.expect(TokenType.RBRACE)
        
        node = ASTNode('exception')
        node.children = [try_body]
        node.line = token.line
        node.column = token.column
        
        # Check for catch
        self.skip_newlines()
        if self.current_token() and self.current_token().value == 'catch':
            self.advance()
            self.skip_newlines()
            self.expect(TokenType.LBRACE)
            catch_body = self.parse_block()
            self.expect(TokenType.RBRACE)
            node.children.append(catch_body)
        
        return node
    
    def parse_block(self) -> ASTNode:
        """Parse a block of statements."""
        node = ASTNode('block')
        self.skip_newlines()
        while self.current_token() and self.current_token().type != TokenType.RBRACE:
            stmt = self.parse_statement()
            if stmt:
                node.children.append(stmt)
            self.skip_newlines()
        return node
    
    def parse_expression(self) -> ASTNode:
        """Parse an expression (simplified)."""
        return self.parse_comparison()
    
    def parse_comparison(self) -> ASTNode:
        """Parse comparison expression."""
        left = self.parse_additive()
        
        while self.current_token() and self.current_token().type in (
            TokenType.EQUALS, TokenType.NOT_EQUALS, TokenType.GREATER,
            TokenType.LESS, TokenType.GREATER_EQ, TokenType.LESS_EQ
        ):
            op = self.advance()
            right = self.parse_additive()
            node = ASTNode('binary_op', value=op.value)
            node.children = [left, right]
            left = node
        
        return left
    
    def parse_additive(self) -> ASTNode:
        """Parse additive expression."""
        left = self.parse_multiplicative()
        
        while self.current_token() and self.current_token().type in (TokenType.PLUS, TokenType.MINUS):
            op = self.advance()
            right = self.parse_multiplicative()
            node = ASTNode('binary_op', value=op.value)
            node.children = [left, right]
            left = node
        
        return left
    
    def parse_multiplicative(self) -> ASTNode:
        """Parse multiplicative expression."""
        left = self.parse_unary()
        
        while self.current_token() and self.current_token().type in (TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            op = self.advance()
            right = self.parse_unary()
            node = ASTNode('binary_op', value=op.value)
            node.children = [left, right]
            left = node
        
        return left
    
    def parse_unary(self) -> ASTNode:
        """Parse unary expression."""
        if self.current_token() and self.current_token().type in (TokenType.MINUS, TokenType.NOT):
            op = self.advance()
            operand = self.parse_unary()
            node = ASTNode('unary_op', value=op.value)
            node.children = [operand]
            return node
        return self.parse_primary()
    
    def parse_primary(self) -> ASTNode:
        """Parse primary expression."""
        token = self.current_token()
        
        if token.type == TokenType.NUMBER:
            self.advance()
            return ASTNode('number', value=token.value, line=token.line, column=token.column)
        elif token.type == TokenType.STRING:
            self.advance()
            return ASTNode('string', value=token.value, line=token.line, column=token.column)
        elif token.type == TokenType.BOOLEAN:
            self.advance()
            return ASTNode('boolean', value=token.value, line=token.line, column=token.column)
        elif token.type == TokenType.IDENTIFIER:
            self.advance()
            # Handle compound identifiers like self.name or obj.method
            full_name = token.value
            while self.current_token() and self.current_token().type == TokenType.DOT:
                self.advance()  # consume '.'
                if self.current_token() and self.current_token().type == TokenType.IDENTIFIER:
                    next_part = self.advance()
                    full_name += '.' + next_part.value
                else:
                    break
            
            node = ASTNode('identifier', value=full_name, line=token.line, column=token.column)
            # Check for function call
            if self.current_token() and self.current_token().type == TokenType.LPAREN:
                return self.parse_function_call(node)
            return node
        elif token.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr
        elif token.type == TokenType.LBRACKET:
            return self.parse_array()
        
        raise SyntaxError(f"Unexpected token: {token.type} at line {token.line}")
    
    def parse_function_call(self, name_node: ASTNode) -> ASTNode:
        """Parse function call: name(args)"""
        self.advance()  # consume '('
        
        args = []
        while self.current_token() and self.current_token().type != TokenType.RPAREN:
            args.append(self.parse_expression())
            if self.current_token() and self.current_token().type == TokenType.COMMA:
                self.advance()
        
        self.expect(TokenType.RPAREN)
        
        node = ASTNode('function_call', value=name_node.value)
        node.children = args
        return node
    
    def parse_array(self) -> ASTNode:
        """Parse array literal: [elem1, elem2, ...]"""
        self.advance()  # consume '['
        
        elements = []
        while self.current_token() and self.current_token().type != TokenType.RBRACKET:
            elements.append(self.parse_expression())
            if self.current_token() and self.current_token().type == TokenType.COMMA:
                self.advance()
        
        self.expect(TokenType.RBRACKET)
        
        node = ASTNode('array')
        node.children = elements
        return node


def parse_flame(source: str) -> ASTNode:
    """
    Parse Flame Lang source code and return the AST.
    
    Args:
        source: Flame Lang source code string
        
    Returns:
        ASTNode representing the program
    """
    lexer = FlameLangLexer(source)
    tokens = lexer.tokenize()
    parser = FlameLangParser(tokens)
    return parser.parse()


def print_ast(node: ASTNode, indent: int = 0):
    """Pretty print an AST node."""
    prefix = "  " * indent
    print(f"{prefix}{node.node_type}", end="")
    if node.value is not None:
        print(f": {node.value}", end="")
    print()
    for child in node.children:
        print_ast(child, indent + 1)


# Example usage and testing
if __name__ == "__main__":
    sample_code = '''
# Flame Lang Example - Sovereignty Architecture
forge "sovereignty_core"

flame SovereignNode {
    ignite init(name, tier) {
        spark self.name = name
        spark self.tier = tier
        spark self.active = true
    }
    
    ignite activate() {
        oath {
            bearer: self.name,
            seal: "SHA256"
        }
        ash true
    }
}

ignite main() {
    spark node = SovereignNode("Nova", 1)
    
    ember (node.active) {
        node.activate()
        print("Node activated: " + node.name)
    }
    
    spark counter = 0
    blaze (counter < 10) {
        spark counter = counter + 1
        print(counter)
    }
    
    inferno {
        spark result = riskyOperation()
    } catch {
        print("Operation failed safely")
    }
    
    ash 0
}
'''
    
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  FLAME LANG PARSER - WhiteCellOS / Pantheon Core             ║")
    print("╠══════════════════════════════════════════════════════════════╣")
    print("║  Parsing sample Flame Lang code...                           ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    
    ast = parse_flame(sample_code)
    print("AST Generated:")
    print("-" * 60)
    print_ast(ast)
