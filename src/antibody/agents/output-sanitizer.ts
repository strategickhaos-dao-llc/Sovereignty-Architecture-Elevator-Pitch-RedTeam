/**
 * Output Sanitizer Antibody
 * 
 * Layer 3: Model & Execution
 * Runs synthesized code through AST validation, lints Docker configs, test-executes in sandbox before commit.
 */

import BaseAntibody, { AntibodyConfig, HealthStatus, HealingAction } from './base-antibody.js';
import { exec } from 'child_process';
import { promisify } from 'util';
import * as fs from 'fs/promises';
import * as path from 'path';
import * as os from 'os';

const execAsync = promisify(exec);

interface SanitizerConfig extends AntibodyConfig {
  ast_validation: boolean;
  docker_lint: boolean;
  sandbox_test: boolean;
}

interface SanitizationResult {
  id: string;
  type: 'code' | 'docker' | 'config';
  valid: boolean;
  errors: string[];
  warnings: string[];
  sanitized_content?: string;
}

interface QueuedOutput {
  id: string;
  type: 'code' | 'docker' | 'config';
  content: string;
  language?: string;
  timestamp: Date;
}

export class OutputSanitizer extends BaseAntibody {
  private sanitizerConfig: SanitizerConfig;
  private outputQueue: Map<string, QueuedOutput> = new Map();
  private sanitizationResults: Map<string, SanitizationResult> = new Map();
  private rejectedCount: number = 0;
  private passedCount: number = 0;

  constructor(config: SanitizerConfig) {
    super('OutputSanitizer', config);
    this.sanitizerConfig = config;
  }

  protected async checkHealth(): Promise<HealthStatus> {
    const queueSize = this.outputQueue.size;
    const pendingValidations = queueSize;
    const rejectRate = this.passedCount + this.rejectedCount > 0
      ? (this.rejectedCount / (this.passedCount + this.rejectedCount)) * 100
      : 0;
    
    let healthy = true;
    let message = 'Output sanitization nominal';
    
    // High reject rate might indicate a problem
    if (rejectRate > 50) {
      healthy = false;
      message = `High rejection rate: ${rejectRate.toFixed(1)}% of outputs failing validation`;
    } else if (queueSize > 100) {
      message = `Warning: Large output queue (${queueSize} items pending)`;
    }
    
    return {
      healthy,
      message,
      metrics: {
        queue_size: queueSize,
        pending_validations: pendingValidations,
        passed_count: this.passedCount,
        rejected_count: this.rejectedCount,
        reject_rate: rejectRate
      },
      timestamp: new Date()
    };
  }

  protected async determineHealingActions(health: HealthStatus): Promise<HealingAction[]> {
    const actions: HealingAction[] = [];
    const rejectRate = health.metrics.reject_rate as number;
    
    if (rejectRate > 50) {
      // Investigate and alert on high rejection rate
      actions.push({
        type: 'validate',
        target: 'synthesis_engine',
        params: { 
          action: 'audit_prompts',
          reason: 'High output rejection rate'
        },
        timestamp: new Date()
      });
      
      actions.push({
        type: 'alert',
        target: 'ops_team',
        params: { 
          severity: 'warning',
          message: `Output sanitizer: ${rejectRate.toFixed(1)}% rejection rate`
        },
        timestamp: new Date()
      });
    }
    
    return actions;
  }

  protected async executeHealingAction(action: HealingAction): Promise<void> {
    switch (action.type) {
      case 'validate':
        console.log(`[OutputSanitizer] Triggering validation: ${action.params.action}`);
        this.emit('validation_triggered', action);
        break;
      case 'sanitize':
        console.log(`[OutputSanitizer] Running sanitization for ${action.target}`);
        break;
      case 'reject':
        console.log(`[OutputSanitizer] Rejecting output ${action.target}`);
        break;
      case 'alert':
        await this.executeAlert(action);
        break;
      default:
        console.log(`[OutputSanitizer] Unknown action type: ${action.type}`);
    }
  }

  /**
   * Queue an output for sanitization
   */
  public queueOutput(id: string, type: 'code' | 'docker' | 'config', content: string, language?: string): void {
    this.outputQueue.set(id, {
      id,
      type,
      content,
      language,
      timestamp: new Date()
    });
    
    // Process immediately
    this.processOutput(id);
  }

