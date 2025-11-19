"""
Möbius Transform Chess Evaluation
Uses conformal mappings to evaluate chess positions in phase space
"""

import numpy as np
import chess
from typing import Dict, Tuple, List, Optional
from dataclasses import dataclass


@dataclass
class MobiusTransform:
    """
    Represents a Möbius transformation: f(z) = (az + b) / (cz + d)
    where ad - bc ≠ 0
    """
    a: complex
    b: complex
    c: complex
    d: complex
    
    def __post_init__(self):
        """Validate the transformation"""
        determinant = self.a * self.d - self.b * self.c
        if abs(determinant) < 1e-10:
            raise ValueError("Invalid Möbius transform: determinant is zero")
    
    def apply(self, z: complex) -> complex:
        """Apply the transformation to a complex number"""
        return (self.a * z + self.b) / (self.c * z + self.d)
    
    def inverse(self) -> 'MobiusTransform':
        """Return the inverse transformation"""
        return MobiusTransform(self.d, -self.b, -self.c, self.a)


class MobiusChessEvaluator:
    """
    Evaluates chess positions using Möbius transformations
    Maps board state to complex plane and applies conformal transformations
    """
    
    # Piece values in the complex plane (traditional + imaginary components)
    PIECE_VALUES = {
        chess.PAWN: 1.0 + 0.1j,
        chess.KNIGHT: 3.0 + 0.3j,
        chess.BISHOP: 3.0 + 0.4j,
        chess.ROOK: 5.0 + 0.2j,
        chess.QUEEN: 9.0 + 0.5j,
        chess.KING: 0.0 + 10.0j,  # King has infinite tactical value (imaginary)
    }
    
    def __init__(self, phase_angle: float = 0.0):
        """
        Initialize evaluator with a phase angle (0-360 degrees)
        Each agent layer has a unique phase angle
        """
        self.phase_angle = phase_angle
        self.phase_radians = np.radians(phase_angle)
        
        # Create layer-specific Möbius transform based on phase angle
        self.transform = self._create_phase_transform()
    
    def _create_phase_transform(self) -> MobiusTransform:
        """
        Create a Möbius transformation based on the layer's phase angle
        """
        # Use phase angle to create rotation + scaling
        theta = self.phase_radians
        
        # Rotation matrix in complex form
        a = np.exp(1j * theta)
        b = 0.0 + 0.0j
        c = 0.0 + 0.0j
        d = 1.0 + 0.0j
        
        return MobiusTransform(a, b, c, d)
    
    def position_to_complex(self, square: int) -> complex:
        """
        Convert chess square (0-63) to complex number on unit disk
        Maps the 8x8 board to the complex plane
        """
        rank = square // 8
        file = square % 8
        
        # Map to [-1, 1] x [-1, 1]
        x = (file - 3.5) / 4.0
        y = (rank - 3.5) / 4.0
        
        # Convert to complex number and project to unit disk
        z = x + 1j * y
        magnitude = abs(z)
        
        if magnitude > 1.0:
            z = z / magnitude  # Project to unit circle
        
        return z
    
    def evaluate_piece_placement(
        self,
        board: chess.Board,
        color: chess.Color
    ) -> complex:
        """
        Evaluate piece placement for a color using complex arithmetic
        """
        total = 0.0 + 0.0j
        
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            
            if piece and piece.color == color:
                # Get piece value
                piece_value = self.PIECE_VALUES[piece.piece_type]
                
                # Get position in complex plane
                position = self.position_to_complex(square)
                
                # Weight by position (center control is important)
                position_weight = 1.0 + abs(position) * 0.5
                
                # Add to total
                total += piece_value * position_weight
        
        return total
    
    def evaluate_mobility(self, board: chess.Board, color: chess.Color) -> complex:
        """
        Evaluate mobility (number of legal moves) as a complex value
        """
        # Save current turn
        original_turn = board.turn
        
        # Set turn to evaluate
        board.turn = color
        
        # Count legal moves
        mobility = len(list(board.legal_moves))
        
        # Restore turn
        board.turn = original_turn
        
        # Convert to complex (real = mobility, imaginary = mobility squared for nonlinearity)
        return mobility + 1j * (mobility ** 0.5)
    
    def evaluate_king_safety(self, board: chess.Board, color: chess.Color) -> complex:
        """
        Evaluate king safety using distance from edges and attacker proximity
        """
        king_square = board.king(color)
        
        if king_square is None:
            return -100.0 - 100.0j  # King is captured
        
        king_pos = self.position_to_complex(king_square)
        
        # Distance from center (negative is bad for endgame, positive for opening)
        center_distance = abs(king_pos)
        
        # Count attackers near king
        attackers = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece and piece.color != color:
                piece_pos = self.position_to_complex(square)
                distance = abs(king_pos - piece_pos)
                if distance < 0.3:  # Close to king
                    attackers += 1
        
        # Safety score (real = position, imaginary = threat level)
        safety = (1.0 - center_distance) - 1j * attackers
        
        return safety
    
    def evaluate_position(self, board: chess.Board) -> float:
        """
        Main evaluation function: returns a float score
        Positive = advantage for white, negative = advantage for black
        """
        # Evaluate both sides
        white_material = self.evaluate_piece_placement(board, chess.WHITE)
        black_material = self.evaluate_piece_placement(board, chess.BLACK)
        
        white_mobility = self.evaluate_mobility(board, chess.WHITE)
        black_mobility = self.evaluate_mobility(board, chess.BLACK)
        
        white_safety = self.evaluate_king_safety(board, chess.WHITE)
        black_safety = self.evaluate_king_safety(board, chess.BLACK)
        
        # Combine evaluations
        white_total = white_material + 0.1 * white_mobility + 2.0 * white_safety
        black_total = black_material + 0.1 * black_mobility + 2.0 * black_safety
        
        # Apply Möbius transformation to the difference
        difference = white_total - black_total
        
        # Transform through phase space
        transformed = self.transform.apply(difference)
        
        # Return real part as the evaluation (with phase angle influence)
        # The imaginary part represents uncertainty/dynamism
        score = transformed.real
        uncertainty = abs(transformed.imag)
        
        # Weight score by inverse of uncertainty (more certain = more weight)
        if uncertainty > 0:
            score = score / (1.0 + 0.1 * uncertainty)
        
        return score
    
    def evaluate_move(
        self,
        board: chess.Board,
        move: chess.Move
    ) -> Tuple[float, Dict[str, float]]:
        """
        Evaluate a specific move and return score + metrics
        """
        # Make move on a copy
        board_copy = board.copy()
        board_copy.push(move)
        
        # Evaluate resulting position
        score = self.evaluate_position(board_copy)
        
        # Calculate additional metrics
        metrics = {
            "material_change": self._calculate_material_change(board, move),
            "mobility_change": self._calculate_mobility_change(board, board_copy),
            "phase_influence": abs(self.transform.apply(score + 0j).imag),
        }
        
        return score, metrics
    
    def _calculate_material_change(
        self,
        board: chess.Board,
        move: chess.Move
    ) -> float:
        """Calculate material gained/lost from a move"""
        if board.is_capture(move):
            captured = board.piece_at(move.to_square)
            if captured:
                value = self.PIECE_VALUES[captured.piece_type]
                return abs(value)
        return 0.0
    
    def _calculate_mobility_change(
        self,
        board_before: chess.Board,
        board_after: chess.Board
    ) -> float:
        """Calculate change in mobility after a move"""
        mobility_before = len(list(board_before.legal_moves))
        mobility_after = len(list(board_after.legal_moves))
        return mobility_after - mobility_before
    
    def visualize_transform(self, z: complex) -> str:
        """
        Generate a string visualization of how a point transforms
        """
        transformed = self.transform.apply(z)
        return (
            f"z = {z:.3f}\n"
            f"f(z) = {transformed:.3f}\n"
            f"Phase angle: {self.phase_angle:.1f}°\n"
            f"Magnitude: |f(z)| = {abs(transformed):.3f}"
        )
