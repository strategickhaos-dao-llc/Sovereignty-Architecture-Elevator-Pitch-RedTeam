"""
Virtual Machine for StrategicKhaos.
Executes AST nodes directly (interpreter mode).
"""

from .interpreter import Interpreter, InterpreterError

__all__ = ['Interpreter', 'InterpreterError']
