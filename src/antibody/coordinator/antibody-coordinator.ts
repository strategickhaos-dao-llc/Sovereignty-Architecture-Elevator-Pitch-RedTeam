/**
 * Antibody Coordinator
 * 
 * Central orchestration service for the Sovereign Antibody System.
 * Coordinates all healing agents, aggregates states, decides failover strategies,
 * and executes self-healing actions across nodes.
 * 
 * This is the "immune system" for the entire sovereign infrastructure.
 */

import * as expressModule from 'express';
import type { Request, Response, Application } from 'express';
import { EventEmitter } from 'events';
import * as fs from 'fs/promises';
import * as yaml from 'js-yaml';

const express = expressModule.default || expressModule;

// Import antibody agents
import { ThermalSentinel } from '../agents/thermal-sentinel.js';
import { PowerGuardian } from '../agents/power-guardian.js';
import { StorageWatcher } from '../agents/storage-watcher.js';
import { MeshHealer } from '../agents/mesh-healer.js';
import { LoopBreaker } from '../agents/loop-breaker.js';
import { OutputSanitizer } from '../agents/output-sanitizer.js';
import type { AntibodyState, HealingAction } from '../agents/base-antibody.js';

interface CoordinatorConfig {
  port: number;
  health_check_interval_ms: number;
  failover_timeout_ms: number;
  max_concurrent_healings: number;
  nats?: {
    enabled: boolean;
    url: string;
    cluster_name: string;
  };
  metrics?: {
    enabled: boolean;
    port: number;
  };
}

interface AntibodyRegistry {
  [key: string]: {
    instance: EventEmitter;
    layer: number;
    enabled: boolean;
  };
}

interface HealingEvent {
  source: string;
  action: HealingAction;
  timestamp: Date;
  status: 'pending' | 'executing' | 'completed' | 'failed';
}

interface SystemHealth {
  overall: 'healthy' | 'degraded' | 'critical';
  layers: {
    [key: string]: {
      status: 'healthy' | 'degraded' | 'critical';
      antibodies: AntibodyState[];
    };
  };
  active_healings: number;
  last_check: Date;
}

export class AntibodyCoordinator extends EventEmitter {
  private config: CoordinatorConfig;
  private app: Application;
  private antibodies: AntibodyRegistry = {};
  private healingQueue: HealingEvent[] = [];
  private activeHealings: number = 0;
  private systemHealth: SystemHealth;
  private started: boolean = false;

  constructor(configPath?: string) {
    super();
    this.app = express();
    this.app.use(express.json());
    
    // Default config
    this.config = {
      port: 8090,
      health_check_interval_ms: 5000,
      failover_timeout_ms: 30000,
      max_concurrent_healings: 10
    };
    
    this.systemHealth = {
      overall: 'healthy',
      layers: {},
      active_healings: 0,
      last_check: new Date()
    };
    
    // Setup routes
    this.setupRoutes();
    
    // Load config if provided
    if (configPath) {
      this.loadConfig(configPath);
    }
  }

  /**
   * Load configuration from YAML file
   */
  private async loadConfig(configPath: string): Promise<void> {
    try {
      const content = await fs.readFile(configPath, 'utf-8');
      const fullConfig = yaml.load(content) as Record<string, unknown>;
      
      if (fullConfig.coordinator) {
        this.config = { ...this.config, ...fullConfig.coordinator as CoordinatorConfig };
      }
      
      console.log('[Coordinator] Configuration loaded successfully');
    } catch (error) {
      console.log('[Coordinator] Using default configuration');
    }
  }

