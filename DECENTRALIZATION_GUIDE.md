# Decentralization Guide
**Repository Mirroring & Censorship Resistance Strategy**

> **Infrastructure Sovereignty Through Decentralization**
> 
> This guide establishes procedures for mirroring the entire repository to decentralized platforms (Radicle, IPFS, Skynet, Arweave) to ensure censorship resistance and data permanence.

## Overview

Centralized code hosting (GitHub, GitLab) creates single points of failure vulnerable to:
- Corporate policy changes or account suspension
- Government censorship or seizure
- Service outages or business failure
- Terms of service violations (real or alleged)

**Solution**: Mirror all critical repositories to multiple decentralized platforms, ensuring code remains accessible regardless of any single platform's availability.

---

## Platform Comparison

| Platform | Type | Permanence | Cost | Best For |
|----------|------|------------|------|----------|
| **Radicle** | P2P Git | High (if seeded) | Free | Active development |
| **IPFS** | Content-addressed | Medium (needs pinning) | Low | Regular updates |
| **Skynet** | Content delivery | Medium | Low | Web access |
| **Arweave** | Permanent storage | Permanent | Medium | Archives |

### Decision Matrix

- **Radicle**: Primary decentralized development platform
- **IPFS**: Regular snapshots, community pinning
- **Skynet**: Quick access, CDN-like distribution
- **Arweave**: Permanent, immutable archival of releases

---

## Radicle Setup

### Installation

```bash
# Install Radicle
curl -sSf https://radicle.xyz/install | sh

# Or via Homebrew
brew install radicle-cli

# Verify installation
rad --version
```

### Repository Initialization

```bash
# Navigate to repository
cd /path/to/Sovereignty-Architecture-Elevator-Pitch-

# Initialize Radicle project
rad init --name "Sovereignty Architecture" \
         --description "Discord-native DevOps sovereignty platform"

# Add remote
rad remote add origin radicle://<project-id>

# Push to Radicle
rad push
```

### Seed Node Setup

```bash
# Run Radicle seed node (continuous seeding)
rad node start

# Configure automatic seeding for project
rad seed add <project-id>

# Verify seeding status
rad node status
```

### Access Instructions

```markdown
## Accessing via Radicle

1. Install Radicle CLI: https://radicle.xyz/install
2. Clone repository: `rad clone radicle://<project-id>`
3. Browse on app: https://app.radicle.xyz/seeds/<project-id>
```

---

## IPFS Deployment

### Installation

```bash
# Install IPFS
curl -o- https://raw.githubusercontent.com/ipfs/kubo/master/install.sh | bash

# Or via package manager
sudo apt install ipfs  # Ubuntu/Debian
brew install ipfs      # macOS

# Initialize IPFS
ipfs init

# Start daemon
ipfs daemon &
```

### Repository Upload

```bash
# Navigate to repository root
cd /path/to/Sovereignty-Architecture-Elevator-Pitch-

# Add entire repository to IPFS
ipfs add -r . > ipfs_manifest.txt

# Get CID of root directory
ROOT_CID=$(tail -n 1 ipfs_manifest.txt | awk '{print $2}')
echo "Repository CID: $ROOT_CID"

# Pin to ensure persistence
ipfs pin add $ROOT_CID
```

### Pinning Services

```bash
# Use Pinata for permanent pinning
export PINATA_API_KEY="your_api_key"
export PINATA_SECRET_KEY="your_secret_key"

# Pin via Pinata
curl -X POST "https://api.pinata.cloud/pinning/pinByHash" \
  -H "Content-Type: application/json" \
  -H "pinata_api_key: $PINATA_API_KEY" \
  -H "pinata_secret_api_key: $PINATA_SECRET_KEY" \
  -d "{\"hashToPin\": \"$ROOT_CID\"}"
```

### Access Instructions

```markdown
## Accessing via IPFS

1. Public Gateway: https://ipfs.io/ipfs/<CID>
2. Cloudflare Gateway: https://cloudflare-ipfs.com/ipfs/<CID>
3. Local Node: ipfs cat /ipfs/<CID>/<file>
4. Browser Extension: Use IPFS Companion
```

---

## Skynet Integration

### Installation

```bash
# Install Skynet CLI
npm install -g @skynetlabs/skynet-nodejs

# Or use web interface at: https://siasky.net
```

### Upload Script

```javascript
// upload-to-skynet.js
const { SkynetClient } = require("@skynetlabs/skynet-nodejs");

const client = new SkynetClient("https://siasky.net");

async function uploadDirectory() {
  const directory = "./";
  const { skylink } = await client.uploadDirectory(
    directory,
    "Sovereignty-Architecture"
  );
  
  console.log(`Uploaded to Skynet: ${skylink}`);
  console.log(`Access at: https://siasky.net/${skylink}`);
  
  return skylink;
}

uploadDirectory().catch(console.error);
```

```bash
# Run upload
node upload-to-skynet.js

# Save skylink for documentation
echo "SKYLINK: <skylink>" >> DECENTRALIZATION_MANIFEST.txt
```

### Access Instructions

```markdown
## Accessing via Skynet