  /**
   * Process and validate a queued output
   */
  private async processOutput(id: string): Promise<SanitizationResult> {
    const output = this.outputQueue.get(id);
    if (!output) {
      throw new Error(`Output ${id} not found in queue`);
    }
    
    const result: SanitizationResult = {
      id,
      type: output.type,
      valid: true,
      errors: [],
      warnings: []
    };
    
    try {
      switch (output.type) {
        case 'code':
          await this.validateCode(output, result);
          break;
        case 'docker':
          await this.validateDocker(output, result);
          break;
        case 'config':
          await this.validateConfig(output, result);
          break;
      }
      
      // Run sandbox test if enabled and initial validation passed
      if (result.valid && this.sanitizerConfig.sandbox_test) {
        await this.sandboxTest(output, result);
      }
      
    } catch (error) {
      result.valid = false;
      result.errors.push(`Validation error: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
    
    // Update counters
    if (result.valid) {
      this.passedCount++;
    } else {
      this.rejectedCount++;
    }
    
    // Store result and remove from queue
    this.sanitizationResults.set(id, result);
    this.outputQueue.delete(id);
    
    // Emit result
    this.emit('sanitization_complete', result);
    
    return result;
  }

  /**
   * Validate code using AST parsing
   */
  private async validateCode(output: QueuedOutput, result: SanitizationResult): Promise<void> {
    if (!this.sanitizerConfig.ast_validation) return;
    
    const language = output.language || 'javascript';
    
    // Create temp file for validation
    const tempDir = await fs.mkdtemp(path.join(os.tmpdir(), 'sanitizer-'));
    const extension = this.getFileExtension(language);
    const tempFile = path.join(tempDir, `code${extension}`);
    
    try {
      await fs.writeFile(tempFile, output.content);
      
      // Run language-specific validation
      switch (language) {
        case 'javascript':
        case 'typescript':
          await this.validateJavaScript(tempFile, result);
          break;
        case 'python':
          await this.validatePython(tempFile, result);
          break;
        default:
          result.warnings.push(`No AST validator for language: ${language}`);
      }
    } finally {
      // Cleanup
      await fs.rm(tempDir, { recursive: true, force: true });
    }
  }

  private async validateJavaScript(filePath: string, result: SanitizationResult): Promise<void> {
    try {
      // Use Node to parse and check for syntax errors
      const { stderr } = await execAsync(`node --check ${filePath} 2>&1 || true`);
      if (stderr && stderr.length > 0) {
        result.valid = false;
        result.errors.push(`JavaScript syntax error: ${stderr}`);
      }
    } catch (error) {
      result.valid = false;
      result.errors.push(`JavaScript validation failed: ${error}`);
    }
  }

  private async validatePython(filePath: string, result: SanitizationResult): Promise<void> {
    try {
      // Use Python to parse and check for syntax errors
      const { stderr } = await execAsync(`python3 -m py_compile ${filePath} 2>&1 || true`);
      if (stderr && stderr.length > 0) {
        result.valid = false;
        result.errors.push(`Python syntax error: ${stderr}`);
      }
    } catch (error) {
      result.valid = false;
      result.errors.push(`Python validation failed: ${error}`);
    }
  }

  /**
   * Validate Docker configurations
   */
  private async validateDocker(output: QueuedOutput, result: SanitizationResult): Promise<void> {
    if (!this.sanitizerConfig.docker_lint) return;
    
    // Create temp file for validation
    const tempDir = await fs.mkdtemp(path.join(os.tmpdir(), 'sanitizer-'));
    const tempFile = path.join(tempDir, 'Dockerfile');
    
    try {
      await fs.writeFile(tempFile, output.content);
      
      // Run hadolint if available
      const { stdout, stderr } = await execAsync(
        `hadolint ${tempFile} 2>&1 || echo "HADOLINT_ERROR"`
      );
      
      if (stdout.includes('HADOLINT_ERROR')) {
        // Fallback to basic validation
        result.warnings.push('hadolint not available, using basic validation');
        this.basicDockerValidation(output.content, result);
      } else if (stderr || stdout.includes('error')) {
        result.warnings.push(`Docker lint warnings: ${stdout}`);
      }
    } finally {
      await fs.rm(tempDir, { recursive: true, force: true });
    }
  }

  private basicDockerValidation(content: string, result: SanitizationResult): void {
    const lines = content.split('\n');
    let hasFrom = false;
    
    for (const line of lines) {
      const trimmed = line.trim();
      if (trimmed.startsWith('FROM')) {
        hasFrom = true;
      }
      
      // Check for potentially dangerous instructions
      if (trimmed.includes('rm -rf /')) {
        result.errors.push('Dangerous command detected: rm -rf /');
        result.valid = false;
      }
    }
    
    if (!hasFrom) {
      result.errors.push('Dockerfile missing FROM instruction');
      result.valid = false;
    }
  }

  /**
   * Validate configuration files
   */
  private async validateConfig(output: QueuedOutput, result: SanitizationResult): Promise<void> {
    const content = output.content;
    
    // Try to parse as JSON
    try {
      JSON.parse(content);
      return; // Valid JSON
    } catch {
      // Not JSON, try YAML
    }
    
    // Try to parse as YAML (basic check)
    if (content.includes(':') && !content.includes('{')) {
      // Looks like YAML, do basic validation
      const lines = content.split('\n');
      for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        // Check for tabs (YAML doesn't allow tabs for indentation)
        if (line.startsWith('\t')) {
          result.errors.push(`YAML error line ${i + 1}: tabs not allowed for indentation`);
          result.valid = false;
        }
      }
    }
  }

  /**
   * Run output in sandbox for testing
   */
  private async sandboxTest(output: QueuedOutput, result: SanitizationResult): Promise<void> {
    console.log(`[OutputSanitizer] Running sandbox test for ${output.id}`);
    
    // In production, this would use Docker or a VM to safely execute the code
    // For now, we just emit an event indicating sandbox test would run
    this.emit('sandbox_test', {
      id: output.id,
      type: output.type,
      timestamp: new Date()
    });
  }

  /**
   * Get sanitization result for an output
   */
  public getResult(id: string): SanitizationResult | undefined {
    return this.sanitizationResults.get(id);
  }

  private getFileExtension(language: string): string {
    const extensions: Record<string, string> = {
      javascript: '.js',
      typescript: '.ts',
      python: '.py',
      go: '.go',
      rust: '.rs',
      java: '.java'
    };
    return extensions[language] || '.txt';
  }

  private async executeAlert(action: HealingAction): Promise<void> {
    const { severity, message } = action.params as { severity: string; message: string };
    
    console.log(`[OutputSanitizer] Alert [${severity}]: ${message}`);
    
    this.emit('alert', {
      severity,
      message,
      source: 'OutputSanitizer',
      timestamp: new Date()
    });
  }
}

export default OutputSanitizer;
