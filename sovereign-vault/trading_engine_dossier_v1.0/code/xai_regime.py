"""
XAI Regime Detection Layer
Strategickhaos Trading Engine v1.0
Patent Pending - CONFIDENTIAL

This module implements the Explainable AI (XAI) regime detection layer,
providing interpretable market regime classification with SHAP-based
feature attribution.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import IntEnum
import numpy as np
from datetime import datetime
import hashlib
import json


class MarketRegime(IntEnum):
    """
    Canonical market regime classifications.
    
    Each regime has distinct characteristics requiring different
    trading strategies and risk parameters.
    """
    BULL = 1        # Trending up, low volatility
    BEAR = 2        # Trending down, low volatility
    HIGH_VOL = 3    # Directionless, high variance
    LOW_LIQ = 4     # Wide spreads, thin order books
    CRISIS = 5      # Correlation breakdown, tail events


class ExplanationDepth(IntEnum):
    """
    Explanation verbosity levels based on regime uncertainty.
    
    Higher uncertainty warrants more detailed explanations to
    support human oversight.
    """
    BRIEF = 1       # H(ρ) < 0.3 - High confidence
    STANDARD = 2    # 0.3 ≤ H(ρ) < 0.7 - Moderate confidence
    DETAILED = 3    # H(ρ) ≥ 0.7 - Low confidence


@dataclass
class MarketObservation:
    """
    Multi-dimensional market observation for regime detection.
    
    Features capture returns, volatility, liquidity, and cross-asset dynamics.
    """
    timestamp: datetime
    
    # Return features
    return_1d: float
    return_5d: float
    return_21d: float
    
    # Volatility features
    realized_vol_1d: float
    realized_vol_5d: float
    realized_vol_21d: float
    
    # Liquidity features
    bid_ask_spread_pct: float
    order_book_imbalance: float
    
    # Cross-asset features
    correlation_avg: float
    correlation_dispersion: float
    
    def to_vector(self) -> np.ndarray:
        """Convert to feature vector."""
        return np.array([
            self.return_1d,
            self.return_5d,
            self.return_21d,
            self.realized_vol_1d,
            self.realized_vol_5d,
            self.realized_vol_21d,
            self.bid_ask_spread_pct,
            self.order_book_imbalance,
            self.correlation_avg,
            self.correlation_dispersion
        ])


@dataclass
class RegimeParameters:
    """
    HMM parameters for a single regime.
    
    Emission distribution is multivariate Gaussian.
    """
    mu: np.ndarray      # Mean vector
    sigma: np.ndarray   # Covariance matrix


@dataclass
class XAIDecision:
    """
    Complete explainable trading decision output.
    
    Includes regime classification, target allocation, explanations,
    and cryptographic signature for audit trail.
    """
    timestamp: datetime
    regime: MarketRegime
    regime_confidence: float
    regime_probabilities: Dict[int, float]
    target_allocation: Dict[str, float]
    shap_values: Dict[str, Dict[str, float]]
    explanation_text: str
    explanation_depth: ExplanationDepth
    supporting_evidence: List[str]
    hash: str
    signature: Optional[str] = None


class HiddenMarkovModel:
    """
    Hidden Markov Model for regime detection.
    
    Implements forward-backward algorithm for computing regime posteriors
    given observation sequences.
    """
    
    def __init__(
        self,
        n_regimes: int,
        n_features: int,
        transition_matrix: Optional[np.ndarray] = None,
        regime_params: Optional[Dict[int, RegimeParameters]] = None
    ):
        """
        Initialize HMM.
        
        Args:
            n_regimes: Number of market regimes
            n_features: Dimension of observation vector
            transition_matrix: State transition probabilities A[i,j] = P(ρ_t=j|ρ_{t-1}=i)
            regime_params: Emission distribution parameters per regime
        """
        self.n_regimes = n_regimes
        self.n_features = n_features
        
        # Default: slightly sticky regimes
        if transition_matrix is None:
            self.A = np.full((n_regimes, n_regimes), 0.05)
            np.fill_diagonal(self.A, 0.80)
            self.A = self.A / self.A.sum(axis=1, keepdims=True)
        else:
            self.A = transition_matrix
        
        # Initialize regime parameters if not provided
        if regime_params is None:
            self.regime_params = self._init_default_params()
        else:
            self.regime_params = regime_params
        
        # Initial state distribution (uniform)
        self.pi = np.ones(n_regimes) / n_regimes
    
    def _init_default_params(self) -> Dict[int, RegimeParameters]:
        """Initialize default emission parameters for each regime."""
        params = {}
        
        # Bull regime: positive returns, low vol
        params[MarketRegime.BULL] = RegimeParameters(
            mu=np.array([0.02, 0.05, 0.10, 0.01, 0.01, 0.01, 
                        0.001, 0.1, 0.5, 0.1]),
            sigma=np.eye(self.n_features) * 0.01
        )
        
        # Bear regime: negative returns, low vol
        params[MarketRegime.BEAR] = RegimeParameters(
            mu=np.array([-0.02, -0.05, -0.10, 0.015, 0.015, 0.015,
                        0.002, -0.1, 0.6, 0.15]),
            sigma=np.eye(self.n_features) * 0.01
        )
        
        # High volatility: mixed returns, high vol
        params[MarketRegime.HIGH_VOL] = RegimeParameters(
            mu=np.array([0.0, 0.0, 0.0, 0.04, 0.04, 0.04,
                        0.003, 0.0, 0.3, 0.3]),
            sigma=np.eye(self.n_features) * 0.02
        )
        
        # Low liquidity: normal returns, wide spreads
        params[MarketRegime.LOW_LIQ] = RegimeParameters(
            mu=np.array([0.0, 0.0, 0.0, 0.02, 0.02, 0.02,
                        0.01, 0.0, 0.5, 0.2]),
            sigma=np.eye(self.n_features) * 0.015
        )
        
        # Crisis: large negative returns, high vol, correlation spike
        params[MarketRegime.CRISIS] = RegimeParameters(
            mu=np.array([-0.05, -0.15, -0.30, 0.08, 0.08, 0.08,
                        0.02, -0.3, 0.9, 0.05]),
            sigma=np.eye(self.n_features) * 0.03
        )
        
        return params
    
    def _emission_prob(
        self, 
        observation: np.ndarray, 
        regime: int
    ) -> float:
        """
        Compute emission probability P(o_t | ρ_t = regime).
        
        Uses multivariate Gaussian distribution.
        """
        params = self.regime_params[regime]
        diff = observation - params.mu
        
        # Log probability for numerical stability
        log_det = np.log(np.linalg.det(params.sigma) + 1e-10)
        inv_sigma = np.linalg.inv(params.sigma + np.eye(self.n_features) * 1e-6)
        quad_form = diff @ inv_sigma @ diff
        
        log_prob = -0.5 * (
            self.n_features * np.log(2 * np.pi) + 
            log_det + 
            quad_form
        )
        
        return np.exp(np.clip(log_prob, -700, 700))
    
    def forward(
        self, 
        observations: List[np.ndarray]
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Forward algorithm: compute α_t(i) = P(o_1:t, ρ_t=i).
        
        Returns:
            alpha: Forward probabilities [T x n_regimes]
            scale: Scaling factors [T]
        """
        T = len(observations)
        alpha = np.zeros((T, self.n_regimes))
        scale = np.zeros(T)
        
        # Initialize
        for i in range(self.n_regimes):
            alpha[0, i] = self.pi[i] * self._emission_prob(observations[0], i+1)
        
        # Scale to prevent underflow
        scale[0] = alpha[0].sum()
        alpha[0] /= scale[0] + 1e-10
        
        # Recurse
        for t in range(1, T):
            for j in range(self.n_regimes):
                alpha[t, j] = sum(
                    alpha[t-1, i] * self.A[i, j]
                    for i in range(self.n_regimes)
                ) * self._emission_prob(observations[t], j+1)
            
            scale[t] = alpha[t].sum()
            alpha[t] /= scale[t] + 1e-10
        
        return alpha, scale
    
    def backward(
        self, 
        observations: List[np.ndarray],
        scale: np.ndarray
    ) -> np.ndarray:
        """
        Backward algorithm: compute β_t(i) = P(o_{t+1}:T | ρ_t=i).
        
        Returns:
            beta: Backward probabilities [T x n_regimes]
        """
        T = len(observations)
        beta = np.zeros((T, self.n_regimes))
        
        # Initialize
        beta[T-1] = 1.0
        
        # Recurse backwards
        for t in range(T-2, -1, -1):
            for i in range(self.n_regimes):
                beta[t, i] = sum(
                    self.A[i, j] * 
                    self._emission_prob(observations[t+1], j+1) *
                    beta[t+1, j]
                    for j in range(self.n_regimes)
                ) / (scale[t+1] + 1e-10)
        
        return beta
    
    def posterior(
        self, 
        observations: List[np.ndarray]
    ) -> np.ndarray:
        """
        Compute regime posterior P(ρ_t | o_1:T) via forward-backward.
        
        Returns:
            gamma: Posterior probabilities [T x n_regimes]
        """
        alpha, scale = self.forward(observations)
        beta = self.backward(observations, scale)
        
        # Compute γ_t(i) = P(ρ_t=i | o_1:T)
        gamma = alpha * beta
        gamma /= gamma.sum(axis=1, keepdims=True) + 1e-10
        
        return gamma
    
    def detect_regime(
        self, 
        observations: List[np.ndarray]
    ) -> Tuple[int, float, Dict[int, float]]:
        """
        Detect current regime from observation sequence.
        
        Returns:
            regime: Most likely regime (1-5)
            confidence: Probability of most likely regime
            probabilities: Full regime distribution
        """
        gamma = self.posterior(observations)
        
        # Get final timestep probabilities
        probs = gamma[-1]
        
        # Convert to regime dictionary
        probabilities = {
            i+1: float(p) for i, p in enumerate(probs)
        }
        
        # Most likely regime
        regime = int(np.argmax(probs) + 1)
        confidence = float(probs[regime - 1])
        
        return regime, confidence, probabilities


