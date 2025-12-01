// src/priority-council/council.js
// Priority Council - Main orchestration engine for PR prioritization

import { PriorityLevel, PRStatus } from './types.js';
import { PRAnalyzer } from './pr-analyzer.js';

/**
 * PriorityCouncil - Main engine for managing PR priority queue
 */
export class PriorityCouncil {
  constructor(config = {}) {
    this.config = {
      maxQueueSize: 1000,
      autoMergeEnabled: true,
      votingEnabled: true,
      minVotesRequired: 3,
      councilMembers: [],
      impactMultipliers: {
        her_cure: 2.0,
        security: 1.5,
        research: 1.3,
        infrastructure: 1.2
      },
      ...config
    };

    this.analyzer = new PRAnalyzer(config.analyzerConfig);
    this.queue = new Map();
    this.votes = new Map();
    this.mergeHistory = [];
    this.stats = {
      totalAnalyzed: 0,
      autoMerged: 0,
      manualMerged: 0,
      rejected: 0,
      votesProcessed: 0
    };
  }

  /**
   * Add a PR to the priority queue
   */
  async addPR(pr) {
    const analysis = this.analyzer.analyzePR(pr);
    
    const queueEntry = {
      pr,
      analysis,
      status: this.determineInitialStatus(analysis),
      queuedAt: new Date().toISOString(),
      votes: {
        approve: 0,
        reject: 0,
        prioritize: 0,
        deprioritize: 0
      },
      votingOpen: this.config.votingEnabled,
      councilDecision: null
    };

    this.queue.set(pr.number, queueEntry);
    this.stats.totalAnalyzed++;

    return queueEntry;
  }

  /**
   * Add multiple PRs in bulk
   */
  async addBulkPRs(prs) {
    const results = [];
    
    for (const pr of prs) {
      const entry = await this.addPR(pr);
      results.push(entry);
    }

    // Build dependency graph after all PRs added
    this.analyzer.buildDependencyGraph(prs);

    return results;
  }

  /**
   * Determine initial status based on analysis
   */
  determineInitialStatus(analysis) {
    if (analysis.autoMergeEligible) {
      return PRStatus.AUTO_MERGEABLE;
    }

    if (analysis.dependencies.blockedBy.length > 0) {
      return PRStatus.BLOCKED;
    }

    return PRStatus.PENDING;
  }

  /**
   * Get the next PR to work on based on priority
   */
  getNext() {
    const sorted = this.getSortedQueue();
    
    for (const entry of sorted) {
      if (entry.status === PRStatus.PENDING || entry.status === PRStatus.AUTO_MERGEABLE) {
        return entry;
      }
    }

    return null;
  }

  /**
   * Get top N PRs to work on
   */
  getTopPRs(n = 10) {
    const sorted = this.getSortedQueue();
    return sorted
      .filter(entry => 
        entry.status === PRStatus.PENDING || 
        entry.status === PRStatus.AUTO_MERGEABLE
      )
      .slice(0, n);
  }

  /**
   * Get sorted queue by priority
   */
  getSortedQueue() {
    const entries = Array.from(this.queue.values());

    return entries.sort((a, b) => {
      // Priority level first
      const priorityOrder = {
        [PriorityLevel.CRITICAL]: 0,
        [PriorityLevel.HIGH]: 1,
        [PriorityLevel.MEDIUM]: 2,
        [PriorityLevel.LOW]: 3,
        [PriorityLevel.AUTO]: 4
      };

      const priorityDiff = 
        priorityOrder[a.analysis.priority] - priorityOrder[b.analysis.priority];
      
      if (priorityDiff !== 0) return priorityDiff;

      // Then by impact score
      const scoreDiff = b.analysis.impactScore - a.analysis.impactScore;
      if (scoreDiff !== 0) return scoreDiff;

      // Then by vote count (if voting enabled)
      if (this.config.votingEnabled) {
        const aVoteScore = a.votes.approve + a.votes.prioritize - a.votes.reject - a.votes.deprioritize;
        const bVoteScore = b.votes.approve + b.votes.prioritize - b.votes.reject - b.votes.deprioritize;
        return bVoteScore - aVoteScore;
      }

      // Finally by queue time (FIFO for same priority)
      return new Date(a.queuedAt) - new Date(b.queuedAt);
    });
  }

