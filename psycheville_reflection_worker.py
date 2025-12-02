#!/usr/bin/env python3
"""
PsycheVille Reflection Worker
Self-Observing Infrastructure Architecture

Aggregates department logs and generates AI-powered insights using Ollama LLM.
"""

import json
import os
import sys
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional
from collections import defaultdict
import yaml


class PsycheVilleWorker:
    """Main reflection worker that processes logs and generates insights"""
    
    def __init__(self, config_path: str = "psycheville.yaml"):
        """Initialize worker with configuration"""
        self.config_path = config_path
        self.config = self._load_config()
        
        self.departments = self.config['psycheville']['departments']
        self.worker_config = self.config['psycheville']['reflection_worker']
        self.analytics_config = self.config['psycheville']['analytics']
        
        self.output_dir = Path(self.worker_config['output_dir'])
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        (self.output_dir / "Daily Reports").mkdir(exist_ok=True)
        (self.output_dir / "Weekly Synthesis").mkdir(exist_ok=True)
    
    def _load_config(self) -> Dict[str, Any]:
        """Load YAML configuration file"""
        try:
            with open(self.config_path) as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"❌ Configuration file not found: {self.config_path}")
            sys.exit(1)
        except yaml.YAMLError as e:
            print(f"❌ Error parsing YAML configuration: {e}")
            sys.exit(1)
    
    def collect_logs(self, department: str, hours: int = 24) -> List[Dict[str, Any]]:
        """Collect logs from a department for the last N hours"""
        log_file = self.departments[department]['log_file']
        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours)
        
        events = []
        try:
            with open(log_file, 'r') as f:
                for line in f:
                    try:
                        event = json.loads(line.strip())
                        # Parse timestamp
                        timestamp_str = event.get('timestamp', '')
                        if timestamp_str:
                            # Handle various timestamp formats
                            timestamp_str = timestamp_str.replace('Z', '+00:00')
                            try:
                                event_time = datetime.fromisoformat(timestamp_str)
                            except ValueError:
                                # Try parsing as unix timestamp if it's numeric
                                try:
                                    event_time = datetime.fromtimestamp(float(timestamp_str), tz=timezone.utc)
                                except (ValueError, TypeError):
                                    # Skip events with invalid timestamps
                                    continue
                            
                            if event_time >= cutoff_time:
                                events.append(event)
                    except (json.JSONDecodeError, KeyError, ValueError) as e:
                        # Skip malformed log entries
                        continue
        except FileNotFoundError:
            print(f"  ⚠️  Log file not found: {log_file}")
        except Exception as e:
            print(f"  ⚠️  Error reading log file: {e}")
        
        return events
    
    def analyze_department(self, department: str, events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze department events and calculate metrics"""
        if not events:
            return {
                'total_events': 0,
                'event_types': {},
                'time_range': None,
                'metrics': {},
                'anomalies': []
            }
        
        metrics = {
            'total_events': len(events),
            'event_types': defaultdict(int),
            'time_range': {
                'start': events[0].get('timestamp'),
                'end': events[-1].get('timestamp')
            },
            'metrics': {},
            'anomalies': []
        }
        
        # Count event types
        for event in events:
            event_type = event.get('event_type', 'unknown')
            metrics['event_types'][event_type] += 1
        
        # Convert defaultdict to regular dict for JSON serialization
        metrics['event_types'] = dict(metrics['event_types'])
        
        # Calculate department-specific metrics
        dept_config = self.departments[department]
        
        # Check thresholds if defined
        if 'thresholds' in dept_config:
            self._check_thresholds(department, events, metrics)
        
        # Calculate response times if available
        self._calculate_response_times(events, metrics)
        
        # Detect patterns
        self._detect_patterns(events, metrics)
        
        return metrics
    
    def _check_thresholds(self, department: str, events: List[Dict[str, Any]], metrics: Dict[str, Any]):
        """Check if metrics exceed defined thresholds"""
        thresholds = self.departments[department].get('thresholds', {})
        
        # Check error rate
        if 'max_error_rate_percent' in thresholds:
            error_events = sum(1 for e in events if e.get('event_type') == 'error' or e.get('error', False))
            error_rate = (error_events / len(events)) * 100 if events else 0
            metrics['metrics']['error_rate'] = round(error_rate, 2)
            
            if error_rate > thresholds['max_error_rate_percent']:
                metrics['anomalies'].append({
                    'type': 'high_error_rate',
                    'severity': 'critical',
                    'message': f"Error rate {error_rate:.2f}% exceeds threshold {thresholds['max_error_rate_percent']}%"
                })
    
    def _calculate_response_times(self, events: List[Dict[str, Any]], metrics: Dict[str, Any]):
        """Calculate response time statistics"""
        response_times = []
        for event in events:
            if 'response_time_ms' in event.get('metadata', {}):
                response_times.append(event['metadata']['response_time_ms'])
            elif 'duration_ms' in event.get('metadata', {}):
                response_times.append(event['metadata']['duration_ms'])
        
        if response_times:
            metrics['metrics']['response_times'] = {
                'avg': round(sum(response_times) / len(response_times), 2),
                'min': min(response_times),
                'max': max(response_times),
                'count': len(response_times)
            }
    
    def _detect_patterns(self, events: List[Dict[str, Any]], metrics: Dict[str, Any]):
        """Detect interesting patterns in the event stream"""
        # Group events by hour
        hourly_distribution = defaultdict(int)
        for event in events:
            timestamp_str = event.get('timestamp', '')
            if timestamp_str:
                try:
                    timestamp_str = timestamp_str.replace('Z', '+00:00')
                    event_time = datetime.fromisoformat(timestamp_str)
                    hour = event_time.hour
                    hourly_distribution[hour] += 1
                except (ValueError, AttributeError):
                    continue
        
        if hourly_distribution:
            # Find peak hour
            peak_hour = max(hourly_distribution.items(), key=lambda x: x[1])
            metrics['metrics']['peak_hour'] = {
                'hour': peak_hour[0],
                'events': peak_hour[1]
            }
    
    def generate_llm_prompt(self, department: str, metrics: Dict[str, Any]) -> str:
        """Generate prompt for LLM analysis"""
        dept_name = self.departments[department]['name']
        dept_description = self.departments[department].get('description', '')
        
        prompt = f"""You are analyzing observability data for the {dept_name} department.

Department: {dept_name}
Description: {dept_description}
Time Period: Last 24 hours
Total Events: {metrics['total_events']}

Event Breakdown:
"""
        # Add event types
        if metrics['event_types']:
            for event_type, count in sorted(metrics['event_types'].items(), key=lambda x: x[1], reverse=True):
                prompt += f"- {event_type}: {count}\n"
        else:
            prompt += "- No events recorded\n"
        
        # Add metrics
        if metrics.get('metrics'):
            prompt += "\nKey Metrics:\n"
            if 'error_rate' in metrics['metrics']:
                prompt += f"- Error Rate: {metrics['metrics']['error_rate']}%\n"
            if 'response_times' in metrics['metrics']:
                rt = metrics['metrics']['response_times']
                prompt += f"- Response Times: avg={rt['avg']}ms, min={rt['min']}ms, max={rt['max']}ms\n"
            if 'peak_hour' in metrics['metrics']:
                ph = metrics['metrics']['peak_hour']
                prompt += f"- Peak Activity: Hour {ph['hour']} with {ph['events']} events\n"
        
        # Add anomalies
        if metrics.get('anomalies'):
            prompt += "\nAnomalies Detected:\n"
            for anomaly in metrics['anomalies']:
                prompt += f"- [{anomaly['severity'].upper()}] {anomaly['message']}\n"
        
        prompt += """
Please provide a concise analysis with:
1. Key insights about department activity
2. Potential issues or anomalies (if any)
3. Optimization recommendations (if applicable)
4. Action items for the team (if any)

Keep the analysis practical and actionable. If activity is normal, say so briefly.
"""
        
        return prompt
    
    def query_llm(self, prompt: str) -> str:
        """Query Ollama LLM for analysis"""
        llm_model = self.worker_config.get('llm_model', 'llama3:latest')
        
        try:
            # Check if ollama is available
            subprocess.run(['ollama', '--version'], capture_output=True, check=True)
            
            # Run ollama with prompt
            result = subprocess.run(
                ['ollama', 'run', llm_model, prompt],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return f"LLM query failed: {result.stderr}"
                
        except subprocess.TimeoutExpired:
            return "⚠️ LLM query timeout - analysis unavailable. Consider using a smaller model or increasing timeout."
        except FileNotFoundError:
            return "⚠️ Ollama not installed - analysis unavailable. Install from https://ollama.ai/"
        except subprocess.CalledProcessError as e:
            return f"⚠️ Ollama error: {e.stderr}"
        except Exception as e:
            return f"⚠️ Unexpected error querying LLM: {str(e)}"
    
    def generate_obsidian_note(self, department: str, metrics: Dict[str, Any], analysis: str):
        """Generate Obsidian markdown note"""
        dept_name = self.departments[department]['name']
        today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        
        # Save to Daily Reports folder
        note_path = self.output_dir / "Daily Reports" / f"{today}-{department}.md"
        
        content = f"""# {dept_name} Daily Report
**Date:** {today}
**Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC

## 📊 Metrics Summary

- **Total Events:** {metrics['total_events']:,}
"""
        
        if metrics['time_range']:
            content += f"- **Time Range:** {metrics['time_range']['start']} to {metrics['time_range']['end']}\n"
        
        # Add metrics
        if metrics.get('metrics'):
            if 'error_rate' in metrics['metrics']:
                content += f"- **Error Rate:** {metrics['metrics']['error_rate']}%\n"
            if 'response_times' in metrics['metrics']:
                rt = metrics['metrics']['response_times']
                content += f"- **Avg Response Time:** {rt['avg']}ms (min: {rt['min']}ms, max: {rt['max']}ms)\n"
            if 'peak_hour' in metrics['metrics']:
                ph = metrics['metrics']['peak_hour']
                content += f"- **Peak Activity:** Hour {ph['hour']}:00 with {ph['events']} events\n"
        
        # Event breakdown
        if metrics['event_types']:
            content += "\n### Event Breakdown\n"
            for event_type, count in sorted(metrics['event_types'].items(), key=lambda x: x[1], reverse=True):
                percentage = (count / metrics['total_events']) * 100 if metrics['total_events'] > 0 else 0
                content += f"- **{event_type}:** {count:,} ({percentage:.1f}%)\n"
        
        # Anomalies
        if metrics.get('anomalies'):
            content += "\n### 🚨 Anomalies\n"
            for anomaly in metrics['anomalies']:
                severity_emoji = {'critical': '🔴', 'warning': '⚠️', 'info': 'ℹ️'}.get(anomaly['severity'], '•')
                content += f"{severity_emoji} **{anomaly['type'].replace('_', ' ').title()}**: {anomaly['message']}\n"
        
        # AI Analysis
        content += f"""
## 🤖 AI Analysis

{analysis}

## 🔗 Related Notes

- [[PsycheVille Dashboard]]
- [[{dept_name} Archive]]
- [[Weekly Synthesis {datetime.now(timezone.utc).strftime('%Y-W%U')}]]

## 📝 Tags

#psycheville #daily-report #{department.replace('_', '-')} #{datetime.now(timezone.utc).strftime('%Y-%m-%d')}

---
*Generated by PsycheVille Reflection Worker v{self.config['psycheville']['version']}*
"""
        
        with open(note_path, 'w') as f:
            f.write(content)
        
        return note_path
    
    def generate_dashboard(self, all_metrics: Dict[str, Dict[str, Any]]):
        """Generate main dashboard note"""
        today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        dashboard_path = self.output_dir / "PsycheVille Dashboard.md"
        
        content = f"""# PsycheVille Dashboard
**Self-Observing Infrastructure Architecture**

Last Updated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC

## 📊 Department Overview

"""
        
        # Add summary for each department
        for dept_id, metrics in sorted(all_metrics.items()):
            dept_name = self.departments[dept_id]['name']
            status_emoji = "✅" if metrics['total_events'] > 0 else "⚠️"
            
            content += f"### {status_emoji} {dept_name}\n"
            content += f"- **Events (24h):** {metrics['total_events']:,}\n"
            
            if metrics.get('metrics', {}).get('error_rate'):
                error_emoji = "✅" if metrics['metrics']['error_rate'] < 1.0 else "⚠️"
                content += f"- {error_emoji} **Error Rate:** {metrics['metrics']['error_rate']}%\n"
            
            if metrics.get('anomalies'):
                content += f"- 🚨 **Anomalies:** {len(metrics['anomalies'])}\n"
            
            content += f"- 📄 [[{today}-{dept_id}|View Report]]\n\n"
        
        # Quick stats
        total_events = sum(m['total_events'] for m in all_metrics.values())
        active_departments = sum(1 for m in all_metrics.values() if m['total_events'] > 0)
        total_anomalies = sum(len(m.get('anomalies', [])) for m in all_metrics.values())
        
        content += f"""
## 📈 Quick Stats

- **Total Events (24h):** {total_events:,}
- **Active Departments:** {active_departments}/{len(all_metrics)}
- **Anomalies:** {total_anomalies}

## 🔗 Quick Links

- [[Daily Reports]] — Browse all daily reports
- [[Weekly Synthesis]] — View weekly summaries
- [[PsycheVille Architecture]] — System documentation

## 📝 Configuration

- **Version:** {self.config['psycheville']['version']}
- **Departments:** {len(self.departments)}
- **Update Frequency:** {self.worker_config['schedule']}
- **LLM Model:** {self.worker_config['llm_model']}

---
*Last refresh: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC*
"""
        
        with open(dashboard_path, 'w') as f:
            f.write(content)
        
        print(f"✅ Updated dashboard: {dashboard_path}")
    
    def run_daily_reflection(self):
        """Run daily reflection for all departments"""
        print(f"\n{'='*60}")
        print(f"🔄 PsycheVille Daily Reflection")
        print(f"{'='*60}")
        print(f"Started: {datetime.now(timezone.utc).isoformat()}")
        print(f"Config: {self.config_path}")
        print(f"Departments: {len(self.departments)}")
        print(f"{'='*60}\n")
        
        all_metrics = {}
        
        for dept_id, dept_config in self.departments.items():
            dept_name = dept_config['name']
            print(f"📂 Processing {dept_name}...")
            
            # Collect logs
            events = self.collect_logs(dept_id, hours=24)
            print(f"  └─ Collected {len(events):,} events")
            
            # Analyze metrics
            metrics = self.analyze_department(dept_id, events)
            all_metrics[dept_id] = metrics
            
            if metrics['total_events'] == 0:
                print(f"  └─ ⚠️  No events found for {dept_name}")
                # Still generate a report noting inactivity
                analysis = f"No activity detected in the last 24 hours for {dept_name}. This may indicate:\n- Department is idle or unused\n- Logging is not configured\n- System is offline\n\nAction: Investigate department status."
            else:
                # Generate LLM analysis
                print(f"  └─ 🤖 Generating AI analysis...")
                prompt = self.generate_llm_prompt(dept_id, metrics)
                analysis = self.query_llm(prompt)
            
            # Generate Obsidian note
            note_path = self.generate_obsidian_note(dept_id, metrics, analysis)
            print(f"  └─ ✅ Report saved: {note_path.name}\n")
        
        # Generate dashboard
        print("📊 Generating dashboard...")
        self.generate_dashboard(all_metrics)
        
        print(f"\n{'='*60}")
        print(f"✅ Daily reflection complete!")
        print(f"{'='*60}")
        print(f"Reports: {self.output_dir / 'Daily Reports'}")
        print(f"Dashboard: {self.output_dir / 'PsycheVille Dashboard.md'}")
        print(f"{'='*60}\n")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='PsycheVille Reflection Worker - Self-Observing Infrastructure',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with default config
  python psycheville_reflection_worker.py
  
  # Run with custom config
  python psycheville_reflection_worker.py --config /path/to/config.yaml
  
  # Run in verbose mode
  python psycheville_reflection_worker.py --verbose
        """
    )
    
    parser.add_argument(
        '--config', '-c',
        default='psycheville.yaml',
        help='Path to configuration file (default: psycheville.yaml)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='PsycheVille Reflection Worker 1.0.0'
    )
    
    args = parser.parse_args()
    
    try:
        worker = PsycheVilleWorker(config_path=args.config)
        worker.run_daily_reflection()
        return 0
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        return 130
    except Exception as e:
        print(f"\n❌ Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
