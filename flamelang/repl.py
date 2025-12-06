"""
FlameLang REPL (Read-Eval-Print Loop)
Interactive shell for FlameLang
"""

import sys
from typing import Optional

from .core.lexer import Lexer
from .core.parser import Parser
from .core.interpreter import Interpreter


class REPL:
    """Interactive FlameLang shell"""
    
    BANNER = """
╔═══════════════════════════════════════════════════════╗
║           🔥 FlameLang REPL v0.1.0 🔥                ║
║        Sovereign Computing Platform                   ║
╚═══════════════════════════════════════════════════════╝

Type 'help' for help, 'exit' or Ctrl+D to exit.
Glyphs: 🔥 ⚔ ▶ 🧠 🌐 ⟐ ◇ ∿ 〜 ⚡ α ◉ ⟁ ⊕ ⊗ ∇ ∫
    """
    
    HELP_TEXT = """
FlameLang Commands:
  help              Show this help message
  exit, quit        Exit the REPL
  clear             Clear the screen
  glyphs            Show available glyphs
  constants         Show built-in constants
  
Built-in Functions:
  print(x)          Print value
  sqrt(x)           Square root
  sin(x), cos(x)    Trigonometric functions
  log(x), exp(x)    Logarithm and exponential
  abs(x), pow(x,y)  Absolute value and power
  
Physics Operations:
  schwarzschild(mass, radius)        Calculate black hole metrics
  geodesic(x,y,z,vx,vy,vz,mass)     Integrate geodesic
  eddy([[u,v]])                      Analyze ocean eddies
  tensor(A, B)                       Tensor product
  
Sovereignty Operations:
  isolate(domain)   Check network isolation
  monitor()         Check system coherence
  harden(data)      Create cryptographic boundary
  audit()           Get audit summary
  
Examples:
  let x = 42
  print(x * 2)
  🔥  # Glyph with 741Hz frequency
  schwarzschild(1.989e30, 1e10)
  isolate("analytics.google.com")
    """
    
    def __init__(self):
        self.interpreter = Interpreter()
        self.multiline_buffer = []
        self.in_multiline = False
    
    def show_banner(self):
        """Display welcome banner"""
        print(self.BANNER)
    
    def show_help(self):
        """Display help text"""
        print(self.HELP_TEXT)
    
    def show_glyphs(self):
        """Display available glyphs"""
        print("\n🔥 Available Glyphs:")
        print("=" * 60)
        
        glyphs = self.interpreter.glyph_registry.list_all()
        glyphs.sort(key=lambda g: g.frequency, reverse=True)
        
        for glyph in glyphs:
            print(f"{glyph.symbol:3} {glyph.name:15} {glyph.frequency:4}Hz  {glyph.function}")
        
        print(f"\nTotal: {len(glyphs)} glyphs")
        print("=" * 60)
    
    def show_constants(self):
        """Display built-in constants"""
        print("\n🔥 Built-in Constants:")
        print("=" * 40)
        
        constants = {
            'pi': 'π (3.14159...)',
            'e': "Euler's number (2.71828...)",
            'phi': 'Golden ratio (1.61803...)',
            'c': 'Speed of light (m/s)',
            'G': 'Gravitational constant',
            'h': 'Planck constant',
            'alpha': 'Fine structure constant'
        }
        
        for name, description in constants.items():
            value = self.interpreter.environment.get(name)
            print(f"{name:8} = {value:15.6e}  # {description}")
        
        print("=" * 40)
    
    def evaluate(self, source: str) -> Optional[str]:
        """
        Evaluate FlameLang source code
        
        Args:
            source: Source code string
            
        Returns:
            Result string or None
        """
        try:
            # Lexical analysis
            lexer = Lexer(source)
            tokens = lexer.tokenize()
            
            # Syntax analysis
            parser = Parser(tokens)
            ast = parser.parse()
            
            # Execution
            self.interpreter.clear_output()
            result = self.interpreter.interpret(ast)
            
            # Get any print output
            output = self.interpreter.get_output()
            
            # Format result
            result_str = None
            if output:
                result_str = output
            elif result is not None:
                if isinstance(result, dict):
                    # Pretty print dictionaries
                    import json
                    result_str = json.dumps(result, indent=2)
                else:
                    result_str = str(result)
            
            return result_str
            
        except SyntaxError as e:
            return f"Syntax Error: {e}"
        except Exception as e:
            return f"Error: {e}"
    
    def run(self):
        """Run the REPL loop"""
        self.show_banner()
        
        while True:
            try:
                # Prompt
                if self.in_multiline:
                    prompt = "... "
                else:
                    prompt = "🔥▶ "
                
                # Read input
                try:
                    line = input(prompt)
                except EOFError:
                    print("\n👋 Goodbye!")
                    break
                
                # Handle special commands
                line_stripped = line.strip()
                
                if line_stripped in ['exit', 'quit']:
                    print("👋 Goodbye!")
                    break
                
                if line_stripped == 'help':
                    self.show_help()
                    continue
                
                if line_stripped == 'glyphs':
                    self.show_glyphs()
                    continue
                
                if line_stripped == 'constants':
                    self.show_constants()
                    continue
                
                if line_stripped == 'clear':
                    print('\033[2J\033[H')  # Clear screen
                    continue
                
                if not line_stripped:
                    continue
                
                # Check for multiline input (ends with backslash)
                if line_stripped.endswith('\\'):
                    self.multiline_buffer.append(line_stripped[:-1])
                    self.in_multiline = True
                    continue
                
                # Complete multiline input
                if self.in_multiline:
                    self.multiline_buffer.append(line)
                    source = '\n'.join(self.multiline_buffer)
                    self.multiline_buffer = []
                    self.in_multiline = False
                else:
                    source = line
                
                # Evaluate
                result = self.evaluate(source)
                
                # Print result
                if result:
                    print(result)
                
            except KeyboardInterrupt:
                print("\n(Use 'exit' or Ctrl+D to quit)")
                self.multiline_buffer = []
                self.in_multiline = False
                continue
            except Exception as e:
                print(f"Unexpected error: {e}")
                continue


if __name__ == '__main__':
    repl = REPL()
    repl.run()
