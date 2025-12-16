# INV-080: Glyph-Decoded Statistical Semantics (GDSS)

**Date:** 2025-12-15
**Status:** Captured
**Category:** Cognitive Architecture / Visual Compilation

## Core Insight
Charts are semantic glyphs, not data outputs. Decode meaning from geometry, not computation.

## Pipeline Shift
```yaml
traditional: DATA → COMPUTE → ANSWER
GDSS:        SYMBOL → MEANING → ANSWER
```

## Evidence
- 3 frontier LLMs (Claude, Grok, GPT) required cross-validation
- Human with correct model reads picture directly
- Box plot example: gridline misread ≠ math error → visual quantization error

## FlameLang Integration
```flame
glyph boxplot {
    whisker.low   -> MIN
    box.low       -> Q1
    box.center    -> MEDIAN
    box.high      -> Q3
    whisker.high  -> MAX
    detached.dot  -> OUTLIER
}
```

## Applications
Box plots, histograms, candlesticks, control charts, medical imaging, dashboards

## Next Steps
- Formalize as `flame::glyphstats` module
- Patent abstract draft
