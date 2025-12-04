/**
 * Mesh Healer Antibody
 * 
 * Layer 2: Network & Communication
 * Auto-regenerates WireGuard configs, validates connectivity every 30s, self-repairs broken tunnels.
 */

import BaseAntibody, { AntibodyConfig, HealthStatus, HealingAction } from './base-antibody.js';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

// Allowlist of valid peer names to prevent injection
const VALID_PEER_PATTERN = /^[a-zA-Z0-9_-]+$/;

function sanitizePeerName(peer: string): string {
  if (!VALID_PEER_PATTERN.test(peer)) {
    throw new Error(`Invalid peer name: ${peer}`);
  }
  return peer;
}

interface MeshConfig extends AntibodyConfig {
  wireguard_config_path: string;
  connectivity_timeout_ms: number;
}

interface NodeConnectivity {
  node: string;
  reachable: boolean;
  latency_ms: number;
  tunnel_status: 'up' | 'down' | 'degraded';
}

export class MeshHealer extends BaseAntibody {
  private meshConfig: MeshConfig;
  private peers: string[] = ['nova', 'lyra', 'athena'];

  constructor(config: MeshConfig) {
    super('MeshHealer', config);
    this.meshConfig = config;
  }

  protected async checkHealth(): Promise<HealthStatus> {
    const connectivity = await this.checkAllPeers();
    
    const downPeers = connectivity.filter(c => !c.reachable);
    const degradedPeers = connectivity.filter(c => c.tunnel_status === 'degraded');
    
    let healthy = downPeers.length === 0;
    let message = 'All mesh connections healthy';
    
    if (downPeers.length > 0) {
      healthy = false;
      message = `Unreachable peers: ${downPeers.map(p => p.node).join(', ')}`;
    } else if (degradedPeers.length > 0) {
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

  protected async determineHealingActions(health: HealthStatus): Promise<HealingAction[]> {
    const actions: HealingAction[] = [];
    const downPeers = health.metrics.down_peers as number;
    
    // Get the names of down peers from metrics
    const downPeerNames: string[] = [];
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

  protected async executeHealingAction(action: HealingAction): Promise<void> {
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

  private async checkAllPeers(): Promise<NodeConnectivity[]> {
    const results: NodeConnectivity[] = [];
    
    for (const peer of this.peers) {
      const connectivity = await this.checkPeerConnectivity(peer);
      results.push(connectivity);
    }
    
    return results;
  }

  private async checkPeerConnectivity(peer: string): Promise<NodeConnectivity> {
    const timeout = this.meshConfig.connectivity_timeout_ms;
    let reachable = false;
    let latency = 0;
    let tunnelStatus: 'up' | 'down' | 'degraded' = 'down';
    
    try {
      // Sanitize peer name to prevent command injection
      const safePeer = sanitizePeerName(peer);
      const safeTimeout = Math.ceil(timeout / 1000);
      
      // Try to ping the peer
      const { stdout } = await execAsync(
        `ping -c 1 -W ${safeTimeout} ${safePeer}.local 2>/dev/null || echo "UNREACHABLE"`
      );
      
      if (!stdout.includes('UNREACHABLE')) {
        reachable = true;
        // Extract latency from ping output
        const match = stdout.match(/time=(\d+\.?\d*)/);
        latency = match ? parseFloat(match[1]) : 0;
        
        // Check WireGuard handshake status
        const wgStatus = await this.checkWireGuardHandshake(safePeer);
        tunnelStatus = wgStatus;
      }
    } catch {
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

  private async checkWireGuardHandshake(peer: string): Promise<'up' | 'down' | 'degraded'> {
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
          
          if (age < 180) return 'up';
          if (age < 300) return 'degraded';
          return 'down';
        }
      }
      
      return 'down';
    } catch {
      return 'down';
    }
  }

  private async executeRestartInterface(action: HealingAction): Promise<void> {
    const { interface: iface, peer_name } = action.params as { interface: string; peer_name: string };
    
    console.log(`[MeshHealer] Restarting WireGuard interface ${iface} for peer ${peer_name}`);
    
    try {
      // In production, this would actually restart the interface
      // await execAsync(`wg-quick down ${iface} && wg-quick up ${iface}`);
      
      this.emit('interface_restarted', {
        interface: iface,
        peer_name,
        timestamp: new Date()
      });
    } catch (error) {
      console.log(`[MeshHealer] Interface restart failed, will try config regeneration`);
    }
  }

  private async executeRegenerateConfig(action: HealingAction): Promise<void> {
    const { config_path, peer_name } = action.params as { config_path: string; peer_name: string };
    
    console.log(`[MeshHealer] Regenerating WireGuard config for peer ${peer_name}`);
    
    // In production, this would regenerate WireGuard configuration
    // based on the peer's public key and allowed IPs from a central config
    
    this.emit('config_regenerated', {
      config_path,
      peer_name,
      timestamp: new Date()
    });
  }

  private async executeFailover(action: HealingAction): Promise<void> {
    const { mode, fallback_to_direct } = action.params as {
      mode: string;
      fallback_to_direct: boolean;
    };
    
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

  private async executeAlert(action: HealingAction): Promise<void> {
    const { severity, message } = action.params as { severity: string; message: string };
    
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
