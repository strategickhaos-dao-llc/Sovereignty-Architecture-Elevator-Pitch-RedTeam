/**
 * Validator for Grok-generated execution plans
 * Phase 2: Safety rails for automated portfolio rebalancing
 *
 * This validator can be used:
 * - As a Zapier Code step
 * - As a Cloud Function
 * - In a Node.js backend
 *
 * It verifies:
 * - Math correctness (investable, treasury, rebalance amounts)
 * - Constraint compliance (no margin, no shorting, min trade sizes)
 * - Trade direction correctness (moves toward targets)
 * - Hard guards (no negative shares, no over-spend)
 */

import {
  type PortfolioConfig,
  type PaycheckEvent,
  type PortfolioSnapshot,
  type ExecutionPlan,
  type ValidationInput,
  type ValidationResult,
  type Trade,
  ExecutionPlanSchema,
  PortfolioConfigSchema,
  PaycheckEventSchema,
  PortfolioSnapshotSchema,
} from './types.js';

/**
 * Main validation function
 * Returns validation result with errors and warnings
 */
export function validateExecutionPlan(input: ValidationInput): ValidationResult {
  const errors: string[] = [];
  const warnings: string[] = [];

  // 1. Validate schema compliance
  const schemaErrors = validateSchemas(input);
  errors.push(...schemaErrors);

  if (schemaErrors.length > 0) {
    return { valid: false, errors, warnings };
  }

  // 2. Validate math correctness
  const mathErrors = validateMath(input.paycheck, input.config, input.plan);
  errors.push(...mathErrors);

  // 3. Validate constraint compliance
  const constraintErrors = validateConstraints(input.config, input.snapshot, input.plan);
  errors.push(...constraintErrors);

  // 4. Validate trade direction
  const directionWarnings = validateTradeDirection(input.config, input.snapshot, input.plan);
  warnings.push(...directionWarnings);

  // 5. Validate hard guards
  const guardErrors = validateHardGuards(input.snapshot, input.plan);
  errors.push(...guardErrors);

  return {
    valid: errors.length === 0,
    errors,
    warnings,
  };
}

/**
 * Validate all input schemas
 */
function validateSchemas(input: ValidationInput): string[] {
  const errors: string[] = [];

  const paycheckResult = PaycheckEventSchema.safeParse(input.paycheck);
  if (!paycheckResult.success) {
    errors.push(`Invalid paycheck event: ${paycheckResult.error.message}`);
  }

  const snapshotResult = PortfolioSnapshotSchema.safeParse(input.snapshot);
  if (!snapshotResult.success) {
    errors.push(`Invalid portfolio snapshot: ${snapshotResult.error.message}`);
  }

  const configResult = PortfolioConfigSchema.safeParse(input.config);
  if (!configResult.success) {
    errors.push(`Invalid portfolio config: ${configResult.error.message}`);
  }

  const planResult = ExecutionPlanSchema.safeParse(input.plan);
  if (!planResult.success) {
    errors.push(`Invalid execution plan: ${planResult.error.message}`);
  }

  return errors;
}

/**
 * Validate mathematical correctness of the plan
 */
function validateMath(
  paycheck: PaycheckEvent,
  config: PortfolioConfig,
  plan: ExecutionPlan
): string[] {
  const errors: string[] = [];
  const tolerance = 0.01; // $0.01 tolerance for rounding

  // Calculate expected values
  const expectedInvestable = paycheck.paycheck_net_usd * (config.meta.paycheck_rebalance_pct / 100);
  const expectedTreasury = expectedInvestable * (config.meta.swarmgate_treasury_pct / 100);
  const expectedRebalance = expectedInvestable - expectedTreasury;

  // Validate investable amount
  if (Math.abs(plan.summary.investable_amount_usd - expectedInvestable) > tolerance) {
    errors.push(
      `Investable amount mismatch: expected ${expectedInvestable.toFixed(2)}, got ${plan.summary.investable_amount_usd.toFixed(2)}`
    );
  }

  // Validate treasury amount
  if (Math.abs(plan.summary.treasury_amount_usd - expectedTreasury) > tolerance) {
    errors.push(
      `Treasury amount mismatch: expected ${expectedTreasury.toFixed(2)}, got ${plan.summary.treasury_amount_usd.toFixed(2)}`
    );
  }

  // Validate rebalance amount
  if (Math.abs(plan.summary.rebalance_amount_usd - expectedRebalance) > tolerance) {
    errors.push(
      `Rebalance amount mismatch: expected ${expectedRebalance.toFixed(2)}, got ${plan.summary.rebalance_amount_usd.toFixed(2)}`
    );
  }

  // Validate treasury transfer matches summary
  if (Math.abs(plan.treasury_transfer.amount_usd - plan.summary.treasury_amount_usd) > tolerance) {
    errors.push(
      `Treasury transfer amount ${plan.treasury_transfer.amount_usd.toFixed(2)} does not match summary ${plan.summary.treasury_amount_usd.toFixed(2)}`
    );
  }

  // Validate total BUY trade value doesn't exceed rebalance amount
  // (SELL trades free up cash, so we only check BUY trades against the rebalance budget)
  const totalBuyValue = plan.trades
    .filter((t) => t.action === 'BUY')
    .reduce((sum, t) => sum + t.approx_value_usd, 0);

  if (totalBuyValue > plan.summary.rebalance_amount_usd + tolerance) {
    errors.push(
      `Total BUY value ${totalBuyValue.toFixed(2)} exceeds rebalance amount ${plan.summary.rebalance_amount_usd.toFixed(2)}`
    );
  }

  return errors;
}

