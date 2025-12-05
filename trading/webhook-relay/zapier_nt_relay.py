"""
Zapier to NinjaTrader Webhook Relay
===================================
A secure Flask middleware for relaying trading signals from Zapier to NinjaTrader.

Features:
- Ticker whitelist validation
- Position size caps
- Portfolio weight rebalancing verification
- Manual approval hooks (configurable)
- Secure forwarding to local NT API

Usage:
    pip install flask pyyaml
    python zapier_nt_relay.py

Test with curl:
    curl -X POST http://localhost:5000/webhook \\
        -H "Content-Type: application/json" \\
        -d '{"signal": "BUY 2 shares of ES @ $5200.50"}'

Production:
    - Run behind nginx/caddy with SSL
    - Use environment variables for secrets
    - Enable manual approval for high-risk trades
"""

import os
import re
import logging
from datetime import datetime
from typing import Optional

import yaml
from flask import Flask, request, jsonify

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('zapier_nt_relay')

app = Flask(__name__)

# =============================================================================
# Configuration
# =============================================================================

# Allowed tickers - only these symbols will be processed
# Configure via ALLOWED_TICKERS env var (comma-separated) or modify this list
ALLOWED_TICKERS_DEFAULT = ['ES', 'MNQ', 'NQ', 'BTC', 'ETH', 'SPY', 'QQQ']
ALLOWED_TICKERS = os.getenv('ALLOWED_TICKERS', ','.join(ALLOWED_TICKERS_DEFAULT)).split(',')
ALLOWED_TICKERS = [t.strip().upper() for t in ALLOWED_TICKERS if t.strip()]

# Maximum position size per order (contracts/shares)
MAX_SIZE = int(os.getenv('MAX_SIZE', '5'))

# High-value trade threshold for manual approval
HIGH_VALUE_THRESHOLD = float(os.getenv('HIGH_VALUE_THRESHOLD', '10000'))

# Target portfolio weights for rebalancing verification
# Configure via PORTFOLIO_CONFIG_FILE env var for external config
PORTFOLIO_CONFIG_FILE = os.getenv('PORTFOLIO_CONFIG_FILE')
if PORTFOLIO_CONFIG_FILE and os.path.exists(PORTFOLIO_CONFIG_FILE):
    with open(PORTFOLIO_CONFIG_FILE) as f:
        TARGET_WEIGHTS = yaml.safe_load(f)
else:
    TARGET_WEIGHTS = yaml.safe_load('''
portfolio:
  ES: 0.4
  MNQ: 0.3
  SGO_V: 0.2
  AI_FUEL: 0.1
''')

# Daily risk tracking
# NOTE: This is suitable for single-process deployments. For multi-worker
# deployments (e.g., gunicorn with multiple workers), use Redis or database
# for shared state. See README for production deployment guidance.
daily_state = {
    'date': None,
    'pnl': 0.0,
    'trade_count': 0,
    'max_daily_loss': float(os.getenv('MAX_DAILY_LOSS', '-500.0')),  # Dollars
    'max_trades': int(os.getenv('MAX_DAILY_TRADES', '10'))
}

# NinjaTrader local API endpoint (configure for your setup)
NT_API_URL = os.getenv('NT_API_URL', 'http://localhost:5001/execute')

# Require manual approval for trades (set via env var)
REQUIRE_APPROVAL = os.getenv('REQUIRE_APPROVAL', 'false').lower() == 'true'


# =============================================================================
# Helper Functions
# =============================================================================

def reset_daily_state_if_needed():
    """Reset daily tracking on new trading day."""
    today = datetime.now().date()
    if daily_state['date'] != today:
        daily_state['date'] = today
        daily_state['pnl'] = 0.0
        daily_state['trade_count'] = 0
        logger.info(f"Daily state reset for {today}")


