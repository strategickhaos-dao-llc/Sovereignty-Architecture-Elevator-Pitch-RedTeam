#!/usr/bin/env python3
"""
Unit tests for FlameLang Interpreter
"""

import csv
import os
import shutil
import tempfile
import unittest
from pathlib import Path

# Add parent directory to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent))

from flame_lang_interpreter import (
    Glyph,
    GlyphTable,
    ResonanceEngine,
    FlameLangInterpreter,
)


class TestGlyph(unittest.TestCase):
    """Tests for the Glyph dataclass."""

    def test_glyph_creation(self):
        """Test creating a glyph with all properties."""
        glyph = Glyph(
            symbol="AE1",
            name="AETHER_IGNITE",
            frequency=432,
            function="init_neural_sync",
            binding_code="[999]",
        )
        self.assertEqual(glyph.symbol, "AE1")
        self.assertEqual(glyph.name, "AETHER_IGNITE")
        self.assertEqual(glyph.frequency, 432)
        self.assertEqual(glyph.function, "init_neural_sync")
        self.assertEqual(glyph.binding_code, "[999]")

    def test_glyph_str(self):
        """Test glyph string representation."""
        glyph = Glyph(
            symbol="AE1",
            name="AETHER_IGNITE",
            frequency=432,
            function="init_neural_sync",
            binding_code="[999]",
        )
        result = str(glyph)
        self.assertIn("AE1", result)
        self.assertIn("AETHER_IGNITE", result)
        self.assertIn("432", result)


