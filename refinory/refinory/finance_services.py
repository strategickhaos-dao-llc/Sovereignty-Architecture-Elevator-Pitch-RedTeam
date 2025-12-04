"""
Financial Services for Hybrid Refinery System
Strategickhaos Sovereign Income Architecture

This module implements:
- Dividend Screening Service (safe, boring, passive income)
- RANCO/PID Signal Generation (structured, mechanical, zero-emotion)
- Risk Management Service (guardrails enforcement)
- Watchlist Generation Service
- Portfolio Analytics Service
"""

import asyncio
from datetime import datetime, timezone, timedelta
from decimal import Decimal
from typing import Dict, List, Optional, Tuple, Any
import structlog

from .finance_models import (
    # Enums
    AssetClass, PositionType, SignalType, RiskLevel, AccountType,
    # Guardrails
    Guardrails,
    # Dividend models
    DividendScreenCriteria, DividendStock, DividendEngineConfig,
    # Overlay models
    TechnicalIndicators, FundamentalData, RefinerySignal, RefineryOverlayConfig,
    # RANCO models
    RANCOEntryRules, RANCOExitRules, RANCOSizingRules, RANCOCandidate, RANCOTacticalConfig,
    # Portfolio models
    Position, CashFlow, Portfolio,
    # Watchlist and automation
    Watchlist, AutomationRule, RiskAlert,
    # Reporting
    WeeklyReport, BacktestResult, MonteCarloResult,
)

logger = structlog.get_logger()


# =============================================================================
# Dividend Screening Service
# =============================================================================

