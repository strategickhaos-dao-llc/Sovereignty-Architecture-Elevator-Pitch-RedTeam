"""
WebSocket Bridge to Unity Visualizer
Syncs TRS chess state to TRSChessBoardVisualizer.cs in Unity
"""

import asyncio
import json
from typing import Dict, List, Optional, Set
import structlog
from dataclasses import dataclass, asdict

try:
    import websockets
    from websockets.server import WebSocketServerProtocol
except ImportError:
    print("Warning: websockets not installed. Install with: pip install websockets")
    websockets = None


logger = structlog.get_logger()


@dataclass
class BoardState:
    """Represents the state of one chess board layer"""
    layer: int
    fen: str  # Forsyth-Edwards Notation
    agent_id: int
    move_count: int
    last_move: Optional[str] = None


@dataclass
class MoveEvent:
    """Represents a chess move event"""
    agent_id: int
    layer: int
    move: str  # Standard algebraic notation
    from_square: str
    to_square: str
    piece: str
    captured: Optional[str] = None
    timestamp: float = 0.0


@dataclass
class AgentState:
    """Represents the state of an agent"""
    agent_id: int
    layer: int
    mode: str
    element: str
    active: bool
    thinking: bool = False


class WebSocketBridge:
    """
    WebSocket server that bridges Python chess engine to Unity visualizer
    Sends board states, move events, and agent information
    """
    
    def __init__(self, host: str = "localhost", port: int = 8765):
        self.host = host
        self.port = port
        self.server = None
        self.clients: Set[WebSocketServerProtocol] = set()
        
        # State tracking
        self.board_states: Dict[int, BoardState] = {}
        self.agent_states: Dict[int, AgentState] = {}
        
        logger.info("websocket_bridge_initialized", host=host, port=port)
    
    async def start(self):
        """Start the WebSocket server"""
        if websockets is None:
            logger.error("websockets_not_available")
            return
        
        try:
            self.server = await websockets.serve(
                self._handle_client,
                self.host,
                self.port
            )
            logger.info("websocket_server_started", host=self.host, port=self.port)
        except Exception as e:
            logger.error("websocket_start_failed", error=str(e))
    
    async def stop(self):
        """Stop the WebSocket server"""
        if self.server:
            self.server.close()
            await self.server.wait_closed()
            logger.info("websocket_server_stopped")
    
    async def _handle_client(self, websocket: WebSocketServerProtocol, path: str):
        """Handle a new WebSocket client connection"""
        self.clients.add(websocket)
        client_id = id(websocket)
        
        logger.info("websocket_client_connected", client_id=client_id, path=path)
        
        try:
            # Send initial state to new client
            await self._send_initial_state(websocket)
            
            # Listen for messages from client
            async for message in websocket:
                await self._handle_message(websocket, message)
                
        except websockets.exceptions.ConnectionClosed:
            logger.info("websocket_client_disconnected", client_id=client_id)
        except Exception as e:
            logger.error("websocket_client_error", client_id=client_id, error=str(e))
        finally:
            self.clients.remove(websocket)
    
    async def _send_initial_state(self, websocket: WebSocketServerProtocol):
        """Send current state to a newly connected client"""
        # Send board states
        for board_state in self.board_states.values():
            await self._send_to_client(websocket, {
                "type": "board_state",
                "data": asdict(board_state)
            })
        
        # Send agent states
        for agent_state in self.agent_states.values():
            await self._send_to_client(websocket, {
                "type": "agent_state",
                "data": asdict(agent_state)
            })
    
    async def _handle_message(self, websocket: WebSocketServerProtocol, message: str):
        """Handle incoming message from client"""
        try:
            data = json.loads(message)
            msg_type = data.get("type")
            
            logger.debug("websocket_message_received", type=msg_type)
            
            if msg_type == "ping":
                await self._send_to_client(websocket, {"type": "pong"})
            
            elif msg_type == "request_state":
                await self._send_initial_state(websocket)
            
            elif msg_type == "client_ready":
                logger.info("unity_client_ready")
                await self._send_to_client(websocket, {
                    "type": "server_ready",
                    "num_layers": len(self.board_states)
                })
        
        except json.JSONDecodeError as e:
            logger.error("invalid_json_message", error=str(e))
    
    async def _send_to_client(
        self,
        websocket: WebSocketServerProtocol,
        message: dict
    ):
        """Send a message to a specific client"""
        try:
            await websocket.send(json.dumps(message))
        except Exception as e:
            logger.error("send_to_client_failed", error=str(e))
    
    async def broadcast(self, message: dict):
        """Broadcast a message to all connected clients"""
        if not self.clients:
            return
        
        message_json = json.dumps(message)
        
        # Send to all clients concurrently
        await asyncio.gather(
            *[client.send(message_json) for client in self.clients],
            return_exceptions=True
        )
        
        logger.debug("websocket_broadcast", type=message.get("type"), clients=len(self.clients))
    
    # Public API for updating state
    
    async def update_board_state(
        self,
        layer: int,
        fen: str,
        agent_id: int,
        move_count: int,
        last_move: Optional[str] = None
    ):
        """Update and broadcast board state for a layer"""
        board_state = BoardState(
            layer=layer,
            fen=fen,
            agent_id=agent_id,
            move_count=move_count,
            last_move=last_move
        )
        
        self.board_states[layer] = board_state
        
        await self.broadcast({
            "type": "board_state",
            "data": asdict(board_state)
        })
    
    async def send_move_event(self, move_event: MoveEvent):
        """Broadcast a move event"""
        await self.broadcast({
            "type": "move_event",
            "data": asdict(move_event)
        })
        
        logger.info(
            "move_event_sent",
            agent=move_event.agent_id,
            layer=move_event.layer,
            move=move_event.move
        )
    
    async def update_agent_state(
        self,
        agent_id: int,
        layer: int,
        mode: str,
        element: str,
        active: bool,
        thinking: bool = False
    ):
        """Update and broadcast agent state"""
        agent_state = AgentState(
            agent_id=agent_id,
            layer=layer,
            mode=mode,
            element=element,
            active=active,
            thinking=thinking
        )
        
        self.agent_states[agent_id] = agent_state
        
        await self.broadcast({
            "type": "agent_state",
            "data": asdict(agent_state)
        })
    
    async def send_game_event(
        self,
        event_type: str,
        data: dict
    ):
        """Send a general game event"""
        await self.broadcast({
            "type": "game_event",
            "event_type": event_type,
            "data": data
        })
    
    async def send_voice_commentary(
        self,
        agent_id: int,
        layer: int,
        text: str
    ):
        """Send voice commentary to Unity for display"""
        await self.broadcast({
            "type": "voice_commentary",
            "data": {
                "agent_id": agent_id,
                "layer": layer,
                "text": text
            }
        })
    
    async def send_phase_angles(self, phase_angles: Dict[int, float]):
        """Send phase angles for all layers (for visualization)"""
        await self.broadcast({
            "type": "phase_angles",
            "data": phase_angles
        })
    
    async def send_mobius_transform(
        self,
        layer: int,
        transform_data: dict
    ):
        """Send Möbius transform visualization data"""
        await self.broadcast({
            "type": "mobius_transform",
            "layer": layer,
            "data": transform_data
        })
    
    def get_status(self) -> dict:
        """Get current bridge status"""
        return {
            "running": self.server is not None,
            "host": self.host,
            "port": self.port,
            "connected_clients": len(self.clients),
            "active_boards": len(self.board_states),
            "active_agents": len(self.agent_states),
        }


class UnityMessageProtocol:
    """
    Defines the message protocol between Python and Unity
    Documents expected message formats
    """
    
    @staticmethod
    def board_state_message(layer: int, fen: str, agent_id: int) -> dict:
        """Format: Board state update"""
        return {
            "type": "board_state",
            "data": {
                "layer": layer,
                "fen": fen,
                "agent_id": agent_id
            }
        }
    
    @staticmethod
    def move_event_message(
        agent_id: int,
        layer: int,
        move: str,
        from_sq: str,
        to_sq: str
    ) -> dict:
        """Format: Chess move event"""
        return {
            "type": "move_event",
            "data": {
                "agent_id": agent_id,
                "layer": layer,
                "move": move,
                "from": from_sq,
                "to": to_sq
            }
        }
    
    @staticmethod
    def agent_thinking_message(agent_id: int, thinking: bool) -> dict:
        """Format: Agent thinking status"""
        return {
            "type": "agent_state",
            "data": {
                "agent_id": agent_id,
                "thinking": thinking
            }
        }
