# Chess Council Games

This directory contains records of bibliographic chess games played by the AI council.

## What is Bibliographic Chess?

Bibliographic chess is a research methodology where AI agents debate research questions using claims and counter-claims, with citations as evidence.

### Game Structure

```yaml
game_format:
  players:
    white: "Research Position (Proponent)"
    black: "Counter-Position (Critic)"
  
  move_types:
    claim: "Assertion with citation"
    counter: "Refutation with evidence"
    synthesis: "Combining perspectives"
    question: "Identifying gaps"
  
  victory_conditions:
    checkmate: "Irrefutable synthesis achieved"
    draw: "Mutual uncertainty, more research needed"
    stalemate: "Insufficient evidence to proceed"
```

## Planned Games

| Game ID | Topic | White Position | Black Position | Status |
|---------|-------|----------------|----------------|--------|
| GAME-001 | Quantum vs Crypto | Quantum computing will break crypto | Post-quantum cryptography is ready | Planned |
| GAME-002 | Climate vs Policy | Technology can solve climate change | Policy changes are essential | Planned |
| GAME-003 | Drug Discovery | AI will democratize drug discovery | Regulatory barriers remain | Planned |
| GAME-004 | AI Alignment | Constitutional AI is sufficient | More robust alignment needed | Planned |

## How to Read a Game

```json
{
  "game_id": "GAME-001",
  "topic": "Quantum vs Crypto",
  "date": "2025-12-01",
  "moves": [
    {
      "move_number": 1,
      "player": "white",
      "type": "claim",
      "content": "Shor's algorithm can break RSA in polynomial time",
      "citation": "Shor, P. (1994). Algorithms for quantum computation"
    },
    {
      "move_number": 1,
      "player": "black",
      "type": "counter",
      "content": "Current quantum computers have insufficient qubits",
      "citation": "IBM Quantum Roadmap 2024"
    }
  ],
  "result": "ongoing",
  "synthesis": null
}
```

## How to Propose a Game

1. Create an issue in the repository
2. Define the topic and positions
3. Specify the research question
4. Identify relevant citations
5. Request agent assignment

## Active Research Questions

### Drug Discovery Domain
- Can open-source AI match commercial AlphaFold alternatives?
- Is AI drug discovery accessible to low-income countries?
- Will AI-designed molecules face patent challenges?

### Legal Domain
- Can DAOs achieve regulatory clarity in the US?
- Is the Howey test applicable to utility tokens?
- How will the EU AI Act affect research?

### Cross-Domain
- How does AI governance intersect with drug regulation?
- Can non-profits sustainably fund AI research?
- What's the optimal balance of open vs. proprietary AI?

*Part of the Library of Alexandria*
