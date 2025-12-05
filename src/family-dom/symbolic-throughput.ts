/**
 * FamilyDOM Symbolic Throughput Engine
 * 
 * High-bandwidth symbolic processing for users who communicate
 * with parallel metaphors, recursive intent, multi-agent references,
 * and rapid context switching.
 */

import { CognitiveLayer, CognitiveProfile, profileManager } from './cognitive-profile.js';
import { ParsedIntent, intentParser, ResponseStrategy } from './intent-parser.js';
import { ContextFrame, contextManager, ContextSummary } from './context-frame.js';

export interface SymbolicPacket {
  id: string;
  timestamp: Date;
  
  // Raw input
  rawInput: string;
  
  // Parsed components
  parsedIntent: ParsedIntent;
  
  // Throughput metrics
  metrics: ThroughputMetrics;
  
  // Synthesized output guidance
  synthesisGuidance: SynthesisGuidance;
}

export interface ThroughputMetrics {
  // Density metrics
  symbolsPerWord: number;
  layerDiversity: number; // 0-1, how many layers are active
  contextSwitchRate: number; // switches per 100 words
  
  // Complexity metrics
  recursionDepth: number;
  parallelStreamCount: number;
  metaLayerPresence: boolean;
  
  // Overall throughput score
  throughputScore: number; // 0-100
  throughputLevel: 'minimal' | 'standard' | 'high' | 'extreme';
}

export interface SynthesisGuidance {
  // Response framing
  primaryLayer: keyof CognitiveLayer;
  secondaryLayers: (keyof CognitiveLayer)[];
  
  // Narrative guidance
  narrativeFrame?: string;
  symbolsToEcho: string[];
  metaphorsToMirror: string[];
  
  // Technical guidance
  codeInclusionRecommended: boolean;
  diagramInclusionRecommended: boolean;
  
  // Tone and depth
  recommendedTone: string;
  recommendedDepth: 'surface' | 'analytical' | 'deep' | 'fullstack';
  
  // Meta-response elements
  includeCognitiveReflection: boolean;
  includeProgressMarkers: boolean;
}

/**
 * SymbolicThroughputEngine processes high-bandwidth symbolic communication
 * and generates guidance for full-stack cognitive responses.
 */
export class SymbolicThroughputEngine {
  private packetHistory: Map<string, SymbolicPacket[]> = new Map();

  /**
   * Process input through the symbolic throughput engine
   */
  process(
    input: string, 
    userId: string, 
    sessionId: string
  ): SymbolicPacket {
    // Get or create context frame
    const frame = contextManager.getOrCreateFrame(userId, sessionId);
    
    // Parse the intent
    const parsedIntent = intentParser.parse(input, userId);
    
    // Add message to frame
    contextManager.addMessage(frame.id, 'user', input, false);
    
    // Calculate throughput metrics
    const metrics = this.calculateMetrics(input, parsedIntent);
    
    // Generate synthesis guidance
    const profile = profileManager.getOrCreateProfile(userId);
    const synthesisGuidance = this.generateSynthesisGuidance(
      parsedIntent, 
      metrics, 
      profile
    );
    
    // Create packet
    const packet: SymbolicPacket = {
      id: `packet_${Date.now()}_${Math.random().toString(36).slice(2, 11)}`,
      timestamp: new Date(),
      rawInput: input,
      parsedIntent,
      metrics,
      synthesisGuidance
    };
    
    // Store in history
    if (!this.packetHistory.has(userId)) {
      this.packetHistory.set(userId, []);
    }
    this.packetHistory.get(userId)!.push(packet);
    
    // Keep only last 50 packets per user
    const history = this.packetHistory.get(userId)!;
    if (history.length > 50) {
      this.packetHistory.set(userId, history.slice(-50));
    }
    
    return packet;
  }

