# Network Fallacies of Distributed Computing

**Canon Reference: #16**

## The Eight Fallacies

L. Peter Deutsch and others at Sun Microsystems identified eight assumptions that developers often make about networks—all of them false.

### 1. The Network Is Reliable

**Reality:** Networks drop packets, cables fail, switches crash, cosmic rays flip bits.

**Impact:**
- Lost requests
- Partial data transmission
- Silent failures

**Mitigation:**
```typescript
// Implement retries with exponential backoff
async function reliableRequest(url: string, maxRetries = 3): Promise<Response> {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      const response = await fetch(url, { timeout: 5000 });
      return response;
    } catch (err) {
      if (attempt === maxRetries - 1) throw err;
      
      const backoff = Math.pow(2, attempt) * 1000; // 1s, 2s, 4s
      await sleep(backoff);
      logger.warn('request_retry', { url, attempt, backoff });
    }
  }
}
```

### 2. Latency Is Zero

**Reality:** Network calls are 1000× slower than in-process calls.

**Latency Numbers:**
- L1 cache: 0.5 ns
- RAM: 100 ns
- SSD read: 150 μs
- Network within datacenter: 0.5 ms
- Cross-datacenter (same region): 5-10 ms
- Cross-region: 50-200 ms

**Impact:**
- Chatty APIs kill performance
- N+1 query problems
- Sequential calls compound latency

**Mitigation:**
```typescript
// Bad: N+1 queries (11 network calls for 10 users)
async function getOrdersWithUsers(orderIds: string[]) {
  const orders = await db.orders.findMany({ id: { in: orderIds } });
  for (const order of orders) {
    order.user = await db.users.findOne({ id: order.userId }); // ❌ N calls
  }
  return orders;
}

// Good: Batch loading (2 network calls total)
async function getOrdersWithUsers(orderIds: string[]) {
  const orders = await db.orders.findMany({ id: { in: orderIds } });
  const userIds = orders.map(o => o.userId);
  const users = await db.users.findMany({ id: { in: userIds } }); // ✅ 1 call
  
  const userMap = new Map(users.map(u => [u.id, u]));
  orders.forEach(o => o.user = userMap.get(o.userId));
  return orders;
}
```

### 3. Bandwidth Is Infinite

**Reality:** Networks have limited throughput, especially on mobile or remote connections.

**Impact:**
- Large payloads slow down requests
- Multiple concurrent requests saturate bandwidth
- Mobile users suffer

**Mitigation:**
```typescript
// Paginate large responses
app.get('/api/orders', async (req, res) => {
  const page = parseInt(req.query.page) || 1;
  const limit = Math.min(parseInt(req.query.limit) || 20, 100); // Max 100
  
  const orders = await db.orders.findMany({
    skip: (page - 1) * limit,
    take: limit
  });
  
  res.json({
    data: orders,
    pagination: {
      page,
      limit,
      hasNext: orders.length === limit
    }
  });
});

// Compress responses
app.use(compression());

// Use appropriate data formats (Protobuf < JSON < XML)
```

### 4. The Network Is Secure

**Reality:** Networks are hostile environments full of attackers.

**Impact:**
- Man-in-the-middle attacks
- Eavesdropping on sensitive data
- Injection attacks

**Mitigation:**
- TLS everywhere (Canon #77)
- Never trust client input
- Verify cryptographic signatures
- Zero trust architecture (Canon #66-70)

```typescript
// Always use HTTPS
const server = https.createServer({
  key: fs.readFileSync('private-key.pem'),
  cert: fs.readFileSync('certificate.pem')
}, app);

// Validate and sanitize all inputs
app.post('/api/orders', async (req, res) => {
  const schema = z.object({
    userId: z.string().uuid(),
    total: z.number().positive().max(1000000)
  });
  
  const validated = schema.parse(req.body); // Throws if invalid
  // ... process order
});
```

### 5. Topology Doesn't Change

**Reality:** Servers come and go, IPs change, routes shift, load balancers rebalance.

**Impact:**
- Hardcoded IPs break
- DNS changes take time to propagate
- Connection pools become stale

**Mitigation:**
```typescript
// Use service discovery instead of hardcoded IPs
const serviceUrl = await consul.getService('payment-api');

// DNS with short TTL
const response = await fetch('https://api.example.com/payments');

// Health checks and circuit breakers
class ServiceClient {
  private isHealthy = true;
  private failureCount = 0;
  
  async call(endpoint: string) {
    if (!this.isHealthy) {
      throw new Error('Circuit breaker open');
    }
    
    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`);
      this.failureCount = 0;
      return response;
    } catch (err) {
      this.failureCount++;
      if (this.failureCount > 5) {
        this.isHealthy = false;
        setTimeout(() => this.isHealthy = true, 30000); // Retry after 30s
      }
      throw err;
    }
  }
}
```

### 6. There Is One Administrator

**Reality:** Multiple teams manage different parts of the infrastructure.

**Impact:**
- Coordination challenges
- Inconsistent configurations
- Different maintenance windows
- Communication failures

**Mitigation:**
- Infrastructure as Code (everyone sees config)
- Automated deployments (no manual coordination)
- Service Level Agreements between teams
- Clear ownership (RACI matrix)

```yaml
# Declare dependencies in code
services:
  order-api:
    depends_on:
      - postgres
      - redis
      - payment-service
    environment:
      PAYMENT_API_URL: http://payment-service:8080