/**
 * Validate constraint compliance
 */
function validateConstraints(
  config: PortfolioConfig,
  snapshot: PortfolioSnapshot,
  plan: ExecutionPlan
): string[] {
  const errors: string[] = [];

  // Check forbid_shorting constraint
  if (config.constraints.execution.forbid_shorting) {
    for (const trade of plan.trades) {
      if (trade.action === 'SELL') {
        const position = snapshot.positions.find((p) => p.symbol === trade.symbol);
        const currentShares = position?.shares ?? 0;
        if (trade.shares > currentShares) {
          errors.push(
            `Trade would result in short position: selling ${trade.shares} shares of ${trade.symbol}, but only have ${currentShares}`
          );
        }
      }
    }
  }

  // Check forbid_margin constraint (no buying more than available cash + sales)
  if (config.constraints.execution.forbid_margin) {
    const sellValue = plan.trades
      .filter((t) => t.action === 'SELL')
      .reduce((sum, t) => sum + t.approx_value_usd, 0);
    const buyValue = plan.trades
      .filter((t) => t.action === 'BUY')
      .reduce((sum, t) => sum + t.approx_value_usd, 0);

    const availableForBuying = snapshot.cash_available_usd + sellValue;
    if (buyValue > availableForBuying) {
      errors.push(
        `Trades require margin: buying ${buyValue.toFixed(2)} but only ${availableForBuying.toFixed(2)} available`
      );
    }
  }

  // Check minimum trade sizes
  for (const trade of plan.trades) {
    const instrument = config.targets.instruments.find((i) => i.symbol === trade.symbol);
    const minSize = instrument?.min_trade_size_usd ?? config.constraints.position.min_trade_usd;

    if (trade.approx_value_usd < minSize) {
      errors.push(
        `Trade for ${trade.symbol} ($${trade.approx_value_usd.toFixed(2)}) is below minimum trade size ($${minSize})`
      );
    }
  }

  // Check cash buffer requirement
  // Account for: incoming rebalance amount + SELL proceeds - BUY costs - treasury transfer
  const requiredBuffer =
    snapshot.total_portfolio_value_usd * (config.constraints.liquidity.keep_cash_buffer_pct / 100);
  const incomingCash = plan.summary.rebalance_amount_usd + plan.summary.treasury_amount_usd;
  const sellProceeds = plan.trades
    .filter((t) => t.action === 'SELL')
    .reduce((sum, t) => sum + t.approx_value_usd, 0);
  const buyCosts = plan.trades
    .filter((t) => t.action === 'BUY')
    .reduce((sum, t) => sum + t.approx_value_usd, 0);
  const netCashChange = incomingCash + sellProceeds - buyCosts - plan.treasury_transfer.amount_usd;

  const projectedCash = snapshot.cash_available_usd + netCashChange;
  if (projectedCash < requiredBuffer) {
    errors.push(
      `Projected cash ${projectedCash.toFixed(2)} would be below required buffer ${requiredBuffer.toFixed(2)}`
    );
  }

  return errors;
}

/**
 * Validate trade direction moves toward targets (warnings only)
 */
function validateTradeDirection(
  config: PortfolioConfig,
  snapshot: PortfolioSnapshot,
  plan: ExecutionPlan
): string[] {
  const warnings: string[] = [];

  // Calculate current weights
  const totalValue = snapshot.total_portfolio_value_usd;
  const currentWeights = new Map<string, number>();

  for (const position of snapshot.positions) {
    const value = position.shares * position.price_usd;
    currentWeights.set(position.symbol, (value / totalValue) * 100);
  }

  // Check each trade moves in correct direction
  for (const trade of plan.trades) {
    const instrument = config.targets.instruments.find((i) => i.symbol === trade.symbol);
    if (!instrument) continue;

    const currentWeight = currentWeights.get(trade.symbol) ?? 0;
    const targetWeight = instrument.target_pct_of_portfolio;
    const isUnderweight = currentWeight < targetWeight;

    if (trade.action === 'BUY' && !isUnderweight) {
      warnings.push(
        `Buying ${trade.symbol} but it's already at or above target (${currentWeight.toFixed(1)}% vs ${targetWeight}% target)`
      );
    }

    if (trade.action === 'SELL' && isUnderweight) {
      warnings.push(
        `Selling ${trade.symbol} but it's below target (${currentWeight.toFixed(1)}% vs ${targetWeight}% target)`
      );
    }
  }

  return warnings;
}

