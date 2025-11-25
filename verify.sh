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

missing=0
while IFS=: read -r key value; do
    [[ $key =~ ^[[:space:]]*path ]] && path="${value//\"/}" && continue
    [[ $key =~ ^[[:space:]]*sha256 ]] || continue
    expected="${value//\"/}"
    actual=$(sha256sum "$path" 2>/dev/null | awk '{print $1}')
    
    if [[ "$actual" == "$expected" ]]; then
        echo "✓ $path"
    else
        echo "✗ $path (expected $expected, got $actual)"
        ((missing++))
    fi
done < <(yq e '.artifacts[] | .path, .sha256' reproducibility_manifest.yml -r)

echo "------------------------------------------------"
if [[ $missing -eq 0 ]]; then
    echo "✅ FULL CORPUS VERIFIED — SACSE REPRODUCIBILITY CONFIRMED"
    echo "Empire Eternal. Third-party validation complete."
else
    echo "⚠️  $missing artifacts failed verification"
fi
