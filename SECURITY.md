# Security Policy

## Supported Versions

Use this section to tell people about which versions of your project are
currently being supported with security updates.

| Version | Supported          |
| ------- | ------------------ |
| 5.1.x   | :white_check_mark: |
| 5.0.x   | :x:                |
| 4.0.x   | :white_check_mark: |
| < 4.0   | :x:                |

## Reporting a Vulnerability

Use this section to tell people how to report a vulnerability.

Tell them where to go, how often they can expect to get an update on a
reported vulnerability, what to expect if the vulnerability is accepted or
declined, etc.

## Methodology

### 4.5 Contribution to the Field

See [README.md](README.md) for project overview and contributions.

### 4.6 Adversarial Threat Model and Mitigations

SACSE operates under a formally defined threat model assuming a capable adversary able to attempt:  
(a) private key compromise, (b) supply-chain or model-poisoning attacks against LLM inference endpoints, (c) repository compromise via stolen credentials or CI/CD subversion, and (d) network-level interception or replay.

Mitigations currently deployed or scheduled for v1.1 (December 2025):  
- All primary GPG keys stored offline on YubiKey 5 FIPS hardware security modules; daily subkeys only touch internet-connected devices.  
- LLM inference executed exclusively via local Ollama instances (qwen2.5:72b, llama3.3:405b) with reproducible model hashes; cloud endpoints used only under explicit, signed HITL override.  
- All CI/CD pipelines disabled; every commit manually GPG-signed; merge-to-main requires detached signature verification.  
- Repository access protected by SSH keys stored on hardware tokens; GitHub emergency backup mirror uses push-only deploy key with zero read permissions.  
- Full artifact corpus published with SHA-256 manifest and verification script (see Section 4.7) enabling third-party cryptographic validation.

These controls reduce the single-operator risk surface to hardware-token possession and physical security — the same standard used by high-security cryptocurrency custodians.

### 4.7 Reproducibility Verification

For cryptographic reproducibility verification of the SACSE corpus, see:
- [reproducibility_manifest.yml](reproducibility_manifest.yml) - SHA-256 manifest of all artifacts
- [verify.sh](verify.sh) - One-command third-party reproducibility verification script
