/**
 * Power Guardian Antibody
 * 
 * Layer 1: Hardware Resilience
 * UPS integration and instant node failover. If Nova drops, Lyra picks up mid-synthesis.
 */

import BaseAntibody, { AntibodyConfig, HealthStatus, HealingAction } from './base-antibody.js';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

interface PowerConfig extends AntibodyConfig {
  ups_integration: boolean;
  failover_threshold_percent: number;
}

interface PowerMetrics {
  battery_level: number;
  on_battery: boolean;
  time_remaining_minutes: number;
  voltage: number;
}

export class PowerGuardian extends BaseAntibody {
  private powerConfig: PowerConfig;
  private lastKnownGoodState: PowerMetrics | null = null;

  constructor(config: PowerConfig) {
    super('PowerGuardian', config);
    this.powerConfig = config;
  }

  protected async checkHealth(): Promise<HealthStatus> {
    const metrics = await this.collectPowerMetrics();
    
    let healthy = true;
    let message = 'Power status nominal';
    
    // Check if on battery power
    if (metrics.on_battery) {
      message = `Running on battery: ${metrics.battery_level}% remaining`;
      
      // Check battery threshold
      if (metrics.battery_level <= this.powerConfig.failover_threshold_percent) {
        healthy = false;
        message = `Critical battery level: ${metrics.battery_level}%`;
      }
      
      // Check time remaining
      if (metrics.time_remaining_minutes < 5) {
        healthy = false;
        message = `Critical: Only ${metrics.time_remaining_minutes} minutes of battery remaining`;
      }
    }
    
    this.lastKnownGoodState = metrics;
    
    return {
      healthy,
      message,
      metrics: {
        battery_level: metrics.battery_level,
        on_battery: metrics.on_battery ? 1 : 0,
        time_remaining: metrics.time_remaining_minutes,
        voltage: metrics.voltage
      },
      timestamp: new Date()
    };
  }

  protected async determineHealingActions(health: HealthStatus): Promise<HealingAction[]> {
    const actions: HealingAction[] = [];
    const batteryLevel = health.metrics.battery_level as number;
    const timeRemaining = health.metrics.time_remaining as number;
    
    // Critical power situation - initiate failover
    if (batteryLevel <= this.powerConfig.failover_threshold_percent || timeRemaining < 5) {
      actions.push({
        type: 'failover',
        target: 'node',
        params: { 
          source: 'current',
          target: 'lyra',
          preserve_state: true,
          migrate_workload: true
        },
        timestamp: new Date()
      });
      
      actions.push({
        type: 'alert',
        target: 'ops_team',
        params: { 
          severity: 'critical',
          message: `Power emergency: Battery at ${batteryLevel}%, ${timeRemaining}min remaining. Initiating failover.`
        },
        timestamp: new Date()
      });
      
      // If critically low, prepare for graceful shutdown
      if (batteryLevel < 10 || timeRemaining < 2) {
        actions.push({
          type: 'graceful_shutdown',
          target: 'current_node',
          params: { 
            timeout_seconds: 60,
            save_state: true
          },
          timestamp: new Date()
        });
      }
    } else {
      // Warning level - just alert
      actions.push({
        type: 'alert',
        target: 'ops_team',
        params: { 
          severity: 'warning',
          message: `Power warning: Running on battery at ${batteryLevel}%`
        },
        timestamp: new Date()
      });
    }
    
    return actions;
  }

  protected async executeHealingAction(action: HealingAction): Promise<void> {
    switch (action.type) {
      case 'failover':
        await this.executeFailover(action);
        break;
      case 'graceful_shutdown':
        await this.executeGracefulShutdown(action);
        break;
      case 'alert':
        await this.executeAlert(action);
        break;
      default:
        console.log(`[PowerGuardian] Unknown action type: ${action.type}`);
    }
  }

  private async collectPowerMetrics(): Promise<PowerMetrics> {
    let batteryLevel = 100;
    let onBattery = false;
    let timeRemaining = 999;
    let voltage = 120;

    try {
      // Try to get UPS status using apcaccess (APC UPS)
      const { stdout } = await execAsync('apcaccess 2>/dev/null || echo "FALLBACK"');
      
      if (!stdout.includes('FALLBACK')) {
        const lines = stdout.split('\n');
        for (const line of lines) {
          if (line.startsWith('BCHARGE')) {
            batteryLevel = parseFloat(line.split(':')[1]) || 100;
          } else if (line.startsWith('STATUS')) {
            onBattery = line.includes('ONBATT');
          } else if (line.startsWith('TIMELEFT')) {
            timeRemaining = parseFloat(line.split(':')[1]) || 999;
          } else if (line.startsWith('LINEV')) {
            voltage = parseFloat(line.split(':')[1]) || 120;
          }
        }
      }
    } catch {
      // Try alternative: upower for laptops
      try {
        const { stdout } = await execAsync(
          'upower -i /org/freedesktop/UPower/devices/battery_BAT0 2>/dev/null || echo "FALLBACK"'
        );
        
        if (!stdout.includes('FALLBACK')) {
          if (stdout.includes('state:')) {
            onBattery = stdout.includes('discharging');
          }
          const percentMatch = stdout.match(/percentage:\s*(\d+)%/);
          if (percentMatch) {
            batteryLevel = parseInt(percentMatch[1]);
          }
          const timeMatch = stdout.match(/time to empty:\s*(\d+)/);
          if (timeMatch) {
            timeRemaining = parseInt(timeMatch[1]);
          }
        }
      } catch {
        console.log('[PowerGuardian] No UPS/battery info available, using defaults');
      }
    }

    return {
      battery_level: batteryLevel,
      on_battery: onBattery,
      time_remaining_minutes: timeRemaining,
      voltage
    };
  }

  private async executeFailover(action: HealingAction): Promise<void> {
    const { source, target, migrate_workload } = action.params as {
      source: string;
      target: string;
      migrate_workload: boolean;
    };
    
    console.log(`[PowerGuardian] Initiating failover from ${source} to ${target}`);
    
    if (migrate_workload) {
      console.log('[PowerGuardian] Migrating active workloads...');
      // In production, this would coordinate with the Antibody Coordinator
      // to migrate active synthesis jobs to the target node
    }
    
    this.emit('failover_initiated', {
      source,
      target,
      migrate_workload,
      timestamp: new Date()
    });
  }

  private async executeGracefulShutdown(action: HealingAction): Promise<void> {
    const { timeout_seconds, save_state } = action.params as {
      timeout_seconds: number;
      save_state: boolean;
    };
    
    console.log(`[PowerGuardian] Initiating graceful shutdown in ${timeout_seconds}s`);
    
    if (save_state) {
      console.log('[PowerGuardian] Saving current state before shutdown...');
      this.emit('state_saved', { timestamp: new Date() });
    }
    
    this.emit('shutdown_initiated', {
      timeout_seconds,
      save_state,
      timestamp: new Date()
    });
    
    // In production, this would trigger actual shutdown sequence
    // For now, we just emit the event for the coordinator to handle
  }

  private async executeAlert(action: HealingAction): Promise<void> {
    const { severity, message } = action.params as { severity: string; message: string };
    
    console.log(`[PowerGuardian] Alert [${severity}]: ${message}`);
    
    this.emit('alert', {
      severity,
      message,
      source: 'PowerGuardian',
      timestamp: new Date()
    });
  }
}

export default PowerGuardian;
