"""
36 Vectorization Algorithms for Linguistic Sovereignty Framework.

Each algorithm contributes to the 36-dimensional vector space used for
cryptographic glyph mapping and Kubernetes namespace naming.

Algorithm Categories:
- Dimensions 0-7:   Geometric features
- Dimensions 8-15:  Phonetic features  
- Dimensions 16-23: Hebrew correlation matrix
- Dimensions 24-31: Egyptian correlation matrix
- Dimensions 32-35: Cryptographic hash features
"""

import hashlib
import math
from typing import List, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from .glyph import Glyph

# Phoneme encoding table for dimension 8-15
PHONEME_ENCODING = {
    "a": 0.1, "e": 0.15, "i": 0.2, "o": 0.25, "u": 0.3,
    "da": 0.35, "ta": 0.4, "ro": 0.45, "lo": 0.5, "pa": 0.55,
    "ba": 0.6, "ma": 0.65, "na": 0.7, "ka": 0.75, "ga": 0.8,
    "sa": 0.85, "za": 0.9, "wa": 0.95, "ya": 1.0
}

# Hebrew letter gematria values
HEBREW_GEMATRIA = {
    "aleph": 1, "bet": 2, "gimel": 3, "dalet": 4, "he": 5,
    "vav": 6, "zayin": 7, "chet": 8, "tet": 9, "yod": 10,
    "kaf": 20, "lamed": 30, "mem": 40, "nun": 50, "samekh": 60,
    "ayin": 70, "pe": 80, "tsadi": 90, "qoph": 100, "resh": 200,
    "shin": 300, "tav": 400
}

# Hebrew letters ordered by index
HEBREW_LETTERS = list(HEBREW_GEMATRIA.keys())


