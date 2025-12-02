#!/usr/bin/env python3
"""
PsycheVille Sample Logger
Generates sample log events for testing the reflection worker
"""

import json
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Sample event types for each department
DEPARTMENT_EVENTS = {
    'tools_refinery': [
        ('endpoint_called', {'endpoint': '/api/v1/tools/list'}),
        ('endpoint_called', {'endpoint': '/api/v1/tools/search'}),
        ('endpoint_called', {'endpoint': '/api/v1/tools/create'}),
        ('endpoint_called', {'endpoint': '/api/v1/tools/update'}),
        ('endpoint_called', {'endpoint': '/api/v1/tools/delete'}),
        ('error', {'error_code': 404, 'message': 'Tool not found'}),
        ('error', {'error_code': 500, 'message': 'Internal server error'}),
    ],
    'sovereign_ai_lab': [
        ('model_inference', {'model': 'llama3', 'tokens': 150}),
        ('model_inference', {'model': 'mistral', 'tokens': 200}),
        ('training_session', {'model': 'custom-lora', 'epochs': 10}),
        ('error', {'error_type': 'model_loading_failed'}),
        ('embedding_generation', {'count': 1000}),
    ],
    'rf_sensor_lab': [
        ('sensor_reading', {'sensor_id': 'rf-001', 'frequency_mhz': 2400}),
        ('calibration', {'sensor_id': 'rf-001', 'success': True}),
        ('data_quality_check', {'score': 0.95}),
    ],
    'quantum_emulation': [
        ('emulation_run', {'qubits': 8, 'depth': 10}),
        ('gate_operation', {'gate_type': 'CNOT', 'fidelity': 0.98}),
        ('measurement', {'qubit': 3, 'result': 1}),
    ],
    'cloud_os': [
        ('container_start', {'container': 'api-server', 'status': 'success'}),
        ('deployment', {'service': 'web-app', 'version': 'v1.2.3'}),
        ('build', {'project': 'main', 'duration_ms': 45000}),
        ('test_run', {'suite': 'integration', 'passed': 42, 'failed': 0}),
    ]
}


def generate_event(department: str, base_time: datetime = None) -> dict:
    """Generate a random event for a department"""
    if base_time is None:
        base_time = datetime.now(timezone.utc)
    
    # Random time offset within the last 24 hours
    time_offset = timedelta(seconds=random.randint(0, 86400))
    event_time = base_time - time_offset
    # Format as ISO 8601 with Z suffix (UTC) - replace timezone offset with Z
    timestamp = event_time.isoformat().replace('+00:00', 'Z')
    
    # Select random event type
    event_type, metadata = random.choice(DEPARTMENT_EVENTS[department])
    
    # Add common metadata
    event_metadata = dict(metadata)
    
    # Add response time for endpoint calls
    if event_type == 'endpoint_called':
        event_metadata['response_time_ms'] = random.randint(20, 300)
    
    # Add duration for other events
    elif event_type in ['model_inference', 'training_session', 'build']:
        event_metadata['duration_ms'] = random.randint(500, 5000)
    
    event = {
        'timestamp': timestamp,
        'department': department,
        'event_type': event_type,
        'metadata': event_metadata
    }
    
    return event


def generate_logs(log_dir: str = '/var/log/psycheville', num_events: int = 100):
    """Generate sample logs for all departments"""
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)
    
    print(f"🔄 Generating {num_events} events per department...")
    print(f"📁 Log directory: {log_dir}\n")
    
    for department in DEPARTMENT_EVENTS.keys():
        log_file = log_path / f"{department}.jsonl"
        
        with open(log_file, 'w') as f:
            for _ in range(num_events):
                event = generate_event(department)
                f.write(json.dumps(event) + '\n')
        
        print(f"✅ Generated {num_events} events for {department}")
    
    print(f"\n✅ Sample logs generated successfully!")
    print(f"📊 Run reflection worker: python3 psycheville_reflection_worker.py")


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate sample logs for PsycheVille')
    parser.add_argument('--log-dir', default='/var/log/psycheville',
                        help='Directory to write log files (default: /var/log/psycheville)')
    parser.add_argument('--events', type=int, default=100,
                        help='Number of events per department (default: 100)')
    
    args = parser.parse_args()
    
    try:
        generate_logs(args.log_dir, args.events)
    except PermissionError:
        print(f"\n⚠️  Permission denied writing to {args.log_dir}")
        print(f"💡 Try running with: --log-dir ~/.psycheville/logs")
        print(f"   Or run with sudo: sudo python3 {__file__}")
