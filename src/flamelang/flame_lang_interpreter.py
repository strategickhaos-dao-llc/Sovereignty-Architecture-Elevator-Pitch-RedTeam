#!/usr/bin/env python3
"""
FlameLang Interpreter - A Resonance-Based Symbolic Execution System
Strategickhaos DAO LLC - Sovereignty Architecture
---
FlameLang is a glyph-based symbolic language where each symbol carries:
- A unique identifier (Symbol)
- A descriptive name (Glyph_Name)
- A frequency value (Frequency) representing resonance/vibration
- A function binding (Function) for execution
- A binding code (Binding_Code) for quick invocation
"""

import csv
import sys
import os
from pathlib import Path
from typing import Dict, Optional, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Glyph:
    """Represents a single FlameLang glyph with all its properties."""
    symbol: str
    name: str
    frequency: int
    function: str
    binding_code: str

    def __str__(self) -> str:
        return f"🔥 {self.symbol} ({self.name}) @ {self.frequency}Hz → {self.function} [{self.binding_code}]"


class GlyphTable:
    """Manages the glyph table - the lexicon of FlameLang symbols."""

    def __init__(self, csv_path: Optional[str] = None):
        self.glyphs: Dict[str, Glyph] = {}
        self.binding_map: Dict[str, Glyph] = {}

        if csv_path is None:
            csv_path = str(Path(__file__).parent / "glyph_table.csv")

        self.load_from_csv(csv_path)

    def load_from_csv(self, csv_path: str) -> None:
        """Load glyphs from the CSV glyph table."""
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"Glyph table not found: {csv_path}")

        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                glyph = Glyph(
                    symbol=row["Symbol"],
                    name=row["Glyph_Name"],
                    frequency=int(row["Frequency"]),
                    function=row["Function"],
                    binding_code=row["Binding_Code"],
                )
                self.glyphs[glyph.symbol] = glyph
                self.binding_map[glyph.binding_code] = glyph

    def get_by_symbol(self, symbol: str) -> Optional[Glyph]:
        """Look up a glyph by its symbol (e.g., 'AE1')."""
        return self.glyphs.get(symbol.upper())

    def get_by_binding(self, binding_code: str) -> Optional[Glyph]:
        """Look up a glyph by its binding code (e.g., '[999]')."""
        normalized = binding_code if binding_code.startswith("[") else f"[{binding_code}]"
        return self.binding_map.get(normalized)

    def search(self, query: str) -> List[Glyph]:
        """Search glyphs by partial name or function match."""
        query_lower = query.lower()
        return [
            g
            for g in self.glyphs.values()
            if query_lower in g.name.lower() or query_lower in g.function.lower()
        ]

    def list_all(self) -> List[Glyph]:
        """Return all glyphs sorted by symbol."""
        return sorted(self.glyphs.values(), key=lambda g: g.symbol)


class ResonanceEngine:
    """Handles the execution of glyph functions with neural sync metaphor."""

    def __init__(self):
        self.sync_state: Dict[str, bool] = {}
        self.execution_log: List[str] = []
        self.resonance_level: float = 0.0

    def execute_glyph(self, glyph: Glyph) -> str:
        """Execute a glyph's function and return the result."""
        timestamp = datetime.now().isoformat()

        # Simulate resonance calculation based on frequency
        resonance_delta = glyph.frequency / 1000.0
        self.resonance_level = min(1.0, self.resonance_level + resonance_delta)

        # Log execution
        log_entry = f"[{timestamp}] EXEC: {glyph.symbol} → {glyph.function} @ {glyph.frequency}Hz"
        self.execution_log.append(log_entry)

        # Generate execution output based on function type
        output_lines = [
            f"⚡ Executing: {glyph.name}",
            f"   Symbol: {glyph.symbol}",
            f"   Frequency: {glyph.frequency}Hz",
            f"   Function: {glyph.function}",
            f"   Binding: {glyph.binding_code}",
            f"   Resonance Level: {self.resonance_level:.3f}",
        ]

        # Special behaviors for certain glyph types
        if glyph.symbol.startswith("SY"):
            self.sync_state[glyph.symbol] = True
            output_lines.append("   🔗 Neural Sync complete. Resonance achieved.")
        elif glyph.symbol.startswith("ND"):
            output_lines.append(f"   📡 Node operation: {glyph.function}")
        elif glyph.symbol.startswith("SW"):
            output_lines.append(f"   🐝 Swarm directive: {glyph.function}")
        elif glyph.symbol.startswith("SC"):
            output_lines.append(f"   👑 Sovereignty assertion: {glyph.function}")
        elif glyph.symbol.startswith("VW"):
            output_lines.append(f"   📜 Vow binding: {glyph.function}")
        elif glyph.symbol.startswith("FL") or glyph.symbol.startswith("IG"):
            output_lines.append(f"   🔥 Flame intensity: {glyph.frequency}Hz")
        elif glyph.symbol.startswith("QT"):
            output_lines.append(f"   ⚛️  Quantum operation: {glyph.function}")

        return "\n".join(output_lines)

    def get_sync_status(self) -> str:
        """Get current neural sync status."""
        active_syncs = [k for k, v in self.sync_state.items() if v]
        return f"Active syncs: {active_syncs if active_syncs else 'None'}, Resonance: {self.resonance_level:.3f}"