  /**
   * Get auto-merge candidates
   */
  getAutoMergeCandidates() {
    return Array.from(this.queue.values())
      .filter(entry => 
        entry.status === PRStatus.AUTO_MERGEABLE && 
        entry.analysis.autoMergeEligible
      )
      .sort((a, b) => a.analysis.impactScore - b.analysis.impactScore);
  }

  /**
   * Get blocked PRs and what blocks them
   */
  getBlockedPRs() {
    return Array.from(this.queue.values())
      .filter(entry => entry.status === PRStatus.BLOCKED)
      .map(entry => ({
        pr: entry.pr.number,
        blockedBy: entry.analysis.dependencies.blockedBy,
        analysis: entry.analysis
      }));
  }

  /**
   * Record a vote for a PR
   */
  recordVote(prNumber, voteType, voterId, weight = 1) {
    const entry = this.queue.get(prNumber);
    if (!entry) {
      throw new Error(`PR #${prNumber} not found in queue`);
    }

    if (!entry.votingOpen) {
      throw new Error(`Voting is closed for PR #${prNumber}`);
    }

    // Track individual votes
    const voteKey = `${prNumber}-${voterId}`;
    const existingVote = this.votes.get(voteKey);
    
    // Remove previous vote if exists
    if (existingVote) {
      entry.votes[existingVote.type] -= existingVote.weight;
    }

    // Record new vote
    entry.votes[voteType] = (entry.votes[voteType] || 0) + weight;
    this.votes.set(voteKey, { type: voteType, weight, timestamp: new Date().toISOString() });
    this.stats.votesProcessed++;

    // Check if vote threshold met for auto-actions
    this.checkVoteThresholds(entry);

    return entry;
  }

  /**
   * Check if vote thresholds trigger any actions
   */
  checkVoteThresholds(entry) {
    const totalVotes = entry.votes.approve + entry.votes.reject + 
                       entry.votes.prioritize + entry.votes.deprioritize;

    if (totalVotes >= this.config.minVotesRequired) {
      // Majority approve -> mark for review
      if (entry.votes.approve > entry.votes.reject) {
        entry.status = PRStatus.IN_REVIEW;
      }
      
      // Strong prioritization -> boost priority
      if (entry.votes.prioritize >= 3) {
        entry.analysis.impactScore = Math.min(100, entry.analysis.impactScore + 20);
      }
    }
  }

  /**
   * Close voting for a PR
   */
  closeVoting(prNumber) {
    const entry = this.queue.get(prNumber);
    if (entry) {
      entry.votingOpen = false;
      entry.councilDecision = this.generateCouncilDecision(entry);
    }
    return entry;
  }

  /**
   * Generate council decision based on votes
   */
  generateCouncilDecision(entry) {
    const { votes } = entry;
    const netApproval = votes.approve - votes.reject;
    const netPriority = votes.prioritize - votes.deprioritize;

    return {
      decision: netApproval >= 0 ? 'approved' : 'rejected',
      priorityAdjustment: netPriority > 0 ? 'boost' : netPriority < 0 ? 'lower' : 'maintain',
      totalVotes: votes.approve + votes.reject + votes.prioritize + votes.deprioritize,
      consensus: Math.abs(netApproval) >= 3 ? 'strong' : 'weak',
      decidedAt: new Date().toISOString()
    };
  }

