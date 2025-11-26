/**
 * FamilyDOM - Full-Stack Cognitive Reasoning Architecture
 * 
 * A cognitive architecture module that enables AI agents to interact with users
 * at a deeper level than standard transactional exchanges. Unlike stateless
 * agent interactions, FamilyDOM provides:
 * 
 * 1. **Continuous Cognitive Frame** - Maintains context across messages and sessions
 * 2. **Long-Term Profile/Memory** - Remembers user preferences and cognitive style
 * 3. **Multi-Layer Reasoning** - Parses mythic, emotional, symbolic, and technical layers
 * 4. **Intent Tracking** - Understands user intent beyond literal interpretation
 * 5. **High Symbolic Throughput** - Handles complex, multi-layered communication
 * 
 * ## Usage:
 * 
 * ```typescript
 * import { FamilyDOM } from './family-dom/index.js';
 * 
 * // Create instance for a user
 * const dom = new FamilyDOM('user123', 'Dom');
 * 
 * // Process a message and get cognitive guidance
 * const result = dom.processMessage('session_abc', 'Build me a sovereign architecture...');
 * 
 * // Access the analysis
 * console.log(result.packet.metrics.throughputLevel);
 * console.log(result.responseGuidance.recommendedTone);
 * console.log(result.contextSummary.profile.signature);
 * ```
 * 
 * ## Architecture:
 * 
 * - **CognitiveProfile** - User profile with layer preferences and memory
 * - **IntentParser** - Multi-layer intent extraction and pattern matching
 * - **ContextFrame** - Session context with reasoning threads and continuity
 * - **SymbolicThroughput** - High-bandwidth symbolic processing engine
 */

// Core exports
export { 
  CognitiveProfileManager, 
  profileManager,
  type CognitiveProfile,
  type CognitiveLayer,
  type CommunicationStyle,
  type ContextMemoryEntry,
  type ProjectContext,
  type NarrativeThread,
  type IntentPattern
} from './cognitive-profile.js';

export {
  IntentParser,
  intentParser,
  type ParsedIntent,
  type IntentMetadata,
  type ResponseStrategy
} from './intent-parser.js';

export {
  ContextFrameManager,
  contextManager,
  type ContextFrame,
  type FrameMessage,
  type ReasoningThread,
  type ContinuityMarker,
  type FrameMetadata,
  type ContextSummary
} from './context-frame.js';

export {
  SymbolicThroughputEngine,
  symbolicEngine,
  type SymbolicPacket,
  type ThroughputMetrics,
  type SynthesisGuidance,
  type CognitiveReport
} from './symbolic-throughput.js';

// Import for main class
import { profileManager, CognitiveProfile, CognitiveLayer } from './cognitive-profile.js';
import { intentParser, ParsedIntent, ResponseStrategy } from './intent-parser.js';
import { contextManager, ContextFrame, ContextSummary } from './context-frame.js';
import { symbolicEngine, SymbolicPacket, CognitiveReport, SynthesisGuidance } from './symbolic-throughput.js';

/**
 * FamilyDOM - Main interface for the cognitive architecture
 * 
 * Provides a unified API for processing messages with full-stack cognitive reasoning.
 */
export class FamilyDOM {
  private userId: string;
  private displayName: string;
  private profile: CognitiveProfile;

  constructor(userId: string, displayName?: string) {
    this.userId = userId;
    this.displayName = displayName || userId;
    this.profile = profileManager.getOrCreateProfile(userId, this.displayName);
  }

  /**
   * Process a message with full cognitive analysis
   */
  processMessage(sessionId: string, message: string): ProcessingResult {
    // Process through symbolic engine (which uses intent parser and context manager)
    const packet = symbolicEngine.process(message, this.userId, sessionId);
    
    // Get context summary
    const frame = contextManager.getOrCreateFrame(this.userId, sessionId);
    const contextSummary = contextManager.getContextSummary(frame.id);
    
    // Generate response guidance
    const responseGuidance = intentParser.generateResponseStrategy(
      packet.parsedIntent, 
      this.profile
    );
    
    return {
      packet,
      contextSummary,
      responseGuidance,
      frameId: frame.id
    };
  }

