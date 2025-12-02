/**
 * TypeScript types for portfolio rebalancing automation
 * Phase 1: Type definitions for Grok prompt contract
 * Phase 2: Will be used by validator and execution engine
 */

import { z } from 'zod';

// ============================================================================
// Portfolio Configuration Types (portfolio.yaml schema)
// ============================================================================

export const OwnerSchema = z.object({
  id: z.string(),
  name: z.string(),
  base_currency: z.string().default('USD'),
});

export const MetaSchema = z.object({
  last_reviewed: z.string(),
  rebalance_threshold_pct: z.number().min(0).max(100),
  paycheck_rebalance_pct: z.number().min(0).max(100),
  swarmgate_treasury_pct: z.number().min(0).max(100),
});

export const AccountSchema = z.object({
  id: z.string(),
  type: z.enum(['brokerage', 'treasury', 'retirement', 'crypto']),
  provider: z.string(),
  currency: z.string().default('USD'),
  allow_fractional_shares: z.boolean().default(false),
  execution_mode: z.enum(['auto', 'manual-review']).default('manual-review'),
  tags: z.array(z.string()).default([]),
});

export const BucketSchema = z.object({
  id: z.string(),
  label: z.string(),
  target_pct: z.number().min(0).max(100),
});

export const InstrumentSchema = z.object({
  symbol: z.string(),
  name: z.string(),
  bucket: z.string(),
  target_pct_of_portfolio: z.number().min(0).max(100),
  min_trade_size_usd: z.number().min(0),
  account_id: z.string(),
});

export const PositionConstraintsSchema = z.object({
  max_single_position_pct: z.number().min(0).max(100),
  max_bucket_pct_over_target: z.number().min(0).max(100),
  min_trade_usd: z.number().min(0),
});

export const LiquidityConstraintsSchema = z.object({
  keep_cash_buffer_pct: z.number().min(0).max(100),
});

export const ExecutionConstraintsSchema = z.object({
  rounding: z.object({
    fractional_precision: z.number().int().min(0).max(8),
  }),
  forbid_shorting: z.boolean().default(true),
  forbid_margin: z.boolean().default(true),
});

export const ConstraintsSchema = z.object({
  position: PositionConstraintsSchema,
  liquidity: LiquidityConstraintsSchema,
  execution: ExecutionConstraintsSchema,
});

export const SwarmgateSchema = z.object({
  treasury_account_id: z.string(),
  min_treasury_transfer_usd: z.number().min(0),
  tags: z.array(z.string()).default([]),
});

export const PortfolioConfigSchema = z.object({
  owner: OwnerSchema,
  meta: MetaSchema,
  accounts: z.array(AccountSchema),
  targets: z.object({
    buckets: z.array(BucketSchema),
    instruments: z.array(InstrumentSchema),
  }),
  constraints: ConstraintsSchema,
  swarmgate: SwarmgateSchema,
});

// ============================================================================
// Paycheck Event Types (Zapier input)
// ============================================================================

export const PaycheckEventSchema = z.object({
  paycheck_gross_usd: z.number().positive(),
  paycheck_net_usd: z.number().positive(),
  paycheck_date: z.string().datetime(),
  source: z.string(),
  memo: z.string().optional(),
});

// ============================================================================
// Portfolio Snapshot Types (Broker API response)
// ============================================================================

export const PositionSchema = z.object({
  symbol: z.string(),
  account_id: z.string(),
  shares: z.number().nonnegative(),
  price_usd: z.number().positive(),
});

export const PortfolioSnapshotSchema = z.object({
  total_portfolio_value_usd: z.number().nonnegative(),
  cash_available_usd: z.number().nonnegative(),
  positions: z.array(PositionSchema),
});

// ============================================================================
// Grok Output Types (Execution Plan)
// ============================================================================

export const SummarySchema = z.object({
  paycheck_net_usd: z.number(),
  investable_amount_usd: z.number(),
  treasury_amount_usd: z.number(),
  rebalance_amount_usd: z.number(),
  timestamp_utc: z.string().datetime(),
});

export const ChecksSchema = z.object({
  constraints_respected: z.boolean(),
  notes: z.array(z.string()),
});

export const TreasuryTransferSchema = z.object({
  account_id: z.string(),
  amount_usd: z.number().nonnegative(),
});

export const TradeSchema = z.object({
  symbol: z.string(),
  account_id: z.string(),
  action: z.enum(['BUY', 'SELL']),
  shares: z.number(),
  approx_value_usd: z.number(),
  reason: z.string(),
});

export const ExecutionPlanSchema = z.object({
  summary: SummarySchema,
  checks: ChecksSchema,
  treasury_transfer: TreasuryTransferSchema,
  trades: z.array(TradeSchema),
});

// ============================================================================
// TypeScript Type Exports
// ============================================================================

export type Owner = z.infer<typeof OwnerSchema>;
export type Meta = z.infer<typeof MetaSchema>;
export type Account = z.infer<typeof AccountSchema>;
export type Bucket = z.infer<typeof BucketSchema>;
export type Instrument = z.infer<typeof InstrumentSchema>;
export type PositionConstraints = z.infer<typeof PositionConstraintsSchema>;
export type LiquidityConstraints = z.infer<typeof LiquidityConstraintsSchema>;
export type ExecutionConstraints = z.infer<typeof ExecutionConstraintsSchema>;
export type Constraints = z.infer<typeof ConstraintsSchema>;
export type Swarmgate = z.infer<typeof SwarmgateSchema>;
export type PortfolioConfig = z.infer<typeof PortfolioConfigSchema>;
export type PaycheckEvent = z.infer<typeof PaycheckEventSchema>;
export type Position = z.infer<typeof PositionSchema>;
export type PortfolioSnapshot = z.infer<typeof PortfolioSnapshotSchema>;
export type Summary = z.infer<typeof SummarySchema>;
export type Checks = z.infer<typeof ChecksSchema>;
export type TreasuryTransfer = z.infer<typeof TreasuryTransferSchema>;
export type Trade = z.infer<typeof TradeSchema>;
export type ExecutionPlan = z.infer<typeof ExecutionPlanSchema>;

// ============================================================================
// Validation Input Type (for validator.ts)
// ============================================================================

export interface ValidationInput {
  paycheck: PaycheckEvent;
  snapshot: PortfolioSnapshot;
  config: PortfolioConfig;
  plan: ExecutionPlan;
}

export interface ValidationResult {
  valid: boolean;
  errors: string[];
  warnings: string[];
}
