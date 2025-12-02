# Roadmap B: Balanced - "Give Me the Minimum Theory That Stops Things Breaking"

**Practical solutions + just enough theory to understand why they work.**

This roadmap provides 60 items that bridge your experimental chaos with foundational understanding. You'll learn the minimum architectural concepts needed to scale without hitting walls, explained in plain language with your actual code as examples.

## Philosophy

You're already solving distributed systems problems (5-node cluster, Tailscale networking, air-gapped deployments). Roadmap B shows you:
- The patterns you're already using (without knowing their formal names)
- Why certain approaches break at scale
- How to fix issues before they cascade
- The architectural vocabulary to communicate with any team

## Quick Start

```powershell
# Run the diagnostic
./roadmaps/roadmap-b/diagnose-patterns.ps1

# Read the personalized guide
cat ./roadmaps/roadmap-b/guides/your-patterns-explained.md

# Apply the fixes
./roadmaps/roadmap-b/apply-fixes.ps1
```

## The 60 Items

### Section 1: Common Failure Modes + One-Line Fixes (Items 1-20)

#### 1. Circular Dependencies
**What you're seeing:** Import errors, modules can't find each other
**Why it breaks:** A imports B, B imports A = deadlock
**One-line fix:** Move shared code to a third module C that both import

```python
# Before (breaks):
# user_service.py imports order_service.py
# order_service.py imports user_service.py

# After (works):
# user_service.py imports models.py
# order_service.py imports models.py
# models.py has shared User and Order classes
```

#### 2. Hardcoded Configuration
**What you're seeing:** Different behavior on different nodes, can't deploy to new environments
**Why it breaks:** Code expects specific hostnames/ports that don't exist elsewhere
**One-line fix:** Move all environment-specific values to environment variables or config files

```python
# Before: DB_HOST = "node1.local"
# After: DB_HOST = os.getenv("DB_HOST", "localhost")
```

#### 3. Missing Error Handling
**What you're seeing:** One network error brings down the entire service
**Why it breaks:** Uncaught exceptions propagate up and kill the process
**One-line fix:** Wrap external calls in try/except with retry logic

```python
# Before: data = requests.get(url).json()
# After:
for attempt in range(3):
    try:
        data = requests.get(url, timeout=10).json()
        break
    except RequestException:
        if attempt == 2: raise
        time.sleep(2 ** attempt)
```

#### 4. Race Conditions
**What you're seeing:** Intermittent errors that you can't reproduce
**Why it breaks:** Multiple threads/processes modifying shared state
**One-line fix:** Use locks, atomic operations, or message queues

```python
# Before: counter += 1  # Multiple threads = wrong count
# After: 
with threading.Lock():
    counter += 1
# Or better: use queue.Queue() for thread-safe operations
```

#### 5. Memory Leaks
**What you're seeing:** Service uses more RAM over time, eventually crashes
**Why it breaks:** Objects never get garbage collected (circular refs, unclosed files)
**One-line fix:** Use context managers (with statement) and close resources

```python
# Before: 
file = open('data.txt')
data = file.read()  # Never closed!

# After:
with open('data.txt') as file:
    data = file.read()  # Auto-closed
```

#### 6. Database Connection Exhaustion
**What you're seeing:** "Too many connections" errors after high load
**Why it breaks:** Opening connections without closing them
**One-line fix:** Use connection pooling

```python
# Before: conn = psycopg2.connect(...)  # New connection every time
# After: conn = pool.getconn()  # Reuse from pool
# And: pool.putconn(conn)  # Return to pool
```

#### 7. Slow Queries Blocking Everything
**What you're seeing:** One slow database query makes entire API unresponsive
**Why it breaks:** Synchronous processing blocks other requests
**One-line fix:** Use async/await or background workers

```python
# Before: 
result = slow_database_query()  # Blocks for 30 seconds
return result

# After:
result = await asyncio.create_task(slow_database_query())  # Non-blocking
```

#### 8. Missing Idempotency
**What you're seeing:** Retry logic causes duplicate payments/actions
**Why it breaks:** Same request processed multiple times has different effects
**One-line fix:** Add unique request IDs and check for duplicates

```python
# Before:
def create_order(user_id, items):
    order = Order.create(user_id, items)  # Creates duplicate on retry!

# After:
def create_order(user_id, items, request_id):
    if Order.exists(request_id): return Order.get(request_id)
    return Order.create(user_id, items, request_id)
```

#### 9. Unbounded Queues
**What you're seeing:** Memory grows until process crashes
**Why it breaks:** Producer faster than consumer, queue grows infinitely
**One-line fix:** Set max queue size and handle backpressure

```python
# Before: queue = Queue()  # Infinite size
# After: queue = Queue(maxsize=1000)  # Blocks when full
```

