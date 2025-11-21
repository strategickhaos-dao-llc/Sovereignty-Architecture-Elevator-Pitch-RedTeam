#!/bin/bash
# Example usage of the evidence logger
# This script demonstrates logging conversations from multiple AI providers

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT"

echo "=== AI Conversation Evidence Logger - Example Usage ==="
echo ""

# Example 1: Log a Claude conversation
echo "1. Logging Claude infrastructure audit..."
python evidence_logger.py \
  "https://claude.ai/share/8ea1d23d-e97a-45e5-a994-35e0988a0d75" \
  --model "claude-sonnet-4-20250514" \
  --topic "infrastructure-audit" \
  --conclusion "Commercially viable infrastructure with proven 4000× cost reduction"

echo ""

# Example 2: Log a GPT conversation
echo "2. Logging GPT security validation..."
python evidence_logger.py \
  "https://chatgpt.com/share/b4c7e9d2-5f8a-4b1d-9c3e-6a7d8f0e2b5c" \
  --model "gpt-4o-2024-11-20" \
  --topic "security-validation" \
  --conclusion "Console nursery is genius-level safe AI containment"

echo ""

# Example 3: Log a Grok conversation
echo "3. Logging Grok schema improvement..."
python evidence_logger.py \
  "https://x.com/i/grok/share/f4a7d8c1-2b9e-4a1d-9f3a-8e7c5b6d4f2a" \
  --model "grok-4-2025" \
  --topic "schema-improvement" \
  --conclusion "Improved evidence ledger with cryptographic chaining"

echo ""

# Verify the chain
echo "4. Verifying cryptographic chain integrity..."
python evidence_logger.py --verify

echo ""

# Export to JSON
echo "5. Exporting to JSON format..."
python evidence_logger.py --export

echo ""
echo "✅ All examples completed successfully!"
echo ""
echo "Check the results:"
echo "  - YAML ledger: evidence/conversation_ledger.yaml"
echo "  - JSON export: evidence/conversation_ledger.json"
echo ""