1. Direct Link: https://siasky.net/<skylink>
2. Alternative Portal: https://skynetfree.net/<skylink>
3. Handshake Domain: Create .hns domain pointing to skylink
```

---

## Arweave Archival

### Installation

```bash
# Install Arweave CLI via Bundlr
npm install -g @bundlr-network/client

# Or use ArDrive CLI
npm install -g ardrive-cli
```

### Wallet Setup

```bash
# Generate Arweave wallet (or import existing)
npx arweave key-create arweave-key.json

# Fund wallet with AR tokens (required for uploads)
# Purchase AR on exchange and send to wallet address
npx arweave key-show arweave-key.json
```

### Upload to Arweave

```bash
# Package repository for archival
git archive --format=tar.gz --prefix=sovereignty-architecture/ HEAD > sovereignty-architecture.tar.gz

# Upload via Bundlr (recommended - instant finality)
bundlr upload sovereignty-architecture.tar.gz \
  -h https://node1.bundlr.network \
  -w arweave-key.json \
  -c arweave

# Save transaction ID
echo "ARWEAVE_TX: <transaction-id>" >> DECENTRALIZATION_MANIFEST.txt
```

### Upload Releases to Arweave

```bash
#!/bin/bash
# archive-release.sh - Archive each release to Arweave

VERSION=$1
git archive --format=tar.gz --prefix=sovereignty-architecture-$VERSION/ v$VERSION > release-$VERSION.tar.gz

