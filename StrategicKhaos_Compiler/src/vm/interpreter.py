"""
Interpreter for StrategicKhaos AST.
Directly evaluates AST nodes (tree-walking interpreter).
"""

from typing import Any, Dict, List
from ..ast.nodes import ASTNode, NumberNode, StringNode, SymbolNode, ListNode


class InterpreterError(Exception):
    """Exception raised for interpreter errors."""
    pass


class Interpreter:
    """
    Tree-walking interpreter for StrategicKhaos.
    
    Evaluates AST nodes directly without compilation.
    This is a simple interpreter for the bootstrap phase.
    """
    
    def __init__(self):
        """Initialize the interpreter with a global environment."""
        self.global_env: Dict[str, Any] = {}
        self._setup_builtins()
    
    def _setup_builtins(self):
        """Setup built-in functions."""
        # Built-in print function
        self.global_env['print'] = self._builtin_print
        
        # Arithmetic operators
        self.global_env['+'] = lambda *args: sum(args)
        self.global_env['-'] = lambda a, b: a - b
        self.global_env['*'] = lambda *args: self._product(args)
        self.global_env['/'] = lambda a, b: a / b
    
    def _product(self, args):
        """Helper to compute product of arguments."""
        result = 1
        for arg in args:
            result *= arg
        return result
    
    def _builtin_print(self, *args):
        """Built-in print function."""
        output = ' '.join(str(arg) for arg in args)
        print(output)
        return None
    
    def eval(self, node: ASTNode, env: Dict[str, Any] = None) -> Any:
        """
        Evaluate an AST node.
        
        Args:
            node: The AST node to evaluate
            env: The environment (variable bindings)
        
        Returns:
            The result of evaluating the node
        
        Raises:
            InterpreterError: If evaluation fails
        """
        if env is None:
            env = self.global_env
        
        # Evaluate number literals
        if isinstance(node, NumberNode):
            return node.value
        
        # Evaluate string literals
        if isinstance(node, StringNode):
            return node.value
        
        # Evaluate symbols (variable lookup)
        if isinstance(node, SymbolNode):
            if node.name in env:
                return env[node.name]
            raise InterpreterError(f"Undefined symbol: {node.name}")
        
        # Evaluate lists (function calls)
        if isinstance(node, ListNode):
            if len(node.elements) == 0:
                return []
            
            # Get the function
            func_node = node.elements[0]
            
            # Handle special forms
            if isinstance(func_node, SymbolNode):
                func_name = func_node.name
                
                # Special form: quote (not implemented yet, but placeholder)
                if func_name == 'quote':
                    if len(node.elements) != 2:
                        raise InterpreterError("quote requires exactly one argument")
                    return node.elements[1]
            
            # Evaluate the function
            func = self.eval(func_node, env)
            
            if not callable(func):
                raise InterpreterError(f"Not a function: {func}")
            
            # Evaluate arguments
            args = [self.eval(arg, env) for arg in node.elements[1:]]
            
            # Call the function
            try:
                return func(*args)
            except Exception as e:
                raise InterpreterError(f"Error calling function: {e}")
        
        raise InterpreterError(f"Unknown node type: {type(node)}")
    
    def run(self, nodes: List[ASTNode]) -> Any:
        """
        Run a list of AST nodes (a program).
        
        Args:
            nodes: List of AST nodes to evaluate
        
        Returns:
            The result of the last expression
        """
        result = None
        for node in nodes:
            result = self.eval(node)
        return result
