# Observability

**Canon References: #46-50, #9**

## The Three Pillars (Plus One)

Observability is not monitoring. Monitoring tells you when something is broken. Observability lets you understand *why* it's broken, even for issues you've never seen before.

```
Traditional Monitoring:        Observability:
"CPU is at 95%"               "Why is CPU at 95%?"
                              → Trace slow requests
                              → Find N+1 queries in logs
                              → See cache miss rate metrics
                              → Fix root cause
```

### 1. Logs - The "What Happened"

**Structured logs** with consistent schema and correlation IDs.

**Bad Logging:**
```javascript
console.log('User logged in');
console.log('Failed to save order');
```

**Good Logging:**
```javascript
logger.info('user_logged_in', {
  userId: '12345',
  ip: '192.168.1.100',
  traceId: 'abc-def-123',
  timestamp: '2024-01-15T10:30:00Z'
});

logger.error('order_save_failed', {
  orderId: 'ord-789',
  userId: '12345',
  error: 'database_connection_timeout',
  databaseHost: 'db-primary.local',
  attemptNumber: 3,
  traceId: 'abc-def-123',
  timestamp: '2024-01-15T10:30:05Z'
});
```

**Key Elements:**
- Structured format (JSON)
- Correlation IDs (traceId) to follow requests across services
- Context (userId, orderId, etc.)
- Consistent timestamps
- Severity levels (debug, info, warn, error)

### 2. Metrics - The "How Much/How Fast"

Time-series data for aggregation and trending.

#### RED Metrics (#48) - For Request-Driven Services
- **Rate:** Requests per second
- **Errors:** Error rate (percentage)
- **Duration:** Response time (p50, p95, p99)

**Implementation:**
```typescript
import { Histogram, Counter } from 'prom-client';

const requestDuration = new Histogram({
  name: 'http_request_duration_seconds',
  help: 'HTTP request latency in seconds',
  labelNames: ['method', 'route', 'status_code']
});

const requestCounter = new Counter({
  name: 'http_requests_total',
  help: 'Total HTTP requests',
  labelNames: ['method', 'route', 'status_code']
});

app.use((req, res, next) => {
  const start = Date.now();
  
  res.on('finish', () => {
    const duration = (Date.now() - start) / 1000;
    requestDuration.observe(
      { method: req.method, route: req.route.path, status_code: res.statusCode },
      duration
    );
    requestCounter.inc({ method: req.method, route: req.route.path, status_code: res.statusCode });
  });
  
  next();
});
```

#### USE Metrics (#49) - For Resource Monitoring
- **Utilization:** % time resource is busy
- **Saturation:** Queue depth, waiting work
- **Errors:** Error count

**Example:**
```
# CPU
node_cpu_utilization_percent{cpu="0"} 45
node_cpu_saturation_load_average{period="1m"} 2.5

# Memory
node_memory_utilization_percent 72
node_memory_saturation_swap_used_bytes 104857600

# Disk
node_disk_utilization_percent{device="sda1"} 68
node_disk_saturation_queue_length{device="sda1"} 3
```

### 3. Traces - The "Where It Went"

Distributed request flow across services.

**OpenTelemetry Example:**
```typescript
import { trace } from '@opentelemetry/api';

async function processOrder(orderId: string) {
  const tracer = trace.getTracer('order-service');
  
  // Create parent span
  return tracer.startActiveSpan('process_order', async (span) => {
    span.setAttribute('order.id', orderId);
    
    try {
      // Child span for database
      await tracer.startActiveSpan('db.load_order', async (dbSpan) => {
        const order = await db.orders.findById(orderId);
        dbSpan.setAttribute('db.rows_returned', 1);
        dbSpan.end();
        return order;
      });
      
      // Child span for payment
      await tracer.startActiveSpan('payment.charge', async (paySpan) => {
        const result = await paymentService.charge(order.total);
        paySpan.setAttribute('payment.amount', order.total);
        paySpan.setAttribute('payment.status', result.status);
        paySpan.end();
        return result;
      });
      
      span.setStatus({ code: 1 }); // OK
      return { success: true };
    } catch (err) {
      span.recordException(err);
      span.setStatus({ code: 2, message: err.message }); // ERROR
      throw err;
    } finally {
      span.end();
    }
  });
}
```

**Trace Visualization:**
```
process_order (200ms)
├─ db.load_order (50ms)
├─ payment.charge (120ms)
│  ├─ http.post /api/charge (100ms)
│  └─ db.save_transaction (15ms)
└─ notification.send (25ms)
```

### 4. Events - The "State Changes"

Significant occurrences that don't fit neatly into logs/metrics/traces.

**Examples:**
- Deployment started/completed
- Configuration changed
- Auto-scaling triggered
- Circuit breaker opened/closed
- Chaos test initiated

**Event Structure:**
```json
{
  "eventType": "deployment_completed",
  "timestamp": "2024-01-15T10:30:00Z",
  "environment": "production",
  "service": "order-api",
  "version": "v2.5.0",
  "deployedBy": "john@example.com",
  "metadata": {
    "previousVersion": "v2.4.1",
    "rolloutStrategy": "canary",
    "affectedInstances": 50
  }
}
```

