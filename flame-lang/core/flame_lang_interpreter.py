#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  FLAME LANG INTERPRETER - Execution Engine                                   ║
║  Runtime environment for Flame Language programs                             ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Part of the Strategic Khaos Sovereignty Architecture                        ║
║  Author: Domenic Garza / StrategicKhaos DAO LLC                             ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import hashlib
import json
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

# Import the parser
from flamelang_parser import ASTNode, parse_flame


class FlameError(Exception):
    """Base exception for Flame Lang runtime errors."""
    pass


class FlameTypeError(FlameError):
    """Type error in Flame Lang."""
    pass


class FlameRuntimeError(FlameError):
    """Runtime error in Flame Lang."""
    pass


class FlameSecurityError(FlameError):
    """Security violation in Flame Lang."""
    pass


@dataclass
class FlameObject:
    """Base class for Flame Lang objects."""
    type_name: str = "object"
    properties: dict = field(default_factory=dict)
    methods: dict = field(default_factory=dict)


@dataclass
class FlameFunction:
    """Represents a Flame Lang function."""
    name: str
    params: list[str]
    body: ASTNode
    closure: dict = field(default_factory=dict)


@dataclass
class FlameClass:
    """Represents a Flame Lang class (flame)."""
    name: str
    methods: dict = field(default_factory=dict)
    body: ASTNode = None


@dataclass
class FlameInstance:
    """Instance of a FlameClass."""
    class_ref: FlameClass
    properties: dict = field(default_factory=dict)


@dataclass
class OathToken:
    """Represents a sovereignty oath token."""
    bearer: str
    seal: str
    timestamp: float
    signature: str


class ReturnValue(Exception):
    """Used to unwind the stack for return statements."""
    def __init__(self, value):
        self.value = value


class FlameEnvironment:
    """
    Environment/scope for variable bindings.
    """
    
    def __init__(self, parent: "FlameEnvironment | None" = None):
        self.bindings: dict[str, Any] = {}
        self.parent = parent
    
    def get(self, name: str) -> Any:
        """Get a variable from this scope or parent scopes."""
        if name in self.bindings:
            return self.bindings[name]
        if self.parent:
            return self.parent.get(name)
        raise FlameRuntimeError(f"Undefined variable: {name}")
    
    def set(self, name: str, value: Any):
        """Set a variable in the current scope."""
        self.bindings[name] = value
    
    def update(self, name: str, value: Any):
        """Update an existing variable in this scope or parent scopes."""
        if name in self.bindings:
            self.bindings[name] = value
        elif self.parent:
            self.parent.update(name, value)
        else:
            # Create new if doesn't exist
            self.bindings[name] = value


