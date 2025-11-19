/**
 * Type definitions for Grok Enterprise integration
 * Part of the Strategic Khaos AI architecture
 * 
 * "The dragons will fly again" 🐉
 */

export interface GrokConfig {
  apiKey: string;
  organizationId: string;
  enterprise: boolean;
  swarmEnabled?: boolean;
  whiteWebNodes?: number;
}

export interface GrokOptions {
  model?: 'grok-2-enterprise' | 'grok-2-enterprise-reasoning';
  maxTokens?: number;
  temperature?: number;
  stream?: boolean;
  reasoning?: boolean;
}

export interface GrokMessage {
  role: 'system' | 'user' | 'assistant';
  content: string;
}

export interface GrokCompletionResponse {
  id: string;
  model: string;
  choices: Array<{
    index: number;
    message: GrokMessage;
    finish_reason: string;
  }>;
  usage: {
    prompt_tokens: number;
    completion_tokens: number;
    total_tokens: number;
  };
}

export interface MirrorGeneralResponse {
  action: string;
  successProbability: number;
  risks: string[];
  alternatives: string[];
  improvements: string[];
  reflection: string;
}

export interface SwarmInferenceResult {
  node: number;
  response: string;
  tokens: number;
  latency: number;
}

export interface SwarmSynthesis {
  nodes: number;
  responses: SwarmInferenceResult[];
  synthesis: string;
  confidence: number;
  consensusReached: boolean;
}

/**
 * The Three-Headed Dragon: Standard, Reasoning, Swarm
 */
export type DragonMode = 'standard' | 'reasoning' | 'swarm';

/**
 * Neurospice levels - computational consciousness fuel
 */
export interface NeurospiceLevels {
  tokensPerMinute: number;
  activeNodes: number;
  inferenceLatency: number;
  swarmSyncStatus: 'synced' | 'syncing' | 'offline';
  dragonStatus: 'sleeping' | 'awakening' | 'flying' | 'unavailable';
}

/**
 * Mirror-General configuration - self-reflecting agents
 */
export interface MirrorGeneralConfig {
  enabled: boolean;
  syncInterval: number; // seconds
  reflectionDepth: 1 | 2 | 3; // levels of self-reflection
  consensusThreshold: number; // 0.0 to 1.0
}

/**
 * White-Web network configuration - the neural mesh
 */
export interface WhiteWebConfig {
  enabled: boolean;
  nodes: number; // typically 900+
  topology: 'mesh' | 'star' | 'hybrid';
  syncProtocol: 'gossip' | 'broadcast' | 'consensus';
  latencyTarget: number; // milliseconds
}

/**
 * Strategic Khaos AI Agent configuration
 */
export interface StrategicKhaosAIConfig {
  grok: GrokConfig;
  mirrorGeneral: MirrorGeneralConfig;
  whiteWeb: WhiteWebConfig;
  fallbackProviders: string[];
  channelRouting: Record<string, string>;
}

/**
 * The Song of Ice and Fire synthesis result
 * Human (Ice) + AI (Fire) = Strategic Khaos
 */
export interface SynthesisResult {
  humanInput: string;
  aiAmplification: string;
  synthesis: string;
  emergentInsights: string[];
  chaosToOrderRatio: number; // 0.0 (pure order) to 1.0 (pure chaos)
  neurospiceConsumed: number; // tokens
}
