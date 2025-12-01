// src/priority-council/pr-analyzer.js
// PR Analysis and Dependency Mapping for Priority Council

import { PRCategory, ImpactArea, RiskLevel, PriorityLevel } from './types.js';

/**
 * Keywords that indicate specific categories and impact areas
 */
const CATEGORY_KEYWORDS = {
  [PRCategory.HER_CURE]: ['her cure', 'cure', 'disease', 'medical', 'health', 'treatment', 'therapy'],
  [PRCategory.RESEARCH]: ['research', 'study', 'analysis', 'experiment', 'lab', 'science'],
  [PRCategory.INFRASTRUCTURE]: ['infrastructure', 'deploy', 'kubernetes', 'docker', 'ci/cd', 'pipeline'],
  [PRCategory.AI_AGENTS]: ['ai', 'agent', 'learning', 'model', 'neural', 'ml', 'machine learning', 'llm'],
  [PRCategory.SECURITY]: ['security', 'auth', 'encryption', 'vulnerability', 'audit', 'compliance'],
  [PRCategory.DOCUMENTATION]: ['docs', 'readme', 'documentation', 'comment', 'guide'],
  [PRCategory.REFACTOR]: ['refactor', 'cleanup', 'optimize', 'reorganize', 'restructure'],
  [PRCategory.BUGFIX]: ['fix', 'bug', 'error', 'issue', 'patch', 'hotfix'],
  [PRCategory.FEATURE]: ['feature', 'add', 'implement', 'create', 'new', 'build'],
  [PRCategory.DEPENDENCY]: ['dependency', 'upgrade', 'update', 'version', 'package', 'npm', 'pip']
};

const IMPACT_KEYWORDS = {
  [ImpactArea.HER_CURE_RESEARCH]: ['her cure', 'disease model', 'personalized', 'treatment'],
  [ImpactArea.AUTONOMOUS_LEARNING]: ['autonomous', 'self-improving', 'adaptive', 'learning system'],
  [ImpactArea.QUANTUM_COMPUTING]: ['quantum', 'superposition', 'entanglement', 'qubit'],
  [ImpactArea.AI_REFINEMENT]: ['refinery', 'refinement', 'training', 'fine-tune', 'model improvement'],
  [ImpactArea.VISUALIZATION]: ['visualization', 'dashboard', 'chart', 'graph', 'real-time', 'streaming'],
  [ImpactArea.DATA_PIPELINE]: ['pipeline', 'etl', 'data flow', 'ingestion', 'processing'],
  [ImpactArea.SECURITY_COMPLIANCE]: ['security', 'compliance', 'audit', 'governance', 'policy'],
  [ImpactArea.COMMUNITY_TOOLS]: ['community', 'voting', 'council', 'collaboration', 'discord']
};

/**
 * PRAnalyzer - Analyzes pull requests for categorization, impact scoring, and dependencies
 */
export class PRAnalyzer {
  constructor(config = {}) {
    this.config = {
      impactWeights: {
        [ImpactArea.HER_CURE_RESEARCH]: 10,
        [ImpactArea.AUTONOMOUS_LEARNING]: 9,
        [ImpactArea.QUANTUM_COMPUTING]: 8,
        [ImpactArea.AI_REFINEMENT]: 8,
        [ImpactArea.VISUALIZATION]: 6,
        [ImpactArea.DATA_PIPELINE]: 7,
        [ImpactArea.SECURITY_COMPLIANCE]: 7,
        [ImpactArea.COMMUNITY_TOOLS]: 5
      },
      categoryPriorityBoost: {
        [PRCategory.HER_CURE]: 50,
        [PRCategory.SECURITY]: 30,
        [PRCategory.RESEARCH]: 25,
        [PRCategory.AI_AGENTS]: 20,
        [PRCategory.INFRASTRUCTURE]: 15,
        [PRCategory.BUGFIX]: 10,
        [PRCategory.FEATURE]: 5,
        [PRCategory.REFACTOR]: 0,
        [PRCategory.DOCUMENTATION]: -5,
        [PRCategory.DEPENDENCY]: -10
      },
      ...config
    };
    this.dependencyGraph = new Map();
  }

  /**
   * Analyze a PR and return comprehensive analysis results
   */
  analyzePR(pr) {
    const title = (pr.title || '').toLowerCase();
    const body = (pr.body || '').toLowerCase();
    const combinedText = `${title} ${body}`;
    const files = pr.files || [];

    const categories = this.detectCategories(combinedText, files);
    const impactAreas = this.detectImpactAreas(combinedText);
    const riskLevel = this.assessRiskLevel(pr, files);
    const impactScore = this.calculateImpactScore(categories, impactAreas, pr);
    const priority = this.determinePriority(impactScore, riskLevel, categories);
    const dependencies = this.detectDependencies(pr, combinedText);
    const autoMergeEligible = this.isAutoMergeEligible(riskLevel, categories, pr);

    return {
      prNumber: pr.number,
      title: pr.title,
      categories,
      impactAreas,
      riskLevel,
      impactScore,
      priority,
      dependencies,
      autoMergeEligible,
      analysisTimestamp: new Date().toISOString(),
      recommendations: this.generateRecommendations(categories, impactScore, riskLevel)
    };
  }

