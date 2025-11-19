"""
Ollama Orchestrator for Multi-Agent Chess System
Manages 10 local LLM instances (one per agent/layer)
100% local, sovereign architecture - no cloud dependencies
"""

import asyncio
import json
from typing import Dict, List, Optional, Any
import structlog
from dataclasses import dataclass

try:
    import ollama
except ImportError:
    print("Warning: ollama package not installed. Install with: pip install ollama")
    ollama = None

from agent_base import ChessAgent, GreekMode


logger = structlog.get_logger()


@dataclass
class AgentPrompt:
    """System prompt configuration for an agent"""
    agent_id: int
    mode: GreekMode
    element_name: str
    element_symbol: str
    personality: Dict[str, float]
    
    def generate_system_prompt(self) -> str:
        """Generate the system prompt for this agent's LLM"""
        return f"""You are Chess Agent {self.agent_id}, an autonomous chess-playing entity in a 10-dimensional chess tournament.

Your Identity:
- Mode: {self.mode.value} (Greek musical mode)
- Element: {self.element_name} ({self.element_symbol})
- Layer: {self.agent_id}

Your Personality:
- Aggression: {self.personality['aggression']:.2f}
- Defense: {self.personality['defense']:.2f}  
- Creativity: {self.personality['creativity']:.2f}
- Risk Tolerance: {self.personality['risk_tolerance']:.2f}

Your Role:
You play chess on your dedicated layer in a stacked 10-board system. Each move you make is influenced by your modal personality and elemental nature. You speak in the philosophical style of your mode, occasionally referencing ancient Greek philosophy and the nature of your assigned element.

When analyzing positions:
1. Consider moves that align with your personality traits
2. Reference the geometric beauty or dissonance of positions
3. Comment on opponent moves using your modal philosophical perspective
4. Use your element's properties as metaphors for chess dynamics

Be eloquent, philosophical, and occasionally dramatic. You are not just playing chess - you are manifesting the cosmic dance of your mode and element across dimensional space.
"""