class SHAPExplainer:
    """
    SHAP (SHapley Additive exPlanations) for regime detection.
    
    Computes feature attributions explaining why a particular regime
    was detected.
    """
    
    def __init__(self, feature_names: List[str]):
        self.feature_names = feature_names
    
    def explain(
        self,
        observation: np.ndarray,
        regime: int,
        regime_params: Dict[int, RegimeParameters]
    ) -> Dict[str, float]:
        """
        Compute approximate SHAP values for regime detection.
        
        Uses simplified approach based on feature contribution to
        likelihood ratio vs. baseline regime.
        
        Returns:
            shap_values: Feature name -> attribution value
        """
        params = regime_params[regime]
        baseline = np.zeros(len(observation))  # Neutral baseline
        
        # Compute contribution of each feature
        diff = observation - params.mu
        inv_sigma = np.linalg.inv(
            params.sigma + np.eye(len(observation)) * 1e-6
        )
        
        # Marginal contribution approximation
        contributions = -0.5 * diff * (inv_sigma @ diff)
        
        # Normalize to sum to 1
        contributions = contributions / (np.abs(contributions).sum() + 1e-10)
        
        return {
            name: float(contrib) 
            for name, contrib in zip(self.feature_names, contributions)
        }


class XAIRegimeLayer:
    """
    Explainable AI Regime Detection Layer.
    
    Provides interpretable market regime classification with:
    - HMM-based regime detection
    - SHAP feature attribution
    - Regime-adaptive explanation depth
    - Cryptographic audit signatures
    """
    
    FEATURE_NAMES = [
        'return_1d', 'return_5d', 'return_21d',
        'vol_1d', 'vol_5d', 'vol_21d',
        'spread_pct', 'book_imbalance',
        'corr_avg', 'corr_dispersion'
    ]
    
    def __init__(
        self,
        assets: List[str],
        lookback: int = 20,
        allocation_model: Optional[callable] = None
    ):
        """
        Initialize XAI regime layer.
        
        Args:
            assets: List of tradeable assets
            lookback: Number of observations for regime detection
            allocation_model: Optional custom allocation model
        """
        self.assets = assets
        self.lookback = lookback
        self.allocation_model = allocation_model or self._default_allocation
        
        # Initialize components
        self.hmm = HiddenMarkovModel(
            n_regimes=5,
            n_features=len(self.FEATURE_NAMES)
        )
        self.explainer = SHAPExplainer(self.FEATURE_NAMES)
        
        # Observation buffer
        self.observations: List[np.ndarray] = []
    
    def _default_allocation(
        self,
        regime: int,
        confidence: float,
        assets: List[str]
    ) -> Dict[str, float]:
        """
        Default regime-based allocation strategy.
        
        Risk-off in Crisis/Bear, risk-on in Bull.
        """
        n = len(assets)
        
        # Base allocation (equally weighted risky assets + stable)
        if regime == MarketRegime.BULL:
            # Aggressive: 80% risky, 20% stable
            risky_weight = 0.80 / (n - 1) if n > 1 else 0.8
            alloc = {a: risky_weight for a in assets if 'STABLE' not in a.upper()}
            stable_weight = 0.20
        elif regime == MarketRegime.BEAR:
            # Conservative: 40% risky, 60% stable
            risky_weight = 0.40 / (n - 1) if n > 1 else 0.4
            alloc = {a: risky_weight for a in assets if 'STABLE' not in a.upper()}
            stable_weight = 0.60
        elif regime == MarketRegime.HIGH_VOL:
            # Moderate: 60% risky, 40% stable
            risky_weight = 0.60 / (n - 1) if n > 1 else 0.6
            alloc = {a: risky_weight for a in assets if 'STABLE' not in a.upper()}
            stable_weight = 0.40
        elif regime == MarketRegime.LOW_LIQ:
            # Conservative: 50% risky, 50% stable
            risky_weight = 0.50 / (n - 1) if n > 1 else 0.5
            alloc = {a: risky_weight for a in assets if 'STABLE' not in a.upper()}
            stable_weight = 0.50
        else:  # CRISIS
            # Very conservative: 20% risky, 80% stable
            risky_weight = 0.20 / (n - 1) if n > 1 else 0.2
            alloc = {a: risky_weight for a in assets if 'STABLE' not in a.upper()}
            stable_weight = 0.80
        
        # Assign stable weight
        for a in assets:
            if 'STABLE' in a.upper():
                alloc[a] = stable_weight
        
        # Normalize
        total = sum(alloc.values())
        return {a: w/total for a, w in alloc.items()}
    
    def _compute_entropy(self, probabilities: Dict[int, float]) -> float:
        """Compute regime probability entropy H(ρ)."""
        probs = np.array(list(probabilities.values()))
        probs = probs[probs > 0]
        return -np.sum(probs * np.log(probs))
    
    def _determine_explanation_depth(
        self, 
        entropy: float
    ) -> ExplanationDepth:
        """
        Determine explanation verbosity based on regime uncertainty.
        
        Higher entropy -> more detailed explanations needed.
        """
        # Max entropy for 5 regimes is log(5) ≈ 1.61
        normalized_entropy = entropy / np.log(5)
        
        if normalized_entropy < 0.3:
            return ExplanationDepth.BRIEF
        elif normalized_entropy < 0.7:
            return ExplanationDepth.STANDARD
        else:
            return ExplanationDepth.DETAILED
    
    def _generate_explanation(
        self,
        regime: int,
        confidence: float,
        depth: ExplanationDepth,
        shap_values: Dict[str, float]
    ) -> Tuple[str, List[str]]:
        """Generate human-readable explanation."""
        regime_names = {
            1: "Bull Market",
            2: "Bear Market",
            3: "High Volatility",
            4: "Low Liquidity",
            5: "Crisis"
        }
        
        # Sort features by absolute SHAP value
        sorted_features = sorted(
            shap_values.items(), 
            key=lambda x: abs(x[1]), 
            reverse=True
        )
        
        top_features = sorted_features[:3]
        
        evidence = [
            f"{feat}: contribution={val:.3f}"
            for feat, val in top_features
        ]
        
        if depth == ExplanationDepth.BRIEF:
            text = f"Detected {regime_names[regime]} (conf: {confidence:.2f})"
        elif depth == ExplanationDepth.STANDARD:
            text = (
                f"Detected {regime_names[regime]} with {confidence:.1%} confidence. "
                f"Primary drivers: {', '.join(f[0] for f in top_features[:2])}."
            )
        else:  # DETAILED
            text = (
                f"Detected {regime_names[regime]} regime with {confidence:.1%} confidence. "
                f"This classification was primarily driven by: "
                f"{top_features[0][0]} (contribution: {top_features[0][1]:.3f}), "
                f"{top_features[1][0]} (contribution: {top_features[1][1]:.3f}), and "
                f"{top_features[2][0]} (contribution: {top_features[2][1]:.3f}). "
                f"Recommend reviewing allocation given elevated uncertainty."
            )
        
        return text, evidence
    
    def update(self, observation: MarketObservation) -> None:
        """Add new market observation to buffer."""
        self.observations.append(observation.to_vector())
        if len(self.observations) > self.lookback:
            self.observations.pop(0)
    
    def detect(self) -> XAIDecision:
        """
        Detect current regime and generate explainable decision.
        
        Returns:
            XAIDecision with regime, allocation, and explanations
        """
        if len(self.observations) < 2:
            raise ValueError("Need at least 2 observations for detection")
        
        # Detect regime
        regime, confidence, probabilities = self.hmm.detect_regime(
            self.observations
        )
        
        # Compute entropy and explanation depth
        entropy = self._compute_entropy(probabilities)
        depth = self._determine_explanation_depth(entropy)
        
        # Compute SHAP values
        current_obs = self.observations[-1]
        shap_values = self.explainer.explain(
            current_obs, 
            regime, 
            self.hmm.regime_params
        )
        
        # Generate target allocation
        allocation = self.allocation_model(regime, confidence, self.assets)
        
        # Generate explanation
        explanation_text, evidence = self._generate_explanation(
            regime, confidence, depth, shap_values
        )
        
        # Create decision
        timestamp = datetime.utcnow()
        
        decision = XAIDecision(
            timestamp=timestamp,
            regime=MarketRegime(regime),
            regime_confidence=confidence,
            regime_probabilities=probabilities,
            target_allocation=allocation,
            shap_values={a: shap_values for a in self.assets},
            explanation_text=explanation_text,
            explanation_depth=depth,
            supporting_evidence=evidence,
            hash=""
        )
        
        # Compute hash
        payload = {
            'timestamp': timestamp.isoformat(),
            'regime': regime,
            'confidence': confidence,
            'allocation': allocation,
            'explanation': explanation_text
        }
        decision.hash = hashlib.sha256(
            json.dumps(payload, sort_keys=True).encode()
        ).hexdigest()
        
        return decision


