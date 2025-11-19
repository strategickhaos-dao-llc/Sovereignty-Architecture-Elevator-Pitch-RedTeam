"""
TRS Multi-Agent Chess System
100% local, sovereign architecture for 10-dimensional chess
"""

__version__ = "1.0.14"
__author__ = "Strategickhaos Swarm Intelligence"

from .agent_base import ChessAgent, GreekMode, AGENT_ELEMENTS
from .mobius_eval import MobiusChessEvaluator, MobiusTransform
from .ollama_orchestrator import OllamaOrchestrator
from .voice_interface import VoiceInterface, VoiceCommandHandler
from .websocket_bridge import WebSocketBridge, MoveEvent, BoardState, AgentState

__all__ = [
    "ChessAgent",
    "GreekMode",
    "AGENT_ELEMENTS",
    "MobiusChessEvaluator",
    "MobiusTransform",
    "OllamaOrchestrator",
    "VoiceInterface",
    "VoiceCommandHandler",
    "WebSocketBridge",
    "MoveEvent",
    "BoardState",
    "AgentState",
]
