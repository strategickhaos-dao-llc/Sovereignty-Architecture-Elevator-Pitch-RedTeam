#!/usr/bin/env python3
"""FlameLang REPL - Interactive interpreter."""

import sys
import os
from typing import Dict, Any, Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.lexer import Lexer, TokenType
from glyphs.registry import REGISTRY
from physics.engine import ENGINE, PhysicsConstants
from security.sovereignty import SOVEREIGNTY

class Interpreter:
    """FlameLang interpreter."""
    
    def __init__(self):
        self.variables: Dict[str, Any] = {}
        self.glyphs = REGISTRY
        self.physics = ENGINE
        self.sovereignty = SOVEREIGNTY
        self.constants = PhysicsConstants()
        
        # Initialize built-in constants
        self.variables['pi'] = self.constants.pi
        self.variables['e'] = self.constants.e
        self.variables['phi'] = self.constants.phi
        self.variables['c'] = self.constants.c
        self.variables['G'] = self.constants.G
        self.variables['alpha'] = self.constants.alpha
    
    def execute(self, source: str) -> Optional[Any]:
        """Execute FlameLang code."""
        source = source.strip()
        
        # Handle empty input
        if not source:
            return None
        
        # Handle meta commands
        if source.startswith('.'):
            return self.handle_meta_command(source)
        
        # Tokenize
        try:
            lexer = Lexer(source)
            tokens = lexer.tokenize()
        except SyntaxError as e:
            print(f"Syntax error: {e}")
            return None
        
        # Filter out newlines and EOF
        tokens = [t for t in tokens if t.type not in (TokenType.NEWLINE, TokenType.EOF)]
        
        if not tokens:
            return None
        
        # Parse and execute based on first token
        try:
            if tokens[0].type == TokenType.SIM:
                return self.execute_sim(tokens)
            elif len(tokens) >= 3 and tokens[1].type == TokenType.EQUALS:
                return self.execute_assignment(tokens)
            elif tokens[0].type == TokenType.GLYPH:
                return self.execute_glyph_pipeline(tokens)
            else:
                print(f"Unknown command starting with: {tokens[0].value}")
                return None
        except Exception as e:
            print(f"Execution error: {e}")
            return None
    
    def execute_sim(self, tokens) -> Optional[Any]:
        """Execute simulation command: sim BH1 M=1.989e30 r=1e7"""
        if len(tokens) < 2:
            print("Usage: sim <NAME> [param=value ...]")
            return None
        
        sim_name = tokens[1].value
        params = {}
        
        # Parse parameters
        i = 2
        while i < len(tokens):
            if i + 2 < len(tokens) and tokens[i + 1].type == TokenType.EQUALS:
                param_name = tokens[i].value
                param_value = tokens[i + 2].value
                params[param_name] = param_value
                i += 3
            else:
                i += 1
        
        # Execute simulation based on name
        glyph = self.glyphs.get(sim_name)
        
        if glyph and glyph.category == 'physics':
            if sim_name == 'BH1':
                M = params.get('M', 1.989e30)
                r = params.get('r', 1e7)
                result = self.physics.simulate_black_hole(sim_name, float(M), float(r))
                print(f"✓ {sim_name}: Schwarzschild radius = {result['r_s']/1000:.2f} km, g_tt = {result['g_tt']:.6f}")
                return result
            
            elif sim_name == 'OC1':
                coherence = params.get('coherence', 0.95)
                result = self.physics.simulate_ocean_eddy(sim_name, float(coherence))
                print(f"✓ {sim_name}: Ocean eddy coherence = {result['coherence']:.2f}")
                return result
            
            elif sim_name == 'PS1':
                M = params.get('M', 1.989e30)
                result = self.physics.simulate_photon_sphere(sim_name, float(M))
                print(f"✓ {sim_name}: Photon sphere radius = {result['r_photon']/1000:.2f} km")
                return result
            
            else:
                print(f"Simulation {sim_name} not yet implemented")
                return None
        else:
            print(f"Unknown simulation: {sim_name}")
            return None
    
    def execute_assignment(self, tokens) -> Optional[Any]:
        """Execute variable assignment: x = 42"""
        var_name = tokens[0].value
        value = tokens[2].value
        
        self.variables[var_name] = value
        print(f"✓ {var_name} = {value}")
        return value
    
    def execute_glyph_pipeline(self, tokens) -> Optional[Any]:
        """Execute glyph pipeline: ⚡ -> [OC1] |> 🔥"""
        operations = []
        i = 0
        
        while i < len(tokens):
            token = tokens[i]
            
            if token.type == TokenType.GLYPH:
                glyph = self.glyphs.get(token.value)
                if glyph:
                    operations.append(('glyph', glyph))
                else:
                    print(f"Unknown glyph: {token.value}")
            
            elif token.type == TokenType.LBRACKET:
                # Get simulation reference
                if i + 2 < len(tokens) and tokens[i + 1].type == TokenType.IDENTIFIER:
                    sim_name = tokens[i + 1].value
                    sim = self.physics.get_simulation(sim_name)
                    if sim:
                        operations.append(('sim', sim))
                    else:
                        print(f"Simulation not found: {sim_name}")
                    i += 2  # Skip to ]
            
            i += 1
        
        # Execute pipeline
        if operations:
            print(f"✓ Pipeline executed with {len(operations)} operations")
            for op_type, op_data in operations:
                if op_type == 'glyph':
                    print(f"  - {op_data.symbol} {op_data.name} @ {op_data.frequency}Hz")
                elif op_type == 'sim':
                    print(f"  - [{op_data['name']}] {op_data['type']}")
            return operations
        
        return None
    
    def handle_meta_command(self, command: str) -> Optional[Any]:
        """Handle REPL meta commands."""
        cmd = command.strip().lower()
        
        if cmd == '.help':
            self.show_help()
        elif cmd == '.glyphs':
            self.show_glyphs()
        elif cmd == '.physics':
            self.show_physics()
        elif cmd == '.vars':
            self.show_variables()
        elif cmd == '.exit':
            print("🔥 Stay Sovereign. Compute Freely. 🔥")
            sys.exit(0)
        else:
            print(f"Unknown meta command: {cmd}")
            print("Type .help for available commands")
        
        return None
    
    def show_help(self):
        """Show help information."""
        print("""
FlameLang REPL Meta Commands:
  .help      Show this help
  .glyphs    List all glyphs
  .physics   Show physics status
  .vars      Show variables
  .exit      Exit REPL

Syntax:
  sim BH1 M=1e30 r=1e7       # Create simulation
  x = 42                      # Variable assignment
  ⚡ -> [OC1] |> 🔥            # Glyph pipeline
  🛡️ -> 🔒                    # Security operations
""")
    
    def show_glyphs(self):
        """Show all registered glyphs."""
        print("\nRegistered Glyphs:")
        for category in ['core', 'physics', 'security']:
            print(f"\n{category.upper()}:")
            glyphs = self.glyphs.by_category(category)
            for glyph in sorted(glyphs, key=lambda g: g.name):
                print(f"  {glyph.symbol:4} {glyph.name:20} @ {glyph.frequency}Hz")
    
    def show_physics(self):
        """Show physics engine status."""
        print("\nPhysics Engine Status:")
        sims = self.physics.list_simulations()
        if sims:
            for name, sim in sims.items():
                print(f"  [{name}] {sim['type']}")
        else:
            print("  No simulations running")
        
        print(f"\nConstants: pi={self.constants.pi:.5f}, e={self.constants.e:.5f}, c={self.constants.c}, G={self.constants.G:.5e}")
    
    def show_variables(self):
        """Show all variables."""
        print("\nVariables:")
        if self.variables:
            for name, value in sorted(self.variables.items()):
                print(f"  {name} = {value}")
        else:
            print("  No variables defined")

def repl():
    """Run the FlameLang REPL."""
    print("🔥 FlameLang REPL v0.1.0")
    print("Type .help for commands, .exit to quit")
    print("=" * 60)
    
    # Initialize sovereignty
    SOVEREIGNTY.initialize_sovereign_environment()
    print()
    
    interpreter = Interpreter()
    
    while True:
        try:
            line = input("🔥> ")
            interpreter.execute(line)
        except KeyboardInterrupt:
            print("\n🔥 Stay Sovereign. Compute Freely. 🔥")
            break
        except EOFError:
            print("\n🔥 Stay Sovereign. Compute Freely. 🔥")
            break

def main():
    """Entry point for REPL."""
    repl()

if __name__ == '__main__':
    main()
