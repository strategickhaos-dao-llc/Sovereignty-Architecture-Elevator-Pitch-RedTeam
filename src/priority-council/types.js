// src/priority-council/types.js
// Type definitions and enums for Priority Council Department

/**
 * PR Priority Levels
 */
export const PriorityLevel = {
  CRITICAL: 'critical',     // Urgent - Her Cure impact, security fixes
  HIGH: 'high',             // High impact - core functionality
  MEDIUM: 'medium',         // Standard priority
  LOW: 'low',               // Minor changes, documentation
  AUTO: 'auto'              // Auto-merge candidates
};

/**
 * PR Categories for impact scoring
 */
export const PRCategory = {
  HER_CURE: 'her_cure',           // Direct Her Cure research impact
  RESEARCH: 'research',           // General research capabilities
  INFRASTRUCTURE: 'infrastructure', // Core infrastructure
  AI_AGENTS: 'ai_agents',         // AI/ML agent improvements
  SECURITY: 'security',           // Security enhancements
  DOCUMENTATION: 'documentation', // Docs and README updates
  REFACTOR: 'refactor',           // Code refactoring
  BUGFIX: 'bugfix',               // Bug fixes
  FEATURE: 'feature',             // New features
  DEPENDENCY: 'dependency'        // Dependency updates
};

/**
 * PR Status in the priority queue
 */
export const PRStatus = {
  PENDING: 'pending',
  IN_REVIEW: 'in_review',
  APPROVED: 'approved',
  BLOCKED: 'blocked',
  AUTO_MERGEABLE: 'auto_mergeable',
  MERGED: 'merged',
  CLOSED: 'closed'
};

/**
 * Vote types for community voting
 */
export const VoteType = {
  APPROVE: 'approve',
  REJECT: 'reject',
  ABSTAIN: 'abstain',
  PRIORITIZE: 'prioritize',
  DEPRIORITIZE: 'deprioritize'
};

/**
 * Impact areas for scoring
 */
export const ImpactArea = {
  HER_CURE_RESEARCH: 'her_cure_research',
  AUTONOMOUS_LEARNING: 'autonomous_learning',
  QUANTUM_COMPUTING: 'quantum_computing',
  AI_REFINEMENT: 'ai_refinement',
  VISUALIZATION: 'visualization',
  DATA_PIPELINE: 'data_pipeline',
  SECURITY_COMPLIANCE: 'security_compliance',
  COMMUNITY_TOOLS: 'community_tools'
};

/**
 * Risk levels for auto-merge decisions
 */
export const RiskLevel = {
  NONE: 'none',       // Documentation only
  LOW: 'low',         // Minor changes, well-tested
  MEDIUM: 'medium',   // Standard code changes
  HIGH: 'high',       // Core functionality changes
  CRITICAL: 'critical' // Security-sensitive changes
};

export default {
  PriorityLevel,
  PRCategory,
  PRStatus,
  VoteType,
  ImpactArea,
  RiskLevel
};
