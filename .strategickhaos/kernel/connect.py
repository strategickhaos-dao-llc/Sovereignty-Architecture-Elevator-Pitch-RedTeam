import git
import os
import json
import time
import uuid
import yaml

class LegionKernel:
    def __init__(self, workspace_id: str):
        self.workspace_id = workspace_id
        self.repo = git.Repo.init(os.getcwd())
        self.kernel_config = self._load_config()
        
    def _load_config(self):
        if 'origin' in [r.name for r in self.repo.remotes]:
            origin = self.repo.remotes.origin
            origin.pull('main')
        return self._parse_yaml('.strategickhaos/kernel/config.yml')
    
    def _parse_yaml(self, filepath: str) -> dict:
        """Parse a YAML configuration file."""
        if not os.path.exists(filepath):
            return {}
        with open(filepath, 'r') as f:
            return yaml.safe_load(f) or {}
    
    def _generate_id(self) -> str:
        """Generate a unique proposal ID."""
        return str(uuid.uuid4())
    
    def propose_change(self, proposal: dict) -> str:
        proposal_id = self._generate_id()
        proposals_dir = '.strategickhaos/proposals'
        os.makedirs(proposals_dir, exist_ok=True)
        with open(f'{proposals_dir}/{proposal_id}.json', 'w') as f:
            json.dump(proposal, f, indent=2)
        return proposal_id