```

### 7. Transport Cost Is Zero

**Reality:** Serialization, deserialization, and network transfer consume CPU and time.

**Impact:**
- JSON parsing overhead
- Compression CPU cost
- Memory allocation for buffers
- Network card interrupts

**Mitigation:**
```typescript
// Use efficient serialization (Protobuf, MessagePack)
import * as protobuf from 'protobufjs';

// Pool connections to avoid setup/teardown cost
const pool = new Pool({
  host: 'localhost',
  database: 'mydb',
  max: 20, // Reuse connections
  idleTimeoutMillis: 30000
});

// Cache frequently accessed data
const cache = new LRU({ max: 1000 });
async function getUser(id: string) {
  const cached = cache.get(id);
  if (cached) return cached;
  
  const user = await db.users.findOne({ id });
  cache.set(id, user);
  return user;
}
```

### 8. The Network Is Homogeneous

**Reality:** Mix of vendors, protocols, versions, operating systems.

**Impact:**
- Different MTU sizes fragment packets
- IPv4 vs IPv6 incompatibilities
- Firewall rules vary
- Protocol version mismatches

**Mitigation:**
```typescript
// Use standard protocols (HTTP, gRPC)
// Version your APIs
app.get('/v1/orders', handleOrdersV1);
app.get('/v2/orders', handleOrdersV2); // New version, backward compatible

// Content negotiation
app.get('/api/orders', (req, res) => {
  const format = req.accepts(['json', 'xml', 'protobuf']);
  
  switch (format) {
    case 'json':
      res.json(orders);
      break;
    case 'xml':
      res.type('xml').send(toXML(orders));
      break;
    case 'protobuf':
      res.type('application/protobuf').send(toProtobuf(orders));
      break;
  }
});
```

## Designing for Fallacies

### Checklist for Every Network Call

✅ **Reliability:** Can this fail? What happens if it does?
✅ **Latency:** How long might this take? What if it's slow?
✅ **Bandwidth:** How much data am I sending? Can I send less?
✅ **Security:** Is this encrypted? Authenticated?
✅ **Topology:** What if the endpoint moves?
✅ **Administration:** Who manages this dependency?
✅ **Cost:** Is the serialization/transport overhead acceptable?
✅ **Homogeneity:** Will this work across different systems?

### Pattern: Resilient Service Calls

```typescript
class ResilientClient {
  constructor(
    private baseUrl: string,
    private options = {
      timeout: 5000,
      retries: 3,
      circuitBreaker: true,
      cache: true
    }
  ) {}
  
  async call<T>(endpoint: string): Promise<T> {
    // 1. Check cache (Fallacy #2: Latency)
    if (this.options.cache) {
      const cached = cache.get(endpoint);
      if (cached) return cached;
    }
    
    // 2. Circuit breaker (Fallacy #5: Topology changes)
    if (this.options.circuitBreaker && !this.isHealthy) {
      throw new Error('Circuit breaker open');
    }
    
    // 3. Retry with backoff (Fallacy #1: Reliability)
    let lastError: Error;
    for (let attempt = 0; attempt < this.options.retries; attempt++) {
      try {
        const response = await fetch(`${this.baseUrl}${endpoint}`, {
          timeout: this.options.timeout, // Fallacy #2: Latency
          headers: {
            'Authorization': `Bearer ${this.token}`, // Fallacy #4: Security
            'Accept': 'application/json', // Fallacy #8: Homogeneity
            'Accept-Encoding': 'gzip' // Fallacy #3: Bandwidth
          }
        });
        
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }
        
        const data = await response.json();
        
        // Cache success (Fallacy #7: Transport cost)
        if (this.options.cache) {
          cache.set(endpoint, data, 60000); // 1 minute TTL
        }
        
        return data;
      } catch (err) {
        lastError = err;
        const backoff = Math.pow(2, attempt) * 1000;
        await sleep(backoff);
      }
    }
    
    // All retries failed
    this.recordFailure();
    throw lastError;
  }
  
  private recordFailure() {
    this.failureCount++;
    if (this.failureCount > 5) {
      this.isHealthy = false;
      setTimeout(() => {
        this.isHealthy = true;
        this.failureCount = 0;
      }, 30000);
    }
  }
}
```

## Related Concepts

- [[CAP_Theorem]] - Network partitions are inevitable
- [[Latency_Numbers]] - Understanding performance costs
- [[Circuit_Breaker]] - Handling unreliable networks
- [[Chaos_Engineering]] - Testing network failures

## Further Reading

- "Fallacies of Distributed Computing Explained" by Arnon Rotem-Gal-Oz
- "Release It!" by Michael Nygard
- "Designing Data-Intensive Applications" by Martin Kleppmann

---

**Key Takeaway:** Networks are unreliable, slow, insecure, and constantly changing. Design for failure, not for the happy path. Every network call is a potential failure point—handle it gracefully.
