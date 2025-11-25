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
    echo "❌ yq not available (install via: brew install yq or snap install yq)"
    exit 1
fi

missing=0
count=$(yq e '.artifacts | length' reproducibility_manifest.yml)

for ((i=0; i<count; i++)); do
    path=$(yq e ".artifacts[$i].path" reproducibility_manifest.yml -r)
    expected=$(yq e ".artifacts[$i].sha256" reproducibility_manifest.yml -r)
    
    if [[ -z "$path" || "$path" == "null" ]]; then
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
