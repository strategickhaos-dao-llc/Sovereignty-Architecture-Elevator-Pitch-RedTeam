# Event Sourcing

**Canon References: #31-35**

## Core Concept

Instead of storing current state, store the sequence of events that led to that state. State is derived by replaying events.

```
Traditional:                Event Sourcing:

State = Current Value       State = f(Events)

┌─────────────┐            ┌──────────────────┐
│ User        │            │ Events           │
│ name: John  │            │ 1. UserCreated   │
│ email: j@   │            │ 2. NameChanged   │
│ status: act │            │ 3. EmailChanged  │
└─────────────┘            │ 4. Activated     │
                           └──────────────────┘
Update overwrites          Events are append-only
```

## Why Event Sourcing?

### 1. Complete Audit Trail
Every change is recorded. You can answer:
- Who changed what, when, and why?
- What was the state at any point in time?
- How did we get to the current state?

### 2. Time Travel
Rebuild state as of any point in time:

```typescript
// Get user state as of 2024-01-01
const events = await eventStore.getEvents('user-123', { before: '2024-01-01' });
const user = events.reduce(applyEvent, emptyUser);
```

### 3. Debugging & Analysis
Reproduce bugs by replaying events:

```typescript
// Reproduce production bug locally
const prodEvents = await fetchProductionEvents('order-456');
const localOrder = replayEvents(prodEvents);
// Now debug with exact production state
```

### 4. New Projections
Add new read models without migrating data:

```typescript
// Decide you need "total spent by user"
// Just replay all purchase events and build new projection
for await (const event of allPurchaseEvents) {
  if (event.type === 'OrderCompleted') {
    userTotals[event.userId] += event.total;
  }
}
```

## Implementation

### Event Structure

```typescript
interface Event {
  id: string;              // Unique event ID
  streamId: string;        // Aggregate ID (e.g., user-123)
  type: string;            // Event type (e.g., UserCreated)
  data: any;               // Event payload
  metadata: {
    timestamp: string;     // When event occurred
    causationId?: string;  // What caused this event
    correlationId: string; // Request trace ID
    userId?: string;       // Who triggered event
  };
  version: number;         // Version in stream (for optimistic locking)
}
```

### Example Events

```typescript
// User aggregate events
const events = [
  {
    id: 'evt-1',
    streamId: 'user-123',
    type: 'UserCreated',
    data: { email: 'john@example.com', name: 'John Doe' },
    metadata: { timestamp: '2024-01-01T10:00:00Z', userId: 'system' },
    version: 1
  },
  {
    id: 'evt-2',
    streamId: 'user-123',
    type: 'EmailVerified',
    data: { verifiedAt: '2024-01-01T10:05:00Z' },
    metadata: { timestamp: '2024-01-01T10:05:00Z', userId: 'user-123' },
    version: 2
  },
  {
    id: 'evt-3',
    streamId: 'user-123',
    type: 'ProfileUpdated',
    data: { name: 'John Smith' },
    metadata: { timestamp: '2024-01-02T14:30:00Z', userId: 'user-123' },
    version: 3
  }
];
```

### Event Store Interface

```typescript
interface EventStore {
  // Append events to a stream
  appendToStream(
    streamId: string,
    events: Event[],
    expectedVersion: number // Optimistic concurrency control
  ): Promise<void>;
  
  // Read events from a stream
  getEvents(
    streamId: string,
    options?: { fromVersion?: number; toVersion?: number }
  ): Promise<Event[]>;
  
  // Read all events (for projections)
  getAllEvents(
    options?: { fromPosition?: number; batchSize?: number }
  ): AsyncIterator<Event>;
}
```

### Aggregate Pattern

```typescript
class User {
  id: string;
  email: string;
  name: string;
  verified: boolean;
  version: number = 0;
  private changes: Event[] = [];
  
  // Factory method from events
  static fromEvents(events: Event[]): User {
    const user = new User();
    events.forEach(event => user.apply(event, false));
    return user;
  }
  
  // Command: Change name
  changeName(newName: string) {
    if (!newName) throw new Error('Name required');
    
    // Create event
    const event = {
      id: generateId(),
      streamId: this.id,
      type: 'NameChanged',
      data: { oldName: this.name, newName },
      metadata: { timestamp: new Date().toISOString() },
      version: this.version + 1
    };
    
    // Apply event locally
    this.apply(event, true);
  }
  
  // Apply event to state
  private apply(event: Event, isNew: boolean) {
    switch (event.type) {
      case 'UserCreated':
        this.id = event.streamId;
        this.email = event.data.email;
        this.name = event.data.name;
        this.verified = false;
        break;
        
      case 'EmailVerified':
        this.verified = true;
        break;
        
      case 'NameChanged':
        this.name = event.data.newName;
        break;
    }
    
    this.version = event.version;
    
    if (isNew) {
      this.changes.push(event);
    }
  }
  
  // Get uncommitted changes
  getUncommittedChanges(): Event[] {
    return this.changes;
  }
  
  // Mark changes as committed
  markChangesAsCommitted() {
    this.changes = [];
  }
}
```

### Repository Pattern

```typescript
class UserRepository {
  constructor(private eventStore: EventStore) {}
  
  async getById(id: string): Promise<User> {
    const events = await this.eventStore.getEvents(id);
    return User.fromEvents(events);
  }
  
  async save(user: User) {
    const changes = user.getUncommittedChanges();
    if (changes.length === 0) return;
    
    await this.eventStore.appendToStream(
      user.id,
      changes,
      user.version - changes.length // Expected version before new events
    );
    
    user.markChangesAsCommitted();
  }
}
```

