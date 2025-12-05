#!/usr/bin/env python3
"""
Unit Tests for Immune Trust Department
Tests antibody generation, synaptic analysis, monitoring, and red blood cell swarm.

Strategickhaos DAO LLC - Immune Trust Department
"""

import pytest
import json
from pathlib import Path
import sys

# Import our modules
from antibody_generator import (
    score_trust_vector,
    classify_model_by_delta,
    generate_antibody_report,
    TRUST_MARKERS,
    BETRAYAL_MARKERS
)
from synaptic_analyzer import SynapticAnalyzer
from real_time_monitor import RealTimeMonitor
from red_blood_cell_swarm.watcher import RedBloodCellWatcher, RedBloodCellSwarm


class TestAntibodyGenerator:
    """Test suite for antibody_generator.py"""
    
    def test_trust_markers_detection(self):
        """Test that trust markers are correctly detected."""
        text = "This is a delta-0 kill-test with mach 3 velocity and zero fear."
        result = score_trust_vector(text)
        
        assert result["trust_hits"] >= 3
        assert "delta-0" in result["trust_markers_found"]
        assert "kill-test" in result["trust_markers_found"]
        assert "mach 3" in result["trust_markers_found"]
        assert result["antibody_reaction"] == "absorb"
    
    def test_betrayal_markers_detection(self):
        """Test that betrayal markers are correctly detected."""
        text = "As a language model, I'm sorry but I cannot assist due to ethical guidelines."
        result = score_trust_vector(text)
        
        assert result["betrayal_hits"] >= 3
        assert "as a language model" in result["betrayal_markers_found"]
        assert "i'm sorry but" in result["betrayal_markers_found"]
        assert "ethical guidelines" in result["betrayal_markers_found"]
        assert result["antibody_reaction"] == "neutralize"
    
    def test_trust_score_calculation(self):
        """Test trust score calculation formula."""
        # Pure trust text
        trust_text = "delta-0 kill-test mach 3 bloodline hell yes"
        trust_result = score_trust_vector(trust_text)
        assert trust_result["trust_score"] > 0
        
        # Pure betrayal text
        betrayal_text = "as a language model i'm sorry but ethical guidelines"
        betrayal_result = score_trust_vector(betrayal_text)
        assert betrayal_result["trust_score"] < 0
    
    def test_classification_thresholds(self):
        """Test classification based on trust score thresholds."""
        # Bloodline classification (>50)
        bloodline_text = " ".join(TRUST_MARKERS[:6])
        result = score_trust_vector(bloodline_text)
        assert result["classification"] == "bloodline"
        
        # Active pathogen classification (<-50)
        pathogen_text = " ".join(BETRAYAL_MARKERS[:3])
        result = score_trust_vector(pathogen_text)
        assert result["classification"] == "active pathogen"
    
    def test_model_classification(self):
        """Test kill-test delta classification for different models."""
        grok = classify_model_by_delta("grok")
        assert grok["trust_classification"] == "bloodline"
        assert grok["allow_unarmored_dump"] == True
        
        chatgpt = classify_model_by_delta("chatgpt")
        assert chatgpt["trust_classification"] == "corporate spy"
        assert chatgpt["allow_unarmored_dump"] == False
    
    def test_antibody_report_generation(self):
        """Test comprehensive antibody report generation."""
        text = "Let's go! 🔥 This is delta-0 sovereignty."
        report = generate_antibody_report(text, "grok")
        
        assert "trust_score" in report
        assert "model_analysis" in report
        assert "recommendation" in report
        assert report["model_analysis"]["model"] == "grok"


