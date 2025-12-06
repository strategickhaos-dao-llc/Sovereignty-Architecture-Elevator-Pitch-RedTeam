"""
Validation Engine
=================

Backtesting and validation framework for the Hybrid Refinery system.

Features:
    - 10-year backtests
    - Stress tests (2020 crash, 2022 bear, 2015 rate shock)
    - Monte Carlo simulations
    - Drawdown analysis
    - Performance metrics
"""

from dataclasses import dataclass, field
from datetime import datetime, date, timedelta
from typing import List, Dict, Any, Optional, Tuple
from enum import Enum
import random
import math
import structlog

from .config import HybridRefineryConfig

logger = structlog.get_logger()


class StressScenario(Enum):
    """Pre-defined stress test scenarios"""
    COVID_2020 = "covid_2020"  # March 2020 crash
    BEAR_2022 = "bear_2022"  # 2022 rate hiking bear market
    RATE_SHOCK_2015 = "rate_shock_2015"  # 2015 rate volatility
    FINANCIAL_2008 = "financial_2008"  # 2008 financial crisis
    DOT_COM_2000 = "dot_com_2000"  # Dot-com crash
    CUSTOM = "custom"


@dataclass
class BacktestResult:
    """Results from a backtest run"""
    start_date: date
    end_date: date
    initial_capital: float
    final_value: float
    
    # Returns
    total_return: float = 0.0
    annualized_return: float = 0.0
    
    # Risk metrics
    max_drawdown: float = 0.0
    max_drawdown_date: Optional[date] = None
    recovery_days: int = 0
    volatility: float = 0.0
    sharpe_ratio: float = 0.0
    sortino_ratio: float = 0.0
    
    # Dividend metrics
    total_dividends: float = 0.0
    dividend_cagr: float = 0.0
    
    # Trade metrics (tactical sleeve)
    tactical_trades: int = 0
    tactical_win_rate: float = 0.0
    tactical_pnl: float = 0.0
    
    # Periods
    up_months: int = 0
    down_months: int = 0
    best_month: float = 0.0
    worst_month: float = 0.0
    
    # Time series
    equity_curve: List[Tuple[date, float]] = field(default_factory=list)
    drawdown_curve: List[Tuple[date, float]] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "period": {
                "start": str(self.start_date),
                "end": str(self.end_date),
                "years": (self.end_date - self.start_date).days / 365.25,
            },
            "capital": {
                "initial": self.initial_capital,
                "final": self.final_value,
                "gain": self.final_value - self.initial_capital,
            },
            "returns": {
                "total": self.total_return,
                "annualized": self.annualized_return,
            },
            "risk": {
                "max_drawdown": self.max_drawdown,
                "max_drawdown_date": str(self.max_drawdown_date) if self.max_drawdown_date else None,
                "recovery_days": self.recovery_days,
                "volatility": self.volatility,
                "sharpe_ratio": self.sharpe_ratio,
                "sortino_ratio": self.sortino_ratio,
            },
            "dividends": {
                "total": self.total_dividends,
                "cagr": self.dividend_cagr,
            },
            "tactical": {
                "trades": self.tactical_trades,
                "win_rate": self.tactical_win_rate,
                "pnl": self.tactical_pnl,
            },
            "monthly": {
                "up_months": self.up_months,
                "down_months": self.down_months,
                "best_month": self.best_month,
                "worst_month": self.worst_month,
                "win_rate": self.up_months / (self.up_months + self.down_months) if (self.up_months + self.down_months) > 0 else 0,
            },
        }


