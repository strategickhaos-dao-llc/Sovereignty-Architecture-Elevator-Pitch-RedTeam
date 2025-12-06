/**
 * Example: Dividend Capture Bot Usage
 * 
 * This example demonstrates how to use the dividend capture bot
 * with NinjaTrader integration and XAI decision-making.
 */

import { DividendCaptureBot, BotConfig } from '../src/trading/dividend-bot.js';
import { DividendCaptureStrategy } from '../src/trading/dividend-capture.js';
import { XAISwarm } from '../src/trading/xai-layer.js';

/**
 * Example 1: Simple Dividend Scanner
 */
async function exampleDividendScanner() {
  console.log('='.repeat(60));
  console.log('Example 1: Dividend Scanner');
  console.log('='.repeat(60));

  const strategy = new DividendCaptureStrategy();
  const scanner = strategy.getScanner();

  // Get dividend aristocrats
  const aristocrats = scanner.getDividendAristocrats();
  console.log('\n💎 Dividend Aristocrats:');
  console.log(aristocrats.join(', '));

  // Scan for upcoming dividends
  const upcomingDividends = await scanner.scanUpcomingDividends(0.025, 30);
  console.log(`\n📊 Found ${upcomingDividends.length} upcoming dividend opportunities`);
}

/**
 * Example 2: Options Dividend Capture Analysis
 */
async function exampleOptionsCapture() {
  console.log('\n' + '='.repeat(60));
  console.log('Example 2: Options Dividend Capture');
  console.log('='.repeat(60));

  const strategy = new DividendCaptureStrategy();
  const optionsStrategy = strategy.getOptionsStrategy();

  // Example dividend event
  const dividend = {
    ticker: 'T',
    exDivDate: new Date('2026-01-09'),
    paymentDate: new Date('2026-02-01'),
    dividendAmount: 0.2775,
    frequency: 'quarterly' as const,
    yield: 0.0389
  };

  console.log(`\n📊 Analyzing options for ${dividend.ticker}`);
  console.log(`Dividend: $${dividend.dividendAmount}`);
  console.log(`Yield: ${(dividend.yield * 100).toFixed(2)}%`);

  // Find optimal options strategy
  const optimal = await optionsStrategy.findOptimalOptions(dividend.ticker, dividend);
  
  if (optimal) {
    const expectedReturn = optionsStrategy.calculateExpectedReturn(optimal);
    const isValid = optionsStrategy.validateStrategy(optimal);
    
    console.log(`\nExpected Return: ${(expectedReturn * 100).toFixed(2)}%`);
    console.log(`Strategy Valid: ${isValid ? '✓' : '✗'}`);
  }
}

/**
 * Example 3: XAI Analysis
 */
async function exampleXAIAnalysis() {
  console.log('\n' + '='.repeat(60));
  console.log('Example 3: XAI Swarm Analysis');
  console.log('='.repeat(60));

  const xaiSwarm = new XAISwarm();

  // Example dividend event
  const dividend = {
    ticker: 'KO',
    exDivDate: new Date('2026-03-15'),
    paymentDate: new Date('2026-04-01'),
    dividendAmount: 0.485,
    frequency: 'quarterly' as const,
    yield: 0.0312
  };

  console.log(`\n🤖 Running XAI Swarm Analysis for ${dividend.ticker}`);
  
  // Get swarm analysis
  const decisions = await xaiSwarm.swarmAnalysis(dividend);
  const consensus = xaiSwarm.getSwarmConsensus(decisions);

  console.log(`\nAction: ${consensus.action}`);
  console.log(`Confidence: ${(consensus.confidence * 100).toFixed(1)}%`);
  console.log(`Risk Level: ${consensus.riskLevel.toUpperCase()}`);
  console.log('\nReasoning:');
  consensus.reasoning.forEach(reason => console.log(`  ${reason}`));
}

/**
 * Example 4: Full Bot with Sim Mode
 */
async function exampleBotSimMode() {
  console.log('\n' + '='.repeat(60));
  console.log('Example 4: Full Bot in SIM Mode');
  console.log('='.repeat(60));

  const config: BotConfig = {
    ninjatrader: {
      mode: 'sim',  // SIM MODE - Zero real money at risk
      dataFeedProvider: 'Polygon',
      enableATM: true,
      enableBasketTrader: true
    },
    strategy: {
      methods: ['options', 'drip'],
      minYield: 0.025,
      maxDeltaRisk: 0.10,
      scanIntervalHours: 6
    },
    notifications: {
      discordEnabled: false  // Disable for example
    },
    backtest: {
      startDate: new Date('2024-01-01'),
      endDate: new Date('2024-12-31'),
      initialCapital: 100000,
      includeDividends: true,
      includeCorporateActions: true
    }
  };

  const bot = new DividendCaptureBot(config);

  // Start the bot
  await bot.start();

  // Run a single scan
  await bot.scan();

  // Check status
  const status = bot.getStatus();
  console.log('\n📊 Bot Status:');
  console.log(`Running: ${status.running}`);
  console.log(`Mode: ${status.mode.toUpperCase()}`);
  console.log(`Connected: ${status.connected}`);

  // Stop the bot
  await bot.stop();
}

/**
 * Example 5: Backtest with Historical Data
 */
