#!/usr/bin/env python3
"""
Test script to generate sample logs for PsycheVille
This helps verify that the monitoring system is working
"""

import logging
import json
import time
from datetime import datetime
from pathlib import Path
import random

# Ensure log directory exists
log_dir = Path(__file__).parent / "logs" / "tools_refinery"
log_dir.mkdir(parents=True, exist_ok=True)

# Configure logging
log_file = log_dir / "tools.log"
logging.basicConfig(
    filename=str(log_file),
    level=logging.INFO,
    format='%(message)s'
)
logger = logging.getLogger('tools_refinery')


def log_tool_event(event_type, tool_name, **kwargs):
    """Log tool events for PsycheVille monitoring"""
    event = {
        'pattern': event_type,
        'tool_name': tool_name,
        'timestamp': datetime.now().isoformat(),
        **kwargs
    }
    logger.info(json.dumps(event))
    print(f"✓ Logged: {event_type} for {tool_name}")


def generate_sample_logs():
    """Generate sample logs to test PsycheVille"""
    
    tools = [
        'deploy-script',
        'test-runner',
        'linter',
        'backup-tool',
        'monitoring-agent',
        'data-sync',
        'security-scanner',
        'performance-analyzer'
    ]
    
    print("\n" + "="*60)
    print("Generating Sample Logs for PsycheVille")
    print("="*60 + "\n")
    
    # Simulate tool creation
    print("📝 Creating tools...")
    for tool in random.sample(tools, 4):
        log_tool_event('tool_created', tool, creator='test_user')
        time.sleep(0.1)
    
    # Simulate tool usage
    print("\n🔧 Invoking tools...")
    for _ in range(15):
        tool = random.choice(tools)
        params = {'arg1': 'value1', 'arg2': random.randint(1, 100)}
        result = random.choice(['success', 'success', 'success', 'warning'])
        log_tool_event('tool_invoked', tool, parameters=params, result=result)
        time.sleep(0.1)
    
    # Simulate some failures
    print("\n⚠️  Simulating failures...")
    for _ in range(3):
        tool = random.choice(tools)
        errors = [
            'Connection timeout',
            'Permission denied',
            'Resource not found',
            'Invalid configuration'
        ]
        log_tool_event('tool_failed', tool, error=random.choice(errors))
        time.sleep(0.1)
    
    print("\n" + "="*60)
    print(f"✅ Sample logs generated!")
    print(f"📁 Log file: {log_file}")
    print(f"📊 Total events: 22")
    print("="*60 + "\n")
    
    print("Next steps:")
    print("1. Start PsycheVille: docker-compose -f docker-compose.psycheville.yml up -d")
    print("2. Wait for reflection generation (runs immediately on startup)")
    print("3. Check reports: ls -la psycheville/obsidian_vault/PsycheVille/Departments/Tools_Refinery/")
    print()


if __name__ == '__main__':
    generate_sample_logs()