class FlameLangInterpreter:
    """Main interpreter class for FlameLang."""

    def __init__(self, glyph_table_path: Optional[str] = None):
        self.glyph_table = GlyphTable(glyph_table_path)
        self.engine = ResonanceEngine()
        self.running = True

    def execute(self, command: str) -> str:
        """Execute a FlameLang command (symbol or binding code)."""
        command = command.strip()

        if not command:
            return ""

        # Check if it's a binding code (e.g., [999] or just 999)
        if command.startswith("[") or command.isdigit():
            glyph = self.glyph_table.get_by_binding(command)
        else:
            glyph = self.glyph_table.get_by_symbol(command)

        if glyph:
            return self.engine.execute_glyph(glyph)
        else:
            return f"❌ Glyph not found: {command}"

    def search(self, query: str) -> str:
        """Search for glyphs matching a query."""
        results = self.glyph_table.search(query)
        if not results:
            return f"No glyphs found matching: {query}"

        lines = [f"Found {len(results)} glyph(s):"]
        for glyph in results:
            lines.append(f"  {glyph}")
        return "\n".join(lines)

    def list_glyphs(self, filter_prefix: Optional[str] = None) -> str:
        """List all glyphs, optionally filtered by prefix."""
        glyphs = self.glyph_table.list_all()

        if filter_prefix:
            glyphs = [g for g in glyphs if g.symbol.startswith(filter_prefix.upper())]

        if not glyphs:
            return "No glyphs found."

        lines = [f"Glyph Table ({len(glyphs)} entries):"]
        lines.append("-" * 70)
        for glyph in glyphs:
            lines.append(str(glyph))
        return "\n".join(lines)

    def show_help(self) -> str:
        """Display help information."""
        return """
🔥 FlameLang Interpreter - Help
================================

COMMANDS:
  <SYMBOL>       Execute glyph by symbol (e.g., AE1, IG1, FL1)
  [CODE]         Execute glyph by binding code (e.g., [999], [800])
  
  list [PREFIX]  List all glyphs (optionally filtered by prefix)
  search <QUERY> Search glyphs by name or function
  status         Show current sync/resonance status
  log            Show execution log
  help           Show this help message
  exit / quit    Exit the interpreter

EXAMPLES:
  AE1            Execute AETHER_IGNITE glyph
  [999]          Execute glyph with binding code 999
  list FL        List all FLAME glyphs
  search sync    Find all sync-related glyphs

GLYPH CATEGORIES:
  AE* - Aether (initialization, flow)
  IG* - Ignis (core fire operations)
  FL* - Flame (flame states)
  SY* - Sync (neural synchronization)
  RS* - Resonance (frequency tuning)
  ND* - Node (mesh node operations)
  SW* - Swarm (collective operations)
  PR* - Protocol (execution control)
  SC* - Sovereign (authority assertions)
  VW* - Vow (commitment bindings)
  CH* - Chain (blockchain/linking)
  EM* - Ember (subtle states)
  FN* - Finalize (completion operations)
  CR* - Crypt (encryption)
  ME* - Mesh (network topology)
  QT* - Quantum (quantum operations)
  AL* - Align (calibration)
  DR* - Dream (dreamstate operations)
  TM* - Time (temporal operations)
  SP* - Spirit (meta operations)
"""

    def run_interactive(self) -> None:
        """Run the interpreter in interactive REPL mode."""
        print("🔥 FlameLang Interpreter v1.0")
        print("   Resonance-based symbolic execution system")
        print("   Type 'help' for commands, 'exit' to quit")
        print("-" * 50)

        while self.running:
            try:
                user_input = input("🔥 flamelang> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n✨ Resonance fading... Goodbye!")
                break

            if not user_input:
                continue

            command_lower = user_input.lower()

            if command_lower in ("exit", "quit"):
                print("✨ Resonance fading... Goodbye!")
                self.running = False
            elif command_lower == "help":
                print(self.show_help())
            elif command_lower == "status":
                print(self.engine.get_sync_status())
            elif command_lower == "log":
                if self.engine.execution_log:
                    for entry in self.engine.execution_log:
                        print(entry)
                else:
                    print("No executions logged yet.")
            elif command_lower.startswith("list"):
                parts = user_input.split(maxsplit=1)
                prefix = parts[1] if len(parts) > 1 else None
                print(self.list_glyphs(prefix))
            elif command_lower.startswith("search "):
                query = user_input[7:]
                print(self.search(query))
            else:
                result = self.execute(user_input)
                print(result)

    def run_batch(self, commands: List[str]) -> List[str]:
        """Execute a batch of commands and return results."""
        results = []
        for cmd in commands:
            result = self.execute(cmd)
            results.append(result)
        return results


def main() -> int:
    """Main entry point for the FlameLang interpreter."""
    import argparse

    parser = argparse.ArgumentParser(
        description="FlameLang Interpreter - Resonance-based symbolic execution",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python flame_lang_interpreter.py               # Interactive mode
  python flame_lang_interpreter.py -e AE1        # Execute single glyph
  python flame_lang_interpreter.py -e "[999]"    # Execute by binding code
  python flame_lang_interpreter.py -l            # List all glyphs
  python flame_lang_interpreter.py -s sync       # Search for glyphs
        """,
    )

    parser.add_argument(
        "-t",
        "--table",
        help="Path to glyph_table.csv",
        default=None,
    )
    parser.add_argument(
        "-e",
        "--execute",
        help="Execute a single glyph command",
    )
    parser.add_argument(
        "-l",
        "--list",
        action="store_true",
        help="List all glyphs",
    )
    parser.add_argument(
        "-s",
        "--search",
        help="Search glyphs by query",
    )
    parser.add_argument(
        "-p",
        "--prefix",
        help="Filter list by prefix (use with -l)",
    )

    args = parser.parse_args()

    try:
        interpreter = FlameLangInterpreter(args.table)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    if args.execute:
        print(interpreter.execute(args.execute))
    elif args.list:
        print(interpreter.list_glyphs(args.prefix))
    elif args.search:
        print(interpreter.search(args.search))
    else:
        interpreter.run_interactive()

    return 0


if __name__ == "__main__":
    sys.exit(main())
