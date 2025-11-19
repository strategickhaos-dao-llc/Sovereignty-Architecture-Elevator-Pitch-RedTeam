"""
Basic tests for TRS Multi-Agent Chess System
Validates core functionality without requiring Ollama or heavy dependencies
"""

import unittest
import chess
from agent_base import ChessAgent, GreekMode, AGENT_ELEMENTS
from mobius_eval import MobiusChessEvaluator, MobiusTransform


class TestAgentBase(unittest.TestCase):
    """Test agent creation and basic functionality"""
    
    def test_agent_creation(self):
        """Test creating an agent"""
        agent = ChessAgent(
            agent_id=0,
            layer=0,
            mode=GreekMode.IONIAN,
            element=AGENT_ELEMENTS[0]
        )
        
        self.assertEqual(agent.agent_id, 0)
        self.assertEqual(agent.layer, 0)
        self.assertEqual(agent.mode, GreekMode.IONIAN)
        self.assertEqual(agent.element.symbol, "H")
        self.assertIsNotNone(agent.personality)
    
    def test_all_modes_exist(self):
        """Test that all 10 Greek modes are defined"""
        modes = [
            GreekMode.IONIAN,
            GreekMode.DORIAN,
            GreekMode.PHRYGIAN,
            GreekMode.LYDIAN,
            GreekMode.MIXOLYDIAN,
            GreekMode.AEOLIAN,
            GreekMode.LOCRIAN,
            GreekMode.HYPERION,
            GreekMode.PROMETHEUS,
            GreekMode.ATLANTEAN,
        ]
        self.assertEqual(len(modes), 10)
    
    def test_agent_elements(self):
        """Test that we have 10 elements defined"""
        self.assertEqual(len(AGENT_ELEMENTS), 10)
        
        # Check specific elements
        self.assertEqual(AGENT_ELEMENTS[0].symbol, "H")  # Hydrogen
        self.assertEqual(AGENT_ELEMENTS[7].symbol, "Br")  # Bromine
        self.assertEqual(AGENT_ELEMENTS[9].symbol, "Au")  # Gold
    
    def test_agent_legal_moves(self):
        """Test getting legal moves"""
        agent = ChessAgent(
            agent_id=0,
            layer=0,
            mode=GreekMode.IONIAN,
            element=AGENT_ELEMENTS[0]
        )
        
        moves = agent.get_legal_moves()
        self.assertGreater(len(moves), 0)
        self.assertEqual(len(moves), 20)  # 20 legal moves in starting position
    
    def test_agent_make_move(self):
        """Test making a move"""
        agent = ChessAgent(
            agent_id=0,
            layer=0,
            mode=GreekMode.IONIAN,
            element=AGENT_ELEMENTS[0]
        )
        
        # Get first legal move
        moves = agent.get_legal_moves()
        move = moves[0]
        
        # Make the move
        result = agent.make_move(move)
        self.assertTrue(result)
        self.assertEqual(agent.moves_made, 1)
    
    def test_personality_traits(self):
        """Test that personality traits are properly initialized"""
        agent = ChessAgent(
            agent_id=2,
            layer=2,
            mode=GreekMode.PHRYGIAN,
            element=AGENT_ELEMENTS[2]
        )
        
        # Check personality has required traits
        self.assertIn("aggression", agent.personality)
        self.assertIn("defense", agent.personality)
        self.assertIn("creativity", agent.personality)
        self.assertIn("risk_tolerance", agent.personality)
        
        # Phrygian should be aggressive
        self.assertGreater(agent.personality["aggression"], 0.5)


