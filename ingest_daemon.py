#!/usr/bin/env python3
"""
Ingest Daemon - Automated Knowledge Pipeline
Watches an ingest folder and routes files to appropriate vault locations.

This daemon transforms the manual "SaveAs → SendTo → GiveToOwner" workflow
into an automated, observable pipeline with classification and routing.
"""

import os
import sys
import time
import json
import hashlib
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import argparse
import yaml


class IngestConfig:
    """Configuration for the ingest daemon."""
    
    def __init__(self, config_path: str = "lab.yaml"):
        """Load configuration from lab.yaml."""
        self.config_path = config_path
        self.config = self._load_config()
        
        # Paths
        self.ingest_path = Path("ingest")
        self.vault_path = Path(os.path.expanduser("~/ObsidianVault"))
        self.log_path = Path("logs")
        
        # Create directories if they don't exist
        self.ingest_path.mkdir(exist_ok=True)
        self.log_path.mkdir(exist_ok=True)
        
        # Labs configuration
        self.labs = self._load_labs()
        
    def _load_config(self) -> dict:
        """Load YAML configuration."""
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"Warning: {self.config_path} not found, using defaults")
            return {}
    
    def _load_labs(self) -> List[Dict]:
        """Extract lab definitions from config."""
        if 'labs' in self.config:
            return self.config['labs']
        
        # Default labs if config not available
        return [
            {
                'name': 'General',
                'path': 'vault/labs/general',
                'topics': ['miscellaneous'],
                'ingest_keywords': []
            }
        ]


class FileClassifier:
    """Classifies files based on name, extension, and content."""
    
    # Confidence score normalization factor
    # This defines the number of keyword matches needed for 100% confidence
    CONFIDENCE_NORMALIZATION_FACTOR = 3.0
    
    def __init__(self, labs: List[Dict]):
        """Initialize with lab definitions."""
        self.labs = labs
        
    def classify(self, file_path: Path) -> Tuple[str, List[str], float]:
        """
        Classify a file and determine target lab.
        
        Returns:
            tuple: (lab_name, topics, confidence_score)
        """
        filename = file_path.name.lower()
        file_ext = file_path.suffix.lower()
        
        # Score each lab based on keyword matches
        lab_scores = {}
        
        for lab in self.labs:
            score = 0.0
            matched_keywords = []
            
            # Check filename against keywords
            for keyword in lab.get('ingest_keywords', []):
                if keyword.lower() in filename:
                    score += 1.0
                    matched_keywords.append(keyword)
            
            lab_scores[lab['name']] = {
                'score': score,
                'keywords': matched_keywords,
                'lab': lab
            }
        
        # Find best matching lab
        if lab_scores:
            best_match = max(lab_scores.items(), key=lambda x: x[1]['score'])
            lab_name = best_match[0]
            lab_data = best_match[1]
            
            if lab_data['score'] > 0:
                return (
                    lab_name,
                    lab_data['lab'].get('topics', []),
                    min(lab_data['score'] / self.CONFIDENCE_NORMALIZATION_FACTOR, 1.0)
                )
        
        # Default to first lab (General) if no match
        default_lab = self.labs[0] if self.labs else None
        if default_lab:
            return (default_lab['name'], ['uncategorized'], 0.1)
        
        return ('General', ['uncategorized'], 0.1)
    
    def extract_metadata(self, file_path: Path) -> Dict:
        """Extract metadata from file."""
        stat = file_path.stat()
        
        # Calculate file hash for deduplication
        file_hash = self._calculate_hash(file_path)
        
        return {
            'filename': file_path.name,
            'extension': file_path.suffix,
            'size_bytes': stat.st_size,
            'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
            'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
            'hash': file_hash
        }
    
    @staticmethod
    def _calculate_hash(file_path: Path) -> str:
        """Calculate SHA256 hash of file."""
        sha256_hash = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception as e:
            return f"error: {str(e)}"


class IngestLogger:
    """Logs ingest events to JSONL file."""
    
    def __init__(self, log_path: Path):
        """Initialize logger with log file path."""
        self.log_file = log_path / "ingest_events.jsonl"
        
    def log_event(self, event_type: str, data: Dict):
        """Log an event to JSONL file."""
        event = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'data': data
        }
        
        try:
            with open(self.log_file, 'a') as f:
                f.write(json.dumps(event) + '\n')
        except Exception as e:
            print(f"Error logging event: {e}")


