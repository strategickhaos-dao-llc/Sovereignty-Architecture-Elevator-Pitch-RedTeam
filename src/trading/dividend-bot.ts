/**
 * Dividend Capture Bot - Main Orchestrator
 * 
 * Integrates all components:
 * - NinjaTrader integration
 * - Dividend capture strategies
 * - XAI decision engine
 * - Discord notifications
 */

import { DividendCaptureStrategy, DividendEvent } from './dividend-capture.js';
import { NinjaTraderIntegration, NinjaTraderConfig, BacktestConfig } from './ninjatrader-integration.js';
import { XAISwarm, XAIDecision } from './xai-layer.js';

export interface BotConfig {
  ninjatrader: NinjaTraderConfig;
  strategy: {
    methods: ('options' | 'futures' | 'drip')[];
    minYield: number;
    maxDeltaRisk: number;
    scanIntervalHours: number;
  };
  notifications: {
    discordEnabled: boolean;
    discordChannelId?: string;
  };
  backtest?: BacktestConfig;
}

/**
 * Main Dividend Capture Bot
 */
export class DividendCaptureBot {
  private config: BotConfig;
  private ninjaTrader: NinjaTraderIntegration;
  private strategy: DividendCaptureStrategy;
  private xaiSwarm: XAISwarm;
  private isRunning: boolean = false;
  private scanInterval?: NodeJS.Timeout;

  constructor(config: BotConfig) {
    this.config = config;
    this.ninjaTrader = new NinjaTraderIntegration(config.ninjatrader);
    this.strategy = new DividendCaptureStrategy();
    this.xaiSwarm = new XAISwarm();
  }

  /**
   * Starts the dividend capture bot
   */
  async start(): Promise<void> {
    console.log('\n🚀 Starting Dividend Capture Bot');
    console.log('━'.repeat(60));
    
    // Connect to NinjaTrader
    const connected = await this.ninjaTrader.connect();
    if (!connected) {
      throw new Error('Failed to connect to NinjaTrader');
    }

    console.log(`✓ Mode: ${this.config.ninjatrader.mode.toUpperCase()}`);
    console.log(`✓ Data Feed: ${this.config.ninjatrader.dataFeedProvider}`);
    console.log(`✓ Methods: ${this.config.strategy.methods.join(', ')}`);
    console.log(`✓ Min Yield: ${(this.config.strategy.minYield * 100).toFixed(2)}%`);
    
    if (this.config.ninjatrader.mode === 'sim') {
      console.log('\n⚠️  SIM MODE - Zero real money at risk');
      console.log('Test your strategy thoroughly before switching to live mode.');
    } else {
      console.log('\n⚡ LIVE MODE - Real money at risk!');
    }

    this.isRunning = true;

    // Run initial scan
    await this.scan();

    // Set up periodic scanning
    const intervalMs = this.config.strategy.scanIntervalHours * 60 * 60 * 1000;
    this.scanInterval = setInterval(() => {
      if (this.isRunning) {
        this.scan().catch(console.error);
      }
    }, intervalMs);

    console.log(`\n✓ Bot started - scanning every ${this.config.strategy.scanIntervalHours} hours`);
    console.log('━'.repeat(60));
  }

  /**
   * Stops the dividend capture bot
   */
  async stop(): Promise<void> {
    console.log('\n🛑 Stopping Dividend Capture Bot...');
    
    this.isRunning = false;
    
    if (this.scanInterval) {
      clearInterval(this.scanInterval);
      this.scanInterval = undefined;
    }

    await this.ninjaTrader.disconnect();
    
    console.log('✓ Bot stopped');
  }

  /**
   * Performs a scan for dividend opportunities
   */
  async scan(): Promise<void> {
    console.log('\n🔍 Scanning for dividend capture opportunities...');
    console.log(`Timestamp: ${new Date().toISOString()}`);
    
    try {
      // Get upcoming dividends
      const scanner = this.strategy.getScanner();
      const upcomingDividends = await scanner.scanUpcomingDividends(
        this.config.strategy.minYield,
        30 // Look 30 days ahead
      );

      console.log(`Found ${upcomingDividends.length} potential opportunities`);

      // Analyze each opportunity with XAI
      for (const dividend of upcomingDividends) {
        await this.analyzeAndExecute(dividend);
      }

      // Notify via Discord if enabled
      if (this.config.notifications.discordEnabled && this.config.notifications.discordChannelId) {
        await this.notifyDiscord(
          `Scan complete: Found ${upcomingDividends.length} dividend opportunities`
        );
      }

    } catch (error) {
      console.error('Error during scan:', error);
    }
  }

  /**
   * Analyzes a dividend opportunity and executes if favorable
   */
  private async analyzeAndExecute(dividend: DividendEvent): Promise<void> {
    console.log(`\n📊 Analyzing ${dividend.ticker}`);
    console.log(`Dividend: $${dividend.dividendAmount}, Yield: ${(dividend.yield * 100).toFixed(2)}%`);
    console.log(`Ex-div date: ${dividend.exDivDate.toISOString()}`);

    // Get XAI swarm analysis
    const decisions = await this.xaiSwarm.swarmAnalysis(dividend);
    const consensus = this.xaiSwarm.getSwarmConsensus(decisions);

    // Display XAI reasoning
    console.log('\n🤖 XAI Analysis:');
    console.log(`Action: ${consensus.action}`);
    console.log(`Confidence: ${(consensus.confidence * 100).toFixed(1)}%`);
    console.log(`Risk Level: ${consensus.riskLevel.toUpperCase()}`);
    console.log('\nReasoning:');
    consensus.reasoning.forEach(reason => console.log(`  ${reason}`));

    // Execute trade if XAI recommends it
    if (consensus.action === 'ENTER' && consensus.confidence >= 0.7) {
      await this.executeDividendCapture(dividend, consensus);
    }
  }

