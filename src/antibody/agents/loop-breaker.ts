/**
 * Loop Breaker Antibody
 * 
 * Layer 3: Model & Execution
 * Tracks synthesis genealogy (parent contradictions), max 3 recursive depth, circuit-breaker pattern.
 */

import BaseAntibody, { AntibodyConfig, HealthStatus, HealingAction } from './base-antibody.js';

interface LoopBreakerConfig extends AntibodyConfig {
  max_recursive_depth: number;
  genealogy_tracking: boolean;
  circuit_breaker_threshold: number;
}

interface SynthesisRecord {
  id: string;
  parent_id: string | null;
  depth: number;
  contradiction_hash: string;
  timestamp: Date;
  status: 'pending' | 'completed' | 'broken';
}

export class LoopBreaker extends BaseAntibody {
  private loopConfig: LoopBreakerConfig;
  private synthesisGenealogy: Map<string, SynthesisRecord> = new Map();
  private circuitBreakerTrips: number = 0;
  private circuitBreakerOpen: boolean = false;
  private lastCircuitReset: Date = new Date();

  constructor(config: LoopBreakerConfig) {
    super('LoopBreaker', config);
    this.loopConfig = config;
  }

  protected async checkHealth(): Promise<HealthStatus> {
    const activeRecursions = this.countActiveRecursions();
    const deepRecursions = this.countDeepRecursions();
    const loopDetected = this.detectLoops();
    
    let healthy = true;
    let message = 'Synthesis loop status nominal';
    
    if (this.circuitBreakerOpen) {
      healthy = false;
      message = `Circuit breaker OPEN - too many recursive loops detected`;
    } else if (loopDetected) {
      healthy = false;
      message = `Infinite loop detected in synthesis genealogy`;
    } else if (deepRecursions > 0) {
      message = `Warning: ${deepRecursions} synthesis chains at max depth`;
    }
    
    return {
      healthy,
      message,
      metrics: {
        active_recursions: activeRecursions,
        deep_recursions: deepRecursions,
        circuit_breaker_trips: this.circuitBreakerTrips,
        circuit_breaker_open: this.circuitBreakerOpen ? 1 : 0,
        tracked_syntheses: this.synthesisGenealogy.size
      },
      timestamp: new Date()
    };
  }

  protected async determineHealingActions(health: HealthStatus): Promise<HealingAction[]> {
    const actions: HealingAction[] = [];
    
    if (this.circuitBreakerOpen) {
      actions.push({
        type: 'circuit_break',
        target: 'synthesis_engine',
        params: { 
          action: 'halt_all',
          reason: 'Circuit breaker tripped'
        },
        timestamp: new Date()
      });
      
      actions.push({
        type: 'alert',
        target: 'ops_team',
        params: { 
          severity: 'critical',
          message: `Circuit breaker OPEN: ${this.circuitBreakerTrips} recursive loop trips`
        },
        timestamp: new Date()
      });
    } else {
      // Find and break specific deep recursions
      const deepSyntheses = this.getDeepSyntheses();
      
      for (const synthesis of deepSyntheses) {
        actions.push({
          type: 'depth_limit',
          target: synthesis.id,
          params: { 
            current_depth: synthesis.depth,
            max_depth: this.loopConfig.max_recursive_depth,
            parent_id: synthesis.parent_id
          },
          timestamp: new Date()
        });
      }
      
      if (deepSyntheses.length > 0) {
        actions.push({
          type: 'alert',
          target: 'ops_team',
          params: { 
            severity: 'warning',
            message: `Breaking ${deepSyntheses.length} deep recursion chains`
          },
          timestamp: new Date()
        });
      }
    }
    
    return actions;
  }

  protected async executeHealingAction(action: HealingAction): Promise<void> {
    switch (action.type) {
      case 'depth_limit':
        await this.executeDepthLimit(action);
        break;
      case 'circuit_break':
        await this.executeCircuitBreak(action);
        break;
      case 'alert':
        await this.executeAlert(action);
        break;
      default:
        console.log(`[LoopBreaker] Unknown action type: ${action.type}`);
    }
  }

  /**
   * Register a new synthesis for genealogy tracking
   */
  public registerSynthesis(id: string, parentId: string | null, contradictionHash: string): boolean {
    const parentRecord = parentId ? this.synthesisGenealogy.get(parentId) : null;
    const depth = parentRecord ? parentRecord.depth + 1 : 0;
    
    // Check depth limit
    if (depth >= this.loopConfig.max_recursive_depth) {
      console.log(`[LoopBreaker] Rejecting synthesis ${id}: max depth exceeded`);
      this.circuitBreakerTrips++;
      
      if (this.circuitBreakerTrips >= this.loopConfig.circuit_breaker_threshold) {
        this.circuitBreakerOpen = true;
        this.emit('circuit_breaker_open', { trips: this.circuitBreakerTrips });
      }
      
      return false;
    }
    
    // Check for loops (same contradiction being synthesized in genealogy)
    if (parentId && this.hasLoopInGenealogy(parentId, contradictionHash)) {
      console.log(`[LoopBreaker] Rejecting synthesis ${id}: loop detected`);
      this.circuitBreakerTrips++;
      return false;
    }
    
    const record: SynthesisRecord = {
      id,
      parent_id: parentId,
      depth,
      contradiction_hash: contradictionHash,
      timestamp: new Date(),
      status: 'pending'
    };
    
    this.synthesisGenealogy.set(id, record);
    return true;
  }