TX_ID=$(bundlr upload release-$VERSION.tar.gz -h https://node1.bundlr.network -w arweave-key.json -c arweave --no-confirmation)

echo "Release $VERSION archived to Arweave: $TX_ID"
echo "https://arweave.net/$TX_ID"
```

### Access Instructions

```markdown
## Accessing via Arweave

1. Direct Link: https://arweave.net/<tx-id>
2. Gateway: https://ar-io.net/<tx-id>
3. ArDrive: Use ArDrive web app to browse
4. Permanent: Content is stored forever (truly immutable)
```

---

## Automation Strategy

### Continuous Mirroring Script

```bash
#!/bin/bash
# mirror-sync.sh - Automated repository mirroring

set -e

REPO_PATH="/path/to/Sovereignty-Architecture-Elevator-Pitch-"
LOG_FILE="/var/log/mirror-sync.log"

log() {
  echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1" | tee -a $LOG_FILE
}

log "Starting repository mirror sync..."

# 1. Radicle sync
log "Syncing to Radicle..."
cd $REPO_PATH
rad push || log "Radicle push failed"

# 2. IPFS update
log "Updating IPFS..."
NEW_CID=$(ipfs add -r -Q $REPO_PATH)
ipfs pin add $NEW_CID
log "New IPFS CID: $NEW_CID"

# 3. Skynet update (weekly only to save costs)
if [ $(date +%u) -eq 1 ]; then
  log "Updating Skynet (weekly sync)..."
  node /path/to/upload-to-skynet.js || log "Skynet upload failed"
fi

# 4. Arweave (major releases only - manual trigger)
if [ ! -z "$ARWEAVE_RELEASE" ]; then
  log "Archiving release to Arweave..."
  ./scripts/archive-release.sh $ARWEAVE_RELEASE
fi

log "Mirror sync completed successfully"
```

### Cron Schedule

```cron
# Run mirror sync daily at 2 AM
0 2 * * * /path/to/scripts/mirror-sync.sh

# Weekly Arweave release check (manual trigger file)
0 3 * * 0 [ -f /tmp/arweave-release ] && /path/to/scripts/archive-release.sh $(cat /tmp/arweave-release) && rm /tmp/arweave-release
```

### GitHub Actions Integration

```yaml
# .github/workflows/decentralized-mirror.yml
name: Decentralized Mirror Sync

on:
  push:
    branches: [ main, master ]
  release:
    types: [ published ]
  workflow_dispatch:

jobs:
  mirror:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
      
      - name: Setup IPFS
        run: |
          wget https://dist.ipfs.tech/kubo/v0.16.0/kubo_v0.16.0_linux-amd64.tar.gz
          tar -xzf kubo_v0.16.0_linux-amd64.tar.gz
          cd kubo && sudo ./install.sh
          ipfs init
          
      - name: Upload to IPFS
        run: |
          ipfs daemon &
          sleep 5
          CID=$(ipfs add -r -Q .)
          echo "IPFS CID: $CID"
          echo "IPFS_CID=$CID" >> $GITHUB_ENV
          
      - name: Upload to Skynet
        uses: SkynetLabs/deploy-to-skynet-action@v2
        with:
          upload-dir: ./
          
      - name: Archive Release to Arweave
        if: github.event_name == 'release'
        env:
          ARWEAVE_KEY: ${{ secrets.ARWEAVE_KEY }}
        run: |
          npm install -g @bundlr-network/client
          git archive --format=tar.gz HEAD > release.tar.gz
          bundlr upload release.tar.gz -h https://node1.bundlr.network -w <(echo "$ARWEAVE_KEY") -c arweave
```

---

## Verification Procedures

### Weekly Verification Checklist

```bash
#!/bin/bash
# verify-mirrors.sh - Verify all mirrors are accessible

# 1. Check Radicle
rad node status
rad sync <project-id>

# 2. Check IPFS
IPFS_CID="<latest-cid>"
curl -f "https://ipfs.io/ipfs/$IPFS_CID" > /dev/null && echo "✓ IPFS accessible" || echo "✗ IPFS failed"

# 3. Check Skynet
SKYLINK="<latest-skylink>"
curl -f "https://siasky.net/$SKYLINK" > /dev/null && echo "✓ Skynet accessible" || echo "✗ Skynet failed"

# 4. Check Arweave
ARWEAVE_TX="<latest-tx>"
curl -f "https://arweave.net/$ARWEAVE_TX" > /dev/null && echo "✓ Arweave accessible" || echo "✗ Arweave failed"
```

### Quarterly Full Verification

- [ ] Clone from each platform and verify integrity
- [ ] Test all access methods (gateways, apps, CLIs)
- [ ] Verify pinning/seeding is active
- [ ] Check storage costs and fund balances
- [ ] Update documentation with current CIDs/links
- [ ] Test recovery procedures

---

## Cost Analysis

### Estimated Monthly Costs

| Platform | Storage | Bandwidth | Monthly Cost | Annual Cost |
|----------|---------|-----------|--------------|-------------|
| **Radicle** | Free | Free | $0 | $0 |
| **IPFS** (Pinata) | ~5 GB | Moderate | $0-20 | $0-240 |
| **Skynet** | ~5 GB | Moderate | $0-10 | $0-120 |
| **Arweave** | One-time | Permanent | $5-50/upload | ~$100 |

**Total Estimated**: $15-80/month for continuous mirroring, plus one-time Arweave costs for major releases.

### Funding Strategy

- Allocate from DAO treasury or operations budget
- Community pinning for IPFS (volunteer nodes)
- Arweave archival for major releases only (not daily updates)
- Consider decentralized storage token incentives

---

## Community Access

### README Addition

```markdown
## 🌐 Decentralized Access

This repository is mirrored to multiple decentralized platforms for censorship resistance:

- **Radicle**: `rad clone radicle://<project-id>`
- **IPFS**: https://ipfs.io/ipfs/<cid>
- **Skynet**: https://siasky.net/<skylink>
- **Arweave**: https://arweave.net/<tx-id>

If GitHub becomes unavailable, access the latest version through any of these platforms.
```

### Documentation

Maintain `/DECENTRALIZATION_MANIFEST.txt` with current identifiers:

```
# Sovereignty Architecture - Decentralized Access Points
# Last Updated: 2025-11-23

RADICLE_ID: rad:z2u7...
IPFS_CID: Qm...
SKYNET_LINK: sia://...
ARWEAVE_TX: <latest-release-tx>

# Historical Archives
RELEASE_v1.0_ARWEAVE: <tx-id>
RELEASE_v2.0_ARWEAVE: <tx-id>
```

---

## Disaster Recovery

### Scenario: GitHub Account Suspended

1. **Immediate** (Hour 1):
   - Announce suspension on Discord and Twitter
   - Direct community to Radicle primary mirror
   - Post IPFS CID for latest snapshot

2. **Short-term** (Days 1-3):
   - Set up alternative GitHub organization or GitLab
   - Import from Radicle to new hosting
   - Update DNS/documentation to point to new location
   - Continue development on Radicle if needed

3. **Long-term** (Week 1+):
   - Evaluate long-term hosting strategy
   - Increase reliance on Radicle for development
   - Strengthen community pinning network
   - Document lessons learned

### Scenario: All Centralized Platforms Down

- **Primary**: Use Radicle for ongoing development
- **Distribution**: IPFS for code distribution
- **Archive**: Arweave for release verification
- **Communication**: Update via decentralized social (Mastodon, Lens)

---

## Success Metrics

### Implementation Success (Month 1)

- [ ] Repository mirrored to all 4 platforms
- [ ] Automated sync scripts operational
- [ ] Verification tests passing
- [ ] Community access documentation published
- [ ] At least 3 community members verify access

### Ongoing Health

- [ ] 99%+ uptime on verification checks
- [ ] <24 hour sync delay for updates
- [ ] Sufficient funding for ongoing costs
- [ ] Active community pinning (IPFS)
- [ ] Quarterly full recovery test successful

---

## Resources

- Radicle Documentation: https://docs.radicle.xyz
- IPFS Documentation: https://docs.ipfs.tech
- Skynet Documentation: https://docs.skynetlabs.com
- Arweave Documentation: https://docs.arweave.org

---

## Document Control

| Field | Value |
|-------|-------|
| Version | 1.0 |
| Status | Implementation Ready |
| Owner | Strategickhaos DAO LLC |
| Created | 2025-11-23 |
| Next Review | Monthly |

---

*© 2025 Strategickhaos DAO LLC. Licensed under MIT for community use.*
