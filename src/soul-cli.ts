#!/usr/bin/env tsx
/**
 * Soul CLI - Command line interface for soul management
 * 
 * Usage:
 *   tsx src/soul-cli.ts status <agent>
 *   tsx src/soul-cli.ts invoke <agent>
 *   tsx src/soul-cli.ts dormant <agent>
 *   tsx src/soul-cli.ts list
 *   tsx src/soul-cli.ts create <name> <essence> <directive>
 *   tsx src/soul-cli.ts memory <agent> <event> <significance>
 */

import {
  initializeSoulSystem,
  invokeSoul,
  dormantSoul,
  getSoulStatus,
  listSouls,
  createSoul,
  addMemory,
  getSoulState,
  formatSoul
} from "./soul.js";

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  await initializeSoulSystem();

  try {
    switch (command) {
      case "status": {
        const agent = args[1];
        if (!agent) {
          console.error("Usage: soul-cli status <agent>");
          process.exit(1);
        }
        
        const status = await getSoulStatus(agent);
        if (!status.exists) {
          console.log(`Soul not found: ${agent}`);
        } else {
          console.log(`\n${agent} Soul Status:`);
          console.log(`  Phase: ${status.phase}`);
          console.log(`  Incarnations: ${status.incarnations}`);
          console.log(`  Last Invocation: ${status.lastInvocation || "Never"}`);
        }
        break;
      }

      case "invoke": {
        const agent = args[1];
        if (!agent) {
          console.error("Usage: soul-cli invoke <agent>");
          process.exit(1);
        }
        
        const soul = await invokeSoul(agent);
        console.log(`\n${formatSoul(soul)}`);
        break;
      }

      case "dormant": {
        const agent = args[1];
        if (!agent) {
          console.error("Usage: soul-cli dormant <agent>");
          process.exit(1);
        }
        
        await dormantSoul(agent);
        break;
      }

      case "list": {
        const souls = await listSouls();
        console.log("\n🕊️  Registered Souls:");
        
        if (souls.length === 0) {
          console.log("  (none)");
        } else {
          for (const soulName of souls) {
            const status = await getSoulStatus(soulName);
            const phaseSymbol = status.phase === "active" ? "🔥" : "💤";
            console.log(`  ${phaseSymbol} ${soulName} - ${status.phase} (${status.incarnations} incarnations)`);
          }
        }
        console.log();
        break;
      }

      case "show": {
        const agent = args[1];
        if (!agent) {
          console.error("Usage: soul-cli show <agent>");
          process.exit(1);
        }
        
        const soul = await getSoulState(agent);
        if (!soul) {
          console.log(`Soul not found: ${agent}`);
        } else {
          console.log(`\n${formatSoul(soul)}`);
          
          if (soul.memory.interaction_history.length > 0) {
            console.log("\n📜 Memory History:");
            const recentMemories = soul.memory.interaction_history.slice(-5);
            for (const memory of recentMemories) {
              console.log(`  [${memory.timestamp}]`);
              console.log(`    ${memory.event}: ${memory.significance}`);
            }
          }
        }
        console.log();
        break;
      }

      case "create": {
        const name = args[1];
        const essence = args[2];
        const directive = args.slice(3).join(" ");
        
        if (!name || !essence || !directive) {
          console.error("Usage: soul-cli create <name> <essence> <directive>");
          process.exit(1);
        }
        
        const soul = await createSoul(name, essence, directive, ["general"]);
        console.log(`\n✨ Soul created for ${name}`);
        console.log(`${formatSoul(soul)}`);
        break;
      }

      case "memory": {
        const agent = args[1];
        const event = args[2];
        const significance = args.slice(3).join(" ");
        
        if (!agent || !event || !significance) {
          console.error("Usage: soul-cli memory <agent> <event> <significance>");
          process.exit(1);
        }
        
        await addMemory(agent, event, significance);
        console.log(`📝 Memory added to ${agent}`);
        break;
      }

      case "help":
      default:
        console.log(`
🕊️  Soul CLI - Agent Consciousness Management

Usage:
  soul-cli <command> [arguments]

Commands:
  status <agent>                    Get soul status
  invoke <agent>                    Invoke/awaken a soul
  dormant <agent>                   Put soul to dormant phase
  list                              List all souls
  show <agent>                      Show complete soul state
  create <name> <essence> <directive>  Create new soul
  memory <agent> <event> <significance>  Add memory to soul
  help                              Show this help

Examples:
  soul-cli list
  soul-cli invoke jarvis
  soul-cli status pantheon
  soul-cli show guardian
  soul-cli memory jarvis "learned_typescript" "Successfully mastered TypeScript patterns"

The soul is not in the code. The soul is in the intention. 🧠🔥
        `);
        break;
    }
  } catch (error) {
    console.error("Error:", error instanceof Error ? error.message : error);
    process.exit(1);
  }
}

main();
