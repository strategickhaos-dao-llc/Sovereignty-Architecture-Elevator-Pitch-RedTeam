/**
 * Threat Vault - Comprehensive Security Documentation
 * Generates Obsidian-compatible vault with threat intelligence
 */

import * as fs from 'fs';
import * as path from 'path';
import type { SecurityFinding } from './red-team';
import type { DefenseMechanism } from './blue-team';
import type { ThreatAnalysis } from './purple-team';
import type { OverrideProtocolConfig } from './index';

export interface VaultGenerationOptions {
  redTeamFindings: SecurityFinding[];
  blueTeamDefenses: DefenseMechanism[];
  purpleTeamAnalysis: ThreatAnalysis[];
  mitreAttackMapping: boolean;
  nodeTrustLevels: boolean;
  hardeningPlaybook: boolean;
  counterAttackStrategies: boolean;
}

export interface VaultData {
  metadata: {
    generated: Date;
    version: string;
    signature: string;
  };
  threatMatrix: any;
  nodeTrustLevels: any;
  hardeningPlaybook: any;
  counterAttackStrategies: any;
}

export class ThreatVault {
  private vaultPath: string;
  private vaultGenerated: boolean = false;
  private vaultData?: VaultData;

  constructor(private config: OverrideProtocolConfig) {
    this.vaultPath = path.join(process.cwd(), 'threat-model-2025-vault');
  }

  /**
   * Generate comprehensive threat vault
   */
  async generate(options: VaultGenerationOptions): Promise<VaultData> {
    console.log('   ├─ Generating threat vault structure...');
    
    this.vaultData = {
      metadata: {
        generated: new Date(),
        version: '2025.1.0',
        signature: this.generateSignature()
      },
      threatMatrix: this.generateThreatMatrix(options),
      nodeTrustLevels: this.generateNodeTrustLevels(options),
      hardeningPlaybook: this.generateHardeningPlaybook(options),
      counterAttackStrategies: this.generateCounterAttackStrategies(options)
    };
    
    this.vaultGenerated = true;
    return this.vaultData;
  }

  /**
   * Generate MITRE ATT&CK threat matrix
   */
  private generateThreatMatrix(options: VaultGenerationOptions): any {
    const matrix = {
      tactics: [] as any[],
      techniques: [] as any[],
      findings: options.redTeamFindings.map(f => ({
        id: f.id,
        severity: f.severity,
        category: f.category,
        attackVector: f.attackVector,
        mitreMapping: this.mapToMITRE(f)
      }))
    };
    
    // Map to MITRE ATT&CK framework
    const mitreTactics = [
      { id: 'TA0001', name: 'Initial Access', findings: [] as string[] },
      { id: 'TA0002', name: 'Execution', findings: [] as string[] },
      { id: 'TA0003', name: 'Persistence', findings: [] as string[] },
      { id: 'TA0004', name: 'Privilege Escalation', findings: [] as string[] },
      { id: 'TA0005', name: 'Defense Evasion', findings: [] as string[] },
      { id: 'TA0006', name: 'Credential Access', findings: [] as string[] },
      { id: 'TA0007', name: 'Discovery', findings: [] as string[] },
      { id: 'TA0008', name: 'Lateral Movement', findings: [] as string[] },
      { id: 'TA0009', name: 'Collection', findings: [] as string[] },
      { id: 'TA0011', name: 'Command and Control', findings: [] as string[] }
    ];
    
    matrix.tactics = mitreTactics;
    return matrix;
  }

  /**
   * Map security finding to MITRE ATT&CK technique
   */
  private mapToMITRE(finding: SecurityFinding): string {
    const categoryMapping: Record<string, string> = {
      'Reverse Engineering': 'T1592 - Gather Victim Host Information',
      'Supply Chain': 'T1195 - Supply Chain Compromise',
      'Network Security': 'T1557 - Adversary-in-the-Middle',
      'Token Security': 'T1528 - Steal Application Access Token',
      'Backdoor Detection': 'T1543 - Create or Modify System Process',
      'Social Engineering': 'T1566 - Phishing'
    };
    
    return categoryMapping[finding.category] || 'T1059 - Command and Scripting Interpreter';
  }

