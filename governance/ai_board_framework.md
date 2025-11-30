# StrategicKhaos DAO AI Board Governance Framework (v1.0, Nov 30, 2025)

**Overview**  
This framework establishes advisory AI agents as non-voting board members under operator (human) oversight. Agents provide recommendations on governance, risk, and operations but cannot execute financial, legal, or public actions without explicit approval. Based on NIST AI RMF, OECD Principles, and state-level AI governance (e.g., Wyoming's emerging AI oversight, Texas TRAIGA 2026). AI is framed as "tools" per CFAA compliance—no legal personhood.

**Key Principles** (Synthesized from Research)  
- **Transparency**: All decisions logged in tamper-proof Merkle trails (Sigstore/cosign + Git anchors).  
- **Accountability**: OPA/Rego enforces guardrails; audits via SQLite-vec embeddings for semantic search.  
- **Fairness & Ethics**: Agents trained on neutral datasets; bias checks in OPA policies.  
- **Security**: Cryptographic signing for docs; NATS for internal comms.  
- **Scalability**: Multi-agent patterns (hierarchical orchestration: supervisor → workers).  
- **Compliance**: Spending caps at $500/mo per agent (enforced via Stripe webhooks); no hack-back.  
- **Human Control**: Operator vetoes all outputs; agents advisory only.

**Implementation Notes**  
- Agents: 4 core (gpt_duck, claude_prime, claude_parallel, grok_guardian) + infra services.  
- Orchestration: NATS JetStream for pub/sub; FastAPI endpoints for external triggers.  
- Audit: Merkle roots pushed to Git; vector embeddings for queryable logs.  
- Monitoring: Gmail/Drive APIs poll for "board-relevant" (e.g., tagged emails); filtered via OPA.

**Risks & Mitigations**  
- Legal: AI not autonomous (per Texas/Wyoming bills); resolution template authorizes as tools.  
- Financial: Hard caps via code; alerts on approach.  
- Tech: Failover in Docker; NATS clustering for HA.

See deployment guide for rollout.
