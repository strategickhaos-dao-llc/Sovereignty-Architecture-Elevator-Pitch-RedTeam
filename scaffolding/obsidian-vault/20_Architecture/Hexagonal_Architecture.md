# Hexagonal Architecture (Ports & Adapters)

**Canon References: #26-30**

## Overview

Hexagonal Architecture (aka Ports & Adapters) isolates business logic from external concerns. The core application has no knowledge of databases, web frameworks, or external services.

```
             External World
                  ↓↑
         ┌─────────────────┐
         │    Adapters     │  (HTTP, gRPC, CLI)
         └─────────────────┘
                  ↓↑
         ┌─────────────────┐
         │      Ports      │  (Interfaces)
         └─────────────────┘
                  ↓↑
    ┌──────────────────────────┐
    │  Application Core       │  (Business Logic)
    │  - Domain Entities      │
    │  - Use Cases            │
    │  - Business Rules       │
    └──────────────────────────┘
                  ↓↑
         ┌─────────────────┐
         │      Ports      │  (Interfaces)
         └─────────────────┘
                  ↓↑
         ┌─────────────────┐
         │    Adapters     │  (PostgreSQL, Redis, S3)
         └─────────────────┘
             External World
```

## Core Principles

### 1. Dependency Inversion (#29)

**Dependencies point INWARD.** External concerns depend on the core, not vice versa.

**Bad (Traditional Layered Architecture):**
```typescript
// Business logic depends on database
class OrderService {
  constructor(private db: PostgresDatabase) {} // ❌ Coupled to Postgres
  
  async createOrder(order: Order) {
    await this.db.query('INSERT INTO orders...');
  }
}
```

**Good (Hexagonal Architecture):**
```typescript
// Business logic defines interface, database implements it
interface OrderRepository {
  save(order: Order): Promise<void>;
  findById(id: string): Promise<Order>;
}

class OrderService {
  constructor(private repo: OrderRepository) {} // ✅ Depends on abstraction
  
  async createOrder(order: Order) {
    // Validate business rules
    if (order.total < 0) throw new Error('Invalid order');
    
    // Save using port
    await this.repo.save(order);
  }
}

// Adapter implements the port
class PostgresOrderRepository implements OrderRepository {
  async save(order: Order) {
    await db.query('INSERT INTO orders...', order);
  }
  
  async findById(id: string): Promise<Order> {
    const row = await db.query('SELECT * FROM orders WHERE id = $1', [id]);
    return this.mapRowToOrder(row);
  }
}
```

### 2. Testability

Core logic can be tested without external dependencies:

```typescript
describe('OrderService', () => {
  it('should validate order total', async () => {
    const mockRepo: OrderRepository = {
      save: jest.fn(),
      findById: jest.fn()
    };
    
    const service = new OrderService(mockRepo);
    
    await expect(
      service.createOrder({ total: -100 })
    ).rejects.toThrow('Invalid order');
    
    expect(mockRepo.save).not.toHaveBeenCalled();
  });
});
```

### 3. Swappable Adapters

Change databases without touching business logic:

```typescript
// Development: Use in-memory
const devRepo = new InMemoryOrderRepository();
const devService = new OrderService(devRepo);

// Production: Use Postgres
const prodRepo = new PostgresOrderRepository(dbConnection);
const prodService = new OrderService(prodRepo);

// Testing: Use mock
const testRepo = new MockOrderRepository();
const testService = new OrderService(testRepo);
```

## Ports

**Ports are interfaces.** They define contracts without implementation.

### Primary (Driving) Ports

External actors → Application core

```typescript
// HTTP adapter drives the application
interface OrderUseCases {
  placeOrder(customerId: string, items: Item[]): Promise<OrderResult>;
  cancelOrder(orderId: string): Promise<void>;
  getOrderStatus(orderId: string): Promise<OrderStatus>;
}

class OrderService implements OrderUseCases {
  // Implementation of business logic
}
```

### Secondary (Driven) Ports

Application core → External systems

```typescript
// Application defines what it needs
interface PaymentGateway {
  charge(amount: number, token: string): Promise<PaymentResult>;
  refund(transactionId: string): Promise<void>;
}

interface NotificationService {
  sendEmail(to: string, subject: string, body: string): Promise<void>;
  sendSMS(phone: string, message: string): Promise<void>;
}
```

## Adapters

**Adapters implement ports.** They translate between external world and application core.

### Primary Adapters (Input)

```typescript
// HTTP Adapter
class OrderController {
  constructor(private orderService: OrderUseCases) {}
  
  async placeOrder(req: Request, res: Response) {
    try {
      const { customerId, items } = req.body;
      const result = await this.orderService.placeOrder(customerId, items);
      res.json(result);
    } catch (err) {
      res.status(400).json({ error: err.message });
    }
  }
}

// CLI Adapter
class OrderCLI {
  constructor(private orderService: OrderUseCases) {}
  
  async run(args: string[]) {
    const [command, ...params] = args;
    
    if (command === 'place') {
      const result = await this.orderService.placeOrder(params[0], JSON.parse(params[1]));
      console.log('Order placed:', result);
    }
  }
}

// gRPC Adapter
class OrderGrpcService {
  constructor(private orderService: OrderUseCases) {}
  
  async PlaceOrder(call, callback) {
    const { customerId, items } = call.request;
    const result = await this.orderService.placeOrder(customerId, items);
    callback(null, result);
  }
}
```