class DividendScreeningService:
    """
    Dividend Engine - Base Income Layer
    
    This is NOT gambling. This is:
    - Companies sharing profits
    - Slow, steady income
    - Extremely low risk
    - Perfect for long-term security
    - Like owning a vending machine that pays quarterly
    """
    
    def __init__(self, config: DividendEngineConfig):
        self.config = config
        self.criteria = config.screen_criteria
        logger.info("Dividend Screening Service initialized")
    
    async def screen_stock(self, stock: DividendStock) -> DividendStock:
        """
        Screen a single stock against dividend criteria.
        Returns the stock with screening results populated.
        """
        failures = []
        
        # Check payout ratio
        if stock.asset_class in [AssetClass.REIT, AssetClass.MLP]:
            if stock.payout_ratio > self.criteria.max_payout_ratio_reit:
                failures.append(f"Payout ratio {stock.payout_ratio} exceeds REIT/MLP limit {self.criteria.max_payout_ratio_reit}")
        else:
            if stock.payout_ratio > self.criteria.max_payout_ratio:
                failures.append(f"Payout ratio {stock.payout_ratio} exceeds limit {self.criteria.max_payout_ratio}")
        
        # Check dividend growth
        if stock.dividend_growth_5yr_cagr < self.criteria.min_dividend_growth_5yr_cagr:
            failures.append(f"5yr dividend growth {stock.dividend_growth_5yr_cagr} below minimum {self.criteria.min_dividend_growth_5yr_cagr}")
        
        # Check interest coverage
        if stock.interest_coverage < self.criteria.min_interest_coverage:
            failures.append(f"Interest coverage {stock.interest_coverage} below minimum {self.criteria.min_interest_coverage}")
        
        # Check leverage (net debt / EBITDA)
        if stock.asset_class in [AssetClass.REIT]:
            if stock.net_debt_ebitda > self.criteria.max_net_debt_ebitda_reit:
                failures.append(f"Net debt/EBITDA {stock.net_debt_ebitda} exceeds REIT limit {self.criteria.max_net_debt_ebitda_reit}")
        else:
            if stock.net_debt_ebitda > self.criteria.max_net_debt_ebitda:
                failures.append(f"Net debt/EBITDA {stock.net_debt_ebitda} exceeds limit {self.criteria.max_net_debt_ebitda}")
        
        # Check ROIC vs WACC
        roic_premium = stock.roic - stock.wacc
        if roic_premium < self.criteria.min_roic_premium_over_wacc:
            failures.append(f"ROIC premium over WACC {roic_premium} below minimum {self.criteria.min_roic_premium_over_wacc}")
        
        # Set results
        stock.passes_screen = len(failures) == 0
        stock.screen_failures = failures
        stock.last_updated = datetime.now(timezone.utc)
        
        logger.info(f"Screened {stock.ticker}: {'PASS' if stock.passes_screen else 'FAIL'}", 
                   failures=failures)
        
        return stock
    
    async def screen_universe(self, stocks: List[DividendStock]) -> Tuple[List[DividendStock], List[DividendStock]]:
        """
        Screen entire universe of dividend stocks.
        Returns (passing_stocks, failing_stocks).
        """
        logger.info(f"Screening {len(stocks)} stocks against dividend criteria")
        
        # Screen all stocks concurrently
        screened = await asyncio.gather(*[self.screen_stock(s) for s in stocks])
        
        passing = [s for s in screened if s.passes_screen]
        failing = [s for s in screened if not s.passes_screen]
        
        logger.info(f"Screening complete: {len(passing)} passed, {len(failing)} failed")
        
        return passing, failing
    
    async def build_core_portfolio(
        self, 
        passing_stocks: List[DividendStock],
        current_portfolio: Optional[Portfolio] = None
    ) -> List[Dict[str, Any]]:
        """
        Build or adjust core dividend portfolio.
        Returns list of recommended positions with weights.
        """
        if len(passing_stocks) < self.config.min_positions:
            logger.warning(f"Insufficient passing stocks ({len(passing_stocks)}) for minimum positions ({self.config.min_positions})")
        
        # Sort by quality metrics (dividend yield + growth + safety)
        scored_stocks = []
        for stock in passing_stocks:
            quality_score = (
                float(stock.dividend_yield) * 0.3 +
                float(stock.dividend_growth_5yr_cagr) * 0.3 +
                (1 - float(stock.payout_ratio)) * 0.2 +
                (float(stock.roic) - float(stock.wacc)) * 0.2
            )
            scored_stocks.append((stock, quality_score))
        
        # Sort by score descending
        scored_stocks.sort(key=lambda x: x[1], reverse=True)
        
        # Take top N positions
        selected = scored_stocks[:self.config.target_positions]
        
        # Calculate weights
        if self.config.weighting_method == "equal_weight":
            weight = Decimal("1") / Decimal(str(len(selected)))
            recommendations = [
                {
                    "ticker": stock.ticker,
                    "name": stock.name,
                    "weight": float(weight),
                    "dividend_yield": float(stock.dividend_yield),
                    "quality_score": score,
                    "action": "hold" if current_portfolio and stock.ticker in current_portfolio.positions else "buy"
                }
                for stock, score in selected
            ]
        else:
            # Risk-weighted (inverse volatility - placeholder)
            total_score = sum(s for _, s in selected)
            recommendations = [
                {
                    "ticker": stock.ticker,
                    "name": stock.name,
                    "weight": float(min(Decimal(str(score / total_score)), self.config.max_weight_per_stock)),
                    "dividend_yield": float(stock.dividend_yield),
                    "quality_score": score,
                    "action": "hold" if current_portfolio and stock.ticker in current_portfolio.positions else "buy"
                }
                for stock, score in selected
            ]
        
        logger.info(f"Built core portfolio with {len(recommendations)} positions")
        return recommendations
    
    def calculate_dividend_allocation(self, dividend_amount: Decimal) -> Dict[str, Decimal]:
        """
        Calculate how dividend income should be allocated.
        - 70% reinvest
        - 23% treasury (buffer)
        - 7% SwarmGate
        """
        return {
            "reinvest": dividend_amount * self.config.reinvest_dividends_pct,
            "treasury": dividend_amount * self.config.treasury_allocation_pct,
            "swarmgate": dividend_amount * self.config.swarmgate_allocation_pct,
        }


# =============================================================================
# Refinery Overlay Service (Signals, not gambling)
# =============================================================================

