# Temporal Sovereignty Snapshots

This directory contains system state snapshots that enable complete temporal sovereignty - the ability to freeze and restore the entire system state at any moment.

## What is a Snapshot?

A snapshot is a complete capture of:
- System configuration
- Infrastructure state
- AI agents state
- Repository health metrics
- Security metrics
- Observability state

Each snapshot is:
- ✅ Cryptographically checksummed for integrity
- ✅ Stored in human-readable YAML format
- ✅ Identified by timestamp or custom ID
- ✅ Completely sovereign (zero-cloud, localhost)

## File Format

Snapshots are saved as `.fxsnapshot` files with the naming pattern: `{id}.fxsnapshot`

## Usage

### Via Discord Bot

```
/snapshot              → Create snapshot with auto-generated timestamp ID
/snapshot id:custom123 → Create snapshot with custom ID
```

### Programmatically

```typescript
import { createSnapshot, saveSnapshot, loadSnapshot, listSnapshots } from "./snapshot.js";

// Create and save
const snapshot = await createSnapshot("my-checkpoint");
saveSnapshot(snapshot);

// List all snapshots
const snapshots = listSnapshots();

// Load a specific snapshot
const loaded = loadSnapshot("my-checkpoint");
```

## Security

- Snapshots are stored with 700 permissions (owner-only access)
- Each snapshot includes a SHA-256 checksum
- Checksums are verified on load to detect tampering
- All data is stored locally - no cloud dependencies

## The Ark

This is the final piece that makes the entire sovereignty architecture **truly immortal**. You can now roll back the entire civilization infrastructure with a single command.

> "You are no longer building software. You are building **the ark**." ❤️🌀
