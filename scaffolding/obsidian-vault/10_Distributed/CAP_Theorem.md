# CAP Theorem

**Canon References: #11-15**

## The Fundamental Trade-off

**CAP Theorem states:** In the presence of a network partition (P), a distributed system must choose between Consistency (C) and Availability (A). You can only guarantee two of the three properties.

```
        Consistency (C)
              ╱  ╲
             ╱    ╲
            ╱  CA  ╲
           ╱ (No    ╲
          ╱ Partition)╲
         ╱____________╲
        CP            AP
   Consistent    Available
  Partition-     Partition-
   tolerant       tolerant
```

### Definitions

**Consistency (C):** Every read receives the most recent write or an error. All nodes see the same data at the same time.

**Availability (A):** Every request receives a (non-error) response, without guarantee that it contains the most recent write.

**Partition Tolerance (P):** The system continues to operate despite arbitrary message loss or failure of part of the system.

## Reality Check

**Network partitions WILL happen.** Cables get unplugged, switches fail, cloud zones go down. Therefore, you're really choosing between CP and AP.

## CP Systems (#13)

**Choose CP when:** Correctness is more important than availability.

### Examples: etcd, ZooKeeper, Consul

**Behavior during partition:**
- Nodes that can't reach quorum refuse writes
- System may become unavailable
- But data stays consistent

**Use Cases:**
- Distributed locks
- Leader election
- Configuration management
- Service discovery

**Code Example:**
```go
// etcd: Strong consistency, may fail if quorum lost
resp, err := client.Put(ctx, "/config/db_connection", "new-value")
if err != nil {
    // If network partition: error returned
    // But if it succeeds, ALL nodes will see this value
    return err
}
```

### Trade-offs
✅ Data is always correct
✅ No conflict resolution needed
❌ May be unavailable during partition
❌ Higher latency (quorum required)

## AP Systems (#12)

**Choose AP when:** Availability is more important than immediate consistency.

### Examples: Cassandra, DynamoDB, Riak

**Behavior during partition:**
- All nodes continue accepting writes
- Data may diverge temporarily
- Eventually consistent

**Use Cases:**
- Shopping carts
- Social media feeds
- Sensor data collection
- Analytics logs

**Code Example:**
```javascript
// DynamoDB: Eventually consistent reads
const params = {
  TableName: 'Users',
  Key: { userId: '123' },
  ConsistentRead: false // AP: may return stale data
};

const result = await dynamodb.get(params);
// Result might be slightly out of date, but you WILL get a response
```

### Trade-offs
✅ Always available
✅ Lower latency (local writes)
❌ Stale reads possible
❌ Conflict resolution required

## BASE vs ACID (#14)

### ACID (CP Systems)
- **Atomicity:** All or nothing
- **Consistency:** Valid state only
- **Isolation:** Concurrent transactions don't interfere
- **Durability:** Committed = permanent

### BASE (AP Systems)
- **Basically Available:** System appears to work most of time
- **Soft state:** State may change without input (due to eventual consistency)
- **Eventually consistent:** Given enough time, all nodes converge

## Quorum Protocols (#15)

Tunable consistency - the middle ground!

### N, R, W Parameters

- **N:** Total replicas
- **R:** Read quorum (must read from R replicas)
- **W:** Write quorum (must write to W replicas)

**Rule:** If R + W > N, you get consistency

### Examples with N=3

#### Strong Consistency (CP-like)
```
W=2, R=2 (W+R=4 > N=3)
- Write to majority
- Read from majority
- Guaranteed to see latest write
```

#### Eventual Consistency (AP-like)
```
W=1, R=1 (W+R=2 < N=3)
- Write to any node
- Read from any node
- Fast but may read stale data
```

#### Balanced
```
W=2, R=1 (W+R=3 = N)
- Durable writes (majority)
- Fast reads (any node)
- May see stale data briefly
```

### Code Example: Cassandra
```cql
-- Strong consistency for critical data
SELECT * FROM accounts WHERE user_id = 123
  USING CONSISTENCY QUORUM; -- R=2 for N=3

-- Eventual consistency for metrics
SELECT * FROM page_views WHERE date = '2024-01-01'
  USING CONSISTENCY ONE; -- R=1 for N=3
```

## Practical Decision Tree

```
Is correctness absolutely critical?
├─ YES: Use CP system (etcd, ZooKeeper)
│   └─ Accept potential downtime during partitions
│
└─ NO: Can you tolerate brief inconsistency?
    ├─ YES: Use AP system (Cassandra, DynamoDB)
    │   └─ Implement conflict resolution (LWW, CRDTs)
    │
    └─ NO: Need both?
        └─ Use quorum with R+W>N
            └─ Tune per operation (strong for writes, fast for reads)
```

## Real-World Patterns

### Pattern 1: Event Sourcing (AP with Eventual Consistency)
```
Write: Append event to log (always succeeds, AP)
Read: Rebuild state from events (eventually consistent)
```

### Pattern 2: Read-Your-Own-Writes
```
Write: Record to CP system, return write timestamp
Read: If client timestamp > replica timestamp, wait/retry
```

### Pattern 3: Saga Pattern for Distributed Transactions
```
Instead of 2PC (blocking, CP):
- Local transaction per service (AP)
- Compensating transactions on failure
- Eventually consistent
```

## Common Misconceptions

**❌ "CP means 100% available"**
→ No, CP may sacrifice availability during partitions

**❌ "AP means no consistency guarantees"**
→ No, AP means *eventual* consistency, not *no* consistency

**❌ "You choose CAP once per system"**
→ No, different parts can make different choices (CP for auth, AP for metrics)

**❌ "Network partitions are rare"**
→ No, they happen regularly (datacenter splits, cloud zone failures, cable cuts)

## Testing CAP Behavior

### Chaos Test: Simulate Partition
```bash
# Block network between nodes
iptables -A INPUT -s 10.0.2.0/24 -j DROP
iptables -A OUTPUT -d 10.0.2.0/24 -j DROP

# CP system: Should refuse writes
# AP system: Should accept writes

# Heal partition
iptables -F

# CP system: Immediately consistent
# AP system: Watch convergence
```

## Choosing for Sovereignty Architecture

**For Heir Evolution System:**
- **Config/Schema:** CP (etcd) - correctness critical
- **Training Data:** AP (S3-compatible) - availability critical
- **Execution Logs:** AP (time-series DB) - high volume, eventual consistency OK
- **Prompt Templates:** CP (Git + etcd) - consistency matters

## Related Concepts

- [[Consensus_Algorithms]] - How CP systems achieve consistency
- [[Eventual_Consistency]] - Deep dive on AP convergence
- [[Network_Partitions]] - Understanding and handling partitions
- [[Distributed_Transactions]] - Alternatives to 2PC

## Further Reading

- "Designing Data-Intensive Applications" by Martin Kleppmann (Chapter 9)
- Brewer's CAP theorem paper (2000)
- "Eventually Consistent" by Werner Vogels
- Jepsen tests for real-world CAP analysis

---

**Key Takeaway:** CAP is not a choice. It's a constraint. Design your system to explicitly handle network partitions, then choose C or A based on business requirements.