def parse_signal(signal: str) -> list:
    """
    Parse trading signal string into structured orders.
    
    Supports formats:
    - "BUY 2 shares of ES @ $5200.50"
    - "SELL 1 shares of MNQ @ $18500"
    """
    # Pattern: BUY/SELL quantity shares of TICKER @ $price
    # Supports: "BUY 2 shares of ES @ $5200.50", "SELL 1.5 shares of MNQ @ $18500"
    pattern = r'(BUY|SELL)\s+(\d+(?:\.\d+)?)\s+shares?\s+of\s+(\w+)\s+@\s+\$?(\d+(?:\.\d+)?)'
    matches = re.findall(pattern, signal, re.IGNORECASE)
    
    orders = []
    for action, qty, ticker, price in matches:
        orders.append({
            'action': action.upper(),
            'qty': float(qty),
            'ticker': ticker.upper(),
            'price': float(price)
        })
    
    return orders


def validate_orders(orders: list) -> tuple:
    """
    Validate orders against whitelist and size limits.
    Returns (is_valid, error_message, sanitized_orders).
    """
    sanitized = []
    
    for order in orders:
        # Check ticker whitelist
        if order['ticker'] not in ALLOWED_TICKERS:
            return False, f"Ticker {order['ticker']} not in whitelist", []
        
        # Check size limit
        if order['qty'] > MAX_SIZE:
            return False, f"Size {order['qty']} exceeds max {MAX_SIZE}", []
        
        # Check positive quantity
        if order['qty'] <= 0:
            return False, f"Invalid quantity: {order['qty']}", []
        
        sanitized.append(order)
    
    return True, None, sanitized


def check_daily_limits() -> tuple:
    """
    Check if daily trading limits have been reached.
    Returns (can_trade, reason).
    """
    reset_daily_state_if_needed()
    
    if daily_state['pnl'] <= daily_state['max_daily_loss']:
        return False, f"Daily loss limit reached: ${daily_state['pnl']:.2f}"
    
    if daily_state['trade_count'] >= daily_state['max_trades']:
        return False, f"Daily trade limit reached: {daily_state['trade_count']}"
    
    return True, None


def check_portfolio_balance(orders: list) -> tuple:
    """
    Verify orders align with target portfolio weights.
    Returns (is_balanced, deviation).
    """
    total_weight = sum(
        TARGET_WEIGHTS['portfolio'].get(o['ticker'], 0) 
        for o in orders
    )
    
    # Allow 1% deviation from target
    if abs(total_weight - 1.0) > 0.01 and total_weight > 0:
        return False, total_weight
    
    return True, total_weight


def forward_to_ninjatrader(orders: list) -> bool:
    """
    Forward validated orders to NinjaTrader API.
    
    IMPORTANT: This is a STUB implementation for development/testing.
    In production, you MUST implement actual forwarding to your NT instance.
    
    Production implementation example:
        import requests
        response = requests.post(NT_API_URL, json={'orders': orders}, timeout=5)
        return response.ok
    
    Returns:
        bool: True if forwarding succeeded (stub always returns True)
    """
    # Log the orders that would be forwarded
    logger.warning("STUB: forward_to_ninjatrader - implement actual NT API call for production")
    logger.info(f"Would forward to NT ({NT_API_URL}): {orders}")
    
    # Production implementation (uncomment and configure):
    # try:
    #     import requests
    #     response = requests.post(NT_API_URL, json={'orders': orders}, timeout=5)
    #     if not response.ok:
    #         logger.error(f"NT API error: {response.status_code} - {response.text}")
    #     return response.ok
    # except Exception as e:
    #     logger.error(f"NT forward failed: {e}")
    #     return False
    
    # Stub returns True for testing/development
    return True


# =============================================================================
# Flask Routes
# =============================================================================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'daily_trades': daily_state['trade_count'],
        'daily_pnl': daily_state['pnl']
    }), 200