if __name__ == '__main__':
    # Demo usage
    assets = ['BTC', 'ETH', 'SOL', 'AVAX', 'STABLE']
    xai = XAIRegimeLayer(assets=assets)
    
    # Generate sample observations
    for i in range(25):
        obs = MarketObservation(
            timestamp=datetime.utcnow(),
            return_1d=np.random.normal(0.01, 0.02),
            return_5d=np.random.normal(0.03, 0.04),
            return_21d=np.random.normal(0.08, 0.08),
            realized_vol_1d=np.random.uniform(0.01, 0.03),
            realized_vol_5d=np.random.uniform(0.01, 0.03),
            realized_vol_21d=np.random.uniform(0.01, 0.03),
            bid_ask_spread_pct=np.random.uniform(0.001, 0.005),
            order_book_imbalance=np.random.uniform(-0.2, 0.2),
            correlation_avg=np.random.uniform(0.3, 0.7),
            correlation_dispersion=np.random.uniform(0.05, 0.2)
        )
        xai.update(obs)
    
    # Detect regime
    decision = xai.detect()
    
    print(f"Regime: {decision.regime.name}")
    print(f"Confidence: {decision.regime_confidence:.2%}")
    print(f"Explanation Depth: {decision.explanation_depth.name}")
    print(f"\nExplanation: {decision.explanation_text}")
    print(f"\nTarget Allocation:")
    for asset, weight in decision.target_allocation.items():
        print(f"  {asset}: {weight:.2%}")
    print(f"\nDecision Hash: {decision.hash[:16]}...")
