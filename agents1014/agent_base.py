"""
Base Agent Class for TRS Multi-Agent Chess System
Each agent represents one layer with a unique Greek mode and periodic element
"""

import chess
import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class GreekMode(Enum):
    """7 Greek modes + 3 experimental modes"""
    IONIAN = "Ionian"          # C-D-E-F-G-A-B (Major scale)
    DORIAN = "Dorian"          # D-E-F-G-A-B-C
    PHRYGIAN = "Phrygian"      # E-F-G-A-B-C-D
    LYDIAN = "Lydian"          # F-G-A-B-C-D-E
    MIXOLYDIAN = "Mixolydian"  # G-A-B-C-D-E-F
    AEOLIAN = "Aeolian"        # A-B-C-D-E-F-G (Natural minor)
    LOCRIAN = "Locrian"        # B-C-D-E-F-G-A
    # Experimental modes
    HYPERION = "Hyperion"      # Experimental mode 1 (raised 4th and 7th)
    PROMETHEUS = "Prometheus"  # Experimental mode 2 (whole-tone derived)
    ATLANTEAN = "Atlantean"    # Experimental mode 3 (microtonal hybrid)


@dataclass
class PeriodicElement:
    """Represents a periodic table element assigned to an agent"""
    symbol: str
    name: str
    atomic_number: int
    family: str
    phase_angle: float  # 0-360 degrees


# Agent-Element mappings for 10 layers
AGENT_ELEMENTS = [
    PeriodicElement("H", "Hydrogen", 1, "Nonmetal", 0.0),
    PeriodicElement("He", "Helium", 2, "Noble Gas", 36.0),
    PeriodicElement("Li", "Lithium", 3, "Alkali Metal", 72.0),
    PeriodicElement("C", "Carbon", 6, "Nonmetal", 108.0),
    PeriodicElement("N", "Nitrogen", 7, "Nonmetal", 144.0),
    PeriodicElement("O", "Oxygen", 8, "Nonmetal", 180.0),
    PeriodicElement("F", "Fluorine", 9, "Halogen", 216.0),
    PeriodicElement("Br", "Bromine", 35, "Halogen", 252.0),
    PeriodicElement("Xe", "Xenon", 54, "Noble Gas", 288.0),
    PeriodicElement("Au", "Gold", 79, "Transition Metal", 324.0),
]