/**
 * Validate hard guards (critical safety checks)
 */
function validateHardGuards(snapshot: PortfolioSnapshot, plan: ExecutionPlan): string[] {
  const errors: string[] = [];

  // No negative shares
  for (const trade of plan.trades) {
    if (trade.shares < 0) {
      errors.push(`Invalid negative shares for ${trade.symbol}: ${trade.shares}`);
    }
  }

  // No negative values
  for (const trade of plan.trades) {
    if (trade.approx_value_usd < 0) {
      errors.push(`Invalid negative value for ${trade.symbol}: $${trade.approx_value_usd}`);
    }
  }

  // Treasury transfer must be non-negative
  if (plan.treasury_transfer.amount_usd < 0) {
    errors.push(`Invalid negative treasury transfer: $${plan.treasury_transfer.amount_usd}`);
  }

  // Validate summary amounts are non-negative
  if (plan.summary.investable_amount_usd < 0) {
    errors.push(`Invalid negative investable amount: $${plan.summary.investable_amount_usd}`);
  }

  if (plan.summary.rebalance_amount_usd < 0) {
    errors.push(`Invalid negative rebalance amount: $${plan.summary.rebalance_amount_usd}`);
  }

  return errors;
}

/**
 * Generate a human-readable dry-run summary
 * For email/Slack review before execution
 */
export function generateDryRunSummary(
  input: ValidationInput,
  validation: ValidationResult
): string {
  const { paycheck, snapshot, plan } = input;

  const lines: string[] = [
    '# Portfolio Rebalance - Dry Run Summary',
    '',
    `**Date:** ${plan.summary.timestamp_utc}`,
    `**Paycheck:** $${paycheck.paycheck_net_usd.toFixed(2)} (net)`,
    '',
    '## Allocation Breakdown',
    '',
    `| Item | Amount |`,
    `|------|--------|`,
    `| Investable (${input.config.meta.paycheck_rebalance_pct}% of net) | $${plan.summary.investable_amount_usd.toFixed(2)} |`,
    `| Treasury (${input.config.meta.swarmgate_treasury_pct}%) | $${plan.summary.treasury_amount_usd.toFixed(2)} |`,
    `| Available for Trades | $${plan.summary.rebalance_amount_usd.toFixed(2)} |`,
    '',
    '## Treasury Transfer',
    '',
    `→ **$${plan.treasury_transfer.amount_usd.toFixed(2)}** to \`${plan.treasury_transfer.account_id}\``,
    '',
    '## Proposed Trades',
    '',
    `| Action | Symbol | Shares | Est. Value | Reason |`,
    `|--------|--------|--------|------------|--------|`,
  ];

  for (const trade of plan.trades) {
    lines.push(
      `| ${trade.action} | ${trade.symbol} | ${trade.shares.toFixed(4)} | $${trade.approx_value_usd.toFixed(2)} | ${trade.reason} |`
    );
  }

  lines.push('');
  lines.push('## Validation Status');
  lines.push('');

  if (validation.valid) {
    lines.push('✅ **All checks passed**');
  } else {
    lines.push('❌ **Validation failed**');
    lines.push('');
    lines.push('### Errors');
    for (const error of validation.errors) {
      lines.push(`- ${error}`);
    }
  }

  if (validation.warnings.length > 0) {
    lines.push('');
    lines.push('### Warnings');
    for (const warning of validation.warnings) {
      lines.push(`- ⚠️ ${warning}`);
    }
  }

  if (plan.checks.notes.length > 0) {
    lines.push('');
    lines.push('### Notes from Grok');
    for (const note of plan.checks.notes) {
      lines.push(`- ${note}`);
    }
  }

  lines.push('');
  lines.push('---');
  lines.push('');
  lines.push(
    `**Portfolio Value:** $${snapshot.total_portfolio_value_usd.toFixed(2)} | **Cash Available:** $${snapshot.cash_available_usd.toFixed(2)}`
  );

  return lines.join('\n');
}

/**
 * Parse and validate a raw Grok JSON response
 */
export function parseGrokResponse(rawJson: string): { plan: ExecutionPlan | null; error: string | null } {
  try {
    const parsed = JSON.parse(rawJson);
    const result = ExecutionPlanSchema.safeParse(parsed);

    if (result.success) {
      return { plan: result.data, error: null };
    } else {
      return { plan: null, error: `Schema validation failed: ${result.error.message}` };
    }
  } catch (err) {
    return { plan: null, error: `JSON parse error: ${err instanceof Error ? err.message : 'Unknown error'}` };
  }
}

export default {
  validateExecutionPlan,
  generateDryRunSummary,
  parseGrokResponse,
};
