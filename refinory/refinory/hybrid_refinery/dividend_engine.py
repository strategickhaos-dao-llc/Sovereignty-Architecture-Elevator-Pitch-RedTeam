"""
Dividend Engine - Core Stable Yield Reactor
============================================

The Dividend Engine is the foundation of the Hybrid Refinery system.
It provides a slow, compounding, cannot-die machine for wealth building.

Screening Logic:
    1. Dividend Achievers + Aristocrats + Quality REITs & regulated utilities
    2. Hard filters applied (payout ratio, CAGR, coverage, debt ratios)

Portfolio Construction:
    - 20-25 stocks
    - Equal weight or volatility weight
    - 5% max position weight
"""

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import List, Dict, Any, Optional
from enum import Enum
import structlog

from .config import HybridRefineryConfig, ScreeningFilters

logger = structlog.get_logger()


class StockCategory(Enum):
    """Stock categorization"""
    DIVIDEND_ACHIEVER = "dividend_achiever"
    DIVIDEND_ARISTOCRAT = "dividend_aristocrat"
    DIVIDEND_KING = "dividend_king"
    QUALITY_REIT = "quality_reit"
    REGULATED_UTILITY = "regulated_utility"
    STANDARD = "standard"


class ScreeningStatus(Enum):
    """Status of screening result"""
    PASSED = "passed"
    FAILED = "failed"
    PENDING = "pending"
    EXCLUDED = "excluded"  # e.g., earnings window


@dataclass
class DividendMetrics:
    """Dividend-related metrics for a stock"""
    current_yield: float
    payout_ratio: float
    dividend_cagr_5yr: float
    consecutive_years_increased: int
    ex_dividend_date: Optional[date] = None
    next_earnings_date: Optional[date] = None
    ffo_payout_ratio: Optional[float] = None  # For REITs


@dataclass
class FinancialMetrics:
    """Financial health metrics"""
    interest_coverage: float
    net_debt_ebitda: float
    roic: float
    wacc: float
    average_daily_volume: float
    market_cap: float
    
    @property
    def roic_wacc_spread(self) -> float:
        """Calculate economic profit indicator"""
        return self.roic - self.wacc


@dataclass
class DividendStock:
    """Complete dividend stock data structure"""
    symbol: str
    name: str
    sector: str
    industry: str
    category: StockCategory
    
    # Metrics
    dividend_metrics: DividendMetrics
    financial_metrics: FinancialMetrics
    
    # Current price data
    current_price: float
    ma_20: float
    ma_50: float
    ma_200: float
    
    # Screening status
    screening_status: ScreeningStatus = ScreeningStatus.PENDING
    screening_failures: List[str] = field(default_factory=list)
    
    # Timestamps
    last_updated: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        if self.screening_failures is None:
            self.screening_failures = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "symbol": self.symbol,
            "name": self.name,
            "sector": self.sector,
            "industry": self.industry,
            "category": self.category.value,
            "dividend_metrics": {
                "current_yield": self.dividend_metrics.current_yield,
                "payout_ratio": self.dividend_metrics.payout_ratio,
                "dividend_cagr_5yr": self.dividend_metrics.dividend_cagr_5yr,
                "consecutive_years_increased": self.dividend_metrics.consecutive_years_increased,
                "ex_dividend_date": str(self.dividend_metrics.ex_dividend_date) if self.dividend_metrics.ex_dividend_date else None,
                "next_earnings_date": str(self.dividend_metrics.next_earnings_date) if self.dividend_metrics.next_earnings_date else None,
                "ffo_payout_ratio": self.dividend_metrics.ffo_payout_ratio,
            },
            "financial_metrics": {
                "interest_coverage": self.financial_metrics.interest_coverage,
                "net_debt_ebitda": self.financial_metrics.net_debt_ebitda,
                "roic": self.financial_metrics.roic,
                "wacc": self.financial_metrics.wacc,
                "roic_wacc_spread": self.financial_metrics.roic_wacc_spread,
                "average_daily_volume": self.financial_metrics.average_daily_volume,
                "market_cap": self.financial_metrics.market_cap,
            },
            "current_price": self.current_price,
            "ma_20": self.ma_20,
            "ma_50": self.ma_50,
            "ma_200": self.ma_200,
            "screening_status": self.screening_status.value,
            "screening_failures": self.screening_failures,
            "last_updated": self.last_updated.isoformat(),
        }