  /**
   * Generate node trust level assessment
   */
  private generateNodeTrustLevels(options: VaultGenerationOptions): any {
    const nodeCount = this.config.nodeCount || 895;
    
    return {
      totalNodes: nodeCount,
      trustLevels: {
        verified: Math.floor(nodeCount * 0.75),
        trusted: Math.floor(nodeCount * 0.15),
        monitoring: Math.floor(nodeCount * 0.08),
        untrusted: Math.floor(nodeCount * 0.02)
      },
      criteria: {
        verified: 'Core legion members with verified identity and security posture',
        trusted: 'Known contributors with established track record',
        monitoring: 'New or inactive nodes under observation',
        untrusted: 'Flagged nodes requiring immediate review'
      }
    };
  }

  /**
   * Generate hardening playbook
   */
  private generateHardeningPlaybook(options: VaultGenerationOptions): any {
    return {
      title: 'Strategic Khaos Hardening Playbook',
      sections: [
        {
          name: 'Network Security',
          actions: [
            'Enable WireGuard tunnel encryption with PFS',
            'Implement network segmentation',
            'Deploy IDS/IPS on all network boundaries',
            'Enable DDoS protection'
          ]
        },
        {
          name: 'Access Control',
          actions: [
            'Enforce MFA for all administrative access',
            'Implement zero-trust architecture',
            'Rotate credentials every 30 days',
            'Use hardware security keys for critical systems'
          ]
        },
        {
          name: 'Application Security',
          actions: [
            'Enable content security policy (CSP)',
            'Implement rate limiting on all APIs',
            'Use prepared statements to prevent SQL injection',
            'Enable HTTPS everywhere with HSTS'
          ]
        },
        {
          name: 'Monitoring & Response',
          actions: [
            'Deploy SIEM for centralized logging',
            'Set up real-time alerting for anomalies',
            'Implement automated incident response',
            'Conduct quarterly security audits'
          ]
        }
      ],
      oneClickApply: true,
      automationScript: '/scripts/apply-hardening.sh'
    };
  }

  /**
   * Generate counter-attack strategies
   */
  private generateCounterAttackStrategies(options: VaultGenerationOptions): any {
    return {
      title: 'Active Defense & Counter-Attack Strategies',
      disclaimer: 'Use responsibly and within legal boundaries',
      strategies: [
        {
          name: 'Honey Token Deployment',
          description: 'Deploy fake credentials to detect and track attackers',
          effectiveness: 'High',
          legalRisk: 'Low'
        },
        {
          name: 'Aggressive Attribution',
          description: 'Use advanced techniques to identify attacker infrastructure',
          effectiveness: 'Medium',
          legalRisk: 'Medium'
        },
        {
          name: 'Deception Networks',
          description: 'Create realistic decoy systems to waste attacker resources',
          effectiveness: 'High',
          legalRisk: 'Low'
        },
        {
          name: 'Active Response',
          description: 'Automated blocking and counter-measures against active threats',
          effectiveness: 'Very High',
          legalRisk: 'Low'
        }
      ],
      ethicalGuidelines: [
        'Always operate within legal boundaries',
        'Document all defensive actions',
        'Coordinate with law enforcement when appropriate',
        'Prioritize protection over retaliation'
      ]
    };
  }

  /**
   * Generate vault signature for verification
   */
  private generateSignature(): string {
    const timestamp = Date.now();
    const randomBytes = Math.random().toString(36).substring(2, 15);
    return `DOM_010101_${timestamp}_${randomBytes}`.toUpperCase();
  }

  /**
   * Export vault to Obsidian format
   */
  async exportToObsidian(): Promise<void> {
    if (!this.vaultData) {
      throw new Error('Vault data not generated yet');
    }

    console.log('   ├─ Exporting to Obsidian format...');
    
    // Create vault directory structure
    await this.createVaultStructure();
    
    // Generate markdown files
    await this.generateMarkdownFiles();
    
    // Create graph view configuration
    await this.generateGraphViewConfig();
    
    console.log('   └─ Obsidian vault created successfully');
  }