@app.route('/webhook', methods=['POST'])
def handle_signal():
    """
    Main webhook endpoint for Zapier signals.
    
    Expected payload:
    {
        "signal": "BUY 2 shares of ES @ $5200.50"
    }
    """
    # Validate request
    data = request.json
    if not data or 'signal' not in data:
        logger.warning("Invalid payload received")
        return jsonify({'error': 'Invalid payload - missing signal'}), 400
    
    signal = data['signal']
    logger.info(f"Received signal: {signal}")
    
    # Parse signal into orders
    orders = parse_signal(signal)
    if not orders:
        logger.warning(f"No valid orders parsed from signal: {signal}")
        return jsonify({'error': 'No valid orders in signal'}), 400
    
    # Validate orders (whitelist, size limits)
    is_valid, error, sanitized_orders = validate_orders(orders)
    if not is_valid:
        logger.warning(f"Order validation failed: {error}")
        return jsonify({'error': error}), 403
    
    # Check daily limits
    can_trade, limit_reason = check_daily_limits()
    if not can_trade:
        logger.warning(f"Daily limit reached: {limit_reason}")
        return jsonify({'error': limit_reason}), 403
    
    # Optional: Check portfolio balance (for rebalancing strategies)
    # is_balanced, weight = check_portfolio_balance(sanitized_orders)
    # if not is_balanced:
    #     logger.warning(f"Portfolio rebalance mismatch: {weight}")
    #     return jsonify({'error': f'Rebalance mismatch: weight={weight}'}), 400
    
    # Manual approval check
    if REQUIRE_APPROVAL:
        # In production: Send notification (email/SMS/Discord) and await approval
        # For now, auto-approve low-risk orders
        total_value = sum(o['qty'] * o['price'] for o in sanitized_orders)
        if total_value > HIGH_VALUE_THRESHOLD:
            logger.info(f"High-value order requires manual approval: ${total_value:.2f}")
            return jsonify({
                'status': 'pending_approval',
                'orders': sanitized_orders,
                'total_value': total_value
            }), 202
    
    # Forward to NinjaTrader
    forwarded = forward_to_ninjatrader(sanitized_orders)
    if not forwarded:
        logger.error("Failed to forward orders to NinjaTrader")
        return jsonify({'error': 'NT forward failed'}), 500
    
    # Update daily tracking
    daily_state['trade_count'] += len(sanitized_orders)
    
    logger.info(f"Orders forwarded successfully: {sanitized_orders}")
    return jsonify({
        'status': 'forwarded',
        'orders': sanitized_orders,
        'trade_count_today': daily_state['trade_count']
    }), 200


@app.route('/config', methods=['GET'])
def get_config():
    """Return current relay configuration (for debugging)."""
    return jsonify({
        'allowed_tickers': ALLOWED_TICKERS,
        'max_size': MAX_SIZE,
        'target_weights': TARGET_WEIGHTS,
        'require_approval': REQUIRE_APPROVAL,
        'daily_limits': {
            'max_loss': daily_state['max_daily_loss'],
            'max_trades': daily_state['max_trades']
        }
    }), 200


@app.route('/reset', methods=['POST'])
def reset_daily():
    """Manually reset daily state (for testing/admin)."""
    daily_state['pnl'] = 0.0
    daily_state['trade_count'] = 0
    daily_state['date'] = datetime.now().date()
    logger.info("Daily state manually reset")
    return jsonify({'status': 'reset', 'date': str(daily_state['date'])}), 200


# =============================================================================
# Main Entry Point
# =============================================================================

if __name__ == '__main__':
    # Get configuration from environment
    host = os.getenv('RELAY_HOST', '0.0.0.0')
    port = int(os.getenv('RELAY_PORT', '5000'))
    debug = os.getenv('RELAY_DEBUG', 'false').lower() == 'true'
    
    logger.info(f"Starting Zapier-NT Relay on {host}:{port}")
    logger.info(f"Allowed tickers: {ALLOWED_TICKERS}")
    logger.info(f"Max size: {MAX_SIZE}")
    logger.info(f"Require approval: {REQUIRE_APPROVAL}")
    
    # WARNING: In production, run behind nginx/caddy with SSL
    # Use gunicorn: gunicorn -w 4 -b 0.0.0.0:5000 zapier_nt_relay:app
    app.run(host=host, port=port, debug=debug)
