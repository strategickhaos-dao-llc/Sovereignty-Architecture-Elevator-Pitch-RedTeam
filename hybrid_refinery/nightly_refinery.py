#!/usr/bin/env python3
"""
Strategickhaos Hybrid Refinery - Nightly Automation Script
Runs daily at 3:00 AM EST to track portfolio equity and drift.

Features:
- Pulls current prices from Yahoo Finance
- Calculates position drift from target weights
- Logs equity curve to CSV
- Sends email summary
"""

import csv
import datetime
import os
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from typing import Optional

import yaml

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Portfolio holdings as of November 27, 2025
PORTFOLIO = {
    'JPM': {'shares': 0.1555, 'cost_basis': 36.40, 'target_weight': 7.00},
    'CB': {'shares': 0.1238, 'cost_basis': 36.40, 'target_weight': 7.01},
    'TD': {'shares': 0.617, 'cost_basis': 36.40, 'target_weight': 7.00},
    'PG': {'shares': 0.244, 'cost_basis': 41.60, 'target_weight': 8.00},
    'KO': {'shares': 0.592, 'cost_basis': 41.60, 'target_weight': 8.00},
    'PEP': {'shares': 0.206, 'cost_basis': 36.40, 'target_weight': 7.00},
    'CL': {'shares': 0.305, 'cost_basis': 31.20, 'target_weight': 6.00},
    'NEE': {'shares': 0.428, 'cost_basis': 36.40, 'target_weight': 7.00},
    'O': {'shares': 0.676, 'cost_basis': 41.60, 'target_weight': 8.01},
    'VICI': {'shares': 1.112, 'cost_basis': 36.40, 'target_weight': 7.01},
    'PLD': {'shares': 0.267, 'cost_basis': 31.20, 'target_weight': 5.99},
    'ABBV': {'shares': 0.185, 'cost_basis': 36.40, 'target_weight': 7.00},
    'JNJ': {'shares': 0.255, 'cost_basis': 41.60, 'target_weight': 8.00},
    'XOM': {'shares': 0.255, 'cost_basis': 31.20, 'target_weight': 6.00},
    'WEC': {'shares': 0.387, 'cost_basis': 36.40, 'target_weight': 7.00},
}

# Base directory for the hybrid refinery
BASE_DIR = Path(__file__).parent
LOGS_DIR = BASE_DIR / 'logs'


def ensure_logs_directory():
    """Create logs directory if it doesn't exist."""
    LOGS_DIR.mkdir(exist_ok=True)
    logger.info(f"Logs directory: {LOGS_DIR}")


def get_stock_prices(tickers: list) -> dict:
    """
    Fetch current stock prices.
    
    In production, this would use yfinance or another data provider.
    For demonstration, returns simulated prices based on cost basis.
    """
    prices = {}
    
    try:
        # Try to import yfinance for real prices
        import yfinance as yf
        
        for ticker in tickers:
            try:
                stock = yf.Ticker(ticker)
                hist = stock.history(period="1d")
                if not hist.empty:
                    prices[ticker] = float(hist['Close'].iloc[-1])
                else:
                    # Fallback to cost basis if no data
                    prices[ticker] = PORTFOLIO[ticker]['cost_basis'] / PORTFOLIO[ticker]['shares']
            except Exception as e:
                logger.warning(f"Could not fetch {ticker}: {e}")
                prices[ticker] = PORTFOLIO[ticker]['cost_basis'] / PORTFOLIO[ticker]['shares']
                
    except ImportError:
        logger.warning("yfinance not installed, using simulated prices")
        # Simulate prices based on cost basis with small random variation
        import random
        for ticker in tickers:
            base_price = PORTFOLIO[ticker]['cost_basis'] / PORTFOLIO[ticker]['shares']
            # Add small random variation (-1% to +1%)
            variation = random.uniform(-0.01, 0.01)
            prices[ticker] = base_price * (1 + variation)
            
    return prices


def calculate_portfolio_values(prices: dict) -> dict:
    """Calculate current portfolio values and weights."""
    values = {}
    total_value = 0.0
    
    for ticker, data in PORTFOLIO.items():
        price = prices.get(ticker, data['cost_basis'] / data['shares'])
        market_value = data['shares'] * price
        values[ticker] = {
            'shares': data['shares'],
            'price': price,
            'market_value': market_value,
            'cost_basis': data['cost_basis'],
            'target_weight': data['target_weight'],
            'gain_loss': market_value - data['cost_basis'],
            'gain_loss_pct': ((market_value - data['cost_basis']) / data['cost_basis']) * 100
        }
        total_value += market_value
        
    # Calculate actual weights and drift
    for ticker in values:
        actual_weight = (values[ticker]['market_value'] / total_value) * 100
        target_weight = values[ticker]['target_weight']
        drift = actual_weight - target_weight
        drift_pct = (drift / target_weight) * 100 if target_weight > 0 else 0
        
        values[ticker]['actual_weight'] = actual_weight
        values[ticker]['drift'] = drift
        values[ticker]['drift_pct'] = drift_pct
        
    return values, total_value


def log_equity_curve(total_value: float, prev_value: Optional[float] = None):
    """Log daily equity value to CSV."""
    csv_path = LOGS_DIR / 'equity_curve.csv'
    today = datetime.date.today().isoformat()
    
    # Calculate daily change
    daily_change = total_value - prev_value if prev_value else 0
    daily_change_pct = (daily_change / prev_value * 100) if prev_value else 0
    
    # Check if file exists to write headers
    file_exists = csv_path.exists()
    
    with open(csv_path, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['date', 'total_equity', 'daily_change', 'daily_change_pct'])
        writer.writerow([today, f'{total_value:.2f}', f'{daily_change:.2f}', f'{daily_change_pct:.2f}'])
        
    logger.info(f"Logged equity: ${total_value:.2f} (change: ${daily_change:.2f})")
    return daily_change, daily_change_pct


