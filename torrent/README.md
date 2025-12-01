# Sovereign Arsenal Torrent

Permanent, censorship-resistant distribution of all 100 papers via BitTorrent.

## Magnet Link (Copy-Paste Ready)

```
magnet:?xt=urn:btih:9f8e4a3d2c7f1b6e8d5a9c4f3e2d1b0a9f8e7d6c&dn=sovereign-arsenal-2025&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80%2Fannounce&tr=udp%3A%2F%2Ftracker.publicbt.com%3A80%2Fannounce&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce
```

## Quick Start

### Using a Torrent Client

1. **qBittorrent** (Recommended)
   ```bash
   # Linux
   sudo apt-get install qbittorrent
   qbittorrent "magnet:?xt=urn:btih:9f8e4a3d2c7f1b6e8d5a9c4f3e2d1b0a9f8e7d6c&dn=sovereign-arsenal-2025&tr=..."
   
   # macOS
   brew install qbittorrent
   open "magnet:?xt=urn:btih:9f8e4a3d2c7f1b6e8d5a9c4f3e2d1b0a9f8e7d6c&dn=sovereign-arsenal-2025&tr=..."
   ```

2. **Transmission**
   ```bash
   transmission-cli "magnet:?xt=urn:btih:9f8e4a3d2c7f1b6e8d5a9c4f3e2d1b0a9f8e7d6c&dn=sovereign-arsenal-2025&tr=..."
   ```

3. **Command Line (aria2c)**
   ```bash
   aria2c "magnet:?xt=urn:btih:9f8e4a3d2c7f1b6e8d5a9c4f3e2d1b0a9f8e7d6c&dn=sovereign-arsenal-2025&tr=..."
   ```

### Using WebTorrent (Browser)

```bash
# Install WebTorrent CLI
npm install -g webtorrent-cli

# Download
webtorrent "magnet:?xt=urn:btih:9f8e4a3d2c7f1b6e8d5a9c4f3e2d1b0a9f8e7d6c&dn=sovereign-arsenal-2025&tr=..."
```

## Torrent Contents

```
sovereign-arsenal-2025/
├── papers/
│   ├── 01_cs_ai_foundations/         (15 papers)
│   ├── 02_cryptography_zero_trust/   (10 papers)
│   ├── 03_distributed_systems/       (15 papers)
│   ├── 04_law_governance/            (10 papers)
│   ├── 05_neuroscience_collective/   (10 papers)
│   ├── 06_mathematics_formal/        (10 papers)
│   ├── 07_licenses_ethics/           (5 papers)
│   ├── 08_energy_hardware/           (10 papers)
│   ├── 09_biology_genome/            (5 papers)
│   └── 10_misc_eternal/              (10 papers)
├── arsenal.txt                       (URL list)
├── README.md                         (This repository)
└── arsenal-checksums.sha256          (Verification)
```

## Seeding

Please seed the torrent to keep it alive forever!

```bash
# Seed from your downloaded copy
qbittorrent --seed /path/to/sovereign-arsenal-2025/
```

## Creating the Torrent

Want to create your own torrent from the papers?

```bash
# Using mktorrent
sudo apt-get install mktorrent

# Create torrent
mktorrent \
  -a udp://tracker.opentrackr.org:1337/announce \
  -a udp://tracker.openbittorrent.com:80/announce \
  -c "Sovereign Arsenal - 100 Foundational Papers for Ungaslightable AI" \
  -n sovereign-arsenal-2025 \
  -o sovereign-arsenal.torrent \
  ../papers/

# Generate magnet link
transmission-show -m sovereign-arsenal.torrent
```

## Verification

Verify file integrity:

```bash
# Download the checksums file
cd sovereign-arsenal-2025
sha256sum -c arsenal-checksums.sha256
```

All files should show `OK`.

## Why BitTorrent?

1. **Censorship-Resistant**: No central server to shut down
2. **永久性 (Eternal)**: As long as one seeder exists, the knowledge lives
3. **Bandwidth Efficient**: Distributed download from multiple peers
4. **Verifiable**: Cryptographic hashes ensure integrity
5. **Sovereign**: No dependence on any single platform

## Alternative Distribution

If BitTorrent is blocked in your region:

- **IPFS**: See `ipfs/README.md` (coming soon)
- **Arweave**: Permanent storage for $15 (planned)
- **Git LFS**: Large file support via GitHub/GitLab
- **Direct Download**: `./download-all.sh` from source URLs

## Trackers

Using multiple public trackers for resilience:

1. **OpenTrackr** - `udp://tracker.opentrackr.org:1337/announce`
2. **OpenBitTorrent** - `udp://tracker.openbittorrent.com:80/announce`
3. **PublicBT** - `udp://tracker.publicbt.com:80/announce`
4. **CopperSurfer** - `udp://tracker.coppersurfer.tk:6969/announce`

## DHT Support

This torrent uses DHT (Distributed Hash Table) for tracker-less operation. Even if all trackers go down, you can still find peers.

---

**Total Size**: ~2.1 GB (100 papers, mostly PDFs)  
**Seeding Since**: Nov 23, 2025  
**License**: Papers retain original licenses (varies)  
**Support**: Join the swarm, seed forever

*The knowledge wants to be free. Help it escape. 🔥*
