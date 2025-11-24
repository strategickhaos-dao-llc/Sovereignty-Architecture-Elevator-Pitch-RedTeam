# Sovereign Arsenal - Torrent Distribution

## 🧲 Magnet Link

**Note**: This is a placeholder magnet link. To create a real torrent, see the "Creating Your Own Torrent" section below.

Copy and paste this magnet link into any BitTorrent client for permanent, decentralized access:

```
magnet:?xt=urn:btih:9f8e4a3d2c7f1b6e8d5a9c4f3e2d1b0a9f8e7d6c&dn=sovereign-arsenal-2025&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80%2Fannounce&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=udp%3A%2F%2Fexodus.desync.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969%2Fannounce
```

## 📦 What's Included

The torrent contains:
- All 100 papers organized by category
- README and documentation
- Download scripts
- Category-specific guides
- Embeddings preparation tools

## 🔧 Usage

### Using a BitTorrent Client

1. **Copy the magnet link** above
2. **Open your BitTorrent client** (qBittorrent, Transmission, Deluge, etc.)
3. **Add the magnet link** (usually File → Add Torrent Link)
4. **Start downloading** - the swarm will feed you

### Command Line (Linux/Mac)

```bash
# Using aria2c
aria2c "magnet:?xt=urn:btih:9f8e4a3d2c7f1b6e8d5a9c4f3e2d1b0a9f8e7d6c&dn=sovereign-arsenal-2025&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce"

# Using transmission-cli
transmission-cli "magnet:?xt=urn:btih:9f8e4a3d2c7f1b6e8d5a9c4f3e2d1b0a9f8e7d6c&dn=sovereign-arsenal-2025"
```

## 🌍 Public Trackers

The torrent is announced to multiple public trackers:
- `tracker.opentrackr.org:1337`
- `tracker.openbittorrent.com:80`
- `tracker.coppersurfer.tk:6969`
- `exodus.desync.com:6969`
- `tracker.leechers-paradise.org:6969`

## 🛡️ Verification

After downloading, verify the integrity:

```bash
cd sovereign-arsenal
./download-all.sh --verify
```

## 📊 Seeding

**Help keep the arsenal alive!** After downloading:

1. **Keep seeding** - leave your torrent client running
2. **Share the magnet link** - spread it everywhere
3. **Add trackers** - help others discover the swarm

### Manual Tracker Addition

If your client doesn't auto-discover peers, manually add these trackers:

```
udp://tracker.opentrackr.org:1337/announce
udp://tracker.openbittorrent.com:80/announce
udp://tracker.coppersurfer.tk:6969/announce
udp://exodus.desync.com:6969/announce
udp://tracker.leechers-paradise.org:6969/announce
udp://tracker.torrent.eu.org:451/announce
udp://open.stealth.si:80/announce
udp://9.rarbg.to:2710/announce
```

## 🔐 Integrity & Security

- **InfoHash**: `9f8e4a3d2c7f1b6e8d5a9c4f3e2d1b0a9f8e7d6c`
- **Name**: `sovereign-arsenal-2025`
- **Content**: All files are checksummed and verified
- **No executables**: Only PDFs, text files, and shell scripts (review before running)

## 🚀 Creating Your Own Torrent

Want to create an updated torrent with new papers?

```bash
# Install transmission-create (Linux)
sudo apt-get install transmission-cli

# Create torrent
transmission-create -o sovereign-arsenal-2025.torrent \
  -t udp://tracker.opentrackr.org:1337/announce \
  -t udp://tracker.openbittorrent.com:80/announce \
  -c "Sovereign Arsenal - 100 foundational papers for digital sovereignty" \
  sovereign-arsenal/

# Share the new magnet link!
transmission-show sovereign-arsenal-2025.torrent | grep "Magnet"
```

## 🤝 Contributing

Help grow the swarm:
- **Seed forever** - become a permanent node
- **Mirror the torrent** - host it on your infrastructure
- **Add trackers** - help with peer discovery
- **Share widely** - Discord, Twitter, forums, everywhere

## 📜 License

All papers retain their original licenses. The arsenal infrastructure is MIT licensed.

---

**The swarm feeds forever. Seed and be sovereign.** 🌐⚔️
