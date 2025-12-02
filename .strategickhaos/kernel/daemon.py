#!/usr/bin/env python3
"""
Strategickhaos Legions of Minds OS - Background Daemon

Runs as a background service in any codespace to:
- Listen for new proposals
- Monitor voting progress
- Auto-execute approved proposals
- Synchronize state with remote repository
"""

import json
import os
import signal
import sys
import time
from pathlib import Path
from threading import Event
from typing import Any

from connect import LegionKernel


class LegionDaemon:
    """
    Background daemon for the Legion OS.
    
    Continuously monitors:
    - New proposals requiring votes
    - Voting completion status
    - Approved proposals ready for execution
    """
    
    def __init__(self, workspace_id: str | None = None):
        """Initialize the daemon."""
        self.kernel = LegionKernel(workspace_id)
        self.running = Event()
        self.poll_interval = 30  # seconds
        
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._handle_shutdown)
        signal.signal(signal.SIGTERM, self._handle_shutdown)
        
        self._log("info", "LegionDaemon initialized")
    
    def _log(self, level: str, message: str) -> None:
        """Log a message."""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{level.upper()}] [daemon] {message}")
    
    def _handle_shutdown(self, signum: int, frame: Any) -> None:
        """Handle shutdown signals gracefully."""
        self._log("info", "Shutdown signal received, stopping daemon...")
        self.running.clear()
    
    def start(self) -> None:
        """Start the daemon loop."""
        self._log("info", "Starting LegionDaemon...")
        self._log("info", f"Workspace ID: {self.kernel.workspace_id}")
        self._log("info", f"Poll interval: {self.poll_interval}s")
        
        self.running.set()
        
        while self.running.is_set():
            try:
                self._process_cycle()
            except KeyboardInterrupt:
                self._log("info", "Interrupted, stopping...")
                break
            except Exception as e:
                self._log("error", f"Error in daemon cycle: {e}")
            
            # Wait for next cycle
            for _ in range(self.poll_interval):
                if not self.running.is_set():
                    break
                time.sleep(1)
        
        self._log("info", "LegionDaemon stopped")
    
    def _process_cycle(self) -> None:
        """Process one daemon cycle."""
        self._log("info", "Processing cycle...")
        
        # 1. Sync with remote
        self._sync_repository()
        
        # 2. Check for pending vote requests
        self._process_vote_requests()
        
        # 3. Check proposal statuses
        self._check_proposal_statuses()
        
        # 4. Execute any approved proposals
        self._execute_approved_proposals()
    
    def _sync_repository(self) -> None:
        """Sync with remote repository to get latest state."""
        if self.kernel.repo is None:
            return
        
        try:
            if self.kernel.repo.remotes:
                origin = self.kernel.repo.remotes.origin
                origin.fetch()
                
                # Pull if we're on main
                current_branch = self.kernel.repo.active_branch.name
                if current_branch == "main":
                    origin.pull()
                    self._log("info", "Synced with remote repository")
        except Exception as e:
            self._log("warning", f"Repository sync failed: {e}")
    
    def _process_vote_requests(self) -> None:
        """Process pending vote requests from AI departments."""
        proposals_path = self.kernel.proposals_path
        
        for request_file in proposals_path.glob("*_request.json"):
            try:
                with open(request_file) as f:
                    request = json.load(f)
                
                proposal_id = request.get("proposal_id")
                department = request.get("department")
                
                self._log("info", f"Processing vote request: {department} for {proposal_id}")
                
                # In production, this would call the actual AI agent API
                # For now, we simulate by checking if vote already exists
                proposal = self.kernel.get_proposal(proposal_id)
                if proposal and department in proposal.get("votes", {}):
                    # Vote already recorded, remove request
                    request_file.unlink()
                    self._log("info", f"Vote already recorded for {department} on {proposal_id}")
                    continue
                
                # Note: In production, you would call the AI agent here
                # For now, leave request for manual processing
                
            except Exception as e:
                self._log("error", f"Error processing vote request {request_file}: {e}")
    
    def _check_proposal_statuses(self) -> None:
        """Check and update proposal statuses."""
        pending_proposals = self.kernel.list_proposals(status_filter="pending")
        
        for proposal in pending_proposals:
            proposal_id = proposal.get("id")
            status = self.kernel.check_proposal_status(proposal_id)
            
            # Check for timeout
            created_time = proposal.get("timestamp", 0)
            timeout = self.kernel.kernel_config.get("legion_os", {}).get(
                "voting_rules", {}
            ).get("timeout", 300)
            
            if time.time() - created_time > timeout:
                self._log("warning", f"Proposal {proposal_id} timed out")
                self._update_proposal_status(proposal_id, "timeout")
                continue
            
            # Log current status
            if status.get("status") != "pending":
                self._log("info", f"Proposal {proposal_id} status: {status.get('status')}")
    
    def _update_proposal_status(self, proposal_id: str, new_status: str) -> None:
        """Update a proposal's status."""
        proposal_file = self.kernel.proposals_path / f"{proposal_id}.json"
        
        if not proposal_file.exists():
            return
        
        with open(proposal_file) as f:
            proposal = json.load(f)
        
        proposal["status"] = new_status
        proposal["status_updated"] = time.time()
        
        with open(proposal_file, "w") as f:
            json.dump(proposal, f, indent=2)
    
    def _execute_approved_proposals(self) -> None:
        """Execute proposals that have been approved but not yet executed."""
        pending_proposals = self.kernel.list_proposals(status_filter="pending")
        
        for proposal in pending_proposals:
            proposal_id = proposal.get("id")
            status = self.kernel.check_proposal_status(proposal_id)
            
            if status.get("status") == "approved":
                self._log("info", f"Executing approved proposal: {proposal_id}")
                
                # Check if auto-execute is enabled
                auto_execute = self.kernel.kernel_config.get("legion_os", {}).get(
                    "execution", {}
                ).get("auto_execute", True)
                
                if auto_execute:
                    result = self.kernel.execute_approved(proposal_id)
                    self._log("info", f"Execution result: {result.get('success')}")
                else:
                    self._log("info", f"Auto-execute disabled, marking as ready")
                    self._update_proposal_status(proposal_id, "ready_for_execution")


def main() -> None:
    """Main entry point for the daemon."""
    workspace_id = os.getenv("CODESPACE_NAME") or os.getenv("WORKSPACE_ID")
    
    daemon = LegionDaemon(workspace_id)
    
    print("╔════════════════════════════════════════════════════════════╗")
    print("║    Strategickhaos Legions of Minds OS - Daemon Started    ║")
    print("╠════════════════════════════════════════════════════════════╣")
    print(f"║  Workspace: {daemon.kernel.workspace_id:<46} ║")
    print(f"║  Poll Interval: {daemon.poll_interval}s{' ' * 41}║")
    print("╚════════════════════════════════════════════════════════════╝")
    
    daemon.start()


if __name__ == "__main__":
    main()
