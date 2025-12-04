#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
10D Chess Council - Agent Application
═══════════════════════════════════════════════════════════════════════════════

Each agent is a containerized LLM that:
- Participates in adversarial research games
- Scrapes bibliographic data from academic sources
- Generates citations, hypotheses, and research papers
- Communicates with other agents via frequency-tuned echolocation
- Trains via self-play

═══════════════════════════════════════════════════════════════════════════════
"""

import asyncio
import json
import logging
import math
import os
import sys
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional

import httpx
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from prometheus_client import Counter, Gauge, Histogram, generate_latest, CONTENT_TYPE_LATEST
from pydantic import BaseModel, Field
import uvicorn

# ═══════════════════════════════════════════════════════════════════════════════
# Configuration
# ═══════════════════════════════════════════════════════════════════════════════

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class AgentConfig:
    """Agent configuration loaded from environment."""
    board_layer: int = int(os.getenv("BOARD_LAYER", "0"))
    agent_position: str = os.getenv("AGENT_POSITION", "chess-board-0-0")
    layer_name: str = os.getenv("LAYER_NAME", "empirical-data")
    frequency_hz: float = float(os.getenv("FREQUENCY_HZ", "440.0"))
    ollama_host: str = os.getenv("OLLAMA_HOST", "http://ollama-service:11434")
    primary_model: str = os.getenv("PRIMARY_MODEL", "qwen2.5:72b")
    qdrant_url: str = os.getenv("QDRANT_URL", "http://qdrant-service:6333")
    postgres_host: str = os.getenv("POSTGRES_HOST", "postgres-service")
    postgres_db: str = os.getenv("POSTGRES_DB", "chess_council")
    grok_api_key: str = os.getenv("GROK_API_KEY", "")
    serpapi_key: str = os.getenv("SERPAPI_KEY", "")
    
    @property
    def row(self) -> int:
        """Calculate row from position (0-7)."""
        ordinal = self._get_ordinal()
        return ordinal // 8
    
    @property
    def col(self) -> int:
        """Calculate column from position (0-7)."""
        ordinal = self._get_ordinal()
        return ordinal % 8
    
    @property
    def chess_notation(self) -> str:
        """Get chess notation (e.g., 'A1', 'H8')."""
        cols = 'ABCDEFGH'
        return f"{cols[self.col]}{self.row + 1}"
    
    def _get_ordinal(self) -> int:
        """Extract ordinal from agent position name."""
        try:
            return int(self.agent_position.split('-')[-1])
        except (ValueError, IndexError):
            return 0
    
    @classmethod
    def calculate_frequency(cls, board: int, row: int, col: int) -> float:
        """Calculate frequency for agent at given position using Circle of 5ths."""
        position = board * 64 + row * 8 + col
        piano_key = position % 88
        # A4 = 440 Hz is piano key 49
        frequency = 440 * (2 ** ((piano_key - 49) / 12))
        return round(frequency, 2)


# ═══════════════════════════════════════════════════════════════════════════════
# Game Types and Mechanics
# ═══════════════════════════════════════════════════════════════════════════════

class GameType(str, Enum):
    """Types of adversarial research games."""
    BIBLIOGRAPHIC_SYNTHESIS = "bibliographic_synthesis_chess"
    HYPOTHESIS_TESTING = "adversarial_hypothesis_testing"
    LITERATURE_REVIEW = "multi_agent_literature_review"


class MoveType(str, Enum):
    """Types of moves in a research game."""
    CITE_PAPER = "cite_paper"
    MAKE_CLAIM = "make_claim"
    REFUTE_CLAIM = "refute_claim"
    SYNTHESIZE = "synthesize"
    VERIFY = "verify"


@dataclass
class GameMove:
    """Represents a single move in an adversarial research game."""
    move_type: MoveType
    action: str
    claim: Optional[str] = None
    citation_doi: Optional[str] = None
    citation_title: Optional[str] = None
    points_earned: int = 0
    stockfish_score: Optional[float] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class GameState:
    """Current state of an adversarial research game."""
    game_id: str
    game_type: GameType
    participants: list[str]
    moves: list[GameMove] = field(default_factory=list)
    current_turn: int = 0
    status: str = "in_progress"
    scores: dict[str, int] = field(default_factory=dict)


# ═══════════════════════════════════════════════════════════════════════════════
# Prometheus Metrics
# ═══════════════════════════════════════════════════════════════════════════════

GAMES_PLAYED = Counter(
    'chess_agent_games_played_total',
    'Total number of games played',
    ['game_type', 'result']
)

MOVES_MADE = Counter(
    'chess_agent_moves_total',
    'Total number of moves made',
    ['move_type']
)

CITATIONS_GENERATED = Counter(
    'chess_agent_citations_total',
    'Total citations generated',
    ['source']
)

AGENT_SCORE = Gauge(
    'chess_agent_score',
    'Current agent score',
    ['layer', 'position']
)

LLM_REQUEST_DURATION = Histogram(
    'chess_agent_llm_request_seconds',
    'LLM request duration in seconds',
    ['model']
)

FREQUENCY_HZ = Gauge(
    'chess_agent_frequency_hz',
    'Agent frequency in Hz',
    ['layer', 'position']
)


# ═══════════════════════════════════════════════════════════════════════════════
# API Models
# ═══════════════════════════════════════════════════════════════════════════════

class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    agent_id: str
    layer: int
    position: str
    frequency_hz: float


class ReadyResponse(BaseModel):
    """Readiness check response."""
    ready: bool
    ollama_connected: bool
    qdrant_connected: bool


class GameStartRequest(BaseModel):
    """Request to start a new game."""
    game_type: GameType
    opponent_id: str
    topic: Optional[str] = None


class MoveRequest(BaseModel):
    """Request to make a move in a game."""
    game_id: str
    move_type: MoveType
    action: str
    claim: Optional[str] = None
    citation_doi: Optional[str] = None


class ResearchRequest(BaseModel):
    """Request to perform research on a topic."""
    topic: str
    sources: list[str] = Field(default=["arxiv", "scholar", "pubmed"])
    max_papers: int = Field(default=10, ge=1, le=100)


class EcholocationRequest(BaseModel):
    """Request to find harmonically compatible agents."""
    target_interval: str = Field(default="perfect_fifth")


# ═══════════════════════════════════════════════════════════════════════════════
# Agent Core
# ═══════════════════════════════════════════════════════════════════════════════

class ChessAgent:
    """
    A 10D Chess Council agent that participates in adversarial research games.
    """
    
    def __init__(self, config: AgentConfig):
        self.config = config
        self.http_client = httpx.AsyncClient(timeout=60.0)
        self.current_games: dict[str, GameState] = {}
        self.total_score: int = 0
        
        # Set metrics
        FREQUENCY_HZ.labels(
            layer=str(config.board_layer),
            position=config.chess_notation
        ).set(config.frequency_hz)
        
        logger.info(
            f"Agent initialized: Layer {config.board_layer} "
            f"({config.layer_name}), Position {config.chess_notation}, "
            f"Frequency {config.frequency_hz} Hz"
        )
    
    async def close(self):
        """Close HTTP client."""
        await self.http_client.aclose()
    
    # ═══════════════════════════════════════════════════════════════════════════
    # LLM Interface
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def query_llm(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None
    ) -> str:
        """Query the local LLM via Ollama."""
        model = model or self.config.primary_model
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        with LLM_REQUEST_DURATION.labels(model=model).time():
            try:
                response = await self.http_client.post(
                    f"{self.config.ollama_host}/api/chat",
                    json={
                        "model": model,
                        "messages": messages,
                        "stream": False
                    }
                )
                response.raise_for_status()
                return response.json().get("message", {}).get("content", "")
            except httpx.HTTPStatusError as e:
                logger.error(
                    f"LLM query failed - model: {model}, status: {e.response.status_code}, "
                    f"prompt_length: {len(prompt)}, host: {self.config.ollama_host}"
                )
                raise
            except httpx.RequestError as e:
                logger.error(
                    f"LLM request error - model: {model}, host: {self.config.ollama_host}, "
                    f"error: {type(e).__name__}: {e}"
                )
                raise
            except Exception as e:
                logger.error(
                    f"LLM unexpected error - model: {model}, error: {type(e).__name__}: {e}"
                )
                raise
    
    # ═══════════════════════════════════════════════════════════════════════════
    # Research Functions
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def search_arxiv(self, query: str, max_results: int = 10) -> list[dict]:
        """Search arXiv for papers."""
        try:
            import arxiv
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.Relevance
            )
            papers = []
            for result in search.results():
                papers.append({
                    "title": result.title,
                    "authors": [str(a) for a in result.authors],
                    "summary": result.summary,
                    "arxiv_id": result.entry_id,
                    "published": result.published.isoformat(),
                    "doi": result.doi
                })
            CITATIONS_GENERATED.labels(source="arxiv").inc(len(papers))
            return papers
        except Exception as e:
            logger.error(f"arXiv search failed: {e}")
            return []
    
    async def search_scholar(self, query: str, max_results: int = 10) -> list[dict]:
        """Search Google Scholar via SerpAPI."""
        if not self.config.serpapi_key:
            logger.warning("SerpAPI key not configured")
            return []
        
        try:
            response = await self.http_client.get(
                "https://serpapi.com/search",
                params={
                    "engine": "google_scholar",
                    "q": query,
                    "api_key": self.config.serpapi_key,
                    "num": max_results
                }
            )
            response.raise_for_status()
            data = response.json()
            
            papers = []
            for result in data.get("organic_results", [])[:max_results]:
                papers.append({
                    "title": result.get("title", ""),
                    "snippet": result.get("snippet", ""),
                    "link": result.get("link", ""),
                    "cited_by": result.get("inline_links", {}).get("cited_by", {}).get("total", 0)
                })
            CITATIONS_GENERATED.labels(source="scholar").inc(len(papers))
            return papers
        except Exception as e:
            logger.error(f"Google Scholar search failed: {e}")
            return []
    
    async def perform_research(self, request: ResearchRequest) -> dict:
        """Perform comprehensive research on a topic."""
        results = {
            "topic": request.topic,
            "sources": {},
            "synthesis": ""
        }
        
        # Search each source
        if "arxiv" in request.sources:
            results["sources"]["arxiv"] = await self.search_arxiv(
                request.topic, request.max_papers
            )
        
        if "scholar" in request.sources:
            results["sources"]["scholar"] = await self.search_scholar(
                request.topic, request.max_papers
            )
        
        # Synthesize findings using LLM
        all_papers = []
        for source, papers in results["sources"].items():
            all_papers.extend(papers)
        
        if all_papers:
            synthesis_prompt = f"""
            Research Topic: {request.topic}
            
            Papers Found:
            {json.dumps(all_papers[:10], indent=2)}
            
            Please synthesize the key findings from these papers into a coherent
            summary. Identify:
            1. Main themes and consensus views
            2. Contradictions or debates
            3. Research gaps
            4. Novel insights
            """
            
            results["synthesis"] = await self.query_llm(
                synthesis_prompt,
                system_prompt="You are a research synthesis agent specializing in academic literature review."
            )
        
        return results
    
    # ═══════════════════════════════════════════════════════════════════════════
    # Game Functions
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def start_game(self, request: GameStartRequest) -> GameState:
        """Start a new adversarial research game."""
        import uuid
        
        game_id = str(uuid.uuid4())
        game = GameState(
            game_id=game_id,
            game_type=request.game_type,
            participants=[self.config.agent_position, request.opponent_id],
            scores={
                self.config.agent_position: 0,
                request.opponent_id: 0
            }
        )
        
        self.current_games[game_id] = game
        logger.info(f"Started game {game_id}: {request.game_type.value}")
        
        return game
    
    async def make_move(self, request: MoveRequest) -> GameMove:
        """Make a move in an active game."""
        if request.game_id not in self.current_games:
            raise ValueError(f"Game {request.game_id} not found")
        
        game = self.current_games[request.game_id]
        
        # Calculate points based on move type
        points = 0
        if request.move_type == MoveType.CITE_PAPER:
            # Verify citation exists and is relevant
            points = 5 if request.citation_doi else 2
        elif request.move_type == MoveType.MAKE_CLAIM:
            points = 3
        elif request.move_type == MoveType.REFUTE_CLAIM:
            points = 10
        elif request.move_type == MoveType.SYNTHESIZE:
            points = 15
        
        move = GameMove(
            move_type=request.move_type,
            action=request.action,
            claim=request.claim,
            citation_doi=request.citation_doi,
            points_earned=points
        )
        
        game.moves.append(move)
        game.scores[self.config.agent_position] += points
        game.current_turn += 1
        
        # Update metrics
        MOVES_MADE.labels(move_type=request.move_type.value).inc()
        AGENT_SCORE.labels(
            layer=str(self.config.board_layer),
            position=self.config.chess_notation
        ).set(game.scores[self.config.agent_position])
        
        logger.info(f"Move made in game {request.game_id}: {request.move_type.value}")
        
        return move
    
    # ═══════════════════════════════════════════════════════════════════════════
    # Echolocation (Agent Discovery)
    # ═══════════════════════════════════════════════════════════════════════════
    
    def get_harmonic_frequencies(self) -> dict[str, float]:
        """Calculate harmonically related frequencies (Circle of 5ths)."""
        base = self.config.frequency_hz
        return {
            "unison": base,
            "minor_second": base * (16/15),
            "major_second": base * (9/8),
            "minor_third": base * (6/5),
            "major_third": base * (5/4),
            "perfect_fourth": base * (4/3),
            "tritone": base * (45/32),
            "perfect_fifth": base * (3/2),
            "minor_sixth": base * (8/5),
            "major_sixth": base * (5/3),
            "minor_seventh": base * (9/5),
            "major_seventh": base * (15/8),
            "octave": base * 2
        }
    
    async def echolocate(self, request: EcholocationRequest) -> list[dict]:
        """Find agents at harmonically compatible frequencies."""
        harmonics = self.get_harmonic_frequencies()
        target_freq = harmonics.get(request.target_interval, harmonics["perfect_fifth"])
        
        # In production, this would query the game orchestrator
        # to find agents with matching frequencies
        compatible_agents = []
        
        # Calculate which agent positions match the target frequency
        for board in range(10):
            for row in range(8):
                for col in range(8):
                    freq = AgentConfig.calculate_frequency(board, row, col)
                    # Check if frequency is within 1% of target
                    if abs(freq - target_freq) / target_freq < 0.01:
                        compatible_agents.append({
                            "board": board,
                            "row": row,
                            "col": col,
                            "frequency_hz": freq,
                            "interval": request.target_interval
                        })
        
        logger.info(
            f"Echolocation found {len(compatible_agents)} compatible agents "
            f"at {request.target_interval} ({target_freq:.2f} Hz)"
        )
        
        return compatible_agents


# ═══════════════════════════════════════════════════════════════════════════════
# FastAPI Application
# ═══════════════════════════════════════════════════════════════════════════════

config = AgentConfig()
agent: Optional[ChessAgent] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    global agent
    agent = ChessAgent(config)
    logger.info("Chess Agent started")
    yield
    await agent.close()
    logger.info("Chess Agent stopped")


app = FastAPI(
    title="10D Chess Council Agent",
    description="AI Research Agent for adversarial synthesis games",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        agent_id=config.agent_position,
        layer=config.board_layer,
        position=config.chess_notation,
        frequency_hz=config.frequency_hz
    )


@app.get("/ready", response_model=ReadyResponse)
async def readiness_check():
    """Readiness check endpoint."""
    ollama_ok = False
    qdrant_ok = False
    
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(f"{config.ollama_host}/api/version")
            ollama_ok = resp.status_code == 200
    except Exception:
        pass
    
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(f"{config.qdrant_url}/health")
            qdrant_ok = resp.status_code == 200
    except Exception:
        pass
    
    return ReadyResponse(
        ready=ollama_ok,  # Minimum requirement
        ollama_connected=ollama_ok,
        qdrant_connected=qdrant_ok
    )


@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    return JSONResponse(
        content=generate_latest().decode("utf-8"),
        media_type=CONTENT_TYPE_LATEST
    )


@app.post("/research")
async def research(request: ResearchRequest):
    """Perform research on a topic."""
    if not agent:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    return await agent.perform_research(request)


@app.post("/game/start")
async def start_game(request: GameStartRequest):
    """Start a new adversarial research game."""
    if not agent:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    game = await agent.start_game(request)
    return {"game_id": game.game_id, "status": game.status}


@app.post("/game/move")
async def make_move(request: MoveRequest):
    """Make a move in an active game."""
    if not agent:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    try:
        move = await agent.make_move(request)
        return {
            "move_type": move.move_type.value,
            "points_earned": move.points_earned,
            "timestamp": move.timestamp.isoformat()
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/echolocate")
async def echolocate(request: EcholocationRequest):
    """Find harmonically compatible agents."""
    if not agent:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    return await agent.echolocate(request)


@app.get("/harmonics")
async def get_harmonics():
    """Get all harmonic frequencies for this agent."""
    if not agent:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    return agent.get_harmonic_frequencies()


@app.get("/info")
async def agent_info():
    """Get agent information."""
    return {
        "agent_id": config.agent_position,
        "board_layer": config.board_layer,
        "layer_name": config.layer_name,
        "chess_notation": config.chess_notation,
        "frequency_hz": config.frequency_hz,
        "row": config.row,
        "col": config.col,
        "model": config.primary_model
    }


# ═══════════════════════════════════════════════════════════════════════════════
# Main Entry Point
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080,
        log_level="info"
    )
