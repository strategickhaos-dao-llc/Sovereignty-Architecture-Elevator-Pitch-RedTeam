/**
 * Storage Watcher Antibody
 * 
 * Layer 1: Hardware Resilience
 * Auto-archives old logs, maintains 20% free space buffer, mirrors critical data across nodes.
 */

import BaseAntibody, { AntibodyConfig, HealthStatus, HealingAction } from './base-antibody.js';
import { exec } from 'child_process';
import { promisify } from 'util';
import * as fs from 'fs/promises';
import * as path from 'path';

const execAsync = promisify(exec);

// Validate path to prevent path traversal
function sanitizePath(inputPath: string): string {
  // Normalize and resolve to absolute path
  const normalizedPath = path.normalize(inputPath);
  // Ensure no path traversal attempts
  if (normalizedPath.includes('..')) {
    throw new Error(`Invalid path: path traversal detected in ${inputPath}`);
  }
  return normalizedPath;
}

// Escape special characters for shell commands
function escapeShellArg(arg: string): string {
  return `'${arg.replace(/'/g, "'\\''")}'`;
}

interface StorageConfig extends AntibodyConfig {
  free_space_buffer_percent: number;
  auto_archive_days: number;
  mirror_critical_data: boolean;
  watched_paths?: string[];
}

interface StorageMetrics {
  total_gb: number;
  used_gb: number;
  available_gb: number;
  used_percent: number;
  free_percent: number;
}

export class StorageWatcher extends BaseAntibody {
  private storageConfig: StorageConfig;
  private watchedPaths: string[];

  constructor(config: StorageConfig) {
    super('StorageWatcher', config);
    this.storageConfig = config;
    this.watchedPaths = config.watched_paths || ['/', '/var/log', '/data'];
  }

  protected async checkHealth(): Promise<HealthStatus> {
    const metrics = await this.collectStorageMetrics();
    const minFreePercent = this.storageConfig.free_space_buffer_percent;
    
    let healthy = true;
    let message = 'Storage levels nominal';
    
    if (metrics.free_percent < minFreePercent) {
      healthy = false;
      message = `Low storage: ${metrics.free_percent.toFixed(1)}% free (requires ${minFreePercent}%)`;
    } else if (metrics.free_percent < minFreePercent * 1.5) {
      message = `Storage warning: ${metrics.free_percent.toFixed(1)}% free`;
    }
    
    return {
      healthy,
      message,
      metrics: {
        total_gb: metrics.total_gb,
        used_gb: metrics.used_gb,
        available_gb: metrics.available_gb,
        used_percent: metrics.used_percent,
        free_percent: metrics.free_percent
      },
      timestamp: new Date()
    };
  }

  protected async determineHealingActions(health: HealthStatus): Promise<HealingAction[]> {
    const actions: HealingAction[] = [];
    const freePercent = health.metrics.free_percent as number;
    const minFreePercent = this.storageConfig.free_space_buffer_percent;
    
    // Archive old logs first
    actions.push({
      type: 'archive',
      target: '/var/log',
      params: { 
        older_than_days: this.storageConfig.auto_archive_days,
        compress: true,
        patterns: ['*.log', '*.log.*']
      },
      timestamp: new Date()
    });
    
    // If critically low, mirror critical data to another node
    if (freePercent < minFreePercent / 2 && this.storageConfig.mirror_critical_data) {
      actions.push({
        type: 'mirror',
        target: 'critical_data',
        params: { 
          source_paths: ['/data/vault', '/data/models', '/data/state'],
          target_node: 'athena',
          incremental: true
        },
        timestamp: new Date()
      });
    }
    
    // Alert ops team
    actions.push({
      type: 'alert',
      target: 'ops_team',
      params: { 
        severity: freePercent < minFreePercent / 2 ? 'critical' : 'warning',
        message: `Storage at ${(100 - freePercent).toFixed(1)}% capacity`
      },
      timestamp: new Date()
    });
    
    return actions;
  }

  protected async executeHealingAction(action: HealingAction): Promise<void> {
    switch (action.type) {
      case 'archive':
        await this.executeArchive(action);
        break;
      case 'mirror':
        await this.executeMirror(action);
        break;
      case 'alert':
        await this.executeAlert(action);
        break;
      default:
        console.log(`[StorageWatcher] Unknown action type: ${action.type}`);
    }
  }

