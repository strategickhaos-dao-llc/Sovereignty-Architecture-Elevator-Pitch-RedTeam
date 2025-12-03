"""
StrategicKhaos Python Code Generator - Stage 0
Generates Python code from StrategicKhaos AST
"""

from typing import List
from .parser import (
    ASTNode, Program, PrintStatement, LetStatement,
    StringLiteral, NumberLiteral, Identifier, BinaryOp,
    Lambda, FunctionCall, Block
)


class PythonCodeGenerator:
    def __init__(self):
        self.indent_level = 0
        self.output: List[str] = []
        self.lambda_counter = 0
    
    def indent(self):
        return "    " * self.indent_level
    
    def emit(self, code: str):
        self.output.append(code)
    
    def emit_line(self, code: str = ""):
        if code:
            self.output.append(self.indent() + code + "\n")
        else:
            self.output.append("\n")
    
    def generate(self, program: Program) -> str:
        self.output = []
        
        # Add header
        self.emit_line("# Generated Python code from StrategicKhaos")
        self.emit_line()
        
        # Generate code for each statement
        for statement in program.statements:
            self.gen_statement(statement)
        
        return "".join(self.output)
    
    def gen_statement(self, node: ASTNode):
        if isinstance(node, PrintStatement):
            self.gen_print(node)
        elif isinstance(node, LetStatement):
            self.gen_let(node)
        else:
            # Expression statement
            expr = self.gen_expression(node)
            self.emit_line(expr)
    
    def gen_print(self, node: PrintStatement):
        expr = self.gen_expression(node.expression)
        self.emit_line(f"print({expr})")
    
    def gen_let(self, node: LetStatement):
        # Special handling for lambdas with blocks
        if isinstance(node.value, Lambda) and isinstance(node.value.body, Block):
            self.gen_function_def(node.name, node.value)
        else:
            value = self.gen_expression(node.value)
            self.emit_line(f"{node.name} = {value}")
    
    def gen_function_def(self, name: str, lambda_node: Lambda):
        """Generate a Python function definition from a lambda with a block body"""
        params = ", ".join(lambda_node.params) if lambda_node.params else ""
        self.emit_line(f"def {name}({params}):")
        self.indent_level += 1
        
        # Generate body statements
        for stmt in lambda_node.body.statements:
            if isinstance(stmt, PrintStatement):
                self.gen_print(stmt)
            elif isinstance(stmt, LetStatement):
                self.gen_let(stmt)
            else:
                expr = self.gen_expression(stmt)
                self.emit_line(expr)
        
        self.indent_level -= 1
        self.emit_line()
    
    def gen_expression(self, node: ASTNode) -> str:
        if isinstance(node, StringLiteral):
            # Escape the string properly for Python (backslash first to avoid double-escaping)
            escaped = (node.value
                      .replace('\\', '\\\\')
                      .replace('"', '\\"')
                      .replace('\n', '\\n')
                      .replace('\t', '\\t')
                      .replace('\r', '\\r'))
            return f'"{escaped}"'
        
        elif isinstance(node, NumberLiteral):
            # Remove .0 for whole numbers
            if node.value.is_integer():
                return str(int(node.value))
            return str(node.value)
        
        elif isinstance(node, Identifier):
            return node.name
        
        elif isinstance(node, BinaryOp):
            left = self.gen_expression(node.left)
            right = self.gen_expression(node.right)
            return f"({left} {node.operator} {right})"
        
        elif isinstance(node, Lambda):
            return self.gen_lambda(node)
        
        elif isinstance(node, FunctionCall):
            return self.gen_function_call(node)
        
        elif isinstance(node, Block):
            # Blocks in expressions not fully supported, just generate statements
            return self.gen_block(node)
        
        else:
            raise RuntimeError(f"Unknown expression type: {type(node)}")
    
    def gen_lambda(self, node: Lambda) -> str:
        params = ", ".join(node.params) if node.params else ""
        
        if isinstance(node.body, Block):
            # Multi-statement lambda - not directly supported in Python expressions
            # We'll need to create a function for this
            # For now, just generate the last expression
            if node.body.statements:
                last = node.body.statements[-1]
                body = self.gen_expression(last) if not isinstance(last, (PrintStatement, LetStatement)) else "None"
            else:
                body = "None"
        else:
            body = self.gen_expression(node.body)
        
        return f"lambda {params}: {body}"
    
    def gen_function_call(self, node: FunctionCall) -> str:
        func = self.gen_expression(node.function)
        args = ", ".join(self.gen_expression(arg) for arg in node.arguments)
        return f"{func}({args})"
    
    def gen_block(self, node: Block) -> str:
        # For blocks, we generate statements
        # This is tricky in expression context
        result = []
        for stmt in node.statements:
            if isinstance(stmt, PrintStatement):
                expr = self.gen_expression(stmt.expression)
                result.append(f"print({expr})")
            elif isinstance(stmt, LetStatement):
                value = self.gen_expression(stmt.value)
                result.append(f"{stmt.name} = {value}")
            else:
                result.append(self.gen_expression(stmt))
        
        return "; ".join(result) if result else "None"