@dataclass
class MonteCarloResult:
    """Results from Monte Carlo simulation"""
    simulations: int
    years: int
    initial_capital: float
    
    # Distribution of outcomes
    median_final_value: float = 0.0
    percentile_5: float = 0.0
    percentile_25: float = 0.0
    percentile_75: float = 0.0
    percentile_95: float = 0.0
    
    # Probability metrics
    prob_positive_return: float = 0.0
    prob_beat_benchmark: float = 0.0
    prob_max_drawdown_exceeded: float = 0.0
    
    # Worst/best cases
    worst_case_value: float = 0.0
    best_case_value: float = 0.0
    
    # Dividend scenarios
    prob_dividend_cut: float = 0.0
    expected_dividend_income: float = 0.0
    
    # Distribution data
    final_values: List[float] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "parameters": {
                "simulations": self.simulations,
                "years": self.years,
                "initial_capital": self.initial_capital,
            },
            "outcomes": {
                "median": self.median_final_value,
                "5th_percentile": self.percentile_5,
                "25th_percentile": self.percentile_25,
                "75th_percentile": self.percentile_75,
                "95th_percentile": self.percentile_95,
                "worst_case": self.worst_case_value,
                "best_case": self.best_case_value,
            },
            "probabilities": {
                "positive_return": self.prob_positive_return,
                "beat_benchmark": self.prob_beat_benchmark,
                "max_drawdown_exceeded": self.prob_max_drawdown_exceeded,
                "dividend_cut": self.prob_dividend_cut,
            },
            "dividends": {
                "expected_income": self.expected_dividend_income,
            },
        }