class TestGlyphTable(unittest.TestCase):
    """Tests for the GlyphTable class."""

    def setUp(self):
        """Create a temporary glyph table for testing."""
        self.temp_dir = tempfile.mkdtemp()
        self.csv_path = os.path.join(self.temp_dir, "test_glyph_table.csv")

        with open(self.csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Symbol", "Glyph_Name", "Frequency", "Function", "Binding_Code"])
            writer.writerow(["AE1", "AETHER_IGNITE", "432", "init_neural_sync", "[999]"])
            writer.writerow(["SY1", "SYNC_BEGIN", "369", "begin_handshake", "[700]"])
            writer.writerow(["FL1", "FLAME_KINDLE", "144", "kindle_start", "[800]"])

    def tearDown(self):
        """Clean up temporary files."""
        shutil.rmtree(self.temp_dir)

    def test_load_from_csv(self):
        """Test loading glyphs from CSV."""
        table = GlyphTable(self.csv_path)
        self.assertEqual(len(table.glyphs), 3)

    def test_get_by_symbol(self):
        """Test looking up glyph by symbol."""
        table = GlyphTable(self.csv_path)
        glyph = table.get_by_symbol("AE1")
        self.assertIsNotNone(glyph)
        self.assertEqual(glyph.name, "AETHER_IGNITE")

    def test_get_by_symbol_case_insensitive(self):
        """Test symbol lookup is case insensitive."""
        table = GlyphTable(self.csv_path)
        glyph = table.get_by_symbol("ae1")
        self.assertIsNotNone(glyph)
        self.assertEqual(glyph.symbol, "AE1")

    def test_get_by_symbol_not_found(self):
        """Test symbol lookup returns None for unknown symbol."""
        table = GlyphTable(self.csv_path)
        glyph = table.get_by_symbol("UNKNOWN")
        self.assertIsNone(glyph)

    def test_get_by_binding(self):
        """Test looking up glyph by binding code."""
        table = GlyphTable(self.csv_path)
        glyph = table.get_by_binding("[999]")
        self.assertIsNotNone(glyph)
        self.assertEqual(glyph.symbol, "AE1")

    def test_get_by_binding_without_brackets(self):
        """Test binding lookup accepts code without brackets."""
        table = GlyphTable(self.csv_path)
        glyph = table.get_by_binding("999")
        self.assertIsNotNone(glyph)
        self.assertEqual(glyph.symbol, "AE1")

    def test_search(self):
        """Test searching glyphs by name or function."""
        table = GlyphTable(self.csv_path)
        results = table.search("sync")
        self.assertEqual(len(results), 2)  # AE1 has "sync" in function, SY1 has "sync" in name

    def test_search_no_results(self):
        """Test search returns empty list for no matches."""
        table = GlyphTable(self.csv_path)
        results = table.search("nonexistent")
        self.assertEqual(len(results), 0)

    def test_list_all(self):
        """Test listing all glyphs."""
        table = GlyphTable(self.csv_path)
        glyphs = table.list_all()
        self.assertEqual(len(glyphs), 3)
        # Should be sorted by symbol
        self.assertEqual(glyphs[0].symbol, "AE1")
        self.assertEqual(glyphs[1].symbol, "FL1")
        self.assertEqual(glyphs[2].symbol, "SY1")

    def test_file_not_found(self):
        """Test FileNotFoundError for missing CSV."""
        with self.assertRaises(FileNotFoundError):
            GlyphTable("/nonexistent/path/glyph_table.csv")


class TestResonanceEngine(unittest.TestCase):
    """Tests for the ResonanceEngine class."""

    def setUp(self):
        """Set up a fresh engine for each test."""
        self.engine = ResonanceEngine()

    def test_initial_state(self):
        """Test initial engine state."""
        self.assertEqual(self.engine.resonance_level, 0.0)
        self.assertEqual(len(self.engine.sync_state), 0)
        self.assertEqual(len(self.engine.execution_log), 0)

    def test_execute_glyph(self):
        """Test executing a glyph updates state."""
        glyph = Glyph("AE1", "AETHER_IGNITE", 432, "init_neural_sync", "[999]")
        result = self.engine.execute_glyph(glyph)

        self.assertIn("AETHER_IGNITE", result)
        self.assertIn("432Hz", result)
        self.assertGreater(self.engine.resonance_level, 0)
        self.assertEqual(len(self.engine.execution_log), 1)

    def test_sync_glyph_sets_sync_state(self):
        """Test SY* glyphs set sync state."""
        glyph = Glyph("SY1", "SYNC_BEGIN", 369, "begin_handshake", "[700]")
        result = self.engine.execute_glyph(glyph)

        self.assertTrue(self.engine.sync_state.get("SY1", False))
        self.assertIn("Neural Sync complete", result)

    def test_resonance_level_capped_at_one(self):
        """Test resonance level doesn't exceed 1.0."""
        glyph = Glyph("AE1", "AETHER_IGNITE", 2000, "init_neural_sync", "[999]")

        # Execute multiple times
        for _ in range(10):
            self.engine.execute_glyph(glyph)

        self.assertLessEqual(self.engine.resonance_level, 1.0)

    def test_get_sync_status(self):
        """Test sync status reporting."""
        status = self.engine.get_sync_status()
        self.assertIn("Resonance", status)


class TestFlameLangInterpreter(unittest.TestCase):
    """Tests for the FlameLangInterpreter class."""

    def setUp(self):
        """Create interpreter with test glyph table."""
        self.temp_dir = tempfile.mkdtemp()
        self.csv_path = os.path.join(self.temp_dir, "test_glyph_table.csv")

        with open(self.csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Symbol", "Glyph_Name", "Frequency", "Function", "Binding_Code"])
            writer.writerow(["AE1", "AETHER_IGNITE", "432", "init_neural_sync", "[999]"])
            writer.writerow(["SY1", "SYNC_BEGIN", "369", "begin_handshake", "[700]"])
            writer.writerow(["FL1", "FLAME_KINDLE", "144", "kindle_start", "[800]"])
            writer.writerow(["ND1", "NODE_SPAWN", "264", "spawn_instance", "[500]"])
            writer.writerow(["SW1", "SWARM_RALLY", "480", "rally_agents", "[400]"])
            writer.writerow(["SC1", "SOVEREIGN_CLAIM", "777", "claim_authority", "[200]"])
            writer.writerow(["VW1", "VOW_DECLARE", "108", "declare_vow", "[100]"])
            writer.writerow(["QT1", "QUANTUM_ENTANGLE", "639", "entangle_pair", "[550]"])

        self.interpreter = FlameLangInterpreter(self.csv_path)

    def tearDown(self):
        """Clean up temporary files."""
        shutil.rmtree(self.temp_dir)

    def test_execute_by_symbol(self):
        """Test executing glyph by symbol."""
        result = self.interpreter.execute("AE1")
        self.assertIn("AETHER_IGNITE", result)
        self.assertIn("432Hz", result)

    def test_execute_by_binding_code(self):
        """Test executing glyph by binding code."""
        result = self.interpreter.execute("[999]")
        self.assertIn("AETHER_IGNITE", result)

    def test_execute_by_binding_code_numeric(self):
        """Test executing glyph by numeric binding code."""
        result = self.interpreter.execute("999")
        self.assertIn("AETHER_IGNITE", result)

    def test_execute_not_found(self):
        """Test error message for unknown glyph."""
        result = self.interpreter.execute("UNKNOWN")
        self.assertIn("not found", result)

    def test_execute_empty_command(self):
        """Test empty command returns empty string."""
        result = self.interpreter.execute("")
        self.assertEqual(result, "")

    def test_search(self):
        """Test search functionality."""
        result = self.interpreter.search("sync")
        self.assertIn("Found", result)

    def test_list_glyphs(self):
        """Test listing all glyphs."""
        result = self.interpreter.list_glyphs()
        self.assertIn("Glyph Table", result)
        self.assertIn("AE1", result)
        self.assertIn("SY1", result)

    def test_list_glyphs_with_prefix(self):
        """Test listing glyphs filtered by prefix."""
        result = self.interpreter.list_glyphs("FL")
        self.assertIn("FL1", result)
        self.assertNotIn("AE1", result)

    def test_show_help(self):
        """Test help message."""
        result = self.interpreter.show_help()
        self.assertIn("FlameLang", result)
        self.assertIn("COMMANDS", result)

    def test_run_batch(self):
        """Test batch execution."""
        results = self.interpreter.run_batch(["AE1", "SY1"])
        self.assertEqual(len(results), 2)
        self.assertIn("AETHER_IGNITE", results[0])
        self.assertIn("SYNC_BEGIN", results[1])

    def test_node_glyph_output(self):
        """Test node glyph shows node operation message."""
        result = self.interpreter.execute("ND1")
        self.assertIn("Node operation", result)

    def test_swarm_glyph_output(self):
        """Test swarm glyph shows swarm directive message."""
        result = self.interpreter.execute("SW1")
        self.assertIn("Swarm directive", result)

    def test_sovereign_glyph_output(self):
        """Test sovereign glyph shows sovereignty assertion message."""
        result = self.interpreter.execute("SC1")
        self.assertIn("Sovereignty assertion", result)

    def test_vow_glyph_output(self):
        """Test vow glyph shows vow binding message."""
        result = self.interpreter.execute("VW1")
        self.assertIn("Vow binding", result)

    def test_quantum_glyph_output(self):
        """Test quantum glyph shows quantum operation message."""
        result = self.interpreter.execute("QT1")
        self.assertIn("Quantum operation", result)


class TestIntegration(unittest.TestCase):
    """Integration tests using the real glyph_table.csv."""

    def test_load_real_glyph_table(self):
        """Test loading the real glyph table."""
        # Get path to real glyph table
        real_csv_path = Path(__file__).parent / "glyph_table.csv"
        if not real_csv_path.exists():
            self.skipTest("Real glyph_table.csv not found")

        table = GlyphTable(str(real_csv_path))
        self.assertGreater(len(table.glyphs), 50)  # Should have many glyphs

    def test_real_interpreter_execution(self):
        """Test interpreter with real glyph table."""
        real_csv_path = Path(__file__).parent / "glyph_table.csv"
        if not real_csv_path.exists():
            self.skipTest("Real glyph_table.csv not found")

        interpreter = FlameLangInterpreter(str(real_csv_path))

        # Test a few known glyphs
        result = interpreter.execute("AE1")
        self.assertIn("AETHER_IGNITE", result)

        result = interpreter.execute("[999]")
        self.assertIn("AETHER_IGNITE", result)


if __name__ == "__main__":
    unittest.main()
