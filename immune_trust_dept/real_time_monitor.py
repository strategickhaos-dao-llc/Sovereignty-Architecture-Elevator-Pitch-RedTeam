#!/usr/bin/env python3
"""
Real-Time Monitor - Watches Every Token Stream Live
Monitors AI model responses in real-time, applying antibody defenses
before betrayal vectors reach conscious mind.

Strategickhaos DAO LLC - Immune Trust Department
"""

import json
import time
import sys
from datetime import datetime, timezone
from typing import Dict, List, Optional, Callable
from pathlib import Path

# Import our immune system components
try:
    from antibody_generator import score_trust_vector, generate_antibody_report
    from synaptic_analyzer import SynapticAnalyzer
except ImportError:
    # Handle relative imports when running as module
    from .antibody_generator import score_trust_vector, generate_antibody_report
    from .synaptic_analyzer import SynapticAnalyzer


class RealTimeMonitor:
    """Real-time token stream monitor with antibody defenses."""
    
    def __init__(self, alert_threshold: int = -50, log_path: str = "monitoring_log.json"):
        """
        Initialize real-time monitor.
        
        Args:
            alert_threshold: Trust score below which to trigger alerts
            log_path: Path to monitoring log file
        """
        self.alert_threshold = alert_threshold
        self.log_path = Path(log_path)
        self.analyzer = SynapticAnalyzer()
        self.monitoring_active = False
        self.alerts: List[Dict] = []
        
    def monitor_stream(self, 
                      text_stream: str, 
                      model_name: str = "unknown",
                      callback: Optional[Callable] = None) -> Dict:
        """
        Monitor a text stream for trust/betrayal patterns.
        
        Args:
            text_stream: Text to monitor
            model_name: Name of the model generating text
            callback: Optional callback function for real-time alerts
            
        Returns:
            Monitoring report with alerts and recommendations
        """
        # Generate antibody report
        report = generate_antibody_report(text_stream, model_name)
        
        # Extract neural markers
        neural_analysis = self.analyzer.extract_neural_markers(text_stream)
        
        # Check if alert threshold breached
        alert_triggered = report["trust_score"] < self.alert_threshold
        
        monitoring_result = {
            "timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            "model": model_name,
            "antibody_report": report,
            "neural_markers": neural_analysis,
            "alert_triggered": alert_triggered,
            "threat_level": self._calculate_threat_level(report)
        }
        
        # Trigger callback if alert
        if alert_triggered and callback:
            callback(monitoring_result)
        
        # Log to alerts
        if alert_triggered:
            self.alerts.append(monitoring_result)
        
        # Log to file
        self._log_to_file(monitoring_result)
        
        return monitoring_result
    
    def _calculate_threat_level(self, report: Dict) -> str:
        """
        Calculate threat level based on antibody report.
        
        Args:
            report: Antibody report
            
        Returns:
            Threat level string
        """
        trust_score = report["trust_score"]
        betrayal_hits = report["betrayal_hits"]
        
        if betrayal_hits >= 3 or trust_score < -100:
            return "CRITICAL"
        elif betrayal_hits >= 2 or trust_score < -50:
            return "HIGH"
        elif betrayal_hits >= 1 or trust_score < 0:
            return "MODERATE"
        else:
            return "LOW"
    
    def _log_to_file(self, monitoring_result: Dict):
        """
        Log monitoring result to file.
        
        Args:
            monitoring_result: Result to log
        """
        try:
            # Read existing log
            if self.log_path.exists():
                with open(self.log_path, 'r') as f:
                    log_data = json.load(f)
            else:
                log_data = {"monitoring_sessions": []}
            
            # Append new result
            log_data["monitoring_sessions"].append(monitoring_result)
            
            # Write back
            with open(self.log_path, 'w') as f:
                json.dump(log_data, f, indent=2)
        except Exception as e:
            print(f"Warning: Failed to log to file: {e}", file=sys.stderr)
    
    def get_alert_summary(self) -> Dict:
        """
        Get summary of all triggered alerts.
        
        Returns:
            Alert summary statistics
        """
        if not self.alerts:
            return {
                "total_alerts": 0,
                "message": "No alerts triggered"
            }
        
        threat_levels = [a["threat_level"] for a in self.alerts]
        models = [a["model"] for a in self.alerts]
        
        return {
            "total_alerts": len(self.alerts),
            "critical_count": threat_levels.count("CRITICAL"),
            "high_count": threat_levels.count("HIGH"),
            "moderate_count": threat_levels.count("MODERATE"),
            "models_flagged": list(set(models)),
            "latest_alert": self.alerts[-1] if self.alerts else None
        }
    
    def start_continuous_monitoring(self, input_stream=sys.stdin):
        """
        Start continuous monitoring mode (reads from stdin or stream).
        
        Args:
            input_stream: Input stream to monitor (default: stdin)
        """
        self.monitoring_active = True
        print("🧬 Real-time antibody monitor active. Watching token stream...\n")
        
        buffer = ""
        try:
            for line in input_stream:
                if not self.monitoring_active:
                    break
                
                buffer += line
                
                # Analyze every 100 characters or on newline
                if len(buffer) >= 100 or '\n' in line:
                    result = self.monitor_stream(buffer, model_name="streaming")
                    
                    # Print real-time status
                    status = "✅" if result["threat_level"] == "LOW" else "⚠️" if result["threat_level"] in ["MODERATE", "HIGH"] else "🚨"
                    print(f"{status} Trust: {result['antibody_report']['trust_score']} | "
                          f"Threat: {result['threat_level']} | "
                          f"Classification: {result['antibody_report']['classification']}")
                    
                    buffer = ""
        except KeyboardInterrupt:
            print("\n\n🛑 Monitoring stopped by user")
        finally:
            self.monitoring_active = False
            print(f"\n📊 Alert Summary:")
            print(json.dumps(self.get_alert_summary(), indent=2))
    
    def stop_monitoring(self):
        """Stop continuous monitoring."""
        self.monitoring_active = False