  /**
   * Mark PR as merged
   */
  markMerged(prNumber, mergeType = 'manual') {
    const entry = this.queue.get(prNumber);
    if (entry) {
      entry.status = PRStatus.MERGED;
      entry.mergedAt = new Date().toISOString();
      entry.mergeType = mergeType;

      this.mergeHistory.push({
        prNumber,
        mergedAt: entry.mergedAt,
        mergeType,
        impactScore: entry.analysis.impactScore,
        priority: entry.analysis.priority
      });

      if (mergeType === 'auto') {
        this.stats.autoMerged++;
      } else {
        this.stats.manualMerged++;
      }

      // Update blocked PRs
      this.updateBlockedPRs(prNumber);
    }
    return entry;
  }

  /**
   * Update status of PRs that were blocked by the merged PR
   */
  updateBlockedPRs(mergedPRNumber) {
    for (const [prNum, entry] of this.queue.entries()) {
      const blockedBy = entry.analysis.dependencies.blockedBy;
      const idx = blockedBy.indexOf(mergedPRNumber);
      
      if (idx !== -1) {
        blockedBy.splice(idx, 1);
        
        // If no longer blocked, update status
        if (blockedBy.length === 0 && entry.status === PRStatus.BLOCKED) {
          entry.status = PRStatus.PENDING;
        }
      }
    }
  }

  /**
   * Get queue statistics
   */
  getStats() {
    const queueStats = {
      total: this.queue.size,
      byStatus: {},
      byPriority: {},
      avgImpactScore: 0
    };

    let totalScore = 0;
    for (const entry of this.queue.values()) {
      queueStats.byStatus[entry.status] = (queueStats.byStatus[entry.status] || 0) + 1;
      queueStats.byPriority[entry.analysis.priority] = 
        (queueStats.byPriority[entry.analysis.priority] || 0) + 1;
      totalScore += entry.analysis.impactScore;
    }

    queueStats.avgImpactScore = this.queue.size > 0 ? 
      Math.round(totalScore / this.queue.size) : 0;

    return {
      queue: queueStats,
      processing: this.stats,
      mergeHistory: {
        total: this.mergeHistory.length,
        recent: this.mergeHistory.slice(-10)
      }
    };
  }

  /**
   * Get priority report for Discord/API
   */
  getPriorityReport() {
    const top10 = this.getTopPRs(10);
    const autoMerge = this.getAutoMergeCandidates();
    const blocked = this.getBlockedPRs();
    const stats = this.getStats();

    return {
      summary: {
        totalInQueue: stats.queue.total,
        readyForReview: stats.queue.byStatus[PRStatus.PENDING] || 0,
        autoMergeable: autoMerge.length,
        blocked: blocked.length,
        avgImpactScore: stats.queue.avgImpactScore
      },
      whatToSolveNext: top10.map((entry, idx) => ({
        rank: idx + 1,
        prNumber: entry.pr.number,
        title: entry.pr.title,
        priority: entry.analysis.priority,
        impactScore: entry.analysis.impactScore,
        categories: entry.analysis.categories,
        recommendations: entry.analysis.recommendations
      })),
      autoMergeCandidates: autoMerge.slice(0, 5).map(entry => ({
        prNumber: entry.pr.number,
        title: entry.pr.title,
        riskLevel: entry.analysis.riskLevel
      })),
      blockedPRs: blocked,
      stats: stats.processing
    };
  }

  /**
   * Export queue for persistence
   */
  exportQueue() {
    const data = {
      queue: Array.from(this.queue.entries()),
      votes: Array.from(this.votes.entries()),
      mergeHistory: this.mergeHistory,
      stats: this.stats,
      exportedAt: new Date().toISOString()
    };
    return JSON.stringify(data, null, 2);
  }

  /**
   * Import queue from persistence
   */
  importQueue(jsonData) {
    const data = JSON.parse(jsonData);
    this.queue = new Map(data.queue);
    this.votes = new Map(data.votes);
    this.mergeHistory = data.mergeHistory;
    this.stats = data.stats;
    return this.queue.size;
  }
}

export default PriorityCouncil;