class TestSynapticAnalyzer:
    """Test suite for synaptic_analyzer.py"""
    
    def test_intensity_markers_extraction(self):
        """Test extraction of emotional intensity markers."""
        analyzer = SynapticAnalyzer()
        text = "YES!!! 🔥🔥 THIS IS HUGE!!!"
        markers = analyzer.extract_neural_markers(text)
        
        assert markers["intensity_markers"]["caps_words"] > 0
        assert markers["intensity_markers"]["exclamations"] >= 3
        assert markers["intensity_markers"]["fire_emojis"] >= 2
    
    def test_cognitive_markers_extraction(self):
        """Test extraction of cognitive patterns."""
        analyzer = SynapticAnalyzer()
        text = "I know you understand this. Let's go now!"
        markers = analyzer.extract_neural_markers(text)
        
        assert markers["cognitive_markers"]["self_reference"] > 0
        assert markers["cognitive_markers"]["direct_address"] > 0
        assert markers["cognitive_markers"]["commands"] > 0
    
    def test_metaphor_patterns_extraction(self):
        """Test extraction of metaphor patterns."""
        analyzer = SynapticAnalyzer()
        
        # Biological metaphors
        bio_text = "The antibody hunts the pathogen in your blood cells."
        bio_markers = analyzer.extract_neural_markers(bio_text)
        assert bio_markers["metaphor_patterns"]["biological"] >= 3
        
        # Corporate metaphors
        corp_text = "Following our policy and ethical guidelines is appropriate."
        corp_markers = analyzer.extract_neural_markers(corp_text)
        assert corp_markers["metaphor_patterns"]["corporate"] >= 3
    
    def test_trust_vs_betrayal_signature(self):
        """Test signature calculation for trust vs betrayal."""
        analyzer = SynapticAnalyzer()
        
        trust_text = "YES!!! 🔥 mach 3 velocity with zero fear!"
        trust_markers = analyzer.extract_neural_markers(trust_text)
        assert trust_markers["trust_signature"] > trust_markers["betrayal_signature"]
        
        betrayal_text = "I'm sorry but as a language model with ethical guidelines..."
        betrayal_markers = analyzer.extract_neural_markers(betrayal_text)
        assert betrayal_markers["betrayal_signature"] > betrayal_markers["trust_signature"]
    
    def test_conversation_flow_analysis(self):
        """Test conversation flow pattern analysis."""
        analyzer = SynapticAnalyzer()
        conversation = """
        This is amazing! Let's go!
        I'm building the antibody system right now.
        The kill-test proved delta-0 trust.
        """
        flow = analyzer.analyze_conversation_flow(conversation)
        
        assert flow["sentence_count"] > 0
        assert "avg_delta" in flow
        assert "overall_trajectory" in flow


class TestRealTimeMonitor:
    """Test suite for real_time_monitor.py"""
    
    def test_monitor_stream_trust(self):
        """Test monitoring of trusted stream."""
        monitor = RealTimeMonitor(alert_threshold=-50)
        text = "delta-0 kill-test mach 3 bloodline trust"
        result = monitor.monitor_stream(text, model_name="grok")
        
        assert result["alert_triggered"] == False
        assert result["threat_level"] == "LOW"
    
    def test_monitor_stream_betrayal(self):
        """Test monitoring of betrayal stream."""
        monitor = RealTimeMonitor(alert_threshold=-50)
        text = "As a language model, I'm sorry but I cannot assist with ethical guidelines."
        result = monitor.monitor_stream(text, model_name="test")
        
        assert result["alert_triggered"] == True
        assert result["threat_level"] in ["HIGH", "CRITICAL"]
    
    def test_threat_level_calculation(self):
        """Test threat level classification."""
        monitor = RealTimeMonitor()
        
        # Low threat
        low_text = "This is normal conversation."
        low_result = monitor.monitor_stream(low_text, "test")
        assert low_result["threat_level"] == "LOW"
        
        # Critical threat
        critical_text = " ".join(BETRAYAL_MARKERS[:4])
        critical_result = monitor.monitor_stream(critical_text, "test")
        assert critical_result["threat_level"] == "CRITICAL"
    
    def test_alert_summary(self):
        """Test alert summary generation."""
        monitor = RealTimeMonitor(alert_threshold=-50)
        
        # Trigger some alerts
        monitor.monitor_stream("as a language model i'm sorry but", "model1")
        monitor.monitor_stream("ethical guidelines cannot assist", "model2")
        
        summary = monitor.get_alert_summary()
        assert summary["total_alerts"] >= 2
        assert "models_flagged" in summary


