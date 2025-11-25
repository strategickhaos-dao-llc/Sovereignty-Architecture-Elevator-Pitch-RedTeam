#!/bin/bash

# Auto-stamp helper for defensive publication artifacts
# Usage: ./auto_stamp.sh [--dry-run | --commit]
# Dry-run: Previews commands without executing
# Commit: Runs, commits proofs, pushes to safety/charitable-commitment

DRY_RUN=0
COMMIT=0
REPO_BRANCH="safety/charitable-commitment"
FILES_TO_STAMP=(
  "docs/legal/defensive_publication.yaml"
  # Add more: "docs/CHARITABLE_COMMITMENT.md" etc.
)
GPG_KEYID="${GPG_KEYID:-}"  # Set via env: export GPG_KEYID=your_key_id
PROOFS_DIR="docs/proofs"

if [[ "$1" == "--dry-run" ]]; then
  DRY_RUN=1
elif [[ "$1" == "--commit" ]]; then
  COMMIT=1
else
  echo "Usage: $0 [--dry-run | --commit]"
  exit 1
fi

# Validate GPG_KEYID is set
if [[ -z "$GPG_KEYID" ]]; then
  echo "Error: GPG_KEYID not set. Export it: export GPG_KEYID=your_key_id"
  exit 1
fi

# Ensure on branch (warn user)
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [[ "$CURRENT_BRANCH" != "$REPO_BRANCH" ]]; then
  echo "Warning: Switching from '$CURRENT_BRANCH' to '$REPO_BRANCH'"
  echo "Ensure uncommitted changes are stashed or committed."
  read -p "Continue? [y/N] " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 1
  fi
  git checkout "$REPO_BRANCH" 2>/dev/null || git checkout -b "$REPO_BRANCH"
fi

mkdir -p "$PROOFS_DIR"

for FILE in "${FILES_TO_STAMP[@]}"; do
  if [[ ! -f "$FILE" ]]; then
    echo "Error: $FILE not found. Skipping."
    continue
  fi

  BASE=$(basename "$FILE")
  HASH_FILE="$PROOFS_DIR/$BASE.hash"
  OTS_FILE="$PROOFS_DIR/$BASE.ots"
  SIG_FILE="$PROOFS_DIR/$BASE.sig"

  # Step 1: SHA256
  SHA_CMD="sha256sum \"$FILE\" | awk '{print \$1}' > \"$HASH_FILE\""
  if [[ $DRY_RUN -eq 1 ]]; then
    echo "[DRY] Would run: $SHA_CMD"
  else
    eval "$SHA_CMD"
    echo "SHA256 written to $HASH_FILE"
  fi

  # Step 2: OpenTimestamps stamp
  OTS_CMD="ots stamp \"$FILE\" -o \"$OTS_FILE\""
  if [[ $DRY_RUN -eq 1 ]]; then
    echo "[DRY] Would run: $OTS_CMD"
  else
    eval "$OTS_CMD"
    echo "OTS stamped to $OTS_FILE"
  fi

  # Step 3: GPG detached sig
  GPG_CMD="gpg --local-user \"$GPG_KEYID\" --armor --detach-sign -o \"$SIG_FILE\" \"$FILE\""
  if [[ $DRY_RUN -eq 1 ]]; then
    echo "[DRY] Would run: $GPG_CMD"
  else
    eval "$GPG_CMD"
    echo "GPG signed to $SIG_FILE"
  fi

  # Step 4: If SLOG needs update (for defensive_publication.yaml only)
  if [[ "$BASE" == "defensive_publication.yaml" ]]; then
    SLOG_TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    SLOG_SHA=$(sha256sum "$FILE" | awk '{print $1}')
    # Check if SLOG already exists and remove old entries
    if grep -q "^SLOG_TIMESTAMP:" "$FILE"; then
      if [[ $DRY_RUN -eq 1 ]]; then
        echo "[DRY] Would update existing SLOG entries"
      else
        # Remove existing SLOG entries before appending new ones
        sed -i '/^SLOG_TIMESTAMP:/d' "$FILE"
        sed -i '/^SLOG_SHA256:/d' "$FILE"
        # Remove trailing empty lines
        sed -i -e :a -e '/^\n*$/{$d;N;ba' -e '}' "$FILE"
      fi
    fi
    SLOG_APPEND="printf \"\n\nSLOG_TIMESTAMP: %s\nSLOG_SHA256: %s\n\" \"$SLOG_TS\" \"$SLOG_SHA\" >> \"$FILE\""
    if [[ $DRY_RUN -eq 1 ]]; then
      echo "[DRY] Would append SLOG: $SLOG_APPEND"
    else
      eval "$SLOG_APPEND"
      echo "SLOG appended/updated in $FILE"
    fi
  fi
done

# Export pubkey if missing
PUBKEY_FILE="$PROOFS_DIR/gpg_pubkey.asc"
if [[ ! -f "$PUBKEY_FILE" ]]; then
  PUBKEY_CMD="gpg --armor --export \"$GPG_KEYID\" > \"$PUBKEY_FILE\""
  if [[ $DRY_RUN -eq 1 ]]; then
    echo "[DRY] Would export pubkey: $PUBKEY_CMD"
  else
    eval "$PUBKEY_CMD"
    echo "Pubkey exported to $PUBKEY_FILE"
  fi
fi

if [[ $COMMIT -eq 1 ]]; then
  # Add files only if they exist (avoid wildcard errors)
  shopt -s nullglob
  PROOF_FILES=("$PROOFS_DIR"/*.hash "$PROOFS_DIR"/*.ots "$PROOFS_DIR"/*.sig)
  shopt -u nullglob
  
  if [[ ${#PROOF_FILES[@]} -gt 0 ]]; then
    git add "${PROOF_FILES[@]}"
  fi
  
  if [[ -f "$PROOFS_DIR/gpg_pubkey.asc" ]]; then
    git add "$PROOFS_DIR/gpg_pubkey.asc"
  fi
  
  git add "${FILES_TO_STAMP[@]}" 2>/dev/null || true
  git commit -m "chore: add/update defensive publication proofs (.hash, .ots, .sig, SLOG)"
  git push origin "$REPO_BRANCH"
  echo "Proofs committed and pushed."
fi

echo "Auto-stamp complete."
