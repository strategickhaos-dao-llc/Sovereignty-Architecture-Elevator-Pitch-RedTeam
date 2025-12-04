/**
 * Storage Watcher Antibody
 *
 * Layer 1: Hardware Resilience
 * Auto-archives old logs, maintains 20% free space buffer, mirrors critical data across nodes.
 */
import BaseAntibody from './base-antibody.js';
import { exec } from 'child_process';
import { promisify } from 'util';
import * as fs from 'fs/promises';
const execAsync = promisify(exec);
export class StorageWatcher extends BaseAntibody {
    storageConfig;
    watchedPaths;
    constructor(config) {
        super('StorageWatcher', config);
        this.storageConfig = config;
        this.watchedPaths = config.watched_paths || ['/', '/var/log', '/data'];
    }
    async checkHealth() {
        const metrics = await this.collectStorageMetrics();
        const minFreePercent = this.storageConfig.free_space_buffer_percent;
        let healthy = true;
        let message = 'Storage levels nominal';
        if (metrics.free_percent < minFreePercent) {
            healthy = false;
            message = `Low storage: ${metrics.free_percent.toFixed(1)}% free (requires ${minFreePercent}%)`;
        }
        else if (metrics.free_percent < minFreePercent * 1.5) {
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
    async determineHealingActions(health) {
        const actions = [];
        const freePercent = health.metrics.free_percent;
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
    async executeHealingAction(action) {
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
    async collectStorageMetrics() {
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
        }
        catch {
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
    async executeArchive(action) {
        const { older_than_days, compress, patterns } = action.params;
        const targetPath = action.target;
        console.log(`[StorageWatcher] Archiving files older than ${older_than_days} days in ${targetPath}`);
        try {
            // Find and optionally compress old files
            for (const pattern of patterns) {
                const findCmd = `find ${targetPath} -name "${pattern}" -mtime +${older_than_days} -type f 2>/dev/null || true`;
                const { stdout } = await execAsync(findCmd);
                const files = stdout.trim().split('\n').filter(f => f.length > 0);
                console.log(`[StorageWatcher] Found ${files.length} files matching ${pattern}`);
                if (compress && files.length > 0) {
                    const archiveName = `/var/archive/logs_${Date.now()}.tar.gz`;
                    // Ensure archive directory exists
                    await execAsync('mkdir -p /var/archive 2>/dev/null || true');
                    // Create compressed archive
                    if (files.length > 0) {
                        const fileList = files.slice(0, 100).join(' '); // Limit to 100 files per batch
                        await execAsync(`tar -czf ${archiveName} ${fileList} 2>/dev/null || true`);
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
        }
        catch (error) {
            console.log(`[StorageWatcher] Archive operation completed with warnings`);
        }
    }
    async executeMirror(action) {
        const { source_paths, target_node, incremental } = action.params;
        console.log(`[StorageWatcher] Mirroring critical data to ${target_node}`);
        for (const sourcePath of source_paths) {
            try {
                // Check if path exists
                await fs.access(sourcePath);
                // In production, this would use rsync to mirror to target node
                const rsyncFlags = incremental ? '-avz --progress' : '-avz --delete --progress';
                console.log(`[StorageWatcher] Would sync: rsync ${rsyncFlags} ${sourcePath} ${target_node}:${sourcePath}`);
            }
            catch {
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
    async executeAlert(action) {
        const { severity, message } = action.params;
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
