/**
 * XAI (Explainable AI) Layer for Dividend Capture Strategy
 * 
 * Provides transparent, explainable reasoning for trading decisions
 * Integrates with PID-RANCO control system for market state analysis
 */

import { DividendEvent, OptionsStrategy } from './dividend-capture.js';

export interface MarketState {
  trend: 'accumulation' | 'distribution' | 'neutral';
  volatility: 'low' | 'medium' | 'high';
  sentiment: number; // -1 to 1 scale
  volume: 'low' | 'average' | 'high';
}

export interface XAIDecision {
  action: 'ENTER' | 'EXIT' | 'HOLD' | 'SKIP';
  confidence: number; // 0 to 1 scale
  reasoning: string[];
  marketState: MarketState;
  riskLevel: 'low' | 'medium' | 'high';
  timestamp: Date;
}

export interface PIDRANCOSignal {
  pid_error: number;
  ranco_state: 'long' | 'short' | 'neutral';
  control_output: number;
  divergence_detected: boolean;
}

/**
 * Explainable AI Decision Engine
 */
export class XAIDecisionEngine {
  /**
   * Analyzes market conditions and dividend opportunity
   * Returns transparent, human-readable decision with reasoning
   */
  async analyzeDividendOpportunity(
    dividend: DividendEvent,
    marketState: MarketState,
    pidSignal: PIDRANCOSignal
  ): Promise<XAIDecision> {
    const reasoning: string[] = [];
    let confidence = 0.5;
    let action: 'ENTER' | 'EXIT' | 'HOLD' | 'SKIP' = 'HOLD';
    let riskLevel: 'low' | 'medium' | 'high' = 'medium';

    // Analyze dividend fundamentals
    if (dividend.yield >= 0.03) {
      reasoning.push(`✓ High dividend yield: ${(dividend.yield * 100).toFixed(2)}%`);
      confidence += 0.15;
    }

    // Analyze market state
    if (marketState.trend === 'accumulation') {
      reasoning.push(`✓ Market in accumulation phase - favorable for entry`);
      confidence += 0.1;
    } else if (marketState.trend === 'distribution') {
      reasoning.push(`⚠ Market in distribution phase - caution advised`);
      confidence -= 0.1;
      riskLevel = 'high';
    }

    // Analyze volatility
    if (marketState.volatility === 'low') {
      reasoning.push(`✓ Low volatility - stable dividend capture environment`);
      confidence += 0.1;
      riskLevel = 'low';
    } else if (marketState.volatility === 'high') {
      reasoning.push(`⚠ High volatility - increased delta risk`);
      confidence -= 0.15;
    }

    // PID-RANCO analysis
    if (pidSignal.ranco_state === 'long') {
      reasoning.push(`✓ PID-RANCO: Long signal detected`);
      confidence += 0.15;
    } else if (pidSignal.ranco_state === 'short') {
      reasoning.push(`⚠ PID-RANCO: Short signal - dividend capture not optimal`);
      confidence -= 0.2;
    }

    if (pidSignal.divergence_detected) {
      reasoning.push(`⚠ Price-momentum divergence detected - proceed with caution`);
      confidence -= 0.1;
    }

    // Calculate days until ex-div
    const now = new Date();
    const daysUntilExDiv = Math.floor(
      (dividend.exDivDate.getTime() - now.getTime()) / (1000 * 60 * 60 * 24)
    );

    if (daysUntilExDiv <= 2 && daysUntilExDiv >= 0) {
      reasoning.push(`✓ Optimal entry window: ${daysUntilExDiv} days until ex-div`);
      confidence += 0.15;
    } else if (daysUntilExDiv < 0) {
      reasoning.push(`✗ Ex-div date has passed - opportunity missed`);
      action = 'SKIP';
      confidence = 0;
    }

    // Make final decision
    if (confidence >= 0.7 && action !== 'SKIP') {
      action = 'ENTER';
      reasoning.push(`💎 ENTER: High confidence dividend capture opportunity`);
    } else if (confidence >= 0.5 && action !== 'SKIP') {
      action = 'HOLD';
      reasoning.push(`⏸ HOLD: Moderate opportunity - monitor for better entry`);
    } else if (action !== 'SKIP') {
      action = 'SKIP';
      reasoning.push(`⏭ SKIP: Low confidence - risk/reward not favorable`);
    }

    // Add love-based reasoning (from problem statement philosophy)
    if (action === 'ENTER') {
      reasoning.push(`💝 Love + dividend = compounding returns. This is the way.`);
    }

    return {
      action,
      confidence: Math.max(0, Math.min(1, confidence)),
      reasoning,
      marketState,
      riskLevel,
      timestamp: new Date()
    };
  }