class FlameInterpreter:
    """
    Interpreter for Flame Lang.
    
    Executes AST nodes and manages the runtime environment.
    """
    
    def __init__(self):
        self.global_env = FlameEnvironment()
        self.current_env = self.global_env
        self.oath_chain: list[OathToken] = []
        self.loaded_modules: dict[str, Any] = {}
        
        # Register built-in functions
        self._register_builtins()
    
    def _register_builtins(self):
        """Register built-in functions."""
        self.global_env.set("print", self._builtin_print)
        self.global_env.set("len", self._builtin_len)
        self.global_env.set("type", self._builtin_type)
        self.global_env.set("str", self._builtin_str)
        self.global_env.set("int", self._builtin_int)
        self.global_env.set("float", self._builtin_float)
        self.global_env.set("range", self._builtin_range)
        self.global_env.set("input", self._builtin_input)
        self.global_env.set("hash", self._builtin_hash)
        self.global_env.set("time", self._builtin_time)
        self.global_env.set("oath_verify", self._builtin_oath_verify)
        self.global_env.set("seal_data", self._builtin_seal_data)
        self.global_env.set("node_status", self._builtin_node_status)
    
    # Built-in functions
    def _builtin_print(self, *args):
        """Print function."""
        print(*[self._to_string(arg) for arg in args])
        return None
    
    def _builtin_len(self, obj):
        """Length function."""
        if isinstance(obj, (str, list)):
            return len(obj)
        if isinstance(obj, dict):
            return len(obj)
        raise FlameTypeError(f"Cannot get length of {type(obj)}")
    
    def _builtin_type(self, obj):
        """Type function."""
        if isinstance(obj, FlameInstance):
            return obj.class_ref.name
        if isinstance(obj, FlameFunction):
            return "function"
        if isinstance(obj, FlameClass):
            return "class"
        return type(obj).__name__
    
    def _builtin_str(self, obj):
        """String conversion."""
        return self._to_string(obj)
    
    def _builtin_int(self, obj):
        """Integer conversion."""
        return int(obj)
    
    def _builtin_float(self, obj):
        """Float conversion."""
        return float(obj)
    
    def _builtin_range(self, *args):
        """Range function."""
        return list(range(*args))
    
    def _builtin_input(self, prompt=""):
        """Input function."""
        return input(prompt)
    
    def _builtin_hash(self, data):
        """Hash function using SHA256."""
        if isinstance(data, str):
            data = data.encode()
        return hashlib.sha256(data).hexdigest()
    
    def _builtin_time(self):
        """Current timestamp."""
        return time.time()
    
    def _builtin_oath_verify(self, token: OathToken):
        """Verify an oath token."""
        expected_sig = hashlib.sha256(
            f"{token.bearer}:{token.seal}:{token.timestamp}".encode()
        ).hexdigest()
        return token.signature == expected_sig
    
    def _builtin_seal_data(self, data, seal_type="SHA256"):
        """Seal data with cryptographic hash."""
        if seal_type == "SHA256":
            return hashlib.sha256(str(data).encode()).hexdigest()
        elif seal_type == "SHA512":
            return hashlib.sha512(str(data).encode()).hexdigest()
        elif seal_type == "MD5":
            return hashlib.md5(str(data).encode()).hexdigest()  # noqa: S324
        raise FlameSecurityError(f"Unknown seal type: {seal_type}")
    
    def _builtin_node_status(self):
        """Get current node status."""
        return {
            "active": True,
            "oath_chain_length": len(self.oath_chain),
            "modules_loaded": list(self.loaded_modules.keys()),
            "timestamp": time.time()
        }
    
    def _to_string(self, obj) -> str:
        """Convert object to string representation."""
        if obj is None:
            return "null"
        if isinstance(obj, bool):
            return "true" if obj else "false"
        if isinstance(obj, FlameInstance):
            return f"<{obj.class_ref.name} instance>"
        if isinstance(obj, FlameFunction):
            return f"<function {obj.name}>"
        if isinstance(obj, FlameClass):
            return f"<class {obj.name}>"
        if isinstance(obj, list):
            return "[" + ", ".join(self._to_string(e) for e in obj) + "]"
        if isinstance(obj, dict):
            pairs = [f"{k}: {self._to_string(v)}" for k, v in obj.items()]
            return "{" + ", ".join(pairs) + "}"
        return str(obj)
    
    def execute(self, ast: ASTNode) -> Any:
        """Execute an AST node."""
        return self._eval(ast)
    
    def _eval(self, node: ASTNode) -> Any:
        """Evaluate an AST node."""
        method_name = f"_eval_{node.node_type}"
        method = getattr(self, method_name, None)
        if method:
            return method(node)
        raise FlameRuntimeError(f"Unknown node type: {node.node_type}")
    
    def _eval_program(self, node: ASTNode) -> Any:
        """Evaluate the entire program."""
        result = None
        for child in node.children:
            result = self._eval(child)
        return result
    
    def _eval_block(self, node: ASTNode) -> Any:
        """Evaluate a block of statements."""
        result = None
        for child in node.children:
            result = self._eval(child)
        return result
    
    def _eval_function_def(self, node: ASTNode) -> None:
        """Evaluate function definition."""
        func = FlameFunction(
            name=node.value['name'],
            params=node.value['params'],
            body=node.children[0] if node.children else ASTNode('block'),
            closure=dict(self.current_env.bindings)
        )
        self.current_env.set(node.value['name'], func)
    
    def _eval_variable_decl(self, node: ASTNode) -> None:
        """Evaluate variable declaration."""
        name = node.value
        value = self._eval(node.children[0]) if node.children else None
        self.current_env.set(name, value)
    
    def _eval_conditional(self, node: ASTNode) -> Any:
        """Evaluate conditional (ember)."""
        condition = self._eval(node.children[0])
        if condition:
            return self._eval(node.children[1])
        elif len(node.children) > 2:
            return self._eval(node.children[2])
        return None
    
    def _eval_loop(self, node: ASTNode) -> Any:
        """Evaluate loop (blaze)."""
        result = None
        while self._eval(node.children[0]):
            try:
                result = self._eval(node.children[1])
            except ReturnValue:
                raise
            except Exception:
                break
        return result
    
    def _eval_class_def(self, node: ASTNode) -> None:
        """Evaluate class definition (flame)."""
        flame_class = FlameClass(
            name=node.value,
            body=node.children[0] if node.children else ASTNode('block')
        )
        
        # Extract methods from the class body
        if flame_class.body:
            for child in flame_class.body.children:
                if child.node_type == 'function_def':
                    func = FlameFunction(
                        name=child.value['name'],
                        params=child.value['params'],
                        body=child.children[0] if child.children else ASTNode('block')
                    )
                    flame_class.methods[child.value['name']] = func
        
        self.current_env.set(node.value, flame_class)
    
    def _eval_return(self, node: ASTNode) -> None:
        """Evaluate return statement (ash)."""
        value = self._eval(node.children[0]) if node.children else None
        raise ReturnValue(value)
    
    def _eval_import(self, node: ASTNode) -> None:
        """Evaluate import (forge)."""
        module_name = node.value
        if module_name not in self.loaded_modules:
            # Try to load the module
            module_path = Path(f"{module_name}.flame")
            if module_path.exists():
                with open(module_path) as f:
                    source = f.read()
                ast = parse_flame(source)
                # Execute in a new environment
                old_env = self.current_env
                self.current_env = FlameEnvironment(self.global_env)
                self._eval(ast)
                self.loaded_modules[module_name] = dict(self.current_env.bindings)
                self.current_env = old_env
            else:
                # Module not found - just mark as loaded
                self.loaded_modules[module_name] = {}
        
        # Import all exports into current scope
        for name, value in self.loaded_modules.get(module_name, {}).items():
            self.current_env.set(name, value)
    
    def _eval_oath(self, node: ASTNode) -> OathToken:
        """Evaluate oath assertion."""
        oath_data = node.value
        
        # Evaluate the oath fields
        bearer = self._eval(oath_data.get('bearer', ASTNode('string', value='anonymous')))
        seal = self._eval(oath_data.get('seal', ASTNode('string', value='SHA256')))
        
        timestamp = time.time()
        signature = hashlib.sha256(f"{bearer}:{seal}:{timestamp}".encode()).hexdigest()
        
        token = OathToken(
            bearer=str(bearer),
            seal=str(seal),
            timestamp=timestamp,
            signature=signature
        )
        
        self.oath_chain.append(token)
        return token
    
    def _eval_exception(self, node: ASTNode) -> Any:
        """Evaluate exception handling (inferno)."""
        try:
            return self._eval(node.children[0])
        except (FlameError, Exception) as e:
            if len(node.children) > 1:
                # Execute catch block
                self.current_env.set("error", str(e))
                return self._eval(node.children[1])
            raise
    
    def _eval_binary_op(self, node: ASTNode) -> Any:
        """Evaluate binary operation."""
        left = self._eval(node.children[0])
        right = self._eval(node.children[1])
        op = node.value
        
        if op == '+':
            if isinstance(left, str) or isinstance(right, str):
                return str(left) + str(right)
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '/':
            if right == 0:
                raise FlameRuntimeError("Division by zero")
            return left / right
        elif op == '%':
            return left % right
        elif op == '==':
            return left == right
        elif op == '!=':
            return left != right
        elif op == '>':
            return left > right
        elif op == '<':
            return left < right
        elif op == '>=':
            return left >= right
        elif op == '<=':
            return left <= right
        elif op == 'and':
            return left and right
        elif op == 'or':
            return left or right
        else:
            raise FlameRuntimeError(f"Unknown operator: {op}")
    
    def _eval_unary_op(self, node: ASTNode) -> Any:
        """Evaluate unary operation."""
        operand = self._eval(node.children[0])
        op = node.value
        
        if op == '-':
            return -operand
        elif op == 'not':
            return not operand
        else:
            raise FlameRuntimeError(f"Unknown unary operator: {op}")
    
    def _eval_function_call(self, node: ASTNode) -> Any:
        """Evaluate function call."""
        func_name = node.value
        args = [self._eval(arg) for arg in node.children]
        
        # Try to get the function
        func = self.current_env.get(func_name)
        
        # Built-in callable
        if callable(func) and not isinstance(func, (FlameFunction, FlameClass)):
            return func(*args)
        
        # FlameClass constructor
        if isinstance(func, FlameClass):
            instance = FlameInstance(class_ref=func, properties={})
            # Call init if exists
            if 'init' in func.methods:
                init_method = func.methods['init']
                self._call_method(instance, init_method, args)
            return instance
        
        # FlameFunction
        if isinstance(func, FlameFunction):
            return self._call_function(func, args)
        
        raise FlameRuntimeError(f"'{func_name}' is not callable")
    
    def _call_function(self, func: FlameFunction, args: list) -> Any:
        """Call a Flame function."""
        # Create new environment with closure
        new_env = FlameEnvironment(self.current_env)
        for k, v in func.closure.items():
            new_env.set(k, v)
        
        # Bind parameters
        for param, arg in zip(func.params, args):
            new_env.set(param, arg)
        
        # Execute
        old_env = self.current_env
        self.current_env = new_env
        try:
            result = self._eval(func.body)
        except ReturnValue as rv:
            result = rv.value
        finally:
            self.current_env = old_env
        
        return result
    
    def _call_method(self, instance: FlameInstance, method: FlameFunction, args: list) -> Any:
        """Call a method on an instance."""
        new_env = FlameEnvironment(self.current_env)
        new_env.set('self', instance)
        
        # Bind parameters (skip 'self' which is first param)
        params = method.params[1:] if method.params and method.params[0] == 'self' else method.params
        for param, arg in zip(params, args):
            new_env.set(param, arg)
        
        old_env = self.current_env
        self.current_env = new_env
        try:
            result = self._eval(method.body)
        except ReturnValue as rv:
            result = rv.value
        finally:
            self.current_env = old_env
        
        return result
    
    def _eval_number(self, node: ASTNode) -> int | float:
        """Evaluate number literal."""
        return node.value
    
    def _eval_string(self, node: ASTNode) -> str:
        """Evaluate string literal."""
        return node.value
    
    def _eval_boolean(self, node: ASTNode) -> bool:
        """Evaluate boolean literal."""
        return node.value
    
    def _eval_identifier(self, node: ASTNode) -> Any:
        """Evaluate identifier."""
        name = node.value
        
        # Check for property access (self.prop)
        if '.' in name:
            parts = name.split('.')
            obj = self.current_env.get(parts[0])
            for part in parts[1:]:
                if isinstance(obj, FlameInstance):
                    if part in obj.properties:
                        obj = obj.properties[part]
                    elif part in obj.class_ref.methods:
                        # Return bound method
                        return lambda *args: self._call_method(obj, obj.class_ref.methods[part], list(args))
                elif isinstance(obj, dict):
                    obj = obj[part]
                else:
                    raise FlameRuntimeError(f"Cannot access '{part}' on {type(obj)}")
            return obj
        
        return self.current_env.get(name)
    
    def _eval_array(self, node: ASTNode) -> list:
        """Evaluate array literal."""
        return [self._eval(child) for child in node.children]