def log_positions(values: dict):
    """Log position details to CSV."""
    csv_path = LOGS_DIR / 'positions.csv'
    today = datetime.date.today().isoformat()
    
    file_exists = csv_path.exists()
    
    with open(csv_path, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['date', 'ticker', 'shares', 'price', 'market_value', 
                           'actual_weight', 'target_weight', 'drift_pct'])
        for ticker, data in values.items():
            writer.writerow([
                today,
                ticker,
                f"{data['shares']:.4f}",
                f"{data['price']:.2f}",
                f"{data['market_value']:.2f}",
                f"{data['actual_weight']:.2f}",
                f"{data['target_weight']:.2f}",
                f"{data['drift_pct']:.2f}"
            ])
            
    logger.info(f"Logged {len(values)} positions")


def get_previous_equity() -> Optional[float]:
    """Get previous day's equity value from log."""
    csv_path = LOGS_DIR / 'equity_curve.csv'
    
    if not csv_path.exists():
        return None
        
    try:
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            if rows:
                return float(rows[-1]['total_equity'])
    except (KeyError, ValueError, IndexError):
        pass
        
    return None


def find_max_drift(values: dict) -> tuple:
    """Find the position with maximum drift from target."""
    max_drift_ticker = None
    max_drift_pct = 0
    
    for ticker, data in values.items():
        if abs(data['drift_pct']) > abs(max_drift_pct):
            max_drift_pct = data['drift_pct']
            max_drift_ticker = ticker
            
    return max_drift_ticker, max_drift_pct


def send_email_summary(total_value: float, daily_change: float, 
                       daily_change_pct: float, max_drift: tuple):
    """Send email summary of daily portfolio status."""
    
    # Email configuration from environment
    smtp_server = os.environ.get('SMTP_SERVER', '')
    smtp_port = int(os.environ.get('SMTP_PORT', '587'))
    email_from = os.environ.get('EMAIL_FROM', '')
    email_to = os.environ.get('EMAIL_TO', '')
    email_password = os.environ.get('EMAIL_PASSWORD', '')
    
    if not all([smtp_server, email_from, email_to]):
        logger.warning("Email configuration incomplete, skipping email notification")
        return False
        
    max_drift_ticker, max_drift_pct = max_drift
    today = datetime.date.today().strftime('%B %d, %Y')
    
    subject = f"🏭 Hybrid Refinery Daily: ${total_value:.2f} ({daily_change_pct:+.2f}%)"
    
    body = f"""
Strategickhaos Hybrid Refinery - Daily Summary
{today}

📊 Portfolio Status:
• Total Equity: ${total_value:.2f}
• Daily Change: ${daily_change:.2f} ({daily_change_pct:+.2f}%)
• Top Drift: {max_drift_ticker} at {max_drift_pct:+.2f}%

{"⚠️ ALERT: Position drift exceeds 10%!" if abs(max_drift_pct) > 10 else "✅ All positions within tolerance."}

Next Actions:
• Monthly contribution ($36.40) scheduled for the 1st
• DRIP enabled for all positions
• Rebalancing triggers at 12% drift

--- 
Automated by Strategickhaos Hybrid Refinery v1.0
    """.strip()
    
    try:
        msg = MIMEMultipart()
        msg['From'] = email_from
        msg['To'] = email_to
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            if email_password:
                server.login(email_from, email_password)
            server.send_message(msg)
            
        logger.info("Email summary sent successfully")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return False


def main():
    """Main execution function."""
    logger.info("=" * 50)
    logger.info("Strategickhaos Hybrid Refinery - Nightly Run")
    logger.info("=" * 50)
    
    # Ensure logs directory exists
    ensure_logs_directory()
    
    # Get stock prices
    tickers = list(PORTFOLIO.keys())
    logger.info(f"Fetching prices for {len(tickers)} positions...")
    prices = get_stock_prices(tickers)
    
    # Calculate portfolio values
    values, total_value = calculate_portfolio_values(prices)
    logger.info(f"Total Portfolio Value: ${total_value:.2f}")
    
    # Get previous equity for comparison
    prev_value = get_previous_equity()
    
    # Log equity curve
    daily_change, daily_change_pct = log_equity_curve(total_value, prev_value)
    
    # Log positions
    log_positions(values)
    
    # Find maximum drift
    max_drift = find_max_drift(values)
    max_drift_ticker, max_drift_pct = max_drift
    logger.info(f"Maximum Drift: {max_drift_ticker} at {max_drift_pct:+.2f}%")
    
    # Check for drift alerts
    if abs(max_drift_pct) > 12:
        logger.warning(f"ALERT: {max_drift_ticker} exceeds 12% drift threshold!")
        
    # Send email summary
    send_email_summary(total_value, daily_change, daily_change_pct, max_drift)
    
    # Print summary
    print(f"\n📊 Daily Summary ({datetime.date.today()})")
    print(f"   Total Equity: ${total_value:.2f}")
    print(f"   Daily Change: ${daily_change:.2f} ({daily_change_pct:+.2f}%)")
    print(f"   Top Drift: {max_drift_ticker} at {max_drift_pct:+.2f}%")
    
    logger.info("Nightly run completed successfully")
    return 0


if __name__ == '__main__':
    exit(main())
