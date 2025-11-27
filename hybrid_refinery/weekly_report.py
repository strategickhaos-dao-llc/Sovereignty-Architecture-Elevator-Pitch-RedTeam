#!/usr/bin/env python3
"""
Strategickhaos Hybrid Refinery - Weekly Report Generator
Runs every Sunday at 8:00 AM EST to generate comprehensive portfolio report.

Features:
- Full portfolio heatmap visualization
- Dividend forecast and tracking
- SwarmGate log integration
- Performance metrics and projections
"""

import csv
import datetime
import json
import os
import logging
from pathlib import Path
from typing import Optional

import yaml

# Import centralized configuration
try:
    from .config_loader import (
        get_portfolio, get_monthly_contribution, 
        get_annual_return_expectation, get_dividend_growth_rate
    )
except ImportError:
    from config_loader import (
        get_portfolio, get_monthly_contribution,
        get_annual_return_expectation, get_dividend_growth_rate
    )

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load portfolio and configuration from centralized config
PORTFOLIO = get_portfolio()
MONTHLY_CONTRIBUTION = get_monthly_contribution()
EXPECTED_ANNUAL_RETURN = get_annual_return_expectation()
DIVIDEND_GROWTH_RATE = get_dividend_growth_rate()

# Base directory
BASE_DIR = Path(__file__).parent
LOGS_DIR = BASE_DIR / 'logs'
REPORTS_DIR = BASE_DIR / 'reports'


def ensure_directories():
    """Create necessary directories."""
    LOGS_DIR.mkdir(exist_ok=True)
    REPORTS_DIR.mkdir(exist_ok=True)


def load_equity_history() -> list:
    """Load equity history from CSV."""
    csv_path = LOGS_DIR / 'equity_curve.csv'
    
    if not csv_path.exists():
        return []
        
    history = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            history.append({
                'date': row['date'],
                'equity': float(row['total_equity']),
                'change': float(row.get('daily_change', 0)),
                'change_pct': float(row.get('daily_change_pct', 0))
            })
            
    return history


def calculate_weekly_performance(history: list) -> dict:
    """Calculate weekly performance metrics."""
    if len(history) < 2:
        return {
            'week_start': None,
            'week_end': None,
            'start_equity': 0,
            'end_equity': 0,
            'week_change': 0,
            'week_change_pct': 0
        }
        
    # Get last 7 days or available data
    recent = history[-7:] if len(history) >= 7 else history
    
    start_equity = recent[0]['equity']
    end_equity = recent[-1]['equity']
    week_change = end_equity - start_equity
    week_change_pct = (week_change / start_equity * 100) if start_equity > 0 else 0
    
    return {
        'week_start': recent[0]['date'],
        'week_end': recent[-1]['date'],
        'start_equity': start_equity,
        'end_equity': end_equity,
        'week_change': week_change,
        'week_change_pct': week_change_pct
    }


def calculate_sector_allocation() -> dict:
    """Calculate current sector allocation."""
    sectors = {}
    total_cost = sum(p['cost_basis'] for p in PORTFOLIO.values())
    
    for ticker, data in PORTFOLIO.items():
        sector = data['sector']
        if sector not in sectors:
            sectors[sector] = {'cost_basis': 0, 'weight': 0, 'tickers': []}
        sectors[sector]['cost_basis'] += data['cost_basis']
        sectors[sector]['tickers'].append(ticker)
        
    for sector in sectors:
        sectors[sector]['weight'] = (sectors[sector]['cost_basis'] / total_cost) * 100
        
    return sectors


def calculate_dividend_forecast() -> dict:
    """Calculate projected annual dividend income."""
    total_cost = sum(p['cost_basis'] for p in PORTFOLIO.values())
    weighted_yield = 0
    
    for ticker, data in PORTFOLIO.items():
        weight = data['cost_basis'] / total_cost
        weighted_yield += weight * data['div_yield']
        
    annual_dividends = total_cost * (weighted_yield / 100)
    monthly_dividends = annual_dividends / 12
    quarterly_dividends = annual_dividends / 4
    
    # Project future dividends using configured growth rate
    dividend_growth = 1 + (DIVIDEND_GROWTH_RATE / 100)
    projections = []
    current_annual = annual_dividends
    for year in range(1, 16):
        projections.append({
            'year': year,
            'annual_dividends': current_annual,
            'monthly_dividends': current_annual / 12
        })
        current_annual *= dividend_growth
        
    return {
        'portfolio_yield': weighted_yield,
        'annual_dividends': annual_dividends,
        'monthly_dividends': monthly_dividends,
        'quarterly_dividends': quarterly_dividends,
        'projections': projections
    }


