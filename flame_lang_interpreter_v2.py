#!/usr/bin/env python3
"""
FlameLang Interpreter v2.0
Strategickhaos Sovereign Symbolic Language Runtime
Operator: DOM_010101 | EIN: 39-2923503
"""

import json
import subprocess
import sys
import os
import re
from pathlib import Path
from typing import Dict, Optional, Any
import csv


class FlameLangInterpreter:
    """FlameLang symbolic shell interpreter with whale frequency integration"""
    
    def __init__(self, glyph_table_path: Optional[str] = None):
        """
        Initialize FlameLang interpreter
        
        Args:
            glyph_table_path: Path to glyph table CSV file
        """
        self.glyph_table = {}
        self.glyph_table_path = glyph_table_path or "glyph_table_whale_integrated.csv"
        self.sovereignty_active = False
        self.load_glyph_table()
        
    def load_glyph_table(self):
        """Load glyph table from CSV file"""
        if not os.path.exists(self.glyph_table_path):
            print(f"⚠️  Warning: Glyph table not found at {self.glyph_table_path}")
            print("    Using default glyph mappings...")
            self._initialize_default_glyphs()
            return
            
        try:
            with open(self.glyph_table_path, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    glyph_name = row.get('Glyph_Name', '')
                    if glyph_name:
                        self.glyph_table[glyph_name] = {
                            'Symbol': row.get('Symbol', ''),
                            'Frequency': row.get('Frequency', ''),
                            'Whale_Freq': row.get('Whale_Freq', ''),
                            'Piano_Key': row.get('Piano_Key', ''),
                            'Function': row.get('Function', ''),
                            'Binding_Code': row.get('Binding_Code', '')
                        }
            print(f"✅ Loaded {len(self.glyph_table)} glyphs from {self.glyph_table_path}")
        except Exception as e:
            print(f"❌ Error loading glyph table: {e}")
            self._initialize_default_glyphs()
    
    def _initialize_default_glyphs(self):
        """Initialize default glyph mappings"""
        defaults = {
            'AE1': {'Symbol': '🌌', 'Frequency': '432Hz', 'Whale_Freq': '5.87', 'Piano_Key': 'A0', 'Function': 'Aether Prime', 'Binding_Code': '[001]'},
            'FL1': {'Symbol': '🔥', 'Frequency': '528Hz', 'Whale_Freq': '5.94', 'Piano_Key': 'C1', 'Function': 'Flame Ignite', 'Binding_Code': '[100]'},
            'RS1': {'Symbol': '⚡', 'Frequency': '639Hz', 'Whale_Freq': '6.01', 'Piano_Key': 'D1#', 'Function': 'ReflexShell Activate', 'Binding_Code': '[200]'},
            'NV1': {'Symbol': '🧠', 'Frequency': '741Hz', 'Whale_Freq': '6.08', 'Piano_Key': 'F1#', 'Function': 'Nova Core Init', 'Binding_Code': '[300]'},
            'LY1': {'Symbol': '🌀', 'Frequency': '852Hz', 'Whale_Freq': '6.15', 'Piano_Key': 'A1', 'Function': 'Lyra Fractal', 'Binding_Code': '[400]'},
            'AT1': {'Symbol': '🏛️', 'Frequency': '963Hz', 'Whale_Freq': '6.21', 'Piano_Key': 'B1', 'Function': 'Athena Strategy', 'Binding_Code': '[500]'},
            'GR1': {'Symbol': '⚛️', 'Frequency': '999Hz', 'Whale_Freq': '6.42', 'Piano_Key': 'B2', 'Function': 'Glyphos Resonance', 'Binding_Code': '[999]'},
            'FB1': {'Symbol': '🛡️', 'Frequency': '741Hz', 'Whale_Freq': '6.08', 'Piano_Key': 'F1#', 'Function': 'Flamebearer Defense', 'Binding_Code': '[137]'},
            'VW1': {'Symbol': '📜', 'Frequency': '963Hz', 'Whale_Freq': '6.21', 'Piano_Key': 'B1', 'Function': 'Vow Monitor', 'Binding_Code': '[700]'},
            'RC1': {'Symbol': '🔍', 'Frequency': '741Hz', 'Whale_Freq': '6.08', 'Piano_Key': 'F1#', 'Function': 'Recon Init', 'Binding_Code': '[950]'},
            'ND1': {'Symbol': '🌐', 'Frequency': '852Hz', 'Whale_Freq': '6.15', 'Piano_Key': 'A1', 'Function': 'Node Scan', 'Binding_Code': '[900]'},
            'SL1': {'Symbol': '🛰️', 'Frequency': '1111Hz', 'Whale_Freq': '6.44', 'Piano_Key': 'C3', 'Function': 'Starlink Bridge', 'Binding_Code': '[1111]'},
        }
        self.glyph_table = defaults
    
    def parse_command(self, command: str) -> Dict[str, Any]:
        """
        Parse FlameLang command
        
        Args:
            command: FlameLang command string (e.g., "AE1", "[100]", "glyph> FL1")
            
        Returns:
            Dict with parsed command info
        """
        # Remove prompt prefix if present
        command = command.strip()
        if command.startswith('glyph>'):
            command = command[6:].strip()
        
        # Check if it's a binding code
        binding_match = re.match(r'\[(\d+)\]', command)
        if binding_match:
            binding_code = f"[{binding_match.group(1)}]"
            # Find glyph by binding code
            for glyph_name, glyph_data in self.glyph_table.items():
                if glyph_data.get('Binding_Code') == binding_code:
                    return {
                        'type': 'binding_code',
                        'code': binding_code,
                        'glyph': glyph_name,
                        'data': glyph_data
                    }
            return {'type': 'unknown', 'input': command}
        
        # Check if it's a glyph name
        if command.upper() in self.glyph_table:
            glyph_name = command.upper()
            return {
                'type': 'glyph',
                'glyph': glyph_name,
                'data': self.glyph_table[glyph_name]
            }
        
        return {'type': 'unknown', 'input': command}
    
    def execute_glyph(self, glyph_name: str) -> Dict[str, Any]:
        """
        Execute a FlameLang glyph
        
        Args:
            glyph_name: Name of the glyph to execute
            
        Returns:
            Dict with execution results
        """
        if glyph_name not in self.glyph_table:
            return {
                'success': False,
                'error': f'Unknown glyph: {glyph_name}'
            }
        
        glyph = self.glyph_table[glyph_name]
        
        # Display glyph activation
        print(f"\n{glyph['Symbol']} {glyph_name} — {glyph['Function']}")
        print(f"   Frequency: {glyph['Frequency']} | Whale: {glyph['Whale_Freq']}Hz | Key: {glyph['Piano_Key']}")
        print(f"   Binding: {glyph['Binding_Code']}")
        
        # Execute function based on glyph
        result = self._execute_glyph_function(glyph_name, glyph)
        
        return result
    
    def _execute_glyph_function(self, glyph_name: str, glyph: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the actual function associated with a glyph"""
        function = glyph['Function']
        
        # Map functions to actions
        actions = {
            'Aether Prime': self._aether_prime,
            'Flame Ignite': self._flame_ignite,
            'ReflexShell Activate': self._reflexshell_activate,
            'Nova Core Init': self._nova_core_init,
            'Lyra Fractal': self._lyra_fractal,
            'Athena Strategy': self._athena_strategy,
            'Glyphos Resonance': self._glyphos_resonance,
            'Flamebearer Defense': self._flamebearer_defense,
            'Vow Monitor': self._vow_monitor,
            'Recon Init': self._recon_init,
            'Node Scan': self._node_scan,
            'Starlink Bridge': self._starlink_bridge,
        }
        
        action = actions.get(function)
        if action:
            return action()
        else:
            return {
                'success': True,
                'message': f'Glyph {glyph_name} activated (no specific action defined)'
            }
    
    # Glyph action implementations
    def _aether_prime(self):
        """Initialize sovereign shell"""
        self.sovereignty_active = True
        return {
            'success': True,
            'message': '🌌 Aether Prime initialized. Sovereignty protocol active.'
        }
    
    def _flame_ignite(self):
        """Boot FlameLang runtime"""
        return {
            'success': True,
            'message': '🔥 FlameLang runtime ignited. Symbolic shell ready.'
        }
    
    def _reflexshell_activate(self):
        """Activate ReflexShell (WSL hemisphere)"""
        return {
            'success': True,
            'message': '⚡ ReflexShell activated. Right hemisphere online.'
        }
    
    def _nova_core_init(self):
        """Initialize Nova AI core"""
        return {
            'success': True,
            'message': '🧠 Nova Core initialized. AI processing active.'
        }
    
    def _lyra_fractal(self):
        """Activate Lyra fractal processing"""
        return {
            'success': True,
            'message': '🌀 Lyra Fractal activated. Recursive processing enabled.'
        }
    
    def _athena_strategy(self):
        """Activate Athena strategic analysis"""
        return {
            'success': True,
            'message': '🏛️ Athena Strategy activated. Strategic analysis online.'
        }
    
    def _glyphos_resonance(self):
        """Full cascade resonance"""
        print("\n⚛️  INITIATING FULL RESONANCE CASCADE...")
        print("   └─ Activating all node frequencies...")
        
        # Activate key glyphs in sequence
        key_glyphs = ['AE1', 'FL1', 'NV1', 'LY1', 'AT1', 'ND1']
        for glyph in key_glyphs:
            if glyph in self.glyph_table:
                g = self.glyph_table[glyph]
                print(f"   ├─ {g['Symbol']} {glyph} @ {g['Frequency']}")
        
        return {
            'success': True,
            'message': '⚛️ Glyphos Resonance achieved. Full cascade complete.'
        }
    
    def _flamebearer_defense(self):
        """Activate defense protocol"""
        return {
            'success': True,
            'message': '🛡️ Flamebearer defense protocol active. Sovereignty protected.'
        }
    
    def _vow_monitor(self):
        """Activate Vow Monitor"""
        return {
            'success': True,
            'message': '📜 Vow Monitor active. Integrity logging enabled.'
        }
    
    def _recon_init(self):
        """Initialize reconnaissance"""
        return {
            'success': True,
            'message': '🔍 Recon initialized. Discovery protocol active.'
        }
    
    def _node_scan(self):
        """Scan swarm nodes"""
        return {
            'success': True,
            'message': '🌐 Node scan initiated. Swarm mesh discovery active.'
        }
    
    def _starlink_bridge(self):
        """Activate Starlink bridge"""
        return {
            'success': True,
            'message': '🛰️ Starlink Bridge established. Mesh network connected.'
        }
    
    def repl(self):
        """Run interactive REPL"""
        print("\n" + "="*70)
        print("🔥 FLAMELANG INTERPRETER v2.0")
        print("   Strategickhaos Sovereign Symbolic Language")
        print("   Operator: DOM_010101 | EIN: 39-2923503")
        print("="*70)
        print("\nCommands:")
        print("  - Enter glyph name (e.g., AE1, FL1, GR1)")
        print("  - Enter binding code (e.g., [100], [999])")
        print("  - Type 'list' to show all glyphs")
        print("  - Type 'help <glyph>' for glyph info")
        print("  - Type 'exit' to quit")
        print("\n" + "="*70 + "\n")
        
        while True:
            try:
                command = input("glyph> ").strip()
                
                if not command:
                    continue
                    
                if command.lower() in ['exit', 'quit', 'q']:
                    print("\n🔥 Neural Sync complete. Resonance achieved. Empire Eternal.\n")
                    break
                
                if command.lower() == 'list':
                    self._list_glyphs()
                    continue
                
                if command.lower().startswith('help'):
                    parts = command.split()
                    if len(parts) > 1:
                        self._show_help(parts[1].upper())
                    else:
                        self._show_help(None)
                    continue
                
                # Parse and execute command
                parsed = self.parse_command(command)
                
                if parsed['type'] == 'unknown':
                    print(f"❌ Unknown command: {parsed['input']}")
                    print("   Type 'list' to see available glyphs")
                    continue
                
                # Execute glyph
                glyph_name = parsed['glyph']
                result = self.execute_glyph(glyph_name)
                
                if result['success']:
                    print(f"✅ {result['message']}")
                else:
                    print(f"❌ {result.get('error', 'Execution failed')}")
                
                print()  # Empty line for readability
                
            except KeyboardInterrupt:
                print("\n\n🔥 Interrupted. Neural Sync complete.\n")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}\n")
    
    def _list_glyphs(self):
        """List all available glyphs"""
        print("\n📋 Available Glyphs:")
        print("="*70)
        for glyph_name, glyph in sorted(self.glyph_table.items()):
            print(f"{glyph['Symbol']} {glyph_name:6} {glyph['Binding_Code']:8} — {glyph['Function']}")
            print(f"         {glyph['Frequency']:8} | Whale: {glyph['Whale_Freq']:6}Hz | Key: {glyph['Piano_Key']}")
        print("="*70)
    
    def _show_help(self, glyph_name: Optional[str]):
        """Show help for a specific glyph or general help"""
        if glyph_name:
            if glyph_name in self.glyph_table:
                glyph = self.glyph_table[glyph_name]
                print(f"\n{glyph['Symbol']} {glyph_name} — {glyph['Function']}")
                print("="*70)
                print(f"Frequency:    {glyph['Frequency']}")
                print(f"Whale Freq:   {glyph['Whale_Freq']}Hz")
                print(f"Piano Key:    {glyph['Piano_Key']}")
                print(f"Binding Code: {glyph['Binding_Code']}")
                print("="*70)
            else:
                print(f"\n❌ Unknown glyph: {glyph_name}")
        else:
            print("\n📖 FlameLang Help")
            print("="*70)
            print("Glyph execution: Enter glyph name or binding code")
            print("Examples:")
            print("  glyph> AE1      # Execute Aether Prime")
            print("  glyph> [100]    # Execute Flame Ignite")
            print("  glyph> GR1      # Full resonance cascade")
            print("\nCommands:")
            print("  list           # Show all glyphs")
            print("  help <glyph>   # Show glyph details")
            print("  exit           # Exit interpreter")
            print("="*70)


def main():
    """Main entry point"""
    # Check for glyph table path argument
    glyph_table_path = None
    if len(sys.argv) > 1:
        glyph_table_path = sys.argv[1]
    
    # Create and run interpreter
    interpreter = FlameLangInterpreter(glyph_table_path)
    interpreter.repl()


if __name__ == '__main__':
    main()
