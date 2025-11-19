#!/usr/bin/env python3
"""
Demo script for TRS Multi-Agent Chess System
Demonstrates basic functionality without requiring Ollama or full setup
"""

import sys
from agent_base import ChessAgent, GreekMode, AGENT_ELEMENTS
from mobius_eval import MobiusChessEvaluator
import chess


def print_header():
    print("=" * 70)
    print("TRS MULTI-AGENT CHESS SYSTEM - DEMO")
    print("100% Local, Sovereign Architecture")
    print("=" * 70)
    print()


def demo_agent_creation():
    """Demonstrate creating agents with different personalities"""
    print("📊 CREATING 10 AUTONOMOUS AGENTS")
    print("-" * 70)
    
    agents = []
    for i in range(10):
        mode = [
            GreekMode.IONIAN, GreekMode.DORIAN, GreekMode.PHRYGIAN,
            GreekMode.LYDIAN, GreekMode.MIXOLYDIAN, GreekMode.AEOLIAN,
            GreekMode.LOCRIAN, GreekMode.HYPERION, GreekMode.PROMETHEUS,
            GreekMode.ATLANTEAN
        ][i]
        
        agent = ChessAgent(
            agent_id=i,
            layer=i,
            mode=mode,
            element=AGENT_ELEMENTS[i]
        )
        agents.append(agent)
        
        print(f"✓ Agent {i}: {agent.element.symbol:<2} ({agent.element.name:<10}) "
              f"- {mode.value:<12} - Phase: {agent.element.phase_angle:>5.1f}°")
    
    print()
    return agents


def demo_personality_comparison():
    """Compare personalities of different agents"""
    print("🎭 AGENT PERSONALITY COMPARISON")
    print("-" * 70)
    
    # Create three contrasting agents
    agents = [
        ChessAgent(0, 0, GreekMode.IONIAN, AGENT_ELEMENTS[0]),
        ChessAgent(2, 2, GreekMode.PHRYGIAN, AGENT_ELEMENTS[2]),
        ChessAgent(7, 7, GreekMode.HYPERION, AGENT_ELEMENTS[7]),
    ]
    
    traits = ["aggression", "defense", "creativity", "risk_tolerance"]
    
    # Print header
    print(f"{'Trait':<20} {'Ionian':<10} {'Phrygian':<10} {'Hyperion':<10}")
    print("-" * 70)
    
    for trait in traits:
        values = [agent.personality[trait] for agent in agents]
        print(f"{trait.capitalize():<20} {values[0]:<10.2f} {values[1]:<10.2f} {values[2]:<10.2f}")
    
    print()


def demo_mobius_evaluation():
    """Demonstrate Möbius transformation evaluation"""
    print("🔮 MÖBIUS TRANSFORMATION EVALUATION")
    print("-" * 70)
    
    # Create evaluators for different phase angles
    evaluators = [
        MobiusChessEvaluator(phase_angle=0.0),
        MobiusChessEvaluator(phase_angle=120.0),
        MobiusChessEvaluator(phase_angle=240.0),
    ]
    
    board = chess.Board()
    
    print("Starting position evaluation from different phase angles:")
    print()
    
    for i, evaluator in enumerate(evaluators):
        score = evaluator.evaluate_position(board)
        print(f"  Phase {evaluator.phase_angle:>5.1f}° → Score: {score:>7.3f}")
    
    print()


