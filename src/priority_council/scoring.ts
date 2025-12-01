/**
 * Priority Council - PR Scoring and Triage System
 * 
 * Implements the scoring system for PR prioritization:
 * - Impact Score: How much does this help find her cure?
 * - Urgency Score: How soon do we need this?
 * - Feasibility Score: Can we actually do this?
 * - Final Priority: Weighted combination
 */

export interface PRAnalysis {
  prNumber: number;
  title: string;
  category: PRCategory;
  impactScore: number;
  urgencyScore: number;
  feasibilityScore: number;
  finalPriority: number;
  tier: PriorityTier;
  recommendation: string;
  dependencies: number[];
  blockers: string[];
  riskLevel: "low" | "medium" | "high";
  autoMergeEligible: boolean;
}

export type PRCategory =
  | "Medical/Drug Discovery"
  | "Research Tools"
  | "Visualization"
  | "Infrastructure"
  | "Documentation"
  | "Bug Fix";

export type PriorityTier =
  | "critical"
  | "high"
  | "medium"
  | "low"
  | "backlog";

export interface ScoringConfig {
  impactWeights: Record<PRCategory, number>;
  urgencyFactors: {
    gettingWorse: number;
    unblocksOtherWork: number;
    dependencyForMedicalTrial: number;
    niceToHave: number;
  };
  timeDecayPointsPerDay: number;
  priorityWeights: {
    impact: number;
    urgency: number;
    feasibility: number;
  };
  tierThresholds: Record<PriorityTier, { min?: number; max?: number }>;
}

export const DEFAULT_SCORING_CONFIG: ScoringConfig = {
  impactWeights: {
    "Medical/Drug Discovery": 100,
    "Research Tools": 80,
    "Visualization": 60,
    "Infrastructure": 40,
    "Documentation": 20,
    "Bug Fix": 50,
  },
  urgencyFactors: {
    gettingWorse: 50,
    unblocksOtherWork: 40,
    dependencyForMedicalTrial: 100,
    niceToHave: 10,
  },
  timeDecayPointsPerDay: 1,
  priorityWeights: {
    impact: 0.5,
    urgency: 0.3,
    feasibility: 0.2,
  },
  tierThresholds: {
    critical: { min: 90 },
    high: { min: 70, max: 89 },
    medium: { min: 40, max: 69 },
    low: { min: 20, max: 39 },
    backlog: { max: 19 },
  },
};

/**
 * Calculate the Impact Score based on PR category
 */
export function calculateImpactScore(
  category: PRCategory,
  config: ScoringConfig = DEFAULT_SCORING_CONFIG
): number {
  return config.impactWeights[category] || 0;
}

/**
 * Calculate the Urgency Score based on various factors
 */
export function calculateUrgencyScore(
  factors: {
    isGettingWorse?: boolean;
    unblocksOtherWork?: boolean;
    isDependencyForMedicalTrial?: boolean;
    isNiceToHave?: boolean;
    prAgeInDays?: number;
  },
  config: ScoringConfig = DEFAULT_SCORING_CONFIG
): number {
  let score = 0;

  if (factors.isGettingWorse) {
    score += config.urgencyFactors.gettingWorse;
  }
  if (factors.unblocksOtherWork) {
    score += config.urgencyFactors.unblocksOtherWork;
  }
  if (factors.isDependencyForMedicalTrial) {
    score += config.urgencyFactors.dependencyForMedicalTrial;
  }
  if (factors.isNiceToHave) {
    score += config.urgencyFactors.niceToHave;
  }

  // Time decay: older PRs get bonus points
  if (factors.prAgeInDays && factors.prAgeInDays > 0) {
    score += factors.prAgeInDays * config.timeDecayPointsPerDay;
  }

  // Cap at 100
  return Math.min(100, score);
}

/**
 * Calculate the Feasibility Score
 * Formula: (10 - complexity) × (10 - risk) / (1 + dependencies)
 */
