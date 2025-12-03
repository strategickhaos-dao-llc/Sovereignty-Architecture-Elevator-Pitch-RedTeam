/**
 * Priority Council Module
 * 
 * "What to Solve Next" — AI-Powered PR Triage & Roadmap
 * 
 * This module provides:
 * - PR scoring and prioritization
 * - Automatic triage via GitHub webhooks
 * - Roadmap generation and dependency analysis
 * - Discord integration for notifications
 * 
 * For her. Build what matters most, fastest.
 */

// Scoring system
export {
  analyzePR,
  calculateImpactScore,
  calculateUrgencyScore,
  calculateFeasibilityScore,
  calculateFinalPriority,
  determineTier,
  getRecommendation,
  getPriorityLabel,
  isAutoMergeEligible,
  formatAnalysisEmbed,
  DEFAULT_SCORING_CONFIG,
  type PRAnalysis,
  type PRCategory,
  type PriorityTier,
  type ScoringConfig,
} from "./scoring.js";

// Roadmap generation
export {
  generateRoadmap,
  buildDependencyGraph,
  buildReverseGraph,
  findCriticalPath,
  assignToWeeks,
  findBlockedPRs,
  formatRoadmapMarkdown,
  formatRoadmapEmbed,
  topologicalSort,
  type Roadmap,
  type RoadmapEntry,
} from "./roadmap.js";

// Triage handling
export {
  createTriageHandler,
  classifyPRCategory,
  estimateComplexity,
  estimateRisk,
  calculatePRAge,
  extractDependencies,
  extractBlockers,
  formatTriageComment,
} from "./triage.js";
