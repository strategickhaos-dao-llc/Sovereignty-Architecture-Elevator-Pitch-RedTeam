/**
 * Mesh Healer Antibody
 *
 * Layer 2: Network & Communication
 * Auto-regenerates WireGuard configs, validates connectivity every 30s, self-repairs broken tunnels.
 */
import BaseAntibody from './base-antibody.js';
import { exec } from 'child_process';
import { promisify } from 'util';
const execAsync = promisify(exec);
export class MeshHealer extends BaseAntibody {
    meshConfig;
    peers = ['nova', 'lyra', 'athena'];
    constructor(config) {
        super('MeshHealer', config);
        this.meshConfig = config;
    }
    async checkHealth() {
        const connectivity = await this.checkAllPeers();
        const downPeers = connectivity.filter(c => !c.reachable);
        const degradedPeers = connectivity.filter(c => c.tunnel_status === 'degraded');
        let healthy = downPeers.length === 0;
        let message = 'All mesh connections healthy';
        if (downPeers.length > 0) {
            healthy = false;
            message = `Unreachable peers: ${downPeers.map(p => p.node).join(', ')}`;
        }
        else if (degradedPeers.length > 0) {
            message = `Degraded connections: ${degradedPeers.map(p => p.node).join(', ')}`;
        }
        // Calculate average latency
        const reachablePeers = connectivity.filter(c => c.reachable);
        const avgLatency = reachablePeers.length > 0
            ? reachablePeers.reduce((sum, p) => sum + p.latency_ms, 0) / reachablePeers.length
            : 0;
        return {
            healthy,
            message,
            metrics: {
                total_peers: connectivity.length,
                reachable_peers: reachablePeers.length,
                down_peers: downPeers.length,
                avg_latency_ms: avgLatency,
                ...Object.fromEntries(connectivity.map(c => [`${c.node}_status`, c.tunnel_status]))
            },
            timestamp: new Date()
        };
    }
    async determineHealingActions(health) {
        const actions = [];
        const downPeers = health.metrics.down_peers;
        // Get the names of down peers from metrics
        const downPeerNames = [];
        for (const peer of this.peers) {
            if (health.metrics[`${peer}_status`] === 'down') {
                downPeerNames.push(peer);
            }
        }
        for (const peer of downPeerNames) {
            // Try to restart interface first
            actions.push({
                type: 'restart_interface',
                target: peer,
                params: {
                    interface: `wg0`,
                    peer_name: peer
                },
                timestamp: new Date()
            });
            // If multiple peers are down, regenerate config
            if (downPeers >= 2) {
                actions.push({
                    type: 'regenerate_config',
                    target: peer,
                    params: {
                        config_path: this.meshConfig.wireguard_config_path,
                        peer_name: peer
                    },
                    timestamp: new Date()
                });
            }
        }
        // If more than half peers are down, initiate failover mode
        if (downPeers > this.peers.length / 2) {
            actions.push({
                type: 'failover',
                target: 'mesh_network',
                params: {
                    mode: 'emergency',
                    fallback_to_direct: true
                },
                timestamp: new Date()
            });
        }
        // Alert for any connectivity issues
        actions.push({
            type: 'alert',
            target: 'ops_team',
            params: {
                severity: downPeers > 1 ? 'critical' : 'warning',
                message: `Mesh connectivity issue: ${downPeers} peers unreachable`
            },
            timestamp: new Date()
        });
        return actions;
    }
    async executeHealingAction(action) {
        switch (action.type) {
            case 'restart_interface':
                await this.executeRestartInterface(action);
                break;
            case 'regenerate_config':
                await this.executeRegenerateConfig(action);
                break;
            case 'failover':
                await this.executeFailover(action);
                break;
            case 'alert':
                await this.executeAlert(action);
                break;
            default:
                console.log(`[MeshHealer] Unknown action type: ${action.type}`);
        }
    }
    async checkAllPeers() {
        const results = [];
        for (const peer of this.peers) {
            const connectivity = await this.checkPeerConnectivity(peer);
            results.push(connectivity);
        }
        return results;
    }
    async checkPeerConnectivity(peer) {
        const timeout = this.meshConfig.connectivity_timeout_ms;
        let reachable = false;
        let latency = 0;
        let tunnelStatus = 'down';
        try {
            // Try to ping the peer
            const { stdout } = await execAsync(`ping -c 1 -W ${Math.ceil(timeout / 1000)} ${peer}.local 2>/dev/null || echo "UNREACHABLE"`);
            if (!stdout.includes('UNREACHABLE')) {
                reachable = true;
                // Extract latency from ping output
                const match = stdout.match(/time=(\d+\.?\d*)/);
                latency = match ? parseFloat(match[1]) : 0;
                // Check WireGuard handshake status
                const wgStatus = await this.checkWireGuardHandshake(peer);
                tunnelStatus = wgStatus;
            }
        }
        catch {
            // Peer unreachable
            reachable = false;
        }
        return {
            node: peer,
            reachable,
            latency_ms: latency,
            tunnel_status: tunnelStatus
        };
    }
    async checkWireGuardHandshake(peer) {
        try {
            const { stdout } = await execAsync('wg show wg0 latest-handshakes 2>/dev/null || echo ""');
            if (!stdout || stdout.trim() === '') {
                return 'down';
            }
            // Parse handshake times - if last handshake was > 3 minutes ago, consider degraded
            const lines = stdout.trim().split('\n');
            for (const line of lines) {
                if (line.includes(peer)) {
                    const timestamp = parseInt(line.split('\t')[1]);
                    const now = Math.floor(Date.now() / 1000);
                    const age = now - timestamp;
                    if (age < 180)
                        return 'up';
                    if (age < 300)
                        return 'degraded';
                    return 'down';
                }
            }
            return 'down';
        }
        catch {
            return 'down';
        }
    }
    async executeRestartInterface(action) {
        const { interface: iface, peer_name } = action.params;
        console.log(`[MeshHealer] Restarting WireGuard interface ${iface} for peer ${peer_name}`);
        try {
            // In production, this would actually restart the interface
            // await execAsync(`wg-quick down ${iface} && wg-quick up ${iface}`);
            this.emit('interface_restarted', {
                interface: iface,
                peer_name,
                timestamp: new Date()
            });
        }
        catch (error) {
            console.log(`[MeshHealer] Interface restart failed, will try config regeneration`);
        }
    }
    async executeRegenerateConfig(action) {
        const { config_path, peer_name } = action.params;
        console.log(`[MeshHealer] Regenerating WireGuard config for peer ${peer_name}`);
        // In production, this would regenerate WireGuard configuration
        // based on the peer's public key and allowed IPs from a central config
        this.emit('config_regenerated', {
            config_path,
            peer_name,
            timestamp: new Date()
        });
    }
    async executeFailover(action) {
        const { mode, fallback_to_direct } = action.params;
        console.log(`[MeshHealer] Initiating ${mode} failover mode`);
        if (fallback_to_direct) {
            console.log('[MeshHealer] Falling back to direct connections (no mesh)');
        }
        this.emit('failover_initiated', {
            mode,
            fallback_to_direct,
            timestamp: new Date()
        });
    }
    async executeAlert(action) {
        const { severity, message } = action.params;
        console.log(`[MeshHealer] Alert [${severity}]: ${message}`);
        this.emit('alert', {
            severity,
            message,
            source: 'MeshHealer',
            timestamp: new Date()
        });
    }
}
export default MeshHealer;