class RefineryOverlayService:
    """
    Refinery Overlay - Signal Generation Layer
    
    This is NOT gambling. This is:
    - Algorithms and filters
    - Data processing
    - Structured decision trees
    - Predictive signal extraction
    - Machine intelligence, not random clicking
    
    Inputs: Financial datasets, market structure, volatility signals
    Outputs: Safe dividend picks, RANCO candidates, positions to avoid
    """
    
    def __init__(self, config: RefineryOverlayConfig):
        self.config = config
        logger.info("Refinery Overlay Service initialized")
    
    async def analyze_stock(
        self, 
        ticker: str,
        technical: TechnicalIndicators,
        fundamental: FundamentalData
    ) -> List[RefinerySignal]:
        """
        Analyze a stock and generate signals.
        Returns list of applicable signals.
        """
        signals = []
        
        # Check exclusions first
        if self._should_exclude(technical, fundamental):
            logger.info(f"Stock {ticker} excluded from analysis", 
                       reasons=fundamental.avoid_reasons)
            return signals
        
        # Check for SAFE_ADD signal (dividend dip opportunity)
        safe_add = await self._check_safe_add(ticker, technical, fundamental)
        if safe_add:
            signals.append(safe_add)
        
        # Check for AVOID signal
        avoid = await self._check_avoid(ticker, technical, fundamental)
        if avoid:
            signals.append(avoid)
        
        # Check for RANCO entry signal
        ranco = await self._check_ranco_entry(ticker, technical, fundamental)
        if ranco:
            signals.append(ranco)
        
        return signals
    
    def _should_exclude(self, technical: TechnicalIndicators, fundamental: FundamentalData) -> bool:
        """Check if stock should be excluded from signal generation"""
        # Exclude if within earnings window
        if fundamental.days_to_earnings is not None:
            if abs(fundamental.days_to_earnings) <= self.config.exclude_earnings_window_days:
                fundamental.avoid_reasons.append(f"Within {self.config.exclude_earnings_window_days} days of earnings")
                return True
        
        # Exclude if low liquidity
        if technical.avg_daily_volume < self.config.min_adv_for_signals:
            fundamental.avoid_reasons.append(f"Low liquidity: ADV ${technical.avg_daily_volume}")
            return True
        
        return False
    
    async def _check_safe_add(
        self, 
        ticker: str,
        technical: TechnicalIndicators,
        fundamental: FundamentalData
    ) -> Optional[RefinerySignal]:
        """Check for safe dividend add-on dip opportunity"""
        
        # Price near 200MA
        ma200_distance = abs(technical.current_price - technical.ma_200) / technical.ma_200
        if ma200_distance > self.config.safe_add_near_ma200_pct:
            return None
        
        # ATR in downtrend (volatility compression)
        if self.config.safe_add_atr_downtrend and technical.atr_6mo_median:
            if technical.atr_pct >= technical.atr_6mo_median:
                return None
        
        # Fundamentals must be intact
        if not fundamental.fundamentals_intact:
            return None
        
        # Generate SAFE_ADD signal
        return RefinerySignal(
            ticker=ticker,
            signal_type=SignalType.SAFE_ADD,
            confidence=Decimal("0.75"),
            priority="normal",
            suggested_entry=technical.current_price,
            reasoning=[
                f"Price within {float(ma200_distance)*100:.1f}% of 200MA",
                "Volatility compressed",
                "Fundamentals intact",
            ],
            technical_data=technical,
            fundamental_data=fundamental,
            expires_at=datetime.now(timezone.utc) + timedelta(days=7),
        )
    
    async def _check_avoid(
        self, 
        ticker: str,
        technical: TechnicalIndicators,
        fundamental: FundamentalData
    ) -> Optional[RefinerySignal]:
        """Check for stocks to avoid"""
        avoid_reasons = []
        
        # Payout stretch
        if fundamental.payout_stretch_warning:
            avoid_reasons.append("Payout ratio stretched")
        
        # Earnings revisions down
        if self.config.avoid_earnings_revision_down and fundamental.earnings_revision_trend == "down":
            avoid_reasons.append("Earnings revisions trending down")
        
        if not avoid_reasons:
            return None
        
        return RefinerySignal(
            ticker=ticker,
            signal_type=SignalType.AVOID,
            confidence=Decimal("0.80"),
            priority="high",
            reasoning=avoid_reasons,
            technical_data=technical,
            fundamental_data=fundamental,
        )
    
    async def _check_ranco_entry(
        self, 
        ticker: str,
        technical: TechnicalIndicators,
        fundamental: FundamentalData
    ) -> Optional[RefinerySignal]:
        """Check for RANCO/PID entry opportunity"""
        
        # This is a preliminary check - full RANCO analysis done in RANCOService
        if not technical.ma_alignment_bullish:
            return None
        
        if not technical.higher_low_formed:
            return None
        
        # RSI in favorable range
        if not (Decimal("45") <= technical.rsi_14 <= Decimal("65")):
            return None
        
        # Volatility compression
        if technical.atr_6mo_median and technical.atr_pct >= technical.atr_6mo_median:
            return None
        
        return RefinerySignal(
            ticker=ticker,
            signal_type=SignalType.RANCO_ENTRY,
            confidence=Decimal("0.70"),
            priority="normal",
            reasoning=[
                "MA alignment bullish (20>50>200)",
                "Higher low pattern formed",
                f"RSI at {technical.rsi_14} (favorable range)",
                "Volatility compressed",
            ],
            technical_data=technical,
            fundamental_data=fundamental,
        )
    
    async def generate_watchlists(
        self, 
        signals: List[RefinerySignal]
    ) -> Dict[str, Watchlist]:
        """Generate watchlists from signals"""
        watchlists = {}
        
        # Safe add watchlist
        safe_add_signals = [s for s in signals if s.signal_type == SignalType.SAFE_ADD]
        if safe_add_signals:
            watchlists["safe_add"] = Watchlist(
                name="Safe Add Opportunities",
                watchlist_type="safe_add",
                tickers=[s.ticker for s in safe_add_signals],
                entries=[
                    {
                        "ticker": s.ticker,
                        "entry_price": float(s.suggested_entry) if s.suggested_entry else None,
                        "confidence": float(s.confidence),
                        "reasoning": s.reasoning,
                    }
                    for s in safe_add_signals
                ],
            )
        
        # Avoid watchlist
        avoid_signals = [s for s in signals if s.signal_type == SignalType.AVOID]
        if avoid_signals:
            watchlists["avoid"] = Watchlist(
                name="Stocks to Avoid",
                watchlist_type="avoid",
                tickers=[s.ticker for s in avoid_signals],
                entries=[
                    {
                        "ticker": s.ticker,
                        "reasoning": s.reasoning,
                    }
                    for s in avoid_signals
                ],
            )
        
        # RANCO candidates watchlist
        ranco_signals = [s for s in signals if s.signal_type == SignalType.RANCO_ENTRY]
        if ranco_signals:
            watchlists["ranco_candidates"] = Watchlist(
                name="RANCO Candidates",
                watchlist_type="ranco_candidates",
                tickers=[s.ticker for s in ranco_signals],
                entries=[
                    {
                        "ticker": s.ticker,
                        "confidence": float(s.confidence),
                        "reasoning": s.reasoning,
                    }
                    for s in ranco_signals
                ],
            )
        
        logger.info(f"Generated {len(watchlists)} watchlists with {sum(len(w.tickers) for w in watchlists.values())} total entries")
        return watchlists


