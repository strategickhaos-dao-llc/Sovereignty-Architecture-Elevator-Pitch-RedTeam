/**
 * Survivorship Memory Logging Engine for Athena
 * 
 * This module implements comprehensive failure tracking and lesson extraction
 * for the Trinity Genome architecture. It captures not just what happened,
 * but why it happened, and transforms that into actionable wisdom.
 */

export interface Challenge {
  id: string;
  type: string;
  complexity: number;
  requirements: string[];
  description: string;
}

export interface ResourceSnapshot {
  cpu_percent: number;
  memory_mb: number;
  api_calls_available: number;
  concurrent_agents: number;
}

export interface ResourceUsage {
  cpu_seconds: number;
  memory_peak_mb: number;
  api_calls_used: number;
  wall_time_seconds: number;
}

export interface ErrorContext {
  error_type: string;
  error_message: string;
  stack_trace?: string;
  failed_at_step: string;
  recovery_attempted: boolean;
  recovery_successful?: boolean;
}

export interface Change {
  change_id: string;
  type: string;
  description: string;
  timestamp: string;
}

export interface SurvivorshipLog {
  // Identification
  log_id: string;
  timestamp: string; // ISO8601
  agent_id: string;
  agent_type: "nova" | "lyra";
  
  // Challenge Context
  challenge: Challenge;
  
  // Attempt Details
  attempt: {
    approach: string;
    reasoning: string; // Why this approach was chosen
    alternatives_considered: string[];
    resources_allocated: ResourceSnapshot;
    estimated_difficulty: number; // 0-10 scale
  };
  
  // Outcome
  outcome: {
    status: "success" | "failure" | "partial";
    execution_time_seconds: number;
    resources_consumed: ResourceUsage;
    quality_score?: number; // if success or partial
    failure_mode?: string; // if failure
    error_details?: ErrorContext; // if failure
  };
  
  // Learning
  lessons_extracted: {
    what_worked: string[];
    what_failed: string[];
    why_it_failed: string[];
    what_to_try_next: string[];
    generalizable_pattern: string;
  };
  
  // Context for Future Reference
  environmental_factors: {
    system_load: number; // 0-1
    concurrent_agents: number;
    time_of_day: string; // ISO8601
    recent_changes: Change[];
  };
}

export interface Pattern {
  pattern_id: string;
  pattern_type: "failure_sequence" | "environmental_trigger" | "approach_effectiveness" | "resource_correlation";
  description: string;
  confidence: number; // 0-1
  occurrences: number;
  first_seen: string;
  last_seen: string;
  related_logs: string[]; // log_ids
}

export interface Lesson {
  lesson_id: string;
  title: string;
  summary: string;
  applicability: string[]; // challenge types this applies to
  confidence: number; // 0-1
  evidence_count: number; // number of logs supporting this
  created_at: string;
  updated_at: string;
  actionable_advice: string[];
}

export interface HistoricalContext {
  similar_challenges: {
    challenge_id: string;
    similarity_score: number;
    outcome: string;
    lessons_learned: string[];
  }[];
  relevant_patterns: Pattern[];
  recommended_approaches: string[];
  approaches_to_avoid: string[];
}

export interface RiskAssessment {
  challenge_id: string;
  predicted_failure_modes: {
    mode: string;
    probability: number;
    severity: number; // 0-10
    mitigation_strategy: string;
  }[];
  overall_risk_score: number; // 0-10
  confidence: number; // 0-1
}

/**
 * The core Survivorship Memory Engine that Athena uses to capture,
 * analyze, and learn from all agent attempts.
 */
export class SurvivorshipMemoryEngine {
  private logs: Map<string, SurvivorshipLog> = new Map();
  private patterns: Map<string, Pattern> = new Map();
  private lessons: Map<string, Lesson> = new Map();
  
  constructor() {
    console.log("🧠 Athena Survivorship Memory Engine initialized");
  }
  
  /**
   * Log a complete attempt by a Nova or Lyra agent.
   * This is the primary entry point for capturing agent experiences.
   */
  logAttempt(log: SurvivorshipLog): void {
    this.logs.set(log.log_id, log);
    console.log(`📝 Logged attempt ${log.log_id}: ${log.outcome.status}`);
    
    // Trigger asynchronous analysis
    this.analyzeLogAsync(log);
  }
  
  /**
   * Extract lessons from a specific log entry.
   * This transforms raw failure data into actionable wisdom.
   */
  private async analyzeLogAsync(log: SurvivorshipLog): Promise<void> {
    // In a real implementation, this would use ML/LLM to extract patterns
    // For now, we do rule-based extraction
    
    if (log.outcome.status === "failure") {
      await this.extractFailureLessons(log);
    } else if (log.outcome.status === "success") {
      await this.extractSuccessPatterns(log);
    }
    
    // Update patterns across multiple logs
    await this.updatePatterns();
  }
  
