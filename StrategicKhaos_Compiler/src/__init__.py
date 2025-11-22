"""
StrategicKhaos Compiler
A programming language that embraces chaos as a feature.

Version: 0.0.1-alpha.chaos
Born: 2025-11-21
"""

__version__ = '0.0.1-alpha.chaos'
__author__ = 'StrategicKhaos Collective'
__license__ = 'MIT'

# Package metadata
VERSION_INFO = {
    'major': 0,
    'minor': 0,
    'patch': 1,
    'stage': 'alpha',
    'chaos_level': 'controlled'
}

def get_version():
    """Return the version string."""
    return __version__

def get_chaos_level():
    """Return the current chaos level of the compiler."""
    return VERSION_INFO['chaos_level']
