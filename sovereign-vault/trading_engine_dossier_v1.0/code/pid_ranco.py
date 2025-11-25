"""
PID-RANCO Controller Reference Implementation
Strategickhaos Trading Engine v1.0
Patent Pending - CONFIDENTIAL

This module implements the PID-RANCO (Proportional-Integral-Derivative with
Range-Normalized Constrained Optimization) controller for adaptive portfolio
management.
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
import numpy as np
from scipy.optimize import minimize
import hashlib
import json
from datetime import datetime


@dataclass
class PortfolioState:
    """Current portfolio allocation state."""
    timestamp: datetime
    allocations: Dict[str, float]  # asset -> weight
    nav: float  # Net Asset Value
    
    def to_vector(self, assets: List[str]) -> np.ndarray:
        """Convert to numpy vector for computation."""
        return np.array([self.allocations.get(a, 0.0) for a in assets])


@dataclass
class TargetAllocation:
    """Target allocation from XAI layer."""
    timestamp: datetime
    allocations: Dict[str, float]
    regime: int
    regime_confidence: float
    explanation: str
    
    def to_vector(self, assets: List[str]) -> np.ndarray:
        """Convert to numpy vector for computation."""
        return np.array([self.allocations.get(a, 0.0) for a in assets])


@dataclass
class PIDGains:
    """PID controller gain matrices."""
    Kp: np.ndarray  # Proportional gain
    Ki: np.ndarray  # Integral gain
    Kd: np.ndarray  # Derivative gain


@dataclass
class RANCOConstraints:
    """RANCO optimization constraints."""
    max_allocation: float = 0.30  # Max per-asset allocation
    min_allocation: float = 0.00  # Min (no shorting)
    max_risk: float = 0.20  # Max portfolio risk budget
    risk_coefficients: Optional[np.ndarray] = None


class RangeNormalizer:
    """
    Range normalization operator for bounded control signals.
    
    Maintains rolling window of signal history to compute adaptive bounds.
    """
    
    def __init__(self, window_size: int = 100, epsilon: float = 1e-8):
        self.window_size = window_size
        self.epsilon = epsilon
        self.history: List[np.ndarray] = []
    
    def update(self, signal: np.ndarray) -> None:
        """Add signal to history."""
        self.history.append(signal.copy())
        if len(self.history) > self.window_size:
            self.history.pop(0)
    
    def normalize(self, signal: np.ndarray) -> np.ndarray:
        """
        Apply range normalization: R(x) = (x - x_min) / (x_max - x_min + ε)
        """
        if len(self.history) < 2:
            # Not enough history, return clipped signal
            return np.clip(signal, 0, 1)
        
        history_array = np.array(self.history)
        x_min = history_array.min(axis=0)
        x_max = history_array.max(axis=0)
        
        normalized = (signal - x_min) / (x_max - x_min + self.epsilon)
        return np.clip(normalized, 0, 1)


class RANCOOptimizer:
    """
    Range-Normalized Constrained Optimization solver.
    
    Transforms normalized control signals into executable trade orders
    satisfying regulatory and risk constraints.
    """
    
    def __init__(self, constraints: RANCOConstraints):
        self.constraints = constraints
    
    def solve(self, u_normalized: np.ndarray) -> np.ndarray:
        """
        Solve constrained optimization problem:
        
        min ||u - u_normalized||²
        s.t. sum(u) = 1          (allocation constraint)
             u >= 0               (no shorting)
             u <= u_max          (concentration limits)
             r'u <= r_max        (risk budget)
        """
        n = len(u_normalized)
        
        # Objective: minimize squared distance from normalized signal
        def objective(u):
            return np.sum((u - u_normalized) ** 2)
        
        # Gradient for faster optimization
        def gradient(u):
            return 2 * (u - u_normalized)
        
        # Constraints
        constraints = [
            # Sum to 1
            {'type': 'eq', 'fun': lambda u: np.sum(u) - 1.0},
        ]
        
        # Risk budget constraint (if risk coefficients provided)
        if self.constraints.risk_coefficients is not None:
            constraints.append({
                'type': 'ineq',
                'fun': lambda u: self.constraints.max_risk - np.dot(
                    self.constraints.risk_coefficients, u
                )
            })
        
        # Bounds: [min_allocation, max_allocation] for each asset
        bounds = [
            (self.constraints.min_allocation, self.constraints.max_allocation)
            for _ in range(n)
        ]
        
        # Initial guess: normalized signal projected to feasible set
        x0 = u_normalized / (np.sum(u_normalized) + 1e-8)
        x0 = np.clip(x0, self.constraints.min_allocation, 
                     self.constraints.max_allocation)
        
        # Solve
        result = minimize(
            objective,
            x0,
            method='SLSQP',
            jac=gradient,
            bounds=bounds,
            constraints=constraints,
            options={'ftol': 1e-9, 'maxiter': 1000}
        )
        
        if result.success:
            return result.x
        else:
            # Fallback: return equally weighted portfolio
            return np.ones(n) / n


class PIDRANCOController:
    """
    PID-RANCO Controller for adaptive portfolio management.
    
    Combines classical PID control with Range-Normalized Constrained
    Optimization for trading applications.
    
    Features:
    - Adaptive gain scheduling based on market regime
    - Range normalization for numerical stability
    - Constrained optimization for regulatory compliance
    - Complete audit trail with cryptographic signatures
    """
    
    def __init__(
        self,
        assets: List[str],
        regime_gains: Dict[int, PIDGains],
        constraints: RANCOConstraints,
        dt: float = 1.0  # Sampling period in minutes
    ):
        """
        Initialize controller.
        
        Args:
            assets: List of asset symbols
            regime_gains: Dict mapping regime ID to PID gain matrices
            constraints: RANCO optimization constraints
            dt: Sampling period
        """
        self.assets = assets
        self.n_assets = len(assets)
        self.regime_gains = regime_gains
        self.constraints = constraints
        self.dt = dt
        
        # State variables
        self.e_prev = np.zeros(self.n_assets)
        self.e_integral = np.zeros(self.n_assets)
        
        # Normalization and optimization
        self.normalizer = RangeNormalizer()
        self.optimizer = RANCOOptimizer(constraints)
        
        # Audit trail
        self.audit_records: List[Dict] = []
    
    def get_adaptive_gains(
        self, 
        regime_weights: Dict[int, float]
    ) -> PIDGains:
        """
        Compute effective gains as weighted combination of regime-specific gains.
        
        K_eff = Σ_r α_r * K^(r)
        
        where α_r are soft regime membership weights.
        """
        # Initialize with zeros
        n = self.n_assets
        Kp_eff = np.zeros((n, n))
        Ki_eff = np.zeros((n, n))
        Kd_eff = np.zeros((n, n))
        
        # Weighted sum across regimes
        for regime, weight in regime_weights.items():
            if regime in self.regime_gains:
                gains = self.regime_gains[regime]
                Kp_eff += weight * gains.Kp
                Ki_eff += weight * gains.Ki
                Kd_eff += weight * gains.Kd
        
        return PIDGains(Kp=Kp_eff, Ki=Ki_eff, Kd=Kd_eff)
    
    def compute_control(
        self,
        current: PortfolioState,
        target: TargetAllocation,
        regime_weights: Dict[int, float]
    ) -> Tuple[np.ndarray, Dict]:
        """
        Compute optimal control signal (trade orders).
        
        PID law: u_raw = Kp*e + Ki*∫e*dt + Kd*de/dt
        Then normalize and optimize.
        
        Returns:
            u_optimal: Optimal allocation vector
            audit_record: Complete decision provenance
        """
        # Get adaptive gains
        gains = self.get_adaptive_gains(regime_weights)
        
        # Compute error signal
        p = current.to_vector(self.assets)
        p_star = target.to_vector(self.assets)
        e = p_star - p
        
        # PID control law (matrix form)
        e_deriv = (e - self.e_prev) / self.dt
        self.e_integral += e * self.dt
        
        # Raw control signal
        u_raw = (
            gains.Kp @ e +
            gains.Ki @ self.e_integral +
            gains.Kd @ e_deriv
        )
        
        # Range normalization
        self.normalizer.update(u_raw)
        u_norm = self.normalizer.normalize(u_raw)
        
        # Constrained optimization
        u_optimal = self.optimizer.solve(u_norm)
        
        # Update state
        self.e_prev = e.copy()
        
        # Create audit record
        audit_record = self._create_audit_record(
            current, target, e, u_raw, u_norm, u_optimal, regime_weights
        )
        self.audit_records.append(audit_record)
        
        return u_optimal, audit_record
    
    def _create_audit_record(
        self,
        current: PortfolioState,
        target: TargetAllocation,
        error: np.ndarray,
        u_raw: np.ndarray,
        u_norm: np.ndarray,
        u_optimal: np.ndarray,
        regime_weights: Dict[int, float]
    ) -> Dict:
        """Create cryptographically signed audit record."""
        timestamp = datetime.utcnow().isoformat()
        
        payload = {
            'timestamp': timestamp,
            'current_nav': current.nav,
            'current_allocation': {
                a: float(w) for a, w in 
                zip(self.assets, current.to_vector(self.assets))
            },
            'target_allocation': {
                a: float(w) for a, w in 
                zip(self.assets, target.to_vector(self.assets))
            },
            'regime': target.regime,
            'regime_confidence': target.regime_confidence,
            'regime_weights': regime_weights,
            'error_vector': error.tolist(),
            'u_raw': u_raw.tolist(),
            'u_normalized': u_norm.tolist(),
            'u_optimal': u_optimal.tolist(),
            'explanation': target.explanation
        }
        
        # Compute hash
        payload_json = json.dumps(payload, sort_keys=True)
        hash_value = hashlib.sha256(payload_json.encode()).hexdigest()
        
        # Previous hash for chain
        prev_hash = (
            self.audit_records[-1]['hash'] 
            if self.audit_records else '0' * 64
        )
        
        return {
            'payload': payload,
            'hash': hash_value,
            'prev_hash': prev_hash,
            'chain_hash': hashlib.sha256(
                (prev_hash + hash_value).encode()
            ).hexdigest()
        }
    
    def verify_audit_chain(self) -> bool:
        """Verify integrity of audit chain."""
        if not self.audit_records:
            return True
        
        prev_hash = '0' * 64
        for record in self.audit_records:
            # Verify payload hash
            payload_json = json.dumps(record['payload'], sort_keys=True)
            computed_hash = hashlib.sha256(payload_json.encode()).hexdigest()
            if computed_hash != record['hash']:
                return False
            
            # Verify chain link
            if record['prev_hash'] != prev_hash:
                return False
            
            prev_hash = record['hash']
        
        return True
    
    def reset(self):
        """Reset controller state (for new trading session)."""
        self.e_prev = np.zeros(self.n_assets)
        self.e_integral = np.zeros(self.n_assets)
        self.normalizer = RangeNormalizer()


# =============================================================================
# Example Usage and Factory Functions
# =============================================================================

def create_default_gains(n_assets: int) -> Dict[int, PIDGains]:
    """
    Create default PID gains for each market regime.
    
    Regime-specific tuning:
    - Bull (1): Aggressive tracking (high Kp)
    - Bear (2): Conservative, smooth response (high Kd)
    - High Volatility (3): Reduced gains overall
    - Low Liquidity (4): Slow integral action
    - Crisis (5): Maximum smoothing, minimal action
    """
    gains = {}
    
    # Regime 1: Bull Market
    gains[1] = PIDGains(
        Kp=np.eye(n_assets) * 0.8,
        Ki=np.eye(n_assets) * 0.1,
        Kd=np.eye(n_assets) * 0.2
    )
    
    # Regime 2: Bear Market
    gains[2] = PIDGains(
        Kp=np.eye(n_assets) * 0.5,
        Ki=np.eye(n_assets) * 0.05,
        Kd=np.eye(n_assets) * 0.4
    )
    
    # Regime 3: High Volatility
    gains[3] = PIDGains(
        Kp=np.eye(n_assets) * 0.3,
        Ki=np.eye(n_assets) * 0.02,
        Kd=np.eye(n_assets) * 0.3
    )
    
    # Regime 4: Low Liquidity
    gains[4] = PIDGains(
        Kp=np.eye(n_assets) * 0.4,
        Ki=np.eye(n_assets) * 0.01,
        Kd=np.eye(n_assets) * 0.25
    )
    
    # Regime 5: Crisis
    gains[5] = PIDGains(
        Kp=np.eye(n_assets) * 0.2,
        Ki=np.eye(n_assets) * 0.005,
        Kd=np.eye(n_assets) * 0.5
    )
    
    return gains


def create_controller(
    assets: List[str],
    max_allocation: float = 0.30,
    max_risk: float = 0.20
) -> PIDRANCOController:
    """
    Factory function to create PID-RANCO controller with sensible defaults.
    
    Args:
        assets: List of tradeable asset symbols
        max_allocation: Maximum allocation per asset
        max_risk: Maximum portfolio risk budget
    
    Returns:
        Configured PIDRANCOController instance
    """
    n = len(assets)
    
    # Create default regime-specific gains
    regime_gains = create_default_gains(n)
    
    # Create constraints
    constraints = RANCOConstraints(
        max_allocation=max_allocation,
        min_allocation=0.0,
        max_risk=max_risk,
        risk_coefficients=np.ones(n) / n  # Equal risk contribution default
    )
    
    return PIDRANCOController(
        assets=assets,
        regime_gains=regime_gains,
        constraints=constraints,
        dt=1.0  # 1-minute sampling
    )


if __name__ == '__main__':
    # Demo usage
    assets = ['BTC', 'ETH', 'SOL', 'AVAX', 'STABLE']
    controller = create_controller(assets)
    
    # Simulate one control step
    current = PortfolioState(
        timestamp=datetime.utcnow(),
        allocations={'BTC': 0.25, 'ETH': 0.20, 'SOL': 0.15, 
                     'AVAX': 0.10, 'STABLE': 0.30},
        nav=1_000_000.0
    )
    
    target = TargetAllocation(
        timestamp=datetime.utcnow(),
        allocations={'BTC': 0.30, 'ETH': 0.25, 'SOL': 0.15, 
                     'AVAX': 0.10, 'STABLE': 0.20},
        regime=1,  # Bull market
        regime_confidence=0.85,
        explanation="Increasing BTC/ETH allocation due to bullish momentum"
    )
    
    regime_weights = {1: 0.85, 2: 0.10, 3: 0.05}
    
    u_optimal, audit = controller.compute_control(current, target, regime_weights)
    
    print("Optimal Allocation:")
    for asset, weight in zip(assets, u_optimal):
        print(f"  {asset}: {weight:.4f}")
    
    print(f"\nAudit Hash: {audit['hash'][:16]}...")
    print(f"Chain Valid: {controller.verify_audit_chain()}")