@dataclass
class ScreeningResult:
    """Result of the screening process"""
    stock: DividendStock
    passed: bool
    filters_checked: Dict[str, bool]
    notes: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "symbol": self.stock.symbol,
            "name": self.stock.name,
            "passed": self.passed,
            "filters_checked": self.filters_checked,
            "notes": self.notes,
            "category": self.stock.category.value,
            "yield": self.stock.dividend_metrics.current_yield,
        }


class DividendEngine:
    """
    Dividend Engine - Core component for stable yield generation
    
    Purpose: slow, compounding, cannot-die machine
    Flow: Screen → Construct → Reinvest → Buffer → SwarmGate
    """
    
    def __init__(self, config: HybridRefineryConfig):
        self.config = config
        self.filters = config.screening
        self.core_positions: List[DividendStock] = []
        self.screening_results: List[ScreeningResult] = []
        
        logger.info("Dividend Engine initialized", 
                   max_positions=config.guardrails.max_positions,
                   max_weight=config.guardrails.max_position_weight)
    
    def screen_stock(self, stock: DividendStock) -> ScreeningResult:
        """
        Apply hard filters to a dividend stock
        
        Filters:
            - Payout Ratio < 70% (REIT FFO < 80%)
            - 5-yr Dividend CAGR > 3%
            - Interest Coverage > 4×
            - Net Debt/EBITDA < 3× (REITs < 6×)
            - ROIC − WACC > 2%
            - ADV > $1M
            - No earnings window (±5 days)
        """
        filters_checked = {}
        notes = []
        passed = True
        
        is_reit = stock.category == StockCategory.QUALITY_REIT
        
        # 1. Payout ratio check
        if is_reit:
            ffo_payout = stock.dividend_metrics.ffo_payout_ratio or stock.dividend_metrics.payout_ratio
            filter_passed = ffo_payout < self.filters.max_reit_ffo_payout
            filters_checked["ffo_payout_ratio"] = filter_passed
            if not filter_passed:
                notes.append(f"FFO payout {ffo_payout:.1%} exceeds {self.filters.max_reit_ffo_payout:.0%}")
                passed = False
        else:
            filter_passed = stock.dividend_metrics.payout_ratio < self.filters.max_payout_ratio
            filters_checked["payout_ratio"] = filter_passed
            if not filter_passed:
                notes.append(f"Payout ratio {stock.dividend_metrics.payout_ratio:.1%} exceeds {self.filters.max_payout_ratio:.0%}")
                passed = False
        
        # 2. Dividend CAGR check
        filter_passed = stock.dividend_metrics.dividend_cagr_5yr > self.filters.min_dividend_cagr_5yr
        filters_checked["dividend_cagr_5yr"] = filter_passed
        if not filter_passed:
            notes.append(f"Dividend CAGR {stock.dividend_metrics.dividend_cagr_5yr:.1%} below {self.filters.min_dividend_cagr_5yr:.0%}")
            passed = False
        
        # 3. Interest coverage check
        filter_passed = stock.financial_metrics.interest_coverage > self.filters.min_interest_coverage
        filters_checked["interest_coverage"] = filter_passed
        if not filter_passed:
            notes.append(f"Interest coverage {stock.financial_metrics.interest_coverage:.1f}x below {self.filters.min_interest_coverage:.0f}x")
            passed = False
        
        # 4. Net Debt/EBITDA check
        max_debt_ratio = self.filters.max_reit_net_debt_ebitda if is_reit else self.filters.max_net_debt_ebitda
        filter_passed = stock.financial_metrics.net_debt_ebitda < max_debt_ratio
        filters_checked["net_debt_ebitda"] = filter_passed
        if not filter_passed:
            notes.append(f"Net Debt/EBITDA {stock.financial_metrics.net_debt_ebitda:.1f}x exceeds {max_debt_ratio:.0f}x")
            passed = False
        
        # 5. Economic profit (ROIC - WACC spread)
        roic_wacc_spread = stock.financial_metrics.roic_wacc_spread
        filter_passed = roic_wacc_spread > self.filters.min_roic_wacc_spread
        filters_checked["roic_wacc_spread"] = filter_passed
        if not filter_passed:
            notes.append(f"ROIC-WACC spread {roic_wacc_spread:.1%} below {self.filters.min_roic_wacc_spread:.0%}")
            passed = False
        
        # 6. Liquidity check (ADV)
        adv_million = stock.financial_metrics.average_daily_volume / 1_000_000
        filter_passed = adv_million >= self.filters.min_adv_million
        filters_checked["average_daily_volume"] = filter_passed
        if not filter_passed:
            notes.append(f"ADV ${adv_million:.1f}M below ${self.filters.min_adv_million:.0f}M minimum")
            passed = False
        
        # 7. Earnings window exclusion
        if stock.dividend_metrics.next_earnings_date:
            days_to_earnings = (stock.dividend_metrics.next_earnings_date - date.today()).days
            filter_passed = abs(days_to_earnings) > self.filters.earnings_exclusion_days
            filters_checked["earnings_window"] = filter_passed
            if not filter_passed:
                notes.append(f"Within {self.filters.earnings_exclusion_days}-day earnings window")
                passed = False
        else:
            filters_checked["earnings_window"] = True  # No earnings date = pass
        
        # Update stock screening status
        stock.screening_status = ScreeningStatus.PASSED if passed else ScreeningStatus.FAILED
        stock.screening_failures = [n for n in notes if not n.startswith("OK")]
        
        result = ScreeningResult(
            stock=stock,
            passed=passed,
            filters_checked=filters_checked,
            notes=notes
        )
        
        logger.info("Stock screened", 
                   symbol=stock.symbol, 
                   passed=passed,
                   failures=len(stock.screening_failures))
        
        return result
    
    def screen_universe(self, stocks: List[DividendStock]) -> Dict[str, List[ScreeningResult]]:
        """
        Screen a universe of stocks and categorize results
        
        Returns:
            dividends_core: Passed all filters
            safe_add: Safe to add to core
            avoid: Failed critical filters
            ranco_candidates: Suitable for tactical overlay
        """
        results = {
            "dividends_core": [],
            "safe_add": [],
            "avoid": [],
            "ranco_candidates": [],
        }
        
        for stock in stocks:
            result = self.screen_stock(stock)
            self.screening_results.append(result)
            
            if result.passed:
                results["dividends_core"].append(result)
                
                # Check if also suitable for tactical trading
                if self._is_ranco_candidate(stock):
                    results["ranco_candidates"].append(result)
            else:
                # Categorize failures
                critical_failures = ["payout_ratio", "ffo_payout_ratio", "net_debt_ebitda"]
                has_critical_failure = any(
                    not result.filters_checked.get(f, True) 
                    for f in critical_failures
                )
                
                if has_critical_failure:
                    results["avoid"].append(result)
                else:
                    # Minor failures - might be safe to add later
                    results["safe_add"].append(result)
        
        logger.info("Universe screening complete",
                   core=len(results["dividends_core"]),
                   safe_add=len(results["safe_add"]),
                   avoid=len(results["avoid"]),
                   ranco=len(results["ranco_candidates"]))
        
        return results
    
    def _is_ranco_candidate(self, stock: DividendStock) -> bool:
        """
        Check if stock is suitable for RANCO/PID tactical trading
        
        Criteria:
            - Uptrend (20 > 50 > 200)
            - Good liquidity
            - Not near earnings
        """
        # Check trend
        has_uptrend = (
            stock.ma_20 > stock.ma_50 > stock.ma_200
        )
        
        # Check liquidity
        good_liquidity = (
            stock.financial_metrics.average_daily_volume >= self.filters.min_adv_million * 1_000_000
        )
        
        # Check earnings window
        not_near_earnings = True
        if stock.dividend_metrics.next_earnings_date:
            days_to_earnings = abs((stock.dividend_metrics.next_earnings_date - date.today()).days)
            not_near_earnings = days_to_earnings > self.filters.earnings_exclusion_days
        
        return has_uptrend and good_liquidity and not_near_earnings
    
    def construct_portfolio(
        self, 
        screened_stocks: List[ScreeningResult],
        weighting: str = "equal"
    ) -> List[Dict[str, Any]]:
        """
        Construct core dividend portfolio
        
        Args:
            screened_stocks: Stocks that passed screening
            weighting: "equal" or "volatility" weighted
            
        Returns:
            List of position allocations
        """
        if not screened_stocks:
            logger.warning("No stocks passed screening for portfolio construction")
            return []
        
        # Limit to max positions
        max_positions = self.config.guardrails.max_positions
        selected = screened_stocks[:max_positions]
        
        positions = []
        total_capital = self.config.total_capital
        max_weight = self.config.guardrails.max_position_weight
        
        if weighting == "equal":
            # Equal weight, capped at max_weight
            base_weight = 1.0 / len(selected)
            weight = min(base_weight, max_weight)
            
            for result in selected:
                stock = result.stock
                allocation = total_capital * weight
                shares = int(allocation / stock.current_price)
                
                positions.append({
                    "symbol": stock.symbol,
                    "name": stock.name,
                    "sector": stock.sector,
                    "weight": weight,
                    "allocation": allocation,
                    "shares": shares,
                    "price": stock.current_price,
                    "yield": stock.dividend_metrics.current_yield,
                    "category": stock.category.value,
                })
        
        elif weighting == "volatility":
            # Inverse volatility weighting
            #
            # Implementation Note: This is a placeholder that falls back to equal weight.
            # 
            # To implement proper inverse volatility weighting:
            # 1. Requires ATR (Average True Range) data for each stock
            # 2. Calculate inverse ATR weight: weight_i = (1/ATR_i) / sum(1/ATR_j)
            # 3. This gives higher allocation to lower-volatility stocks
            # 4. Cap individual weights at max_position_weight
            #
            # Required data structure extension:
            #   - Add 'atr_14' field to DividendStock.financial_metrics
            #   - Or pass technical_data dict with ATR values
            #
            # Example implementation:
            #   total_inv_atr = sum(1/stock.atr for stock in selected if stock.atr > 0)
            #   for stock in selected:
            #       weight = (1/stock.atr) / total_inv_atr
            #       weight = min(weight, max_weight)  # Cap at guardrail
            #
            # For now, use equal weight as fallback until ATR data is available
            logger.warning("Volatility weighting requested but not fully implemented - using equal weight")
            return self.construct_portfolio(screened_stocks, weighting="equal")
        
        logger.info("Portfolio constructed",
                   positions=len(positions),
                   weighting=weighting,
                   total_allocation=sum(p["allocation"] for p in positions))
        
        return positions
    
    def calculate_dividend_income(self, positions: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Calculate expected dividend income from portfolio
        
        Returns:
            Annual, quarterly, and monthly expected income
        """
        annual_income = sum(
            p["allocation"] * p["yield"]
            for p in positions
        )
        
        return {
            "annual": annual_income,
            "quarterly": annual_income / 4,
            "monthly": annual_income / 12,
            "yield_on_cost": annual_income / self.config.total_capital if self.config.total_capital > 0 else 0,
        }
    
    def calculate_flow_routing(self, dividend_income: float) -> Dict[str, float]:
        """
        Calculate flow routing for dividend income
        
        Flow routing:
            70% → Auto reinvest to compounding core
            23% → Treasury buffer for dislocations
            7%  → SwarmGate (autonomous AI flow router)
        """
        return {
            "core_reinvest": dividend_income * self.config.guardrails.core_reinvest_pct,
            "treasury_buffer": dividend_income * self.config.guardrails.treasury_buffer_pct,
            "swarmgate": dividend_income * self.config.guardrails.swarmgate_pct,
            "routing_percentages": {
                "core_reinvest": f"{self.config.guardrails.core_reinvest_pct:.0%}",
                "treasury_buffer": f"{self.config.guardrails.treasury_buffer_pct:.0%}",
                "swarmgate": f"{self.config.guardrails.swarmgate_pct:.0%}",
            }
        }
    
    def get_sector_breakdown(self, positions: List[Dict[str, Any]]) -> Dict[str, float]:
        """Get sector allocation breakdown"""
        sector_weights = {}
        for position in positions:
            sector = position["sector"]
            sector_weights[sector] = sector_weights.get(sector, 0) + position["weight"]
        return sector_weights
    
    def check_guardrails(self, positions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Check if portfolio adheres to guardrails
        
        Returns:
            Guardrails status and any violations
        """
        violations = []
        
        # Check position count
        if len(positions) < self.config.guardrails.min_positions:
            violations.append(f"Below minimum positions ({len(positions)} < {self.config.guardrails.min_positions})")
        if len(positions) > self.config.guardrails.max_positions:
            violations.append(f"Above maximum positions ({len(positions)} > {self.config.guardrails.max_positions})")
        
        # Check position weights
        for position in positions:
            if position["weight"] > self.config.guardrails.max_position_weight:
                violations.append(f"{position['symbol']} weight {position['weight']:.1%} exceeds max {self.config.guardrails.max_position_weight:.0%}")
        
        # Check sector weights
        sector_weights = self.get_sector_breakdown(positions)
        for sector, weight in sector_weights.items():
            if weight > self.config.guardrails.max_sector_weight:
                violations.append(f"Sector {sector} weight {weight:.1%} exceeds max {self.config.guardrails.max_sector_weight:.0%}")
        
        return {
            "passed": len(violations) == 0,
            "violations": violations,
            "positions_count": len(positions),
            "sector_weights": sector_weights,
        }