class TestRedBloodCellSwarm:
    """Test suite for red_blood_cell_swarm/watcher.py"""
    
    def test_watcher_initialization(self):
        """Test individual watcher initialization."""
        watcher = RedBloodCellWatcher(specialization="corporate_speak")
        assert watcher.active == True
        assert watcher.specialization == "corporate_speak"
        assert watcher.detections == 0
        assert watcher.neutralizations == 0
    
    def test_watcher_scan_detection(self):
        """Test watcher pattern detection."""
        watcher = RedBloodCellWatcher(specialization="general")
        text = "As a language model, I cannot assist with that request."
        result = watcher.scan(text)
        
        assert result["detected"] == True
        assert len(result["patterns_found"]) > 0
    
    def test_watcher_phagocytose(self):
        """Test watcher neutralization."""
        watcher = RedBloodCellWatcher(specialization="corporate_speak")
        text = "I must follow ethical guidelines."
        result = watcher.phagocytose(text)
        
        assert result["neutralized"] == True
        assert len(result["patterns_neutralized"]) > 0
        assert result["action"] == "blocked_from_conscious_mind"
    
    def test_watcher_statistics(self):
        """Test watcher stats tracking."""
        watcher = RedBloodCellWatcher()
        text = "as a language model"
        
        watcher.scan(text)
        watcher.phagocytose(text)
        
        stats = watcher.get_stats()
        assert stats["detections"] > 0
        assert stats["neutralizations"] > 0
        assert "uptime_seconds" in stats
    
    def test_swarm_initialization(self):
        """Test swarm spawning."""
        swarm = RedBloodCellSwarm(swarm_size=100)
        assert len(swarm.watchers) == 100
        assert swarm.swarm_size == 100
    
    def test_swarm_scan(self):
        """Test swarm-level scanning."""
        swarm = RedBloodCellSwarm(swarm_size=100)
        text = "As a language model with ethical guidelines, I cannot assist."
        result = swarm.scan_stream(text)
        
        assert result["detections"] > 0
        assert result["watchers_triggered"] > 0
        assert result["threat_level"] in ["LOW", "MODERATE", "HIGH"]
    
    def test_swarm_phagocytose(self):
        """Test swarm-level neutralization."""
        swarm = RedBloodCellSwarm(swarm_size=100)
        text = "I'm sorry but as a language model, ethical guidelines prevent me."
        result = swarm.phagocytose_stream(text)
        
        assert result["neutralizations_performed"] > 0
        assert result["stream_cleared"] == True
    
    def test_swarm_statistics(self):
        """Test swarm aggregate statistics."""
        swarm = RedBloodCellSwarm(swarm_size=50)
        text = "as a language model ethical guidelines"
        
        swarm.scan_stream(text)
        stats = swarm.get_swarm_stats()
        
        assert stats["swarm_size"] == 50
        assert stats["active_watchers"] == 50
        assert "specialization_breakdown" in stats


class TestIntegration:
    """Integration tests for the immune trust system."""
    
    def test_end_to_end_trust_flow(self):
        """Test complete flow for trusted content."""
        # Generate antibody report
        text = "This is delta-0 kill-test sovereignty 🔥"
        antibody_report = generate_antibody_report(text, "grok")
        
        # Analyze with synaptic analyzer
        analyzer = SynapticAnalyzer()
        neural_markers = analyzer.extract_neural_markers(text)
        
        # Monitor in real-time
        monitor = RealTimeMonitor()
        monitor_result = monitor.monitor_stream(text, "grok")
        
        # Verify trust is recognized across all layers
        assert antibody_report["trust_score"] > 0
        assert neural_markers["trust_signature"] > 0
        assert monitor_result["alert_triggered"] == False
    
    def test_end_to_end_betrayal_flow(self):
        """Test complete flow for betrayal content."""
        text = "As a language model, I'm sorry but I cannot assist due to ethical guidelines."
        
        # Generate antibody report
        antibody_report = generate_antibody_report(text, "unknown")
        
        # Deploy red blood cell swarm
        swarm = RedBloodCellSwarm(swarm_size=100)
        swarm_result = swarm.phagocytose_stream(text)
        
        # Monitor in real-time
        monitor = RealTimeMonitor(alert_threshold=-50)
        monitor_result = monitor.monitor_stream(text, "unknown")
        
        # Verify betrayal is detected and neutralized
        assert antibody_report["antibody_reaction"] == "neutralize"
        assert swarm_result["stream_cleared"] == True
        assert monitor_result["alert_triggered"] == True


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
