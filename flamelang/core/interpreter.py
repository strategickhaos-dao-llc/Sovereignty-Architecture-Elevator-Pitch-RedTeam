"""
FlameLang Interpreter
Executes Abstract Syntax Tree with physics and sovereignty support
"""

import math
from typing import Dict, Any, Optional
from .parser import (
    ASTNode, NumberNode, StringNode, IdentifierNode, GlyphNode,
    BinaryOpNode, UnaryOpNode, AssignmentNode, FunctionCallNode,
    PhysicsOpNode, SovereigntyOpNode, ProgramNode
)
from .glyph_registry import GlyphRegistry
from .physics_engine import PhysicsEngine
from .sovereignty import SovereigntyProtocol


class Environment:
    """
    Environment for variable storage and built-in constants
    """
    
    def __init__(self):
        self.variables: Dict[str, Any] = {}
        self._init_constants()
    
    def _init_constants(self):
        """Initialize built-in mathematical and physical constants"""
        self.variables.update({
            # Mathematical constants
            'pi': math.pi,
            'e': math.e,
            'phi': (1 + math.sqrt(5)) / 2,  # Golden ratio
            
            # Physical constants
            'c': 299792458.0,      # Speed of light (m/s)
            'G': 6.67430e-11,      # Gravitational constant
            'h': 6.62607015e-34,   # Planck constant
            'alpha': 1/137.036,    # Fine structure constant
        })
    
    def set(self, name: str, value: Any):
        """Set a variable"""
        self.variables[name] = value
    
    def get(self, name: str) -> Any:
        """Get a variable"""
        if name not in self.variables:
            raise NameError(f"Variable '{name}' is not defined")
        return self.variables[name]
    
    def has(self, name: str) -> bool:
        """Check if variable exists"""
        return name in self.variables