#### 10. Missing Health Checks
**What you're seeing:** Load balancer sends traffic to crashed instances
**Why it breaks:** No way for orchestrator to know service is unhealthy
**One-line fix:** Add /health endpoint that checks dependencies

```python
@app.get("/health")
def health():
    try:
        db.execute("SELECT 1")  # Check database
        return {"status": "healthy"}
    except:
        return {"status": "unhealthy"}, 503
```

#### 11. Timezone Confusion
**What you're seeing:** Events appear at wrong times across nodes
**Why it breaks:** Mixing naive and timezone-aware datetimes
**One-line fix:** Store everything in UTC, convert at display time

```python
# Before: now = datetime.now()  # Local time, varies by node
# After: now = datetime.now(timezone.utc)  # Always UTC
```

#### 12. Integer Overflow
**What you're seeing:** Counters wrap to negative numbers
**Why it breaks:** Exceeding max value for integer type
**One-line fix:** Use BigInt/Long or check before incrementing

```python
# Before: counter = 2147483647; counter += 1  # Wraps!
# After: counter = 2147483647; counter = min(counter + 1, sys.maxsize)
```

#### 13. File Path Issues
**What you're seeing:** "File not found" on some nodes but not others
**Why it breaks:** Hardcoded paths that don't exist on all systems
**One-line fix:** Use relative paths or environment variables

```python
# Before: data = open('/home/user/data.txt')  # Breaks on other nodes
# After: data = open(os.path.join(os.getcwd(), 'data.txt'))
```

#### 14. Logging Filling Disk
**What you're seeing:** Disk full, service crashes
**Why it breaks:** Logs never rotate or have size limits
**One-line fix:** Configure log rotation

```python
# Use RotatingFileHandler or TimedRotatingFileHandler
handler = RotatingFileHandler('app.log', maxBytes=10_000_000, backupCount=5)
```

#### 15. Missing Timeouts
**What you're seeing:** Request hangs forever waiting for response
**Why it breaks:** No limit on how long to wait for external service
**One-line fix:** Add timeout to all external calls

```python
# Before: response = requests.get(url)
# After: response = requests.get(url, timeout=30)
```

#### 16. SQL Injection
**What you're seeing:** Malicious users can execute arbitrary SQL
**Why it breaks:** Building SQL strings with user input
**One-line fix:** Use parameterized queries

```python
# Before: cursor.execute(f"SELECT * FROM users WHERE name = '{name}'")
# After: cursor.execute("SELECT * FROM users WHERE name = %s", (name,))
```

#### 17. Password Storage
**What you're seeing:** Passwords compromised in database breach
**Why it breaks:** Storing plaintext or weakly hashed passwords
**One-line fix:** Use bcrypt or argon2

```python
# Before: user.password = password  # Plaintext!
# After: user.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
```

#### 18. CORS Issues
**What you're seeing:** Frontend can't call your API from browser
**Why it breaks:** Browser blocks cross-origin requests
**One-line fix:** Add CORS headers

```python
# Flask example:
from flask_cors import CORS
CORS(app)
```

#### 19. Port Conflicts
**What you're seeing:** "Address already in use" errors
**Why it breaks:** Multiple services trying to bind same port
**One-line fix:** Use environment variable for port, set SO_REUSEADDR

```python
# Before: app.run(port=8080)
# After: app.run(port=int(os.getenv("PORT", 8080)))
```

#### 20. Unhandled Promise Rejections
**What you're seeing:** JavaScript process exits unexpectedly
**Why it breaks:** Async errors not caught
**One-line fix:** Add .catch() or try/catch with await

```javascript
// Before: await riskyOperation();  // Unhandled rejection
// After: 
try {
    await riskyOperation();
} catch (error) {
    console.error('Operation failed:', error);
}
```

### Section 2: Design Patterns You Already Use (Items 21-40)

These are the patterns in your current code. Now you know their names.

#### 21-25. Strategy Pattern
**What it is:** Different algorithms for the same task, switchable at runtime
**Where you use it:** Legal document processing (Wyoming SF0068 vs generic compliance)
**Why it matters:** Add new document types without modifying existing code

```python
# Your code (legal/processors/):
class WyomingProcessor:
    def process(self, doc): ...

class GenericProcessor:
    def process(self, doc): ...

# This is the Strategy pattern!
processor = WyomingProcessor() if doc.state == "WY" else GenericProcessor()
processor.process(doc)
```

#### 26-30. Observer Pattern
**What it is:** Objects notify other objects when state changes
**Where you use it:** Discord notifications when PR status changes
**Why it matters:** Decouple event producers from consumers

