// src/priority-council/index.js
// Priority Council Department - What to Solve Next
// Manages PR prioritization, voting, and auto-merge for the Strategickhaos ecosystem

import { PriorityCouncil } from './council.js';
import { PRAnalyzer } from './pr-analyzer.js';
import { VotingSystem } from './voting.js';
import { AutoMergeEngine } from './auto-merge.js';
import * as Types from './types.js';

export {
  PriorityCouncil,
  PRAnalyzer,
  VotingSystem,
  AutoMergeEngine,
  Types
};

/**
 * Create a fully configured Priority Council instance
 */
export function createPriorityCouncil(config = {}) {
  const council = new PriorityCouncil(config.council);
  const voting = new VotingSystem(council, config.voting);
  const autoMerge = new AutoMergeEngine(council, config.autoMerge);

  return {
    council,
    voting,
    autoMerge,
    
    // Convenience methods
    addPR: (pr) => council.addPR(pr),
    getNext: () => council.getNext(),
    getTopPRs: (n) => council.getTopPRs(n),
    getReport: () => council.getPriorityReport(),
    castVote: (prNumber, voterId, voteType, comment) => 
      voting.castVote(prNumber, voterId, voteType, comment),
    processAutoMerge: (callback) => autoMerge.processQueue(callback)
  };
}

export default {
  PriorityCouncil,
  PRAnalyzer,
  VotingSystem,
  AutoMergeEngine,
  Types,
  createPriorityCouncil
};