  /**
   * Setup Express routes
   */
  private setupRoutes(): void {
    // Health check endpoint
    this.app.get('/health', (req: Request, res: Response) => {
      res.json({
        status: this.systemHealth.overall,
        timestamp: new Date().toISOString(),
        version: '1.0.0',
        antibodies: Object.keys(this.antibodies).length,
        active_healings: this.activeHealings
      });
    });

    // Detailed system health
    this.app.get('/health/detailed', (req: Request, res: Response) => {
      res.json(this.systemHealth);
    });

    // List all antibodies
    this.app.get('/antibodies', (req: Request, res: Response) => {
      const antibodiesList = Object.entries(this.antibodies).map(([name, info]) => ({
        name,
        layer: info.layer,
        enabled: info.enabled,
        state: this.getAntibodyState(name)
      }));
      res.json({ antibodies: antibodiesList });
    });

    // Get specific antibody state
    this.app.get('/antibodies/:name', (req: Request, res: Response) => {
      const name = req.params.name;
      const state = this.getAntibodyState(name);
      if (state) {
        res.json(state);
      } else {
        res.status(404).json({ error: `Antibody ${name} not found` });
      }
    });

    // Healing queue status
    this.app.get('/healing', (req: Request, res: Response) => {
      res.json({
        queue_length: this.healingQueue.length,
        active_healings: this.activeHealings,
        max_concurrent: this.config.max_concurrent_healings,
        recent_events: this.healingQueue.slice(-10)
      });
    });

    // Trigger manual healing action
    this.app.post('/healing/trigger', (req: Request, res: Response) => {
      const { antibody, action_type, target, params } = req.body;
      
      if (!antibody || !action_type) {
        return res.status(400).json({ error: 'Missing required fields: antibody, action_type' });
      }
      
      const event: HealingEvent = {
        source: antibody,
        action: {
          type: action_type,
          target: target || 'manual',
          params: params || {},
          timestamp: new Date()
        },
        timestamp: new Date(),
        status: 'pending'
      };
      
      this.queueHealing(event);
      res.json({ message: 'Healing action queued', event });
    });

    // System metrics (Prometheus format)
    this.app.get('/metrics', (req: Request, res: Response) => {
      const metrics = this.generatePrometheusMetrics();
      res.set('Content-Type', 'text/plain');
      res.send(metrics);
    });

    // Coordination API for cross-node communication
    this.app.post('/coordinate', (req: Request, res: Response) => {
      const { action, source_node, target_node, payload } = req.body;
      
      console.log(`[Coordinator] Cross-node coordination: ${action} from ${source_node} to ${target_node}`);
      
      this.emit('coordinate', { action, source_node, target_node, payload });
      res.json({ status: 'coordinated', action });
    });
  }

  /**
   * Initialize all antibody agents
   */
  public async initializeAntibodies(antibodyConfigs: Record<string, unknown>): Promise<void> {
    console.log('[Coordinator] Initializing antibody agents...');
    
    // Layer 1: Hardware Resilience
    if ((antibodyConfigs.thermal_sentinel as Record<string, unknown>)?.enabled) {
      const config = antibodyConfigs.thermal_sentinel as ConstructorParameters<typeof ThermalSentinel>[0];
      const thermal = new ThermalSentinel(config);
      this.registerAntibody('thermal_sentinel', thermal, 1);
    }
    
    if ((antibodyConfigs.power_guardian as Record<string, unknown>)?.enabled) {
      const config = antibodyConfigs.power_guardian as ConstructorParameters<typeof PowerGuardian>[0];
      const power = new PowerGuardian(config);
      this.registerAntibody('power_guardian', power, 1);
    }
    
    if ((antibodyConfigs.storage_watcher as Record<string, unknown>)?.enabled) {
      const config = antibodyConfigs.storage_watcher as ConstructorParameters<typeof StorageWatcher>[0];
      const storage = new StorageWatcher(config);
      this.registerAntibody('storage_watcher', storage, 1);
    }
    
    // Layer 2: Network & Communication
    if ((antibodyConfigs.mesh_healer as Record<string, unknown>)?.enabled) {
      const config = antibodyConfigs.mesh_healer as ConstructorParameters<typeof MeshHealer>[0];
      const mesh = new MeshHealer(config);
      this.registerAntibody('mesh_healer', mesh, 2);
    }
    
    // Layer 3: Model & Execution
    if ((antibodyConfigs.loop_breaker as Record<string, unknown>)?.enabled) {
      const config = antibodyConfigs.loop_breaker as ConstructorParameters<typeof LoopBreaker>[0];
      const loopBreaker = new LoopBreaker(config);
      this.registerAntibody('loop_breaker', loopBreaker, 3);
    }
    
    if ((antibodyConfigs.output_sanitizer as Record<string, unknown>)?.enabled) {
      const config = antibodyConfigs.output_sanitizer as ConstructorParameters<typeof OutputSanitizer>[0];
      const sanitizer = new OutputSanitizer(config);
      this.registerAntibody('output_sanitizer', sanitizer, 3);
    }
    
    console.log(`[Coordinator] Initialized ${Object.keys(this.antibodies).length} antibody agents`);
  }

  /**
   * Register an antibody agent with the coordinator
   */
  private registerAntibody(name: string, instance: EventEmitter, layer: number): void {
    this.antibodies[name] = {
      instance,
      layer,
      enabled: true
    };
    
    // Subscribe to antibody events
    instance.on('health_check', (event) => this.handleHealthCheck(name, event));
    instance.on('healing_action', (action) => this.handleHealingAction(name, action));
    instance.on('healing_complete', (event) => this.handleHealingComplete(name, event));
    instance.on('healing_error', (event) => this.handleHealingError(name, event));
    instance.on('alert', (alert) => this.handleAlert(name, alert));
    
    console.log(`[Coordinator] Registered antibody: ${name} (Layer ${layer})`);
  }

