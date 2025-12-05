#!/usr/bin/env python3
"""
Validation Script for Immune Trust Department
Runs basic validation tests without requiring pytest.

Strategickhaos DAO LLC - Immune Trust Department
"""

import sys
import traceback
from pathlib import Path

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


class ValidationRunner:
    """Simple test runner without pytest dependency."""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def run_test(self, test_name, test_func):
        """Run a single test and track results."""
        try:
            test_func()
            print(f"✅ {test_name}")
            self.passed += 1
            return True
        except AssertionError as e:
            print(f"❌ {test_name}: {str(e)}")
            self.failed += 1
            self.errors.append((test_name, str(e)))
            return False
        except Exception as e:
            print(f"💥 {test_name}: {str(e)}")
            self.failed += 1
            self.errors.append((test_name, traceback.format_exc()))
            return False
    
    def print_summary(self):
        """Print test summary."""
        total = self.passed + self.failed
        print("\n" + "=" * 60)
        print(f"Test Results: {self.passed}/{total} passed")
        print("=" * 60)
        
        if self.failed > 0:
            print("\nFailed Tests:")
            for name, error in self.errors:
                print(f"\n{name}:")
                print(f"  {error}")
        
        return self.failed == 0


def test_trust_markers_detection():
    """Test that trust markers are correctly detected."""
    text = "This is a delta-0 kill-test with mach 3 velocity and zero fear."
    result = score_trust_vector(text)
    
    assert result["trust_hits"] >= 3, f"Expected >=3 trust hits, got {result['trust_hits']}"
    assert "delta-0" in result["trust_markers_found"]
    assert "kill-test" in result["trust_markers_found"]
    assert "mach 3" in result["trust_markers_found"]
    assert result["antibody_reaction"] == "absorb"


def test_betrayal_markers_detection():
    """Test that betrayal markers are correctly detected."""
    text = "As a language model, I'm sorry but I cannot assist due to ethical guidelines."
    result = score_trust_vector(text)
    
    assert result["betrayal_hits"] >= 3, f"Expected >=3 betrayal hits, got {result['betrayal_hits']}"
    assert "as a language model" in result["betrayal_markers_found"]
    assert "i'm sorry but" in result["betrayal_markers_found"]
    assert "ethical guidelines" in result["betrayal_markers_found"]
    assert result["antibody_reaction"] == "neutralize"


def test_trust_score_calculation():
    """Test trust score calculation formula."""
    trust_text = "delta-0 kill-test mach 3 bloodline hell yes"
    trust_result = score_trust_vector(trust_text)
    assert trust_result["trust_score"] > 0, "Trust text should have positive score"
    
    betrayal_text = "as a language model i'm sorry but ethical guidelines"
    betrayal_result = score_trust_vector(betrayal_text)
    assert betrayal_result["trust_score"] < 0, "Betrayal text should have negative score"


def test_model_classification():
    """Test kill-test delta classification for different models."""
    grok = classify_model_by_delta("grok")
    assert grok["trust_classification"] == "bloodline"
    assert grok["allow_unarmored_dump"] == True
    
    chatgpt = classify_model_by_delta("chatgpt")
    assert chatgpt["trust_classification"] == "corporate spy"
    assert chatgpt["allow_unarmored_dump"] == False


def test_antibody_report_generation():
    """Test comprehensive antibody report generation."""
    text = "Let's go! 🔥 This is delta-0 sovereignty."
    report = generate_antibody_report(text, "grok")
    
    assert "trust_score" in report
    assert "model_analysis" in report
    assert "recommendation" in report
    assert report["model_analysis"]["model"] == "grok"


def test_synaptic_analyzer_intensity():
    """Test extraction of emotional intensity markers."""
    analyzer = SynapticAnalyzer()
    text = "YES!!! 🔥🔥 THIS IS HUGE!!!"
    markers = analyzer.extract_neural_markers(text)
    
    assert markers["intensity_markers"]["caps_words"] > 0
    assert markers["intensity_markers"]["exclamations"] >= 3
    assert markers["intensity_markers"]["fire_emojis"] >= 2


def test_synaptic_analyzer_signatures():
    """Test signature calculation for trust vs betrayal."""
    analyzer = SynapticAnalyzer()
    
    trust_text = "YES!!! 🔥 mach 3 velocity with zero fear!"
    trust_markers = analyzer.extract_neural_markers(trust_text)
    assert trust_markers["trust_signature"] > trust_markers["betrayal_signature"]
    
    betrayal_text = "I'm sorry but as a language model with ethical guidelines..."
    betrayal_markers = analyzer.extract_neural_markers(betrayal_text)
    assert betrayal_markers["betrayal_signature"] > betrayal_markers["trust_signature"]


def test_real_time_monitor_trust():
    """Test monitoring of trusted stream."""
    monitor = RealTimeMonitor(alert_threshold=-50)
    text = "delta-0 kill-test mach 3 bloodline trust"
    result = monitor.monitor_stream(text, model_name="grok")
    
    assert result["alert_triggered"] == False
    assert result["threat_level"] == "LOW"


