import git
import os
import json
import time

class LegionKernel:
    def __init__(self, workspace_id: str):
        self.workspace_id = workspace_id
        self.repo = git.Repo.init(os.getcwd())
        self.kernel_config = self._load_config()
        
    def _load_config(self):
        origin = self.repo.remotes.origin
        origin.pull('main')
        return self._parse_yaml('.strategickhaos/kernel/config.yml')
    
    def propose_change(self, proposal: dict) -> str:
        proposal_id = self._generate_id()
        with open(f'.strategickhaos/proposals/{proposal_id}.json', 'w') as f:
            json.dump(proposal, f, indent=2)
        return proposal_id