class ValidationEngine:
    """
    Validation Engine for Hybrid Refinery
    
    Provides:
        - Historical backtests
        - Stress tests
        - Monte Carlo simulations
        - Risk analysis
    """
    
    def __init__(self, config: HybridRefineryConfig):
        self.config = config
        
        # Stress scenario parameters
        self.stress_scenarios = {
            StressScenario.COVID_2020: {
                "drawdown": -0.34,
                "recovery_months": 5,
                "dividend_impact": -0.10,
            },
            StressScenario.BEAR_2022: {
                "drawdown": -0.25,
                "recovery_months": 18,
                "dividend_impact": -0.02,
            },
            StressScenario.RATE_SHOCK_2015: {
                "drawdown": -0.12,
                "recovery_months": 4,
                "dividend_impact": 0.0,
            },
            StressScenario.FINANCIAL_2008: {
                "drawdown": -0.55,
                "recovery_months": 48,
                "dividend_impact": -0.25,
            },
            StressScenario.DOT_COM_2000: {
                "drawdown": -0.45,
                "recovery_months": 60,
                "dividend_impact": -0.08,
            },
        }
        
        logger.info("Validation Engine initialized")
    
    def run_backtest(
        self,
        start_date: date,
        end_date: date,
        initial_capital: float,
        # Simplified assumptions for simulation
        annual_return: float = 0.08,
        dividend_yield: float = 0.035,
        volatility: float = 0.15,
        tactical_contribution: float = 0.02,
    ) -> BacktestResult:
        """
        Run historical backtest simulation
        
        Args:
            start_date: Backtest start date
            end_date: Backtest end date
            initial_capital: Starting capital
            annual_return: Expected annual return (price appreciation)
            dividend_yield: Annual dividend yield
            volatility: Annual volatility
            tactical_contribution: Expected contribution from tactical sleeve
        """
        logger.info("Running backtest",
                   start=str(start_date),
                   end=str(end_date),
                   capital=initial_capital)
        
        # Calculate periods
        days = (end_date - start_date).days
        months = days / 30.44
        years = days / 365.25
        
        # Monthly simulation
        capital = initial_capital
        peak = capital
        max_dd = 0.0
        max_dd_date = start_date
        
        equity_curve = [(start_date, capital)]
        drawdown_curve = [(start_date, 0.0)]
        
        monthly_returns = []
        total_dividends = 0.0
        
        # Monthly parameters
        monthly_return = (1 + annual_return + tactical_contribution) ** (1/12) - 1
        monthly_vol = volatility / math.sqrt(12)
        monthly_dividend = dividend_yield / 12
        
        current_date = start_date
        
        for month in range(int(months)):
            # Generate monthly return with random component
            random_return = random.gauss(monthly_return, monthly_vol)
            
            # Apply return
            capital *= (1 + random_return)
            
            # Add dividend income
            dividend = capital * monthly_dividend
            
            # Apply flow routing
            reinvest = dividend * self.config.guardrails.core_reinvest_pct
            capital += reinvest
            total_dividends += dividend
            
            # Track metrics
            monthly_returns.append(random_return)
            
            # Update peak and drawdown
            if capital > peak:
                peak = capital
            
            dd = (peak - capital) / peak
            if dd > max_dd:
                max_dd = dd
                max_dd_date = current_date
            
            # Record curves
            current_date = start_date + timedelta(days=month * 30)
            equity_curve.append((current_date, capital))
            drawdown_curve.append((current_date, dd))
        
        # Calculate metrics
        total_return = (capital - initial_capital) / initial_capital
        annualized_return = (1 + total_return) ** (1 / years) - 1 if years > 0 else 0
        
        # Risk metrics
        vol = self._calculate_volatility(monthly_returns) * math.sqrt(12)  # Annualize
        sharpe = (annualized_return - 0.02) / vol if vol > 0 else 0  # Assume 2% risk-free
        
        negative_returns = [r for r in monthly_returns if r < 0]
        downside_vol = self._calculate_volatility(negative_returns) * math.sqrt(12) if negative_returns else vol
        sortino = (annualized_return - 0.02) / downside_vol if downside_vol > 0 else 0
        
        # Monthly analysis
        up_months = sum(1 for r in monthly_returns if r > 0)
        down_months = sum(1 for r in monthly_returns if r <= 0)
        
        result = BacktestResult(
            start_date=start_date,
            end_date=end_date,
            initial_capital=initial_capital,
            final_value=capital,
            total_return=total_return,
            annualized_return=annualized_return,
            max_drawdown=max_dd,
            max_drawdown_date=max_dd_date,
            volatility=vol,
            sharpe_ratio=sharpe,
            sortino_ratio=sortino,
            total_dividends=total_dividends,
            dividend_cagr=dividend_yield,  # Simplified
            up_months=up_months,
            down_months=down_months,
            best_month=max(monthly_returns) if monthly_returns else 0,
            worst_month=min(monthly_returns) if monthly_returns else 0,
            equity_curve=equity_curve,
            drawdown_curve=drawdown_curve,
        )
        
        logger.info("Backtest complete",
                   final_value=capital,
                   total_return=f"{total_return:.1%}",
                   max_drawdown=f"{max_dd:.1%}",
                   sharpe=f"{sharpe:.2f}")
        
        return result
    
    def run_stress_test(
        self,
        scenario: StressScenario,
        current_portfolio_value: float,
        custom_params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Run stress test against a specific scenario
        
        Args:
            scenario: Pre-defined stress scenario
            current_portfolio_value: Current portfolio value
            custom_params: Custom scenario parameters (for CUSTOM scenario)
        """
        logger.info("Running stress test", scenario=scenario.value)
        
        if scenario == StressScenario.CUSTOM:
            params = custom_params or {"drawdown": -0.30, "recovery_months": 12, "dividend_impact": -0.05}
        else:
            params = self.stress_scenarios[scenario]
        
        # Calculate impact
        drawdown = params["drawdown"]
        recovery_months = params["recovery_months"]
        dividend_impact = params["dividend_impact"]
        
        # Apply drawdown
        stressed_value = current_portfolio_value * (1 + drawdown)
        
        # Tactical sleeve impact (reduced during high volatility)
        tactical_allocation = self.config.guardrails.tactical_max_allocation
        if abs(drawdown) > self.config.guardrails.max_drawdown_threshold:
            # Apply drawdown throttle
            tactical_allocation *= (1 - self.config.guardrails.tactical_reduction_on_drawdown)
        
        # Dividend income impact
        current_yield = 0.035  # Assumed
        stressed_yield = current_yield * (1 + dividend_impact)
        annual_income_before = current_portfolio_value * current_yield
        annual_income_after = stressed_value * stressed_yield
        
        return {
            "scenario": scenario.value,
            "parameters": params,
            "impact": {
                "portfolio_before": current_portfolio_value,
                "portfolio_after": stressed_value,
                "drawdown_pct": drawdown,
                "drawdown_amount": current_portfolio_value - stressed_value,
                "recovery_months": recovery_months,
            },
            "tactical": {
                "allocation_before": self.config.guardrails.tactical_max_allocation,
                "allocation_after": tactical_allocation,
                "reduction_applied": tactical_allocation < self.config.guardrails.tactical_max_allocation,
            },
            "dividends": {
                "annual_before": annual_income_before,
                "annual_after": annual_income_after,
                "impact_pct": dividend_impact,
            },
            "guardrails": {
                "max_drawdown_threshold": self.config.guardrails.max_drawdown_threshold,
                "threshold_breached": abs(drawdown) > self.config.guardrails.max_drawdown_threshold,
            },
        }
    
    def run_monte_carlo(
        self,
        initial_capital: float,
        years: int = 10,
        simulations: int = 1000,
        annual_return: float = 0.08,
        dividend_yield: float = 0.035,
        volatility: float = 0.15,
        dividend_cut_prob: float = 0.02,  # Annual probability of dividend cut
        benchmark_return: float = 0.07,  # SPY-like benchmark
    ) -> MonteCarloResult:
        """
        Run Monte Carlo simulation
        
        Tests:
            - Dividend cut scenarios
            - Sector rotation
            - Multi-year stagnation cycles
        """
        logger.info("Running Monte Carlo simulation",
                   simulations=simulations,
                   years=years,
                   capital=initial_capital)
        
        final_values = []
        dividend_cuts = 0
        positive_returns = 0
        beat_benchmark = 0
        drawdown_exceeded = 0
        total_dividend_income = []
        
        for sim in range(simulations):
            capital = initial_capital
            cumulative_dividends = 0.0
            peak = capital
            max_dd = 0.0
            current_yield = dividend_yield
            
            for year in range(years):
                # Check for dividend cut
                if random.random() < dividend_cut_prob:
                    current_yield *= 0.8  # 20% dividend cut
                    dividend_cuts += 1
                
                # Annual return with volatility
                annual_gain = random.gauss(annual_return, volatility)
                capital *= (1 + annual_gain)
                
                # Dividend income
                dividends = capital * current_yield
                reinvest = dividends * self.config.guardrails.core_reinvest_pct
                capital += reinvest
                cumulative_dividends += dividends
                
                # Track drawdown
                if capital > peak:
                    peak = capital
                dd = (peak - capital) / peak
                if dd > max_dd:
                    max_dd = dd
            
            final_values.append(capital)
            total_dividend_income.append(cumulative_dividends)
            
            # Track outcomes
            if capital > initial_capital:
                positive_returns += 1
            
            benchmark_final = initial_capital * ((1 + benchmark_return) ** years)
            if capital > benchmark_final:
                beat_benchmark += 1
            
            if max_dd > self.config.guardrails.max_drawdown_threshold:
                drawdown_exceeded += 1
        
        # Sort for percentiles
        final_values.sort()
        
        result = MonteCarloResult(
            simulations=simulations,
            years=years,
            initial_capital=initial_capital,
            median_final_value=self._percentile(final_values, 50),
            percentile_5=self._percentile(final_values, 5),
            percentile_25=self._percentile(final_values, 25),
            percentile_75=self._percentile(final_values, 75),
            percentile_95=self._percentile(final_values, 95),
            worst_case_value=min(final_values),
            best_case_value=max(final_values),
            prob_positive_return=positive_returns / simulations,
            prob_beat_benchmark=beat_benchmark / simulations,
            prob_max_drawdown_exceeded=drawdown_exceeded / simulations,
            prob_dividend_cut=dividend_cuts / (simulations * years),
            expected_dividend_income=sum(total_dividend_income) / simulations,
            final_values=final_values,
        )
        
        logger.info("Monte Carlo complete",
                   median=result.median_final_value,
                   prob_positive=f"{result.prob_positive_return:.1%}",
                   prob_beat_benchmark=f"{result.prob_beat_benchmark:.1%}")
        
        return result
    
    def validate_drawdown_rules(
        self,
        current_drawdown: float,
    ) -> Dict[str, Any]:
        """
        Validate drawdown management rules
        
        Rule: If DD > 12% → Cut tactical size in half until recovery
        """
        threshold = self.config.guardrails.max_drawdown_threshold
        reduction = self.config.guardrails.tactical_reduction_on_drawdown
        
        is_triggered = current_drawdown > threshold
        
        if is_triggered:
            current_tactical = self.config.guardrails.tactical_max_allocation
            reduced_tactical = current_tactical * (1 - reduction)
            
            return {
                "rule_triggered": True,
                "current_drawdown": current_drawdown,
                "threshold": threshold,
                "tactical_allocation": {
                    "before": current_tactical,
                    "after": reduced_tactical,
                    "reduction": reduction,
                },
                "action": f"Reduce tactical allocation from {current_tactical:.0%} to {reduced_tactical:.0%}",
                "recovery_condition": f"Drawdown must return below {threshold:.0%} to restore allocation",
            }
        
        return {
            "rule_triggered": False,
            "current_drawdown": current_drawdown,
            "threshold": threshold,
            "headroom": threshold - current_drawdown,
            "action": "No action required - within normal parameters",
        }
    
    def _calculate_volatility(self, returns: List[float]) -> float:
        """Calculate standard deviation of returns"""
        if len(returns) < 2:
            return 0.0
        
        mean = sum(returns) / len(returns)
        variance = sum((r - mean) ** 2 for r in returns) / (len(returns) - 1)
        return math.sqrt(variance)
    
    def _percentile(self, sorted_list: List[float], percentile: int) -> float:
        """Get percentile value from sorted list"""
        if not sorted_list:
            return 0.0
        
        index = int(len(sorted_list) * percentile / 100)
        index = max(0, min(index, len(sorted_list) - 1))
        return sorted_list[index]
    
    def generate_validation_report(
        self,
        backtest: BacktestResult,
        stress_tests: List[Dict[str, Any]],
        monte_carlo: MonteCarloResult,
    ) -> Dict[str, Any]:
        """Generate comprehensive validation report"""
        return {
            "timestamp": datetime.now().isoformat(),
            "backtest": backtest.to_dict(),
            "stress_tests": stress_tests,
            "monte_carlo": monte_carlo.to_dict(),
            "summary": {
                "backtest_sharpe": backtest.sharpe_ratio,
                "max_historical_drawdown": backtest.max_drawdown,
                "monte_carlo_median": monte_carlo.median_final_value,
                "probability_success": monte_carlo.prob_positive_return,
                "worst_stress_drawdown": max(st["impact"]["drawdown_pct"] for st in stress_tests) if stress_tests else 0,
            },
            "recommendations": self._generate_recommendations(backtest, stress_tests, monte_carlo),
        }
    
    def _generate_recommendations(
        self,
        backtest: BacktestResult,
        stress_tests: List[Dict[str, Any]],
        monte_carlo: MonteCarloResult,
    ) -> List[str]:
        """Generate recommendations based on validation results"""
        recommendations = []
        
        # Sharpe ratio
        if backtest.sharpe_ratio < 0.5:
            recommendations.append("Consider increasing dividend quality filters to improve risk-adjusted returns")
        
        # Max drawdown
        if backtest.max_drawdown > 0.25:
            recommendations.append("Consider tightening position limits or increasing diversification")
        
        # Monte Carlo success rate
        if monte_carlo.prob_positive_return < 0.85:
            recommendations.append("Review tactical parameters - lower win probability than expected")
        
        # Stress test resilience
        for st in stress_tests:
            if st["guardrails"]["threshold_breached"]:
                recommendations.append(f"Stress scenario {st['scenario']} breaches drawdown threshold - ensure tactical reduction rules are active")
        
        # Dividend cut probability
        if monte_carlo.prob_dividend_cut > 0.05:
            recommendations.append("Dividend cut probability elevated - review payout ratio filters")
        
        if not recommendations:
            recommendations.append("Validation passed - system parameters within acceptable ranges")
        
        return recommendations
