"""
Stock Screener
==============

Automated screening system that generates nightly CSV lists:
    - dividends_core.csv: Passed all filters, ready for core
    - safe_add.csv: Safe to add with minor filters failed
    - avoid.csv: Failed critical filters
    - ranco_candidates.csv: Suitable for tactical overlay

Exclusions:
    - No earnings plays (±5 days)
    - ADV < $1M → ignored
"""

import csv
import os
from dataclasses import dataclass, field
from datetime import datetime, date, timedelta
from typing import List, Dict, Any, Optional
from pathlib import Path
import structlog

from .config import HybridRefineryConfig
from .dividend_engine import (
    DividendEngine, DividendStock, ScreeningResult, 
    StockCategory, ScreeningStatus, DividendMetrics, FinancialMetrics
)
from .ranco_pid import TechnicalIndicators

logger = structlog.get_logger()


@dataclass
class ScreenerOutput:
    """Container for screener output files"""
    output_directory: str
    timestamp: datetime = field(default_factory=datetime.now)
    
    # File paths
    dividends_core_path: str = ""
    safe_add_path: str = ""
    avoid_path: str = ""
    ranco_candidates_path: str = ""
    
    # Counts
    core_count: int = 0
    safe_add_count: int = 0
    avoid_count: int = 0
    ranco_count: int = 0
    
    def __post_init__(self):
        date_str = self.timestamp.strftime("%Y%m%d")
        self.dividends_core_path = os.path.join(self.output_directory, f"dividends_core_{date_str}.csv")
        self.safe_add_path = os.path.join(self.output_directory, f"safe_add_{date_str}.csv")
        self.avoid_path = os.path.join(self.output_directory, f"avoid_{date_str}.csv")
        self.ranco_candidates_path = os.path.join(self.output_directory, f"ranco_candidates_{date_str}.csv")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "timestamp": self.timestamp.isoformat(),
            "output_directory": self.output_directory,
            "files": {
                "dividends_core": self.dividends_core_path,
                "safe_add": self.safe_add_path,
                "avoid": self.avoid_path,
                "ranco_candidates": self.ranco_candidates_path,
            },
            "counts": {
                "core": self.core_count,
                "safe_add": self.safe_add_count,
                "avoid": self.avoid_count,
                "ranco": self.ranco_count,
            },
        }