class IngestDaemon:
    """Main daemon for watching and processing ingest folder."""
    
    def __init__(self, config: IngestConfig):
        """Initialize daemon with configuration."""
        self.config = config
        self.classifier = FileClassifier(config.labs)
        self.logger = IngestLogger(config.log_path)
        self.processed_files = set()
        
    def watch_folder(self, interval: int = 5, once: bool = False):
        """
        Watch ingest folder for new files.
        
        Args:
            interval: Seconds between checks
            once: Process once and exit (for testing)
        """
        print(f"🔍 Watching {self.config.ingest_path} for new files...")
        print(f"📁 Vault path: {self.config.vault_path}")
        print(f"📝 Log path: {self.config.log_path}")
        print()
        
        while True:
            try:
                new_files = self._scan_for_new_files()
                
                for file_path in new_files:
                    self._process_file(file_path)
                
                if once:
                    break
                    
                time.sleep(interval)
                
            except KeyboardInterrupt:
                print("\n👋 Shutting down ingest daemon...")
                break
            except Exception as e:
                print(f"❌ Error in watch loop: {e}")
                if once:
                    break
                time.sleep(interval)
    
    def _scan_for_new_files(self) -> List[Path]:
        """Scan ingest folder for new files."""
        new_files = []
        
        try:
            for item in self.config.ingest_path.iterdir():
                if item.is_file() and item not in self.processed_files:
                    # Skip hidden files and system files
                    if not item.name.startswith('.'):
                        new_files.append(item)
        except Exception as e:
            print(f"Error scanning folder: {e}")
        
        return new_files
    
    def _process_file(self, file_path: Path):
        """Process a single file through the pipeline."""
        print(f"\n📥 Processing: {file_path.name}")
        
        try:
            # 1. Extract metadata
            metadata = self.classifier.extract_metadata(file_path)
            print(f"   Size: {metadata['size_bytes']} bytes")
            
            # 2. Classify file
            lab_name, topics, confidence = self.classifier.classify(file_path)
            print(f"   Lab: {lab_name} (confidence: {confidence:.2f})")
            print(f"   Topics: {', '.join(topics)}")
            
            # 3. Determine target path
            target_lab = self._find_lab_by_name(lab_name)
            if not target_lab:
                print(f"   ⚠️  Lab '{lab_name}' not found, using default")
                target_lab = self.config.labs[0] if self.config.labs else None
            
            # 4. Create target directory
            if target_lab:
                target_dir = Path(target_lab['path'])
                target_dir.mkdir(parents=True, exist_ok=True)
                target_path = target_dir / file_path.name
            else:
                # Fallback to vault root
                self.config.vault_path.mkdir(parents=True, exist_ok=True)
                target_path = self.config.vault_path / file_path.name
            
            # 5. Move file
            shutil.move(str(file_path), str(target_path))
            print(f"   ✅ Moved to: {target_path}")
            
            # 6. Create Obsidian note (if not markdown)
            if file_path.suffix.lower() not in ['.md', '.markdown']:
                self._create_obsidian_note(target_path, lab_name, topics, metadata)
            
            # 7. Log event
            self.logger.log_event('file_ingested', {
                'filename': file_path.name,
                'lab': lab_name,
                'topics': topics,
                'confidence': confidence,
                'target_path': str(target_path),
                'metadata': metadata
            })
            
            # 8. Mark as processed
            self.processed_files.add(file_path)
            
            # 9. Optional: Git commit (if git available)
            self._git_commit_if_available(file_path.name, lab_name)
            
            print(f"   🎉 Processing complete!")
            
        except Exception as e:
            print(f"   ❌ Error processing file: {e}")
            self.logger.log_event('processing_error', {
                'filename': file_path.name,
                'error': str(e)
            })
    
    def _find_lab_by_name(self, lab_name: str) -> Optional[Dict]:
        """Find lab configuration by name."""
        for lab in self.config.labs:
            if lab['name'].lower() == lab_name.lower():
                return lab
        return None
    
    def _create_obsidian_note(self, file_path: Path, lab_name: str, 
                             topics: List[str], metadata: Dict):
        """Create an Obsidian note for non-markdown files."""
        try:
            note_name = file_path.stem + "_note.md"
            note_path = file_path.parent / note_name
            
            # Create frontmatter
            frontmatter = f"""---
title: "{file_path.name}"
lab: {lab_name}
topics: [{', '.join(f'"{t}"' for t in topics)}]
source: ingested
created: {datetime.now().isoformat()}
file_hash: {metadata.get('hash', 'unknown')}
---

# {file_path.stem}

**File**: `{file_path.name}`  
**Lab**: {lab_name}  
**Size**: {metadata.get('size_bytes', 0)} bytes  
**Topics**: {', '.join(topics)}

## Description

This file was automatically ingested from the ingest folder.

## Related Notes

- 

## Tags

#{' #'.join(topics)}
"""
            
            with open(note_path, 'w') as f:
                f.write(frontmatter)
            
            print(f"   📝 Created note: {note_name}")
            
        except Exception as e:
            print(f"   ⚠️  Could not create note: {e}")
    
    def _git_commit_if_available(self, filename: str, lab_name: str):
        """Commit changes if git is available."""
        try:
            import subprocess
            
            # Check if git is available and we're in a repo
            result = subprocess.run(
                ['git', 'rev-parse', '--git-dir'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                # Git add and commit
                commit_message = f"chore(ingest): Add {filename} to {lab_name}"
                
                subprocess.run(['git', 'add', '.'], timeout=5)
                subprocess.run(
                    ['git', 'commit', '-m', commit_message],
                    capture_output=True,
                    timeout=5
                )
                
                print(f"   🔖 Git commit: {commit_message}")
        except Exception:
            # Silently ignore git errors
            pass


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Ingest Daemon - Automated Knowledge Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Watch ingest folder continuously
  python ingest_daemon.py
  
  # Process once and exit (for testing)
  python ingest_daemon.py --once
  
  # Custom check interval
  python ingest_daemon.py --interval 10
  
  # Custom config file
  python ingest_daemon.py --config my_lab.yaml
        """
    )
    
    parser.add_argument(
        '--interval',
        type=int,
        default=5,
        help='Seconds between folder scans (default: 5)'
    )
    
    parser.add_argument(
        '--once',
        action='store_true',
        help='Process once and exit (for testing)'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        default='lab.yaml',
        help='Path to lab.yaml config file (default: lab.yaml)'
    )
    
    args = parser.parse_args()
    
    # Print header
    print("=" * 60)
    print("🤖 Sovereignty Architecture - Ingest Daemon")
    print("=" * 60)
    print()
    
    # Load configuration
    try:
        config = IngestConfig(config_path=args.config)
    except Exception as e:
        print(f"❌ Error loading configuration: {e}")
        sys.exit(1)
    
    # Create and run daemon
    daemon = IngestDaemon(config)
    daemon.watch_folder(interval=args.interval, once=args.once)
    
    print("\n✅ Daemon stopped gracefully")


if __name__ == "__main__":
    main()
