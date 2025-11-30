"""
AST Node Definitions for StrategicKhaos

Defines all node types in the Abstract Syntax Tree.
"""

from dataclasses import dataclass
from typing import List, Optional, Any
from abc import ABC, abstractmethod


class ASTNode(ABC):
    """Base class for all AST nodes"""
    
    @abstractmethod
    def accept(self, visitor):
        """Accept a visitor for the visitor pattern"""
        pass


@dataclass
class Program(ASTNode):
    """Root node representing the entire program"""
    statements: List['Statement']
    
    def accept(self, visitor):
        return visitor.visit_program(self)


# ============================================================================
# Statements
# ============================================================================

class Statement(ASTNode):
    """Base class for all statements"""
    pass


@dataclass
class VariableDeclaration(Statement):
    """Variable declaration: let x = expr; or const x = expr;"""
    name: str
    value: 'Expression'
    is_const: bool = False
    
    def accept(self, visitor):
        return visitor.visit_variable_declaration(self)


@dataclass
class FunctionDeclaration(Statement):
    """Function declaration: fn name(params) { body }"""
    name: str
    parameters: List[str]
    body: List[Statement]
    
    def accept(self, visitor):
        return visitor.visit_function_declaration(self)


@dataclass
class IfStatement(Statement):
    """If statement: if condition { then_body } else { else_body }"""
    condition: 'Expression'
    then_body: List[Statement]
    else_body: Optional[List[Statement]] = None
    
    def accept(self, visitor):
        return visitor.visit_if_statement(self)


@dataclass
class WhileStatement(Statement):
    """While loop: while condition { body }"""
    condition: 'Expression'
    body: List[Statement]
    
    def accept(self, visitor):
        return visitor.visit_while_statement(self)


@dataclass
class ForStatement(Statement):
    """For loop: for variable in iterable { body }"""
    variable: str
    iterable: 'Expression'
    body: List[Statement]
    
    def accept(self, visitor):
        return visitor.visit_for_statement(self)


@dataclass
class ReturnStatement(Statement):
    """Return statement: return expr;"""
    value: Optional['Expression'] = None
    
    def accept(self, visitor):
        return visitor.visit_return_statement(self)


@dataclass
class PrintStatement(Statement):
    """Print statement: print expr; or show expr;"""
    expression: 'Expression'
    is_show: bool = False  # True for 'show', False for 'print'
    
    def accept(self, visitor):
        return visitor.visit_print_statement(self)


@dataclass
class ExpressionStatement(Statement):
    """Statement consisting of a single expression"""
    expression: 'Expression'
    
    def accept(self, visitor):
        return visitor.visit_expression_statement(self)


@dataclass
class BreakStatement(Statement):
    """Break statement: break;"""
    
    def accept(self, visitor):
        return visitor.visit_break_statement(self)


@dataclass
class ContinueStatement(Statement):
    """Continue statement: continue;"""
    
    def accept(self, visitor):
        return visitor.visit_continue_statement(self)


# ============================================================================
# Expressions
# ============================================================================

class Expression(ASTNode):
    """Base class for all expressions"""
    pass


@dataclass
class BinaryExpression(Expression):
    """Binary operation: left op right"""
    operator: str
    left: Expression
    right: Expression
    
    def accept(self, visitor):
        return visitor.visit_binary_expression(self)


@dataclass
class UnaryExpression(Expression):
    """Unary operation: op operand"""
    operator: str
    operand: Expression
    
    def accept(self, visitor):
        return visitor.visit_unary_expression(self)


@dataclass
class Identifier(Expression):
    """Variable reference"""
    name: str
    
    def accept(self, visitor):
        return visitor.visit_identifier(self)


@dataclass
class Literal(Expression):
    """Literal value (number, string, boolean)"""
    value: Any
    
    def accept(self, visitor):
        return visitor.visit_literal(self)


@dataclass
class FunctionCall(Expression):
    """Function call: func(args)"""
    function: Expression  # Usually an Identifier, but could be any expression
    arguments: List[Expression]
    
    def accept(self, visitor):
        return visitor.visit_function_call(self)


@dataclass
class AssignmentExpression(Expression):
    """Assignment: target = value"""
    target: str
    value: Expression
    
    def accept(self, visitor):
        return visitor.visit_assignment_expression(self)


@dataclass
class ArrayLiteral(Expression):
    """Array literal: [elements]"""
    elements: List[Expression]
    
    def accept(self, visitor):
        return visitor.visit_array_literal(self)


@dataclass
class IndexExpression(Expression):
    """Array/object indexing: object[index]"""
    object: Expression
    index: Expression
    
    def accept(self, visitor):
        return visitor.visit_index_expression(self)


# ============================================================================
# Special Nodes
# ============================================================================

@dataclass
class Decorator(ASTNode):
    """Decorator/annotation: @optimize(neural=true)"""
    name: str
    arguments: dict
    
    def accept(self, visitor):
        return visitor.visit_decorator(self)


@dataclass
class DecoratedFunction(Statement):
    """Function with decorators"""
    decorators: List[Decorator]
    function: FunctionDeclaration
    
    def accept(self, visitor):
        return visitor.visit_decorated_function(self)