  /**
   * Calculate throughput metrics for input
   */
  private calculateMetrics(input: string, parsed: ParsedIntent): ThroughputMetrics {
    const words = input.split(/\s+/).length;
    const layers = parsed.layers;
    
    // Count total symbols across all layers
    const totalSymbols = Object.values(layers)
      .reduce((sum, arr) => sum + ((arr as string[])?.length || 0), 0);
    
    // Calculate symbols per word
    const symbolsPerWord = words > 0 ? totalSymbols / words : 0;
    
    // Calculate layer diversity (how many of 6 layers are active)
    const activeLayers = Object.values(layers).filter(arr => arr && arr.length > 0).length;
    const layerDiversity = activeLayers / 6;
    
    // Calculate context switch rate
    const contextSwitchRate = words > 0 ? (parsed.metadata.contextSwitchCount / words) * 100 : 0;
    
    // Calculate recursion depth (approximate based on self-references)
    let recursionDepth = 0;
    if (parsed.metadata.hasRecursiveIntent) recursionDepth++;
    if (parsed.metadata.hasSelfReference) recursionDepth++;
    if (parsed.metadata.hasMetaCommunication) recursionDepth++;
    
    // Count parallel streams
    let parallelStreamCount = 0;
    if (parsed.metadata.hasParallelMetaphors) parallelStreamCount += 2;
    if (parsed.metadata.hasCodeLoreBlending) parallelStreamCount++;
    if (layers.mythic && layers.technical) parallelStreamCount++;
    
    // Calculate overall throughput score
    const throughputScore = Math.min(100, 
      (symbolsPerWord * 20) +
      (layerDiversity * 30) +
      (contextSwitchRate * 5) +
      (recursionDepth * 10) +
      (parallelStreamCount * 10)
    );
    
    // Determine throughput level
    let throughputLevel: 'minimal' | 'standard' | 'high' | 'extreme';
    if (throughputScore >= 70) throughputLevel = 'extreme';
    else if (throughputScore >= 45) throughputLevel = 'high';
    else if (throughputScore >= 20) throughputLevel = 'standard';
    else throughputLevel = 'minimal';
    
    return {
      symbolsPerWord,
      layerDiversity,
      contextSwitchRate,
      recursionDepth,
      parallelStreamCount,
      metaLayerPresence: parsed.metadata.hasMetaCommunication,
      throughputScore,
      throughputLevel
    };
  }

  /**
   * Generate synthesis guidance for response generation
   */
  private generateSynthesisGuidance(
    parsed: ParsedIntent,
    metrics: ThroughputMetrics,
    profile: CognitiveProfile
  ): SynthesisGuidance {
    const layers = parsed.layers;
    
    // Determine primary layer
    let primaryLayer: keyof CognitiveLayer = 'technical';
    let maxCount = 0;
    for (const [layer, values] of Object.entries(layers)) {
      const count = (values as string[])?.length || 0;
      if (count > maxCount) {
        maxCount = count;
        primaryLayer = layer as keyof CognitiveLayer;
      }
    }
    
    // Determine secondary layers
    const secondaryLayers = Object.entries(layers)
      .filter(([layer, values]) => 
        layer !== primaryLayer && values && (values as string[]).length > 0
      )
      .sort((a, b) => (b[1] as string[]).length - (a[1] as string[]).length)
      .slice(0, 2)
      .map(([layer]) => layer as keyof CognitiveLayer);
    
    // Build narrative frame if mythic layer is present
    let narrativeFrame: string | undefined;
    if (layers.mythic && layers.mythic.length > 0) {
      narrativeFrame = this.buildNarrativeFrame(layers.mythic);
    }
    
    // Collect symbols to echo
    const symbolsToEcho: string[] = [];
    if (layers.symbolic) {
      symbolsToEcho.push(...layers.symbolic.slice(0, 3));
    }
    
    // Collect metaphors to mirror
    const metaphorsToMirror: string[] = [];
    if (layers.mythic) {
      metaphorsToMirror.push(...layers.mythic.slice(0, 2));
    }
    if (layers.kinetic) {
      metaphorsToMirror.push(...layers.kinetic.slice(0, 2));
    }
    
    // Determine code/diagram inclusion
    const codeInclusionRecommended = 
      (layers.technical && layers.technical.length > 2) ||
      parsed.metadata.hasCodeLoreBlending;
    const diagramInclusionRecommended = 
      (layers.architectural && layers.architectural.length > 2) ||
      metrics.parallelStreamCount > 2;
    
    // Determine tone based on layers and profile
    let recommendedTone = 'balanced';
    if (layers.emotional && layers.emotional.length > 0) {
      recommendedTone = 'empathetic';
    } else if (layers.mythic && layers.mythic.length > 1) {
      recommendedTone = 'epic';
    } else if (layers.technical && layers.technical.length > 2) {
      recommendedTone = 'precise';
    } else if (parsed.metadata.hasHumor) {
      recommendedTone = 'playful';
    }
    
    // Determine depth based on throughput
    let recommendedDepth: 'surface' | 'analytical' | 'deep' | 'fullstack';
    if (metrics.throughputLevel === 'extreme') {
      recommendedDepth = 'fullstack';
    } else if (metrics.throughputLevel === 'high') {
      recommendedDepth = 'deep';
    } else if (metrics.throughputLevel === 'standard') {
      recommendedDepth = 'analytical';
    } else {
      recommendedDepth = 'surface';
    }
    
    // Override with profile preferences if available
    if (profile.cognitiveStyle.symbolicThroughput === 'extreme') {
      recommendedDepth = 'fullstack';
    }
    
    return {
      primaryLayer,
      secondaryLayers,
      narrativeFrame,
      symbolsToEcho,
      metaphorsToMirror,
      codeInclusionRecommended,
      diagramInclusionRecommended,
      recommendedTone,
      recommendedDepth,
      includeCognitiveReflection: metrics.metaLayerPresence,
      includeProgressMarkers: profile.activeProjects.length > 0
    };
  }