async function exampleBacktest() {
  console.log('\n' + '='.repeat(60));
  console.log('Example 5: Backtest with Dividend Data');
  console.log('='.repeat(60));

  const config: BotConfig = {
    ninjatrader: {
      mode: 'sim',
      dataFeedProvider: 'Polygon',
      enableATM: true,
      enableBasketTrader: true
    },
    strategy: {
      methods: ['options'],
      minYield: 0.03,
      maxDeltaRisk: 0.10,
      scanIntervalHours: 12
    },
    notifications: {
      discordEnabled: false
    },
    backtest: {
      startDate: new Date('2023-01-01'),
      endDate: new Date('2023-12-31'),
      initialCapital: 50000,
      includeDividends: true,  // CRITICAL: Include dividend credits
      includeCorporateActions: true,
      tickDataPath: '/path/to/historical/data'
    }
  };

  const bot = new DividendCaptureBot(config);
  
  console.log('\n🧪 Running backtest...');
  await bot.runBacktest();
}

/**
 * Example 6: DRIP Strategy
 */
async function exampleDRIPStrategy() {
  console.log('\n' + '='.repeat(60));
  console.log('Example 6: DRIP Strategy (Dividend Aristocrats)');
  console.log('='.repeat(60));

  const strategy = new DividendCaptureStrategy();
  const dripStrategy = strategy.getDRIPStrategy();

  // Build portfolio
  console.log('\n💎 Building dividend aristocrats portfolio...');
  const portfolio = await dripStrategy.buildPortfolio(20, 0.025);

  // Calculate DRIP growth
  const initialInvestment = 100000;
  const avgYield = 0.035;
  const years = 20;
  
  const futureValue = dripStrategy.calculateDRIPGrowth(initialInvestment, avgYield, years);
  
  console.log(`\n📈 DRIP Compound Growth Calculation:`);
  console.log(`Initial Investment: $${initialInvestment.toLocaleString()}`);
  console.log(`Average Yield: ${(avgYield * 100).toFixed(2)}%`);
  console.log(`Time Horizon: ${years} years`);
  console.log(`Future Value: $${futureValue.toLocaleString()}`);
  console.log(`Total Return: ${((futureValue / initialInvestment - 1) * 100).toFixed(2)}%`);

  // Get rebalancing recommendations
  const actions = await dripStrategy.getRebalancingActions();
  console.log(`\n🔄 Monthly Rebalancing:`);
  console.log(`Buy: ${actions.buy.length} positions`);
  console.log(`Sell: ${actions.sell.length} positions`);
  console.log(`Hold: ${actions.hold.length} positions`);
}

/**
 * Example 7: Real-World AT&T Example
 */
async function exampleATTDividend() {
  console.log('\n' + '='.repeat(60));
  console.log('Example 7: Real AT&T Dividend Capture (2025)');
  console.log('='.repeat(60));

  const xaiSwarm = new XAISwarm();
  const decisionEngine = xaiSwarm.getDecisionEngine();

  // Real AT&T dividend data
  const dividend = {
    ticker: 'T',
    exDivDate: new Date('2026-01-09'),
    paymentDate: new Date('2026-02-01'),
    dividendAmount: 0.2775,
    frequency: 'quarterly' as const,
    yield: 0.0389
  };

  // Example options strategy
  const optionsStrategy = {
    ticker: 'T',
    strike: 20,
    expiration: new Date('2026-01-16'),
    premium: 2.50,
    stockPrice: 22.40,
    dividendCapture: 0.2775,
    deltaRisk: 0.15,
    expectedReturn: 0.111
  };

  console.log('\n📊 AT&T Dividend Capture Analysis');
  console.log(`Stock Price: $${optionsStrategy.stockPrice}`);
  console.log(`Dividend: $${dividend.dividendAmount}`);
  console.log(`Ex-Div Date: ${dividend.exDivDate.toISOString().split('T')[0]}`);
  
  // XAI analysis of options strategy
  const decision = await decisionEngine.analyzeOptionsStrategy(optionsStrategy);
  
  console.log(`\n🤖 XAI Decision:`);
  console.log(`Action: ${decision.action}`);
  console.log(`Confidence: ${(decision.confidence * 100).toFixed(1)}%`);
  console.log(`Risk: ${decision.riskLevel.toUpperCase()}`);
  console.log('\nReasoning:');
  decision.reasoning.forEach(reason => console.log(`  ${reason}`));

  // Calculate potential return
  const contractValue = optionsStrategy.premium * 100;
  const dividendCapture = optionsStrategy.dividendCapture * 100;
  const netReturn = ((dividendCapture - optionsStrategy.deltaRisk * 100) / contractValue) * 100;
  
  console.log(`\n💰 Return Calculation:`);
  console.log(`Contract Cost: $${contractValue.toFixed(2)}`);
  console.log(`Dividend Capture: $${dividendCapture.toFixed(2)}`);
  console.log(`Delta Risk: $${(optionsStrategy.deltaRisk * 100).toFixed(2)}`);
  console.log(`Net Return: ${netReturn.toFixed(2)}%`);
  console.log(`Annualized: ${(netReturn * 365).toFixed(0)}%`);
}

/**
 * Main function - runs all examples
 */
async function main() {
  console.log('\n🚀 Dividend Capture Bot - Examples\n');

  try {
    await exampleDividendScanner();
    await exampleOptionsCapture();
    await exampleXAIAnalysis();
    await exampleBotSimMode();
    await exampleBacktest();
    await exampleDRIPStrategy();
    await exampleATTDividend();

    console.log('\n' + '='.repeat(60));
    console.log('✓ All examples completed successfully!');
    console.log('='.repeat(60));
    console.log('\n💎 Ready to farm dividends with love.');
    console.log('Deploy it. The market pays. Your bot collects.');
    console.log('\n');

  } catch (error) {
    console.error('\n❌ Error running examples:', error);
  }
}

// Run if this is the main module
if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch(console.error);
}

export {
  exampleDividendScanner,
  exampleOptionsCapture,
  exampleXAIAnalysis,
  exampleBotSimMode,
  exampleBacktest,
  exampleDRIPStrategy,
  exampleATTDividend
};
