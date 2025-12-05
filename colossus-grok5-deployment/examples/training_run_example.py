#!/usr/bin/env python3
"""
Training Run Example

Demonstrates how to run Grok-5 training with energy-aware scheduling
and checkpoint consensus.

Artifact #3558 - Colossus Grok-5 Deployment Suite
"""

import logging
import sys
import os
import time
from typing import Iterator

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from training.grok5_trainer import Grok5Trainer
from training.energy_scheduler import EnergyScheduler
from training.checkpoint_guardian import CheckpointGuardian


class MockPowerClient:
    """Mock power client for demonstration."""

    def __init__(self, base_power: float = 200.0):
        self.base_power = base_power
        self._step = 0

    def current_mw(self) -> float:
        # Simulate power fluctuation
        import random
        fluctuation = random.uniform(-20, 20)
        self._step += 1
        return self.base_power + fluctuation


class MockMegapackClient:
    """Mock Megapack client for demonstration."""

    def __init__(self, base_soc: float = 0.75):
        self.base_soc = base_soc

    def current_soc(self) -> float:
        # Simulate SoC fluctuation
        import random
        fluctuation = random.uniform(-0.05, 0.05)
        return min(1.0, max(0.0, self.base_soc + fluctuation))


class MockDataLoader:
    """Mock data loader for demonstration."""

    def __init__(self, num_batches: int = 10):
        self.num_batches = num_batches

    def __iter__(self) -> Iterator[dict]:
        for i in range(self.num_batches):
            yield {
                "batch_id": i,
                "data": f"batch_{i}",
                "size": 4096,
            }


def main():
    """Run the training example."""
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logger = logging.getLogger("training_example")

    print("=" * 60)
    print("Training Run Example - Colossus Grok-5")
    print("=" * 60)
    print()

    # Create mock clients
    power_client = MockPowerClient(base_power=180.0)
    megapack_client = MockMegapackClient(base_soc=0.8)

    # Create energy scheduler
    energy_scheduler = EnergyScheduler(
        power_client=power_client,
        megapack_client=megapack_client,
        power_limit_mw=250.0,
        soc_min=0.4,
        logger=logger,
    )

    # Create checkpoint guardian
    import tempfile
    checkpoint_dir = tempfile.mkdtemp()
    checkpoint_guardian = CheckpointGuardian(
        checkpoint_dir=checkpoint_dir,
        logger=logger,
    )

    # Register some nodes for consensus
    for i in range(10):
        checkpoint_guardian.consensus.register_node(f"node-{i}")

    # Create trainer
    trainer = Grok5Trainer(
        energy_scheduler=energy_scheduler,
        checkpoint_guardian=checkpoint_guardian,
        checkpoint_interval=5,  # Checkpoint every 5 steps for demo
        max_steps=10,
        logger=logger,
    )

    # Check initial energy status
    print("Initial Energy Status:")
    status = energy_scheduler.get_status()
    print(f"  Power: {status.power_mw:.1f} MW")
    print(f"  SoC: {status.soc:.2%}")
    print(f"  Off-peak: {status.in_offpeak}")
    print()

    # Check energy window
    print("Evaluating energy window...")
    decision = energy_scheduler.evaluate_window()
    print(f"  Allowed: {decision.allowed}")
    print(f"  Reason: {decision.reason}")
    print(f"  Suggested scale: {decision.suggested_scale:.1%}")
    print()

    if not decision.allowed:
        print(f"Training blocked: {decision.reason}")
        print(f"Would need to wait {decision.delay_seconds}s")
        return

    # Create mock data loader
    data_loader = MockDataLoader(num_batches=10)

    # Run training
    print("Starting training loop...")
    print("-" * 60)

    trainer.train(data_loader)

    print("-" * 60)
    print()

    # Show training state
    state = trainer.get_state()
    print("Final Training State:")
    print(f"  Step: {state.step}")
    print(f"  GPU Utilization: {state.gpu_util:.1%}")
    print()

    # Show checkpoints
    checkpoints = checkpoint_guardian.list_checkpoints()
    print(f"Created {len(checkpoints)} checkpoints:")
    for cp in checkpoints:
        consensus_str = f"{cp.consensus.fraction:.1%}" if cp.consensus else "N/A"
        print(f"  Step {cp.step}: hash={cp.hash[:16]}... consensus={consensus_str}")
    print()

    # Show final consensus
    consensus_fraction = checkpoint_guardian.latest_consensus_fraction()
    print(f"Latest consensus fraction: {consensus_fraction:.4f}")
    print()

    print("=" * 60)
    print("Training example complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
