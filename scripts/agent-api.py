#!/usr/bin/env python3
"""
Chess Council Agent API Server
Provides HTTP API for agent communication and game moves.
"""

import json
import os
import math
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Any, Dict, Optional, Union
from urllib.parse import urlparse, parse_qs
import subprocess


class AgentConfig:
    """Agent configuration loaded from environment."""
    
    def __init__(self):
        self.agent_id = os.environ.get('AGENT_ID', 'agent-0')
        self.board_layer = int(os.environ.get('BOARD_LAYER', '0'))
        self.position = int(self.agent_id.split('-')[-1]) if '-' in self.agent_id else 0
        self.frequency_hz = float(os.environ.get('FREQUENCY_HZ', '440'))
        self.note_name = os.environ.get('NOTE_NAME', 'A4')
        self.primary_model = os.environ.get('PRIMARY_MODEL', 'qwen2.5:72b')
        self.ollama_host = os.environ.get('OLLAMA_HOST', 'http://localhost:11434')
        self.qdrant_url = os.environ.get('QDRANT_URL', 'http://qdrant:6333')
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'agent_id': self.agent_id,
            'board_layer': self.board_layer,
            'position': self.position,
            'frequency_hz': self.frequency_hz,
            'note_name': self.note_name,
            'primary_model': self.primary_model,
            'ollama_host': self.ollama_host,
            'qdrant_url': self.qdrant_url,
        }


config = AgentConfig()


def calculate_harmonic_partners(frequency: float) -> Dict[str, float]:
    """Calculate harmonically related frequencies."""
    return {
        'perfect_5th': round(frequency * 3/2, 2),
        'perfect_4th': round(frequency * 4/3, 2),
        'major_3rd': round(frequency * 5/4, 2),
        'minor_3rd': round(frequency * 6/5, 2),
        'octave_up': round(frequency * 2, 2),
        'octave_down': round(frequency / 2, 2),
    }


