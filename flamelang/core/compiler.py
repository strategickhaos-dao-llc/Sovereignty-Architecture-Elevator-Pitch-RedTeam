"""
FlameLang Compiler
Main entry point and interpreter
"""
import sys
from typing import Dict, Any, Optional

try:
    from .lexer import Lexer, Token, TokenType
    from ..glyphs.registry import GLYPH_REGISTRY, get_glyph
    from ..physics.engine import ENGINE
    from ..security.sovereignty import PROTOCOL
except ImportError:
    from core.lexer import Lexer, Token, TokenType
    from glyphs.registry import GLYPH_REGISTRY, get_glyph
    from physics.engine import ENGINE
    from security.sovereignty import PROTOCOL


class FlameLangCompiler:
    """
    FlameLang Compiler and Interpreter
    Executes glyph-based code with physics and sovereignty
    """
    
    def __init__(self):
        self.variables = {}
        self.lexer = None
        self.tokens = []
        self.current_token_idx = 0
        
        # Initialize constants
        self._init_constants()
        
    def _init_constants(self):
        """Initialize physical constants"""
        self.variables.update(ENGINE.constants)
        
    def compile(self, source: str) -> Any:
        """
        Compile and execute FlameLang source code
        
        Args:
            source: FlameLang source code
            
        Returns:
            Execution result
        """
        # Lexical analysis
        self.lexer = Lexer(source)
        self.tokens = self.lexer.tokenize()
        self.current_token_idx = 0
        
        # Execute
        result = self.execute()
        return result
    
    def current_token(self) -> Optional[Token]:
        """Get current token"""
        if self.current_token_idx >= len(self.tokens):
            return None
        return self.tokens[self.current_token_idx]
    
    def advance(self):
        """Move to next token"""
        self.current_token_idx += 1
    
    def skip_newlines(self):
        """Skip newline tokens"""
        while self.current_token() and self.current_token().type == TokenType.NEWLINE:
            self.advance()
    
    def execute(self) -> Any:
        """Execute tokenized code"""
        results = []
        
        while self.current_token() and self.current_token().type != TokenType.EOF:
            self.skip_newlines()
            
            if not self.current_token() or self.current_token().type == TokenType.EOF:
                break
            
            # Skip comments
            if self.current_token().type == TokenType.COMMENT:
                self.advance()
                continue
            
            # Handle statements
            result = self.execute_statement()
            if result is not None:
                results.append(result)
        
        return results[-1] if results else None
    
    def execute_statement(self) -> Any:
        """Execute a single statement"""
        token = self.current_token()
        
        if not token:
            return None
        
        # Simulation command
        if token.type == TokenType.SIM:
            return self.execute_simulation()
        
        # Variable assignment
        if token.type == TokenType.IDENTIFIER:
            next_token = self.tokens[self.current_token_idx + 1] if self.current_token_idx + 1 < len(self.tokens) else None
            if next_token and next_token.type == TokenType.EQUALS:
                return self.execute_assignment()
            else:
                # Variable lookup
                var_name = token.value
                self.advance()
                return self.variables.get(var_name, None)
        
        # Constant lookup
        if token.type == TokenType.IDENTIFIER:
            value = self.variables.get(token.value)
            self.advance()
            return value
        
        # Glyph expression
        if token.type == TokenType.GLYPH:
            return self.execute_glyph_expression()
        
        # Unknown - skip
        self.advance()
        return None
    
    def execute_simulation(self) -> Dict:
        """Execute simulation command: sim BH1 M=... r=..."""
        self.advance()  # Skip 'sim'
        self.skip_newlines()
        
        # Get simulation type
        if not self.current_token() or self.current_token().type != TokenType.GLYPH:
            return {'error': 'Expected glyph after sim'}
        
        sim_type = self.current_token().value
        self.advance()
        
        # Parse parameters
        params = {}
        while self.current_token() and self.current_token().type not in [TokenType.NEWLINE, TokenType.EOF]:
            if self.current_token().type == TokenType.IDENTIFIER:
                param_name = self.current_token().value
                self.advance()
                
                if self.current_token() and self.current_token().type == TokenType.EQUALS:
                    self.advance()
                    
                    if self.current_token() and self.current_token().type == TokenType.NUMBER:
                        param_value = float(self.current_token().value)
                        params[param_name] = param_value
                        self.advance()
            else:
                self.advance()
        
        # Execute simulation
        return self.run_simulation(sim_type, params)
    
    def run_simulation(self, sim_type: str, params: Dict) -> Dict:
        """Run physics simulation"""
        if sim_type == 'BH1':
            # Black hole simulation
            mass = params.get('M', 1.989e30)  # Solar mass default
            radius = params.get('r', 1e7)     # 10,000 km default
            
            result = ENGINE.compute_schwarzschild(mass, radius)
            
            # Get frequency from glyph registry
            bh1_glyph = get_glyph('BH1')
            frequency = f"{bh1_glyph['frequency']}Hz" if bh1_glyph else '137Hz'
            
            # Format output
            output = {
                'simulation': 'Schwarzschild Black Hole',
                'frequency': frequency,
                'schwarzschild_radius_km': result['schwarzschild_radius'] / 1000,
                'redshift_factor': result['redshift_factor'],
                'escape_velocity_km_s': result['escape_velocity'] / 1000,
                'inside_horizon': result['is_inside_horizon'],
            }
            return output
        
        elif sim_type == 'PS1':
            # Photon sphere
            mass = params.get('M', 1.989e30)
            r_ps = ENGINE.photon_sphere_radius(mass)
            return {
                'simulation': 'Photon Sphere',
                'radius_km': r_ps / 1000,
            }
        
        elif sim_type == 'OC1':
            # Ocean eddy (placeholder)
            return {
                'simulation': 'Ocean Eddy',
                'status': 'Circulation analysis ready',
            }
        
        else:
            return {'error': f'Unknown simulation type: {sim_type}'}
    
    def execute_assignment(self) -> Any:
        """Execute variable assignment"""
        var_name = self.current_token().value
        self.advance()  # Skip identifier
        self.advance()  # Skip '='
        
        # Evaluate right-hand side
        value = None
        if self.current_token() and self.current_token().type == TokenType.NUMBER:
            value = float(self.current_token().value)
            self.advance()
        
        self.variables[var_name] = value
        return value
    
    def execute_glyph_expression(self) -> Any:
        """Execute glyph expression"""
        glyph = self.current_token().value
        self.advance()
        
        # Look up glyph info
        glyph_info = get_glyph(glyph)
        if glyph_info:
            return {
                'glyph': glyph,
                'name': glyph_info['name'],
                'frequency': glyph_info['frequency'],
                'description': glyph_info['description'],
            }
        
        return {'glyph': glyph, 'status': 'unknown'}


def compile_file(filename: str) -> Any:
    """Compile and execute a FlameLang file"""
    with open(filename, 'r', encoding='utf-8') as f:
        source = f.read()
    
    compiler = FlameLangCompiler()
    return compiler.compile(source)


def compile_string(source: str) -> Any:
    """Compile and execute FlameLang source string"""
    compiler = FlameLangCompiler()
    return compiler.compile(source)
