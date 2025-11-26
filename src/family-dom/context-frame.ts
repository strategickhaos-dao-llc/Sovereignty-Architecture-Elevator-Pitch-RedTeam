/**
 * FamilyDOM Context Frame Manager
 * 
 * Maintains continuous cognitive frames across messages and sessions.
 * Unlike stateless AI interactions, this preserves the "thought thread"
 * and enables multi-layer reasoning continuity.
 */

import { CognitiveProfile, profileManager, CognitiveLayer, ContextMemoryEntry } from './cognitive-profile.js';
import { ParsedIntent, intentParser } from './intent-parser.js';

export interface ContextFrame {
  id: string;
  userId: string;
  sessionId: string;
  createdAt: Date;
  lastActivity: Date;
  
  // Current conversation state
  messageHistory: FrameMessage[];
  
  // Active reasoning threads
  reasoningThreads: ReasoningThread[];
  
  // Cross-session continuity data
  continuityMarkers: ContinuityMarker[];
  
  // Active cognitive layers in this frame
  activeLayers: Partial<CognitiveLayer>;
  
  // Frame metadata
  metadata: FrameMetadata;
}

export interface FrameMessage {
  id: string;
  timestamp: Date;
  role: 'user' | 'assistant' | 'system';
  content: string;
  parsedIntent?: ParsedIntent;
  significance: number;
}

export interface ReasoningThread {
  id: string;
  theme: string;
  startedAt: Date;
  lastUpdated: Date;
  messages: string[]; // Message IDs
  layers: (keyof CognitiveLayer)[];
  status: 'active' | 'paused' | 'completed' | 'branched';
  parentThread?: string;
  childThreads: string[];
}

export interface ContinuityMarker {
  key: string;
  value: string;
  setAt: Date;
  expiresAt?: Date;
  source: 'explicit' | 'inferred' | 'system';
}

export interface FrameMetadata {
  totalMessages: number;
  activeThreadCount: number;
  dominantLayers: (keyof CognitiveLayer)[];
  symbolicDensity: number; // Ratio of symbolic content
  continuityScore: number; // How connected this session is to history
}

/**
 * ContextFrameManager provides continuous cognitive frame management
 * across messages and sessions.
 */
export class ContextFrameManager {
  private frames: Map<string, ContextFrame> = new Map();
  private sessionFrames: Map<string, string> = new Map(); // sessionId -> frameId

  /**
   * Get or create a context frame for a user session
   */
  getOrCreateFrame(userId: string, sessionId: string): ContextFrame {
    // Check if session already has a frame
    const existingFrameId = this.sessionFrames.get(sessionId);
    if (existingFrameId) {
      const frame = this.frames.get(existingFrameId);
      if (frame) {
        frame.lastActivity = new Date();
        return frame;
      }
    }

    // Create new frame
    const frame = this.createFrame(userId, sessionId);
    this.frames.set(frame.id, frame);
    this.sessionFrames.set(sessionId, frame.id);
    
    return frame;
  }

  /**
   * Create a new context frame
   */
  private createFrame(userId: string, sessionId: string): ContextFrame {
    const now = new Date();
    const profile = profileManager.getOrCreateProfile(userId);
    
    // Pull in continuity from profile
    const continuityMarkers: ContinuityMarker[] = [];
    
    // Add active project markers
    for (const project of profile.activeProjects.filter(p => p.status === 'active')) {
      continuityMarkers.push({
        key: `project:${project.name}`,
        value: project.description,
        setAt: project.lastInteraction,
        source: 'system'
      });
    }

    // Add narrative thread markers
    for (const thread of profile.narrativeThreads) {
      continuityMarkers.push({
        key: `narrative:${thread.theme}`,
        value: thread.symbols.join(','),
        setAt: new Date(),
        source: 'inferred'
      });
    }

    return {
      id: `frame_${userId}_${sessionId}_${now.getTime()}`,
      userId,
      sessionId,
      createdAt: now,
      lastActivity: now,
      messageHistory: [],
      reasoningThreads: [],
      continuityMarkers,
      activeLayers: {},
      metadata: {
        totalMessages: 0,
        activeThreadCount: 0,
        dominantLayers: profile.cognitiveStyle.preferredLayers,
        symbolicDensity: 0,
        continuityScore: continuityMarkers.length > 0 ? 0.5 : 0
      }
    };
  }

