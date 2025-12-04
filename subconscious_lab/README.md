# 🧠 SubconsciousLab: Frequency + Speed + Flow

**A subconscious training lab with isochronic tones, binaural beats, and speed-reading.**

> "You basically built a protocol. You were training your subconscious as a high-throughput co-processor."

## 🎯 What This Does

SubconsciousLab coordinates multiple training modalities:

- **🎧 Audio Engine** - Binaural beats and isochronic tones for frequency entrainment
- **📖 RSVP Engine** - Rapid Serial Visual Presentation for speed-reading
- **🔄 Session Protocol** - Integrated training sessions combining audio + visual

### The Science (Simplified)

| Component | What It Does |
|-----------|--------------|
| **Binaural Beats** | Two slightly different frequencies in each ear → brain perceives difference as a beat |
| **Isochronic Tones** | Rhythmic on/off pulsing of a tone → direct entrainment signal |
| **RSVP** | Single-word flashing → bypasses subvocalization, trains parallel processing |

## 🚀 Quick Start

### Installation

```bash
cd subconscious_lab
pip install -r requirements.txt
```

### Generate Audio Files

```bash
# List available presets
python tones.py --list

# Generate a specific preset (10 minutes default)
python tones.py --preset calm_focus

# Generate all presets
python tones.py --all --duration 600
```

### Run Speed-Reading (RSVP)

```bash
# Default text at 400 WPM
python rsvp.py

# Custom speed
python rsvp.py --wpm 600

# Custom text file
python rsvp.py --file your_book.txt --wpm 500
```

### Run a Full Session

```bash
# Interactive session with audio + RSVP
python session.py run --preset calm_focus --duration 10

# Quick 5-minute session
python session.py quick

# See available presets
python session.py presets

# View session history
python session.py history
```

## 🎧 Frequency Presets

| Preset | Type | Beat Hz | Description |
|--------|------|---------|-------------|
| `calm_focus` | binaural | 10 Hz | Focused but relaxed (alpha/low beta) |
| `deep_chill` | binaural | 5 Hz | Introspective, reflective (theta) |
| `feral_god_mode` | isochronic | 14 Hz | High alert, fast pattern recognition (beta-high) |
| `pre_sleep` | binaural | 3 Hz | Wind-down (delta) |
| `flow_state` | binaural | 8 Hz | Creative flow (alpha) |
| `deep_learning` | isochronic | 12 Hz | Memory consolidation (SMR) |

## 📖 Session Protocol

A typical training session:

1. **Choose your state** - Pick a preset that matches your goal
2. **Put on headphones** - Required for binaural beats
3. **Start the session** - Audio begins, RSVP starts
4. **Add physical drills** (optional):
   - Juggling
   - Rubik's cube
   - Ambidextrous writing
   - Peripheral vision exercises
5. **Stay soft** - Don't strain; let the subconscious handle the load

### The Key Insight

> Your conscious job: Stay soft. Don't strain. Let the subconscious handle load.

You're not trying to consciously process everything. You're giving your subconscious:
- **Rhythm** (frequency entrainment)
- **High-bandwidth input** (speed reading)
- **Complex challenges** (physical drills)

And trusting it to adapt.

## 🗂️ File Structure

```
subconscious_lab/
├── README.md           # This file
├── requirements.txt    # Python dependencies
├── frequency_map.json  # Emotion → Frequency mappings
├── tones.py           # Audio engine (binaural/isochronic)
├── rsvp.py            # Speed-reading visual stream
└── session.py         # Session protocol runner
```

## 🔊 Audio Players

For audio playback in sessions, install one of:
- `ffplay` (from FFmpeg) - recommended
- `mpv`
- `vlc`

Or just generate the WAV files and play them manually while running RSVP.

## 📊 Session Logging

Sessions are logged to `session_log.json` for tracking your training over time:

```json
{
  "sessions": [
    {
      "timestamp": "2024-01-15T14:30:00",
      "preset": "calm_focus",
      "duration_minutes": 10,
      "wpm": 400,
      "notes": "Good flow state achieved"
    }
  ]
}
```

## ⚠️ Safety Notes

1. **Use responsibly** - This is experimental self-training
2. **Start slow** - Begin with lower WPM and shorter sessions
3. **Headphones required** - Binaural beats only work with stereo headphones
4. **Not for driving** - Use the lab on a couch, not a highway
5. **Listen to your body** - Stop if you feel discomfort

## 🔮 Future Directions

- [ ] Web-based UI with Web Audio API
- [ ] Canvas-based RSVP with better typography
- [ ] Personal emotion-frequency map evolution
- [ ] EEG integration for feedback loops
- [ ] Spaced repetition text scheduling
- [ ] Multi-modal stimulus protocols

---

*"You didn't just 'use' your subconscious. You raised it."*
