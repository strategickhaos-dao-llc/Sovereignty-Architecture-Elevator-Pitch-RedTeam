// src/priority-council/voting.js
// Community Voting System for Priority Council

import { VoteType } from './types.js';

/**
 * VotingSystem - Manages community voting on PRs
 */
export class VotingSystem {
  constructor(council, config = {}) {
    this.council = council;
    this.config = {
      votingPeriodHours: 24,
      minVotesToClose: 5,
      weightByRole: {
        core_maintainer: 3,
        council_member: 2,
        contributor: 1.5,
        community: 1
      },
      requireVerification: false,
      allowAnonymous: false,
      discordIntegration: true,
      ...config
    };

    this.activeSessions = new Map();
    this.voterRegistry = new Map();
  }

  /**
   * Start a voting session for a PR
   */
  startVotingSession(prNumber, options = {}) {
    const entry = this.council.queue.get(prNumber);
    if (!entry) {
      throw new Error(`PR #${prNumber} not found in queue`);
    }

    const session = {
      prNumber,
      startedAt: new Date().toISOString(),
      expiresAt: new Date(Date.now() + this.config.votingPeriodHours * 60 * 60 * 1000).toISOString(),
      votes: new Map(),
      status: 'active',
      options: {
        allowedVoteTypes: [VoteType.APPROVE, VoteType.REJECT, VoteType.PRIORITIZE, VoteType.DEPRIORITIZE],
        quorum: this.config.minVotesToClose,
        ...options
      }
    };

    this.activeSessions.set(prNumber, session);
    return session;
  }

  /**
   * Cast a vote in a session
   */
  castVote(prNumber, voterId, voteType, comment = null) {
    const session = this.activeSessions.get(prNumber);
    if (!session) {
      throw new Error(`No active voting session for PR #${prNumber}`);
    }

    if (session.status !== 'active') {
      throw new Error(`Voting session for PR #${prNumber} is ${session.status}`);
    }

    if (new Date() > new Date(session.expiresAt)) {
      session.status = 'expired';
      throw new Error(`Voting session for PR #${prNumber} has expired`);
    }

    if (!session.options.allowedVoteTypes.includes(voteType)) {
      throw new Error(`Vote type '${voteType}' not allowed for this session`);
    }

    // Get voter weight
    const voterInfo = this.voterRegistry.get(voterId) || { role: 'community' };
    const weight = this.config.weightByRole[voterInfo.role] || 1;

    // Record vote
    const vote = {
      voterId,
      voteType,
      weight,
      comment,
      timestamp: new Date().toISOString()
    };

    session.votes.set(voterId, vote);

    // Update council queue
    this.council.recordVote(prNumber, voteType, voterId, weight);

    // Check if quorum reached
    if (session.votes.size >= session.options.quorum) {
      this.checkAutoClose(session);
    }

    return vote;
  }

  /**
   * Check if session should auto-close
   */
  checkAutoClose(session) {
    const votes = Array.from(session.votes.values());
    const approves = votes.filter(v => v.voteType === VoteType.APPROVE).reduce((sum, v) => sum + v.weight, 0);
    const rejects = votes.filter(v => v.voteType === VoteType.REJECT).reduce((sum, v) => sum + v.weight, 0);

    // Strong consensus - auto close
    if (approves >= 5 || rejects >= 5) {
      session.status = 'closed';
      session.result = approves > rejects ? 'approved' : 'rejected';
      session.closedAt = new Date().toISOString();
    }
  }

  /**
   * Close a voting session manually
   */
  closeSession(prNumber) {
    const session = this.activeSessions.get(prNumber);
    if (!session) {
      throw new Error(`No active voting session for PR #${prNumber}`);
    }

    const votes = Array.from(session.votes.values());
    const results = this.tallyVotes(votes);

    session.status = 'closed';
    session.closedAt = new Date().toISOString();
    session.result = results.decision;
    session.tally = results;

    // Update council decision
    this.council.closeVoting(prNumber);

    return session;
  }

