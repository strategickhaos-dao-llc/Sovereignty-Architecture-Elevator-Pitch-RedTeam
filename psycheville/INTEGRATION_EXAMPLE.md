# PsycheVille Integration Examples

This document shows how to integrate PsycheVille monitoring into various components of the Sovereignty Architecture.

## Table of Contents

- [Python Projects](#python-projects)
- [Shell Scripts](#shell-scripts)
- [Docker Services](#docker-services)
- [Refinory Integration](#refinory-integration)
- [Custom Integrations](#custom-integrations)

---

## Python Projects

### Basic Integration

```python
from psycheville.psycheville_logger import PsycheVilleLogger

# Initialize logger
pv = PsycheVilleLogger()

# Log tool events
def create_backup_tool():
    pv.tool_created('backup-tool', creator='admin')
    # ... tool creation logic ...

def run_backup():
    pv.tool_invoked('backup-tool', parameters={'destination': '/backup'})
    try:
        # ... backup logic ...
        pv.tool_invoked('backup-tool', result='success')
    except Exception as e:
        pv.tool_failed('backup-tool', error=str(e))
```

### Advanced Integration with Context

```python
from psycheville.psycheville_logger import PsycheVilleLogger
import time

class ToolManager:
    def __init__(self):
        self.pv = PsycheVilleLogger(department='tools_refinery')
    
    def execute_tool(self, tool_name, **params):
        """Execute a tool with automatic PsycheVille logging"""
        start_time = time.time()
        
        self.pv.tool_invoked(
            tool_name,
            parameters=params,
            user=params.get('user', 'system')
        )
        
        try:
            # Tool execution logic here
            result = self._execute(tool_name, **params)
            
            latency = time.time() - start_time
            self.pv.tool_invoked(
                tool_name,
                result='success',
                latency=latency,
                output_size=len(str(result))
            )
            
            return result
            
        except Exception as e:
            self.pv.tool_failed(
                tool_name,
                error=str(e),
                stack_trace=repr(e)
            )
            raise
```

---

## Shell Scripts

### Basic Shell Integration

```bash
#!/bin/bash
# deploy-service.sh - Service deployment script with PsycheVille logging

LOG_FILE="${PSYCHEVILLE_LOGS:-./psycheville/logs/tools_refinery/tools.log}"
TOOL_NAME="deploy-service"

log_event() {
    local pattern=$1
    shift
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    echo "{\"pattern\":\"$pattern\",\"tool_name\":\"$TOOL_NAME\",\"timestamp\":\"$timestamp\",$*}" >> "$LOG_FILE"
}

# Log tool invocation
log_event "tool_invoked" "\"parameters\":{\"service\":\"$1\",\"environment\":\"$2\"}"

# Deployment logic
if deploy_service "$1" "$2"; then
    log_event "tool_invoked" "\"result\":\"success\""
else
    log_event "tool_failed" "\"error\":\"Deployment failed\""
    exit 1
fi
```

### Advanced Shell Integration

```bash
#!/bin/bash
# monitoring-check.sh - Health check with resource monitoring

source "$(dirname "$0")/psycheville_shell_helpers.sh"

pv_init "monitoring-check"

# Check memory usage
MEMORY_USAGE=$(free | grep Mem | awk '{print $3/$2 * 100.0}')
if (( $(echo "$MEMORY_USAGE > 80" | bc -l) )); then
    pv_log_resource_alert "memory" 80 "$MEMORY_USAGE"
fi

# Check disk usage
DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -gt 80 ]; then
    pv_log_resource_alert "disk" 80 "$DISK_USAGE"
fi

pv_log_tool_invoked "result=success"
```

---

## Docker Services

### Docker Compose Integration

Add PsycheVille logging to your services:

```yaml
services:
  my-service:
    image: my-service:latest
    environment:
      - PSYCHEVILLE_ENABLED=true
      - PSYCHEVILLE_LOGS=/app/logs/tools_refinery
    volumes:
      - ./psycheville/logs/tools_refinery:/app/logs/tools_refinery
      - ./psycheville/psycheville_logger.py:/app/psycheville_logger.py:ro
```

### Service with Built-in Logging

```python
# my_service.py
import os
from psycheville_logger import PsycheVilleLogger

# Initialize with environment variable
log_dir = os.getenv('PSYCHEVILLE_LOGS', './logs')
pv = PsycheVilleLogger(log_dir=log_dir)

def startup():
    pv.deployment('my-service', status='starting', environment=os.getenv('ENV', 'dev'))

def health_check():
    pv.log_event('health_check', status='healthy', service='my-service')
```

---

## Refinory Integration

### Adding PsycheVille to Refinory Orchestrator

**File**: `refinory/refinory/orchestrator.py`

```python
# Add import at the top
from psycheville.psycheville_logger import PsycheVilleLogger

class ExpertOrchestrator:
    def __init__(self, database: Database, expert_team: ExpertTeam, settings: Settings):
        self.db = database
        self.experts = expert_team
        self.settings = settings
        
        # Initialize PsycheVille logger
        self.pv_logger = PsycheVilleLogger(department='ai_agents')
        
    async def create_architecture_request(self, request: ArchitectureRequest):
        """Create new architecture generation request"""
        
        # Log tool creation
        self.pv_logger.tool_created(
            f'architecture-{request.project_name}',
            creator=request.github_repo or 'system'
        )
        
        # ... existing logic ...
        
    async def process_request(self, request_id: str):
        """Process architecture request"""
        
        # Log tool invocation
        self.pv_logger.tool_invoked(
            f'architecture-{request_id}',
            parameters={'experts': len(request.experts_requested or [])}
        )
        
        try:
            # ... existing processing logic ...
            
            # Log success
            self.pv_logger.tool_invoked(
                f'architecture-{request_id}',
                result='success'
            )
            
        except Exception as e:
            # Log failure
            self.pv_logger.tool_failed(
                f'architecture-{request_id}',
                error=str(e)
            )
            raise
```

### Adding PsycheVille to Refinory Experts

**File**: `refinory/refinory/experts.py`

```python
from psycheville.psycheville_logger import PsycheVilleLogger

class ExpertTeam:
    def __init__(self, openai_client, settings):
        self.client = openai_client
        self.settings = settings
        self.pv_logger = PsycheVilleLogger(department='ai_agents')
    
    async def invoke_expert(self, expert_name: str, prompt: str):
        """Invoke an expert with logging"""
        import time
        start_time = time.time()
        
        try:
            # Call OpenAI
            response = await self.client.chat.completions.create(
                model=self.settings.openai_model,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Calculate metrics
            latency = time.time() - start_time
            tokens = response.usage.total_tokens
            cost = self._calculate_cost(tokens)
            
            # Log agent query
            self.pv_logger.agent_query(
                expert_name,
                query_type='architecture_generation',
                latency=latency,
                success=True
            )
            
            # Log model invocation
            self.pv_logger.model_invocation(
                self.settings.openai_model,
                tokens=tokens,
                cost=cost
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            self.pv_logger.agent_query(
                expert_name,
                query_type='architecture_generation',
                success=False,
                error=str(e)
            )
            raise
```

---

## Custom Integrations

### Custom Department

Create a custom department for specialized monitoring:

```python
from psycheville.psycheville_logger import PsycheVilleLogger

# Create logger for custom department
security_logger = PsycheVilleLogger(department='security')

# Log security events
security_logger.log_event('vulnerability_scan', 
                         scan_type='dependencies',
                         findings=5,
                         severity='high')

security_logger.log_event('access_denied',
                         user='anonymous',
                         resource='/admin',
                         ip_address='192.168.1.1')
```

Update `psycheville/psycheville.yaml` to add the department:

```yaml
departments:
  Security:
    description: "Security events and vulnerability scans"
    log_path: "/app/logs/security"
    obsidian_path: "/app/obsidian_vault/PsycheVille/Departments/Security"
    observation_patterns:
      - pattern: "vulnerability_scan"
        extract: ["scan_type", "findings", "severity"]
      - pattern: "access_denied"
        extract: ["user", "resource", "ip_address"]
    reflection_questions:
      - "What security events occurred?"
      - "Are there patterns in access denials?"
      - "What vulnerabilities were discovered?"
```

### Decorator Pattern

Create a decorator for automatic logging:

```python
from functools import wraps
from psycheville.psycheville_logger import get_logger

def log_tool(tool_name=None):
    """Decorator to automatically log tool invocations"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            pv = get_logger()
            name = tool_name or func.__name__
            
            # Log invocation
            pv.tool_invoked(name, parameters=kwargs)
            
            try:
                result = func(*args, **kwargs)
                pv.tool_invoked(name, result='success')
                return result
            except Exception as e:
                pv.tool_failed(name, error=str(e))
                raise
                
        return wrapper
    return decorator

# Usage
@log_tool('data-processor')
def process_data(input_file, output_file):
    # ... processing logic ...
    pass
```

### Context Manager Pattern

```python
from contextlib import contextmanager
from psycheville.psycheville_logger import get_logger
import time

@contextmanager
def tool_execution(tool_name, **params):
    """Context manager for tool execution with automatic logging"""
    pv = get_logger()
    start_time = time.time()
    
    pv.tool_invoked(tool_name, parameters=params)
    
    try:
        yield
        latency = time.time() - start_time
        pv.tool_invoked(tool_name, result='success', latency=latency)
    except Exception as e:
        pv.tool_failed(tool_name, error=str(e))
        raise

# Usage
with tool_execution('image-processor', size='1024x1024', format='png'):
    # ... processing logic ...
    process_image()
```

---

## Testing Your Integration

After adding PsycheVille logging:

1. **Generate test events**:
   ```bash
   python3 psycheville/test_logging.py
   ```

2. **Run your service** and execute operations

3. **Check logs**:
   ```bash
   cat psycheville/logs/tools_refinery/tools.log
   ```

4. **Trigger reflection**:
   ```bash
   # If PsycheVille is running in Docker
   docker-compose -f docker-compose.psycheville.yml restart psycheville-worker
   
   # Wait a moment, then check reports
   ls -la psycheville/obsidian_vault/PsycheVille/Departments/*/
   ```

---

## Best Practices

1. **Log at Key Points**: Focus on creation, invocation, and failure events
2. **Include Context**: Add relevant metadata like user, environment, parameters
3. **Don't Over-Log**: Log significant events, not every operation
4. **Use Appropriate Departments**: Keep related events in the same department
5. **Handle Failures Gracefully**: Catch exceptions and log them before re-raising
6. **Test Your Integration**: Verify logs are being written correctly

---

## Troubleshooting

### Logs Not Appearing

**Problem**: Events are logged but not appearing in reflection reports

**Solution**: 
1. Check log file exists: `ls -la psycheville/logs/tools_refinery/`
2. Verify JSON format: `cat psycheville/logs/tools_refinery/tools.log | python3 -m json.tool`
3. Ensure patterns match config: Check `psycheville/psycheville.yaml`

### Permission Issues

**Problem**: Cannot write to log directory

**Solution**:
```bash
# Create directory with correct permissions
mkdir -p psycheville/logs/tools_refinery
chmod -R 755 psycheville/logs
```

### Module Not Found

**Problem**: `ModuleNotFoundError: No module named 'psycheville_logger'`

**Solution**:
```python
# Option 1: Add to Python path
import sys
sys.path.insert(0, '/path/to/repository')
from psycheville.psycheville_logger import PsycheVilleLogger

# Option 2: Copy psycheville_logger.py to your project
# Option 3: Install as package (if packaged)
```

---

## Next Steps

- Review [PsycheVille README](README.md) for deployment instructions
- Check [psycheville.yaml](psycheville.yaml) for configuration options
- Explore generated reports in `psycheville/obsidian_vault/`