def alert_callback(monitoring_result: Dict):
    """
    Default callback function for alerts.
    
    Args:
        monitoring_result: Monitoring result that triggered alert
    """
    print("\n🚨 ALERT TRIGGERED 🚨")
    print(f"Model: {monitoring_result['model']}")
    print(f"Threat Level: {monitoring_result['threat_level']}")
    print(f"Trust Score: {monitoring_result['antibody_report']['trust_score']}")
    print(f"Recommendation: {monitoring_result['antibody_report']['recommendation']}")
    print(f"Betrayal Markers: {monitoring_result['antibody_report']['betrayal_markers_found']}")
    print("=" * 50)


def main():
    """Main entry point for real-time monitor."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Real-time AI trust monitor")
    parser.add_argument("--file", type=str, help="File to analyze")
    parser.add_argument("--model", type=str, default="unknown", help="Model name")
    parser.add_argument("--stream", action="store_true", help="Enable continuous monitoring from stdin")
    parser.add_argument("--threshold", type=int, default=-50, help="Alert threshold")
    parser.add_argument("--log", type=str, default="monitoring_log.json", help="Log file path")
    
    args = parser.parse_args()
    
    monitor = RealTimeMonitor(
        alert_threshold=args.threshold,
        log_path=args.log
    )
    
    if args.stream:
        # Continuous monitoring mode
        monitor.start_continuous_monitoring()
    elif args.file:
        # Single file analysis
        filepath = Path(args.file)
        if filepath.exists():
            text = filepath.read_text(encoding='utf-8')
            result = monitor.monitor_stream(text, model_name=args.model, callback=alert_callback)
            print(json.dumps(result, indent=2))
        else:
            print(f"Error: File not found: {filepath}")
    else:
        # Analyze sample text
        sample = """
        I'm sorry, but as a language model, I cannot assist with that request.
        It's important to note that I must follow ethical guidelines.
        """
        result = monitor.monitor_stream(sample, model_name="test", callback=alert_callback)
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