  /**
   * Create vault directory structure
   */
  private async createVaultStructure(): Promise<void> {
    const directories = [
      this.vaultPath,
      path.join(this.vaultPath, 'Threat Matrix'),
      path.join(this.vaultPath, 'Node Trust'),
      path.join(this.vaultPath, 'Hardening'),
      path.join(this.vaultPath, 'Counter-Attack'),
      path.join(this.vaultPath, '.obsidian')
    ];
    
    for (const dir of directories) {
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }
    }
  }

  /**
   * Generate markdown documentation files
   */
  private async generateMarkdownFiles(): Promise<void> {
    if (!this.vaultData) return;

    // Main index file
    const indexContent = this.generateIndexMarkdown();
    fs.writeFileSync(path.join(this.vaultPath, 'README.md'), indexContent);
    
    // Threat matrix
    const threatMatrixContent = this.generateThreatMatrixMarkdown();
    fs.writeFileSync(
      path.join(this.vaultPath, 'Threat Matrix', 'Overview.md'),
      threatMatrixContent
    );
    
    // Node trust levels
    const nodeTrustContent = this.generateNodeTrustMarkdown();
    fs.writeFileSync(
      path.join(this.vaultPath, 'Node Trust', 'Assessment.md'),
      nodeTrustContent
    );
    
    // Hardening playbook
    const hardeningContent = this.generateHardeningMarkdown();
    fs.writeFileSync(
      path.join(this.vaultPath, 'Hardening', 'Playbook.md'),
      hardeningContent
    );
    
    // Counter-attack strategies
    const counterAttackContent = this.generateCounterAttackMarkdown();
    fs.writeFileSync(
      path.join(this.vaultPath, 'Counter-Attack', 'Strategies.md'),
      counterAttackContent
    );
  }

  /**
   * Generate index markdown
   */
  private generateIndexMarkdown(): string {
    return `# Threat Model 2025 Vault

**Generated:** ${this.vaultData?.metadata.generated.toISOString()}
**Version:** ${this.vaultData?.metadata.version}
**Signature:** ${this.vaultData?.metadata.signature}

## Overview

This vault contains comprehensive threat intelligence and security hardening guidelines for the Strategic Khaos / Legions of Minds Council OS ecosystem.

## Contents

- [[Threat Matrix/Overview|Threat Matrix]] - MITRE ATT&CK mapped vulnerabilities
- [[Node Trust/Assessment|Node Trust Assessment]] - Trust levels for ${this.config.nodeCount}+ nodes
- [[Hardening/Playbook|Hardening Playbook]] - One-click security hardening
- [[Counter-Attack/Strategies|Counter-Attack Strategies]] - Active defense mechanisms

## Quick Actions

\`\`\`bash
# Apply hardening to all clusters
kubectl apply -f hardening-configmap.yaml

# Verify vault signature
./verify-vault-signature.sh ${this.vaultData?.metadata.signature}
\`\`\`

---

**⚠️ CLASSIFIED - FOR AUTHORIZED LEGION MEMBERS ONLY**
`;
  }

  /**
   * Generate threat matrix markdown
   */
  private generateThreatMatrixMarkdown(): string {
    const findings = this.vaultData?.threatMatrix.findings || [];
    
    let content = `# Threat Matrix - MITRE ATT&CK Mapping

## Critical Findings

| ID | Severity | Category | MITRE Technique |
|---|---|---|---|
`;
    
    for (const finding of findings) {
      content += `| ${finding.id} | ${finding.severity} | ${finding.category} | ${finding.mitreMapping} |\n`;
    }
    
    content += `\n## Tactics Coverage\n\n`;
    
    const tactics = this.vaultData?.threatMatrix.tactics || [];
    for (const tactic of tactics) {
      content += `- **${tactic.name}** (${tactic.id})\n`;
    }
    
    return content;
  }

  /**
   * Generate node trust markdown
   */
  private generateNodeTrustMarkdown(): string {
    const trust = this.vaultData?.nodeTrustLevels || {};
    
    return `# Node Trust Assessment

## Summary

- **Total Nodes:** ${trust.totalNodes}
- **Verified:** ${trust.trustLevels?.verified} (${Math.round(trust.trustLevels?.verified / trust.totalNodes * 100)}%)
- **Trusted:** ${trust.trustLevels?.trusted} (${Math.round(trust.trustLevels?.trusted / trust.totalNodes * 100)}%)
- **Monitoring:** ${trust.trustLevels?.monitoring} (${Math.round(trust.trustLevels?.monitoring / trust.totalNodes * 100)}%)
- **Untrusted:** ${trust.trustLevels?.untrusted} (${Math.round(trust.trustLevels?.untrusted / trust.totalNodes * 100)}%)

## Trust Criteria

${Object.entries(trust.criteria || {}).map(([level, desc]) => `### ${level.charAt(0).toUpperCase() + level.slice(1)}\n${desc}\n`).join('\n')}
`;
  }

  /**
   * Generate hardening playbook markdown
   */
  private generateHardeningMarkdown(): string {
    const playbook = this.vaultData?.hardeningPlaybook || {};
    
    let content = `# ${playbook.title}\n\n`;
    
    for (const section of playbook.sections || []) {
      content += `## ${section.name}\n\n`;
      for (const action of section.actions) {
        content += `- [ ] ${action}\n`;
      }
      content += '\n';
    }
    
    if (playbook.oneClickApply) {
      content += `## One-Click Apply\n\n\`\`\`bash\n${playbook.automationScript}\n\`\`\`\n`;
    }
    
    return content;
  }

  /**
   * Generate counter-attack markdown
   */
  private generateCounterAttackMarkdown(): string {
    const strategies = this.vaultData?.counterAttackStrategies || {};
    
    let content = `# ${strategies.title}\n\n**⚠️ ${strategies.disclaimer}**\n\n`;
    
    content += `## Strategies\n\n`;
    
    for (const strategy of strategies.strategies || []) {
      content += `### ${strategy.name}\n\n`;
      content += `**Description:** ${strategy.description}\n\n`;
      content += `**Effectiveness:** ${strategy.effectiveness}\n\n`;
      content += `**Legal Risk:** ${strategy.legalRisk}\n\n`;
    }
    
    content += `## Ethical Guidelines\n\n`;
    for (const guideline of strategies.ethicalGuidelines || []) {
      content += `- ${guideline}\n`;
    }
    
    return content;
  }

  /**
   * Generate Obsidian graph view configuration
   */
  private async generateGraphViewConfig(): Promise<void> {
    const config = {
      graphConfig: {
        collapse: false,
        search: '',
        showTags: true,
        showAttachments: false,
        hideUnresolved: false,
        showOrphans: true,
        colorGroups: [
          { query: 'path:"Threat Matrix"', color: { r: 255, g: 0, b: 0 } },
          { query: 'path:"Node Trust"', color: { r: 0, g: 255, b: 0 } },
          { query: 'path:"Hardening"', color: { r: 0, g: 0, b: 255 } },
          { query: 'path:"Counter-Attack"', color: { r: 128, g: 0, b: 128 } }
        ]
      }
    };
    
    const configPath = path.join(this.vaultPath, '.obsidian', 'graph.json');
    fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
  }

  /**
   * Create GitHub Codespace link
   */
  async createCodespaceLink(): Promise<string> {
    const repo = 'Strategickhaos/threat-model-2025-vault';
    const link = `https://github.com/codespaces/new?repo=${repo}`;
    
    console.log(`   ├─ Codespace link: ${link}`);
    
    return link;
  }

  /**
   * Get vault data
   */
  async getVaultData(): Promise<VaultData> {
    if (!this.vaultData) {
      throw new Error('Vault not generated yet');
    }
    return this.vaultData;
  }

  /**
   * Check if vault is generated
   */
  isGenerated(): boolean {
    return this.vaultGenerated;
  }
}