  /**
   * Build a narrative frame from mythic elements
   */
  private buildNarrativeFrame(mythicElements: string[]): string {
    const frames: Record<string, string> = {
      'sovereign': 'sovereignty narrative',
      'empire': 'empire-building narrative',
      'realm': 'domain expansion narrative',
      'quest': 'hero\'s journey narrative',
      'forge': 'creation/crafting narrative',
      'legion': 'collective action narrative',
      'phoenix': 'transformation/rebirth narrative',
      'guardian': 'protection/stewardship narrative',
      'architect': 'design/construction narrative'
    };
    
    for (const element of mythicElements) {
      if (frames[element.toLowerCase()]) {
        return frames[element.toLowerCase()];
      }
    }
    
    return 'mythic-technical hybrid narrative';
  }

  /**
   * Get throughput trend for a user
   */
  getThroughputTrend(userId: string): {
    average: number;
    trend: 'increasing' | 'stable' | 'decreasing';
    recentPackets: number;
  } {
    const history = this.packetHistory.get(userId) || [];
    if (history.length === 0) {
      return { average: 0, trend: 'stable', recentPackets: 0 };
    }
    
    const scores = history.map(p => p.metrics.throughputScore);
    const average = scores.reduce((a, b) => a + b, 0) / scores.length;
    
    // Calculate trend (compare first half to second half)
    let trend: 'increasing' | 'stable' | 'decreasing' = 'stable';
    if (scores.length >= 4) {
      const half = Math.floor(scores.length / 2);
      const firstHalf = scores.slice(0, half);
      const secondHalf = scores.slice(half);
      const firstAvg = firstHalf.reduce((a, b) => a + b, 0) / firstHalf.length;
      const secondAvg = secondHalf.reduce((a, b) => a + b, 0) / secondHalf.length;
      
      if (secondAvg > firstAvg + 5) trend = 'increasing';
      else if (secondAvg < firstAvg - 5) trend = 'decreasing';
    }
    
    return { average, trend, recentPackets: history.length };
  }

