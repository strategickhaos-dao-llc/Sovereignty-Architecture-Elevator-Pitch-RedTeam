"""
Strategickhaos Legion Kernel - Core Governance Connection Layer

Connects any development environment to the Strategickhaos collective.
Handles proposal submission, department voting, consensus calculation,
and approved execution with Git-backed versioned memory.
"""

import json
import time
import socket
import os
from typing import Dict, List, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('legion_kernel')

# Optional imports - gracefully degrade if not installed
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    logger.warning("requests not installed - Discord notifications disabled")

try:
    import git
    HAS_GIT = True
except ImportError:
    HAS_GIT = False
    logger.warning("GitPython not installed - using stub git operations")

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False
    logger.warning("PyYAML not installed - using fallback config")


class LegionKernel:
    """
    Connects any development environment to the Strategickhaos collective.
    Manages proposals, voting, consensus, and execution through Git-backed state.
    """

    def __init__(self, workspace_id: str):
        self.workspace_id = workspace_id
        self.repo = self._init_repo()
        self.kernel_config = self._load_config()
        logger.info(f"LegionKernel initialized for workspace: {workspace_id}")

    def _init_repo(self) -> Optional[object]:
        """Initialize Git repository connection"""
        if HAS_GIT:
            try:
                return git.Repo(os.getcwd())
            except git.InvalidGitRepositoryError:
                logger.warning("Not a git repository - using stub operations")
                return None
        return None

    def _load_config(self) -> Dict:
        """Pull latest governance rules from GitHub"""
        # Try to pull latest if we have a real repo
        if self.repo is not None:
            try:
                self.repo.remotes.origin.pull('main')
            except Exception as e:
                logger.warning(f"Could not pull from origin: {e}")

        # Load config file
        config_path = '.strategickhaos/kernel/config.yml'
        if HAS_YAML and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)

        # Fallback default config
        return {
            'legion_os': {
                'departments': [],
                'voting_rules': {
                    'quorum': 3,
                    'threshold': 0.6,
                    'veto_blocks': True,
                    'timeout': 300
                }
            },
            'integrations': {
                'discord': {'webhook': None}
            }
        }

    def _generate_id(self) -> str:
        """Generate unique proposal ID"""
        return f"{int(time.time())}_{self.workspace_id}"

    def propose_change(self, proposal: Dict) -> str:
        """
        Submit a change proposal to the Legion for voting.

        Args:
            proposal: Dict containing title, description, and optional actions

        Returns:
            proposal_id for tracking
        """
        proposal_id = self._generate_id()
        proposal['workspace_id'] = self.workspace_id
        proposal['timestamp'] = time.time()

        # Create proposals dir if needed
        os.makedirs('.strategickhaos/proposals', exist_ok=True)

        # Create proposal file
        proposal_path = f'.strategickhaos/proposals/{proposal_id}.json'
        with open(proposal_path, 'w') as f:
            json.dump(proposal, f, indent=2)

        # Git operations if available
        if self.repo is not None:
            try:
                branch_name = f'proposal/{proposal_id}'
                self.repo.git.checkout('-b', branch_name)
                self.repo.index.add([proposal_path])
                self.repo.index.commit(f'Proposal {proposal_id}: {proposal["title"]}')

                # Push and notify departments
                self.repo.remotes.origin.push(branch_name)
            except Exception as e:
                logger.error(f"Git operation failed: {e}")

        self._notify_departments(proposal_id, proposal)
        logger.info(f"Proposal {proposal_id} submitted: {proposal.get('title', 'Untitled')}")

        return proposal_id

    def _notify_departments(self, proposal_id: str, proposal: Dict):
        """
        Trigger voting across all departments.
        Each department is an AI agent that reviews the proposal.
        """
        departments = self.kernel_config.get('legion_os', {}).get('departments', [])

        votes = {}
        for dept in departments:
            dept_name = dept.get('name', 'unknown')
            agent = dept.get('agent') or dept.get('agents', ['unknown'])[0]

            # Build review prompt
            prompt = f"""
You are the {dept_name.upper()} department of Strategickhaos.

A new proposal requires your vote:

{json.dumps(proposal, indent=2)}

Analyze this proposal from your department's perspective.

Respond with JSON: {{"decision": "APPROVE/REJECT/ABSTAIN", "explanation": "reason"}}

Your department has weight {dept.get('weight', 1)}.
Veto power: {dept.get('veto_power', False)}
"""
            agent_response = self._query_agent(agent, prompt)

            # Record vote
            vote = {
                'decision': agent_response.get('decision', 'ABSTAIN'),
                'weight': dept.get('weight', 1),
                'has_veto': dept.get('veto_power', False),
                'explanation': agent_response.get('explanation', '')
            }
            votes[dept_name] = vote
            self._record_vote(proposal_id, dept_name, vote)

        return votes

    def _query_agent(self, agent: str, prompt: str) -> Dict:
        """
        Query an AI agent for their vote.
        Stub implementation - replace with real API calls.
        """
        # Stub: Real impl would call OpenAI/Anthropic/Ollama API
        logger.info(f"Querying agent: {agent}")
        return {
            'decision': 'APPROVE',
            'explanation': f'Stub approval from {agent}'
        }

    def _record_vote(self, proposal_id: str, dept_name: str, vote: Dict):
        """Commit vote as JSON file"""
        os.makedirs('.strategickhaos/proposals', exist_ok=True)
        vote_path = f'.strategickhaos/proposals/{proposal_id}_{dept_name}_vote.json'

        with open(vote_path, 'w') as f:
            json.dump(vote, f, indent=2)

        if self.repo is not None:
            try:
                self.repo.index.add([vote_path])
                self.repo.index.commit(f'Vote from {dept_name} on {proposal_id}')
            except Exception as e:
                logger.error(f"Failed to commit vote: {e}")

    def _get_votes(self, proposal_id: str) -> Dict:
        """Load all votes for a proposal from the filesystem"""
        votes = {}
        proposals_dir = '.strategickhaos/proposals'

        if not os.path.exists(proposals_dir):
            return votes

        for filename in os.listdir(proposals_dir):
            if filename.startswith(f'{proposal_id}_') and filename.endswith('_vote.json'):
                # Extract department name from filename
                parts = filename.replace('.json', '').split('_')
                if len(parts) >= 3:
                    dept_name = parts[-2]  # Get dept name before _vote
                    vote_path = os.path.join(proposals_dir, filename)
                    try:
                        with open(vote_path, 'r') as f:
                            votes[dept_name] = json.load(f)
                    except (json.JSONDecodeError, IOError) as e:
                        logger.error(f"Failed to load vote {filename}: {e}")

        return votes

    def check_proposal_status(self, proposal_id: str) -> Dict:
        """
        Check if enough departments have voted and if proposal passed.
        """
        votes = self._get_votes(proposal_id)
        rules = self.kernel_config.get('legion_os', {}).get('voting_rules', {})

        quorum = rules.get('quorum', 3)
        threshold = rules.get('threshold', 0.6)
        veto_blocks = rules.get('veto_blocks', True)

        # Check quorum
        if len(votes) < quorum:
            return {
                'status': 'pending',
                'reason': f'quorum not met ({len(votes)}/{quorum})',
                'votes_received': len(votes)
            }

        # Check vetoes
        if veto_blocks:
            for dept, vote in votes.items():
                if vote.get('decision') == 'REJECT' and vote.get('has_veto'):
                    return {
                        'status': 'blocked',
                        'reason': f'{dept} vetoed',
                        'blocking_dept': dept
                    }

        # Calculate weighted approval
        total_weight = sum(v.get('weight', 1) for v in votes.values()) or 1
        approve_weight = sum(
            v.get('weight', 1) for v in votes.values()
            if v.get('decision') == 'APPROVE'
        )

        approval_rate = approve_weight / total_weight

        if approval_rate >= threshold:
            return {
                'status': 'approved',
                'approval_rate': approval_rate,
                'votes': len(votes)
            }
        else:
            return {
                'status': 'rejected',
                'approval_rate': approval_rate,
                'votes': len(votes),
                'threshold': threshold
            }

    def _load_proposal(self, proposal_id: str) -> Dict:
        """Load a proposal from the filesystem"""
        path = f'.strategickhaos/proposals/{proposal_id}.json'
        with open(path, 'r') as f:
            return json.load(f)

    def _execute_actions(self, actions: List[str]):
        """
        Execute approved proposal actions.
        WARNING: This executes shell commands - sanitize carefully!
        """
        allowed_prefixes = ['echo ', 'git ', 'python3 ', 'npm ']

        for action in actions:
            # Basic sanitization - only allow safe commands
            is_safe = any(action.startswith(prefix) for prefix in allowed_prefixes)
            if is_safe:
                logger.info(f"Executing action: {action}")
                os.system(action)
            else:
                logger.warning(f"Blocked unsafe action: {action}")

    def _notify_discord(self, message: str):
        """Send notification to Discord webhook"""
        if not HAS_REQUESTS:
            logger.warning("Cannot notify Discord - requests not installed")
            return

        webhook = self.kernel_config.get('integrations', {}).get('discord', {}).get('webhook')
        if webhook and not webhook.startswith('$'):
            try:
                requests.post(webhook, json={'content': message}, timeout=10)
            except Exception as e:
                logger.error(f"Discord notification failed: {e}")

    def execute_approved(self, proposal_id: str) -> Dict:
        """
        If proposal approved, merge proposal branch and execute actions.
        """
        status = self.check_proposal_status(proposal_id)

        if status['status'] == 'approved':
            # Merge proposal branch if we have git
            if self.repo is not None:
                try:
                    self.repo.git.checkout('main')
                    self.repo.git.merge(f'proposal/{proposal_id}')
                    self.repo.remotes.origin.push('main')
                except Exception as e:
                    logger.error(f"Failed to merge proposal: {e}")

            # Execute actions
            try:
                proposal = self._load_proposal(proposal_id)
                self._execute_actions(proposal.get('actions', []))
            except FileNotFoundError:
                logger.error(f"Proposal file not found: {proposal_id}")

            # Notify
            self._notify_discord(
                f"✅ Proposal {proposal_id} APPROVED and EXECUTED\n"
                f"Approval rate: {status['approval_rate']:.1%}"
            )

            return {'executed': True, 'status': status}

        return {'executed': False, 'status': status}


def main():
    """Main entry point for kernel initialization"""
    workspace_id = os.getenv('CODESPACE_NAME') or socket.gethostname()
    kernel = LegionKernel(workspace_id)
    print(f"✅ Connected to Strategickhaos Legions OS from {workspace_id}")
    print(f"   Memory backend: {kernel.kernel_config.get('legion_os', {}).get('memory_backend', 'git')}")
    print(f"   Consensus protocol: {kernel.kernel_config.get('legion_os', {}).get('consensus_protocol', 'weighted_voting')}")

    departments = kernel.kernel_config.get('legion_os', {}).get('departments', [])
    print(f"   Departments online: {len(departments)}")

    return kernel


if __name__ == '__main__':
    main()
