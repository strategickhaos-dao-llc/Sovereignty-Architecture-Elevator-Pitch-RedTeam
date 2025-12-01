// src/priority-council/auto-merge.js
// Auto-Merge Engine for Low-Risk PRs

import { RiskLevel, PRCategory, PRStatus } from './types.js';

/**
 * AutoMergeEngine - Handles automatic merging of low-risk PRs
 */
export class AutoMergeEngine {
  constructor(council, config = {}) {
    this.council = council;
    this.config = {
      enabled: true,
      maxAutoMergesPerHour: 10,
      requireCIPassing: true,
      requireApproval: true,
      minApprovals: 1,
      excludeCategories: [PRCategory.SECURITY, PRCategory.INFRASTRUCTURE],
      allowedRiskLevels: [RiskLevel.NONE, RiskLevel.LOW],
      excludeLabels: ['do-not-merge', 'needs-review', 'security'],
      includeLabels: ['auto-merge-ok', 'documentation', 'minor'],
      dryRun: false,
      notifyChannel: '#prs',
      cooldownMinutes: 5,
      ...config
    };

    this.mergeQueue = [];
    this.mergedThisHour = 0;
    this.lastMergeTime = null;
    this.history = [];

    // Reset hourly counter
    setInterval(() => {
      this.mergedThisHour = 0;
    }, 60 * 60 * 1000);
  }

  /**
   * Check if a PR is eligible for auto-merge
   */
  isEligible(pr, analysis) {
    const checks = [];

    // Check if auto-merge is enabled
    if (!this.config.enabled) {
      return { eligible: false, reason: 'Auto-merge is disabled', checks };
    }

    // Rate limit check
    if (this.mergedThisHour >= this.config.maxAutoMergesPerHour) {
      return { eligible: false, reason: 'Hourly auto-merge limit reached', checks };
    }

    // Cooldown check
    if (this.lastMergeTime) {
      const cooldownMs = this.config.cooldownMinutes * 60 * 1000;
      if (Date.now() - this.lastMergeTime < cooldownMs) {
        return { eligible: false, reason: 'Cooldown period active', checks };
      }
    }

    // Risk level check
    const riskCheck = {
      name: 'risk_level',
      passed: this.config.allowedRiskLevels.includes(analysis.riskLevel),
      value: analysis.riskLevel,
      allowed: this.config.allowedRiskLevels
    };
    checks.push(riskCheck);

    // Category check
    const hasExcludedCategory = analysis.categories.some(
      cat => this.config.excludeCategories.includes(cat)
    );
    const categoryCheck = {
      name: 'categories',
      passed: !hasExcludedCategory,
      value: analysis.categories,
      excluded: this.config.excludeCategories
    };
    checks.push(categoryCheck);

    // CI status check
    const ciPassing = pr.mergeable_state === 'clean' || 
                      pr.status?.state === 'success' ||
                      !this.config.requireCIPassing;
    const ciCheck = {
      name: 'ci_status',
      passed: ciPassing,
      value: pr.mergeable_state || pr.status?.state || 'unknown'
    };
    checks.push(ciCheck);

    // Approval check
    const approvals = pr.approvals || (pr.reviews?.filter(r => r.state === 'APPROVED').length) || 0;
    const approvalCheck = {
      name: 'approvals',
      passed: !this.config.requireApproval || approvals >= this.config.minApprovals,
      value: approvals,
      required: this.config.minApprovals
    };
    checks.push(approvalCheck);

    // Label checks
    const prLabels = (pr.labels || []).map(l => (l.name || l).toLowerCase());
    const hasExcludedLabel = prLabels.some(
      label => this.config.excludeLabels.includes(label)
    );
    const labelCheck = {
      name: 'labels',
      passed: !hasExcludedLabel,
      excludedLabels: prLabels.filter(l => this.config.excludeLabels.includes(l))
    };
    checks.push(labelCheck);

    // Determine overall eligibility
    const allPassed = checks.every(c => c.passed);
    
    return {
      eligible: allPassed,
      reason: allPassed ? 'All checks passed' : this.getFailureReason(checks),
      checks
    };
  }

  /**
   * Get the first failure reason
   */
  getFailureReason(checks) {
    const failed = checks.find(c => !c.passed);
    if (!failed) return 'Unknown';

    switch (failed.name) {
      case 'risk_level':
        return `Risk level too high: ${failed.value}`;
      case 'categories':
        return `Contains excluded category: ${failed.value.join(', ')}`;
      case 'ci_status':
        return `CI not passing: ${failed.value}`;
      case 'approvals':
        return `Insufficient approvals: ${failed.value}/${failed.required}`;
      case 'labels':
        return `Has excluded label: ${failed.excludedLabels.join(', ')}`;
      default:
        return `Check failed: ${failed.name}`;
    }
  }

  /**
   * Get all auto-merge candidates from the council queue
   */
  getCandidates() {
    const candidates = [];

    for (const entry of this.council.queue.values()) {
      if (entry.status === PRStatus.AUTO_MERGEABLE) {
        const eligibility = this.isEligible(entry.pr, entry.analysis);
        candidates.push({
          prNumber: entry.pr.number,
          title: entry.pr.title,
          analysis: entry.analysis,
          eligibility
        });
      }
    }

    return candidates.filter(c => c.eligibility.eligible);
  }