class GlyphAlgorithms:
    """Collection of 36 algorithms for glyph vectorization."""
    
    # ═══════════════════════════════════════════════════════════
    # GEOMETRIC FEATURES (Dimensions 0-7)
    # ═══════════════════════════════════════════════════════════
    
    @staticmethod
    def calculate_stroke_count(pattern: List[Tuple[int, int]]) -> float:
        """Algorithm 0: Count of stroke coordinates."""
        return float(len(pattern)) if pattern else 0.0
    
    @staticmethod
    def calculate_symmetry(pattern: List[Tuple[int, int]]) -> float:
        """Algorithm 1: Geometric symmetry measure.
        
        Calculates reflection symmetry across x=0, y=0, y=x, y=-x axes.
        """
        if not pattern or len(pattern) < 2:
            return 0.5
        
        symmetries = []
        
        # Reflection symmetry across x-axis
        x_reflected = [(x, -y) for x, y in pattern]
        symmetries.append(GlyphAlgorithms._pattern_similarity(pattern, x_reflected))
        
        # Reflection symmetry across y-axis
        y_reflected = [(-x, y) for x, y in pattern]
        symmetries.append(GlyphAlgorithms._pattern_similarity(pattern, y_reflected))
        
        # Reflection symmetry across y=x (diagonal)
        diag_reflected = [(y, x) for x, y in pattern]
        symmetries.append(GlyphAlgorithms._pattern_similarity(pattern, diag_reflected))
        
        # Reflection symmetry across y=-x (anti-diagonal)
        anti_diag_reflected = [(-y, -x) for x, y in pattern]
        symmetries.append(GlyphAlgorithms._pattern_similarity(pattern, anti_diag_reflected))
        
        return sum(symmetries) / len(symmetries)
    
    @staticmethod
    def _pattern_similarity(p1: List[Tuple[int, int]], 
                           p2: List[Tuple[int, int]]) -> float:
        """Calculate similarity between two patterns."""
        if not p1 or not p2:
            return 0.0
        
        # Count matching points
        set1 = set(p1)
        set2 = set(p2)
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        
        return intersection / union if union > 0 else 0.0
    
    @staticmethod
    def calculate_angular_momentum(pattern: List[Tuple[int, int]]) -> float:
        """Algorithm 2: Rotational inertia tensor.
        
        Measures the moment of inertia around the centroid.
        """
        if not pattern:
            return 0.0
        
        # Calculate centroid
        cx = sum(p[0] for p in pattern) / len(pattern)
        cy = sum(p[1] for p in pattern) / len(pattern)
        
        # Calculate moment of inertia
        moment = sum((p[0] - cx) ** 2 + (p[1] - cy) ** 2 for p in pattern)
        return moment / len(pattern) if pattern else 0.0
    
    @staticmethod
    def calculate_centroid_x(pattern: List[Tuple[int, int]]) -> float:
        """Algorithm 3: X-coordinate of centroid."""
        if not pattern:
            return 0.0
        return sum(p[0] for p in pattern) / len(pattern)
    
    @staticmethod
    def calculate_centroid_y(pattern: List[Tuple[int, int]]) -> float:
        """Algorithm 4: Y-coordinate of centroid."""
        if not pattern:
            return 0.0
        return sum(p[1] for p in pattern) / len(pattern)
    
    @staticmethod
    def calculate_bounding_box_ratio(pattern: List[Tuple[int, int]]) -> float:
        """Algorithm 5: Aspect ratio of bounding box."""
        if not pattern or len(pattern) < 2:
            return 1.0
        
        xs = [p[0] for p in pattern]
        ys = [p[1] for p in pattern]
        
        width = max(xs) - min(xs)
        height = max(ys) - min(ys)
        
        if height == 0:
            return 1.0
        return width / height if height != 0 else float(width) if width > 0 else 1.0
    
    @staticmethod
    def calculate_fractal_dimension(pattern: List[Tuple[int, int]]) -> float:
        """Algorithm 6: Box-counting fractal dimension.
        
        Estimates fractal dimension using simplified box-counting method.
        """
        if len(pattern) < 2:
            return 1.0
        
        scales = [1, 2, 4, 8]
        counts = []
        
        for scale in scales:
            boxes = set()
            for x, y in pattern:
                boxes.add((x // scale, y // scale))
            counts.append(max(1, len(boxes)))
        
        # Linear regression in log-log space
        log_scales = [math.log(s) for s in scales]
        log_counts = [math.log(c) for c in counts]
        
        # Calculate slope using least squares
        n = len(scales)
        sum_x = sum(log_scales)
        sum_y = sum(log_counts)
        sum_xy = sum(x * y for x, y in zip(log_scales, log_counts))
        sum_x2 = sum(x * x for x in log_scales)
        
        denominator = n * sum_x2 - sum_x * sum_x
        if denominator == 0:
            return 1.0
        
        slope = (n * sum_xy - sum_x * sum_y) / denominator
        return -slope
    
    @staticmethod
    def calculate_topological_genus(pattern: List[Tuple[int, int]]) -> float:
        """Algorithm 7: Topological genus estimate.
        
        Estimates the number of holes in the glyph shape.
        Uses Euler characteristic: V - E + F = 2 - 2g (for genus g)
        """
        if len(pattern) < 3:
            return 0.0
        
        # Simplified estimation based on pattern complexity
        # More complex patterns tend to have higher genus
        vertices = len(pattern)
        edges = vertices - 1  # Simplified: assuming connected path
        faces = 1  # Simplified: single bounded region
        
        euler = vertices - edges + faces
        genus = max(0.0, (2 - euler) / 2)
        return genus
    
    # ═══════════════════════════════════════════════════════════
    # PHONETIC FEATURES (Dimensions 8-15)
    # ═══════════════════════════════════════════════════════════
    
    @staticmethod
    def encode_phoneme(phoneme: str) -> float:
        """Algorithm 8-15: Encode phoneme to numeric value."""
        if not phoneme:
            return 0.0
        return PHONEME_ENCODING.get(phoneme.lower(), 0.5)
    
    @staticmethod
    def encode_phoneme_list(hypotheses: List[str], index: int) -> float:
        """Get phoneme encoding at specific index."""
        if index < len(hypotheses):
            return GlyphAlgorithms.encode_phoneme(hypotheses[index])
        return 0.0
    
    # ═══════════════════════════════════════════════════════════
    # HEBREW CORRELATION MATRIX (Dimensions 16-23)
    # ═══════════════════════════════════════════════════════════
    
    @staticmethod
    def hebrew_gematria_value(glyph: "Glyph") -> float:
        """Algorithm 17: Hebrew numerical mysticism correlation.
        
        Maps glyph to Hebrew gematria system (1-900, normalized).
        """
        vec_sum = sum(ord(c) for c in glyph.symbol)
        return (vec_sum % 900) / 900
    
    @staticmethod
    def hebrew_root_pattern(glyph: "Glyph") -> float:
        """Algorithm 18: Hebrew triliteral root pattern correlation.
        
        Hebrew words typically derive from 3-letter roots.
        """
        # Map stroke count to root pattern probability
        strokes = len(glyph.geometric_pattern)
        if strokes == 3:
            return 1.0  # Perfect triliteral match
        return max(0.0, 1.0 - abs(strokes - 3) * 0.2)
    
    @staticmethod
    def hebrew_shape_similarity(glyph: "Glyph") -> float:
        """Algorithm 19: Visual similarity to Hebrew letters.
        
        Based on angular vs. curved stroke patterns.
        """
        if not glyph.geometric_pattern:
            return 0.5
        
        # Count angular changes
        pattern = glyph.geometric_pattern
        if len(pattern) < 3:
            return 0.5
        
        angles = 0
        for i in range(1, len(pattern) - 1):
            dx1 = pattern[i][0] - pattern[i-1][0]
            dy1 = pattern[i][1] - pattern[i-1][1]
            dx2 = pattern[i+1][0] - pattern[i][0]
            dy2 = pattern[i+1][1] - pattern[i][1]
            
            # Check for direction change
            if (dx1 * dx2 < 0) or (dy1 * dy2 < 0):
                angles += 1
        
        # Hebrew letters tend to have 1-4 angle changes
        return min(1.0, angles / 4) if angles <= 4 else max(0.0, 1.0 - (angles - 4) * 0.1)
    
    @staticmethod
    def hebrew_phonetic_distance(glyph: "Glyph") -> float:
        """Algorithm 20: Phonetic distance to Hebrew phoneme inventory."""
        if not glyph.phonetic_hypothesis:
            return 0.5
        
        # Hebrew phonemes (simplified)
        hebrew_phonemes = {"a", "e", "i", "o", "u", "b", "g", "d", "h", "v", 
                         "z", "ch", "t", "y", "k", "l", "m", "n", "s", "p", 
                         "ts", "q", "r", "sh"}
        
        matches = 0
        for hyp in glyph.phonetic_hypothesis:
            # Check if first consonant or vowel matches
            for phoneme in hebrew_phonemes:
                if hyp.lower().startswith(phoneme):
                    matches += 1
                    break
        
        return matches / len(glyph.phonetic_hypothesis) if glyph.phonetic_hypothesis else 0.0
    
    @staticmethod
    def hebrew_semantic_field(glyph: "Glyph") -> float:
        """Algorithm 21: Semantic field overlap with Hebrew pictographic origins."""
        # Hebrew letters originally had pictographic meanings
        # Map semantic clusters to Hebrew categories
        semantic_map = {
            0: 0.3,  # Abstract -> Aleph (ox/strength)
            1: 0.5,  # Transformation -> Bet (house)
            2: 0.7,  # Motion -> Gimel (camel)
            3: 0.4,  # Gateway -> Dalet (door)
            4: 0.6,  # Breath -> He (window)
            5: 0.8,  # Connection -> Vav (hook)
            6: 0.2,  # Weapon -> Zayin (weapon)
            7: 0.9,  # Enclosure -> Chet (fence)
            8: 0.5,  # Serpent -> Tet (snake)
            9: 0.7   # Hand -> Yod (hand)
        }
        return semantic_map.get(glyph.semantic_cluster % 10, 0.5)
    
    @staticmethod
    def hebrew_frequency_ratio(glyph: "Glyph") -> float:
        """Algorithm 22: Frequency ratio compared to Hebrew letter frequencies."""
        # Average Hebrew letter frequency is ~0.045 (1/22 letters)
        avg_hebrew_freq = 0.045
        if glyph.frequency == 0:
            return 0.5
        
        ratio = glyph.frequency / avg_hebrew_freq
        return min(1.0, ratio) if ratio <= 1 else max(0.0, 2.0 - ratio)
    
    @staticmethod
    def hebrew_context_overlap(glyph: "Glyph") -> float:
        """Algorithm 23: Context pattern overlap.
        
        Measures how often glyph appears in contexts similar to Hebrew patterns.
        """
        # Use semantic cluster and frequency as proxy for context
        context_score = (glyph.frequency * 0.4 + 
                        glyph.hebrew_correlation * 0.4 + 
                        (glyph.semantic_cluster / 9) * 0.2)
        return min(1.0, max(0.0, context_score))
    
    # ═══════════════════════════════════════════════════════════
    # EGYPTIAN CORRELATION MATRIX (Dimensions 24-31)
    # ═══════════════════════════════════════════════════════════
    
    @staticmethod
    def egyptian_determinative_match(glyph: "Glyph") -> float:
        """Algorithm 25: Egyptian semantic classifier correlation.
        
        Egyptian hieroglyphs use determinatives (semantic markers).
        """
        determinative_classes = {
            "human": 0.2,
            "animal": 0.4,
            "plant": 0.6,
            "building": 0.8,
            "abstract": 1.0
        }
        
        strokes = len(glyph.geometric_pattern)
        if strokes < 3:
            return determinative_classes["abstract"]
        elif strokes < 6:
            return determinative_classes["plant"]
        elif strokes < 9:
            return determinative_classes["animal"]
        elif strokes < 12:
            return determinative_classes["building"]
        else:
            return determinative_classes["human"]
    
    @staticmethod
    def egyptian_phonetic_complement(glyph: "Glyph") -> float:
        """Algorithm 26: Phonetic complement pattern.
        
        Egyptian often uses 1-consonant signs to clarify pronunciation.
        """
        if not glyph.phonetic_hypothesis:
            return 0.5
        
        # Single consonant phonemes are phonetic complements
        single_consonant = sum(1 for h in glyph.phonetic_hypothesis 
                              if len(h) == 1 or (len(h) == 2 and h.endswith('a')))
        return min(1.0, single_consonant / len(glyph.phonetic_hypothesis))
    
    @staticmethod
    def egyptian_ideographic_class(glyph: "Glyph") -> float:
        """Algorithm 27: Ideographic classification.
        
        Classifies glyph as logogram, phonogram, or determinative.
        """
        # Complex patterns suggest logograms, simple patterns suggest phonograms
        complexity = len(glyph.geometric_pattern)
        if complexity > 8:
            return 1.0  # Logogram
        elif complexity > 4:
            return 0.5  # Phonogram
        else:
            return 0.0  # Determinative
    
    @staticmethod
    def egyptian_hieratic_variant(glyph: "Glyph") -> float:
        """Algorithm 28: Hieratic script correlation.
        
        Hieratic is cursive form of hieroglyphs.
        """
        # Curved patterns suggest hieratic influence
        if not glyph.geometric_pattern or len(glyph.geometric_pattern) < 3:
            return 0.5
        
        # Count direction changes (curves)
        curves = 0
        pattern = glyph.geometric_pattern
        for i in range(2, len(pattern)):
            dx1 = pattern[i-1][0] - pattern[i-2][0]
            dy1 = pattern[i-1][1] - pattern[i-2][1]
            dx2 = pattern[i][0] - pattern[i-1][0]
            dy2 = pattern[i][1] - pattern[i-1][1]
            
            if (dx1 != dx2) or (dy1 != dy2):
                curves += 1
        
        return min(1.0, curves / (len(pattern) - 2)) if len(pattern) > 2 else 0.5
    
    @staticmethod
    def egyptian_cartouche_frequency(glyph: "Glyph") -> float:
        """Algorithm 29: Royal cartouche usage frequency.
        
        Cartouches encircle royal names - high-frequency royal phonemes.
        """
        # Royal phonemes in Egyptian (simplified)
        royal_phonemes = {"ra", "sa", "ka", "ma", "ne", "tu", "an"}
        
        if not glyph.phonetic_hypothesis:
            return 0.3
        
        matches = sum(1 for h in glyph.phonetic_hypothesis 
                     if h.lower() in royal_phonemes)
        return min(1.0, matches * 0.5)
    
    @staticmethod
    def egyptian_dynasty_distribution(glyph: "Glyph") -> float:
        """Algorithm 30: Dynasty period distribution.
        
        Glyphs evolved across Old, Middle, New Kingdom periods.
        """
        # Use semantic cluster as proxy for time period
        # Lower clusters = older styles, higher = newer
        return glyph.semantic_cluster / 9
    
    @staticmethod
    def egyptian_temple_vs_secular(glyph: "Glyph") -> float:
        """Algorithm 31: Temple vs secular usage ratio.
        
        Some hieroglyphs appear more in religious vs administrative contexts.
        """
        # High frequency glyphs tend to be secular (administrative)
        # Low frequency tend to be sacred (temple)
        if glyph.frequency > 0.05:
            return 0.3  # Secular
        elif glyph.frequency > 0.02:
            return 0.5  # Mixed
        else:
            return 0.8  # Temple/sacred
    
    # ═══════════════════════════════════════════════════════════
    # CRYPTOGRAPHIC HASH FEATURES (Dimensions 32-35)
    # ═══════════════════════════════════════════════════════════
    
    @staticmethod
    def compute_hash_features(symbol: str) -> Tuple[float, float, float, float]:
        """Algorithms 32-35: Cryptographic hash-derived features.
        
        Returns 4 normalized values from SHA-256 hash of the symbol.
        """
        hash_bytes = hashlib.sha256(symbol.encode('utf-8')).digest()
        
        # Split 32-byte hash into 4 8-byte segments
        v32 = int.from_bytes(hash_bytes[0:8], 'big') / (2**64)
        v33 = int.from_bytes(hash_bytes[8:16], 'big') / (2**64)
        v34 = int.from_bytes(hash_bytes[16:24], 'big') / (2**64)
        v35 = int.from_bytes(hash_bytes[24:32], 'big') / (2**64)
        
        return v32, v33, v34, v35
