#!/usr/bin/env python3
"""
PsycheVille Reflection Worker
Monitors logs from Tools Refinery and generates automated reflection reports
"""

import os
import yaml
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Any, Optional
import schedule
import time
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('PsycheVille')


class ReflectionWorker:
    """Monitors logs and generates reflection reports"""
    
    def __init__(self, config_path: str = "/app/psycheville.yaml"):
        """Initialize the reflection worker"""
        self.config_path = config_path
        self.config = self._load_config()
        self.observations = defaultdict(list)
        logger.info("PsycheVille Reflection Worker initialized")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)
            logger.info(f"Loaded configuration from {self.config_path}")
            return config
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            raise
    
    def _parse_log_line(self, line: str, patterns: List[Dict]) -> Optional[Dict]:
        """Parse a log line against observation patterns"""
        for pattern_config in patterns:
            pattern = pattern_config['pattern']
            if pattern in line:
                # Extract data based on pattern
                observation = {
                    'pattern': pattern,
                    'raw_line': line,
                    'timestamp': datetime.now().isoformat(),
                    'extracted': {}
                }
                
                # Try to extract structured data
                for field in pattern_config.get('extract', []):
                    # Simple extraction - look for field=value or field:value patterns
                    # Escape field name to handle special regex characters
                    escaped_field = re.escape(field)
                    match = re.search(rf'{escaped_field}[=:]\s*([^\s,;]+)', line)
                    if match:
                        observation['extracted'][field] = match.group(1)
                
                return observation
        return None
    
    def monitor_logs(self, department: str, log_path: str, patterns: List[Dict]):
        """Monitor logs for a specific department"""
        log_dir = Path(log_path)
        
        if not log_dir.exists():
            logger.warning(f"Log directory does not exist: {log_path}")
            log_dir.mkdir(parents=True, exist_ok=True)
            return
        
        # Read all log files in directory
        for log_file in log_dir.glob("*.log"):
            try:
                with open(log_file, 'r') as f:
                    for line in f:
                        observation = self._parse_log_line(line.strip(), patterns)
                        if observation:
                            self.observations[department].append(observation)
            except Exception as e:
                logger.error(f"Error reading log file {log_file}: {e}")
    
    def analyze_observations(self, department: str) -> Dict[str, Any]:
        """Analyze observations and extract patterns"""
        obs_list = self.observations.get(department, [])
        
        if not obs_list:
            return {
                'total_observations': 0,
                'patterns': {},
                'insights': ["No observations recorded yet"],
                'recommendations': ["Start using the Tools Refinery to generate logs"]
            }
        
        # Count patterns
        pattern_counts = Counter([obs['pattern'] for obs in obs_list])
        
        # Extract insights based on patterns
        insights = []
        recommendations = []
        
        # Tool usage analysis
        if 'tool_invoked' in pattern_counts:
            invoked_count = pattern_counts['tool_invoked']
            insights.append(f"Tools were invoked {invoked_count} times")
            
            # Get most used tools
            tool_names = [
                obs['extracted'].get('tool_name', 'unknown')
                for obs in obs_list
                if obs['pattern'] == 'tool_invoked'
            ]
            if tool_names:
                most_common = Counter(tool_names).most_common(3)
                insights.append(f"Most used tools: {', '.join([f'{name} ({count}x)' for name, count in most_common])}")
        
        if 'tool_created' in pattern_counts:
            created_count = pattern_counts['tool_created']
            insights.append(f"{created_count} new tools were created")
            recommendations.append("Consider documenting new tools for team visibility")
        
        if 'tool_failed' in pattern_counts:
            failed_count = pattern_counts['tool_failed']
            insights.append(f"⚠️ {failed_count} tool failures detected")
            recommendations.append("Investigate failing tools and improve error handling")
        
        # Generic insights
        if not insights:
            insights.append("System is operational but usage is low")
            recommendations.append("Increase engagement with Tools Refinery")
        
        return {
            'total_observations': len(obs_list),
            'patterns': dict(pattern_counts),
            'insights': insights,
            'recommendations': recommendations
        }
    
    def generate_report(self, department: str, analysis: Dict[str, Any]) -> str:
        """Generate a markdown report"""
        template = self.config['reports']['template']
        
        # Build observations section
        obs_list = self.observations.get(department, [])
        observations_md = ""
        if obs_list:
            observations_md = f"Total observations: {analysis['total_observations']}\n\n"
            observations_md += "Pattern breakdown:\n"
            for pattern, count in analysis['patterns'].items():
                observations_md += f"- `{pattern}`: {count} times\n"
        else:
            observations_md = "No observations recorded yet."
        
        # Build patterns section
        patterns_md = "\n".join([f"- {p}: {c}" for p, c in analysis['patterns'].items()])
        if not patterns_md:
            patterns_md = "No patterns detected yet."
        
        # Build insights section
        insights_md = "\n".join([f"- {insight}" for insight in analysis['insights']])
        
        # Build recommendations section
        recommendations_md = "\n".join([f"- {rec}" for rec in analysis['recommendations']])
        
        # Fill template
        report = template.replace('{{date}}', datetime.now().strftime('%Y-%m-%d'))
        report = report.replace('{{department}}', department)
        report = report.replace('{{observations}}', observations_md)
        report = report.replace('{{patterns}}', patterns_md)
        report = report.replace('{{insights}}', insights_md)
        report = report.replace('{{recommendations}}', recommendations_md)
        
        return report
    
    def save_report(self, department: str, report: str):
        """Save report to Obsidian vault"""
        dept_config = self.config['departments'].get(department, {})
        obsidian_path = dept_config.get('obsidian_path', 
                                       f"/app/obsidian_vault/PsycheVille/Departments/{department}")
        
        # Create directory if it doesn't exist
        Path(obsidian_path).mkdir(parents=True, exist_ok=True)
        
        # Generate filename
        filename = f"reflection_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.md"
        filepath = Path(obsidian_path) / filename
        
        # Write report
        try:
            with open(filepath, 'w') as f:
                f.write(report)
            logger.info(f"Report saved to {filepath}")
        except Exception as e:
            logger.error(f"Failed to save report: {e}")
    
    def run_daily_reflection(self):
        """Run daily reflection for all departments"""
        logger.info("Running daily reflection...")
        
        departments = self.config.get('reflection', {}).get('daily', {}).get('departments', [])
        
        for dept_name in departments:
            dept_config = self.config['departments'].get(dept_name)
            if not dept_config:
                logger.warning(f"Department config not found: {dept_name}")
                continue
            
            logger.info(f"Processing department: {dept_name}")
            
            # Monitor logs
            self.monitor_logs(
                dept_name,
                dept_config['log_path'],
                dept_config.get('observation_patterns', [])
            )
            
            # Analyze observations
            analysis = self.analyze_observations(dept_name)
            
            # Generate report
            report = self.generate_report(dept_name, analysis)
            
            # Save report
            self.save_report(dept_name, report)
            
            logger.info(f"Completed reflection for {dept_name}")
        
        # Clear observations after reporting
        self.observations.clear()
        logger.info("Daily reflection completed")
    
    def schedule_reflections(self):
        """Schedule reflection jobs based on configuration"""
        reflection_config = self.config.get('reflection', {})
        
        # Daily reflection
        if reflection_config.get('daily', {}).get('enabled', False):
            time_str = reflection_config['daily'].get('time', '06:00')
            schedule.every().day.at(time_str).do(self.run_daily_reflection)
            logger.info(f"Scheduled daily reflection at {time_str}")
        
        # Weekly reflection
        if reflection_config.get('weekly', {}).get('enabled', False):
            day = reflection_config['weekly'].get('day', 'Sunday')
            time_str = reflection_config['weekly'].get('time', '08:00')
            getattr(schedule.every(), day.lower()).at(time_str).do(self.run_daily_reflection)
            logger.info(f"Scheduled weekly reflection on {day} at {time_str}")
        
        # For immediate testing, also run once on startup
        logger.info("Running initial reflection on startup...")
        self.run_daily_reflection()
    
    def run(self):
        """Main run loop"""
        logger.info("Starting PsycheVille Reflection Worker")
        
        # Schedule reflections
        self.schedule_reflections()
        
        # Run scheduler
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute


def main():
    """Entry point"""
    config_path = os.getenv('PSYCHEVILLE_CONFIG', '/app/psycheville.yaml')
    worker = ReflectionWorker(config_path)
    worker.run()


if __name__ == '__main__':
    main()