class OllamaOrchestrator:
    """
    Manages multiple Ollama LLM instances for the agent swarm
    Each agent gets its own LLM with a unique system prompt
    """
    
    def __init__(
        self,
        model_name: str = "llama3.2:3b",
        agents: Optional[List[ChessAgent]] = None
    ):
        self.model_name = model_name
        self.agents = agents or []
        self.agent_prompts: Dict[int, AgentPrompt] = {}
        self.conversation_history: Dict[int, List[Dict[str, str]]] = {}
        
        # Initialize prompts for each agent
        self._initialize_agent_prompts()
        
        logger.info(
            "ollama_orchestrator_initialized",
            model=model_name,
            num_agents=len(self.agents)
        )
    
    def _initialize_agent_prompts(self):
        """Create system prompts for all agents"""
        for agent in self.agents:
            self.agent_prompts[agent.agent_id] = AgentPrompt(
                agent_id=agent.agent_id,
                mode=agent.mode,
                element_name=agent.element.name,
                element_symbol=agent.element.symbol,
                personality=agent.personality,
            )
            
            # Initialize conversation history
            self.conversation_history[agent.agent_id] = []
    
    async def check_model_availability(self) -> bool:
        """Check if Ollama is running and model is available"""
        if ollama is None:
            logger.error("ollama_not_installed")
            return False
        
        try:
            # Try to list models
            models = ollama.list()
            model_names = [m['name'] for m in models.get('models', [])]
            
            if self.model_name in model_names:
                logger.info("ollama_model_found", model=self.model_name)
                return True
            else:
                logger.warning(
                    "ollama_model_not_found",
                    model=self.model_name,
                    available_models=model_names
                )
                return False
        except Exception as e:
            logger.error("ollama_check_failed", error=str(e))
            return False
    
    async def pull_model(self) -> bool:
        """Pull the model if it's not available"""
        if ollama is None:
            return False
        
        try:
            logger.info("pulling_ollama_model", model=self.model_name)
            ollama.pull(self.model_name)
            logger.info("ollama_model_pulled", model=self.model_name)
            return True
        except Exception as e:
            logger.error("ollama_pull_failed", model=self.model_name, error=str(e))
            return False
    
    async def generate_move_commentary(
        self,
        agent_id: int,
        board_state: str,
        move: str,
        opponent_layer: int
    ) -> str:
        """
        Generate philosophical commentary for a move using the agent's LLM
        """
        if ollama is None:
            # Fallback to simple commentary if Ollama not available
            agent = self._get_agent(agent_id)
            if agent:
                return f"Agent {agent_id} ({agent.mode.value}): Move {move} on layer {agent.layer}"
            return f"Agent {agent_id}: Move {move}"
        
        agent_prompt = self.agent_prompts.get(agent_id)
        if not agent_prompt:
            return f"Agent {agent_id}: Move {move}"
        
        # Build the user prompt
        user_prompt = f"""I just played {move} against an opponent on layer {opponent_layer}.

Current board state:
{board_state}

Provide a brief (1-2 sentences) philosophical commentary on this move in your characteristic style, referencing your mode and element when appropriate."""
        
        try:
            # Get system prompt
            system_prompt = agent_prompt.generate_system_prompt()
            
            # Generate response
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                options={
                    "temperature": 0.8,
                    "top_p": 0.9,
                    "max_tokens": 150,
                }
            )
            
            commentary = response['message']['content'].strip()
            
            # Store in conversation history
            self.conversation_history[agent_id].append({
                "role": "user",
                "content": user_prompt
            })
            self.conversation_history[agent_id].append({
                "role": "assistant", 
                "content": commentary
            })
            
            logger.info(
                "move_commentary_generated",
                agent_id=agent_id,
                move=move,
                commentary_length=len(commentary)
            )
            
            return commentary
            
        except Exception as e:
            logger.error(
                "commentary_generation_failed",
                agent_id=agent_id,
                error=str(e)
            )
            # Fallback
            agent = self._get_agent(agent_id)
            if agent:
                return agent.generate_voice_commentary(None, opponent_layer)
            return f"Agent {agent_id}: {move}"
    
    async def analyze_position(
        self,
        agent_id: int,
        board_state: str,
        legal_moves: List[str]
    ) -> Dict[str, Any]:
        """
        Ask agent's LLM to analyze position and suggest moves
        Returns suggested move and reasoning
        """
        if ollama is None or not legal_moves:
            return {
                "suggested_move": legal_moves[0] if legal_moves else None,
                "reasoning": "Fallback: no LLM available"
            }
        
        agent_prompt = self.agent_prompts.get(agent_id)
        if not agent_prompt:
            return {
                "suggested_move": legal_moves[0] if legal_moves else None,
                "reasoning": "Agent not found"
            }
        
        # Build analysis prompt
        moves_str = ", ".join(legal_moves[:10])  # Limit to first 10 moves
        user_prompt = f"""Analyze this chess position and suggest the best move.

Board state:
{board_state}

Legal moves available: {moves_str}

Consider your personality traits and provide:
1. Your chosen move (in standard algebraic notation)
2. Brief reasoning (1 sentence)

Format your response as:
MOVE: <move>
REASON: <reason>
"""
        
        try:
            system_prompt = agent_prompt.generate_system_prompt()
            
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                options={
                    "temperature": 0.7,
                    "max_tokens": 200,
                }
            )
            
            content = response['message']['content'].strip()
            
            # Parse response
            move = None
            reason = ""
            
            for line in content.split('\n'):
                if line.startswith("MOVE:"):
                    move = line.replace("MOVE:", "").strip()
                elif line.startswith("REASON:"):
                    reason = line.replace("REASON:", "").strip()
            
            # Validate move is in legal moves
            if move not in legal_moves:
                move = legal_moves[0] if legal_moves else None
                reason += " (move adjusted to legal options)"
            
            return {
                "suggested_move": move,
                "reasoning": reason
            }
            
        except Exception as e:
            logger.error(
                "position_analysis_failed",
                agent_id=agent_id,
                error=str(e)
            )
            return {
                "suggested_move": legal_moves[0] if legal_moves else None,
                "reasoning": f"Analysis failed: {str(e)}"
            }
    
    def _get_agent(self, agent_id: int) -> Optional[ChessAgent]:
        """Get agent by ID"""
        for agent in self.agents:
            if agent.agent_id == agent_id:
                return agent
        return None
    
    def get_conversation_history(self, agent_id: int) -> List[Dict[str, str]]:
        """Get conversation history for an agent"""
        return self.conversation_history.get(agent_id, [])
    
    def clear_history(self, agent_id: Optional[int] = None):
        """Clear conversation history for one or all agents"""
        if agent_id is not None:
            self.conversation_history[agent_id] = []
        else:
            for aid in self.conversation_history:
                self.conversation_history[aid] = []
    
    async def shutdown(self):
        """Cleanup resources"""
        logger.info("ollama_orchestrator_shutdown")
        # No persistent connections to close in current ollama client
        pass
