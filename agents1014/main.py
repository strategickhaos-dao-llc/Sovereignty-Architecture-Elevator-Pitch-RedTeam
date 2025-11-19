"""
Main Orchestrator for TRS Multi-Agent Chess System
Coordinates 10 autonomous agents playing chess across 10 stacked boards
100% local, sovereign architecture
"""

import asyncio
import time
import random
from typing import List, Dict, Optional
import structlog
from pathlib import Path

from agent_base import ChessAgent, GreekMode, AGENT_ELEMENTS
from mobius_eval import MobiusChessEvaluator
from ollama_orchestrator import OllamaOrchestrator
from voice_interface import VoiceInterface, VoiceCommandHandler
from websocket_bridge import WebSocketBridge, MoveEvent

import chess


# Configure structured logging
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer()
    ]
)

logger = structlog.get_logger()


class TRSChessOrchestrator:
    """
    Main orchestrator for the 10-agent TRS chess tournament
    Manages game state, agent coordination, and all subsystems
    """
    
    def __init__(
        self,
        num_agents: int = 10,
        ollama_model: str = "llama3.2:3b",
        enable_voice: bool = True,
        enable_websocket: bool = True,
        websocket_host: str = "localhost",
        websocket_port: int = 8765
    ):
        self.num_agents = num_agents
        self.ollama_model = ollama_model
        self.enable_voice = enable_voice
        self.enable_websocket = enable_websocket
        
        # Greek modes for 10 agents
        self.modes = [
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
        
        # Initialize agents
        self.agents: List[ChessAgent] = []
        self.evaluators: Dict[int, MobiusChessEvaluator] = {}
        
        self._initialize_agents()
        
        # Initialize subsystems
        self.ollama = OllamaOrchestrator(
            model_name=ollama_model,
            agents=self.agents
        )
        
        self.voice = VoiceInterface(
            enable_voice_input=enable_voice,
            enable_voice_output=enable_voice
        )
        
        self.websocket = WebSocketBridge(
            host=websocket_host,
            port=websocket_port
        )
        
        # Game state
        self.tournament_active = False
        self.games_played = 0
        self.current_matchups: List[tuple] = []
        
        logger.info(
            "orchestrator_initialized",
            num_agents=num_agents,
            voice_enabled=enable_voice,
            websocket_enabled=enable_websocket
        )
    
    def _initialize_agents(self):
        """Create all 10 agents with their modes and elements"""
        for i in range(self.num_agents):
            agent = ChessAgent(
                agent_id=i,
                layer=i,
                mode=self.modes[i],
                element=AGENT_ELEMENTS[i],
                ollama_model=self.ollama_model
            )
            self.agents.append(agent)
            
            # Create evaluator for this agent
            self.evaluators[i] = MobiusChessEvaluator(
                phase_angle=AGENT_ELEMENTS[i].phase_angle
            )
            
            logger.info(
                "agent_created",
                agent_id=i,
                mode=self.modes[i].value,
                element=AGENT_ELEMENTS[i].symbol
            )
    
    async def initialize(self):
        """Initialize all subsystems"""
        logger.info("initializing_subsystems")
        
        # Initialize voice interface
        await self.voice.initialize()
        
        # Check Ollama availability
        model_available = await self.ollama.check_model_availability()
        if not model_available:
            logger.warning("ollama_model_not_available_attempting_pull")
            await self.ollama.pull_model()
        
        # Start WebSocket server
        if self.enable_websocket:
            await self.websocket.start()
        
        # Update initial agent states in WebSocket
        for agent in self.agents:
            if self.enable_websocket:
                await self.websocket.update_agent_state(
                    agent_id=agent.agent_id,
                    layer=agent.layer,
                    mode=agent.mode.value,
                    element=agent.element.symbol,
                    active=True,
                    thinking=False
                )
        
        logger.info("subsystems_initialized")
    
    async def start_tournament(self):
        """Start the infinite tournament between agents"""
        self.tournament_active = True
        
        # Announce start
        if self.enable_voice:
            await self.voice.announce_game_start(self.num_agents)
        
        logger.info("tournament_started")
        
        # Main tournament loop
        while self.tournament_active:
            # Create matchups (each agent plays against adjacent layer)
            matchups = self._create_matchups()
            
            # Play all games concurrently
            await asyncio.gather(
                *[self._play_game(agent1_id, agent2_id) for agent1_id, agent2_id in matchups]
            )
            
            self.games_played += 1
            
            logger.info("tournament_round_complete", round=self.games_played)
            
            # Brief pause between rounds
            await asyncio.sleep(2)
    
    def _create_matchups(self) -> List[tuple]:
        """
        Create matchups for the tournament
        Each agent plays against another agent on a different layer
        """
        matchups = []
        
        # Simple pairing: agent i plays against agent (i+1) % num_agents
        for i in range(self.num_agents // 2):
            agent1 = i * 2
            agent2 = (i * 2 + 1) % self.num_agents
            matchups.append((agent1, agent2))
        
        return matchups
    
    async def _play_game(self, agent1_id: int, agent2_id: int):
        """
        Play a single game between two agents
        """
        agent1 = self.agents[agent1_id]
        agent2 = self.agents[agent2_id]
        
        logger.info(
            "game_started",
            agent1=agent1_id,
            agent2=agent2_id,
            layer1=agent1.layer,
            layer2=agent2.layer
        )
        
        # Reset boards
        agent1.reset_board()
        agent2.reset_board()
        
        # Game loop
        move_count = 0
        max_moves = 100  # Limit moves per game
        
        while move_count < max_moves:
            # Determine current player
            current_agent = agent1 if agent1.board.turn == chess.WHITE else agent2
            opponent_agent = agent2 if current_agent == agent1 else agent1
            
            # Check if game is over
            if current_agent.board.is_game_over():
                await self._handle_game_over(agent1, agent2, current_agent.board)
                break
            
            # Agent thinks and makes move
            move = await self._agent_make_move(current_agent, opponent_agent)
            
            if move is None:
                logger.warning("no_legal_moves", agent=current_agent.agent_id)
                break
            
            # Update both boards (they should be in sync)
            agent1.board = current_agent.board.copy()
            agent2.board = current_agent.board.copy()
            
            move_count += 1
            
            # Brief pause between moves (0.8 seconds as per spec)
            await asyncio.sleep(0.8)
        
        logger.info(
            "game_completed",
            agent1=agent1_id,
            agent2=agent2_id,
            moves=move_count
        )
    
    async def _agent_make_move(
        self,
        agent: ChessAgent,
        opponent: ChessAgent
    ) -> Optional[chess.Move]:
        """
        Agent analyzes position and makes a move
        """
        # Update WebSocket: agent is thinking
        if self.enable_websocket:
            await self.websocket.update_agent_state(
                agent_id=agent.agent_id,
                layer=agent.layer,
                mode=agent.mode.value,
                element=agent.element.symbol,
                active=True,
                thinking=True
            )
        
        # Get legal moves
        legal_moves = agent.get_legal_moves()
        
        if not legal_moves:
            return None
        
        # Evaluate moves using Möbius evaluator
        evaluator = self.evaluators[agent.agent_id]
        move_scores = []
        
        for move in legal_moves:
            score, metrics = evaluator.evaluate_move(agent.board, move)
            move_scores.append((move, score, metrics))
        
        # Sort by score
        move_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Apply personality: select from top moves based on risk tolerance
        risk_tolerance = agent.personality["risk_tolerance"]
        creativity = agent.personality["creativity"]
        
        # Decide how many top moves to consider
        num_candidates = max(1, int(len(move_scores) * 0.2))  # Top 20%
        candidates = move_scores[:num_candidates]
        
        # If creative, sometimes pick non-optimal moves
        if random.random() < creativity * 0.3:
            selected = random.choice(candidates)
        else:
            selected = candidates[0]
        
        best_move, score, metrics = selected
        
        # Make the move
        agent.make_move(best_move)
        
        # Get commentary from Ollama
        board_fen = agent.board.fen()
        move_san = agent.board.san(best_move)
        
        commentary = await self.ollama.generate_move_commentary(
            agent_id=agent.agent_id,
            board_state=board_fen,
            move=move_san,
            opponent_layer=opponent.layer
        )
        
        # Announce move via voice
        if self.enable_voice:
            await self.voice.announce_move(
                agent_id=agent.agent_id,
                layer=agent.layer,
                move=move_san,
                commentary=commentary
            )
        
        # Send to Unity via WebSocket
        if self.enable_websocket:
            # Update board state
            await self.websocket.update_board_state(
                layer=agent.layer,
                fen=agent.board.fen(),
                agent_id=agent.agent_id,
                move_count=agent.moves_made,
                last_move=move_san
            )
            
            # Send move event
            move_event = MoveEvent(
                agent_id=agent.agent_id,
                layer=agent.layer,
                move=move_san,
                from_square=chess.square_name(best_move.from_square),
                to_square=chess.square_name(best_move.to_square),
                piece=agent.board.piece_at(best_move.to_square).symbol(),
                captured=None,  # Could track captures
                timestamp=time.time()
            )
            await self.websocket.send_move_event(move_event)
            
            # Send commentary
            await self.websocket.send_voice_commentary(
                agent_id=agent.agent_id,
                layer=agent.layer,
                text=commentary
            )
            
            # Agent done thinking
            await self.websocket.update_agent_state(
                agent_id=agent.agent_id,
                layer=agent.layer,
                mode=agent.mode.value,
                element=agent.element.symbol,
                active=True,
                thinking=False
            )
        
        return best_move
    
    async def _handle_game_over(
        self,
        agent1: ChessAgent,
        agent2: ChessAgent,
        board: chess.Board
    ):
        """Handle end of game"""
        result = board.result()
        
        if result == "1-0":
            winner = agent1 if board.turn == chess.BLACK else agent2
            reason = "Checkmate"
        elif result == "0-1":
            winner = agent2 if board.turn == chess.WHITE else agent1
            reason = "Checkmate"
        else:
            winner = None
            reason = "Draw"
        
        winner_id = winner.agent_id if winner else None
        
        logger.info(
            "game_over",
            winner=winner_id,
            reason=reason,
            agent1=agent1.agent_id,
            agent2=agent2.agent_id
        )
        
        if self.enable_voice:
            await self.voice.announce_game_over(winner_id, reason)
        
        if self.enable_websocket:
            await self.websocket.send_game_event(
                "game_over",
                {
                    "winner": winner_id,
                    "reason": reason,
                    "agent1": agent1.agent_id,
                    "agent2": agent2.agent_id
                }
            )
    
    async def stop_tournament(self):
        """Stop the tournament"""
        self.tournament_active = False
        logger.info("tournament_stopped")
    
    async def shutdown(self):
        """Shutdown all subsystems"""
        logger.info("shutting_down")
        
        await self.stop_tournament()
        await self.ollama.shutdown()
        await self.voice.shutdown()
        
        if self.enable_websocket:
            await self.websocket.stop()
        
        logger.info("shutdown_complete")
    
    def get_status(self) -> dict:
        """Get current system status"""
        return {
            "tournament_active": self.tournament_active,
            "games_played": self.games_played,
            "num_agents": self.num_agents,
            "voice_status": self.voice.get_status(),
            "websocket_status": self.websocket.get_status(),
        }


async def main():
    """Main entry point"""
    logger.info("trs_multi_agent_chess_system_starting")
    
    # Create orchestrator
    orchestrator = TRSChessOrchestrator(
        num_agents=10,
        ollama_model="llama3.2:3b",
        enable_voice=True,
        enable_websocket=True,
        websocket_host="0.0.0.0",
        websocket_port=8765
    )
    
    try:
        # Initialize all subsystems
        await orchestrator.initialize()
        
        # Print agent info
        print("\n" + "="*60)
        print("TRS MULTI-AGENT CHESS SYSTEM")
        print("="*60)
        for agent in orchestrator.agents:
            print(agent.get_personality_description())
        print("="*60 + "\n")
        
        # Start tournament
        await orchestrator.start_tournament()
        
    except KeyboardInterrupt:
        logger.info("keyboard_interrupt_received")
    except Exception as e:
        logger.error("orchestrator_error", error=str(e))
    finally:
        await orchestrator.shutdown()


if __name__ == "__main__":
    # Run the orchestrator
    asyncio.run(main())