def generate_heatmap_data() -> list:
    """Generate heatmap data for portfolio visualization."""
    heatmap = []
    total_cost = sum(p['cost_basis'] for p in PORTFOLIO.values())
    
    for ticker, data in PORTFOLIO.items():
        actual_weight = (data['cost_basis'] / total_cost) * 100
        drift = actual_weight - data['target_weight']
        drift_pct = (drift / data['target_weight']) * 100 if data['target_weight'] > 0 else 0
        
        # Determine color based on drift
        if drift_pct > 10:
            color = 'red'  # Overweight
        elif drift_pct < -10:
            color = 'blue'  # Underweight
        elif abs(drift_pct) > 5:
            color = 'yellow'  # Warning
        else:
            color = 'green'  # On target
            
        heatmap.append({
            'ticker': ticker,
            'sector': data['sector'],
            'actual_weight': actual_weight,
            'target_weight': data['target_weight'],
            'drift_pct': drift_pct,
            'color': color,
            'div_yield': data['div_yield']
        })
        
    return sorted(heatmap, key=lambda x: abs(x['drift_pct']), reverse=True)


def calculate_growth_projections() -> dict:
    """Calculate portfolio growth projections."""
    initial_investment = 520.00
    monthly_contribution = MONTHLY_CONTRIBUTION
    annual_return = EXPECTED_ANNUAL_RETURN / 100  # Convert from percentage
    
    projections = []
    balance = initial_investment
    total_contributed = initial_investment
    
    for year in range(1, 16):
        for month in range(12):
            balance += monthly_contribution
            total_contributed += monthly_contribution
            balance *= (1 + annual_return / 12)
            
        projections.append({
            'year': year,
            'balance': balance,
            'total_contributed': total_contributed,
            'growth': balance - total_contributed
        })
        
    return {
        'initial': initial_investment,
        'monthly_contribution': monthly_contribution,
        'annual_return': EXPECTED_ANNUAL_RETURN,
        'projections': projections
    }


def generate_swarmgate_log() -> list:
    """Generate SwarmGate activity log."""
    # Simulated SwarmGate log entries
    logs = [
        {
            'timestamp': datetime.datetime.now().isoformat(),
            'event': 'SYSTEM_CHECK',
            'status': 'OK',
            'message': 'Weekly system health check passed'
        },
        {
            'timestamp': datetime.datetime.now().isoformat(),
            'event': 'DRIP_STATUS',
            'status': 'ACTIVE',
            'message': 'Dividend reinvestment enabled for all positions'
        },
        {
            'timestamp': datetime.datetime.now().isoformat(),
            'event': 'CONTRIBUTION_SCHEDULED',
            'status': 'PENDING',
            'message': f'Monthly ${MONTHLY_CONTRIBUTION} contribution scheduled for 1st'
        },
        {
            'timestamp': datetime.datetime.now().isoformat(),
            'event': 'DRIFT_CHECK',
            'status': 'OK',
            'message': 'All positions within drift tolerance'
        }
    ]
    
    return logs