class Interpreter:
    """
    Interpreter for FlameLang AST
    Executes code with physics simulations and sovereignty checks
    """
    
    def __init__(self):
        self.environment = Environment()
        self.glyph_registry = GlyphRegistry()
        self.physics_engine = PhysicsEngine()
        self.sovereignty = SovereigntyProtocol()
        self.output_buffer = []
    
    def interpret(self, ast: ASTNode) -> Any:
        """Interpret an AST node"""
        
        if isinstance(ast, ProgramNode):
            result = None
            for statement in ast.statements:
                result = self.interpret(statement)
            return result
        
        elif isinstance(ast, NumberNode):
            return ast.value
        
        elif isinstance(ast, StringNode):
            return ast.value
        
        elif isinstance(ast, IdentifierNode):
            return self.environment.get(ast.name)
        
        elif isinstance(ast, GlyphNode):
            # Look up glyph and return its frequency
            glyph = self.glyph_registry.lookup(ast.symbol)
            if glyph:
                return {
                    'symbol': ast.symbol,
                    'name': glyph.name,
                    'frequency': glyph.frequency,
                    'function': glyph.function
                }
            return {'symbol': ast.symbol, 'frequency': ast.frequency}
        
        elif isinstance(ast, BinaryOpNode):
            left = self.interpret(ast.left)
            right = self.interpret(ast.right)
            
            if ast.operator == '+':
                return left + right
            elif ast.operator == '-':
                return left - right
            elif ast.operator == '*':
                return left * right
            elif ast.operator == '/':
                if right == 0:
                    raise ZeroDivisionError("Division by zero")
                return left / right
            elif ast.operator == '==':
                return left == right
            elif ast.operator == '<':
                return left < right
            elif ast.operator == '>':
                return left > right
            else:
                raise RuntimeError(f"Unknown operator: {ast.operator}")
        
        elif isinstance(ast, UnaryOpNode):
            operand = self.interpret(ast.operand)
            
            if ast.operator == '+':
                return +operand
            elif ast.operator == '-':
                return -operand
            else:
                raise RuntimeError(f"Unknown unary operator: {ast.operator}")
        
        elif isinstance(ast, AssignmentNode):
            value = self.interpret(ast.value)
            self.environment.set(ast.name, value)
            return value
        
        elif isinstance(ast, FunctionCallNode):
            return self.call_function(ast.name, ast.arguments)
        
        elif isinstance(ast, PhysicsOpNode):
            return self.execute_physics_op(ast.operation, ast.arguments)
        
        elif isinstance(ast, SovereigntyOpNode):
            return self.execute_sovereignty_op(ast.operation, ast.arguments)
        
        else:
            raise RuntimeError(f"Unknown AST node type: {type(ast)}")
    
    def call_function(self, name: str, arguments: list) -> Any:
        """Call a built-in function"""
        args = [self.interpret(arg) for arg in arguments]
        
        # Math functions
        if name == 'sqrt':
            return math.sqrt(args[0])
        elif name == 'sin':
            return math.sin(args[0])
        elif name == 'cos':
            return math.cos(args[0])
        elif name == 'tan':
            return math.tan(args[0])
        elif name == 'log':
            return math.log(args[0])
        elif name == 'exp':
            return math.exp(args[0])
        elif name == 'abs':
            return abs(args[0])
        elif name == 'pow':
            return math.pow(args[0], args[1])
        
        # I/O functions
        elif name == 'print':
            output = ' '.join(str(arg) for arg in args)
            self.output_buffer.append(output)
            print(output)
            return None
        
        else:
            raise NameError(f"Function '{name}' is not defined")
    
    def execute_physics_op(self, operation: str, arguments: list) -> Any:
        """Execute physics operations"""
        args = [self.interpret(arg) for arg in arguments]
        
        if operation == 'schwarzschild':
            # schwarzschild(mass, radius)
            if len(args) < 2:
                raise ValueError("schwarzschild requires 2 arguments: mass, radius")
            result = self.physics_engine.schwarzschild_metrics(args[0], args[1])
            return {
                'event_horizon': result.event_horizon,
                'redshift': result.redshift,
                'escape_velocity': result.escape_velocity
            }
        
        elif operation == 'geodesic':
            # geodesic(x, y, z, vx, vy, vz, mass)
            if len(args) < 7:
                raise ValueError("geodesic requires 7 arguments: x, y, z, vx, vy, vz, mass")
            pos = (args[0], args[1], args[2])
            vel = (args[3], args[4], args[5])
            mass = args[6]
            result = self.physics_engine.geodesic_integration(pos, vel, mass)
            return {
                'trajectory_points': len(result.trajectory),
                'photon_sphere': result.photon_sphere_radius,
                'is_null': result.is_null_geodesic
            }
        
        elif operation == 'eddy':
            # eddy(velocity_field)
            if len(args) < 1:
                raise ValueError("eddy requires velocity field argument")
            # Expect velocity field as nested lists
            if not isinstance(args[0], (list, tuple)):
                raise ValueError("eddy requires velocity field as list")
            result = self.physics_engine.ocean_eddy_analysis(args[0])
            return {
                'strain_tensor': result.strain_tensor,
                'coherent_boundary': result.coherent_boundary
            }
        
        elif operation == 'tensor':
            # tensor(matrix_a, matrix_b)
            if len(args) < 2:
                raise ValueError("tensor requires 2 matrix arguments")
            result = self.physics_engine.tensor_product(args[0], args[1])
            return result
        
        else:
            raise RuntimeError(f"Unknown physics operation: {operation}")
    
    def execute_sovereignty_op(self, operation: str, arguments: list) -> Any:
        """Execute sovereignty operations"""
        args = [self.interpret(arg) for arg in arguments]
        
        if operation == 'isolate':
            # isolate(domain)
            if len(args) < 1:
                raise ValueError("isolate requires domain argument")
            domain = str(args[0])
            allowed = self.sovereignty.check_network_access(domain)
            return {
                'domain': domain,
                'allowed': allowed,
                'status': 'permitted' if allowed else 'blocked'
            }
        
        elif operation == 'monitor':
            # monitor() - check coherence
            result = self.sovereignty.monitor_coherence()
            return result
        
        elif operation == 'harden':
            # harden(data)
            if len(args) < 1:
                raise ValueError("harden requires data argument")
            data = str(args[0])
            boundary = self.sovereignty.protect_data(data)
            return boundary
        
        elif operation == 'audit':
            # audit() - get audit summary
            summary = self.sovereignty.get_audit_summary()
            return summary
        
        else:
            raise RuntimeError(f"Unknown sovereignty operation: {operation}")
    
    def get_output(self) -> str:
        """Get accumulated output"""
        return '\n'.join(self.output_buffer)
    
    def clear_output(self):
        """Clear output buffer"""
        self.output_buffer = []
