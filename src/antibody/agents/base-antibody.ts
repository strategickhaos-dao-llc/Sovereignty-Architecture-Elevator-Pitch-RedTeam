/**
 * Base Antibody Agent
 * 
 * Foundation class for all sovereign antibody agents in the SKOS system.
 * Provides common functionality for health monitoring, healing actions,
 * and coordination with the Antibody Coordinator.
 */

import { EventEmitter } from 'events';

export interface AntibodyConfig {
  enabled: boolean;
  check_interval_ms: number;
  actions: string[];
  [key: string]: unknown;
}

export interface HealthStatus {
  healthy: boolean;
  message: string;
  metrics: Record<string, number | string>;
  timestamp: Date;
}

export interface HealingAction {
  type: string;
  target: string;
  params: Record<string, unknown>;
  timestamp: Date;
}

export interface AntibodyState {
  name: string;
  status: 'active' | 'healing' | 'inactive' | 'error';
  lastCheck: Date;
  lastHealing: Date | null;
  healingCount: number;
  health: HealthStatus;
}

export abstract class BaseAntibody extends EventEmitter {
  protected name: string;
  protected config: AntibodyConfig;
  protected state: AntibodyState;
  protected checkInterval: ReturnType<typeof setInterval> | null = null;

  constructor(name: string, config: AntibodyConfig) {
    super();
    this.name = name;
    this.config = config;
    this.state = {
      name,
      status: 'inactive',
      lastCheck: new Date(),
      lastHealing: null,
      healingCount: 0,
      health: {
        healthy: true,
        message: 'Initialized',
        metrics: {},
        timestamp: new Date()
      }
    };
  }

  /**
   * Start the antibody agent
   */
  async start(): Promise<void> {
    if (!this.config.enabled) {
      console.log(`[${this.name}] Antibody disabled, skipping start`);
      return;
    }

    console.log(`[${this.name}] Starting antibody agent...`);
    this.state.status = 'active';
    
    // Run initial check
    await this.runHealthCheck();
    
    // Start periodic checks
    this.checkInterval = setInterval(
      () => this.runHealthCheck(),
      this.config.check_interval_ms
    );
    
    this.emit('started', { name: this.name, timestamp: new Date() });
  }

  /**
   * Stop the antibody agent
   */
  async stop(): Promise<void> {
    console.log(`[${this.name}] Stopping antibody agent...`);
    
    if (this.checkInterval) {
      clearInterval(this.checkInterval);
      this.checkInterval = null;
    }
    
    this.state.status = 'inactive';
    this.emit('stopped', { name: this.name, timestamp: new Date() });
  }

  /**
   * Get current state
   */
  getState(): AntibodyState {
    return { ...this.state };
  }

  /**
   * Run a health check cycle
   */
  private async runHealthCheck(): Promise<void> {
    try {
      this.state.lastCheck = new Date();
      const health = await this.checkHealth();
      this.state.health = health;
      
      this.emit('health_check', { 
        name: this.name, 
        health,
        timestamp: new Date() 
      });
      
      if (!health.healthy) {
        console.log(`[${this.name}] Unhealthy state detected: ${health.message}`);
        await this.triggerHealing(health);
      }
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      console.error(`[${this.name}] Health check error: ${errorMessage}`);
      this.state.status = 'error';
      this.emit('error', { name: this.name, error: errorMessage });
    }
  }

  /**
   * Trigger healing actions based on health status
   */
  private async triggerHealing(health: HealthStatus): Promise<void> {
    this.state.status = 'healing';
    this.state.healingCount++;
    
    console.log(`[${this.name}] Initiating healing (count: ${this.state.healingCount})`);
    
    try {
      const actions = await this.determineHealingActions(health);
      
      for (const action of actions) {
        console.log(`[${this.name}] Executing healing action: ${action.type}`);
        this.emit('healing_action', action);
        await this.executeHealingAction(action);
      }
      
      this.state.lastHealing = new Date();
      this.state.status = 'active';
      
      this.emit('healing_complete', { 
        name: this.name,
        actions,
        timestamp: new Date() 
      });
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      console.error(`[${this.name}] Healing error: ${errorMessage}`);
      this.state.status = 'error';
      this.emit('healing_error', { name: this.name, error: errorMessage });
    }
  }

  /**
   * Abstract method: Check health of the monitored domain
   * Must be implemented by each specific antibody
   */
  protected abstract checkHealth(): Promise<HealthStatus>;

  /**
   * Abstract method: Determine healing actions based on health status
   * Must be implemented by each specific antibody
   */
  protected abstract determineHealingActions(health: HealthStatus): Promise<HealingAction[]>;

  /**
   * Abstract method: Execute a specific healing action
   * Must be implemented by each specific antibody
   */
  protected abstract executeHealingAction(action: HealingAction): Promise<void>;
}

export default BaseAntibody;
