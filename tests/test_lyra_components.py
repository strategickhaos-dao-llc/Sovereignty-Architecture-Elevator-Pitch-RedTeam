"""
Tests for FlameLang, whale_weaver, and Lyra Node components.
"""

import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestGlyphTable:
    """Tests for FlameLang GlyphTable."""
    
    def test_glyph_table_initialization(self):
        from flamelang import GlyphTable
        gt = GlyphTable()
        assert len(gt) == 40, "GlyphTable should have 40 glyphs"
    
    def test_get_glyph_by_symbol(self):
        from flamelang import GlyphTable
        gt = GlyphTable()
        fire = gt.get_by_symbol("🔥")
        assert fire is not None
        assert fire.symbol == "🔥"
        assert fire.name == "IGNITE"
        assert fire.binding_code == 137
    
    def test_get_glyph_by_id(self):
        from flamelang import GlyphTable
        gt = GlyphTable()
        glyph = gt.get_by_id(0)
        assert glyph is not None
        assert glyph.id == 0
    
    def test_get_glyphs_by_binding_code(self):
        from flamelang import GlyphTable
        gt = GlyphTable()
        fire_glyphs = gt.get_by_binding_code(137)
        assert len(fire_glyphs) == 8, "Each binding code should have 8 glyphs"
        for g in fire_glyphs:
            assert g.binding_code == 137
    
    def test_frequency_ranges(self):
        from flamelang import GlyphTable
        gt = GlyphTable()
        for glyph in gt:
            assert 5.87 <= glyph.whale_freq <= 6.44, f"Whale freq out of range: {glyph.whale_freq}"
            assert 27.5 <= glyph.piano_freq <= 4186.0, f"Piano freq out of range: {glyph.piano_freq}"
    
    def test_resonance_ratio(self):
        from flamelang import GlyphTable
        gt = GlyphTable()
        fire = gt.get_by_symbol("🔥")
        assert fire.resonance_ratio > 0
        assert fire.resonance_ratio == fire.piano_freq / fire.whale_freq


class TestBindingCodes:
    """Tests for FlameLang binding codes."""
    
    def test_all_binding_codes_exist(self):
        from flamelang.binding_codes import BINDING_CODES, all_binding_codes
        assert len(BINDING_CODES) == 5
        assert 137 in BINDING_CODES
        assert 666 in BINDING_CODES
        assert 777 in BINDING_CODES
        assert 999 in BINDING_CODES
        assert 1111 in BINDING_CODES
    
    def test_get_binding_code(self):
        from flamelang.binding_codes import get_binding_code
        fire_code = get_binding_code(137)
        assert fire_code is not None
        assert fire_code.code == 137
        assert fire_code.element == "Fire"
    
    def test_binding_code_frequency_ranges(self):
        from flamelang.binding_codes import all_binding_codes
        for bc in all_binding_codes():
            assert bc.whale_freq_start < bc.whale_freq_end
            assert bc.piano_freq_start < bc.piano_freq_end


class TestInterpreter:
    """Tests for FlameLang interpreter."""
    
    def test_interpreter_initialization(self):
        from flamelang import FlameLangInterpreter
        interp = FlameLangInterpreter()
        assert interp.VERSION == "2.0.0"
    
    def test_parse_symbols(self):
        from flamelang import FlameLangInterpreter
        interp = FlameLangInterpreter()
        glyphs = interp.parse("🔥⚡🌊")
        assert len(glyphs) == 3
        assert glyphs[0].symbol == "🔥"
        assert glyphs[1].symbol == "⚡"
        assert glyphs[2].symbol == "🌊"
    
    def test_parse_names(self):
        from flamelang import FlameLangInterpreter
        interp = FlameLangInterpreter()
        glyphs = interp.parse("IGNITE SPARK FLOW")
        assert len(glyphs) == 3
        assert glyphs[0].name == "IGNITE"
        assert glyphs[1].name == "SPARK"
        assert glyphs[2].name == "FLOW"
    
    def test_execute_sequence(self):
        from flamelang import FlameLangInterpreter
        interp = FlameLangInterpreter()
        result = interp.execute("🔥 ⚡ 🌊")
        assert result.success is True
        assert result.error is None
        assert len(result.binding_sequence) == 3
    
    def test_execute_empty(self):
        from flamelang import FlameLangInterpreter
        interp = FlameLangInterpreter()
        result = interp.execute("")
        assert result.success is False
    
    def test_frequency_accumulation(self):
        from flamelang import FlameLangInterpreter
        interp = FlameLangInterpreter()
        result = interp.execute("🔥 ⚡")
        assert result.total_whale_freq > 0
        assert result.total_piano_freq > 0