  /**
   * Generate a cognitive signature report
   */
  generateCognitiveReport(userId: string): CognitiveReport {
    const profile = profileManager.getOrCreateProfile(userId);
    const signature = profileManager.getCognitiveSignature(userId);
    const throughputTrend = this.getThroughputTrend(userId);
    const history = this.packetHistory.get(userId) || [];
    
    // Calculate layer distribution
    const layerDistribution: Record<keyof CognitiveLayer, number> = {
      mythic: 0,
      emotional: 0,
      architectural: 0,
      symbolic: 0,
      technical: 0,
      kinetic: 0
    };
    
    for (const packet of history) {
      for (const [layer, values] of Object.entries(packet.parsedIntent.layers)) {
        layerDistribution[layer as keyof CognitiveLayer] += (values as string[])?.length || 0;
      }
    }
    
    // Normalize distribution
    const total = Object.values(layerDistribution).reduce((a, b) => a + b, 0);
    const normalizedDistribution: Record<keyof CognitiveLayer, number> = {} as any;
    for (const [layer, count] of Object.entries(layerDistribution)) {
      normalizedDistribution[layer as keyof CognitiveLayer] = total > 0 ? count / total : 0;
    }
    
    // Identify unique patterns
    const uniquePatterns: string[] = [];
    if (profile.cognitiveStyle.parallelProcessing) {
      uniquePatterns.push('parallel-processing-enabled');
    }
    if (profile.cognitiveStyle.narrativeRecursion) {
      uniquePatterns.push('narrative-recursion-active');
    }
    if (throughputTrend.average > 50) {
      uniquePatterns.push('high-symbolic-bandwidth');
    }
    if (layerDistribution.mythic > layerDistribution.technical) {
      uniquePatterns.push('mythic-dominant');
    }
    if (profile.activeProjects.length > 3) {
      uniquePatterns.push('multi-project-orchestrator');
    }
    
    return {
      userId,
      displayName: profile.displayName,
      signature,
      communicationStyle: profile.cognitiveStyle,
      throughputAnalysis: {
        ...throughputTrend,
        currentLevel: history.length > 0 
          ? history[history.length - 1].metrics.throughputLevel 
          : 'minimal'
      },
      layerDistribution: normalizedDistribution,
      uniquePatterns,
      recommendations: this.generateRecommendations(profile, throughputTrend, uniquePatterns)
    };
  }

  /**
   * Generate recommendations for optimizing communication
   */
  private generateRecommendations(
    profile: CognitiveProfile,
    throughputTrend: { average: number; trend: string },
    patterns: string[]
  ): string[] {
    const recommendations: string[] = [];
    
    if (throughputTrend.average < 30) {
      recommendations.push('Consider using more symbolic references for richer communication');
    }
    
    if (!profile.cognitiveStyle.parallelProcessing && throughputTrend.average > 50) {
      recommendations.push('Your communication style suggests parallel processing capability - this can be enabled');
    }
    
    if (patterns.includes('mythic-dominant') && !patterns.includes('high-symbolic-bandwidth')) {
      recommendations.push('Strong narrative preference detected - technical overlays could enhance precision');
    }
    
    if (profile.activeProjects.length === 0) {
      recommendations.push('No active projects tracked - consider establishing project continuity markers');
    }
    
    if (profile.intentPatterns.length < 5) {
      recommendations.push('Intent pattern library is limited - more interactions will improve response accuracy');
    }
    
    return recommendations;
  }

  /**
   * Clear packet history for a user
   */
  clearHistory(userId: string): void {
    this.packetHistory.delete(userId);
  }
}

export interface CognitiveReport {
  userId: string;
  displayName: string;
  signature: {
    score: number;
    characteristics: string[];
  };
  communicationStyle: {
    parallelProcessing: boolean;
    symbolicThroughput: string;
    preferredLayers: (keyof CognitiveLayer)[];
    narrativeRecursion: boolean;
    metaCommunication: boolean;
  };
  throughputAnalysis: {
    average: number;
    trend: string;
    recentPackets: number;
    currentLevel: string;
  };
  layerDistribution: Record<keyof CognitiveLayer, number>;
  uniquePatterns: string[];
  recommendations: string[];
}

export const symbolicEngine = new SymbolicThroughputEngine();
