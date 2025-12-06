"""
Legion Honeypot Analyzer
Learns from attacks on honeypot, strengthens production defenses.

This module subscribes to honeypot attack events and uses AI to:
1. Analyze attack patterns
2. Generate defensive countermeasures
3. Update SovereignPRManager rules
4. Strengthen production security

Author: Strategickhaos Swarm Intelligence
"""

import asyncio
import json
import os
import logging
from datetime import datetime
from typing import Any

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.environ.get('LOG_LEVEL', 'INFO')),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('legion.honeypot')


class HoneypotAnalyzer:
    """
    Legion's Honeypot Analyzer component.
    
    Analyzes attacks captured by the honeypot and generates
    defensive countermeasures to strengthen production systems.
    """
    
    def __init__(self):
        """Initialize the analyzer with configuration."""
        self.attack_patterns: list[dict] = []
        self.defenses_generated: list[dict] = []
        self.nats_url = os.environ.get('NATS_URL', 'nats://localhost:4222')
        self.rules_path = os.environ.get(
            'RULES_PATH', 
            '/etc/sovereign-pr-manager/rules/honeypot_learned.py'
        )
        
        # AI configuration (supports multiple providers)
        self.ai_provider = os.environ.get('AI_PROVIDER', 'anthropic')
        
    async def connect_nats(self):
        """Connect to NATS for real-time attack events."""
        try:
            # Try to import nats - if not available, use polling mode
            from nats.aio.client import Client as NATS
            self.nc = NATS()
            await self.nc.connect(self.nats_url)
            logger.info(f"Connected to NATS at {self.nats_url}")
            return True
        except ImportError:
            logger.warning("NATS client not available, using polling mode")
            self.nc = None
            return False
        except Exception as e:
            logger.error(f"Failed to connect to NATS: {e}")
            self.nc = None
            return False
    
    async def analyze_attacks(self):
        """Main loop: subscribe to honeypot attacks and analyze."""
        logger.info("🧠 Legion Honeypot Analyzer starting...")
        
        connected = await self.connect_nats()
        
        if connected and self.nc:
            # Real-time mode via NATS
            await self._run_nats_subscriber()
        else:
            # Polling mode - read from log file
            await self._run_polling_mode()
    
    async def _run_nats_subscriber(self):
        """Run in NATS subscriber mode."""
        async def attack_handler(msg):
            try:
                attack = json.loads(msg.data.decode())
                await self.process_attack(attack)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to decode attack message: {e}")
            except Exception as e:
                logger.error(f"Error processing attack: {e}")
        
        await self.nc.subscribe("honeypot.attack.*", cb=attack_handler)
        logger.info("🧠 Subscribed to honeypot.attack.* - analyzing attacks in real-time")
        
        while True:
            await asyncio.sleep(1)
    
    async def _run_polling_mode(self):
        """Run in polling mode, reading from attack log file."""
        log_file = os.environ.get(
            'ATTACK_LOG_FILE', 
            '/var/log/honeytrap/attacks.jsonl'
        )
        poll_interval = int(os.environ.get('POLL_INTERVAL', '5'))
        last_position = 0
        
        logger.info(f"🧠 Running in polling mode, watching {log_file}")
        
        while True:
            try:
                if os.path.exists(log_file):
                    with open(log_file, 'r') as f:
                        f.seek(last_position)
                        for line in f:
                            if line.strip():
                                attack = json.loads(line)
                                await self.process_attack(attack)
                        last_position = f.tell()
            except Exception as e:
                logger.error(f"Error reading attack log: {e}")
            
            await asyncio.sleep(poll_interval)
    
    async def process_attack(self, attack: dict):
        """Process a single attack event."""
        logger.info(
            f"🎯 Processing attack: {attack.get('attack_types', ['UNKNOWN'])} "
            f"from {attack.get('source_ip', 'unknown')}"
        )
        
        # Store the pattern
        self.attack_patterns.append(attack)
        
        # Analyze with AI
        analysis = await self.analyze_attack_with_ai(attack)
        
        if analysis:
            # Generate defense
            defense = await self.generate_defense(analysis, attack)
            
            if defense:
                # Update PR rules
                await self.update_pr_rules(defense)
                
                # Store the defense
                self.defenses_generated.append({
                    'attack': attack,
                    'analysis': analysis,
                    'defense': defense,
                    'timestamp': datetime.utcnow().isoformat()
                })
                
                # Publish to Blue team if NATS connected
                if self.nc:
                    await self.nc.publish(
                        "blue.defense.update",
                        json.dumps({
                            'attack': attack,
                            'analysis': analysis,
                            'defense': defense
                        }).encode()
                    )
    
    async def analyze_attack_with_ai(self, attack: dict) -> dict | None:
        """Analyze attack pattern using AI."""
        
        # Build analysis prompt
        prompt = f"""Analyze this attack captured by our honeypot:

Attack Types Detected: {attack.get('attack_types', ['UNKNOWN'])}
HTTP Method: {attack.get('method', 'UNKNOWN')}
Path: {attack.get('path', '/')}
Body (truncated): {str(attack.get('body', ''))[:500]}
Headers: {json.dumps(attack.get('headers', {}), indent=2)[:500]}
User Agent: {attack.get('user_agent', 'unknown')}

Questions:
1. What vulnerability is being exploited?
2. How would this attack work if successful?
3. What defense would prevent this?
4. Is this a known attack pattern (e.g., OWASP Top 10) or novel?
5. What is the severity level?

Respond in JSON format:
{{
    "vulnerability": "description of vulnerability being exploited",
    "attack_vector": "explanation of how attack works",
    "defense": "mitigation strategy",
    "pattern_type": "known|novel",
    "owasp_category": "category if applicable",
    "severity": "critical|high|medium|low",
    "confidence": 0.0-1.0
}}
"""
        
        try:
            if self.ai_provider == 'anthropic':
                return await self._analyze_with_anthropic(prompt)
            elif self.ai_provider == 'openai':
                return await self._analyze_with_openai(prompt)
            else:
                # Fallback: rule-based analysis
                return self._rule_based_analysis(attack)
        except Exception as e:
            logger.error(f"AI analysis failed: {e}")
            return self._rule_based_analysis(attack)
    
    async def _analyze_with_anthropic(self, prompt: str) -> dict | None:
        """Analyze using Anthropic Claude."""
        try:
            import anthropic
            client = anthropic.Anthropic()
            
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return json.loads(response.content[0].text)
        except ImportError:
            logger.warning("anthropic package not installed")
            return None
        except Exception as e:
            logger.error(f"Anthropic analysis failed: {e}")
            return None
    
    async def _analyze_with_openai(self, prompt: str) -> dict | None:
        """Analyze using OpenAI."""
        try:
            import openai
            client = openai.OpenAI()
            
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000
            )
            
            return json.loads(response.choices[0].message.content)
        except ImportError:
            logger.warning("openai package not installed")
            return None
        except Exception as e:
            logger.error(f"OpenAI analysis failed: {e}")
            return None
    
    def _rule_based_analysis(self, attack: dict) -> dict:
        """Fallback rule-based analysis when AI is not available."""
        attack_types = attack.get('attack_types', ['RECON'])
        
        analysis_map = {
            'XSS_ATTEMPT': {
                'vulnerability': 'Cross-Site Scripting (XSS)',
                'attack_vector': 'Injection of malicious scripts into web pages',
                'defense': 'Input sanitization, Content Security Policy, output encoding',
                'pattern_type': 'known',
                'owasp_category': 'A03:2021 Injection',
                'severity': 'high',
                'confidence': 0.8
            },
            'SQL_INJECTION': {
                'vulnerability': 'SQL Injection',
                'attack_vector': 'Manipulation of SQL queries via user input',
                'defense': 'Parameterized queries, input validation, least privilege DB access',
                'pattern_type': 'known',
                'owasp_category': 'A03:2021 Injection',
                'severity': 'critical',
                'confidence': 0.9
            },
            'PATH_TRAVERSAL': {
                'vulnerability': 'Path Traversal / Directory Traversal',
                'attack_vector': 'Accessing files outside intended directory',
                'defense': 'Input validation, chroot jail, allowlist file paths',
                'pattern_type': 'known',
                'owasp_category': 'A01:2021 Broken Access Control',
                'severity': 'high',
                'confidence': 0.85
            },
            'COMMAND_INJECTION': {
                'vulnerability': 'OS Command Injection',
                'attack_vector': 'Executing arbitrary OS commands',
                'defense': 'Avoid shell commands, input validation, sandboxing',
                'pattern_type': 'known',
                'owasp_category': 'A03:2021 Injection',
                'severity': 'critical',
                'confidence': 0.9
            },
            'SSRF_ATTEMPT': {
                'vulnerability': 'Server-Side Request Forgery (SSRF)',
                'attack_vector': 'Making server request internal resources',
                'defense': 'URL allowlisting, network segmentation, disable redirects',
                'pattern_type': 'known',
                'owasp_category': 'A10:2021 SSRF',
                'severity': 'high',
                'confidence': 0.8
            },
            'BUFFER_OVERFLOW_ATTEMPT': {
                'vulnerability': 'Buffer Overflow',
                'attack_vector': 'Sending oversized input to overflow buffers',
                'defense': 'Input length validation, safe memory functions',
                'pattern_type': 'known',
                'owasp_category': 'Memory Safety',
                'severity': 'high',
                'confidence': 0.7
            },
            'CREDENTIAL_PROBE': {
                'vulnerability': 'Authentication Weakness',
                'attack_vector': 'Credential stuffing or brute force',
                'defense': 'Strong authentication, rate limiting, MFA',
                'pattern_type': 'known',
                'owasp_category': 'A07:2021 Identification Failures',
                'severity': 'medium',
                'confidence': 0.75
            },
            'HEADER_INJECTION': {
                'vulnerability': 'HTTP Header Injection',
                'attack_vector': 'Manipulating HTTP headers for bypass',
                'defense': 'Validate headers, use secure proxy configuration',
                'pattern_type': 'known',
                'owasp_category': 'A05:2021 Security Misconfiguration',
                'severity': 'medium',
                'confidence': 0.7
            },
            'METHOD_TAMPERING': {
                'vulnerability': 'HTTP Verb Tampering',
                'attack_vector': 'Using unauthorized HTTP methods',
                'defense': 'Explicit method whitelisting per endpoint',
                'pattern_type': 'known',
                'owasp_category': 'A01:2021 Broken Access Control',
                'severity': 'low',
                'confidence': 0.8
            },
            'RECON': {
                'vulnerability': 'Reconnaissance',
                'attack_vector': 'Information gathering for future attacks',
                'defense': 'Minimize information disclosure, security headers',
                'pattern_type': 'known',
                'owasp_category': 'Information Disclosure',
                'severity': 'low',
                'confidence': 0.6
            }
        }
        
        # Return analysis for highest severity attack type
        for attack_type in ['SQL_INJECTION', 'COMMAND_INJECTION', 'XSS_ATTEMPT', 
                           'PATH_TRAVERSAL', 'SSRF_ATTEMPT', 'BUFFER_OVERFLOW_ATTEMPT',
                           'CREDENTIAL_PROBE', 'HEADER_INJECTION', 'METHOD_TAMPERING', 'RECON']:
            if attack_type in attack_types:
                return analysis_map.get(attack_type, analysis_map['RECON'])
        
        return analysis_map['RECON']
    
    async def generate_defense(self, analysis: dict, attack: dict) -> dict | None:
        """Generate defense code and configuration from analysis."""
        
        attack_types = attack.get('attack_types', ['UNKNOWN'])
        defense_code = self._generate_detection_code(attack_types, attack)
        
        return {
            'detection_code': defense_code,
            'config': self._generate_config(analysis),
            'network_policy': self._generate_network_policy(analysis),
            'pr_rule': self._generate_pr_rule(analysis, attack_types),
            'severity': analysis.get('severity', 'medium'),
            'generated_at': datetime.utcnow().isoformat()
        }
    
    def _generate_detection_code(self, attack_types: list, attack: dict) -> str:
        """Generate Python detection code for the attack pattern."""
        code_parts = []
        
        if 'XSS_ATTEMPT' in attack_types:
            code_parts.append('''
def detect_xss(input_text: str) -> bool:
    """Detect potential XSS attacks."""
    xss_patterns = [
        r'<script[^>]*>',
        r'javascript:',
        r'on\\w+\\s*=',
        r'<iframe',
        r'<embed',
        r'<object'
    ]
    import re
    for pattern in xss_patterns:
        if re.search(pattern, input_text, re.IGNORECASE):
            return True
    return False
''')
        
        if 'SQL_INJECTION' in attack_types:
            code_parts.append('''
def detect_sql_injection(input_text: str) -> bool:
    """Detect potential SQL injection attacks."""
    sql_patterns = [
        r'union\\s+select',
        r'drop\\s+table',
        r"'\\s*or\\s+'1'\\s*=\\s*'1",
        r';\\s*--',
        r'exec\\s*\\(',
        r'execute\\s*\\('
    ]
    import re
    for pattern in sql_patterns:
        if re.search(pattern, input_text, re.IGNORECASE):
            return True
    return False
''')
        
        if 'PATH_TRAVERSAL' in attack_types:
            code_parts.append('''
def detect_path_traversal(path: str) -> bool:
    """Detect potential path traversal attacks."""
    traversal_patterns = [
        r'\\.\\.',
        r'%2e%2e',
        r'%252e%252e'
    ]
    import re
    for pattern in traversal_patterns:
        if re.search(pattern, path, re.IGNORECASE):
            return True
    return False
''')
        
        if 'COMMAND_INJECTION' in attack_types:
            code_parts.append('''
def detect_command_injection(input_text: str) -> bool:
    """Detect potential command injection attacks."""
    cmd_patterns = [
        r'\\$\\(',
        r'`[^`]+`',
        r'\\|',
        r'&&',
        r';\\s*\\w+',
        r'eval\\s*\\(',
        r'system\\s*\\('
    ]
    import re
    for pattern in cmd_patterns:
        if re.search(pattern, input_text):
            return True
    return False
''')
        
        if not code_parts:
            code_parts.append('''
def detect_suspicious_input(input_text: str) -> bool:
    """Generic suspicious input detection."""
    suspicious_chars = ['<', '>', '"', "'", ';', '|', '&', '$', '`']
    return any(char in input_text for char in suspicious_chars)
''')
        
        return '\n'.join(code_parts)
    
    def _generate_config(self, analysis: dict) -> dict:
        """Generate security configuration based on analysis."""
        return {
            'rate_limiting': {
                'enabled': True,
                'requests_per_minute': 60,
                'burst': 10
            },
            'input_validation': {
                'enabled': True,
                'max_length': 10000,
                'sanitize_html': True
            },
            'security_headers': {
                'X-Content-Type-Options': 'nosniff',
                'X-Frame-Options': 'DENY',
                'Content-Security-Policy': "default-src 'self'",
                'X-XSS-Protection': '1; mode=block'
            }
        }
    
    def _generate_network_policy(self, analysis: dict) -> str:
        """Generate Kubernetes NetworkPolicy YAML."""
        return '''apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: defense-learned-policy
spec:
  podSelector:
    matchLabels:
      app: production-sra
  policyTypes:
    - Ingress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              security: trusted
      ports:
        - port: 8080
          protocol: TCP
'''
    
    def _generate_pr_rule(self, analysis: dict, attack_types: list) -> str:
        """Generate SovereignPRManager rule."""
        vulnerability = analysis.get('vulnerability', 'Unknown')
        defense = analysis.get('defense', 'Review required')
        
        return f'''
# Auto-generated rule from honeypot learning
# Vulnerability: {vulnerability}
# Attack Types: {', '.join(attack_types)}

HONEYPOT_LEARNED_RULE = {{
    "name": "honeypot_learned_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
    "description": "Learned from honeypot attack: {vulnerability}",
    "severity": "{analysis.get('severity', 'medium')}",
    "pattern_types": {attack_types},
    "defense": "{defense}",
    "auto_reject": {analysis.get('severity', '') == 'critical'}
}}
'''
    
    async def update_pr_rules(self, defense: dict):
        """Update SovereignPRManager with new defense rules."""
        try:
            # Ensure directory exists
            rules_dir = os.path.dirname(self.rules_path)
            os.makedirs(rules_dir, exist_ok=True)
            
            # Append new rule to file
            with open(self.rules_path, 'a') as f:
                f.write(f"\n# === Rule learned at {defense['generated_at']} ===\n")
                f.write(defense['detection_code'])
                f.write("\n\n")
                f.write(defense['pr_rule'])
                f.write("\n")
            
            logger.info(f"✅ Updated PR rules at {self.rules_path}")
        except Exception as e:
            logger.warning(f"Could not update PR rules file: {e}")
            # Log the rule anyway
            logger.info(f"Generated PR rule:\n{defense['pr_rule']}")
    
    def get_stats(self) -> dict:
        """Get analyzer statistics."""
        return {
            'patterns_analyzed': len(self.attack_patterns),
            'defenses_generated': len(self.defenses_generated),
            'ai_provider': self.ai_provider,
            'nats_connected': self.nc is not None if hasattr(self, 'nc') else False
        }


async def main():
    """Main entry point."""
    analyzer = HoneypotAnalyzer()
    await analyzer.analyze_attacks()


if __name__ == '__main__':
    asyncio.run(main())