## Practical Implementation

### Instrumentation Checklist

✅ Every HTTP endpoint
✅ Every database query
✅ Every external API call
✅ Every background job
✅ Every cache access
✅ Every queue operation
✅ Every significant state change

### Example: Complete Observability

```typescript
// Complete instrumentation for a single function
async function createUser(userData: UserData) {
  const span = tracer.startSpan('create_user');
  const timer = metrics.histogram('user_creation_duration');
  const logger = structlog.bind({ operation: 'create_user', traceId: span.context().traceId });
  
  logger.info('user_creation_started', { email: userData.email });
  
  try {
    // Validate
    span.addEvent('validation_started');
    const validation = await validateUserData(userData);
    if (!validation.valid) {
      logger.warn('user_validation_failed', { errors: validation.errors });
      metrics.counter('user_creation_failures').inc({ reason: 'validation' });
      throw new ValidationError(validation.errors);
    }
    
    // Save to database
    span.addEvent('database_save_started');
    const dbStart = Date.now();
    const user = await db.users.create(userData);
    metrics.histogram('database_query_duration').observe(Date.now() - dbStart);
    logger.info('user_saved_to_database', { userId: user.id });
    
    // Send welcome email
    span.addEvent('email_send_started');
    await emailService.sendWelcome(user.email);
    logger.info('welcome_email_sent', { userId: user.id });
    
    // Success metrics
    metrics.counter('user_creation_success').inc();
    logger.info('user_creation_completed', { userId: user.id });
    
    return user;
  } catch (err) {
    logger.error('user_creation_failed', { 
      error: err.message, 
      stack: err.stack 
    });
    span.recordException(err);
    metrics.counter('user_creation_failures').inc({ reason: err.constructor.name });
    throw err;
  } finally {
    timer.observe();
    span.end();
  }
}
```

## Query and Visualization

### Logs (Loki/Elasticsearch)
```
# Find all errors for a specific user
{service="order-api"} | json | userId="12345" | level="error"

# Trace a specific request
{service=~"order-api|payment-api"} | json | traceId="abc-def-123"
```

### Metrics (PromQL)
```
# Request rate by status code
rate(http_requests_total[5m])

# 95th percentile latency
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# Error rate percentage
(rate(http_requests_total{status_code=~"5.."}[5m]) / 
 rate(http_requests_total[5m])) * 100
```

### Traces (Jaeger)
- Search by service, operation, tags
- Find slow traces (>1s)
- Compare traces before/after deploy
- Identify bottleneck services

## Alerting

**SLO-Based Alerts (Canon #51-52):**

```yaml
# Error budget alert
- alert: ErrorBudgetBurning
  expr: |
    (1 - (
      sum(rate(http_requests_total{status_code!~"5.."}[1h]))
      /
      sum(rate(http_requests_total[1h]))
    )) > 0.001  # 99.9% SLO, so error rate > 0.1%
  for: 5m
  annotations:
    summary: "Error budget burning too fast"
    description: "Error rate is {{ $value | humanizePercentage }}, exceeding 0.1% threshold"
```

**Resource Alerts:**
```yaml
- alert: HighMemoryUsage
  expr: node_memory_utilization_percent > 90
  for: 10m
  
- alert: DiskFillingUp
  expr: predict_linear(node_disk_used_bytes[6h], 4*3600) > node_disk_total_bytes
  annotations:
    summary: "Disk will be full in 4 hours at current rate"
```

## Observability for AI Systems

**Heir-Specific Metrics:**
```typescript
// Heir execution metrics
heirMetrics.histogram('heir_prompt_tokens', tokens);
heirMetrics.histogram('heir_completion_tokens', completionTokens);
heirMetrics.histogram('heir_latency_seconds', duration);
heirMetrics.counter('heir_tool_invocations', { tool: 'database_query' });
heirMetrics.counter('heir_errors', { errorType: 'rate_limit' });

// Evolution tracking
heirMetrics.gauge('heir_dna_version', version);
heirMetrics.counter('heir_evolutions_total', { result: 'success' });
```

**Heir Traces:**
```
heir_execute (5.2s)
├─ prompt_generation (0.2s)
├─ llm_call (4.5s)
│  └─ api_request /v1/chat/completions (4.5s)
├─ tool_database_query (0.3s)
└─ response_formatting (0.2s)
```

## Related Concepts

- [[SRE_Practices]] - Using observability for reliability
- [[Chaos_Engineering]] - Observing system behavior under failure
- [[Performance_Engineering]] - Using metrics to optimize
- [[Incident_Response]] - Observability during outages

## Further Reading

- "Observability Engineering" by Charity Majors et al.
- "Distributed Tracing in Practice" by Austin Parker et al.
- OpenTelemetry documentation
- Google SRE Book: Chapter 6 (Monitoring Distributed Systems)

---

**Key Takeaway:** If you can't observe it, you can't debug it. Instrument everything, correlate across pillars, and build systems that explain themselves.
