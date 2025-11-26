"""
Grok-5 Trainer

Main training loop with energy-aware scheduling.
"""

import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional, Protocol

try:
    from ..utils.prometheus_exporter import training_step, training_loss, gpu_utilization
except ImportError:
    from utils.prometheus_exporter import training_step, training_loss, gpu_utilization

from .checkpoint_guardian import CheckpointGuardian
from .consensus_protocol import PowerWindowDecision
from .energy_scheduler import EnergyScheduler


class Model(Protocol):
    """Protocol for model interface."""

    def forward(self, batch: Any) -> Any:
        """Forward pass."""
        ...

    def backward(self, loss: Any) -> None:
        """Backward pass."""
        ...

    def state_dict(self) -> dict:
        """Get model state."""
        ...

    def load_state_dict(self, state: dict) -> None:
        """Load model state."""
        ...


class DataLoader(Protocol):
    """Protocol for data loader."""

    def __iter__(self):
        """Iterate over batches."""
        ...


class Optimizer(Protocol):
    """Protocol for optimizer."""

    def step(self) -> None:
        """Optimizer step."""
        ...

    def zero_grad(self) -> None:
        """Zero gradients."""
        ...


@dataclass
class TrainingState:
    """Current training state."""

    step: int
    loss: float
    gpu_util: float
    power_decision: PowerWindowDecision
    timestamp: datetime


class Grok5Trainer:
    """
    Grok-5 distributed trainer with energy-aware scheduling.

    Features:
    - Energy-aware training with power limits
    - Checkpoint consensus across nodes
    - Automatic scaling based on power/battery state
    - Provenance tracking for training data
    """

    def __init__(
        self,
        model: Optional[Model] = None,
        optimizer: Optional[Optimizer] = None,
        energy_scheduler: Optional[EnergyScheduler] = None,
        checkpoint_guardian: Optional[CheckpointGuardian] = None,
        checkpoint_interval: int = 1000,
        max_steps: int = 1000000,
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initialize Grok-5 trainer.

        Args:
            model: Model to train
            optimizer: Optimizer instance
            energy_scheduler: Energy scheduler for power management
            checkpoint_guardian: Checkpoint guardian for state management
            checkpoint_interval: Steps between checkpoints
            max_steps: Maximum training steps
            logger: Logger instance
        """
        self.model = model
        self.optimizer = optimizer
        self.energy = energy_scheduler or EnergyScheduler()
        self.checkpoints = checkpoint_guardian or CheckpointGuardian()
        self.checkpoint_interval = checkpoint_interval
        self.max_steps = max_steps
        self.log = logger or logging.getLogger(__name__)

        self._current_step = 0
        self._running = False

    def train(self, data_loader: DataLoader) -> None:
        """
        Run training loop.

        Args:
            data_loader: Data loader for training batches
        """
        self._running = True
        self.log.info(f"Starting training (max_steps={self.max_steps})")

        for batch in data_loader:
            if not self._running:
                break

            if self._current_step >= self.max_steps:
                break

            # Check energy window
            decision = self.energy.evaluate_window()
            if not decision.allowed:
                self._handle_energy_constraint(decision)
                continue

            # Training step
            loss = self._train_step(batch)

            # Update metrics
            self._update_metrics(loss, decision)

            # Checkpoint if needed
            if self._current_step % self.checkpoint_interval == 0:
                self._create_checkpoint()

            self._current_step += 1

        self.log.info(f"Training complete at step {self._current_step}")

    def _train_step(self, batch: Any) -> float:
        """Execute single training step."""
        if self.model is None or self.optimizer is None:
            # Development mode: simulate training
            import random
            return random.uniform(0.1, 2.0)

        self.optimizer.zero_grad()
        output = self.model.forward(batch)

        # Assuming output contains loss
        loss = output.get("loss", 0.0) if isinstance(output, dict) else 0.0

        self.model.backward(loss)
        self.optimizer.step()

        return float(loss)

    def _handle_energy_constraint(self, decision: PowerWindowDecision) -> None:
        """Handle energy constraint."""
        import time

        self.log.warning(
            f"Energy constraint: {decision.reason} "
            f"(scale={decision.suggested_scale}, delay={decision.delay_seconds}s)"
        )

        # Wait for suggested delay (capped)
        wait_time = min(decision.delay_seconds, 60)
        time.sleep(wait_time)

    def _update_metrics(self, loss: float, decision: PowerWindowDecision) -> None:
        """Update Prometheus metrics."""
        training_step.set(self._current_step)
        training_loss.set(loss)

        # Simulate GPU utilization based on scale factor
        gpu_utilization.set(0.8 * decision.suggested_scale)

    def _create_checkpoint(self) -> None:
        """Create checkpoint with consensus."""
        if self.model is None:
            # Development mode: create dummy checkpoint
            state = {"step": self._current_step}
        else:
            state = self.model.state_dict()

        metadata = self.checkpoints.create_checkpoint(
            step=self._current_step,
            model_state=state,
        )

        if metadata:
            self.log.info(f"Checkpoint created: step={self._current_step}")
        else:
            self.log.warning(f"Checkpoint failed: step={self._current_step}")

    def stop(self) -> None:
        """Stop training."""
        self._running = False
        self.log.info("Training stop requested")

    def resume(self, step: Optional[int] = None) -> bool:
        """
        Resume training from checkpoint.

        Args:
            step: Specific step to resume from, or latest

        Returns:
            True if resume successful
        """
        if step is None:
            metadata = self.checkpoints.get_latest_checkpoint()
            if metadata is None:
                self.log.warning("No checkpoint found to resume from")
                return False
            step = metadata.step

        data = self.checkpoints.load_checkpoint(step)
        if data is None:
            self.log.error(f"Failed to load checkpoint for step {step}")
            return False

        if self.model is not None:
            import pickle
            state = pickle.loads(data)
            self.model.load_state_dict(state)

        self._current_step = step
        self.log.info(f"Resumed from checkpoint: step={step}")
        return True

    @property
    def current_step(self) -> int:
        """Get current training step."""
        return self._current_step

    def get_state(self) -> TrainingState:
        """
        Get current training state.

        Returns:
            TrainingState with current metrics
        """
        decision = self.energy.evaluate_window()
        return TrainingState(
            step=self._current_step,
            loss=0.0,  # Would be from actual training
            gpu_util=0.8 * decision.suggested_scale,
            power_decision=decision,
            timestamp=datetime.utcnow(),
        )