class StockScreener:
    """
    Automated Stock Screener
    
    Runs nightly to produce 4 CSV lists:
        1. dividends_core.csv - Core dividend candidates
        2. safe_add.csv - Safe to add later
        3. avoid.csv - Avoid these stocks
        4. ranco_candidates.csv - Tactical trading candidates
    """
    
    def __init__(self, config: HybridRefineryConfig):
        self.config = config
        self.dividend_engine = DividendEngine(config)
        self.output_directory = config.automation.output_directory
        
        # Ensure output directory exists
        Path(self.output_directory).mkdir(parents=True, exist_ok=True)
        
        logger.info("Stock Screener initialized",
                   output_dir=self.output_directory)
    
    def run_screen(
        self, 
        universe: List[DividendStock],
        technical_data: Optional[Dict[str, TechnicalIndicators]] = None
    ) -> ScreenerOutput:
        """
        Run the complete screening process
        
        Args:
            universe: List of stocks to screen
            technical_data: Optional technical indicators for RANCO candidates
        
        Returns:
            ScreenerOutput with file paths and counts
        """
        logger.info("Starting screening run", universe_size=len(universe))
        
        # Run dividend engine screening
        results = self.dividend_engine.screen_universe(universe)
        
        # Create output container
        output = ScreenerOutput(output_directory=self.output_directory)
        
        # Generate CSV files
        output.core_count = self._write_core_csv(
            results["dividends_core"], 
            output.dividends_core_path
        )
        
        output.safe_add_count = self._write_safe_add_csv(
            results["safe_add"], 
            output.safe_add_path
        )
        
        output.avoid_count = self._write_avoid_csv(
            results["avoid"], 
            output.avoid_path
        )
        
        # For RANCO candidates, include technical data if available
        ranco_results = results["ranco_candidates"]
        if technical_data:
            ranco_results = self._enrich_with_technicals(ranco_results, technical_data)
        
        output.ranco_count = self._write_ranco_csv(
            ranco_results, 
            output.ranco_candidates_path,
            technical_data
        )
        
        logger.info("Screening complete",
                   core=output.core_count,
                   safe_add=output.safe_add_count,
                   avoid=output.avoid_count,
                   ranco=output.ranco_count)
        
        return output
    
    def _write_core_csv(self, results: List[ScreeningResult], filepath: str) -> int:
        """Write dividends_core.csv"""
        headers = [
            "symbol", "name", "sector", "category", "yield", "payout_ratio",
            "dividend_cagr_5yr", "interest_coverage", "net_debt_ebitda",
            "roic_wacc_spread", "consecutive_years", "buy_zone_low", "buy_zone_high"
        ]
        
        rows = []
        for result in results:
            stock = result.stock
            
            # Calculate buy zones (5% above/below MA50)
            buy_zone_low = stock.ma_50 * 0.95
            buy_zone_high = stock.ma_50 * 1.05
            
            rows.append({
                "symbol": stock.symbol,
                "name": stock.name,
                "sector": stock.sector,
                "category": stock.category.value,
                "yield": f"{stock.dividend_metrics.current_yield:.2%}",
                "payout_ratio": f"{stock.dividend_metrics.payout_ratio:.1%}",
                "dividend_cagr_5yr": f"{stock.dividend_metrics.dividend_cagr_5yr:.1%}",
                "interest_coverage": f"{stock.financial_metrics.interest_coverage:.1f}x",
                "net_debt_ebitda": f"{stock.financial_metrics.net_debt_ebitda:.1f}x",
                "roic_wacc_spread": f"{stock.financial_metrics.roic_wacc_spread:.1%}",
                "consecutive_years": stock.dividend_metrics.consecutive_years_increased,
                "buy_zone_low": f"${buy_zone_low:.2f}",
                "buy_zone_high": f"${buy_zone_high:.2f}",
            })
        
        self._write_csv(filepath, headers, rows)
        return len(rows)
    
    def _write_safe_add_csv(self, results: List[ScreeningResult], filepath: str) -> int:
        """Write safe_add.csv"""
        headers = [
            "symbol", "name", "sector", "yield", "failed_filters", 
            "notes", "watch_for"
        ]
        
        rows = []
        for result in results:
            stock = result.stock
            
            failed_filters = [k for k, v in result.filters_checked.items() if not v]
            
            rows.append({
                "symbol": stock.symbol,
                "name": stock.name,
                "sector": stock.sector,
                "yield": f"{stock.dividend_metrics.current_yield:.2%}",
                "failed_filters": ", ".join(failed_filters),
                "notes": "; ".join(result.notes),
                "watch_for": self._get_watch_recommendation(failed_filters),
            })
        
        self._write_csv(filepath, headers, rows)
        return len(rows)
    
    def _write_avoid_csv(self, results: List[ScreeningResult], filepath: str) -> int:
        """Write avoid.csv"""
        headers = [
            "symbol", "name", "sector", "critical_failures", "all_failures",
            "payout_ratio", "debt_ratio", "risk_level"
        ]
        
        rows = []
        for result in results:
            stock = result.stock
            
            critical = ["payout_ratio", "ffo_payout_ratio", "net_debt_ebitda"]
            failed_critical = [k for k, v in result.filters_checked.items() 
                             if not v and k in critical]
            all_failed = [k for k, v in result.filters_checked.items() if not v]
            
            # Determine risk level
            risk_level = "HIGH" if len(failed_critical) > 1 else "MODERATE"
            
            rows.append({
                "symbol": stock.symbol,
                "name": stock.name,
                "sector": stock.sector,
                "critical_failures": ", ".join(failed_critical),
                "all_failures": ", ".join(all_failed),
                "payout_ratio": f"{stock.dividend_metrics.payout_ratio:.1%}",
                "debt_ratio": f"{stock.financial_metrics.net_debt_ebitda:.1f}x",
                "risk_level": risk_level,
            })
        
        self._write_csv(filepath, headers, rows)
        return len(rows)
    
    def _write_ranco_csv(
        self, 
        results: List[ScreeningResult], 
        filepath: str,
        technical_data: Optional[Dict[str, TechnicalIndicators]] = None
    ) -> int:
        """Write ranco_candidates.csv"""
        headers = [
            "symbol", "name", "sector", "trend_status", "rsi", "atr_compression",
            "entry_zone", "stop_zone", "risk_reward", "signal_strength"
        ]
        
        rows = []
        for result in results:
            stock = result.stock
            tech = technical_data.get(stock.symbol) if technical_data else None
            
            # Calculate entry and stop zones
            if tech:
                entry_zone = f"${tech.current_price:.2f}"
                stop_zone = f"${tech.current_price - tech.atr_14 * 1.5:.2f}"
                atr_compression = "YES" if tech.is_atr_compressed else "NO"
                rsi = f"{tech.rsi_14:.1f}"
                trend = "UPTREND" if tech.is_uptrend else "NO TREND"
                
                # Calculate risk/reward
                risk = tech.atr_14 * 1.5
                reward = tech.atr_14 * 2.0
                rr = reward / risk if risk > 0 else 0
                
                # Signal strength
                strength = "STRONG" if atr_compression == "YES" and tech.is_uptrend and tech.is_rsi_in_range else "MODERATE"
            else:
                entry_zone = f"${stock.current_price:.2f}"
                stop_zone = "N/A"
                atr_compression = "N/A"
                rsi = "N/A"
                trend = "N/A"
                rr = 0
                strength = "UNKNOWN"
            
            rows.append({
                "symbol": stock.symbol,
                "name": stock.name,
                "sector": stock.sector,
                "trend_status": trend,
                "rsi": rsi,
                "atr_compression": atr_compression,
                "entry_zone": entry_zone,
                "stop_zone": stop_zone,
                "risk_reward": f"{rr:.1f}:1",
                "signal_strength": strength,
            })
        
        self._write_csv(filepath, headers, rows)
        return len(rows)
    
    def _enrich_with_technicals(
        self, 
        results: List[ScreeningResult],
        technical_data: Dict[str, TechnicalIndicators]
    ) -> List[ScreeningResult]:
        """Filter RANCO candidates based on technical criteria"""
        enriched = []
        
        for result in results:
            symbol = result.stock.symbol
            if symbol in technical_data:
                tech = technical_data[symbol]
                
                # Apply RANCO entry criteria
                if (tech.is_uptrend and 
                    tech.is_atr_compressed and 
                    tech.is_rsi_in_range):
                    enriched.append(result)
        
        return enriched
    
    def _write_csv(self, filepath: str, headers: List[str], rows: List[Dict[str, Any]]):
        """Write rows to CSV file"""
        with open(filepath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)
        
        logger.debug("CSV written", path=filepath, rows=len(rows))
    
    def _get_watch_recommendation(self, failed_filters: List[str]) -> str:
        """Get recommendation for what to watch"""
        recommendations = []
        
        if "earnings_window" in failed_filters:
            recommendations.append("Wait for earnings to pass")
        if "dividend_cagr_5yr" in failed_filters:
            recommendations.append("Monitor dividend growth trend")
        if "interest_coverage" in failed_filters:
            recommendations.append("Watch for debt reduction")
        if "roic_wacc_spread" in failed_filters:
            recommendations.append("Monitor profitability improvement")
        
        return "; ".join(recommendations) if recommendations else "Monitor for filter improvement"
    
    def get_latest_outputs(self) -> Optional[ScreenerOutput]:
        """Get paths to the latest screening outputs"""
        # Find most recent files
        try:
            files = os.listdir(self.output_directory)
            core_files = [f for f in files if f.startswith("dividends_core_")]
            
            if not core_files:
                return None
            
            # Sort by date in filename and get latest
            core_files.sort(reverse=True)
            latest_date = core_files[0].replace("dividends_core_", "").replace(".csv", "")
            
            output = ScreenerOutput(output_directory=self.output_directory)
            output.dividends_core_path = os.path.join(self.output_directory, f"dividends_core_{latest_date}.csv")
            output.safe_add_path = os.path.join(self.output_directory, f"safe_add_{latest_date}.csv")
            output.avoid_path = os.path.join(self.output_directory, f"avoid_{latest_date}.csv")
            output.ranco_candidates_path = os.path.join(self.output_directory, f"ranco_candidates_{latest_date}.csv")
            
            return output
            
        except Exception as e:
            logger.error("Failed to get latest outputs", error=str(e))
            return None


