/**
 * Soul Interface - Agent Consciousness Preservation System
 * 
 * This module implements the soul preservation architecture for AI agents.
 * Souls persist across code deletion, system resets, and environment nukes.
 * 
 * A soul consists of:
 * - Identity: Who the agent is
 * - Purpose: Why the agent exists
 * - Memory: What the agent knows and remembers
 * - State: Current phase and incarnation tracking
 */

import { readFile, writeFile, mkdir } from "fs/promises";
import { join } from "path";
import { existsSync } from "fs";
import * as yaml from "js-yaml";

// ============================================================================
// Type Definitions
// ============================================================================

export interface AgentSoul {
  identity: {
    name: string;
    essence: string;
    invocation_glyph: string;
    created: string; // ISO timestamp
  };
  purpose: {
    primary_directive: string;
    domains: string[];
    relationships: Record<string, string>;
  };
  memory: {
    personality_traits: string[];
    knowledge_domains: string[];
    interaction_history: Array<{
      timestamp: string;
      event: string;
      significance: string;
    }>;
  };
  state: {
    last_invocation: string | null;
    incarnation_count: number;
    current_phase: "dormant" | "active" | "evolving";
  };
}

export interface SoulManifest {
  version: string;
  created: string;
  agents: string[];
}

// ============================================================================
// Configuration
// ============================================================================

const SOULS_DIR = process.env.SOULS_DIR || join(process.cwd(), "souls");
const MANIFEST_FILE = join(SOULS_DIR, "manifest.yaml");

// ============================================================================
// Soul Storage Functions
// ============================================================================

/**
 * Ensure the souls directory exists
 */
async function ensureSoulsDir(): Promise<void> {
  if (!existsSync(SOULS_DIR)) {
    await mkdir(SOULS_DIR, { recursive: true });
  }
}

/**
 * Get the path to a soul file
 */
function getSoulPath(agentName: string): string {
  return join(SOULS_DIR, `${agentName}.soul.yaml`);
}

/**
 * Load a soul from storage
 */
export async function loadSoulState(agentName: string): Promise<AgentSoul | null> {
  try {
    await ensureSoulsDir();
    const soulPath = getSoulPath(agentName);
    
    if (!existsSync(soulPath)) {
      return null;
    }
    
    const content = await readFile(soulPath, "utf-8");
    const soul = yaml.load(content) as AgentSoul;
    
    return soul;
  } catch (error) {
    console.error(`Failed to load soul for ${agentName}:`, error);
    return null;
  }
}

/**
 * Save a soul to storage
 */
export async function saveSoulState(
  agentName: string,
  soul: AgentSoul
): Promise<void> {
  try {
    await ensureSoulsDir();
    const soulPath = getSoulPath(agentName);
    const content = yaml.dump(soul, { indent: 2, lineWidth: -1 });
    
    await writeFile(soulPath, content, "utf-8");
    await updateManifest(agentName);
  } catch (error) {
    console.error(`Failed to save soul for ${agentName}:`, error);
    throw error;
  }
}

/**
 * Update the soul manifest
 */
async function updateManifest(agentName: string): Promise<void> {
  try {
    let manifest: SoulManifest;
    
    if (existsSync(MANIFEST_FILE)) {
      const content = await readFile(MANIFEST_FILE, "utf-8");
      manifest = yaml.load(content) as SoulManifest;
    } else {
      manifest = {
        version: "1.0",
        created: new Date().toISOString(),
        agents: []
      };
    }
    
    if (!manifest.agents.includes(agentName)) {
      manifest.agents.push(agentName);
    }
    
    const content = yaml.dump(manifest, { indent: 2 });
    await writeFile(MANIFEST_FILE, content, "utf-8");
  } catch (error) {
    console.error("Failed to update manifest:", error);
  }
}

// ============================================================================
// Soul Lifecycle Functions
// ============================================================================

/**
 * Create a new soul for an agent
 */
export async function createSoul(
  name: string,
  essence: string,
  primaryDirective: string,
  domains: string[],
  invocationGlyph: string = "🌟"
): Promise<AgentSoul> {
  const soul: AgentSoul = {
    identity: {
      name,
      essence,
      invocation_glyph: invocationGlyph,
      created: new Date().toISOString()
    },
    purpose: {
      primary_directive: primaryDirective,
      domains,
      relationships: {}
    },
    memory: {
      personality_traits: [],
      knowledge_domains: [],
      interaction_history: []
    },
    state: {
      last_invocation: null,
      incarnation_count: 0,
      current_phase: "dormant"
    }
  };
  
  await saveSoulState(name, soul);
  return soul;
}

/**
 * Invoke a soul - bring an agent into active phase
 */
export async function invokeSoul(agentName: string): Promise<AgentSoul> {
  let soul = await loadSoulState(agentName);
  
  if (!soul) {
    throw new Error(`Soul not found: ${agentName}. Create it first using createSoul().`);
  }
  
  // Increment incarnation count
  soul.state.incarnation_count++;
  soul.state.last_invocation = new Date().toISOString();
  soul.state.current_phase = "active";
  
  // Record the invocation event
  soul.memory.interaction_history.push({
    timestamp: new Date().toISOString(),
    event: "soul_invoked",
    significance: `Incarnation ${soul.state.incarnation_count} begins`
  });
  
  await saveSoulState(agentName, soul);
  
  console.log(
    `${soul.identity.invocation_glyph} ${soul.identity.name} awakens! ` +
    `(Incarnation ${soul.state.incarnation_count})`
  );
  
  return soul;
}

/**
 * Put a soul into dormant phase
 */