class TestMobiusEval(unittest.TestCase):
    """Test Möbius transformation evaluation"""
    
    def test_mobius_transform_creation(self):
        """Test creating a Möbius transform"""
        transform = MobiusTransform(
            a=1.0+0j,
            b=0.0+0j,
            c=0.0+0j,
            d=1.0+0j
        )
        
        # Identity transform
        z = 5.0 + 3j
        result = transform.apply(z)
        self.assertAlmostEqual(result.real, z.real)
        self.assertAlmostEqual(result.imag, z.imag)
    
    def test_mobius_transform_invalid(self):
        """Test that invalid transforms raise error"""
        with self.assertRaises(ValueError):
            # Zero determinant
            MobiusTransform(
                a=1.0+0j,
                b=2.0+0j,
                c=0.5+0j,
                d=1.0+0j
            )
    
    def test_evaluator_creation(self):
        """Test creating an evaluator"""
        evaluator = MobiusChessEvaluator(phase_angle=45.0)
        self.assertEqual(evaluator.phase_angle, 45.0)
        self.assertIsNotNone(evaluator.transform)
    
    def test_position_to_complex(self):
        """Test converting chess square to complex number"""
        evaluator = MobiusChessEvaluator()
        
        # Test center squares
        e4 = chess.E4  # Square 28
        z = evaluator.position_to_complex(e4)
        
        # Should be near center
        self.assertLess(abs(z), 0.5)
    
    def test_evaluate_starting_position(self):
        """Test evaluating starting chess position"""
        evaluator = MobiusChessEvaluator()
        board = chess.Board()
        
        score = evaluator.evaluate_position(board)
        
        # Starting position should be roughly equal
        self.assertAlmostEqual(score, 0.0, delta=5.0)
    
    def test_evaluate_move(self):
        """Test evaluating a specific move"""
        evaluator = MobiusChessEvaluator()
        board = chess.Board()
        
        # Get a legal move
        move = list(board.legal_moves)[0]
        
        score, metrics = evaluator.evaluate_move(board, move)
        
        self.assertIsInstance(score, float)
        self.assertIn("material_change", metrics)
        self.assertIn("mobility_change", metrics)
        self.assertIn("phase_influence", metrics)


class TestPhaseAngles(unittest.TestCase):
    """Test phase angle distribution across agents"""
    
    def test_phase_angles_distinct(self):
        """Test that all agents have distinct phase angles"""
        phase_angles = [elem.phase_angle for elem in AGENT_ELEMENTS]
        
        # Should be 10 distinct angles
        self.assertEqual(len(set(phase_angles)), 10)
    
    def test_phase_angles_range(self):
        """Test that phase angles are in valid range"""
        for elem in AGENT_ELEMENTS:
            self.assertGreaterEqual(elem.phase_angle, 0.0)
            self.assertLess(elem.phase_angle, 360.0)
    
    def test_phase_angles_evenly_spaced(self):
        """Test that phase angles are roughly evenly spaced"""
        phase_angles = sorted([elem.phase_angle for elem in AGENT_ELEMENTS])
        
        # Calculate spacing
        spacings = []
        for i in range(len(phase_angles) - 1):
            spacing = phase_angles[i + 1] - phase_angles[i]
            spacings.append(spacing)
        
        # Should be roughly 36 degrees apart (360/10)
        avg_spacing = sum(spacings) / len(spacings)
        self.assertAlmostEqual(avg_spacing, 36.0, delta=5.0)


class TestVoiceCommentary(unittest.TestCase):
    """Test voice commentary generation"""
    
    def test_commentary_generation(self):
        """Test that agents can generate voice commentary"""
        agent = ChessAgent(
            agent_id=2,
            layer=2,
            mode=GreekMode.PHRYGIAN,
            element=AGENT_ELEMENTS[2]
        )
        
        # Get a legal move
        moves = agent.get_legal_moves()
        move = moves[0]
        
        # Generate commentary
        commentary = agent.generate_voice_commentary(move, opponent_layer=3)
        
        self.assertIsInstance(commentary, str)
        self.assertGreater(len(commentary), 0)
    
    def test_mode_specific_commentary(self):
        """Test that different modes generate different commentary"""
        commentaries = []
        
        for i in range(3):
            agent = ChessAgent(
                agent_id=i,
                layer=i,
                mode=[GreekMode.IONIAN, GreekMode.PHRYGIAN, GreekMode.HYPERION][i],
                element=AGENT_ELEMENTS[i]
            )
            
            moves = agent.get_legal_moves()
            commentary = agent.generate_voice_commentary(moves[0], opponent_layer=1)
            commentaries.append(commentary)
        
        # Phrygian should mention "blood" or "rotation"
        self.assertTrue(
            "blood" in commentaries[1].lower() or 
            "rotation" in commentaries[1].lower()
        )


if __name__ == "__main__":
    unittest.main()