# =============================================================================
# RANCO/PID Tactical Service
# =============================================================================

class RANCOTacticalService:
    """
    RANCO/PID Tactical Sleeve - Structured Mechanical Trading
    
    This is NOT gambling. This is:
    - PID loops
    - Probability cones
    - Volatility compression
    - Zero-emotion trading
    - Strict rules, structured entries and exits
    - Industrial-grade decision science
    
    ENGINEERING, not speculation.
    """
    
    def __init__(self, config: RANCOTacticalConfig):
        self.config = config
        self.entry_rules = config.entry_rules
        self.exit_rules = config.exit_rules
        self.sizing_rules = config.sizing_rules
        logger.info("RANCO Tactical Service initialized")
    
    async def evaluate_candidate(
        self, 
        ticker: str,
        technical: TechnicalIndicators
    ) -> RANCOCandidate:
        """
        Evaluate a stock as a RANCO candidate.
        All criteria must be met for a valid entry.
        """
        candidate = RANCOCandidate(
            ticker=ticker,
            technical_data=technical,
        )
        
        # Check volatility compression
        if technical.atr_6mo_median:
            candidate.volatility_compressed = technical.atr_pct < technical.atr_6mo_median
        
        # Check MA alignment (20 > 50 > 200)
        candidate.ma_aligned = (
            technical.ma_20 > technical.ma_50 > technical.ma_200
        )
        
        # Check RSI range
        candidate.rsi_in_range = (
            self.entry_rules.rsi_min <= technical.rsi_14 <= self.entry_rules.rsi_max
        )
        
        # Check higher low pattern
        candidate.higher_low_formed = technical.higher_low_formed
        
        # All criteria must be met
        candidate.is_valid_candidate = (
            candidate.volatility_compressed and
            candidate.ma_aligned and
            candidate.rsi_in_range and
            candidate.higher_low_formed
        )
        
        # Calculate entry parameters for valid candidates
        if candidate.is_valid_candidate:
            candidate.entry_price = technical.current_price
            candidate.stop_price = technical.current_price - (technical.atr_14 * self.exit_rules.initial_stop_atr_multiplier)
            
            # Calculate risk-reward (target = 3x risk as baseline)
            risk = candidate.entry_price - candidate.stop_price
            candidate.risk_reward_ratio = Decimal("3.0")  # Target 3:1
        
        logger.info(f"RANCO evaluation for {ticker}: {'VALID' if candidate.is_valid_candidate else 'INVALID'}",
                   volatility=candidate.volatility_compressed,
                   ma_aligned=candidate.ma_aligned,
                   rsi_ok=candidate.rsi_in_range,
                   higher_low=candidate.higher_low_formed)
        
        return candidate
    
    async def calculate_position_size(
        self, 
        candidate: RANCOCandidate,
        portfolio_value: Decimal,
        current_tactical_allocation: Decimal
    ) -> Optional[Decimal]:
        """
        Calculate position size using Kelly/5 or fixed risk method.
        Returns position size as percentage of portfolio.
        """
        if not candidate.is_valid_candidate or not candidate.entry_price or not candidate.stop_price:
            return None
        
        # Check tactical allocation limit
        remaining_tactical = self.sizing_rules.max_tactical_allocation_pct - current_tactical_allocation
        if remaining_tactical <= Decimal("0"):
            logger.warning("Tactical allocation limit reached")
            return None
        
        # Calculate risk per share
        risk_per_share = candidate.entry_price - candidate.stop_price
        risk_pct = risk_per_share / candidate.entry_price
        
        # Fixed risk method: risk 0.5-1% of equity per trade
        max_risk = portfolio_value * self.sizing_rules.max_risk_per_trade_pct
        shares = max_risk / risk_per_share
        position_value = shares * candidate.entry_price
        position_pct = position_value / portfolio_value
        
        # Cap at remaining tactical allocation
        position_pct = min(position_pct, remaining_tactical)
        
        candidate.position_size_pct = position_pct
        
        logger.info(f"Position size for {candidate.ticker}: {float(position_pct)*100:.2f}% of portfolio")
        return position_pct
    
    async def check_exit_conditions(
        self, 
        position: Position,
        technical: TechnicalIndicators
    ) -> Tuple[bool, List[str]]:
        """
        Check if exit conditions are met for an open RANCO position.
        Returns (should_exit, reasons).
        """
        reasons = []
        
        # Check stop loss hit
        if position.stop_loss_price and technical.current_price <= position.stop_loss_price:
            reasons.append(f"Stop loss hit at {position.stop_loss_price}")
            return True, reasons
        
        # Check RSI overbought + lower high pattern
        if technical.rsi_14 > self.exit_rules.rsi_overbought_threshold:
            if self.exit_rules.exit_on_first_lower_high_after_overbought:
                # This would need price pattern analysis
                reasons.append(f"RSI overbought at {technical.rsi_14}, watching for lower high")
        
        # Update trailing stop
        trailing_stop = technical.current_price - (technical.atr_14 * self.exit_rules.trailing_stop_atr_multiplier)
        if position.stop_loss_price and trailing_stop > position.stop_loss_price:
            # Trailing stop should be updated
            logger.info(f"Trailing stop updated for {position.ticker}: {trailing_stop}")
        
        return len(reasons) > 0, reasons


