"""
FlameLang Interpreter v2.0
Executes FlameLang glyph sequences with frequency-based resonance.

The interpreter processes glyph sequences and executes their
associated operations based on binding codes and frequency mappings.
"""

import json
import logging
from typing import Any, Callable
from dataclasses import dataclass, field

from .glyph_table import GlyphTable, Glyph
from .binding_codes import BINDING_CODES, BindingCode, get_binding_code

logger = logging.getLogger(__name__)


@dataclass
class ExecutionContext:
    """Context for glyph execution with state tracking."""
    
    variables: dict[str, Any] = field(default_factory=dict)
    stack: list[Any] = field(default_factory=list)
    frequency_accumulator: float = 0.0
    binding_history: list[int] = field(default_factory=list)
    execution_log: list[str] = field(default_factory=list)
    
    def log(self, message: str) -> None:
        """Add a message to the execution log."""
        self.execution_log.append(message)
        logger.debug(message)
    
    def push(self, value: Any) -> None:
        """Push a value onto the stack."""
        self.stack.append(value)
    
    def pop(self) -> Any:
        """Pop a value from the stack."""
        if self.stack:
            return self.stack.pop()
        return None
    
    def peek(self) -> Any:
        """Peek at the top of the stack."""
        if self.stack:
            return self.stack[-1]
        return None


@dataclass
class ExecutionResult:
    """Result of executing a FlameLang sequence."""
    
    success: bool
    output: Any
    context: ExecutionContext
    total_whale_freq: float
    total_piano_freq: float
    binding_sequence: list[int]
    error: str | None = None


