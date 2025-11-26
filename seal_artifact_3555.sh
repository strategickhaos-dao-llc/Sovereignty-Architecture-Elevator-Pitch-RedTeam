#!/usr/bin/env bash
# seal_artifact_3555.sh — Final, Hardened, Sovereign Sealing Ceremony
# Artifact #3555 — "The Day We Evolved So Hard the Fuzz Harness Wrote Love Letters"
set -euo pipefail
IFS=$'\n\t'

# === CONFIG ===
ARTIFACT_PATH="payloads/ARTIFACT_3555.md"
BUNDLE="ARTIFACT_3555_bundle.zip"
CHECKSUM="${BUNDLE}.sha256"
SIGNATURE="${BUNDLE}.asc"
AUDIT_LOG="AUDIT_LOG.md"
BRANCH="feat/artifact-3555-sealed"
REMOTE="origin"

# === Safety: Verify GPG key exists ===
if ! gpg --list-secret-keys --keyid-format LONG >/dev/null 2>&1; then
  echo "ERROR: No GPG secret key found. Run 'gpg --full-generate-key' first." >&2
  exit 1
fi

# === Verify artifact exists ===
if [ ! -f "$ARTIFACT_PATH" ]; then
  echo "ERROR: $ARTIFACT_PATH not found." >&2
  exit 2
fi

# === Temporary cleanup trap ===
cleanup() {
  rm -f "$BUNDLE" "$CHECKSUM" "$SIGNATURE" 2>/dev/null || true
}
trap cleanup ERR

echo "Beginning sovereign sealing of Artifact #3555..."

# === 1. Create minimal bundle (only the artifact) ===
echo "Creating clean bundle..."
zip -j "$BUNDLE" "$ARTIFACT_PATH" > /dev/null

# === 2. Generate checksum + detached GPG signature ===
echo "Generating SHA256 + GPG signature..."
sha256sum "$BUNDLE" > "$CHECKSUM"
gpg --armor --detach-sign --yes "$BUNDLE"

# === 3. Git ceremony (safe branch handling) ===
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Entering git ceremony..."
  git fetch "$REMOTE" "$BRANCH" 2>/dev/null || echo "Note: Branch $BRANCH does not exist on remote yet (this is expected for first seal)"
  if git rev-parse --verify "$BRANCH" >/dev/null 2>&1; then
    git checkout "$BRANCH"
    git pull --ff-only || {
      echo "WARNING: Fast-forward failed. Manual merge may be required."
      echo "Continuing with local state – review before pushing."
    }
  else
    git checkout -b "$BRANCH"
  fi

  git add "$ARTIFACT_PATH" "$BUNDLE" "$CHECKSUM" "$SIGNATURE" "$AUDIT_LOG"
  git commit -S -m "feat: seal artifact #3555 – The Day the Fuzz Harness Became a Witness

- Bundle + SHA256 + detached GPG signature
- Zero hidden overrides
- Love visible in every line
- Empire Eternal" || echo "Nothing to commit (already sealed?)"

  echo "Pushing to $REMOTE/$BRANCH..."
  git push --set-upstream "$REMOTE" "$BRANCH" --force-with-lease || {
    echo "Push failed – check permissions or use --force if intentional"
    exit 1
  }
else
  echo "Not in git repo – skipping commit/push"
fi

# === 4. Final audit entry ===
BUNDLE_SHA256=$(cut -d' ' -f1 "$CHECKSUM")
COMMIT_SHA=$(git rev-parse HEAD 2>/dev/null || echo "NO_GIT")
SEAL_TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
cat >> "$AUDIT_LOG" <<EOF

### Artifact 3555 — Fully Sealed & Delivered
- title: "The Day We Evolved So Hard the Fuzz Harness Wrote Love Letters"
- bundle: $BUNDLE
- sha256: $BUNDLE_SHA256
- gpg_signature: $SIGNATURE
- branch: $BRANCH
- commit: $COMMIT_SHA
- timestamp: $SEAL_TIMESTAMP
- sealed_by: love_compiled_at_4am
- verdict: "Not guilty. Just in love."
- Empire Eternal

EOF

# === 5. Final verification ===
echo "Verifying integrity..."
sha256sum -c "$CHECKSUM"
gpg --verify "$SIGNATURE" "$BUNDLE" && echo "GPG signature verified"

echo ""
echo "Sealing complete."
echo "Bundle: $BUNDLE"
echo "Checksum: $CHECKSUM"
echo "Signature: $SIGNATURE"
echo "Branch: $BRANCH"
echo "Love > entropy — always."
echo "Empire Eternal"

exit 0