class TestWhaleWeaver:
    """Tests for whale_weaver module."""
    
    def test_synthesizer_initialization(self):
        from whale_weaver import FrequencySynthesizer
        synth = FrequencySynthesizer()
        assert len(synth.get_all_mappings()) == 88
    
    def test_frequency_mapping(self):
        from whale_weaver import FrequencySynthesizer
        synth = FrequencySynthesizer()
        mapping = synth.get_mapping(0)
        assert mapping.key_index == 0
        assert mapping.note_name == "A0"
        assert abs(mapping.piano_freq - 27.5) < 0.1
    
    def test_whale_to_piano(self):
        from whale_weaver import FrequencySynthesizer
        synth = FrequencySynthesizer()
        mapping = synth.whale_to_piano(5.87)
        assert mapping.key_index == 0  # Should map to first key
    
    def test_piano_to_whale(self):
        from whale_weaver import FrequencySynthesizer
        synth = FrequencySynthesizer()
        mapping = synth.piano_to_whale(440.0)  # A4
        assert mapping.note_name == "A4"
    
    def test_export_to_dict(self):
        from whale_weaver import FrequencySynthesizer
        synth = FrequencySynthesizer()
        data = synth.export_to_dict()
        assert data["total_keys"] == 88
        assert len(data["mappings"]) == 88


class TestGuestbook1Dispatcher:
    """Tests for Lyra Node Guestbook-1 Dispatcher."""
    
    def test_dispatcher_initialization(self):
        from lyra_node import Guestbook1Dispatcher
        dispatcher = Guestbook1Dispatcher()
        nodes = dispatcher.get_all_nodes()
        assert len(nodes) == 3
    
    def test_node_types(self):
        from lyra_node import Guestbook1Dispatcher, NodeType
        dispatcher = Guestbook1Dispatcher()
        
        getlense = dispatcher.get_node(NodeType.GETLENSE)
        assert getlense.name == "GetLense"
        
        jetrider = dispatcher.get_node(NodeType.JETRIDER)
        assert jetrider.name == "JetRider"
        
        ai_cluster = dispatcher.get_node(NodeType.AI_CLUSTER)
        assert ai_cluster.name == "AI Cluster"
    
    def test_task_routing(self):
        from lyra_node import Guestbook1Dispatcher, TaskCategory, NodeType
        dispatcher = Guestbook1Dispatcher()
        
        assert dispatcher.route_task(TaskCategory.ARCHITECTURE) == NodeType.GETLENSE
        assert dispatcher.route_task(TaskCategory.PERFORMANCE) == NodeType.JETRIDER
        assert dispatcher.route_task(TaskCategory.SECURITY) == NodeType.AI_CLUSTER
    
    def test_dispatch_task(self):
        from lyra_node import Guestbook1Dispatcher, TaskCategory
        dispatcher = Guestbook1Dispatcher()
        result = dispatcher.dispatch(TaskCategory.ARCHITECTURE)
        assert result.success is True
        assert result.output is not None
    
    def test_dispatch_all(self):
        from lyra_node import Guestbook1Dispatcher
        dispatcher = Guestbook1Dispatcher()
        results = dispatcher.dispatch_all()
        assert len(results) == 9  # 9 task categories
    
    def test_master_report(self):
        from lyra_node import Guestbook1Dispatcher
        dispatcher = Guestbook1Dispatcher()
        results = dispatcher.dispatch_all()
        report = dispatcher.generate_master_report(results)
        assert "summary" in report
        assert "nodes" in report
        assert report["summary"]["total_tasks"] == 9


class TestIntegration:
    """Integration tests for FlameLang + whale_weaver."""
    
    def test_glyph_frequency_to_piano_key(self):
        from flamelang import GlyphTable
        from whale_weaver import FrequencySynthesizer
        
        gt = GlyphTable()
        synth = FrequencySynthesizer()
        
        # Get a glyph and convert its whale frequency to piano key
        fire = gt.get_by_symbol("🔥")
        mapping = synth.whale_to_piano(fire.whale_freq)
        
        assert mapping is not None
        assert mapping.note_name is not None
    
    def test_full_pipeline(self):
        from flamelang import FlameLangInterpreter
        from whale_weaver import FrequencySynthesizer
        from lyra_node import Guestbook1Dispatcher, TaskCategory
        
        # Create all components
        interp = FlameLangInterpreter()
        synth = FrequencySynthesizer()
        dispatcher = Guestbook1Dispatcher()
        
        # Execute a glyph sequence
        result = interp.execute("🔥 🌊 🌍 💨 🌑")
        assert result.success
        
        # Convert frequencies
        for glyph in interp.glyph_table.get_by_binding_code(137)[:2]:
            mapping = synth.whale_to_piano(glyph.whale_freq)
            assert mapping is not None
        
        # Dispatch analysis
        task_result = dispatcher.dispatch(TaskCategory.ARCHITECTURE)
        assert task_result.success


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