class FlameLangInterpreter:
    """
    FlameLang Interpreter v2.0
    
    Executes glyph sequences with frequency-based resonance tracking.
    Supports both symbol-based and binding code-based execution.
    """
    
    VERSION = "2.0.0"
    
    def __init__(self):
        """Initialize the interpreter with a fresh glyph table."""
        self.glyph_table = GlyphTable()
        self._handlers: dict[str, Callable[[ExecutionContext, Glyph], Any]] = {}
        self._register_default_handlers()
    
    def _register_default_handlers(self) -> None:
        """Register default glyph operation handlers."""
        # Fire domain handlers
        self._handlers["IGNITE"] = self._handle_ignite
        self._handlers["SPARK"] = self._handle_spark
        self._handlers["RADIATE"] = self._handle_radiate
        self._handlers["MANIFEST"] = self._handle_manifest
        
        # Water domain handlers
        self._handlers["FLOW"] = self._handle_flow
        self._handlers["VORTEX"] = self._handle_vortex
        self._handlers["CRYSTALLIZE"] = self._handle_crystallize
        
        # Earth domain handlers
        self._handlers["GROUND"] = self._handle_ground
        self._handlers["ANCHOR"] = self._handle_anchor
        self._handlers["ROOT"] = self._handle_root
        
        # Air domain handlers
        self._handlers["TRANSMIT"] = self._handle_transmit
        self._handlers["BREATHE"] = self._handle_breathe
        self._handlers["SCATTER"] = self._handle_scatter
        
        # Void domain handlers
        self._handlers["VOID"] = self._handle_void
        self._handlers["PORTAL"] = self._handle_portal
        self._handlers["INFINITE"] = self._handle_infinite
        self._handlers["OMEGA"] = self._handle_omega
    
    def register_handler(self, operation: str, handler: Callable[[ExecutionContext, Glyph], Any]) -> None:
        """Register a custom handler for a glyph operation."""
        self._handlers[operation] = handler
    
    def parse(self, source: str) -> list[Glyph]:
        """
        Parse a FlameLang source string into a sequence of glyphs.
        
        Supports:
        - Direct symbol sequences: "🔥⚡🌊"
        - Named operations: "IGNITE SPARK FLOW"
        - Binding code references: "[137] [666]"
        """
        glyphs = []
        tokens = source.split()
        
        for token in tokens:
            # Try as binding code reference [XXX]
            if token.startswith("[") and token.endswith("]"):
                try:
                    code = int(token[1:-1])
                    code_glyphs = self.glyph_table.get_by_binding_code(code)
                    if code_glyphs:
                        glyphs.append(code_glyphs[0])  # Use first glyph of binding
                except ValueError:
                    pass
                continue
            
            # Try as symbol
            glyph = self.glyph_table.get_by_symbol(token)
            if glyph:
                glyphs.append(glyph)
                continue
            
            # Try as operation name
            for g in self.glyph_table:
                if g.name == token.upper():
                    glyphs.append(g)
                    break
            else:
                # Check each character as potential symbol
                for char in token:
                    glyph = self.glyph_table.get_by_symbol(char)
                    if glyph:
                        glyphs.append(glyph)
        
        return glyphs
    
    def execute(self, source: str | list[Glyph], context: ExecutionContext = None) -> ExecutionResult:
        """
        Execute a FlameLang sequence.
        
        Args:
            source: Either a source string or pre-parsed glyph list
            context: Optional execution context (created if not provided)
            
        Returns:
            ExecutionResult with output and metadata
        """
        if context is None:
            context = ExecutionContext()
        
        # Parse if string
        if isinstance(source, str):
            glyphs = self.parse(source)
        else:
            glyphs = source
        
        if not glyphs:
            return ExecutionResult(
                success=False,
                output=None,
                context=context,
                total_whale_freq=0.0,
                total_piano_freq=0.0,
                binding_sequence=[],
                error="No valid glyphs found in source"
            )
        
        total_whale = 0.0
        total_piano = 0.0
        binding_sequence = []
        output = None
        error = None
        
        try:
            for glyph in glyphs:
                context.log(f"Executing: {glyph}")
                
                # Track frequencies
                total_whale += glyph.whale_freq
                total_piano += glyph.piano_freq
                context.frequency_accumulator += glyph.resonance_ratio
                
                # Track binding history
                if glyph.binding_code not in context.binding_history[-1:]:
                    context.binding_history.append(glyph.binding_code)
                binding_sequence.append(glyph.binding_code)
                
                # Execute handler if available
                handler = self._handlers.get(glyph.name)
                if handler:
                    result = handler(context, glyph)
                    if result is not None:
                        output = result
                else:
                    # Default: push glyph info to stack
                    context.push({
                        "glyph": glyph.symbol,
                        "name": glyph.name,
                        "whale_freq": glyph.whale_freq,
                        "piano_freq": glyph.piano_freq
                    })
            
            # Final output is last stack value if no explicit output
            if output is None and context.stack:
                output = context.stack
                
        except Exception as e:
            error = str(e)
            logger.exception(f"Execution error: {e}")
        
        return ExecutionResult(
            success=error is None,
            output=output,
            context=context,
            total_whale_freq=total_whale,
            total_piano_freq=total_piano,
            binding_sequence=binding_sequence,
            error=error
        )
    
    # Default operation handlers
    
    def _handle_ignite(self, ctx: ExecutionContext, glyph: Glyph) -> Any:
        """Initialize a new process or creation."""
        ctx.variables["ignited"] = True
        ctx.log(f"🔥 IGNITE: Process initialized at {glyph.whale_freq:.2f}Hz")
        return {"status": "ignited", "frequency": glyph.whale_freq}
    
    def _handle_spark(self, ctx: ExecutionContext, glyph: Glyph) -> Any:
        """Quick activation trigger."""
        ctx.variables["spark_count"] = ctx.variables.get("spark_count", 0) + 1
        ctx.log(f"⚡ SPARK: Activation #{ctx.variables['spark_count']}")
        return None
    
    def _handle_radiate(self, ctx: ExecutionContext, glyph: Glyph) -> Any:
        """Broadcast signal to all listeners."""
        ctx.log(f"☀️ RADIATE: Broadcasting at {glyph.piano_freq:.2f}Hz")
        return {"broadcast": True, "frequency": glyph.piano_freq}
    
    def _handle_manifest(self, ctx: ExecutionContext, glyph: Glyph) -> Any:
        """Create tangible output from stack."""
        manifested = ctx.pop()
        ctx.log(f"✨ MANIFEST: Created output from stack")
        return {"manifested": manifested}
    
    def _handle_flow(self, ctx: ExecutionContext, glyph: Glyph) -> Any:
        """Enable continuous data stream."""
        ctx.variables["flow_active"] = True
        ctx.log(f"🌊 FLOW: Stream activated")
        return None
    
    def _handle_vortex(self, ctx: ExecutionContext, glyph: Glyph) -> Any:
        """Enable recursive processing."""
        depth = ctx.variables.get("vortex_depth", 0) + 1
        ctx.variables["vortex_depth"] = depth
        ctx.log(f"🌀 VORTEX: Recursion depth {depth}")
        return None
    
    def _handle_crystallize(self, ctx: ExecutionContext, glyph: Glyph) -> Any:
        """Lock current state permanently."""
        frozen_state = dict(ctx.variables)
        ctx.variables["crystallized"] = frozen_state
        ctx.log(f"❄️ CRYSTALLIZE: State locked")
        return {"crystallized": frozen_state}
    
    def _handle_ground(self, ctx: ExecutionContext, glyph: Glyph) -> Any:
        """Establish foundation."""
        ctx.variables["grounded"] = True
        ctx.log(f"🌍 GROUND: Foundation established")
        return None
    
    def _handle_anchor(self, ctx: ExecutionContext, glyph: Glyph) -> Any:
        """Permanent storage operation."""
        to_anchor = ctx.peek()
        ctx.variables["anchored"] = to_anchor
        ctx.log(f"⛰️ ANCHOR: Data anchored")
        return None
    
    def _handle_root(self, ctx: ExecutionContext, glyph: Glyph) -> Any:
        """Deep system access."""
        ctx.variables["root_access"] = True
        ctx.log(f"🌲 ROOT: Deep access granted")
        return None
    
    def _handle_transmit(self, ctx: ExecutionContext, glyph: Glyph) -> Any:
        """Send message."""
        message = ctx.pop()
        ctx.log(f"💨 TRANSMIT: Sending message")
        return {"transmitted": message}
    
    def _handle_breathe(self, ctx: ExecutionContext, glyph: Glyph) -> Any:
        """System heartbeat."""
        ctx.variables["heartbeat"] = ctx.variables.get("heartbeat", 0) + 1
        ctx.log(f"🌬️ BREATHE: Heartbeat #{ctx.variables['heartbeat']}")
        return None
    
    def _handle_scatter(self, ctx: ExecutionContext, glyph: Glyph) -> Any:
        """Distribute load across nodes."""
        items = ctx.stack.copy()
        ctx.stack.clear()
        ctx.log(f"🌪️ SCATTER: Distributed {len(items)} items")
        return {"scattered": items}
    
    def _handle_void(self, ctx: ExecutionContext, glyph: Glyph) -> Any:
        """Return to null state."""
        ctx.stack.clear()
        ctx.log(f"🌑 VOID: Stack cleared")
        return None
    
    def _handle_portal(self, ctx: ExecutionContext, glyph: Glyph) -> Any:
        """Create cross-dimension link."""
        ctx.variables["portal_active"] = True
        ctx.log(f"🕳️ PORTAL: Dimensional link established")
        return {"portal": True, "resonance": glyph.resonance_ratio}
    
    def _handle_infinite(self, ctx: ExecutionContext, glyph: Glyph) -> Any:
        """Enable unbounded loop."""
        ctx.variables["infinite_mode"] = True
        ctx.log(f"∞ INFINITE: Unbounded mode enabled")
        return None
    
    def _handle_omega(self, ctx: ExecutionContext, glyph: Glyph) -> Any:
        """Final termination."""
        ctx.log(f"Ω OMEGA: Final termination")
        return {
            "terminated": True,
            "final_state": dict(ctx.variables),
            "total_frequency": ctx.frequency_accumulator
        }
    
    def get_glyph_table(self) -> GlyphTable:
        """Return the glyph table."""
        return self.glyph_table
    
    def export_state(self) -> dict:
        """Export interpreter state as dictionary."""
        return {
            "version": self.VERSION,
            "registered_handlers": list(self._handlers.keys()),
            "glyph_table": self.glyph_table.to_dict()
        }
