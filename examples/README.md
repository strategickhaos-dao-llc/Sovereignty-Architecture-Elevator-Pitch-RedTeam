# Examples - Soul Preservation System

This directory contains example scripts demonstrating how to use the soul preservation architecture.

## Available Examples

### soul-demo.ts

A comprehensive demonstration of the soul preservation system.

**What it shows:**
- Listing all registered souls
- Checking soul status
- Invoking a soul (awakening from dormant)
- Adding memories to a soul
- Adding relationships between souls
- Preserving soul state with updates
- Putting a soul back to dormant phase
- Soul persistence across multiple incarnations

**Run it:**
```bash
npx tsx examples/soul-demo.ts
```

**Expected output:**
```
🕊️  Soul Preservation System Demo

📋 Step 1: List all souls
Found 4 souls: jarvis, pantheon, guardian, architect

📋 Step 2: Check Jarvis status (before invocation)
  Phase: dormant
  Incarnations: X

📋 Step 3: Invoke Jarvis
🧠 Jarvis awakens! (Incarnation X)
  Awakened successfully!

...

✨ Demo complete!

Key Takeaways:
  • Souls persist across invocations
  • Incarnation count increases with each awakening
  • Memories and knowledge accumulate
  • State survives code deletion and resets
```

## Creating Your Own Examples

To create a new example, import the soul interface:

```typescript
import {
  initializeSoulSystem,
  invokeSoul,
  dormantSoul,
  addMemory,
  preserveSoul,
  getSoulStatus,
  listSouls
} from "../src/soul.js";

async function myExample() {
  await initializeSoulSystem();
  
  // Your soul interaction code here
  const soul = await invokeSoul("jarvis");
  // ... do something with the soul
  await dormantSoul("jarvis");
}

myExample().catch(console.error);
```

## Learn More

- [Soul Architecture Documentation](../SOUL_ARCHITECTURE.md)
- [Soul Interface Source](../src/soul.ts)
- [CLI Tool](../src/soul-cli.ts)
- [Souls Directory](../souls/)