  /**
   * Detect categories based on PR content and files
   */
  detectCategories(text, files = []) {
    const categories = new Set();
    
    // Check text against category keywords
    for (const [category, keywords] of Object.entries(CATEGORY_KEYWORDS)) {
      if (keywords.some(keyword => text.includes(keyword))) {
        categories.add(category);
      }
    }

    // Check file patterns
    const filePatterns = {
      [PRCategory.DOCUMENTATION]: [/\.md$/i, /readme/i, /docs\//i],
      [PRCategory.INFRASTRUCTURE]: [/dockerfile/i, /\.ya?ml$/i, /k8s\//i, /\.tf$/i],
      [PRCategory.SECURITY]: [/security/i, /auth/i, /\.pem$/i],
      [PRCategory.DEPENDENCY]: [/package\.json$/i, /requirements\.txt$/i, /go\.mod$/i]
    };

    for (const file of files) {
      const filename = (file.filename || file).toLowerCase();
      for (const [category, patterns] of Object.entries(filePatterns)) {
        if (patterns.some(pattern => pattern.test(filename))) {
          categories.add(category);
        }
      }
    }

    // Default to FEATURE if no category detected
    if (categories.size === 0) {
      categories.add(PRCategory.FEATURE);
    }

    return Array.from(categories);
  }

  /**
   * Detect impact areas based on PR content
   */
  detectImpactAreas(text) {
    const impactAreas = [];

    for (const [area, keywords] of Object.entries(IMPACT_KEYWORDS)) {
      if (keywords.some(keyword => text.includes(keyword))) {
        impactAreas.push(area);
      }
    }

    return impactAreas;
  }

  /**
   * Assess risk level of PR
   */
  assessRiskLevel(pr, files = []) {
    const fileCount = files.length;
    const additions = pr.additions || 0;
    const deletions = pr.deletions || 0;
    const totalChanges = additions + deletions;

    // Documentation-only PRs
    if (files.every(f => /\.(md|txt|rst)$/i.test(f.filename || f))) {
      return RiskLevel.NONE;
    }

    // Security-sensitive files
    const securityPatterns = [/auth/i, /security/i, /\.pem$/i, /secret/i, /password/i];
    if (files.some(f => securityPatterns.some(p => p.test(f.filename || f)))) {
      return RiskLevel.CRITICAL;
    }

    // Large changes are higher risk
    if (totalChanges > 1000 || fileCount > 50) {
      return RiskLevel.HIGH;
    }

    if (totalChanges > 500 || fileCount > 20) {
      return RiskLevel.MEDIUM;
    }

    return RiskLevel.LOW;
  }

  /**
   * Calculate impact score (0-100)
   */
  calculateImpactScore(categories, impactAreas, pr) {
    let score = 0;

    // Category-based scoring
    for (const category of categories) {
      const boost = this.config.categoryPriorityBoost[category] || 0;
      score += boost;
    }

    // Impact area scoring
    for (const area of impactAreas) {
      const weight = this.config.impactWeights[area] || 1;
      score += weight * 5;
    }

    // PR engagement bonus
    const comments = pr.comments || 0;
    const reviewComments = pr.review_comments || 0;
    score += Math.min((comments + reviewComments) * 2, 20);

    // Recency bonus (newer PRs get slight boost)
    const ageInDays = (Date.now() - new Date(pr.created_at).getTime()) / (1000 * 60 * 60 * 24);
    if (ageInDays < 7) {
      score += 10;
    } else if (ageInDays < 30) {
      score += 5;
    }

    // Normalize to 0-100
    return Math.max(0, Math.min(100, score));
  }

  /**
   * Determine priority level based on analysis
   */
  determinePriority(impactScore, riskLevel, categories) {
    // Her Cure PRs are always critical
    if (categories.includes(PRCategory.HER_CURE)) {
      return PriorityLevel.CRITICAL;
    }

    // Security PRs are high priority
    if (categories.includes(PRCategory.SECURITY)) {
      return PriorityLevel.HIGH;
    }

    // Score-based priority
    if (impactScore >= 80) {
      return PriorityLevel.CRITICAL;
    } else if (impactScore >= 60) {
      return PriorityLevel.HIGH;
    } else if (impactScore >= 40) {
      return PriorityLevel.MEDIUM;
    } else if (riskLevel === RiskLevel.NONE || riskLevel === RiskLevel.LOW) {
      return PriorityLevel.AUTO;
    }

    return PriorityLevel.LOW;
  }

  /**
   * Detect dependencies between PRs
   */
  detectDependencies(pr, text) {
    const dependencies = {
      blocks: [],      // This PR blocks other PRs
      blockedBy: [],   // This PR is blocked by other PRs
      related: []      // Related PRs
    };

    // Look for PR references in the text
    const prRefPattern = /#(\d+)/g;
    let match;
    while ((match = prRefPattern.exec(text)) !== null) {
      const refNum = parseInt(match[1], 10);
      if (refNum !== pr.number) {
        dependencies.related.push(refNum);
      }
    }

    // Look for explicit dependency markers
    const blocksPattern = /blocks?\s*#?(\d+)/gi;
    const blockedByPattern = /blocked\s*by\s*#?(\d+)/gi;
    const dependsPattern = /depends\s*on\s*#?(\d+)/gi;

    while ((match = blocksPattern.exec(text)) !== null) {
      dependencies.blocks.push(parseInt(match[1], 10));
    }
    
    while ((match = blockedByPattern.exec(text)) !== null) {
      dependencies.blockedBy.push(parseInt(match[1], 10));
    }
    
    while ((match = dependsPattern.exec(text)) !== null) {
      dependencies.blockedBy.push(parseInt(match[1], 10));
    }

    return dependencies;
  }

  /**
   * Check if PR is eligible for auto-merge
   */
  isAutoMergeEligible(riskLevel, categories, pr) {
    // Must have CI passing
    const ciPassing = pr.mergeable_state === 'clean' || pr.mergeable !== false;
    
    // Must be low risk or documentation
    const lowRisk = riskLevel === RiskLevel.NONE || riskLevel === RiskLevel.LOW;
    
    // Must not be security-related
    const notSecurity = !categories.includes(PRCategory.SECURITY);
    
    // Must have at least one approval
    const hasApproval = (pr.approvals || 0) >= 1;

    return ciPassing && lowRisk && notSecurity && hasApproval;
  }

  /**
   * Generate recommendations based on analysis
   */
  generateRecommendations(categories, impactScore, riskLevel) {
    const recommendations = [];

    if (impactScore >= 80) {
      recommendations.push('🔥 HIGH IMPACT: Prioritize for immediate review');
    }

    if (categories.includes(PRCategory.HER_CURE)) {
      recommendations.push('💉 HER CURE: Direct impact on cure research - expedite');
    }

    if (categories.includes(PRCategory.SECURITY)) {
      recommendations.push('🔒 SECURITY: Requires security team review');
    }

    if (riskLevel === RiskLevel.CRITICAL) {
      recommendations.push('⚠️ CRITICAL RISK: Thorough testing required before merge');
    }

    if (riskLevel === RiskLevel.NONE) {
      recommendations.push('✅ LOW RISK: Candidate for auto-merge if CI passes');
    }

    if (categories.includes(PRCategory.DOCUMENTATION)) {
      recommendations.push('📚 DOCS: Quick win - can merge without blocking');
    }

    return recommendations;
  }

  /**
   * Build dependency graph for multiple PRs
   */
  buildDependencyGraph(prs) {
    this.dependencyGraph.clear();

    for (const pr of prs) {
      const analysis = this.analyzePR(pr);
      this.dependencyGraph.set(pr.number, {
        pr,
        analysis,
        dependencies: analysis.dependencies
      });
    }

    return this.dependencyGraph;
  }

  /**
   * Get PRs that are blocking others
   */
  getBlockingPRs() {
    const blocking = [];
    
    for (const [prNum, data] of this.dependencyGraph.entries()) {
      if (data.dependencies.blocks.length > 0) {
        blocking.push({
          prNumber: prNum,
          blocking: data.dependencies.blocks,
          analysis: data.analysis
        });
      }
    }

    return blocking.sort((a, b) => b.blocking.length - a.blocking.length);
  }

  /**
   * Get optimal merge order considering dependencies
   */
  getMergeOrder() {
    const visited = new Set();
    const order = [];

    const visit = (prNum) => {
      if (visited.has(prNum)) return;
      visited.add(prNum);

      const data = this.dependencyGraph.get(prNum);
      if (data) {
        // Visit dependencies first
        for (const depNum of data.dependencies.blockedBy) {
          visit(depNum);
        }
        order.push(prNum);
      }
    };

    // Sort by priority first, then visit
    const sortedPRs = [...this.dependencyGraph.entries()]
      .sort((a, b) => b[1].analysis.impactScore - a[1].analysis.impactScore);

    for (const [prNum] of sortedPRs) {
      visit(prNum);
    }

    return order;
  }
}

export default PRAnalyzer;