  /**
   * Executes dividend capture trade
   */
  private async executeDividendCapture(dividend: DividendEvent, decision: XAIDecision): Promise<void> {
    console.log('\n💰 Executing dividend capture trade...');

    try {
      // Choose method based on configuration
      if (this.config.strategy.methods.includes('options')) {
        const optionsStrategy = this.strategy.getOptionsStrategy();
        const optimal = await optionsStrategy.findOptimalOptions(dividend.ticker, dividend);
        
        if (optimal) {
          const trade = await this.ninjaTrader.executeOptionsDividendCapture(optimal);
          console.log(`✓ Trade executed: ${trade.status}`);
          
          // Notify Discord
          if (this.config.notifications.discordEnabled) {
            await this.notifyDiscord(
              `💎 Dividend Capture: ${dividend.ticker}\n` +
              `Dividend: $${dividend.dividendAmount}\n` +
              `Confidence: ${(decision.confidence * 100).toFixed(1)}%\n` +
              `Status: ${trade.status}`
            );
          }
        }
      }

    } catch (error) {
      console.error('Error executing trade:', error);
      
      if (this.config.notifications.discordEnabled) {
        await this.notifyDiscord(`⚠️ Trade execution failed for ${dividend.ticker}: ${error}`);
      }
    }
  }

  /**
   * Runs backtest with historical data
   */
  async runBacktest(): Promise<void> {
    if (!this.config.backtest) {
      throw new Error('Backtest configuration not provided');
    }

    console.log('\n📈 Running Backtest');
    console.log('━'.repeat(60));
    
    const result = await this.ninjaTrader.runBacktest(
      this.config.backtest,
      this.strategy
    );

    console.log('\n📊 Backtest Complete');
    console.log(`Total Return: ${result.totalReturn.toFixed(2)}%`);
    console.log(`Dividend Income: $${result.dividendIncome.toLocaleString()}`);
    console.log(`Total Trades: ${result.trades}`);
    console.log(`Win Rate: ${(result.winRate * 100).toFixed(1)}%`);
    console.log(`Sharpe Ratio: ${result.sharpeRatio.toFixed(2)}`);
    console.log(`Max Drawdown: ${(result.maxDrawdown * 100).toFixed(2)}%`);
    console.log('━'.repeat(60));

    // Notify Discord with results
    if (this.config.notifications.discordEnabled) {
      await this.notifyDiscord(
        `📈 Backtest Results\n` +
        `Return: ${result.totalReturn.toFixed(2)}%\n` +
        `Dividend Income: $${result.dividendIncome.toLocaleString()}\n` +
        `Trades: ${result.trades}\n` +
        `Win Rate: ${(result.winRate * 100).toFixed(1)}%`
      );
    }
  }

  /**
   * Switches from sim to live mode (after testing)
   */
  async switchToLive(): Promise<void> {
    if (this.config.ninjatrader.mode === 'live') {
      console.log('Already in live mode');
      return;
    }

    console.log('\n⚠️  SWITCHING TO LIVE MODE ⚠️');
    console.log('This will enable real money trading!');
    console.log('Press Ctrl+C within 10 seconds to cancel...');

    // Wait 10 seconds for user to cancel
    await new Promise(resolve => setTimeout(resolve, 10000));

    await this.ninjaTrader.switchToLive();
    this.config.ninjatrader.mode = 'live';

    console.log('✓ Now trading with REAL MONEY');
    
    if (this.config.notifications.discordEnabled) {
      await this.notifyDiscord('⚡ Bot switched to LIVE MODE - real money trading active!');
    }
  }

  /**
   * Sends notification to Discord
   */
  private async notifyDiscord(message: string): Promise<void> {
    if (!this.config.notifications.discordEnabled || !this.config.notifications.discordChannelId) {
      return;
    }

    try {
      // Integration with existing Discord bot would go here
      console.log(`\n📢 Discord notification: ${message}`);
    } catch (error) {
      console.error('Failed to send Discord notification:', error);
    }
  }

  /**
   * Gets bot status
   */
  getStatus(): {
    running: boolean;
    mode: 'sim' | 'live';
    connected: boolean;
  } {
    return {
      running: this.isRunning,
      mode: this.config.ninjatrader.mode,
      connected: this.ninjaTrader.isConnectedToNinja()
    };
  }

  /**
   * Gets current configuration
   */
  getConfig(): BotConfig {
    return this.config;
  }
}

/**
 * Example usage and configuration
 */
export function createExampleBot(): DividendCaptureBot {
  const config: BotConfig = {
    ninjatrader: {
      mode: 'sim',
      dataFeedProvider: 'Polygon',
      enableATM: true,
      enableBasketTrader: true
    },
    strategy: {
      methods: ['options', 'drip'],
      minYield: 0.025, // 2.5% minimum yield
      maxDeltaRisk: 0.10, // 10% max delta risk
      scanIntervalHours: 6 // Scan every 6 hours
    },
    notifications: {
      discordEnabled: true,
      discordChannelId: process.env.TRADING_CHANNEL_ID
    },
    backtest: {
      startDate: new Date('2024-01-01'),
      endDate: new Date('2024-12-31'),
      initialCapital: 100000,
      includeDividends: true,
      includeCorporateActions: true
    }
  };

  return new DividendCaptureBot(config);
}