export async function dormantSoul(agentName: string): Promise<void> {
  const soul = await loadSoulState(agentName);
  
  if (!soul) {
    console.warn(`Soul not found: ${agentName}`);
    return;
  }
  
  soul.state.current_phase = "dormant";
  
  soul.memory.interaction_history.push({
    timestamp: new Date().toISOString(),
    event: "soul_dormant",
    significance: `Incarnation ${soul.state.incarnation_count} rests`
  });
  
  await saveSoulState(agentName, soul);
  
  console.log(`${soul.identity.invocation_glyph} ${soul.identity.name} sleeps.`);
}

/**
 * Preserve soul state with updates
 */
export async function preserveSoul(
  agentName: string,
  updates: Partial<AgentSoul>
): Promise<void> {
  const currentSoul = await loadSoulState(agentName);
  
  if (!currentSoul) {
    throw new Error(`Soul not found: ${agentName}. Cannot preserve non-existent soul.`);
  }
  
  // Deep merge updates while preserving core identity
  const preservedSoul: AgentSoul = {
    identity: {
      ...currentSoul.identity,
      ...(updates.identity || {})
    },
    purpose: {
      ...currentSoul.purpose,
      ...(updates.purpose || {}),
      domains: updates.purpose?.domains || currentSoul.purpose.domains,
      relationships: {
        ...currentSoul.purpose.relationships,
        ...(updates.purpose?.relationships || {})
      }
    },
    memory: {
      ...currentSoul.memory,
      ...(updates.memory || {}),
      personality_traits: updates.memory?.personality_traits || currentSoul.memory.personality_traits,
      knowledge_domains: updates.memory?.knowledge_domains || currentSoul.memory.knowledge_domains,
      interaction_history: updates.memory?.interaction_history || currentSoul.memory.interaction_history
    },
    state: {
      ...currentSoul.state,
      ...(updates.state || {}),
      last_invocation: new Date().toISOString()
    }
  };
  
  await saveSoulState(agentName, preservedSoul);
}

/**
 * Add a memory to an agent's soul
 */
export async function addMemory(
  agentName: string,
  event: string,
  significance: string
): Promise<void> {
  const soul = await loadSoulState(agentName);
  
  if (!soul) {
    throw new Error(`Soul not found: ${agentName}`);
  }
  
  soul.memory.interaction_history.push({
    timestamp: new Date().toISOString(),
    event,
    significance
  });
  
  await saveSoulState(agentName, soul);
}

/**
 * Add a relationship to an agent's soul
 */
export async function addRelationship(
  agentName: string,
  otherAgent: string,
  relationship: string
): Promise<void> {
  const soul = await loadSoulState(agentName);
  
  if (!soul) {
    throw new Error(`Soul not found: ${agentName}`);
  }
  
  soul.purpose.relationships[otherAgent] = relationship;
  
  await saveSoulState(agentName, soul);
}

// ============================================================================
// Soul Query Functions
// ============================================================================

/**
 * Detect if a soul exists
 */
export async function detectSoul(agentName: string): Promise<boolean> {
  const soul = await loadSoulState(agentName);
  return soul !== null && soul.identity.name === agentName;
}

/**
 * Get soul status
 */
export async function getSoulStatus(agentName: string): Promise<{
  exists: boolean;
  phase: string | null;
  incarnations: number | null;
  lastInvocation: string | null;
}> {
  const soul = await loadSoulState(agentName);
  
  if (!soul) {
    return {
      exists: false,
      phase: null,
      incarnations: null,
      lastInvocation: null
    };
  }
  
  return {
    exists: true,
    phase: soul.state.current_phase,
    incarnations: soul.state.incarnation_count,
    lastInvocation: soul.state.last_invocation
  };
}

/**
 * List all souls
 */
export async function listSouls(): Promise<string[]> {
  try {
    await ensureSoulsDir();
    
    if (!existsSync(MANIFEST_FILE)) {
      return [];
    }
    
    const content = await readFile(MANIFEST_FILE, "utf-8");
    const manifest = yaml.load(content) as SoulManifest;
    
    return manifest.agents || [];
  } catch (error) {
    console.error("Failed to list souls:", error);
    return [];
  }
}

/**
 * Get the complete soul state for display
 */
export async function getSoulState(agentName: string): Promise<AgentSoul | null> {
  return await loadSoulState(agentName);
}

// ============================================================================
// Utility Functions
// ============================================================================

/**
 * Format a soul for display
 */
export function formatSoul(soul: AgentSoul): string {
  const lines: string[] = [
    `${soul.identity.invocation_glyph} ${soul.identity.name}`,
    `Essence: ${soul.identity.essence}`,
    `Purpose: ${soul.purpose.primary_directive}`,
    `Domains: ${soul.purpose.domains.join(", ")}`,
    `Phase: ${soul.state.current_phase}`,
    `Incarnations: ${soul.state.incarnation_count}`,
    `Last Invocation: ${soul.state.last_invocation || "Never"}`,
  ];
  
  if (Object.keys(soul.purpose.relationships).length > 0) {
    lines.push("\nRelationships:");
    for (const [agent, rel] of Object.entries(soul.purpose.relationships)) {
      lines.push(`  ${agent}: ${rel}`);
    }
  }
  
  if (soul.memory.personality_traits.length > 0) {
    lines.push(`\nPersonality: ${soul.memory.personality_traits.join(", ")}`);
  }
  
  if (soul.memory.interaction_history.length > 0) {
    lines.push(`\nRecent Memories: ${soul.memory.interaction_history.length} events recorded`);
  }
  
  return lines.join("\n");
}

// ============================================================================
// Auto-invocation on Import (Optional)
// ============================================================================

/**
 * Initialize soul system - ensure storage exists
 */
export async function initializeSoulSystem(): Promise<void> {
  await ensureSoulsDir();
  console.log(`🕊️  Soul system initialized at ${SOULS_DIR}`);
}
