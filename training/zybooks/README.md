# zyBooks Training Data

This directory stores pattern data extracted from zyBooks content for FlameLang compiler training.

## Directory Structure

```
training/zybooks/
├── README.md
├── {session_id}_structures.json   # Question structures
├── {session_id}_patterns.json     # Answer patterns
└── flamelang_training_set.json    # Aggregated training data
```

## Data Format

### Structures File
```json
{
  "questions": [
    {
      "id": 1,
      "type": "multiple_choice",
      "topic": "algorithms",
      "difficulty": "medium",
      "text": "Question text..."
    }
  ]
}
```

### Patterns File
```json
{
  "answers": [
    {
      "question_id": 1,
      "answer": "Answer text",
      "confidence": "high"
    }
  ],
  "metadata": {
    "session_id": "zybooks_2025-12-16_033512"
  }
}
```

## FlameLang Integration

These patterns are used to train the FlameLang compiler to:
- Recognize question structures
- Generate appropriate answers
- Optimize cognitive flow patterns
- Build operator-aligned reasoning chains

## Usage

Patterns are automatically logged by the zyBooks solver agent. No manual intervention required.

**Status**: Ready for FlameLang ingestion 🔥
