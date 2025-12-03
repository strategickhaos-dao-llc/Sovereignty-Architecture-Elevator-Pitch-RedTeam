"""
StrategicKhaos Interpreter - Stage 0
Interprets and executes StrategicKhaos AST
"""

from typing import Any, Dict, Callable
from .parser import (
    ASTNode, Program, PrintStatement, LetStatement,
    StringLiteral, NumberLiteral, Identifier, BinaryOp,
    Lambda, FunctionCall, Block
)


class Environment:
    def __init__(self, parent=None):
        self.vars: Dict[str, Any] = {}
        self.parent = parent
    
    def define(self, name: str, value: Any):
        self.vars[name] = value
    
    def get(self, name: str) -> Any:
        if name in self.vars:
            return self.vars[name]
        if self.parent:
            return self.parent.get(name)
        raise NameError(f"Undefined variable: {name}")
    
    def set(self, name: str, value: Any):
        if name in self.vars:
            self.vars[name] = value
        elif self.parent:
            self.parent.set(name, value)
        else:
            raise NameError(f"Undefined variable: {name}")


class LambdaValue:
    def __init__(self, params, body, closure):
        self.params = params
        self.body = body
        self.closure = closure
    
    def call(self, interpreter, args):
        # Create new environment for function execution
        env = Environment(self.closure)
        
        # Bind parameters
        for i, param in enumerate(self.params):
            if i < len(args):
                env.define(param, args[i])
            else:
                env.define(param, None)
        
        # Execute body
        return interpreter.eval(self.body, env)


class Interpreter:
    def __init__(self):
        self.global_env = Environment()
        self.output = []
    
    def interpret(self, program: Program):
        for statement in program.statements:
            self.eval(statement, self.global_env)
    
    def eval(self, node: ASTNode, env: Environment) -> Any:
        if isinstance(node, Program):
            result = None
            for stmt in node.statements:
                result = self.eval(stmt, env)
            return result
        
        elif isinstance(node, PrintStatement):
            value = self.eval(node.expression, env)
            output = self.stringify(value)
            print(output)
            self.output.append(output)
            return value
        
        elif isinstance(node, LetStatement):
            value = self.eval(node.value, env)
            env.define(node.name, value)
            return value
        
        elif isinstance(node, StringLiteral):
            return node.value
        
        elif isinstance(node, NumberLiteral):
            return node.value
        
        elif isinstance(node, Identifier):
            return env.get(node.name)
        
        elif isinstance(node, BinaryOp):
            left = self.eval(node.left, env)
            right = self.eval(node.right, env)
            
            if node.operator == '+':
                # String concatenation or addition
                if isinstance(left, str) or isinstance(right, str):
                    return self.stringify(left) + self.stringify(right)
                return left + right
            else:
                raise RuntimeError(f"Unknown operator: {node.operator}")
        
        elif isinstance(node, Lambda):
            return LambdaValue(node.params, node.body, env)
        
        elif isinstance(node, FunctionCall):
            func = self.eval(node.function, env)
            args = [self.eval(arg, env) for arg in node.arguments]
            
            if isinstance(func, LambdaValue):
                return func.call(self, args)
            elif callable(func):
                return func(*args)
            else:
                raise RuntimeError(f"Not a function: {func}")
        
        elif isinstance(node, Block):
            result = None
            for stmt in node.statements:
                result = self.eval(stmt, env)
            return result
        
        else:
            raise RuntimeError(f"Unknown AST node type: {type(node)}")
    
    def stringify(self, value: Any) -> str:
        if value is None:
            return "nil"
        elif isinstance(value, bool):
            return "true" if value else "false"
        elif isinstance(value, str):
            return value
        elif isinstance(value, (int, float)):
            # Remove .0 for whole numbers
            if isinstance(value, float) and value.is_integer():
                return str(int(value))
            return str(value)
        elif isinstance(value, LambdaValue):
            return f"<lambda>"
        else:
            return str(value)