  /**
   * Start the coordinator and all antibodies
   */
  public async start(): Promise<void> {
    if (this.started) {
      console.log('[Coordinator] Already started');
      return;
    }
    
    console.log('[Coordinator] Starting Antibody Coordinator...');
    
    // Start Express server
    this.app.listen(this.config.port, () => {
      console.log(`[Coordinator] API listening on port ${this.config.port}`);
    });
    
    // Start all antibody agents
    for (const [name, info] of Object.entries(this.antibodies)) {
      if (info.enabled && 'start' in info.instance) {
        try {
          await (info.instance as { start: () => Promise<void> }).start();
          console.log(`[Coordinator] Started antibody: ${name}`);
        } catch (error) {
          console.error(`[Coordinator] Failed to start ${name}:`, error);
        }
      }
    }
    
    // Start periodic system health aggregation
    setInterval(() => this.aggregateSystemHealth(), this.config.health_check_interval_ms);
    
    // Start healing queue processor
    setInterval(() => this.processHealingQueue(), 1000);
    
    this.started = true;
    this.emit('started', { timestamp: new Date() });
    
    console.log('[Coordinator] 🛡️ Antibody Coordinator started - Sovereign immune system active');
  }

  /**
   * Stop the coordinator and all antibodies
   */
  public async stop(): Promise<void> {
    console.log('[Coordinator] Stopping Antibody Coordinator...');
    
    // Stop all antibody agents
    for (const [name, info] of Object.entries(this.antibodies)) {
      if ('stop' in info.instance) {
        try {
          await (info.instance as { stop: () => Promise<void> }).stop();
          console.log(`[Coordinator] Stopped antibody: ${name}`);
        } catch (error) {
          console.error(`[Coordinator] Error stopping ${name}:`, error);
        }
      }
    }
    
    this.started = false;
    this.emit('stopped', { timestamp: new Date() });
  }

  /**
   * Handle health check events from antibodies
   */
  private handleHealthCheck(antibodyName: string, event: { health: AntibodyState['health'] }): void {
    // Update layer health based on antibody health
    this.emit('health_update', { antibody: antibodyName, health: event.health });
  }

  /**
   * Handle healing action events from antibodies
   */
  private handleHealingAction(antibodyName: string, action: HealingAction): void {
    const event: HealingEvent = {
      source: antibodyName,
      action,
      timestamp: new Date(),
      status: 'pending'
    };
    
    this.queueHealing(event);
  }

  /**
   * Handle healing completion events
   */
  private handleHealingComplete(antibodyName: string, event: { actions: HealingAction[] }): void {
    this.activeHealings = Math.max(0, this.activeHealings - 1);
    this.emit('healing_complete', { antibody: antibodyName, ...event });
  }

  /**
   * Handle healing error events
   */
  private handleHealingError(antibodyName: string, event: { error: string }): void {
    console.error(`[Coordinator] Healing error from ${antibodyName}: ${event.error}`);
    this.activeHealings = Math.max(0, this.activeHealings - 1);
    this.emit('healing_error', { antibody: antibodyName, ...event });
  }

  /**
   * Handle alert events from antibodies
   */
  private handleAlert(antibodyName: string, alert: { severity: string; message: string }): void {
    console.log(`[Coordinator] Alert from ${antibodyName} [${alert.severity}]: ${alert.message}`);
    
    // Emit for external notification systems
    this.emit('alert', {
      source: antibodyName,
      ...alert,
      timestamp: new Date()
    });
    
    // Critical alerts trigger immediate coordination
    if (alert.severity === 'critical') {
      this.triggerEmergencyCoordination(antibodyName, alert);
    }
  }

  /**
   * Queue a healing action
   */
  private queueHealing(event: HealingEvent): void {
    this.healingQueue.push(event);
    console.log(`[Coordinator] Healing queued: ${event.action.type} from ${event.source}`);
  }

  /**
   * Process the healing queue
   */
  private processHealingQueue(): void {
    while (
      this.healingQueue.length > 0 && 
      this.activeHealings < this.config.max_concurrent_healings
    ) {
      const event = this.healingQueue.shift();
      if (event && event.status === 'pending') {
        event.status = 'executing';
        this.activeHealings++;
        
        // Coordinate the healing action
        this.coordinateHealing(event);
      }
    }
  }

  /**
   * Coordinate a healing action across the system
   */
  private async coordinateHealing(event: HealingEvent): Promise<void> {
    console.log(`[Coordinator] Coordinating healing: ${event.action.type}`);
    
    try {
      // Determine if cross-node coordination is needed
      const needsCrossNode = this.needsCrossNodeCoordination(event.action);
      
      if (needsCrossNode) {
        console.log('[Coordinator] Initiating cross-node healing coordination');
        this.emit('cross_node_healing', event);
      }
      
      event.status = 'completed';
      this.emit('healing_coordinated', event);
      
    } catch (error) {
      event.status = 'failed';
      console.error(`[Coordinator] Healing coordination failed:`, error);
    } finally {
      this.activeHealings = Math.max(0, this.activeHealings - 1);
    }
  }

