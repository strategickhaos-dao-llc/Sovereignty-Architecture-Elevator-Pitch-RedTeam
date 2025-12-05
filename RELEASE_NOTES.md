# Release Notes Index

This document tracks all releases for the Sovereignty Architecture project.

## Release Categories

- **SwarmGate** - Eternal 7% Engine releases
- **Core** - Main platform releases
- **Governance** - Governance and policy updates

---

## SwarmGate Releases

### [swarmgate/v1.0](https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-/releases/tag/swarmgate/v1.0)

**SwarmGate v1.0 — Eternal 7% Engine**

*Release Date: 2025-11-27*

#### Scope
- Initial release of SwarmGate revenue split mechanism
- Smart contract implementation for 7% split distribution
- Control plane configuration and status tracking
- CI/CD workflows for build, test, and deployment
- Deployment documentation for testnet and mainnet
- Governance change policy documentation

#### Components
- `contracts/SwarmGate.sol` - Main revenue split contract
- `swarmgate/status.yaml` - Status and provenance tracking
- `swarmgate/config.yaml` - Control plane configuration
- `docs/DEPLOY_SWARMGATE.md` - Deployment guide
- `governance/SWARMGATE_CHANGE_POLICY.md` - Change management policy

#### Split Parameters
- **Total Split**: 7% (700 basis points)
- **Distribution**:
  - Operations: 40% (2.8% of revenue)
  - Development: 30% (2.1% of revenue)
  - Governance: 20% (1.4% of revenue)
  - Reserves: 10% (0.7% of revenue)

#### Artifact Checksums
```
contracts/SwarmGate.sol: sha256:[computed-on-release]
```

#### Deployment Status
- Testnet: Pending
- Mainnet: Pending

#### Quick Start
```bash
# Deploy to testnet
gh workflow run contracts-deploy.yml -f environment=testnet -f confirm=confirm

# See full deployment guide
cat docs/DEPLOY_SWARMGATE.md
```

#### Documentation Links
- [Deployment Guide](docs/DEPLOY_SWARMGATE.md)
- [Change Policy](governance/SWARMGATE_CHANGE_POLICY.md)
- [Contract README](contracts/README.md)
- [AI Constitution](governance/AI_CONSTITUTION.yaml)

---

## Core Platform Releases

### Initial Release

*See main README.md for current platform features*

- Discord DevOps Control Plane
- Event Gateway
- GitLens Integration
- Java Development Workspace
- AI Agent Integration

---

## Governance Updates

### Policy v1.0

*2025-11-27*

- Initial SwarmGate change policy
- Access matrix for authorized operations
- Article 7 authorized signers documentation

---

## Version History

| Version | Date | Type | Description |
|---------|------|------|-------------|
| swarmgate/v1.0 | 2025-11-27 | SwarmGate | Initial 7% Engine release |

---

## Release Process

1. **Preparation**: Update version in relevant files
2. **Changelog**: Document changes in this file
3. **Review**: Obtain required approvals
4. **Tag**: Create signed tag (`git tag -s`)
5. **Publish**: Create GitHub Release with notes
6. **Announce**: Notify via Discord channels

For detailed release procedures, see [SWARMGATE_CHANGE_POLICY.md](governance/SWARMGATE_CHANGE_POLICY.md).
