#!/bin/bash
# verify.sh — One-command third-party reproducibility verification
# Place in repo root, chmod +x verify.sh

echo "Strategickhaos SACSE Corpus Verification — $(date)"
echo "Manifest: reproducibility_manifest.yml"
echo "------------------------------------------------"

if ! command -v sha256sum >/dev/null; then
    echo "❌ sha256sum not available"
    exit 1
fi

if ! command -v yq >/dev/null; then
    echo "❌ yq not available (install: https://github.com/mikefarah/yq)"
    exit 1
fi

# Get the repo root directory for path validation
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

missing=0
artifact_count=$(yq e '.artifacts | length' reproducibility_manifest.yml)

for ((i=0; i<artifact_count; i++)); do
    path=$(yq e ".artifacts[$i].path" reproducibility_manifest.yml -r)
    expected=$(yq e ".artifacts[$i].sha256" reproducibility_manifest.yml -r)
    
    # Validate path doesn't escape repo root (prevent path traversal)
    resolved_path=$(realpath -m "$REPO_ROOT/$path" 2>/dev/null)
    if [[ ! "$resolved_path" == "$REPO_ROOT"/* ]]; then
        echo "⚠ $path (unsafe path - skipped)"
        ((missing++))
        continue
    fi
    
    actual=$(sha256sum "$path" 2>/dev/null | awk '{print $1}')
    
    if [[ "$actual" == "$expected" ]]; then
        echo "✓ $path"
    else
        echo "✗ $path (expected $expected, got $actual)"
        ((missing++))
    fi
done

echo "------------------------------------------------"
if [[ $missing -eq 0 ]]; then
    echo "✅ FULL CORPUS VERIFIED — SACSE REPRODUCIBILITY CONFIRMED"
    echo "Empire Eternal. Third-party validation complete."
else
    echo "⚠️  $missing artifacts failed verification"
fi
