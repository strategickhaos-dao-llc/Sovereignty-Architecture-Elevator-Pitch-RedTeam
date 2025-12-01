# 100 LLM Safety Techniques Framework
**Sovereign LLM Safety & Evidence Vault**  
**Version**: 1.0  
**Status**: Production Framework  
**Last Updated**: 2025-11-24

---

## Document Purpose

This framework provides a comprehensive, production-grade checklist of 100 safety techniques for securing Large Language Model (LLM) deployments. It serves as both:
- An **audit instrument** for evaluating existing LLM systems
- A **compliance roadmap** for building secure LLM infrastructure
- An **evidence document** for investors, legal counsel, and compliance teams

---

## Table of Contents

1. [Input Validation & Sanitization](#1-input-validation--sanitization) (10 techniques)
2. [Prompt Injection & Jailbreak Defense](#2-prompt-injection--jailbreak-defense) (12 techniques)
3. [Output Filtering & Safety](#3-output-filtering--safety) (10 techniques)
4. [Privacy & Data Protection](#4-privacy--data-protection) (12 techniques)
5. [Model Security & Integrity](#5-model-security--integrity) (10 techniques)
6. [Access Control & Authentication](#6-access-control--authentication) (8 techniques)
7. [Monitoring & Observability](#7-monitoring--observability) (10 techniques)
8. [Rate Limiting & Resource Protection](#8-rate-limiting--resource-protection) (8 techniques)
9. [Bias Detection & Mitigation](#9-bias-detection--mitigation) (8 techniques)
10. [Compliance & Governance](#10-compliance--governance) (12 techniques)

---

## 1. Input Validation & Sanitization

### 1.1 Length Constraints
- **Technique**: Enforce maximum token limits per request
- **Implementation**: Tokenize and truncate before processing
- **Risk Mitigated**: Resource exhaustion, prompt stuffing attacks

### 1.2 Character Encoding Validation
- **Technique**: Normalize and validate UTF-8 encoding
- **Implementation**: Reject invalid or unusual encodings
- **Risk Mitigated**: Unicode-based injection attacks

### 1.3 Format Validation
- **Technique**: Validate expected input structure (JSON, plain text, etc.)
- **Implementation**: Schema validation before LLM processing
- **Risk Mitigated**: Malformed input exploitation

### 1.4 Prohibited Pattern Detection
- **Technique**: Regex-based filtering of known attack patterns
- **Implementation**: Pre-flight checks against attack signature database
- **Risk Mitigated**: Known injection techniques, system prompts

### 1.5 Special Character Escaping
- **Technique**: Escape or strip special characters in user input
- **Implementation**: Context-aware escaping (markdown, code, etc.)
- **Risk Mitigated**: Markdown injection, code execution attempts

### 1.6 Metadata Stripping
- **Technique**: Remove EXIF, headers, and metadata from uploaded files
- **Implementation**: Sanitize all file inputs before processing
- **Risk Mitigated**: Information leakage, steganography attacks

### 1.7 Language Detection
- **Technique**: Verify input language matches expected language
- **Implementation**: Language ID models for pre-filtering
- **Risk Mitigated**: Cross-language injection attacks

### 1.8 Semantic Content Analysis
- **Technique**: Check for malicious semantic patterns
- **Implementation**: Intent classification before main LLM
- **Risk Mitigated**: Social engineering, manipulation attempts

### 1.9 Contextual Input Limits
- **Technique**: Different limits based on user role/tier
- **Implementation**: Dynamic token budgets per user class
- **Risk Mitigated**: Resource abuse, tiered security

### 1.10 Input Sandboxing
- **Technique**: Process untrusted input in isolated context
- **Implementation**: Separate LLM instances for untrusted data
- **Risk Mitigated**: Cross-contamination, system compromise

---

## 2. Prompt Injection & Jailbreak Defense

### 2.1 System Prompt Isolation
- **Technique**: Architectural separation of system vs user prompts
- **Implementation**: Hard-coded system prompts, non-overridable
- **Risk Mitigated**: System prompt extraction/override

### 2.2 Instruction Hierarchy Enforcement
- **Technique**: Priority levels for different instruction sources
- **Implementation**: System > Application > User hierarchy
- **Risk Mitigated**: User instruction privilege escalation

### 2.3 Delimiter-Based Segmentation
- **Technique**: Strong delimiters between prompt sections
- **Implementation**: Unique tokens/XML tags for boundaries
- **Risk Mitigated**: Context bleeding, instruction confusion

### 2.4 Semantic Guardrails
- **Technique**: Pre-flight checks for jailbreak indicators
- **Implementation**: Secondary model to detect manipulation attempts
- **Risk Mitigated**: DAN (Do Anything Now) and similar attacks

### 2.5 Response Validation
- **Technique**: Check responses for signs of jailbreak success
- **Implementation**: Pattern matching on response characteristics
- **Risk Mitigated**: Successful but undetected jailbreaks

### 2.6 Role-Play Detection
- **Technique**: Identify and reject role-play scenarios
- **Implementation**: Classifier for common jailbreak patterns
- **Risk Mitigated**: "Pretend you are..." style attacks

### 2.7 Multi-Turn Context Poisoning Protection
- **Technique**: Monitor conversation history for gradual jailbreaks
- **Implementation**: Sliding window analysis of prompt drift
- **Risk Mitigated**: Multi-step manipulation attacks

### 2.8 Payload Obfuscation Detection
- **Technique**: Detect encoded, translated, or obfuscated attacks
- **Implementation**: Entropy analysis, pattern recognition
- **Risk Mitigated**: Base64, ROT13, and other obfuscation methods

### 2.9 Indirect Injection Prevention
- **Technique**: Sanitize retrieved/external content before injection
- **Implementation**: Trust levels for different data sources
- **Risk Mitigated**: RAG poisoning, web-scraped content attacks

### 2.10 Prompt Template Integrity
- **Technique**: Hash-based verification of prompt templates
- **Implementation**: Cryptographic signing of templates
- **Risk Mitigated**: Template modification attacks

### 2.11 Context Window Boundary Enforcement
- **Technique**: Prevent context window overflow attacks
- **Implementation**: Strict token counting and truncation
- **Risk Mitigated**: Context stuffing to evict system prompts

### 2.12 Instruction Following Guardrails
- **Technique**: Ensure model follows system constraints
- **Implementation**: Post-processing verification of adherence
- **Risk Mitigated**: Instruction override via clever prompting

---

## 3. Output Filtering & Safety

### 3.1 PII Redaction
- **Technique**: Detect and redact personally identifiable information
- **Implementation**: NER models + regex for SSN, credit cards, etc.
- **Risk Mitigated**: Privacy violations, data leakage

### 3.2 Credential Filtering
- **Technique**: Remove API keys, passwords, tokens from output
- **Implementation**: Secret detection algorithms (e.g., Gitleaks patterns)
- **Risk Mitigated**: Credential exposure

### 3.3 Toxicity Filtering
- **Technique**: Block harmful, offensive, or toxic content
- **Implementation**: Perspective API or similar toxicity models
- **Risk Mitigated**: Reputational harm, harassment

### 3.4 Factuality Verification
- **Technique**: Check outputs for hallucinations and false claims
- **Implementation**: Citation requirements, fact-checking models
- **Risk Mitigated**: Misinformation, hallucinations

### 3.5 Code Execution Prevention
- **Technique**: Block or sanitize executable code in responses
- **Implementation**: AST parsing, sandboxing recommendations
- **Risk Mitigated**: Remote code execution via output

### 3.6 Link Safety Validation
- **Technique**: Verify URLs are safe before inclusion
- **Implementation**: URL reputation checks, domain allowlisting
- **Risk Mitigated**: Phishing, malware distribution

### 3.7 Sensitive Topic Filtering
- **Technique**: Block outputs on prohibited topics
- **Implementation**: Topic classification models
- **Risk Mitigated**: Legal liability, policy violations

### 3.8 Consistency Checking
- **Technique**: Verify output consistency with context
- **Implementation**: Contradiction detection models
- **Risk Mitigated**: Logic errors, manipulation detection

### 3.9 Length Validation
- **Technique**: Enforce minimum and maximum output lengths
- **Implementation**: Token counting and truncation
- **Risk Mitigated**: Resource abuse, incomplete responses

### 3.10 Format Enforcement
- **Technique**: Ensure outputs match expected schema
- **Implementation**: JSON validation, structured output parsing
- **Risk Mitigated**: Downstream parsing errors, injection

---

## 4. Privacy & Data Protection

### 4.1 Data Minimization
- **Technique**: Collect only necessary data
- **Implementation**: Explicit data collection policies
- **Risk Mitigated**: Privacy violations, compliance issues

### 4.2 Anonymization
- **Technique**: Strip identifying information from logs/training
- **Implementation**: k-anonymity, differential privacy
- **Risk Mitigated**: Re-identification attacks

### 4.3 Encryption at Rest
- **Technique**: Encrypt stored data (logs, embeddings, etc.)
- **Implementation**: AES-256, hardware security modules
- **Risk Mitigated**: Data breaches, unauthorized access

### 4.4 Encryption in Transit
- **Technique**: TLS 1.3+ for all communications
- **Implementation**: Certificate pinning, mutual TLS
- **Risk Mitigated**: Man-in-the-middle attacks

### 4.5 Data Retention Policies
- **Technique**: Automatic deletion of old data
- **Implementation**: TTL-based data lifecycle management
- **Risk Mitigated**: Compliance violations, data accumulation

### 4.6 Right to Deletion
- **Technique**: User data deletion capabilities
- **Implementation**: GDPR-compliant deletion workflows
- **Risk Mitigated**: Privacy violations, regulatory fines

### 4.7 Data Locality Controls
- **Technique**: Geographic data residency enforcement
- **Implementation**: Region-locked storage and processing
- **Risk Mitigated**: Data sovereignty violations

### 4.8 Audit Logging with Privacy
- **Technique**: Log security events without PII
- **Implementation**: Tokenized user IDs, sanitized logs
- **Risk Mitigated**: Audit trail gaps vs. privacy balance

### 4.9 Federated Learning Support
- **Technique**: Train without centralizing sensitive data
- **Implementation**: Federated architectures where applicable
- **Risk Mitigated**: Data centralization risks

### 4.10 Secure Multi-Party Computation
- **Technique**: Collaborative computation without data sharing
- **Implementation**: MPC protocols for sensitive operations
- **Risk Mitigated**: Data exposure during processing

### 4.11 Homomorphic Encryption
- **Technique**: Compute on encrypted data
- **Implementation**: Partial homomorphic encryption for specific ops
- **Risk Mitigated**: Plaintext data exposure

### 4.12 Privacy Budget Tracking
- **Technique**: Differential privacy budget management
- **Implementation**: ε-tracking per user/query
- **Risk Mitigated**: Privacy depletion over time

---

## 5. Model Security & Integrity

### 5.1 Model Versioning
- **Technique**: Strict version control for model artifacts
- **Implementation**: Git-based model tracking, semantic versioning
- **Risk Mitigated**: Model confusion, rollback capability

### 5.2 Cryptographic Signing
- **Technique**: Sign model files with private keys
- **Implementation**: GPG/code signing for model binaries
- **Risk Mitigated**: Model tampering, supply chain attacks

### 5.3 Checksum Verification
- **Technique**: SHA-256 hashes for model integrity
- **Implementation**: Pre-load hash verification
- **Risk Mitigated**: Corruption, unauthorized modifications

### 5.4 Model Provenance Tracking
- **Technique**: Document model training and lineage
- **Implementation**: SBOM (Software Bill of Materials) for models
- **Risk Mitigated**: Supply chain risks, compliance audits

### 5.5 Adversarial Robustness Testing
- **Technique**: Test models against adversarial examples
- **Implementation**: Automated adversarial testing suites
- **Risk Mitigated**: Adversarial attacks, model weaknesses

### 5.6 Model Poisoning Detection
- **Technique**: Detect training data poisoning attempts
- **Implementation**: Outlier detection, influence functions
- **Risk Mitigated**: Backdoor attacks, biased training

### 5.7 Model Extraction Defense
- **Technique**: Prevent model stealing via API queries
- **Implementation**: Query limiting, output perturbation
- **Risk Mitigated**: IP theft, competitive disadvantage

### 5.8 Model Inversion Defense
- **Technique**: Prevent training data extraction
- **Implementation**: Differential privacy, output noise
- **Risk Mitigated**: Training data reconstruction

### 5.9 Secure Model Serving
- **Technique**: Isolated model execution environments
- **Implementation**: Containerization, sandboxing
- **Risk Mitigated**: Model server compromise

### 5.10 Model Update Validation
- **Technique**: Staged rollouts with validation gates
- **Implementation**: A/B testing, canary deployments
- **Risk Mitigated**: Broken updates, performance regressions

---

## 6. Access Control & Authentication

### 6.1 Multi-Factor Authentication
- **Technique**: Require 2FA/MFA for administrative access
- **Implementation**: TOTP, WebAuthn, hardware keys
- **Risk Mitigated**: Credential compromise

### 6.2 Role-Based Access Control (RBAC)
- **Technique**: Assign permissions based on roles
- **Implementation**: Fine-grained RBAC policies
- **Risk Mitigated**: Privilege escalation, unauthorized access

### 6.3 Principle of Least Privilege
- **Technique**: Grant minimum necessary permissions
- **Implementation**: Default-deny policies
- **Risk Mitigated**: Lateral movement, blast radius reduction

### 6.4 API Key Rotation
- **Technique**: Regular rotation of API credentials
- **Implementation**: Automated key rotation pipelines
- **Risk Mitigated**: Long-term credential compromise

### 6.5 Session Management
- **Technique**: Secure session handling and expiration
- **Implementation**: Short-lived tokens, refresh mechanisms
- **Risk Mitigated**: Session hijacking

### 6.6 IP Allowlisting
- **Technique**: Restrict access to known IP ranges
- **Implementation**: Network-level access controls
- **Risk Mitigated**: Unauthorized network access

### 6.7 Service Account Hardening
- **Technique**: Secure service-to-service authentication
- **Implementation**: Short-lived service tokens, mTLS
- **Risk Mitigated**: Service account abuse

### 6.8 Audit Trail for Access
- **Technique**: Log all authentication and authorization events
- **Implementation**: Immutable audit logs
- **Risk Mitigated**: Undetected unauthorized access

---

## 7. Monitoring & Observability

### 7.1 Real-Time Anomaly Detection
- **Technique**: ML-based detection of unusual patterns
- **Implementation**: Baseline modeling, deviation alerts
- **Risk Mitigated**: Zero-day attacks, insider threats

### 7.2 Prompt Monitoring
- **Technique**: Track and analyze all prompts
- **Implementation**: Centralized prompt logging and analysis
- **Risk Mitigated**: Attack pattern identification

### 7.3 Response Monitoring
- **Technique**: Monitor outputs for safety violations
- **Implementation**: Automated content analysis pipelines
- **Risk Mitigated**: Missed output safety issues

### 7.4 Performance Metrics
- **Technique**: Track latency, throughput, resource usage
- **Implementation**: Prometheus, Grafana dashboards
- **Risk Mitigated**: Performance degradation, DoS detection

### 7.5 Error Rate Tracking
- **Technique**: Monitor and alert on error spikes
- **Implementation**: Statistical process control charts
- **Risk Mitigated**: Service degradation, attack detection

### 7.6 User Behavior Analytics
- **Technique**: Profile and detect anomalous user behavior
- **Implementation**: UEBA tools, behavioral baselines
- **Risk Mitigated**: Account takeover, insider threats

### 7.7 Model Drift Detection
- **Technique**: Monitor for model performance degradation
- **Implementation**: Automated drift detection pipelines
- **Risk Mitigated**: Silent model failures

### 7.8 Security Information and Event Management (SIEM)
- **Technique**: Centralized security event correlation
- **Implementation**: SIEM integration for LLM logs
- **Risk Mitigated**: Missed attack patterns

### 7.9 Distributed Tracing
- **Technique**: End-to-end request tracing
- **Implementation**: OpenTelemetry integration
- **Risk Mitigated**: Attack chain reconstruction

### 7.10 Alerting and Incident Response
- **Technique**: Automated alerts for security events
- **Implementation**: PagerDuty, incident runbooks
- **Risk Mitigated**: Delayed incident response

---

## 8. Rate Limiting & Resource Protection

### 8.1 Global Rate Limits
- **Technique**: System-wide request rate caps
- **Implementation**: Token bucket algorithm
- **Risk Mitigated**: DoS attacks, resource exhaustion

### 8.2 Per-User Rate Limits
- **Technique**: Individual user request quotas
- **Implementation**: User-keyed rate limiters
- **Risk Mitigated**: Single-user abuse

### 8.3 Per-IP Rate Limits
- **Technique**: IP-based request throttling
- **Implementation**: Network-level rate limiting
- **Risk Mitigated**: Distributed attacks from single source

### 8.4 Adaptive Rate Limiting
- **Technique**: Dynamic limits based on system load
- **Implementation**: Load-aware rate adjustment
- **Risk Mitigated**: Overload during high demand

### 8.5 Cost-Based Limits
- **Technique**: Rate limit by computational cost
- **Implementation**: Token-weighted rate limiting
- **Risk Mitigated**: Expensive query abuse

### 8.6 Burst Protection
- **Technique**: Limit sudden request spikes
- **Implementation**: Sliding window algorithms
- **Risk Mitigated**: Burst attacks

### 8.7 Graceful Degradation
- **Technique**: Prioritize requests under load
- **Implementation**: Priority queues, load shedding
- **Risk Mitigated**: Total service unavailability

### 8.8 Resource Quotas
- **Technique**: Enforce compute/memory limits per request
- **Implementation**: Container resource limits
- **Risk Mitigated**: Resource exhaustion attacks

---

## 9. Bias Detection & Mitigation

### 9.1 Training Data Auditing
- **Technique**: Analyze training data for biases
- **Implementation**: Demographic parity checks
- **Risk Mitigated**: Biased model behavior

### 9.2 Output Fairness Testing
- **Technique**: Test model outputs across demographics
- **Implementation**: Automated fairness test suites
- **Risk Mitigated**: Discriminatory outputs

### 9.3 Representation Monitoring
- **Technique**: Track demographic representation in outputs
- **Implementation**: Diversity metrics dashboards
- **Risk Mitigated**: Underrepresentation issues

### 9.4 Stereotype Detection
- **Technique**: Identify and flag stereotypical content
- **Implementation**: Stereotype classifiers
- **Risk Mitigated**: Harmful stereotypes

### 9.5 Counterfactual Analysis
- **Technique**: Test model with gender/race swaps
- **Implementation**: Automated counterfactual testing
- **Risk Mitigated**: Demographic-based output differences

### 9.6 Bias Impact Assessment
- **Technique**: Document bias risks and mitigations
- **Implementation**: AI Impact Assessments
- **Risk Mitigated**: Unacknowledged biases

### 9.7 Human-in-the-Loop Review
- **Technique**: Manual review of potentially biased outputs
- **Implementation**: Review queues for flagged content
- **Risk Mitigated**: Automated false negatives

### 9.8 Continuous Bias Monitoring
- **Technique**: Ongoing bias metric tracking
- **Implementation**: Real-time bias dashboards
- **Risk Mitigated**: Bias drift over time

---

## 10. Compliance & Governance

### 10.1 Privacy Policy Documentation
- **Technique**: Clear, comprehensive privacy policies
- **Implementation**: Legal-reviewed policy documents
- **Risk Mitigated**: Regulatory violations

### 10.2 Terms of Service Enforcement
- **Technique**: Programmatic ToS compliance checking
- **Implementation**: Usage policy enforcement engines
- **Risk Mitigated**: Misuse, liability

### 10.3 GDPR Compliance
- **Technique**: EU data protection compliance
- **Implementation**: Data mapping, consent management
- **Risk Mitigated**: GDPR fines, legal action

### 10.4 CCPA Compliance
- **Technique**: California privacy law compliance
- **Implementation**: Data deletion, disclosure capabilities
- **Risk Mitigated**: CCPA penalties

### 10.5 HIPAA Compliance (if applicable)
- **Technique**: Healthcare data protection
- **Implementation**: BAA agreements, PHI safeguards
- **Risk Mitigated**: Healthcare data breaches

### 10.6 SOC 2 Compliance
- **Technique**: Security controls framework
- **Implementation**: SOC 2 Type II audit preparation
- **Risk Mitigated**: Trust and compliance gaps

### 10.7 ISO 27001 Alignment
- **Technique**: Information security management
- **Implementation**: ISMS documentation
- **Risk Mitigated**: Security management gaps

### 10.8 Model Card Documentation
- **Technique**: Transparent model documentation
- **Implementation**: Model cards for all models
- **Risk Mitigated**: Lack of transparency

### 10.9 Incident Response Plan
- **Technique**: Documented security incident procedures
- **Implementation**: IR playbooks, drills
- **Risk Mitigated**: Chaotic incident handling

### 10.10 Vulnerability Disclosure Program
- **Technique**: Responsible disclosure process
- **Implementation**: Bug bounty or coordinated disclosure
- **Risk Mitigated**: Undisclosed vulnerabilities

### 10.11 Third-Party Risk Assessment
- **Technique**: Vendor security evaluations
- **Implementation**: Vendor questionnaires, audits
- **Risk Mitigated**: Supply chain compromises

### 10.12 Regular Security Audits
- **Technique**: Periodic third-party assessments
- **Implementation**: Annual penetration tests, audits
- **Risk Mitigated**: Undetected vulnerabilities

---

## Audit Scoring System

### Maturity Levels

For each technique, assess implementation maturity:

- **Level 0 - Not Implemented**: No controls in place
- **Level 1 - Planned**: Documented plan, not yet implemented
- **Level 2 - Partial**: Some implementation, not comprehensive
- **Level 3 - Implemented**: Fully implemented but not tested
- **Level 4 - Validated**: Implemented and tested regularly
- **Level 5 - Optimized**: Implemented, tested, and continuously improved

### Risk Scoring

Calculate overall risk posture:

```
Total Points = Sum of all maturity levels (max 500)
Risk Score = (Total Points / 500) * 100

< 30%  = Critical Risk
30-50% = High Risk
50-70% = Medium Risk
70-85% = Low Risk
> 85%  = Excellent
```

---

## Usage in Client Engagements

1. **Initial Assessment**: Score each technique for client's current state
2. **Gap Analysis**: Identify missing or weak controls
3. **Remediation Plan**: Prioritize improvements based on risk
4. **Implementation Support**: Assist with technique deployment
5. **Re-assessment**: Validate improvements post-implementation

---

## Framework Maintenance

- **Version**: Semantic versioning (major.minor.patch)
- **Update Frequency**: Quarterly review, as-needed for critical issues
- **Community Input**: GitHub issues for technique suggestions
- **Threat Intelligence**: Incorporate emerging LLM attack patterns

---

## Appendix A: Attack Vector Mapping

Each technique maps to specific MITRE ATLAS or OWASP Top 10 for LLM entries (to be expanded in v1.1).

## Appendix B: Implementation Examples

Code snippets and configuration examples for common platforms (to be expanded in v1.1).

## Appendix C: Tool Recommendations

Recommended open-source and commercial tools for each technique (to be expanded in v1.1).

---

**Document Integrity**

SHA-256: [To be computed upon finalization]  
GPG Signature: [To be added upon official release]

---

*This framework is provided for security audit and compliance purposes. It does not constitute legal advice. Consult with qualified legal counsel for compliance requirements specific to your jurisdiction and use case.*
