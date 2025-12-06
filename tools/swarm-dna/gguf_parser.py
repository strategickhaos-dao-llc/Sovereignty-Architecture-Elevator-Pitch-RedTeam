#!/usr/bin/env python3
"""
GGUF Metadata Parser for Swarm DNA Architecture

Extracts metadata from GGUF (GPT-Generated Unified Format) model files
found in .ollama/models/blob/ directories and converts them to YAML.

This tool enables Dom's vision: treating model blobs as parseable projects
with structured metadata, lineage tracking, and narrative integration.

Built for Strategickhaos Swarm Intelligence
"""

import os
import sys
import struct
import json
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


class GGUFParser:
    """Parse GGUF model files and extract metadata"""
    
    # GGUF magic number and version
    GGUF_MAGIC = 0x46554747  # "GGUF" in little-endian
    GGUF_VERSION = 3
    
    # GGUF value types
    GGUF_TYPE_UINT8 = 0
    GGUF_TYPE_INT8 = 1
    GGUF_TYPE_UINT16 = 2
    GGUF_TYPE_INT16 = 3
    GGUF_TYPE_UINT32 = 4
    GGUF_TYPE_INT32 = 5
    GGUF_TYPE_FLOAT32 = 6
    GGUF_TYPE_BOOL = 7
    GGUF_TYPE_STRING = 8
    GGUF_TYPE_ARRAY = 9
    GGUF_TYPE_UINT64 = 10
    GGUF_TYPE_INT64 = 11
    GGUF_TYPE_FLOAT64 = 12
    
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.metadata = {}
        
    def parse(self) -> Dict[str, Any]:
        """Parse GGUF file and extract metadata"""
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")
            
        with open(self.file_path, 'rb') as f:
            # Read magic number
            magic = struct.unpack('<I', f.read(4))[0]
            if magic != self.GGUF_MAGIC:
                raise ValueError(
                    f"Invalid GGUF file: expected magic {hex(self.GGUF_MAGIC)}, "
                    f"got {hex(magic)}"
                )
                
            # Read version
            version = struct.unpack('<I', f.read(4))[0]
            
            # Read tensor count and metadata count
            tensor_count = struct.unpack('<Q', f.read(8))[0]
            metadata_count = struct.unpack('<Q', f.read(8))[0]
            
            # Parse metadata key-value pairs
            metadata = {}
            for _ in range(metadata_count):
                key = self._read_string(f)
                value_type = struct.unpack('<I', f.read(4))[0]
                value = self._read_value(f, value_type)
                metadata[key] = value
                
            return {
                'file_info': {
                    'path': str(self.file_path),
                    'name': self.file_path.name,
                    'size_bytes': self.file_path.stat().st_size,
                    'modified': datetime.fromtimestamp(
                        self.file_path.stat().st_mtime
                    ).isoformat(),
                },
                'gguf_info': {
                    'version': version,
                    'tensor_count': tensor_count,
                    'metadata_count': metadata_count,
                },
                'metadata': metadata,
            }
            
    def _read_string(self, f) -> str:
        """Read a GGUF string (length-prefixed)"""
        length = struct.unpack('<Q', f.read(8))[0]
        return f.read(length).decode('utf-8')
        
    def _read_value(self, f, value_type: int) -> Any:
        """Read a GGUF value based on its type"""
        if value_type == self.GGUF_TYPE_UINT8:
            return struct.unpack('<B', f.read(1))[0]
        elif value_type == self.GGUF_TYPE_INT8:
            return struct.unpack('<b', f.read(1))[0]
        elif value_type == self.GGUF_TYPE_UINT16:
            return struct.unpack('<H', f.read(2))[0]
        elif value_type == self.GGUF_TYPE_INT16:
            return struct.unpack('<h', f.read(2))[0]
        elif value_type == self.GGUF_TYPE_UINT32:
            return struct.unpack('<I', f.read(4))[0]
        elif value_type == self.GGUF_TYPE_INT32:
            return struct.unpack('<i', f.read(4))[0]
        elif value_type == self.GGUF_TYPE_FLOAT32:
            return struct.unpack('<f', f.read(4))[0]
        elif value_type == self.GGUF_TYPE_UINT64:
            return struct.unpack('<Q', f.read(8))[0]
        elif value_type == self.GGUF_TYPE_INT64:
            return struct.unpack('<q', f.read(8))[0]
        elif value_type == self.GGUF_TYPE_FLOAT64:
            return struct.unpack('<d', f.read(8))[0]
        elif value_type == self.GGUF_TYPE_BOOL:
            return struct.unpack('<?', f.read(1))[0]
        elif value_type == self.GGUF_TYPE_STRING:
            return self._read_string(f)
        elif value_type == self.GGUF_TYPE_ARRAY:
            array_type = struct.unpack('<I', f.read(4))[0]
            array_length = struct.unpack('<Q', f.read(8))[0]
            return [self._read_value(f, array_type) for _ in range(array_length)]
        else:
            raise ValueError(f"Unknown GGUF type: {value_type}")


def parse_blob_directory(blob_dir: str) -> Dict[str, Any]:
    """Parse all GGUF files in a blob directory"""
    blob_path = Path(blob_dir).expanduser()
    
    if not blob_path.exists():
        return {
            'error': f"Directory not found: {blob_path}",
            'models': [],
        }
        
    models = []
    for file_path in blob_path.rglob('*'):
        if file_path.is_file():
            try:
                # Try to parse as GGUF
                parser = GGUFParser(str(file_path))
                metadata = parser.parse()
                models.append(metadata)
            except (ValueError, struct.error):
                # Not a GGUF file or parsing failed - create basic metadata
                models.append({
                    'file_info': {
                        'path': str(file_path),
                        'name': file_path.name,
                        'size_bytes': file_path.stat().st_size,
                        'modified': datetime.fromtimestamp(
                            file_path.stat().st_mtime
                        ).isoformat(),
                    },
                    'type': 'unknown_blob',
                    'note': 'Could not parse as GGUF format',
                })
            except Exception as e:
                models.append({
                    'file_info': {
                        'path': str(file_path),
                        'name': file_path.name,
                    },
                    'error': str(e),
                })
                
    return {
        'swarm_dna_component': 'model_blob_metadata',
        'scan_date': datetime.now().isoformat(),
        'blob_directory': str(blob_path),
        'total_files': len(models),
        'models': models,
    }


def main():
    """CLI interface for GGUF parser"""
    if len(sys.argv) < 2:
        print("Usage: gguf_parser.py <blob_directory> [output.yaml]")
        print()
        print("Examples:")
        print("  gguf_parser.py ~/.ollama/models/blob/")
        print("  gguf_parser.py ~/.ollama/models/blob/ model_metadata.yaml")
        sys.exit(1)
        
    blob_dir = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    print(f"🔍 Scanning blob directory: {blob_dir}")
    result = parse_blob_directory(blob_dir)
    
    print(f"📦 Found {result['total_files']} files")
    
    if output_file:
        with open(output_file, 'w') as f:
            yaml.dump(result, f, default_flow_style=False, sort_keys=False)
        print(f"✅ Metadata written to: {output_file}")
    else:
        print("\n" + "="*60)
        print(yaml.dump(result, default_flow_style=False, sort_keys=False))
        

if __name__ == '__main__':
    main()
