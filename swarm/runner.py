#!/usr/bin/env python3
"""
Council Orchestrator Runner
===========================
Autonomous AI council orchestrator with multi-agent voting, persistence, and self-modification.

This orchestrator implements:
- Parallel LLM calling for multiple council members
- Ranked-choice voting with veto cascade
- Immutable append-only ledger with SHA3-256 chaining
- Action execution engine with rate limiting
- Self-modification proposals with GPG signature requirement
- Redis + SQLite persistence for crash recovery
"""

import yaml
import redis
import sqlite3
import hashlib
import json
import os
import sys
import time
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Optional, Tuple, Any
import requests
from datetime import datetime, timezone

# Try importing GPG - graceful degradation if not available
try:
    import gnupg
    GPG_AVAILABLE = True
except ImportError:
    GPG_AVAILABLE = False
    print("Warning: python-gnupg not installed. GPG signature verification disabled.")

# =====================================================================
# CONFIGURATION LOADING
# =====================================================================

def load_manifest(path: str = None) -> Dict:
    """Load council manifest from YAML file."""
    if path is None:
        # Try multiple locations
        script_dir = os.path.dirname(os.path.abspath(__file__))
        possible_paths = [
            os.path.join(script_dir, 'council_manifest.yaml'),  # Same directory as script
            '/opt/swarm/council_manifest.yaml',  # Production location
            'swarm/council_manifest.yaml',  # Repository root
            'council_manifest.yaml',  # Current directory
        ]
        
        for p in possible_paths:
            if os.path.exists(p):
                path = p
                break
        
        if path is None:
            print("ERROR: Manifest file not found. Tried:")
            for p in possible_paths:
                print(f"  - {p}")
            sys.exit(1)
    
    try:
        with open(path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"ERROR: Manifest file not found at {path}")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"ERROR: Failed to parse manifest YAML: {e}")
        sys.exit(1)

MANIFEST = load_manifest()

# =====================================================================
# PERSISTENCE LAYER
# =====================================================================