  /**
   * Extract lessons specifically from failures.
   */
  private async extractFailureLessons(log: SurvivorshipLog): Promise<void> {
    const lessonId = `lesson-${Date.now()}-${log.log_id}`;
    
    const lesson: Lesson = {
      lesson_id: lessonId,
      title: `Avoid ${log.outcome.failure_mode} in ${log.challenge.type}`,
      summary: log.lessons_extracted.generalizable_pattern,
      applicability: [log.challenge.type],
      confidence: 0.7, // Would be computed based on evidence
      evidence_count: 1,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      actionable_advice: [
        ...log.lessons_extracted.what_to_try_next,
        `Avoid: ${log.attempt.approach}`,
      ],
    };
    
    this.lessons.set(lessonId, lesson);
    console.log(`💡 Extracted lesson: ${lesson.title}`);
  }
  
  /**
   * Extract patterns from successful attempts.
   */
  private async extractSuccessPatterns(log: SurvivorshipLog): Promise<void> {
    // Record what worked for similar challenges in the future
    const patternId = `pattern-success-${log.challenge.type}`;
    
    const existingPattern = this.patterns.get(patternId);
    
    if (existingPattern) {
      existingPattern.occurrences++;
      existingPattern.last_seen = log.timestamp;
      existingPattern.related_logs.push(log.log_id);
      existingPattern.confidence = Math.min(
        0.95,
        existingPattern.confidence + 0.05
      );
    } else {
      const pattern: Pattern = {
        pattern_id: patternId,
        pattern_type: "approach_effectiveness",
        description: `Approach '${log.attempt.approach}' works well for ${log.challenge.type}`,
        confidence: 0.6,
        occurrences: 1,
        first_seen: log.timestamp,
        last_seen: log.timestamp,
        related_logs: [log.log_id],
      };
      
      this.patterns.set(patternId, pattern);
    }
  }
  
  /**
   * Identify patterns across multiple logs.
   */
  private async updatePatterns(): Promise<void> {
    // Analyze logs to find repeated patterns
    // This would use clustering, sequence analysis, etc.
    
    const failureLogs = Array.from(this.logs.values())
      .filter(log => log.outcome.status === "failure");
    
    // Look for repeated failure modes
    const failureModes = new Map<string, number>();
    
    for (const log of failureLogs) {
      if (log.outcome.failure_mode) {
        const count = failureModes.get(log.outcome.failure_mode) || 0;
        failureModes.set(log.outcome.failure_mode, count + 1);
      }
    }
    
    // Create patterns for frequently occurring failures
    for (const [mode, count] of Array.from(failureModes.entries())) {
      if (count >= 3) { // Threshold for pattern recognition
        const patternId = `pattern-failure-${mode}`;
        
        if (!this.patterns.has(patternId)) {
          const pattern: Pattern = {
            pattern_id: patternId,
            pattern_type: "failure_sequence",
            description: `Repeated failure mode: ${mode}`,
            confidence: Math.min(0.9, 0.5 + (count * 0.1)),
            occurrences: count,
            first_seen: new Date().toISOString(),
            last_seen: new Date().toISOString(),
            related_logs: [],
          };
          
          this.patterns.set(patternId, pattern);
          console.log(`⚠️  Pattern detected: ${pattern.description} (${count} occurrences)`);
        }
      }
    }
  }
  
  /**
   * Provide historical context for a new challenge.
   * This is what Lyra queries before assigning work to Novas.
   */
  provideContext(challenge: Challenge): HistoricalContext {
    // Find similar past challenges
    const similarChallenges = Array.from(this.logs.values())
      .filter(log => log.challenge.type === challenge.type)
      .map(log => ({
        challenge_id: log.challenge.id,
        similarity_score: this.calculateSimilarity(challenge, log.challenge),
        outcome: log.outcome.status,
        lessons_learned: log.lessons_extracted.what_worked,
      }))
      .sort((a, b) => b.similarity_score - a.similarity_score)
      .slice(0, 5);
    
    // Find relevant patterns
    const relevantPatterns = Array.from(this.patterns.values())
      .filter(p => p.description.includes(challenge.type))
      .sort((a, b) => b.confidence - a.confidence);
    
    // Extract recommendations
    const recommendedApproaches = similarChallenges
      .filter(sc => sc.outcome === "success")
      .flatMap(sc => sc.lessons_learned)
      .slice(0, 3);
    
    const approachesToAvoid = Array.from(this.logs.values())
      .filter(log => 
        log.challenge.type === challenge.type && 
        log.outcome.status === "failure"
      )
      .map(log => log.attempt.approach)
      .slice(0, 3);
    
    return {
      similar_challenges: similarChallenges,
      relevant_patterns: relevantPatterns,
      recommended_approaches: recommendedApproaches,
      approaches_to_avoid: approachesToAvoid,
    };
  }
  