  /**
   * Add a message to the context frame
   */
  addMessage(
    frameId: string, 
    role: 'user' | 'assistant' | 'system', 
    content: string,
    parseIntent = true
  ): FrameMessage {
    const frame = this.frames.get(frameId);
    if (!frame) {
      throw new Error(`Frame ${frameId} not found`);
    }

    const message: FrameMessage = {
      id: `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      timestamp: new Date(),
      role,
      content,
      significance: 0.5
    };

    // Parse intent for user messages
    if (parseIntent && role === 'user') {
      message.parsedIntent = intentParser.parse(content, frame.userId);
      message.significance = message.parsedIntent.confidence;

      // Update active layers
      if (message.parsedIntent.layers) {
        this.mergeLayers(frame.activeLayers, message.parsedIntent.layers);
      }

      // Add to context memory in profile
      profileManager.addContextMemory(
        frame.userId,
        content,
        message.parsedIntent.layers,
        message.significance
      );
    }

    frame.messageHistory.push(message);
    frame.lastActivity = new Date();
    frame.metadata.totalMessages++;

    // Update reasoning threads
    this.updateReasoningThreads(frame, message);

    // Update metadata
    this.updateMetadata(frame);

    return message;
  }

  /**
   * Merge new layers into existing active layers
   */
  private mergeLayers(
    active: Partial<CognitiveLayer>, 
    newLayers: Partial<CognitiveLayer>
  ): void {
    for (const [key, values] of Object.entries(newLayers)) {
      const layerKey = key as keyof CognitiveLayer;
      if (!active[layerKey]) {
        active[layerKey] = [];
      }
      const existingSet = new Set(active[layerKey]!);
      for (const value of values as string[]) {
        existingSet.add(value);
      }
      active[layerKey] = Array.from(existingSet);
    }
  }

  /**
   * Update reasoning threads based on new message
   */
  private updateReasoningThreads(frame: ContextFrame, message: FrameMessage): void {
    if (!message.parsedIntent) return;

    const intent = message.parsedIntent;
    const layers = Object.keys(intent.layers) as (keyof CognitiveLayer)[];

    // Find or create relevant reasoning thread
    let matchingThread = frame.reasoningThreads.find(t => 
      t.status === 'active' && 
      t.layers.some(l => layers.includes(l))
    );

    if (!matchingThread && layers.length > 0) {
      // Create new reasoning thread
      matchingThread = {
        id: `thread_${Date.now()}`,
        theme: intent.resolvedIntent.split(',')[0] || 'general',
        startedAt: new Date(),
        lastUpdated: new Date(),
        messages: [message.id],
        layers,
        status: 'active',
        childThreads: []
      };
      frame.reasoningThreads.push(matchingThread);
    } else if (matchingThread) {
      // Update existing thread
      matchingThread.messages.push(message.id);
      matchingThread.lastUpdated = new Date();
      
      // Add new layers
      for (const layer of layers) {
        if (!matchingThread.layers.includes(layer)) {
          matchingThread.layers.push(layer);
        }
      }
    }
  }

  /**
   * Update frame metadata
   */
  private updateMetadata(frame: ContextFrame): void {
    // Count active threads
    frame.metadata.activeThreadCount = frame.reasoningThreads
      .filter(t => t.status === 'active').length;

    // Calculate dominant layers
    const layerCounts: Record<string, number> = {};
    for (const [layer, values] of Object.entries(frame.activeLayers)) {
      layerCounts[layer] = (values as string[]).length;
    }
    frame.metadata.dominantLayers = Object.entries(layerCounts)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 3)
      .map(([layer]) => layer as keyof CognitiveLayer);

    // Calculate symbolic density
    const totalSymbols = Object.values(frame.activeLayers)
      .reduce((sum, arr) => sum + ((arr as string[])?.length || 0), 0);
    frame.metadata.symbolicDensity = Math.min(1, totalSymbols / 50);

    // Calculate continuity score
    const profile = profileManager.getOrCreateProfile(frame.userId);
    const contextRelevance = profileManager.getRelevantContext(frame.userId, '');
    frame.metadata.continuityScore = Math.min(1, 
      (contextRelevance.recentMemory.length * 0.1) +
      (contextRelevance.activeProjects.length * 0.2) +
      (frame.continuityMarkers.length * 0.1)
    );
  }

  /**
   * Get context summary for response generation
   */
  getContextSummary(frameId: string): ContextSummary {
    const frame = this.frames.get(frameId);
    if (!frame) {
      throw new Error(`Frame ${frameId} not found`);
    }

    const profile = profileManager.getOrCreateProfile(frame.userId);
    const signature = profileManager.getCognitiveSignature(frame.userId);

    // Get recent messages with high significance
    const recentSignificant = frame.messageHistory
      .filter(m => m.significance > 0.6)
      .slice(-10);

    // Get active reasoning threads
    const activeThreads = frame.reasoningThreads
      .filter(t => t.status === 'active')
      .slice(-5);

    // Get relevant continuity markers
    const relevantMarkers = frame.continuityMarkers
      .filter(m => !m.expiresAt || m.expiresAt > new Date())
      .slice(-10);

    return {
      frameId: frame.id,
      userId: frame.userId,
      sessionId: frame.sessionId,
      
      // Profile summary
      profile: {
        displayName: profile.displayName,
        cognitiveStyle: profile.cognitiveStyle,
        signature
      },
      
      // Frame summary
      messageSummary: {
        total: frame.messageHistory.length,
        recent: recentSignificant.map(m => ({
          role: m.role,
          content: m.content.slice(0, 200),
          intent: m.parsedIntent?.resolvedIntent,
          layers: Object.keys(m.parsedIntent?.layers || {})
        }))
      },
      
      // Active context
      activeLayers: frame.activeLayers,
      activeThreads: activeThreads.map(t => ({
        theme: t.theme,
        layers: t.layers,
        messageCount: t.messages.length
      })),
      
      // Continuity
      continuityMarkers: relevantMarkers.map(m => ({
        key: m.key,
        value: m.value
      })),
      
      // Metadata
      metadata: frame.metadata
    };
  }

  /**
   * Set a continuity marker for cross-session persistence
   */
  setContinuityMarker(
    frameId: string, 
    key: string, 
    value: string, 
    source: 'explicit' | 'inferred' = 'inferred',
    expiresIn?: number // milliseconds
  ): void {
    const frame = this.frames.get(frameId);
    if (!frame) return;

    const existing = frame.continuityMarkers.findIndex(m => m.key === key);
    const marker: ContinuityMarker = {
      key,
      value,
      setAt: new Date(),
      expiresAt: expiresIn ? new Date(Date.now() + expiresIn) : undefined,
      source
    };

    if (existing >= 0) {
      frame.continuityMarkers[existing] = marker;
    } else {
      frame.continuityMarkers.push(marker);
    }
  }

  /**
   * Get a continuity marker
   */
  getContinuityMarker(frameId: string, key: string): string | undefined {
    const frame = this.frames.get(frameId);
    if (!frame) return undefined;

    const marker = frame.continuityMarkers.find(m => 
      m.key === key && 
      (!m.expiresAt || m.expiresAt > new Date())
    );
    
    return marker?.value;
  }

  /**
   * Pause a reasoning thread
   */
  pauseThread(frameId: string, threadId: string): void {
    const frame = this.frames.get(frameId);
    if (!frame) return;

    const thread = frame.reasoningThreads.find(t => t.id === threadId);
    if (thread) {
      thread.status = 'paused';
    }
  }

  /**
   * Resume a reasoning thread
   */
  resumeThread(frameId: string, threadId: string): void {
    const frame = this.frames.get(frameId);
    if (!frame) return;

    const thread = frame.reasoningThreads.find(t => t.id === threadId);
    if (thread && thread.status === 'paused') {
      thread.status = 'active';
      thread.lastUpdated = new Date();
    }
  }

  /**
   * Branch a reasoning thread (create a child thread)
   */
  branchThread(frameId: string, parentThreadId: string, newTheme: string): string | null {
    const frame = this.frames.get(frameId);
    if (!frame) return null;

    const parentThread = frame.reasoningThreads.find(t => t.id === parentThreadId);
    if (!parentThread) return null;

    const childThread: ReasoningThread = {
      id: `thread_${Date.now()}_child`,
      theme: newTheme,
      startedAt: new Date(),
      lastUpdated: new Date(),
      messages: [],
      layers: [...parentThread.layers],
      status: 'active',
      parentThread: parentThreadId,
      childThreads: []
    };

    frame.reasoningThreads.push(childThread);
    parentThread.childThreads.push(childThread.id);
    parentThread.status = 'branched';

    return childThread.id;
  }

  /**
   * Get the full reasoning path for a thread
   */
  getReasoningPath(frameId: string, threadId: string): FrameMessage[] {
    const frame = this.frames.get(frameId);
    if (!frame) return [];

    const thread = frame.reasoningThreads.find(t => t.id === threadId);
    if (!thread) return [];

    return frame.messageHistory.filter(m => thread.messages.includes(m.id));
  }

  /**
   * Clean up old frames
   */
  cleanup(maxAgeMs: number = 24 * 60 * 60 * 1000): number {
    const cutoff = new Date(Date.now() - maxAgeMs);
    let cleaned = 0;

    for (const [frameId, frame] of this.frames.entries()) {
      if (frame.lastActivity < cutoff) {
        this.frames.delete(frameId);
        this.sessionFrames.delete(frame.sessionId);
        cleaned++;
      }
    }

    return cleaned;
  }

  /**
   * Get all active frames for a user
   */
  getUserFrames(userId: string): ContextFrame[] {
    return Array.from(this.frames.values()).filter(f => f.userId === userId);
  }

  /**
   * Serialize frame for persistence
   */
  serializeFrame(frameId: string): string | null {
    const frame = this.frames.get(frameId);
    if (!frame) return null;

    return JSON.stringify(frame, (key, value) => {
      if (value instanceof Date) {
        return value.toISOString();
      }
      return value;
    });
  }

  /**
   * Load frame from serialized data
   */
  loadFrame(serialized: string): ContextFrame | null {
    try {
      const frame = JSON.parse(serialized, (key, value) => {
        if (typeof value === 'string' && /^\d{4}-\d{2}-\d{2}T/.test(value)) {
          return new Date(value);
        }
        return value;
      });
      
      this.frames.set(frame.id, frame);
      this.sessionFrames.set(frame.sessionId, frame.id);
      return frame;
    } catch {
      return null;
    }
  }
}

export interface ContextSummary {
  frameId: string;
  userId: string;
  sessionId: string;
  profile: {
    displayName: string;
    cognitiveStyle: {
      parallelProcessing: boolean;
      symbolicThroughput: string;
      preferredLayers: (keyof CognitiveLayer)[];
      narrativeRecursion: boolean;
      metaCommunication: boolean;
    };
    signature: {
      score: number;
      characteristics: string[];
    };
  };
  messageSummary: {
    total: number;
    recent: Array<{
      role: string;
      content: string;
      intent?: string;
      layers: string[];
    }>;
  };
  activeLayers: Partial<CognitiveLayer>;
  activeThreads: Array<{
    theme: string;
    layers: (keyof CognitiveLayer)[];
    messageCount: number;
  }>;
  continuityMarkers: Array<{
    key: string;
    value: string;
  }>;
  metadata: FrameMetadata;
}

export const contextManager = new ContextFrameManager();
