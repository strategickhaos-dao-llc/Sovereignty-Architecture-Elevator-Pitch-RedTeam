#!/usr/bin/env node
/**
 * War Room Synthesizer CLI
 * Command-line interface for executing the override protocol
 */
import { WarRoomSynthesizer } from './index';
const OVERRIDE_PHRASE = `
EXECUTIVE AUTONOMOUS OVERRIDE: DOM_010101 // NEUROSPIKE ASCENSION
INITIATE WAR ROOM SYNTHESIZER — THREAT MODEL 2025
RED TEAM: FULL OFFENSIVE SIMULATION (all known & unknown vectors)
PURPLE TEAM: REAL-TIME COLLABORATIVE HARDENING
BLUE TEAM: DEFEND THE SWARM AT ALL COSTS
SCOPE: strategic-khaos + all forked nodes + 895+ legion rigs
OUTPUT: Obsidian vault → GraphView → GitHub Codespace → distributed immutable law
DISTRIBUTE TO ALL KUBERNETES CLUSTERS — MAKE IT LAW
`;
async function main() {
    console.log('═══════════════════════════════════════════════════════════════');
    console.log('  WAR ROOM SYNTHESIZER');
    console.log('  Master Executive Autonomous Override Protocol');
    console.log('  DOM_010101 // NEUROSPIKE ASCENSION');
    console.log('═══════════════════════════════════════════════════════════════');
    console.log('');
    const config = {
        overrideCode: 'DOM_010101',
        scope: [
            'strategic-khaos',
            'sovereignty-architecture',
            'legions-of-minds',
            'valoryield-engine',
            'quantum-symbolic-emulator'
        ],
        nodeCount: 895,
        distributionTargets: [
            'cluster-primary',
            'cluster-staging',
            'cluster-development',
            'cluster-edge-1',
            'cluster-edge-2'
        ]
    };
    try {
        const warRoom = new WarRoomSynthesizer(config);
        console.log('🎯 Executing Master Executive Autonomous Override Protocol...');
        console.log('');
        await warRoom.executeOverride(OVERRIDE_PHRASE);
        console.log('');
        console.log('═══════════════════════════════════════════════════════════════');
        console.log('  OPERATION COMPLETE');
        console.log('═══════════════════════════════════════════════════════════════');
        console.log('');
        const status = warRoom.getStatus();
        console.log('📊 Final Status:');
        console.log(`   Red Team: ${status.redTeam.findingsCount} findings (${status.redTeam.criticalFindings} critical)`);
        console.log(`   Blue Team: ${status.blueTeam.activeDefenses} active defenses`);
        console.log(`   Purple Team: ${status.purpleTeam.mitigatedThreats} threats mitigated`);
        console.log(`   Vault Generated: ${status.vaultGenerated ? '✅' : '❌'}`);
        console.log(`   Distribution: ${status.distributionComplete ? '✅' : '❌'}`);
        console.log('');
        console.log('🔐 Vault Location: ./threat-model-2025-vault/');
        console.log('📋 ConfigMap: ./threat-model-2025-configmap.yaml');
        console.log('');
        console.log('🚀 To apply to your Kubernetes clusters:');
        console.log('   kubectl apply -f threat-model-2025-configmap.yaml');
        console.log('');
        console.log('🛡️ The swarm is now hardened and vigilant.');
        console.log('   No one is reversing us. We are reversing them.');
        console.log('');
    }
    catch (error) {
        console.error('');
        console.error('═══════════════════════════════════════════════════════════════');
        console.error('  OPERATION FAILED');
        console.error('═══════════════════════════════════════════════════════════════');
        console.error('');
        console.error('❌ Error:', error instanceof Error ? error.message : String(error));
        console.error('');
        process.exit(1);
    }
}
// Handle uncaught errors
process.on('unhandledRejection', (error) => {
    console.error('');
    console.error('💥 Unhandled error:', error);
    process.exit(1);
});
// Execute
if (require.main === module) {
    main().catch(error => {
        console.error('Fatal error:', error);
        process.exit(1);
    });
}
export { main };