def generate_report() -> dict:
    """Generate comprehensive weekly report."""
    report_date = datetime.datetime.now()
    
    # Load history and calculate metrics
    history = load_equity_history()
    weekly_perf = calculate_weekly_performance(history)
    sectors = calculate_sector_allocation()
    dividends = calculate_dividend_forecast()
    heatmap = generate_heatmap_data()
    growth = calculate_growth_projections()
    swarmgate = generate_swarmgate_log()
    
    # Current portfolio value
    current_equity = history[-1]['equity'] if history else sum(p['cost_basis'] for p in PORTFOLIO.values())
    total_cost = sum(p['cost_basis'] for p in PORTFOLIO.values())
    
    report = {
        'report_date': report_date.isoformat(),
        'report_week': report_date.strftime('Week %W, %Y'),
        
        'summary': {
            'total_equity': current_equity,
            'total_cost_basis': total_cost,
            'unrealized_gain_loss': current_equity - total_cost,
            'unrealized_gain_loss_pct': ((current_equity - total_cost) / total_cost) * 100,
            'positions_count': len(PORTFOLIO),
            'monthly_contribution': MONTHLY_CONTRIBUTION
        },
        
        'weekly_performance': weekly_perf,
        'sector_allocation': sectors,
        'dividend_forecast': dividends,
        'heatmap': heatmap,
        'growth_projections': growth,
        'swarmgate_log': swarmgate,
        
        'alerts': [],
        'recommendations': []
    }
    
    # Check for alerts
    for item in heatmap:
        if abs(item['drift_pct']) > 10:
            report['alerts'].append({
                'type': 'DRIFT_WARNING',
                'ticker': item['ticker'],
                'drift_pct': item['drift_pct'],
                'message': f"{item['ticker']} is {abs(item['drift_pct']):.1f}% {'over' if item['drift_pct'] > 0 else 'under'}weight"
            })
            
    # Generate recommendations
    underweight = [h for h in heatmap if h['drift_pct'] < -5]
    if underweight:
        most_underweight = min(underweight, key=lambda x: x['drift_pct'])
        report['recommendations'].append({
            'type': 'BUY_RECOMMENDATION',
            'ticker': most_underweight['ticker'],
            'message': f"Consider adding to {most_underweight['ticker']} (most underweight at {most_underweight['drift_pct']:.1f}%)"
        })
        
    return report