def demo_game_simulation():
    """Simulate a few moves between two agents"""
    print("♟️  GAME SIMULATION: IONIAN vs PHRYGIAN")
    print("-" * 70)
    
    # Create two agents
    agent_white = ChessAgent(0, 0, GreekMode.IONIAN, AGENT_ELEMENTS[0])
    agent_black = ChessAgent(2, 2, GreekMode.PHRYGIAN, AGENT_ELEMENTS[2])
    
    # Create evaluators
    eval_white = MobiusChessEvaluator(phase_angle=0.0)
    eval_black = MobiusChessEvaluator(phase_angle=72.0)
    
    print(f"White: {agent_white.mode.value} ({agent_white.element.name})")
    print(f"Black: {agent_black.mode.value} ({agent_black.element.name})")
    print()
    
    # Simulate 5 moves
    for move_num in range(1, 6):
        # White's turn
        moves = agent_white.get_legal_moves()
        
        # Evaluate all moves
        best_move = None
        best_score = float('-inf')
        
        for move in moves[:5]:  # Just check first 5 for demo
            score, _ = eval_white.evaluate_move(agent_white.board, move)
            if score > best_score:
                best_score = score
                best_move = move
        
        # Get SAN notation before making move
        move_san = agent_white.board.san(best_move)
        
        # Make white's move
        agent_white.make_move(best_move)
        agent_black.board = agent_white.board.copy()
        
        print(f"{move_num}. {move_san:<8} (eval: {best_score:>6.2f})", end="")
        
        # Black's turn
        if agent_black.board.is_game_over():
            print()
            break
        
        moves = agent_black.get_legal_moves()
        best_move = None
        best_score = float('-inf')
        
        for move in moves[:5]:
            score, _ = eval_black.evaluate_move(agent_black.board, move)
            if score > best_score:
                best_score = score
                best_move = move
        
        # Get SAN notation before making move
        move_san = agent_black.board.san(best_move)
        
        # Make black's move
        agent_black.make_move(best_move)
        agent_white.board = agent_black.board.copy()
        
        print(f"  {move_san:<8} (eval: {best_score:>6.2f})")
    
    print()
    print(f"Final position FEN: {agent_white.board.fen()}")
    print()


def demo_voice_commentary():
    """Demonstrate voice commentary generation"""
    print("🗣️  VOICE COMMENTARY EXAMPLES")
    print("-" * 70)
    
    modes_to_demo = [
        (GreekMode.PHRYGIAN, 2),
        (GreekMode.HYPERION, 7),
        (GreekMode.AEOLIAN, 5),
    ]
    
    for mode, idx in modes_to_demo:
        agent = ChessAgent(idx, idx, mode, AGENT_ELEMENTS[idx])
        
        # Get a legal move
        move = list(agent.board.legal_moves)[0]
        
        # Generate commentary
        commentary = agent.generate_voice_commentary(move, opponent_layer=idx+1)
        
        print(f"{mode.value:>12}: \"{commentary}\"")
    
    print()


def demo_phase_space_visualization():
    """Show phase angles in the phase space"""
    print("🌀 PHASE SPACE DISTRIBUTION")
    print("-" * 70)
    
    import math
    
    print("Agent distribution across 360° phase space:")
    print()
    
    # Create a simple ASCII visualization
    for i, element in enumerate(AGENT_ELEMENTS):
        angle = element.phase_angle
        # Convert to position on circle (simplified ASCII art)
        bars = int(angle / 10)  # 36 positions for 360 degrees
        visualization = " " * bars + "●"
        
        print(f"Layer {i} ({element.symbol:<2}): {angle:>5.1f}° {visualization}")
    
    print()
    print("Each agent operates in a unique phase angle of the conformal")
    print("transformation space, creating 10 distinct evaluation perspectives.")
    print()


def main():
    """Run all demos"""
    print_header()
    
    try:
        # Run demonstrations
        agents = demo_agent_creation()
        demo_personality_comparison()
        demo_mobius_evaluation()
        demo_game_simulation()
        demo_voice_commentary()
        demo_phase_space_visualization()
        
        print("=" * 70)
        print("DEMO COMPLETE")
        print("=" * 70)
        print()
        print("To run the full system with Ollama:")
        print("  1. Install Ollama: https://ollama.ai")
        print("  2. Pull model: ollama pull llama3.2:3b")
        print("  3. Run: ./run.sh")
        print()
        print("Or use Docker:")
        print("  docker-compose -f docker-compose.agents.yml up")
        print()
        
    except Exception as e:
        print(f"❌ Error during demo: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