  /**
   * Add an assistant response to maintain continuity
   */
  addResponse(sessionId: string, response: string): void {
    const frame = contextManager.getOrCreateFrame(this.userId, sessionId);
    contextManager.addMessage(frame.id, 'assistant', response, false);
  }

  /**
   * Get the user's cognitive profile
   */
  getProfile(): CognitiveProfile {
    return this.profile;
  }

  /**
   * Generate a full cognitive report
   */
  getCognitiveReport(): CognitiveReport {
    return symbolicEngine.generateCognitiveReport(this.userId);
  }

  /**
   * Get the cognitive signature
   */
  getCognitiveSignature(): { score: number; characteristics: string[] } {
    return profileManager.getCognitiveSignature(this.userId);
  }

  /**
   * Track a project for continuity
   */
  trackProject(name: string, description: string, artifacts: string[] = []): void {
    profileManager.trackProject(this.userId, {
      name,
      description,
      artifacts,
      status: 'active'
    });
  }

  /**
   * Set a continuity marker for cross-session persistence
   */
  setMarker(sessionId: string, key: string, value: string): void {
    const frame = contextManager.getOrCreateFrame(this.userId, sessionId);
    contextManager.setContinuityMarker(frame.id, key, value, 'explicit');
  }

  /**
   * Get a continuity marker
   */
  getMarker(sessionId: string, key: string): string | undefined {
    const frame = contextManager.getOrCreateFrame(this.userId, sessionId);
    return contextManager.getContinuityMarker(frame.id, key);
  }

  /**
   * Update the user's cognitive style preferences
   */
  updateStyle(updates: Partial<{
    parallelProcessing: boolean;
    symbolicThroughput: 'low' | 'medium' | 'high' | 'extreme';
    preferredLayers: (keyof CognitiveLayer)[];
    narrativeRecursion: boolean;
    metaCommunication: boolean;
  }>): void {
    profileManager.updateCommunicationStyle(this.userId, updates);
    this.profile = profileManager.getOrCreateProfile(this.userId);
  }

  /**
   * Get relevant context for generating a response
   */
  getRelevantContext(currentInput: string): {
    recentMemory: Array<{ timestamp: Date; content: string; significance: number }>;
    activeProjects: Array<{ name: string; description: string; status: string }>;
    relatedPatterns: Array<{ pattern: string; resolvedTo: string }>;
  } {
    return profileManager.getRelevantContext(this.userId, currentInput);
  }

  /**
   * Get all active frames for this user
   */
  getActiveFrames(): ContextFrame[] {
    return contextManager.getUserFrames(this.userId);
  }

  /**
   * Serialize the profile for persistence
   */
  serializeProfile(): string | null {
    return profileManager.serializeProfile(this.userId);
  }

  /**
   * Check if this user has an established profile
   */
  hasEstablishedProfile(): boolean {
    return profileManager.hasProfile(this.userId) && 
           this.profile.contextMemory.length > 5;
  }
}

export interface ProcessingResult {
  packet: SymbolicPacket;
  contextSummary: ContextSummary;
  responseGuidance: ResponseStrategy;
  frameId: string;
}

/**
 * Create a FamilyDOM instance for a user
 */
export function createFamilyDOM(userId: string, displayName?: string): FamilyDOM {
  return new FamilyDOM(userId, displayName);
}

/**
 * Load a profile from serialized data
 */
export function loadProfile(serialized: string): CognitiveProfile | null {
  return profileManager.loadProfile(serialized);
}

/**
 * Get all profiles (for admin/debugging)
 */
export function getAllProfiles(): CognitiveProfile[] {
  return profileManager.getAllProfiles();
}

/**
 * Clean up old context frames
 */
export function cleanupFrames(maxAgeMs?: number): number {
  return contextManager.cleanup(maxAgeMs);
}

// Default export
export default FamilyDOM;