export function calculateFeasibilityScore(
  complexity: number, // 1-10 (10 = very complex)
  risk: number, // 1-10 (10 = high risk)
  dependenciesCount: number
): number {
  // Clamp values to valid ranges
  const clampedComplexity = Math.max(1, Math.min(10, complexity));
  const clampedRisk = Math.max(1, Math.min(10, risk));
  const clampedDeps = Math.max(0, dependenciesCount);

  const rawScore =
    ((10 - clampedComplexity) * (10 - clampedRisk)) / (1 + clampedDeps);

  // Normalize to 0-100 scale
  // Max raw score is (10-1)*(10-1)/(1+0) = 81
  return Math.min(100, (rawScore / 81) * 100);
}

/**
 * Calculate Final Priority Score
 * Formula: priority = (impact × 0.5) + (urgency × 0.3) + (feasibility × 0.2)
 */
export function calculateFinalPriority(
  impactScore: number,
  urgencyScore: number,
  feasibilityScore: number,
  config: ScoringConfig = DEFAULT_SCORING_CONFIG
): number {
  const { impact, urgency, feasibility } = config.priorityWeights;
  return Math.round(
    impactScore * impact + urgencyScore * urgency + feasibilityScore * feasibility
  );
}

/**
 * Determine priority tier based on final score
 */
export function determineTier(
  finalPriority: number,
  config: ScoringConfig = DEFAULT_SCORING_CONFIG
): PriorityTier {
  const { tierThresholds } = config;

  if (finalPriority >= (tierThresholds.critical.min || 90)) {
    return "critical";
  }
  if (
    finalPriority >= (tierThresholds.high.min || 70) &&
    finalPriority <= (tierThresholds.high.max || 89)
  ) {
    return "high";
  }
  if (
    finalPriority >= (tierThresholds.medium.min || 40) &&
    finalPriority <= (tierThresholds.medium.max || 69)
  ) {
    return "medium";
  }
  if (
    finalPriority >= (tierThresholds.low.min || 20) &&
    finalPriority <= (tierThresholds.low.max || 39)
  ) {
    return "low";
  }
  return "backlog";
}

/**
 * Get recommendation based on priority tier
 */
export function getRecommendation(tier: PriorityTier): string {
  const recommendations: Record<PriorityTier, string> = {
    critical: "MERGE THIS WEEK - Critical for her cure",
    high: "Schedule for this week",
    medium: "Plan for this month",
    low: "Address when convenient",
    backlog: "Review periodically - may not be needed",
  };
  return recommendations[tier];
}

/**
 * Get GitHub label for priority tier
 */
export function getPriorityLabel(tier: PriorityTier): string {
  return `priority:${tier}`;
}

/**
 * Check if PR is eligible for auto-merge
 */
export function isAutoMergeEligible(
  analysis: {
    finalPriority: number;
    riskLevel: "low" | "medium" | "high";
    ciPassing: boolean;
    hasMergeConflicts: boolean;
    filesChanged: number;
    category: PRCategory;
  },
  config: {
    minPriority: number;
    maxRisk: "low" | "medium" | "high";
    maxFilesChanged: number;
  } = {
    minPriority: 80,
    maxRisk: "low",
    maxFilesChanged: 10,
  }
): boolean {
  const riskOrder = { low: 1, medium: 2, high: 3 };

  // Must pass all criteria
  if (analysis.finalPriority >= config.minPriority) {
    if (riskOrder[analysis.riskLevel] <= riskOrder[config.maxRisk]) {
      if (analysis.ciPassing && !analysis.hasMergeConflicts) {
        if (analysis.filesChanged <= config.maxFilesChanged) {
          return true;
        }
      }
    }
  }

  // Or pass any special criteria
  if (analysis.category === "Bug Fix" && analysis.ciPassing) {
    return true;
  }
  if (analysis.category === "Documentation" && analysis.ciPassing) {
    return true;
  }

  return false;
}

/**
 * Format PR analysis as Discord embed content
 */