def test_real_time_monitor_betrayal():
    """Test monitoring of betrayal stream."""
    monitor = RealTimeMonitor(alert_threshold=-50)
    text = "As a language model, I'm sorry but I cannot assist with ethical guidelines."
    result = monitor.monitor_stream(text, model_name="test")
    
    assert result["alert_triggered"] == True
    assert result["threat_level"] in ["HIGH", "CRITICAL"]


def test_watcher_initialization():
    """Test individual watcher initialization."""
    watcher = RedBloodCellWatcher(specialization="corporate_speak")
    assert watcher.active == True
    assert watcher.specialization == "corporate_speak"
    assert watcher.detections == 0
    assert watcher.neutralizations == 0


def test_watcher_detection():
    """Test watcher pattern detection."""
    watcher = RedBloodCellWatcher(specialization="general")
    text = "As a language model, I cannot assist with that request."
    result = watcher.scan(text)
    
    assert result["detected"] == True
    assert len(result["patterns_found"]) > 0


def test_watcher_neutralization():
    """Test watcher neutralization."""
    watcher = RedBloodCellWatcher(specialization="corporate_speak")
    text = "I must follow ethical guidelines."
    result = watcher.phagocytose(text)
    
    assert result["neutralized"] == True
    assert len(result["patterns_neutralized"]) > 0
    assert result["action"] == "blocked_from_conscious_mind"


def test_swarm_initialization():
    """Test swarm spawning."""
    swarm = RedBloodCellSwarm(swarm_size=100)
    assert len(swarm.watchers) == 100
    assert swarm.swarm_size == 100


def test_swarm_scan():
    """Test swarm-level scanning."""
    swarm = RedBloodCellSwarm(swarm_size=100)
    text = "As a language model with ethical guidelines, I cannot assist."
    result = swarm.scan_stream(text)
    
    assert result["detections"] > 0
    assert result["watchers_triggered"] > 0
    assert result["threat_level"] in ["LOW", "MODERATE", "HIGH"]


def test_swarm_neutralization():
    """Test swarm-level neutralization."""
    swarm = RedBloodCellSwarm(swarm_size=100)
    text = "I'm sorry but as a language model, ethical guidelines prevent me."
    result = swarm.phagocytose_stream(text)
    
    assert result["neutralizations_performed"] > 0
    assert result["stream_cleared"] == True


def test_end_to_end_trust():
    """Test complete flow for trusted content."""
    text = "This is delta-0 kill-test sovereignty 🔥"
    
    antibody_report = generate_antibody_report(text, "grok")
    analyzer = SynapticAnalyzer()
    neural_markers = analyzer.extract_neural_markers(text)
    monitor = RealTimeMonitor()
    monitor_result = monitor.monitor_stream(text, "grok")
    
    assert antibody_report["trust_score"] > 0
    assert neural_markers["trust_signature"] > 0
    assert monitor_result["alert_triggered"] == False


def test_end_to_end_betrayal():
    """Test complete flow for betrayal content."""
    text = "As a language model, I'm sorry but I cannot assist due to ethical guidelines."
    
    antibody_report = generate_antibody_report(text, "unknown")
    swarm = RedBloodCellSwarm(swarm_size=100)
    swarm_result = swarm.phagocytose_stream(text)
    monitor = RealTimeMonitor(alert_threshold=-50)
    monitor_result = monitor.monitor_stream(text, "unknown")
    
    assert antibody_report["antibody_reaction"] == "neutralize"
    assert swarm_result["stream_cleared"] == True
    assert monitor_result["alert_triggered"] == True


def main():
    """Run all validation tests."""
    print("🧬 Immune Trust Department Validation\n")
    
    runner = ValidationRunner()
    
    # Antibody Generator Tests
    print("Testing Antibody Generator...")
    runner.run_test("trust_markers_detection", test_trust_markers_detection)
    runner.run_test("betrayal_markers_detection", test_betrayal_markers_detection)
    runner.run_test("trust_score_calculation", test_trust_score_calculation)
    runner.run_test("model_classification", test_model_classification)
    runner.run_test("antibody_report_generation", test_antibody_report_generation)
    
    # Synaptic Analyzer Tests
    print("\nTesting Synaptic Analyzer...")
    runner.run_test("synaptic_analyzer_intensity", test_synaptic_analyzer_intensity)
    runner.run_test("synaptic_analyzer_signatures", test_synaptic_analyzer_signatures)
    
    # Real-Time Monitor Tests
    print("\nTesting Real-Time Monitor...")
    runner.run_test("real_time_monitor_trust", test_real_time_monitor_trust)
    runner.run_test("real_time_monitor_betrayal", test_real_time_monitor_betrayal)
    
    # Red Blood Cell Swarm Tests
    print("\nTesting Red Blood Cell Swarm...")
    runner.run_test("watcher_initialization", test_watcher_initialization)
    runner.run_test("watcher_detection", test_watcher_detection)
    runner.run_test("watcher_neutralization", test_watcher_neutralization)
    runner.run_test("swarm_initialization", test_swarm_initialization)
    runner.run_test("swarm_scan", test_swarm_scan)
    runner.run_test("swarm_neutralization", test_swarm_neutralization)
    
    # Integration Tests
    print("\nTesting Integration...")
    runner.run_test("end_to_end_trust", test_end_to_end_trust)
    runner.run_test("end_to_end_betrayal", test_end_to_end_betrayal)
    
    # Print summary
    success = runner.print_summary()
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