def run_stockfish_eval(fen: str = None, moves: list = None) -> Dict[str, Any]:
    """Run Stockfish evaluation on a position."""
    try:
        stockfish_path = os.environ.get('STOCKFISH_PATH', '/usr/games/stockfish')
        if not os.path.exists(stockfish_path):
            return {'error': 'Stockfish not found'}
        
        # Simple evaluation - can be extended
        proc = subprocess.Popen(
            [stockfish_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        commands = ['uci', 'isready']
        if fen:
            commands.append(f'position fen {fen}')
        else:
            commands.append('position startpos')
        if moves:
            commands[-1] += f" moves {' '.join(moves)}"
        commands.extend(['go depth 10', 'quit'])
        
        stdout, _ = proc.communicate('\n'.join(commands), timeout=10)
        
        # Parse evaluation
        eval_score = None
        best_move = None
        for line in stdout.split('\n'):
            if 'score cp' in line:
                parts = line.split('score cp')
                if len(parts) > 1:
                    eval_score = int(parts[1].split()[0]) / 100
            elif 'bestmove' in line:
                best_move = line.split()[1]
        
        return {
            'evaluation': eval_score,
            'best_move': best_move,
            'raw_output': stdout[-500:] if len(stdout) > 500 else stdout
        }
    except Exception as e:
        return {'error': str(e)}


class AgentHandler(BaseHTTPRequestHandler):
    """HTTP request handler for agent API."""
    
    def _send_json(self, data: Dict[str, Any], status: int = 200):
        """Send JSON response."""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def do_GET(self):
        """Handle GET requests."""
        parsed = urlparse(self.path)
        path = parsed.path
        
        if path == '/health':
            self._send_json({'status': 'healthy', 'agent_id': config.agent_id})
        
        elif path == '/ready':
            self._send_json({'ready': True, 'agent_id': config.agent_id})
        
        elif path == '/info':
            self._send_json({
                'config': config.to_dict(),
                'harmonics': calculate_harmonic_partners(config.frequency_hz),
                'layer_info': self._get_layer_info(),
            })
        
        elif path == '/harmonics':
            self._send_json({
                'frequency_hz': config.frequency_hz,
                'note': config.note_name,
                'partners': calculate_harmonic_partners(config.frequency_hz),
            })
        
        elif path == '/metrics':
            # Prometheus-style metrics
            metrics = f"""# HELP chess_agent_info Agent information
# TYPE chess_agent_info gauge
chess_agent_info{{agent_id="{config.agent_id}",board="{config.board_layer}",position="{config.position}"}} 1
# HELP chess_agent_frequency_hz Agent frequency in Hz
# TYPE chess_agent_frequency_hz gauge
chess_agent_frequency_hz{{agent_id="{config.agent_id}"}} {config.frequency_hz}
"""
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(metrics.encode())
        
        else:
            self._send_json({'error': 'Not found'}, 404)
    
    def do_POST(self):
        """Handle POST requests."""
        parsed = urlparse(self.path)
        path = parsed.path
        
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode() if content_length > 0 else '{}'
        
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self._send_json({'error': 'Invalid JSON'}, 400)
            return
        
        if path == '/move':
            # Record a game move
            move = data.get('move', {})
            self._send_json({
                'agent_id': config.agent_id,
                'move_accepted': True,
                'move': move,
            })
        
        elif path == '/evaluate':
            # Evaluate a position using Stockfish
            fen = data.get('fen')
            moves = data.get('moves', [])
            result = run_stockfish_eval(fen, moves)
            self._send_json(result)
        
        elif path == '/cite':
            # Record a citation move
            citation = data.get('citation', {})
            claim = data.get('claim', '')
            self._send_json({
                'agent_id': config.agent_id,
                'citation_recorded': True,
                'citation': citation,
                'claim': claim,
            })
        
        elif path == '/ping':
            # Echolocation ping for harmonic discovery
            target_frequency = data.get('frequency_hz')
            my_freq = config.frequency_hz
            
            # Check if harmonically related
            harmonics = calculate_harmonic_partners(my_freq)
            is_harmonic = any(
                abs(target_frequency - h) < 1.0 
                for h in harmonics.values()
            ) if target_frequency else False
            
            self._send_json({
                'agent_id': config.agent_id,
                'frequency_hz': my_freq,
                'note': config.note_name,
                'responds': is_harmonic,
                'relationship': self._find_relationship(target_frequency) if is_harmonic else None,
            })
        
        else:
            self._send_json({'error': 'Not found'}, 404)
    
    def _get_layer_info(self) -> Dict[str, Any]:
        """Get information about the agent's layer."""
        layers = [
            {'id': 0, 'name': 'Empirical Data', 'role': 'Data collection'},
            {'id': 1, 'name': 'Preprocessing', 'role': 'Data cleaning'},
            {'id': 2, 'name': 'Analysis', 'role': 'Statistical analysis'},
            {'id': 3, 'name': 'Synthesis', 'role': 'Knowledge synthesis'},
            {'id': 4, 'name': 'Modeling', 'role': 'Predictive modeling'},
            {'id': 5, 'name': 'Strategic', 'role': 'Game theory'},
            {'id': 6, 'name': 'Ethical', 'role': 'Ethics evaluation'},
            {'id': 7, 'name': 'Linguistic', 'role': 'Paper writing'},
            {'id': 8, 'name': 'Validation', 'role': 'Peer review'},
            {'id': 9, 'name': 'Publication', 'role': 'Dissemination'},
        ]
        return layers[config.board_layer] if config.board_layer < len(layers) else {}
    
    def _find_relationship(self, target_freq: float) -> Optional[str]:
        """Find harmonic relationship to target frequency."""
        if not target_freq:
            return None
        
        my_freq = config.frequency_hz
        ratios = {
            'unison': 1.0,
            'octave': 2.0,
            'perfect_5th': 1.5,
            'perfect_4th': 4/3,
            'major_3rd': 1.25,
            'minor_3rd': 1.2,
        }
        
        for name, ratio in ratios.items():
            if abs(target_freq / my_freq - ratio) < 0.01:
                return name
            if abs(my_freq / target_freq - ratio) < 0.01:
                return f"inverse_{name}"
        
        return 'dissonant'
    
    def log_message(self, format: str, *args):
        """Override to reduce log noise."""
        pass


def main():
    """Start the agent API server."""
    port = int(os.environ.get('AGENT_API_PORT', '8080'))
    server = HTTPServer(('0.0.0.0', port), AgentHandler)
    print(f"Agent API server starting on port {port}")
    print(f"Agent ID: {config.agent_id}")
    print(f"Frequency: {config.frequency_hz} Hz ({config.note_name})")
    server.serve_forever()


if __name__ == '__main__':
    main()
