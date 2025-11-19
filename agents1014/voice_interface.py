"""
Voice Interface for TRS Multi-Agent Chess System
Local voice input (Whisper) and output (Piper-TTS)
100% local, sovereign architecture
"""

import asyncio
import wave
import struct
import threading
from typing import Optional, Callable
import structlog

try:
    import whisper
except ImportError:
    print("Warning: whisper not installed. Install with: pip install openai-whisper")
    whisper = None

try:
    import sounddevice as sd
    import soundfile as sf
except ImportError:
    print("Warning: sounddevice/soundfile not installed")
    sd = None
    sf = None

import numpy as np
from pathlib import Path


logger = structlog.get_logger()


class VoiceInterface:
    """
    Handles voice input and output for the agent system
    Input: Whisper (local speech-to-text)
    Output: Piper-TTS (local text-to-speech)
    """
    
    def __init__(
        self,
        whisper_model: str = "base",
        sample_rate: int = 16000,
        enable_voice_output: bool = True,
        enable_voice_input: bool = True
    ):
        self.whisper_model_name = whisper_model
        self.sample_rate = sample_rate
        self.enable_voice_output = enable_voice_output
        self.enable_voice_input = enable_voice_input
        
        self.whisper_model = None
        self.recording = False
        self.audio_buffer = []
        
        logger.info(
            "voice_interface_initialized",
            whisper_model=whisper_model,
            voice_output=enable_voice_output,
            voice_input=enable_voice_input
        )
    
    async def initialize(self):
        """Initialize voice models"""
        if self.enable_voice_input and whisper is not None:
            try:
                logger.info("loading_whisper_model", model=self.whisper_model_name)
                self.whisper_model = whisper.load_model(self.whisper_model_name)
                logger.info("whisper_model_loaded")
            except Exception as e:
                logger.error("whisper_load_failed", error=str(e))
                self.enable_voice_input = False
        
        # Note: Piper-TTS initialization would go here
        # For now, we'll use a simpler TTS approach or text output
        if self.enable_voice_output:
            logger.info("voice_output_enabled", method="text_fallback")
    
    async def start_listening(self, callback: Optional[Callable[[str], None]] = None):
        """
        Start listening for voice commands
        Calls callback with transcribed text when speech is detected
        """
        if not self.enable_voice_input or self.whisper_model is None:
            logger.warning("voice_input_not_available")
            return
        
        if sd is None:
            logger.error("sounddevice_not_available")
            return
        
        self.recording = True
        
        logger.info("starting_voice_input")
        
        # Run recording in a separate thread
        def record_audio():
            duration = 5  # Record in 5-second chunks
            
            while self.recording:
                try:
                    logger.debug("recording_audio_chunk")
                    
                    # Record audio
                    audio = sd.rec(
                        int(duration * self.sample_rate),
                        samplerate=self.sample_rate,
                        channels=1,
                        dtype=np.float32
                    )
                    sd.wait()
                    
                    # Check if audio has significant content
                    if np.max(np.abs(audio)) > 0.01:  # Simple voice activity detection
                        # Transcribe with Whisper
                        audio_flat = audio.flatten()
                        result = self.whisper_model.transcribe(
                            audio_flat,
                            language="en",
                            fp16=False
                        )
                        
                        text = result["text"].strip()
                        
                        if text and callback:
                            logger.info("voice_transcribed", text=text)
                            callback(text)
                    
                except Exception as e:
                    logger.error("recording_error", error=str(e))
                    import time
                    time.sleep(1)
        
        # Start recording thread
        self.record_thread = threading.Thread(target=record_audio, daemon=True)
        self.record_thread.start()
    
    def stop_listening(self):
        """Stop listening for voice commands"""
        self.recording = False
        logger.info("voice_input_stopped")
    
    async def speak(self, text: str, agent_id: Optional[int] = None):
        """
        Speak text using TTS
        In full implementation, this would use Piper-TTS
        For now, logs the text
        """
        if not self.enable_voice_output:
            return
        
        prefix = f"[Agent {agent_id}]" if agent_id is not None else "[System]"
        logger.info("voice_output", agent=agent_id, text=text)
        
        # In production, this would:
        # 1. Call Piper-TTS to generate audio
        # 2. Play audio through speakers
        # For now, we just log it
        print(f"{prefix} {text}")
        
        # Simulate speaking time
        await asyncio.sleep(len(text) / 50)  # ~50 chars per second
    
    async def process_voice_command(self, text: str) -> dict:
        """
        Parse voice command for chess moves
        Expected format: "knight to e4 layer 7 ionian"
        """
        text = text.lower().strip()
        
        result = {
            "valid": False,
            "move": None,
            "layer": None,
            "mode": None,
        }
        
        # Extract move (simple pattern matching)
        # Format: "[piece] to [square]" or just "[square]"
        words = text.split()
        
        # Look for "to" keyword
        if "to" in words:
            to_idx = words.index("to")
            if to_idx + 1 < len(words):
                square = words[to_idx + 1]
                
                # Simple validation: square should be like "e4", "a1", etc.
                if len(square) == 2 and square[0] in 'abcdefgh' and square[1] in '12345678':
                    result["move"] = square
                    result["valid"] = True
        
        # Extract layer number
        if "layer" in words:
            layer_idx = words.index("layer")
            if layer_idx + 1 < len(words):
                try:
                    layer = int(words[layer_idx + 1])
                    result["layer"] = layer
                except ValueError:
                    pass
        
        # Extract mode
        modes = [
            "ionian", "dorian", "phrygian", "lydian",
            "mixolydian", "aeolian", "locrian",
            "hyperion", "prometheus", "atlantean"
        ]
        for mode in modes:
            if mode in text:
                result["mode"] = mode
                break
        
        logger.debug("voice_command_parsed", result=result)
        
        return result
    
    async def announce_game_start(self, num_agents: int):
        """Announce the start of the tournament"""
        text = (
            f"Initializing TRS Multi-Agent Chess Tournament. "
            f"{num_agents} agents are preparing for battle across {num_agents} dimensional layers. "
            f"May the best mode prevail."
        )
        await self.speak(text)
    
    async def announce_move(
        self,
        agent_id: int,
        layer: int,
        move: str,
        commentary: str
    ):
        """Announce a move with agent commentary"""
        text = f"Layer {layer}, Agent {agent_id}: {move}. {commentary}"
        await self.speak(text, agent_id=agent_id)
    
    async def announce_game_over(
        self,
        winner_id: Optional[int],
        reason: str
    ):
        """Announce game over"""
        if winner_id is not None:
            text = f"Game over. Agent {winner_id} is victorious. {reason}"
        else:
            text = f"Game over. {reason}"
        
        await self.speak(text)
    
    def get_status(self) -> dict:
        """Get current status of voice interface"""
        return {
            "voice_input_enabled": self.enable_voice_input,
            "voice_output_enabled": self.enable_voice_output,
            "whisper_loaded": self.whisper_model is not None,
            "recording": self.recording,
        }
    
    async def shutdown(self):
        """Cleanup resources"""
        self.stop_listening()
        logger.info("voice_interface_shutdown")


class VoiceCommandHandler:
    """
    Handles incoming voice commands and routes them to appropriate handlers
    """
    
    def __init__(self, voice_interface: VoiceInterface):
        self.voice = voice_interface
        self.command_handlers = {}
    
    def register_handler(self, command: str, handler: Callable):
        """Register a handler for a specific command"""
        self.command_handlers[command] = handler
    
    async def handle_command(self, text: str):
        """Process a voice command"""
        parsed = await self.voice.process_voice_command(text)
        
        if not parsed["valid"]:
            await self.voice.speak("Command not recognized. Please try again.")
            return
        
        # Route to appropriate handler
        if "move" in text:
            handler = self.command_handlers.get("move")
            if handler:
                await handler(parsed)
        elif "status" in text:
            handler = self.command_handlers.get("status")
            if handler:
                await handler()
        elif "stop" in text or "pause" in text:
            handler = self.command_handlers.get("stop")
            if handler:
                await handler()
    
    async def start(self):
        """Start listening for commands"""
        def callback(text: str):
            asyncio.create_task(self.handle_command(text))
        
        await self.voice.start_listening(callback)