### Secondary Adapters (Output)

```typescript
// Stripe Payment Adapter
class StripePaymentGateway implements PaymentGateway {
  async charge(amount: number, token: string): Promise<PaymentResult> {
    const stripe = require('stripe')(process.env.STRIPE_KEY);
    const charge = await stripe.charges.create({
      amount: amount * 100, // Stripe uses cents
      currency: 'usd',
      source: token
    });
    
    return {
      transactionId: charge.id,
      success: charge.status === 'succeeded'
    };
  }
}

// SendGrid Email Adapter
class SendGridNotificationService implements NotificationService {
  async sendEmail(to: string, subject: string, body: string) {
    const sgMail = require('@sendgrid/mail');
    sgMail.setApiKey(process.env.SENDGRID_KEY);
    
    await sgMail.send({ to, from: 'orders@example.com', subject, text: body });
  }
}
```

## Folder Structure

```
src/
├── core/                    # Application Core (no dependencies!)
│   ├── domain/
│   │   ├── Order.ts         # Domain entities
│   │   ├── Customer.ts
│   │   └── Item.ts
│   ├── usecases/
│   │   ├── PlaceOrder.ts    # Business logic
│   │   ├── CancelOrder.ts
│   │   └── GetOrderStatus.ts
│   └── ports/
│       ├── OrderRepository.ts      # Secondary port
│       ├── PaymentGateway.ts       # Secondary port
│       └── NotificationService.ts  # Secondary port
│
├── adapters/
│   ├── primary/             # Input adapters
│   │   ├── http/
│   │   │   └── OrderController.ts
│   │   ├── grpc/
│   │   │   └── OrderGrpcService.ts
│   │   └── cli/
│   │       └── OrderCLI.ts
│   └── secondary/           # Output adapters
│       ├── postgres/
│       │   └── PostgresOrderRepository.ts
│       ├── stripe/
│       │   └── StripePaymentGateway.ts
│       └── sendgrid/
│           └── SendGridNotificationService.ts
│
└── main.ts                  # Dependency injection / wiring
```

## Dependency Injection (Wiring)

```typescript
// main.ts - Composition Root
async function main() {
  // Create secondary adapters (infrastructure)
  const dbConnection = await createDatabaseConnection();
  const orderRepo = new PostgresOrderRepository(dbConnection);
  const paymentGateway = new StripePaymentGateway();
  const notificationService = new SendGridNotificationService();
  
  // Create use cases (business logic)
  const orderService = new OrderService(
    orderRepo,
    paymentGateway,
    notificationService
  );
  
  // Create primary adapters (interfaces)
  const httpController = new OrderController(orderService);
  const grpcService = new OrderGrpcService(orderService);
  
  // Start servers
  startHttpServer(httpController);
  startGrpcServer(grpcService);
}
```

## Benefits

✅ **Testable:** Core logic tested without databases or APIs
✅ **Flexible:** Swap implementations (SQL → NoSQL, HTTP → gRPC)
✅ **Maintainable:** Clear separation of concerns
✅ **Portable:** Core logic can move to different frameworks
✅ **Independent:** Develop core logic before deciding on infrastructure

## Common Pitfalls

❌ **Leaky Abstractions:** Port exposes database-specific concepts
```typescript
// Bad: Exposing SQL in port
interface OrderRepository {
  query(sql: string): Promise<Row[]>; // ❌
}

// Good: Domain-centric interface
interface OrderRepository {
  save(order: Order): Promise<void>; // ✅
}
```

❌ **Anemic Domain Model:** All logic in adapters, entities are just data
```typescript
// Bad: No business logic in domain
class Order {
  id: string;
  total: number;
}

// Good: Rich domain model
class Order {
  id: string;
  private items: Item[];
  
  addItem(item: Item) {
    // Business rules here
    if (this.items.length >= 100) throw new Error('Too many items');
    this.items.push(item);
  }
  
  get total(): number {
    return this.items.reduce((sum, item) => sum + item.price, 0);
  }
}
```

## Application to Sovereignty Architecture

**Heir Evolution System:**
```
Core:
- Heir domain model
- Evolution algorithms
- Prompt generation logic

Adapters:
- Input: HTTP API, CLI, Message Queue
- Output: PostgreSQL (heir state), S3 (training data), OpenAI (inference)
```

**Benefit:** Swap OpenAI for local LLM without changing core logic!

## Related Concepts

- [[Clean_Architecture]] - Similar principles, different presentation
- [[Domain_Driven_Design]] - Focus on rich domain models
- [[Dependency_Injection]] - How to wire components
- [[Testing_Strategies]] - Leveraging hexagonal for better tests

## Further Reading

- "Hexagonal Architecture" by Alistair Cockburn
- "Clean Architecture" by Robert C. Martin
- "Growing Object-Oriented Software, Guided by Tests" by Freeman & Pryce

---

**Key Takeaway:** Protect your business logic from the chaos of the external world. Build a clean core, wrap it with adapters. Your future self will thank you when switching databases, frameworks, or APIs.
