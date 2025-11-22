#!/usr/bin/env python3
"""
Zip File Analyzer for Sovereignty Architecture
Strategickhaos DAO LLC - UPL-Safe File Analysis

Analyzes zip file contents, provides metadata, and validates archive integrity.
"""

import zipfile
import sys
import json
import os
import io
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import hashlib


def format_size(size_bytes: int) -> str:
    """Format bytes to human-readable size"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def get_file_hash(zip_path: str) -> str:
    """Calculate SHA256 hash of the zip file"""
    sha256_hash = hashlib.sha256()
    try:
        with open(zip_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        return f"Error calculating hash: {str(e)}"


def analyze_zip_file(zip_path: str, detailed: bool = False) -> Dict[str, Any]:
    """
    Analyze a zip file and return comprehensive metadata
    
    Args:
        zip_path: Path to the zip file
        detailed: If True, includes detailed per-file analysis
        
    Returns:
        Dictionary containing analysis results
    """
    if not os.path.exists(zip_path):
        return {
            "status": "error",
            "message": f"File not found: {zip_path}",
            "timestamp": datetime.now().isoformat()
        }
    
    if not zipfile.is_zipfile(zip_path):
        return {
            "status": "error",
            "message": f"Not a valid zip file: {zip_path}",
            "timestamp": datetime.now().isoformat()
        }
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Get basic info
            file_list = zip_ref.namelist()
            total_files = len(file_list)
            
            # Analyze contents
            total_compressed_size = 0
            total_uncompressed_size = 0
            file_types = {}
            directories = []
            files = []
            
            for item in zip_ref.infolist():
                total_compressed_size += item.compress_size
                total_uncompressed_size += item.file_size
                
                if item.is_dir():
                    directories.append(item.filename)
                else:
                    # Calculate compression ratio with proper zero handling
                    if item.file_size > 0:
                        compression_ratio = round(
                            (1 - item.compress_size / max(item.file_size, 1)) * 100, 2
                        )
                    else:
                        compression_ratio = 0.0
                    
                    files.append({
                        "filename": item.filename,
                        "compressed_size": item.compress_size,
                        "uncompressed_size": item.file_size,
                        "compression_ratio": compression_ratio,
                        "date_time": datetime(*item.date_time).isoformat(),
                        "crc": item.CRC
                    })
                    
                    # Track file types
                    ext = Path(item.filename).suffix.lower()
                    if ext:
                        file_types[ext] = file_types.get(ext, 0) + 1
                    else:
                        file_types['no_extension'] = file_types.get('no_extension', 0) + 1
            
            # Check for test results
            testinfo = None
            try:
                testinfo = zip_ref.testzip()
            except Exception:
                testinfo = "Unable to test"
            
            # Build analysis result
            analysis = {
                "status": "success",
                "timestamp": datetime.now().isoformat(),
                "file_info": {
                    "path": zip_path,
                    "name": os.path.basename(zip_path),
                    "size": os.path.getsize(zip_path),
                    "size_formatted": format_size(os.path.getsize(zip_path)),
                    "hash_sha256": get_file_hash(zip_path)
                },
                "archive_info": {
                    "total_files": total_files,
                    "total_directories": len(directories),
                    "file_count": len(files),
                    "total_compressed_size": total_compressed_size,
                    "total_compressed_size_formatted": format_size(total_compressed_size),
                    "total_uncompressed_size": total_uncompressed_size,
                    "total_uncompressed_size_formatted": format_size(total_uncompressed_size),
                    "compression_ratio": round(
                        (1 - total_compressed_size / total_uncompressed_size) * 100 
                        if total_uncompressed_size > 0 else 0, 2
                    ),
                    "integrity_check": "PASSED" if testinfo is None else f"FAILED: {testinfo}",
                    "file_types": file_types
                }
            }
            
            if detailed:
                analysis["files"] = files
                analysis["directories"] = directories
            
            return analysis
            
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error analyzing zip file: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }


def print_analysis_report(analysis: Dict[str, Any], format_type: str = "text"):
    """Print analysis report in specified format"""
    
    if analysis["status"] == "error":
        print(f"❌ ERROR: {analysis['message']}")
        return
    
    if format_type == "json":
        print(json.dumps(analysis, indent=2))
        return
    
    # Text format
    print("\n" + "="*70)
    print("📦 ZIP FILE ANALYSIS REPORT")
    print("="*70)
    print(f"\n🕒 Analysis Time: {analysis['timestamp']}")
    
    file_info = analysis['file_info']
    print(f"\n📄 File Information:")
    print(f"   Name: {file_info['name']}")
    print(f"   Path: {file_info['path']}")
    print(f"   Size: {file_info['size_formatted']}")
    print(f"   SHA256: {file_info['hash_sha256']}")
    
    archive_info = analysis['archive_info']
    print(f"\n📊 Archive Contents:")
    print(f"   Total Entries: {archive_info['total_files']}")
    print(f"   Files: {archive_info['file_count']}")
    print(f"   Directories: {archive_info['total_directories']}")
    print(f"   Compressed Size: {archive_info['total_compressed_size_formatted']}")
    print(f"   Uncompressed Size: {archive_info['total_uncompressed_size_formatted']}")
    print(f"   Compression Ratio: {archive_info['compression_ratio']}%")
    print(f"   Integrity Check: {archive_info['integrity_check']}")
    
    print(f"\n📑 File Types Distribution:")
    for ext, count in sorted(archive_info['file_types'].items(), key=lambda x: x[1], reverse=True):
        ext_display = ext if ext != 'no_extension' else '[no extension]'
        print(f"   {ext_display}: {count} file(s)")
    
    if 'files' in analysis:
        print(f"\n📋 Detailed File List:")
        for file in analysis['files']:
            print(f"\n   • {file['filename']}")
            print(f"     Size: {format_size(file['uncompressed_size'])} "
                  f"(compressed: {format_size(file['compressed_size'])}, "
                  f"ratio: {file['compression_ratio']}%)")
            print(f"     Modified: {file['date_time']}")
            print(f"     CRC32: {hex(file['crc'])}")
    
    print("\n" + "="*70)
    print("✅ Analysis Complete")
    print("="*70 + "\n")


def main():
    """Main entry point for the script"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Analyze zip file contents and metadata",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s files.zip
  %(prog)s -d files.zip
  %(prog)s -f json files.zip > analysis.json
  %(prog)s -d -f json files.zip
        """
    )
    
    parser.add_argument(
        'zip_file',
        help='Path to the zip file to analyze'
    )
    
    parser.add_argument(
        '-d', '--detailed',
        action='store_true',
        help='Include detailed per-file analysis'
    )
    
    parser.add_argument(
        '-f', '--format',
        choices=['text', 'json'],
        default='text',
        help='Output format (default: text)'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Save analysis to file instead of printing to stdout'
    )
    
    args = parser.parse_args()
    
    # Analyze the zip file
    print(f"🔍 Analyzing: {args.zip_file}...", file=sys.stderr)
    analysis = analyze_zip_file(args.zip_file, detailed=args.detailed)
    
    # Output results
    if args.output:
        try:
            output_path = Path(args.output)
            # Only create parent directory if path contains directories
            if output_path.parent != Path('.'):
                output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w') as f:
                if args.format == 'json':
                    json.dump(analysis, f, indent=2)
                else:
                    # Redirect print to file
                    string_buffer = io.StringIO()
                    original_stdout = sys.stdout
                    sys.stdout = string_buffer
                    print_analysis_report(analysis, args.format)
                    sys.stdout = original_stdout
                    f.write(string_buffer.getvalue())
            
            print(f"✅ Analysis saved to: {output_path}", file=sys.stderr)
        except Exception as e:
            print(f"❌ Error saving output file: {str(e)}", file=sys.stderr)
            sys.exit(1)
    else:
        print_analysis_report(analysis, args.format)
    
    # Exit with appropriate code
    sys.exit(0 if analysis['status'] == 'success' else 1)


if __name__ == "__main__":
    main()