  /**
   * Determine if an action needs cross-node coordination
   */
  private needsCrossNodeCoordination(action: HealingAction): boolean {
    const crossNodeTypes = ['failover', 'redistribute', 'mirror', 'coordinate'];
    return crossNodeTypes.includes(action.type);
  }

  /**
   * Trigger emergency coordination for critical alerts
   */
  private triggerEmergencyCoordination(source: string, alert: { severity: string; message: string }): void {
    console.log(`[Coordinator] ⚠️ Emergency coordination triggered by ${source}`);
    
    this.emit('emergency', {
      source,
      alert,
      timestamp: new Date(),
      recommended_actions: this.determineEmergencyActions(source)
    });
  }

  /**
   * Determine emergency actions based on the alert source
   */
  private determineEmergencyActions(source: string): string[] {
    const actions: string[] = [];
    
    switch (source) {
      case 'thermal_sentinel':
        actions.push('throttle_all_inference');
        actions.push('activate_secondary_node');
        break;
      case 'power_guardian':
        actions.push('initiate_failover');
        actions.push('save_all_state');
        break;
      case 'mesh_healer':
        actions.push('switch_to_direct_mode');
        actions.push('regenerate_all_tunnels');
        break;
      case 'loop_breaker':
        actions.push('halt_synthesis_engine');
        actions.push('clear_synthesis_queue');
        break;
      default:
        actions.push('alert_operator');
    }
    
    return actions;
  }

  /**
   * Aggregate system health from all antibodies
   */
  private aggregateSystemHealth(): void {
    const layerHealth: SystemHealth['layers'] = {};
    let criticalCount = 0;
    let degradedCount = 0;
    
    // Organize by layer
    for (const [name, info] of Object.entries(this.antibodies)) {
      const layerKey = `layer_${info.layer}`;
      
      if (!layerHealth[layerKey]) {
        layerHealth[layerKey] = {
          status: 'healthy',
          antibodies: []
        };
      }
      
      const state = this.getAntibodyState(name);
      if (state) {
        layerHealth[layerKey].antibodies.push(state);
        
        if (!state.health.healthy) {
          if (state.status === 'error') {
            criticalCount++;
            layerHealth[layerKey].status = 'critical';
          } else {
            degradedCount++;
            if (layerHealth[layerKey].status !== 'critical') {
              layerHealth[layerKey].status = 'degraded';
            }
          }
        }
      }
    }
    
    // Determine overall health
    let overall: 'healthy' | 'degraded' | 'critical' = 'healthy';
    if (criticalCount > 0) {
      overall = 'critical';
    } else if (degradedCount > 0) {
      overall = 'degraded';
    }
    
    this.systemHealth = {
      overall,
      layers: layerHealth,
      active_healings: this.activeHealings,
      last_check: new Date()
    };
  }

  /**
   * Get state of a specific antibody
   */
  private getAntibodyState(name: string): AntibodyState | null {
    const info = this.antibodies[name];
    if (info && 'getState' in info.instance) {
      return (info.instance as { getState: () => AntibodyState }).getState();
    }
    return null;
  }

  /**
   * Generate Prometheus metrics
   */
  private generatePrometheusMetrics(): string {
    const lines: string[] = [
      '# HELP skos_antibody_system_health Overall system health (1=healthy, 0.5=degraded, 0=critical)',
      '# TYPE skos_antibody_system_health gauge',
      `skos_antibody_system_health ${this.systemHealth.overall === 'healthy' ? 1 : this.systemHealth.overall === 'degraded' ? 0.5 : 0}`,
      '',
      '# HELP skos_active_healings Number of active healing operations',
      '# TYPE skos_active_healings gauge',
      `skos_active_healings ${this.activeHealings}`,
      '',
      '# HELP skos_healing_queue_length Number of pending healing operations',
      '# TYPE skos_healing_queue_length gauge',
      `skos_healing_queue_length ${this.healingQueue.length}`,
      '',
      '# HELP skos_antibodies_total Total number of registered antibodies',
      '# TYPE skos_antibodies_total gauge',
      `skos_antibodies_total ${Object.keys(this.antibodies).length}`,
    ];
    
    // Per-antibody metrics
    for (const [name, info] of Object.entries(this.antibodies)) {
      const state = this.getAntibodyState(name);
      if (state) {
        lines.push(`skos_antibody_healthy{name="${name}",layer="${info.layer}"} ${state.health.healthy ? 1 : 0}`);
        lines.push(`skos_antibody_healing_count{name="${name}",layer="${info.layer}"} ${state.healingCount}`);
      }
    }
    
    return lines.join('\n');
  }
}

export default AntibodyCoordinator;