  /**
   * Add PR to auto-merge queue
   */
  queueForMerge(prNumber, reason = 'Auto-detected eligible') {
    const entry = this.council.queue.get(prNumber);
    if (!entry) {
      throw new Error(`PR #${prNumber} not found`);
    }

    const eligibility = this.isEligible(entry.pr, entry.analysis);
    if (!eligibility.eligible) {
      throw new Error(`PR #${prNumber} not eligible: ${eligibility.reason}`);
    }

    this.mergeQueue.push({
      prNumber,
      queuedAt: new Date().toISOString(),
      reason,
      eligibility
    });

    return {
      queued: true,
      position: this.mergeQueue.length,
      prNumber
    };
  }

  /**
   * Process the merge queue
   */
  async processQueue(mergeCallback) {
    if (this.mergeQueue.length === 0) {
      return { processed: 0, results: [] };
    }

    const results = [];
    const toProcess = [...this.mergeQueue];
    this.mergeQueue = [];

    for (const item of toProcess) {
      // Rate limit check
      if (this.mergedThisHour >= this.config.maxAutoMergesPerHour) {
        // Re-queue remaining items
        this.mergeQueue.push(item);
        continue;
      }

      // Re-check eligibility before merge
      const entry = this.council.queue.get(item.prNumber);
      if (!entry) {
        results.push({ prNumber: item.prNumber, success: false, reason: 'PR no longer in queue' });
        continue;
      }

      const eligibility = this.isEligible(entry.pr, entry.analysis);
      if (!eligibility.eligible) {
        results.push({ prNumber: item.prNumber, success: false, reason: eligibility.reason });
        continue;
      }

      // Execute merge
      if (this.config.dryRun) {
        results.push({
          prNumber: item.prNumber,
          success: true,
          dryRun: true,
          message: 'Would merge (dry run)'
        });
      } else {
        try {
          // Call the actual merge callback
          if (mergeCallback) {
            await mergeCallback(entry.pr);
          }

          // Update council
          this.council.markMerged(item.prNumber, 'auto');
          this.mergedThisHour++;
          this.lastMergeTime = Date.now();

          // Record history
          this.history.push({
            prNumber: item.prNumber,
            mergedAt: new Date().toISOString(),
            checks: eligibility.checks
          });

          results.push({
            prNumber: item.prNumber,
            success: true,
            message: 'Auto-merged successfully'
          });
        } catch (error) {
          results.push({
            prNumber: item.prNumber,
            success: false,
            reason: error.message
          });
        }
      }
    }

    return {
      processed: results.length,
      successful: results.filter(r => r.success).length,
      failed: results.filter(r => !r.success).length,
      results
    };
  }

  /**
   * Get auto-merge status
   */
  getStatus() {
    return {
      enabled: this.config.enabled,
      dryRun: this.config.dryRun,
      queueLength: this.mergeQueue.length,
      mergedThisHour: this.mergedThisHour,
      maxPerHour: this.config.maxAutoMergesPerHour,
      lastMergeTime: this.lastMergeTime,
      cooldownRemaining: this.lastMergeTime 
        ? Math.max(0, (this.config.cooldownMinutes * 60 * 1000) - (Date.now() - this.lastMergeTime))
        : 0,
      candidates: this.getCandidates().length,
      historyCount: this.history.length
    };
  }

  /**
   * Get merge history
   */
  getHistory(limit = 20) {
    return this.history.slice(-limit);
  }

  /**
   * Enable/disable auto-merge
   */
  setEnabled(enabled) {
    this.config.enabled = enabled;
    return { enabled: this.config.enabled };
  }

  /**
   * Set dry run mode
   */
  setDryRun(dryRun) {
    this.config.dryRun = dryRun;
    return { dryRun: this.config.dryRun };
  }

  /**
   * Generate notification for auto-merge action
   */
  generateNotification(prNumber, result) {
    const entry = this.council.queue.get(prNumber);
    const title = entry?.pr?.title || `PR #${prNumber}`;

    if (result.success) {
      return {
        title: '🤖 Auto-Merged',
        description: `PR #${prNumber}: ${title}`,
        color: 0x00ff00,
        fields: [
          { name: 'Status', value: result.dryRun ? 'Dry Run' : 'Merged', inline: true },
          { name: 'Risk Level', value: entry?.analysis?.riskLevel || 'N/A', inline: true }
        ],
        footer: { text: `Auto-merge engine | ${new Date().toLocaleString()}` }
      };
    } else {
      return {
        title: '⚠️ Auto-Merge Failed',
        description: `PR #${prNumber}: ${title}`,
        color: 0xff0000,
        fields: [
          { name: 'Reason', value: result.reason, inline: false }
        ],
        footer: { text: `Auto-merge engine | ${new Date().toLocaleString()}` }
      };
    }
  }
}

export default AutoMergeEngine;
