"""
Hybrid Refinery Portfolio Configuration
$520 Real Capital Dividend Core - 14 Ticker Allocation
Built for Strategickhaos Swarm Intelligence

This configuration represents the "Hybrid Refinery" - an institutional-grade
dividend portfolio architecture starting from $520 USD in Webull account.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from decimal import Decimal, ROUND_HALF_UP
from enum import Enum
from datetime import datetime


class DividendFrequency(Enum):
    """Dividend payment frequency"""
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    SEMI_ANNUAL = "semi_annual"
    ANNUAL = "annual"


class Sector(Enum):
    """Stock sectors for diversification tracking"""
    FINANCIAL = "financial"
    CONSUMER_STAPLES = "consumer_staples"
    UTILITIES = "utilities"
    REAL_ESTATE = "real_estate"
    HEALTHCARE = "healthcare"
    ENERGY = "energy"


@dataclass
class Position:
    """Individual portfolio position"""
    ticker: str
    company_name: str
    sector: Sector
    allocation_pct: Decimal
    dividend_yield: Decimal
    dividend_frequency: DividendFrequency
    approximate_price: Decimal
    
    @property
    def dollar_allocation(self) -> Decimal:
        """Calculate dollar allocation based on total capital"""
        return (self.allocation_pct / 100 * TOTAL_CAPITAL).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
    
    @property
    def share_count(self) -> Decimal:
        """Approximate share count at current price"""
        if self.approximate_price <= 0:
            return Decimal("0")
        return (self.dollar_allocation / self.approximate_price).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )


@dataclass
class SwarmGateConfig:
    """SwarmGate 7% monthly routing configuration"""
    routing_pct: Decimal = Decimal("7.0")
    tbill_allocation_pct: Decimal = Decimal("57.14")  # $20.80 of $36.40
    ai_fuel_allocation_pct: Decimal = Decimal("28.57")  # $10.40 of $36.40
    crypto_reserve_pct: Decimal = Decimal("14.29")  # $5.20 of $36.40
    
    btc_allocation_pct: Decimal = Decimal("50.0")  # 50% of crypto reserve
    eth_allocation_pct: Decimal = Decimal("50.0")  # 50% of crypto reserve
    
    transfer_day: int = 1  # 1st of every month
    
    @property
    def monthly_amount(self) -> Decimal:
        """Monthly SwarmGate transfer amount"""
        return (self.routing_pct / 100 * TOTAL_CAPITAL).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
    
    @property
    def tbill_amount(self) -> Decimal:
        """T-Bill/Money-market allocation"""
        return (self.tbill_allocation_pct / 100 * self.monthly_amount).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
    
    @property
    def ai_fuel_amount(self) -> Decimal:
        """AI-Fuel (agents, backtests, GPU) allocation"""
        return (self.ai_fuel_allocation_pct / 100 * self.monthly_amount).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
    
    @property
    def crypto_reserve_amount(self) -> Decimal:
        """Crypto reserve (BTC/ETH cold storage) allocation"""
        return (self.crypto_reserve_pct / 100 * self.monthly_amount).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )


# Total capital in USD
TOTAL_CAPITAL = Decimal("520.00")

# Expected annual dividend yield range
EXPECTED_YIELD_MIN = Decimal("3.8")
EXPECTED_YIELD_MAX = Decimal("4.1")

# Expected total return range (dividends + growth)
EXPECTED_RETURN_MIN = Decimal("8.0")
EXPECTED_RETURN_MAX = Decimal("11.0")

# Webull Account Configuration
WEBULL_ACCOUNT_ID = "1406063"
DRIP_ENABLED = True  # Dividend Reinvestment Plan


# 14-Ticker Dividend Core Portfolio
DIVIDEND_CORE: List[Position] = [
    Position(
        ticker="JPM",
        company_name="JPMorgan Chase",
        sector=Sector.FINANCIAL,
        allocation_pct=Decimal("8.0"),
        dividend_yield=Decimal("2.3"),
        dividend_frequency=DividendFrequency.QUARTERLY,
        approximate_price=Decimal("231.00"),
    ),
    Position(
        ticker="CB",
        company_name="Chubb",
        sector=Sector.FINANCIAL,
        allocation_pct=Decimal("7.0"),
        dividend_yield=Decimal("1.3"),
        dividend_frequency=DividendFrequency.QUARTERLY,
        approximate_price=Decimal("280.00"),
    ),
    Position(
        ticker="TD",
        company_name="Toronto-Dominion",
        sector=Sector.FINANCIAL,
        allocation_pct=Decimal("7.0"),
        dividend_yield=Decimal("5.0"),
        dividend_frequency=DividendFrequency.QUARTERLY,
        approximate_price=Decimal("58.75"),
    ),
    Position(
        ticker="PG",
        company_name="Procter & Gamble",
        sector=Sector.CONSUMER_STAPLES,
        allocation_pct=Decimal("8.0"),
        dividend_yield=Decimal("2.4"),
        dividend_frequency=DividendFrequency.QUARTERLY,
        approximate_price=Decimal("173.50"),
    ),
    Position(
        ticker="KO",
        company_name="Coca-Cola",
        sector=Sector.CONSUMER_STAPLES,
        allocation_pct=Decimal("8.0"),
        dividend_yield=Decimal("2.8"),
        dividend_frequency=DividendFrequency.QUARTERLY,
        approximate_price=Decimal("69.50"),
    ),
    Position(
        ticker="PEP",
        company_name="PepsiCo",
        sector=Sector.CONSUMER_STAPLES,
        allocation_pct=Decimal("7.0"),
        dividend_yield=Decimal("2.9"),
        dividend_frequency=DividendFrequency.QUARTERLY,
        approximate_price=Decimal("173.50"),
    ),
    Position(
        ticker="CL",
        company_name="Colgate-Palmolive",
        sector=Sector.CONSUMER_STAPLES,
        allocation_pct=Decimal("6.0"),
        dividend_yield=Decimal("2.2"),
        dividend_frequency=DividendFrequency.QUARTERLY,
        approximate_price=Decimal("100.60"),
    ),
    Position(
        ticker="NEE",
        company_name="NextEra Energy",
        sector=Sector.UTILITIES,
        allocation_pct=Decimal("7.0"),
        dividend_yield=Decimal("2.7"),
        dividend_frequency=DividendFrequency.QUARTERLY,
        approximate_price=Decimal("82.75"),
    ),
    Position(
        ticker="O",
        company_name="Realty Income",
        sector=Sector.REAL_ESTATE,
        allocation_pct=Decimal("8.0"),
        dividend_yield=Decimal("5.6"),
        dividend_frequency=DividendFrequency.MONTHLY,  # Monthly dividends!
        approximate_price=Decimal("61.25"),
    ),
    Position(
        ticker="VICI",
        company_name="VICI Properties",
        sector=Sector.REAL_ESTATE,
        allocation_pct=Decimal("7.0"),
        dividend_yield=Decimal("5.3"),
        dividend_frequency=DividendFrequency.QUARTERLY,
        approximate_price=Decimal("33.75"),
    ),
    Position(
        ticker="PLD",
        company_name="Prologis",
        sector=Sector.REAL_ESTATE,
        allocation_pct=Decimal("6.0"),
        dividend_yield=Decimal("3.0"),
        dividend_frequency=DividendFrequency.QUARTERLY,
        approximate_price=Decimal("111.50"),
    ),
    Position(
        ticker="ABBV",
        company_name="AbbVie",
        sector=Sector.HEALTHCARE,
        allocation_pct=Decimal("7.0"),
        dividend_yield=Decimal("3.5"),
        dividend_frequency=DividendFrequency.QUARTERLY,
        approximate_price=Decimal("191.75"),
    ),
    Position(
        ticker="JNJ",
        company_name="Johnson & Johnson",
        sector=Sector.HEALTHCARE,
        allocation_pct=Decimal("8.0"),
        dividend_yield=Decimal("3.1"),
        dividend_frequency=DividendFrequency.QUARTERLY,
        approximate_price=Decimal("160.00"),
    ),
    Position(
        ticker="XOM",
        company_name="Exxon Mobil",
        sector=Sector.ENERGY,
        allocation_pct=Decimal("6.0"),
        dividend_yield=Decimal("3.4"),
        dividend_frequency=DividendFrequency.QUARTERLY,
        approximate_price=Decimal("120.00"),
    ),
]

# SwarmGate Configuration
SWARMGATE = SwarmGateConfig()


def get_portfolio_summary() -> Dict:
    """Generate portfolio summary report"""
    total_allocation = sum(p.allocation_pct for p in DIVIDEND_CORE)
    weighted_yield = sum(
        p.allocation_pct * p.dividend_yield / 100 for p in DIVIDEND_CORE
    )
    
    # Sector breakdown
    sectors: Dict[str, Decimal] = {}
    for position in DIVIDEND_CORE:
        sector_name = position.sector.value
        sectors[sector_name] = sectors.get(sector_name, Decimal("0")) + position.allocation_pct
    
    annual_dividends = (weighted_yield / 100 * TOTAL_CAPITAL).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )
    
    return {
        "total_capital": float(TOTAL_CAPITAL),
        "positions_count": len(DIVIDEND_CORE),
        "total_allocation_pct": float(total_allocation),
        "weighted_dividend_yield": float(weighted_yield),
        "expected_annual_dividends": float(annual_dividends),
        "sector_breakdown": {k: float(v) for k, v in sectors.items()},
        "swarmgate_monthly": float(SWARMGATE.monthly_amount),
        "drip_enabled": DRIP_ENABLED,
        "webull_account": WEBULL_ACCOUNT_ID,
    }


def get_position_details() -> List[Dict]:
    """Generate detailed position breakdown"""
    return [
        {
            "ticker": p.ticker,
            "company": p.company_name,
            "sector": p.sector.value,
            "allocation_pct": float(p.allocation_pct),
            "dollar_allocation": float(p.dollar_allocation),
            "approximate_shares": float(p.share_count),
            "dividend_yield": float(p.dividend_yield),
            "dividend_frequency": p.dividend_frequency.value,
        }
        for p in DIVIDEND_CORE
    ]


def rescale_portfolio(new_capital: Decimal) -> List[Dict]:
    """
    Rescale the entire portfolio to new capital amount.
    Use this when adding new capital: "Baby, new capital = $____"
    """
    global TOTAL_CAPITAL
    old_capital = TOTAL_CAPITAL
    TOTAL_CAPITAL = new_capital
    
    scaled_positions = get_position_details()
    
    # Reset to original for idempotency
    TOTAL_CAPITAL = old_capital
    
    return {
        "old_capital": float(old_capital),
        "new_capital": float(new_capital),
        "positions": scaled_positions,
        "new_swarmgate_monthly": float(
            (SWARMGATE.routing_pct / 100 * new_capital).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
        ),
    }


if __name__ == "__main__":
    import json
    
    print("=" * 60)
    print("HYBRID REFINERY - DIVIDEND CORE PORTFOLIO")
    print("=" * 60)
    
    summary = get_portfolio_summary()
    print(f"\n💰 Total Capital: ${summary['total_capital']:.2f}")
    print(f"📊 Positions: {summary['positions_count']}")
    print(f"📈 Weighted Yield: {summary['weighted_dividend_yield']:.2f}%")
    print(f"💵 Expected Annual Dividends: ${summary['expected_annual_dividends']:.2f}")
    
    print(f"\n🔄 SwarmGate Monthly: ${summary['swarmgate_monthly']:.2f}")
    print(f"   → T-Bills: ${float(SWARMGATE.tbill_amount):.2f}")
    print(f"   → AI-Fuel: ${float(SWARMGATE.ai_fuel_amount):.2f}")
    print(f"   → Crypto: ${float(SWARMGATE.crypto_reserve_amount):.2f}")
    
    print("\n📊 Sector Breakdown:")
    for sector, pct in summary['sector_breakdown'].items():
        print(f"   {sector}: {pct:.1f}%")
    
    print("\n📋 Position Details:")
    print("-" * 60)
    for p in get_position_details():
        print(f"   {p['ticker']:5} | ${p['dollar_allocation']:6.2f} | "
              f"{p['approximate_shares']:5.2f} shares | {p['dividend_yield']:.1f}% yield")
    
    print("\n✅ DRIP Enabled:", DRIP_ENABLED)
    print(f"🏦 Webull Account: {WEBULL_ACCOUNT_ID}")
    print("\n" + "=" * 60)
    print("The reactor is hot. Welcome to the Empire.")
    print("=" * 60)