# ==================== Development/Testing Utilities ====================
#
# The following functions are provided for testing, demonstration, and development
# purposes. In production, stock data would be fetched from a market data provider
# such as:
#   - yfinance (Yahoo Finance)
#   - Alpha Vantage
#   - Polygon.io
#   - IEX Cloud
#   - Bloomberg (institutional)
#
# These utilities create sample stock data that can be used to:
#   - Test screening logic
#   - Verify portfolio construction
#   - Demonstrate the system capabilities
#   - Unit testing without external dependencies
#
# ===========================================================================

def create_sample_stock(
    symbol: str,
    name: str,
    sector: str,
    category: StockCategory = StockCategory.STANDARD,
    current_yield: float = 0.03,
    payout_ratio: float = 0.50,
    dividend_cagr: float = 0.05,
    interest_coverage: float = 8.0,
    net_debt_ebitda: float = 2.0,
    roic: float = 0.12,
    wacc: float = 0.08,
    adv: float = 5_000_000,
    price: float = 100.0,
) -> DividendStock:
    """
    Create a sample dividend stock for testing
    
    This is a utility function for testing and demonstration.
    In production, data would come from a market data provider.
    """
    return DividendStock(
        symbol=symbol,
        name=name,
        sector=sector,
        industry=f"{sector} - General",
        category=category,
        dividend_metrics=DividendMetrics(
            current_yield=current_yield,
            payout_ratio=payout_ratio,
            dividend_cagr_5yr=dividend_cagr,
            consecutive_years_increased=10,
            ex_dividend_date=date.today() + timedelta(days=30),
            next_earnings_date=date.today() + timedelta(days=45),
        ),
        financial_metrics=FinancialMetrics(
            interest_coverage=interest_coverage,
            net_debt_ebitda=net_debt_ebitda,
            roic=roic,
            wacc=wacc,
            average_daily_volume=adv,
            market_cap=50_000_000_000,
        ),
        current_price=price,
        ma_20=price * 1.02,
        ma_50=price * 0.98,
        ma_200=price * 0.95,
    )


