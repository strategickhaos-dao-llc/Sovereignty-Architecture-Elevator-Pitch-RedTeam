"""
FlameLang REPL
Interactive shell with PowerShell-like features
"""
import sys
from typing import Optional

try:
    from .compiler import FlameLangCompiler
    from ..glyphs.registry import GLYPH_REGISTRY
    from ..physics.engine import CONSTANTS
    from ..security.sovereignty import PROTOCOL
except ImportError:
    from core.compiler import FlameLangCompiler
    from glyphs.registry import GLYPH_REGISTRY
    from physics.engine import CONSTANTS
    from security.sovereignty import PROTOCOL


class REPL:
    """
    FlameLang Read-Eval-Print Loop
    Interactive programming environment
    """
    
    def __init__(self):
        self.compiler = FlameLangCompiler()
        self.history = []
        self.running = True
        
    def print_banner(self):
        """Print welcome banner"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║          🔥 FlameLang v0.1.0 - Sovereign REPL 🔥            ║
║                                                              ║
║  Glyph-based programming with physics simulation            ║
║  Type 'help' for commands, 'exit' to quit                   ║
║                                                              ║
║  Sovereignty: ACTIVE | Network: ISOLATED | Freq: 137Hz      ║
╚══════════════════════════════════════════════════════════════╝
"""
        print(banner)
    
    def print_help(self):
        """Print help information"""
        help_text = """
🔥 FlameLang Commands:

Simulations:
  sim BH1 M=1.989e30 r=1e7    - Black hole simulation
  sim PS1 M=1.989e30          - Photon sphere
  sim OC1                     - Ocean eddy

Glyphs:
  ⚡ 🔥 🌊 ⚛️ 🎯 🔮           - Core glyphs
  🛡️ 🔒 👁️ ⚔️ 🌐           - Security glyphs
  BH1 OC1 PS1 GR1 ED1 MT1    - Physics glyphs

Constants:
  c, G, alpha, pi, e, phi    - Physical constants

REPL Commands:
  help      - Show this help
  glyphs    - List all glyphs
  constants - List all constants
  status    - Sovereignty status
  clear     - Clear screen
  exit      - Exit REPL
"""
        print(help_text)
    
    def list_glyphs(self):
        """List all available glyphs"""
        print("\n🔥 FlameLang Glyph Registry:\n")
        
        categories = {}
        for symbol, info in GLYPH_REGISTRY.items():
            cat = info['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append((symbol, info))
        
        for category, glyphs in sorted(categories.items()):
            print(f"{category.upper()}:")
            for symbol, info in glyphs:
                print(f"  {symbol:6} {info['name']:20} {info['frequency']:4}Hz  {info['description']}")
            print()
    
    def list_constants(self):
        """List all physical constants"""
        print("\n🔥 Physical Constants:\n")
        for name, value in CONSTANTS.items():
            print(f"  {name:10} = {value}")
        print()
    
    def show_status(self):
        """Show sovereignty protocol status"""
        status = PROTOCOL.get_sovereignty_status()
        print("\n🔥 Sovereignty Status:\n")
        print(f"  Network Isolated:  {status['network_isolated']}")
        print(f"  Boundary Hash:     {status['boundary_hash'][:32]}...")
        print(f"  Telemetry Detected: {status['telemetry_detected_count']}")
        print(f"  Coherence Checks:  {status['coherence_checks_count']}")
        print(f"  Sovereign:         {status['sovereign']}")
        print()
    
    def format_result(self, result) -> str:
        """Format execution result for display"""
        if result is None:
            return ""
        
        if isinstance(result, dict):
            lines = []
            for key, value in result.items():
                if isinstance(value, float):
                    lines.append(f"  {key}: {value:.6g}")
                else:
                    lines.append(f"  {key}: {value}")
            return "\n".join(lines)
        
        return str(result)
    
    def execute(self, source: str) -> Optional[str]:
        """Execute FlameLang code and return formatted output"""
        if not source.strip():
            return None
        
        try:
            result = self.compiler.compile(source)
            return self.format_result(result)
        except Exception as e:
            return f"Error: {e}"
    
    def run(self):
        """Run the REPL"""
        self.print_banner()
        
        while self.running:
            try:
                # Prompt
                line = input("🔥> ")
                
                # Add to history
                if line.strip():
                    self.history.append(line)
                
                # Handle REPL commands
                if line.strip().lower() == 'exit':
                    print("\n🔥 Stay sovereign. Goodbye.")
                    break
                
                if line.strip().lower() == 'help':
                    self.print_help()
                    continue
                
                if line.strip().lower() == 'glyphs':
                    self.list_glyphs()
                    continue
                
                if line.strip().lower() == 'constants':
                    self.list_constants()
                    continue
                
                if line.strip().lower() == 'status':
                    self.show_status()
                    continue
                
                if line.strip().lower() == 'clear':
                    print("\033[2J\033[H")  # ANSI clear screen
                    self.print_banner()
                    continue
                
                # Execute FlameLang code
                output = self.execute(line)
                if output:
                    print(output)
            
            except KeyboardInterrupt:
                print("\n(Use 'exit' to quit)")
                continue
            
            except EOFError:
                print("\n🔥 Stay sovereign. Goodbye.")
                break


def start_repl():
    """Start the FlameLang REPL"""
    repl = REPL()
    repl.run()