  /**
   * Analyzes options strategy with XAI reasoning
   */
  async analyzeOptionsStrategy(strategy: OptionsStrategy): Promise<XAIDecision> {
    const reasoning: string[] = [];
    let confidence = 0.5;
    let action: 'ENTER' | 'EXIT' | 'HOLD' | 'SKIP' = 'HOLD';
    let riskLevel: 'low' | 'medium' | 'high' = 'medium';

    // Analyze ITM depth
    const itmDepth = (strategy.stockPrice - strategy.strike) / strategy.stockPrice;
    if (itmDepth >= 0.15) {
      reasoning.push(`✓ Deep ITM call (${(itmDepth * 100).toFixed(1)}% ITM) - minimal delta risk`);
      confidence += 0.2;
      riskLevel = 'low';
    } else if (itmDepth < 0.05) {
      reasoning.push(`⚠ Shallow ITM - higher delta risk exposure`);
      confidence -= 0.15;
      riskLevel = 'high';
    }

    // Analyze expected return
    if (strategy.expectedReturn > 0.02) {
      reasoning.push(`✓ Expected return: ${(strategy.expectedReturn * 100).toFixed(2)}%`);
      confidence += 0.15;
    } else {
      reasoning.push(`⚠ Low expected return: ${(strategy.expectedReturn * 100).toFixed(2)}%`);
      confidence -= 0.1;
    }

    // Analyze delta risk
    if (strategy.deltaRisk <= 0.05) {
      reasoning.push(`✓ Minimal delta risk: $${strategy.deltaRisk.toFixed(2)}`);
      confidence += 0.1;
    } else {
      reasoning.push(`⚠ Elevated delta risk: $${strategy.deltaRisk.toFixed(2)}`);
      confidence -= 0.15;
    }

    // Final decision
    if (confidence >= 0.7) {
      action = 'ENTER';
      reasoning.push(`💰 ENTER: Buy deep ITM calls for dividend capture`);
    } else if (confidence >= 0.5) {
      action = 'HOLD';
      reasoning.push(`⏸ HOLD: Monitor for better option pricing`);
    } else {
      action = 'SKIP';
      reasoning.push(`⏭ SKIP: Risk/reward not optimal for this strategy`);
    }

    return {
      action,
      confidence: Math.max(0, Math.min(1, confidence)),
      reasoning,
      marketState: {
        trend: 'neutral',
        volatility: 'medium',
        sentiment: 0,
        volume: 'average'
      },
      riskLevel,
      timestamp: new Date()
    };
  }

  /**
   * Provides explanation for why a particular stock was selected for DRIP
   */
  explainDRIPSelection(ticker: string, years: number, yieldRate: number, sector: string): string[] {
    return [
      `💎 ${ticker}: Dividend Aristocrat with ${years} years of consecutive increases`,
      `✓ Current yield: ${(yieldRate * 100).toFixed(2)}%`,
      `✓ Sector: ${sector} - provides portfolio diversification`,
      `✓ DRIP eligible - automatic dividend reinvestment`,
      `💝 Long-term compounding through love and consistency`
    ];
  }
}

/**
 * PID-RANCO Control System Integration
 */
export class PIDRANCOController {
  private kp: number = 0.5; // Proportional gain
  private ki: number = 0.1; // Integral gain
  private kd: number = 0.2; // Derivative gain
  
  private integral: number = 0;
  private previousError: number = 0;