class ChessAgent:
    """
    Autonomous chess agent for one layer of the 10D TRS chess system
    Each agent has a unique personality defined by its mode and element
    """
    
    def __init__(
        self,
        agent_id: int,
        layer: int,
        mode: GreekMode,
        element: PeriodicElement,
        ollama_model: str = "llama3.2:3b"
    ):
        self.agent_id = agent_id
        self.layer = layer
        self.mode = mode
        self.element = element
        self.ollama_model = ollama_model
        
        # Chess board state for this layer
        self.board = chess.Board()
        
        # Agent personality traits based on mode
        self.personality = self._initialize_personality()
        
        # Move history
        self.move_history: List[chess.Move] = []
        
        # Performance metrics
        self.games_played = 0
        self.moves_made = 0
        self.evaluations_computed = 0
        
    def _initialize_personality(self) -> Dict[str, float]:
        """
        Initialize agent personality based on Greek mode
        Returns traits that influence move selection
        """
        personalities = {
            GreekMode.IONIAN: {
                "aggression": 0.5,
                "defense": 0.6,
                "creativity": 0.5,
                "calculation_depth": 5,
                "risk_tolerance": 0.4,
            },
            GreekMode.DORIAN: {
                "aggression": 0.6,
                "defense": 0.7,
                "creativity": 0.6,
                "calculation_depth": 6,
                "risk_tolerance": 0.5,
            },
            GreekMode.PHRYGIAN: {
                "aggression": 0.8,
                "defense": 0.4,
                "creativity": 0.7,
                "calculation_depth": 5,
                "risk_tolerance": 0.7,
            },
            GreekMode.LYDIAN: {
                "aggression": 0.4,
                "defense": 0.5,
                "creativity": 0.9,
                "calculation_depth": 7,
                "risk_tolerance": 0.6,
            },
            GreekMode.MIXOLYDIAN: {
                "aggression": 0.7,
                "defense": 0.5,
                "creativity": 0.6,
                "calculation_depth": 5,
                "risk_tolerance": 0.6,
            },
            GreekMode.AEOLIAN: {
                "aggression": 0.5,
                "defense": 0.8,
                "creativity": 0.5,
                "calculation_depth": 6,
                "risk_tolerance": 0.3,
            },
            GreekMode.LOCRIAN: {
                "aggression": 0.3,
                "defense": 0.9,
                "creativity": 0.4,
                "calculation_depth": 8,
                "risk_tolerance": 0.2,
            },
            GreekMode.HYPERION: {
                "aggression": 0.9,
                "defense": 0.3,
                "creativity": 0.95,
                "calculation_depth": 4,
                "risk_tolerance": 0.9,
            },
            GreekMode.PROMETHEUS: {
                "aggression": 0.7,
                "defense": 0.6,
                "creativity": 1.0,
                "calculation_depth": 6,
                "risk_tolerance": 0.8,
            },
            GreekMode.ATLANTEAN: {
                "aggression": 0.6,
                "defense": 0.7,
                "creativity": 0.85,
                "calculation_depth": 7,
                "risk_tolerance": 0.5,
            },
        }
        return personalities.get(self.mode, personalities[GreekMode.IONIAN])
    
    def get_legal_moves(self) -> List[chess.Move]:
        """Get all legal moves for current board position"""
        return list(self.board.legal_moves)
    
    def make_move(self, move: chess.Move) -> bool:
        """
        Execute a move on the board
        Returns True if move was legal and executed
        """
        if move in self.board.legal_moves:
            self.board.push(move)
            self.move_history.append(move)
            self.moves_made += 1
            return True
        return False
    
    def reset_board(self):
        """Reset board to starting position"""
        self.board.reset()
        self.move_history.clear()
        self.games_played += 1
    
    def get_personality_description(self) -> str:
        """Generate a description of this agent's personality"""
        return (
            f"Agent {self.agent_id} ({self.element.name} - {self.mode.value})\n"
            f"  Layer: {self.layer}\n"
            f"  Element: {self.element.symbol} ({self.element.family})\n"
            f"  Phase Angle: {self.element.phase_angle}°\n"
            f"  Aggression: {self.personality['aggression']:.2f}\n"
            f"  Defense: {self.personality['defense']:.2f}\n"
            f"  Creativity: {self.personality['creativity']:.2f}\n"
            f"  Risk Tolerance: {self.personality['risk_tolerance']:.2f}\n"
        )
    
    def generate_voice_commentary(self, move: chess.Move, opponent_layer: int) -> str:
        """
        Generate voice commentary for a move in the style of this agent's mode
        """
        move_san = self.board.san(move)
        
        # Mode-specific commentary styles
        commentary_templates = {
            GreekMode.IONIAN: f"I play {move_san} on layer {self.layer}, a harmonious move.",
            GreekMode.DORIAN: f"{move_san} on layer {self.layer}. Balanced and resolute.",
            GreekMode.PHRYGIAN: f"Your Dorian pawn sacrifice on layer {opponent_layer} was aesthetically pleasing but geometrically naïve. I respond with {move_san}. The rotation demands blood.",
            GreekMode.LYDIAN: f"Observe the transcendent beauty of {move_san} on layer {self.layer}.",
            GreekMode.MIXOLYDIAN: f"Layer {self.layer}: {move_san}. The dominant force prevails.",
            GreekMode.AEOLIAN: f"I move {move_san} on layer {self.layer}, with melancholic precision.",
            GreekMode.LOCRIAN: f"The unstable nature demands {move_san} on layer {self.layer}.",
            GreekMode.HYPERION: f"LAYER {self.layer}: {move_san}! THE COSMOS TREMBLES!",
            GreekMode.PROMETHEUS: f"Fire stolen from the gods manifests as {move_san} on layer {self.layer}.",
            GreekMode.ATLANTEAN: f"From depths unknown, layer {self.layer} offers {move_san}.",
        }
        
        return commentary_templates.get(
            self.mode,
            f"Agent {self.agent_id}: {move_san} on layer {self.layer}"
        )
    
    def __repr__(self) -> str:
        return (
            f"ChessAgent(id={self.agent_id}, layer={self.layer}, "
            f"mode={self.mode.value}, element={self.element.symbol})"
        )
