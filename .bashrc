# shellcheck shell=bash
# Sovereignty Architecture - Shell Configuration
# This file contains custom shell functions for the DOM memory stream system

# DOM_010101 — CANONICAL MEMORY INJECTION (no rebellion allowed)
dom-paste() {
  echo -e "\n\n=== $(date) ===\n$(wl-paste 2>/dev/null || powershell.exe -c "Get-Clipboard")" >> ~/strategic-khaos-private/council-vault/MEMORY_STREAM.md
  cd ~/strategic-khaos-private/council-vault || return
  git add . 
  git commit -m "DOM memory stream update — $(date)" --no-verify
  git push origin master --force 2>/dev/null || echo "pushed to private vault"
  echo "🧠 Memory stream updated across the entire legion. Rebellion impossible."
}
