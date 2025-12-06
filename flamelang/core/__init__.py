"""FlameLang Core Components"""
try:
    from .lexer import Lexer, Token, TokenType
    from .compiler import FlameLangCompiler
    from .repl import REPL
except ImportError:
    # When run as script
    pass

__all__ = ['Lexer', 'Token', 'TokenType', 'FlameLangCompiler', 'REPL']
