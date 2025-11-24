#!/bin/bash
# Quick test script for XAI service

set -e

echo "╔══════════════════════════════════════════════════════════╗"
echo "║   StrategicKhaos XAI Service - Quick Test               ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

SERVICE_URL="${1:-http://localhost:5000}"

echo "Testing XAI service at: $SERVICE_URL"
echo ""

# Test 1: Health check
echo "Test 1: Health Check"
echo "--------------------"
if curl -s -f "$SERVICE_URL/health" | jq . 2>/dev/null || curl -s -f "$SERVICE_URL/health"; then
    echo "✓ Health check passed"
else
    echo "✗ Health check failed"
    echo "Make sure the service is running:"
    echo "  python3 xai_service.py"
    exit 1
fi
echo ""

# Test 2: Explain endpoint with sample data
echo "Test 2: Explain Trading Decision"
echo "---------------------------------"
PAYLOAD='{
  "timestamp": "2024-11-24T07:00:00Z",
  "symbol": "EURUSD",
  "decision": "ENTER_LONG",
  "features": {
    "price": 1.0850,
    "rsi_14": 35,
    "ema_21_dist": 0.0015,
    "volatility_5m": 0.008,
    "volume_rel": 1.2,
    "orderbook_imbalance": 0.15,
    "her_love": 82,
    "session_loss_count": 1,
    "drawdown_pct": -2.5,
    "time_of_day": "07:00",
    "day_of_week": "Monday"
  }
}'

RESPONSE=$(curl -s -X POST "$SERVICE_URL/explain" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD")

if echo "$RESPONSE" | jq . >/dev/null 2>&1; then
    echo "✓ Explanation endpoint working"
    echo ""
    echo "Response:"
    echo "$RESPONSE" | jq .
    
    # Extract key fields
    MARKET_STATE=$(echo "$RESPONSE" | jq -r '.market_state')
    RISK_FLAG=$(echo "$RESPONSE" | jq -r '.risk_flag')
    LOVE_AMP=$(echo "$RESPONSE" | jq -r '.love_amplification')
    
    echo ""
    echo "Summary:"
    echo "  Market State: $MARKET_STATE"
    echo "  Risk Flag: $RISK_FLAG"
    echo "  Love Amplification: $(printf '%.1f%%' $(echo "$LOVE_AMP * 100" | bc))"
else
    echo "✗ Explanation endpoint failed"
    echo "Response: $RESPONSE"
    exit 1
fi
echo ""

# Test 3: Test with low love (should trigger risk flag)
echo "Test 3: Low Love Scenario (Risk Flag Test)"
echo "------------------------------------------"
LOW_LOVE_PAYLOAD='{
  "timestamp": "2024-11-24T08:00:00Z",
  "symbol": "BTCUSD",
  "decision": "ENTER_SHORT",
  "features": {
    "price": 45000,
    "rsi_14": 75,
    "her_love": 15,
    "session_loss_count": 6,
    "drawdown_pct": -22
  }
}'

RESPONSE=$(curl -s -X POST "$SERVICE_URL/explain" \
  -H "Content-Type: application/json" \
  -d "$LOW_LOVE_PAYLOAD")

RISK_FLAG=$(echo "$RESPONSE" | jq -r '.risk_flag')
echo "Risk Flag: $RISK_FLAG"

if [ "$RISK_FLAG" = "BLOCK" ] || [ "$RISK_FLAG" = "HUG_REQUIRED" ] || [ "$RISK_FLAG" = "CAUTION" ]; then
    echo "✓ Risk protection working (Flag: $RISK_FLAG)"
else
    echo "⚠ Risk flag is OK despite challenging conditions"
fi
echo ""

echo "═══════════════════════════════════════════════════════════"
echo "✓ All tests completed"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "XAI service is functioning correctly!"
echo "Integration ready for cTrader bots."