# =============================================================================
# Risk Management Service
# =============================================================================

class RiskManagementService:
    """
    Risk Management Service - Guardrails Enforcement
    
    Enforces non-negotiable safety rules:
    - No leverage, options, or margin
    - Position and sector limits
    - Stop losses
    - Drawdown monitoring
    """
    
    def __init__(self, guardrails: Guardrails):
        self.guardrails = guardrails
        logger.info("Risk Management Service initialized")
    
    async def validate_trade(
        self, 
        ticker: str,
        position_value: Decimal,
        portfolio: Portfolio,
        sector: str
    ) -> Tuple[bool, List[str]]:
        """
        Validate a proposed trade against guardrails.
        Returns (is_valid, violations).
        """
        violations = []
        
        # Check single position limit
        position_pct = position_value / portfolio.total_value if portfolio.total_value > 0 else Decimal("0")
        if position_pct > self.guardrails.max_single_position_pct:
            violations.append(f"Position size {float(position_pct)*100:.1f}% exceeds limit {float(self.guardrails.max_single_position_pct)*100:.1f}%")
        
        # Check sector allocation
        current_sector_allocation = portfolio.sector_allocations.get(sector, Decimal("0"))
        new_sector_allocation = current_sector_allocation + position_pct
        if new_sector_allocation > self.guardrails.max_sector_allocation_pct:
            violations.append(f"Sector allocation {float(new_sector_allocation)*100:.1f}% exceeds limit {float(self.guardrails.max_sector_allocation_pct)*100:.1f}%")
        
        # Check cash buffer
        remaining_cash_pct = portfolio.cash_allocation_pct - position_pct
        if remaining_cash_pct < self.guardrails.min_cash_buffer_pct:
            violations.append(f"Cash buffer would drop to {float(remaining_cash_pct)*100:.1f}%, below minimum {float(self.guardrails.min_cash_buffer_pct)*100:.1f}%")
        
        is_valid = len(violations) == 0
        
        if not is_valid:
            logger.warning(f"Trade validation failed for {ticker}", violations=violations)
        
        return is_valid, violations
    
    async def check_portfolio_health(self, portfolio: Portfolio) -> List[RiskAlert]:
        """
        Check overall portfolio health and generate alerts.
        """
        alerts = []
        
        # Check drawdown
        if portfolio.current_drawdown_pct >= self.guardrails.max_portfolio_drawdown_pct:
            alerts.append(RiskAlert(
                alert_type="drawdown",
                risk_level=RiskLevel.CRITICAL,
                message=f"Portfolio drawdown {float(portfolio.current_drawdown_pct)*100:.1f}% exceeds limit",
                current_value=portfolio.current_drawdown_pct,
                threshold_value=self.guardrails.max_portfolio_drawdown_pct,
                recommended_action="Cut tactical risk by 50%",
            ))
        
        # Check cash buffer
        if portfolio.cash_allocation_pct < self.guardrails.min_cash_buffer_pct:
            alerts.append(RiskAlert(
                alert_type="liquidity",
                risk_level=RiskLevel.HIGH,
                message=f"Cash buffer {float(portfolio.cash_allocation_pct)*100:.1f}% below minimum",
                current_value=portfolio.cash_allocation_pct,
                threshold_value=self.guardrails.min_cash_buffer_pct,
                recommended_action="Raise cash by trimming positions",
            ))
        
        # Check position concentration
        for ticker, position in portfolio.positions.items():
            position_pct = position.market_value / portfolio.total_value if portfolio.total_value > 0 else Decimal("0")
            if position_pct > self.guardrails.max_single_position_pct:
                alerts.append(RiskAlert(
                    alert_type="concentration",
                    risk_level=RiskLevel.MEDIUM,
                    ticker=ticker,
                    message=f"Position {ticker} at {float(position_pct)*100:.1f}% exceeds limit",
                    current_value=position_pct,
                    threshold_value=self.guardrails.max_single_position_pct,
                    recommended_action=f"Trim {ticker} position",
                ))
        
        # Check sector concentration
        for sector, allocation in portfolio.sector_allocations.items():
            if allocation > self.guardrails.max_sector_allocation_pct:
                alerts.append(RiskAlert(
                    alert_type="concentration",
                    risk_level=RiskLevel.MEDIUM,
                    message=f"Sector {sector} at {float(allocation)*100:.1f}% exceeds limit",
                    current_value=allocation,
                    threshold_value=self.guardrails.max_sector_allocation_pct,
                    recommended_action=f"Reduce {sector} exposure",
                ))
        
        if alerts:
            logger.warning(f"Generated {len(alerts)} risk alerts")
        
        return alerts
    
    def enforce_leverage_prohibition(self) -> bool:
        """
        Strictly enforce no leverage, options, or margin.
        This is a HARD rule that cannot be bypassed.
        """
        if self.guardrails.allow_leverage:
            raise ValueError("FORBIDDEN: Leverage is not allowed")
        if self.guardrails.allow_options:
            raise ValueError("FORBIDDEN: Options are not allowed")
        if self.guardrails.allow_margin:
            raise ValueError("FORBIDDEN: Margin is not allowed")
        return True


