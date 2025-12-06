"""
FlameLang Glyph Registry
Frequency-based symbolic execution system
"""

# Solfeggio frequencies + fine-structure constant
FREQUENCIES = {
    'alpha': 137,      # Fine-structure constant (1/137)
    'defense': 137,    # Boundaries/sovereignty
    'coherence': 432,  # Flow/harmony
    'transform': 528,  # DNA repair/transformation
    'evolution': 741,  # Problem solving/change
    'unity': 963,      # Higher consciousness
}

# Glyph Registry - 17 glyphs as specified
GLYPH_REGISTRY = {
    # Core glyphs (6)
    '⚡': {
        'name': 'execute',
        'symbol': '⚡',
        'frequency': 528,
        'description': 'Execute/Energy',
        'category': 'core',
    },
    '🔥': {
        'name': 'flame',
        'symbol': '🔥',
        'frequency': 528,
        'description': 'Transform/Flame',
        'category': 'core',
    },
    '🌊': {
        'name': 'ocean',
        'symbol': '🌊',
        'frequency': 432,
        'description': 'Flow/Ocean',
        'category': 'core',
    },
    '⚛️': {
        'name': 'atom',
        'symbol': '⚛️',
        'frequency': 741,
        'description': 'Quantum/Atom',
        'category': 'core',
    },
    '🎯': {
        'name': 'target',
        'symbol': '🎯',
        'frequency': 963,
        'description': 'Focus/Target',
        'category': 'core',
    },
    '🔮': {
        'name': 'oracle',
        'symbol': '🔮',
        'frequency': 963,
        'description': 'Prediction/Oracle',
        'category': 'core',
    },
    
    # Physics glyphs (6)
    'BH1': {
        'name': 'black_hole',
        'symbol': 'BH1',
        'frequency': 137,
        'description': 'Schwarzschild Black Hole',
        'category': 'physics',
    },
    'OC1': {
        'name': 'ocean_eddy',
        'symbol': 'OC1',
        'frequency': 432,
        'description': 'Ocean Eddy Circulation',
        'category': 'physics',
    },
    'PS1': {
        'name': 'photon_sphere',
        'symbol': 'PS1',
        'frequency': 741,
        'description': 'Photon Sphere',
        'category': 'physics',
    },
    'GR1': {
        'name': 'general_relativity',
        'symbol': 'GR1',
        'frequency': 963,
        'description': 'General Relativity Metric',
        'category': 'physics',
    },
    'ED1': {
        'name': 'eddy',
        'symbol': 'ED1',
        'frequency': 432,
        'description': 'Eddy Detection',
        'category': 'physics',
    },
    'MT1': {
        'name': 'metric_tensor',
        'symbol': 'MT1',
        'frequency': 528,
        'description': 'Metric Tensor',
        'category': 'physics',
    },
    
    # Security glyphs (5)
    '🛡️': {
        'name': 'shield',
        'symbol': '🛡️',
        'frequency': 137,
        'description': 'Defense/Shield',
        'category': 'security',
    },
    '🔒': {
        'name': 'lock',
        'symbol': '🔒',
        'frequency': 137,
        'description': 'Encryption/Lock',
        'category': 'security',
    },
    '👁️': {
        'name': 'eye',
        'symbol': '👁️',
        'frequency': 137,
        'description': 'Surveillance/Monitor',
        'category': 'security',
    },
    '⚔️': {
        'name': 'sword',
        'symbol': '⚔️',
        'frequency': 137,
        'description': 'Attack/Sword',
        'category': 'security',
    },
    '🌐': {
        'name': 'network',
        'symbol': '🌐',
        'frequency': 432,
        'description': 'Network/Globe',
        'category': 'security',
    },
}


def get_glyph(symbol):
    """Retrieve glyph information by symbol"""
    return GLYPH_REGISTRY.get(symbol, None)


def register_glyph(symbol, name, frequency, description, category):
    """Register a new glyph"""
    GLYPH_REGISTRY[symbol] = {
        'name': name,
        'symbol': symbol,
        'frequency': frequency,
        'description': description,
        'category': category,
    }


def list_glyphs_by_category(category=None):
    """List glyphs, optionally filtered by category"""
    if category:
        return {k: v for k, v in GLYPH_REGISTRY.items() if v['category'] == category}
    return GLYPH_REGISTRY


def get_glyph_frequency(symbol):
    """Get the frequency of a glyph"""
    glyph = get_glyph(symbol)
    return glyph['frequency'] if glyph else None
