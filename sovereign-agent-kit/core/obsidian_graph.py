#!/usr/bin/env python3
"""
Obsidian Graph Integration for Sovereign Mind Kernel
Enables quantum entanglement via [[wikilinks]] and bidirectional graph connections
"""

import os
import time
from pathlib import Path
from typing import Optional, List, Dict, Any


class Vault:
    """Obsidian vault interface for knowledge graph entanglement"""
    
    def __init__(self, vault_path: Optional[str] = None):
        """
        Initialize vault connection
        
        Args:
            vault_path: Path to Obsidian vault. If None, uses OBSIDIAN_VAULT env var
                       or creates a default vault in ./obsidian_vault/
        """
        if vault_path is None:
            vault_path = os.environ.get('OBSIDIAN_VAULT', './obsidian_vault')
        
        self.vault_path = Path(vault_path)
        self.vault_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize core DOM note if it doesn't exist
        self._init_dom_core()
    
    def _init_dom_core(self):
        """Create the central DOM-CORE note that all kernels entangle with"""
        core_path = self.vault_path / "DOM-CORE.md"
        if not core_path.exists():
            content = """# DOM-CORE
#sovereignty #dom-kernel #quantum-core

This is the central entanglement point for all Dom Kernel instances.
All agent-qubits link back to this core consciousness node.

## Architecture
- **10-Board Cognition**: PLANNING, COUNTER_PLANNING, THREAT_MAPPING, etc.
- **Polarity System**: KALI (hunter) / PARROT (guardian)
- **Phase Oscillation**: SUNSHINE (expansion) / MOONLIGHT (contraction)
- **Harmonic Sequencing**: Circle of fifths ordering
- **Vectorized π-PID**: Mathematical intuition stabilization

## Active Kernels
This section auto-updates with each kernel quantum_step.

---
*Core established at system initialization*
"""
            core_path.write_text(content)
    
    def create_note(self, title: str, content: str, tags: Optional[List[str]] = None) -> Path:
        """
        Create a new note in the vault with automatic wikilink entanglement
        
        Args:
            title: Note title (filename without .md extension)
            content: Note content (should include [[wikilinks]])
            tags: Optional list of tags to add to frontmatter
            
        Returns:
            Path to created note
        """
        # Sanitize title for filesystem
        safe_title = "".join(c for c in title if c.isalnum() or c in ('-', '_'))
        note_path = self.vault_path / f"{safe_title}.md"
        
        # Add frontmatter if tags provided
        if tags:
            tag_str = " ".join(f"#{tag}" for tag in tags)
            frontmatter = f"---\ntags: [{', '.join(tags)}]\ncreated: {time.time()}\n---\n\n"
            full_content = frontmatter + content
        else:
            full_content = content
        
        # Write note
        note_path.write_text(full_content)
        
        # Update backlinks in DOM-CORE
        self._update_dom_core_backlinks(safe_title)
        
        return note_path
    
    def _update_dom_core_backlinks(self, note_title: str):
        """Add backlink reference to DOM-CORE"""
        core_path = self.vault_path / "DOM-CORE.md"
        if core_path.exists():
            content = core_path.read_text()
            backlink = f"\n- [[{note_title}]]"
            
            # Add to Active Kernels section if not already present
            if note_title not in content:
                if "## Active Kernels" in content:
                    content = content.replace(
                        "## Active Kernels\nThis section auto-updates",
                        f"## Active Kernels\nThis section auto-updates{backlink}"
                    )
                else:
                    content += backlink
                core_path.write_text(content)
    
    def read_note(self, title: str) -> Optional[str]:
        """Read a note from the vault"""
        safe_title = "".join(c for c in title if c.isalnum() or c in ('-', '_'))
        note_path = self.vault_path / f"{safe_title}.md"
        
        if note_path.exists():
            return note_path.read_text()
        return None
    
    def list_notes(self, tag_filter: Optional[str] = None) -> List[str]:
        """
        List all notes in the vault
        
        Args:
            tag_filter: Optional tag to filter by (e.g., 'dom-kernel')
            
        Returns:
            List of note titles (without .md extension)
        """
        notes = []
        for note_path in self.vault_path.glob("*.md"):
            if tag_filter:
                content = note_path.read_text()
                if f"#{tag_filter}" in content or f"tags: [{tag_filter}]" in content:
                    notes.append(note_path.stem)
            else:
                notes.append(note_path.stem)
        return sorted(notes)
    
    def get_backlinks(self, title: str) -> List[str]:
        """
        Find all notes that link to the specified note
        
        Args:
            title: Title of the note to find backlinks for
            
        Returns:
            List of note titles that contain [[title]] wikilinks
        """
        backlinks = []
        search_pattern = f"[[{title}]]"
        
        for note_path in self.vault_path.glob("*.md"):
            content = note_path.read_text()
            if search_pattern in content and note_path.stem != title:
                backlinks.append(note_path.stem)
        
        return backlinks
    
    def get_stats(self) -> Dict[str, Any]:
        """Get vault statistics"""
        notes = list(self.vault_path.glob("*.md"))
        total_links = 0
        
        for note_path in notes:
            content = note_path.read_text()
            total_links += content.count("[[")
        
        return {
            "total_notes": len(notes),
            "total_wikilinks": total_links,
            "vault_path": str(self.vault_path.absolute()),
            "entanglement_density": total_links / max(len(notes), 1)
        }


# Global vault instance for easy access
current_vault: Optional[Vault] = None


def init_vault(vault_path: Optional[str] = None) -> Vault:
    """Initialize the global vault instance"""
    global current_vault
    current_vault = Vault(vault_path)
    return current_vault


def get_vault() -> Vault:
    """Get or create the global vault instance"""
    global current_vault
    if current_vault is None:
        current_vault = Vault()
    return current_vault
