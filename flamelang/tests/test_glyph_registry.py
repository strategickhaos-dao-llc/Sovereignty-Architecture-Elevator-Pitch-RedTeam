"""
Tests for Glyph Registry
"""

import unittest
from flamelang.core.glyph_registry import GlyphRegistry, GlyphCategory


class TestGlyphRegistry(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.registry = GlyphRegistry()
    
    def test_registry_initialization(self):
        """Test that registry initializes with glyphs"""
        self.assertGreater(self.registry.count(), 0)
        self.assertEqual(self.registry.count(), 17)
    
    def test_glyph_lookup_by_symbol(self):
        """Test looking up glyphs by symbol"""
        flame = self.registry.lookup("🔥")
        self.assertIsNotNone(flame)
        self.assertEqual(flame.name, "transform")
        self.assertEqual(flame.frequency, 741)
    
    def test_glyph_lookup_by_name(self):
        """Test looking up glyphs by name"""
        synthesis = self.registry.lookup("synthesis")
        self.assertIsNotNone(synthesis)
        self.assertEqual(synthesis.symbol, "⚡")
        self.assertEqual(synthesis.frequency, 963)
    
    def test_get_by_frequency(self):
        """Test getting glyphs by frequency"""
        glyphs_528 = self.registry.get_by_frequency(528)
        self.assertGreater(len(glyphs_528), 0)
        for glyph in glyphs_528:
            self.assertEqual(glyph.frequency, 528)
    
    def test_get_by_category(self):
        """Test getting glyphs by category"""
        high_energy = self.registry.get_by_category(GlyphCategory.HIGH_ENERGY)
        self.assertGreater(len(high_energy), 0)
        for glyph in high_energy:
            self.assertEqual(glyph.category, GlyphCategory.HIGH_ENERGY)
    
    def test_quantum_level_glyph(self):
        """Test the quantum level glyph (fine structure constant)"""
        alpha = self.registry.lookup("α")
        self.assertIsNotNone(alpha)
        self.assertEqual(alpha.frequency, 137)
        self.assertEqual(alpha.category, GlyphCategory.QUANTUM_LEVEL)
    
    def test_list_all_glyphs(self):
        """Test listing all glyphs"""
        all_glyphs = self.registry.list_all()
        self.assertEqual(len(all_glyphs), 17)
        
        # Check that all glyphs have required attributes
        for glyph in all_glyphs:
            self.assertIsNotNone(glyph.symbol)
            self.assertIsNotNone(glyph.name)
            self.assertIsNotNone(glyph.frequency)
            self.assertIsNotNone(glyph.function)
            self.assertIsNotNone(glyph.category)


if __name__ == '__main__':
    unittest.main()