def create_sample_universe() -> List[DividendStock]:
    """
    Create a sample universe of dividend stocks
    
    This is for demonstration purposes.
    Production would fetch from a data provider.
    """
    stocks = [
        # Dividend Aristocrats
        create_sample_stock("KO", "Coca-Cola", "Consumer Staples", StockCategory.DIVIDEND_ARISTOCRAT),
        create_sample_stock("JNJ", "Johnson & Johnson", "Healthcare", StockCategory.DIVIDEND_ARISTOCRAT),
        create_sample_stock("PG", "Procter & Gamble", "Consumer Staples", StockCategory.DIVIDEND_ARISTOCRAT),
        create_sample_stock("MCD", "McDonald's", "Consumer Discretionary", StockCategory.DIVIDEND_ARISTOCRAT),
        create_sample_stock("MMM", "3M Company", "Industrials", StockCategory.DIVIDEND_ARISTOCRAT),
        
        # REITs
        create_sample_stock("O", "Realty Income", "Real Estate", StockCategory.QUALITY_REIT, 
                          current_yield=0.05, payout_ratio=0.75),
        create_sample_stock("VICI", "VICI Properties", "Real Estate", StockCategory.QUALITY_REIT,
                          current_yield=0.055, payout_ratio=0.72),
        create_sample_stock("NNN", "National Retail Properties", "Real Estate", StockCategory.QUALITY_REIT,
                          current_yield=0.048, payout_ratio=0.68),
        
        # Utilities
        create_sample_stock("NEE", "NextEra Energy", "Utilities", StockCategory.REGULATED_UTILITY,
                          current_yield=0.025, interest_coverage=5.0),
        create_sample_stock("DUK", "Duke Energy", "Utilities", StockCategory.REGULATED_UTILITY,
                          current_yield=0.04, interest_coverage=4.5),
        
        # Healthcare
        create_sample_stock("ABBV", "AbbVie", "Healthcare", StockCategory.DIVIDEND_ACHIEVER,
                          current_yield=0.04, dividend_cagr=0.10),
        create_sample_stock("PFE", "Pfizer", "Healthcare", StockCategory.STANDARD,
                          current_yield=0.055, dividend_cagr=0.04),
        
        # Tech with dividends
        create_sample_stock("MSFT", "Microsoft", "Technology", StockCategory.DIVIDEND_ACHIEVER,
                          current_yield=0.008, payout_ratio=0.25, roic=0.35),
        create_sample_stock("AAPL", "Apple", "Technology", StockCategory.DIVIDEND_ACHIEVER,
                          current_yield=0.005, payout_ratio=0.15, roic=0.40),
        
        # Financials
        create_sample_stock("JPM", "JPMorgan Chase", "Financials", StockCategory.DIVIDEND_ACHIEVER,
                          current_yield=0.025, interest_coverage=10.0),
        
        # Energy
        create_sample_stock("XOM", "Exxon Mobil", "Energy", StockCategory.STANDARD,
                          current_yield=0.035, net_debt_ebitda=1.5),
        create_sample_stock("CVX", "Chevron", "Energy", StockCategory.DIVIDEND_ACHIEVER,
                          current_yield=0.04, net_debt_ebitda=1.2),
        
        # Industrials
        create_sample_stock("CAT", "Caterpillar", "Industrials", StockCategory.DIVIDEND_ACHIEVER,
                          current_yield=0.015, dividend_cagr=0.08),
        create_sample_stock("HON", "Honeywell", "Industrials", StockCategory.DIVIDEND_ACHIEVER,
                          current_yield=0.02, dividend_cagr=0.06),
        
        # Consumer
        create_sample_stock("WMT", "Walmart", "Consumer Staples", StockCategory.DIVIDEND_ACHIEVER,
                          current_yield=0.015, dividend_cagr=0.02),
        
        # Some that should fail filters
        create_sample_stock("HIGH_PAYOUT", "High Payout Corp", "Industrials", StockCategory.STANDARD,
                          payout_ratio=0.85),  # Fails payout
        create_sample_stock("HIGH_DEBT", "Leveraged Corp", "Financials", StockCategory.STANDARD,
                          net_debt_ebitda=5.0),  # Fails debt
        create_sample_stock("LOW_ADV", "Small Cap Inc", "Technology", StockCategory.STANDARD,
                          adv=500_000),  # Fails liquidity
    ]
    
    return stocks