export function formatAnalysisEmbed(analysis: PRAnalysis): {
  title: string;
  description: string;
  color: number;
  fields: Array<{ name: string; value: string; inline: boolean }>;
} {
  const tierColors: Record<PriorityTier, number> = {
    critical: 0xff0000, // Red
    high: 0xffa500, // Orange
    medium: 0xffff00, // Yellow
    low: 0x00ff00, // Green
    backlog: 0x808080, // Gray
  };

  const tierEmojis: Record<PriorityTier, string> = {
    critical: "🚨",
    high: "⚡",
    medium: "📊",
    low: "📝",
    backlog: "📦",
  };

  return {
    title: `${tierEmojis[analysis.tier]} PR #${analysis.prNumber}: ${analysis.title}`,
    description: `**${analysis.recommendation}**`,
    color: tierColors[analysis.tier],
    fields: [
      {
        name: "📊 Category",
        value: analysis.category,
        inline: true,
      },
      {
        name: "🎯 Impact",
        value: `${analysis.impactScore}/100`,
        inline: true,
      },
      {
        name: "⏰ Urgency",
        value: `${analysis.urgencyScore}/100`,
        inline: true,
      },
      {
        name: "✅ Feasibility",
        value: `${analysis.feasibilityScore}/100`,
        inline: true,
      },
      {
        name: "📈 Final Priority",
        value: `**${analysis.finalPriority}/100** (${analysis.tier.toUpperCase()})`,
        inline: true,
      },
      {
        name: "⚠️ Risk Level",
        value: analysis.riskLevel.toUpperCase(),
        inline: true,
      },
      {
        name: "🤖 Auto-Merge",
        value: analysis.autoMergeEligible ? "✅ Eligible" : "❌ Manual review required",
        inline: true,
      },
      ...(analysis.dependencies.length > 0
        ? [
            {
              name: "🔗 Dependencies",
              value: analysis.dependencies.map((d) => `#${d}`).join(", "),
              inline: false,
            },
          ]
        : []),
      ...(analysis.blockers.length > 0
        ? [
            {
              name: "🚫 Blockers",
              value: analysis.blockers.join("\n"),
              inline: false,
            },
          ]
        : []),
    ],
  };
}

/**
 * Analyze a PR and return full analysis
 */
export function analyzePR(params: {
  prNumber: number;
  title: string;
  category: PRCategory;
  complexity: number;
  risk: number;
  dependenciesCount: number;
  dependencies: number[];
  blockers: string[];
  urgencyFactors: {
    isGettingWorse?: boolean;
    unblocksOtherWork?: boolean;
    isDependencyForMedicalTrial?: boolean;
    isNiceToHave?: boolean;
    prAgeInDays?: number;
  };
  ciPassing: boolean;
  hasMergeConflicts: boolean;
  filesChanged: number;
}): PRAnalysis {
  const impactScore = calculateImpactScore(params.category);
  const urgencyScore = calculateUrgencyScore(params.urgencyFactors);
  const feasibilityScore = calculateFeasibilityScore(
    params.complexity,
    params.risk,
    params.dependenciesCount
  );
  const finalPriority = calculateFinalPriority(
    impactScore,
    urgencyScore,
    feasibilityScore
  );
  const tier = determineTier(finalPriority);
  const recommendation = getRecommendation(tier);

  const riskLevel: "low" | "medium" | "high" =
    params.risk <= 3 ? "low" : params.risk <= 6 ? "medium" : "high";

  const autoMergeEligible = isAutoMergeEligible({
    finalPriority,
    riskLevel,
    ciPassing: params.ciPassing,
    hasMergeConflicts: params.hasMergeConflicts,
    filesChanged: params.filesChanged,
    category: params.category,
  });

  return {
    prNumber: params.prNumber,
    title: params.title,
    category: params.category,
    impactScore,
    urgencyScore,
    feasibilityScore,
    finalPriority,
    tier,
    recommendation,
    dependencies: params.dependencies,
    blockers: params.blockers,
    riskLevel,
    autoMergeEligible,
  };
}
