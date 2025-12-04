#!/usr/bin/env node
/**
 * SKOS Antibody System Entry Point
 * 
 * Starts the Sovereign Antibody System with all configured healing agents.
 * Run: npm run antibody or tsx src/antibody/main.ts
 */

import * as fs from 'fs/promises';
import * as path from 'path';
import * as yaml from 'js-yaml';
import { AntibodyCoordinator } from './coordinator/antibody-coordinator.js';

interface AntibodySystemConfig {
  version: string;
  system: {
    name: string;
    description: string;
  };
  coordinator: {
    port: number;
    health_check_interval_ms: number;
    failover_timeout_ms: number;
    max_concurrent_healings: number;
  };
  antibodies: Record<string, unknown>;
}

async function loadConfiguration(): Promise<AntibodySystemConfig> {
  const configPaths = [
    process.env.ANTIBODY_CONFIG_PATH,
    path.join(process.cwd(), 'src/antibody/config/antibody-config.yaml'),
    path.join(process.cwd(), 'antibody-config.yaml'),
    '/etc/skos/antibody-config.yaml'
  ];

  for (const configPath of configPaths) {
    if (!configPath) continue;
    
    try {
      const content = await fs.readFile(configPath, 'utf-8');
      const config = yaml.load(content) as AntibodySystemConfig;
      console.log(`[SKOS] Loaded configuration from: ${configPath}`);
      return config;
    } catch {
      // Try next path
    }
  }

  // Return default configuration
  console.log('[SKOS] Using default configuration');
  return {
    version: '1.0.0',
    system: {
      name: 'SKOS Antibody System',
      description: 'Sovereign self-healing infrastructure'
    },
    coordinator: {
      port: 8090,
      health_check_interval_ms: 5000,
      failover_timeout_ms: 30000,
      max_concurrent_healings: 10
    },
    antibodies: {
      thermal_sentinel: {
        enabled: true,
        check_interval_ms: 10000,
        actions: ['throttle', 'redistribute', 'alert'],
        thresholds: {
          cpu_warning: 70,
          cpu_critical: 85,
          gpu_warning: 75,
          gpu_critical: 90
        }
      },
      power_guardian: {
        enabled: true,
        check_interval_ms: 5000,
        actions: ['failover', 'alert', 'graceful_shutdown'],
        ups_integration: true,
        failover_threshold_percent: 20
      },
      storage_watcher: {
        enabled: true,
        check_interval_ms: 30000,
        actions: ['archive', 'alert', 'mirror'],
        free_space_buffer_percent: 20,
        auto_archive_days: 30,
        mirror_critical_data: true
      },
      mesh_healer: {
        enabled: true,
        check_interval_ms: 30000,
        actions: ['regenerate_config', 'restart_interface', 'failover'],
        wireguard_config_path: '/etc/wireguard',
        connectivity_timeout_ms: 5000
      },
      loop_breaker: {
        enabled: true,
        check_interval_ms: 5000,
        actions: ['depth_limit', 'circuit_break', 'alert'],
        max_recursive_depth: 3,
        genealogy_tracking: true,
        circuit_breaker_threshold: 5
      },
      output_sanitizer: {
        enabled: true,
        check_interval_ms: 1000,
        actions: ['validate', 'sanitize', 'reject'],
        ast_validation: true,
        docker_lint: true,
        sandbox_test: true
      }
    }
  };
}

async function main(): Promise<void> {
  console.log('');
  console.log('🛡️  ═══════════════════════════════════════════════════════════');
  console.log('    SKOS - StrategicKhaos Orchestration System');
  console.log('    Sovereign Antibody System v1.0.0');
  console.log('    "The system GETS STRONGER from failures. Pure antifragility."');
  console.log('═══════════════════════════════════════════════════════════════');
  console.log('');

  try {
    // Load configuration
    const config = await loadConfiguration();
    
    console.log(`[SKOS] System: ${config.system.name}`);
    console.log(`[SKOS] Version: ${config.version}`);
    console.log(`[SKOS] Coordinator Port: ${config.coordinator.port}`);
    console.log('');

    // Initialize coordinator
    const coordinator = new AntibodyCoordinator();
    
    // Initialize all antibodies from config
    await coordinator.initializeAntibodies(config.antibodies);
    
    // Setup event handlers for external notifications
    coordinator.on('alert', (alert) => {
      console.log(`[ALERT] ${alert.source}: [${alert.severity}] ${alert.message}`);
      // In production, this would send to Discord, PagerDuty, etc.
    });
    
    coordinator.on('emergency', (emergency) => {
      console.log(`[EMERGENCY] Source: ${emergency.source}`);
      console.log(`[EMERGENCY] Message: ${emergency.alert.message}`);
      console.log(`[EMERGENCY] Recommended: ${emergency.recommended_actions.join(', ')}`);
    });
    
    coordinator.on('healing_coordinated', (event) => {
      console.log(`[HEALING] Coordinated: ${event.action.type} from ${event.source}`);
    });
    
    // Start the system
    await coordinator.start();
    
    console.log('');
    console.log('🛡️  Antibody System Active');
    console.log(`   API: http://localhost:${config.coordinator.port}/health`);
    console.log(`   Metrics: http://localhost:${config.coordinator.port}/metrics`);
    console.log(`   Antibodies: http://localhost:${config.coordinator.port}/antibodies`);
    console.log('');

    // Handle shutdown gracefully
    const shutdown = async (signal: string): Promise<void> => {
      console.log(`\n[SKOS] Received ${signal}, shutting down gracefully...`);
      await coordinator.stop();
      process.exit(0);
    };

    process.on('SIGINT', () => shutdown('SIGINT'));
    process.on('SIGTERM', () => shutdown('SIGTERM'));

  } catch (error) {
    console.error('[SKOS] Failed to start:', error);
    process.exit(1);
  }
}

// Run main
main();
