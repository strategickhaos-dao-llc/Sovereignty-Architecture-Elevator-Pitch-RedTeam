#!/usr/bin/env python3
"""
Strategickhaos Legion Daemon - Proposal Polling Service

Continuously monitors for new proposals and triggers voting.
Expand this stub for production use with proper event handling.
"""

import time
import os
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('legion_daemon')

# Import kernel if available
try:
    from connect import LegionKernel
    HAS_KERNEL = True
except ImportError:
    HAS_KERNEL = False
    logger.warning("LegionKernel not available")


class LegionDaemon:
    """
    Background daemon that polls for new proposals and manages voting lifecycle.
    """

    def __init__(self, poll_interval: int = 60):
        self.poll_interval = poll_interval
        self.processed_proposals = set()
        self.proposals_dir = Path('.strategickhaos/proposals')

        if HAS_KERNEL:
            self.kernel = LegionKernel(workspace_id='daemon')
        else:
            self.kernel = None

    def scan_for_proposals(self) -> list:
        """Scan for new proposal files"""
        new_proposals = []

        if not self.proposals_dir.exists():
            return new_proposals

        for filepath in self.proposals_dir.glob('*.json'):
            # Skip vote files
            if '_vote.json' in filepath.name:
                continue

            proposal_id = filepath.stem
            if proposal_id not in self.processed_proposals:
                new_proposals.append(proposal_id)

        return new_proposals

    def process_proposal(self, proposal_id: str):
        """Process a single proposal"""
        logger.info(f"Processing proposal: {proposal_id}")

        if self.kernel:
            status = self.kernel.check_proposal_status(proposal_id)
            logger.info(f"Proposal {proposal_id} status: {status['status']}")

            # Auto-execute if approved and not yet executed
            if status['status'] == 'approved':
                result = self.kernel.execute_approved(proposal_id)
                if result['executed']:
                    logger.info(f"Proposal {proposal_id} auto-executed")

        self.processed_proposals.add(proposal_id)

    def run(self):
        """Main daemon loop"""
        logger.info(f"Legion daemon started (poll interval: {self.poll_interval}s)")

        while True:
            try:
                # Poll for new proposals
                logger.debug("Polling for proposals...")
                new_proposals = self.scan_for_proposals()

                for proposal_id in new_proposals:
                    self.process_proposal(proposal_id)

                if new_proposals:
                    logger.info(f"Processed {len(new_proposals)} new proposal(s)")

            except KeyboardInterrupt:
                logger.info("Daemon stopped by user")
                break
            except Exception as e:
                logger.error(f"Daemon error: {e}")

            time.sleep(self.poll_interval)


def main():
    """Main entry point"""
    poll_interval = int(os.getenv('LEGION_POLL_INTERVAL', '60'))
    daemon = LegionDaemon(poll_interval=poll_interval)

    print("🔄 Strategickhaos Legion Daemon")
    print(f"   Poll interval: {poll_interval}s")
    print("   Press Ctrl+C to stop")
    print()

    daemon.run()


if __name__ == '__main__':
    main()