  /**
   * Calculates PID control output for market positioning
   */
  calculate(
    targetPrice: number,
    currentPrice: number,
    deltaTime: number = 1
  ): PIDRANCOSignal {
    const error = targetPrice - currentPrice;
    
    // Proportional term
    const p = this.kp * error;
    
    // Integral term
    this.integral += error * deltaTime;
    const i = this.ki * this.integral;
    
    // Derivative term
    const derivative = (error - this.previousError) / deltaTime;
    const d = this.kd * derivative;
    
    // Total control output
    const controlOutput = p + i + d;
    
    // RANCO state determination
    let rancoState: 'long' | 'short' | 'neutral' = 'neutral';
    if (controlOutput > 0.5) {
      rancoState = 'long';
    } else if (controlOutput < -0.5) {
      rancoState = 'short';
    }
    
    // Detect divergence
    const divergenceDetected = Math.abs(derivative) > 1.0;
    
    this.previousError = error;
    
    return {
      pid_error: error,
      ranco_state: rancoState,
      control_output: controlOutput,
      divergence_detected: divergenceDetected
    };
  }

  /**
   * Analyzes market state using PID-RANCO
   */
  async analyzeMarketState(ticker: string, historicalData: any[]): Promise<MarketState> {
    console.log(`Analyzing market state for ${ticker} using PID-RANCO`);
    
    // Real implementation would analyze:
    // - Price action and momentum
    // - Volume patterns
    // - Accumulation/distribution indicators
    // - Market sentiment
    
    return {
      trend: 'accumulation',
      volatility: 'low',
      sentiment: 0.7,
      volume: 'average'
    };
  }

  /**
   * Resets the PID controller state
   */
  reset(): void {
    this.integral = 0;
    this.previousError = 0;
  }
}

/**
 * XAI Swarm - Multiple AI agents analyzing opportunities
 */
export class XAISwarm {
  private decisionEngine: XAIDecisionEngine;
  private pidController: PIDRANCOController;

  constructor() {
    this.decisionEngine = new XAIDecisionEngine();
    this.pidController = new PIDRANCOController();
  }

  /**
   * Swarm intelligence analysis - multiple agents evaluate opportunity
   */
  async swarmAnalysis(dividend: DividendEvent): Promise<XAIDecision[]> {
    console.log(`🐝 XAI Swarm analyzing ${dividend.ticker} dividend opportunity`);
    
    const decisions: XAIDecision[] = [];
    
    // Agent 1: Fundamental analyst
    const marketState = await this.pidController.analyzeMarketState(dividend.ticker, []);
    const pidSignal = this.pidController.calculate(dividend.dividendAmount, 0.25);
    
    const fundamentalDecision = await this.decisionEngine.analyzeDividendOpportunity(
      dividend,
      marketState,
      pidSignal
    );
    decisions.push(fundamentalDecision);
    
    // Agent 2: Technical analyst
    // Agent 3: Risk manager
    // Agent 4: Portfolio optimizer
    // ... more agents can be added for swarm intelligence
    
    return decisions;
  }

  /**
   * Gets consensus decision from swarm
   */
  getSwarmConsensus(decisions: XAIDecision[]): XAIDecision {
    if (decisions.length === 0) {
      throw new Error('No decisions to analyze');
    }

    // Calculate average confidence
    const avgConfidence = decisions.reduce((sum, d) => sum + d.confidence, 0) / decisions.length;
    
    // Count action votes
    const actionVotes = decisions.reduce((acc, d) => {
      acc[d.action] = (acc[d.action] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);
    
    // Get consensus action
    const consensusAction = Object.entries(actionVotes).reduce((a, b) => 
      b[1] > a[1] ? b : a
    )[0] as 'ENTER' | 'EXIT' | 'HOLD' | 'SKIP';
    
    // Aggregate reasoning
    const allReasoning = decisions.flatMap(d => d.reasoning);
    
    return {
      action: consensusAction,
      confidence: avgConfidence,
      reasoning: [`🐝 Swarm consensus from ${decisions.length} agents:`, ...allReasoning],
      marketState: decisions[0].marketState,
      riskLevel: decisions[0].riskLevel,
      timestamp: new Date()
    };
  }

  /**
   * Gets the decision engine
   */
  getDecisionEngine(): XAIDecisionEngine {
    return this.decisionEngine;
  }

  /**
   * Gets the PID controller
   */
  getPIDController(): PIDRANCOController {
    return this.pidController;
  }
}