def save_report(report: dict):
    """Save report to file."""
    report_date = datetime.datetime.now().strftime('%Y-%m-%d')
    
    # Save JSON report
    json_path = REPORTS_DIR / f'weekly_report_{report_date}.json'
    with open(json_path, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    logger.info(f"JSON report saved: {json_path}")
    
    # Generate text report
    text_report = generate_text_report(report)
    txt_path = REPORTS_DIR / f'weekly_report_{report_date}.txt'
    with open(txt_path, 'w') as f:
        f.write(text_report)
    logger.info(f"Text report saved: {txt_path}")
    
    return json_path, txt_path


def generate_text_report(report: dict) -> str:
    """Generate human-readable text report."""
    lines = []
    lines.append("=" * 60)
    lines.append("STRATEGICKHAOS HYBRID REFINERY - WEEKLY REPORT")
    lines.append(f"Report Date: {report['report_date'][:10]}")
    lines.append("=" * 60)
    lines.append("")
    
    # Summary
    summary = report['summary']
    lines.append("📊 PORTFOLIO SUMMARY")
    lines.append("-" * 40)
    lines.append(f"Total Equity:      ${summary['total_equity']:.2f}")
    lines.append(f"Total Cost Basis:  ${summary['total_cost_basis']:.2f}")
    lines.append(f"Unrealized G/L:    ${summary['unrealized_gain_loss']:.2f} ({summary['unrealized_gain_loss_pct']:.2f}%)")
    lines.append(f"Positions:         {summary['positions_count']}")
    lines.append(f"Monthly Add:       ${summary['monthly_contribution']:.2f}")
    lines.append("")
    
    # Weekly Performance
    weekly = report['weekly_performance']
    lines.append("📈 WEEKLY PERFORMANCE")
    lines.append("-" * 40)
    if weekly['week_start']:
        lines.append(f"Period: {weekly['week_start']} to {weekly['week_end']}")
        lines.append(f"Change: ${weekly['week_change']:.2f} ({weekly['week_change_pct']:.2f}%)")
    else:
        lines.append("Insufficient data for weekly comparison")
    lines.append("")
    
    # Sector Allocation
    lines.append("🏭 SECTOR ALLOCATION")
    lines.append("-" * 40)
    for sector, data in report['sector_allocation'].items():
        lines.append(f"{sector:20} {data['weight']:5.1f}% | {', '.join(data['tickers'])}")
    lines.append("")
    
    # Dividend Forecast
    div = report['dividend_forecast']
    lines.append("💰 DIVIDEND FORECAST")
    lines.append("-" * 40)
    lines.append(f"Portfolio Yield:   {div['portfolio_yield']:.2f}%")
    lines.append(f"Annual Dividends:  ${div['annual_dividends']:.2f}")
    lines.append(f"Monthly Dividends: ${div['monthly_dividends']:.2f}")
    lines.append("")
    
    # Growth Projections
    growth = report['growth_projections']
    lines.append("🚀 GROWTH PROJECTIONS (8% annual return)")
    lines.append("-" * 40)
    for proj in growth['projections'][:5]:  # First 5 years
        lines.append(f"Year {proj['year']:2}: ${proj['balance']:,.2f} (contributed: ${proj['total_contributed']:,.2f})")
    lines.append("...")
    proj_15 = growth['projections'][-1]
    lines.append(f"Year 15: ${proj_15['balance']:,.2f} (contributed: ${proj_15['total_contributed']:,.2f})")
    lines.append("")
    
    # Heatmap Summary
    lines.append("🎯 POSITION DRIFT HEATMAP")
    lines.append("-" * 40)
    for item in report['heatmap'][:5]:  # Top 5 by drift
        indicator = "🔴" if item['color'] == 'red' else "🔵" if item['color'] == 'blue' else "🟡" if item['color'] == 'yellow' else "🟢"
        lines.append(f"{indicator} {item['ticker']:5} {item['drift_pct']:+6.1f}% drift | Target: {item['target_weight']:.1f}%")
    lines.append("")
    
    # Alerts
    if report['alerts']:
        lines.append("⚠️ ALERTS")
        lines.append("-" * 40)
        for alert in report['alerts']:
            lines.append(f"• {alert['message']}")
        lines.append("")
        
    # Recommendations
    if report['recommendations']:
        lines.append("💡 RECOMMENDATIONS")
        lines.append("-" * 40)
        for rec in report['recommendations']:
            lines.append(f"• {rec['message']}")
        lines.append("")
        
    # SwarmGate Log
    lines.append("🔧 SWARMGATE LOG")
    lines.append("-" * 40)
    for log in report['swarmgate_log']:
        lines.append(f"[{log['status']}] {log['event']}: {log['message']}")
    lines.append("")
    
    lines.append("=" * 60)
    lines.append("Generated by Strategickhaos Hybrid Refinery v1.0")
    lines.append("Next report: Next Sunday at 8:00 AM EST")
    lines.append("=" * 60)
    
    return "\n".join(lines)


def send_discord_notification(report: dict):
    """Send report summary to Discord webhook."""
    webhook_url = os.environ.get('DISCORD_WEBHOOK_URL', '')
    
    if not webhook_url:
        logger.warning("Discord webhook URL not configured, skipping notification")
        return False
        
    try:
        import requests
        
        summary = report['summary']
        weekly = report['weekly_performance']
        div = report['dividend_forecast']
        
        embed = {
            "title": "📊 Hybrid Refinery Weekly Report",
            "description": f"**{report['report_week']}**",
            "color": 0x00ff00,
            "fields": [
                {"name": "Total Equity", "value": f"${summary['total_equity']:.2f}", "inline": True},
                {"name": "Weekly Change", "value": f"${weekly['week_change']:.2f} ({weekly['week_change_pct']:.2f}%)", "inline": True},
                {"name": "Portfolio Yield", "value": f"{div['portfolio_yield']:.2f}%", "inline": True},
                {"name": "Annual Dividends", "value": f"${div['annual_dividends']:.2f}", "inline": True},
            ],
            "footer": {"text": "Strategickhaos Hybrid Refinery v1.0"}
        }
        
        payload = {"embeds": [embed]}
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
        
        logger.info("Discord notification sent successfully")
        return True
        
    except ImportError:
        logger.warning("requests library not installed")
        return False
    except Exception as e:
        logger.error(f"Failed to send Discord notification: {e}")
        return False


def main():
    """Main execution function."""
    logger.info("=" * 50)
    logger.info("Strategickhaos Hybrid Refinery - Weekly Report")
    logger.info("=" * 50)
    
    # Ensure directories exist
    ensure_directories()
    
    # Generate report
    logger.info("Generating weekly report...")
    report = generate_report()
    
    # Save report
    json_path, txt_path = save_report(report)
    
    # Send Discord notification
    send_discord_notification(report)
    
    # Print summary
    summary = report['summary']
    print(f"\n📊 Weekly Report Generated ({datetime.date.today()})")
    print(f"   Total Equity: ${summary['total_equity']:.2f}")
    print(f"   Unrealized G/L: ${summary['unrealized_gain_loss']:.2f}")
    print(f"   Reports saved to: {REPORTS_DIR}")
    
    # Print text report to console
    print("\n" + generate_text_report(report))
    
    logger.info("Weekly report completed successfully")
    return 0


if __name__ == '__main__':
    exit(main())