  /**
   * Predict likely failure modes for a new challenge.
   */
  predictFailureModes(challenge: Challenge): RiskAssessment {
    const historicalFailures = Array.from(this.logs.values())
      .filter(log => 
        log.challenge.type === challenge.type && 
        log.outcome.status === "failure"
      );
    
    const failureModeFrequency = new Map<string, number>();
    
    for (const log of historicalFailures) {
      if (log.outcome.failure_mode) {
        const count = failureModeFrequency.get(log.outcome.failure_mode) || 0;
        failureModeFrequency.set(log.outcome.failure_mode, count + 1);
      }
    }
    
    const predictedFailureModes = Array.from(failureModeFrequency.entries())
      .map(([mode, count]) => ({
        mode,
        probability: count / historicalFailures.length,
        severity: 5, // Would be computed from impact analysis
        mitigation_strategy: this.getMitigationStrategy(mode),
      }))
      .sort((a, b) => b.probability - a.probability);
    
    const overallRiskScore = predictedFailureModes.length > 0
      ? predictedFailureModes.reduce((sum, fm) => sum + (fm.probability * fm.severity), 0) / predictedFailureModes.length
      : 0;
    
    return {
      challenge_id: challenge.id,
      predicted_failure_modes: predictedFailureModes,
      overall_risk_score: overallRiskScore,
      confidence: Math.min(0.9, historicalFailures.length * 0.1),
    };
  }
  
  /**
   * Generate a learning curriculum for a new agent.
   */
  generateCurriculum(agentType: "nova" | "lyra"): Lesson[] {
    // Return the most important lessons for this agent type
    return Array.from(this.lessons.values())
      .sort((a, b) => b.confidence * b.evidence_count - a.confidence * a.evidence_count)
      .slice(0, 10);
  }
  
  /**
   * Get all logs for analysis or export.
   */
  getAllLogs(): SurvivorshipLog[] {
    return Array.from(this.logs.values());
  }
  
  /**
   * Get all identified patterns.
   */
  getAllPatterns(): Pattern[] {
    return Array.from(this.patterns.values());
  }
  
  /**
   * Get all extracted lessons.
   */
  getAllLessons(): Lesson[] {
    return Array.from(this.lessons.values());
  }
  
  /**
   * Calculate similarity between two challenges (simplified).
   */
  private calculateSimilarity(c1: Challenge, c2: Challenge): number {
    if (c1.type !== c2.type) return 0;
    
    // Simple similarity based on shared requirements
    const c1Reqs = new Set(c1.requirements);
    const c2Reqs = new Set(c2.requirements);
    const intersection = new Set(Array.from(c1Reqs).filter(r => c2Reqs.has(r)));
    const union = new Set([...Array.from(c1Reqs), ...Array.from(c2Reqs)]);
    
    return intersection.size / union.size;
  }
  
  /**
   * Get mitigation strategy for a known failure mode.
   */
  private getMitigationStrategy(failureMode: string): string {
    // In a real system, this would be learned or retrieved from a knowledge base
    const strategies: Record<string, string> = {
      "timeout": "Increase timeout or use async processing",
      "rate_limit": "Implement exponential backoff and request throttling",
      "invalid_input": "Add input validation and sanitization",
      "resource_exhaustion": "Implement resource limits and cleanup",
      "authentication_failure": "Check credentials and refresh tokens",
    };
    
    return strategies[failureMode] || "Analyze logs and implement specific mitigation";
  }
}

/**
 * Utility function to create a log entry from an agent attempt.
 */
export function createLogEntry(
  agentId: string,
  agentType: "nova" | "lyra",
  challenge: Challenge,
  approach: string,
  reasoning: string,
  outcome: SurvivorshipLog["outcome"],
  lessonsExtracted: SurvivorshipLog["lessons_extracted"],
  environmentalFactors: SurvivorshipLog["environmental_factors"]
): SurvivorshipLog {
  return {
    log_id: `log-${Date.now()}-${agentId}`,
    timestamp: new Date().toISOString(),
    agent_id: agentId,
    agent_type: agentType,
    challenge,
    attempt: {
      approach,
      reasoning,
      alternatives_considered: [],
      resources_allocated: {
        cpu_percent: 0,
        memory_mb: 0,
        api_calls_available: 100,
        concurrent_agents: 1,
      },
      estimated_difficulty: challenge.complexity,
    },
    outcome,
    lessons_extracted: lessonsExtracted,
    environmental_factors: environmentalFactors,
  };
}

// Export a singleton instance
export const athenaMemory = new SurvivorshipMemoryEngine();