  /**
   * Mark a synthesis as completed
   */
  public completeSynthesis(id: string): void {
    const record = this.synthesisGenealogy.get(id);
    if (record) {
      record.status = 'completed';
    }
  }

  /**
   * Reset circuit breaker after cooldown
   */
  public resetCircuitBreaker(): void {
    const cooldownMs = 60000; // 1 minute cooldown
    const now = new Date();
    
    if (now.getTime() - this.lastCircuitReset.getTime() > cooldownMs) {
      this.circuitBreakerOpen = false;
      this.circuitBreakerTrips = 0;
      this.lastCircuitReset = now;
      console.log('[LoopBreaker] Circuit breaker reset');
      this.emit('circuit_breaker_reset', { timestamp: now });
    }
  }

  private countActiveRecursions(): number {
    let count = 0;
    const records = Array.from(this.synthesisGenealogy.values());
    for (const record of records) {
      if (record.status === 'pending' && record.depth > 0) {
        count++;
      }
    }
    return count;
  }

  private countDeepRecursions(): number {
    const maxDepth = this.loopConfig.max_recursive_depth;
    let count = 0;
    const records = Array.from(this.synthesisGenealogy.values());
    for (const record of records) {
      if (record.depth >= maxDepth - 1) {
        count++;
      }
    }
    return count;
  }

  private getDeepSyntheses(): SynthesisRecord[] {
    const maxDepth = this.loopConfig.max_recursive_depth;
    return Array.from(this.synthesisGenealogy.values())
      .filter(r => r.depth >= maxDepth - 1 && r.status === 'pending');
  }

  private detectLoops(): boolean {
    // Check for any repeated contradiction hashes in active genealogies
    const records = Array.from(this.synthesisGenealogy.values());
    for (const record of records) {
      if (record.status === 'pending' && record.parent_id) {
        if (this.hasLoopInGenealogy(record.id, record.contradiction_hash)) {
          return true;
        }
      }
    }
    return false;
  }

  private hasLoopInGenealogy(synthesisId: string, contradictionHash: string): boolean {
    const visited = new Set<string>();
    let currentId: string | null = synthesisId;
    
    while (currentId) {
      if (visited.has(currentId)) {
        return true; // Cycle detected
      }
      visited.add(currentId);
      
      const record = this.synthesisGenealogy.get(currentId);
      if (!record) break;
      
      // Check if same contradiction appears in ancestry
      if (record.parent_id) {
        const parentRecord = this.synthesisGenealogy.get(record.parent_id);
        if (parentRecord && parentRecord.contradiction_hash === contradictionHash) {
          return true;
        }
      }
      
      currentId = record.parent_id;
    }
    
    return false;
  }

  private async executeDepthLimit(action: HealingAction): Promise<void> {
    const { current_depth, max_depth, parent_id } = action.params as {
      current_depth: number;
      max_depth: number;
      parent_id: string | null;
    };
    
    const synthesisId = action.target;
    console.log(`[LoopBreaker] Breaking recursion chain for ${synthesisId} at depth ${current_depth}/${max_depth}`);
    
    const record = this.synthesisGenealogy.get(synthesisId);
    if (record) {
      record.status = 'broken';
    }
    
    this.emit('recursion_broken', {
      synthesis_id: synthesisId,
      depth: current_depth,
      parent_id,
      timestamp: new Date()
    });
  }

  private async executeCircuitBreak(action: HealingAction): Promise<void> {
    const { action: breakAction, reason } = action.params as {
      action: string;
      reason: string;
    };
    
    console.log(`[LoopBreaker] Circuit breaker action: ${breakAction} - ${reason}`);
    
    // Mark all pending syntheses as broken
    const records = Array.from(this.synthesisGenealogy.values());
    for (const record of records) {
      if (record.status === 'pending') {
        record.status = 'broken';
      }
    }
    
    this.emit('circuit_break_executed', {
      action: breakAction,
      reason,
      affected_syntheses: this.synthesisGenealogy.size,
      timestamp: new Date()
    });
  }

  private async executeAlert(action: HealingAction): Promise<void> {
    const { severity, message } = action.params as { severity: string; message: string };
    
    console.log(`[LoopBreaker] Alert [${severity}]: ${message}`);
    
    this.emit('alert', {
      severity,
      message,
      source: 'LoopBreaker',
      timestamp: new Date()
    });
  }
}

export default LoopBreaker;