```python
# Your code (webhook handling):
class PRUpdated:
    def __init__(self):
        self.observers = []
    
    def notify(self, pr):
        for observer in self.observers:
            observer.update(pr)

# This is the Observer pattern!
pr_event.observers.append(DiscordNotifier())
pr_event.observers.append(DatabaseLogger())
```

#### 31-35. Factory Pattern
**What it is:** Object creation logic in one place
**Where you use it:** Creating different Refinory agents based on task
**Why it matters:** Complex initialization hidden from caller

```python
# Your code (refinory/experts.py):
def create_expert(task_type):
    if task_type == "legal":
        return LegalExpert(config.legal_model)
    elif task_type == "safety":
        return SafetyExpert(config.safety_model)
    # ...

# This is the Factory pattern!
expert = create_expert("legal")
```

#### 36-37. Singleton Pattern
**What it is:** Only one instance of a class exists
**Where you use it:** Database connection pool, configuration manager
**Why it matters:** Expensive resources shared across application

```python
# Your code (probably):
class DatabasePool:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.pool = create_pool()
        return cls._instance

# This is the Singleton pattern!
```

#### 38-40. Decorator Pattern
**What it is:** Add behavior to objects without modifying their class
**Where you use it:** Adding retry logic, logging, authentication
**Why it matters:** Cross-cutting concerns separated from business logic

```python
# Your code:
@retry(max_attempts=3)
@log_execution_time
def process_document(doc):
    ...

# This is the Decorator pattern!
```

### Section 3: Distributed Systems Truths (Items 41-60)

Why your Tailscale + NAS architecture already works.

#### 41-44. CAP Theorem
**What it is:** Can't have Consistency, Availability, AND Partition tolerance simultaneously
**Your choice:** You chose AP (Available + Partition tolerant) with eventual consistency
**Why it works:** Better to serve stale data than be down
**Your implementation:** Each node caches data, syncs asynchronously via NAS

#### 45-48. Eventual Consistency
**What it is:** All nodes eventually see the same data, but not immediately
**Your implementation:** Refinory results written to NAS, other nodes read when needed
**Why it works:** Legal analysis doesn't need real-time consistency
**Trade-off:** Accept brief inconsistency for better availability

#### 49-52. Idempotency
**What it is:** Operation can be repeated without changing result beyond first application
**Your implementation:** RAG indexing with document IDs, re-indexing same doc is safe
**Why it matters:** Retry logic doesn't corrupt data
**Rule:** All external-facing operations should be idempotent

#### 53-56. Network Partitions
**What it is:** Nodes can't communicate due to network failure
**Your reality:** Phone node loses WiFi, continues working offline
**Why Tailscale helps:** Automatic reconnection, peer-to-peer healing
**Your strategy:** Each node is autonomous, syncs when connection restored

#### 57-58. Latency vs Throughput
**What it is:** Speed of single request vs total requests per second
**Your optimization:** Batch operations (process multiple documents together)
**Trade-off:** Individual doc takes longer, but total throughput higher
**When to prefer:** Throughput for batch jobs, latency for user-facing APIs

#### 59-60. Backpressure
**What it is:** Slow consumer tells fast producer to slow down
**Your implementation:** Queue sizes limit how fast documents fed to Refinory
**Why it matters:** Prevents memory overflow on slow nodes
**Alternative:** Circuit breaker pattern (fail fast when overloaded)

## Applying This Knowledge

### Step 1: Identify Your Patterns
```powershell
./roadmaps/roadmap-b/diagnose-patterns.ps1
# Output: Lists all design patterns detected in your code
```

### Step 2: Fix High-Priority Issues
```powershell
./roadmaps/roadmap-b/apply-fixes.ps1 -Priority High
# Fixes: Missing timeouts, error handling, health checks
```

### Step 3: Document Your Architecture
```powershell
./roadmaps/roadmap-b/document-architecture.ps1
# Generates: Architecture decision records (ADRs) for your patterns
```

## Integration with Roadmap A

- **Roadmap A** gave you clean file structure
- **Roadmap B** explains why that structure prevents circular dependencies
- **Combined:** Fast iteration + architectural safety

## When to Move to Roadmap C

Stay on Roadmap B until you hit:
- Complex multi-service orchestration
- Need for CQRS or event sourcing
- Large team coordination issues
- Compliance requiring formal architecture docs

## Success Metrics

You'll know Roadmap B is working when:
- [ ] You can explain why your architecture makes specific trade-offs
- [ ] New team members understand the reasoning behind code organization
- [ ] You catch architectural problems during design, not production
- [ ] You speak the same language as enterprise architects (when needed)
- [ ] Scaling issues are predictable and preventable

---

**Remember:** This roadmap teaches only what you need to maintain velocity while growing. Not theory for theory's sake. 🚀