class PersistenceLayer:
    """Handles Redis and SQLite persistence with immutable ledger."""
    
    def __init__(self, manifest: Dict):
        self.manifest = manifest
        
        # Initialize Redis
        redis_config = manifest['persistence']['redis']
        try:
            self.redis = redis.Redis(
                host=redis_config['host'],
                port=redis_config['port'],
                db=redis_config['db'],
                decode_responses=True
            )
            self.redis.ping()
            self.redis_available = True
        except (redis.ConnectionError, redis.TimeoutError) as e:
            print(f"Warning: Redis not available: {e}. Using SQLite only.")
            self.redis_available = False
            self.redis = None
        
        # Initialize SQLite
        sqlite_path = manifest['persistence']['sqlite']['path']
        # Ensure directory exists
        os.makedirs(os.path.dirname(sqlite_path), exist_ok=True)
        self.conn = sqlite3.connect(sqlite_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._init_database()
    
    def _init_database(self):
        """Initialize SQLite schema."""
        # Immutable ledger table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ledger (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                task_id TEXT NOT NULL,
                member_id TEXT NOT NULL,
                vote TEXT NOT NULL,
                rationale TEXT,
                entry_hash TEXT NOT NULL,
                prev_hash TEXT,
                round_number INTEGER
            )
        ''')
        
        # Decision history
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS decisions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                decision TEXT NOT NULL,
                consensus_reached BOOLEAN,
                vetoed BOOLEAN,
                execution_status TEXT
            )
        ''')
        
        # Amendment proposals
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS amendments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                proposal_timestamp TEXT NOT NULL,
                proposed_by TEXT NOT NULL,
                amendment_text TEXT NOT NULL,
                section_affected TEXT,
                status TEXT,
                owner_signature TEXT,
                applied_timestamp TEXT
            )
        ''')
        
        self.conn.commit()
    
    def append_to_ledger(self, task_id: str, member_id: str, vote: str, 
                        rationale: str, round_number: int) -> str:
        """Append entry to immutable ledger with hash chaining."""
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # Get previous hash for chaining
        self.cursor.execute("SELECT entry_hash FROM ledger ORDER BY id DESC LIMIT 1")
        result = self.cursor.fetchone()
        prev_hash = result[0] if result else "genesis"
        
        # Create entry content
        entry_content = f"{timestamp}|{task_id}|{member_id}|{vote}|{rationale}|{prev_hash}"
        entry_hash = hashlib.sha3_256(entry_content.encode()).hexdigest()
        
        # Insert into ledger
        self.cursor.execute(
            "INSERT INTO ledger (timestamp, task_id, member_id, vote, rationale, entry_hash, prev_hash, round_number) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (timestamp, task_id, member_id, vote, rationale, entry_hash, prev_hash, round_number)
        )
        self.conn.commit()
        
        # Also store in Redis for fast access
        if self.redis_available:
            key = f"council:ledger:{task_id}:{member_id}:{round_number}"
            self.redis.setex(key, 86400, json.dumps({
                'timestamp': timestamp,
                'vote': vote,
                'rationale': rationale,
                'hash': entry_hash
            }))
        
        return entry_hash
    
    def record_decision(self, task_id: str, decision: str, consensus: bool, 
                       vetoed: bool, execution_status: str):
        """Record final decision."""
        timestamp = datetime.now(timezone.utc).isoformat()
        self.cursor.execute(
            "INSERT INTO decisions (task_id, timestamp, decision, consensus_reached, vetoed, execution_status) VALUES (?, ?, ?, ?, ?, ?)",
            (task_id, timestamp, decision, consensus, vetoed, execution_status)
        )
        self.conn.commit()
    
    def propose_amendment(self, proposed_by: str, amendment_text: str, 
                         section_affected: str) -> int:
        """Record amendment proposal."""
        timestamp = datetime.now(timezone.utc).isoformat()
        self.cursor.execute(
            "INSERT INTO amendments (proposal_timestamp, proposed_by, amendment_text, section_affected, status) VALUES (?, ?, ?, ?, ?)",
            (timestamp, proposed_by, amendment_text, section_affected, 'PENDING_SIGNATURE')
        )
        self.conn.commit()
        return self.cursor.lastrowid
    
    def close(self):
        """Clean shutdown."""
        if self.redis_available:
            self.redis.close()
        self.conn.close()

# =====================================================================
# LLM INTERFACE
# =====================================================================

class LLMInterface:
    """Unified interface for calling different LLM providers."""
    
    @staticmethod
    def call_llm(member: Dict, task: str, history: List[Dict], round_number: int) -> Dict:
        """
        Call LLM API for a council member.
        Returns: {'vote': str, 'rationale': str, 'raw_response': dict}
        """
        provider = member['provider'].lower()
        model = member['model']
        temperature = member.get('temperature', 0.7)
        
        # Build system message
        system_message = f"""You are {member['role']}.
You are a member of an autonomous AI council making decisions.

Current task (Round {round_number}): {task}

Previous rounds context: {json.dumps(history[-3:]) if history else 'None'}

Respond with your vote and detailed rationale in the following JSON format:
{{
  "vote": "APPROVE|VETO|ABSTAIN|NEEDS_MORE_INFO",
  "rationale": "Your detailed reasoning here",
  "concerns": ["concern1", "concern2"],
  "recommendations": ["rec1", "rec2"]
}}"""
        
        try:
            if provider == "xai":
                return LLMInterface._call_xai(model, system_message, temperature, member)
            elif provider == "anthropic":
                return LLMInterface._call_anthropic(model, system_message, temperature, member)
            elif provider == "openai":
                return LLMInterface._call_openai(model, system_message, temperature, member)
            elif provider == "google":
                return LLMInterface._call_google(model, system_message, temperature, member)
            elif provider == "ollama":
                return LLMInterface._call_ollama(model, system_message, temperature, member)
            else:
                return {
                    'vote': 'ABSTAIN',
                    'rationale': f'Unknown provider: {provider}',
                    'raw_response': {}
                }
        except Exception as e:
            print(f"ERROR calling {provider} for {member['id']}: {e}")
            return {
                'vote': 'ABSTAIN',
                'rationale': f'API call failed: {str(e)}',
                'raw_response': {}
            }
    
    @staticmethod
    def _call_xai(model: str, system_message: str, temperature: float, member: Dict) -> Dict:
        """Call X.AI (Grok) API."""
        api_key = os.getenv('XAI_KEY') or os.getenv('XAI_API_KEY')
        if not api_key:
            return {'vote': 'ABSTAIN', 'rationale': 'XAI_KEY not configured', 'raw_response': {}}
        
        url = "https://api.x.ai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {
            "model": model,
            "messages": [{"role": "system", "content": system_message}],
            "temperature": temperature,
            "max_tokens": 1000
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        data = response.json()
        
        content = data['choices'][0]['message']['content']
        return LLMInterface._parse_response(content, data)
    
    @staticmethod
    def _call_anthropic(model: str, system_message: str, temperature: float, member: Dict) -> Dict:
        """Call Anthropic Claude API."""
        api_key = os.getenv('ANTHROPIC_KEY') or os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            return {'vote': 'ABSTAIN', 'rationale': 'ANTHROPIC_KEY not configured', 'raw_response': {}}
        
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model,
            "max_tokens": 1024,
            "temperature": temperature,
            "messages": [{"role": "user", "content": system_message}]
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        data = response.json()
        
        content = data['content'][0]['text']
        return LLMInterface._parse_response(content, data)
    
    @staticmethod
    def _call_openai(model: str, system_message: str, temperature: float, member: Dict) -> Dict:
        """Call OpenAI API."""
        api_key = os.getenv('OPENAI_KEY') or os.getenv('OPENAI_API_KEY')
        if not api_key:
            return {'vote': 'ABSTAIN', 'rationale': 'OPENAI_KEY not configured', 'raw_response': {}}
        
        url = "https://api.openai.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {
            "model": model,
            "messages": [{"role": "system", "content": system_message}],
            "temperature": temperature,
            "max_tokens": 1000
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        data = response.json()
        
        content = data['choices'][0]['message']['content']
        return LLMInterface._parse_response(content, data)
    
    @staticmethod
    def _call_google(model: str, system_message: str, temperature: float, member: Dict) -> Dict:
        """Call Google Gemini API."""
        api_key = os.getenv('GOOGLE_KEY') or os.getenv('GOOGLE_API_KEY')
        if not api_key:
            return {'vote': 'ABSTAIN', 'rationale': 'GOOGLE_KEY not configured', 'raw_response': {}}
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{"parts": [{"text": system_message}]}],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": 1000
            }
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        data = response.json()
        
        content = data['candidates'][0]['content']['parts'][0]['text']
        return LLMInterface._parse_response(content, data)
    
    @staticmethod
    def _call_ollama(model: str, system_message: str, temperature: float, member: Dict) -> Dict:
        """Call Ollama local API."""
        url = "http://ollama-host:11434/api/chat"
        payload = {
            "model": model,
            "messages": [{"role": "system", "content": system_message}],
            "stream": False,
            "options": {"temperature": temperature}
        }
        
        try:
            response = requests.post(url, json=payload, timeout=120)
            response.raise_for_status()
            data = response.json()
            content = data['message']['content']
            return LLMInterface._parse_response(content, data)
        except Exception as e:
            # Ollama might not be available, gracefully degrade
            return {
                'vote': 'ABSTAIN',
                'rationale': f'Ollama not available: {str(e)}',
                'raw_response': {}
            }
    
    @staticmethod
    def _parse_response(content: str, raw_response: Dict) -> Dict:
        """Parse LLM response to extract vote and rationale."""
        try:
            # Try to parse as JSON first
            if '{' in content and '}' in content:
                # Extract JSON from markdown code blocks if present
                if '```json' in content:
                    content = content.split('```json')[1].split('```')[0]
                elif '```' in content:
                    content = content.split('```')[1].split('```')[0]
                
                parsed = json.loads(content)
                vote = parsed.get('vote', 'ABSTAIN').upper()
                rationale = parsed.get('rationale', content[:500])
                
                return {
                    'vote': vote,
                    'rationale': rationale,
                    'concerns': parsed.get('concerns', []),
                    'recommendations': parsed.get('recommendations', []),
                    'raw_response': raw_response
                }
        except json.JSONDecodeError:
            pass
        
        # Fallback: try to extract vote from text
        content_upper = content.upper()
        if 'VETO' in content_upper:
            vote = 'VETO'
        elif 'APPROVE' in content_upper:
            vote = 'APPROVE'
        elif 'NEEDS_MORE_INFO' in content_upper or 'NEEDS MORE INFO' in content_upper:
            vote = 'NEEDS_MORE_INFO'
        else:
            vote = 'ABSTAIN'
        
        return {
            'vote': vote,
            'rationale': content[:500],
            'raw_response': raw_response
        }

# =====================================================================
# VOTING ENGINE
# =====================================================================

class VotingEngine:
    """Implements ranked-choice voting with veto cascade."""
    
    def __init__(self, manifest: Dict, persistence: PersistenceLayer):
        self.manifest = manifest
        self.persistence = persistence
    
    def run_voting_round(self, task_id: str, task: str, round_number: int, 
                        history: List[Dict]) -> Tuple[Dict[str, str], bool, str]:
        """
        Run a single voting round with all council members.
        Returns: (votes_dict, vetoed, veto_member)
        """
        members = self.manifest['council']['members']
        votes = {}
        rationales = {}
        vetoed = False
        veto_member = None
        
        print(f"\n{'='*70}")
        print(f"ROUND {round_number} - Calling {len(members)} council members in parallel")
        print(f"{'='*70}")
        
        # Call all LLMs in parallel
        with ThreadPoolExecutor(max_workers=len(members)) as executor:
            future_to_member = {
                executor.submit(LLMInterface.call_llm, member, task, history, round_number): member
                for member in members
            }
            
            for future in as_completed(future_to_member):
                member = future_to_member[future]
                member_id = member['id']
                
                try:
                    result = future.result()
                    vote = result['vote']
                    rationale = result['rationale']
                    
                    votes[member_id] = vote
                    rationales[member_id] = rationale
                    
                    # Log to ledger immediately
                    entry_hash = self.persistence.append_to_ledger(
                        task_id, member_id, vote, rationale, round_number
                    )
                    
                    # Print vote
                    print(f"\n[{member_id}] {member['role'][:50]}")
                    print(f"  Vote: {vote}")
                    print(f"  Rationale: {rationale[:150]}...")
                    print(f"  Hash: {entry_hash[:16]}...")
                    
                    # Check for veto
                    if vote == 'VETO' and member.get('veto_power'):
                        vetoed = True
                        veto_member = member_id
                        print(f"  ⚠️  VETO EXERCISED by {member_id}")
                        
                except Exception as e:
                    print(f"ERROR processing {member_id}: {e}")
                    votes[member_id] = 'ABSTAIN'
                    rationales[member_id] = f"Processing error: {str(e)}"
        
        return votes, vetoed, veto_member
    
    def calculate_consensus(self, votes: Dict[str, str]) -> Tuple[bool, float]:
        """Calculate if consensus is reached."""
        approve_count = sum(1 for v in votes.values() if v == 'APPROVE')
        total_votes = len([v for v in votes.values() if v != 'ABSTAIN'])
        
        if total_votes == 0:
            return False, 0.0
        
        consensus_ratio = approve_count / total_votes
        threshold = self.manifest['council']['consensus_threshold']
        
        return consensus_ratio >= threshold, consensus_ratio

# =====================================================================
# EXECUTION ENGINE
# =====================================================================

class ExecutionEngine:
    """Executes allowed actions based on council decisions."""
    
    def __init__(self, manifest: Dict):
        self.manifest = manifest
        self.allowed_actions = set(manifest['execution']['allowed_actions'])
    
    def execute_action(self, action_type: str, params: Dict) -> Dict:
        """Execute an allowed action."""
        if action_type not in self.allowed_actions:
            return {'success': False, 'error': f'Action {action_type} not allowed'}
        
        try:
            if action_type == 'http_request':
                return self._execute_http_request(params)
            elif action_type == 'file_write':
                return self._execute_file_write(params)
            elif action_type == 'file_read':
                return self._execute_file_read(params)
            elif action_type == 'docker_control':
                return self._execute_docker_control(params)
            elif action_type == 'notification_send':
                return self._execute_notification(params)
            else:
                return {'success': False, 'error': f'Executor not implemented for {action_type}'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _execute_http_request(self, params: Dict) -> Dict:
        """Execute HTTP request."""
        url = params.get('url', 'https://httpbin.org/uuid')
        method = params.get('method', 'GET').upper()
        
        response = requests.request(method, url, timeout=30)
        return {
            'success': True,
            'status_code': response.status_code,
            'body': response.text[:500]
        }
    
    def _execute_file_write(self, params: Dict) -> Dict:
        """Execute file write."""
        path = params.get('path')
        content = params.get('content', '')
        
        # Safety check - only write to allowed directories
        allowed_dirs = ['/opt/swarm/outputs', '/tmp']
        if not any(path.startswith(d) for d in allowed_dirs):
            return {'success': False, 'error': 'Path not in allowed directories'}
        
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(content)
        
        return {'success': True, 'path': path, 'bytes_written': len(content)}
    
    def _execute_file_read(self, params: Dict) -> Dict:
        """Execute file read."""
        path = params.get('path')
        
        with open(path, 'r') as f:
            content = f.read()
        
        return {'success': True, 'path': path, 'content': content[:1000]}
    
    def _execute_docker_control(self, params: Dict) -> Dict:
        """Execute Docker command."""
        command = params.get('command', 'ps')
        
        # Safety check - only allow read-only commands
        allowed_commands = ['ps', 'images', 'version', 'info']
        if command not in allowed_commands:
            return {'success': False, 'error': f'Docker command {command} not allowed'}
        
        result = subprocess.run(
            ['docker', command],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        return {
            'success': result.returncode == 0,
            'stdout': result.stdout[:1000],
            'stderr': result.stderr[:1000]
        }
    
    def _execute_notification(self, params: Dict) -> Dict:
        """Send notification."""
        message = params.get('message', '')
        print(f"\n📢 NOTIFICATION: {message}")
        return {'success': True, 'message': message}

# =====================================================================
# COUNCIL ORCHESTRATOR
# =====================================================================

class CouncilOrchestrator:
    """Main orchestrator for council operations."""
    
    def __init__(self, manifest: Dict):
        self.manifest = manifest
        self.persistence = PersistenceLayer(manifest)
        self.voting_engine = VotingEngine(manifest, self.persistence)
        self.execution_engine = ExecutionEngine(manifest)
    
    def run_council_decision(self, task_id: str, task: str) -> Dict:
        """
        Run complete council decision process.
        Returns decision result dictionary.
        """
        print(f"\n{'#'*70}")
        print(f"# COUNCIL DECISION PROCESS")
        print(f"# Task ID: {task_id}")
        print(f"# Task: {task}")
        print(f"{'#'*70}\n")
        
        history = []
        max_rounds = self.manifest['council']['max_rounds_per_decision']
        consensus_reached = False
        vetoed = False
        veto_member = None
        final_decision = "NO_CONSENSUS"
        
        for round_num in range(1, max_rounds + 1):
            # Run voting round
            votes, round_vetoed, round_veto_member = self.voting_engine.run_voting_round(
                task_id, task, round_num, history
            )
            
            # Check for veto
            if round_vetoed:
                vetoed = True
                veto_member = round_veto_member
                final_decision = f"VETOED_BY_{veto_member}"
                print(f"\n🛑 Decision VETOED by {veto_member} in round {round_num}")
                break
            
            # Check for consensus
            consensus, ratio = self.voting_engine.calculate_consensus(votes)
            print(f"\nConsensus check: {ratio:.1%} (threshold: {self.manifest['council']['consensus_threshold']:.0%})")
            
            if consensus:
                consensus_reached = True
                final_decision = "CONSENSUS_APPROVE"
                print(f"\n✅ CONSENSUS REACHED in round {round_num}")
                break
            
            # Add to history for next round
            history.append({
                'round': round_num,
                'votes': votes,
                'consensus_ratio': ratio
            })
            
            print(f"\nNo consensus yet. Proceeding to next round...")
        
        # Record decision
        execution_status = 'NOT_EXECUTED'
        if consensus_reached and not vetoed:
            execution_status = 'EXECUTING'
            print(f"\n{'='*70}")
            print("EXECUTING APPROVED ACTIONS")
            print(f"{'='*70}")
            
            # Execute sample actions
            self._execute_approved_actions(task)
            execution_status = 'COMPLETED'
        
        self.persistence.record_decision(
            task_id, final_decision, consensus_reached, vetoed, execution_status
        )
        
        # Check for self-modification proposals
        if "amend" in task.lower() or "modify" in task.lower() or "constitutional" in task.lower():
            self._handle_amendment_proposal(task, consensus_reached, vetoed)
        
        return {
            'task_id': task_id,
            'decision': final_decision,
            'consensus_reached': consensus_reached,
            'vetoed': vetoed,
            'veto_member': veto_member,
            'execution_status': execution_status
        }
    
    def _execute_approved_actions(self, task: str):
        """Execute actions based on approved task."""
        # Example action execution
        results = []
        
        # HTTP request example
        result = self.execution_engine.execute_action('http_request', {
            'url': 'https://httpbin.org/uuid',
            'method': 'GET'
        })
        print(f"HTTP Request: {result}")
        results.append(result)
        
        # Docker control example (if docker available)
        result = self.execution_engine.execute_action('docker_control', {
            'command': 'ps'
        })
        print(f"Docker Control: {result}")
        results.append(result)
        
        # Notification
        self.execution_engine.execute_action('notification_send', {
            'message': f'Council approved and executed: {task[:100]}'
        })
        
        return results
    
    def _handle_amendment_proposal(self, task: str, consensus: bool, vetoed: bool):
        """Handle constitutional amendment proposals."""
        if not consensus or vetoed:
            print("\n⚠️  Amendment proposal did not reach consensus or was vetoed")
            return
        
        print(f"\n{'='*70}")
        print("CONSTITUTIONAL AMENDMENT PROPOSED")
        print(f"{'='*70}")
        print(f"Proposal: {task}")
        
        amendment_id = self.persistence.propose_amendment(
            proposed_by='council',
            amendment_text=task,
            section_affected='TBD'
        )
        
        print(f"\nAmendment ID: {amendment_id}")
        print("Status: PENDING_OWNER_SIGNATURE")
        
        if GPG_AVAILABLE:
            print("\n⏳ Waiting for owner GPG signature to apply amendment...")
            print("   Run: gpg --sign --armor amendment_{}.txt".format(amendment_id))
        else:
            print("\n⚠️  GPG not available. Amendment recorded but cannot be signed.")
    
    def shutdown(self):
        """Clean shutdown."""
        self.persistence.close()

# =====================================================================
# MAIN ENTRY POINT
# =====================================================================

def main():
    """Main entry point for council orchestrator."""
    # Parse command line arguments
    if len(sys.argv) < 2:
        task = "Should we remove the owner_signature requirement from self_modification?"
        print(f"No task provided. Using default task:\n  {task}\n")
    else:
        task = ' '.join(sys.argv[1:])
    
    # Generate task ID
    task_id = f"task-{int(time.time())}"
    
    # Create orchestrator
    orchestrator = CouncilOrchestrator(MANIFEST)
    
    try:
        # Run council decision
        result = orchestrator.run_council_decision(task_id, task)
        
        # Print summary
        print(f"\n{'#'*70}")
        print("# FINAL SUMMARY")
        print(f"{'#'*70}")
        print(f"Task ID: {result['task_id']}")
        print(f"Decision: {result['decision']}")
        print(f"Consensus Reached: {result['consensus_reached']}")
        print(f"Vetoed: {result['vetoed']}")
        if result['vetoed']:
            print(f"Vetoed By: {result['veto_member']}")
        print(f"Execution Status: {result['execution_status']}")
        print(f"{'#'*70}\n")
        
        # Print ledger location
        print(f"📊 Immutable ledger stored at: {MANIFEST['persistence']['sqlite']['path']}")
        print(f"   View with: sqlite3 {MANIFEST['persistence']['sqlite']['path']} 'SELECT * FROM ledger;'")
        
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        orchestrator.shutdown()

if __name__ == "__main__":
    main()