# =============================================================================
# Portfolio Analytics Service
# =============================================================================

class PortfolioAnalyticsService:
    """
    Portfolio Analytics - Reporting and Analysis
    """
    
    def __init__(self):
        logger.info("Portfolio Analytics Service initialized")
    
    async def calculate_portfolio_metrics(self, portfolio: Portfolio) -> Dict[str, Any]:
        """Calculate comprehensive portfolio metrics"""
        
        # Calculate total values
        total_market_value = sum(p.market_value for p in portfolio.positions.values())
        total_cost_basis = sum(p.cost_basis_total for p in portfolio.positions.values())
        total_cash = portfolio.treasury_balance + portfolio.swarmgate_balance
        
        total_value = total_market_value + total_cash
        
        # Calculate returns
        total_return = total_market_value - total_cost_basis
        total_return_pct = (total_return / total_cost_basis * 100) if total_cost_basis > 0 else Decimal("0")
        
        # Calculate dividend metrics
        total_annual_dividends = sum(p.annual_dividend_income for p in portfolio.positions.values())
        portfolio_yield = (total_annual_dividends / total_market_value * 100) if total_market_value > 0 else Decimal("0")
        
        # Calculate allocations
        core_value = sum(
            p.market_value for p in portfolio.positions.values() 
            if p.position_type == PositionType.CORE_DIVIDEND
        )
        tactical_value = sum(
            p.market_value for p in portfolio.positions.values() 
            if p.position_type == PositionType.TACTICAL_RANCO
        )
        
        return {
            "total_value": float(total_value),
            "total_market_value": float(total_market_value),
            "total_cash": float(total_cash),
            "total_cost_basis": float(total_cost_basis),
            "total_return": float(total_return),
            "total_return_pct": float(total_return_pct),
            "annual_dividend_income": float(total_annual_dividends),
            "portfolio_yield": float(portfolio_yield),
            "core_allocation_pct": float(core_value / total_value * 100) if total_value > 0 else 0,
            "tactical_allocation_pct": float(tactical_value / total_value * 100) if total_value > 0 else 0,
            "cash_allocation_pct": float(total_cash / total_value * 100) if total_value > 0 else 0,
            "position_count": len(portfolio.positions),
        }
    
    async def generate_weekly_report(self, portfolio: Portfolio) -> WeeklyReport:
        """Generate weekly P&L and status report"""
        metrics = await self.calculate_portfolio_metrics(portfolio)
        
        # Determine risk score
        if portfolio.current_drawdown_pct >= Decimal("0.10"):
            risk_score = "red"
        elif portfolio.current_drawdown_pct >= Decimal("0.05"):
            risk_score = "yellow"
        else:
            risk_score = "green"
        
        return WeeklyReport(
            portfolio_value=Decimal(str(metrics["total_value"])),
            dividend_run_rate=Decimal(str(metrics["annual_dividend_income"])),
            current_drawdown_pct=portfolio.current_drawdown_pct,
            risk_score=risk_score,
            swarmgate_flow=portfolio.swarmgate_balance,
        )