def run_flame_file(filepath: str) -> Any:
    """
    Run a Flame Lang file.
    
    Args:
        filepath: Path to .flame file
        
    Returns:
        Result of execution
    """
    with open(filepath) as f:
        source = f.read()
    
    ast = parse_flame(source)
    interpreter = FlameInterpreter()
    return interpreter.execute(ast)


def run_flame_repl():
    """
    Run the Flame Lang REPL (Read-Eval-Print Loop).
    """
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  FLAME LANG INTERPRETER v1.0                                 ║")
    print("║  Strategic Khaos Sovereignty Architecture                    ║")
    print("╠══════════════════════════════════════════════════════════════╣")
    print("║  Type 'exit' to quit, 'help' for commands                    ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    
    interpreter = FlameInterpreter()
    buffer = []
    
    while True:
        try:
            prompt = "flame>>> " if not buffer else "     ... "
            line = input(prompt)
            
            if line.strip() == 'exit':
                print("🔥 Flame extinguished. Goodbye!")
                break
            
            if line.strip() == 'help':
                print("""
Flame Lang Commands:
  exit        - Exit the REPL
  help        - Show this help
  status      - Show interpreter status
  oath_chain  - Show oath chain history
  
Keywords:
  ignite      - Define a function
  spark       - Declare a variable
  ember       - Conditional (if)
  blaze       - Loop (while)
  flame       - Define a class
  ash         - Return value
  forge       - Import module
  oath        - Create sovereignty oath
  inferno     - Exception handling
""")
                continue
            
            if line.strip() == 'status':
                status = interpreter._builtin_node_status()
                print(f"Status: {json.dumps(status, indent=2)}")
                continue
            
            if line.strip() == 'oath_chain':
                for i, oath in enumerate(interpreter.oath_chain):
                    print(f"  [{i}] Bearer: {oath.bearer}, Seal: {oath.seal}")
                continue
            
            buffer.append(line)
            source = '\n'.join(buffer)
            
            # Try to parse - if incomplete, continue collecting
            try:
                ast = parse_flame(source)
                result = interpreter.execute(ast)
                if result is not None:
                    print(f"=> {interpreter._to_string(result)}")
                buffer = []
            except SyntaxError:
                # Might be incomplete, continue
                pass
                
        except KeyboardInterrupt:
            print("\n🔥 Interrupted")
            buffer = []
        except Exception as e:
            print(f"Error: {e}")
            buffer = []


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        if filepath.endswith('.flame'):
            result = run_flame_file(filepath)
            if result is not None:
                print(f"Result: {result}")
        else:
            print(f"Error: Expected .flame file, got: {filepath}")
            sys.exit(1)
    else:
        run_flame_repl()


if __name__ == "__main__":
    main()