## CQRS Integration (#32)

Event Sourcing pairs naturally with CQRS (Command Query Responsibility Segregation).

```
Commands (Write)          Events              Queries (Read)
      ↓                     ↓                       ↑
┌──────────┐         ┌──────────┐         ┌──────────────┐
│ Change   │────────→│  Event   │────────→│ Projections  │
│  Name    │         │  Store   │         │              │
└──────────┘         └──────────┘         │ - User List  │
                           │              │ - Analytics  │
                           │              │ - Search     │
                           └─────────────→└──────────────┘
```

**Write Model:** Append events
**Read Model:** Projections optimized for queries

### Projection Example

```typescript
// User list projection (for queries)
class UserListProjection {
  constructor(private db: Database) {}
  
  async handle(event: Event) {
    switch (event.type) {
      case 'UserCreated':
        await this.db.users.insert({
          id: event.streamId,
          email: event.data.email,
          name: event.data.name,
          createdAt: event.metadata.timestamp
        });
        break;
        
      case 'NameChanged':
        await this.db.users.update(
          { id: event.streamId },
          { name: event.data.newName }
        );
        break;
        
      case 'UserDeleted':
        await this.db.users.delete({ id: event.streamId });
        break;
    }
  }
}

// Subscribe to events and update projection
for await (const event of eventStore.getAllEvents()) {
  await userListProjection.handle(event);
}
```

## Patterns & Best Practices

### Snapshots

For long event streams, snapshots avoid replaying thousands of events:

```typescript
interface Snapshot {
  streamId: string;
  state: any;
  version: number;
  timestamp: string;
}

async function loadAggregate(id: string): Promise<User> {
  // Load latest snapshot
  const snapshot = await snapshotStore.getLatest(id);
  
  if (snapshot) {
    // Load events after snapshot
    const events = await eventStore.getEvents(id, {
      fromVersion: snapshot.version + 1
    });
    
    const user = User.fromSnapshot(snapshot);
    events.forEach(event => user.apply(event));
    return user;
  } else {
    // No snapshot, load all events
    const events = await eventStore.getEvents(id);
    return User.fromEvents(events);
  }
}

// Create snapshots periodically
if (user.version % 100 === 0) {
  await snapshotStore.save({
    streamId: user.id,
    state: user.toSnapshot(),
    version: user.version,
    timestamp: new Date().toISOString()
  });
}
```

### Idempotency

Ensure replaying events is safe:

```typescript
// Bad: Not idempotent
function applyMoneyAdded(state: Account, event: MoneyAddedEvent) {
  state.balance += event.amount; // ❌ Replaying adds money again!
}

// Good: Idempotent
function applyMoneyAdded(state: Account, event: MoneyAddedEvent) {
  if (!state.processedEvents.has(event.id)) {
    state.balance += event.amount;
    state.processedEvents.add(event.id);
  }
}

// Even better: Event is the truth
function applyMoneyAdded(state: Account, event: MoneyAddedEvent) {
  // Events say what happened, state is just a cache
  state.balance = calculateBalance(state.allEvents);
}
```

### Versioning Events

Events are forever. Handle schema changes:

```typescript
// V1
interface UserCreatedV1 {
  type: 'UserCreated';
  data: { email: string };
}

// V2: Added name field
interface UserCreatedV2 {
  type: 'UserCreated';
  data: { email: string; name: string };
}

// Upcaster: Convert old events to new format
function upcastUserCreated(event: Event): Event {
  if (event.version === 1) {
    return {
      ...event,
      data: {
        ...event.data,
        name: event.data.email.split('@')[0] // Default name from email
      },
      version: 2
    };
  }
  return event;
}
```

## Trade-offs

### Pros ✅
- Complete audit trail
- Time travel debugging
- Easy to add new projections
- Natural fit for event-driven architectures
- Supports temporal queries

### Cons ❌
- Learning curve
- Eventual consistency (projections lag behind events)
- Event store is append-only (can't delete easily - GDPR challenge)
- Schema evolution complexity
- More infrastructure (event store + projections)

## When to Use Event Sourcing

**Good fit:**
- Financial systems (audit trail critical)
- Collaborative editing (conflict resolution via events)
- Complex domains with many state transitions
- Systems requiring historical analysis

**Bad fit:**
- Simple CRUD applications
- Systems with minimal state changes
- Teams unfamiliar with event-driven design
- Cases where eventual consistency is unacceptable

## Tools & Libraries

- **EventStoreDB**: Purpose-built event store
- **Kafka**: Can be used as event log
- **PostgreSQL**: Can store events in table
- **AWS EventBridge / Azure Event Grid**: Managed event buses

## Related Concepts

- [[CQRS]] - Separating reads from writes
- [[Event_Driven_Architecture]] - Building with events
- [[Domain_Driven_Design]] - Modeling aggregates
- [[Eventual_Consistency]] - Handling projection lag

## Further Reading

- "Implementing Domain-Driven Design" by Vaughn Vernon
- "Versioning in an Event Sourced System" by Greg Young
- "Event Sourcing" by Martin Fowler

---

**Key Takeaway:** Events are facts about what happened. State is derived. With event sourcing, you never lose information and can always reconstruct how you got to the current state.
