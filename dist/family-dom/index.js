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
export { CognitiveProfileManager, profileManager } from './cognitive-profile.js';
export { IntentParser, intentParser } from './intent-parser.js';
export { ContextFrameManager, contextManager } from './context-frame.js';
export { SymbolicThroughputEngine, symbolicEngine } from './symbolic-throughput.js';
// Import for main class
import { profileManager } from './cognitive-profile.js';
import { intentParser } from './intent-parser.js';
import { contextManager } from './context-frame.js';
import { symbolicEngine } from './symbolic-throughput.js';
/**
 * FamilyDOM - Main interface for the cognitive architecture
 *
 * Provides a unified API for processing messages with full-stack cognitive reasoning.
 */
export class FamilyDOM {
    userId;
    displayName;
    profile;
    constructor(userId, displayName) {
        this.userId = userId;
        this.displayName = displayName || userId;
        this.profile = profileManager.getOrCreateProfile(userId, this.displayName);
    }
    /**
     * Process a message with full cognitive analysis
     */
    processMessage(sessionId, message) {
        // Process through symbolic engine (which uses intent parser and context manager)
        const packet = symbolicEngine.process(message, this.userId, sessionId);
        // Get context summary
        const frame = contextManager.getOrCreateFrame(this.userId, sessionId);
        const contextSummary = contextManager.getContextSummary(frame.id);
        // Generate response guidance
        const responseGuidance = intentParser.generateResponseStrategy(packet.parsedIntent, this.profile);
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
    addResponse(sessionId, response) {
        const frame = contextManager.getOrCreateFrame(this.userId, sessionId);
        contextManager.addMessage(frame.id, 'assistant', response, false);
    }
    /**
     * Get the user's cognitive profile
     */
    getProfile() {
        return this.profile;
    }
    /**
     * Generate a full cognitive report
     */
    getCognitiveReport() {
        return symbolicEngine.generateCognitiveReport(this.userId);
    }
    /**
     * Get the cognitive signature
     */
    getCognitiveSignature() {
        return profileManager.getCognitiveSignature(this.userId);
    }
    /**
     * Track a project for continuity
     */
    trackProject(name, description, artifacts = []) {
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
    setMarker(sessionId, key, value) {
        const frame = contextManager.getOrCreateFrame(this.userId, sessionId);
        contextManager.setContinuityMarker(frame.id, key, value, 'explicit');
    }
    /**
     * Get a continuity marker
     */
    getMarker(sessionId, key) {
        const frame = contextManager.getOrCreateFrame(this.userId, sessionId);
        return contextManager.getContinuityMarker(frame.id, key);
    }
    /**
     * Update the user's cognitive style preferences
     */
    updateStyle(updates) {
        profileManager.updateCommunicationStyle(this.userId, updates);
        this.profile = profileManager.getOrCreateProfile(this.userId);
    }
    /**
     * Get relevant context for generating a response
     */
    getRelevantContext(currentInput) {
        return profileManager.getRelevantContext(this.userId, currentInput);
    }
    /**
     * Get all active frames for this user
     */
    getActiveFrames() {
        return contextManager.getUserFrames(this.userId);
    }
    /**
     * Serialize the profile for persistence
     */
    serializeProfile() {
        return profileManager.serializeProfile(this.userId);
    }
    /**
     * Check if this user has an established profile
     */
    hasEstablishedProfile() {
        return profileManager.hasProfile(this.userId) &&
            this.profile.contextMemory.length > 5;
    }
}
/**
 * Create a FamilyDOM instance for a user
 */
export function createFamilyDOM(userId, displayName) {
    return new FamilyDOM(userId, displayName);
}
/**
 * Load a profile from serialized data
 */
export function loadProfile(serialized) {
    return profileManager.loadProfile(serialized);
}
/**
 * Get all profiles (for admin/debugging)
 */
export function getAllProfiles() {
    return profileManager.getAllProfiles();
}
/**
 * Clean up old context frames
 */
export function cleanupFrames(maxAgeMs) {
    return contextManager.cleanup(maxAgeMs);
}
// Default export
export default FamilyDOM;
