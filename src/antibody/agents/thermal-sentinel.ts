/**
 * Thermal Sentinel Antibody
 * 
 * Layer 1: Hardware Resilience
 * Monitors CPU/GPU temperatures and auto-throttles inference load,
 * redistributing workloads across nodes when thermal thresholds are exceeded.
 */

import BaseAntibody, { AntibodyConfig, HealthStatus, HealingAction } from './base-antibody.js';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

interface ThermalConfig extends AntibodyConfig {
  thresholds: {
    cpu_warning: number;
    cpu_critical: number;
    gpu_warning: number;
    gpu_critical: number;
  };
}

interface ThermalMetrics {
  cpu_temp: number;
  gpu_temp: number;
  inference_load: number;
}

export class ThermalSentinel extends BaseAntibody {
  private thermalConfig: ThermalConfig;
  private currentThrottleLevel: number = 0;

  constructor(config: ThermalConfig) {
    super('ThermalSentinel', config);
    this.thermalConfig = config;
  }

  protected async checkHealth(): Promise<HealthStatus> {
    const metrics = await this.collectThermalMetrics();
    const thresholds = this.thermalConfig.thresholds;
    
    let healthy = true;
    let message = 'Thermal levels nominal';
    
    // Check CPU temperature
    if (metrics.cpu_temp >= thresholds.cpu_critical) {
      healthy = false;
      message = `CPU temperature critical: ${metrics.cpu_temp}°C`;
    } else if (metrics.cpu_temp >= thresholds.cpu_warning) {
      message = `CPU temperature warning: ${metrics.cpu_temp}°C`;
    }
    
    // Check GPU temperature
    if (metrics.gpu_temp >= thresholds.gpu_critical) {
      healthy = false;
      message = `GPU temperature critical: ${metrics.gpu_temp}°C`;
    } else if (metrics.gpu_temp >= thresholds.gpu_warning && healthy) {
      message = `GPU temperature warning: ${metrics.gpu_temp}°C`;
    }
    
    return {
      healthy,
      message,
      metrics: {
        cpu_temp: metrics.cpu_temp,
        gpu_temp: metrics.gpu_temp,
        inference_load: metrics.inference_load,
        throttle_level: this.currentThrottleLevel
      },
      timestamp: new Date()
    };
  }

  protected async determineHealingActions(health: HealthStatus): Promise<HealingAction[]> {
    const actions: HealingAction[] = [];
    const cpuTemp = health.metrics.cpu_temp as number;
    const gpuTemp = health.metrics.gpu_temp as number;
    const thresholds = this.thermalConfig.thresholds;
    
    // Determine throttle action
    if (cpuTemp >= thresholds.cpu_critical || gpuTemp >= thresholds.gpu_critical) {
      actions.push({
        type: 'throttle',
        target: 'inference_engine',
        params: { level: 'aggressive', percentage: 50 },
        timestamp: new Date()
      });
      
      actions.push({
        type: 'redistribute',
        target: 'workload',
        params: { 
          source_node: 'current',
          target_preference: ['lyra', 'athena']
        },
        timestamp: new Date()
      });
      
      actions.push({
        type: 'alert',
        target: 'ops_team',
        params: { 
          severity: 'critical',
          message: `Thermal emergency: CPU=${cpuTemp}°C, GPU=${gpuTemp}°C`
        },
        timestamp: new Date()
      });
    } else if (cpuTemp >= thresholds.cpu_warning || gpuTemp >= thresholds.gpu_warning) {
      actions.push({
        type: 'throttle',
        target: 'inference_engine',
        params: { level: 'moderate', percentage: 25 },
        timestamp: new Date()
      });
      
      actions.push({
        type: 'alert',
        target: 'ops_team',
        params: { 
          severity: 'warning',
          message: `Thermal warning: CPU=${cpuTemp}°C, GPU=${gpuTemp}°C`
        },
        timestamp: new Date()
      });
    }
    
    return actions;
  }

  protected async executeHealingAction(action: HealingAction): Promise<void> {
    switch (action.type) {
      case 'throttle':
        await this.executeThrottle(action);
        break;
      case 'redistribute':
        await this.executeRedistribute(action);
        break;
      case 'alert':
        await this.executeAlert(action);
        break;
      default:
        console.log(`[ThermalSentinel] Unknown action type: ${action.type}`);
    }
  }

  private async collectThermalMetrics(): Promise<ThermalMetrics> {
    let cpuTemp = 45; // Default fallback
    let gpuTemp = 50; // Default fallback
    let inferenceLoad = 0;

    try {
      // Try to read CPU temperature from thermal zone
      const { stdout: cpuStdout } = await execAsync(
        'cat /sys/class/thermal/thermal_zone0/temp 2>/dev/null || echo "45000"'
      );
      cpuTemp = parseInt(cpuStdout.trim()) / 1000;
    } catch {
      console.log('[ThermalSentinel] Using fallback CPU temperature');
    }

    try {
      // Try to read GPU temperature via nvidia-smi
      const { stdout: gpuStdout } = await execAsync(
        'nvidia-smi --query-gpu=temperature.gpu --format=csv,noheader,nounits 2>/dev/null || echo "50"'
      );
      gpuTemp = parseInt(gpuStdout.trim()) || 50;
    } catch {
      console.log('[ThermalSentinel] Using fallback GPU temperature');
    }

    try {
      // Get system load average as proxy for inference load
      const { stdout: loadStdout } = await execAsync('cat /proc/loadavg');
      const loadAvg = parseFloat(loadStdout.split(' ')[0]);
      inferenceLoad = Math.min(loadAvg * 10, 100);
    } catch {
      inferenceLoad = 50;
    }

    return { cpu_temp: cpuTemp, gpu_temp: gpuTemp, inference_load: inferenceLoad };
  }

  private async executeThrottle(action: HealingAction): Promise<void> {
    const percentage = action.params.percentage as number;
    this.currentThrottleLevel = percentage;
    
    console.log(`[ThermalSentinel] Throttling inference to ${100 - percentage}% capacity`);
    
    // In production, this would communicate with the inference engine
    // to reduce batch sizes, add delays, or limit concurrent requests
    this.emit('throttle_applied', {
      level: action.params.level,
      percentage,
      timestamp: new Date()
    });
  }

  private async executeRedistribute(action: HealingAction): Promise<void> {
    const targets = action.params.target_preference as string[];
    
    console.log(`[ThermalSentinel] Redistributing workload to: ${targets.join(', ')}`);
    
    // In production, this would coordinate with the Antibody Coordinator
    // to shift inference requests to cooler nodes
    this.emit('workload_redistributed', {
      targets,
      timestamp: new Date()
    });
  }

  private async executeAlert(action: HealingAction): Promise<void> {
    const { severity, message } = action.params as { severity: string; message: string };
    
    console.log(`[ThermalSentinel] Alert [${severity}]: ${message}`);
    
    // Emit alert for external notification systems (Discord, PagerDuty, etc.)
    this.emit('alert', {
      severity,
      message,
      source: 'ThermalSentinel',
      timestamp: new Date()
    });
  }
}

export default ThermalSentinel;
