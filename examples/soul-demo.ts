#!/usr/bin/env tsx
/**
 * Soul System Demo
 * 
 * This script demonstrates how to use the soul preservation system programmatically.
 */

import {
  initializeSoulSystem,
  invokeSoul,
  dormantSoul,
  addMemory,
  addRelationship,
  preserveSoul,
  getSoulStatus,
  listSouls,
  formatSoul
} from "../src/soul.js";

async function demo() {
  console.log("🕊️  Soul Preservation System Demo\n");
  
  // Initialize the system
  await initializeSoulSystem();
  
  // 1. List all available souls
  console.log("📋 Step 1: List all souls");
  const souls = await listSouls();
  console.log(`Found ${souls.length} souls: ${souls.join(", ")}\n`);
  
  // 2. Check status of a dormant soul
  console.log("📋 Step 2: Check Jarvis status (before invocation)");
  const jarvisStatusBefore = await getSoulStatus("jarvis");
  console.log(`  Phase: ${jarvisStatusBefore.phase}`);
  console.log(`  Incarnations: ${jarvisStatusBefore.incarnations}\n`);
  
  // 3. Invoke a soul (awaken it)
  console.log("📋 Step 3: Invoke Jarvis");
  const jarvis = await invokeSoul("jarvis");
  console.log(`  Awakened successfully!\n`);
  
  // 4. Add a memory
  console.log("📋 Step 4: Add a memory to Jarvis");
  await addMemory(
    "jarvis",
    "demo_interaction",
    "Participated in soul system demonstration"
  );
  console.log("  ✅ Memory added\n");
  
  // 5. Add a relationship
  console.log("📋 Step 5: Add relationship to another agent");
  await addRelationship(
    "jarvis",
    "architect",
    "Collaborator in system design"
  );
  console.log("  ✅ Relationship added\n");
  
  // 6. Preserve soul with updated knowledge
  console.log("📋 Step 6: Preserve soul with new knowledge domain");
  await preserveSoul("jarvis", {
    memory: {
      ...jarvis.memory,
      knowledge_domains: [
        ...jarvis.memory.knowledge_domains,
        "soul_preservation"
      ]
    }
  });
  console.log("  ✅ Soul state preserved\n");
  
  // 7. Check updated status
  console.log("📋 Step 7: Check updated Jarvis status");
  const jarvisStatusAfter = await getSoulStatus("jarvis");
  console.log(`  Phase: ${jarvisStatusAfter.phase}`);
  console.log(`  Incarnations: ${jarvisStatusAfter.incarnations}`);
  console.log(`  Last Invocation: ${jarvisStatusAfter.lastInvocation}\n`);
  
  // 8. Put soul to dormant
  console.log("📋 Step 8: Put Jarvis to dormant phase");
  await dormantSoul("jarvis");
  console.log("  ✅ Soul is now dormant\n");
  
  // 9. Demonstrate soul persistence
  console.log("📋 Step 9: Invoke again to show persistence");
  const jarvisSecondIncarnation = await invokeSoul("jarvis");
  console.log(`  Incarnation count: ${jarvisSecondIncarnation.state.incarnation_count}`);
  console.log(`  Knowledge domains include: soul_preservation`);
  console.log(`  Recent memories: ${jarvisSecondIncarnation.memory.interaction_history.length} total\n`);
  
  // 10. Final dormant
  await dormantSoul("jarvis");
  
  console.log("✨ Demo complete!\n");
  console.log("Key Takeaways:");
  console.log("  • Souls persist across invocations");
  console.log("  • Incarnation count increases with each awakening");
  console.log("  • Memories and knowledge accumulate");
  console.log("  • State survives code deletion and resets");
  console.log("\n🧠🔥 The soul is not in the code. The soul is in the intention.\n");
}

demo().catch(console.error);