  /**
   * Tally votes and determine result
   */
  tallyVotes(votes) {
    const tally = {
      approve: 0,
      reject: 0,
      prioritize: 0,
      deprioritize: 0,
      abstain: 0
    };

    for (const vote of votes) {
      const voteType = vote.voteType;
      if (voteType in tally) {
        tally[voteType] += vote.weight;
      }
    }

    const netApproval = tally.approve - tally.reject;
    const netPriority = tally.prioritize - tally.deprioritize;

    return {
      tally,
      totalVoters: votes.length,
      totalWeight: votes.reduce((sum, v) => sum + v.weight, 0),
      netApproval,
      netPriority,
      decision: netApproval >= 0 ? 'approved' : 'rejected',
      priorityChange: netPriority > 0 ? 'boost' : netPriority < 0 ? 'lower' : 'unchanged',
      consensus: Math.abs(netApproval) >= 3 ? 'strong' : 'weak'
    };
  }

  /**
   * Register a voter with their role
   */
  registerVoter(voterId, role, metadata = {}) {
    this.voterRegistry.set(voterId, {
      role,
      registeredAt: new Date().toISOString(),
      ...metadata
    });
  }

  /**
   * Get active sessions
   */
  getActiveSessions() {
    const now = new Date();
    const active = [];

    for (const [prNumber, session] of this.activeSessions.entries()) {
      if (session.status === 'active' && new Date(session.expiresAt) > now) {
        active.push({
          prNumber,
          votesCount: session.votes.size,
          quorum: session.options.quorum,
          timeRemaining: new Date(session.expiresAt) - now,
          expiresAt: session.expiresAt
        });
      }
    }

    return active;
  }

  /**
   * Get session results for display
   */
  getSessionResults(prNumber) {
    const session = this.activeSessions.get(prNumber);
    if (!session) {
      return null;
    }

    const votes = Array.from(session.votes.values());
    const currentTally = this.tallyVotes(votes);

    return {
      prNumber,
      status: session.status,
      startedAt: session.startedAt,
      expiresAt: session.expiresAt,
      closedAt: session.closedAt,
      result: session.result,
      currentTally,
      voters: votes.map(v => ({
        voterId: this.config.allowAnonymous ? 'anonymous' : v.voterId,
        voteType: v.voteType,
        comment: v.comment,
        timestamp: v.timestamp
      }))
    };
  }

  /**
   * Generate Discord embed for voting
   */
  generateDiscordEmbed(prNumber) {
    const session = this.activeSessions.get(prNumber);
    if (!session) return null;

    const entry = this.council.queue.get(prNumber);
    const results = this.getSessionResults(prNumber);

    return {
      title: `🗳️ Vote on PR #${prNumber}`,
      description: entry ? entry.pr.title : 'Unknown PR',
      color: session.status === 'active' ? 0x00ff00 : 0xff0000,
      fields: [
        {
          name: 'Impact Score',
          value: entry ? `${entry.analysis.impactScore}/100` : 'N/A',
          inline: true
        },
        {
          name: 'Current Priority',
          value: entry ? entry.analysis.priority.toUpperCase() : 'N/A',
          inline: true
        },
        {
          name: 'Status',
          value: session.status.toUpperCase(),
          inline: true
        },
        {
          name: 'Votes',
          value: `✅ Approve: ${results.currentTally.tally.approve || 0}\n` +
                 `❌ Reject: ${results.currentTally.tally.reject || 0}\n` +
                 `⬆️ Prioritize: ${results.currentTally.tally.prioritize || 0}\n` +
                 `⬇️ Deprioritize: ${results.currentTally.tally.deprioritize || 0}`,
          inline: false
        },
        {
          name: 'Instructions',
          value: 'React with:\n✅ to approve\n❌ to reject\n⬆️ to boost priority\n⬇️ to lower priority',
          inline: false
        }
      ],
      footer: {
        text: session.status === 'active' 
          ? `Expires: ${new Date(session.expiresAt).toLocaleString()}`
          : `Closed: ${new Date(session.closedAt).toLocaleString()}`
      }
    };
  }
}

export default VotingSystem;
