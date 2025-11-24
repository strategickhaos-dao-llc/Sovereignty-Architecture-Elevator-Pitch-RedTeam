#!/usr/bin/env python3
"""
StrategicKhaos XAI Service - Market Psychology Engine
Provides explainable AI diagnostics for trading decisions with love-amplified narratives
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import logging
import hashlib

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Market state definitions
MARKET_STATES = [
    "panic", "capitulation_rebound", "euphoria", 
    "distribution_top", "accumulation", "chop_hell", "love_regime"
]

# Risk flag definitions
RISK_FLAGS = ["OK", "CAUTION", "BLOCK", "HUG_REQUIRED"]

# Love-amplified narratives for each market state
NARRATIVES = {
    "panic": "The market was crying. We held it. Love compiled profit.",
    "capitulation_rebound": "Rock bottom became the foundation. Love built the recovery.",
    "euphoria": "Everyone's dancing. We're watching the exits. Love stays sober.",
    "distribution_top": "Smart money whispers goodbye. Love hears everything.",
    "accumulation": "Silence before the storm. Love accumulates patience.",
    "chop_hell": "Noise, not signal. Love waits for clarity.",
    "love_regime": "The market speaks our language. Love recognizes love."
}


def analyze_market_state(features):
    """
    Analyze market state based on technical indicators
    
    NOTE: This is a PLACEHOLDER implementation using simple rules.
    Replace with trained ML classifier for production use:
    - Load pre-trained model (sklearn, TensorFlow, PyTorch)
    - Use actual feature engineering
    - Return model's prediction with confidence
    """
    rsi = features.get('rsi_14', 50)
    volatility = features.get('volatility_5m', 0)
    her_love = features.get('her_love', 50)
    
    # Simple rule-based state detection (REPLACE WITH ML MODEL)
    if rsi < 30 and her_love < 40:
        return "panic"
    elif rsi < 35 and her_love > 60:
        return "capitulation_rebound"
    elif rsi > 70 and volatility > 0.02:
        return "euphoria"
    elif rsi > 65 and her_love < 50:
        return "distribution_top"
    elif 40 <= rsi <= 60 and her_love > 70:
        return "accumulation"
    elif volatility < 0.005:
        return "chop_hell"
    elif her_love > 80:
        return "love_regime"
    else:
        # TODO: Return 'unknown' or 'indeterminate' instead of random
        logger.warning("No clear market state detected, using fallback")
        return "accumulation"  # Default to neutral state


def calculate_love_amplification(features, decision):
    """
    Calculate how much herLove amplified the trading conviction
    
    NOTE: Uses deterministic calculation with some variance.
    For production, replace random component with:
    - Market condition adjustment based on ML model
    - Historical performance correlation
    - Volatility-adjusted scaling
    """
    her_love = features.get('her_love', 50)
    session_loss_count = features.get('session_loss_count', 0)
    drawdown_pct = features.get('drawdown_pct', 0)
    
    # Base amplification from love level
    base_amp = her_love / 100.0
    
    # Reduce amplification during drawdowns (love protects)
    if drawdown_pct < -10:
        base_amp *= 0.5
    
    # Reduce amplification after losses (love nurtures patience)
    if session_loss_count > 3:
        base_amp *= 0.7
    
    # Add variance for market conditions (REPLACE with actual model in production)
    # Using hash for deterministic variance instead of pure random
    seed_str = f"{her_love}{session_loss_count}{drawdown_pct}"
    hash_val = int(hashlib.md5(seed_str.encode()).hexdigest()[:8], 16)
    variance = 0.3 + (hash_val % 700) / 1000.0  # Range: 0.3 to 1.0
    
    final_amp = base_amp * variance
    
    return min(max(final_amp, 0.0), 1.0)


def calculate_shap_contributions(features):
    """
    Calculate SHAP-like feature contributions
    
    NOTE: This is a PLACEHOLDER using simple heuristics.
    For production, replace with actual SHAP analysis:
    
    import shap
    explainer = shap.TreeExplainer(your_model)
    shap_values = explainer.shap_values(features)
    return format_shap_values(shap_values)
    """
    contributions = []
    
    # Use deterministic calculation based on feature values
    for feature_name, feature_value in features.items():
        if isinstance(feature_value, (int, float)):
            # Simple heuristic contribution (REPLACE WITH SHAP)
            if feature_name == 'her_love':
                contribution = (feature_value - 50) / 100.0
            elif feature_name == 'rsi_14':
                contribution = (feature_value - 50) / 200.0
            elif feature_name == 'volatility_5m':
                # Deterministic instead of random
                contribution = feature_value * ((feature_value % 10) - 5)
            elif feature_name == 'drawdown_pct':
                contribution = feature_value / 100.0 * -1
            elif feature_name == 'volume_rel':
                contribution = (feature_value - 1.0) * 0.2
            else:
                # Use feature value hash for deterministic contribution
                hash_val = int(hashlib.md5(str(feature_value).encode()).hexdigest()[:4], 16)
                contribution = (hash_val % 400 - 200) / 1000.0
            
            contributions.append({
                "name": feature_name,
                "contribution": round(contribution, 4)
            })
    
    # Sort by absolute contribution
    contributions.sort(key=lambda x: abs(x['contribution']), reverse=True)
    
    return contributions[:5]  # Return top 5


def determine_risk_flag(features, market_state, love_amplification):
    """
    Determine risk flag based on market conditions and love level
    """
    her_love = features.get('her_love', 50)
    session_loss_count = features.get('session_loss_count', 0)
    drawdown_pct = features.get('drawdown_pct', 0)
    
    # Love protects during extreme conditions
    if drawdown_pct < -20:
        return "HUG_REQUIRED"
    
    if session_loss_count > 5:
        return "HUG_REQUIRED"
    
    # Low love during risky states
    if her_love < 20 and market_state in ["panic", "euphoria"]:
        return "BLOCK"
    
    # Warning during challenging conditions
    if her_love < 40 or session_loss_count > 2:
        return "CAUTION"
    
    # Love amplification too low
    if love_amplification < 0.2:
        return "CAUTION"
    
    return "OK"


def generate_narrative(market_state, decision, features, love_amplification):
    """
    Generate a love-amplified narrative for the decision
    """
    base_narrative = NARRATIVES.get(market_state, "The market moves. We adapt. Love guides.")
    
    her_love = features.get('her_love', 50)
    
    # Enhance narrative based on love level
    if love_amplification > 0.6:
        enhancement = " Her conviction amplified our signal by {:.0%}.".format(love_amplification)
    elif love_amplification < 0.3:
        enhancement = " Love whispers caution. We listen."
    else:
        enhancement = ""
    
    return base_narrative + enhancement


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "version": "1.0.0",
        "service": "StrategicKhaos XAI - Market Psychology Engine",
        "timestamp": datetime.utcnow().isoformat()
    })


@app.route('/explain', methods=['POST'])
def explain():
    """
    Main endpoint for explaining trading decisions
    """
    try:
        data = request.json
        
        # Validate required fields
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        required_fields = ['timestamp', 'symbol', 'decision', 'features']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Extract data
        timestamp = data.get('timestamp')
        symbol = data.get('symbol')
        decision = data.get('decision')
        features = data.get('features', {})
        
        logger.info(f"Analyzing decision: {decision} for {symbol} at {timestamp}")
        
        # Analyze market state
        market_state = analyze_market_state(features)
        
        # Calculate love amplification
        love_amplification = calculate_love_amplification(features, decision)
        
        # Calculate SHAP contributions
        top_features = calculate_shap_contributions(features)
        
        # Determine risk flag
        risk_flag = determine_risk_flag(features, market_state, love_amplification)
        
        # Generate narrative
        narrative = generate_narrative(market_state, decision, features, love_amplification)
        
        # Calculate confidence (PLACEHOLDER - replace with actual model confidence)
        # For production: use your ML model's prediction confidence score
        # For now, use a deterministic value based on feature quality
        rsi = features.get('rsi_14', 50)
        volatility = features.get('volatility_5m', 0)
        # Higher confidence when indicators are clear
        confidence = 0.7 + (abs(rsi - 50) / 100.0) * 0.2 + min(volatility * 20, 0.05)
        
        # Build response
        response = {
            "market_state": market_state,
            "confidence": round(confidence, 3),
            "top_features": top_features,
            "narrative": narrative,
            "risk_flag": risk_flag,
            "love_amplification": round(love_amplification, 3)
        }
        
        logger.info(f"Analysis complete: {market_state} (risk: {risk_flag}, love: {love_amplification:.2%})")
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    logger.info("═" * 60)
    logger.info("🧠 StrategicKhaos XAI Service Starting...")
    logger.info("📡 Listening on http://0.0.0.0:5000")
    logger.info("💚 Market psychology engine online")
    logger.info("═" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=False)