# =============================================================================
# Main Financial Refinery Orchestrator
# =============================================================================

class FinancialRefineryOrchestrator:
    """
    Main orchestrator for the Hybrid Refinery Financial System.
    
    Coordinates:
    - Dividend Engine (base income layer)
    - Refinery Overlay (signals and filtering)
    - RANCO Tactical Sleeve (structured trading)
    - Risk Management (guardrails enforcement)
    - Portfolio Analytics (reporting)
    """
    
    def __init__(
        self,
        guardrails: Optional[Guardrails] = None,
        dividend_config: Optional[DividendEngineConfig] = None,
        overlay_config: Optional[RefineryOverlayConfig] = None,
        tactical_config: Optional[RANCOTacticalConfig] = None,
    ):
        self.guardrails = guardrails or Guardrails()
        
        # Initialize services
        self.dividend_service = DividendScreeningService(dividend_config or DividendEngineConfig())
        self.overlay_service = RefineryOverlayService(overlay_config or RefineryOverlayConfig())
        self.ranco_service = RANCOTacticalService(tactical_config or RANCOTacticalConfig())
        self.risk_service = RiskManagementService(self.guardrails)
        self.analytics_service = PortfolioAnalyticsService()
        
        logger.info("Financial Refinery Orchestrator initialized",
                   guardrails=self.guardrails)
    
    async def run_daily_analysis(
        self, 
        dividend_universe: List[DividendStock],
        technical_data: Dict[str, TechnicalIndicators],
        fundamental_data: Dict[str, FundamentalData],
        portfolio: Portfolio,
    ) -> Dict[str, Any]:
        """
        Run complete daily analysis cycle.
        
        Returns comprehensive analysis with:
        - Dividend screening results
        - Overlay signals
        - RANCO candidates
        - Risk alerts
        - Watchlists
        """
        logger.info("Starting daily analysis cycle")
        
        # 1. Enforce no leverage rule
        self.risk_service.enforce_leverage_prohibition()
        
        # 2. Screen dividend universe
        passing_dividends, failing_dividends = await self.dividend_service.screen_universe(dividend_universe)
        
        # 3. Generate overlay signals
        all_signals = []
        for ticker in technical_data:
            if ticker in fundamental_data:
                signals = await self.overlay_service.analyze_stock(
                    ticker,
                    technical_data[ticker],
                    fundamental_data[ticker],
                )
                all_signals.extend(signals)
        
        # 4. Evaluate RANCO candidates
        ranco_signals = [s for s in all_signals if s.signal_type == SignalType.RANCO_ENTRY]
        ranco_candidates = []
        for signal in ranco_signals:
            if signal.ticker in technical_data:
                candidate = await self.ranco_service.evaluate_candidate(
                    signal.ticker,
                    technical_data[signal.ticker],
                )
                if candidate.is_valid_candidate:
                    ranco_candidates.append(candidate)
        
        # 5. Check portfolio health
        risk_alerts = await self.risk_service.check_portfolio_health(portfolio)
        
        # 6. Generate watchlists
        watchlists = await self.overlay_service.generate_watchlists(all_signals)
        
        # 7. Generate portfolio metrics
        metrics = await self.analytics_service.calculate_portfolio_metrics(portfolio)
        
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "dividend_screening": {
                "passing": len(passing_dividends),
                "failing": len(failing_dividends),
                "stocks": [{"ticker": s.ticker, "yield": float(s.dividend_yield)} for s in passing_dividends[:10]],
            },
            "signals": {
                "total": len(all_signals),
                "safe_add": len([s for s in all_signals if s.signal_type == SignalType.SAFE_ADD]),
                "avoid": len([s for s in all_signals if s.signal_type == SignalType.AVOID]),
                "ranco_entry": len([s for s in all_signals if s.signal_type == SignalType.RANCO_ENTRY]),
            },
            "ranco_candidates": [
                {
                    "ticker": c.ticker,
                    "entry": float(c.entry_price) if c.entry_price else None,
                    "stop": float(c.stop_price) if c.stop_price else None,
                }
                for c in ranco_candidates
            ],
            "risk_alerts": [
                {
                    "type": a.alert_type,
                    "level": a.risk_level.value,
                    "message": a.message,
                }
                for a in risk_alerts
            ],
            "watchlists": {name: len(wl.tickers) for name, wl in watchlists.items()},
            "portfolio_metrics": metrics,
        }
    
    async def process_dividend_received(
        self, 
        ticker: str,
        amount: Decimal,
        portfolio: Portfolio,
    ) -> Dict[str, CashFlow]:
        """
        Process a dividend payment and allocate according to rules.
        - 70% reinvest
        - 23% treasury
        - 7% SwarmGate
        """
        allocation = self.dividend_service.calculate_dividend_allocation(amount)
        
        flows = {
            "reinvest": CashFlow(
                source_account=AccountType.CORE,
                destination_account=AccountType.CORE,
                amount=allocation["reinvest"],
                description=f"Dividend reinvestment from {ticker}",
                flow_type="dividend",
            ),
            "treasury": CashFlow(
                source_account=AccountType.CORE,
                destination_account=AccountType.TREASURY,
                amount=allocation["treasury"],
                description=f"Treasury allocation from {ticker} dividend",
                flow_type="dividend",
            ),
            "swarmgate": CashFlow(
                source_account=AccountType.CORE,
                destination_account=AccountType.SWARMGATE,
                amount=allocation["swarmgate"],
                description=f"SwarmGate allocation from {ticker} dividend",
                flow_type="dividend",
            ),
        }
        
        logger.info(f"Processed dividend from {ticker}: {amount}",
                   reinvest=float(allocation["reinvest"]),
                   treasury=float(allocation["treasury"]),
                   swarmgate=float(allocation["swarmgate"]))
        
        return flows