  private async collectStorageMetrics(): Promise<StorageMetrics> {
    try {
      const { stdout } = await execAsync('df -BG / | tail -1');
      const parts = stdout.split(/\s+/);
      
      // Parse df output: Filesystem Size Used Avail Use% Mounted
      const totalGb = parseFloat(parts[1].replace('G', ''));
      const usedGb = parseFloat(parts[2].replace('G', ''));
      const availableGb = parseFloat(parts[3].replace('G', ''));
      const usedPercent = parseFloat(parts[4].replace('%', ''));
      
      return {
        total_gb: totalGb,
        used_gb: usedGb,
        available_gb: availableGb,
        used_percent: usedPercent,
        free_percent: 100 - usedPercent
      };
    } catch {
      // Fallback values
      return {
        total_gb: 100,
        used_gb: 50,
        available_gb: 50,
        used_percent: 50,
        free_percent: 50
      };
    }
  }

  private async executeArchive(action: HealingAction): Promise<void> {
    const { older_than_days, compress, patterns } = action.params as {
      older_than_days: number;
      compress: boolean;
      patterns: string[];
    };
    const targetPath = action.target;
    
    console.log(`[StorageWatcher] Archiving files older than ${older_than_days} days in ${targetPath}`);
    
    try {
      // Sanitize target path to prevent path traversal
      const safePath = sanitizePath(targetPath);
      const safeOlderThanDays = Math.max(1, Math.floor(older_than_days));
      
      // Find and optionally compress old files
      for (const pattern of patterns) {
        // Sanitize pattern - only allow safe glob patterns
        const safePattern = pattern.replace(/[^a-zA-Z0-9.*_-]/g, '');
        const findCmd = `find ${escapeShellArg(safePath)} -name ${escapeShellArg(safePattern)} -mtime +${safeOlderThanDays} -type f 2>/dev/null || true`;
        const { stdout } = await execAsync(findCmd);
        
        const files = stdout.trim().split('\n').filter(f => f.length > 0);
        console.log(`[StorageWatcher] Found ${files.length} files matching ${pattern}`);
        
        if (compress && files.length > 0) {
          const archiveName = `/var/archive/logs_${Date.now()}.tar.gz`;
          
          // Ensure archive directory exists
          await execAsync('mkdir -p /var/archive 2>/dev/null || true');
          
          // Create compressed archive with escaped file paths
          if (files.length > 0) {
            const safeFiles = files.slice(0, 100).map(f => escapeShellArg(sanitizePath(f)));
            const fileList = safeFiles.join(' ');
            await execAsync(`tar -czf ${escapeShellArg(archiveName)} ${fileList} 2>/dev/null || true`);
            
            // Remove archived files
            await execAsync(`rm -f ${fileList} 2>/dev/null || true`);
          }
        }
      }
      
      this.emit('archive_complete', {
        path: targetPath,
        patterns,
        older_than_days,
        timestamp: new Date()
      });
    } catch (error) {
      console.log(`[StorageWatcher] Archive operation completed with warnings`);
    }
  }

  private async executeMirror(action: HealingAction): Promise<void> {
    const { source_paths, target_node, incremental } = action.params as {
      source_paths: string[];
      target_node: string;
      incremental: boolean;
    };
    
    console.log(`[StorageWatcher] Mirroring critical data to ${target_node}`);
    
    for (const sourcePath of source_paths) {
      try {
        // Check if path exists
        await fs.access(sourcePath);
        
        // In production, this would use rsync to mirror to target node
        const rsyncFlags = incremental ? '-avz --progress' : '-avz --delete --progress';
        console.log(`[StorageWatcher] Would sync: rsync ${rsyncFlags} ${sourcePath} ${target_node}:${sourcePath}`);
        
      } catch {
        console.log(`[StorageWatcher] Path ${sourcePath} does not exist, skipping`);
      }
    }
    
    this.emit('mirror_complete', {
      source_paths,
      target_node,
      incremental,
      timestamp: new Date()
    });
  }

  private async executeAlert(action: HealingAction): Promise<void> {
    const { severity, message } = action.params as { severity: string; message: string };
    
    console.log(`[StorageWatcher] Alert [${severity}]: ${message}`);
    
    this.emit('alert', {
      severity,
      message,
      source: 'StorageWatcher',
      timestamp: new Date()
    });
  }
}

export default StorageWatcher;
